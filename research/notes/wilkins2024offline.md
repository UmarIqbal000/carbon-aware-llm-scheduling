# wilkins2024offline: Offline Energy-Optimal LLM Serving: Workload-Based Energy Models for LLM Inference on Heterogeneous Systems

## 1. Citation & Access Metadata
- **Citation ID:** `wilkins2024offline`
- **Authors:** Grant Wilkins, Srinivasan Keshav, Richard Mortier
- **Year:** 2024
- **Title:** Offline Energy-Optimal LLM Serving: Workload-Based Energy Models for LLM Inference on Heterogeneous Systems
- **Venue:** ACM SIGEnergy Energy Informatics Review, Vol. 4, Issue 5, pp. 113-119
- **DOI / URL:** https://doi.org/10.1145/3727200.3727217
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\wilkins2024offline.pdf` (7 pp.)

## 2. Problem Addressed
Inference schedulers lack accurate, generalizable parametric runtime and energy models capturing joint interactions between input prompt length, generated output length, and heterogeneous GPU-CPU configurations.

## 3. Method / Architecture / Control Mechanism
Performs controlled offline inference sweeps and fits bivariate ordinary least squares (OLS) runtime and energy models incorporating input length, output length, and their cross-product interaction term (`p < 1e-11`, pp. 3–6).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Measured on Argonne's Swing cluster (`8x A100-40GB` + dual AMD EPYC) across seven dense and sparse MoE models (Falcon-7B/40B, Llama-2-7B/13B/70B, Mistral-7B, Mixtral-8x7B, Table 1, p. 2), sweeping `8–2,048` prompt tokens and `8–4,096` output tokens.

## 5. Key Quantitative Results
Two-way ANOVA demonstrates input tokens, output tokens, and their interaction term all significantly impact energy and execution time (`p < 1e-11`, Table 2, p. 5). The resulting parametric OLS energy models achieve `R^2 = 0.964–0.980` and runtime models achieve `R^2 = 0.962–0.992` across tested models (Table 3, p. 5).

## 6. Limitations
Limited to single-request/offline batch execution without continuous batching, P/D disaggregation, DVFS power throttling, time-varying grid carbon intensity, serverless keep-alive, or embodied silicon emissions.

## 7. Relevance to Research Questions (RQ1–RQ4)
Validates for RQ1 and RQ2 why scheduling energy models must explicitly track `(L_in, L_out)` interactions rather than aggregate token counts alone, supporting our phase-decomposed `(L_in, L_out)` latency/energy formulation in `DESIGN.md`.
