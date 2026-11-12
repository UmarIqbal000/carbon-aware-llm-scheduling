# Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation

**Author:** Umar Iqbal  
**Affiliation:** IILM University, Greater Noida, India  
**Email:** [umar.iqbal.cs28@iilm.edu](mailto:umar.iqbal.cs28@iilm.edu)  
**ORCID:** [https://orcid.org/0009-0004-3968-4857](https://orcid.org/0009-0004-3968-4857)

---

## Overview

This repository contains the complete single-author research paper, compiled PDF ([`main.pdf`](./main.pdf)), LaTeX source (`IEEEtran`), Overleaf bundle ([`cloud-paper.zip`](./cloud-paper.zip)), PRISMA-2020 systematic review audit (`47` works), and reproducible `SimPy 4.1.2` discrete-event simulation suite (`226` configurations × `10` paired seeds = `2,260` runs) investigating carbon-aware scheduling for phase-disaggregated Large Language Model (LLM) inference across multi-region cloud clusters and serverless GPU pools.

### Key Highlights
- **Systematic PRISMA-2020 Gap Audit (`47` sources, `42` full-text / `5` abstract-only):** Identifies zero overlap (`0/6`) between phase-disaggregated LLM serving systems and grid/embodied carbon accounting, zero (`0/4`) multi-region cloud carbon schedulers modeling wide-area KV-cache transfer costs, and `78.7%` omission of manufacturing ("embodied") emissions.
- **Multi-Region Cluster Dispatch (`E1`, `SW1–SW3`):** Carbon-and-queue-aware hybrid routing (`P4`) cuts operational Software Carbon Intensity (`SCI_op`) by up to **`60.8%`** (`-54.9%` total lifecycle `SCI_tot`, $p=0.002$) on conversational Azure LLM traces at `0.81%–0.82%` SLO violations, while cutting bursty-code tail SLO violations by **`85.2%–86.0%`** compared to unconditional geographic carbon chasing (`P3`).
- **Serverless GPU Keep-Alive (`E2`, `SW4`):** Dynamic hazard-driven keep-alive (`S3`) adapts oppositely across grid carbon regimes—cutting operational carbon by `7.0%–11.0%` on fossil-heavy `TEPCO` (`23.7%–30.9%` under slow `48–84 s` loaders) while cutting SLO violations by `32.6%` vs. static `30 s` timeout on wind-clean `South Scotland`.
- **Clean Scale-Out Paradox (`H4`):** On wind-clean grids (`South Scotland`), amortized embodied hardware emissions constitute **`93.0%–97.6%`** of total lifecycle carbon, causing four spare clean-region nodes (`+4` over-provisioning) to *increase* net lifecycle carbon by **`+27.7%` to `+32.6%`**.

---

## Repository Structure

```text
.
├── main.pdf                  # Compiled 13-page paper PDF
├── main.tex                  # Master IEEEtran LaTeX file
├── references.bib            # 47 verified BibTeX references
├── cloud-paper.zip           # Self-contained Overleaf upload bundle
├── sections/                 # Section-by-section LaTeX sources (01–08)
├── figures/                  # Vector PDF figures (fig1–fig7), icons, and generate_figures.py
├── experiments/
│   ├── sim_config.py         # Hardware, grid, SLO, and sweep configurations
│   ├── trace_loader.py       # CC-BY-4.0 Azure, UK NESO, and Japan TSO loaders
│   ├── simulator.py          # SimPy 4.1.2 discrete-event cluster & serverless engine
│   ├── run_experiments.py    # Executes all 226 configs × 10 seeds (2,260 runs)
│   ├── analyze_results.py    # Computes Student-t 95% CIs, Wilcoxon tests, H1–H4 verdicts
│   ├── parameter_sources.json# Verified parameter provenance
│   ├── DESIGN.md             # Formal simulation equations & sweep design
│   ├── data/                 # Open CC-BY-4.0 traces & DATA_MANIFEST.md
│   └── results/              # All 21 raw, summary, and statistical CSV outputs
├── research/                 # PRISMA screening log, sources.csv, comparison matrix, audit reports
├── BLOCKERS.md               # Transparent log of paywalled/unreachable resources (never bypassed)
├── SETUP_LOG.md              # Environment & toolchain setup log
└── SUBMISSION_NOTES.md       # Target venues, cover letter draft, and pre-submission checklist
```

---

## Reproducing Simulations, Figures, and PDF

### 1. Python Environment
Install Python `3.10+` dependencies:
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install simpy numpy pandas scipy matplotlib seaborn requests bibtexparser pybtex pillow
```

### 2. Run Simulation Suite & Statistical Analysis
```bash
python experiments/run_experiments.py
python experiments/analyze_results.py
```

### 3. Regenerate All Figures
```bash
python figures/generate_figures.py
```

### 4. Compile LaTeX Manuscript
```bash
latexmk -pdf -interaction=nonstopmode main.tex
```
Or upload `cloud-paper.zip` directly to **Overleaf** using the **`pdfLaTeX`** compiler.

---

## Datasets & Attribution
All external traces and hardware carbon tables are open-licensed under **CC-BY-4.0** (full provenance in [`experiments/data/DATA_MANIFEST.md`](./experiments/data/DATA_MANIFEST.md)):
- **Microsoft Azure LLM Inference Trace & GreenSKU Carbon Data:** `Azure/AzurePublicDataset` and Zenodo [`doi:10.5281/zenodo.10896254`](https://doi.org/10.5281/zenodo.10896254).
- **UK Regional Grid Carbon Intensity (Oct 2025):** [UK NESO Carbon Intensity API](https://api.carbonintensity.org.uk).
- **Japan FY2024 TSO-Level CO2 Emission Factors:** Zenodo [`doi:10.5281/zenodo.18396311`](https://doi.org/10.5281/zenodo.18396311).
