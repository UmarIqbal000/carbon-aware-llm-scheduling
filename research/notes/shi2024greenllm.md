# shi2024greenllm: GreenLLM: Disaggregating Large Language Model Serving on Heterogeneous GPUs for Lower Carbon Emissions

## 1. Citation & Access Metadata
- **Citation ID:** `shi2024greenllm`
- **Authors:** Tianyao Shi, Yanran Wu, Sihang Liu, Yi Ding
- **Year:** 2024
- **Title:** GreenLLM: Disaggregating Large Language Model Serving on Heterogeneous GPUs for Lower Carbon Emissions
- **Venue:** arXiv preprint (arXiv:2412.20322v1)
- **DOI / URL:** https://arxiv.org/abs/2412.20322
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\greenllm_2412.20322.txt` (15 pp.)

## 2. Problem Addressed
Disaggregated prefill/decode and speculative-decoding vLLM serving across heterogeneous new (A100) and older (T4/V100) GPUs incorporating grid carbon intensity and amortized GPU embodied carbon over lifetime LT.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Intra-Node / Multi-GPU Engine`
- **Phase Awareness:** `Disaggregated P/D`
- **Spatial / Temporal Scope:** `Single-Node / Rack Local`
- **Control Knobs:** Heterogeneous P/D Pool Routing (A100 + T4/V100) + Speculative Draft/Verify + GPU Lifetime Reuse
- **Carbon / Energy Signal:** Operational CI + Embodied Carbon
- **Embodied Carbon Considered:** Yes (Hardware Amortization)

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Autoregressive LLM Serving (ShareGPT & Azure Traces, OPT-6.7B/13B/30B)
- **Hardware / GPU Profile:** GCP NVIDIA A100 + T4 + V100
- **Evaluation Platform:** Hardware Cloud vLLM Cluster (GCP)

## 5. Key Quantitative Results
Cuts total carbon 31.3-40.6% vs single-gen baseline at 90% SLO attainment (27.9% in clean hydro NCSW grid @ 17 gCO2/kWh) via 5-7 yr GPU reuse (pp. 1, 9-11)

## 6. Limitations
Single-cluster scope: omits cross-region multi-DC routing, cross-region WAN KV transfer, host/chassis embodied carbon, and serverless keep-alive

## 7. Verification Notes
Part A1 verified full text (arXiv:2412.20322v1, 29 Dec 2024, 15 pp.). Models both P/D disaggregation, grid CI (CISO 261, NCSW 17, MISO 501), and GPU embodied carbon; single-cluster GCP scope without cross-region WAN KV or serverless keep-alive.
