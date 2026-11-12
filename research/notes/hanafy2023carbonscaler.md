# hanafy2023carbonscaler: CarbonScaler: Leveraging Cloud Workload Elasticity for Optimizing Carbon-Efficiency

## 1. Citation & Access Metadata
- **Citation ID:** `hanafy2023carbonscaler`
- **Authors:** Walid A. Hanafy, Qianlin Liang, Noman Bashir, David Irwin, Prashant Shenoy
- **Year:** 2023
- **Title:** CarbonScaler: Leveraging Cloud Workload Elasticity for Optimizing Carbon-Efficiency
- **Venue:** Proceedings of the ACM on Measurement and Analysis of Computing Systems (POMACS), Vol. 7, No. 3, pp. 1-28
- **DOI / URL:** https://doi.org/10.1145/3626788
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\hanafy2023carbonscaler.pdf` (28 pp.)

## 2. Problem Addressed
Conventional suspend-resume temporal carbon schedulers toggle jobs binary on/off, missing non-linear efficiency sweet spots of elastically scalable cloud jobs whose resource capacity (`1..M` nodes) can expand during green grid troughs and shrink during carbon spikes.

## 3. Method / Architecture / Control Mechanism
Introduces an `O(nM log nM)` Greedy Marginal Capacity/Carbon allocator computing optimal per-epoch instance counts from profiled throughput scaling curves and marginal carbon forecasts, implemented in a 2,500-SLOC Go Kubernetes/Kubeflow controller and paired with the *Carbon Advisor* simulator (pp. 6–14).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Trace-driven evaluation over 2020–2022 hourly Electricity Maps data across 37 regions (and 16 AWS zones, pp. 13, 19) using ResNet18, EfficientNetB1, VGG16 training and MPI N-body simulations (Table 1, p. 12), cross-validated against a 15-run cloud testbed.

## 5. Key Quantitative Results
Matches real cloud runs within <5% simulation error (p. 14). Cuts operational emissions 42% on MPI N-body (`T=2l`, p. 14), 36% in California and 51% in the Netherlands vs. carbon-agnostic baselines (and 22%/37% over suspend-resume at `T=1.5l`, p. 17), remaining within 1.2–8% of oracle scaling (p. 16). Saves 30–42% across cluster scales (p. 18) and 19% mean (16% median) across 16 AWS zones (p. 19). Under 30% CI forecast error, P95 emissions degrade by <=4% (p. 20), incurring 20–40s scaling lag and a one-time 40-min profiling overhead (p. 21).

## 6. Limitations
Explicitly omits hardware embodied carbon (p. 22), assumes batch slack ratios (`1.5x–2x` runtime deadline) incompatible with sub-second interactive LLM TTFT/TPOT targets, and treats compute nodes homogeneously without prefill/decode KV state pinning.

## 7. Relevance to Research Questions (RQ1–RQ4)
Key baseline comparison in RQ1 and informs RQ2/RQ4 elastic scaling limits: scaling out replicas during low-CI windows can cut operational emissions unless embodied hardware amortization (`DESIGN.md` H4) or 20–40s cold-start lag outweighs the green window.
