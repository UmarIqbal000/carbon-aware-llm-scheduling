# Fact-Check and Citation Verification Report (Pre-Humanizer Audit)

**Auditor:** Agent 6 (Citation Verifier and Fact-Checker)  
**Scope:** `./cloud-paper/references.bib`, `./cloud-paper/main.tex`, `./cloud-paper/sections/01_introduction.tex`–`08_conclusion.tex`, `./cloud-paper/experiments/results/*.csv`, `./cloud-paper/experiments/sim_config.py`, `./cloud-paper/experiments/parameter_sources.json`, `./cloud-paper/research/notes/*.md`, `./cloud-paper/research/sources_metadata.json`, `./cloud-paper/research/comparison_matrix.csv`, and `./cloud-paper/research/pdfs/*.pdf`.  
**Deliverables Produced/Updated:**
- `./cloud-paper/research/reference_audit.csv` (47 entries)
- `./cloud-paper/research/fact_check_report.md` (this report)
- Audited & recompiled manuscript: `./cloud-paper/main.pdf` (12 pages, 0 errors, 0 undefined citations/references, 0 overfull `\hbox`es)

---

## 1. Programmatic Reference Verification Summary (`47/47`)

All 47 entries in `./cloud-paper/references.bib` were audited programmatically against live authoritative APIs (`Crossref`, `OpenAlex`, `arXiv Atom API`), publisher/standards/repository HTTP endpoints (IEEE, ACM, Elsevier, Springer, ACL Anthology, USENIX, NIST, Green Software Foundation, GitHub AzurePublicDataset), and locally archived full-text PDFs/documentation.

| Metric | Result | Status |
|---|---:|---|
| Total BibTeX entries audited | 47 | PASS |
| `VERIFIED` (exact metadata match) | 45 | PASS |
| `FIXED` (corrected in `references.bib` against Crossref/OpenAlex) | 2 | PASS |
| `REMOVED` (unverifiable entries) | 0 | PASS |
| Missing `\cite{}` keys in `main.tex` + `sections/*.tex` | 0 (`47` cited / `47` in `.bib`) | PASS |
| Uncited BibTeX entries | 0 | PASS |
| Duplicate BibTeX keys / duplicate DOIs | 0 / 0 | PASS |
| Recency (`2022–2026`, target `>= 60%`) | 42 / 47 (**89.4%**) | PASS |
| Ultra-recent (`2025–2026`) | 23 / 47 (**48.9%**) | PASS |
| Back-matter & trace links (Zenodo `10896254`, Zenodo `18396311`, GitHub `AzurePublicDataset`, UK NESO API) | HTTP 200 | PASS |

### BibTeX Entries Fixed (`status = FIXED`)
1. `calavaro2026offloading` (`10.1016/j.future.2026.108670`): Corrected title phrasing `"Edge-Cloud Continuum"` $\rightarrow$ `"cloud-to-edge continuum"` to match Crossref and OpenAlex verbatim.
2. `sinha2025utilization` (`10.1145/3757892.3757903`): Corrected title `"{LLM} Inference"` $\rightarrow$ `"Inference Serving"` to match Crossref and OpenAlex verbatim.

### Metadata Verification Notes (`VERIFIED`)
- `miao2025serving` (`10.1145/3754448`): Kept `year = {2025}` (Crossref `published-online=[[2025, 9, 4]]`, `published-print=[[2026, 1, 31]]`; local ACM CSUR PDF p. 1 carries `January 2025`).
- `hewage2026carbon` (`arXiv:2609.03270`): arXiv Atom API omits the 5th author while local v2 PDF p. 1 explicitly lists all 5 BibTeX authors including Patricia Arroba.
- `faiz2024llmcarbon` (`arXiv:2309.14393`), `wang2026festina` (`arXiv:2606.30391`), `qin2025mooncake` (USENIX FAST 2025), `zhong2024distserve`, `agrawal2024sarathi`, `fu2024serverlessllm`, `shahrad2020serverless`: Cross-checked across USENIX HTML / arXiv / OpenAlex / local PDFs with exact title/author/year/venue confirmation.

---

## 2. Discrepancies Found and Fixed Across the Manuscript

Every numeric claim (100%) and over 30% of qualitative claims were checked against primary simulation CSVs, simulator source/manifests, literature notes, and source PDFs/abstracts. All identified inaccuracies, stale values, and misattributions were resolved directly in LaTeX:

| # | Location | Original Draft Claim | Verified Primary Ground Truth | Resolution Applied |
|---:|---|---|---|---|
| 1 | `06_results_discussion.tex` (`SW1 3.0x conv`) | `P4` $\text{SCI}_{\text{op}}=0.04455$ vs. `B1` $0.07152$ | `summary_sw1_load.csv`: `P4` $= 0.034829$, `B1` $= 0.049427$ | Replaced with exact CSV values (`0.03483 vs. 0.04943`). |
| 2 | `06_results_discussion.tex` (`SW3 strict_code`) | `P4` $7.02\%$, `B1` $8.11\%$ SLO violations | `summary_sw3_slo_hw_wan.csv`: `P4` $= 48.691\%$, `B1` $= 53.302\%$ | Replaced with exact CSV values (`48.69%`, `53.30%`). |
| 3 | `06_results_discussion.tex` (`H4`) | Unqualified `93.0\% embodied share` | `24h E1`: `code` `South Scotland` `92.95%` (`23.20%` cluster-wide); `conv` `90.68%` (`22.47%` cluster-wide) | Scoped explicitly to `code` (`23.2%` cluster-wide; `90.7% / 22.5%` on `conv`). |
| 4 | `main.tex`, `01_introduction.tex`, `06_results_discussion.tex`, `08_conclusion.tex` | Single-point `54.9\%` total SCI cut and `85.2\%` SLO cut | `E1` `1h conv` `-54.92%`, `24h conv` `-54.64%`; `1h code` `-85.22%`, `24h code` `-86.01%` | Updated to exact ranges (`-54.6%--54.9%`, `85.2%--86.0%`; abstract uses `up to 54.9%` / `up to 86.0%`). |
| 5 | `02_background.tex` (Azure `code` prompt) | Mean prompt length `2,047.9` tokens | `DATA_MANIFEST` / trace stats: `2047.8483` tokens | Fixed rounding to `$2{,}047.8$`. |
| 6 | `02_background.tex` & `04_taxonomy_synthesis.tex` (`kwon2023vllm`) | `cuts KV fragmentation by 60\%--80\%` | `kwon2023vllm.pdf` pp. 2, 4: `20.4%--38.2%` active token usage (`61.8%--79.6%` waste), vLLM achieves `96.3%` (`3.7%` waste) | Replaced imprecise range with `cuts KV waste from 61.8%--79.6% down to 3.7%`. |
| 7 | `02_background.tex` (`sun2026lacere`) | Attributed `21\%--83\%` static draw to idle GPUs | `sun2026lacere.pdf` measured `21%--83%` of peak CPU draw in Kepler benchmarks; GPU idle is `60--100 W` | Separated Kepler CPU benchmark draw (`21%--83%`) from GPU idle power (`60--100 W`). |
| 8 | `02_background.tex` (`li2025ecoserve`) & `05_simulation_design.tex` (`tab:params`) | Credited `921.6 kgCO$_2$eq per Genoa host` directly to `li2025ecoserve` | `li2025ecoserve.pdf` uses `800 kgCO2e` host baseline; `921.6297 kgCO2eq` comes from GreenSKU Genoa YAML in `AzurePublicDataset` | Distinguished `800 kgCO2eq` baseline (`li2025ecoserve`) from `921.6 kgCO2eq` GreenSKU assembly (`tab:params` now cites both `azure2024trace,li2025ecoserve`). |
| 9 | `03_methodology.tex` (`42 full-text` split) | `34 peer-reviewed journal, conference, or standards publications` | Corpus includes 31 archival papers, 2 standards, 1 trace release (`azure2024trace`), and 8 preprints | Clarified exact composition (`31` archival papers, `2` standards, `1` trace release, `8` preprints). |
| 10 | `04_taxonomy_synthesis.tex` (`tab:surveys` & `L1.A`) | Credited `bai2026efficiency` with `SCI` coverage; used brittle string-hit counts for `hewage2026carbon`, `yang2025container`, `miao2025serving` | Full-text check of 70-page `bai2026efficiency.pdf` shows `PUE * kWh * CI` (`SCI` count = 0); `yang2025container` covers `SCI` | Corrected `bai2026efficiency` to $\text{PUE}\cdot\text{kWh}\cdot\text{CI}$ and replaced raw concept counts with verified qualitative scope summaries. |
| 11 | `04_taxonomy_synthesis.tex` (`hanafy2023carbonscaler`) | `-36\% CA` (ambiguous/misread as California) | `hanafy2023carbonscaler.pdf` p. 17 explicitly reports `-36%` in `Ontario, Canada` | Changed `-36% CA` $\rightarrow$ `-36% Ontario`. |
| 12 | `04_taxonomy_synthesis.tex` (`wang2026festina`) | `colocated P/D variant (-7\% energy)` | `wang2026festina.pdf` p. 13 (`PD-D` vs `PD-A`) achieves `-7%` additional energy from *disaggregating* P/D | Fixed to `P/D-disaggregated variant (-7% energy)`. |
| 13 | `04_taxonomy_synthesis.tex` (`calheiros2011cloudsim`) | Claimed `discrete-event federated simulation` | `abstract_only` work; abstract states extensible federated cloud simulation (`discrete-event` not in abstract) | Softened to `extensible federated cloud simulation` matching verified abstract. |
| 14 | `05_simulation_design.tex` (Japan TEPCO grid) | `300--670` gCO$_2$eq/kWh | FY2024 TEPCO telemetry bounds: `302.30--671.48` gCO$_2$eq/kWh | Updated to `302.3--671.5`. |

---

## 3. Quantitative, Statistical, PRISMA, and `abstract_only` Audits

### 3.1 Simulation Metrics & Statistical Significance (`100%` Checked)
All simulation figures in `05_simulation_design.tex`, `06_results_discussion.tex`, `01_introduction.tex`, `08_conclusion.tex`, and the Abstract were verified against `experiments/results/{summary_*.csv, wilcoxon_*.csv, hypotheses_verification.csv}`, `sim_config.py`, and `parameter_sources.json`:
- **Track E1 (`conv` & `code`, 1h & 24h, $n=10$ seeds):** `P4` lowers $\text{SCI}_{\text{op}}$ by `60.77%` (`1h conv`) and `60.70%` (`24h conv`) and $\text{SCI}_{\text{tot}}$ by `54.92%` / `54.64%` vs. `B1` ($p=0.002$ vs. `B1`, `B2`, `P3`). `P4` reduces SLO violations vs. `P3` by `85.22%` (`1h code`) and `86.01%` (`24h code`), and by `83.57%` (`1h conv`) and `86.04%` (`24h conv`). `P4` vs. oracle `P5` differences remain non-significant ($p \ge 0.083984$).
- **Track E2 (24h Serverless):** On `TEPCO` (`581.64 gCO2eq/kWh`), `S3` (`0.10825`) improves $\text{SCI}_{\text{op}}$ vs. `S1` (`0.11773`, `-8.0%`), `S2` (`0.11644`, `-7.0%`), and `S2b` (`0.12166`, `-11.0%`) at `28.60%` SLO violations (`4,529.0` cold starts). On `South Scotland` (`9.75 gCO2eq/kWh`, range `0--129`), `S3` cuts SLO violations by `32.6%` vs. `S2` (`12.99%` vs. `19.29%`, $p=0.002$) while embodied hardware reaches `97.4%--97.6%`. On `North Scotland` (`35.65`, std `82.50`, range `0--355`), `S3` cuts SLO violations by `30.5%` vs. `S2` ($p=0.002$) with zero-carbon wind parity ($p \ge 0.50$).
- **Sweeps (`SW1`–`SW4`) & `H4`:** Confirmed exact match on `SW1` (`3.0x conv`: `P4` `2.89%` SLO with `11.30%` Path A, `36.62%` Path B, `52.08%` Path D; `P3` `71.94%`, TTFT P95 `446.7 s`; `B1` `54.48%`, TPOT P95 `2,331 ms`; `B2` `20.00%`), `SW2` (`<0.3%` forecast/lag/noise shift; `low_diff_uk` `P4` `0.08%` SLO / `0.00513` vs. `P3` `10.71%` / `0.00425`), `SW3` (`L4` `P4` `0.76%` vs. `B2` `24.73%` / `P3` `53.47%`; `100 Gbps` `P3 code` `44.45% -> 20.78%`, `P4` `6.57%` with `0.017%` cross-PD on `conv`; `strict_code` `P4` `48.69%`, `B1` `53.30%`, `B2` `75.08%`, `P3` `79.54%`), `SW4` (`PyTorch` `-23.7%` `0.46686 -> 0.35601`, `Safetensors` `-30.9%` `0.35452 -> 0.24488`, `opt_13b` `0.00831 vs 0.00936`, `hardware_exact` `-14.4%` `0.11193 -> 0.09578`), and `H4` (`all-UK` `P4_equal` `53.33%` embodied share; `P3_overprov_plus4` raises $\text{SCI}_{\text{tot}}$ by `+32.61%` on 4-yr life [`0.023003` vs `0.017347`] and `+27.71%` on 9yr/3yr [`0.019366` vs `0.015164`]).
- **Hardware Parameters (`sim_config.py` & `parameter_sources.json`):** Verified `GreenSKU Genoa` host (`562.42 W` peak, `164.644 W` idle, `921.6297 kgCO2e`) and GPU profiles (`H100` `700/60 W`, `124.9 kg`; `A100` `400/100 W`, `121.5 kg`; `L4` `72/14.4 W`, `41.2 kg`).

### 3.2 PRISMA & Bibliometric Consistency
- **PRISMA Counts (`03_methodology.tex`):** `75` identified $-$ `1` duplicate $= 74$ screened $\rightarrow -11$ abstract exclusions $= 63$ assessed $\rightarrow -16$ full-text exclusions $= 47$ retained (`42` full-text `89.4%`; `5` abstract-only `10.6%`). Exact match against screening logs.
- **Taxonomy & Gap Matrix (`04_taxonomy_synthesis.tex`):** `47` works = `35` empirical + `9` surveys + `2` standards + `1` industry report/trace; `0/6` prior P/D engines model grid CI or embodied carbon; `0/4` multi-region carbon schedulers model WAN KV transfer or P/D; `37/47` (`78.7%`) omit embodied carbon (`10/47` include it); `14/35` (`40.0%`) physical testbeds, `10/35` (`28.6%`) hybrid calibrated, `9/35` (`25.7%`) trace/analytical simulations, `2/35` (`5.7%`) abstract-only modeling works.

### 3.3 Strict `abstract_only` Compliance Audit (`5/5 = 100%` Checked)
All manuscript claims citing the five `abstract_only` entries were verified to stay strictly within verified abstract/metadata bounds with zero unverified simulator constants:
1. `roy2026lowcarb`: Serverless cold-start/execution/memory power modeling + carbon-aware idle retention; verified within abstract.
2. `calavaro2026offloading`: LP cloud-to-edge offloading with function variants (`+30%` QoS, `-20%` carbon under equal budgets); title fixed in `.bib`, claims bounded to abstract.
3. `gupta2022act`: Architectural carbon modeling tool (`ACT`) accounting for manufacturing/operational tradeoffs; verified within abstract.
4. `sinha2025utilization`: Utilization-carbon non-linearity across co-located workloads and token ratios; title fixed in `.bib`, text explicitly flags `(abstract only)`.
5. `calheiros2011cloudsim`: Extensible federated cloud simulation toolkit; edited away unsupported `discrete-event` wording not present in abstract.

---

## 4. Automated Plagiarism / Text-Overlap Check

An automated sliding n-gram script compared normalized prose sentences from `./cloud-paper/main.tex` and `./cloud-paper/sections/*.tex` against **89 reference text blobs** (all BibTeX abstracts, `sources_metadata.json`, `research/notes/*.md`, and extracted text from `./cloud-paper/research/pdfs/*.pdf` and local docs), checking for any `>= 8`-word verbatim matches (excluding standard metric names, paper titles/URLs, and the verbatim Section 9 AI declaration):
- **Post-edit `>= 8`-word n-gram overlap hits:** **0**

---

## 5. Mandatory Back-Matter, Constraints & Final PDF Build Check

After all edits were applied, `./cloud-paper/main.tex` was compiled with `latexmk -pdf -g -interaction=nonstopmode main.tex` and checked directly against `main.pdf` and `main.log`:
- **Page count:** **12 pages** (strictly `<= 12` pages)
- **Compilation errors (`!` lines in `main.log`):** **0**
- **Undefined citations / undefined references:** **0 / 0**
- **Overfull `\hbox` warnings:** **0**
- **Abstract:** **190 words** (`>= 180` and within `100–200` word window), `0` `\cite` commands, `0` math expressions (`$`).
- **Declaration of Generative AI Use (`08_conclusion.tex`):** Present verbatim on compiled p. 11.
- **Data and Code Availability (`08_conclusion.tex`):** Verifiable Zenodo DOIs (`10.5281/zenodo.10896254`, `10.5281/zenodo.18396311`), Microsoft `AzurePublicDataset` GitHub URL, and UK NESO API URL; no fabricated GitHub URLs for local study code.

---

## 6. Post-Humanizer Verification Audit (After Agent 7 Prose Pass)

All files edited by Agent 7 (`main.tex` abstract and `sections/01_introduction.tex`–`08_conclusion.tex`) were re-inspected line-by-line and audited programmatically after the final edits.

### 6.1 Post-Humanizer Precision & Overlap Micro-Fixes Applied (4 Fixes)
1. `sections/06_results_discussion.tex` (`E1` oracle `P5` vs. `P4`): Fixed `within 0.03% ($p \ge 0.084$ across all metrics)` $\rightarrow$ `within 0.02% on carbon and 0.25% across all metrics ($p \ge 0.084$)`, matching `wilcoxon_e1_cluster.csv` (`sci_op`/`sci_tot` $\le 0.012\%$, `24h conv slo_viol_pct` $= 0.2476\%$).
2. `sections/04_taxonomy_synthesis.tex` (`tab:matrix`, `calheiros2011cloudsim`, `abstract_only`): Replaced `Taxonomy, DES, conv/code logs` $\rightarrow$ `Taxonomy, Cloud sim, conv/code logs` so zero non-abstract `"discrete-event"` (`DES`) wording leaks into the `abstract_only` CloudSim entry.
3. `sections/02_background.tex` (`calavaro2026offloading`, `abstract_only`): Tightened `edge-cloud continuums, linear-programmed function variant selection raises QoS satisfaction by 30% and cuts carbon by 20%` $\rightarrow$ `cloud-to-edge continuums, linear-programmed function variant selection lets 30% more requests satisfy QoS targets and cuts execution carbon by 20%` to match the published abstract strictly.
4. `main.tex` (Abstract): Reworded `splits into compute-bound prefill and memory-bandwidth-bound decode phases` $\rightarrow$ `separates into compute-intensive prefill and memory-bound decode stages` to remove the sole 8-word match against internal notes while preserving exact technical accuracy.

### 6.2 Post-Humanizer Verification Totals (All Checks Re-Run After Final Edits)
| Check | Post-Humanizer Result | Status |
|---|---|---|
| BibTeX integrity (`references.bib`) | `47` entries, `47` cited, `0` missing `\cite{}`, `0` uncited, `0` dup keys/DOIs | PASS |
| Reference recency (`2022–2026` / `2025–2026`) | `42/47` (**89.4%**) / `23/47` (**48.9%**) | PASS |
| Single-author voice scan (`we`/`our`/`ours`/`us` in prose) | `0` occurrences across `main.tex` + `sections/*.tex` | PASS |
| Simulation CSV, parameter & Wilcoxon alignment | `100%` verified across `E1`, `E2`, `SW1–SW4`, `H4`, `wilcoxon_*.csv` | PASS |
| `abstract_only` strict bounds (`5/5`) | `roy2026lowcarb`, `calavaro2026offloading`, `gupta2022act`, `sinha2025utilization`, `calheiros2011cloudsim` all strictly abstract-bounded | PASS |
| PRISMA & bibliometric arithmetic | `75 - 1 = 74 -> -11 = 63 -> -16 = 47` (`42` full-text, `5` abstract-only); `0/6`, `0/4`, `37/47 = 78.7%` | PASS |
| `>= 8`-word n-gram overlap scan (`87` external blobs + `47` notes) | **`0` hits** across all external abstracts/PDFs/docs (`2` numeric-only tuple hits in internal notes: loader timings & CV/mean stats) | PASS |
| Abstract length & constraints (`main.tex`) | **188 words** (`100–200` and `>= 180`), `0` `\cite{}`, `0` math (`$`) | PASS |
| Section 9 AI declaration (`08_conclusion.tex`) | Exact verbatim match = `True` | PASS |
| Clean `latexmk -C && latexmk -pdf` build (`main.pdf`, `main.log`, `main.blg`) | **12 pages** (`<= 12`), **0** `!` errors, **0** undef cites/refs, **0** BibTeX warnings, **0** Overfull `\hbox`es | PASS |

