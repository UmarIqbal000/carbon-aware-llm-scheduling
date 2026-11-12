# mell2011nist: The NIST Definition of Cloud Computing

## 1. Citation & Access Metadata
- **Citation ID:** `mell2011nist`
- **Authors:** Peter Mell, Timothy Grance
- **Year:** 2011
- **Title:** The NIST Definition of Cloud Computing
- **Venue:** National Institute of Standards and Technology (NIST), Special Publication 800-145
- **DOI / URL:** https://doi.org/10.6028/NIST.SP.800-145
- **Document Type (`sources.csv`):** `standard`
- **Research Pillar:** `e_foundations`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\mell2011nist.pdf` (7 pp.)

## 2. Problem Addressed
Early adoption of cloud computing lacked standardized terminology distinguishing multi-tenant shared infrastructure, service abstraction tiers, and deployment models across academic, enterprise, and government contexts.

## 3. Method / Architecture / Control Mechanism
Establishes the canonical U.S. National Institute of Standards and Technology (NIST SP 800-145, 7 pp.; core definition in Sec. 2, pp. 6–7) specification defining five essential characteristics (on-demand self-service, broad network access, location-independent resource pooling, rapid elasticity, measured service), three service models (SaaS, PaaS, IaaS), and four deployment models (private, community, public, hybrid).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Normative federal/technical specification derived via NIST multi-stakeholder consensus rather than empirical workload benchmarks (Sec. 1, p. 5).

## 5. Key Quantitative Results
Codifies the foundational abstraction where providers pool compute/storage/network resources with high-level geographic location visibility (`country, state, or datacenter`, p. 6) and metered pay-per-use elastic scaling (pp. 6–7)—principles underpinning modern serverless auto-scaling and regional carbon-aware cloud federation.

## 6. Limitations
Predates GPU-accelerated inference, FaaS event-driven billing granularity, and sustainability/carbon metering (`measured service` encompasses capacity, bandwidth, and compute rather than `gCO2eq`).

## 7. Relevance to Research Questions (RQ1–RQ4)
Provides the canonical baseline definition of cloud elasticity, multi-tenant pooling, and regional abstraction framing the paper's introductory cloud-to-serverless evolution (RQ1).
