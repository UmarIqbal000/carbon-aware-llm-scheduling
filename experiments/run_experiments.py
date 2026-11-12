"""Parallel experiment runner for all SimPy evaluation suites (E1, E2, SW1-SW4, H4).

Executes 10 fixed reproducible seeds (100..109) per configuration using
ProcessPoolExecutor and saves raw per-seed metrics directly to `./results/`.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
import time
from typing import Any, Callable, Dict, List, Tuple
import pandas as pd

from sim_config import ClusterConfig, RESULTS_DIR, SEEDS, ServerlessConfig
from simulator import run_cluster_simulation, run_serverless_simulation


def _exec_cluster_job(job: Tuple[Dict[str, Any], ClusterConfig]) -> Dict[str, Any]:
    meta, cfg = job
    metrics = run_cluster_simulation(cfg)
    row = dict(meta)
    row.update(metrics)
    return row


def _exec_serverless_job(job: Tuple[Dict[str, Any], ServerlessConfig]) -> Dict[str, Any]:
    meta, cfg = job
    metrics = run_serverless_simulation(cfg)
    row = dict(meta)
    row.update(metrics)
    return row


def _run_jobs(
    name: str,
    jobs: List[Tuple[Dict[str, Any], Any]],
    worker_fn: Callable[[Tuple[Dict[str, Any], Any]], Dict[str, Any]],
    max_workers: int,
    out_csv: Path,
) -> pd.DataFrame:
    t0 = time.perf_counter()
    print(f"[{name}] Starting {len(jobs)} simulation runs across {max_workers} workers...", flush=True)
    rows: List[Dict[str, Any]] = []
    done = 0
    step = max(1, len(jobs) // 10)
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        futs = [pool.submit(worker_fn, j) for j in jobs]
        for fut in as_completed(futs):
            rows.append(fut.result())
            done += 1
            if done % step == 0 or done == len(jobs):
                elapsed = time.perf_counter() - t0
                print(f"[{name}]   completed {done}/{len(jobs)} ({elapsed:.1f}s)", flush=True)
    df = pd.DataFrame(rows)
    sort_cols = [c for c in ("suite", "sub_exp", "horizon", "workload", "region", "topology", "ci_mode", "slo_name", "decode_tier", "diff_label", "wan_bw_gbps", "wan_rtt_ms", "rps_scale", "model_size", "checkpoint_tier", "cold_power_frac", "idle_power_mode", "lifetime_label", "pue", "mfu_gamma", "extra_clean_nodes", "policy", "seed") if c in df.columns]
    if sort_cols:
        df = df.sort_values(sort_cols)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"[{name}] Saved {len(df)} rows -> {out_csv} ({time.perf_counter() - t0:.1f}s)", flush=True)
    return df


def build_e1_jobs(horizons: Tuple[str, ...] = ("1h", "24h")) -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    jobs = []
    for horizon in horizons:
        for workload in ("conv", "code"):
            for policy in ("B1", "B2", "P3", "P4", "P5"):
                for seed in SEEDS:
                    cfg = ClusterConfig(
                        policy=policy,
                        workload=workload,
                        horizon=horizon,
                        seed=seed,
                    )
                    meta = {
                        "suite": "E1",
                        "horizon": horizon,
                        "workload": workload,
                        "policy": policy,
                        "seed": seed,
                    }
                    jobs.append((meta, cfg))
    return jobs


def build_e2_jobs(horizons: Tuple[str, ...] = ("1h", "24h")) -> List[Tuple[Dict[str, Any], ServerlessConfig]]:
    jobs = []
    pol_specs = [("S1", 0.0), ("S2", 30.0), ("S2b", 60.0), ("S3", 0.0)]
    for horizon in horizons:
        for region in ("South Scotland", "North Scotland", "TEPCO"):
            for policy, k_s in pol_specs:
                for seed in SEEDS:
                    cfg = ServerlessConfig(
                        policy=policy,
                        region=region,
                        workload="code",
                        horizon=horizon,
                        seed=seed,
                        static_k_s=k_s,
                    )
                    meta = {
                        "suite": "E2",
                        "horizon": horizon,
                        "region": region,
                        "workload": "code",
                        "policy": policy,
                        "static_k_s": k_s,
                        "seed": seed,
                    }
                    jobs.append((meta, cfg))
    return jobs


def build_sw1_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    jobs = []
    for rps_scale in (0.5, 1.0, 1.5, 2.0, 3.0):
        for policy in ("B1", "B2", "P3", "P4"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    rps_scale=rps_scale,
                )
                meta = {
                    "suite": "SW1",
                    "sub_exp": "rps_scale",
                    "horizon": "1h",
                    "workload": "conv",
                    "rps_scale": rps_scale,
                    "policy": policy,
                    "seed": seed,
                }
                jobs.append((meta, cfg))
    return jobs


def build_sw2_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    jobs = []
    topologies = {
        "low_diff_uk": ("South Scotland", "North West England"),
        "volatile_uk": ("North Scotland", "South Wales"),
        "cross_cont_60x": ("South Scotland", "TEPCO"),
    }
    # Part A: 3 spatial grid topologies over 24h diurnal cycles
    for topo_name, regs in topologies.items():
        for policy in ("B1", "B2", "P3", "P4", "P5"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="24h",
                    seed=seed,
                    regions=regs,
                    nodes_per_region=2,
                )
                meta = {
                    "suite": "SW2",
                    "sub_exp": "topology",
                    "topology": topo_name,
                    "ci_mode": "actual",
                    "horizon": "24h",
                    "workload": "conv",
                    "policy": policy,
                    "seed": seed,
                }
                jobs.append((meta, cfg))

    # Part B: UK NESO forecast error & telemetry lag sensitivity (24h 3-region)
    for ci_mode in ("actual", "neso_forecast", "lag_30m", "lag_60m", "noise_2x"):
        for policy in ("P3", "P4", "P5"):
            if policy == "P5" and ci_mode != "actual":
                continue  # P5 is Oracle reference on actual future CI
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="24h",
                    seed=seed,
                    ci_mode=ci_mode,
                )
                meta = {
                    "suite": "SW2",
                    "sub_exp": "forecast_noise",
                    "topology": "default_3region",
                    "ci_mode": ci_mode,
                    "horizon": "24h",
                    "workload": "conv",
                    "policy": policy,
                    "seed": seed,
                }
                jobs.append((meta, cfg))
    return jobs


def build_sw3_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    jobs = []
    # SW3a: SLO Tightness on bursty code trace (1h)
    for slo_name in ("strict_code", "mixed_dynamollm", "moderate_chatbot", "relaxed_sum"):
        for policy in ("B1", "B2", "P3", "P4"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="code",
                    horizon="1h",
                    seed=seed,
                    slo_name=slo_name,
                )
                meta = {
                    "suite": "SW3",
                    "sub_exp": "slo_tightness",
                    "slo_name": slo_name,
                    "decode_tier": "H100_cap55",
                    "wan_bw_gbps": 10.0,
                    "rps_scale": 1.0,
                    "workload": "code",
                    "policy": policy,
                    "seed": seed,
                }
                jobs.append((meta, cfg))

    # SW3b: Decode Hardware Tier on conv trace (1h)
    tiers = [
        ("H100_cap55", "H100", "H100", 0.55),
        ("H100_uncap", "H100", "H100", 1.00),
        ("A100_400W", "A100", "A100", 1.00),
        ("L4_72W_decode", "H100", "L4", 1.00),
    ]
    for tier_lbl, p_gpu, d_gpu, d_cap in tiers:
        for policy in ("B1", "B2", "P3", "P4"):
            if policy == "B1" and tier_lbl == "L4_72W_decode":
                # Colocated homogeneous L4 node cannot run fast prefill at 70B without H100 prefill
                continue
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    prefill_gpu_type=p_gpu,
                    decode_gpu_type=d_gpu,
                    decode_power_cap=d_cap,
                )
                meta = {
                    "suite": "SW3",
                    "sub_exp": "decode_tier",
                    "slo_name": "mixed_dynamollm",
                    "decode_tier": tier_lbl,
                    "wan_bw_gbps": 10.0,
                    "rps_scale": 1.0,
                    "workload": "conv",
                    "policy": policy,
                    "seed": seed,
                }
                jobs.append((meta, cfg))

    # SW3c: WAN KV Bandwidth sweep (10, 25, 100 Gbps) on code (1.0x) and conv (2.0x)
    for workload, rps_sc in (("code", 1.0), ("conv", 2.0)):
        for bw in (10.0, 25.0, 100.0):
            for policy in ("B2", "P3", "P4"):
                for seed in SEEDS:
                    cfg = ClusterConfig(
                        policy=policy,
                        workload=workload,
                        horizon="1h",
                        seed=seed,
                        wan_bw_gbps=bw,
                        rps_scale=rps_sc,
                    )
                    meta = {
                        "suite": "SW3",
                        "sub_exp": "wan_bw",
                        "slo_name": "mixed_dynamollm",
                        "decode_tier": "H100_cap55",
                        "wan_bw_gbps": bw,
                        "rps_scale": rps_sc,
                        "workload": workload,
                        "policy": policy,
                        "seed": seed,
                    }
                    jobs.append((meta, cfg))
    return jobs


def build_sw4_jobs() -> Tuple[
    List[Tuple[Dict[str, Any], ServerlessConfig]],
    List[Tuple[Dict[str, Any], ClusterConfig]],
]:
    srv_jobs = []
    # SW4a-1: Checkpoint format & model size (TEPCO 1h)
    for model_size in ("llama2_70b", "opt_13b"):
        for tier in ("serverlessllm", "safetensors", "pytorch"):
            for policy, k_s in (("S1", 0.0), ("S2", 30.0), ("S2b", 60.0), ("S3", 0.0)):
                for seed in SEEDS:
                    cfg = ServerlessConfig(
                        policy=policy,
                        region="TEPCO",
                        workload="code",
                        horizon="1h",
                        seed=seed,
                        model_size=model_size,
                        checkpoint_tier=tier,
                        static_k_s=k_s,
                    )
                    meta = {
                        "suite": "SW4",
                        "sub_exp": "checkpoint_tier",
                        "model_size": model_size,
                        "checkpoint_tier": tier,
                        "cold_power_frac": 0.65,
                        "idle_power_mode": "lace_rl",
                        "policy": policy,
                        "seed": seed,
                    }
                    srv_jobs.append((meta, cfg))

    # SW4a-2: Cold-start power fraction sensitivity
    for f_cold in (0.45, 0.65, 0.85):
        for policy, k_s in (("S1", 0.0), ("S2", 30.0), ("S3", 0.0)):
            for seed in SEEDS:
                cfg = ServerlessConfig(
                    policy=policy,
                    region="TEPCO",
                    workload="code",
                    horizon="1h",
                    seed=seed,
                    cold_power_frac=f_cold,
                    static_k_s=k_s,
                )
                meta = {
                    "suite": "SW4",
                    "sub_exp": "cold_power_frac",
                    "model_size": "llama2_70b",
                    "checkpoint_tier": "serverlessllm",
                    "cold_power_frac": f_cold,
                    "idle_power_mode": "lace_rl",
                    "policy": policy,
                    "seed": seed,
                }
                srv_jobs.append((meta, cfg))

    # SW4a-3: Idle power model (LACE-RL 0.20*TDP vs H100 hardware-exact 60W)
    for idle_mode in ("lace_rl", "hardware_exact"):
        for policy, k_s in (("S1", 0.0), ("S2", 30.0), ("S2b", 60.0), ("S3", 0.0)):
            for seed in SEEDS:
                cfg = ServerlessConfig(
                    policy=policy,
                    region="TEPCO",
                    workload="code",
                    horizon="1h",
                    seed=seed,
                    idle_power_mode=idle_mode,
                    static_k_s=k_s,
                )
                meta = {
                    "suite": "SW4",
                    "sub_exp": "idle_power_mode",
                    "model_size": "llama2_70b",
                    "checkpoint_tier": "serverlessllm",
                    "cold_power_frac": 0.65,
                    "idle_power_mode": idle_mode,
                    "policy": policy,
                    "seed": seed,
                }
                srv_jobs.append((meta, cfg))

    # SW4b: Embodied hardware lifetime, PUE, and sublinear gamma sensitivity (conv 1h)
    clu_jobs = []
    lifetimes = [
        ("3yr_unif", 3.0, 3.0),
        ("4yr_unif", 4.0, 4.0),
        ("5yr_unif", 5.0, 5.0),
        ("6yr_unif", 6.0, 6.0),
        ("9yr_host_3yr_gpu", 9.0, 3.0),
    ]
    for lt_lbl, h_lt, g_lt in lifetimes:
        for policy in ("B1", "B2", "P3", "P4"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    host_lifetime_yr=h_lt,
                    gpu_lifetime_yr=g_lt,
                )
                meta = {
                    "suite": "SW4",
                    "sub_exp": "lifetime",
                    "lifetime_label": lt_lbl,
                    "host_lifetime_yr": h_lt,
                    "gpu_lifetime_yr": g_lt,
                    "pue": 1.12,
                    "mfu_gamma": 0.70,
                    "policy": policy,
                    "seed": seed,
                }
                clu_jobs.append((meta, cfg))

    for pue in (1.10, 1.12, 1.20):
        for policy in ("B1", "B2", "P4"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    pue=pue,
                )
                meta = {
                    "suite": "SW4",
                    "sub_exp": "pue",
                    "lifetime_label": "4yr_unif",
                    "host_lifetime_yr": 4.0,
                    "gpu_lifetime_yr": 4.0,
                    "pue": pue,
                    "mfu_gamma": 0.70,
                    "policy": policy,
                    "seed": seed,
                }
                clu_jobs.append((meta, cfg))

    for gamma in (0.50, 0.70, 1.00):
        for policy in ("B1", "B2", "P4"):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    mfu_gamma=gamma,
                )
                meta = {
                    "suite": "SW4",
                    "sub_exp": "mfu_gamma",
                    "lifetime_label": "4yr_unif",
                    "host_lifetime_yr": 4.0,
                    "gpu_lifetime_yr": 4.0,
                    "pue": 1.12,
                    "mfu_gamma": gamma,
                    "policy": policy,
                    "seed": seed,
                }
                clu_jobs.append((meta, cfg))

    return srv_jobs, clu_jobs


def build_h4_elastic_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    """Explicit test of H4 scale-out paradox in clean low-carbon grid (South Scotland + London)."""
    jobs = []
    # Compare equal-fleet vs over-provisioned clean scale-out (+4 extra nodes in South Scotland)
    # under 4yr uniform and 9yr/3yr asymmetric lifespans
    configs = [
        ("B2_equal", "B2", 0),
        ("P3_equal", "P3", 0),
        ("P3_overprov_plus4", "P3_overprov", 4),
        ("P4_equal", "P4", 0),
    ]
    for lt_lbl, h_lt, g_lt in (("4yr_unif", 4.0, 4.0), ("9yr_host_3yr_gpu", 9.0, 3.0)):
        for pol_lbl, policy, extra in configs:
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy=policy,
                    workload="conv",
                    horizon="1h",
                    seed=seed,
                    regions=("South Scotland", "North East England", "London"),
                    clean_scaleout_extra_nodes=extra,
                    host_lifetime_yr=h_lt,
                    gpu_lifetime_yr=g_lt,
                )
                meta = {
                    "suite": "H4_elastic",
                    "sub_exp": "clean_scaleout",
                    "lifetime_label": lt_lbl,
                    "policy": pol_lbl,
                    "extra_clean_nodes": extra,
                    "seed": seed,
                }
                jobs.append((meta, cfg))
    return jobs


def build_sw5_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    """SW5: Cross-region Path C activation regime across WAN BW, RTT, differential, and load."""
    jobs: List[Tuple[Dict[str, Any], ClusterConfig]] = []
    bws = (10.0, 25.0, 100.0, 400.0)
    rtts = (5.0, 20.0, 50.0, 100.0, 200.0)

    # 1) Full BW x RTT grid on conv across high differential (1.0x nominal & 2.0x congested) and low differential (2.0x)
    grid_slices = [
        ("bw_rtt_high_nom", "conv", 1.0, "high_S_TEP", ("South Scotland", "TEPCO")),
        ("bw_rtt_high_cong", "conv", 2.0, "high_S_TEP", ("South Scotland", "TEPCO")),
        ("bw_rtt_low_cong", "conv", 2.0, "low_S_NW", ("South Scotland", "North West England")),
    ]
    for sub_exp, wl, rps, dlbl, regs in grid_slices:
        for bw in bws:
            for rtt in rtts:
                for seed in SEEDS:
                    cfg = ClusterConfig(
                        policy="P4",
                        regions=regs,
                        workload=wl,
                        horizon="1h",
                        seed=seed,
                        rps_scale=rps,
                        wan_bw_gbps=bw,
                        wan_rtt_override_ms=rtt,
                    )
                    meta = {
                        "suite": "SW5",
                        "sub_exp": sub_exp,
                        "workload": wl,
                        "rps_scale": rps,
                        "diff_label": dlbl,
                        "wan_bw_gbps": bw,
                        "wan_rtt_ms": rtt,
                        "policy": "P4",
                        "seed": seed,
                    }
                    jobs.append((meta, cfg))

    # 2) Targeted code 2.0x slice verifying large-KV Path C pruning under congestion
    for bw in (10.0, 100.0, 400.0):
        for rtt in (5.0, 20.0, 100.0):
            for seed in SEEDS:
                cfg = ClusterConfig(
                    policy="P4",
                    regions=("South Scotland", "London"),
                    workload="code",
                    horizon="1h",
                    seed=seed,
                    rps_scale=2.0,
                    wan_bw_gbps=bw,
                    wan_rtt_override_ms=rtt,
                )
                meta = {
                    "suite": "SW5",
                    "sub_exp": "code_cong",
                    "workload": "code",
                    "rps_scale": 2.0,
                    "diff_label": "med_S_Lon",
                    "wan_bw_gbps": bw,
                    "wan_rtt_ms": rtt,
                    "policy": "P4",
                    "seed": seed,
                }
                jobs.append((meta, cfg))
    return jobs


def build_sw6_jobs() -> List[Tuple[Dict[str, Any], ClusterConfig]]:
    """SW6: Extended H4 clean-region scale-out break-even sweep across RPS utilization (1.0x-3.0x)."""
    jobs: List[Tuple[Dict[str, Any], ClusterConfig]] = []
    configs = [
        ("P3_equal", "P3", 0),
        ("P3_overprov_plus4", "P3_overprov", 4),
        ("P4_equal", "P4", 0),
        ("P4_overprov_plus4", "P4", 4),
    ]
    for lt_lbl, h_lt, g_lt in (("4yr_unif", 4.0, 4.0), ("9yr_host_3yr_gpu", 9.0, 3.0)):
        for rps in (1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0):
            for pol_lbl, policy, extra in configs:
                for seed in SEEDS:
                    cfg = ClusterConfig(
                        policy=policy,
                        workload="conv",
                        horizon="1h",
                        seed=seed,
                        rps_scale=rps,
                        regions=("South Scotland", "North East England", "London"),
                        clean_scaleout_extra_nodes=extra,
                        host_lifetime_yr=h_lt,
                        gpu_lifetime_yr=g_lt,
                    )
                    meta = {
                        "suite": "SW6",
                        "sub_exp": "scaleout_breakeven",
                        "lifetime_label": lt_lbl,
                        "rps_scale": rps,
                        "policy": pol_lbl,
                        "extra_clean_nodes": extra,
                        "seed": seed,
                    }
                    jobs.append((meta, cfg))
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser(description="Run SimPy carbon-aware LLM scheduling experiments.")
    parser.add_argument(
        "--suite",
        type=str,
        default="all",
        choices=["all", "e1_1h", "e1_24h", "e1", "e2", "sw1", "sw2", "sw3", "sw4", "h4", "sw5", "sw6"],
        help="Which experiment suite to execute.",
    )
    parser.add_argument("--workers", type=int, default=10, help="Parallel worker processes.")
    args = parser.parse_args()

    s = args.suite
    if s in ("all", "e1", "e1_1h"):
        _run_jobs("E1_1h", build_e1_jobs(("1h",)), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_e1_1h.csv")
    if s in ("all", "e1", "e1_24h"):
        _run_jobs("E1_24h", build_e1_jobs(("24h",)), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_e1_24h.csv")
    if s in ("all", "e2"):
        _run_jobs("E2", build_e2_jobs(("1h", "24h")), _exec_serverless_job, args.workers, RESULTS_DIR / "raw_e2_serverless.csv")
    if s in ("all", "sw1"):
        _run_jobs("SW1", build_sw1_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw1_load.csv")
    if s in ("all", "sw2"):
        _run_jobs("SW2", build_sw2_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw2_grid.csv")
    if s in ("all", "sw3"):
        _run_jobs("SW3", build_sw3_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw3_slo_hw_wan.csv")
    if s in ("all", "sw4"):
        srv_jobs, clu_jobs = build_sw4_jobs()
        _run_jobs("SW4_srv", srv_jobs, _exec_serverless_job, args.workers, RESULTS_DIR / "raw_sw4_serverless.csv")
        _run_jobs("SW4_clu", clu_jobs, _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw4_cluster_lifetime.csv")
    if s in ("all", "h4"):
        _run_jobs("H4_elastic", build_h4_elastic_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_h4_elastic.csv")
    if s in ("all", "sw5"):
        _run_jobs("SW5", build_sw5_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw5_pathc.csv")
    if s in ("all", "sw6"):
        _run_jobs("SW6", build_sw6_jobs(), _exec_cluster_job, args.workers, RESULTS_DIR / "raw_sw6_breakeven.csv")


if __name__ == "__main__":
    main()
