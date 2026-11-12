# hewage2026carbon: Carbon-aware Resource Management for Latency-Sensitive Cloud Computing Environments: A Taxonomy and Future Directions

## 1. Citation & Access Metadata
- **Citation ID:** `hewage2026carbon`
- **Authors:** Tharindu B. Hewage, Shashikant Ilager, Maria Rodriguez Read, Patricia Arroba, Rajkumar Buyya
- **Year:** 2026
- **Title:** Carbon-aware Resource Management for Latency-Sensitive Cloud Computing Environments: A Taxonomy and Future Directions
- **Venue:** arXiv preprint (arXiv:2609.03270v2)
- **DOI / URL:** https://arxiv.org/abs/2609.03270
- **Document Type (`sources.csv`):** `survey`
- **Research Pillar:** `a_surveys`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\hewage2026carbon.pdf` (28 pp.)

## 2. Problem Addressed
Interactive cloud microservices and latency-sensitive workloads cannot readily tolerate multi-hour deferral or uncompensated WAN transit delays typical of batch-job carbon schedulers. Existing sustainability reviews largely treated workloads as delay-tolerant or focused strictly on grid electricity, leaving operational and embodied carbon mechanisms for strict-SLO latency-sensitive environments uncategorized.

## 3. Method / Architecture / Control Mechanism
Constructs a multi-dimensional taxonomy covering both operational and embodied carbon management across edge, cloud, and serverless architectures (Table 1, p. 8), alongside a structured synthesis of latency-sensitive resource controllers (Tables 2–3, p. 21). Classifies spatiotemporal request routing, fine-grained hardware power/frequency control, serverless idle-vs-cold-start adaptation (e.g., LACE-RL, p. 21; Caribou, pp. 13–16), and hardware lifetime/aging management.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Systematic literature corpus spanning peer-reviewed cloud, systems, and architecture venues (pp. 1–28, references p. 26). Evaluated target platforms synthesized from prior works include geo-distributed CDNs, Kubernetes/serverless clusters, and multi-region cloud environments constrained by millisecond-to-second SLAs.

## 5. Key Quantitative Results
Body-text audit documents 281 operational/general carbon mentions, 61 embodied carbon mentions, 40 SLO mentions, and 21 serverless mentions across the 28-page manuscript. Synthesizes empirical latency-carbon regimes showing that small interactive delay budgets can unlock substantial operational emission reductions—for instance, citing prior CDN routing results achieving over 60% operational carbon reduction under 60 ms latency slack (Murillo et al., cited p. 10), and contrasts RL-driven FaaS keep-alive tuning (p. 21) with hardware embodied amortization models.

## 6. Limitations
Full-text corpus screening reveals only 2 passing mentions of GPUs and zero occurrences of `llm`, `large language model`, `prefill`, `decode`, `disaggregat`, `kv cache`, `ttft`, or `tpot`. Workloads are modeled as generic microservices or DAG functions without autoregressive phase asymmetry, multi-GB KV-cache state transfers, or multi-second GPU weight cold-start penalties.

## 7. Relevance to Research Questions (RQ1–RQ4)
Establishes the closest sustainability-oriented cloud taxonomy for RQ1 while proving that latency-sensitive carbon-aware reviews omit LLM inference mechanics. Provides operational-plus-embodied conceptual framing supporting RQ4 and motivates translating millisecond SLO slack routing (`P4`) and dynamic FaaS keep-alive control (`S3`) into GPU-based LLM serving.
