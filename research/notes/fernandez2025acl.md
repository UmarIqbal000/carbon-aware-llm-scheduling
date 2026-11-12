# fernandez2025acl: Energy Considerations of Large Language Model Inference and Efficiency Optimizations

## 1. Citation & Access Metadata
- **Citation ID:** `fernandez2025acl`
- **Authors:** Jared Fernandez, Clara Na, Vashisth Tiwari, Yonatan Bisk, Sasha Luccioni, Emma Strubell
- **Year:** 2025
- **Title:** Energy Considerations of Large Language Model Inference and Efficiency Optimizations
- **Venue:** Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025, Volume 1: Long Papers), pp. 32556-32569
- **DOI / URL:** https://doi.org/10.18653/v1/2025.acl-long.1563
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\fernandez2025acl.pdf` (14 pp.)

## 2. Problem Addressed
Prior NLP sustainability benchmarks conflate model FLOPs, latency, and actual inference energy across serving stacks, hiding how batching, quantization, MoE sparsity, continuous batching, and tensor parallelism affect Joules per token.

## 3. Method / Architecture / Control Mechanism
Conducts controlled hardware power profiling across classic NLP tasks and simulated LLM serving distributions, evaluating PyTorch eager/`torch.compile`, `vLLM`, quantization, speculative decoding (`gamma=4`), and tensor parallelism against idealized FLOPs/TDP efficiency lower bounds (pp. 2–9).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Benchmarked on NVIDIA `A6000`, `A6000 Ada`, and `A100-80GB PCIe` GPUs (Table 5, p. 14) over classic NLP plus offline binned profiles of BurstGPT, Azure Chat (mean `1631.58 in / 105.51 out`), and Azure Code (mean `2511.28 in / 22.69 out`, Tables 1–3, p. 8).

## 5. Key Quantitative Results
Optimized `vLLM` continuous batching slashes energy by 73.00% on BurstGPT, 72.18% on Azure Conversational, and 37.58% on Azure Code relative to vanilla PyTorch, reaching within 26.59–64.22% of the idealized theoretical bound (Table 4, pp. 8–9). Finds decode dominates total energy (except 1-token classification), sparse OLMoE consumes up to +54.24% more energy than dense OLMo-7B, speculative decoding saves energy only at small batch sizes before backfiring at large batches (Fig. 3, p. 4), and `TP4` cuts latency 61.34% while inflating total energy +55.23% (p. 6).

## 6. Limitations
Explicitly restricts scope to GPU-only dynamic energy under offline binned request mixes (p. 10), ignoring host CPU/DRAM overhead, embodied silicon emissions, grid carbon variations, online prefill-decode disaggregation, and serverless cold starts.

## 7. Relevance to Research Questions (RQ1–RQ4)
Critical empirical evidence for RQ1 and RQ2 showing decode energy dominance, why multi-GPU TP4 carries heavy energy penalties unless latency SLOs demand it, and why optimizing `J/token` alone remains incomplete without grid `gCO2eq/kWh` and embodied accounting.
