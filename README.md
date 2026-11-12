# Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation

[![ORCID](https://img.shields.io/badge/ORCID-0009--0004--3968--4857-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0004-3968-4857)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](./LICENSE)
[![Paper & Data: CC BY 4.0](https://img.shields.io/badge/Paper%20%26%20Notes-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Simulator](https://img.shields.io/badge/Simulator-SimPy%204.1.2-orange.svg)](./experiments/simulator.py)
[![Paper PDF](https://img.shields.io/badge/Manuscript-main.pdf-red.svg)](./main.pdf)

**Author:** **Umar Iqbal**  
**Affiliation:** IILM University, Greater Noida, India  
**Email:** [umar.iqbal.cs28@iilm.edu](mailto:umar.iqbal.cs28@iilm.edu) · **ORCID:** [https://orcid.org/0009-0004-3968-4857](https://orcid.org/0009-0004-3968-4857)

---

## Abstract & Core Problem

Interactive Large Language Model (LLM) serving splits into two asymmetric phases: compute-bound **prefill** (governed by Time-To-First-Token, TTFT) and memory-bandwidth-bound **decode** (governed by Time-Per-Output-Token, TPOT) linked by a large Key-Value (**KV**) cache. Meanwhile, cloud carbon-aware schedulers optimize across clean/dirty regional electricity grids without modeling multi-megabyte KV WAN transfer costs, LLM phase separation, multi-gigabyte GPU checkpoint cold starts (`10.3–84.0 s`), or hardware manufacturing (**embodied**) carbon.

This repository archives the Revision v2 multi-target paper builds ([`main.pdf`](./main.pdf) IEEE T-SUSC 12 pp., [`main_elsevier.pdf`](./main_elsevier.pdf) `elsarticle`, [`main_anon.pdf`](./main_anon.pdf) anonymized, [`supplement.pdf`](./supplement.pdf)), the PRISMA-2020-guided literature review (`61` retained works), and the deterministic `SimPy 4.1.2` simulation suite (`2,260` main runs across `226` configurations × `10` paired seeds `100..109`, plus `120` 24h trace-tiling ablation runs and `24` anchor validation checks) driven by open **CC-BY-4.0** Azure LLM traces, UK NESO carbon telemetry, Japan FY2024 TSO grid factors, and Azure GreenSKU hardware carbon tables.

---

## System Architecture

### Dual-Track Control Plane (`Track A` Cluster + `Track B` Serverless -> `ISO/IEC 21031:2024 SCI`)

```mermaid
flowchart LR
    T["Open CC-BY-4.0 Traces\nAzure Conv (CV 1.094) & Code (CV 13.152)\nUK NESO + Japan TSO Grid CI (30m)"] --> D1

    subgraph TrackA["Track A: Multi-Region Cluster Dispatch (P4 Hybrid Router)"]
        D1["Prefill & KV Gate\nCheck TTFT Slack + WAN Carbon Crossover"] --> PA["Path A: Local Colocated Spillover"]
        D1 --> PB["Path B: Intra-Region P/D (55% Decode Cap)"]
        D1 --> PC["Path C: Cross-Region P/D (Pruned at 0% on 10G WAN)"]
        D1 --> PD["Path D: Clean Remote DC Execution"]
    end

    subgraph TrackB["Track B: Serverless GPU Keep-Alive (S3 GapHazard)"]
        W["Inter-Arrival EWMA Hazard + Grid CI"] --> KA["Dynamic Keep-Alive k* (1, 5, 10, 30, 60 s)"]
        KA --> COLD["Cold Reload (10.3s SLLM / 48s Safe / 84s PyT) vs. Warm Idle"]
    end

    E["Embodied Lifecycle\nGreenSKU Host + H100/A100/L4\n(4-yr Uniform & 9yr/3yr Sensitivity)"] --> SCI

    PA --> SCI["ISO/IEC 21031:2024 SCI Meter\nSCI_tot = (E * PUE * I + M_emb) / (Tokens / 1000)"]
    PB --> SCI
    PC --> SCI
    PD --> SCI
    COLD --> SCI
```

![Dual-Track Architecture](./assets/fig1_architecture.png)

---

## PRISMA-2020-Guided Literature Review & Honest Gap Audit (`n = 61`)

```mermaid
flowchart TD
    Q["Identification (n = 98)\nStage-1 Surveys + Bounded API Queries + V2 Follow-ups"] --> D["Duplicates Removed (n = 3)"]
    D --> S["Unique Records Screened (n = 95)"]
    S --> EX1["Excluded: Out of Scope (n = 14)"]
    S --> EL["Full-Text & Metadata Assessed (n = 81)"]
    EL --> EX2["Excluded on Eligibility (n = 20)"]
    EL --> INC["Included in Synthesis (n = 61)\n56 Full-Text (91.8%) + 5 Abstract-Only (8.2%)\n56 Works in 2022-2026 (91.8%) | 34 in 2025-2026 (55.7%)"]
```

<p align="center">
  <img src="./assets/fig2_prisma_flow.png" width="46%" alt="PRISMA-2020 Flow Diagram"/>
  <img src="./assets/fig3_taxonomy_heatmap.png" width="49%" alt="Research Gap Matrix"/>
</p>

| Structural Coverage vs. Closest Prior Works | Observed Result | Architectural Implication |
|---|---:|---|
| Phase-disaggregated engine modeling Grid CI & GPU reuse (`GreenLLM`, single GCP cluster) | **`1 / 8`** P/D systems | Does not model cross-region WAN KV gating, host/chassis Share on `>=90%` wind grids, or serverless KA |
| Geo-distributed LLM routers (`Topcu et al.`, `SLIT`, `CarbonRouter`, `Cleanest Grid`) | **`0 / 8`** use P/D or WAN KV transfer | Route whole requests only; omit P/D power-cap disaggregation, embodied lifecycles, and keep-alive |
| Reviewed studies omitting hardware manufacturing (embodied) carbon | **`46 / 61` (`75.4%`)** | Misses factory carbon dominance (`93.0%–97.6%`) on wind-clean grids |
| Implemented systems jointly unifying P/D, WAN KV gates, Host+GPU embodied, & keep-alive | **`0`** prior systems | Motivates joint control-plane simulation (`P4` + `S3`; only `Sisodia 2026` sketches a related agenda with 0 expts.) |

![Corpus Publication Trends](./assets/fig4_publication_trends.png)

---

## Key Simulation Results (`2,260` `SimPy 4.1.2` Runs, `10` Paired Seeds)

### 1. Multi-Region Cluster Carbon–SLO Frontier (`E1`)
- **Conversational traffic (`conv`):** Hybrid router **`P4`** reduces operational SCI by **`60.8%`** (`1h`) and **`60.7%`** (`24h`)—and total lifecycle SCI by **`54.6%–54.9%`**—versus carbon-agnostic colocation `B1` (`p = 0.002`) while keeping SLO violations at **`0.81%–0.82%`** (well inside the `5%` SLA ceiling).
- **Bursty code traffic (`code`, `CV = 13.152`):** Unconditional geographic routing **`P3`** suffers WAN KV stalls (`44.45%–44.57%` SLO violations, `30.7–39.3 s` P95 TTFT). **`P4`** automatically prunes cross-region KV forwarding (`Path C = 0%`) and cuts tail SLO violations by **`85.2%–86.0%`**, tracking the 30-minute future-seeing oracle **`P5`** within **`0.02%`** carbon.

![Experiment E1 Multi-Region Results](./assets/fig5_e1_pareto_paths.png)

### 2. Serverless GPU Keep-Alive Inversion (`E2` & `SW4`)
- **Dirty Grid (`TEPCO`, `581.6 gCO2eq/kWh`):** `GapHazard` (**`S3`**) cuts operational carbon by **`8.0%`** vs. `0 s` (`S1`), `7.0%` vs. `30 s` (`S2`), and `11.0%` vs. `60 s` (`S2b`, `p = 0.002`), trading faster eviction for `28.60%` cold-start SLO violations. Under slower 70B loaders, **`S3`** saves **`23.7%`** (`84 s` PyTorch) to **`30.9%`** (`48 s` Safetensors) operational carbon.
- **Clean Wind Grid (`South Scotland`, `9.75 gCO2eq/kWh`):** Because operational emissions are negligible, **`S3`** extends warm retention selectively, cutting SLO violations by **`32.6%`** vs. `30 s` timeout (`12.99%` vs. `19.29%`, `p = 0.002`).

![Experiment E2 Serverless Results](./assets/fig6_e2_serverless.png)

### 3. Stress Tests & The Clean Scale-Out Paradox (`SW1–SW3`, `H4`)
- **Extreme `3.0x` Load (`SW1`) & Tiered `L4` Decode (`SW3`):** **`P4`** maintains **`2.89%`** SLO violations at `3.0x` load (vs. `71.94%` under `P3` and `54.48%` under `B1`) and **`0.76%`** on memory-constrained `L4` decode nodes (vs. `53.47%` under `P3`).
- **Embodied Scale-Out Paradox (`H4`):** In wind-clean `South Scotland`, embodied manufacturing accounts for **`93.0%`** (cluster) to **`97.6%`** (serverless) of total lifecycle SCI. Adding **4 spare clean-region nodes** (`10` vs. `6`) lowers operational carbon slightly (`0.00837 -> 0.00804`) but **raises total lifecycle carbon by `+32.6%` (`4-yr` life) and `+27.7%` (`9-yr` host / `3-yr` GPU life)**.

![Sensitivity Sweeps and Clean Scale-Out Paradox](./assets/fig7_sw_sensitivity_embodied.png)

---

## Repository Layout

```text
.
├── LICENSE                   # MIT License (code); README notes CC-BY-4.0 for text/notes/data
├── CITATION.cff              # Machine-readable citation metadata
├── .zenodo.json              # Zenodo archive metadata
├── CHANGELOG.md              # Section/line log of all Revision v2 edits & % TODO-VERIFY list
├── Makefile                  # Multi-target LaTeX build (ieee, elsevier, anon, supplement, check)
├── requirements.txt          # Pinned Python dependencies (simpy==4.1.2, numpy==2.5.4, ...)
├── main.pdf                  # Compiled 12-page IEEE T-SUSC manuscript
├── main_elsevier.pdf         # Compiled elsarticle manuscript (FGCS / SUSCOM)
├── main_anon.pdf             # Compiled 12-page double-blind anonymized PDF
├── supplement.pdf            # Online supplement (V2 screening, 24 validation checks, tiling table)
├── cover_letter.md           # Non-open-access traditional journal submission cover letter
├── highlights.md             # Elsevier Research Highlights (<= 85 chars each)
├── references.bib            # 61 verified BibTeX references
├── assets/                   # Rendered PNG previews (fig1–fig7) for GitHub README display
├── sections/                 # Section LaTeX sources (00_abstract.tex – 08_conclusion.tex)
├── figures/                  # Vector PDF figures (fig1–fig7), icons, and generate_figures.py
├── experiments/
│   ├── sim_config.py         # Hardware, grid, SLO, and sweep configurations (seeds 100..109)
│   ├── trace_loader.py       # CC-BY-4.0 Azure, UK NESO, Japan TSO loaders + tiling regimes
│   ├── simulator.py          # SimPy 4.1.2 discrete-event cluster & serverless engine
│   ├── run_experiments.py    # Executes all 226 configs × 10 paired seeds (2,260 runs)
│   ├── run_tiling_ablation.py# 24h Azure block-tiling sensitivity ablation (4 modes × 3 pol. × 10 seeds)
│   ├── validate_simulator.py # 24 quantitative literature-anchor checks (Splitwise, SLLM, Li 2026)
│   ├── analyze_results.py    # Student-t 95% CIs, paired Wilcoxon, rank-biserial r_rb, Cohen d_z
│   ├── audit_consistency.py  # Automated consistency check across CSVs & LaTeX claims
│   ├── reproduce_all.py      # One-command reproduction entry point (default fast or --rerun-sims)
│   ├── parameter_sources.json# Documented hardware & latency provenance
│   ├── DESIGN.md             # Simulation design & hypothesis specification
│   ├── data/                 # Open CC-BY-4.0 traces & DATA_MANIFEST.md
│   └── results/              # Raw, summary, validation_benchmarks.csv, & tiling_ablation_*.csv
├── research/                 # PRISMA search_log.md, sources.csv, comparison matrix, notes/
├── tools/                    # latex_prose_guard.py automated style/dash/AI-tell linter
├── BLOCKERS.md               # Transparent log of paywalled/blocked resources (never bypassed)
└── SETUP_LOG.md              # Local toolchain and verification log
```

---

## Reproducing Everything Locally

### 1. Create Environment & Install Pinned Packages
Requires **Python 3.10+** (verified on `simpy==4.1.2`):
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

### 2. One-Command Verification, Validation, and Figure Generation
To verify all statistics, run all 24 simulator validation checks, regenerate all 7 figures, sync `./assets/`, and audit LaTeX consistency from archived raw CSVs (~10 s):
```bash
python experiments/reproduce_all.py
```
To re-run the entire 2,260-run `SimPy 4.1.2` suite and 120-run 24h trace-tiling ablation from scratch (paired random seeds `100..109`, longest step):
```bash
python experiments/reproduce_all.py --rerun-sims
```

### 3. Compile All LaTeX Targets & Run Prose Checks
```bash
make all       # Builds main.pdf, main_elsevier.pdf, main_anon.pdf, supplement.pdf
make check     # Runs automated LaTeX prose guard across sections/*.tex
```

---

## Datasets & Attribution

All external workload and electricity grid traces are openly licensed under **CC-BY-4.0** (full provenance in [`experiments/data/DATA_MANIFEST.md`](./experiments/data/DATA_MANIFEST.md)):
- **Microsoft Azure LLM Inference Trace & GreenSKU Carbon Data:** `Azure/AzurePublicDataset` and Zenodo [`doi:10.5281/zenodo.10896254`](https://doi.org/10.5281/zenodo.10896254).
- **UK Regional Grid Carbon Intensity (Oct 2025):** [UK NESO Carbon Intensity API](https://api.carbonintensity.org.uk).
- **Japan FY2024 TSO-Level CO2 Emission Factors:** Zenodo [`doi:10.5281/zenodo.18396311`](https://doi.org/10.5281/zenodo.18396311).

---

## Citation

If you use this simulator, PRISMA audit matrix, or findings, please cite:

```bibtex
@unpublished{iqbal2026carbon,
  author = {Umar Iqbal},
  title  = {Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation},
  note   = {IILM University, Greater Noida, India; code and artifacts at \url{https://github.com/UmarIqbal000/carbon-aware-llm-scheduling}},
  year   = {2026}
}
```

---

## License

- **Simulation, Analysis & Plotting Code (`experiments/*.py`, `figures/*.py`):** Licensed under the [**MIT License**](./LICENSE) (`Copyright (c) 2026 Umar Iqbal`).
- **Manuscript Text, Figures & PRISMA Synthesis Artifacts (`sections/`, `figures/*.pdf`, `assets/`, `research/`):** Licensed under [**Creative Commons Attribution 4.0 International (CC BY 4.0)**](https://creativecommons.org/licenses/by/4.0/), compatible with all upstream `CC-BY-4.0` datasets.
