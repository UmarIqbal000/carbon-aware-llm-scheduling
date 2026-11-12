# iso2024sci: Software Carbon Intensity (SCI) Specification (Version 1.1.0; ISO/IEC 21031:2024 Basis)

## 1. Citation & Access Metadata
- **Citation ID:** `iso2024sci`
- **Authors:** Green Software Foundation Standards Working Group
- **Year:** 2024
- **Title:** Software Carbon Intensity (SCI) Specification (Version 1.1.0; ISO/IEC 21031:2024 Basis)
- **Venue:** Green Software Foundation / ISO/IEC 21031:2024 Standard Specification
- **DOI / URL:** https://sci.greensoftware.foundation/
- **Document Type (`sources.csv`):** `standard`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\docs\iso2024sci.html` (Full-text specification/dataset doc)

## 2. Problem Addressed
Software teams lacked a uniform, auditable metric distinguishing genuine operational/hardware carbon optimization from corporate market-based renewable offsets or coarse datacenter averages.

## 3. Method / Architecture / Control Mechanism
*(Local artifact: `docs/iso2024sci.html`, Green Software Foundation SCI v1.1.0 / ISO/IEC 21031:2024 basis.)* Codifies the Software Carbon Intensity rate `SCI = ((E * I) + M) / R`, integrating energy (`E`, kWh), location-based marginal or average grid carbon intensity (`I`, `gCO2eq/kWh`), time- and resource-proportioned embodied emissions (`M = TE * (TS/EL) * (RS/RR)`), and a functional unit (`R`), explicitly disallowing carbon offsets from lowering SCI.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Normative international standard specification spanning compute, memory, storage, and networking boundaries rather than a benchmark dataset.

## 5. Key Quantitative Results
Establishes the universal carbon rate accounting standard combining operational energy emissions (`E * I`) and amortized embodied hardware carbon (`M`) per delivered software work unit (`R`, e.g., per 1,000 generated tokens).

## 6. Limitations
Accounting specification rather than a scheduler; does not prescribe marginal vs. average emission signal choice under multi-region latency constraints, GPU DVFS bounds, or P/D KV-cache boundaries.

## 7. Relevance to Research Questions (RQ1–RQ4)
Normative metric backbone for RQ1, RQ4, and `DESIGN.md` Sec. 4.5 & 6 (`SCI_op`, `SCI_emb`, and `SCI_tot` reported per 1k tokens).
