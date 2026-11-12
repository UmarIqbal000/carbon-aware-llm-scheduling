# PRISMA-2020 Systematic Literature Search Log

**Paper Title:** *Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation*  
**Protocol:** PRISMA-2020 Systematic Search & Multi-Channel Verification  
**Execution Date:** `2026-11-11` UTC (`2026-11-12` IST)  
**Target Inclusion Window:** `2019–2026` (plus max 2 foundational references from `2011`: NIST SP 800-145 & CloudSim), weighted toward `2022–2026` ($\ge 70\%$) and `2025–2026` ($\ge 12\text{--}18$ works).

---

## 1. Search Channels & Sources Executed

Three complementary identification channels were executed and reconciled cleanly without duplication:

1. **Channel 1 — Stage-1 Audited Survey Corpus (`16` records):**  
   Inherited verified core and supplementary surveys from `./cloud-paper/research/topic_decision.md` and `./cloud-paper/research/scout_surveys_raw.json` (executed `2026-11-11T20:12:16Z` via OpenAlex & arXiv), covering carbon-aware cloud/container scheduling, serverless configuration/AI serving, and efficient/KV-cache/LLM serving surveys (`8` Core + `8` Supplementary = `16`).
2. **Channel 2 — Bounded Systematic PRISMA API Queries (`30` records):**  
   Executed `10` structured, reproducible queries across **OpenAlex (`OA1`–`OA4`)**, **arXiv (`AX1`–`AX3`)**, and **Crossref (`CR1`–`CR3`)** on `2026-11-11`, bounded to top-3 relevance-ranked hits per query (`10 × 3 = 30` records) using `openalex_cli.py`, `search_arxiv.py` (`1 req / 3s`), and `https://api.crossref.org/works`.
3. **Channel 3 — Targeted Top-Venue Proceedings, Reference Chasing, Standards & Benchmarks (`29` records):**  
   Targeted searches via Crossref, OpenAlex, ACL Anthology, USENIX technical session pages, GitHub Public Dataset documentation, Green Software Foundation specifications, and NIST SP 800-145 covering top systems/architecture/NLP venues (**OSDI, SOSP, EuroSys, ASPLOS, ISCA, HPCA, SC, USENIX ATC, FAST, ACL, ICLR, IEEE Middleware, ACM POMACS, ACM e-Energy, ACM SIGEnergy EIR, IEEE IGSC**) plus the `2` foundational 2011 works.

---

## 2. Exact Query Log (Bounded Systematic & Verification Queries)

### 2.1 Channel 2: Systematic Bounded PRISMA Queries (`2026-11-11`)

| Query ID | Source / API | Exact Query String & Filters | Bound / Sort | Raw Index Hits | Retrieved Records |
| :--- | :--- | :--- | :--- | ---: | ---: |
| `OA1` | OpenAlex (`/works`) | `--search '"carbon-aware" (serverless OR FaaS OR Kubernetes OR "cloud scheduling")'` \| `--filter 'publication_year:2019-2026'` | `per-page=3`, `relevance_score:desc` | 774 | 3 |
| `OA2` | OpenAlex (`/works`) | `--search '(prefill decode disaggregation OR "disaggregated LLM" OR "KV cache") ("LLM inference" OR "LLM serving")'` \| `--filter 'publication_year:2022-2026'` | `per-page=3`, `relevance_score:desc` | 4,309 | 3 |
| `OA3` | OpenAlex (`/works`) | `--search '(carbon OR energy OR power OR DVFS OR "cold start") ("LLM inference" OR "LLM serving" OR "serverless LLM")'` \| `--filter 'publication_year:2022-2026'` | `per-page=3`, `relevance_score:desc` | 13,458 | 3 |
| `OA4` | OpenAlex (`/works`) | `--search '("embodied carbon" OR "operational carbon" OR "LLMCarbon" OR "carbon footprint") ("data center" OR "LLM" OR "cloud computing")'` \| `--filter 'publication_year:2019-2026'` | `per-page=3`, `relevance_score:desc` | 24,293 | 3 |
| `AX1` | arXiv Atom API | `(ti:"carbon-aware" OR abs:"carbon-aware" OR abs:"carbon intensity") AND (abs:serverless OR abs:FaaS OR abs:Kubernetes OR abs:"cloud scheduling")` | `max_results=3`, `sort_by=relevance` | *(top-k bounded)* | 3 |
| `AX2` | arXiv Atom API | `(abs:"prefill" AND abs:"decode") AND (abs:"disaggregat" OR abs:"KV cache" OR abs:"energy" OR abs:"carbon" OR abs:"power") AND (abs:"LLM" OR abs:"large language model")` | `max_results=3`, `sort_by=relevance` | *(top-k bounded)* | 3 |
| `AX3` | arXiv Atom API | `(abs:"serverless LLM" OR (abs:"serverless" AND abs:"LLM inference") OR abs:"embodied carbon") AND (abs:"GPU" OR abs:"cold start" OR abs:"carbon" OR abs:"energy")` | `max_results=3`, `sort_by=relevance` | *(top-k bounded)* | 3 |
| `CR1` | Crossref (`/works`) | `query="carbon-aware scheduling serverless cloud"` \| `filter="from-pub-date:2019-01-01,type:journal-article,type:proceedings-article"` | `rows=3` (default relevance) | 704,141 | 3 |
| `CR2` | Crossref (`/works`) | `query.title="prefill decode disaggregation LLM inference serving"` \| `filter="from-pub-date:2022-01-01,type:journal-article,type:proceedings-article"` | `rows=3` (default relevance) | 59,604 | 3 |
| `CR3` | Crossref (`/works`) | `query.title="energy carbon LLM inference serving cloud"` \| `filter="from-pub-date:2019-01-01,type:journal-article,type:proceedings-article"` | `rows=3` (default relevance) | 1,146,558 | 3 |
| **Subtotal** | **Channel 2 Total** | **10 systematic bounded API queries** | **Top-3 per query** | **—** | **30** |

### 2.2 Channel 1 & Channel 3 Metadata & Full-Text Verification Queries (`2026-11-11`)

- **OpenAlex Single-Work Lookups (`openalex_cli.py get`):** Verified metadata, venue, authorship, and inverted-index abstracts for `48` DOIs (`oa_get_batch.json` [34] + `oa_extra2.json` [14]) plus `4` title verification queries (`faiz2024llmcarbon`, `zhong2024distserve`, `agrawal2024sarathi`, `fu2024serverlessllm`).
- **Crossref Authoritative Record Lookups (`https://api.crossref.org/works/<doi>`):** Retrieved authoritative print/online dates, page ranges, container titles, and author arrays across `47` primary/candidate DOIs plus `9` extended checks (`extra_meta.json`) and `6` survey/journal DOIs (`verify_usenix_and_missing.json`).
- **arXiv Atom XML & PDF Retrieval (`search_arxiv.py` & `download_paper.py`):** Verified versioned metadata and abstracts across `3` batch queries (`arxiv_verify_batch.json` [20], `arxiv_preprints_check.json` [21], `arxiv_extra_check2.json` [11]) and downloaded `27` arXiv OA PDFs (`23` primary + `4` USENIX camera-ready arXiv versions).
- **Direct Publisher / Spec / Trace Verification (`2026-11-11`):**
  - **USENIX Proceedings Pages (HTTP 200):** `osdi24/presentation/zhong-yinmin`, `osdi24/presentation/agrawal`, `osdi24/presentation/fu`, `fast25/presentation/qin`, `atc20/presentation/shahrad` (PDF retrieved directly for `shahrad2020serverless`).
  - **ACL Anthology (HTTP 200):** `2025.acl-long.1563`, `2026.findings-acl.1916` (PDFs + HTML abstracts retrieved), plus `2026.acl-long.1842` & `2026.findings-acl.1610` screened.
  - **UBC Cirrus Author Mirror (HTTP 200):** `https://cirrus.ece.ubc.ca/papers/sosp24_caribou.pdf` (`gsteiger2024caribou.pdf`).
  - **NIST Official PDF (HTTP 200):** `https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf` (`mell2011nist.pdf`).
  - **Standards & Dataset Cards (HTTP 200):** `https://sci.greensoftware.foundation/` -> `docs/iso2024sci.html`; `AzureLLMInferenceDataset2024.md` -> `docs/azure2024trace.md`.
  - **Paywall Checks:** Confirmed HTTP 403/HTML paywalls on ACM Digital Library (`dl.acm.org`), IEEE Xplore (`hpca68181.2026.11408586`), Elsevier ScienceDirect (`10.1016/j.future.2026.108670`), and Wiley Online Library (`10.1002/spe.995`), retaining the `5` essential paywalled works strictly as `access_level = abstract_only` using verified OpenAlex + Crossref metadata/abstracts.

---

## 3. PRISMA-2020 Flow Summary & Arithmetic Check

All PRISMA stages balance identically across every identification channel:

| PRISMA Stage | Channel 1 (Stage-1 Surveys) | Channel 2 (Bounded API Queries) | Channel 3 (Targeted / Benchmarks / Standards) | **Total** |
| :--- | :---: | :---: | :---: | :---: |
| **Records Identified (Retrieved & Logged)** | 16 | 30 | 29 | **75** |
| *(Less)* Duplicate Records Removed | 0 | 1 | 0 | **1** |
| **Unique Records Screened (Title & Abstract)** | **16** | **29** | **29** | **74** |
| *(Less)* Excluded at Title / Abstract Screening | 1 | 10 | 0 | **11** |
| **Full-Text / Metadata Assessed for Eligibility** | **15** | **19** | **29** | **63** |
| *(Less)* Excluded at Eligibility Assessment | 6 | 10 | 0 | **16** |
| **Studies Included in Final Corpus (`sources.csv`)** | **9** | **9** | **29** | **47** |

```text
Identification:   75 records identified (16 Channel 1 + 30 Channel 2 + 29 Channel 3)
                     │  [-1 duplicate removed across channels]
                     ▼
Screening (T/A):  74 unique records screened
                     │  [-11 excluded on Title & Abstract]
                     ▼
Eligibility:      63 records assessed via full-text PDF/HTML or verified API metadata/abstract
                     │  [-16 excluded on Eligibility criteria]
                     ▼
Included:         47 sources retained in sources.csv (42 full_text, 5 abstract_only)
```

*(Arithmetic verification: `75 - 1 = 74`; `74 - 11 = 63`; `63 - 16 = 47`; `9 + 9 + 29 = 47`.)*

---

## 4. Complete Itemized Screening & Exclusion Log

### 4.1 Deduplicated Record (`1`)

1. **Li, B., Jiang, Y., Gadepally, V. N., et al. (2024).** *"LLM Inference Serving: Survey of Recent Advances and Opportunities."* IEEE HPEC 2024 (`10.1109/hpec62836.2024.10938426`). Retrieved in Channel 2 (`OA3`) and already present in Channel 1 (Stage-1 Supplementary Survey); deduplicated from Channel 2 (`30 -> 29`) prior to screening.

### 4.2 Title / Abstract Exclusions (`11`)

**Channel 1 (`1`):**
1. **Chen, X., Yu, H., Ni, W., et al. (2026).** *"Networking-Aware Energy Efficiency in Agentic AI Inference: A Survey."* `arXiv:2604.07857v1`. **Reason:** Out of scope — addresses 6G/wireless networking for closed-loop agentic AI edge systems rather than cloud/serverless datacenter phase-disaggregated LLM scheduling.

**Channel 2 (`10`):**
2. **Bhavsagar, D. V. (2026).** *"Recent Trends and Developments in Cloud Computing: A Comprehensive Survey on Edge-Cloud Continuum, Serverless Paradigms, and AI-Integrated Architectures."* *IJSAT*, `10.71097/ijsat.v17.i2.10889` (`OA1`). **Reason:** Broad descriptive overview lacking technical depth on carbon-aware scheduling or LLM serving systems.
3. **Vartziotis, T., & Schmidt, M. (2024).** *"Carbon Footprint Evaluation of Code Generation through LLM as a Service."* *Springer Proceedings*, `10.1007/978-3-658-45010-6_15` (`OA4`). **Reason:** Out of scope — measures application-level carbon emissions of LLM-generated source code rather than inference cluster scheduling.
4. **Park, J., & Yoon, J. (2026).** *"HAWK: Heterogeneity-Aware KV Cache Transfer for Efficient GPU-NPU Phase-Disaggregated LLM Inference."* `arXiv:2610.29873v2` (`AX2`). **Reason:** Out of scope — targets on-device edge GPU–NPU SoC KV transfer rather than cloud/serverless cluster orchestration or carbon awareness.
5. **Luo, X., & Shen, J. (2026).** *"SmartGen: Seamless Disaggregated LLM Inference with Selective KV Cache Transfer."* `arXiv:2607.28150v1` (`AX2`). **Reason:** Out of scope — latency-focused selective KV transfer mechanism with no energy, power, DVFS, carbon, or serverless dimensions.
6. **Ni, Y., & Yang, X. (2025).** *"Predictive-LoRA: A Proactive and Fragmentation-Aware Serverless Inference System for LLMs."* `arXiv:2512.20210v1` (`AX3`). **Reason:** Out of scope — optimizes multi-LoRA adapter memory fragmentation without energy or carbon modeling.
7. **Rani, S. (2022).** *"Workflow Scheduling in Serverless Multi-Cloud Environments."* *IJSER*, `10.70729/se221203103057` (`CR1`). **Reason:** Out of scope — generic serverless DAG workflow scheduling without carbon/energy signals or AI/LLM serving.
8. **Roy, S., & Sarkar, S. (2026).** *"Data-Parallel and Heterogeneity-Aware Scheduling for Geo-Distributed Serverless Scientific Workflows."* *IEEE CLOUD 2026*, `10.1109/cloud72782.2026.00020` (`CR1`). **Reason:** Out of scope — scientific DAG workflow orchestration without carbon-aware metrics or LLM serving.
9. **Zhang, J., & Yang, W. (2026).** *"AsymFlow: Enabling Long-Context LLM Serving via CPU-GPU Prefill-Decode Disaggregation."* *ICPP 2026*, `10.1145/3832810.3832866` (`CR2`). **Reason:** Out of scope — CPU–GPU memory offloading for long contexts without power, energy, or carbon awareness.
10. **Chen, Y., & Cui, W. (2026).** *"Towards High-Goodput LLM Serving with Prefill-decode Multiplexing."* *ASPLOS 2026*, `10.1145/3779212.3790236` (`CR2`). **Reason:** Out of scope — throughput/goodput multiplexing without energy or carbon modeling (core disaggregation baselines are covered by `patel2024splitwise`, `zhong2024distserve`, and `agrawal2024sarathi`).
11. **Chu, W., & Shao, Y. (2025).** *"A Cloud-Edge Collaborative Inference System for Data-secure LLM Serving."* *ACM WNAC 2025*, `10.1145/3748273.3749205` (`CR3`). **Reason:** Out of scope — privacy-preserving split inference rather than energy/carbon-aware cloud/serverless scheduling.

### 4.3 Eligibility Exclusions (`16`)

**Channel 1 (`6`):**
1. **Golec, M., Walia, G. K., Kumar, M., et al. (2024).** *"Cold Start Latency in Serverless Computing: A Systematic Review, Taxonomy, and Future Directions."* *ACM Computing Surveys*, `10.1145/3700875`. **Reason:** Focuses purely on general cold-start latency mitigation without carbon/sustainability metrics or LLM serving; serverless taxonomy is covered by `agarwal2026serverless` (2026) and `besozzi2025serverless` (2025).
2. **Li, B., Jiang, Y., Gadepally, V. N., et al. (2024).** *"LLM Inference Serving: Survey of Recent Advances and Opportunities."* *IEEE HPEC 2024*, `10.1109/hpec62836.2024.10938426`. **Reason:** Brief 2024 workshop-style survey superseded in comprehensiveness and recency by retained 2025–2026 serving surveys (`miao2025serving`, `bai2026efficiency`, `pan2025inference`, `jiang2026kvcache`).
3. **Sisodia, T. (2026).** *"From Inference Engine to Inference Control Plane: Connecting vLLM, llm-d, and the Evolution of Efficient Distributed LLM Serving."* `arXiv:2609.23130v1`. **Reason:** Single-author narrative architectural overview lacking systematic survey methodology and lacking carbon/energy evaluation.
4. **Tirel, N., Roose, P., Ilarri, S., et al. (2025).** *"Workload Shifting Techniques: From Digital Inebriation to Sobriety."* *ACM Computing Surveys*, `10.1145/3769301`. **Reason:** Broad digital-sobriety shifting review whose cloud/container/latency-sensitive scheduling material is directly covered with stronger systems taxonomies in `hewage2026carbon` and `yang2025container` plus primary SOSP/EuroSys/ASPLOS systems.
5. **Wang, L., Jiang, Y., & Mi, N. (2024).** *"Advancing Serverless Computing for Scalable AI Model Inference: Challenges and Opportunities."* *ACM WoSC 2024*, `10.1145/3702634.3702950`. **Reason:** Short position paper lacking systematic coverage; serverless AI/LLM serving is covered in depth by `besozzi2025serverless`, `fu2024serverlessllm`, and `wang2026festina`.
6. **Lazreg, Y. (2025).** *"Sustainable Serverless Computing: A Taxonomy of Challenges and Solutions."* *ACM WoSC 2025*, `10.1145/3774899.3775019`. **Reason:** Short workshop taxonomy superseded by retained primary serverless carbon schedulers (`chadha2023greencourier`, `gsteiger2024caribou`, `qi2024casa`, `jiang2024ecolife`, `roy2026lowcarb`, `sun2026lacere`) and `hewage2026carbon`.

**Channel 2 (`10`):**
7. **Mouad, A., & Hessane, A. (2026).** *"Carbon-Aware Serverless AI Inference: A Scoping Review of Green Techniques and Dynamic Accuracy Adaptation in FaaS."* *Open Science Framework*, `10.17605/osf.io/4p6s7` (`OA1`). **Reason:** Non-peer-reviewed OSF scoping note lacking phase-disaggregation or rigorous LLM serving evaluation; superseded by peer-reviewed CSUR/arXiv surveys (`hewage2026carbon`, `agarwal2026serverless`).
8. **Hu, C.-C., Huang, H., et al. (2025).** *"ShuffleInfer: Disaggregate LLM Inference for Mixed Downstream Workloads."* *ACM TACO*, `10.1145/3732941` (`OA2`). **Reason:** Disaggregation work targeting mixed downstream SLO latency without energy, DVFS, power, or carbon modeling.
9. **Hu, C., Huang, H., Hu, J., et al. (2024).** *"MemServe: Context Caching for Disaggregated LLM Serving with Elastic Memory Pool."* `arXiv:2406.17565` (`OA2`). **Reason:** Memory-pool context caching for latency/throughput optimization with no energy or carbon evaluation.
10. **Liu, Y., Cheng, Y., Yao, J., et al. (2025).** *"LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference."* `arXiv:2510.09665` (`OA2`). **Reason:** KV cache reuse/offloading middleware without energy, power, or carbon scheduling model (KV disaggregation/energy coverage anchored by `qin2025mooncake`, `li2026revisiting`, `basit2026dualscale`).
11. **Lou, C., Qi, S., Jin, C., et al. (2025).** *"HydraServe: Minimizing Cold Start Latency for Serverless LLM Serving in Public Clouds."* `arXiv:2502.15524v2` (accepted NSDI'26; `OA3`). **Reason:** Focuses on serverless LLM cold-start latency via inter-layer model/KV pipelining without power, DVFS, or carbon scheduling (serverless LLM energy/cold-start axis covered by `fu2024serverlessllm` + `wang2026festina`).
12. **Uwizeyimana, I., & Enright Jerger, N. (2025).** *"Carbon-Aware Server Replacement."* *IEEE ISPASS 2025*, `10.1109/ispass64960.2025.00046` (`OA4`). **Reason:** Long-horizon hardware procurement/decommissioning cadence policy rather than runtime workload scheduling or phase-disaggregated LLM inference.
13. **Chaudhary, A., & Mishra, R. (2026).** *"SLA-Constrained Carbon-Aware Routing in Geo-Distributed Serverless Clouds."* `arXiv:2607.22806v1` (`AX1`). **Reason:** Unrefereed generic FaaS routing preprint without LLM/GPU phase awareness; geo-distributed carbon-aware serverless routing is rigorously represented by peer-reviewed `gsteiger2024caribou` (SOSP'24), `chadha2023greencourier` (WoSC'23), and `sukprasert2024limitations` (EuroSys'24).
14. **Ferreira, G., & Ilager, S. (2026).** *"EcoKube: Simulating Carbon-Aware Scheduling Policies in Heterogeneous Edge-Cloud Environments."* *ACM* / `arXiv:2607.09318v1`, `10.1145/3802513.3803486` (`AX1`). **Reason:** Kubernetes edge-cloud container simulator lacking LLM serving, phase-disaggregation, or serverless cold-start GPU dynamics.
15. **Gao, S., & Guo, F. (2026).** *"gKSM: GPU Memory Deduplication at Driver Layer for Serverless LLM Inference."* `10.1145/3828523.3857017` / `arXiv:2610.25219v1` (`AX3`). **Reason:** Driver-level GPU memory deduplication focused purely on memory footprint/startup latency without energy, DVFS, or carbon modeling.
16. **Zhang, H., Mengsi, L., et al. (2026).** *"PDTrim: Targeted Pruning for Prefill-Decode Disaggregation in Inference."* *ACL 2026*, `10.18653/v1/2026.acl-long.1842` (`CR2`). **Reason:** Model/token-level prompt pruning technique for disaggregated inference without cluster power/DVFS, carbon intensity, or serverless scheduling analysis.

---

## 5. Retained Corpus Breakdown (`47` Verified Sources)

### 5.1 By Thematic Pillar
- **Pillar (a) — Core & Supplementary Surveys:** `9` (`hewage2026carbon`, `yang2025container`, `alam2026computing`, `agarwal2026serverless`, `besozzi2025serverless`, `miao2025serving`, `bai2026efficiency`, `jiang2026kvcache`, `pan2025inference`)
- **Pillar (b) — Carbon-Aware Cloud, Container & Serverless/FaaS Schedulers:** `11` (`wiesner2021letswait`, `hanafy2023carbonscaler`, `souza2023ecovisor`, `chadha2023greencourier`, `sukprasert2024limitations`, `gsteiger2024caribou`, `qi2024casa`, `jiang2024ecolife`, `roy2026lowcarb`, `calavaro2026offloading`, `sun2026lacere`)
- **Pillar (c) — Phase-Disaggregated, Energy-Aware & Serverless LLM Serving Systems:** `16` (`kwon2023vllm`, `li2023clover`, `patel2024splitwise`, `zhong2024distserve`, `agrawal2024sarathi`, `fu2024serverlessllm`, `wilkins2024offline`, `qin2025mooncake`, `stojkovic2025dynamollm`, `stojkovic2025tapas`, `kakolyris2025throttllem`, `fernandez2025acl`, `li2025ecoserve`, `basit2026dualscale`, `li2026revisiting`, `wang2026festina`)
- **Pillar (d) — Operational vs. Embodied Carbon Modeling, Production Traces & Standards:** `9` (`shahrad2020serverless`, `gupta2021chasing`, `gupta2022act`, `acun2023carbonexplorer`, `faiz2024llmcarbon`, `azure2024trace`, `iso2024sci`, `sinha2025utilization`, `hewage2025aging`)
- **Pillar (e) — Cloud & Serverless Foundations:** `2` (`mell2011nist`, `calheiros2011cloudsim`)

### 5.2 By Year, Recency, Type, and Access Level
- **By Year:** `2011`: 2 | `2020`: 1 | `2021`: 2 | `2022`: 1 | `2023`: 6 | `2024`: 12 | `2025`: 12 | `2026`: 11 (Total = **47**)
- **Recency Compliance:**
  - `2022–2026`: **42 / 47 (89.4%)** — exceeds $\ge 70\%$ threshold.
  - `2025–2026`: **23 / 47 (48.9%)** — exceeds $12\text{--}18$ target.
  - Pre-2019 foundations: **2 / 47** (`mell2011nist`, `calheiros2011cloudsim`).
- **By Type:** `survey`: 9 | `empirical`: 35 | `industry`: 1 (`azure2024trace`) | `standard`: 2 (`iso2024sci`, `mell2011nist`).
- **By `access_level`:**
  - `full_text`: **42** (`40` verified PDFs in `./cloud-paper/research/pdfs/<id>.pdf` validated with `pypdf`, plus `2` full HTML/Markdown specifications in `./cloud-paper/research/docs/`).
  - `abstract_only`: **5** paywalled articles (`roy2026lowcarb`, `calavaro2026offloading`, `gupta2022act`, `sinha2025utilization`, `calheiros2011cloudsim`), retained with verified OpenAlex + Crossref abstracts and metadata.
- **Explicit Preprint Flagging (`8` items):**
  - *arXiv-only preprints (`6`):* `hewage2026carbon`, `yang2025container`, `pan2025inference`, `li2025ecoserve`, `basit2026dualscale`, `li2026revisiting` (all tagged `preprint;arxiv_preprint`).
  - *Accepted peer-reviewed conference preprints awaiting publisher DOI indexing (`2`):* `sun2026lacere` (accepted at IEEE CCGrid 2026, CC-BY arXiv v1) and `wang2026festina` (accepted at ACM SIGOPS ATC 2026, arXiv v2; tagged `preprint;accepted_preprint`).
