"""Consistency, Effect-Size, and Path-Mix Audit Script (Part B3, B6, B7).

Audits all quantitative claims in `./cloud-paper/sections/*.tex`, `./cloud-paper/main.tex`,
and `./cloud-paper/README.md` directly against raw/summary CSV outputs under
`./experiments/results/`. Outputs `./experiments/consistency_report.md` and prints
key exact values for manuscript synchronization.
"""

from __future__ import annotations

from pathlib import Path
import math
import re
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = Path(__file__).resolve().parent / "results"
OUT_MD = Path(__file__).resolve().parent / "consistency_report.md"

T_CRIT_9 = float(stats.t.ppf(0.975, df=9))


def paired_stats(x: np.ndarray, y: np.ndarray) -> dict:
    """Compute paired mean diff with 95% CI, relative diff %, Wilcoxon p, and rank-biserial r."""
    diff = x - y
    n = len(diff)
    m_diff = float(np.mean(diff))
    s_diff = float(np.std(diff, ddof=1))
    ci_hw = T_CRIT_9 * s_diff / math.sqrt(n)
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))
    rel_pct = 100.0 * (x_mean - y_mean) / y_mean if abs(y_mean) > 1e-12 else 0.0
    # Matched-pairs Cohen's d_z and rank-biserial correlation
    d_z = m_diff / s_diff if s_diff > 1e-12 else 0.0
    nz = diff[np.abs(diff) > 1e-12]
    if len(nz) == 0:
        pval, stat, r_rb = 1.0, 0.0, 0.0
    else:
        res = stats.wilcoxon(x, y, alternative="two-sided", zero_method="wilcox")
        stat = float(res.statistic)
        pval = float(res.pvalue)
        # Rank-biserial r from signed ranks W+ and W-
        ranks = stats.rankdata(np.abs(nz))
        w_pos = float(np.sum(ranks[nz > 0]))
        w_neg = float(np.sum(ranks[nz < 0]))
        total_r = w_pos + w_neg
        r_rb = (w_pos - w_neg) / total_r if total_r > 0 else 0.0
    return {
        "target_mean": x_mean,
        "base_mean": y_mean,
        "mean_diff": m_diff,
        "diff_ci95_low": m_diff - ci_hw,
        "diff_ci95_high": m_diff + ci_hw,
        "rel_diff_pct": rel_pct,
        "cohens_dz": d_z,
        "rank_biserial_r": r_rb,
        "wilcoxon_stat": stat,
        "p_value": pval,
    }


def pct_red(base: float, target: float) -> float:
    return 100.0 * (base - target) / base


def main() -> None:
    lines = ["# Quantitative Consistency, Effect-Size & Path-Mix Audit Report", ""]
    lines.append("Generated directly from `./experiments/results/*.csv` (N = 10 paired seeds `100..109`).")
    lines.append("")

    # 1. Load raw CSVs
    e1_1h = pd.read_csv(RESULTS_DIR / "raw_e1_1h.csv")
    e1_24h = pd.read_csv(RESULTS_DIR / "raw_e1_24h.csv")
    e2 = pd.read_csv(RESULTS_DIR / "raw_e2_serverless.csv")
    sw1 = pd.read_csv(RESULTS_DIR / "raw_sw1_load.csv")
    sw2 = pd.read_csv(RESULTS_DIR / "raw_sw2_grid.csv")
    sw3 = pd.read_csv(RESULTS_DIR / "raw_sw3_slo_hw_wan.csv")
    sw4_srv = pd.read_csv(RESULTS_DIR / "raw_sw4_serverless.csv")
    sw4_clu = pd.read_csv(RESULTS_DIR / "raw_sw4_cluster_lifetime.csv")
    h4 = pd.read_csv(RESULTS_DIR / "raw_h4_elastic.csv")

    # Summary check
    lines.append("## 1. E1 Track A Paired Comparisons & Effect Sizes (B3)")
    lines.append("")
    lines.append("| Horizon | Workload | Comparison | Metric | Target Mean | Base Mean | Paired Diff [95% CI] | Rel Diff | Rank-Biserial r | Cohen's d_z | Wilcoxon p |")
    lines.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|")

    for h_lbl, df in (("1h", e1_1h), ("24h", e1_24h)):
        for w in ("conv", "code"):
            sub = df[df["workload"] == w]
            p4 = sub[sub["policy"] == "P4"].sort_values("seed")
            for b_pol in ("B1", "B2", "P3", "P5"):
                b_df = sub[sub["policy"] == b_pol].sort_values("seed")
                merged = pd.merge(p4, b_df, on="seed", suffixes=("_t", "_b"))
                for m in ("sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms"):
                    st = paired_stats(merged[f"{m}_t"].to_numpy(), merged[f"{m}_b"].to_numpy())
                    lines.append(
                        f"| {h_lbl} | {w} | P4 vs {b_pol} | {m} | "
                        f"{st['target_mean']:.5f} | {st['base_mean']:.5f} | "
                        f"{st['mean_diff']:+.5f} [{st['diff_ci95_low']:+.5f}, {st['diff_ci95_high']:+.5f}] | "
                        f"{st['rel_diff_pct']:+.2f}% | {st['rank_biserial_r']:+.3f} | "
                        f"{st['cohens_dz']:+.2f} | {st['p_value']:.4f} |"
                    )

    lines.append("")
    lines.append("## 2. E2 Track B Serverless Paired Comparisons & Exact S3 Gains (B3 + B6)")
    lines.append("")
    lines.append("Note: Verify distinction between S3 operational carbon reduction vs S3 SLO violation reduction!")
    lines.append("")
    lines.append("| Horizon | Region | Policy | SCI_op (g/1k) | SCI_tot (g/1k) | OpExec (g) | OpIdle (g) | OpCold (g) | ColdStarts | SLO Viol (%) | TTFT p95 (ms) |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    e2_grp = e2.groupby(["horizon", "region", "policy"])[
        ["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "op_exec_g", "op_idle_g", "op_cold_g", "cold_start_count", "slo_viol_pct", "ttft_p95_ms"]
    ].mean().reset_index()
    for _, r in e2_grp.iterrows():
        lines.append(
            f"| {r['horizon']} | {r['region']} | {r['policy']} | "
            f"{r['sci_op_g_per_1k_tok']:.5f} | {r['sci_tot_g_per_1k_tok']:.5f} | "
            f"{r['op_exec_g']:.2f} | {r['op_idle_g']:.2f} | {r['op_cold_g']:.2f} | "
            f"{r['cold_start_count']:.1f} | {r['slo_viol_pct']:.2f}% | {r['ttft_p95_ms']:.1f} |"
        )

    lines.append("")
    lines.append("### E2 S3 Paired Stats vs S1, S2, S2b")
    lines.append("")
    lines.append("| Horizon | Region | Comp | Metric | Target Mean | Base Mean | Paired Diff [95% CI] | Rel Diff | Rank-Biserial r | Wilcoxon p |")
    lines.append("|---|---|---|---|---:|---:|---:|---:|---:|---:|")
    for (h, reg), grp in e2.groupby(["horizon", "region"]):
        s3 = grp[grp["policy"] == "S3"].sort_values("seed")
        for b_pol in ("S1", "S2", "S2b"):
            b_df = grp[grp["policy"] == b_pol].sort_values("seed")
            merged = pd.merge(s3, b_df, on="seed", suffixes=("_t", "_b"))
            for m in ("sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms", "cold_start_count"):
                st = paired_stats(merged[f"{m}_t"].to_numpy(), merged[f"{m}_b"].to_numpy())
                lines.append(
                    f"| {h} | {reg} | S3 vs {b_pol} | {m} | "
                    f"{st['target_mean']:.5f} | {st['base_mean']:.5f} | "
                    f"{st['mean_diff']:+.5f} [{st['diff_ci95_low']:+.5f}, {st['diff_ci95_high']:+.5f}] | "
                    f"{st['rel_diff_pct']:+.2f}% | {st['rank_biserial_r']:+.3f} | {st['p_value']:.4f} |"
                )

    # 3. SW3c WAN Bandwidth Path Mix (B7)
    lines.append("")
    lines.append("## 3. SW3c WAN Bandwidth Path-Mix & Performance Breakdown (B7)")
    lines.append("")
    sw3c = sw3[sw3["sub_exp"] == "wan_bw"]
    sw3c_grp = sw3c.groupby(["workload", "rps_scale", "wan_bw_gbps", "policy"])[
        ["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms",
         "kv_wan_gb_per_1k_req", "path_coloc_pct", "path_intra_pd_pct", "path_cross_pd_pct", "path_remote_pd_pct"]
    ].mean().reset_index()
    lines.append("| Workload | RPS | WAN BW | Policy | SCI_op | SLO (%) | TTFT p95 | KV WAN GB/1k | Path A (%) | Path B (%) | Path C (%) | Path D (%) |")
    lines.append("|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in sw3c_grp.iterrows():
        lines.append(
            f"| {r['workload']} | {r['rps_scale']:.1f} | {r['wan_bw_gbps']:.0f} Gbps | {r['policy']} | "
            f"{r['sci_op_g_per_1k_tok']:.5f} | {r['slo_viol_pct']:.2f} | {r['ttft_p95_ms']:.1f} | "
            f"{r['kv_wan_gb_per_1k_req']:.2f} | {r['path_coloc_pct']:.2f} | {r['path_intra_pd_pct']:.2f} | "
            f"{r['path_cross_pd_pct']:.2f} | {r['path_remote_pd_pct']:.2f} |"
        )

    # Also check E1 path mixes!
    lines.append("")
    lines.append("### E1 Path Mixes")
    lines.append("| Horizon | Workload | Policy | Path A (%) | Path B (%) | Path C (%) | Path D (%) | KV WAN GB/1k |")
    lines.append("|---|---|---|---:|---:|---:|---:|---:|")
    for h_lbl, df in (("1h", e1_1h), ("24h", e1_24h)):
        g = df.groupby(["workload", "policy"])[
            ["path_coloc_pct", "path_intra_pd_pct", "path_cross_pd_pct", "path_remote_pd_pct", "kv_wan_gb_per_1k_req"]
        ].mean().reset_index()
        for _, r in g.iterrows():
            lines.append(
                f"| {h_lbl} | {r['workload']} | {r['policy']} | {r['path_coloc_pct']:.2f} | {r['path_intra_pd_pct']:.2f} | "
                f"{r['path_cross_pd_pct']:.2f} | {r['path_remote_pd_pct']:.2f} | {r['kv_wan_gb_per_1k_req']:.2f} |"
            )

    # 4. H4 Clean Scale-out Paradox exact checks (B6: +32.6%?)
    lines.append("")
    lines.append("## 4. H4 Clean Scale-Out Paradox Exact Check (B6)")
    lines.append("")
    h4_grp = h4.groupby(["lifetime_label", "policy"])[
        ["sci_op_g_per_1k_tok", "sci_emb_g_per_1k_tok", "sci_tot_g_per_1k_tok", "embodied_share_pct", "clean_region_emb_share_pct", "dirty_region_emb_share_pct", "slo_viol_pct"]
    ].mean().reset_index()
    lines.append("| Lifetime | Policy | SCI_op | SCI_emb | SCI_tot | Emb Share (%) | Clean Emb (%) | Dirty Emb (%) | SLO (%) |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in h4_grp.iterrows():
        lines.append(
            f"| {r['lifetime_label']} | {r['policy']} | {r['sci_op_g_per_1k_tok']:.5f} | "
            f"{r['sci_emb_g_per_1k_tok']:.5f} | {r['sci_tot_g_per_1k_tok']:.5f} | {r['embodied_share_pct']:.2f} | "
            f"{r['clean_region_emb_share_pct']:.2f} | {r['dirty_region_emb_share_pct']:.2f} | {r['slo_viol_pct']:.2f} |"
        )
    for lt in h4_grp["lifetime_label"].unique():
        sub = h4_grp[h4_grp["lifetime_label"] == lt].set_index("policy")
        ov = sub.loc["P3_overprov_plus4"]
        p4eq = sub.loc["P4_equal"]
        p3eq = sub.loc["P3_equal"]
        b2eq = sub.loc["B2_equal"]
        lines.append(
            f"- **{lt}**: `P3_overprov_plus4` vs `P4_equal` `SCI_tot`: "
            f"{100.0*(ov['sci_tot_g_per_1k_tok']-p4eq['sci_tot_g_per_1k_tok'])/p4eq['sci_tot_g_per_1k_tok']:+.2f}%, "
            f"`SCI_op`: {100.0*(ov['sci_op_g_per_1k_tok']-p4eq['sci_op_g_per_1k_tok'])/p4eq['sci_op_g_per_1k_tok']:+.2f}%; "
            f"vs `P3_equal` `SCI_tot`: {100.0*(ov['sci_tot_g_per_1k_tok']-p3eq['sci_tot_g_per_1k_tok'])/p3eq['sci_tot_g_per_1k_tok']:+.2f}%; "
            f"vs `B2_equal` `SCI_tot`: {100.0*(ov['sci_tot_g_per_1k_tok']-b2eq['sci_tot_g_per_1k_tok'])/b2eq['sci_tot_g_per_1k_tok']:+.2f}%."
        )

    # 5. SW1, SW2, SW3a, SW3b, SW4 key summary checks
    lines.append("")
    lines.append("## 5. Parameter Sweeps Quick Checks (SW1–SW4)")
    lines.append("")
    sw1_g = sw1.groupby(["rps_scale", "policy"])[["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms"]].mean().reset_index()
    lines.append("### SW1 RPS Scale")
    for s_val in sorted(sw1_g["rps_scale"].unique()):
        sub = sw1_g[sw1_g["rps_scale"] == s_val].set_index("policy")
        lines.append(
            f"- RPS={s_val:.2f}x: B1={sub.loc['B1','sci_op_g_per_1k_tok']:.5f} (SLO {sub.loc['B1','slo_viol_pct']:.2f}%), "
            f"B2={sub.loc['B2','sci_op_g_per_1k_tok']:.5f} ({sub.loc['B2','slo_viol_pct']:.2f}%), "
            f"P3={sub.loc['P3','sci_op_g_per_1k_tok']:.5f} ({sub.loc['P3','slo_viol_pct']:.2f}%), "
            f"P4={sub.loc['P4','sci_op_g_per_1k_tok']:.5f} ({sub.loc['P4','slo_viol_pct']:.2f}%), "
            f"P4 vs B1 SCI_op={pct_red(sub.loc['B1','sci_op_g_per_1k_tok'], sub.loc['P4','sci_op_g_per_1k_tok']):.2f}%"
        )

    lines.append("")
    lines.append("### SW2 Topologies & Forecast Noise")
    sw2_t = sw2[sw2["sub_exp"] == "topology"].groupby(["topology", "policy"])[["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct"]].mean().reset_index()
    for topo in sorted(sw2_t["topology"].unique()):
        sub = sw2_t[sw2_t["topology"] == topo].set_index("policy")
        lines.append(
            f"- Topo `{topo}`: B1={sub.loc['B1','sci_op_g_per_1k_tok']:.5f}, P4={sub.loc['P4','sci_op_g_per_1k_tok']:.5f} "
            f"(red vs B1={pct_red(sub.loc['B1','sci_op_g_per_1k_tok'], sub.loc['P4','sci_op_g_per_1k_tok']):.2f}%, P4 SLO={sub.loc['P4','slo_viol_pct']:.2f}%, P3 SLO={sub.loc['P3','slo_viol_pct']:.2f}%)"
        )
    sw2_f = sw2[sw2["sub_exp"] == "forecast_noise"].groupby(["ci_mode", "policy"])[["sci_op_g_per_1k_tok", "slo_viol_pct"]].mean().reset_index()
    for cm in sorted(sw2_f["ci_mode"].unique()):
        sub = sw2_f[sw2_f["ci_mode"] == cm]
        row_str = ", ".join(f"{r['policy']}: {r['sci_op_g_per_1k_tok']:.5f} (SLO {r['slo_viol_pct']:.2f}%)" for _, r in sub.iterrows())
        lines.append(f"- CI mode `{cm}`: {row_str}")

    lines.append("")
    lines.append("### SW3a SLO Tightness & SW3b Decode Tier")
    sw3a = sw3[sw3["sub_exp"] == "slo_tightness"].groupby(["slo_name", "policy"])[["sci_op_g_per_1k_tok", "slo_viol_pct", "ttft_p95_ms"]].mean().reset_index()
    for sn in sorted(sw3a["slo_name"].unique()):
        sub = sw3a[sw3a["slo_name"] == sn].set_index("policy")
        lines.append(
            f"- SLO `{sn}`: B1={sub.loc['B1','sci_op_g_per_1k_tok']:.5f} (SLO {sub.loc['B1','slo_viol_pct']:.2f}%), "
            f"P3={sub.loc['P3','sci_op_g_per_1k_tok']:.5f} ({sub.loc['P3','slo_viol_pct']:.2f}%), "
            f"P4={sub.loc['P4','sci_op_g_per_1k_tok']:.5f} ({sub.loc['P4','slo_viol_pct']:.2f}%)"
        )
    sw3b = sw3[sw3["sub_exp"] == "decode_tier"].groupby(["decode_tier", "policy"])[["sci_op_g_per_1k_tok", "sci_tot_g_per_1k_tok", "embodied_share_pct", "slo_viol_pct"]].mean().reset_index()
    for dt in sorted(sw3b["decode_tier"].unique()):
        sub = sw3b[sw3b["decode_tier"] == dt]
        row_str = ", ".join(f"{r['policy']}: op={r['sci_op_g_per_1k_tok']:.5f} tot={r['sci_tot_g_per_1k_tok']:.5f} slo={r['slo_viol_pct']:.2f}%" for _, r in sub.iterrows())
        lines.append(f"- Tier `{dt}`: {row_str}")

    lines.append("")
    lines.append("### SW4a Checkpoint Tiers & SW4b Lifetimes")
    sw4s_cp = sw4_srv[sw4_srv["sub_exp"] == "checkpoint_tier"].groupby(["model_size", "checkpoint_tier", "policy"])[["sci_op_g_per_1k_tok", "slo_viol_pct", "cold_start_count"]].mean().reset_index()
    for (ms, cp), grp in sw4s_cp.groupby(["model_size", "checkpoint_tier"]):
        sub = grp.set_index("policy")
        lines.append(
            f"- {ms}/{cp}: S1={sub.loc['S1','sci_op_g_per_1k_tok']:.5f} (SLO {sub.loc['S1','slo_viol_pct']:.2f}%, CS {sub.loc['S1','cold_start_count']:.0f}), "
            f"S2={sub.loc['S2','sci_op_g_per_1k_tok']:.5f} ({sub.loc['S2','slo_viol_pct']:.2f}%, CS {sub.loc['S2','cold_start_count']:.0f}), "
            f"S3={sub.loc['S3','sci_op_g_per_1k_tok']:.5f} ({sub.loc['S3','slo_viol_pct']:.2f}%, CS {sub.loc['S3','cold_start_count']:.0f})"
        )

    sw4c_lt = sw4_clu[sw4_clu["sub_exp"] == "lifetime"].groupby(["lifetime_label", "policy"])[["sci_tot_g_per_1k_tok", "embodied_share_pct", "clean_region_emb_share_pct"]].mean().reset_index()
    for lt, grp in sw4c_lt.groupby("lifetime_label"):
        sub = grp.set_index("policy")
        lines.append(
            f"- Lifetime `{lt}`: P4 SCI_tot={sub.loc['P4','sci_tot_g_per_1k_tok']:.5f}, "
            f"emb_share={sub.loc['P4','embodied_share_pct']:.2f}%, clean_emb={sub.loc['P4','clean_region_emb_share_pct']:.2f}%"
        )

    sw5_p = RESULTS_DIR / "raw_sw5_pathc.csv"
    if sw5_p.exists():
        sw5 = pd.read_csv(sw5_p)
        lines.append("")
        lines.append("### SW5 Path C Regime Activation (10 Seeds)")
        sw5_g = sw5.groupby(["sub_exp", "workload", "rps_scale", "diff_label", "wan_bw_gbps", "wan_rtt_ms"])[
            ["path_coloc_pct", "path_intra_pd_pct", "path_cross_pd_pct", "path_remote_pd_pct", "sci_op_g_per_1k_tok", "slo_viol_pct"]
        ].mean().reset_index()
        nz = sw5_g[sw5_g["path_cross_pd_pct"] > 0.001].sort_values("path_cross_pd_pct", ascending=False)
        lines.append(f"- Configs with Path C > 0.001%: {len(nz)}/{len(sw5_g)}, max Path C = {sw5_g['path_cross_pd_pct'].max():.4f}%")
        for _, r in nz.head(12).iterrows():
            lines.append(
                f"  - `{r['sub_exp']}` wl={r['workload']} rps={r['rps_scale']:.1f} {r['diff_label']} "
                f"BW={r['wan_bw_gbps']:.0f} RTT={r['wan_rtt_ms']:.0f}: C={r['path_cross_pd_pct']:.3f}%, "
                f"D={r['path_remote_pd_pct']:.2f}%, op={r['sci_op_g_per_1k_tok']:.5f}, SLO={r['slo_viol_pct']:.2f}%"
            )

    sw6_p = RESULTS_DIR / "raw_sw6_breakeven.csv"
    if sw6_p.exists():
        sw6 = pd.read_csv(sw6_p)
        lines.append("")
        lines.append("### SW6 Clean-Region Scale-Out Break-Even (10 Seeds)")
        sw6_g = sw6.groupby(["lifetime_label", "rps_scale", "policy"])[
            ["sci_op_g_per_1k_tok", "sci_emb_g_per_1k_tok", "sci_tot_g_per_1k_tok", "slo_viol_pct"]
        ].mean().reset_index()
        for lt in sw6_g["lifetime_label"].unique():
            lines.append(f"- Lifetime `{lt}`:")
            for rps_v in sorted(sw6_g["rps_scale"].unique()):
                sub = sw6_g[(sw6_g["lifetime_label"] == lt) & (sw6_g["rps_scale"] == rps_v)].set_index("policy")
                d_p4 = 100.0 * (sub.loc["P4_overprov_plus4", "sci_tot_g_per_1k_tok"] - sub.loc["P4_equal", "sci_tot_g_per_1k_tok"]) / sub.loc["P4_equal", "sci_tot_g_per_1k_tok"]
                lines.append(
                    f"  - RPS={rps_v:.2f}x: P4_eq={sub.loc['P4_equal','sci_tot_g_per_1k_tok']:.5f} (SLO {sub.loc['P4_equal','slo_viol_pct']:.2f}%), "
                    f"P4+4={sub.loc['P4_overprov_plus4','sci_tot_g_per_1k_tok']:.5f} (SLO {sub.loc['P4_overprov_plus4','slo_viol_pct']:.2f}%, {d_p4:+.2f}%), "
                    f"P3_eq={sub.loc['P3_equal','sci_tot_g_per_1k_tok']:.5f} (SLO {sub.loc['P3_equal','slo_viol_pct']:.2f}%), "
                    f"P3+4={sub.loc['P3_overprov_plus4','sci_tot_g_per_1k_tok']:.5f} (SLO {sub.loc['P3_overprov_plus4','slo_viol_pct']:.2f}%)"
                )

    # 6. Check current LaTeX/README numbers for specific recurring flags
    lines.append("")
    lines.append("## 6. Automated Claim Scan on Current Draft Texts")
    lines.append("")
    check_files = [ROOT / "main.tex", ROOT / "README.md"] + sorted((ROOT / "sections").glob("*.tex"))
    patterns = {
        "em_dash_latex": re.compile(r"---"),
        "hardware_validated": re.compile(r"hardware[- ]validated", re.IGNORECASE),
        "claim_0_of_6": re.compile(r"0/6|0\s+of\s+6"),
        "claim_0_of_4": re.compile(r"0/4|0\s+of\s+4"),
        "stale_n47": re.compile(r"\b47\b"),
        "stale_n61": re.compile(r"\b61\b"),
        "stale_32_6": re.compile(r"32\.6"),
        "stale_p_002": re.compile(r"0\.002"),
        "plural_we_our": re.compile(r"\b(we|our|ours|us)\b", re.IGNORECASE),
    }
    for fpath in check_files:
        if not fpath.exists():
            continue
        txt = fpath.read_text(encoding="utf-8", errors="replace")
        hits = {k: len(pat.findall(txt)) for k, pat in patterns.items() if pat.findall(txt)}
        lines.append(f"- `{fpath.relative_to(ROOT)}`: {hits if hits else 'no flags'}")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
