# bai2026efficiency: Beyond Efficiency: A Systematic Survey of Resource-Efficient Large Language Models

## 1. Citation & Access Metadata
- **Citation ID:** `bai2026efficiency`
- **Authors:** Guangji Bai, Zheng Chai, Chen Ling, Shiyu Wang, Jiaying Lu, Nan Zhang, Tingwei Shi, Ziyang Yu, Mengdan Zhu, Yifei Zhang, Xinyuan Song, Carl Yang, Yue Cheng, Liang Zhao
- **Year:** 2026
- **Title:** Beyond Efficiency: A Systematic Survey of Resource-Efficient Large Language Models
- **Venue:** ACM Computing Surveys, Vol. 58, No. 16, pp. 1-45
- **DOI / URL:** https://doi.org/10.1145/3845797
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\bai2026efficiency.pdf` (70 pp.)

## 2. Problem Addressed
Large language models face compounding computational, memory, energy, network, and monetary bottlenecks spanning model architecture, pre-training, fine-tuning, and deployment.

## 3. Method / Architecture / Control Mechanism
Proposes a five-resource taxonomy—computation, memory, energy, financial cost, and communication—across the LLM lifecycle (Sec. 2.2, p. 9; 70 pp., references p. 44). Sections 7–9 (pp. 31–41) formalize energy measurement, PUE-adjusted operational carbon (`PUE * kWh * gCO2eq/kWh`), and Software Carbon Intensity (`SCI`) metrics alongside compression and system simulators.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Surveys pruning, quantization (e.g., AWQ protecting 1% salient weights, p. 24; 60% structural pruning, p. 23), edge/cloud accelerators, `LLMServingSim`, and eight standardized efficiency benchmarks (pp. 31–41).

## 5. Key Quantitative Results
Records 36 energy and 10 carbon body mentions alongside formal carbon conversion formulations (pp. 31–41), mapping energy drivers from FLOPs and DRAM access through system deployment.

## 6. Limitations
Zero occurrences across 70 pages of `prefill`, `disaggregat`, `serverless`, `cold start`, `embodied`, `operational carbon`, or `tpot` (`decode` refers solely to decoder model architectures). Completely omits phase-disaggregated inference scheduling, inter-node KV transfer energy, FaaS cold-start penalties, and embodied hardware carbon.

## 7. Relevance to Research Questions (RQ1–RQ4)
Supplies canonical SCI operational electricity-to-carbon formulation for RQ1 and RQ2 while exposing how macro-level resource-efficient LLM surveys overlook disaggregated scheduling and embodied silicon footprints (RQ4).
