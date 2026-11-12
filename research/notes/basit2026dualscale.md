# basit2026dualscale: DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS

## 1. Citation & Access Metadata
- **Citation ID:** `basit2026dualscale`
- **Authors:** Omar Basit, Yunzhao Liu, Z. Jonny Kong, Y. Charlie Hu
- **Year:** 2026
- **Title:** DualScale: Energy-Efficient Disaggregated LLM Serving via Phase-Aware Placement and DVFS
- **Venue:** arXiv preprint (arXiv:2602.18755v3)
- **DOI / URL:** https://arxiv.org/abs/2602.18755
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\basit2026dualscale.pdf` (18 pp.)

## 2. Problem Addressed
Existing phase-disaggregated LLM engines balance latency using coarse heuristics and overlook distinct phase-specific DVFS opportunities—missing fine-grained control across bursty prompt queues and TBT-slack-rich decode loops.

## 3. Method / Architecture / Control Mechanism
Develops *DualScale*, pairing Tier-1 coarse 5-minute ILP phase pool sizing/model placement with Tier-2 fine-grained runtime scaling: Model Predictive Control (`K=8` future step lookahead, `3^{K'}-1` greedy mutation search in 4 ms, p. 8) jointly tuning prefill batching and DVFS to protect TTFT, alongside lightweight TBT-slack frequency scaling on decode nodes (pp. 4–9).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated on `16x H100` InfiniBand (`2x8`) servers running Llama 3.3 70B on ShareGPT and Azure traces at 67% and 85% target utilization (`TTFT SLO = 600 ms`, `TPOT SLO = 100 ms`, Sec. 6.1, p. 10) against DistServe and PlaceOnly.

## 5. Key Quantitative Results
Cuts prefill energy by up to 39% (27–36% steady state; +15.5% energy-delay-product gain over PlaceOnly) and decode energy by up to 48% (+6.3% over PlaceOnly) while maintaining P99 SLO compliance (pp. 1, 11–12). Analytical predictors achieve 2.7–2.9% latency and 1.0–4.1% energy MAPE, with trace simulation matching real runs within 2.3% / 1.2% MAPE (p. 15).

## 6. Limitations
Optimizes intra-cluster energy (`J`) over InfiniBand rather than grid carbon intensity (`gCO2eq/kWh`), cross-region WAN KV migration vs. recomputation crossovers, serverless cold starts, or embodied carbon.

## 7. Relevance to Research Questions (RQ1–RQ4)
Demonstrates state-of-the-art phase-aware energy savings for RQ1 and RQ2, validating that asymmetric prefill-decode power control (echoing Splitwise) remains untapped under multi-region grid carbon differentials (`DESIGN.md` H1).
