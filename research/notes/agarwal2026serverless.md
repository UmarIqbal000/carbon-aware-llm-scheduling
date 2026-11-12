# agarwal2026serverless: Dynamic Function Configuration and its Management in Serverless Computing: A Taxonomy and Future Directions

## 1. Citation & Access Metadata
- **Citation ID:** `agarwal2026serverless`
- **Authors:** Siddharth Agarwal, Maria Rodriguez, Rajkumar Buyya
- **Year:** 2026
- **Title:** Dynamic Function Configuration and its Management in Serverless Computing: A Taxonomy and Future Directions
- **Venue:** ACM Computing Surveys, Vol. 58, No. 14, pp. 1-35
- **DOI / URL:** https://doi.org/10.1145/3821534
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\agarwal2026serverless.pdf` (36 pp.)

## 2. Problem Addressed
Static serverless function settings (memory allocation, concurrency, keep-alive window, timeout) degrade QoS under dynamic traffic bursts or inflate provider idle footprint, motivating dynamic runtime reconfiguration.

## 3. Method / Architecture / Control Mechanism
Presents a comprehensive taxonomy and comparison of 40 dynamic serverless configuration management techniques across sizing, scaling, scheduling, and warm-pool control (Table 2, p. 28; 36 pp., references p. 31), explicitly evaluating carbon and energy objectives in Section 3.4.3 (*Sustainability-Oriented Configuration*).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Catalog of 40 primary FaaS systems evaluated across AWS Lambda (noted as commanding over 50% commercial FaaS share, p. 7), Apache OpenWhisk, Knative, and simulated CPU function traces.

## 5. Key Quantitative Results
Documents 149 serverless, 13 cold-start, 14 SLO, 18 carbon, and 10 energy body mentions, revealing in Section 3.4.3 and Table 2 (p. 28) that merely 4 of the 40 cataloged configuration frameworks optimize carbon or energy sustainability, with sustainability tagged as a newly emerging, under-developed KPI.

## 6. Limitations
Records zero occurrences of `prefill`, `decode`, `disaggregat`, `kv cache`, `ttft`, `tpot`, `embodied`, or `operational carbon`, and only one passing mention each of `gpu` (identified as an open specialized-hardware gap) and `llm`.

## 7. Relevance to Research Questions (RQ1–RQ4)
Demonstrates for RQ1 and RQ3 that dynamic FaaS configuration research remains almost exclusively CPU-centric and rarely evaluates grid carbon, motivating our `S3: Dynamic Carbon-Aware Keep-Alive` policy for multi-GB GPU LLM checkpoints.
