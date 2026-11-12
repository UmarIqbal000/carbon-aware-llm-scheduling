# wiesner2021letswait: Let's Wait Awhile: How Temporal Workload Shifting Can Reduce Carbon Emissions in the Cloud

## 1. Citation & Access Metadata
- **Citation ID:** `wiesner2021letswait`
- **Authors:** Philipp Wiesner, Ilja Behnke, Dominik Scheinert, Kordian Gontarska, Lauritz Thamsen
- **Year:** 2021
- **Title:** Let's Wait Awhile: How Temporal Workload Shifting Can Reduce Carbon Emissions in the Cloud
- **Venue:** Proceedings of the 22nd International Middleware Conference (Middleware 2021), pp. 260-272
- **DOI / URL:** https://doi.org/10.1145/3464298.3493399
- **Document Type (`sources.csv`):** `empirical`
- **Research Pillar:** `b_carbon_schedulers`
- **Access Level:** `full_text`
- **Local Artifact:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper\research\pdfs\wiesner2021letswait.pdf` (13 pp.)

## 2. Problem Addressed
Grid carbon intensity exhibits strong diurnal and weekday-weekend cycles, yet traditional cloud job schedulers dispatch workloads immediately upon submission, forfeiting opportunities to align delay-tolerant executions with low-carbon electricity windows.

## 3. Method / Architecture / Control Mechanism
Formulates and evaluates temporal workload shifting strategies—*Wait Awhile* bounded delay windows (`+-2h` to `+-8h`), *Next Workday* overnight deferral, and *Semi-Weekly* pause-and-resume execution via job checkpointing—balancing queuing concurrency surges against forecasted regional carbon intensity (pp. 4–10).

## 4. Dataset, Workload, Benchmark & Hardware Platform
Evaluated using the LEAF discrete-event simulation environment driven by 2020 hourly ENTSO-E and CAISO grid carbon signals across four regions (Germany `311.4`, Great Britain `211.9`, France `56.3`, California `279.7 gCO2/kWh` mean, p. 6) and two traces: Scenario I (`+-8h` synthetic jobs) and Scenario II (3,387 StyleGAN2-ADA training runs totaling 325 MWh, pp. 8–10).

## 5. Key Quantitative Results
Under 5% CI forecast error (`+-8h` shifting), Scenario I lowers emissions by 11.2% in Germany, 7.4% in Great Britain, and 4.1% in France (without forecast noise, `+-6h`/`+-8h` yield 13.1% and 33.7%, p. 8). In Scenario II, Next Workday shifting saves 2.5–6.3% non-interruptibly and 5.7–8.5% interruptibly, while Semi-Weekly saves 6.1–14.4% non-interruptibly and 13.3–18.9% interruptibly (8.9 tCO2 in Germany vs. 1.2 tCO2 in France; checkpoint-resume adds 24.2–36.6% extra savings in EU grids and 131.2% in California, pp. 9–10). Peak cluster concurrency rises up to +42% (64 vs. 45 concurrent jobs, Sec. 5.3, p. 10).

## 6. Limitations
Excludes interactive sub-second LLM serving SLOs (`TTFT`/`TPOT`), spatial cross-region shifting, hardware embodied carbon, and KV-cache memory occupancy; long temporal pauses (`+-8h` to weekend deferral) are incompatible with interactive chatbots.

## 7. Relevance to Research Questions (RQ1–RQ4)
Foundational empirical anchor for RQ1 and RQ2 showing both how temporal deferral unlocks operational savings on coal/gas grids (Germany/CAISO) and why latency-constrained LLM requests must substitute spatial or phase-aware mechanisms instead of multi-hour delays.
