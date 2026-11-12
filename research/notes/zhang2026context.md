# zhang2026context: Context Is Not Free: Carbon-Aware LLM Routing for Multi-Turn LLM Web Services across Geo-Distributed Data Centers

## 1. Citation & Access Metadata
- **Citation ID:** `zhang2026context`
- **Authors:** Xiaoyang Zhang, Yuejun Yan, Qingang Zhang, Yonggang Wen
- **Year:** 2026
- **Title:** Context Is Not Free: Carbon-Aware LLM Routing for Multi-Turn LLM Web Services across Geo-Distributed Data Centers
- **Venue:** arXiv preprint (arXiv:2610.35230v1)
- **DOI / URL:** https://arxiv.org/abs/2610.35230
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\contextnotfree_2610.35230.txt` (11 pp.)

## 2. Problem Addressed
CarbonRouter selects model, GPU, and region for multi-turn LLM sessions by pricing full prompt history recomputation carbon when moving sessions across geo-distributed datacenters.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Cross-Region / Multi-DC`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Spatial Multi-Region`
- **Control Knobs:** Joint Model/GPU/Region Routing + Prompt-History Recomputation Carbon Gate + Hysteresis
- **Carbon / Energy Signal:** Grid Operational CI (gCO2eq/kWh)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Multi-Turn Web LLM Conversations (ShareGPT + WildChat)
- **Hardware / GPU Profile:** A100 / A40 / V100 Analytical Profile
- **Evaluation Platform:** Trace-Driven Analytical Sim (4 US Regions, 5-min Electricity Maps)

## 5. Key Quantitative Results
Reduces operational CO2 by 16.1% vs FairCarbon overall and 23.1% for >30-turn conversations by avoiding redundant context prefill (pp. 1, 7-9)

## 6. Limitations
Relies on history recomputation rather than cross-region KV transfer (future work); omits P/D disaggregation, embodied carbon, and serverless cold starts

## 7. Verification Notes
Part A1 verified full text (arXiv:2610.35230v1, 26 Oct 2026, 11 pp.). Explicitly defers cross-region KV migration to future work; omits P/D disaggregation, embodied carbon, and serverless cold starts.
