# chadha2023greencourier: GreenCourier: Carbon-Aware Scheduling for Serverless Functions

## 1. Citation & Access Metadata
- **Citation ID:** `chadha2023greencourier`
- **Authors:** Mohak Chadha, Thandayuthapani Subramanian, Eishi Arima, Michael Gerndt, Martin Schulz, Osama Abboud
- **Year:** 2023
- **Title:** GreenCourier: Carbon-Aware Scheduling for Serverless Functions
- **Venue:** Proceedings of the 9th International Workshop on Serverless Computing (WoSC9 2023), pp. 18-23
- **DOI / URL:** https://doi.org/10.1145/3631295.3631396
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\chadha2023greencourier.pdf` (7 pp.)

## 2. Problem Addressed
Default Kubernetes and GeoAware multi-cluster serverless schedulers ignore spatial variations in grid carbon intensity across geographically distributed clusters, placing stateless FaaS invocations in high-emission regions merely because they are close.

## 3. Method / Architecture / Control Mechanism
Implements *GreenCourier*, a custom Kubernetes scheduler priority plugin integrated with Knative, Liqo multi-cluster virtual-kubelet offloading, and WattTime/GSF Carbon-Aware SDK marginal operating emissions rate (MOER) feeds updated every 5 minutes (pp. 2–5). Quantifies operational footprint via SCI ignoring hardware embodied share `M` (Eq. 1–2, Sec. 3.1.4, p. 5).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated live on Google Kubernetes Engine (GKE): one 16-vCPU Frankfurt management cluster federating four European provider clusters (Madrid, Paris, St. Ghislain, Eemshaven; four `e2-standard-4` Skylake-SP VMs each, Table 1, p. 4), running 8 Python gRPC FunctionBench functions (Table 2, p. 4) under 10-min k6 Azure 2019 Poisson load bursts (5 repeats).

## 5. Key Quantitative Results
Cuts operational carbon per invocation by 8.7% vs. default K8s and 17.8% vs. GeoAware (summarized as 13.25% average across baselines in Sec. 5, pp. 5–6). Routing to cleaner distant grids (Madrid/Paris) incurs 10.26% geometric-mean response slowdown vs. default K8s and 16.24% vs. GeoAware, alongside 539 ms vs. 515 ms scheduling latency and 8.28 s vs. 4.53 s Liqo pod binding latency (pp. 5–6).

## 6. Limitations
Excludes embodied carbon (`M` omitted, p. 5), omits GPU accelerators and multi-GB model cold starts (where 8.28s remote binding plus weight fetch would blow sub-second TTFT budgets), and lacks SLO-enforcement or temporal keep-alive awareness.

## 7. Relevance to Research Questions (RQ1–RQ4)
Represents the canonical spatial serverless carbon scheduler for RQ1 and anchors `P3`-style spatial shifting failure modes in RQ2/RQ3 when latency-sensitive stateful LLMs encounter cross-region RTT and binding overhead.
