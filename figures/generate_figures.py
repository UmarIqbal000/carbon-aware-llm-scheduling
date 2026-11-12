"""Reproducible publication-quality figure generator for the IEEE T-SUSC manuscript.

Reads strictly from ./cloud-paper/research/*.csv, search_log.md counts, and
./cloud-paper/experiments/results/*.csv. Outputs vector PDFs (>= 8 pt print font,
Okabe-Ito colorblind-safe palette, grayscale-distinct hatching/markers) plus
temporary PNG previews for visual verification.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES_DIR = ROOT / "experiments" / "results"
RESEARCH_DIR = ROOT / "research"
FIG_DIR = ROOT / "figures"
PREVIEW_DIR = FIG_DIR / "_preview"

# Okabe-Ito colorblind-safe palette
OI = {
    "black": "#111827",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "teal": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermilion": "#D55E00",
    "purple": "#CC79A7",
    "darkpurple": "#7E2F5E",
    "grey": "#6B7280",
    "lightgrey": "#E5E7EB",
    "slate": "#374151",
}

POLICY_COLORS = {
    "B1": OI["blue"],
    "B2": OI["orange"],
    "P3": OI["vermilion"],
    "P4": OI["teal"],
    "P5": OI["sky"],
    "S1": OI["blue"],
    "S2": OI["orange"],
    "S2b": OI["purple"],
    "S3": OI["teal"],
}

POLICY_MARKERS = {
    "B1": "s",
    "B2": "^",
    "P3": "D",
    "P4": "o",
    "P5": "v",
}

POLICY_HATCHES = {
    "B1": "",
    "B2": "//",
    "P3": "xx",
    "P4": "",
    "P5": "..",
    "S1": "",
    "S2": "//",
    "S2b": "..",
    "S3": "",
}


def setup_mpl() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 8.5,
            "axes.titlesize": 8.8,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 8.0,
            "ytick.labelsize": 8.0,
            "legend.fontsize": 8.0,
            "figure.titlesize": 9.5,
            "axes.linewidth": 0.7,
            "grid.linewidth": 0.45,
            "lines.linewidth": 1.35,
            "lines.markersize": 4.5,
            "patch.linewidth": 0.6,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.03,
        }
    )


def save_fig(fig: plt.Figure, stem: str, make_preview: bool, tight: bool = False) -> None:
    pdf_path = FIG_DIR / f"{stem}.pdf"
    kw = {"bbox_inches": "tight", "pad_inches": 0.02} if tight else {}
    fig.savefig(pdf_path, format="pdf", **kw)
    if make_preview:
        PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
        fig.savefig(PREVIEW_DIR / f"{stem}.png", dpi=220, **kw)
    plt.close(fig)


def draw_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    facecolor: str,
    edgecolor: str = "#1F2937",
    textcolor: str = "#111827",
    fontsize: float = 8.0,
    bold: bool = False,
    linestyle: str = "-",
    lw: float = 0.85,
    va: str = "center",
    y_offset: float = 0.0,
) -> None:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.015",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        linestyle=linestyle,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2.0,
        y + h / 2.0 + y_offset,
        text,
        ha="center",
        va=va,
        fontsize=fontsize,
        fontweight="bold" if bold else "normal",
        color=textcolor,
        linespacing=1.15,
    )


def draw_arrow(
    ax: plt.Axes,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: str = "#374151",
    lw: float = 0.9,
    ls: str = "-",
    rad: float = 0.0,
) -> None:
    arr = FancyArrowPatch(
        p1,
        p2,
        arrowstyle="-|>,head_length=4.2,head_width=2.6",
        color=color,
        linewidth=lw,
        linestyle=ls,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(arr)


# ---------------------------------------------------------------------------
# Figure 1: Dual-Track Carbon-Aware Phase-Disaggregated LLM & Serverless Arch
# ---------------------------------------------------------------------------
def make_fig1(make_preview: bool) -> None:
    fig = plt.figure(figsize=(7.16, 2.60))
    ax = fig.add_axes([0.005, 0.01, 0.99, 0.98])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    cluster_zone = FancyBboxPatch(
        (0.242, 0.360),
        0.548,
        0.615,
        boxstyle="round,pad=0.008,rounding_size=0.016",
        facecolor="#F8FAFC",
        edgecolor="#94A3B8",
        linewidth=0.8,
        linestyle="--",
    )
    ax.add_patch(cluster_zone)
    ax.text(
        0.516,
        0.962,
        "Track A: Disaggregated Cluster (E1, SW1-SW3, H4)",
        fontsize=8.3,
        fontweight="bold",
        color=OI["blue"],
        ha="center",
        va="top",
    )

    sl_zone = FancyBboxPatch(
        (0.242, 0.035),
        0.548,
        0.285,
        boxstyle="round,pad=0.008,rounding_size=0.016",
        facecolor="#F0FDF4",
        edgecolor="#86EFAC",
        linewidth=0.8,
        linestyle="--",
    )
    ax.add_patch(sl_zone)
    ax.text(
        0.516,
        0.308,
        "Track B: Serverless Keep-Alive (E2, SW4)",
        fontsize=8.3,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
        va="top",
    )

    draw_box(
        ax,
        0.010,
        0.70,
        0.206,
        0.250,
        "Grid CI & Forecasts\nUK NESO (30m), JP TSO\nN./S. Scotland, London,\nTEPCO, Kyushu",
        "#EFF6FF",
        edgecolor=OI["blue"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.010,
        0.385,
        0.206,
        0.255,
        "LLM Request Traces\nAzure Conv (CV 1.09)\n& Code (CV 13.15)\nTTFT/TPOT SLO Gates",
        "#FFF7ED",
        edgecolor=OI["orange"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.010,
        0.045,
        0.206,
        0.270,
        "Embodied Lifecycle\nGreenSKU & LLMCarbon\nHost 9yr / GPU 3yr or 4yr\n(M = 921.6 + GPU kgCO2e)",
        "#FDF2F8",
        edgecolor=OI["darkpurple"],
        fontsize=8.0,
    )

    draw_box(
        ax,
        0.258,
        0.415,
        0.228,
        0.470,
        "Hybrid Dispatcher (P4)\nMin C_op + Queue Risk\n(Eq. 9) + WAN KV Gate\n\nPath A: Coloc. Fallback\nPath B: Intra-DC P->D\nPath C: WAN KV (pruned)\nPath D: Clean Remote DC",
        "#ECFDF5",
        edgecolor=OI["teal"],
        fontsize=8.0,
        lw=1.2,
    )

    draw_box(
        ax,
        0.530,
        0.700,
        0.244,
        0.190,
        "Prefill Pool (Uncapped)\nCompute-Bound Prompt Eval\nBatch (gamma=0.7) -> TTFT",
        "#E0F2FE",
        edgecolor=OI["blue"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.530,
        0.395,
        0.244,
        0.195,
        "Decode Pool (Tiered)\n55% Cap / L4 / A100\nMemory-BW -> TPOT",
        "#E0F2FE",
        edgecolor=OI["blue"],
        fontsize=8.0,
    )

    draw_box(
        ax,
        0.258,
        0.055,
        0.228,
        0.190,
        "GapHazard Policy (S3)\nDynamic K_t vs Static TTL\nIdle Hazard vs Cold Penalty",
        "#ECFDF5",
        edgecolor=OI["teal"],
        fontsize=8.0,
        lw=1.1,
    )
    draw_box(
        ax,
        0.530,
        0.055,
        0.244,
        0.190,
        "Warm / Cold GPU Pool\nSLLM 10.3s vs Safetensors\n48s / PyTorch 84s",
        "#FFFBEB",
        edgecolor=OI["orange"],
        fontsize=8.0,
    )

    draw_box(
        ax,
        0.815,
        0.060,
        0.175,
        0.875,
        "ISO/IEC 21031\nSCI Carbon Meter\n\nOperational:\nE_p + E_d + E_idle\n+ E_KV_WAN + E_cold\n\u00d7 I(r,t)\n\nEmbodied:\nM_node * t_slot / T\n\nOutputs:\nSCI_op, SCI_emb,\nSCI_tot (g/1k tok)",
        "#F3F4F6",
        edgecolor=OI["black"],
        fontsize=8.0,
        lw=1.1,
    )

    draw_arrow(ax, (0.216, 0.81), (0.258, 0.75), color=OI["blue"])
    draw_arrow(ax, (0.216, 0.53), (0.258, 0.61), color=OI["orange"])
    draw_arrow(ax, (0.216, 0.43), (0.258, 0.17), color=OI["orange"])

    ax.plot([0.113, 0.113, 0.902], [0.045, 0.015, 0.015], color=OI["darkpurple"], ls=":", lw=1.15)
    draw_arrow(ax, (0.902, 0.015), (0.902, 0.058), color=OI["darkpurple"], ls=":")

    draw_arrow(ax, (0.486, 0.74), (0.530, 0.79), color=OI["teal"])
    draw_arrow(ax, (0.486, 0.55), (0.530, 0.50), color=OI["teal"])
    draw_arrow(ax, (0.652, 0.700), (0.652, 0.590), color=OI["vermilion"], lw=1.1)
    ax.text(0.662, 0.646, "KV Cache\n(NVLink / WAN)", fontsize=8.0, color=OI["vermilion"], va="center")

    draw_arrow(ax, (0.486, 0.150), (0.530, 0.150), color=OI["teal"])
    draw_arrow(ax, (0.774, 0.79), (0.815, 0.70), color=OI["slate"])
    draw_arrow(ax, (0.774, 0.49), (0.815, 0.50), color=OI["slate"])
    draw_arrow(ax, (0.774, 0.150), (0.815, 0.25), color=OI["slate"])

    save_fig(fig, "fig1_architecture", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 2: Exact PRISMA-2020 Flow Diagram (search_log.md, n=65)
# ---------------------------------------------------------------------------
def make_fig2(make_preview: bool) -> None:
    fig = plt.figure(figsize=(3.50, 2.55))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    draw_box(
        ax,
        0.015,
        0.785,
        0.59,
        0.19,
        "Records Identified (n = 102)\nCh. 1 (16) + Ch. 2 API (44)\n+ Ch. 3 Audit/Bench (42)",
        "#EFF6FF",
        edgecolor=OI["blue"],
        fontsize=8.0,
        bold=True,
    )
    draw_box(
        ax,
        0.015,
        0.54,
        0.59,
        0.16,
        "Records Screened\nTitle & Abstract (n = 99)",
        "#EFF6FF",
        edgecolor=OI["blue"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.015,
        0.295,
        0.59,
        0.16,
        "Full-Text & Metadata\nEligibility Assessed (n = 85)",
        "#EFF6FF",
        edgecolor=OI["blue"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.015,
        0.02,
        0.59,
        0.20,
        "Included in Synthesis (n = 65)\n60 Full-Text (42 peer-rev.,\n17 arXiv, 1 acc. conf. preprint)\n+ 5 Abstract-Only",
        "#ECFDF5",
        edgecolor=OI["teal"],
        fontsize=8.0,
        bold=True,
        lw=1.1,
    )

    draw_box(
        ax,
        0.665,
        0.805,
        0.32,
        0.15,
        "Duplicates\nRemoved (n=3)",
        "#FEF2F2",
        edgecolor=OI["vermilion"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.665,
        0.55,
        0.32,
        0.145,
        "Excluded at\nScreen (n=14)",
        "#FEF2F2",
        edgecolor=OI["vermilion"],
        fontsize=8.0,
    )
    draw_box(
        ax,
        0.665,
        0.255,
        0.32,
        0.24,
        "Excluded at\nEligibility (n=20)\nNo carbon / no\ncloud LLM scope",
        "#FEF2F2",
        edgecolor=OI["vermilion"],
        fontsize=8.0,
    )

    draw_arrow(ax, (0.31, 0.785), (0.31, 0.70), color=OI["blue"])
    draw_arrow(ax, (0.31, 0.54), (0.31, 0.455), color=OI["blue"])
    draw_arrow(ax, (0.31, 0.295), (0.31, 0.22), color=OI["teal"])

    draw_arrow(ax, (0.605, 0.88), (0.665, 0.88), color=OI["vermilion"])
    draw_arrow(ax, (0.605, 0.62), (0.665, 0.62), color=OI["vermilion"])
    draw_arrow(ax, (0.605, 0.375), (0.665, 0.375), color=OI["vermilion"])

    save_fig(fig, "fig2_prisma_flow", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 3: Annotated Heatmap of Phase Awareness x Carbon/Energy Signal (n=54)
# ---------------------------------------------------------------------------
def make_fig3(make_preview: bool) -> None:
    cm = pd.read_csv(RESEARCH_DIR / "comparison_matrix.csv")
    ns = cm[cm["doc_type"] != "survey"].copy()
    assert len(ns) == 54

    row_order = [
        "Disaggregated P/D",
        "Colocated + P/D Variant",
        "Colocated Phase-Aware",
        "Phase-Agnostic LLM",
        "Non-LLM / Generic Workload",
    ]
    row_totals = {r: int((ns["phase_awareness"] == r).sum()) for r in row_order}
    row_labels = [
        f"Disagg. P/D\n(n={row_totals['Disaggregated P/D']})",
        f"Coloc.+P/D\nVar. (n={row_totals['Colocated + P/D Variant']})",
        f"Coloc. Phase\nAware (n={row_totals['Colocated Phase-Aware']})",
        f"Agnostic\nLLM (n={row_totals['Phase-Agnostic LLM']})",
        f"Non-LLM /\nGen. (n={row_totals['Non-LLM / Generic Workload']})",
    ]

    def map_signal(sig: str) -> str:
        if sig.startswith("None"):
            return "Perf / Telemetry"
        if "Local Power" in sig:
            return "Local W/J"
        if sig.startswith("Grid"):
            return "Grid Op. CI*"
        if "Embodied" in sig:
            return "Op. + Embodied*"
        raise ValueError(f"Unmapped signal: {sig}")

    ns["sig_bin"] = ns["carbon_energy_signal"].map(map_signal)
    col_order = ["Perf / Telemetry", "Local W/J", "Grid Op. CI*", "Op. + Embodied*"]
    col_labels = ["Perf /\nTelem.", "Local\nW/J", "Grid\nOp. CI*", "Op. +\nEmb.*"]

    mat = np.zeros((len(row_order), len(col_order)), dtype=int)
    for i, r in enumerate(row_order):
        for j, c in enumerate(col_order):
            mat[i, j] = int(((ns["phase_awareness"] == r) & (ns["sig_bin"] == c)).sum())
    assert mat.sum() == 54

    fig, ax = plt.subplots(figsize=(3.50, 2.35))
    fig.subplots_adjust(left=0.26, right=0.86, top=0.87, bottom=0.16)
    im = ax.imshow(mat, cmap="Blues", aspect="auto", vmin=0, vmax=13)

    ax.set_xticks(np.arange(len(col_order)))
    ax.set_xticklabels(col_labels, fontsize=8.0)
    ax.set_yticks(np.arange(len(row_order)))
    ax.set_yticklabels(row_labels, fontsize=8.0)
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)

    gap_cells = {(0, 2), (1, 2), (1, 3), (2, 3)}
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat[i, j]
            if (i, j) in gap_cells and val == 0:
                rect = plt.Rectangle(
                    (j - 0.46, i - 0.44),
                    0.92,
                    0.88,
                    fill=True,
                    facecolor="#FFF1F2",
                    edgecolor=OI["vermilion"],
                    linewidth=1.2,
                    linestyle="--",
                )
                ax.add_patch(rect)
                txt = "0 (GAP)" if i in (0, 1) else "0"
                ax.text(j, i, txt, ha="center", va="center", fontsize=8.0, fontweight="bold", color=OI["vermilion"])
            elif (i, j) == (0, 3) and val == 1:
                rect = plt.Rectangle(
                    (j - 0.46, i - 0.44),
                    0.92,
                    0.88,
                    fill=False,
                    edgecolor=OI["orange"],
                    linewidth=1.2,
                    linestyle="-",
                )
                ax.add_patch(rect)
                ax.text(j, i, "1*", ha="center", va="center", fontsize=8.5, fontweight="bold", color=OI["black"])
            else:
                color = "white" if val >= 8 else OI["black"]
                ax.text(j, i, f"{val}", ha="center", va="center", fontsize=8.5, fontweight="bold" if val > 0 else "normal", color=color)

    ax.set_title("Research Gap Matrix (n = 54 Non-Survey)", fontsize=8.8, fontweight="bold", pad=6)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=8.0)
    cbar.set_label("# Works", fontsize=8.0)

    save_fig(fig, "fig3_taxonomy_heatmap", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 4: Bibliometric Trends & Empirical Modality (n=65 / n=51)
# ---------------------------------------------------------------------------
def make_fig4(make_preview: bool) -> None:
    s = pd.read_csv(RESEARCH_DIR / "sources.csv")
    cm = pd.read_csv(RESEARCH_DIR / "comparison_matrix.csv")
    m = s.merge(cm[["id", "pillar", "doc_type", "embodied_carbon_considered", "evaluation_platform"]], on="id")
    assert len(m) == 65

    years = sorted(m["year"].unique())
    pillar_counts = m["pillar"].value_counts().to_dict()
    pillar_order = [
        ("c_llm_serving", f"LLM Serving ({pillar_counts['c_llm_serving']})", OI["blue"], ""),
        ("b_carbon_schedulers", f"Carbon Sched. ({pillar_counts['b_carbon_schedulers']})", OI["teal"], "//"),
        ("a_surveys", f"Surveys ({pillar_counts['a_surveys']})", OI["orange"], ".."),
        ("d_modeling_traces_standards", f"Models / Std. ({pillar_counts['d_modeling_traces_standards']})", OI["purple"], "xx"),
        ("e_foundations", f"Foundations ({pillar_counts['e_foundations']})", OI["grey"], ""),
    ]

    fig = plt.figure(figsize=(3.50, 2.85))
    ax1 = fig.add_axes([0.145, 0.585, 0.825, 0.34])
    ax2 = fig.add_axes([0.395, 0.125, 0.575, 0.335])

    x = np.arange(len(years))
    bottom = np.zeros(len(years), dtype=int)
    for col, label, color, hatch in pillar_order:
        vals = np.array([int(((m["year"] == y) & (m["pillar"] == col)).sum()) for y in years])
        ax1.bar(
            x,
            vals,
            bottom=bottom,
            width=0.66,
            color=color,
            edgecolor="#1F2937",
            hatch=hatch,
            label=label,
            linewidth=0.5,
        )
        bottom += vals

    for idx, tot in enumerate(bottom):
        ax1.text(idx, tot + 0.35, str(tot), ha="center", va="bottom", fontsize=8.0, fontweight="bold")

    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontsize=8.0)
    ax1.set_ylabel("Works (n=65)", fontsize=8.3)
    ax1.set_ylim(0, max(bottom) + 3.5)
    ax1.set_title("(a) Publication Timeline by Thematic Pillar", fontsize=8.6, fontweight="bold", loc="left")
    ax1.grid(axis="y", alpha=0.35, linestyle=":")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.95, edgecolor="#D1D5DB", fontsize=7.8, ncol=1, borderpad=0.28, labelspacing=0.22)

    n_emp = int((m["type"] == "empirical").sum())
    assert n_emp == 51

    def eval_bucket(row: pd.Series) -> str:
        if row["id"] in {"roy2026lowcarb", "sinha2025utilization"}:
            return "Abstract-Only (Unverified)"
        if row["id"] in {
            "hanafy2023carbonscaler",
            "souza2023ecovisor",
            "qi2024casa",
            "jiang2024ecolife",
            "sun2026lacere",
            "patel2024splitwise",
            "zhong2024distserve",
            "stojkovic2025dynamollm",
            "stojkovic2025tapas",
            "li2025ecoserve",
            "bernhard2026cleanest",
            "lu2026etcinfer",
            "yan2026pdprov",
            "he2025freesh",
        }:
            return "Hybrid Testbed + Sim."
        if row["id"] in {
            "wiesner2021letswait",
            "sukprasert2024limitations",
            "calavaro2026offloading",
            "gupta2021chasing",
            "gupta2022act",
            "acun2023carbonexplorer",
            "faiz2024llmcarbon",
            "hewage2025aging",
            "calheiros2011cloudsim",
            "topcu2026tension",
            "zhang2026context",
            "moore2025slit",
            "ozcan2025vidurvessim",
            "jegham2025hungryai",
            "more2026cedar",
            "cheng2026greenllm",
            "tsiopani2026infactplanner",
        }:
            return "Trace Sim. / Analytical"
        return "Hardware / Prod. Cluster"

    emp_df = m[m["type"] == "empirical"].copy()
    emp_df["modality"] = emp_df.apply(eval_bucket, axis=1)

    emb_omitted = int((m["embodied_carbon_considered"] == "No").sum())
    emb_incl = int(len(m) - emb_omitted)
    assert emb_omitted == 50 and emb_incl == 15

    cats = [
        f"Emb. Omitted ({len(m)})",
        f"Emb. Included ({len(m)})",
        f"HW Cluster ({n_emp})",
        f"Hybrid Sim ({n_emp})",
        f"Trace/Model ({n_emp})",
        f"Abstract-Only ({n_emp})",
    ]
    counts = [
        emb_omitted,
        emb_incl,
        int((emp_df["modality"] == "Hardware / Prod. Cluster").sum()),
        int((emp_df["modality"] == "Hybrid Testbed + Sim.").sum()),
        int((emp_df["modality"] == "Trace Sim. / Analytical").sum()),
        int((emp_df["modality"] == "Abstract-Only (Unverified)").sum()),
    ]
    pcts = [
        100.0 * emb_omitted / len(m),
        100.0 * emb_incl / len(m),
        100.0 * counts[2] / n_emp,
        100.0 * counts[3] / n_emp,
        100.0 * counts[4] / n_emp,
        100.0 * counts[5] / n_emp,
    ]
    colors = [OI["vermilion"], OI["teal"], OI["blue"], OI["sky"], OI["orange"], OI["grey"]]
    hatches = ["xx", "", "", "//", "..", ""]

    y_pos = np.arange(len(cats))[::-1]
    ax2.barh(y_pos, pcts, height=0.62, color=colors, edgecolor="#1F2937", hatch=hatches, linewidth=0.5)
    ax2.axhline(3.5, color="#9CA3AF", linestyle="--", linewidth=0.8)
    for yp, cnt, pct in zip(y_pos, counts, pcts):
        ax2.text(pct + 1.8, yp, f"{cnt} ({pct:.1f}%)", va="center", ha="left", fontsize=8.0)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(cats, fontsize=8.0)
    ax2.set_xlim(0, 128)
    ax2.set_xticks([0, 25, 50, 75, 100])
    ax2.set_xticklabels(["0", "25", "50", "75", "100"], fontsize=8.0)
    ax2.set_xlabel("Share Within Group (%)", fontsize=8.3)
    ax2.set_title("(b) Embodied Coverage & Empirical Modality", fontsize=8.6, fontweight="bold", loc="left")
    ax2.grid(axis="x", alpha=0.35, linestyle=":")

    save_fig(fig, "fig4_publication_trends", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 5: Experiment E1 Carbon-SLO Pareto & Hybrid Path Routing
# ---------------------------------------------------------------------------
def make_fig5(make_preview: bool) -> None:
    e1_1h = pd.read_csv(RES_DIR / "summary_e1_1h.csv")
    e1_24h = pd.read_csv(RES_DIR / "summary_e1_24h.csv")
    sw1 = pd.read_csv(RES_DIR / "summary_sw1_load.csv")
    w_e1 = pd.read_csv(RES_DIR / "wilcoxon_e1_cluster.csv")

    fig, (ax1, ax2, ax3) = plt.subplots(
        1, 3, figsize=(7.16, 2.34), gridspec_kw={"width_ratios": [1.14, 1.06, 0.96], "wspace": 0.36}
    )
    fig.subplots_adjust(left=0.075, right=0.985, top=0.88, bottom=0.33)

    pols = ["B1", "B2", "P3", "P4", "P5"]
    workloads = ["conv", "code"]
    x_base = np.arange(len(pols))
    width = 0.36
    for w_idx, wl in enumerate(workloads):
        sub = e1_24h[e1_24h["workload"] == wl].set_index("policy").loc[pols]
        offset = -width / 2 if w_idx == 0 else width / 2
        op = sub["sci_op_g_per_1k_tok_mean"].values
        emb = sub["sci_emb_g_per_1k_tok_mean"].values
        tot = sub["sci_tot_g_per_1k_tok_mean"].values
        ci = sub["sci_tot_g_per_1k_tok_ci95"].values
        color_op = OI["blue"] if wl == "conv" else OI["orange"]
        color_emb = "#93C5FD" if wl == "conv" else "#FDE68A"
        hatch = "" if wl == "conv" else "//"
        ax1.bar(
            x_base + offset,
            op,
            width=width,
            color=color_op,
            edgecolor="#1F2937",
            hatch=hatch,
            label=f"{wl} op",
        )
        ax1.bar(
            x_base + offset,
            emb,
            bottom=op,
            width=width,
            color=color_emb,
            edgecolor="#1F2937",
            hatch="..",
            label=f"{wl} emb",
        )
        ax1.errorbar(
            x_base + offset,
            tot,
            yerr=ci,
            fmt="none",
            ecolor=OI["black"],
            elinewidth=0.9,
            capsize=2.0,
        )

    p_val = w_e1[
        (w_e1["horizon"] == "24h")
        & (w_e1["workload"] == "conv")
        & (w_e1["target_policy"] == "P4")
        & (w_e1["baseline_policy"] == "B1")
        & (w_e1["metric"] == "sci_op_g_per_1k_tok")
    ]["p_value"].iloc[0]
    ax1.annotate(
        f"-60.7% op vs B1\n(p={p_val:.3f})",
        xy=(3 - width / 2, 0.044),
        xytext=(2.70, 0.082),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.9),
        fontsize=8.0,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
    )
    ax1.set_xticks(x_base)
    ax1.set_xticklabels(pols, fontsize=8.0)
    ax1.set_ylabel("SCI (gCO2eq/1k tok)", fontsize=8.2)
    ax1.set_ylim(0, 0.114)
    ax1.set_title("(a) E1 24h Lifecycle SCI", fontsize=8.5, fontweight="bold", loc="left")
    ax1.grid(axis="y", alpha=0.35, linestyle=":")
    ax1.legend(loc="upper center", bbox_to_anchor=(0.48, -0.14), ncol=2, fontsize=8.0, frameon=False, columnspacing=0.8)

    for wl, ls, tag in [("conv", "-", "V"), ("code", "--", "C")]:
        sub = e1_1h[e1_1h["workload"] == wl].set_index("policy").loc[["B1", "B2", "P3", "P4"]]
        xs = sub["slo_viol_pct_mean"].values
        ys = sub["sci_tot_g_per_1k_tok_mean"].values
        ax2.plot(xs, ys, linestyle=ls, color=OI["slate"], lw=0.85, alpha=0.7, zorder=1)
        for pol, xv, yv in zip(["B1", "B2", "P3", "P4"], xs, ys):
            ax2.scatter(
                xv,
                yv,
                color=POLICY_COLORS[pol],
                marker=POLICY_MARKERS[pol],
                s=34,
                edgecolor="#111827",
                linewidth=0.5,
                zorder=3,
            )
            offsets = {
                ("conv", "B1"): (1.6, 0.0005),
                ("conv", "B2"): (1.8, -0.0020),
                ("conv", "P3"): (1.6, -0.0040),
                ("conv", "P4"): (1.8, 0.0022),
                ("code", "B1"): (1.6, 0.0022),
                ("code", "B2"): (1.6, 0.0018),
                ("code", "P3"): (-12.5, -0.0068),
                ("code", "P4"): (1.6, -0.0058),
            }
            dx, dy = offsets[(wl, pol)]
            ax2.text(xv + dx, yv + dy, f"{pol}-{tag}", fontsize=8.0, color=OI["black"])

    ax2.axvline(5.0, color=OI["vermilion"], linestyle=":", linewidth=1.0)
    ax2.text(6.6, 0.097, "5% SLO", fontsize=8.0, color=OI["vermilion"], fontweight="bold")
    ax2.text(23.5, 0.079, "V:Conv (-)\nC:Code (--)", fontsize=8.0, color=OI["slate"], bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#D1D5DB", lw=0.6))
    ax2.set_xlabel("SLO Violation Rate (%)", fontsize=8.2)
    ax2.set_ylabel("SCI_tot (gCO2eq/1k)", fontsize=8.2)
    ax2.set_xlim(-2, 49)
    ax2.set_ylim(0.032, 0.106)
    ax2.set_title("(b) 1h Carbon vs. SLO", fontsize=8.5, fontweight="bold", loc="left")
    ax2.grid(True, alpha=0.35, linestyle=":")

    regimes = [
        ("Conv 1h", e1_1h[(e1_1h["workload"] == "conv") & (e1_1h["policy"] == "P4")].iloc[0]),
        ("Conv 24h", e1_24h[(e1_24h["workload"] == "conv") & (e1_24h["policy"] == "P4")].iloc[0]),
        ("Code 1h", e1_1h[(e1_1h["workload"] == "code") & (e1_1h["policy"] == "P4")].iloc[0]),
        ("Code 24h", e1_24h[(e1_24h["workload"] == "code") & (e1_24h["policy"] == "P4")].iloc[0]),
        ("Conv 3x", sw1[(sw1["rps_scale"] == 3.0) & (sw1["policy"] == "P4")].iloc[0]),
    ]
    labels = [r[0] for r in regimes]
    pa = np.array([r[1]["path_coloc_pct_mean"] for r in regimes])
    pb = np.array([r[1]["path_intra_pd_pct_mean"] for r in regimes])
    pd_rem = np.array([r[1]["path_remote_pd_pct_mean"] for r in regimes])

    yr = np.arange(len(labels))[::-1]
    ax3.barh(yr, pa, height=0.58, color=OI["orange"], edgecolor="#1F2937", hatch="//", label="A: Coloc.")
    ax3.barh(yr, pb, left=pa, height=0.58, color=OI["blue"], edgecolor="#1F2937", label="B: Intra")
    ax3.barh(yr, pd_rem, left=pa + pb, height=0.58, color=OI["teal"], edgecolor="#1F2937", hatch="..", label="D: Remote")
    ax3.set_yticks(yr)
    ax3.set_yticklabels(labels, fontsize=8.0)
    ax3.set_xlim(0, 100)
    ax3.set_xlabel("P4 Request Share (%)", fontsize=8.2)
    ax3.set_title("(c) P4 Path Mix (C=0%)", fontsize=8.5, fontweight="bold", loc="left")
    ax3.legend(loc="upper center", bbox_to_anchor=(0.45, -0.32), ncol=2, fontsize=8.0, frameon=False, columnspacing=0.6)
    ax3.grid(axis="x", alpha=0.35, linestyle=":")

    save_fig(fig, "fig5_e1_pareto_paths", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 6: Experiment E2 Serverless Keep-Alive & SW4 Checkpoint Sensitivity
# ---------------------------------------------------------------------------
def make_fig6(make_preview: bool) -> None:
    e2 = pd.read_csv(RES_DIR / "summary_e2_serverless.csv")
    sw4 = pd.read_csv(RES_DIR / "summary_sw4_serverless.csv")
    e2_24 = e2[e2["horizon"] == "24h"].copy()

    fig, (ax1, ax2, ax3) = plt.subplots(
        1, 3, figsize=(7.16, 2.15), gridspec_kw={"width_ratios": [1.0, 1.0, 1.06], "wspace": 0.34}
    )
    fig.subplots_adjust(left=0.075, right=0.985, top=0.87, bottom=0.22)

    regions = ["TEPCO", "North Scotland", "South Scotland"]
    reg_short = ["TEPCO\n(580g)", "N.Scot\n(35.7g)", "S.Scot\n(9.8g)"]
    pols = ["S1", "S2", "S2b", "S3"]
    x = np.arange(len(regions))
    w = 0.19

    for i, pol in enumerate(pols):
        sub = e2_24[e2_24["policy"] == pol].set_index("region").loc[regions]
        vals = sub["sci_op_g_per_1k_tok_mean"].values
        ci = sub["sci_op_g_per_1k_tok_ci95"].values
        off = (i - 1.5) * w
        ax1.bar(x + off, vals, width=w, color=POLICY_COLORS[pol], edgecolor="#1F2937", hatch=POLICY_HATCHES[pol], label=pol)
        ax1.errorbar(x + off, vals, yerr=ci, fmt="none", ecolor=OI["black"], elinewidth=0.8, capsize=1.8)

    ax1.annotate(
        "-8.0% vs S1\n(p=0.002)",
        xy=(0 + 1.5 * w, 0.107),
        xytext=(1.15, 0.082),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.9),
        fontsize=8.0,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
    )
    ax1.text(2.0, 0.025, "S.Scot\n97.6% Emb.", ha="center", fontsize=8.0, fontweight="bold", color=OI["darkpurple"])
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_short, fontsize=8.0)
    ax1.set_ylabel("SCI_op (gCO2eq/1k)", fontsize=8.2)
    ax1.set_ylim(0, 0.165)
    ax1.set_title("(a) E2 24h Operational SCI", fontsize=8.5, fontweight="bold", loc="left")
    ax1.grid(axis="y", alpha=0.35, linestyle=":")
    ax1.legend(loc="upper right", fontsize=8.0, ncol=2, frameon=True, borderpad=0.25, labelspacing=0.2, columnspacing=0.6)

    for i, pol in enumerate(pols):
        sub = e2_24[e2_24["policy"] == pol].set_index("region").loc[regions]
        vals = sub["slo_viol_pct_mean"].values
        ci = sub["slo_viol_pct_ci95"].values
        off = (i - 1.5) * w
        ax2.bar(x + off, vals, width=w, color=POLICY_COLORS[pol], edgecolor="#1F2937", hatch=POLICY_HATCHES[pol])
        ax2.errorbar(x + off, vals, yerr=ci, fmt="none", ecolor=OI["black"], elinewidth=0.8, capsize=1.8)

    ax2.annotate(
        "-32.6% SLO\nvs S2",
        xy=(2 + 1.5 * w, 13.5),
        xytext=(2.10, 26.5),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.9),
        fontsize=8.0,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
        bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.85),
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(reg_short, fontsize=8.0)
    ax2.set_xlim(-0.52, 2.62)
    ax2.set_ylabel("SLO Violation Rate (%)", fontsize=8.2)
    ax2.set_ylim(0, 48)
    ax2.set_title("(b) E2 24h Cold-Start SLO", fontsize=8.5, fontweight="bold", loc="left")
    ax2.grid(axis="y", alpha=0.35, linestyle=":")

    tiers = [
        ("llama2_70b", "pytorch", "70B\nPyT\n(84s)"),
        ("llama2_70b", "safetensors", "70B\nSafe\n(48s)"),
        ("llama2_70b", "serverlessllm", "70B\nSLLM\n(10.3s)"),
        ("opt_13b", "serverlessllm", "13B\nSLLM\n(2.0s)"),
    ]
    ckpt_df = sw4[sw4["sub_exp"] == "checkpoint_tier"]
    xt = np.arange(len(tiers))
    wt = 0.25
    for idx_p, pol in enumerate(["S1", "S2", "S3"]):
        vals = []
        cis = []
        for mod, tier, _ in tiers:
            r = ckpt_df[(ckpt_df["model_size"] == mod) & (ckpt_df["checkpoint_tier"] == tier) & (ckpt_df["policy"] == pol)].iloc[0]
            vals.append(r["sci_op_g_per_1k_tok_mean"])
            cis.append(r["sci_op_g_per_1k_tok_ci95"])
        off = (idx_p - 1.0) * wt
        ax3.bar(xt + off, vals, width=wt, color=POLICY_COLORS[pol], edgecolor="#1F2937", hatch=POLICY_HATCHES[pol], label=pol)
        ax3.errorbar(xt + off, vals, yerr=cis, fmt="none", ecolor=OI["black"], elinewidth=0.8, capsize=1.8)

    ax3.set_xticks(xt)
    ax3.set_xticklabels([t[2] for t in tiers], fontsize=8.0)
    ax3.set_ylabel("SCI_op (gCO2eq/1k)", fontsize=8.2)
    ax3.set_ylim(0, 0.54)
    ax3.set_title("(c) SW4 Loaders (1h TEPCO)", fontsize=8.5, fontweight="bold", loc="left")
    ax3.grid(axis="y", alpha=0.35, linestyle=":")
    ax3.legend(loc="upper right", fontsize=8.0, frameon=True, borderpad=0.25, labelspacing=0.2)

    save_fig(fig, "fig6_e2_serverless", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 7: Sensitivity Sweeps (SW1 Load, SW3 Decode Tier/WAN, H4 Scale-Out)
# ---------------------------------------------------------------------------
def make_fig7(make_preview: bool) -> None:
    sw1 = pd.read_csv(RES_DIR / "summary_sw1_load.csv")
    sw3 = pd.read_csv(RES_DIR / "summary_sw3_slo_hw_wan.csv")
    h4 = pd.read_csv(RES_DIR / "summary_h4_elastic.csv")

    fig, (ax1, ax2, ax3) = plt.subplots(
        1, 3, figsize=(7.16, 2.34), gridspec_kw={"width_ratios": [1.05, 1.05, 1.05], "wspace": 0.34}
    )
    fig.subplots_adjust(left=0.065, right=0.985, top=0.87, bottom=0.33)

    scales = sorted(sw1["rps_scale"].unique())
    for pol in ["B1", "B2", "P3", "P4"]:
        sub = sw1[sw1["policy"] == pol].set_index("rps_scale").loc[scales]
        ax1.errorbar(scales, sub["slo_viol_pct_mean"], yerr=sub["slo_viol_pct_ci95"], color=POLICY_COLORS[pol], marker=POLICY_MARKERS[pol], label=pol, capsize=2.0)
    ax1.axhline(5.0, color=OI["vermilion"], linestyle=":", linewidth=1.0)
    ax1.text(0.55, 8.0, "5% SLO", fontsize=8.0, color=OI["vermilion"], fontweight="bold")
    ax1.annotate(
        "P4: 2.89%\nat 3.0x",
        xy=(3.0, 2.89),
        xytext=(2.16, 25.0),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.9),
        fontsize=8.0,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
    )
    ax1.set_xticks(scales)
    ax1.set_xticklabels([f"{s:.1f}x" for s in scales], fontsize=8.0)
    ax1.set_xlabel("Load Scale (Conv 1h)", fontsize=8.2)
    ax1.set_ylabel("SLO Violation Rate (%)", fontsize=8.2)
    ax1.set_ylim(-2, 80)
    ax1.set_title("(a) SW1 Load Stress", fontsize=8.5, fontweight="bold", loc="left")
    ax1.grid(True, alpha=0.35, linestyle=":")
    ax1.legend(loc="upper left", fontsize=8.0, frameon=True, borderpad=0.25, labelspacing=0.2)

    tiers = ["L4_72W_decode", "A100_400W", "H100_cap55", "H100_uncap"]
    t_labels = ["L4", "A100", "H100\nCap55", "H100\nUncap"]
    xt = np.arange(len(tiers))
    wt = 0.25
    sub_tier = sw3[sw3["sub_exp"] == "decode_tier"]
    for idx_p, pol in enumerate(["B2", "P3", "P4"]):
        vals = []
        cis = []
        for t in tiers:
            r = sub_tier[(sub_tier["decode_tier"] == t) & (sub_tier["policy"] == pol)].iloc[0]
            vals.append(r["slo_viol_pct_mean"])
            cis.append(r["slo_viol_pct_ci95"])
        off = (idx_p - 1.0) * wt
        ax2.bar(xt + off, vals, width=wt, color=POLICY_COLORS[pol], edgecolor="#1F2937", hatch=POLICY_HATCHES[pol], label=pol)
        ax2.errorbar(xt + off, vals, yerr=cis, fmt="none", ecolor=OI["black"], elinewidth=0.8, capsize=1.8)

    ax2.axhline(5.0, color=OI["vermilion"], linestyle=":", linewidth=1.0)
    ax2.annotate(
        "P4 on L4:\n0.76% SLO",
        xy=(0 + wt, 1.2),
        xytext=(1.25, 31.0),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.9),
        fontsize=8.0,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
    )
    ax2.set_xticks(xt)
    ax2.set_xticklabels(t_labels, fontsize=8.0)
    ax2.set_ylabel("SLO Violation Rate (%)", fontsize=8.2)
    ax2.set_ylim(0, 62)
    ax2.set_title("(b) SW3 Decode Tier", fontsize=8.5, fontweight="bold", loc="left")
    ax2.grid(axis="y", alpha=0.35, linestyle=":")
    ax2.legend(loc="upper right", fontsize=8.0, frameon=True, borderpad=0.25, labelspacing=0.2)

    sw6 = pd.read_csv(RES_DIR / "summary_sw6_breakeven.csv")
    rps_vals = sorted(sw6["rps_scale"].unique())
    curves = [
        ("4yr_unif", "P4_equal", "4yr 6n", OI["blue"], "-", "o"),
        ("4yr_unif", "P4_overprov_plus4", "4yr 10n", OI["vermilion"], "-", "s"),
        ("9yr_host_3yr_gpu", "P4_equal", "9/3 6n", OI["teal"], "--", "^"),
        ("9yr_host_3yr_gpu", "P4_overprov_plus4", "9/3 10n", OI["purple"], "--", "D"),
    ]
    for lt, pol, lbl, col, ls, mk in curves:
        sub = sw6[(sw6["lifetime_label"] == lt) & (sw6["policy"] == pol)].set_index("rps_scale").loc[rps_vals]
        ax3.errorbar(
            rps_vals,
            sub["sci_tot_g_per_1k_tok_mean"],
            yerr=sub["sci_tot_g_per_1k_tok_ci95"],
            color=col,
            linestyle=ls,
            marker=mk,
            markersize=3.8,
            capsize=1.8,
            label=lbl,
        )

    ax3.axvline(1.71, color=OI["slate"], linestyle=":", linewidth=0.9)
    ax3.text(1.74, 0.0218, "~1.7x\ncross", fontsize=7.5, color=OI["slate"], fontweight="bold")
    ax3.annotate(
        "+32.7%\n@ 1.0x",
        xy=(1.0, 0.0230),
        xytext=(1.18, 0.0242),
        fontsize=7.5,
        fontweight="bold",
        color=OI["vermilion"],
        ha="left",
    )
    ax3.annotate(
        "-30.6% (4yr)\n-36.5% (9/3)",
        xy=(3.0, 0.00896),
        xytext=(2.18, 0.0052),
        arrowprops=dict(arrowstyle="->", color=OI["teal"], lw=0.8),
        fontsize=7.4,
        fontweight="bold",
        color=OI["teal"],
        ha="center",
    )
    ax3.set_xticks([1.0, 1.5, 2.0, 2.5, 3.0])
    ax3.set_xticklabels([f"{s:.1f}x" for s in (1.0, 1.5, 2.0, 2.5, 3.0)], fontsize=8.0)
    ax3.set_xlabel("Load Scale (Conv 1h, UK)", fontsize=8.2)
    ax3.set_ylabel("Total SCI (gCO2eq/1k)", fontsize=8.2)
    ax3.set_ylim(0.003, 0.0275)
    ax3.set_title("(c) SW6 Scale-Out Break-Even", fontsize=8.5, fontweight="bold", loc="left")
    ax3.grid(True, alpha=0.35, linestyle=":")
    ax3.legend(loc="upper center", bbox_to_anchor=(0.48, -0.24), fontsize=7.6, frameon=False, ncol=2, columnspacing=0.7)

    save_fig(fig, "fig7_sw_sensitivity_embodied", make_preview, tight=False)


# ---------------------------------------------------------------------------
# Figure 8: SW5 Path C Cross-Region Activation Regime (BW x RTT)
# ---------------------------------------------------------------------------
def make_fig8(make_preview: bool) -> None:
    sw5 = pd.read_csv(RES_DIR / "summary_sw5_pathc.csv")
    bws = [400.0, 100.0, 25.0, 10.0]
    rtts = [5.0, 20.0, 50.0, 100.0, 200.0]

    panels = [
        ("bw_rtt_high_cong", "(a) High dCI (2.0x Conv)"),
        ("bw_rtt_low_cong", "(b) Low dCI (2.0x Conv)"),
    ]

    fig, axes = plt.subplots(
        1, 2, figsize=(3.54, 2.18), gridspec_kw={"width_ratios": [1.0, 1.0], "wspace": 0.16}
    )
    fig.subplots_adjust(left=0.145, right=0.84, top=0.84, bottom=0.22)

    im_ref = None
    for ax_idx, (sub_exp, title) in enumerate(panels):
        ax = axes[ax_idx]
        sub = sw5[sw5["sub_exp"] == sub_exp]
        mat = np.zeros((len(bws), len(rtts)), dtype=float)
        for i, bw in enumerate(bws):
            for j, rtt in enumerate(rtts):
                row = sub[(sub["wan_bw_gbps"] == bw) & (sub["wan_rtt_ms"] == rtt)].iloc[0]
                mat[i, j] = float(row["path_cross_pd_pct_mean"])
        im = ax.imshow(mat, cmap="YlGnBu", aspect="auto", vmin=0.0, vmax=0.32)
        im_ref = im
        ax.set_xticks(np.arange(len(rtts)))
        ax.set_xticklabels([f"{int(r)}" for r in rtts], fontsize=7.4)
        ax.set_yticks(np.arange(len(bws)))
        if ax_idx == 0:
            ax.set_yticklabels([f"{int(b)}G" for b in bws], fontsize=7.6)
            ax.set_ylabel("WAN Bandwidth", fontsize=8.0)
        else:
            ax.set_yticklabels([])
        ax.set_xlabel("WAN RTT (ms)", fontsize=7.8)
        ax.set_title(title, fontsize=8.0, fontweight="bold", loc="left", pad=4)
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)

        for i in range(len(bws)):
            for j in range(len(rtts)):
                val = mat[i, j]
                txt_col = "white" if val >= 0.18 else OI["black"]
                lbl = "0" if val < 0.0005 else f"{val:.2f}".lstrip("0")
                ax.text(j, i, lbl, ha="center", va="center", fontsize=6.6, fontweight="bold" if val >= 0.10 else "normal", color=txt_col)

    cax = fig.add_axes([0.865, 0.22, 0.032, 0.62])
    cbar = fig.colorbar(im_ref, cax=cax)
    cbar.ax.tick_params(labelsize=7.4)
    cbar.set_label("Path C (%)", fontsize=7.8)

    save_fig(fig, "fig8_sw5_pathC_heatmap", make_preview, tight=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-preview", action="store_true", help="Skip PNG preview generation")
    args = parser.parse_args()

    setup_mpl()
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    make_preview = not args.no_preview

    make_fig1(make_preview)
    make_fig2(make_preview)
    make_fig3(make_preview)
    make_fig4(make_preview)
    make_fig5(make_preview)
    make_fig6(make_preview)
    make_fig7(make_preview)
    make_fig8(make_preview)
    print("Generated 8 vector PDFs in", FIG_DIR)


if __name__ == "__main__":
    main()
