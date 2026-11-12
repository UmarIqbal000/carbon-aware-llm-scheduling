"""Loaders and deterministic seed-paired builders for Azure LLM and UK/Japan carbon traces.

All workload and grid carbon traces derive directly from local CC-BY-4.0 files in
`./data/`. Japan FY2024 TSO files report `emission_factor_kgco2_per_kwh` in
kgCO2/kWh and are multiplied by 1000.0 upon ingestion to yield gCO2eq/kWh.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Sequence, Tuple
import math
import numpy as np
import pandas as pd

from sim_config import DATA_DIR, JAPAN_TSO_DIR, REGIONS, SLOT_SECONDS


JAPAN_FILE_MAP: Dict[str, str] = {
    "TEPCO": "emission_factor_2024_TEPCO_Power_Grid.csv",
    "Kansai": "emission_factor_2024_Kansai_Transmission_and_Distribution.csv",
    "Kyushu": "emission_factor_2024_Kyushu_Electric_Power_Transmission_and_Distribution.csv",
    "Hokkaido": "emission_factor_2024_Hokkaido_Electric_Power_Network.csv",
    "Chubu": "emission_factor_2024_Chubu_Electric_Power_Grid.csv",
}


@dataclass(frozen=True)
class RawAzureTrace:
    """Immutable arrays representing a parsed 2023 Azure LLM inference trace."""

    name: str
    rel_times_s: np.ndarray
    dts_s: np.ndarray
    context_tokens: np.ndarray
    generated_tokens: np.ndarray
    span_s: float
    rps: float
    ia_cv: float


@dataclass(frozen=True)
class RequestStream:
    """Seed-deterministic request arrival stream ready for SimPy replay."""

    arrival_times_s: np.ndarray
    context_tokens: np.ndarray
    generated_tokens: np.ndarray
    origin_region_idx: np.ndarray  # index into active region tuple
    duration_s: float


@dataclass(frozen=True)
class CarbonSeriesBundle:
    """Aligned 30-minute carbon intensity arrays (actual vs scheduler-observed)."""

    regions: Tuple[str, ...]
    actual_ci: Dict[str, np.ndarray]     # shape (n_slots + extra,) in gCO2eq/kWh
    observed_ci: Dict[str, np.ndarray]   # scheduler-visible CI (forecast/lagged/noisy)
    ci_max_ref: Dict[str, float]         # regional reference ceiling from 28-day window


@lru_cache(maxsize=4)
def load_raw_azure_trace(workload: str) -> RawAzureTrace:
    """Parse `AzureLLMInferenceTrace_{conv,code}.csv` into cached NumPy arrays."""
    if workload not in ("conv", "code"):
        raise ValueError(f"Unsupported workload '{workload}'; expected 'conv' or 'code'.")
    path = DATA_DIR / f"AzureLLMInferenceTrace_{workload}.csv"
    df = pd.read_csv(path)
    ts = pd.to_datetime(df["TIMESTAMP"])
    rel = (ts - ts.iloc[0]).dt.total_seconds().to_numpy(dtype=np.float64)
    dts = np.diff(rel, prepend=0.0)
    ctx = df["ContextTokens"].to_numpy(dtype=np.int32)
    gen = df["GeneratedTokens"].to_numpy(dtype=np.int32)
    span_s = float(rel[-1] - rel[0])
    pos_dts = dts[1:]
    ia_cv = float(np.std(pos_dts) / np.mean(pos_dts))
    rps = float(len(df) / span_s)
    return RawAzureTrace(
        name=workload,
        rel_times_s=rel,
        dts_s=dts,
        context_tokens=ctx,
        generated_tokens=gen,
        span_s=span_s,
        rps=rps,
        ia_cv=ia_cv,
    )


@lru_cache(maxsize=1)
def _load_uk_regional_table() -> Dict[str, np.ndarray]:
    """Return 30-min forecast_gco2_kwh arrays aligned from 2025-10-01T00:00Z (1296+ slots)."""
    df = pd.read_csv(DATA_DIR / "uk_regional_carbon_intensity_oct2025.csv")
    df["from_dt"] = pd.to_datetime(df["from"], utc=True)
    # Trim slot 0 (2025-09-30T23:30Z) so index 0 aligns cleanly to 00:00Z on 2025-10-01
    df = df[df["from_dt"] >= pd.Timestamp("2025-10-01T00:00:00Z")].copy()
    df = df.sort_values(["shortname", "from_dt"])
    out: Dict[str, np.ndarray] = {}
    for name, grp in df.groupby("shortname"):
        out[str(name)] = grp["forecast_gco2_kwh"].to_numpy(dtype=np.float64)
    return out


@lru_cache(maxsize=1)
def _load_uk_national_forecast_errors() -> Tuple[np.ndarray, np.ndarray]:
    """Return empirical (additive_err, relative_err) from UK NESO national forecast vs actual."""
    df = pd.read_csv(DATA_DIR / "uk_national_carbon_intensity_oct2025.csv")
    fc = df["forecast_gco2_kwh"].to_numpy(dtype=np.float64)
    act = df["actual_gco2_kwh"].to_numpy(dtype=np.float64)
    add_err = fc - act
    rel_err = (fc - act) / np.maximum(act, 10.0)
    return add_err, rel_err


@lru_cache(maxsize=8)
def _load_japan_oct_table(region: str) -> np.ndarray:
    """Return October 2024 UTC-aligned 30-min carbon intensity in gCO2eq/kWh (* 1000.0)."""
    fname = JAPAN_FILE_MAP[region]
    df = pd.read_csv(JAPAN_TSO_DIR / fname)
    df["utc"] = pd.to_datetime(df["timestamp_jst_iso"], utc=True)
    mask = (df["utc"] >= pd.Timestamp("2024-10-01T00:00:00Z")) & (
        df["utc"] < pd.Timestamp("2024-10-29T00:00:00Z")
    )
    sub = df.loc[mask].sort_values("utc")
    # CRITICAL UNIT CONVERSION: kgCO2/kWh * 1000.0 -> gCO2eq/kWh
    return sub["emission_factor_kgco2_per_kwh"].to_numpy(dtype=np.float64) * 1000.0


@lru_cache(maxsize=16)
def get_full_region_ci_oct(region: str) -> np.ndarray:
    """Return 28-day October 30-min gCO2eq/kWh array aligned at 00:00Z."""
    spec = REGIONS[region]
    if spec.country == "UK":
        uk_tbl = _load_uk_regional_table()
        arr = uk_tbl[spec.trace_key]
    elif spec.country == "JP":
        arr = _load_japan_oct_table(spec.trace_key)
    else:
        raise ValueError(f"Unknown country for region {region}")
    return arr


def build_carbon_bundle(
    regions: Sequence[str],
    horizon: str,
    seed: int,
    ci_mode: str = "actual",
) -> CarbonSeriesBundle:
    """Slice deterministic seed-aligned 30-min grid CI traces for 1h or 24h runs.

    Includes extra padding slots beyond the horizon so 30-min lookahead (P5) or
    request spillover near T_sim_end never hits out-of-bounds indices.
    """
    rng = np.random.default_rng(seed * 97 + 13)
    n_horizon_slots = 2 if horizon == "1h" else 48
    pad_slots = 4

    # UK table has 1343 slots from 2025-10-01T00:00Z (27 full days = 1296 slots).
    if horizon == "24h":
        day_idx = int(rng.integers(0, 26))  # 0..25 leaves >= 2 days padding
        start_slot = day_idx * 48
    else:
        start_slot = int(rng.integers(2, 1296 - 6))  # leaves >=2 lag slots before & >=6 after

    actual_ci: Dict[str, np.ndarray] = {}
    observed_ci: Dict[str, np.ndarray] = {}
    ci_max_ref: Dict[str, float] = {}

    add_errs, rel_errs = _load_uk_national_forecast_errors()

    for r in regions:
        full_arr = get_full_region_ci_oct(r)
        # Keep 2 history slots before start_slot so lag_30m/lag_60m use real prior slots
        window_actual = full_arr[start_slot : start_slot + n_horizon_slots + pad_slots].copy()
        actual_ci[r] = window_actual
        ci_max_ref[r] = float(np.percentile(full_arr, 95))

        if ci_mode == "actual":
            obs = window_actual.copy()
        elif ci_mode == "lag_30m":
            obs = full_arr[start_slot - 1 : start_slot - 1 + n_horizon_slots + pad_slots].copy()
        elif ci_mode == "lag_60m":
            obs = full_arr[start_slot - 2 : start_slot - 2 + n_horizon_slots + pad_slots].copy()
        elif ci_mode in ("neso_forecast", "noise_2x"):
            scale = 1.0 if ci_mode == "neso_forecast" else 2.0
            # Sample empirical NESO forecast residuals proportionally/additively
            sampled_rel = rng.choice(rel_errs, size=len(window_actual), replace=True)
            sampled_add = rng.choice(add_errs, size=len(window_actual), replace=True)
            # Blend additive + relative noise cleanly for low vs high-CI regions
            noise = np.where(
                window_actual > 50.0,
                window_actual * sampled_rel * scale,
                sampled_add * 0.5 * scale,
            )
            obs = np.clip(window_actual + noise, 0.0, None)
        else:
            raise ValueError(f"Unknown ci_mode '{ci_mode}'")
        observed_ci[r] = obs

    return CarbonSeriesBundle(
        regions=tuple(regions),
        actual_ci=actual_ci,
        observed_ci=observed_ci,
        ci_max_ref=ci_max_ref,
    )


def build_request_stream(
    workload: str,
    horizon: str,
    regions: Sequence[str],
    seed: int,
    rps_scale: float = 1.0,
) -> RequestStream:
    """Build deterministic seed-paired request arrival stream for SimPy replay.

    - For `horizon == '1h'` and `rps_scale == 1.0`: replays the raw 2023 Azure
      timestamps directly (`19,366` conv or `8,819` code requests) with tiny
      sub-millisecond seed jitter and balanced regional gateway assignment.
    - For `horizon == '1h'` and `rps_scale != 1.0`: scales empirical inter-arrival
      times by `1 / rps_scale` and tiles empirical blocks cleanly to fill a fixed
      `3600 s` 1-hour window so grid exposure stays constant across load levels.
    - For `horizon == '24h'`: empirically block-bootstraps 5-minute blocks from
      the real Azure trace over 48 x 30-min slots (`86,400 s`), modulated by a
      zero-mean regional local-time diurnal demand curve (`0.70x` night to `1.30x`
      afternoon) preserving exact empirical token distributions and burst CV.
    """
    raw = load_raw_azure_trace(workload)
    rng = np.random.default_rng(seed * 131 + 7)
    n_reg = len(regions)

    if horizon == "1h":
        if abs(rps_scale - 1.0) < 1e-9:
            # Direct raw trace replay with tiny non-reordering seed jitter (<= 1 ms)
            jitter = rng.uniform(-0.001, 0.001, size=len(raw.rel_times_s))
            arr_t = np.maximum.accumulate(np.maximum(0.0, raw.rel_times_s + jitter))
            ctx = raw.context_tokens.copy()
            gen = raw.generated_tokens.copy()
            origin = rng.integers(0, n_reg, size=len(arr_t), dtype=np.int32)
            duration_s = float(raw.span_s)
            return RequestStream(arr_t, ctx, gen, origin, duration_s)

        # Scaled 1h window (3600 s) preserving empirical sequence & burstiness
        target_dur = 3600.0
        scaled_dts = raw.dts_s / rps_scale
        # Concatenate full trace wraps until reaching 3600 s
        t_cur = 0.0
        arr_parts: List[np.ndarray] = []
        ctx_parts: List[np.ndarray] = []
        gen_parts: List[np.ndarray] = []
        while t_cur < target_dur:
            offset = int(rng.integers(0, len(raw.dts_s) // 4))
            dts_rot = np.roll(scaled_dts, -offset)
            dts_rot[0] = max(0.005, float(dts_rot[0]))
            t_block = t_cur + np.cumsum(dts_rot)
            keep = t_block < target_dur
            if not np.any(keep):
                break
            arr_parts.append(t_block[keep])
            ctx_parts.append(np.roll(raw.context_tokens, -offset)[keep])
            gen_parts.append(np.roll(raw.generated_tokens, -offset)[keep])
            t_cur = float(arr_parts[-1][-1]) + 0.05
            if t_block[-1] >= target_dur:
                break
        arr_t = np.concatenate(arr_parts)
        ctx = np.concatenate(ctx_parts)
        gen = np.concatenate(gen_parts)
        origin = rng.integers(0, n_reg, size=len(arr_t), dtype=np.int32)
        return RequestStream(arr_t, ctx, gen, origin, target_dur)

    if horizon == "24h":
        # Build 12 contiguous ~280s blocks from the raw Azure trace so empirical
        # burstiness (ia_cv=13.15 for code, 1.09 for conv) and token pairs stay intact.
        n_blocks = 12
        block_bounds = np.linspace(0, len(raw.dts_s), n_blocks + 1, dtype=int)
        blocks: List[Tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for b in range(n_blocks):
            s_i, e_i = block_bounds[b], block_bounds[b + 1]
            b_dts = raw.dts_s[s_i:e_i].copy()
            if b == 0:
                b_dts[0] = max(0.01, float(np.median(raw.dts_s[1:])))
            b_ctx = raw.context_tokens[s_i:e_i].copy()
            b_gen = raw.generated_tokens[s_i:e_i].copy()
            blocks.append((b_dts, b_ctx, b_gen))

        target_dur = 86400.0
        arr_parts = []
        ctx_parts = []
        gen_parts = []
        org_parts = []

        # Diurnal envelope per 30-min UTC slot (mean across 24h = 1.0 per region)
        offsets_h = np.array([REGIONS[r].utc_offset_hours for r in regions], dtype=np.float64)
        for slot in range(48):
            slot_start = slot * SLOT_SECONDS
            slot_end = (slot + 1) * SLOT_SECONDS
            utc_hour = slot * 0.5 + 0.25
            local_hours = (utc_hour + offsets_h) % 24.0
            # Peak at 14:00 local time (1.30x), trough at 02:00 local time (0.70x)
            reg_mult = 1.0 + 0.30 * np.cos(2.0 * math.pi * (local_hours - 14.0) / 24.0)
            total_mult = float(np.mean(reg_mult)) * rps_scale
            reg_probs = reg_mult / np.sum(reg_mult)

            t_cur = slot_start
            while t_cur < slot_end:
                b_idx = int(rng.integers(0, n_blocks))
                b_dts, b_ctx, b_gen = blocks[b_idx]
                scaled_b_dts = b_dts / total_mult
                t_block = t_cur + np.cumsum(scaled_b_dts)
                keep = t_block < slot_end
                if not np.any(keep):
                    break
                n_keep = int(np.sum(keep))
                arr_parts.append(t_block[keep])
                ctx_parts.append(b_ctx[keep])
                gen_parts.append(b_gen[keep])
                org_parts.append(rng.choice(n_reg, size=n_keep, p=reg_probs).astype(np.int32))
                t_cur = float(t_block[keep][-1])
                if t_block[-1] >= slot_end:
                    break

        arr_t = np.concatenate(arr_parts)
        ctx = np.concatenate(ctx_parts)
        gen = np.concatenate(gen_parts)
        origin = np.concatenate(org_parts)
        return RequestStream(arr_t, ctx, gen, origin, target_dur)

    raise ValueError(f"Unsupported horizon '{horizon}'; expected '1h' or '24h'.")
