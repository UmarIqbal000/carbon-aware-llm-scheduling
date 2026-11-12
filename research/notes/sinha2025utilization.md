# sinha2025utilization: The Utilization Fallacy and the Real Drivers of Carbon-Efficient LLM Inference

## 1. Citation & Access Metadata
- **Citation ID:** `sinha2025utilization`
- **Authors:** Prasoon Sinha, Dimitrios Liakopoulos, Ruihao Li, Neeraja J. Yadwadkar
- **Year:** 2025
- **Title:** The Utilization Fallacy and the Real Drivers of Carbon-Efficient LLM Inference
- **Venue:** ACM SIGEnergy Energy Informatics Review, Vol. 5, No. 2
- **DOI / URL:** https://doi.org/10.1145/3757892.3757903
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `abstract_only`
- **Local Artifact:** None (`abstract_only`; verified via Crossref + OpenAlex API metadata)

## 2. Problem Addressed
Inference operators routinely assume maximizing GPU spatial sharing and raw hardware utilization automatically minimizes carbon emissions—an assumption that breaks when co-located models interact under dynamic grid mixes.

## 3. Method / Architecture / Control Mechanism
*(Access Level: `abstract_only` — paywalled ACM SIGEnergy EIR 2025; strictly bounded to verified Crossref/OpenAlex abstract and metadata.)* Characterizes GPU spatial sharing carbon efficiency, introduces a preliminary method to estimate GPU power under concurrent model execution, and investigates tailored GPU frequency scaling across specific co-located model combinations.

## 4. Dataset, Workload, Benchmark & Hardware Platform
*(Abstract-only record.)* Cites industry manufacturing context noting that producing `350,000` NVIDIA `A100` GPUs generates roughly `7.54 million kgCO2`; exact benchmark suites and model lists beyond GPU spatial sharing remain unverified behind the paywall.

## 5. Key Quantitative Results
*(Abstract-only record.)* Verified abstract refutes the utilization fallacy, establishing that higher GPU utilization does not universally optimize carbon efficiency and depends strongly on co-located model identities, grid energy fluctuations, request rates, and input/output token ratios—with tailored per-combination DVFS improving shared-GPU carbon efficiency.

## 6. Limitations
*(Abstract-only record.)* Exact concurrent power regression equations, frequency settings, embodied amortization curves, and P/D disaggregation findings are inaccessible behind ACM paywall.

## 7. Relevance to Research Questions (RQ1–RQ4)
Reinforces RQ2 and RQ4 (`DESIGN.md` H4): warns that naive GPU consolidation or utilization-only packing does not guarantee minimum `SCI_tot` across varying grid carbon regimes and token distributions.
