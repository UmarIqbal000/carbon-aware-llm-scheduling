# faiz2024llmcarbon: LLMCarbon: Modeling the End-to-End Carbon Footprint of Large Language Models

## 1. Citation & Access Metadata
- **Citation ID:** `faiz2024llmcarbon`
- **Authors:** Ahmad Faiz, Sotaro Kaneda, Ruhan Wang, Rita Osi, Prateek Sharma, Fan Chen, Lei Jiang
- **Year:** 2024
- **Title:** LLMCarbon: Modeling the End-to-End Carbon Footprint of Large Language Models
- **Venue:** Proceedings of the Twelfth International Conference on Learning Representations (ICLR 2024)
- **DOI / URL:** https://arxiv.org/abs/2309.14393
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\faiz2024llmcarbon.pdf` (15 pp.)

## 2. Problem Addressed
Existing ML carbon calculators (`mlco2`, experiment trackers) mispredict large distributed LLM training and inference emissions by >60% because they ignore parallelism efficiency, hardware manufacturing footprints, and scaling laws.

## 3. Method / Architecture / Control Mechanism
Builds *LLMCarbon*, an analytical end-to-end carbon estimator predicting dense and MoE training/inference emissions from Chinchilla scaling, data/tensor/pipeline parallelism models (`Pd`, `Pe`), PUE-scaled grid electricity, and chip-area/capacity embodied factors (Table 3, p. 6: TSMC 4nm H100 `814 mm2 @ 1.8 kgCO2/cm2`, V100 `1.2`, DRAM `0.4 kg/GB`, SSD `0.018 kg/GB`).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Validated against real training logs (e.g., GPT-3, Meta XLM/LLaMA-class deployments), GPT-3 `16x A100` inference traces, and datacenter storage benchmarks across global PUE and regional CI mixes (Tables 4–5, pp. 7–8).

## 5. Key Quantitative Results
Predicts LLM training carbon within <=8.2% error (vs. `mlco2` >69% error, Table 4, p. 7), GPT-3 `16x A100` inference carbon within +3.3%, storage carbon within <3.6% (p. 7), and Meta XLM embodied carbon within -3.05% of `0.66 tCO2eq` actual (Table 5, p. 8). Establishes that embodied silicon contributes 24–35% of end-to-end LLM carbon (p. 8) and H100 upgrades trim operational carbon 71% vs. V100 (p. 9).

## 6. Limitations
Static offline footprint model: lacks continuous batching queues, prefill-decode phase disaggregation, dynamic grid shifting, KV-cache transfer overhead, and serverless GPU cold-start dynamics.

## 7. Relevance to Research Questions (RQ1–RQ4)
Primary carbon modeling reference for RQ1, RQ4, and `DESIGN.md` Eq. 11–13, providing validated hardware embodied calibration checks alongside `EcoServe`.
