# zhong2024distserve: DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

## 1. Citation & Access Metadata
- **Citation ID:** `zhong2024distserve`
- **Authors:** Yinmin Zhong, Shengyu Liu, Junda Chen, Jianbo Hu, Yibo Zhu, Xuanzhe Liu, Xin Jin, Hao Zhang
- **Year:** 2024
- **Title:** DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving
- **Venue:** 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2024)
- **DOI / URL:** https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\zhong2024distserve.pdf` (18 pp.)

## 2. Problem Addressed
Co-locating prefill and decode enforces a shared parallelism strategy and batch interference across phases whose distinct SLOs (strict TTFT vs. strict TPOT) degrade total SLO-compliant goodput.

## 3. Method / Architecture / Control Mechanism
Introduces *DistServe*, disaggregating prefill and decode onto separate GPU pools so each stage independently optimizes tensor/pipeline parallelism and batch sizes for goodput under explicit TTFT and TPOT targets over high-bandwidth intra-cluster links (pp. 4–8).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Benchmarked on 4 nodes x 8 SXM `A100-80GB` GPUs (32 GPUs, 25 Gbps cross-node IB/RDMA noted in Table 1 & Sec. 6.1, p. 9) running OPT-13B/66B/175B on ShareGPT, HumanEval, and LongBench against vLLM and DeepSpeed-MII, paired with a high-fidelity simulator.

## 5. Key Quantitative Results
At 90% SLO attainment, supports 2.0–4.6x higher arrival rates than vLLM and 1.6–7.4x higher than DeepSpeed-MII while meeting 1.8–12.6x tighter latency SLOs (pp. 10–11). Simulator validation matches physical cluster latency within <2% error (Table 2, p. 12).

## 6. Limitations
Purely goodput/SLO-centric; omits GPU power/DVFS measurements, operational electricity carbon intensity, WAN KV-transfer energy costs, serverless cold starts, and embodied GPU footprints.

## 7. Relevance to Research Questions (RQ1–RQ4)
Anchors RQ2 goodput/SLO baseline thresholds in `DESIGN.md` Table 5.1 (DistServe Table 1 Chatbot `0.25/0.10 s` to Summarization `15.0/0.15 s` TTFT/TPOT SLOs) and quantifies intra-cluster disaggregated vs. colocated behavior (`B2` vs. `B1`).
