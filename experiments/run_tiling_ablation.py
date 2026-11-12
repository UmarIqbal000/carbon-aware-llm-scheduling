"""24-Hour Azure Trace-Tiling Sensitivity Ablation (Part B4).

Tests whether 24-hour Track A cluster simulation findings (P4 vs B1, B2) are sensitive
to how the ~58-minute Azure trace is tiled across 24 hours (random-with-replacement ~280 s
blocks vs. without-replacement block permutations, finer ~90 s blocks, and coarser ~870 s
blocks) across all N=10 paired seeds using identical grid CI series (`build_carbon_bundle`).
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import math
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from sim_config import ClusterConfig, REGIONS, RESULTS_DIR, SEEDS, SLOT_SECONDS
import trace_loader
import simulator


def build_ablated_24h_stream(
    workload: str,
    regions: tuple[str, ...],
    seed: int,
    mode: str,
) -> trace_loader.RequestStream:
    """Build 24h RequestStream under controlled block-shuffling and block-length regimes."""
    if mode == "orig_280s_repl":
        return trace_loader.build_request_stream(workload, "24h", regions, seed, rps_scale=1.0)

    mode_blocks = {
        "perm_280s_norepl": 12,
        "fine_90s_perm": 38,
        "coarse_900s_perm": 4,
    }
    if mode not in mode_blocks:
        raise ValueError(f"Unknown tiling ablation mode: {mode}")

    raw = trace_loader.load_raw_azure_trace(workload)
    rng = np.random.default_rng(seed * 131 + 7)
    n_reg = len(regions)
    n_blocks = mode_blocks[mode]

    block_bounds = np.linspace(0, len(raw.dts_s), n_blocks + 1, dtype=int)
    blocks = []
    for b in range(n_blocks):
        s_i, e_i = block_bounds[b], block_bounds[b + 1]
        b_dts = raw.dts_s[s_i:e_i].copy()
        if b == 0:
            b_dts[0] = max(0.01, float(np.median(raw.dts_s[1:])))
        blocks.append((b_dts, raw.context_tokens[s_i:e_i].copy(), raw.generated_tokens[s_i:e_i].copy()))

    deck = list(rng.permutation(n_blocks))
    deck_pos = 0

    def next_block_idx() -> int:
        nonlocal deck, deck_pos
        if deck_pos >= len(deck):
            deck = list(rng.permutation(n_blocks))
            deck_pos = 0
        idx = int(deck[deck_pos])
        deck_pos += 1
        return idx

    target_dur = 86400.0
    arr_parts, ctx_parts, gen_parts, org_parts = [], [], [], []
    offsets_h = np.array([REGIONS[r].utc_offset_hours for r in regions], dtype=np.float64)

    for slot in range(48):
        slot_start = slot * SLOT_SECONDS
        slot_end = (slot + 1) * SLOT_SECONDS
        utc_hour = slot * 0.5 + 0.25
        local_hours = (utc_hour + offsets_h) % 24.0
        reg_mult = 1.0 + 0.30 * np.cos(2.0 * math.pi * (local_hours - 14.0) / 24.0)
        total_mult = float(np.mean(reg_mult))
        reg_probs = reg_mult / np.sum(reg_mult)

        t_cur = slot_start
        while t_cur < slot_end:
            b_idx = next_block_idx()
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

    return trace_loader.RequestStream(
        np.concatenate(arr_parts),
        np.concatenate(ctx_parts),
        np.concatenate(gen_parts),
        np.concatenate(org_parts),
        target_dur,
    )


def _exec_ablation_job(task: tuple[str, str, int]) -> dict:
    mode, policy, seed = task
    cfg = ClusterConfig(policy=policy, workload="conv", horizon="24h", seed=seed)
    orig_fn = simulator.build_request_stream
    simulator.build_request_stream = lambda wl, hz, regs, sd, rps_scale=1.0: build_ablated_24h_stream(
        wl, tuple(regs), sd, mode
    )
    try:
        res = simulator.run_cluster_simulation(cfg)
    finally:
        simulator.build_request_stream = orig_fn
    res["tiling_mode"] = mode
    res["policy"] = policy
    res["seed"] = seed
    return res


def main() -> None:
    modes = ("perm_280s_norepl", "fine_90s_perm", "coarse_900s_perm")
    policies = ("B1", "B2", "P4")

    raw_out = RESULTS_DIR / "tiling_ablation_raw.csv"
    rows: list[dict] = []

    e1_24h_path = RESULTS_DIR / "raw_e1_24h.csv"
    if e1_24h_path.exists():
        e1_df = pd.read_csv(e1_24h_path)
        sub = e1_df[(e1_df["workload"] == "conv") & (e1_df["policy"].isin(policies))].copy()
        sub["tiling_mode"] = "orig_280s_repl"
        rows.extend(sub.to_dict(orient="records"))
        print(f"Loaded {len(rows)} baseline orig_280s_repl rows from {e1_24h_path.name}", flush=True)
    else:
        modes = ("orig_280s_repl",) + modes

    tasks = [(m, p, s) for m in modes for p in policies for s in SEEDS]
    total = len(tasks)
    print(f"Running {total} 24h tiling ablation jobs across 12 workers...", flush=True)
    with ProcessPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(_exec_ablation_job, t): t for t in tasks}
        done_cnt = 0
        for f in as_completed(futs):
            done_cnt += 1
            rows.append(f.result())
            if done_cnt % 10 == 0 or done_cnt == total:
                print(f"  progress: {done_cnt}/{total}", flush=True)

    df = pd.DataFrame(rows).sort_values(["tiling_mode", "policy", "seed"])
    df.to_csv(raw_out, index=False)

    grp = df.groupby(["tiling_mode", "policy"])[
        ["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms", "n_requests"]
    ].agg(["mean", "std"]).reset_index()
    grp.columns = ["_".join(c).strip("_") for c in grp.columns]
    sum_out = RESULTS_DIR / "tiling_ablation_summary.csv"
    grp.to_csv(sum_out, index=False)
    print(grp.to_string(index=False), flush=True)
    print(f"\nSaved {raw_out} and {sum_out}", flush=True)


if __name__ == "__main__":
    main()
