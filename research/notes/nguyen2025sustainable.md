# nguyen2025sustainable: Towards Sustainable Large Language Model Serving

## 1. Citation & Access Metadata
- **Citation ID:** `nguyen2025sustainable`
- **Authors:** Sophia Nguyen, Beihao Zhou, Yi Ding, Sihang Liu
- **Year:** 2024
- **Title:** Towards Sustainable Large Language Model Serving
- **Venue:** ACM SIGEnergy Energy Informatics Review (HotCarbon'24), Vol. 4, No. 5, pp. 134-140
- **DOI / URL:** https://doi.org/10.1145/3727200.3727220
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\shisurvey_2501.01990.txt` (7 pp.)

## 2. Problem Addressed
Per-token energy benchmarking and analytical operational plus ACT-based embodied carbon modeling across T4 and RTX 6000 Ada GPUs serving LLaMA-1B/3B/7B under hydro, wind, and coal grids.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Lifecycle Carbon Model / Simulator`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Accounting / Static Lifecycle`
- **Control Knobs:** Characterization + Static Operational & ACT Embodied Model across T4 vs RTX 6000 Ada
- **Carbon / Energy Signal:** Operational CI + Embodied Carbon
- **Embodied Carbon Considered:** Yes (Hardware Amortization)

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** LLaMA-1B/3B/7B Inference (Static Prompts & Batches)
- **Hardware / GPU Profile:** NVIDIA T4 vs RTX 6000 Ada
- **Evaluation Platform:** Hardware Profiling + Analytical Carbon Model

## 5. Key Quantitative Results
Older T4 uses 27.1% less energy than RTX 6000 Ada at BS=1 decode, while RTX 6000 Ada improves total carbon at high load/grids with low clean lifetime penalty (pp. 4-6)

## 6. Limitations
Characterization study only: no runtime scheduler, no P/D disaggregation, no cross-region WAN KV routing, and no serverless keep-alive

## 7. Verification Notes
Part A1 verified full text (arXiv:2501.01990v1, 7 pp.) and Crossref ACM SIGEnergy EIR Vol. 4 No. 5 (Dec 2024) pp. 134-140 DOI 10.1145/3727200.3727220.
