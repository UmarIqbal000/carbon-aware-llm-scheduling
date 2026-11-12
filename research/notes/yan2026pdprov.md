# yan2026pdprov: Analytical Power-Aware Provisioning for Prefill--Decode Disaggregated AI Inference

## 1. Citation & Access Metadata
- **Citation ID:** `yan2026pdprov`
- **Authors:** Mingyuan Yan, Haiyu Wang, Linxuan Biao, H. Jonathan Chao, Sai Qian Zhang, Wenqi Cui
- **Year:** 2026
- **Title:** Analytical Power-Aware Provisioning for Prefill--Decode Disaggregated AI Inference
- **Venue:** arXiv preprint (arXiv:2609.24639v1)
- **DOI / URL:** https://arxiv.org/abs/2609.24639
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\pdprov_2609.24639.txt` (17 pp.)

## 2. Problem Addressed
Analytical roofline + M/G/n_P + memory-balance solver for P/D disaggregated provisioning and GPU power reduction on SGLang+Mooncake H200 clusters.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Intra-Node / Multi-GPU Engine`
- **Phase Awareness:** `Disaggregated P/D`
- **Spatial / Temporal Scope:** `Single-Node / Rack Local`
- **Control Knobs:** Analytical P/D Instance Count Optimization + Capped-Ramp Power Provisioning
- **Carbon / Energy Signal:** Local Power / Energy Only (W/J)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Disaggregated LLM Serving (Qwen3-32B, Azure & Mooncake Traces)
- **Hardware / GPU Profile:** NVIDIA H200 GPUs (SGLang 0.5.9 + Mooncake)
- **Evaluation Platform:** Hardware H200 Cluster + Analytical Model

## 5. Key Quantitative Results
Matches H200 SGLang capacity within 1.2-3.0% MAPE and power within 2.3-2.7%; reconfiguring 3p2d->3p1d saves ~830W total under rate shifts (pp. 10-13)

## 6. Limitations
Local intra-DC electrical power (W) only: excludes grid CI, cross-region WAN KV, embodied carbon, and startup/shutdown transients

## 7. Verification Notes
Part A2 screened & verified full text (arXiv:2609.24639v1, 21 Sep 2026, 17 pp.). Intra-DC Watts only; excludes startup transients, grid CI, WAN KV, and embodied carbon.
