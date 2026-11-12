# Discrete-Event Simulation Design Specification (`SimPy`)

**Project:** Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation  
**Author:** Umar Iqbal (`umar.iqbal.cs28@directiilm.edu`), IILM University, Greater Noida, India  
**Phase:** 3A (Experimental & Simulation Architecture Design)  
**Parameter Provenance:** [`parameter_sources.json`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/parameter_sources.json)  
**Trace Provenance:** [`DATA_MANIFEST.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/DATA_MANIFEST.md)

---

## 1. Explicit Scope & Methodological Boundary

> **IMPORTANT SCOPE NOTE:** All empirical experiments produced from this design are **parameterized discrete-event simulations** executed in Python using **`SimPy 4.1.2`**, **not** physical multi-GPU or multi-region production cluster deployments. Consistent with the precedent noted in the cloud scheduling review literature (where 70% of AI cloud/serverless resource-management studies evaluate multi-region policies via discrete-event simulation), this framework models queue dynamics, KV-cache network transfers, checkpoint cold-start reloads, sublinear power scaling, and coupled operational-plus-embodied carbon accounting using peer-reviewed hardware/serving parameters and real `CC-BY-4.0` workload and grid-intensity traces. Every calibrated heuristic assumption (cross-region WAN RTT, commodity WAN bandwidth, sublinear MFU exponent caveat, and cold-start GPU power fraction) is explicitly separated from published physical measurements in Section 5.3.

---

## 2. Research Hypotheses (Mapped to RQ2, RQ3, and RQ4)

| ID | Mapped RQ | Hypothesis Statement | Null Comparison / Falsification Criterion |
|---|---|---|---|
| **H1** | **RQ2** (Phase-Split Asymmetric Carbon Sensitivity) | Under mixed conversational and code-completion LLM workloads, separating compute-bound prefill onto high-throughput GPUs in low-carbon regions while placing memory-bound decode onto power-capped (`50–70%` TDP) or efficiency-matched tiers reduces operational carbon (`gCO2eq/1k tokens`) by **>= 15–30%** relative to `B1: Carbon-Agnostic Colocated` and `B2: Carbon-Agnostic Disaggregated` while keeping P90 `TTFT` and `TPOT` SLO violation rates below **5%**. | H1 is rejected if phase-disaggregated carbon routing fails to reduce operational `gCO2eq/1k tokens` over `B1`/`B2` at matched SLO attainment (`<= 5%` violations). |
| **H2** | **RQ2** (KV-Cache Transfer vs. Recomputation Crossover) | Unconditional cross-region P/D separation degrades tail `TTFT` and wastes network/decode energy when cross-region KV-cache transfer delay plus WAN energy exceeds remote prefill recomputation (the carbon-extended Sisodia crossover boundary). The proposed **`P4: Carbon+KV-Aware Hybrid Router`**—which dynamically switches among local colocation, intra-region P/D, cross-region P/D KV forwarding, and remote recomputation—achieves lower combined carbon and fewer SLO violations than both `B2` and unconditional **`P3: Spatiotemporal Carbon-Aware Disaggregated`** across small regional carbon differentials (`Delta_CI <= 50 gCO2eq/kWh`) and long prompts (`ContextTokens >= P95`). | H2 is rejected if unconditional cross-region P/D (`P3`) strictly Pareto-dominates `P4` across all context lengths and regional carbon gaps. |
| **H3** | **RQ3** (Serverless Keep-Alive Idle-vs-Reload Carbon Trade-Off) | Under bursty serverless arrivals (`AzureLLMInferenceTrace_code`, inter-arrival `CV = 13.152`), fixed long keep-alive (`k = 60 s`) incurs excessive GPU idle carbon during dirty-grid intervals, whereas scale-to-zero (`k = 0 s`) induces repeated multi-second checkpoint-loading energy spikes and cold-start SLO breaches. Our **`S3: Dynamic Carbon-Aware Keep-Alive`** controller—which scales `k in {1, 5, 10, 30, 60} s` inversely with grid carbon intensity `CI_r(t)` and burst reuse probability—reduces total serverless operational carbon (`gCO2eq/1k tokens`) compared to both `S1` (`k = 0`) and `S2` (`k = 30 s`/`60 s`) at equal or lower cold-start SLO violations. | H3 is rejected if any static keep-alive `k` achieves equal or lower total operational carbon and SLO violation rate than dynamic `S3` across dirty and volatile grid regimes. |
| **H4** | **RQ4** (Operational vs. Amortized Embodied Carbon Dominance) | When GPU and host embodied emissions (`EcoServe` / `GreenSKU`) are amortized across standard (`4 yr`) or asymmetric (`9-yr host / 3-yr GPU`) lifespans, amortized embodied carbon accounts for **> 50% of total lifecycle carbon** (`gCO2eq/1k tokens`) in low-carbon regions (`South Scotland` mean `9.75 gCO2eq/kWh`, `North East England` `28.83 gCO2eq/kWh`). Consequently, purely operational-carbon schedulers that scale out redundant GPUs across clean regions can paradoxically *increase* total SCI emissions compared to utilization- and lifetime-aware policies (`P4`). | H4 is rejected if embodied carbon remains a negligible (`< 15%`) fraction of total `gCO2eq/1k tokens` across low-carbon regions or if over-provisioned low-carbon replication consistently minimizes total lifecycle carbon. |

---

## 3. Evaluated Scheduling Policies & Baselines

### Track A: Cloud & Multi-Region Cluster Serving (Addressing RQ2 & RQ4)

1. **`B1: Carbon-Agnostic Colocated` (Baseline):**  
   Models conventional continuous-batching engines (vLLM / Sarathi-Serve colocated pools) running prefill and decode on the same GPU pool (`A100-80GB` or `H100-80GB`), with uniform round-robin / latency-nearest regional load balancing and zero grid carbon awareness (`CI_r(t)` ignored).
2. **`B2: Carbon-Agnostic Disaggregated` (Baseline):**  
   Models intra-region P/D phase disaggregation (Splitwise / DistServe) over high-speed intra-DC interconnect (`NVLink 600 GB/s` or `200–400 Gbps InfiniBand`). Separates prefill and decode pools to eliminate chunked/continuous-batching interference, optionally capping decode GPU power, but routes requests without `CI_r(t)` awareness.
3. **`P3: Spatiotemporal Carbon-Aware Disaggregated` (Spatial Carbon Baseline):**  
   Routes prefill and decode stages toward regions offering lower instantaneous `CI_r(t)` subject to coarse SLA feasibility (`RTT_wan <= slack_budget`), always executing prefill-to-decode KV-cache forwarding across regions whenever `r_P != r_D`. Represents naive geographic carbon shifting applied to disaggregated serving without KV-crossover intelligence.
4. **`P4: Carbon+KV-Aware Hybrid Router` (Proposed Unified Scheduler):**  
   Evaluates four candidate execution paths per incoming request `(i, L_in, L_out, SLO_i)` across active regions `r in R` at time `t`:
   - *Path A (Intra-Region Colocated):* Low-overhead local execution when queues are shallow or cross-region slack is exhausted.
   - *Path B (Intra-Region P/D Disaggregated):* High-speed local NVLink/IB P/D separation with decode power capping (`0.50–0.70x TDP`) when utilization rises.
   - *Path C (Cross-Region P/D with Pipelined KV Transfer):* Prefill in ultra-clean region `r_P`, stream compressed/layered KV over WAN to decode pool in `r_D` only when the **carbon-extended Sisodia crossover condition** (Eq. 9) is strictly satisfied.
   - *Path D (Low-Carbon Remote Execution / Recomputation):* Shift entire request (or recompute prompt on clean region `r_dest`) when `(C_op_shift + C_emb_alloc) < C_local` and `RTT + T_exec <= TTFT_SLO`.
   Selects the feasible path minimizing `w_c * (C_op + C_emb) + w_q * Q_risk` where embodied tie-breaking penalizes spawning cold or underutilized replicas.
5. **`P5: Oracle Future-Carbon Disaggregated` (Theoretical Lower-Carbon Reference):**  
   Identical decision space to `P4`, but given look-ahead over future 30-minute `CI_r(t)` intervals (instead of lagged/current grid telemetry) to quantify scheduling sensitivity to grid intensity forecast noise (`UK NESO forecast` vs `actual`).

### Track B: Serverless GPU LLM Serving (Addressing RQ3 & RQ4)

6. **`S1: Scale-to-Zero Cold` (`k = 0 s`):**  
   Immediately evicts GPU model weights (`130 GB` FP16 for 70B or `~26 GB` for 13B) upon queue drain (`+ 15 s` optional Knative shutdown grace parameter in sensitivity sweeps). Zero idle GPU power, paying full `T_cold` and `E_cold` on every gap exceeding service completion.
7. **`S2: Static Keep-Alive` (`k = 30 s` default; `k = 60 s` sensitivity):**  
   Retains active GPU workers in warm memory for a fixed window `k` after the last request completes (`lambda_idle = 0.20 * P_TDP` per LACE-RL, or exact GPU idle draw `60 W H100` / `100 W A100`), agnostic to instantaneous `CI_r(t)`.
8. **`S3: Dynamic Carbon-Aware Keep-Alive` (Proposed Serverless Controller):**  
   Periodically updates keep-alive window `k* in {1, 5, 10, 30, 60} s` (matching LACE-RL's discrete action grid) using a lookback arrival rate EWMA (`lambda_hat`) and instantaneous normalized regional carbon intensity `CI_norm(t) = CI_r(t) / CI_r_max`:
   - During **high-carbon intervals** (`CI_norm > theta_high`), shortens `k` toward `{1, 5, 10} s` whenever expected idle energy `E_idle(k) * CI(t)` exceeds expected amortized cold-start penalty `p_miss(k) * E_cold * CI(t)` plus SLO tail penalty.
   - During **abundant clean-grid intervals** (`CI_norm < theta_low`) or bursty episodes (`CV > 2`), extends `k` toward `{30, 60} s` to absorb spikes with low operational carbon penalty.
   - Evaluates checkpoint tier speed across `ServerlessLLM` (`10.3 s` for 70B / `2.0 s` for 13B) vs. `Safetensors` (`48.0 s` / `8.2 s`) vs. `PyTorch` (`84.0 s` / `14.0 s`).

---

## 4. Mathematical Simulation Model

### 4.1 Phase Execution & Queueing Latency

For request `i` arriving at timestamp `t_i` with prompt length `L_in(i)` (`ContextTokens`) and output length `L_out(i)` (`GeneratedTokens`):

1. **Prefill Service Time** on GPU tier `g` running active prefill batch of `N_P` prompt tokens:
   $$T_{\text{exec},P}(i, g) = \tau_{P,0}(g) \cdot \left(\frac{L_{\text{in}}(i)}{L_{\text{ref}}}\right) \cdot \phi_{\text{batch}}(N_P)$$
   where uncontended single-request latency anchors match Splitwise Table IV (`Llama-70B`: Coding `TTFT = 185 ms` on A100 / `95 ms` on H100; Conv `155 ms` on A100 / `84 ms` on H100 at trace median prompt lengths).

2. **Decode Step Latency (Memory-Bandwidth Bound):**  
   Each autoregressive iteration for an active decode batch of `B_D` sequences sharing total resident KV context `K_res` completes in:
   $$t_{\text{step}}(g, B_D, K_{\text{res}}) = \max\left(\tau_{D,\min}(g),\ \tau_{D,0}(g) \cdot \left(1 + \alpha_{\text{mem}}(g) \cdot \frac{K_{\text{res}}}{\text{BW}_{\text{HBM}}(g)}\right)\right)$$
   Total decode execution time is $T_{\text{exec},D}(i) = L_{\text{out}}(i) \cdot t_{\text{step}}$. Uncontended baselines follow Splitwise Table IV (`TBT = 52 ms / 40 ms` on A100 vs `31 ms / 28 ms` on H100) and DynamoLLM (`20–30 ms` decode steps). Under **colocated (`B1`)** execution, prefill batches preempt or stall concurrent decode iterations, introducing contention inflation factor $\psi_{\text{coloc}}$ calibrated to Sarathi/Splitwise stall interference, whereas **disaggregated (`B2, P3, P4`)** pools isolate decode from prefill compute interference.

3. **End-to-End Request Metrics:**
   $$\text{TTFT}_i = T_{\text{cold},i} + T_{\text{queue},P,i} + T_{\text{exec},P,i} + T_{\text{kv\_sync},i} + \text{RTT}_{\text{client},i}$$
   $$\text{TPOT}_i = \frac{T_{\text{queue},D,\text{wait},i} + \sum_{k=1}^{L_{\text{out}}(i)} t_{\text{step},k}}{L_{\text{out}}(i)}$$

---

### 4.2 Sublinear MFU Phase Power & Power Capping Model

Following **Özcan et al. (2025, `arXiv:2507.11417v1`, Eq. 1, p. 3)**, instantaneous GPU power as a function of Model FLOPs Utilization ($\text{mfu}$) and active power cap ratio $c_{\text{cap}} \in (0, 1]$ (**Splitwise §III-F, §IV-D**) is:
$$P_{\text{gpu}}(\text{mfu}, c_{\text{cap}}) = P_{\text{idle}} + \left(\min\left(P_{\max,\text{inst}},\ c_{\text{cap}} \cdot P_{\text{TDP}}\right) - P_{\text{idle}}\right) \cdot \left(\min\left(1.0,\ \frac{\text{mfu}}{\text{mfu}_{\text{sat}}}\right)\right)^{\gamma}$$
with $\text{mfu}_{\text{sat}} = 0.45$ and $\gamma = 0.7$ *(explicitly documented in Özcan et al. fn. 3, p. 5 as heuristically calibrated for sublinear inference power scaling)*. Specifically:
- **Prefill Nodes:** Compute-intensive ($\text{mfu} \to \text{mfu}_{\text{sat}}$), un-capped ($c_{\text{cap}} = 1.0$: `400 W` A100, `700 W` H100 SXM5).
- **Decode Nodes:** Memory-bandwidth bound with low arithmetic intensity; Splitwise §III-F shows decode GPUs tolerate a **50% power cap** (`700 W -> 350 W`, $c_{\text{cap}} = 0.5$ to $0.7$) without violating TBT SLOs, or can run on lower-TDP hardware (`L4 72 W`, `A100 PCIe 250 W`, `A40 300 W`).
- **Node Ancillary Power:** Non-GPU server components (host CPU, DRAM, SSD, 100G NIC, chassis PSU/fan) follow GreenSKU component specifications (`CPU 290 W` Genoa, `DRAM 23.68 W` per 64 GB DDR5, `SSD 11.2 W` 2 TB, `NIC 19.0 W` 100G, `chassis 35 + 112.5 W`), allocated proportionally across the GPUs hosted per chassis (`4-GPU` or `8-GPU` server baseline).

---

### 4.3 KV-Cache Footprint, Migration Energy, & Hybrid Crossover Rule

From **EcoServe-Cost (2025)** and **DistServe (2024)**:
$$S_{\text{kv}}(L_{\text{in}}) = 2 \cdot n_{\text{layers}} \cdot n_{\text{kv\_heads}} \cdot d_{\text{head}} \cdot b_{\text{dtype}} \cdot L_{\text{in}}$$
Default workload profiles benchmark both dense MHA KV footprints (`Llama-30B`: `1.52 MB/token`; `OPT-66B`: `1.13 GB / 512 tokens`) and Grouped-Query Attention (`GQA`, e.g., `Llama-2-70B` `80 layers`, `~0.31 MB/token` at FP16 `GQA-8` vs `CodeLlama-34B` `4.76 GB/s` vs `38.96 GB/s` MHA in EcoServe-Cost Table 3).

Transfer latency and network energy from prefill node $i$ (region $r_P$) to decode node $j$ (region $r_D$):
$$T_{\text{kv}}(S_{\text{kv}}, i, j) = \begin{cases}
\delta_{\text{layer}} + \dfrac{S_{\text{kv}}}{\text{BW}_{\text{local}}}, & r_P = r_D \quad (\text{intra-DC NVLink/IB; }\delta_{\text{layer}} \in \{5, 8\}\text{ ms}) \\[6pt]
\text{RTT}_{\text{wan}}(r_P, r_D) + \dfrac{S_{\text{kv}}}{\text{BW}_{\text{wan}}}, & r_P \neq r_D \quad (\text{cross-region WAN})
\end{cases}$$
$$E_{\text{kv}}(S_{\text{kv}}, i, j) = P_{\text{nic+net}} \cdot \dfrac{S_{\text{kv}}}{\text{BW}(i, j)}$$

**Carbon-Extended Crossover Criterion (extending Sisodia 2026 Eq. 1, p. 4):**  
Pipelined KV transfer from $i \to j$ is strictly admissible over recomputation on $j$ or local decode on $i$ only if **both** the latency condition holds:
$$T_{\text{kv}}(S_{\text{kv}}, i, j) + T_{\text{queue},D}(j) < \min\left(T_{\text{queue},D}(i),\ T_{\text{recompute}}(S_{\text{kv}}, j)\right)$$
**and** the end-to-end marginal carbon cost satisfies:
$$\text{PUE}_{r_P} \cdot E_{\text{prefill}} \cdot \text{CI}_{r_P}(t) + \overline{\text{PUE}} \cdot E_{\text{kv}} \cdot \overline{\text{CI}}_{\text{path}} + \text{PUE}_{r_D} \cdot E_{\text{decode}} \cdot \text{CI}_{r_D}(t) < C_{\text{local}}(i)$$
When this inequality fails—for example under long prompts ($S_{\text{kv}}$ large), tight `BW_wan` (`10 Gbps`), or small regional $\Delta\text{CI}$—`P4` dynamically reverts to intra-region P/D or full low-carbon remote execution.

---

### 4.4 Serverless Cold-Start Reload vs. Keep-Alive Carbon Model

Extending **LACE-RL (Sun et al., 2026, Eq. 2–4, pp. 2–3)** and **ServerlessLLM (Fu et al., 2024, §2.3 & Fig. 6a)**, an idle GPU container held for keep-alive timeout $k \in \{0, 1, 5, 10, 30, 60\}\text{ s}$ consumes:
- **Warm Idle Carbon** over idle gap $\tau_{\text{idle}} = \min(\Delta t_{\text{arr}}, k)$:
  $$C_{\text{idle}}(\tau_{\text{idle}}, t) = \left(\lambda_{\text{idle}} \cdot P_{\text{TDP}} + P_{\text{host,idle}}\right) \cdot \tau_{\text{idle}} \cdot \text{PUE}_r \cdot \text{CI}_r(t)$$
  *(with baseline $\lambda_{\text{idle}} = 0.2$ from LACE-RL Eq. 3, and hardware-exact idle draw `60 W / 700 W = 0.086` H100 or `100 W / 400 W = 0.25` A100 tested directly).*
- **Cold-Start Reload Carbon** whenever $\Delta t_{\text{arr}} > k$:
  $$C_{\text{cold}}(t) = \left(f_{\text{cold}} \cdot P_{\text{TDP}} + P_{\text{host}}\right) \cdot T_{\text{cold}} \cdot \text{PUE}_r \cdot \text{CI}_r(t)$$
  where $T_{\text{cold}} \in \{10.3\text{ s (ServerlessLLM)},\ 48.0\text{ s (Safetensors)},\ 84.0\text{ s (PyTorch)}\}$ for 70B (`130 GB`) and $\{2.0,\ 8.2,\ 14.0\}\text{ s}$ for 13B from local NVMe RAID-0 (`12 GB/s`), plus optional `+ 15 s` Knative termination delay (CASA) or `26 s+` remote S3 download (`5 GB/s`).

**`S3` Dynamic Keep-Alive Policy Rule:**  
At instance idle transition in region $r$, given online arrival-rate estimate $\hat{\lambda}$ and current normalized grid carbon intensity $\widetilde{\text{CI}}_r(t) \in [0, 1]$, select $k^* \in \{1, 5, 10, 30, 60\}\text{ s}$ minimizing the carbon-and-SLO-weighted hazard cost:
$$k^*(t) = \arg\min_{k \in \mathcal{K}} \left[\mathbb{E}[\tau_{\text{idle}}(k)] \cdot C_{\text{idle\_rate}}(t) + e^{-\hat{\lambda} k} \cdot \left(C_{\text{cold}}(t) + \beta_{\text{SLO}} \cdot \widetilde{\text{CI}}_r(t)^{-1} \cdot \mathbb{I}(T_{\text{cold}} > \text{TTFT}_{\text{SLO}})\right)\right]$$

---

### 4.5 Operational & Amortized Embodied Carbon Accounting (SCI-Aligned)

Following **LLMCarbon (2024)**, **EcoServe (2025)**, **Bai et al. (2026)**, and the **Software Carbon Intensity (SCI)** standard:

1. **Operational Carbon (`gCO2eq`):**
   $$C_{\text{op}} = \sum_{r \in \mathcal{R}} \sum_{m \in \mathcal{N}_r} \int_{0}^{T_{\text{sim}}} \frac{P_{\text{total},m}(t)}{1000} \cdot \text{PUE}_r \cdot \text{CI}_r(t)\, dt$$
   where $\text{CI}_r(t)$ is in $\text{gCO}_2\text{eq/kWh}$ *(all Japan FY2024 TSO CSV values multiplied by `1000.0` upon ingestion to convert `kgCO2/kWh` $\to$ `gCO2eq/kWh`)*.

2. **Amortized Embodied Carbon (`gCO2eq`):**
   For server $m$ comprising host components (`CPU`, `DRAM`, `SSD`, `NIC`, `chassis`) and GPU count $G_m$:
   $$C_{\text{emb}}(m) = \left(\frac{C_{\text{emb,host}}(m)}{\text{LT}_{\text{host}}} + \sum_{g=1}^{G_m} \frac{C_{\text{emb,gpu}}(g)}{\text{LT}_{\text{gpu}}}\right) \cdot T_{\text{sim}}$$
   *(converted from `kgCO2e` to `gCO2eq` via $\times 1000$, where $T_{\text{sim}}$ and lifetimes $\text{LT}$ are in hours; baseline uniform lifetime `4.0 yr = 35,040 h`, asymmetric lifetime `LT_host = 9.0 yr = 78,840 h`, `LT_gpu = 3.0 yr = 26,280 h`).*

3. **Composite Lifecycle Intensity Metrics:**
   $$\text{SCI}_{\text{op}} = \frac{C_{\text{op}}}{N_{\text{tok}} / 1000},\qquad \text{SCI}_{\text{emb}} = \frac{C_{\text{emb}}}{N_{\text{tok}} / 1000},\qquad \text{SCI}_{\text{tot}} = \frac{C_{\text{op}} + C_{\text{emb}}}{N_{\text{tok}} / 1000}\quad [\text{gCO}_2\text{eq / 1k tokens}]$$

---

## 5. Complete Verified Parameter & Trace Table

### 5.1 Empirically Verified System, Hardware, & Carbon Parameters

*(All rows audited directly against [`parameter_sources.json`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/parameter_sources.json).)*

| Category | Parameter | Value(s) | Unit | Source Citation & Exact Reference |
|---|---|---|---|---|
| **GPU Hardware** | `A100 SXM4 80GB` TDP / Idle | `400` / `100` | `W` | Splitwise Table I p. 1; Özcan §3.1 p. 3 (`arXiv:2507.11417v1`) |
| **GPU Hardware** | `A100 SXM4 80GB` HBM BW / NVLink / IB | `2039 GB/s` / `50 Gbps` / `200 Gbps` | BW | Splitwise Table I p. 1 (`arXiv:2311.18677v2`) |
| **GPU Hardware** | `H100 SXM5 80GB` TDP / Idle | `700` / `60` | `W` | Splitwise Table I p. 1; Özcan §3.1 p. 3 (`arXiv:2507.11417v1`) |
| **GPU Hardware** | `H100 SXM5 80GB` HBM BW / NVLink / IB | `3352 GB/s` / `100 Gbps` / `400 Gbps` | BW | Splitwise Table I p. 1 & §V-A p. 8 |
| **GPU Decode Tier** | `A40 PCIe` Idle / Peak; `L4` TDP; `T4` TDP | `30 / 300`; `72`; `70` | `W` | Özcan §3.1 p. 3 (`A40`); EcoServe Fig. 4 p. 3 (`L4, T4`) |
| **Power Scaling** | MFU saturation $\text{mfu}_{\text{sat}}$; sublinear $\gamma$ | `0.45`; `0.7` | dimensionless | Özcan §3.1 Eq. (1) p. 3 & §4.1 fn. 3 p. 5 |
| **Phase Power Cap** | Decode power cap tolerance; `HHcap` multiplier | `0.50` (`700->350 W`); `0.70` | fraction | Splitwise §III-F p. 5 & §IV-D Table V p. 8 |
| **Phase Cost/Perf** | Llama-70B Coding P50 `TTFT` / `TBT` (A100 vs H100) | `185 / 52` vs `95 / 31` | `ms` | Splitwise Table IV p. 5 (uncontended baseline) |
| **Phase Cost/Perf** | Llama-70B Conv P50 `TTFT` / `TBT` (A100 vs H100) | `155 / 40` vs `84 / 28` | `ms` | Splitwise Table IV p. 5 (uncontended baseline) |
| **KV Cache Size** | Llama-30B MHA; OPT-66B 512-tok KV | `1.52 MB/tok`; `1.13 GB` | Size | EcoServe-Cost §2.1 p. 3; DistServe §3.3 p. 4 |
| **KV Interconnect** | NVLink / Cross-node BW (DistServe, Sarathi, Mooncake) | `600 GB/s` / `25, 100, 800 Gbps` | BW | DistServe §3.3/6.1; Sarathi; Mooncake §8.1 p. 15 |
| **KV Overhead** | Per-layer non-overlapped KV stall; Live migration | `8 ms (A100) / 5 ms (H100)`; `20–30 ms` | `ms` | Splitwise §VI-A p. 9 (`<7% TTFT`); Llumnix §6.2 p. 10 |
| **SLOs (Buckets)** | DynamoLLM Short / Medium / Long `TTFT` / `TBT` | `250/100`, `400/100`, `2000/100` | `ms` | DynamoLLM Table IV p. 3 (`arXiv:2408.00741`) |
| **SLOs (Apps)** | DistServe Chatbot `13B/66B/175B`; Code `66B`; Sum `66B` | `0.25/0.10`, `2.5/0.15`, `4.0/0.20`, `0.125/0.20`, `15.0/0.15` | `s` (`TTFT/TPOT`) | DistServe Table 1 p. 9 (`arXiv:2401.09670`) |
| **Cold Start** | Llama-2-70B (`130 GB`) load (PyTorch / Safetensors / ServerlessLLM) | `84.0 / 48.0 / 10.3` | `s` | ServerlessLLM §2.3 p. 3 & Fig. 6a / §7.2 p. 10 |
| **Cold Start** | OPT-13B load (PyTorch / Safetensors / ServerlessLLM); Knative stop | `14.0 / 8.2 / 2.0`; `15.0` | `s` | ServerlessLLM Fig. 6a p. 10; CASA §VI-A p. 5 |
| **Keep-Alive** | Idle power multiplier $\lambda_{\text{idle}}$; timeout grid $\mathcal{K}$ | `0.2`; `{1, 5, 10, 30, 60}` | ratio / `s` | LACE-RL §II-B Eq. (2)-(4) p. 2-3 & §IV-A.4 p. 7 |
| **Embodied GPU** | `A100 SXM 80G` / `H100 PCIe` / `L4` / `T4` / `A100 PCIe 40G` | `121.5 / 124.9 / 41.2 / 37.7 / 93.6` | `kgCO2e` | EcoServe Fig. 4 p. 3 (`arXiv:2502.05043v2`) |
| **Embodied Server** | `A100x1..4` full server; EcoServe baseline Host / GPU | `314.9..1259.4`; `800.0 / 120.0` | `kgCO2e` | EcoServe Fig. 5 p. 4 & Fig. 21 p. 9 |
| **Host Parts** | `PUE` default (sweep); CPU Genoa; DDR5 64G; SSD 2T; 100G NIC; 2U | `1.12` (`1.10, 1.12, 1.20`); `30.7`; `105.4`; `34.65`; `58.09`; `375.0` | ratio / `kgCO2e` | Azure GreenSKU (`DOI:10.5281/zenodo.10896254`); LLMCarbon; Özcan |
| **Lifetimes** | Uniform hardware lifetime default (sweep); Asymmetric Host / GPU | `4.0` (`3, 4, 5, 6`); `9.0 / 3.0` | `years` | EcoServe Fig. 6 p. 4 & Fig. 21 p. 9; Chasing Carbon p. 5; GreenSKU (`72 mo`) |

### 5.2 Real Public Traces (`CC-BY-4.0`)

| Trace Component | Exact Local File(s) | Granularity & Empirical Summary |
|---|---|---|
| **Conversational LLM Trace** | [`AzureLLMInferenceTrace_conv.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceTrace_conv.csv) | `19,366` requests over `58.36 min` (`5.53 rps`, `ia_cv = 1.094`); `ContextTokens` mean `1154.7` (P50 `1020`, P95 `4083`, max `14050`); `GeneratedTokens` mean `211.1` (P50 `129`, P95 `451`, max `1000`). |
| **Code-Completion Trace** | [`AzureLLMInferenceTrace_code.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceTrace_code.csv) | `8,819` requests over `57.27 min` (`2.57 rps`, bursty `ia_cv = 13.152`); `ContextTokens` mean `2047.8` (P50 `1469`, P95 `7303.3`, max `7437`); `GeneratedTokens` mean `27.9` (P50 `13`, P95 `90`, max `1899`). |
| **UK Multi-Region Grid** | [`uk_regional_carbon_intensity_oct2025.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/uk_regional_carbon_intensity_oct2025.csv) & [`uk_national_carbon_intensity_oct2025.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/uk_national_carbon_intensity_oct2025.csv) | `1,344` 30-min slots (`2025-10-01`–`2025-10-28`) across `18` DNO zones: `South Scotland` mean `9.75` (`0–129`), `North East England` `28.83` (`3–108`), `North Scotland` `35.65` std `82.50` (`0–355`), `North West England` `78.38`, `London` `163.32`, `South Wales` `240.50 gCO2eq/kWh`. |
| **Japan Multi-Region Grid** | `./experiments/data/japan_tso_2024/*.csv` | `17,520` 30-min rows FY2024 (`x1000` normalized to `gCO2eq/kWh`): `Kansai` mean `356.20`, `Kyushu` `384.41`, `Hokkaido` `529.07`, `Chubu` `537.20`, `TEPCO` `581.64 gCO2eq/kWh` (`~60x` cross-continental mean span vs `South Scotland`). |

### 5.3 Explicit Simulation Calibration Assumptions (Non-Measured Parameters)

| Assumption | Default Value | Sensitivity Range | Justification & Explicit Caveat |
|---|---|---|---|
| **Cross-Region WAN RTT** | Intra-DC `0.5 ms`; Intra-UK `20.0 ms`; Intra-JP `30.0 ms`; Cross-Cont UK-JP `200.0 ms` | Swept per regional topology pair | Design-calibrated synthetic WAN round-trip delays reflecting geographic distance; not telemetry from a multi-continent production cluster. |
| **Cross-Region WAN KV Bandwidth** | `10.0 Gbps` | `{10.0, 25.0, 100.0} Gbps` | Reflects commodity inter-server Ethernet (`10 Gbps`, ServerlessLLM §7.1 p. 9) up to `25–100 Gbps` inter-node WAN/DC links (DistServe §6.1 p. 9; Sarathi §5 p. 10). |
| **Cold-Start GPU Power Fraction** | `0.65 * P_TDP` | `[0.45, 0.65, 0.85] * P_TDP` | Calibrated intermediate draw during weight deserialization, PCIe DMA, and CUDA context warm-up (`P_cold` is duration-dominated per LACE-RL Eq. 4). |
| **Sublinear MFU Exponent $\gamma$** | `0.7` | `[0.5, 0.7, 1.0]` | Adopted directly from Özcan et al. (2025) Eq. (1) & fn. 3, who explicitly state $\gamma = 0.7$ is heuristic; linear (`1.0`) and sublinear (`0.5`) bounds included in sensitivity checks. |
| **24-Hour Trace Extension** | Resampled empirical Azure `(L_in, L_out, dt)` blocks tiled across 24 h | Raw `1-hr` micro-trace vs `24-hr` diurnal modulated profile | Raw 2023 Azure files span `~58 min` each; full-day grid cycles align 30-min UK/JP carbon traces via empirical bootstrap preserving exact token & CV statistics. |

---

## 6. Evaluation Metrics

1. **Carbon Intensity Metrics (`SCI`-Aligned):**
   - Operational Carbon Intensity: $\text{SCI}_{\text{op}}$ (`gCO2eq / 1k generated+prompt tokens`, also reported per generated token)
   - Amortized Embodied Carbon Intensity: $\text{SCI}_{\text{emb}}$ (`gCO2eq / 1k tokens`)
   - Total Lifecycle Carbon Intensity: $\text{SCI}_{\text{tot}} = \text{SCI}_{\text{op}} + \text{SCI}_{\text{emb}}$ (`gCO2eq / 1k tokens`), plus embodied share `%`
2. **Energy Efficiency:** Energy per token (`J/token`), separated into prefill, decode, KV transfer, idle keep-alive, and cold-start reload fractions.
3. **Tail & Mean Latency:** Mean, P95, and P99 `TTFT` (`ms`) and `TPOT` (`ms`).
4. **SLO Attainment & Goodput:** Overall and tail `SLO Violation Rate (%)` against both workload-bucket thresholds (`DynamoLLM` Short/Medium/Long) and application-specific P90 targets (`DistServe` Chatbot & Code Completion).
5. **Serverless & Resource Efficiency:** Cold-start frequency (`%` of requests), mean GPU utilization (`%` active time), KV-cache WAN volume (`GB / 1k requests`), and remote recomputation trigger fraction (`%`).

---

## 7. Experimental Protocol, Seeds, & Sensitivity Plan

### 7.1 Random Seeds & Statistical Rigor
- Every simulation configuration executes across **$S = 10$ fixed, reproducible random seeds**:  
  $$\text{seeds} = \{100,\ 101,\ 102,\ 103,\ 104,\ 105,\ 106,\ 107,\ 108,\ 109\}$$
  controlling stochastic trace resampling/jitter, initial cluster phase alignment, and request-pool ordering.
- All comparative metrics are reported as **sample mean $\pm$ 95% confidence interval** using Student's $t$-distribution ($t_{0.975, 9} = 2.262$):
  $$\bar{x} \pm 2.262 \cdot \frac{s}{\sqrt{10}}$$
- Pairwise significance between baseline policies (`B1`, `B2`, `P3`, `S1`, `S2`) and proposed controllers (`P4`, `S3`) is tested across matched seeds using the two-sided **Wilcoxon signed-rank test** ($\alpha = 0.05$).

### 7.2 Main Experiments & Systematic Sensitivity Sweeps

1. **Main Experiment E1 (Cluster/Multi-Region P/D Carbon Scheduling — `1-hr` High-Fidelity & `24-hr` Diurnal):**  
   Compares `B1`, `B2`, `P3`, `P4`, `P5` across `AzureLLMInferenceTrace_conv` and `AzureLLMInferenceTrace_code` on a 3-region default federation (`South Scotland` clean wind, `London` moderate grid, `TEPCO` high-carbon grid).
2. **Main Experiment E2 (Serverless GPU Keep-Alive Optimization — Bursty Code Trace):**  
   Compares `S1 (k=0)`, `S2 (k=30 s)`, `S2b (k=60 s)`, and `S3 (Dynamic Carbon-Aware)` under `AzureLLMInferenceTrace_code` across low (`South Scotland`), volatile (`North Scotland`), and high-carbon (`TEPCO`) regimes.
3. **Sensitivity Sweep SW1 — Arrival Rate / Cluster Utilization:**  
   Scales request arrival intensity across `{0.5x, 1.0x, 1.5x, 2.0x, 3.0x}` baseline Azure RPS to map idle-vs-saturation operational carbon and queueing SLO breaks (~15% to ~90% GPU utilization).
4. **Sensitivity Sweep SW2 — Grid Carbon Differential & Forecast Volatility:**  
   Tests three spatial topologies: (i) *Low-diff Intra-UK* (`South Scotland` vs `North West England`), (ii) *Volatile Wind* (`North Scotland std 82.50` vs `South Wales 240.50`), and (iii) *Cross-Continental ~60x* (`South Scotland` vs `TEPCO`), plus `UK NESO forecast` vs `actual` noise.
5. **Sensitivity Sweep SW3 — SLO Tightness, Decode Hardware Tier, & WAN Bandwidth:**  
   Varies `TTFT/TPOT` targets (Strict `Code 125 ms TTFT`, Moderate `Chatbot`, Relaxed `Long/Summarization`), decode node hardware (`H100cap 350 W` vs `A100 400 W` vs `L4 72 W`), and cross-region KV WAN bandwidth `{10, 25, 100} Gbps`.
6. **Sensitivity Sweep SW4 — Serverless Cold-Start Reload Speed & Embodied Lifetime:**  
   Evaluates `ServerlessLLM` (`10.3 s` 70B / `2.0 s` 13B) vs `Safetensors` (`48.0 s` / `8.2 s`) vs `PyTorch` (`84.0 s` / `14.0 s`), cold-start power fraction `{0.45, 0.65, 0.85}`, uniform lifetime `LT in {3, 4, 5, 6} yr`, and `EcoServe` asymmetric lifetime (`9-yr host / 3-yr GPU`).
