# lu2026etcinfer: ETCInfer: An Energy-efficient Thermal-aware Cooling-joint Scheduler for LLM Inference in AI Datacenters

## 1. Citation & Access Metadata
- **Citation ID:** `lu2026etcinfer`
- **Authors:** Rui Lu, Rui Ge, Huanghuang Liang, Xiaobo Zhou, Dan Wang
- **Year:** 2026
- **Title:** ETCInfer: An Energy-efficient Thermal-aware Cooling-joint Scheduler for LLM Inference in AI Datacenters
- **Venue:** arXiv preprint (arXiv:2609.15230v1)
- **DOI / URL:** https://arxiv.org/abs/2609.15230
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\etcinfer_2609.15230.txt` (16 pp.)

## 2. Problem Addressed
POMDP + actor-critic joint CRAC cooling setpoint, GPU DVFS, and micro-batch scheduler for colocated vLLM datacenter clusters.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Single-DC Cluster / Pool`
- **Phase Awareness:** `Colocated Phase-Aware`
- **Spatial / Temporal Scope:** `Single-DC Temporal`
- **Control Knobs:** Joint CRAC Supply Air + GPU DVFS + Micro-Batch Sizing (POMDP ETCAdapter)
- **Carbon / Energy Signal:** Local Power / Energy Only (W/J)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Colocated vLLM/KServe Chat & Code (OASST1/WebGPT/Alibaba2020)
- **Hardware / GPU Profile:** CoolSIM 8x H100 Model + 4x RTX 3090 / 4090 Physical Testbed
- **Evaluation Platform:** Hybrid Testbed + Sim (vLLM/K8s + CoolSIM CFD)

## 5. Key Quantitative Results
Cuts total job energy up to 33.1%, CRAC cooling energy up to 49.9%, and thermal throttling up to 92.9% while holding SLO violations <0.7% up to 48C (pp. 1, 12-13)

## 6. Limitations
Single-datacenter IT+CRAC electrical energy only: omits time-varying grid CI, P/D pool separation, embodied carbon, and serverless cold starts

## 7. Verification Notes
Part A2 screened & verified full text (arXiv:2609.15230v1, 14 Sep 2026, 16 pp.). Optimizes local IT+CRAC energy; omits grid CI, P/D disaggregation, WAN KV, and embodied carbon.
