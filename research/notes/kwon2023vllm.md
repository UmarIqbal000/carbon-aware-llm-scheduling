# kwon2023vllm: Efficient Memory Management for Large Language Model Serving with PagedAttention

## 1. Citation & Access Metadata
- **Citation ID:** `kwon2023vllm`
- **Authors:** Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, Ion Stoica
- **Year:** 2023
- **Title:** Efficient Memory Management for Large Language Model Serving with PagedAttention
- **Venue:** Proceedings of the 29th Symposium on Operating Systems Principles (SOSP 2023), pp. 611-626
- **DOI / URL:** https://doi.org/10.1145/3600006.3613165
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\kwon2023vllm.pdf` (16 pp.)

## 2. Problem Addressed
Existing LLM serving runtimes pre-allocate contiguous GPU HBM buffers for maximum sequence lengths, suffering severe internal and external memory fragmentation (wasting 60–80% of KV memory) that strictly bounds batch size and request throughput.

## 3. Method / Architecture / Control Mechanism
Introduces *vLLM* featuring *PagedAttention*, an OS-inspired virtual memory paging mechanism partitioning request KV caches into fixed-size non-contiguous physical blocks tracked via logical-to-physical block tables, enabling zero-copy prefix sharing and copy-on-write beam search branching (pp. 4–9).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Benchmarked on Google Cloud A2 instances equipped with `A100-40GB` and `A100-80GB` GPUs (Table 1, p. 9) serving OPT-13B, OPT-66B, OPT-175B, and LLaMA-13B on ShareGPT, Alpaca, and WMT16 workloads against FasterTransformer and Orca variants.

## 5. Key Quantitative Results
Sustains 1.7–2.7x higher request arrival rates than Orca(Oracle) and 2.7–8x higher than baseline Orca without altering model outputs (p. 11). Copy-on-write sharing lowers KV memory consumption by 6.1–9.8% under parallel sampling and 37.6–55.2% under beam search (p. 11), delivering up to 3.58x throughput improvement on shared prefixes (p. 12) while adding 20–26% attention kernel execution overhead (p. 12).

## 6. Limitations
Colocates prefill and decode batches on shared GPUs (exposing decode TBT to prefill interference), provides no DVFS or power capping, omits operational grid carbon and embodied hardware metrics, and assumes always-warm GPU workers.

## 7. Relevance to Research Questions (RQ1–RQ4)
Establishes the foundational continuous-batching GPU baseline (`B1: Carbon-Agnostic Colocated` in `DESIGN.md`) against which phase-disaggregated engines and carbon-aware schedulers are benchmarked (RQ1, RQ2).
