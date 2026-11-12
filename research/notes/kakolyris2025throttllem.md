# kakolyris2025throttllem: throttLL'eM: Predictive GPU Throttling for Energy Efficient LLM Inference Serving

## 1. Citation & Access Metadata
- **Citation ID:** `kakolyris2025throttllem`
- **Authors:** Andreas Kosmas Kakolyris, Dimosthenis Masouros, Petros Vavaroutsos, Sotirios Xydis, Dimitrios Soudris
- **Year:** 2025
- **Title:** throttLL'eM: Predictive GPU Throttling for Energy Efficient LLM Inference Serving
- **Venue:** 2025 IEEE International Symposium on High Performance Computer Architecture (HPCA 2025)
- **DOI / URL:** https://doi.org/10.1109/hpca61900.2025.00103
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\kakolyris2025throttllem.pdf` (15 pp.)

## 2. Problem Addressed
Iterative decoding batches vary dynamically in sequence lengths and KV-cache occupancy, causing static peak GPU clock settings to waste power during memory-bound intervals while naive DVFS breaks strict TBT SLOs.

## 3. Method / Architecture / Control Mechanism
Introduces *throttLL'eM*, pairing deterministic per-step KV/batch size projections with lightweight ML throughput predictors and a predictive NVML GPU frequency scaler (`8 ms/GPU` switching overhead, `35 ms` combined control latency, p. 8) enforcing SLA margins.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated on AWS `p4d.24xlarge` (`8x A100-40GB`) and `g5.48xlarge` (`8x A10G` Mixtral-8x7B) serving via Triton/TensorRT-LLM on scaled Azure traces (pp. 7–11).

## 5. Key Quantitative Results
Identifies a 1,050 MHz sweet spot yielding +37.4% Tokens-Per-Joule (TPJ) efficiency for minimal latency cost (-6.25% throughput, +8.26% E2E, +5.41% TBT, p. 4) and shows TP outperforms DDP/PP (1.54x/2.74x at TP2, 1.79x/6.26x at TP4; TP2 adds +9.66% TPJ over TP4, p. 5). Throughput predictors achieve `R^2 >= 0.97` (`<1 IPS` MAE, 2.8–5.8% MAPE, Table 3, p. 9) and KV/batch projections achieve 0.19%/2.26% error (p. 9). Cuts total energy up to 43.8% (41.7% even under 30% predictor noise), raises TPJ 1.71–1.78x over Triton TP4 (p. 11), and saves 11.9% energy over ReTail DVFS (p. 12).

## 6. Limitations
Explicitly defers prefill DVFS (noting average prefill `175 ms < 200 ms` switching cost) and P/D disaggregation to future work (p. 8); omits grid carbon intensity, multi-region routing, serverless cold starts, and embodied emissions.

## 7. Relevance to Research Questions (RQ1–RQ4)
Provides rigorous empirical decode DVFS evidence (`+37.4% TPJ`) and parallelism energy scaling (`TP2 vs. TP4`) for RQ1 and RQ2 while explaining why prefill DVFS needs longer batched schedules or disaggregated phase isolation.
