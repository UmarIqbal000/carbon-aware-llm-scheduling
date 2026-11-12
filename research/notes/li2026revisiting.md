# li2026revisiting: Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications

## 1. Citation & Access Metadata
- **Citation ID:** `li2026revisiting`
- **Authors:** Jiaxi Li, Yue Zhu, Eun Kyung Lee, Klara Nahrstedt
- **Year:** 2026
- **Title:** Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications
- **Venue:** arXiv preprint (arXiv:2601.08833v1; submitted Nov 2025)
- **DOI / URL:** https://arxiv.org/abs/2601.08833
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\li2026revisiting.pdf` (10 pp.)

## 2. Problem Addressed
Systems papers frequently assert that prefill-decode disaggregation universally improves performance and energy efficiency, yet systematic evidence across slower KV transfer paths (PCIe P2P, CPU DRAM, NVMe disk) and independent DVFS remained missing.

## 3. Method / Architecture / Control Mechanism
Benchmarks colocated baselines (`co-1gpu`, `co-2gpus` capped at 28 GB KV/GPU) against three disaggregated KV-transfer pipelines (`dis-gpu` PCIe P2P `cuda_ipc`, `dis-cpu` host RAM offload, `dis-disk` storage offload) across batch sizes and symmetric/independent GPU frequency scaling (`0.36–1.26 GHz`) using LMCache + vLLM (pp. 2–8).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Dual-GPU server with an 18-core Xeon E5-2697v4 and 1 TB DDR4 serving Llama-3.2-3B across long-context batches (`16,384 in / 256 out`, `3.5–112 GB` aggregate KV footprint, pp. 4–7).

## 5. Key Quantitative Results
Shows P/D disaggregation performance is highly regime-dependent: `co-2gpus` outperforms disaggregated setups in TTFT at low batch sizes (since disaggregation doubles requests routed per prefill GPU without high-speed NVLink), until `co-2gpus` hits a KV eviction and recomputation collapse around batch 32 (`dis-gpu` leads disaggregated setups, while `dis-disk` surprisingly outperforms `dis-cpu` on TPOT at large batch sizes, pp. 5–7). On DVFS (`0.36–1.26 GHz`, `~0.81 GHz` energy knee), latency-energy Pareto curves form U-shapes, but independent frequency tuning across disaggregated PCIe/host paths never outperforms colocated energy baselines because slower prefill execution inflates baseline energy (pp. 7–8).

## 6. Limitations
Dual-GPU small-model (`3B`) single-node study lacking high-speed NVLink/800G RDMA, multi-region grid CI telemetry, serverless checkpoint cold starts, or embodied carbon accounting.

## 7. Relevance to Research Questions (RQ1–RQ4)
Crucial empirical counterpoint for RQ2 and Hypothesis H2 (`DESIGN.md` Eq. 9): proves quantitatively that unconditional P/D splitting across slower interconnects can backfire in both TTFT and energy, justifying `P4`'s dynamic crossover switch back to colocation/recomputation.
