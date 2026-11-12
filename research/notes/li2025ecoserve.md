# li2025ecoserve: EcoServe: Designing Carbon-Aware AI Inference Systems

## 1. Citation & Access Metadata
- **Citation ID:** `li2025ecoserve`
- **Authors:** Yueying Li, Zhanqiu Hu, Esha Choukse, Rodrigo Fonseca, G. Edward Suh, Udit Gupta
- **Year:** 2025
- **Title:** EcoServe: Designing Carbon-Aware AI Inference Systems
- **Venue:** arXiv preprint (arXiv:2502.05043v2)
- **DOI / URL:** https://arxiv.org/abs/2502.05043
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\li2025ecoserve.pdf` (15 pp.)

## 2. Problem Addressed
Serving LLMs exclusively on brand-new high-TDP GPUs optimizes raw FLOPs while ignoring massive hardware manufacturing embodied emissions, off-peak GPU underutilization, and heterogeneous legacy accelerator suitability.

## 3. Method / Architecture / Control Mechanism
Proposes *EcoServe*, coupling a full lifecycle carbon formulation (host+GPU operational and embodied components, Table 1 p. 2, Eq. p. 4) with four systematic *4R* levers—Reuse (reclaiming idle CPUs via `llama.cpp` for slack-tolerant batch workloads), Rightsize (matching SLO tiers to heterogeneous GPUs via ILP + runtime balancer), Reduce (DVFS/power capping), and Recycle (extending host/GPU lifespans to 9-yr host / 3-yr GPU, Fig. 21, p. 12).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Hardware measurements across PCIe `H100`, `A100`, `A6000`, `L4`, `A40` GPUs and dual Sapphire Rapids CPUs (`vLLM v0.6.2`, `llama.cpp`), paired with an extended `Splitwise-sim` evaluated on ShareGPT, LongBench, Azure Functions, AFT, WattTime (`261 gCO2/kWh` mid CI, Sec. 5, p. 9), and Microsoft GreenSKU component embodied numbers (Table 1 p. 2; Fig. 4–5 pp. 3–4).

## 5. Key Quantitative Results
Individual Reuse, Rightsize, Reduce, and Recycle levers save 29%, 25%, 34%, and 41% carbon respectively, while integrated deployment cuts total operational-plus-embodied carbon by up to 47% (1.4–2.2x vs. performance/cost/energy baselines, pp. 1–2, Fig. 7 p. 5, Fig. 15 p. 10) and outperforms Melange by >2.56x carbon / 2.25x energy (p. 12). CPU Reuse offsets 1.32x–45% offline GPU capacity (p. 6) and accelerates `llama.cpp` 1.34x mean / 4.03x max (p. 11); ILP solves 160-node allocations in 0.585–1.315 s (p. 11).

## 6. Limitations
Operates inside a single datacenter carbon regime without multi-region spatiotemporal WAN routing, prefill-decode cross-DC KV transfer gating, or serverless GPU keep-alive vs. checkpoint reload control.

## 7. Relevance to Research Questions (RQ1–RQ4)
Directly anchors RQ4 and `DESIGN.md` Sec. 4.5 & Table 5.1 (contributing `EcoServe` GPU/server embodied totals `A100 121.5 / H100 124.9 / L4 41.2 kgCO2e`, `800/120 kgCO2e` baseline, and `9-yr host / 3-yr GPU` asymmetric lifetime sweep `SW4` testing Hypothesis H4).
