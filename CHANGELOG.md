# Repository Organization & Cleanup (`2026-11-12`)

- Removed stale v1 `cloud-paper.zip` and cleared all 21 LaTeX auxiliary/log files (`*.aux`, `*.bbl`, `*.blg`, `*.log`, `*.out`, `*.spl`) from root via `make clean` plus local `__pycache__` / `figures/_preview` / `tools/test_tex` caches.
- Moved journal submission assets into `submission/` (`cover_letter.md`, `highlights.md`) and process/setup logs into `docs/` (`BLOCKERS.md`, `SETUP_LOG.md`, `SUBMISSION_NOTES.md`).
- Moved v1 intermediate drafting/audit files (`topic_decision.md`, `survey_staging.json`, `synthesis_draft.md`, `fact_check_report.md`, `reference_audit.csv`) into `research/archive/` while keeping active `research/` PRISMA tables and `notes/` in place.
- Updated `README.md`, `combined/NOTES.md`, `.zenodo.json` (`v2.1.0`, 65 works), and `CITATION.cff` (`2.1.0`).

---

# Final Review Fixes Changelog (`final-fixes`)

**Branch:** `final-fixes` (branched from `revision-v2` at `0e068d8`; untouched `main` stays at `c12434e`)  
**Manuscript:** *Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation*  
**Author:** Umar Iqbal (`umar.iqbal.cs28@iilm.edu`, ORCID `0009-0004-3968-4857`)

---

## Items Marked `% TODO-VERIFY`

1. **`references.bib:379` (`wang2026festina`) and `main_supplement.tex:39`:**
   - **Entry:** Wang et al., *"Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs (Extended),"* accepted at ACM SIGOPS ATC 2026 (`arXiv:2606.30391v2`).
   - **Status:** Marked `% TODO-VERIFY: arXiv:2606.30391v2 lists DOI 10.1145/3828523.3857091, but Crossref returned HTTP 404 on 2026-11-12; retain arXiv URL until indexed`. Do not guess or assert a live publisher URL until Crossref indexes it.

---

## PART A. Text, Framing & Literature Fixes

- **A1 — Benchmark-Validated Framing (`00_abstract.tex:1`, `01_introduction.tex:20`, `05_simulation_design.tex:4,101`, `08_conclusion.tex:3`, `cover_letter.md`, `README.md`):** Removed `"hardware-validated"` everywhere (0 hits verified across all `.tex` and `.md` files) and standardized wording to *"validated against published serving benchmarks and held-out scaling trends"* (acknowledging no physical multi-continent GPU telemetry was collected).
- **A2 — Calibration vs. Held-Out Validation Separation (`experiments/validate_simulator.py`, `experiments/results/validation_benchmarks.csv:1-25`, `sections/05_simulation_design.tex:101-102`, `main_supplement.tex` Table S2):**
  - Annotated every check in `validation_benchmarks.csv` with `check_type`: **19 `calibration_anchor`** checks (Splitwise Table IV conv/code anchors, Splitwise Figs. 8–9 power-cap step curve, ServerlessLLM Fig. 6a 2.0–84.0 s loader times) and **5 `held_out`** checks (Li et al. 2026 `B2` vs. `B1` energy and queueing scaling across `0.25x–2.00x` RPS: `-20.01%` to `-30.40%` J/tok, `+11.4%` to `+44.3%` P95 TTFT, `-7.8%` to `-31.6%` P95 TPOT).
  - Rewrote Section V (`subsec:validation`) to report held-out scaling trends separately from constructed calibration anchors and explicitly state modeled TTFT calibration deviations as limitations (`13.73%–14.24%` on H100, `8.81%–9.50%` on A100 from fixed 5–8 ms KV-transfer stalls).
- **A3 — Additional 2025–2026 Literature Audit (`research/`, `references.bib:576-692`, `sections/03_methodology.tex`, `sections/04_taxonomy_synthesis.tex`, `main_supplement.tex` Table S1):**
  - Added 4 verified 2025–2026 systems (`he2025freesh`, `more2026cedar`, `cheng2026greenllm`, `tsiopani2026infactplanner`), expanding the PRISMA corpus from **61 -> 65 works** (`102` identified -> `3` duplicates -> `99` screened -> `14` T/A excluded -> `85` eligibility -> `20` excluded -> `65` included: `60` full-text [92.3%], `5` abstract-only [7.7%]; `50/65` [76.9%] omit embodied carbon; `18/65` [27.7%] preprints = `17` arXiv + `1` ATC 2026).
  - Updated `ozcan2025vidurvessim` (`references.bib:576-587`) from arXiv-only to archival *Euro-Par 2025: Parallel Processing Workshops* (Springer LNCS, 2026, pp. 223–235, DOI `10.1007/978-3-032-19144-1_18`).
  - Distinguished `FREESH` (`he2025freesh` — generalized P/D tuple notation in Eq. 1c while evaluating colocated TP2/TP4/TP8 pools), `Green-LLM` (`cheng2026greenllm` — distinct from `GreenLLM` `shi2024greenllm`), `CEDAR` (`more2026cedar`, DOI `10.1145/3802973.3804457`), and `InFactPlanner` (`tsiopani2026infactplanner`); updated all denominators (`0/11` implemented cross-region carbon schedulers evaluate separated P/D pools with WAN KV transfer gating).
- **A4 — Exact Discrete Wilcoxon Floor (`sections/05_simulation_design.tex:78`, `sections/06_results_discussion.tex:3`, `sections/08_conclusion.tex:5`):** Explained that for $N=10$ paired seeds, $p = 2/2^{10} \approx 0.00195$ is the minimum attainable two-sided exact paired Wilcoxon $p$-value whenever all pairs share sign ($|r_{\text{rb}}| = 1.000$), reported at three decimals as `0.002`.
- **A5 & A6 — Single-Author AI Disclosure & Compliance (`sections/03_methodology.tex:13`, `sections/07_open_challenges_limitations.tex:23`, `sections/08_conclusion.tex:11-26`):** Added explicit single-author generative AI search/coding/editing disclosure aligned with IEEE PSPB Sec. 8.2.1.B.10 (`Acknowledgments` in `main.tex` and `main_anon.tex` without identity leaks) and Elsevier *Declaration of generative AI and AI-assisted technologies in the writing process* (`main_elsevier.tex`).

---

## PART B. New Simulation Sweeps (`SW5` & `SW6`) — Zero Change to Existing Results

All existing `E1`, `E2`, `SW1–SW4`, and `H4` numbers were preserved **unchanged** (bit-exact regression check on `E1 P4 conv seed=100`: `sci_op=0.04051167`, `slo=0.9140`, `pathC=0.0000`). Main experiment suite expanded cleanly from `226` configs (`2,260` runs) -> **`351` configs (`3,510` runs across 10 paired seeds `100–109`)**:

- **B1 — `SW5` Path C Activation Regime Map (`sim_config.py`, `simulator.py`, `run_experiments.py`, `raw_sw5_pathc.csv`, `summary_sw5_pathc.csv`, `fig8_sw5_pathC_heatmap.pdf`, `sections/06_results_discussion.tex:97`, Supplement Table S4):**
  - **690 runs** (`69` configs × `10` seeds) sweeping WAN bandwidth `{10, 25, 100, 400}` Gbps × RTT `{5, 20, 50, 100, 200}` ms across congested `2.0x` `conv` (high $\Delta$CI `South Scotland–TEPCO` and low $\Delta$CI `South Scotland–NW England`), nominal `1.0x` `conv`, and `2.0x` `code`.
  - **Findings:** At `10–25 Gbps` and `>= 20 ms` RTT, `P4` keeps Path C at **`0.000%`**. Even on congested `400 Gbps / 5 ms` `2.0x` `conv` links, Path C reaches at most **`0.308%`** (high $\Delta$CI) and **`0.228%`** (low $\Delta$CI), vs. `<= 0.060%` at `1.0x` nominal load and `<= 0.009%` on `2.0x` `code`, while Path D handles `38.9%–63.0%` of requests.
- **B2 — `SW6` Clean-Region Scale-Out Break-Even Curve (`run_experiments.py`, `raw_sw6_breakeven.csv`, `summary_sw6_breakeven.csv`, `fig7_sw_sensitivity_embodied.pdf` panel (c), `sections/06_results_discussion.tex:98`, Supplement Table S5):**
  - **560 runs** (`56` configs × `10` seeds) comparing equal 6-node clusters vs. $+4$ spare clean `South Scotland` nodes (`P3+4`, `P4+4`) from `1.0x` to `3.0x` UK `conv` RPS under both `4 yr uniform` and `9 yr host / 3 yr GPU` lifetimes.
  - **Findings (`P4+4` vs. `P4_eq`):** Lifecycle $\text{SCI}_{\text{tot}}$ delta shifts from **`+32.66%`** (`4-yr`) / **`+27.76%`** (`9/3-yr`) at `1.00x`, `+26.96%` / `+21.56%` at `1.25x`, and `+13.62%` / `+7.30%` at `1.50x`, crossing break-even near **`1.6x–1.7x` RPS** (`~1.71x` / `~1.61x`), to carbon savings of `-2.59%` / `-9.51%` at `1.75x`, `-13.61%` / `-20.55%` at `2.00x`, `-26.49%` / `-32.99%` at `2.50x`, and **`-30.63%`** / **`-36.45%`** at `3.00x` (cutting SLO violations from `1.17%` to `0.20%`).
- **B3 — Figures Updated (`figures/generate_figures.py`, `assets/*.png`):** Regenerated all 8 vector PDFs and PNG previews via `.venv/Scripts/python.exe experiments/reproduce_all.py` (`fig2`, `fig3`, `fig4` for $n=65$; `fig7` panel (c) replaced with `SW6`; added `fig8_sw5_pathC_heatmap.pdf`).

---

## PART C & D. Page Budget, Supplement Extensions & Combined Package

- **Strict 12-Page IEEE & Anonymous Limits Without Shrinking Fonts/Margins:** Moved non-measured calibrations table (`tab:calibrations`), 12-row trace-tiling table (`tab:tiling_ablation`), and `SW3c` WAN path-mix table (`tab:wan_pathmix`) into `main_supplement.tex` (expanding `supplement.pdf` to 4 pages, Tables **S1–S7**), and tightened repetitive prose across Sections I–VIII while keeping all equations, figures, citations, and numbers intact. Added `\usepackage{lmodern}` to `main_supplement.tex` and `main_elsevier.tex` (eliminating PK bitmap Type 3 fonts).
- **Combined Showcase Package (`cloud-paper/combined/`):** Built `Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf` (**18 pages, 1,814.1 KB**; Cover `p. 1` + verbatim `main.pdf` `pp. 2–13` + bannered `supplement.pdf` `pp. 14–17` + Elsevier Graphical Abstract & Highlights `p. 18`) via `cover.tex`, `supp_banner_overlay.tex`, `elsevier_frontmatter.tex`, and `build_package.py` (`pypdf`), intentionally excluding `main_anon.pdf` and leaving all 4 individual journal PDFs untouched.
- **Verification Snapshot (all passed after final edit):**
  - `make check` (`latex_prose_guard.py --check` across all 9 `sections/*.tex`): **0 AI-tell / dash flags**.
  - `.venv/Scripts/python.exe experiments/reproduce_all.py`: exited `0` (`24` validation checks, `8` vector PDFs, `8` PNGs, `consistency_report.md` 349 lines).
  - `pdfinfo`: `main.pdf` = **12 pp.** (1,044.6 KB); `main_anon.pdf` = **12 pp.** (1,038.1 KB); `main_elsevier.pdf` = **27 pp.** (1,282.1 KB); `supplement.pdf` = **4 pp.** (356.9 KB); `combined/Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf` = **18 pp.** (1,814.1 KB).
  - `pdffonts`: **0 unembedded fonts** across all 5 PDFs; `0` PK bitmap Type 3 fonts in `main_elsevier.pdf` and `supplement.pdf`.
  - Anonymity scan (`pdftotext main_anon.pdf -`): **0 hits** for `Umar`, `Iqbal`, `IILM`, `Greater Noida`, `umar.iqbal`, `0009-0004-3968-4857`, `github.com/UmarIqbal000`.
  - Combined integrity (`pdftotext` pp. 2–13 vs `main.pdf`): **Equal: True** (`73,738` chars); highlights lengths in `highlights.md` / `main_elsevier.tex` / `combined p.18`: **81, 73, 80, 81, 77 chars** (`<= 85` each; fixed `highlights.md` two `(82 chars)` notes to `(81 chars)`).

---

# Revision v2 Changelog

**Branch:** `revision-v2` (branched from untouched `main` commit `c12434e`; release tag `v2-submission`)  
**Manuscript:** *Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation*  
**Author:** Umar Iqbal (`umar.iqbal.cs28@iilm.edu`, ORCID `0009-0004-3968-4857`)

---

## Items Marked `% TODO-VERIFY` (Honesty Disclosure)

1. **`cloud-paper/references.bib:379` (`wang2026festina`) and `cloud-paper/main_supplement.tex:38`:**  
   - **Citation:** Wang et al., *"Festina: Low-Overhead Serverless LLM Inference via Elastic Model Loading,"* accepted at ACM SIGOPS ATC 2026 (`arXiv:2605.05981`).  
   - **Reason:** Formal ACM/Crossref DOI had not yet been indexed in Crossref as of the November 2026 verification pass (`% TODO-VERIFY: Festina ATC'26 proceedings DOI pending indexing; arXiv:2605.05981 verified`).  
   - **Note on previously pending 2026 DOIs resolved in v2:** Formal 2026 Crossref DOIs were verified and added for `sun2026lacere` (`10.1109/ccgrid68966.2026.00034`, CCGrid 2026), `li2026revisiting` (`10.1145/3805621.3807662`, EuroMLSys 2026), and `tian2026greencache` (`10.1145/3788087`, POMACS 2026).

---

## Part A: Novelty Precision, Literature Verification & Corpus Expansion

- **`research/notes/*.md` (14 newly added structured reading notes):** Full-text/HTML audits recorded for `shi2024greenllm`, `topcu2026tension`, `sisodia2026sicp`, `zhang2026context`, `bernhard2026cleanest`, `tian2026greencache`, `moore2025slit`, `ozcan2025vidurvessim`, `nguyen2025sustainable`, `yan2026pdprov`, `jegham2025hungryai`, `zhen2025taming`, `lu2026etcinfer`, and `li2024sprout`.
- **`research/search_log.md` (lines 1–176) & `sections/03_methodology.tex` (lines 1–27):** Logged fresh 2024–Nov 2026 follow-up search strings (`V2-A1`, `V2-AX-EMB`, `V2-AX-KA`, `V2-AX-SCI`, `V2-CR-SL`) and reconciled PRISMA-2020 screening counts from `75 -> 74 -> 63 -> 47` to `98 identified -> 3 duplicates -> 95 screened -> 14 T/A excluded -> 81 eligibility assessed -> 20 excluded -> 61 included` (`56` full-text audited [91.8%] + `5` abstract-only [8.2%]; `56/61` in 2022–2026 [91.8%]; `34/61` in 2025–2026 [55.7%]; `46/61` omitting embodied accounting [75.4%]).
- **`research/sources.csv`, `research/comparison_matrix.csv`, `research/sources_metadata.json`, `references.bib` (lines 470–647):** Expanded corpus from 47 to 61 verified BibTeX works, adding all 14 newly verified 2024–2026 entries.
- **`figures/generate_figures.py` & `figures/fig1..fig7*.pdf` + `assets/fig*.png`:** Updated Fig. 2 (PRISMA flow), Fig. 3 (research gap matrix highlighting GreenLLM in the P/D + Op.+Emb. cell as `1*`), Fig. 4 (2011–Nov 2026 bibliometrics: `n=61`, 75.4% embodied omission, `n=47` empirical split of 38.3% cluster / 27.7% hybrid / 29.8% sim-only / 4.3% abstract-only).
- **`sections/01_introduction.tex` (lines 1–24) & `sections/04_taxonomy_synthesis.tex` (lines 1–133):**
  - Replaced inaccurate `0/6` and `0/4` blanket novelty statements with exact verified counts (`1/8` P/D systems model single-cluster Grid CI + GPU reuse via GreenLLM; `0/8` cross-region carbon schedulers implement P/D separation or WAN KV transfer).
  - Narrowed novelty claim cleanly to the joint intersection of multi-region P/D scheduling + WAN KV transfer gating + host plus GPU embodied amortization + serverless GPU checkpoint keep-alive.
  - Added Table `tab:closest_work` (`sections/04_taxonomy_synthesis.tex:67-91`, 10 closest systems vs. `P4 + S3`) and Subsection IV-C `subsec:closest_comparison` (`sections/04_taxonomy_synthesis.tex:128-133`) explicitly contrasting Topcu et al. (Penn State, `arXiv:2610.14571`), GreenLLM (`arXiv:2412.20322`), CarbonRouter (`arXiv:2610.35230`), and Sisodia (`arXiv:2609.05565`).

---

## Part B: Scientific Honesty, Statistical Rigor & Validation

- **`sections/00_abstract.tex` (line 1, 178 words) & `sections/01_introduction.tex` (lines 1–24):** Framed every contribution explicitly as a trace-driven discrete-event `SimPy` simulation evaluation anchored on published hardware constants rather than a physical cluster deployment.
- **`sections/03_methodology.tex` (lines 1–27) & `sections/07_open_challenges_limitations.tex` (lines 1–24):** Renamed the review *"PRISMA-2020-guided literature review"* (rather than multi-reviewer systematic synthesis), explicitly disclosed single-author screening with AI tool assistance and 5 abstract-only records, and added Limitation 6 (*Search-Strategy and Index Dependence*).
- **`experiments/audit_consistency.py` & `experiments/consistency_report.md` (lines 1–316) & `sections/06_results_discussion.tex` (lines 1–139):**
  - Explained why $N=10$ two-sided paired Wilcoxon tests reach the minimum discrete floor $p = 2/2^{10} \approx 0.0020$ ($W=0$) whenever all 10 paired seeds agree in sign, and reported paired mean differences $\Delta$, 95% Student-$t$ confidence intervals, rank-biserial correlations ($r_{\text{rb}}$), and Cohen's paired effect sizes ($d_z$).
  - Added explicit simulator validation Subsection V-F (`subsec:validation`, `sections/05_simulation_design.tex:120-121`) summarizing all 24 quantitative anchor checks from `experiments/validate_simulator.py` (`experiments/results/validation_benchmarks.csv`) against Splitwise Table IV, Splitwise Figs. 8–9, ServerlessLLM Fig. 6a, and Li et al. (2026) batching crossover.
  - Implemented and ran 24h trace-tiling sensitivity ablation (`experiments/run_tiling_ablation.py`, `experiments/results/tiling_ablation_summary.csv`, 4 regimes × 3 policies × 10 seeds = 120 runs) reported in Subsection V-G (`subsec:tiling_ablation`, `sections/05_simulation_design.tex:123-143`, Table `tab:tiling_ablation`, Supplement Table S3), confirming `P4` operational SCI invariance within 0.12 percentage points (`60.70%–60.82%` vs. `B1`).
  - Explicitly disambiguated Serverless clean-grid `S3` `-32.63%` SLO violation reduction vs. Cluster `H4` `+32.61%` lifecycle `SCI_tot` inflation (`sections/06_results_discussion.tex`), alongside exact `S3` dirty-grid `SCI_op` savings (`-8.05%` vs. `S1`, `-7.03%` vs. `S2`, `-11.02%` vs. `S2b`).
  - Explicitly stated `Path C = 0.00%` at 10–25 Gbps WAN bandwidth (`0.02%` at 100 Gbps `conv`) so spatial gains originate primarily from whole-request clean-grid Path D + local Path A/B fallbacks, backed by Table `tab:wan_pathmix` (`sections/06_results_discussion.tex:100-124`).

---

## Part C: Format, Conciseness & Multi-Target Builds

- **IEEE Target (`main.tex` lines 1–72 -> `main.pdf`):** Tightened layout spacing and vector figure widths to fit strictly within **12 pages** including all 61 references (`Overfull \hbox`: 0, undefined refs/citations: 0).
- **Elsevier Target (`main_elsevier.tex` lines 1–82 -> `main_elsevier.pdf`):** Added `elsarticle` (`preprint,3p,11pt` with automatic `nonatbib` + `cite` fallback if `natbib.sty` is absent offline), `<graphicalabstract>`, and 5 `<highlights>` bullets (`<= 85` chars each), plus conditional `\ifdefined\BUILDELSEVIER\resizebox{\textwidth}{!}{...}` table wrapping (`Overfull \hbox`: 0, undefined refs/citations: 0).
- **Double-Blind Anonymized Target (`main_anon.tex` lines 1–69 -> `main_anon.pdf`):** Omitted author identity, email, affiliation, ORCID, and GitHub URL (`12 pages`, `Overfull \hbox`: 0, verified 0 identity leaks via extracted PDF text check).
- **Online Supplement (`main_supplement.tex` lines 1–117 -> `supplement.pdf`):** 2-page supplement (`Overfull \hbox`: 0) containing V2 PRISMA accounting summary (Table S1), full 24-check `validation_benchmarks.csv` table (Table S2), and full 12-row `tiling_ablation_summary.csv` matrix (Table S3).
- **Prose & Style Audit (`tools/latex_prose_guard.py`):** Abstract tightened to 178 words (`sections/00_abstract.tex:1`); first-person `"I"` voice preserved; zero em-dash (`---`) or AI-filler flags across all 9 files in `sections/*.tex`.
- **Submission Package (`cover_letter.md`, `highlights.md`, `Makefile` lines 1–58):** Added non-open-access traditional-route journal cover letter (`cover_letter.md`), Elsevier highlights (`highlights.md`), and unified `Makefile` targets (`ieee`, `elsevier`, `anon`, `supplement`, `check`, `clean`, `distclean`).

---

## Part D: Reproducibility & Git Workflow

- **`requirements.txt`, `CITATION.cff`, `.zenodo.json`, `README.md`:** Added exact pinned Python dependency versions (`simpy==4.1.2`, etc.), machine-readable citation/Zenodo metadata, documented deterministic seeds `100..109`, and updated `README.md` for `n=61` and v2 scripts.
- **`experiments/reproduce_all.py` (lines 1–71):** Unified entry point reproducing statistical aggregation, 24 validation checks, 7 vector figures, `assets/*.png` previews, and consistency auditing (`--rerun-sims` optional for full SimPy re-execution).
- **Git isolation:** Original compiling v1 artifact left untouched on `main` (`c12434e`); all v2 work committed in structured batches on `revision-v2` with local annotated tag `v2-submission`.
