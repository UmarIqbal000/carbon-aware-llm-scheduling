# gupta2021chasing: Chasing Carbon: The Elusive Environmental Footprint of Computing

## 1. Citation & Access Metadata
- **Citation ID:** `gupta2021chasing`
- **Authors:** Udit Gupta, Young Geun Kim, Sylvia Lee, Jordan Tse, Hsien-Hsin S. Lee, Gu-Yeon Wei, David Brooks, Carole-Jean Wu
- **Year:** 2021
- **Title:** Chasing Carbon: The Elusive Environmental Footprint of Computing
- **Venue:** 2021 IEEE International Symposium on High-Performance Computer Architecture (HPCA 2021), pp. 854-867
- **DOI / URL:** https://doi.org/10.1109/HPCA51647.2021.00076
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\gupta2021chasing.pdf` (14 pp.)

## 2. Problem Addressed
System designers overwhelmingly equate computing sustainability with operational runtime energy efficiency, masking rapidly growing hardware manufacturing, packaging, and datacenter construction embodied carbon.

## 3. Method / Architecture / Control Mechanism
Synthesizes corporate LCA disclosures, public GHG reports (Scope 2 vs. Scope 3), fab energy/grid mixes (Table III), and lifecycle breakeven models across mobile client devices, always-connected cloud servers, and GPU workstations (pp. 2–12).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Empirical sustainability disclosures from Apple, Facebook (Meta), Google, Intel, AMD, and TSMC alongside mobile Pixel 3 vs. cloud ML inference and dual-Vega Mac Pro case studies (pp. 5–10).

## 5. Key Quantitative Results
Reveals embodied emissions account for 74% of Apple device lifecycle carbon vs. 19% use phase (p. 5), while Facebook and Google Scope 3 emissions reach 23x and 21x their Scope 2 operational footprints (48% of Meta emissions from capital goods, p. 8). Moving to >80% green electricity shifts datacenters into capex/manufacturing dominance (p. 9); adding dual Vega GPUs multiplies Mac Pro manufacturing CO2 by 2.6–2.7x (p. 10), and Pixel 3 neural inference amortizes hardware carbon only past 200M ResNet50 / 5B MobileNetv3 images (p. 7).

## 6. Limitations
High-level lifecycle characterization study without runtime inference schedulers, LLM batching/disaggregation models, or serverless controllers.

## 7. Relevance to Research Questions (RQ1–RQ4)
Foundational empirical motivation for RQ4 and Hypothesis H4 (`DESIGN.md` 4-yr amortization baseline), proving clean electricity grids shift emissions dominance onto GPU manufacturing.
