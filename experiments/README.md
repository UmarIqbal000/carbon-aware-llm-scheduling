# Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference: Simulation Suite

> **Methodological Scope Notice:** All quantitative results under `./results/` are **parameterized discrete-event simulation outputs** generated with `SimPy 4.1.2` driven by open trace inputs and peer-reviewed hardware/serving parameters. They are **not** telemetry collected from a physical multi-continent production GPU cluster or hardware power meter. Explicit calibration assumptions are itemized in [Section 4](#4-calibration-assumptions-and-limitations).

---

## 1. Environment & File Inventory

Verified Python environment (`./cloud-paper/.venv/Scripts/python.exe`):
- `simpy==4.1.2`
- `numpy==2.5.4`
- `pandas==3.1.1`
- `scipy==1.18.1`
- `pyyaml==6.0.3`

### Directory Layout (`./cloud-paper/experiments/`)
- [`DESIGN.md`](DESIGN.md) — Formal discrete-event architecture, mathematical operational/embodied carbon equations, routing/keep-alive policies (`B1, B2, P3, P4, P5, P3_overprov`; `S1, S2, S2b, S3`), hypotheses (`H1–H4`), and evaluation matrix (`E1, E2, SW1–SW4, H4`).
- [`parameter_sources.json`](parameter_sources.json) — Traceable literature parameter table and explicit calibration notes.
- [`data/DATA_MANIFEST.md`](data/DATA_MANIFEST.md) — Trace URLs, `CC-BY-4.0` license records, fetch timestamps, and summary statistics.
- [`sim_config.py`](sim_config.py) — Seed list (`100..109`), `GPU_PROFILES` (`H100`, `A100`, `L4`), `REGIONS`, `SLO_CONFIGS`, GreenSKU YAML loader, WAN RTT matrix, and `ClusterConfig` / `ServerlessConfig` dataclasses.
- [`trace_loader.py`](trace_loader.py) — Cached loaders for 2023 Azure LLM traces, UK NESO regional/national carbon intensity, and Japan FY2024 TSO emission factors (applying `× 1000.0` `kgCO2/kWh -> gCO2eq/kWh` normalization), plus seed-paired request stream generators (`1h` raw replay, `1h` rotated load scaling, and `24h` block-resampled diurnal profile).
- [`simulator.py`](simulator.py) — Two-track `SimPy 4.1.2` discrete-event simulator:
  - **Track A (`run_cluster_simulation`)**: 3-region heterogeneous P/D cluster with non-linear batching energy (`gamma=0.70`), colocated prefill-stall interference (`coloc_decode_rate=0.20`), intra-DC vs. cross-region WAN KV-cache transfer, Sisodia-style compute-vs-transfer crossover routing (`P4`), and counterfactual oracle (`P5`).
  - **Track B (`run_serverless_simulation`)**: Single-region autoscaling serverless worker pool modeling checkpoint cold-start stalls (`ServerlessLLM`, `Safetensors`, `PyTorch`), `LACE-RL`-style execution/idle/cold energy decomposition, online uncensored Kaplan–Meier / Nelson–Aalen hazard tracking, and dynamic carbon-aware keep-alive (`S3`).
- [`run_experiments.py`](run_experiments.py) — Parallel `ProcessPoolExecutor` orchestrator executing 10 seeds (`100..109`) per configuration (`226` configurations = `2,260` total simulation runs) and saving raw per-seed CSVs to `./results/`.
- [`analyze_results.py`](analyze_results.py) — Computes per-configuration sample means, standard deviations, Student-$t$ 95% confidence intervals (`df = 9`, `t_{0.975,9} = 2.262157`), medians, IQRs, matched-seed two-sided Wilcoxon signed-rank tests, and explicit `H1–H4` hypothesis verification outputs.

### Output Artifacts (`./results/`, `22` CSV files)
| File | Rows | Description |
|---|---:|---|
| `raw_e1_1h.csv` | 100 | Raw per-seed Track A runs (`E1`, 1h raw replay, `conv` & `code`, 5 policies × 10 seeds) |
| `raw_e1_24h.csv` | 100 | Raw per-seed Track A runs (`E1`, 24h diurnal resampled, `conv` & `code`, 5 policies × 10 seeds) |
| `raw_e2_serverless.csv` | 240 | Raw per-seed Track B runs (`E2`, `1h` & `24h`, 3 regions, `S1/S2/S2b/S3` × 10 seeds) |
| `raw_sw1_load.csv` | 200 | Sweep SW1 arrival-rate scaling (`0.5x–3.0x` on `conv`) |
| `raw_sw2_grid.csv` | 260 | Sweep SW2 grid topology (`low_diff_uk`, `volatile_uk`, `cross_cont_60x`) & NESO forecast/lag noise (`24h`) |
| `raw_sw3_slo_hw_wan.csv` | 490 | Sweep SW3 decode GPU tiers (`H100_cap55`, `H100_uncap`, `A100_400W`, `L4_72W`), SLO tightness, & WAN BW (`10/25/100 Gbps`) |
| `raw_sw4_serverless.csv` | 410 | Sweep SW4 serverless checkpoints (`ServerlessLLM/Safetensors/PyTorch`), `llama2_70b`/`opt_13b`, cold power frac, idle mode |
| `raw_sw4_cluster_lifetime.csv` | 380 | Sweep SW4 embodied lifetime (`3–6 yr` uniform, `9 yr host / 3 yr GPU`), `PUE` (`1.10/1.12/1.20`), & `MFU gamma` (`0.5/0.7/1.0`) |
| `raw_h4_elastic.csv` | 80 | Explicit H4 clean scale-out paradox (`P3_overprov` +4 clean nodes vs equal-fleet `B2/P3/P4`) |
| `summary_*.csv` (9 files) | 226 configs | Mean, std, 95% Student-$t$ CI half-width & bounds, median, and IQR matching each `raw_*.csv` |
| `wilcoxon_e1_cluster.csv` | 80 tests | Paired two-sided Wilcoxon tests (`P4` vs `B1`, `B2`, `P3`, `P5`) across `E1` horizons, workloads & metrics |
| `wilcoxon_e2_serverless.csv` | 108 tests | Paired two-sided Wilcoxon tests (`S3` vs `S1`, `S2`, `S2b`) across `E2` horizons, regions & metrics |
| `hypotheses_verification.csv` | 18 checks | Quantitative `H1–H4` support/partial/nuanced audit derived directly from saved summaries |

---

## 2. Dataset Provenance, Licenses & Preprocessing

All traces live locally under `./data/` and were fetched from open endpoints under **`CC-BY-4.0`** licenses (verified in [`data/DATA_MANIFEST.md`](data/DATA_MANIFEST.md); paywalled/anti-bot-gated external endpoints returned `HTTP 403` / DNS errors and were omitted without bypass).

1. **Azure LLM Inference Traces 2023 (`conv` and `code`)**
   - **URLs:** `https://raw.githubusercontent.com/Azure/AzurePublicDataset/master/data/AzureLLMInferenceTrace_conv.csv` (`19,366` rows, `5.53 rps`, IA CV `1.094`, `58.36 min`) and `AzureLLMInferenceTrace_code.csv` (`8,819` rows, `2.57 rps`, IA CV `13.152`, `57.27 min`).
   - **Access Timestamp & License:** `2026-11-11T20:37:31Z`, `CC-BY-4.0` ([`AZURE_DATASET_LICENSE.txt`](data/AZURE_DATASET_LICENSE.txt)).
   - **Trace Transformations:**
     - `1h` (`rps_scale=1.0`): Direct timestamp replay with tiny non-reordering seed jitter (`±1 ms`).
     - `1h` (`rps_scale != 1.0`, `SW1`): Inter-arrival times scaled by `1 / rps_scale` and deterministically rotated/tiled over a fixed `3600 s` window.
     - `24h` (**synthetic diurnal extension**): Empirical 5-minute contiguous trace blocks (`12` blocks) block-resampled across `48 × 30-min` UTC slots (`86,400 s`), modulated by a regional local-time sinusoidal multiplier `1.0 + 0.30 * cos(2*pi*(local_hour - 14)/24)` (`0.70x–1.30x`, preserving exact empirical token pairs and within-block burst CV).
2. **UK NESO Regional & National Carbon Intensity (October 2025)**
   - **URLs:** `https://api.carbonintensity.org.uk/regional/intensity/2025-10-01T00:00Z/2025-10-28T23:30Z` and `/intensity/2025-10-01T00:00Z/2025-10-28T23:30Z` (`1,344` 30-min slots per region/national).
   - **Access Timestamp & License:** `2026-11-11T20:37:31Z`, `CC-BY-4.0` (UK NESO).
   - **Noise Model (`SW2`):** Empirical residuals `(actual_gco2_kwh - forecast_gco2_kwh)` from `uk_national_carbon_intensity_oct2025.csv` (verified MAE `8.48`, RMSE `11.43 gCO2eq/kWh`) drive `neso_forecast` and `noise_2x` scheduler signals alongside real `lag_30m` / `lag_60m` lookback slots.
3. **Japan FY2024 TSO-Level 30-Minute CO2 Emission Factors**
   - **URL / DOI:** Zenodo Record `18396311` (`https://doi.org/10.5281/zenodo.18396311`, fetched `2026-11-11`, `CC-BY-4.0`), stored under `./data/japan_tso_2024/*.csv` (`17,520` 30-min rows, `2024-04-01`–`2025-03-31` JST).
   - **Unit Normalization:** Raw column `emission_factor_kgco2_per_kwh` is explicitly **multiplied by `1000.0`** in `trace_loader.py` to yield `gCO2eq/kWh` matching UK NESO (October 2024 slice aligned cleanly to UK Oct 2025 UTC windows).
4. **Azure GreenSKU-Framework Hardware Carbon Tables**
   - **URL / DOI:** `Azure/AzurePublicDataset/analysis/GreenSKU-Framework` (`https://doi.org/10.5281/zenodo.10896254`, fetched `2026-11-11`, `CC-BY-4.0`), stored in `./data/greensku_carbon_data/*.yaml` (`PUE=1.12`, Genoa `290 W` / `30.7 kgCO2e`, 4×64 GB DDR5 `23.68 W` / `105.4 kgCO2e` per DIMM, 2 TB SSD `11.2 W` / `34.65 kgCO2e`, 100G NIC `19.0 W` / `58.09 kgCO2e`, 2U chassis, `0.20` idle derate factor).

---

## 3. Exact Commands to Reproduce All Experiments & Tables

Run all commands from the workspace root (`c:\Users\umari\Cloud Computing Research Paper`) using the project virtual environment:

```powershell
# 1. Run every simulation suite (E1 1h+24h, E2, SW1, SW2, SW3, SW4, H4; 2,260 runs total)
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite all --workers 11

# Or execute individual suites selectively:
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite e1_1h  --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite e1_24h --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite e2     --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite sw1    --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite sw2    --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite sw3    --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite sw4    --workers 11
& ".\cloud-paper\.venv\Scripts\python.exe" -u ".\cloud-paper\experiments\run_experiments.py" --suite h4     --workers 11

# 2. Compute Student-t 95% CIs, two-sided Wilcoxon signed-rank tests, and H1-H4 checks:
& ".\cloud-paper\.venv\Scripts\python.exe" ".\cloud-paper\experiments\analyze_results.py"
```

---

## 4. Calibration Assumptions and Limitations

1. **Analytical Compute/Memory Timing inside Discrete-Event Queues:** Prefill service time and continuous-batching decode step times (`Splitwise` Table IV / Section VI-A anchors) are parameterized discrete-event queueing laws rather than cycle-accurate GPU kernel traces or live vLLM/SGLang runs.
2. **Design-Calibrated WAN Network & Power Parameters:** Inter-region RTTs (`0.5 ms` intra-DC, `20 ms` intra-UK, `30 ms` intra-JP, `200 ms` UK<->JP), default commodity KV WAN bandwidth (`10 Gbps`, swept to `25/100 Gbps`), NIC/WAN port power (`100 W` WAN / `38 W` intra-DC), colocated decode-stall penalty (`0.20x` rate during active prefill), and serverless cold-start power fraction (`0.65 * TDP`, swept `[0.45, 0.85]`) are explicit calibrated modeling assumptions documented in `parameter_sources.json`.
3. **24-Hour Trace Synthesis & Grid Pairing:** Because open 2023 Azure traces span `~58 min`, `24h` runs use empirical block resampling modulated by a synthetic diurnal local-time envelope (`0.70x–1.30x`), paired across Oct 2025 UK NESO and Oct 2024 Japan TSO 30-min intervals.
4. **Zero-Carbon Periods in UK Regions:** North and South Scotland frequently reach `0 gCO2eq/kWh` during windy Oct 2025 days (`8/10` sampled windows in `North Scotland` `24h`), producing exact zero differences across policies on clean days and leaving only `1–2` non-zero pairs for `scipy.stats.wilcoxon` (`p >= 0.50` on `sci_op` in `North Scotland` despite consistent `-10.7%` to `-14.6%` mean reductions triggered on high-carbon excursions).
5. **Statistical Protocol:** All configurations run 10 paired seeds (`100..109`). Confidence intervals use exact Student-$t$ critical values (`t_{0.975,9} = 2.262157`), and significance tests use `scipy.stats.wilcoxon(..., alternative="two-sided", zero_method="wilcox")` with no post-hoc data filtering.

---

## 5. Summary of Verified Hypothesis Outcomes (`hypotheses_verification.csv`)

- **H1 (Disaggregation + Carbon-Aware Scheduling vs. `B1`/`B2`):** **SUPPORTED** on `conv` (`1h`: `P4` cuts `SCI_op` by `60.8%` vs `B1` and `43.9%` vs `B2`, `p = 0.001953`, with `0.81%` SLO violations; `24h`: `60.7%` / `44.1%` reduction, `0.82%` SLO violations); **PARTIALLY SUPPORTED** on bursty `code` (`1h`/`24h`: `28.5%` reduction vs `B1` and `23.4%`/`23.5%` vs `B2`, `p = 0.001953`, cutting SLO violations from `18.25%`/`19.47%` under rigid `B2` down to `6.57%`/`6.24%` via prefill-overflow colocated fallback and Path D, though still slightly above `5%` under extreme burst CV `13.15`).
- **H2 (`P4` Carbon+KV Hybrid Router vs. Naive Cross-Region `P3`):** **SUPPORTED** across all four `E1` settings (`p = 0.001953`): `P4` prevents `10 Gbps` WAN KV congestion via Sisodia crossover routing, reducing SLO violations from `44.45% -> 6.57%` (`1h code`, TTFT P95 `39,318 ms -> 1,614 ms`) and `4.93% -> 0.81%` (`1h conv`, TTFT P95 `1,062 ms -> 506 ms`), with comparable or lower SLO violations across `SW2` (`low_diff_uk`: `0.08%` vs `10.71%` at `+20.7%` operational carbon cost relative to P3).
- **H3 (`S3` Dynamic Keep-Alive in Serverless LLM):** **SUPPORTED** in wind-rich/volatile UK grids (`North Scotland`, `South Scotland`: `S3` cuts SLO violations by `66.9%–69.8%` vs `S1` and `30.5%–35.0%` vs `S2`, `p = 0.001953`, while achieving lowest mean `SCI_op`) and **PARTIALLY SUPPORTED** in persistently carbon-intensive `TEPCO` (`24h`: `S3` significantly lowers `SCI_op` by `-7.03%` vs `S2` and `-11.02%` vs `S2b`, `p = 0.001953`, by trading `+9.15` pp cold-start SLO increase vs `S2` while remaining `11.65` pp below `S1`).
- **H4 (Embodied Dominance & Clean Scale-Out Paradox):** **SUPPORTED**: In clean `South Scotland`, operational carbon shrinks until embodied manufacturing accounts for `93.0%` of regional total carbon (`24h`), and in the equal-SLO clean scale-out experiment (`H4_elastic`), adding `+4` clean nodes under `P3_overprov` decreases `SCI_op` slightly (`0.00821 -> 0.00804 gCO2e/1k-tok`) while inflating amortized `SCI_emb` (`0.00898 -> 0.01497` at 4-yr uniform; `0.00680 -> 0.01133` at `9yr host / 3yr GPU`) and total `SCI` by `+32.6%` (`4yr`) / `+27.7%` (`9yr/3yr`) relative to equal-fleet `P4`.
