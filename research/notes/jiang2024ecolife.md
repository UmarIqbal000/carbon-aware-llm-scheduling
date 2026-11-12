# jiang2024ecolife: EcoLife: Carbon-Aware Serverless Function Scheduling for Sustainable Computing

## 1. Citation & Access Metadata
- **Citation ID:** `jiang2024ecolife`
- **Authors:** Yankai Jiang, Rohan Basu Roy, Baolin Li, Devesh Tiwari
- **Year:** 2024
- **Title:** EcoLife: Carbon-Aware Serverless Function Scheduling for Sustainable Computing
- **Venue:** SC24: International Conference for High Performance Computing, Networking, Storage and Analysis, pp. 1-15
- **DOI / URL:** https://doi.org/10.1109/sc41406.2024.00018
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\jiang2024ecolife.pdf` (13 pp.)

## 2. Problem Addressed
Prior serverless keep-alive tuners assumed homogeneous hardware and optimized purely for cold-start latency or electricity, neglecting how keeping functions warm across heterogeneous multi-generation servers shifts combined operational and embodied emissions.

## 3. Method / Architecture / Control Mechanism
Designs *EcoLife*, a multi-generation serverless scheduler combining Dynamic Particle Swarm Optimization (DPSO) over keep-alive windows with priority warm-pool eviction (Fig. 5–6, pp. 6–7) to jointly minimize service time and total operational-plus-embodied carbon across legacy and modern server tiers.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Bare-metal RAPL power profiling contrasting Intel Xeon E5-2686 (2015) and Platinum 8252C (2020) over 4-year embodied lifetimes, driven by CISO grid carbon traces (`6.75%/h` average variability, SD `59.24`) and Azure Functions 2019 traces (p. 8).

## 5. Key Quantitative Results
Operates within 7.7% of Oracle service time and 5.5% of Oracle total carbon (keeping P95 latency inflation <15% with control overhead <0.4% time and <1.2% CO2, p. 9). Outperforms fixed 10-minute single-generation keep-alive by 12.7% service time and 8.6% carbon (p. 9); DPSO ablation alone trims 5.6% time and 16.9% CO2 (p. 10), staying within 7% carbon / 10% time of Oracle even under 10% embodied estimation uncertainty (p. 11).

## 6. Limitations
Evaluates CPU/DRAM multi-generation servers rather than GPUs, lacks multi-region grid routing, and omits multi-GB LLM checkpoint deserialization energy and prefill-decode KV state.

## 7. Relevance to Research Questions (RQ1–RQ4)
Direct precursor for RQ3 and RQ4 (`DESIGN.md` `S3` and H4): confirms that embodied amortization across older vs. newer server generations meaningfully alters optimal FaaS keep-alive decisions.
