# gsteiger2024caribou: Caribou: Fine-Grained Geospatial Shifting of Serverless Applications for Sustainability

## 1. Citation & Access Metadata
- **Citation ID:** `gsteiger2024caribou`
- **Authors:** Viktor Urban Gsteiger, Pin Hong (Daniel) Long, Yiran (Jerry) Sun, Parshan Javanrood, Mohammad Shahrad
- **Year:** 2024
- **Title:** Caribou: Fine-Grained Geospatial Shifting of Serverless Applications for Sustainability
- **Venue:** Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles (SOSP 2024), pp. 403-420
- **DOI / URL:** https://doi.org/10.1145/3694715.3695954
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\gsteiger2024caribou.pdf` (18 pp.)

## 2. Problem Addressed
Geo-distributed serverless workflows modeled as directed acyclic graphs (DAGs) risk cascade SLO breaches and hidden WAN network energy emissions if each stage is shifted naively across cloud regions.

## 3. Method / Architecture / Control Mechanism
Proposes *Caribou*, a fine-grained serverless DAG placement orchestrator solving an HTTPB token-bucket dynamic program (p. 6) coupled with 2,000-sample Monte Carlo E2E QoS tail estimation (p. 9) to route individual workflow functions across AWS regions within user-specified latency SLAs while accounting for wide-area data transmission energy (`0.001–0.005 kWh/GB`, p. 8).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Five multi-stage serverless applications (Table 1, p. 10, including Image/Video Analytics and Azure 2021 trace workloads) evaluated over four North American AWS regions (`Oct 15–21` grid carbon data).

## 5. Key Quantitative Results
Reduces operational workflow emissions by 22.9% under worst-case network energy (`0.005 kWh/GB`) and 66.6% under low-transmission energy (`0.001 kWh/GB`, reaching 91.2% at `1e-4 kWh/GB`, pp. 11–12), incurring <1% messaging overhead and 2.71–5.72% E2E latency penalty vs. AWS Step Functions (p. 13). Solving 24 hourly plans consumes ~276 s CPU time and `1.98e-2 gCO2eq` (pp. 13–14).

## 6. Limitations
Evaluates CPU Lambda DAGs transferring compact function payloads rather than multi-GB GPU LLM KV caches; explicitly assumes equal embodied baselines across regions (p. 8) and relies on average rather than marginal CI (Sec. 10, p. 14).

## 7. Relevance to Research Questions (RQ1–RQ4)
Provides direct methodological inspiration for RQ2 (`P4` hybrid DAG routing in `DESIGN.md`): demonstrates quantitatively how cross-region data transmission energy (`E_kv` analog) erodes clean-grid shifting savings when payload-to-compute ratios climb.
