# qi2024casa: CASA: A Framework for SLO- and Carbon-Aware Autoscaling and Scheduling in Serverless Cloud Computing

## 1. Citation & Access Metadata
- **Citation ID:** `qi2024casa`
- **Authors:** Sirui Qi, Hayden Moore, Ninad Hogade, Dejan Milojicic, Cullen Bash, Sudeep Pasricha
- **Year:** 2024
- **Title:** CASA: A Framework for SLO- and Carbon-Aware Autoscaling and Scheduling in Serverless Cloud Computing
- **Venue:** 2024 IEEE 15th International Green and Sustainable Computing Conference (IGSC 2024), pp. 1-6
- **DOI / URL:** https://doi.org/10.1109/igsc64514.2024.00010
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\qi2024casa.pdf` (6 pp.)

## 2. Problem Addressed
Geographic carbon routing cannot satisfy strict local/sovereign FaaS deployments or bursty 0–13x traffic spikes that cause concurrent cold-start storms and SLO failures under single-cluster autoscaling.

## 3. Method / Architecture / Control Mechanism
Develops *CASA*, a single-cluster real-time FaaS autoscaler and pod scheduler running dual-antagonist self-guided local searches (an SLO-repair agent paired against a carbon-reduction agent enforcing `Cstr=5%` SLO violation cap, Fig. 6–7, p. 4) over 15-minute windows, modeling execution power, grid CO2, indirect cooling water CO2 (Eq. 6, p. 3), and Knative `T_cold=15s` penalties.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Tested on Knative / AMD EPYC 7713 nodes (128 cores, 64 GB RAM, p. 5) and scaled across 2–32 node cluster simulations (`20x–320x` intensity) driven by Azure Functions 2019 traces and Tampa, Florida grid intensity (pp. 4–5).

## 5. Key Quantitative Results
On a 4-node baseline cluster (`R=20x`), CASA outperforms Score by 1.9x in energy/carbon and 1.6x in utilization, and at `5x` burst load cuts carbon 2.2x, 2.8x, and 1.9x against Score, Hybrid, and Q-table RL baselines respectively (p. 5). Across 2–32 nodes, RL fails to converge within 3 minutes at 16–32 nodes due to Q-table explosion, whereas CASA scales cleanly (reporting up to 2.6x SLO / 1.4x carbon improvement vs. RL in Sec. VI-C.4, p. 5; note Sec. VII conclusion swaps the 2.6x/1.4x labels between carbon and SLO).

## 6. Limitations
Targets CPU FaaS containers (`15s` pod boot) without GPU power modeling, phase-disaggregated LLM execution, multi-region grid routing, or embodied silicon emissions.

## 7. Relevance to Research Questions (RQ1–RQ4)
Supports RQ1 and RQ3 (`DESIGN.md` `T_cold` grace comparison) by modeling intra-cluster carbon-vs-SLO tradeoffs and demonstrating why lightweight search avoids tabular RL state explosion.
