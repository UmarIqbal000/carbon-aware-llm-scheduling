# hewage2025aging: Aging-aware CPU Core Management for Embodied Carbon Amortization in Cloud LLM Inference

## 1. Citation & Access Metadata
- **Citation ID:** `hewage2025aging`
- **Authors:** Tharindu B. Hewage, Shashikant Ilager, Maria Rodriguez Read, Rajkumar Buyya
- **Year:** 2025
- **Title:** Aging-aware CPU Core Management for Embodied Carbon Amortization in Cloud LLM Inference
- **Venue:** Proceedings of the 16th ACM International Conference on Future and Sustainable Energy Systems (ACM e-Energy 2025)
- **DOI / URL:** https://doi.org/10.1145/3679240.3734608
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\hewage2025aging.pdf` (11 pp.)

## 2. Problem Addressed
High inference server duty cycles accelerate silicon Negative Bias Temperature Instability (NBTI) transistor aging, forcing premature hardware replacement that dramatically inflates amortized embodied carbon.

## 3. Method / Architecture / Control Mechanism
Extends `splitwise-sim` (`splitwise-sim-cpu-carbon`) with a reaction-diffusion NBTI CPU aging model and introduces dynamic working-set *Selective Core Idling* alongside aging-aware task mapping to equalize wear and stretch useful hardware life (pp. 3–8).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated using 40-core and 80-core virtualized hosts driven by Splitwise Azure LLM inference traces with baseline 3-year CPU embodied footprint (`278.3 kgCO2eq`, pp. 7–10).

## 5. Key Quantitative Results
Extends sustainable server longevity to slash annualized CPU embodied emissions by 37.67% at P99 frequency performance (and 49.01% at P50 performance), trims core underutilization by 77.8%, and holds CPU oversubscription below 10% (pp. 1, 9–10).

## 6. Limitations
Models CPU core NBTI degradation exclusively while leaving GPU HBM/SM thermal-voltage wear, GPU DVFS power scaling, prefill-decode disaggregation, grid carbon intensity, and serverless cold starts out of scope.

## 7. Relevance to Research Questions (RQ1–RQ4)
Supports RQ1 and RQ4 (`DESIGN.md` `LT` hardware lifetime sensitivity sweep `SW4`): quantifies how operational scheduling policies actively govern physical replacement lifetimes and embodied amortization.
