# shahrad2020serverless: Serverless in the Wild: Characterizing and Optimizing the Serverless Workload at a Large Cloud Provider

## 1. Citation & Access Metadata
- **Citation ID:** `shahrad2020serverless`
- **Authors:** Mohammad Shahrad, Rodrigo Fonseca, Íñigo Goiri, Gohar Chaudhry, Paul Batum, Jason Cooke, Eduardo Laureano, Colby Tresness, Mark Russinovich, Ricardo Bianchini
- **Year:** 2020
- **Title:** Serverless in the Wild: Characterizing and Optimizing the Serverless Workload at a Large Cloud Provider
- **Venue:** 2020 USENIX Annual Technical Conference (USENIX ATC 2020), pp. 205-218
- **DOI / URL:** https://www.usenix.org/conference/atc20/presentation/shahrad
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `d_modeling_traces_standards`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\shahrad2020serverless.pdf` (15 pp.)

## 2. Problem Addressed
Fixed keep-alive intervals in FaaS providers waste vast host DRAM holding infrequently invoked functions warm while still suffering cold starts on bursty or irregular workloads.

## 3. Method / Architecture / Control Mechanism
Characterizes production Azure Functions arrivals and develops a *Hybrid Histogram* + ARIMA keep-alive predictor (separating short-interval distribution heads/tails and coefficient-of-variation gating) integrated directly into Apache OpenWhisk (pp. 8–12).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Production 2-week Microsoft Azure Functions telemetry trace (July 15–28, 2019) simulated and prototyped on a 19-VM OpenWhisk testbed (pp. 4–12).

## 5. Key Quantitative Results
Documents canonical FaaS skew: 50% of functions execute in <1 s and 90% in <=60 s; 81% are invoked <=1/min and 45% <=1/hr, while 18.6% of apps generate 99.6% of traffic; 50% consume <=170 MB RAM and 90% <=400 MB (pp. 5–7). Hybrid Histogram lowers 75th-percentile cold starts relative to a fixed 10-min policy while trimming worker memory 15.6% and cutting avg/P99 execution times 32.5%/82.4% at just `835.7 us` per policy update (pp. 10–12).

## 6. Limitations
CPU/RAM FaaS workload characterization only; excludes GPU hardware, multi-GB model checkpoints, power/energy tracking, and carbon intensity.

## 7. Relevance to Research Questions (RQ1–RQ4)
Canonical empirical origin of serverless keep-alive modeling and burst CV analysis underpinning RQ3 (`S1–S3` keep-alive mechanics in `DESIGN.md`).
