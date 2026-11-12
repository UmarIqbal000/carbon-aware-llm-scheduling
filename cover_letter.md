# Cover Letter

**Date:** November 12, 2026
**To:** Editor-in-Chief, *IEEE Transactions on Sustainable Computing* (Primary Target; formatted companion builds also prepared for *Future Generation Computer Systems* / *Sustainable Computing: Informatics and Systems* and anonymized *Journal of Systems Research*)
**From:** Umar Iqbal, IILM University, Greater Noida, India (`umar.iqbal.cs28@iilm.edu`, ORCID: `https://orcid.org/0009-0004-3968-4857`)

Dear Editor and Editorial Board,

I am pleased to submit my original single-author research manuscript entitled **"Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation"** for consideration via the **traditional (subscription, zero-fee) publishing route** in *IEEE Transactions on Sustainable Computing*.

This manuscript combines a PRISMA-2020-guided literature review of 65 works (2011--November 2026) with a reproducible SimPy 4.1.2 discrete-event simulation study validated against published serving and loader benchmarks (19 calibration anchors plus 5 held-out scaling sweeps) and structured around ISO/IEC 21031:2024 Software Carbon Intensity (SCI). The work directly credits recent 2024--2026 contributions (including single-cluster heterogeneous P/D scheduling in GreenLLM (`arXiv:2412.20322`) and geo-distributed colocated LLM carbon routers (`arXiv:2610.14571`, `arXiv:2511.00807`, `arXiv:2507.09942`, `arXiv:2608.12915`, CEDAR, SLIT, CarbonRouter, GreenCache, and SPROUT)) while demonstrating that zero implemented systems yet jointly integrate prefill/decode disaggregation, cross-region WAN KV-cache transfer gating, amortized host and GPU embodied carbon, and hazard-driven serverless GPU checkpoint keep-alive.

Key verified findings across 10 paired seeds (`100..109`; exact minimum two-sided Wilcoxon floor $p = 2/2^{10} \approx 0.00195$, reported as `0.002` at three decimals) using CC-BY-4.0 Azure LLM traces, UK NESO telemetry, and Japan TSO grid data include:
1. Hybrid carbon-and-queue phase routing (`P4`) reduces operational SCI by 60.70%--60.77% and lifecycle SCI by 54.64%--54.92% on conversational traffic at 0.81%--0.82% SLO violations ($|r_{\text{rb}}|=1.000$, $p=0.002$), keeps cross-region Path C at 0.000% for $\le 25$~Gbps / $\ge 20$~ms links (reaching 0.308% only under congested 400~Gbps / 5~ms regimes, `SW5`) so gains come from Path D remote clean-grid execution and local Path A/B fallbacks, cutting bursty coding tail SLO violations by 85.22%--86.01% below unconditional spatial disaggregation (`P3`).
2. Dynamic hazard-driven serverless keep-alive (`S3`) cuts operational carbon by 7.03%--11.02% on fossil-heavy `TEPCO` (up to 23.74%--30.93% under 48--84 s loaders) while cutting SLO violations by 32.63% below 30 s static timeouts on clean `South Scotland`.
3. In wind-dominated zones, amortized hardware accounts for 93.0%--97.6% of total SCI, creating a utilization-indexed capacity rule (`SW6`): four spare clean nodes raise lifecycle emissions by +27.71% to +32.66% at nominal 1.0x load, cross break-even near 1.6x--1.7x demand, and cut net emissions by -30.63% to -36.45% at 3.0x demand.

I confirm that this manuscript is original, has not been published previously, and is not under consideration elsewhere. No conflicts of interest exist. An explicit Generative AI disclosure is included in the back matter, and all simulator source code, PRISMA records, validation checks, and reproduction scripts are publicly archived at <https://github.com/UmarIqbal000/carbon-aware-llm-scheduling>.

Sincerely,
Umar Iqbal
IILM University, Greater Noida, India
