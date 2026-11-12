# roy2026lowcarb: LowCarb: Carbon-Aware Scheduling of Serverless Functions

## 1. Citation & Access Metadata
- **Citation ID:** `roy2026lowcarb`
- **Authors:** Rohan Basu Roy, Devesh Tiwari
- **Year:** 2026
- **Title:** LowCarb: Carbon-Aware Scheduling of Serverless Functions
- **Venue:** 2026 IEEE International Symposium on High Performance Computer Architecture (HPCA 2026)
- **DOI / URL:** https://doi.org/10.1109/hpca68181.2026.11408586
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `abstract_only`
- **Local Artifact:** None (`abstract_only`; verified via Crossref + OpenAlex API metadata)

## 2. Problem Addressed
Proactive in-memory keep-alive caching dramatically improves serverless tail latency, yet its continuous idle memory/compute draw imposes largely uncharacterized operational carbon penalties creating a conflict between responsiveness and sustainability.

## 3. Method / Architecture / Control Mechanism
*(Access Level: `abstract_only` — paywalled IEEE HPCA 2026 proceedings; strictly bounded to verified Crossref/OpenAlex abstract and metadata.)* Proposes *LowCarb*, a reinforcement-learning-based serverless scheduler that quantifies carbon footprint sources unique to FaaS platforms and dynamically tunes execution and caching decisions to co-optimize function latency performance and operational carbon.

## 4. Dataset, Workload, Benchmark & Hardware Platform
*(Abstract-only record.)* Specific function trace datasets, hardware configurations, and grid intensity traces are not disclosed in the publicly verified abstract.

## 5. Key Quantitative Results
*(Abstract-only record.)* Verified abstract reports that LowCarb resolves the performance-vs-sustainability keep-alive conflict to achieve outcomes within 15% of optimality.

## 6. Limitations
*(Abstract-only record.)* Full-text algorithm formulation, RL state/action space, hardware platform specs, embodied accounting, and LLM support cannot be verified behind publisher paywall.

## 7. Relevance to Research Questions (RQ1–RQ4)
Supports RQ1 and RQ3 positioning alongside open-access `sun2026lacere` and `jiang2024ecolife` as concurrent 2026 evidence that RL-tuned FaaS keep-alive balances latency against idle carbon—while leaving GPU LLM checkpoints and P/D phases open.
