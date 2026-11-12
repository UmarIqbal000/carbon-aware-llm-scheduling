# jiang2026kvcache: Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization

## 1. Citation & Access Metadata
- **Citation ID:** `jiang2026kvcache`
- **Authors:** Jiantong Jiang, Peiyu Yang, Rui Zhang, Feng Liu
- **Year:** 2026
- **Title:** Towards Efficient Large Language Model Serving: A Survey on System-Aware KV Cache Optimization
- **Venue:** Findings of the Association for Computational Linguistics: ACL 2026, pp. 38450-38476
- **DOI / URL:** https://doi.org/10.18653/v1/2026.findings-acl.1916
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\jiang2026kvcache.pdf` (27 pp.)

## 2. Problem Addressed
Key-value cache memory consumption and state transfer overhead increasingly dominate LLM inference bottlenecks under long contexts and disaggregated serving topologies.

## 3. Method / Architecture / Control Mechanism
Introduces the 3D `sKis` infrastructure taxonomy (Tables 2–7, pp. 4–8; 27 pp., references p. 10) spanning temporal execution and prefill-decode disaggregation, spatial memory-tier/distributed KV orchestration, and structural compression/reuse/eviction across six optimization families (`OVLP`, `HAE`, `MHO`, `CDO`, `KVCC`, `KVRM`).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Analyzes system-aware KV serving papers through ACL 2026 using structural co-occurrence analysis (Tanimoto similarity matrices, Tables 11–12, pp. 25–27) and recommends multi-metric evaluation reporting `J/token` alongside `TTFT`, `ITL`, and goodput.

## 5. Key Quantitative Results
Quantifies high-prevalence technique combinations exceeding 70% pairwise adoption across recent engines (p. 8), documenting 38 body (115 full-text) KV-cache mentions, 9 prefill, 12 decode, 9 disaggregation, and 12 energy mentions.

## 6. Limitations
Zero mentions of `carbon`, `embodied`, `operational carbon`, `serverless`, `cold start`, or `water`. Evaluates energy strictly at cluster/node level (`J/token`) without temporal/regional grid carbon intensity or scale-to-zero FaaS lifecycle costs.

## 7. Relevance to Research Questions (RQ1–RQ4)
Guides RQ1 and RQ2 on KV-cache state management mechanics (`KVRM`, `HAE`, `MHO`) and supports our `J/token` reporting and KV-transfer vs. recomputation crossover condition (`P4` in `DESIGN.md` Eq. 9).
