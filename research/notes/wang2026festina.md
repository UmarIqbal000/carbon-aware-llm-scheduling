# wang2026festina: Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs (Extended)

## 1. Citation & Access Metadata
- **Citation ID:** `wang2026festina`
- **Authors:** Tianyu Wang, Gourav Rattihalli, Aditya Dhakal, Longfei Shangguan, Dejan Milojicic
- **Year:** 2026
- **Title:** Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs (Extended)
- **Venue:** Proceedings of the 2026 ACM SIGOPS Annual Technical Conference (SIGOPS ATC 2026, Accepted Preprint; arXiv:2606.30391v2)
- **DOI / URL:** https://arxiv.org/abs/2606.30391
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `c_llm_serving`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\wang2026festina.pdf` (19 pp.)

## 2. Problem Addressed
Multi-model serverless LLM sharing on GPUs (`MuxServe`, `Aegaeon`) packs co-located workers at fixed peak clocks and wastes over half of available SLO latency slack plus high idle power across inactive replicas.

## 3. Method / Architecture / Control Mechanism
Introduces *Festina*, coordinating a 3D hardware lookup table (`795–1635 MHz` GPU freq @ 90 MHz steps x `10–100%` MPS SM share @ 10% steps x `256–8192` token bins, p. 6), MPS spatial sharing, dynamic DVFS throttling, and *Elastic Worker Retention* (EWR) proactive idle shutdown/preload (`Festina+`) within strict multi-LLM SLOs (pp. 4–10).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Tested on `8x H100` NVLink GPUs running 16–32 concurrent LLMs (Qwen, Llama, Yi, Mistral families) over ShareGPT, `ix2`, and `ox2` traces against ServerlessLLM, MuxServe, Aegaeon, and AegVoltana (pp. 10–13; Table 1, p. 3).

## 5. Key Quantitative Results
Characterizes 24% (MuxServe) to >52% (Aegaeon) wasted SLO power slack (p. 4). Festina cuts GPU energy up to 56% (>=22% under heavy loads; `Festina+` reaches 48–64% via EWR shutdown, while EWR shrinks cold starts 85% / 7x) within 2% SLO attainment parity (pp. 1, 11–12), adding <1 ms global overhead at 10k GPUs and 0.1 ms locally (pp. 7–8). Fig. 15 (p. 13) tests a PD-disaggregated variant showing -1.5% SLO from unoptimized KV yet -7% further energy reduction.

## 6. Limitations
Single-cluster NVLink focus; omits grid carbon intensity (`gCO2eq/kWh`), multi-region WAN shifting, and embodied GPU lifecycle carbon.

## 7. Relevance to Research Questions (RQ1–RQ4)
Directly reinforces RQ3 and compares cleanly against `S3` (`DESIGN.md`): illustrates the synergy between serverless idle retention (`EWR`) and dynamic GPU power slack, while leaving grid carbon and cross-region P/D unaddressed.
