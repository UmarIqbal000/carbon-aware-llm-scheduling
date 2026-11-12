# miao2025serving: Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems

## 1. Citation & Access Metadata
- **Citation ID:** `miao2025serving`
- **Authors:** Xupeng Miao, Gabriele Oliaro, Zhihao Zhang, Xinhao Cheng, Hongyi Jin, Tianqi Chen, Zhihao Jia
- **Year:** 2025
- **Title:** Towards Efficient Generative Large Language Model Serving: A Survey from Algorithms to Systems
- **Venue:** ACM Computing Surveys, Vol. 58, No. 1, pp. 1-37
- **DOI / URL:** https://doi.org/10.1145/3754448
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\miao2025serving.pdf` (35 pp.)

## 2. Problem Addressed
Generative LLM serving suffers severe memory fragmentation, batching interference between prompt ingestion and token generation, and strict latency-throughput tensions at large parameter scales.

## 3. Method / Architecture / Control Mechanism
Articulates an end-to-end algorithms-to-systems LLM serving taxonomy (Fig. 1, p. 5; 35 pp., references p. 21), surveying model compression, speculative decoding, continuous batching, PagedAttention, prefill-decode disaggregation (`Splitwise`, `DistServe`, `Mooncake`, `TetriInfer` in Table 2), and serverless loading (`ServerlessLLM`), paired with production trace analysis (pp. 11–18).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Synthesizes MLSys/OSDI/SOSP serving engines evaluated on BurstGPT and Microsoft Azure inference traces, ShareGPT, and multi-GPU A100/H100 clusters (Table 2; pp. 11–18).

## 5. Key Quantitative Results
Documents prefill-decode separation mechanics, KV-cache memory utilization bottlenecks (16 body KV hits, 5 prefill, 5 decode, 4 disaggregat), and serverless checkpoint tiering bottlenecks. Explicitly acknowledges `LLMCarbon` as an environmental modeling work (2 body carbon mentions) while stating the survey evaluates efficiency purely from throughput and latency perspectives.

## 6. Limitations
Contains zero mentions of `embodied`, `operational carbon`, or `water`, only 2 energy mentions, and 1 cold-start hit; omits grid carbon intensity (`gCO2eq/kWh`), DVFS power-capping sustainability trade-offs, and cross-region routing.

## 7. Relevance to Research Questions (RQ1–RQ4)
Core LLM serving foundation for RQ1 and RQ2, supplying the canonical phase-disaggregated taxonomy (`Splitwise`, `DistServe`, `Mooncake`, `ServerlessLLM`) that `DESIGN.md` couples with grid carbon routing and lifecycle emission accounting.
