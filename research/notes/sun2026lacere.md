# sun2026lacere: Green or Fast? Learning to Balance Cold Starts and Idle Carbon in Serverless Computing

## 1. Citation & Access Metadata
- **Citation ID:** `sun2026lacere`
- **Authors:** Bowen Sun, Christos D. Antonopoulos, Evgenia Smirni, Bin Ren, Nikolaos Bellas, Spyros Lalis
- **Year:** 2026
- **Title:** Green or Fast? Learning to Balance Cold Starts and Idle Carbon in Serverless Computing
- **Venue:** Proceedings of the 26th IEEE International Symposium on Cluster, Cloud, and Internet Computing (CCGrid 2026, Accepted Preprint; arXiv:2602.23935v1)
- **DOI / URL:** https://arxiv.org/abs/2602.23935
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\sun2026lacere.pdf` (12 pp.)

## 2. Problem Addressed
Serverless cold starts incur heavy reload latency and initialization energy bursts, while aggressive static keep-alive timers burn excessive idle energy during carbon-intensive grid hours; static thresholds fail across skewed FaaS inter-arrival distributions.

## 3. Method / Architecture / Control Mechanism
Introduces *LACE-RL*, an off-policy Deep Q-Network (DQN) controller dynamically selecting discrete keep-alive durations `K_keep in {1, 5, 10, 30, 60} s` using an application-tunable carbon-vs-latency weight `lambda_carbon` and real-time grid CI signals (Eq. 2–6, pp. 2–5).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Benchmarks idle power multipliers (`lambda_idle` 0.21–0.83, mean ~0.48, Table II, p. 7) via Kepler RAPL over 10 FunctionBench tasks on dual AMD EPYC 7513 servers, then simulates an EC2 `m5` cluster driven by the Huawei Cloud Serverless Trace (>300M invocations, >1,500 functions, 80/10/10 train/val/test split) and Electricity Maps hourly CI traces (p. 7).

## 5. Key Quantitative Results
On the General trace, LACE-RL lowers cold starts by 51.7% (13,958 vs. 28,891 under Huawei's default policy), reduces idle carbon by 77.08%, and trims mean execution latency from 1.43 s to 1.05 s—staying within 6.18% carbon and 7.20% cold starts of Oracle (Table III, pp. 8, 10). On Long-tailed workloads, achieves `404.76 gCO2` total emissions and 17.75 s average latency (within 8.97% carbon and 11.15% latency of Oracle, pp. 9–10).

## 6. Limitations
Evaluates CPU container keep-alive (`~0.48` idle fraction) on single-cluster servers without GPU HBM idle draw, multi-second 70B LLM weight deserialization (`10.3–84.0 s`), cross-region routing, or embodied hardware amortization.

## 7. Relevance to Research Questions (RQ1–RQ4)
Directly calibrates our `S3` serverless controller baseline in RQ3 and `DESIGN.md` Sec. 4.4 (`K in {1, 5, 10, 30, 60} s`, `lambda_idle` formulation), which `S3` extends to GPU LLM cold-start reloads and hardware-exact A100/H100 idle power.
