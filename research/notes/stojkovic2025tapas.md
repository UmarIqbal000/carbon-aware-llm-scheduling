# stojkovic2025tapas: TAPAS: Thermal- and Power-Aware Scheduling for LLM Inference in Cloud Platforms

## 1. Citation & Access Metadata
- **Citation ID:** `stojkovic2025tapas`
- **Authors:** Jovan Stojkovic, Chaojie Zhang, Íñigo Goiri, Esha Choukse, Haoran Qiu, Rodrigo Fonseca, Josep Torrellas, Ricardo Bianchini
- **Year:** 2025
- **Title:** TAPAS: Thermal- and Power-Aware Scheduling for LLM Inference in Cloud Platforms
- **Venue:** Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2025), Vol. 2
- **DOI / URL:** https://doi.org/10.1145/3676641.3716025
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\stojkovic2025tapas.pdf` (14 pp.)

## 2. Problem Addressed
High-density AI clusters (`H100`/`A100`) run near rack thermal and datacenter power ceilings, forcing costly power-cap emergencies and hotspot throttling unless LLM placement and scheduling coordinate thermal, power, and KV-state signals.

## 3. Method / Architecture / Control Mechanism
Proposes *TAPAS*, a datacenter-scale thermal- and power-aware LLM orchestrator combining thermal-aware VM placement, KV-cache-reuse SaaS request routing, and multi-knob serving reconfiguration (GPU frequency, tensor parallelism, batch size, and model-size switching, pp. 4–9).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Grounded in telemetry from >3,000 Azure `A100`/`H100` GPUs, evaluated live on a 2-row 80-server cluster and scaled via a 1-week full-datacenter simulator calibrated within 4% error (p. 10).

## 5. Key Quantitative Results
Lowers peak cluster air temperatures by 15–17%, cuts peak row power draw by 23–24%, and safely permits +40% datacenter power oversubscription with <0.7% active power-capping duration. During 90%/75% grid power emergencies, limits quality degradation to -12%/-6% compared against -35%/-22% baseline losses (pp. 10–11).

## 6. Limitations
Targets intra-datacenter thermal/power capacity safety rather than operational grid carbon intensity (`gCO2eq/kWh`), multi-region routing, disaggregated WAN KV migration, serverless cold starts, or embodied silicon amortization.

## 7. Relevance to Research Questions (RQ1–RQ4)
Illustrates for RQ1 and RQ2 how KV-aware routing interacts with multi-knob power throttling, while showing facility-power optimizers leave cross-region decarbonization and serverless keep-alive untouched.
