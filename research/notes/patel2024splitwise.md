# patel2024splitwise: Splitwise: Efficient Generative LLM Inference Using Phase Splitting

## 1. Citation & Access Metadata
- **Citation ID:** `patel2024splitwise`
- **Authors:** Pratyush Patel, Esha Choukse, Chaojie Zhang, Aashaka Shah, Íñigo Goiri, Saeed Maleki, Ricardo Bianchini
- **Year:** 2024
- **Title:** Splitwise: Efficient Generative LLM Inference Using Phase Splitting
- **Venue:** 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture (ISCA 2024), pp. 118-132
- **DOI / URL:** https://doi.org/10.1109/ISCA59077.2024.00019
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\patel2024splitwise.pdf` (15 pp.)

## 2. Problem Addressed
Compute-bound prefill and memory-bandwidth-bound decode exhibit fundamentally opposite hardware scaling and power profiles, causing colocated continuous batching to stall TBT latency and force expensive homogeneous H100 over-provisioning.

## 3. Method / Architecture / Control Mechanism
Proposes *Splitwise*, disaggregating LLM serving into separate prompt (prefill) and token (decode) machine pools connected via hierarchical NVLink/InfiniBand with layer-wise asynchronous KV-cache streaming (`<7%` TTFT overhead) and mixed-hardware heterogeneous pairing (`H100` prefill + lower-power/capped `A100` decode, pp. 4–10).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated on 2x `DGX-A100` and 2x `DGX-H100` clusters alongside a validated open-source event simulator (<3% MAPE across >50,000 production trace requests, pp. 8–9) on Llama-70B Coding and Conversational prompt/output distributions.

## 5. Key Quantitative Results
Demonstrates that decode nodes tolerate a 50% power cap (`700 W -> 350 W`) with virtually zero TBT penalty while prompt TTFT degrades steeply (Fig. 9, p. 5). Single-request P50 energy matches or favors A100 over H100 (`1.37 vs. 1.37 Wh` coding; `7.9 vs. 9.4 Wh` conversational, Table IV, p. 5). `Splitwise-AA` yields 2.15x throughput at iso-power/iso-cost vs. `Baseline-A100`, `Splitwise-HA` hits 1.18x at -10% cost (p. 10), and peak gains reach 1.76x throughput at -15% power iso-cost or 2.35x iso-power/iso-cost (p. 12); layer-wise KV sync adds just 8 ms (A100) / 5 ms (H100) (p. 9).

## 6. Limitations
Operates strictly inside single-DC high-speed interconnects (`400 Gbps IB`); incorporates zero regional grid carbon intensity, no cross-region WAN KV routing, no serverless cold-start loading, and no embodied hardware carbon amortization.

## 7. Relevance to Research Questions (RQ1–RQ4)
Cornerstone parameter and architecture reference for RQ1, RQ2, and `DESIGN.md` Sec. 4–5 (supplying `B2` baseline logic, A100/H100 TDP & idle power, TTFT/TBT anchors, 50% decode power-cap behavior, and 5–8 ms KV transfer synchronization delays).
