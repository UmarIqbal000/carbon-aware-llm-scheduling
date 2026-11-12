# Submission Notes and Author Checklist

## 1. Manuscript Summary
- **Title:** Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation (14 words)
- **Author:** Umar Iqbal (`umar.iqbal.cs28@iilm.edu`, ORCID: `https://orcid.org/0009-0004-3968-4857`)
- **Affiliation:** IILM University, Greater Noida, India
- **Template & Format:** `IEEEtran` (`\documentclass[journal]{IEEEtran}`), compiled locally via MiKTeX 25.4 (`latexmk -pdf`)
- **Compiled Length:** **13 pages** in the clean, spacious reading layout (headers removed, vector Gmail/ORCID badges added, breathable paragraph/table spacing; 0 fatal errors, 0 overfull boxes, 0 undefined citations/references, 0 BibTeX warnings). *(For final IEEE T-SUSC submission, re-enable `\markboth` and tighten spacing if targeting the 12-page `$0`-MOPC threshold.)*
- **Abstract:** **188 whitespace words** (IEEE Computer Society requirement: 100–200 words, free of `\cite{}` citations and display/inline math)
- **Figures, Tables, Equations & References:** `7` vector PDF figures (`figures/fig1_architecture.pdf` through `figures/fig7_sw_sensitivity_embodied.pdf`), `6` tables, `10` numbered/display equations, `47` cited BibTeX entries (`42/47 = 89.4%` from 2022–2026; `23` from 2025–2026; `42 full_text`, `5 abstract_only`)

---

## 2. Candidate Target Venues

Metadata below is verified directly against accessible official publisher pages and APIs documented in [`research/topic_decision.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/research/topic_decision.md).

| Rank & Venue | Publisher & Fit | Page & Abstract Limits | Fee / OA Model | Required LaTeX Class |
|---|---|---|---|---|
| **1. IEEE Transactions on Sustainable Computing (T-SUSC)** *(Primary)* | **IEEE Computer Society** — exact scope match (sustainability, energy efficiency, carbon/optimization for computing infrastructures; hosted in CSDL & IEEE Xplore, Clarivate JCR tracked). | **12 formatted pages** max incl. refs & bios (`$220/page` MOPC above 12 pp.); abstract **100–200 words** (no math/refs). | **Hybrid:** **`$0` OA APC** via traditional subscription (MOPC `$220/page` only if `> 12` pp.); optional Gold OA `$2,800` USD (2026) / `$2,995` USD (2027). | `IEEEtran` (`\documentclass[journal]{IEEEtran}`) — *ready now* |
| **2. IEEE Transactions on Cloud Computing (TCC)** *(Co-Primary / Backup)* | **IEEE Computer Society** — strong fit on cloud/serverless orchestration, scheduling, and distributed evaluation. | **12 formatted pages** max incl. refs & bios (`$220/page` MOPC above 12 pp.); abstract **100–200 words**. | **Hybrid:** **`$0` subscription**; optional Gold OA `$2,800` USD (2026) / `$2,995` USD (2027). | `IEEEtran` — *ready now* |
| **3. Future Generation Computer Systems (FGCS)** | **Elsevier** — strong fit for distributed cloud/serverless and AI architectures; accepts longer manuscripts without IEEE MOPC. | Elsevier *Your Paper Your Way* initial submission (requires Highlights, CRediT, Data Availability; hard page cap *not stated* on accessible non-paywalled page). | **Hybrid:** **`$0` subscription**; OpenAlex historical Gold OA APC `$3,000` USD. | `elsarticle` (requires class conversion) |
| **4. Sustainable Computing: Informatics and Systems (SUSCOM)** | **Elsevier** — exact fit for energy-aware and green cloud/data-center management. | *Your Paper Your Way*; regular article cap *not stated* on accessible non-paywalled page. | **Hybrid:** **`$0` subscription**; OpenAlex historical Gold OA APC `$3,290` USD. | `elsarticle` (requires class conversion) |
| **5. Journal of Cloud Computing (JoCCASA)** | **SpringerOpen / Springer Nature** — cloud architectures and sustainable serverless orchestration (indexed in DOAJ & OpenAlex). | Format page cap *not stated* on HTTP-406 SpringerOpen page; DOAJ notes ~13-week median turnaround. | **Mandatory Gold OA:** `1,490 EUR / 1,890 USD / 1,340 GBP` (waivers available; CC BY). | `sn-jnl` (requires class conversion) |

---

## 3. Overleaf-Ready Bundle (`cloud-paper.zip`)

Upload [`cloud-paper.zip`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/cloud-paper.zip) directly to **Overleaf -> New Project -> Upload Project**:
- **Included files only:**
  - `main.tex`
  - `references.bib`
  - `sections/01_introduction.tex` through `sections/08_conclusion.tex`
  - `figures/fig1_architecture.pdf` through `figures/fig7_sw_sensitivity_embodied.pdf` plus `figures/icon_gmail.pdf` and `figures/icon_orcid.pdf`
- **Compiler setting in Overleaf:** Set compiler to **`pdfLaTeX`** and main document to **`main.tex`**. (`IEEEtran.cls` and all standard packages used in `main.tex` are pre-installed on Overleaf TeX Live.)
- **Excluded intentionally:** `.venv/`, `tools/`, `research/`, `experiments/`, `figures/generate_figures.py`, logs, and build intermediates (`*.aux`, `*.bbl`, `*.blg`, `*.log`, `*.out`, `*.fls`, `*.fdb_latexmk`) to guarantee a clean Overleaf build without extra helper scripts or dataset weight.

---

## 4. Draft Cover Letter (IEEE Transactions on Sustainable Computing)

> **Date:** `[Insert Submission Date]`  
> **To:** Editor-in-Chief, *IEEE Transactions on Sustainable Computing*  
> **Subject:** Manuscript Submission — *"Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation"*  
>
> Dear Editor-in-Chief,  
>
> Please accept for consideration in *IEEE Transactions on Sustainable Computing* the enclosed single-author original manuscript entitled *"Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation"* (`12` double-column `IEEEtran` pages).  
>
> Interactive large language model (LLM) inference splits into compute-bound prefill and memory-bound decode stages whose resource footprints and Service Level Objective (SLO) sensitivities differ fundamentally from conventional stateless cloud microservices. Through a PRISMA-2020 systematic review of `47` recent and foundational studies (`42` published between `2022` and `2026`), this work documents three unbridged structural gaps across cloud carbon scheduling and LLM systems: (`0/6`) phase-disaggregated LLM serving engines integrate grid carbon intensity or amortized embodied hardware emissions, (`0/4`) multi-region carbon schedulers account for key-value (KV) cache wide-area transfer costs, and `78.7%` of reviewed works exclude manufacturing carbon boundaries.  
>
> To resolve this incompatibility, the manuscript formalizes a dual-track control architecture grounded in ISO/IEC 21031:2024 Software Carbon Intensity (SCI) and evaluates it across `2,260` reproducible `SimPy 4.1.2` discrete-event simulation runs driven by open `CC-BY-4.0` Azure LLM inference traces, Azure GreenSKU component tables, UK NESO regional carbon telemetry, and Japan FY2024 TSO grid emission factors. Quantitative experiments show how unconditional cross-region carbon chasing induces severe tail-latency collapse on bursty code workloads, whereas carbon-and-queue-aware hybrid phase routing preserves sub-1% conversational SLO violations while reducing operational SCI by up to `60.8%` (`-54.9%` total lifecycle SCI vs. fixed single-region colocation) and cutting bursty-code SLO violations by up to `86.0%`. On wind-clean grids, embodied emissions account for `93.0%–97.6%` of lifecycle SCI, explaining why idle clean-region over-provisioning increases total carbon footprint despite near-zero operational grid intensity.  
>
> This manuscript is an original single-author work prepared specifically for *IEEE Transactions on Sustainable Computing*, has not been published previously, and is not under consideration elsewhere. In full accordance with IEEE publishing policy, a transparent *Declaration of Generative AI Use* is included prior to the references alongside complete reproducibility documentation (`SimPy` code, parameter sources, datasets, and PRISMA audit logs).  
>
> Thank you for your time and editorial consideration.  
>
> Sincerely,  
> **Umar Iqbal**  
> IILM University, Greater Noida, India  
> Email: `umar.iqbal.cs28@iilm.edu`  
> ORCID: `https://orcid.org/0009-0004-3968-4857`  

---

## 5. Pre-Submission Author Verification Checklist

Before uploading the manuscript to the IEEE Author Portal / ScholarOne, manually complete and verify each item below:

1. **Publicly Archive Code & Data (GitHub Live / Optional Zenodo DOI):**
   - *Data and Code Availability* in [`sections/08_conclusion.tex`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/sections/08_conclusion.tex#L12-L13) now links to `https://github.com/UmarIqbal000/carbon-aware-llm-scheduling`. Before IEEE camera-ready submission, optionally mint a **Zenodo archival DOI** from a GitHub release and add the DOI alongside the repository URL.
2. **Verify Final Preprint & In-Press Bibliographic Updates:**
   - Check arXiv preprints and 2026 accepted papers in [`references.bib`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/references.bib) (`hewage2026carbon`, `yang2025container`, `pan2025inference`, `li2025ecoserve`, `basit2026dualscale`, `li2026revisiting`, `sun2026lacere`, `wang2026festina`, `faiz2024llmcarbon`) to see if formal journal volume/pages or proceedings DOIs have been assigned prior to submission.
3. **Optional Institutional Full-Text Check on 5 Paywalled Papers:**
   - As logged in [`BLOCKERS.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/BLOCKERS.md), `5` references (`roy2026lowcarb`, `calavaro2026offloading`, `gupta2022act`, `sinha2025utilization`, `calheiros2011cloudsim`) returned `HTTP 403` without subscription cookies and are strictly restricted to abstract-level metadata (`abstract_only`). If you have IEEE/ACM/Elsevier/Wiley institutional access at IILM University, skim their full texts before submission to confirm whether any additional experimental nuance is worth expanding.
4. **Manage Page Budget if Re-Targeting IEEE 12-Page Cap:**
   - The current clean reading layout in [`main.pdf`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/main.pdf) spans `13` balanced pages (with running headers disabled and relaxed spacing). For final IEEE T-SUSC submission, exceeding `12` formatted pages triggers IEEE Computer Society's **`$220/page` Mandatory Overlength Page Charge (MOPC)**, so re-apply `\markboth` and compact float/line spacing (plus trim ~8–12 lines if adding an `IEEEbiographynophoto`) to stay at `<= 12` pages.
5. **Confirm IEEE Generative AI Disclosure & Single-Author Statements:**
   - Verify that the *Declaration of Generative AI Use* statement in [`sections/08_conclusion.tex`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/sections/08_conclusion.tex#L5-L6) aligns with IEEE's active guidelines at submission time, read every sentence carefully (especially results and citations), and confirm your **ORCID iD** (`0009-0004-3968-4857`) and affiliation/email (`Umar Iqbal`, `IILM University, Greater Noida, India`, `umar.iqbal.cs28@iilm.edu`) in the submission portal.
6. **Reproducibility Quick Check (Optional Local Run):**
   - To regenerate all figures and confirm simulation determinism from scratch inside `./cloud-paper/`:
     - Run simulations: `.venv\Scripts\python.exe experiments\run_experiments.py`
     - Regenerate statistical tables: `.venv\Scripts\python.exe experiments\analyze_results.py`
     - Regenerate figures: `.venv\Scripts\python.exe figures\generate_figures.py`
     - Recompile PDF: `$env:PATH = "C:\Program Files\Git\usr\bin;$env:PATH"; latexmk -pdf -interaction=nonstopmode main.tex`
