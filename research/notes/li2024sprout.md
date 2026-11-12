# li2024sprout: SPROUT: Green Generative AI with Carbon-Efficient LLM Inference

## 1. Citation & Access Metadata
- **Citation ID:** `li2024sprout`
- **Authors:** Baolin Li, Yankai Jiang, Vijay Gadepally, Devesh Tiwari
- **Year:** 2024
- **Title:** SPROUT: Green Generative AI with Carbon-Efficient LLM Inference
- **Venue:** Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (EMNLP 2024), pp. 21799-21813
- **DOI / URL:** https://doi.org/10.18653/v1/2024.emnlp-main.1215
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\sprout_2024.emnlp-main.1215.txt` (15 pp.)

## 2. Problem Addressed
Co-optimizes token-budget/directive level via LP under live hourly Electricity Maps grid CI plus prorated 5-year hardware embodied carbon on A100 vLLM clusters.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Single-DC Cluster / Pool`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Single-DC Temporal`
- **Control Knobs:** HiGHS LP Directive Token-Budget Control under Grid CI + Embodied Carbon + Quality Floor
- **Carbon / Energy Signal:** Operational CI + Embodied Carbon
- **Embodied Carbon Considered:** Yes (Hardware Amortization)

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Generative QA/Instruction Serving (Llama-2-7B/13B, AlpacaEval/GSM8K/MMLU)
- **Hardware / GPU Profile:** 2x2 NVIDIA A100-40GB + Dual AMD EPYC 7542 (vLLM)
- **Evaluation Platform:** Hardware A100 vLLM Cluster (Electricity Maps 5 Regions)

## 5. Key Quantitative Results
Reduces inference carbon >40% on average (up to 60%) while retaining >90% normalized generation quality (>95% in South Australia) (pp. 1, 7-9)

## 6. Limitations
Single-region colocated serving relying on output-token directive throttling: omits P/D disaggregation, cross-region WAN KV, and serverless cold starts

## 7. Verification Notes
Part A2 verified full text (EMNLP 2024, 15 pp.) and Crossref DOI 10.18653/v1/2024.emnlp-main.1215. Models both grid CI and hardware embodied carbon; colocated single-DC scope without P/D split or WAN KV.
