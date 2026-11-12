# acun2023carbonexplorer: Carbon Explorer: A Holistic Framework for Designing Carbon Aware Datacenters

## 1. Citation & Access Metadata
- **Citation ID:** `acun2023carbonexplorer`
- **Authors:** Bilge Acun, Benjamin Lee, Fiodar Kazhamiaka, Kiwan Maeng, Udit Gupta, Manoj Chakkaravarthy, David Brooks, Carole-Jean Wu
- **Year:** 2023
- **Title:** Carbon Explorer: A Holistic Framework for Designing Carbon Aware Datacenters
- **Venue:** Proceedings of the 28th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2023), Vol. 2, pp. 118-132
- **DOI / URL:** https://doi.org/10.1145/3575693.3575754
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\acun2023carbonexplorer.pdf` (15 pp.)

## 2. Problem Addressed
Annual renewable energy credits (RECs) overstate real decarbonization by masking hourly supply-demand mismatches; datacenter planners need joint optimization across solar/wind procurement, battery storage, embodied overhead, and flexible scheduling.

## 3. Method / Architecture / Control Mechanism
Constructs *Carbon Explorer*, an investment and operational simulator co-optimizing 24/7 hourly Carbon-Free Energy (`CFE`) across wind/solar capacity, Li-ion batteries, embodied capex amortization, and delay-tolerant Carbon-Aware Scheduling (CAS, pp. 4–12).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Meta and Google datacenter power traces paired with 2020 hourly telemetry from 10 US balancing authorities and 13 cloud regions, modeling `744.5 kgCO2eq` server manufacturing (`863.6 kgCO2eq` with construction = 1.16x, p. 10), `59 kg/kW`-scale renewable and `15 kg/kWh` Li-ion embodied costs, and CAS workloads assuming 40% flexible Borg / 71.2% Meta daily capacity (pp. 6–12).

## 5. Key Quantitative Results
Shows 100% annual net-zero RECs yield only 46–51% actual hourly CFE matching, while chasing 95% -> 99.9% hourly CFE requires 5x renewable capacity overbuilding (p. 6). Holistic renewables + battery + CAS co-design cuts net datacenter emissions 15–65%, with 80% battery DoD adding 5% net carbon reduction over bare capacity scaling (pp. 11–12).

## 6. Limitations
Macro capacity-planning granularity rather than sub-second GPU LLM scheduling; assumes multi-hour workload flexibility unsuitable for interactive chatbot TTFT/TPOT SLOs and omits GPU KV state.

## 7. Relevance to Research Questions (RQ1–RQ4)
Shapes RQ1 and RQ4 understanding of why operational grid carbon volatility and hardware embodied overheads must be co-accounted at sub-hourly resolution (`DESIGN.md` 30-min UK/JP telemetry).
