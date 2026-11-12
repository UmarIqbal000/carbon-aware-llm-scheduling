# sukprasert2024limitations: On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud

## 1. Citation & Access Metadata
- **Citation ID:** `sukprasert2024limitations`
- **Authors:** Thanathorn Sukprasert, Abel Souza, Noman Bashir, David Irwin, Prashant Shenoy
- **Year:** 2024
- **Title:** On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud
- **Venue:** Proceedings of the Nineteenth European Conference on Computer Systems (EuroSys 2024), pp. 924-941
- **DOI / URL:** https://doi.org/10.1145/3627703.3650079
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\sukprasert2024limitations.pdf` (18 pp.)

## 2. Problem Addressed
Many cloud carbon studies report optimistic 30–90% savings without rigorously bounding real-world capacity headroom, WAN latency limits, migration overhead, forecast errors, or ongoing grid decarbonization.

## 3. Method / Architecture / Control Mechanism
Conducts an analytical upper-bound characterization across global electricity grids and production cluster traces, modeling finite cluster utilization ceilings, WAN round-trip latency caps, single vs. unbounded task migrations, temporal slack windows, and carbon-forecast inaccuracy (pp. 3–14).

## 4. Dataset, Workload, Benchmark & Hardware Platform
123 global Electricity Maps grids (2020–2022; global mean `368.39 gCO2eq/kWh`, 40x region spread, Sweden ~`16 gCO2eq/kWh`; 87% of 40 cloud DC grids exhibit 24h periodicity, pp. 5–7) combined with Microsoft Azure and Google Borg v3 production workload traces.

## 5. Key Quantitative Results
Unconstrained infinite spatial capacity suggests up to 96% carbon savings, which collapses to 51.5% at 50% cluster utilization and further to 31% under a 50 ms WAN latency ceiling (pp. 8–9). Continuous live migration yields <=`10 gCO2eq/kWh` additional improvement over a single static placement (p. 9). Temporal shifting hits 27% (Azure) / 30% (Google) only under extreme 1-year slack, while 24h shifting drops from `57` to `3 gCO2eq/kWh` for long jobs (pp. 10–11). A 50% forecast error adds 10–12% carbon overhead (CarbonCast 14% MAPE limits penalty to ~3%, p. 13). Emphasizes savings shrink structurally as grids clean up (p. 13).

## 6. Limitations
Treats workloads as generic CPU/Borg jobs without GPU accelerator disaggregation, KV-cache network transfer penalties, serverless cold-start reloads, or embodied hardware emissions.

## 7. Relevance to Research Questions (RQ1–RQ4)
Essential reality check for RQ1, RQ2, and `DESIGN.md` sweeps (`SW1–SW3`): proves capacity utilization (`50%` headroom), WAN latency budgets, and regional `Delta_CI` compression strictly constrain spatial shifting gains, directly justifying `P4`'s hybrid gating.
