# yang2025container: A Survey on Task Scheduling in Carbon-Aware Container Orchestration

## 1. Citation & Access Metadata
- **Citation ID:** `yang2025container`
- **Authors:** Jialin Yang, Zainab Saad, Jiajun Wu, Xiaoguang Niu, Henry Leung, Steve Drew
- **Year:** 2025
- **Title:** A Survey on Task Scheduling in Carbon-Aware Container Orchestration
- **Venue:** arXiv preprint (arXiv:2508.05949v1; submitted to ACM Computing Surveys)
- **DOI / URL:** https://arxiv.org/abs/2508.05949
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\yang2025container.pdf` (35 pp.)

## 2. Problem Addressed
Container orchestration engines such as Kubernetes schedule workloads primarily for CPU/memory balancing, availability, and network locality, ignoring spatial and temporal variations in grid carbon intensity (`gCO2eq/kWh`) across multi-cluster cloud infrastructure.

## 3. Method / Architecture / Control Mechanism
Follows a PRISMA-aligned dual-layer synthesis organizing infrastructure-level energy telemetry (Kepler, KubeWatt, eBPF power estimation) and orchestration-level carbon-aware scheduling policies across single-cluster and federated multi-cluster Kubernetes topologies (Table 1, p. 3; Tables 2–5, pp. 10–13). Reviews Software Carbon Intensity (SCI) accounting (Sec. 6.2), elastic temporal autoscaling (CarbonScaler, Caspian), serverless routing (GreenCourier, CASA), and DRL/federated schedulers.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Synthesizes Kubernetes, Knative, Liqo, and CloudSim/CloudSim Plus container scheduling studies (Tables 2–5, pp. 10–13), citing Electricity Maps and WattTime telemetry signals alongside macro U.S. data-center electricity projections increasing from 176 TWh toward 580 TWh by 2028 (p. 5).

## 5. Key Quantitative Results
Reports benchmarked operational emission savings from cataloged container orchestrators, including up to 51% reductions via elastic temporal scaling in CarbonScaler and up to 33% reductions in Caspian (Tables 2–5, pp. 10–13), alongside 25 serverless mentions, 20 GPU mentions (e.g., GreenFlow, CASA), and 2 cold-start mentions across the 35-page body (references p. 30).

## 6. Limitations
Contains zero mentions of `prefill`, `decode`, `disaggregat`, `kv cache`, `ttft`, `tpot`, and zero mentions of `embodied` carbon (`llm` appears only once as contextual motivation). Treats GPU pods as monolithic containerized tasks rather than stateful, phase-split autoregressive engines with high-bandwidth KV transfers.

## 7. Relevance to Research Questions (RQ1–RQ4)
Anchors RQ1 on Kubernetes/serverless operational carbon orchestration and reinforces why container-level carbon metrics (`SCI` Sec. 6.2) must be extended to GPU KV-cache transfer energy and embodied amortization (`DESIGN.md` Eq. 11–13) when serving LLMs.
