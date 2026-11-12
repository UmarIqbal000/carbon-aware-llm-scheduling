# tian2026greencache: Cache Your Prompt When It's Green — Carbon-Aware Caching for Large Language Model Serving

## 1. Citation & Access Metadata
- **Citation ID:** `tian2026greencache`
- **Authors:** Yuyang Tian, Desen Sun, Yi Ding, Sihang Liu
- **Year:** 2026
- **Title:** Cache Your Prompt When It's Green — Carbon-Aware Caching for Large Language Model Serving
- **Venue:** Proceedings of the ACM on Measurement and Analysis of Computing Systems (POMACS), Vol. 10, No. 1, pp. 1-28 (arXiv:2505.23970v3)
- **DOI / URL:** https://doi.org/10.1145/3788087
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\embadvisor_2505.23970.txt` (28 pp.)

## 2. Problem Addressed
GreenCache (formerly EmbAdvisor) co-optimizes operational GPU carbon saved by KV prefix caching against dynamic SSD embodied storage carbon via hourly ILP and utility eviction.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Single-DC Cluster / Pool`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Single-DC Temporal`
- **Control Knobs:** Hourly ILP KV Cache/SSD Capacity Sizing + Carbon-Utility Eviction (LCS)
- **Carbon / Energy Signal:** Operational CI + Embodied Carbon
- **Embodied Carbon Considered:** Yes (SSD Hardware Amortization)

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Context-Caching LLM Inference (Llama-3-8B/70B on LooGLE & Azure)
- **Hardware / GPU Profile:** 4x NVIDIA L40 (48GB) + 16TB NVMe SSD Array
- **Evaluation Platform:** Hardware vLLM+LMCache Testbed (FR/DE/CISO Traces)

## 5. Key Quantitative Results
Saves 5.6-15.1% average total carbon across grids (up to 25.3% in nuclear-clean France for Llama-3-70B) while meeting >90% latency SLOs (pp. 1, 16-20)

## 6. Limitations
Single-cluster colocated vLLM cache management: omits P/D disaggregation, cross-region routing/WAN KV, GPU embodied amortization, and serverless keep-alive

## 7. Verification Notes
Part A1 verified full text (arXiv:2505.23970v3, 11 Apr 2026) and Crossref POMACS DOI 10.1145/3788087 (published 26 Mar 2026). Models CI + SSD embodied carbon; single-cluster colocated vLLM+LMCache.
