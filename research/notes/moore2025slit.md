# moore2025slit: Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed Cloud Datacenters

## 1. Citation & Access Metadata
- **Citation ID:** `moore2025slit`
- **Authors:** Hayden Moore, Sirui Qi, Ninad Hogade, Dejan Milojicic, Cullen Bash, Sudeep Pasricha
- **Year:** 2025
- **Title:** Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed Cloud Datacenters
- **Venue:** Proceedings of the Great Lakes Symposium on VLSI 2025 (GLSVLSI 2025), pp. 929-934
- **DOI / URL:** https://doi.org/10.1145/3716368.3735301
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\v2_downloads\slit_2505.23554.txt` (6 pp.)

## 2. Problem Addressed
SLIT co-optimizes TTFT, grid carbon, water scarcity/TOU cost across 5 geo-distributed LLM datacenters using an analytical prefill queueing model.

## 3. Method / Architecture / Control Mechanism
- **Taxonomy Level:** `Cross-Region / Multi-DC`
- **Phase Awareness:** `Phase-Agnostic LLM`
- **Spatial / Temporal Scope:** `Spatial Multi-Region`
- **Control Knobs:** Multi-Objective Geo-Distributed Routing (TTFT + Grid CI + Water WUE/AWS + TOU Cost)
- **Carbon / Energy Signal:** Grid CI + Water Carbon
- **Embodied Carbon Considered:** No

## 4. Dataset, Workload, Benchmark & Hardware Platform
- **Workload:** Geo-Distributed LLM Requests (Chatbot Arena / ShareGPT / Coding)
- **Hardware / GPU Profile:** Homogeneous A100/H100 Datacenter Nodes
- **Evaluation Platform:** Geo-Distributed Python Simulator (5 Global Sites)

## 5. Key Quantitative Results
Single-objective SLIT cuts carbon/water up to 98-99% vs static/Helix/Splitwise; SLIT-Balance delivers joint carbon-water-TTFT Pareto fronts (pp. 4-5)

## 6. Limitations
Treats each site as monolithic queue: omits P/D disaggregation, cross-region WAN KV migration, embodied carbon, and serverless cold starts

## 7. Verification Notes
Part A1 verified full text (arXiv:2505.23554, 6 pp.) and Crossref GLSVLSI 2025 DOI 10.1145/3716368.3735301. No P/D disaggregation, no KV transfer, no embodied carbon, no serverless keep-alive.
