# calavaro2026offloading: Carbon-aware offloading with function variants for serverless computing in the Edge-Cloud Continuum

## 1. Citation & Access Metadata
- **Citation ID:** `calavaro2026offloading`
- **Authors:** Cecilia Calavaro, Valeria Cardellini, Francesco Lo Presti, Gabriele Russo Russo
- **Year:** 2026
- **Title:** Carbon-aware offloading with function variants for serverless computing in the Edge-Cloud Continuum
- **Venue:** Future Generation Computer Systems (Elsevier), 108670
- **DOI / URL:** https://doi.org/10.1016/j.future.2026.108670
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `abstract_only`
- **Local Artifact:** None (`abstract_only`; verified via Crossref + OpenAlex API metadata)

## 2. Problem Addressed
Edge-cloud serverless environments face peak arrival bursts across heterogeneous nodes of varying carbon intensity, requiring joint spatial offloading and per-function fidelity/energy adaptation across multi-class QoS users.

## 3. Method / Architecture / Control Mechanism
*(Access Level: `abstract_only` — paywalled Elsevier FGCS publication; strictly bounded to verified Crossref/OpenAlex abstract and metadata.)* Formulates a runtime linear programming (LP) allocator pairing carbon-aware spatial task offloading across the edge-cloud continuum with adaptive selection of *function variants* (multiple function implementations exposing accuracy, compute, and energy trade-offs) under monetary budgets and multi-class QoS constraints.

## 4. Dataset, Workload, Benchmark & Hardware Platform
*(Abstract-only record.)* Evaluated via simulated edge-cloud FaaS experiments spanning heterogeneous users and service classes; exact grid traces, function implementations, and node counts are omitted from the abstract.

## 5. Key Quantitative Results
*(Abstract-only record.)* Verified abstract reports that under identical monetary budgets, the LP variant-plus-offloading controller enables an average of 30% more requests to satisfy QoS targets while reducing execution carbon emissions by 20% relative to a state-of-the-art baseline.

## 6. Limitations
*(Abstract-only record.)* Full LP constraints, simulation parameters, embodied accounting, and applicability to stateful autoregressive LLM weights/KV caches are unverified behind publisher paywall.

## 7. Relevance to Research Questions (RQ1–RQ4)
Informs RQ1 and RQ2 as an edge-cloud LP spatial shifting precedent that selects lighter variants under tight budgets—conceptually analogous to `P4`'s dynamic path selection (`Path A–D`), though targeting generic edge FaaS rather than P/D GPU inference.
