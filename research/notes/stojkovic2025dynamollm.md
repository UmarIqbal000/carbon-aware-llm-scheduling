# stojkovic2025dynamollm: DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency

## 1. Citation & Access Metadata
- **Citation ID:** `stojkovic2025dynamollm`
- **Authors:** Jovan Stojkovic, Chaojie Zhang, Íñigo Goiri, Josep Torrellas, Esha Choukse
- **Year:** 2025
- **Title:** DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency
- **Venue:** 2025 IEEE International Symposium on High Performance Computer Architecture (HPCA 2025), pp. 1348-1362
- **DOI / URL:** https://doi.org/10.1109/HPCA61900.2025.00102
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\stojkovic2025dynamollm.pdf` (14 pp.)

## 2. Problem Addressed
Production LLM inference workloads exhibit diurnal load swings and heterogeneous prompt/output distributions (`short`, `medium`, `long`), yet static GPU allocations and fixed tensor-parallelism/frequency configurations burn severe idle and dynamic energy.

## 3. Method / Architecture / Control Mechanism
Designs *DynamoLLM*, a hierarchical energy-management stack operating across 30-minute cluster, 5-minute pool, and 5-second instance loops to jointly tune active server counts (VM spawn `6–8 min`, Table V, p. 5), NVLink tensor-parallelism re-sharding (`T=50 ms`, Table VI, p. 8), and NVML GPU core frequency scaling (`50–80 ms` vs. `20–30 ms` decode steps) subject to bucketed TTFT/TBT SLOs (Table IV, p. 3: Short `250/100 ms`, Medium `400/100 ms`, Long `2000/100 ms`).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Measured on `8x H100` servers and a calibrated discrete-time trace simulator driven by 1-hour, 1-day, and 1-week Azure LLM Conversational and Coding inference traces serving Llama2-70B (pp. 7–11).

## 5. Key Quantitative Results
Reduces 1-week cluster energy consumption by 47–56%, lowers average GPU server provisioning cost by 38.5% (40 down to 24.6 servers), improves P99 TTFT and TBT by 5.3% and 11.1%, cuts 1-hour trace energy by 35%, and reduces operational carbon emissions by 38% (pp. 1, 9–11).

## 6. Limitations
Schedules colocated tensor-parallel pools rather than disaggregated prefill-decode servers, operates inside a single datacenter without cross-region grid routing or WAN KV transfer, and omits serverless checkpoint cold-start penalties and embodied hardware carbon.

## 7. Relevance to Research Questions (RQ1–RQ4)
Core baseline and workload benchmark source for RQ1, RQ2, and `DESIGN.md` (providing `DynamoLLM` bucket SLOs in Table 5.1, companion `azure2024trace` characteristics, and DVFS switching vs. decode-step timing constraints).
