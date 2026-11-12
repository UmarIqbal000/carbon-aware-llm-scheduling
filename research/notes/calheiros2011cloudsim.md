# calheiros2011cloudsim: CloudSim: a toolkit for modeling and simulation of cloud computing environments and evaluation of resource provisioning algorithms

## 1. Citation & Access Metadata
- **Citation ID:** `calheiros2011cloudsim`
- **Authors:** Rodrigo N. Calheiros, Rajiv Ranjan, Anton Beloglazov, César A. F. De Rose, Rajkumar Buyya
- **Year:** 2011
- **Title:** CloudSim: a toolkit for modeling and simulation of cloud computing environments and evaluation of resource provisioning algorithms
- **Venue:** Software: Practice and Experience, Vol. 41, Issue 1, pp. 23-50
- **DOI / URL:** https://doi.org/10.1002/spe.995
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `e_foundations`
- **Access Level:** `abstract_only`
- **Local Artifact:** None (`abstract_only`; verified via Crossref + OpenAlex API metadata)

## 2. Problem Addressed
Evaluating cloud VM/resource provisioning algorithms and federation policies directly on commercial clouds is non-repeatable due to dynamic background load, heterogeneous infrastructures, and uncontrolled pricing/networking fluctuations.

## 3. Method / Architecture / Control Mechanism
*(Access Level: `abstract_only` — paywalled Wiley SPE publication; strictly limited to verified Crossref/OpenAlex abstract and metadata.)* Introduces CloudSim, an extensible discrete-event simulation toolkit modeling cloud data centers, virtualized hosts/VMs, application provisioning rules, and federated inter-networked cloud environments with customizable policy interfaces.

## 4. Dataset, Workload, Benchmark & Hardware Platform
*(Abstract-only record.)* Demonstrates applicability via a hybrid federated-cloud case study under fluctuating workload demand and cites adoption by researchers (e.g., HP Labs) studying energy-efficient data-center management.

## 5. Key Quantitative Results
*(Abstract-only record.)* Shows qualitatively in the federated-cloud case study that dynamic application provisioning across federated clouds improves application QoS compliance under time-varying demand without incurring physical cluster non-repeatability.

## 6. Limitations
*(Abstract-only record.)* Classic VM/cloudlet abstraction lacks native autoregressive LLM phase separation (prefill vs. decode), HBM KV-cache eviction dynamics, GPU weight cold starts, and sub-hourly regional carbon accounting; full-text quantitative metrics not verified behind publisher paywall.

## 7. Relevance to Research Questions (RQ1–RQ4)
Establishes the foundational discrete-event simulation precedent in cloud scheduling (widely cited in `alam2026computing` and `yang2025container`) and explains why our `SimPy` simulation extends discrete-event modeling with LLM phase, KV, and carbon primitives.
