"""SimPy 4.1.2 discrete-event simulator for Track A (Cluster P/D) and Track B (Serverless).

All outputs are parameterized discrete-event simulation results grounded in
`parameter_sources.json`, `DESIGN.md`, and local CC-BY-4.0 traces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math
import numpy as np
import simpy

from sim_config import (
    ClusterConfig,
    GPUProfile,
    GPU_PROFILES,
    HostProfile,
    REGIONS,
    SERVERLESS_COLD_START_S,
    SLOT_SECONDS,
    SLO_CONFIGS,
    ServerlessConfig,
    HOURS_PER_YEAR,
    load_greensku_host_profile,
    wan_rtt_ms,
)
from trace_loader import (
    CarbonSeriesBundle,
    RequestStream,
    build_carbon_bundle,
    build_request_stream,
)


def integrate_carbon(
    ci_array: np.ndarray,
    t0: float,
    t1: float,
    power_w: float,
    pue: float,
) -> Tuple[float, float]:
    """Integrate exact energy (kWh) and operational carbon (gCO2eq) over [t0, t1].

    Splits intervals cleanly at every 30-minute (1800 s) carbon intensity boundary.
    """
    if t1 <= t0 or power_w <= 0.0:
        return 0.0, 0.0
    total_kwh = 0.0
    total_g = 0.0
    cur = t0
    n_slots = len(ci_array)
    while cur < t1 - 1e-12:
        slot = min(int(cur // SLOT_SECONDS), n_slots - 1)
        next_boundary = (slot + 1) * SLOT_SECONDS
        seg_end = min(t1, next_boundary) if slot < n_slots - 1 else t1
        dt = seg_end - cur
        kwh = (power_w / 1000.0) * (dt / 3600.0) * pue
        total_kwh += kwh
        total_g += kwh * float(ci_array[slot])
        cur = seg_end
    return total_kwh, total_g


def ci_at(ci_array: np.ndarray, t: float) -> float:
    slot = min(max(int(t // SLOT_SECONDS), 0), len(ci_array) - 1)
    return float(ci_array[slot])


def ci_lookahead_avg(ci_array: np.ndarray, t: float, window_s: float = 1800.0) -> float:
    s0 = min(max(int(t // SLOT_SECONDS), 0), len(ci_array) - 1)
    s1 = min(max(int((t + window_s) // SLOT_SECONDS), s0), len(ci_array) - 1)
    return float(np.mean(ci_array[s0 : s1 + 1]))


# ==============================================================================
# TRACK A: Multi-Region Phase-Disaggregated Cluster Simulation
# ==============================================================================


@dataclass
class ActiveDecodeReq:
    req_id: int
    ctx_tokens: int
    rem_tokens: float
    gen_done: float
    total_out: int
    decode_enter_t: float
    done_event: simpy.Event
    tpot_ms_out: List[float]  # single-element mutable holder


class ClusterNode:
    """Represents one 4-GPU or 8-GPU LLM serving node (colocated, prefill, or decode)."""

    def __init__(
        self,
        env: simpy.Environment,
        node_id: str,
        region: str,
        role: str,  # "colocated", "prefill", "decode"
        gpu: GPUProfile,
        host: HostProfile,
        c_cap: float,
        cfg: ClusterConfig,
        actual_ci: np.ndarray,
    ) -> None:
        self.env = env
        self.node_id = node_id
        self.region = region
        self.role = role
        self.gpu = gpu
        self.host = host
        self.c_cap = c_cap
        self.cfg = cfg
        self.actual_ci = actual_ci
        self.pue = cfg.pue

        self.max_batch = (
            gpu.decode_max_batch_coloc if role == "colocated" else gpu.decode_max_batch_disagg
        )
        self.prefill_res = simpy.Resource(env, capacity=1)
        self.pending_prefill_s: float = 0.0

        # Decode continuous-batching state
        self.active_decode: List[ActiveDecodeReq] = []
        self.decode_wait_queue: List[ActiveDecodeReq] = []
        self.active_prefill_tokens: int = 0
        self.is_prefilling: bool = False

        # Accounting accumulators
        self.last_t: float = 0.0
        self.energy_prefill_kwh: float = 0.0
        self.energy_decode_kwh: float = 0.0
        self.energy_idle_kwh: float = 0.0
        self.carbon_prefill_g: float = 0.0
        self.carbon_decode_g: float = 0.0
        self.carbon_idle_g: float = 0.0
        self.busy_s: float = 0.0
        self.weighted_util_s: float = 0.0

        self._wake_event: simpy.Event = env.event()
        self.decode_proc = env.process(self._decode_loop())

    @property
    def total_decode_load(self) -> int:
        return len(self.active_decode) + len(self.decode_wait_queue)

    @property
    def load_fraction(self) -> float:
        if self.role == "prefill":
            return min(2.0, self.pending_prefill_s / 0.25)
        return self.total_decode_load / float(self.max_batch)

    def estimate_decode_wait_s(self) -> float:
        n_q = len(self.decode_wait_queue)
        if self.total_decode_load < self.max_batch:
            return 0.0
        # Average remaining output ~ 100 tokens * t_step / max_batch
        step_s = self.gpu.decode_step_ms / 1000.0
        return (n_q + 1) * (100.0 * step_s / max(1, self.max_batch))

    def _current_t_step_s(self) -> float:
        if not self.active_decode:
            return self.gpu.decode_step_ms / 1000.0
        k_res_tok = sum(r.ctx_tokens + r.gen_done for r in self.active_decode)
        k_res_gb = k_res_tok * self.cfg.kv_mb_per_tok / 1024.0
        agg_hbm_bw = self.gpu.hbm_bw_gbps * self.gpu.gpus_per_replica
        step_ms = self.gpu.decode_step_ms * (
            1.0 + self.gpu.alpha_mem * (k_res_gb / max(agg_hbm_bw, 1.0))
        )
        # Splitwise Fig. 8-9: decode unaffected down to 0.50 TDP cap; minor penalty below 0.50
        if self.c_cap < 0.50:
            step_ms *= 1.0 + 0.6 * (0.50 - self.c_cap)
        return max(self.gpu.decode_step_ms, step_ms) / 1000.0

    def _current_power_and_phase(self) -> Tuple[float, str]:
        """Compute instantaneous node power (W) using Ozcan sublinear MFU + GreenSKU host."""
        n_dec = len(self.active_decode)
        if self.is_prefilling:
            mfu = min(
                self.cfg.mfu_sat,
                0.28 + 0.17 * min(1.0, self.active_prefill_tokens / 1024.0),
            )
            if n_dec > 0:
                mfu = min(self.cfg.mfu_sat, mfu + 0.04)
            cap = 1.0
            phase = "prefill"
        elif n_dec > 0:
            mfu = min(self.cfg.mfu_sat, 0.03 + 0.22 * (n_dec / float(self.max_batch)))
            cap = self.c_cap
            phase = "decode"
        else:
            mfu = 0.0
            cap = self.c_cap
            phase = "idle"

        if mfu <= 0.0:
            p_gpu = self.gpu.idle_w
            p_host = self.host.idle_power_w
        else:
            p_max_eff = min(self.gpu.tdp_w, cap * self.gpu.tdp_w)
            ratio = min(1.0, mfu / self.cfg.mfu_sat) ** self.cfg.mfu_gamma
            p_gpu = self.gpu.idle_w + max(0.0, p_max_eff - self.gpu.idle_w) * ratio
            p_host = self.host.idle_power_w + (
                self.host.peak_power_w - self.host.idle_power_w
            ) * ratio

        total_w = self.gpu.gpus_per_replica * p_gpu + p_host
        return total_w, phase

    def _advance_to(self, t_now: float) -> None:
        if t_now <= self.last_t:
            return
        dt = t_now - self.last_t
        power_w, phase = self._current_power_and_phase()
        kwh, g_co2 = integrate_carbon(self.actual_ci, self.last_t, t_now, power_w, self.pue)

        if phase == "prefill":
            self.energy_prefill_kwh += kwh
            self.carbon_prefill_g += g_co2
            self.busy_s += dt
            self.weighted_util_s += dt
        elif phase == "decode":
            self.energy_decode_kwh += kwh
            self.carbon_decode_g += g_co2
            self.busy_s += dt
            self.weighted_util_s += dt * (len(self.active_decode) / float(self.max_batch))
        else:
            self.energy_idle_kwh += kwh
            self.carbon_idle_g += g_co2

        if self.active_decode:
            t_step = self._current_t_step_s()
            # Colocated prefill steals SM cycles from concurrent decode iterations
            decode_rate = self.cfg.coloc_decode_rate if self.is_prefilling else 1.0
            tok_adv = (dt / t_step) * decode_rate
            still_active: List[ActiveDecodeReq] = []
            for req in self.active_decode:
                req.rem_tokens -= tok_adv
                req.gen_done += tok_adv
                if req.rem_tokens <= 1e-6:
                    tpot_ms = max(
                        self.gpu.decode_step_ms,
                        (t_now - req.decode_enter_t) * 1000.0 / max(1, req.total_out),
                    )
                    req.tpot_ms_out.append(tpot_ms)
                    if not req.done_event.triggered:
                        req.done_event.succeed()
                else:
                    still_active.append(req)
            self.active_decode = still_active
            while self.decode_wait_queue and len(self.active_decode) < self.max_batch:
                self.active_decode.append(self.decode_wait_queue.pop(0))

        self.last_t = t_now

    def _interrupt_worker(self) -> None:
        if not self._wake_event.triggered:
            self._wake_event.succeed()
        elif self.decode_proc.is_alive and self.env.active_process != self.decode_proc:
            try:
                self.decode_proc.interrupt()
            except RuntimeError:
                pass

    def start_prefill(self, ctx_tokens: int) -> None:
        self._advance_to(self.env.now)
        self.is_prefilling = True
        self.active_prefill_tokens = ctx_tokens
        self._interrupt_worker()

    def end_prefill(self) -> None:
        self._advance_to(self.env.now)
        self.is_prefilling = False
        self.active_prefill_tokens = 0
        self._interrupt_worker()

    def submit_decode(self, req: ActiveDecodeReq) -> None:
        self._advance_to(self.env.now)
        if len(self.active_decode) < self.max_batch:
            self.active_decode.append(req)
        else:
            self.decode_wait_queue.append(req)
        self._interrupt_worker()

    def flush(self, t_end: float) -> None:
        self._advance_to(t_end)

    def _decode_loop(self) -> simpy.events.Event:
        while True:
            if not self.active_decode:
                self._wake_event = self.env.event()
                try:
                    yield self._wake_event
                except simpy.Interrupt:
                    pass
                self._advance_to(self.env.now)
                continue

            t_step = self._current_t_step_s()
            decode_rate = self.cfg.coloc_decode_rate if self.is_prefilling else 1.0
            min_rem = min(r.rem_tokens for r in self.active_decode)
            next_dt = max(1e-6, min_rem * (t_step / max(decode_rate, 1e-4)))
            try:
                yield self.env.timeout(next_dt)
            except simpy.Interrupt:
                pass
            self._advance_to(self.env.now)

    def amortized_embodied_g(self, total_sim_s: float) -> float:
        """EcoServe / GreenSKU amortized embodied carbon (gCO2eq) over simulation horizon."""
        t_hr = total_sim_s / 3600.0
        host_lt_hr = self.cfg.host_lifetime_yr * HOURS_PER_YEAR
        gpu_lt_hr = self.cfg.gpu_lifetime_yr * HOURS_PER_YEAR
        host_g = (self.host.embodied_kgco2e * 1000.0 / host_lt_hr) * t_hr
        gpu_g = (
            self.gpu.gpus_per_replica * self.gpu.embodied_kgco2e * 1000.0 / gpu_lt_hr
        ) * t_hr
        return host_g + gpu_g


def _effective_rtt_ms(r1: str, r2: str, cfg: ClusterConfig) -> float:
    """Return intra-DC RTT if r1 == r2, optional override if set, or calibrated regional WAN RTT."""
    if r1 == r2:
        return 0.5
    if cfg.wan_rtt_override_ms is not None:
        return float(cfg.wan_rtt_override_ms)
    return wan_rtt_ms(r1, r2)


class ClusterRouter:
    """Implements B1, B2, P3, P4, P5, and P3_overprov routing policies."""

    def __init__(
        self,
        cfg: ClusterConfig,
        slo_cfg,
        carbon_bundle: CarbonSeriesBundle,
        prefill_pools: Dict[str, List[ClusterNode]],
        decode_pools: Dict[str, List[ClusterNode]],
    ) -> None:
        self.cfg = cfg
        self.slo_cfg = slo_cfg
        self.carbon = carbon_bundle
        self.prefill_pools = prefill_pools
        self.decode_pools = decode_pools
        self.ewma_l_out = 150.0  # Causal running estimate of L_out (never peeks at L_out)

    def update_l_out_ewma(self, observed_l_out: int) -> None:
        self.ewma_l_out = 0.98 * self.ewma_l_out + 0.02 * float(observed_l_out)

    def _get_ci(self, region: str, t: float) -> float:
        if self.cfg.policy == "P5":
            return ci_lookahead_avg(self.carbon.actual_ci[region], t, 1800.0)
        return ci_at(self.carbon.observed_ci[region], t)

    def _best_p_node(self, region: str) -> ClusterNode:
        return min(self.prefill_pools[region], key=lambda n: n.pending_prefill_s)

    def _best_d_node(self, region: str) -> ClusterNode:
        return min(self.decode_pools[region], key=lambda n: n.total_decode_load)

    def _estimate_exec_energy_kwh(
        self, p_node: ClusterNode, d_node: ClusterNode, l_in: int, l_out_est: float
    ) -> Tuple[float, float]:
        t_p_s = (p_node.gpu.prefill_base_ms + l_in * p_node.gpu.prefill_ms_per_tok) / 1000.0
        mfu_p = min(self.cfg.mfu_sat, 0.28 + 0.17 * min(1.0, l_in / 1024.0))
        r_p = (mfu_p / self.cfg.mfu_sat) ** self.cfg.mfu_gamma
        p_w = p_node.gpu.gpus_per_replica * (
            p_node.gpu.idle_w + (p_node.gpu.tdp_w - p_node.gpu.idle_w) * r_p
        ) + (p_node.host.idle_power_w + (p_node.host.peak_power_w - p_node.host.idle_power_w) * r_p)
        e_p_kwh = (p_w / 1000.0) * (t_p_s / 3600.0) * self.cfg.pue

        # Marginal decode energy amortized across concurrent batch
        t_d_s = l_out_est * (d_node.gpu.decode_step_ms / 1000.0)
        b_est = max(1, d_node.total_decode_load + 1)
        mfu_d = min(self.cfg.mfu_sat, 0.03 + 0.22 * (min(b_est, d_node.max_batch) / float(d_node.max_batch)))
        r_d = (mfu_d / self.cfg.mfu_sat) ** self.cfg.mfu_gamma
        p_cap_eff = min(d_node.gpu.tdp_w, d_node.c_cap * d_node.gpu.tdp_w)
        d_w = d_node.gpu.gpus_per_replica * (
            d_node.gpu.idle_w + max(0.0, p_cap_eff - d_node.gpu.idle_w) * r_d
        ) + (d_node.host.idle_power_w + (d_node.host.peak_power_w - d_node.host.idle_power_w) * r_d)
        # Incremental marginal share per request in batch
        e_d_kwh = (d_w / 1000.0) * (t_d_s / 3600.0) * self.cfg.pue / float(b_est)
        return e_p_kwh, e_d_kwh

    def select_route(
        self, origin_region: str, l_in: int, t_now: float
    ) -> Tuple[str, ClusterNode, ClusterNode]:
        """Return `(path_label, prefill_node, decode_node)`."""
        policy = self.cfg.policy
        ttft_slo_ms, tpot_slo_ms = self.slo_cfg.thresholds_for_request(l_in, int(self.ewma_l_out))
        regions = self.cfg.regions

        # B1: Carbon-Agnostic Colocated (nearest region, spillover only on saturation)
        if policy == "B1":
            local_n = self._best_p_node(origin_region)
            if local_n.load_fraction < 1.35:
                return "A_coloc", local_n, local_n
            # Spill to nearest RTT neighbor
            best_r = min(regions, key=lambda r: (_effective_rtt_ms(origin_region, r, self.cfg), self._best_p_node(r).load_fraction))
            n = self._best_p_node(best_r)
            return "A_coloc", n, n

        # B2: Carbon-Agnostic Disaggregated (intra-region P/D, nearest spillover on saturation)
        if policy == "B2":
            p_loc = self._best_p_node(origin_region)
            d_loc = self._best_d_node(origin_region)
            if d_loc.load_fraction < 1.35:
                return "B_intra_pd", p_loc, d_loc
            best_r = min(regions, key=lambda r: (_effective_rtt_ms(origin_region, r, self.cfg), self._best_d_node(r).load_fraction))
            return "B_intra_pd", self._best_p_node(best_r), self._best_d_node(best_r)

        # P3 / P3_overprov: Spatiotemporal Carbon-Aware Disaggregated without KV-crossover check
        if policy in ("P3", "P3_overprov"):
            feasible_p = [
                r
                for r in regions
                if _effective_rtt_ms(origin_region, r, self.cfg) + self._best_p_node(r).pending_prefill_s * 1000.0 <= 0.90 * ttft_slo_ms
            ]
            if not feasible_p:
                feasible_p = [origin_region]
            r_p = min(feasible_p, key=lambda r: (self._get_ci(r, t_now), _effective_rtt_ms(origin_region, r, self.cfg)))
            p_node = self._best_p_node(r_p)

            # Naive decode selection: if clean region decode saturates (>55%) OR prompt is
            # latency-sensitive near-user decode, place decode in lowest-CI non-saturated region
            # without checking Sisodia S_kv / BW_wan crossover!
            d_in_rp = self._best_d_node(r_p)
            feasible_d = [
                r
                for r in regions
                if _effective_rtt_ms(r_p, r, self.cfg) + _effective_rtt_ms(r, origin_region, self.cfg) * 0.5 <= 0.90 * ttft_slo_ms
            ]
            if not feasible_d:
                feasible_d = [origin_region]
            if d_in_rp.load_fraction < 0.60 and self.ewma_l_out > 60.0:
                r_d = r_p
            else:
                # Pick lowest CI among non-saturated decode regions (or origin if tight)
                under_cap = [r for r in feasible_d if self._best_d_node(r).load_fraction < 0.85]
                cand_d = under_cap if under_cap else feasible_d
                r_d = min(cand_d, key=lambda r: (self._get_ci(r, t_now) + 150.0 * self._best_d_node(r).load_fraction))
            d_node = self._best_d_node(r_d)
            path = "B_intra_pd" if r_p == r_d else "C_cross_pd"
            return path, p_node, d_node

        # P4 & P5: Carbon+KV-Aware Hybrid Router (4 candidate paths + Sisodia crossover)
        if policy in ("P4", "P5"):
            s_kv_mb = l_in * self.cfg.kv_mb_per_tok
            p_loc = self._best_p_node(origin_region)
            d_loc = self._best_d_node(origin_region)
            e_p_loc, e_d_loc = self._estimate_exec_energy_kwh(p_loc, d_loc, l_in, self.ewma_l_out)
            ci_loc = self._get_ci(origin_region, t_now)
            c_loc_est = (e_p_loc + e_d_loc) * ci_loc

            candidates: List[Tuple[float, str, ClusterNode, ClusterNode]] = []
            margin_ttft = self.cfg.p4_slo_margin * ttft_slo_ms

            # Path A: Intra-region colocated fallback (no KV transfer stall) when prefill
            # bursts saturate the local prefill pool while decode node has spare compute,
            # or when decode node saturates while prefill node has spare HBM.
            t_p_loc_ms = p_loc.gpu.prefill_base_ms + l_in * p_loc.gpu.prefill_ms_per_tok
            ttft_a_on_d = (
                _effective_rtt_ms(origin_region, origin_region, self.cfg)
                + d_loc.pending_prefill_s * 1000.0
                + t_p_loc_ms
            )
            if d_loc.load_fraction < 0.70 and p_loc.pending_prefill_s > 0.12 and ttft_a_on_d <= ttft_slo_ms:
                q_risk_a = self.cfg.p4_w_queue * (d_loc.load_fraction + d_loc.pending_prefill_s)
                candidates.append(
                    (self.cfg.p4_w_carbon * c_loc_est * 1.05 + q_risk_a, "A_coloc", d_loc, d_loc)
                )
            elif d_loc.load_fraction > 0.90:
                ttft_a_on_p = (
                    _effective_rtt_ms(origin_region, origin_region, self.cfg)
                    + p_loc.pending_prefill_s * 1000.0
                    + t_p_loc_ms
                )
                if ttft_a_on_p <= ttft_slo_ms:
                    q_risk_a = self.cfg.p4_w_queue * (p_loc.load_fraction ** 2)
                    candidates.append(
                        (self.cfg.p4_w_carbon * c_loc_est * 1.15 + q_risk_a, "A_coloc", p_loc, p_loc)
                    )

            # Path B (origin) & Path D (remote clean-region full intra-DC P/D)
            for r in regions:
                p_n = self._best_p_node(r)
                d_n = self._best_d_node(r)
                t_p_ms = p_n.gpu.prefill_base_ms + l_in * p_n.gpu.prefill_ms_per_tok
                t_kv_local_ms = d_n.gpu.kv_stall_ms + (s_kv_mb * 8.0) / self.cfg.intra_dc_kv_bw_gbps
                ttft_bd = _effective_rtt_ms(origin_region, r, self.cfg) + p_n.pending_prefill_s * 1000.0 + t_p_ms + t_kv_local_ms
                t_d_wait_ms = d_n.estimate_decode_wait_s() * 1000.0
                est_tpot = d_n.gpu.decode_step_ms + t_d_wait_ms / max(1.0, self.ewma_l_out)

                if ttft_bd <= margin_ttft and est_tpot <= 0.95 * tpot_slo_ms:
                    e_p, e_d = self._estimate_exec_energy_kwh(p_n, d_n, l_in, self.ewma_l_out)
                    ci_r = self._get_ci(r, t_now)
                    c_op_est = (e_p + e_d) * ci_r
                    # Marginal risk penalty activates only as pool nears saturation (>60% load)
                    occ = d_n.load_fraction
                    q_risk = self.cfg.p4_w_queue * (max(0.0, occ - 0.60) ** 2 * 40.0)
                    path_lbl = "B_intra_pd" if r == origin_region else "D_remote_pd"
                    candidates.append((self.cfg.p4_w_carbon * c_op_est + q_risk, path_lbl, p_n, d_n))

            # Path C: Cross-region P/D with pipelined KV transfer (Carbon-Extended Sisodia Crossover)
            for r_p in regions:
                p_n = self._best_p_node(r_p)
                ci_p = self._get_ci(r_p, t_now)
                t_p_ms = p_n.gpu.prefill_base_ms + l_in * p_n.gpu.prefill_ms_per_tok
                for r_d in regions:
                    if r_d == r_p:
                        continue
                    d_n = self._best_d_node(r_d)
                    ci_d = self._get_ci(r_d, t_now)
                    t_kv_wan_ms = _effective_rtt_ms(r_p, r_d, self.cfg) + (s_kv_mb * 8.0) / self.cfg.wan_bw_gbps
                    # Recompute time on r_d if sent straight to r_d instead of transferring KV
                    t_recompute_ms = d_n.gpu.prefill_base_ms + l_in * p_n.gpu.prefill_ms_per_tok
                    t_qd_rp = self._best_d_node(r_p).estimate_decode_wait_s() * 1000.0
                    t_qd_rd = d_n.estimate_decode_wait_s() * 1000.0

                    # Condition 1 (Sisodia Eq. 1 / Eq. 9 Latency Crossover):
                    if not (t_kv_wan_ms + t_qd_rd < min(t_qd_rp + 1e-6, t_recompute_ms)):
                        continue
                    ttft_c = (
                        0.5 * _effective_rtt_ms(origin_region, r_p, self.cfg)
                        + p_n.pending_prefill_s * 1000.0
                        + t_p_ms
                        + t_kv_wan_ms
                        + 0.5 * _effective_rtt_ms(r_d, origin_region, self.cfg)
                    )
                    if ttft_c > margin_ttft:
                        continue

                    # Condition 2 (Carbon-Extended Marginal Cost Crossover):
                    e_p, e_d = self._estimate_exec_energy_kwh(p_n, d_n, l_in, self.ewma_l_out)
                    tx_s = (s_kv_mb * 8.0) / (self.cfg.wan_bw_gbps * 1000.0)
                    pue_avg = self.cfg.pue
                    e_kv_kwh = (self.cfg.nic_net_wan_power_w / 1000.0) * (tx_s / 3600.0) * pue_avg
                    ci_path = 0.5 * (ci_p + ci_d)
                    c_c_est = e_p * ci_p + e_kv_kwh * ci_path + e_d * ci_d
                    if c_c_est >= c_loc_est:
                        continue
                    occ = d_n.load_fraction
                    q_risk = self.cfg.p4_w_queue * (max(0.0, occ - 0.60) ** 2 * 40.0)
                    candidates.append((self.cfg.p4_w_carbon * c_c_est + q_risk, "C_cross_pd", p_n, d_n))

            if candidates:
                _, best_path, best_p, best_d = min(candidates, key=lambda x: x[0])
                return best_path, best_p, best_d

            # Strict SLO margin unachievable (extreme load/strict SLO): pick lowest-latency local P/D
            if ttft_slo_ms <= 150.0:
                return "A_coloc", p_loc, p_loc
            return "B_intra_pd", p_loc, d_loc

        raise ValueError(f"Unknown cluster policy '{policy}'")


def run_cluster_simulation(cfg: ClusterConfig) -> Dict[str, float]:
    """Run one complete SimPy Track A cluster simulation and return summary metrics."""
    stream = build_request_stream(
        cfg.workload, cfg.horizon, cfg.regions, cfg.seed, rps_scale=cfg.rps_scale
    )
    carbon = build_carbon_bundle(cfg.regions, cfg.horizon, cfg.seed, ci_mode=cfg.ci_mode)
    slo_cfg = SLO_CONFIGS[cfg.slo_name]
    host_prof = load_greensku_host_profile()

    env = simpy.Environment()
    prefill_pools: Dict[str, List[ClusterNode]] = {r: [] for r in cfg.regions}
    decode_pools: Dict[str, List[ClusterNode]] = {r: [] for r in cfg.regions}
    all_nodes: List[ClusterNode] = []

    p_gpu = GPU_PROFILES[cfg.prefill_gpu_type]
    d_gpu = GPU_PROFILES[cfg.decode_gpu_type]

    for r in cfg.regions:
        ci_arr = carbon.actual_ci[r]
        if cfg.policy == "B1":
            for k in range(cfg.nodes_per_region):
                node = ClusterNode(
                    env, f"{r}-coloc-{k}", r, "colocated", p_gpu, host_prof, 1.0, cfg, ci_arr
                )
                prefill_pools[r].append(node)
                decode_pools[r].append(node)
                all_nodes.append(node)
        else:
            n_p = max(1, cfg.nodes_per_region // 2)
            n_d = max(1, cfg.nodes_per_region - n_p)
            extra = cfg.clean_scaleout_extra_nodes if (cfg.clean_scaleout_extra_nodes > 0 and r == cfg.regions[0]) else 0
            for k in range(n_p + extra // 2):
                node = ClusterNode(
                    env, f"{r}-prefill-{k}", r, "prefill", p_gpu, host_prof, 1.0, cfg, ci_arr
                )
                prefill_pools[r].append(node)
                all_nodes.append(node)
            for k in range(n_d + (extra - extra // 2)):
                node = ClusterNode(
                    env,
                    f"{r}-decode-{k}",
                    r,
                    "decode",
                    d_gpu,
                    host_prof,
                    cfg.decode_power_cap,
                    cfg,
                    ci_arr,
                )
                decode_pools[r].append(node)
                all_nodes.append(node)

    # Directed WAN KV-transfer bottleneck links per region pair
    wan_links: Dict[Tuple[str, str], simpy.Resource] = {
        (r1, r2): simpy.Resource(env, capacity=1)
        for r1 in cfg.regions
        for r2 in cfg.regions
        if r1 != r2
    }

    router = ClusterRouter(cfg, slo_cfg, carbon, prefill_pools, decode_pools)

    n_req = len(stream.arrival_times_s)
    ttfts_ms = np.empty(n_req, dtype=np.float64)
    tpots_ms = np.empty(n_req, dtype=np.float64)
    slo_ttft_viol = np.zeros(n_req, dtype=np.int8)
    slo_tpot_viol = np.zeros(n_req, dtype=np.int8)
    path_counts = {"A_coloc": 0, "B_intra_pd": 0, "C_cross_pd": 0, "D_remote_pd": 0}

    kv_wan_gb = 0.0
    kv_wan_energy_kwh = 0.0
    kv_wan_carbon_g = 0.0
    kv_local_energy_kwh = 0.0
    kv_local_carbon_g = 0.0
    tokens_by_region: Dict[str, float] = {r: 0.0 for r in cfg.regions}

    in_flight = 0
    feeder_done = False
    all_done_ev = env.event()

    def handle_request(idx: int, arr_t: float, l_in: int, l_out: int, origin_r: str):
        nonlocal kv_wan_gb, kv_wan_energy_kwh, kv_wan_carbon_g, kv_local_energy_kwh, kv_local_carbon_g, in_flight
        in_flight += 1
        path_lbl, p_node, d_node = router.select_route(origin_r, l_in, arr_t)
        path_counts[path_lbl] += 1

        t_to_p_s = 0.5 * _effective_rtt_ms(origin_r, p_node.region, cfg) / 1000.0
        if t_to_p_s > 0.0:
            yield env.timeout(t_to_p_s)

        t_exec_p_s = (p_node.gpu.prefill_base_ms + l_in * p_node.gpu.prefill_ms_per_tok) / 1000.0
        p_node.pending_prefill_s += t_exec_p_s
        with p_node.prefill_res.request() as preq:
            yield preq
            p_node.start_prefill(l_in)
            yield env.timeout(t_exec_p_s)
            p_node.end_prefill()
        p_node.pending_prefill_s = max(0.0, p_node.pending_prefill_s - t_exec_p_s)

        # KV transfer phase
        s_kv_mb = l_in * cfg.kv_mb_per_tok
        if path_lbl != "A_coloc":
            if p_node.region == d_node.region:
                t_kv_s = (d_node.gpu.kv_stall_ms / 1000.0) + (s_kv_mb * 8.0) / (
                    cfg.intra_dc_kv_bw_gbps * 1000.0
                )
                e_kv = (cfg.nic_net_local_power_w / 1000.0) * (t_kv_s / 3600.0) * cfg.pue
                c_kv = e_kv * ci_at(carbon.actual_ci[p_node.region], env.now)
                kv_local_energy_kwh += e_kv
                kv_local_carbon_g += c_kv
                yield env.timeout(t_kv_s)
            else:
                rtt_s = _effective_rtt_ms(p_node.region, d_node.region, cfg) / 1000.0
                tx_s = (s_kv_mb * 8.0) / (cfg.wan_bw_gbps * 1000.0)
                yield env.timeout(rtt_s)
                with wan_links[(p_node.region, d_node.region)].request() as wreq:
                    yield wreq
                    yield env.timeout(tx_s)
                pue_avg = cfg.pue
                e_kv = (cfg.nic_net_wan_power_w / 1000.0) * (tx_s / 3600.0) * pue_avg
                ci_avg = 0.5 * (
                    ci_at(carbon.actual_ci[p_node.region], env.now)
                    + ci_at(carbon.actual_ci[d_node.region], env.now)
                )
                kv_wan_gb += s_kv_mb / 1024.0
                kv_wan_energy_kwh += e_kv
                kv_wan_carbon_g += e_kv * ci_avg

        t_ret_s = 0.5 * _effective_rtt_ms(d_node.region, origin_r, cfg) / 1000.0
        ttft_ms = (env.now + t_ret_s - arr_t) * 1000.0
        ttfts_ms[idx] = ttft_ms

        done_ev = env.event()
        tpot_holder: List[float] = []
        d_req = ActiveDecodeReq(
            req_id=idx,
            ctx_tokens=l_in,
            rem_tokens=float(l_out),
            gen_done=0.0,
            total_out=l_out,
            decode_enter_t=env.now,
            done_event=done_ev,
            tpot_ms_out=tpot_holder,
        )
        d_node.submit_decode(d_req)
        yield done_ev

        tpot_ms = tpot_holder[0]
        tpots_ms[idx] = tpot_ms
        router.update_l_out_ewma(l_out)

        ttft_thr, tpot_thr = slo_cfg.thresholds_for_request(l_in, l_out)
        if ttft_ms > ttft_thr:
            slo_ttft_viol[idx] = 1
        if tpot_ms > tpot_thr:
            slo_tpot_viol[idx] = 1

        tot_r_tok = float(l_in + l_out)
        if p_node.region == d_node.region:
            tokens_by_region[p_node.region] += tot_r_tok
        else:
            tokens_by_region[p_node.region] += float(l_in)
            tokens_by_region[d_node.region] += float(l_out)

        in_flight -= 1
        if feeder_done and in_flight == 0 and not all_done_ev.triggered:
            all_done_ev.succeed()

    def feeder():
        nonlocal feeder_done
        prev_t = 0.0
        for idx in range(n_req):
            t_arr = float(stream.arrival_times_s[idx])
            if t_arr > prev_t:
                yield env.timeout(t_arr - prev_t)
                prev_t = t_arr
            env.process(
                handle_request(
                    idx,
                    t_arr,
                    int(stream.context_tokens[idx]),
                    int(stream.generated_tokens[idx]),
                    cfg.regions[int(stream.origin_region_idx[idx])],
                )
            )
        feeder_done = True
        if in_flight == 0 and not all_done_ev.triggered:
            all_done_ev.succeed()

    env.process(feeder())
    env.run(until=all_done_ev)
    t_sim_end = max(stream.duration_s, env.now)
    for node in all_nodes:
        node.flush(t_sim_end)

    # Aggregate operational & embodied carbon across all nodes + KV links
    op_prefill_g = sum(n.carbon_prefill_g for n in all_nodes)
    op_decode_g = sum(n.carbon_decode_g for n in all_nodes)
    op_idle_g = sum(n.carbon_idle_g for n in all_nodes)
    op_carbon_g = op_prefill_g + op_decode_g + op_idle_g + kv_wan_carbon_g + kv_local_carbon_g
    emb_carbon_g = sum(n.amortized_embodied_g(t_sim_end) for n in all_nodes)

    e_prefill_kwh = sum(n.energy_prefill_kwh for n in all_nodes)
    e_decode_kwh = sum(n.energy_decode_kwh for n in all_nodes)
    e_idle_kwh = sum(n.energy_idle_kwh for n in all_nodes)
    e_kv_kwh = kv_wan_energy_kwh + kv_local_energy_kwh
    total_kwh = e_prefill_kwh + e_decode_kwh + e_idle_kwh + e_kv_kwh

    total_ctx = float(np.sum(stream.context_tokens))
    total_gen = float(np.sum(stream.generated_tokens))
    total_tok = total_ctx + total_gen
    tok_1k = total_tok / 1000.0
    gen_1k = total_gen / 1000.0

    slo_any_viol = np.logical_or(slo_ttft_viol > 0, slo_tpot_viol > 0)
    gpu_util_pct = 100.0 * sum(n.weighted_util_s for n in all_nodes) / (len(all_nodes) * t_sim_end)
    gpu_active_time_pct = 100.0 * sum(n.busy_s for n in all_nodes) / (len(all_nodes) * t_sim_end)

    # Regional lifecycle breakdown (for H4 clean vs dirty embodied dominance)
    reg_emb_share: Dict[str, float] = {}
    for r in cfg.regions:
        r_nodes = [n for n in all_nodes if n.region == r]
        r_op_g = sum(n.carbon_prefill_g + n.carbon_decode_g + n.carbon_idle_g for n in r_nodes)
        r_emb_g = sum(n.amortized_embodied_g(t_sim_end) for n in r_nodes)
        reg_emb_share[r] = 100.0 * r_emb_g / max(r_op_g + r_emb_g, 1e-9)

    clean_r = cfg.regions[0]
    dirty_r = cfg.regions[-1]

    return {
        "n_requests": float(n_req),
        "sim_duration_s": float(t_sim_end),
        "total_tokens": total_tok,
        "total_gen_tokens": total_gen,
        "op_carbon_g": op_carbon_g,
        "emb_carbon_g": emb_carbon_g,
        "tot_carbon_g": op_carbon_g + emb_carbon_g,
        "sci_op_g_per_1k_tok": op_carbon_g / tok_1k,
        "sci_emb_g_per_1k_tok": emb_carbon_g / tok_1k,
        "sci_tot_g_per_1k_tok": (op_carbon_g + emb_carbon_g) / tok_1k,
        "sci_op_g_per_1k_gen": op_carbon_g / gen_1k,
        "sci_tot_g_per_1k_gen": (op_carbon_g + emb_carbon_g) / gen_1k,
        "embodied_share_pct": 100.0 * emb_carbon_g / max(op_carbon_g + emb_carbon_g, 1e-9),
        "clean_region_emb_share_pct": reg_emb_share[clean_r],
        "dirty_region_emb_share_pct": reg_emb_share[dirty_r],
        "total_energy_kwh": total_kwh,
        "j_per_tok": (total_kwh * 3.6e6) / total_tok,
        "energy_prefill_pct": 100.0 * e_prefill_kwh / max(total_kwh, 1e-9),
        "energy_decode_pct": 100.0 * e_decode_kwh / max(total_kwh, 1e-9),
        "energy_idle_pct": 100.0 * e_idle_kwh / max(total_kwh, 1e-9),
        "energy_kv_pct": 100.0 * e_kv_kwh / max(total_kwh, 1e-9),
        "ttft_mean_ms": float(np.mean(ttfts_ms)),
        "ttft_p90_ms": float(np.percentile(ttfts_ms, 90)),
        "ttft_p95_ms": float(np.percentile(ttfts_ms, 95)),
        "ttft_p99_ms": float(np.percentile(ttfts_ms, 99)),
        "tpot_mean_ms": float(np.mean(tpots_ms)),
        "tpot_p90_ms": float(np.percentile(tpots_ms, 90)),
        "tpot_p95_ms": float(np.percentile(tpots_ms, 95)),
        "tpot_p99_ms": float(np.percentile(tpots_ms, 99)),
        "slo_viol_pct": float(100.0 * np.mean(slo_any_viol)),
        "slo_ttft_viol_pct": float(100.0 * np.mean(slo_ttft_viol)),
        "slo_tpot_viol_pct": float(100.0 * np.mean(slo_tpot_viol)),
        "gpu_util_pct": gpu_util_pct,
        "gpu_active_time_pct": gpu_active_time_pct,
        "kv_wan_gb_per_1k_req": kv_wan_gb / (n_req / 1000.0),
        "path_coloc_pct": 100.0 * path_counts["A_coloc"] / n_req,
        "path_intra_pd_pct": 100.0 * path_counts["B_intra_pd"] / n_req,
        "path_cross_pd_pct": 100.0 * path_counts["C_cross_pd"] / n_req,
        "path_remote_pd_pct": 100.0 * path_counts["D_remote_pd"] / n_req,
    }


# ==============================================================================
# TRACK B: Serverless GPU LLM Serving & Dynamic Carbon-Aware Keep-Alive
# ==============================================================================


class OnlineGapHazardTracker:
    """Strictly causal online EWMA estimator of idle gap survival probabilities p_miss(k)."""

    K_GRID = (1.0, 5.0, 10.0, 30.0, 60.0)

    def __init__(self) -> None:
        # Mild bimodal heavy-tail prior across gap bins [0-1, 1-5, 5-10, 10-30, 30-60, >60]
        self.bin_edges = np.array([1.0, 5.0, 10.0, 30.0, 60.0, 1e9])
        self.bin_midpoints = np.array([0.5, 3.0, 7.5, 20.0, 45.0, 90.0])
        self.probs = np.array([0.35, 0.25, 0.12, 0.12, 0.08, 0.08], dtype=np.float64)
        self.alpha = 0.08

    def observe_gap(self, gap_s: float) -> None:
        if gap_s < 0.05:
            return
        idx = int(np.searchsorted(self.bin_edges, gap_s, side="right"))
        idx = min(idx, len(self.probs) - 1)
        one_hot = np.zeros_like(self.probs)
        one_hot[idx] = 1.0
        self.probs = (1.0 - self.alpha) * self.probs + self.alpha * one_hot
        self.probs /= np.sum(self.probs)

    def choose_keep_alive(
        self,
        ci_g_kwh: float,
        ci_norm: float,
        p_idle_w: float,
        p_cold_w: float,
        t_cold_s: float,
        pue: float,
        ttft_slo_s: float,
        beta_slo: float,
    ) -> float:
        """Select optimal k* in {1, 5, 10, 30, 60} s minimizing idle + cold carbon + SLO risk."""
        c_idle_rate_g_s = (p_idle_w / 1000.0) * (1.0 / 3600.0) * pue * ci_g_kwh
        c_cold_g = (p_cold_w / 1000.0) * (t_cold_s / 3600.0) * pue * ci_g_kwh
        # SLO penalty scales inversely with normalized grid intensity (DESIGN.md Eq. 11)
        slo_pen_g = (
            beta_slo * (1.0 / max(ci_norm, 0.04)) * (1.0 if t_cold_s > ttft_slo_s else 0.25)
        )

        best_k = 10.0
        best_cost = float("inf")
        for k in self.K_GRID:
            e_tau = float(np.sum(self.probs * np.minimum(self.bin_midpoints, k)))
            p_miss = float(np.sum(self.probs[self.bin_midpoints > k]))
            cost = e_tau * c_idle_rate_g_s + p_miss * (c_cold_g + slo_pen_g)
            if cost < best_cost:
                best_cost = cost
                best_k = k
        return best_k


class ServerlessWorker:
    """One serverless GPU instance transitioning among COLD_OFF, LOADING, ACTIVE, WARM_IDLE."""

    def __init__(
        self,
        env: simpy.Environment,
        worker_id: int,
        cfg: ServerlessConfig,
        gpu: GPUProfile,
        host: HostProfile,
        n_gpus: int,
        t_cold_s: float,
        actual_ci: np.ndarray,
        observed_ci: np.ndarray,
        ci_max_ref: float,
        gap_tracker: OnlineGapHazardTracker,
    ) -> None:
        self.env = env
        self.worker_id = worker_id
        self.cfg = cfg
        self.gpu = gpu
        self.host = host
        self.n_gpus = n_gpus
        self.t_cold_s = t_cold_s
        self.actual_ci = actual_ci
        self.observed_ci = observed_ci
        self.ci_max_ref = ci_max_ref
        self.gap_tracker = gap_tracker
        self.pue = cfg.pue

        self.state = "COLD_OFF"
        self.last_t = 0.0
        self.idle_entered_t: Optional[float] = None
        self.load_done_t: float = 0.0
        self.load_done_ev: Optional[simpy.Event] = None
        self.active_reqs: int = 0
        self.max_concurrency: int = 16  # Serverless per-worker concurrency cap
        self.keep_alive_gen: int = 0
        self.evict_proc: Optional[simpy.Process] = None

        # Power parameters
        idle_ratio = 0.20 if cfg.idle_power_mode == "lace_rl" else (gpu.idle_w / gpu.tdp_w)
        self.host_scale = n_gpus / 4.0  # Proportional host share for 1-GPU (13B) vs 4-GPU (70B)
        self.p_gpu_idle_w = idle_ratio * gpu.tdp_w
        self.p_idle_total_w = n_gpus * self.p_gpu_idle_w + self.host_scale * host.idle_power_w
        self.p_cold_total_w = (
            n_gpus * cfg.cold_power_frac * gpu.tdp_w
            + self.host_scale * (0.5 * (host.idle_power_w + host.peak_power_w))
        )

        # Energy/carbon accumulators
        self.energy_exec_kwh = 0.0
        self.energy_idle_kwh = 0.0
        self.energy_cold_kwh = 0.0
        self.carbon_exec_g = 0.0
        self.carbon_idle_g = 0.0
        self.carbon_cold_g = 0.0
        self.active_s = 0.0
        self.warm_idle_s = 0.0
        self.cold_loading_s = 0.0
        self.cold_starts = 0

    def _current_power(self) -> float:
        if self.state == "COLD_OFF":
            return 0.0
        if self.state == "LOADING":
            return self.p_cold_total_w
        if self.state == "WARM_IDLE":
            return self.p_idle_total_w
        # ACTIVE
        mfu = min(self.cfg.mfu_sat, 0.12 + 0.33 * min(1.0, self.active_reqs / 8.0))
        ratio = (mfu / self.cfg.mfu_sat) ** self.cfg.mfu_gamma
        p_gpu = self.gpu.idle_w + (self.gpu.tdp_w - self.gpu.idle_w) * ratio
        p_host = self.host_scale * (
            self.host.idle_power_w + (self.host.peak_power_w - self.host.idle_power_w) * ratio
        )
        return self.n_gpus * p_gpu + p_host

    def _advance_to(self, t_now: float) -> None:
        if t_now <= self.last_t:
            return
        dt = t_now - self.last_t
        pw = self._current_power()
        kwh, g_co2 = integrate_carbon(self.actual_ci, self.last_t, t_now, pw, self.pue)
        if self.state == "ACTIVE":
            self.energy_exec_kwh += kwh
            self.carbon_exec_g += g_co2
            self.active_s += dt
        elif self.state == "WARM_IDLE":
            self.energy_idle_kwh += kwh
            self.carbon_idle_g += g_co2
            self.warm_idle_s += dt
        elif self.state == "LOADING":
            self.energy_cold_kwh += kwh
            self.carbon_cold_g += g_co2
            self.cold_loading_s += dt
        self.last_t = t_now

    def start_loading(self) -> simpy.Event:
        self._advance_to(self.env.now)
        if self.idle_entered_t is not None:
            self.gap_tracker.observe_gap(self.env.now - self.idle_entered_t)
            self.idle_entered_t = None
        self.state = "LOADING"
        self.cold_starts += 1
        self.load_done_t = self.env.now + self.t_cold_s
        ev = self.env.event()
        self.load_done_ev = ev

        def _loader():
            yield self.env.timeout(self.t_cold_s)
            self._advance_to(self.env.now)
            self.state = "ACTIVE" if self.active_reqs > 0 else "WARM_IDLE"
            if not ev.triggered:
                ev.succeed()
            if self.active_reqs == 0:
                self._enter_idle()

        self.env.process(_loader())
        return ev

    def wake_from_idle(self) -> None:
        self._advance_to(self.env.now)
        if self.idle_entered_t is not None:
            self.gap_tracker.observe_gap(self.env.now - self.idle_entered_t)
            self.idle_entered_t = None
        self.keep_alive_gen += 1
        self.state = "ACTIVE"

    def _enter_idle(self) -> None:
        self._advance_to(self.env.now)
        self.idle_entered_t = self.env.now
        self.keep_alive_gen += 1
        gen = self.keep_alive_gen

        if self.cfg.policy == "S1":
            k_s = 0.0
        elif self.cfg.policy == "S2":
            k_s = self.cfg.static_k_s
        elif self.cfg.policy == "S2b":
            k_s = 60.0
        elif self.cfg.policy == "S3":
            ci_t = ci_at(self.observed_ci, self.env.now)
            ci_norm = min(1.0, ci_t / max(self.ci_max_ref, 50.0))
            k_s = self.gap_tracker.choose_keep_alive(
                ci_t,
                ci_norm,
                self.p_idle_total_w,
                self.p_cold_total_w,
                self.t_cold_s,
                self.pue,
                ttft_slo_s=0.40,
                beta_slo=self.cfg.s3_beta_slo,
            )
        else:
            raise ValueError(f"Unknown serverless policy '{self.cfg.policy}'")

        total_keep = k_s + self.cfg.knative_grace_s
        if total_keep <= 0.0:
            self.state = "COLD_OFF"
            return

        self.state = "WARM_IDLE"

        def _timer(my_gen: int, timeout_s: float):
            yield self.env.timeout(timeout_s)
            if my_gen == self.keep_alive_gen and self.active_reqs == 0 and self.state == "WARM_IDLE":
                self._advance_to(self.env.now)
                # Keep self.idle_entered_t intact until next actual activation (uncensored gap!)
                self.state = "COLD_OFF"

        self.env.process(_timer(gen, total_keep))

    def release_request(self) -> None:
        self._advance_to(self.env.now)
        self.active_reqs -= 1
        if self.active_reqs == 0 and self.state == "ACTIVE":
            self._enter_idle()

    def flush(self, t_end: float) -> None:
        self._advance_to(t_end)

    def embodied_carbon_g(self, t_sim_s: float) -> float:
        t_hr = t_sim_s / 3600.0
        host_lt_hr = self.cfg.host_lifetime_yr * HOURS_PER_YEAR
        gpu_lt_hr = self.cfg.gpu_lifetime_yr * HOURS_PER_YEAR
        host_g = (self.host_scale * self.host.embodied_kgco2e * 1000.0 / host_lt_hr) * t_hr
        gpu_g = (self.n_gpus * self.gpu.embodied_kgco2e * 1000.0 / gpu_lt_hr) * t_hr
        return host_g + gpu_g


def run_serverless_simulation(cfg: ServerlessConfig) -> Dict[str, float]:
    """Run one complete SimPy Track B serverless simulation and return metrics."""
    stream = build_request_stream(cfg.workload, cfg.horizon, (cfg.region,), cfg.seed, rps_scale=1.0)
    carbon = build_carbon_bundle((cfg.region,), cfg.horizon, cfg.seed, ci_mode="actual")
    actual_ci = carbon.actual_ci[cfg.region]
    observed_ci = carbon.observed_ci[cfg.region]
    ci_max_ref = carbon.ci_max_ref[cfg.region]

    gpu = GPU_PROFILES[cfg.gpu_type]
    host = load_greensku_host_profile()
    n_gpus = 4 if cfg.model_size == "llama2_70b" else 1
    latency_scale = 1.0 if cfg.model_size == "llama2_70b" else 0.35
    t_cold_s = SERVERLESS_COLD_START_S[cfg.model_size][cfg.checkpoint_tier]
    slo_cfg = SLO_CONFIGS["mixed_dynamollm"]

    env = simpy.Environment()
    workers = [
        ServerlessWorker(
            env,
            w,
            cfg,
            gpu,
            host,
            n_gpus,
            t_cold_s,
            actual_ci,
            observed_ci,
            ci_max_ref,
            OnlineGapHazardTracker(),
        )
        for w in range(cfg.max_workers)
    ]

    n_req = len(stream.arrival_times_s)
    ttfts_ms = np.empty(n_req, dtype=np.float64)
    tpots_ms = np.empty(n_req, dtype=np.float64)
    slo_viol = np.zeros(n_req, dtype=np.int8)
    cold_hits = 0
    in_flight = 0
    feeder_done = False
    all_done_ev = env.event()

    def handle_serverless_req(idx: int, arr_t: float, l_in: int, l_out: int):
        nonlocal cold_hits, in_flight
        in_flight += 1
        # 1. Prefer ACTIVE worker with free capacity
        chosen = None
        active_cands = [w for w in workers if w.state == "ACTIVE" and w.active_reqs < w.max_concurrency]
        if active_cands:
            chosen = min(active_cands, key=lambda w: w.active_reqs)
            chosen._advance_to(env.now)
            chosen.active_reqs += 1
        else:
            # 2. Check WARM_IDLE workers
            warm_cands = [w for w in workers if w.state == "WARM_IDLE"]
            if warm_cands:
                chosen = warm_cands[0]
                chosen.wake_from_idle()
                chosen.active_reqs += 1
            else:
                # 3. Attach to an already-LOADING worker or cold-start a COLD_OFF worker
                load_cands = [w for w in workers if w.state == "LOADING" and w.active_reqs < w.max_concurrency]
                if load_cands:
                    chosen = min(load_cands, key=lambda w: w.load_done_t)
                    chosen.active_reqs += 1
                    cold_hits += 1
                    if chosen.load_done_ev is not None and not chosen.load_done_ev.triggered:
                        yield chosen.load_done_ev
                else:
                    off_cands = [w for w in workers if w.state == "COLD_OFF"]
                    if off_cands:
                        chosen = off_cands[0]
                        chosen.active_reqs += 1
                        cold_hits += 1
                        ev = chosen.start_loading()
                        yield ev
                    else:
                        # All workers busy; attach to least-loaded active worker
                        chosen = min(workers, key=lambda w: w.active_reqs)
                        chosen._advance_to(env.now)
                        chosen.active_reqs += 1

        # Prefill + Decode service
        q_mult = 1.0 + 0.10 * max(0, chosen.active_reqs - 1)
        t_prefill_s = latency_scale * q_mult * (gpu.prefill_base_ms + l_in * gpu.prefill_ms_per_tok) / 1000.0
        yield env.timeout(t_prefill_s)
        ttft_ms = (env.now - arr_t) * 1000.0
        ttfts_ms[idx] = ttft_ms

        t_step_s = latency_scale * (gpu.decode_step_ms / 1000.0) * (1.0 + 0.04 * max(0, chosen.active_reqs - 1))
        t_decode_s = l_out * t_step_s
        yield env.timeout(t_decode_s)
        tpot_ms = t_step_s * 1000.0
        tpots_ms[idx] = tpot_ms

        chosen.release_request()

        ttft_thr, tpot_thr = slo_cfg.thresholds_for_request(l_in, l_out)
        if ttft_ms > ttft_thr or tpot_ms > tpot_thr:
            slo_viol[idx] = 1
        in_flight -= 1
        if feeder_done and in_flight == 0 and not all_done_ev.triggered:
            all_done_ev.succeed()

    def feeder():
        nonlocal feeder_done
        prev_t = 0.0
        for idx in range(n_req):
            t_arr = float(stream.arrival_times_s[idx])
            if t_arr > prev_t:
                yield env.timeout(t_arr - prev_t)
                prev_t = t_arr
            env.process(
                handle_serverless_req(
                    idx,
                    t_arr,
                    int(stream.context_tokens[idx]),
                    int(stream.generated_tokens[idx]),
                )
            )
        feeder_done = True
        if in_flight == 0 and not all_done_ev.triggered:
            all_done_ev.succeed()

    env.process(feeder())
    env.run(until=all_done_ev)
    t_sim_end = max(stream.duration_s, env.now)
    for w in workers:
        w.flush(t_sim_end)

    op_exec_g = sum(w.carbon_exec_g for w in workers)
    op_idle_g = sum(w.carbon_idle_g for w in workers)
    op_cold_g = sum(w.carbon_cold_g for w in workers)
    op_total_g = op_exec_g + op_idle_g + op_cold_g

    # Peak active pool footprint determines provisioned serverless embodied footprint
    active_workers_used = sum(1 for w in workers if (w.active_s + w.warm_idle_s + w.cold_loading_s) > 0)
    emb_total_g = sum(w.embodied_carbon_g(t_sim_end) for w in workers[:max(1, active_workers_used)])

    e_exec = sum(w.energy_exec_kwh for w in workers)
    e_idle = sum(w.energy_idle_kwh for w in workers)
    e_cold = sum(w.energy_cold_kwh for w in workers)
    e_tot = e_exec + e_idle + e_cold

    total_tok = float(np.sum(stream.context_tokens) + np.sum(stream.generated_tokens))
    tok_1k = total_tok / 1000.0
    total_cold_events = sum(w.cold_starts for w in workers)

    return {
        "n_requests": float(n_req),
        "sim_duration_s": float(t_sim_end),
        "total_tokens": total_tok,
        "op_carbon_g": op_total_g,
        "op_exec_g": op_exec_g,
        "op_idle_g": op_idle_g,
        "op_cold_g": op_cold_g,
        "emb_carbon_g": emb_total_g,
        "sci_op_g_per_1k_tok": op_total_g / tok_1k,
        "sci_emb_g_per_1k_tok": emb_total_g / tok_1k,
        "sci_tot_g_per_1k_tok": (op_total_g + emb_total_g) / tok_1k,
        "embodied_share_pct": 100.0 * emb_total_g / max(op_total_g + emb_total_g, 1e-9),
        "total_energy_kwh": e_tot,
        "energy_exec_pct": 100.0 * e_exec / max(e_tot, 1e-9),
        "energy_idle_pct": 100.0 * e_idle / max(e_tot, 1e-9),
        "energy_cold_pct": 100.0 * e_cold / max(e_tot, 1e-9),
        "cold_start_count": float(total_cold_events),
        "cold_start_req_pct": 100.0 * cold_hits / n_req,
        "ttft_mean_ms": float(np.mean(ttfts_ms)),
        "ttft_p95_ms": float(np.percentile(ttfts_ms, 95)),
        "ttft_p99_ms": float(np.percentile(ttfts_ms, 99)),
        "tpot_mean_ms": float(np.mean(tpots_ms)),
        "tpot_p95_ms": float(np.percentile(tpots_ms, 95)),
        "slo_viol_pct": float(100.0 * np.mean(slo_viol)),
        "workers_used": float(active_workers_used),
    }
