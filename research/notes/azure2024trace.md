# azure2024trace: Azure LLM Inference Trace 2024

## 1. Citation & Access Metadata
- **Citation ID:** `azure2024trace`
- **Authors:** Jovan Stojkovic, Chaojie Zhang, Íñigo Goiri, Josep Torrellas, Esha Choukse
- **Year:** 2024
- **Title:** Azure LLM Inference Trace 2024
- **Venue:** Microsoft Azure Public Dataset (GitHub Repository, CC-BY; HPCA 2025 Companion Trace)
- **DOI / URL:** https://github.com/Azure/AzurePublicDataset/blob/master/AzureLLMInferenceDataset2024.md
- **Document Type (`sources.csv`):** `industry`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\docs\azure2024trace.md` (Full-text specification/dataset doc)

## 2. Problem Addressed
Academic LLM scheduling and sustainability studies lacked public production traces containing realistic prompt/output token lengths and bursty enterprise inter-arrival timing.

## 3. Method / Architecture / Control Mechanism
*(Local artifact: `docs/azure2024trace.md` companion specification to `stojkovic2025dynamollm`.)* Releases anonymized production inference invocation logs capturing `TIMESTAMP`, `ContextTokens`, and `GeneratedTokens` while stripping prompt text and user identifiers.

## 4. Dataset, Workload, Benchmark & Hardware Platform
Two production CSV workload slices (~1 hour each, verified directly in `DESIGN.md` Sec. 5.2): `AzureLLMInferenceTrace_conv.csv` (`19,366` conversational requests; ~5.53 RPS; inter-arrival CV `1.094`; mean `1,154.7` prompt / `211.1` generated tokens) and `AzureLLMInferenceTrace_code.csv` (`8,819` coding requests; ~2.57 RPS; highly bursty CV `13.152`; mean `2,047.8` prompt / `27.9` generated tokens).

## 5. Key Quantitative Results
Demonstrates extreme workload skewness between conversational decode-heavy streams (longer `GeneratedTokens`) and bursty prefill-heavy code completion (`CV = 13.152`, `~73:1` prompt-to-output ratio), directly shaping prefill-vs-decode pool sizing and serverless cold-start bursts.

## 6. Limitations
Covers ~58-minute slices without multi-day seasonality, actual GPU power draw logs, KV prefix overlap identifiers, or regional grid CI.

## 7. Relevance to Research Questions (RQ1–RQ4)
Primary workload driver for our `SimPy` simulation in `DESIGN.md` Sec. 5.2 (experiments `E1–E2` and sensitivity sweeps `SW1–SW4` addressing RQ2–RQ4).
