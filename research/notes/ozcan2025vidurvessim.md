# ozcan2025vidurvessim: Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations

## 1. Citation & Access Metadata
- **Citation ID:** `ozcan2025vidurvessim`
- **Authors:** Miray Ozcan, Philipp Wiesner, Philipp Weiss, Odej Kao
- **Year:** 2025
- **Title:** Quantifying the Energy Consumption and Carbon Emissions of LLM Inference via Simulations
- **Venue:** arXiv preprint (arXiv:2507.11417v1)
- **DOI / URL:** https://arxiv.org/abs/2507.11417
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\vidurvessim_2507.11417.txt` (12 pp.)

## 2. Problem Addressed
Integrates Vidur LLM inference simulator with a sublinear MFU GPU power model and Vessim renewable/grid energy co-simulation.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Lifecycle Carbon Model / Simulator`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Single-DC Temporal`
- **Control Knobs:** Sublinear MFU Power Model + Vidur-to-Vessim Renewable/Battery/WattTime Co-Simulation
- **Carbon / Energy Signal:** Grid Operational CI (Solar + WattTime)
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Zipfian LLM Inference (CodeLlama-34B, Llama-3-70B, Qwen-72B)
- **Hardware / GPU Profile:** A100-SXM4 / H100-SXM5 / A40 Profiles
- **Evaluation Platform:** Trace Sim. / Analytical (Vidur + Vessim)

## 5. Key Quantitative Results
TP=2, PP=1 outperforms TP=4/PP=4 on efficiency; illustrative solar+battery co-sim offsets 69.2% of 2.47 kgCO2 operational emissions (pp. 8-10)

## 6. Limitations
No live scheduling control loop; omits P/D disaggregation, cross-region WAN KV routing, serverless cold starts, and numerical embodied accounting

## 7. Verification Notes
Part A1 verified full text (arXiv:2507.11417v1, 15 Jul 2025, 12 pp.). Formulates phi_manuf symbolically in Eq. (4) but evaluates only operational solar/WattTime carbon numerically (Table 2, p. 9).
