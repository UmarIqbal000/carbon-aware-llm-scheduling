# souza2023ecovisor: Ecovisor: A Virtual Energy System for Carbon-Efficient Applications

## 1. Citation & Access Metadata
- **Citation ID:** `souza2023ecovisor`
- **Authors:** Abel Souza, Noman Bashir, Jorge Murillo, Walid Hanafy, Qianlin Liang, David Irwin, Prashant Shenoy
- **Year:** 2023
- **Title:** Ecovisor: A Virtual Energy System for Carbon-Efficient Applications
- **Venue:** Proceedings of the 28th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2023), Vol. 2, pp. 252-265
- **DOI / URL:** https://doi.org/10.1145/3575693.3575709
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\souza2023ecovisor.pdf` (15 pp.)

## 2. Problem Addressed
Data-center operators treat grid electricity, solar renewables, and battery storage as opaque infrastructure layers, preventing tenant applications from exercising visibility-driven carbon, power-cap, and energy-source tradeoffs.

## 3. Method / Architecture / Control Mechanism
Defines *Ecovisor*, a Virtual Energy System software abstraction exposing programmatic energy/carbon telemetry APIs (`get_grid_carbon`, `get_battery_charge_level`, charging/discharging controls, Tables 1–2, pp. 5–6) so applications can coordinate elastic scaling, hardware capping, local battery buffering, and latency-SLO carbon budgeting.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Hybrid evaluation combining a physical micro-datacenter testbed (NVIDIA Jetson Nano nodes at 1.35 W idle / 5 W CPU / 10 W CPU+GPU, Chroma SAE power supply, 1,440 Wh Li-ion battery at 70% DoD, p. 8) and trace-driven simulation of 16 Dell R430 servers under 2020 CAISO CI.

## 5. Key Quantitative Results
Wait&Scale at 3x concurrency lowers BLAST carbon by 50.05% and execution time by 83.4% compared to suspend-resume, whereas ML training plateaus at 2x (scaling to 3x increases carbon +14.94% from diminishing returns, p. 9). Dynamic carbon budgeting satisfies 60–70 ms P95 SLOs compared to rigid static caps (p. 10), while solar-battery dispatch trims runtime by 39% (p. 12).

## 6. Limitations
Models CPU/edge-GPU batch and web workloads; lacks data-center LLM HBM memory pressure, autoregressive phase disaggregation, KV-cache transfer penalties, serverless cold-start checkpoint reloads, and embodied battery/server amortization.

## 7. Relevance to Research Questions (RQ1–RQ4)
Demonstrates for RQ1 and RQ2 how software-visible carbon budgets preserve millisecond P95 SLOs (analogous to `P4`'s carbon-slack gating) and warns that naive scale-out past scaling knee points increases net emissions.
