# alam2026computing: AI-driven resource allocation in cloud computing: a systematic review revealing critical sustainability and evaluation gaps

## 1. Citation & Access Metadata
- **Citation ID:** `alam2026computing`
- **Authors:** Shahzeb Alam, Muhammad Atif Ramzan, Muhammad Zubair, Ubaid Ullah, Ziaullah, Rab Nawaz, Rahmat Ullah
- **Year:** 2026
- **Title:** AI-driven resource allocation in cloud computing: a systematic review revealing critical sustainability and evaluation gaps
- **Venue:** Computing (Springer), Vol. 108, No. 5, Article 67
- **DOI / URL:** https://doi.org/10.1007/s00607-026-01655-8
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\alam2026computing.pdf` (25 pp.)

## 2. Problem Addressed
AI-driven cloud resource allocators (deep reinforcement learning, heuristics, metaheuristics) proliferate rapidly, yet methodological comparability, production reproducibility, and genuine environmental carbon accounting remain unverified across the literature.

## 3. Method / Architecture / Control Mechanism
Executes a PRISMA-2020 systematic literature review screening 485 candidate studies down to 63 primary AI cloud allocation papers, coding algorithm family, target platform (cloud VM, container, serverless/FaaS), optimization objectives, and experimental validation modality (Table 1, p. 9; 25 pp., references p. 22).

## 4. Dataset, Workload, Benchmark & Hardware Platform
63 peer-reviewed primary studies published through early 2026 covering VM placement, Kubernetes scheduling, and FaaS autoscaling, predominantly evaluated on CloudSim, iFogSim, custom Python/MATLAB simulators, or small synthetic workloads.

## 5. Key Quantitative Results
Quantifies that reinforcement learning represents 40% of reviewed allocation schemes; subsets reporting gains show roughly 45% latency reduction (10 studies), 32% monetary cost reduction (6 studies), and 35% energy savings (16 studies). Crucially reveals that 70% (44 of 63) rely solely on simulation (Table 1, p. 9) and only 4 of 63 (6.3%) incorporate actual grid carbon-aware scheduling.

## 6. Limitations
Records zero mentions of `gpu`, `embodied`, `operational carbon`, `llm`, `large language model`, `prefill`, `decode`, `disaggregat`, `kv cache`, `ttft`, or `tpot`. Confirms a stark sustainability evaluation gap in AI scheduling while leaving GPU-accelerated LLM serving completely unexamined.

## 7. Relevance to Research Questions (RQ1–RQ4)
Directly motivates RQ1's methodological audit and our explicit scope framing in `DESIGN.md` Sec. 1 (citing the 70% simulation precedent while grounding our `SimPy` simulator in real empirical traces and peer-reviewed hardware numbers rather than uncalibrated synthetic parameters).
