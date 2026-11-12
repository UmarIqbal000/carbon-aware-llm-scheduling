# fu2024serverlessllm: ServerlessLLM: Low-Latency Serverless Inference for Large Language Models

## 1. Citation & Access Metadata
- **Citation ID:** `fu2024serverlessllm`
- **Authors:** Yao Fu, Leyang Xue, Yeqi Huang, Andrei-Octavian Brabete, Dmitrii Ustiugov, Yuvraj Patel, Luo Mai
- **Year:** 2024
- **Title:** ServerlessLLM: Low-Latency Serverless Inference for Large Language Models
- **Venue:** 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2024)
- **DOI / URL:** https://www.usenix.org/conference/osdi24/presentation/fu
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\fu2024serverlessllm.pdf` (19 pp.)

## 2. Problem Addressed
Scale-to-zero serverless LLM inference suffers tens-of-seconds cold-start delays when loading 10–130 GB checkpoints from remote object storage and transferring multi-GB KV caches during cross-instance scaling.

## 3. Method / Architecture / Control Mechanism
Builds *ServerlessLLM*, introducing multi-tier loading-optimized checkpoint streaming (`Direct I/O`, pinned host memory, parallel PCIe chunk loading from local NVMe RAID-0), startup-time-aware locality scheduling, and live multi-round token migration that recomputes prompts locally instead of shipping multi-GB KV tensors (`O(10–100 KB)` tokens vs. `1–10 GB` KV, pp. 4–8).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Tested on 8x NVIDIA `A5000` and 4x(4x `A40`, 10 Gbps Ethernet) GPU clusters running OPT-2.7B/6.7B/13B/30B and LLaMA-2-70B on GSM8K, ShareGPT, and Microsoft Azure serverless invocation traces (pp. 9–10).

## 5. Key Quantitative Results
Accelerates checkpoint loading 6x over PyTorch and 3.6x over Safetensors on OPT-2.7B, loads LoRA adapters in 83.5 ms (vs. 370 ms), and loads 130 GB LLaMA-2-70B in `10.3 s` (compared against `48.0 s` Safetensors / `84.0 s` PyTorch in Sec. 2.3 & Fig. 6a, pp. 3, 10). Achieves 10–28x lower E2E serverless latency than Ray Serve—reaching 212x improvement under bursty ShareGPT RPS (pp. 12–13).

## 6. Limitations
Latency-only architecture: tracks zero idle GPU Watts, reload Joules, grid carbon intensity, keep-alive energy tradeoffs, prefill-decode pool separation, or embodied GPU footprints.

## 7. Relevance to Research Questions (RQ1–RQ4)
Core cold-start and migration parameterization reference for RQ3 (`DESIGN.md` `T_cold` sweep across `{10.3, 48.0, 84.0} s` 70B and `{2.0, 8.2, 14.0} s` 13B tiers) and confirms why `S1–S3` serverless GPU keep-alive emissions depend heavily on loader speed.
