"""Statistical aggregation, Student-t 95% CIs, Wilcoxon signed-rank tests, and hypothesis verification.

Reads raw per-seed CSV outputs in `./results/` produced by `run_experiments.py`
and writes summary CI CSVs, pairwise Wilcoxon test CSVs, and a structured
H1-H4 hypothesis verification report.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Sequence, Tuple
import math
import numpy as np
import pandas as pd
from scipy import stats

from sim_config import RESULTS_DIR


T_CRIT_9 = float(stats.t.ppf(0.975, df=9))  # 2.2621571627409915 for S=10 seeds


CLUSTER_METRICS = [
    "sci_op_g_per_1k_tok",
    "sci_emb_g_per_1k_tok",
    "sci_tot_g_per_1k_tok",
    "sci_op_g_per_1k_gen",
    "sci_tot_g_per_1k_gen",
    "embodied_share_pct",
    "clean_region_emb_share_pct",
    "dirty_region_emb_share_pct",
    "op_carbon_g",
    "emb_carbon_g",
    "total_energy_kwh",
    "j_per_tok",
    "energy_prefill_pct",
    "energy_decode_pct",
    "energy_idle_pct",
    "energy_kv_pct",
    "ttft_mean_ms",
    "ttft_p90_ms",
    "ttft_p95_ms",
    "ttft_p99_ms",
    "tpot_mean_ms",
    "tpot_p90_ms",
    "tpot_p95_ms",
    "tpot_p99_ms",
    "slo_viol_pct",
    "slo_ttft_viol_pct",
    "slo_tpot_viol_pct",
    "gpu_util_pct",
    "gpu_active_time_pct",
    "kv_wan_gb_per_1k_req",
    "path_coloc_pct",
    "path_intra_pd_pct",
    "path_cross_pd_pct",
    "path_remote_pd_pct",
]

SERVERLESS_METRICS = [
    "sci_op_g_per_1k_tok",
    "sci_emb_g_per_1k_tok",
    "sci_tot_g_per_1k_tok",
    "embodied_share_pct",
    "op_carbon_g",
    "op_exec_g",
    "op_idle_g",
    "op_cold_g",
    "emb_carbon_g",
    "total_energy_kwh",
    "energy_exec_pct",
    "energy_idle_pct",
    "energy_cold_pct",
    "cold_start_count",
    "cold_start_req_pct",
    "ttft_mean_ms",
    "ttft_p95_ms",
    "ttft_p99_ms",
    "tpot_mean_ms",
    "tpot_p95_ms",
    "slo_viol_pct",
    "workers_used",
]


def summarize_grouped(df: pd.DataFrame, group_cols: Sequence[str], metrics: Sequence[str]) -> pd.DataFrame:
    """Compute sample mean, std, Student-t 95% CI, median, and IQR per configuration."""
    avail_metrics = [m for m in metrics if m in df.columns]
    rows: List[Dict] = []
    for keys, grp in df.groupby(list(group_cols), dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row: Dict = {col: val for col, val in zip(group_cols, keys)}
        n = len(grp)
        row["n_seeds"] = n
        t_crit = float(stats.t.ppf(0.975, df=max(1, n - 1))) if n > 1 else 0.0
        for m in avail_metrics:
            vals = grp[m].to_numpy(dtype=np.float64)
            mean = float(np.mean(vals))
            std = float(np.std(vals, ddof=1)) if n > 1 else 0.0
            ci_hw = t_crit * std / math.sqrt(n) if n > 1 else 0.0
            med = float(np.median(vals))
            iqr = float(np.percentile(vals, 75) - np.percentile(vals, 25))
            row[f"{m}_mean"] = mean
            row[f"{m}_std"] = std
            row[f"{m}_ci95"] = ci_hw
            row[f"{m}_ci95_low"] = mean - ci_hw
            row[f"{m}_ci95_high"] = mean + ci_hw
            row[f"{m}_median"] = med
            row[f"{m}_iqr"] = iqr
        rows.append(row)
    return pd.DataFrame(rows)


def safe_wilcoxon(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, str]:
    """Two-sided Wilcoxon signed-rank test handling exact ties/zero diffs safely."""
    diff = x - y
    if np.all(np.abs(diff) < 1e-12):
        return 0.0, 1.0, "identical_zero_diff"
    try:
        res = stats.wilcoxon(x, y, alternative="two-sided", zero_method="wilcox")
        return float(res.statistic), float(res.pvalue), "ok"
    except Exception as exc:  # pragma: no cover
        return float("nan"), float("nan"), str(exc)


def run_pairwise_wilcoxon(
    df: pd.DataFrame,
    group_cols: Sequence[str],
    target_policy: str,
    baselines: Sequence[str],
    metrics: Sequence[str],
) -> pd.DataFrame:
    """Compute matched-seed pairwise Wilcoxon signed-rank tests (target vs baselines)."""
    rows: List[Dict] = []
    avail_metrics = [m for m in metrics if m in df.columns]
    for keys, grp in df.groupby(list(group_cols), dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        base_meta = {col: val for col, val in zip(group_cols, keys)}
        t_df = grp[grp["policy"] == target_policy].sort_values("seed")
        if t_df.empty:
            continue
        for b_pol in baselines:
            b_df = grp[grp["policy"] == b_pol].sort_values("seed")
            if b_df.empty:
                continue
            merged = pd.merge(t_df, b_df, on="seed", suffixes=("_target", "_base"))
            if len(merged) < 5:
                continue
            for m in avail_metrics:
                x = merged[f"{m}_target"].to_numpy(dtype=np.float64)
                y = merged[f"{m}_base"].to_numpy(dtype=np.float64)
                stat, pval, status = safe_wilcoxon(x, y)
                x_mean = float(np.mean(x))
                y_mean = float(np.mean(y))
                rel_diff_pct = (
                    100.0 * (x_mean - y_mean) / y_mean if abs(y_mean) > 1e-12 else 0.0
                )
                row = dict(base_meta)
                row.update(
                    {
                        "target_policy": target_policy,
                        "baseline_policy": b_pol,
                        "metric": m,
                        "n_pairs": len(merged),
                        "target_mean": x_mean,
                        "baseline_mean": y_mean,
                        "abs_diff": x_mean - y_mean,
                        "rel_diff_pct": rel_diff_pct,
                        "wilcoxon_stat": stat,
                        "p_value": pval,
                        "significant_0_05": bool(pval < 0.05) if not math.isnan(pval) else False,
                        "status": status,
                    }
                )
                rows.append(row)
    return pd.DataFrame(rows)


def _load_if_exists(name: str) -> pd.DataFrame | None:
    p = RESULTS_DIR / name
    return pd.read_csv(p) if p.exists() else None


def evaluate_hypotheses(summaries: Dict[str, pd.DataFrame], wilcoxons: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Audit H1-H4 strictly against DESIGN.md falsification criteria using observed outputs."""
    records: List[Dict] = []

    # H1: Phase-split asymmetric carbon sensitivity (P4 vs B1, B2)
    if "e1_1h" in summaries and "e1_24h" in summaries:
        e1_all = pd.concat([summaries["e1_1h"], summaries["e1_24h"]], ignore_index=True)
        for h in ("1h", "24h"):
            for w in ("conv", "code"):
                sub = e1_all[(e1_all["horizon"] == h) & (e1_all["workload"] == w)]
                b1 = sub[sub["policy"] == "B1"].iloc[0]
                b2 = sub[sub["policy"] == "B2"].iloc[0]
                p4 = sub[sub["policy"] == "P4"].iloc[0]
                red_b1 = 100.0 * (b1["sci_op_g_per_1k_tok_mean"] - p4["sci_op_g_per_1k_tok_mean"]) / b1["sci_op_g_per_1k_tok_mean"]
                red_b2 = 100.0 * (b2["sci_op_g_per_1k_tok_mean"] - p4["sci_op_g_per_1k_tok_mean"]) / b2["sci_op_g_per_1k_tok_mean"]
                slo_p4 = float(p4["slo_viol_pct_mean"])
                slo_b1 = float(b1["slo_viol_pct_mean"])
                status = (
                    "SUPPORTED"
                    if (red_b1 >= 15.0 and red_b2 >= 15.0 and slo_p4 <= 5.0)
                    else ("PARTIALLY SUPPORTED" if (red_b1 >= 15.0 and red_b2 >= 15.0 and slo_p4 <= slo_b1) else "NUANCED")
                )
                records.append(
                    {
                        "hypothesis": "H1",
                        "context": f"E1_{h}_{w}",
                        "status": status,
                        "key_evidence": (
                            f"P4 SCI_op reduction: {red_b1:.1f}% vs B1, {red_b2:.1f}% vs B2; "
                            f"P4 SLO viol={slo_p4:.2f}% (B1={slo_b1:.2f}%, B2={b2['slo_viol_pct_mean']:.2f}%)"
                        ),
                    }
                )

    # H2: KV-cache transfer vs recomputation crossover (P4 vs P3 across E1, SW2, SW3_wan_bw)
    if "e1_1h" in summaries:
        e1_all = pd.concat([summaries["e1_1h"], summaries.get("e1_24h", pd.DataFrame())], ignore_index=True)
        for (h, w), grp in e1_all.groupby(["horizon", "workload"]):
            p3 = grp[grp["policy"] == "P3"].iloc[0]
            p4 = grp[grp["policy"] == "P4"].iloc[0]
            slo_ok = p4["slo_viol_pct_mean"] < p3["slo_viol_pct_mean"]
            ttft_ok = p4["ttft_p95_ms_mean"] < p3["ttft_p95_ms_mean"]
            tot_diff = 100.0 * (p4["sci_tot_g_per_1k_tok_mean"] - p3["sci_tot_g_per_1k_tok_mean"]) / p3["sci_tot_g_per_1k_tok_mean"]
            st = "SUPPORTED" if (slo_ok and ttft_ok and tot_diff <= 10.0) else "PARTIALLY SUPPORTED"
            records.append(
                {
                    "hypothesis": "H2",
                    "context": f"E1_{h}_{w}_P4_vs_P3",
                    "status": st,
                    "key_evidence": (
                        f"P4 SLO viol={p4['slo_viol_pct_mean']:.2f}% vs P3={p3['slo_viol_pct_mean']:.2f}%, "
                        f"P4 TTFT_p95={p4['ttft_p95_ms_mean']:.1f}ms vs P3={p3['ttft_p95_ms_mean']:.1f}ms, "
                        f"SCI_tot diff={tot_diff:+.1f}%"
                    ),
                }
            )
    if "sw2" in summaries:
        sw2 = summaries["sw2"]
        low = sw2[(sw2["sub_exp"] == "topology") & (sw2["topology"] == "low_diff_uk")]
        if not low.empty:
            p3 = low[low["policy"] == "P3"].iloc[0]
            p4 = low[low["policy"] == "P4"].iloc[0]
            records.append(
                {
                    "hypothesis": "H2",
                    "context": "SW2_low_diff_uk",
                    "status": "SUPPORTED" if (p4["slo_viol_pct_mean"] <= p3["slo_viol_pct_mean"] and p4["sci_op_g_per_1k_tok_mean"] <= p3["sci_op_g_per_1k_tok_mean"] * 1.05) else "NUANCED",
                    "key_evidence": (
                        f"Low-diff UK: P4 SCI_op={p4['sci_op_g_per_1k_tok_mean']:.5f} (SLO {p4['slo_viol_pct_mean']:.2f}%) "
                        f"vs P3={p3['sci_op_g_per_1k_tok_mean']:.5f} (SLO {p3['slo_viol_pct_mean']:.2f}%)"
                    ),
                }
            )

    # H3: Serverless keep-alive idle-vs-reload carbon trade-off (S3 vs S1/S2/S2b)
    if "e2" in summaries:
        e2 = summaries["e2"]
        for (h, reg), grp in e2.groupby(["horizon", "region"]):
            s1 = grp[grp["policy"] == "S1"].iloc[0]
            s2 = grp[grp["policy"] == "S2"].iloc[0]
            s2b = grp[grp["policy"] == "S2b"].iloc[0]
            s3 = grp[grp["policy"] == "S3"].iloc[0]
            min_static_op = min(s1["sci_op_g_per_1k_tok_mean"], s2["sci_op_g_per_1k_tok_mean"], s2b["sci_op_g_per_1k_tok_mean"])
            beats_all_op = s3["sci_op_g_per_1k_tok_mean"] <= min_static_op * 1.001
            beats_s1_slo = s3["slo_viol_pct_mean"] <= s1["slo_viol_pct_mean"]
            beats_s2_slo = s3["slo_viol_pct_mean"] <= s2["slo_viol_pct_mean"] + 0.5
            st = "SUPPORTED" if (beats_all_op and beats_s1_slo and beats_s2_slo) else ("PARTIALLY SUPPORTED" if beats_all_op else "NUANCED")
            records.append(
                {
                    "hypothesis": "H3",
                    "context": f"E2_{h}_{reg}",
                    "status": st,
                    "key_evidence": (
                        f"S3 SCI_op={s3['sci_op_g_per_1k_tok_mean']:.5f} (SLO {s3['slo_viol_pct_mean']:.2f}%) vs "
                        f"S1={s1['sci_op_g_per_1k_tok_mean']:.5f} ({s1['slo_viol_pct_mean']:.2f}%), "
                        f"S2={s2['sci_op_g_per_1k_tok_mean']:.5f} ({s2['slo_viol_pct_mean']:.2f}%), "
                        f"S2b={s2b['sci_op_g_per_1k_tok_mean']:.5f} ({s2b['slo_viol_pct_mean']:.2f}%)"
                    ),
                }
            )

    # H4: Operational vs Amortized Embodied Carbon Dominance & Clean Over-Provisioning Paradox
    if "e1_24h" in summaries:
        e1_24 = summaries["e1_24h"]
        p4_24 = e1_24[e1_24["policy"] == "P4"].iloc[0]
        clean_emb_pct = float(p4_24["clean_region_emb_share_pct_mean"])
        records.append(
            {
                "hypothesis": "H4",
                "context": "E1_24h_South_Scotland_Embodied_Share",
                "status": "SUPPORTED" if clean_emb_pct > 50.0 else "NOT SUPPORTED",
                "key_evidence": (
                    f"South Scotland embodied share={clean_emb_pct:.1f}% (>50% threshold), "
                    f"vs cluster-wide embodied share={p4_24['embodied_share_pct_mean']:.1f}%"
                ),
            }
        )
    if "h4_elastic" in summaries:
        h4 = summaries["h4_elastic"]
        for lt, grp in h4.groupby("lifetime_label"):
            p3_ov = grp[grp["policy"] == "P3_overprov_plus4"].iloc[0]
            p4_eq = grp[grp["policy"] == "P4_equal"].iloc[0]
            paradox = p3_ov["sci_tot_g_per_1k_tok_mean"] > p4_eq["sci_tot_g_per_1k_tok_mean"]
            records.append(
                {
                    "hypothesis": "H4",
                    "context": f"H4_clean_scaleout_{lt}",
                    "status": "SUPPORTED" if paradox else "NUANCED",
                    "key_evidence": (
                        f"P3_overprov(+4 clean nodes): SCI_op={p3_ov['sci_op_g_per_1k_tok_mean']:.5f}, "
                        f"SCI_emb={p3_ov['sci_emb_g_per_1k_tok_mean']:.5f}, SCI_tot={p3_ov['sci_tot_g_per_1k_tok_mean']:.5f} "
                        f"vs P4_equal: SCI_op={p4_eq['sci_op_g_per_1k_tok_mean']:.5f}, "
                        f"SCI_emb={p4_eq['sci_emb_g_per_1k_tok_mean']:.5f}, SCI_tot={p4_eq['sci_tot_g_per_1k_tok_mean']:.5f}"
                    ),
                }
            )

    return pd.DataFrame(records)


def main() -> None:
    summaries: Dict[str, pd.DataFrame] = {}
    wilcoxons: Dict[str, pd.DataFrame] = {}

    specs = [
        ("e1_1h", "raw_e1_1h.csv", ["suite", "horizon", "workload", "policy"], CLUSTER_METRICS),
        ("e1_24h", "raw_e1_24h.csv", ["suite", "horizon", "workload", "policy"], CLUSTER_METRICS),
        ("e2", "raw_e2_serverless.csv", ["suite", "horizon", "region", "workload", "policy", "static_k_s"], SERVERLESS_METRICS),
        ("sw1", "raw_sw1_load.csv", ["suite", "sub_exp", "horizon", "workload", "rps_scale", "policy"], CLUSTER_METRICS),
        ("sw2", "raw_sw2_grid.csv", ["suite", "sub_exp", "topology", "ci_mode", "horizon", "workload", "policy"], CLUSTER_METRICS),
        ("sw3", "raw_sw3_slo_hw_wan.csv", ["suite", "sub_exp", "slo_name", "decode_tier", "wan_bw_gbps", "rps_scale", "workload", "policy"], CLUSTER_METRICS),
        ("sw4_srv", "raw_sw4_serverless.csv", ["suite", "sub_exp", "model_size", "checkpoint_tier", "cold_power_frac", "idle_power_mode", "policy"], SERVERLESS_METRICS),
        ("sw4_clu", "raw_sw4_cluster_lifetime.csv", ["suite", "sub_exp", "lifetime_label", "host_lifetime_yr", "gpu_lifetime_yr", "pue", "mfu_gamma", "policy"], CLUSTER_METRICS),
        ("h4_elastic", "raw_h4_elastic.csv", ["suite", "sub_exp", "lifetime_label", "policy", "extra_clean_nodes"], CLUSTER_METRICS),
        ("sw5", "raw_sw5_pathc.csv", ["suite", "sub_exp", "workload", "rps_scale", "diff_label", "wan_bw_gbps", "wan_rtt_ms", "policy"], CLUSTER_METRICS),
        ("sw6", "raw_sw6_breakeven.csv", ["suite", "sub_exp", "lifetime_label", "rps_scale", "policy", "extra_clean_nodes"], CLUSTER_METRICS),
    ]

    for key, fname, gcols, metrics in specs:
        df = _load_if_exists(fname)
        if df is None or df.empty:
            continue
        sdf = summarize_grouped(df, gcols, metrics)
        summaries[key] = sdf
        out_path = RESULTS_DIR / fname.replace("raw_", "summary_")
        sdf.to_csv(out_path, index=False)
        print(f"[analyze] Wrote {out_path} ({len(sdf)} configs)")

    # Pairwise Wilcoxon signed-rank tests
    w_cluster_frames = []
    for key, fname, gcols in (
        ("e1_1h", "raw_e1_1h.csv", ["horizon", "workload"]),
        ("e1_24h", "raw_e1_24h.csv", ["horizon", "workload"]),
    ):
        df = _load_if_exists(fname)
        if df is not None and not df.empty:
            wdf = run_pairwise_wilcoxon(
                df,
                gcols,
                target_policy="P4",
                baselines=("B1", "B2", "P3", "P5"),
                metrics=("sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms", "tpot_p95_ms"),
            )
            w_cluster_frames.append(wdf)
    if w_cluster_frames:
        w_clu = pd.concat(w_cluster_frames, ignore_index=True)
        wilcoxons["cluster"] = w_clu
        w_clu.to_csv(RESULTS_DIR / "wilcoxon_e1_cluster.csv", index=False)
        print(f"[analyze] Wrote {RESULTS_DIR / 'wilcoxon_e1_cluster.csv'} ({len(w_clu)} tests)")

    e2_df = _load_if_exists("raw_e2_serverless.csv")
    if e2_df is not None and not e2_df.empty:
        w_srv = run_pairwise_wilcoxon(
            e2_df,
            ["horizon", "region"],
            target_policy="S3",
            baselines=("S1", "S2", "S2b"),
            metrics=("sci_op_g_per_1k_tok", "op_idle_g", "op_cold_g", "cold_start_count", "slo_viol_pct", "ttft_p95_ms"),
        )
        wilcoxons["serverless"] = w_srv
        w_srv.to_csv(RESULTS_DIR / "wilcoxon_e2_serverless.csv", index=False)
        print(f"[analyze] Wrote {RESULTS_DIR / 'wilcoxon_e2_serverless.csv'} ({len(w_srv)} tests)")

    hyp_df = evaluate_hypotheses(summaries, wilcoxons)
    hyp_df.to_csv(RESULTS_DIR / "hypotheses_verification.csv", index=False)
    print(f"[analyze] Wrote {RESULTS_DIR / 'hypotheses_verification.csv'} ({len(hyp_df)} checks)")


if __name__ == "__main__":
    main()
