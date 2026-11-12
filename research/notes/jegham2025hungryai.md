# jegham2025hungryai: How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference

## 1. Citation & Access Metadata
- **Citation ID:** `jegham2025hungryai`
- **Authors:** Nidhal Jegham, Marwan Abdelatti, Chan Young Koh, Lassad Elmoubarki, Abdeltawab Hendawi
- **Year:** 2025
- **Title:** How Hungry is AI? Benchmarking Energy, Water, and Carbon Footprint of LLM Inference
- **Venue:** arXiv preprint (arXiv:2505.09598v6)
- **DOI / URL:** https://arxiv.org/abs/2505.09598
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\hungryai_2505.09598.txt` (20 pp.)

## 2. Problem Addressed
Monte Carlo and DEA benchmarking of query-level energy, PUE/WUE water, and static-CIF carbon across 30 commercial and open-weight LLMs.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Lifecycle Carbon Model / Simulator`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Accounting / Static Lifecycle`
- **Control Knobs:** Gaussian-Copula Monte Carlo + Cross-Efficiency DEA across 30 LLM APIs
- **Carbon / Energy Signal:** Grid Operational CI (Static CIF + Water)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** 30 Commercial & Open LLMs (3 Synthetic Prompt Tiers)
- **Hardware / GPU Profile:** DGX H100/H200/H800 & DGX A100 API Hardware Profiles
- **Evaluation Platform:** Analytical Monte Carlo & DEA Benchmark

## 5. Key Quantitative Results
DeepSeek-R1 consumes 29.08+-9.73 Wh on long prompts (>65x LLaMA-3.1-8B 0.443 Wh); GPT-4o 0.42 Wh/query scales to ~35k US homes/yr at 700M queries/day (pp. 1, 9-12)

## 6. Limitations
Static provider CIFs with no dynamic routing scheduler, P/D disaggregation, or serverless keep-alive; explicitly excludes Scope 3 embodied carbon

## 7. Verification Notes
Part A2 screened & verified full text (arXiv:2505.09598v6, 24 Nov 2025, 20 pp.). Uses static regional CIF and explicitly excludes Scope 3 embodied carbon (Sec. 4.4).
