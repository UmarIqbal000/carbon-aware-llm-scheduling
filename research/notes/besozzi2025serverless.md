# besozzi2025serverless: High-Performance Serverless Computing: A Systematic Literature Review on Serverless for HPC, AI, and Big Data

## 1. Citation & Access Metadata
- **Citation ID:** `besozzi2025serverless`
- **Authors:** Valerio Besozzi, Matteo Della Bartola, Patrizio Dazzi, Marco Danelutto
- **Year:** 2025
- **Title:** High-Performance Serverless Computing: A Systematic Literature Review on Serverless for HPC, AI, and Big Data
- **Venue:** IEEE Access, Vol. 13, pp. 195611-195656
- **DOI / URL:** https://doi.org/10.1109/access.2025.3633989
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\besozzi2025serverless.pdf` (46 pp.)

## 2. Problem Addressed
Standard FaaS platforms constrain execution duration, statefulness, and accelerator access, creating structural friction for high-performance computing (HPC), distributed AI, and big-data workloads.

## 3. Method / Architecture / Control Mechanism
Conducts a systematic literature review narrowing 579 candidate works to 122 primary high-performance serverless papers (p. 8; 46 pp., references p. 39), categorizing runtime architectures, accelerator virtualization, hardware disaggregation, and cold-start mitigation across Tables 1–8 (pp. 4–19).

## 4. Dataset, Workload, Benchmark & Hardware Platform
122 primary FaaS systems built atop OpenWhisk, Knative, AWS Lambda, Huawei Cloud, and specialized MPI/GPU extensions.

## 5. Key Quantitative Results
Establishes quantitatively that 29.5% of high-performance serverless studies support GPUs/accelerators and 28.6% employ hardware or memory disaggregation (p. 9), alongside 596 serverless, 88 GPU, 46 cold-start, and 44 disaggregation mentions. Explicitly notes that carbon impacts of geo-distributed AI serverless execution remain insufficiently studied.

## 6. Limitations
Only 2 mentions of `carbon` and zero mentions of `llm`, `large language model`, `prefill`, `decode`, `kv cache`, `ttft`, `tpot`, or `embodied`. Disaggregation covers general remote GPU/memory pooling rather than autoregressive LLM phase splitting.

## 7. Relevance to Research Questions (RQ1–RQ4)
Bridges FaaS infrastructure and accelerator disaggregation for RQ1 while validating RQ3's focus on quantifying GPU idle vs. checkpoint cold-start carbon across serverless LLM invocations.
