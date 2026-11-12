# qin2025mooncake: Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot

## 1. Citation & Access Metadata
- **Citation ID:** `qin2025mooncake`
- **Authors:** Ruoyu Qin, Zheming Li, Weiran He, Jialei Cui, Feng Ren, Mingxing Zhang, Yongwei Wu, Weimin Zheng, Xinran Xu
- **Year:** 2025
- **Title:** Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot
- **Venue:** 23rd USENIX Conference on File and Storage Technologies (FAST 2025)
- **DOI / URL:** https://www.usenix.org/conference/fast25/presentation/qin
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\qin2025mooncake.pdf` (23 pp.)

## 2. Problem Addressed
Long-context LLM chatbots experience high prefill recomputation costs, unbalanced KV memory pressure under overload spikes, and SLO violations when prefill and decode pools cannot flexibly share distributed CPU/DRAM/SSD KV pools.

## 3. Method / Architecture / Control Mechanism
Designs *Mooncake*, a KV-cache-centric disaggregated architecture decoupling prefill and decode clusters around a distributed CPU/DRAM/SSD/RDMA KV storage fabric (*Conductor*), incorporating prefix cache reuse, chunked pipeline parallelism, and proactive early rejection under predicted SLO overload (pp. 4–14).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated on `8x NVIDIA A800-80GB` NVLink clusters linked by 800 Gbps RoCE RDMA (`[3P+1D]`, `[2P+2D]`, and `[10P+10D]` configs, pp. 15–17), releasing a 23,608-request Kimi production trace (mean `8,590` in / `182` out tokens; 55% LRU cache-hit ceiling, Sec. 4.2 & Table 1, pp. 7–8) alongside ArXiv Summarization, L-Eval, and simulated 16k–128k contexts (Table 2, p. 15).

## 5. Key Quantitative Results
Boosts effective goodput by +50% to +525% in long-context simulations and +75% on production traces—satisfying ~100% TTFT and TBT SLOs where baseline vLLM drops to 57% TBT compliance (pp. 16–17). Proactive early rejection shrinks wasted request rejections from 4,183 to 3,589 (Table 3, p. 17).

## 6. Limitations
Assumes ultra-high-bandwidth 800 Gbps intra-cluster RDMA and reports zero energy (`J/token`), GPU DVFS, operational grid carbon intensity, WAN transmission overhead, or embodied hardware emissions.

## 7. Relevance to Research Questions (RQ1–RQ4)
Key KV-centric disaggregation anchor for RQ1 and RQ2 (`P4` prefix/KV state vs. recomputation dynamics), highlighting the wide gap between intra-DC 800 Gbps RDMA assumptions and `10–100 Gbps` cross-region carbon routing (`DESIGN.md` SW3).
