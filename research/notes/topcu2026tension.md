# topcu2026tension: Dissecting the Carbon--SLO Tension in Geo-Distributed LLM Serving

## 1. Citation & Access Metadata
- **Citation ID:** `topcu2026tension`
- **Authors:** Burak Topcu, Musa Cim, Zuhal Ozturk, Mahmut Taylan Kandemir
- **Year:** 2026
- **Title:** Dissecting the Carbon--SLO Tension in Geo-Distributed LLM Serving
- **Venue:** arXiv preprint (arXiv:2610.14571v1)
- **DOI / URL:** https://arxiv.org/abs/2610.14571
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\pennstate_2610.14571.txt` (13 pp.)

## 2. Problem Addressed
Geo-distributed carbon-aware LLM scheduling using a continuous-batching discrete-event queueing simulator across 16 US/EU datacenters calibrated against vLLM/A100 traces.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Cross-Region / Multi-DC`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Spatial Multi-Region`
- **Control Knobs:** Facility-Level MILP Multi-Region Request Routing + Batch/Queueing Delay Modeling
- **Carbon / Energy Signal:** Grid Operational CI (gCO2eq/kWh)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Geo-Distributed Autoregressive LLM Serving (BurstGPT / LMSYS / Azure Code)
- **Hardware / GPU Profile:** Homogeneous A100-SXM4-40GB + 300W Host Model
- **Evaluation Platform:** Calibrated Continuous-Batching Sim (16 DCs, 4 Regions)

## 5. Key Quantitative Results
MILP cuts operational CO2 by 26-60% vs round-robin across capacity regimes at ~3% avg SLO violations; sim error <5% TPOT, 9.1% TTFT, <2.5% energy (pp. 6-10)

## 6. Limitations
Homogeneous colocated engines only: omits P/D disaggregation, cross-region KV cache transfer, embodied carbon, and serverless cold starts

## 7. Verification Notes
Part A1 verified full text (arXiv:2610.14571v1, 10 Oct 2026, 13 pp.). Calibrated <5% TPOT / 9.1% TTFT / <2.5% energy error; homogeneous engines only (no P/D disaggregation, no KV transfer, no embodied carbon, no serverless cold starts).
