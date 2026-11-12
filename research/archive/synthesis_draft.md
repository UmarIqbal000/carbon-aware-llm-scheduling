# Literature Synthesis, Hierarchical Taxonomy, and Open Research Challenges

**Manuscript:** *Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Review and Simulation*  
**Author:** Umar Iqbal (`umar.iqbal.cs28@directiilm.edu`), IILM University, Greater Noida, India  
**Corpus Scope:** `47` verified sources (`42 full_text`, `5 abstract_only`) across five pillars (`a_surveys` through `e_foundations`), anchored programmatically to [`sources.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/research/sources.csv) and [`comparison_matrix.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/research/comparison_matrix.csv).

---

## 1. Corpus Overview & Programmatic Bibliometric Trends

All quantitative distributions below are computed directly from the locked 47-source matrix (`comparison_matrix.csv` + `sources.csv`). Two structural trends stand out immediately: (1) intense recent acceleration, with **42 of 47 sources (89.4%)** published between 2022 and 2026 and **23 of 47 (48.9%)** in 2025–2026 alone; and (2) an almost complete disconnection between carbon-aware cloud/serverless scheduling research (`b_carbon_schedulers`) and autoregressive phase-disaggregated LLM serving (`c_llm_serving`).

### Table 1: Publication Timeline by Research Pillar (`N = 47`)

| Year | `a_surveys` | `b_carbon_schedulers` | `c_llm_serving` | `d_modeling_traces_standards` | `e_foundations` | Total (`n`) | Share (`%`) |
|---|---|---|---|---|---|---|---|
| **2011** | 0 | 0 | 0 | 0 | 2 | **2** | 4.3% |
| **2020** | 0 | 0 | 0 | 1 | 0 | **1** | 2.1% |
| **2021** | 0 | 1 | 0 | 1 | 0 | **2** | 4.3% |
| **2022** | 0 | 0 | 0 | 1 | 0 | **1** | 2.1% |
| **2023** | 0 | 3 | 2 | 1 | 0 | **6** | 12.8% |
| **2024** | 0 | 4 | 5 | 3 | 0 | **12** | 25.5% |
| **2025** | 4 | 0 | 6 | 2 | 0 | **12** | 25.5% |
| **2026** | 5 | 3 | 3 | 0 | 0 | **11** | 23.4% |
| **Total** | **9 (19.1%)** | **11 (23.4%)** | **16 (34.0%)** | **9 (19.1%)** | **2 (4.3%)** | **47** | **100.0%** |

### Table 2: Document Types, Access Verification, and Empirical Evaluation Modalities

| Dimension | Category | Count | Share | Retained Source IDs / Notes |
|---|---|---|---|---|
| **Document Type** (`N=47`) | `empirical` | 35 | 74.5% | `11` Pillar B + `16` Pillar C + `7` Pillar D + `1` Pillar E (`calheiros2011cloudsim`) |
| | `survey` | 9 | 19.1% | `hewage2026carbon`, `yang2025container`, `alam2026computing`, `agarwal2026serverless`, `besozzi2025serverless`, `miao2025serving`, `bai2026efficiency`, `jiang2026kvcache`, `pan2025inference` |
| | `standard` | 2 | 4.3% | `iso2024sci`, `mell2011nist` |
| | `industry` | 1 | 2.1% | `azure2024trace` |
| **Access Level** (`N=47`) | `full_text` | 42 | 89.4% | `40` verified PDFs + `azure2024trace.md` + `iso2024sci.html` |
| | `abstract_only` | 5 | 10.6% | `roy2026lowcarb`, `calavaro2026offloading`, `gupta2022act`, `sinha2025utilization`, `calheiros2011cloudsim` (strictly metadata/abstract bounded) |
| **Empirical Validation Mode** (`n=35` empirical) | Hardware Prototype / Live Cluster / Profiling | 14 | 40.0% | `chadha2023greencourier`, `gsteiger2024caribou`, `kwon2023vllm`, `li2023clover`, `agrawal2024sarathi`, `fu2024serverlessllm`, `wilkins2024offline`, `qin2025mooncake`, `kakolyris2025throttllem`, `fernandez2025acl`, `basit2026dualscale`, `li2026revisiting`, `wang2026festina`, `shahrad2020serverless` |
| | Hybrid (Hardware Testbed/Profiling + Simulator) | 10 | 28.6% | `hanafy2023carbonscaler`, `souza2023ecovisor`, `qi2024casa`, `jiang2024ecolife`, `sun2026lacere`, `patel2024splitwise`, `zhong2024distserve`, `stojkovic2025dynamollm`, `stojkovic2025tapas`, `li2025ecoserve` |
| | Simulator / Analytical Model Only | 8 | 22.9% | `wiesner2021letswait`, `sukprasert2024limitations`, `calavaro2026offloading`, `gupta2022act`, `acun2023carbonexplorer`, `faiz2024llmcarbon`, `hewage2025aging`, `calheiros2011cloudsim` |
| | Characterization / Unverified Eval Mode | 3 | 8.6% | `gupta2021chasing` (corporate GHG LCA), `sinha2025utilization` (`abstract_only`), `roy2026lowcarb` (`abstract_only`) |

Notice that **18 of 35 empirical works (51.4%)** incorporate discrete-event simulation or analytical carbon modeling (`10` hybrid testbed+simulator + `8` model/simulation-only), directly validating our methodological choice of a calibrated `SimPy 4.1.2` simulator anchored to physical hardware parameters and `CC-BY-4.0` production traces ([`DESIGN.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/DESIGN.md), Sec. 1). Similarly, across the `38` non-survey works:
- **Physical GPU Hardware Evaluation:** **20 of 38 (52.6%)** evaluate or analytically model GPUs (all `16` Pillar C systems plus `souza2023ecovisor`, `gupta2021chasing`, `faiz2024llmcarbon`, `sinha2025utilization`), whereas **10 of 11** Pillar B carbon schedulers target CPU/VM/Knative/Lambda tasks (except the abstract-only `roy2026lowcarb`, whose hardware is unverified, and `calavaro2026offloading` across generic edge-cloud nodes).
- **Production Trace Benchmarks:** Microsoft Azure traces or Azure cluster telemetry appear in **16 of 38 non-survey sources (42.1%)** (`chadha2023greencourier`, `sukprasert2024limitations`, `gsteiger2024caribou`, `qi2024casa`, `jiang2024ecolife`, `agrawal2024sarathi`, `fu2024serverlessllm`, `stojkovic2025dynamollm`, `stojkovic2025tapas`, `kakolyris2025throttllem`, `fernandez2025acl`, `li2025ecoserve`, `basit2026dualscale`, `shahrad2020serverless`, `azure2024trace`, `hewage2025aging`), while `ShareGPT` variants appear in **7 of 38 (18.4%)**.

---

## 2. Hierarchical Comparative Taxonomy (RQ1)

To resolve the terminological fragmentation between systems architecture and sustainability engineering, we organize all 47 corpus works into a four-level hierarchical taxonomy capturing **(L1) Architectural & Scheduling Granularity**, **(L2) Autoregressive Phase & KV-Cache Handling**, **(L3) Spatiotemporal & Power Control Knobs**, and **(L4) Carbon Accounting Boundary**.

```text
Taxonomic Root: Cloud & Serverless AI Resource Management (N = 47)
├── L1.A Meta-Analysis & Taxonomies (n = 9)
│   ├── Cloud / Container / Serverless Sustainability Surveys (n = 5):
│   │   hewage2026carbon (op+embodied), yang2025container, alam2026computing,
│   │   agarwal2026serverless, besozzi2025serverless  [ALL 0 P/D or KV hits]
│   ├── LLM Resource & Energy Survey without P/D Scheduling (n = 1):
│   │   bai2026efficiency (SCI/kWh formulation; 0 prefill/disagg/serverless/embodied)
│   └── LLM Serving & KV Infrastructure Surveys (n = 3):
│       miao2025serving, jiang2026kvcache (J/token), pan2025inference [0 runtime grid CI]
│
├── L1.B Intra-Node & Multi-GPU LLM Serving Engines (n = 10)
│   ├── Phase-Disaggregated P/D Engines (n = 5):
│   │   ├── Perf/SLO Only (n = 2): zhong2024distserve, qin2025mooncake
│   │   └── Local Energy / Power-Cap Aware (n = 3): patel2024splitwise,
│   │       basit2026dualscale, li2026revisiting  [0 grid CI, 0 WAN, 0 embodied]
│   ├── Colocated Phase-Aware Engines (n = 2):
│   │   agrawal2024sarathi (chunked prefill, perf-only), fernandez2025acl (J/tok profiling)
│   └── Phase-Agnostic LLM Engines / Predictors (n = 3):
│       kwon2023vllm (perf-only), wilkins2024offline (OLS energy), kakolyris2025throttllem (DVFS)
│
├── L1.C Serverless / FaaS Keep-Alive & Cold-Start Controllers (n = 7)
│   ├── CPU FaaS Perf-Only (n = 1): shahrad2020serverless (Hybrid Histogram + ARIMA)
│   ├── CPU FaaS Grid-Carbon Keep-Alive (n = 4):
│   │   ├── Op CI + Water (n = 1): qi2024casa
│   │   ├── Op CI Only (n = 2): roy2026lowcarb [abs], sun2026lacere
│   │   └── Op CI + Multi-Gen Embodied (n = 1): jiang2024ecolife
│   └── GPU LLM Serverless (n = 2):
│       fu2024serverlessllm (perf-only checkpointing), wang2026festina (MPS+DVFS+EWR+PD-D; 0 grid CI)
│
├── L1.D Single-Datacenter Cluster / Pool Carbon & Energy Managers (n = 8)
│   ├── Generic / Non-LLM Temporal & Renewable Managers (n = 4):
│   │   wiesner2021letswait, hanafy2023carbonscaler, souza2023ecovisor (battery), li2023clover (MIG)
│   └── LLM Cluster Energy / Carbon / Aging Managers (n = 4):
│       stojkovic2025tapas (thermal/power), stojkovic2025dynamollm (op CI colocated),
│       hewage2025aging (CPU NBTI embodied), li2025ecoserve (op CI + 4R embodied, phase-agnostic)
│
├── L1.E Cross-Region / Multi-DC Carbon Routing (n = 4)
│   └── Generic / Serverless DAG / Edge-Cloud CPU Tasks Only (n = 4):
│       chadha2023greencourier, sukprasert2024limitations, gsteiger2024caribou, calavaro2026offloading [abs]
│       [0 LLM P/D, 0 KV WAN crossover, 0 GPU embodied]
│
└── L1.F Carbon Models, Traces, Simulators & Standards (n = 9)
    ├── Standards & Telemetry Datasets (n = 3): mell2011nist, iso2024sci, azure2024trace
    └── Lifecycle Models & Macro Simulators (n = 6):
        calheiros2011cloudsim [abs], gupta2021chasing, gupta2022act [abs],
        acun2023carbonexplorer, faiz2024llmcarbon, sinha2025utilization [abs]
```

### Table 3: Phase-Awareness × Carbon/Energy Signal Intersection Matrix (`38` Non-Survey Works)

Crucially, cross-tabulating `phase_awareness` against `carbon_energy_signal` across all 38 primary/empirical/standard/dataset sources reveals **exact populated cells versus completely empty research intersections (`0`)**:

| Phase Awareness (`n = 38`) | None (Perf / Trace / Spec) | Local Power / Energy Only (`W`/`J`) | Grid Operational CI (`gCO2eq/kWh` / `+Batt` / `+Water`) | Operational CI + Embodied Carbon (`+CPU Aging`) | Row Total |
|---|---|---|---|---|---|
| **Disaggregated P/D** (`split P/D pools`) | **2** (`zhong2024distserve`, `qin2025mooncake`) | **3** (`patel2024splitwise`, `basit2026dualscale`, `li2026revisiting`) | **0 (EMPTY)** | **0 (EMPTY)** | **5** |
| **Colocated + P/D Variant** | **0** | **1** (`wang2026festina`) | **0 (EMPTY)** | **0 (EMPTY)** | **1** |
| **Colocated Phase-Aware** | **1** (`agrawal2024sarathi`) | **2** (`stojkovic2025tapas`, `fernandez2025acl`) | **1** (`stojkovic2025dynamollm`) | **0 (EMPTY)** | **4** |
| **Phase-Agnostic LLM** | **3** (`kwon2023vllm`, `fu2024serverlessllm`, `azure2024trace`) | **2** (`wilkins2024offline`, `kakolyris2025throttllem`) | **0 (EMPTY)** | **4** (`li2025ecoserve`, `faiz2024llmcarbon`, `sinha2025utilization`, `hewage2025aging`) | **9** |
| **Non-LLM / Generic Workload** | **3** (`mell2011nist`, `calheiros2011cloudsim`, `shahrad2020serverless`) | **0** | **11** (`wiesner2021letswait`, `hanafy2023carbonscaler`, `souza2023ecovisor`, `chadha2023greencourier`, `sukprasert2024limitations`, `gsteiger2024caribou`, `qi2024casa`, `roy2026lowcarb`, `calavaro2026offloading`, `sun2026lacere`, `li2023clover`) | **5** (`jiang2024ecolife`, `gupta2021chasing`, `gupta2022act`, `acun2023carbonexplorer`, `iso2024sci`) | **19** |
| **Column Total (`n = 38`)** | **9 (23.7%)** | **8 (21.1%)** | **12 (31.6%)** | **9 (23.7%)** | **38** |

**Key Taxonomic Finding (Empty Cells):**  
1. Every **Disaggregated P/D** or **P/D-Variant** serving engine (`6/6`: `patel2024splitwise`, `zhong2024distserve`, `qin2025mooncake`, `basit2026dualscale`, `li2026revisiting`, `wang2026festina`) optimizes strictly inside **local intra-cluster power/energy or latency boundaries**—scoring **`0`** in Grid Operational CI, **`0`** in Cross-Region Multi-DC routing, and **`0`** in Embodied Carbon Accounting.  
2. Conversely, every **Cross-Region / Multi-DC** carbon router (`4/4`: `chadha2023greencourier`, `sukprasert2024limitations`, `gsteiger2024caribou`, `calavaro2026offloading`) operates exclusively on **Non-LLM / Generic CPU workloads**—scoring **`0`** in LLM phase disaggregation and **`0`** in KV-cache migration vs. recomputation crossover modeling.  
3. Only **2 runtime schedulers** track grid operational CI for LLM inference (`stojkovic2025dynamollm` and `li2025ecoserve`), and **neither** implements P/D disaggregation, cross-region WAN KV routing, or serverless checkpoint keep-alive optimization.

### Table 4: Lifecycle Embodied Carbon & Spatial Scope Coverage (`N = 47`)

| Dimension | Category | Count | Share (`N=47`) | Mapped Source IDs |
|---|---|---|---|---|
| **Embodied Carbon** | `No` (Omitted or explicitly excluded) | 37 | 78.7% | 8 surveys + 10 Pillar B + 15 Pillar C + 2 Pillar D (`shahrad2020serverless`, `azure2024trace`) + 2 Pillar E |
| | `Yes` (Hardware / Server Amortization) | 7 | 14.9% | `jiang2024ecolife`, `li2025ecoserve`, `gupta2021chasing`, `gupta2022act`, `acun2023carbonexplorer`, `faiz2024llmcarbon`, `sinha2025utilization` |
| | `Yes` (CPU Aging Amortization) | 1 | 2.1% | `hewage2025aging` |
| | `Yes` (Standard Definition / Survey Taxonomy) | 2 | 4.3% | `iso2024sci`, `hewage2026carbon` |
| **Spatial / Temporal Scope** | `Literature Scope (No Runtime Control)` | 9 | 19.1% | All `9` Pillar A surveys |
| | `Single-Node / Rack Local` | 13 | 27.7% | `12` Pillar C intra-node/serverless engines + `sinha2025utilization` |
| | `Single-DC Temporal` | 13 | 27.7% | `7` Pillar B single-DC + `3` Pillar C (`stojkovic2025dynamollm`, `stojkovic2025tapas`, `li2025ecoserve`) + `shahrad2020serverless`, `hewage2025aging` |
| | `Accounting / Static Lifecycle` | 6 | 12.8% | `gupta2021chasing`, `gupta2022act`, `faiz2024llmcarbon`, `azure2024trace`, `iso2024sci`, `mell2011nist` |
| | `Spatial Multi-Region` | 3 | 6.4% | `chadha2023greencourier`, `gsteiger2024caribou`, `calavaro2026offloading` |
| | `Spatiotemporal Multi-Region` | 2 | 4.3% | `sukprasert2024limitations`, `acun2023carbonexplorer` |
| | `Federated Multi-Cloud (Simulator)` | 1 | 2.1% | `calheiros2011cloudsim` |

---

## 3. Open Research Challenges Linked to RQ1–RQ4 & Simulation Design

Synthesizing the 47 reviewed sources exposes **seven concrete, unresolved research challenges** directly motivating our research questions (**RQ1–RQ4**) and parameterized `SimPy 4.1.2` evaluation plan in [`DESIGN.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/DESIGN.md).

### OC1. Grid-Carbon-Agnostic Prefill–Decode Phase Disaggregation
- **Literature Evidence:** Phase-disaggregated architectures (`patel2024splitwise`, `zhong2024distserve`, `qin2025mooncake`, `basit2026dualscale`, `li2026revisiting`) demonstrate up to 2.15–2.35x iso-power throughput (`patel2024splitwise`, pp. 10, 12), 2.0–4.6x higher request capacity (`zhong2024distserve`, p. 10), and 39%/48% prefill/decode energy cuts (`basit2026dualscale`, p. 1), while `patel2024splitwise` (Fig. 9, p. 5) proves decode tolerates a 50% power cap (`700 W -> 350 W`) with near-zero TBT latency degradation. Yet Table 3 confirms **zero (0/6)** disaggregated P/D engines respond to dynamic regional grid carbon intensity (`gCO2eq/kWh`), whereas existing grid-aware LLM systems (`stojkovic2025dynamollm`, `li2025ecoserve`) use colocated or phase-agnostic pools.
- **Mapping to RQs & `DESIGN.md`:** Directly addresses **RQ1, RQ2**, and Hypothesis **H1** by implementing **`B2` (`Carbon-Agnostic Disaggregated`)**, **`P3` (`Spatiotemporal Carbon-Aware Disaggregated`)**, and **`P4` (`Carbon+KV-Aware Hybrid Router`)** in Experiment **E1**, isolating prefill onto uncapped high-TDP accelerators in low-CI regions while capping or down-tiering decode pools (`c_cap = 0.50–0.70`).

### OC2. Unmodeled Cross-Region KV-Cache Migration vs. Recomputation Energy-Carbon Crossover
- **Literature Evidence:** Intra-cluster P/D systems assume 600 GB/s NVLink or 25–800 Gbps InfiniBand/RDMA (`patel2024splitwise`, `zhong2024distserve`, `qin2025mooncake`), where layer-wise KV streaming adds only 5–8 ms (`patel2024splitwise`, p. 9). Across slower paths (`PCIe`, host DRAM, disk), `li2026revisiting` (pp. 5–8) proves unconditional disaggregation degrades TTFT at small batches and fails to save energy even under independent DVFS. Across wide-area links, `gsteiger2024caribou` (pp. 8, 11–12) shows `0.001–0.005 kWh/GB` network transmission energy halves geo-shifting gains (66.6% -> 22.9%), `chadha2023greencourier` (p. 6) incurs 8.28 s multi-cluster binding overhead, `sukprasert2024limitations` (pp. 8–9) proves 50 ms RTT caps slash spatial savings from 96% to 31%, and `jiang2026kvcache` / `pan2025inference` leave WAN carbon migration boundaries open.
- **Mapping to RQs & `DESIGN.md`:** Directly addresses **RQ2** and Hypothesis **H2** via `DESIGN.md` Eq. 7–9 (the **carbon-extended Sisodia crossover criterion** inside **`P4`**) and Sensitivity Sweep **SW3** (`BW_wan in {10, 25, 100} Gbps`, `AzureLLMInferenceTrace_conv` vs. `code` prompt P95 tails up to `7,303` tokens).

### OC3. Cold-Start Checkpoint Energy Spikes vs. Idle Keep-Alive Carbon in Serverless GPU LLMs
- **Literature Evidence:** FaaS keep-alive carbon optimizers (`qi2024casa`, `jiang2024ecolife`, `roy2026lowcarb`, `sun2026lacere`) operate exclusively on CPU/DRAM serverless functions (`shahrad2020serverless`, `agarwal2026serverless`, `besozzi2025serverless`), where cold starts take sub-second to 15 s and CPU idle power sits near 20–48% of modest TDP. Conversely, serverless GPU LLM systems (`fu2024serverlessllm`, `wang2026festina`) slash 130 GB checkpoint reload from `84.0 s` (`PyTorch`) / `48.0 s` (`Safetensors`) to `10.3 s` (`ServerlessLLM`) or curb idle waste via Elastic Worker Retention (`EWR`), yet ignore grid carbon intensity (`gCO2eq/kWh`). Under bursty Azure code arrivals (`CV = 13.152`, `azure2024trace`), the carbon break-even between holding `60–100 W` GPU idle draw vs. paying `0.65 * P_TDP` multi-second reload spikes remains unquantified.
- **Mapping to RQs & `DESIGN.md`:** Directly anchors **RQ3** and Hypothesis **H3** in Experiment **E2** (`S1: Scale-to-Zero Cold k=0`, `S2: Static Keep-Alive k=30/60 s`, `S3: Dynamic Carbon-Aware Keep-Alive` over `K in {1, 5, 10, 30, 60} s`) and Sensitivity Sweep **SW4** (`T_cold in {10.3, 48.0, 84.0} s` for 70B and `{2.0, 8.2, 14.0} s` for 13B across clean wind vs. high-carbon grids).

### OC4. Clean-Grid Embodied Hardware Dominance & Replicating Over-Provisioning Paradox
- **Literature Evidence:** Industry LCA studies (`gupta2021chasing`, `gupta2022act`, `acun2023carbonexplorer`) and `iso2024sci` establish that as electricity grids decarbonize (>80% renewables), hardware manufacturing dominates lifecycle carbon (`Meta/Google Scope 3 = 21–23x Scope 2`). For LLMs, `faiz2024llmcarbon` (p. 8) puts embodied footprint at 24–35%, `sinha2025utilization` notes `350,000 A100s` emit `7.54M kgCO2` and warns naive GPU utilization packing can backfire, `hewage2025aging` shows CPU NBTI lifetime management cuts embodied emissions 37.67%, and `li2025ecoserve` models server (`800 kgCO2e`, 9-yr) and GPU (`120 kgCO2e`, 3-yr) amortization via 4R policies (-47% total carbon). Yet **78.7% (`37/47`)** of the corpus—and **100% (`6/6`)** of disaggregated P/D routers—omit embodied emissions (`Table 4`). Naive green-region replication (`hanafy2023carbonscaler`-style elastic out-scaling or idle warm pools in clean grids like South Scotland at `9.75 gCO2eq/kWh`) risks increasing total SCI (`((E * I) + M) / R`) once amortized GPU manufacturing (`~121.5–124.9 kgCO2e` GPU + chassis share) dwarfs near-zero grid electricity emissions.
- **Mapping to RQs & `DESIGN.md`:** Directly addresses **RQ4** and Hypothesis **H4** via `DESIGN.md` Sec. 4.5 (`SCI_op`, `SCI_emb`, `SCI_tot`), **`P4`** embodied-aware tie-breaking, and Sweep **SW4** testing uniform `{3, 4, 5, 6} yr` vs. asymmetric `9-yr host / 3-yr GPU` lifespans across `South Scotland` (`9.75`) vs. `TEPCO` (`581.64 gCO2eq/kWh`).

### OC5. Grid Forecast Uncertainty, Average-vs-Marginal Distortion, and Decarbonizing Differentials
- **Literature Evidence:** Real-world grid signals exhibit forecast noise and shrinking geographical gaps: `sukprasert2024limitations` (pp. 8–13) warns 50% forecast errors erase 10–12% of spatial savings (14% MAPE limits penalty to ~3%) while progressive grid greening erodes static differentials, `wiesner2021letswait` (p. 8) incorporates 5% forecast noise, `hanafy2023carbonscaler` (p. 20) tests 30% forecast error, and `gsteiger2024caribou` (Sec. 10, p. 14) flags average-vs-marginal CI distortion as an unresolved gap. Furthermore, `hewage2026carbon` and `yang2025container` show non-stationary renewable volatility (e.g., wind-heavy regions like North Scotland `std = 82.50 gCO2eq/kWh`) can reverse routing rankings within minutes.
- **Mapping to RQs & `DESIGN.md`:** Directly motivates **`P5: Oracle Future-Carbon Disaggregated`** vs. **`P4`** lagged/forecast telemetry and Sensitivity Sweep **SW2** testing low-differential intra-UK (`South Scotland` vs. `North West England`), volatile wind (`North Scotland` vs. `South Wales`), ~60x cross-continental (`South Scotland` vs. `TEPCO`), and `UK NESO forecast` vs. `actual` noise.

### OC6. Hardware DVFS / Re-Sharding Time Constants vs. Sub-Second Autoregressive Execution
- **Literature Evidence:** NVML GPU clock scaling incurs `8–80 ms` latency (`kakolyris2025throttllem` p. 8; `stojkovic2025dynamollm` Sec. 4), forcing `kakolyris2025throttllem` to defer prefill DVFS (`175 ms < 200 ms` switching overhead) and `stojkovic2025dynamollm` to run coarse 5s instance loops above 20–30 ms decode steps, while `basit2026dualscale` applies 4 ms MPC search only on prefill nodes. Meanwhile, `wilkins2024offline` (Table 2, p. 5) proves `(input * output)` cross-terms significantly alter inference energy (`p < 1e-11`), `fernandez2025acl` (p. 6) reveals `TP4` raises total energy +55.23% despite cutting latency 61.34%, and `stojkovic2025tapas` shows rack power emergencies force abrupt quality drops without KV-aware throttling. Bridging fast `ms`-level decode/prefill phase power models with `30-min` grid telemetry remains largely unexplored across heterogeneous hardware (`H100`, `A100`, `L4`).
- **Mapping to RQs & `DESIGN.md`:** Directly guides `DESIGN.md` Sec. 4.1–4.2 (separate compute-bound prefill vs. memory-bound decode service times, `mfu_sat = 0.45`, sublinear `gamma = 0.7` sensitivity `[0.5, 0.7, 1.0]`, decode `c_cap = 0.50–0.70`) and Sweep **SW3** evaluating heterogeneous decode GPU tiers (`H100cap 350 W`, `A100 400 W`, `L4 72 W`).

### OC7. Methodological Fragmentation, Synthetic Calibration Opacity, and Reproducibility Gaps
- **Literature Evidence:** Systematic reviews expose severe experimental inconsistencies across domains: `alam2026computing` proves **70% (`44/63`)** of AI cloud allocation studies rely solely on custom/CloudSim simulations (`calheiros2011cloudsim`) lacking standardized traces or sustainability metrics; `bai2026efficiency` and `jiang2026kvcache` highlight inconsistent adoption of energy-per-token (`J/token`) alongside `TTFT`/`TPOT`; `iso2024sci` mandates rate-normalized `((E * I) + M) / R` accounting without offsets; and foundational specs (`mell2011nist`) precede GPU FaaS energy metering. Even in our 47-source corpus, `10.6%` (`5/47`) remain paywalled (`abstract_only`) and production traces like `azure2024trace` span only ~58 minutes without co-located grid intensity logs.
- **Mapping to RQs & `DESIGN.md`:** Directly dictates our transparent simulation discipline in `DESIGN.md` Sec. 1, 5.3, and 7: explicitly isolating calibrated heuristics (`WAN RTT`, `BW_wan`, `f_cold`, `gamma`) from measured hardware parameters (`parameter_sources.json`), driving runs from open `CC-BY-4.0` Azure + UK NESO + Japan TSO traces (`DATA_MANIFEST.md`), executing `10` deterministic seeds (`100..109`), reporting Student-$t$ 95% confidence intervals ($t_{0.975,9}=2.262$), and running paired Wilcoxon signed-rank significance tests ($\alpha = 0.05$).

---

## 4. Synthesis Bridge to `DESIGN.md` Simulation Architecture

| Open Challenge | Linked RQs | `DESIGN.md` Hypothesis | Simulator Policies / Levers Evaluated | Primary Verification Sweep |
|---|---|---|---|---|
| **OC1** (Grid-agnostic P/D) | RQ1, RQ2 | **H1** (`>=15–30%` op CO2 cut, `<5%` SLO viol.) | `B1`, `B2`, `P3`, `P4` (phase separation + decode `c_cap=0.5–0.7`) | **E1**, **SW1** (`0.5x–3.0x` RPS), **SW3** |
| **OC2** (WAN KV vs. recompute) | RQ2 | **H2** (Sisodia carbon crossover beats naive `P3`) | `P3` vs. `P4` (`Path A–D` Eq. 9 switching) | **E1**, **SW3** (`10/25/100 Gbps` WAN) |
| **OC3** (Serverless GPU cold-start) | RQ3 | **H3** (`S3` beats `S1 k=0` & `S2 k=30/60s`) | `S1`, `S2`, `S2b`, `S3` (`K in {1,5,10,30,60}s`, Eq. 10) | **E2**, **SW4** (`10.3/48/84s` loaders) |
| **OC4** (Embodied dominance) | RQ4 | **H4** (`>50%` embodied share in clean grids) | `SCI_op + SCI_emb`, `4-yr` vs. `9/3-yr` reuse | **E1**, **SW4** (`LT in {3..6} yr`, `9/3 yr`) |
| **OC5** (CI noise & grid greening) | RQ2, RQ4 | Robustness of **H1–H2** under CI variance | `P4` (observed/forecast) vs. `P5` (Oracle CI) | **SW2** (UK-only vs. Wind vs. UK-JP ~60x) |
| **OC6** (Phase DVFS & hardware tier) | RQ1, RQ2 | Magnitude of **H1** power savings | `H100`, `H100cap`, `A100`, `L4` (`gamma in [0.5,0.7,1.0]`) | **SW3** (SLO tiers & decode hardware) |
| **OC7** (Reproducibility deficit) | RQ1–RQ4 | All (**H1–H4**) | Open `SimPy 4.1.2`, `10` seeds (`100..109`), Wilcoxon `p<0.05` | Full suite (**E1–E2**, **SW1–SW4**) |
