# agrawal2024sarathi: Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

## 1. Citation & Access Metadata
- **Citation ID:** `agrawal2024sarathi`
- **Authors:** Amey Agrawal, Nitin Kedia, Ashish Panwar, Jayashree Mohan, Nipun Kwatra, Bhargav Gulavani, Alexey Tumanov, Ramachandran Ramjee
- **Year:** 2024
- **Title:** Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve
- **Venue:** 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2024)
- **DOI / URL:** https://www.usenix.org/conference/osdi24/presentation/agrawal
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\agrawal2024sarathi.pdf` (18 pp.)

## 2. Problem Addressed
Continuous batching prioritizes incoming prefill prompts over ongoing decodes, creating severe generation pipeline stalls (up to >20x TBT spikes) during long-prompt arrivals, while pure decode separation risks underutilizing GPUs.

## 3. Method / Architecture / Control Mechanism
Proposes *Sarathi-Serve*, introducing *chunked prefills* (slicing long prompts into uniform token-budget chunks) and *stall-free batching* (piggybacking decode tokens alongside prefill chunks inside single iterations so compute-bound prefill amortizes memory-bound decode reads without interrupting active generation, pp. 4–9).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated on Azure `NC96ads v4` (`A100-80GB` NVLink) and 8x `A40-48GB` (`TP4-PP2`, Table 1, p. 10) running Mistral-7B, Yi-34B, LLaMA2-70B, and Falcon-180B on `openchat_sharegpt4` (median 1,730 in / 415 out tokens) and `arxiv_summarization` (median 7,059 in, Table 2, p. 10).

## 5. Key Quantitative Results
Eliminates up to 28.3x TBT generation stalls observed in vLLM (p. 8) and expands strict-SLO serving capacity (Table 3 SLO-S, p. 10) by 2.6x on Mistral-7B, 3.7x on Yi-34B, and 5.6x on Falcon-180B relative to vLLM (p. 11). Chunk size 512 keeps prefill overhead <=25% while chunk size 2,048 makes overhead negligible (p. 13).

## 6. Limitations
Remains an intra-DC colocated execution strategy (zero P/D regional splitting), reporting no power, energy, grid carbon, embodied carbon, or serverless cold-start measurements.

## 7. Relevance to Research Questions (RQ1–RQ4)
Provides critical contrast for RQ1 and RQ2 (`B1` colocated chunked scheduling vs. `B2`/`P4` P/D disaggregation) and calibrates colocated prefill-decode interference contention in `DESIGN.md` Sec. 4.1.
