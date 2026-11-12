# li2023clover: Clover: Toward Sustainable AI with Carbon-Aware Machine Learning Inference Service

## 1. Citation & Access Metadata
- **Citation ID:** `li2023clover`
- **Authors:** Baolin Li, Siddharth Samsi, Vijay Gadepally, Devesh Tiwari
- **Year:** 2023
- **Title:** Clover: Toward Sustainable AI with Carbon-Aware Machine Learning Inference Service
- **Venue:** Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis (SC23)
- **DOI / URL:** https://doi.org/10.1145/3581784.3607034
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\li2023clover.pdf` (13 pp.)

## 2. Problem Addressed
Serving fixed heavy ML models across unmanaged GPUs wastes operational electricity and inflates carbon emissions when grid carbon intensity surges or when smaller models/partitions suffice under latency constraints.

## 3. Method / Architecture / Control Mechanism
Designs *Clover*, a single-cluster runtime inference manager optimizing a weighted accuracy-vs-carbon objective (`lambda = 0.5`) via Graph Edit Distance pruning and Simulated Annealing over model accuracy variants, NVIDIA Multi-Instance GPU (MIG) hardware partitioning, and worker routing (pp. 4–7).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Deployed on 5 servers hosting 2 `A100-40GB` GPUs each (`10` GPUs with dual AMD EPYC 7542 CPUs) serving NLP QA, sentiment classification, and vision object-detection models (Table 1, p. 7), monitored via `carbontracker` under 48-hour US CAISO and UK National Grid ESO intensity traces assuming `PUE = 1.5` (p. 8).

## 5. Key Quantitative Results
Reduces operational CO2 emissions by >75% relative to a carbon-agnostic baseline and remains within 5% of an oracle offline optimizer (pp. 8–9), imposing <0.5% runtime control overhead and 1.2% optimization overhead (pp. 7, 9–10).

## 6. Limitations
Targets small static encoder/vision inference tasks (BERT/object detection) rather than stateful autoregressive LLMs; omits prefill-decode separation, KV-cache memory/transfer dynamics, multi-region WAN routing, and dynamic FaaS cold-start loading.

## 7. Relevance to Research Questions (RQ1–RQ4)
Represents an early GPU inference carbon-aware milestone for RQ1 and validates operational GPU carbon-tuning concepts, while highlighting why MIG-based static classification controllers do not directly generalize to phase-disaggregated LLM serving (RQ2).
