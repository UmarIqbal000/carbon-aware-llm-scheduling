# bernhard2026cleanest: Routing LLM Inference to the Cleanest Grid in Real Time

## 1. Citation & Access Metadata
- **Citation ID:** `bernhard2026cleanest`
- **Authors:** Aleks Bernhard, Arif Baran Yardimci
- **Year:** 2026
- **Title:** Routing LLM Inference to the Cleanest Grid in Real Time
- **Venue:** arXiv preprint (arXiv:2608.06188v1)
- **DOI / URL:** https://arxiv.org/abs/2608.06188
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\cleanestgrid_2608.06188.txt` (18 pp.)

## 2. Problem Addressed
Live two-region vLLM routing feasibility testbed and 1-year CONUS historical WattTime MOER replay comparing per-request marginal carbon placement against pressure-based routers.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Cross-Region / Multi-DC`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Spatial Multi-Region`
- **Control Knobs:** WattTime V3 Absolute MOER Dispatch Overlay + DCGM Concurrency Power Model
- **Carbon / Energy Signal:** Grid Operational CI (WattTime MOER)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Cloud LLM Serving (Qwen2.5-7B Live Testbed + CONUS Replay)
- **Hardware / GPU Profile:** Live 2-Region A100/H100 Testbed + CONUS Fleet Model
- **Evaluation Platform:** Hybrid Testbed + Sim (Live vLLM + 1-yr MOER Replay)

## 5. Key Quantitative Results
Demonstrates zero-failure live multi-region steering; year-long replay estimates 22.7% (soft bias) to 50.9-51.0% (cleanest-first) operational CO2 reduction (pp. 1, 9-12)

## 6. Limitations
Homogeneous request routing only: omits P/D disaggregation, WAN KV cache migration, embodied carbon, and serverless cold starts

## 7. Verification Notes
Part A1 verified full text (arXiv:2608.06188v1, 6 Aug 2026, 18 pp.). Live GPU A/B + 1-yr MOER replay; homogeneous sites (no P/D disaggregation, no KV transfer, no embodied carbon, no serverless keep-alive).
