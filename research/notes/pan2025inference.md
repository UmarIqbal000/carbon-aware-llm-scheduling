# pan2025inference: A Survey of LLM Inference Systems

## 1. Citation & Access Metadata
- **Citation ID:** `pan2025inference`
- **Authors:** James Pan, Guoliang Li
- **Year:** 2025
- **Title:** A Survey of LLM Inference Systems
- **Venue:** arXiv preprint (arXiv:2506.21901v1)
- **DOI / URL:** https://arxiv.org/abs/2506.21901
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\pan2025inference.pdf` (25 pp.)

## 2. Problem Addressed
Modern LLM serving engines have evolved into complex distributed data-management systems where orchestrating prompt ingestion, KV-cache routing, and batch scheduling poses tight architectural coupling challenges.

## 3. Method / Architecture / Control Mechanism
Adopts a database/data-management perspective decomposing LLM serving engines into request scheduling, KV-cache storage, synchronous vs. asynchronous prefill-decode disaggregation pipelines (Fig. 20; Tables 3–4, pp. 18–21; 25 pp., references p. 22), and serverless GPU pooling architectures including DeepFlow and ServerlessLLM.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Surveys flagship engines including vLLM, Sarathi-Serve, Splitwise, DistServe, Mooncake, ServerlessLLM, and DeepFlow across latency-critical cloud and serverless serving deployments (Tables 3–4, pp. 18–21).

## 5. Key Quantitative Results
Provides deep structural synthesis of phase separation and stateful data movement with 29 prefill, 28 decode, 24 kv-cache, 12 disaggregation, 6 serverless, and 3 cold-start body mentions across 25 pages.

## 6. Limitations
Contains zero mentions of `carbon`, `embodied`, `operational carbon`, or body-text `energy`, completely omitting GPU power draw, DVFS capping, electricity emissions, and hardware amortization.

## 7. Relevance to Research Questions (RQ1–RQ4)
Reinforces RQ1's demonstration of the systems-vs-sustainability bifurcation and clarifies synchronous vs. asynchronous P/D KV pipeline latencies modeled in `DESIGN.md` Sec. 4.1–4.3.
