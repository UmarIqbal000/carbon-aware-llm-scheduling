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
