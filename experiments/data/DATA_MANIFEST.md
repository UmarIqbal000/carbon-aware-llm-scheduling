# Experimental Dataset & Trace Manifest

**Maintainer:** Umar Iqbal (`umar.iqbal.cs28@directiilm.edu`)  
**Collection Date (UTC):** `2026-11-11T20:37:31Z` to `2026-11-12`  
**Local Root:** `./cloud-paper/experiments/data/`  

All local traces and hardware carbon tables in this directory were fetched from open repositories/APIs returning `HTTP 200` under **`CC-BY-4.0`** licenses, verified directly against repository license files and API metadata. Resources that were unreachable or gated by automated anti-bot/paywall controls were **never** bypassed and are transparently documented in Section 4.

---

## 1. Real LLM Inference Workload Traces

| Local File | Source Repository & Exact URL | License | Access Date | Size (Bytes) | Records & Time Window | Verified Summary Statistics |
|---|---|---|---|---:|---|---|
| [`AzureLLMInferenceTrace_conv.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceTrace_conv.csv) | `Azure/AzurePublicDataset` — `https://raw.githubusercontent.com/Azure/AzurePublicDataset/master/data/AzureLLMInferenceTrace_conv.csv` | `CC-BY-4.0` ([`AZURE_DATASET_LICENSE.txt`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AZURE_DATASET_LICENSE.txt)) | `2026-11-11T20:37:31Z` | `719,188` | `19,366` rows; `2023-11-16 18:15:46.680590` to `19:14:08.402527` (`58.36 min`) | Schema: `TIMESTAMP, ContextTokens, GeneratedTokens`. Mean arrival rate `5.53 rps` (inter-arrival CV `1.094`). `ContextTokens`: mean `1154.7`, P50 `1020.0`, P95 `4083.0`, max `14050`. `GeneratedTokens`: mean `211.1`, P50 `129.0`, P95 `451.0`, max `1000`. |
| [`AzureLLMInferenceTrace_code.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceTrace_code.csv) | `Azure/AzurePublicDataset` — `https://raw.githubusercontent.com/Azure/AzurePublicDataset/master/data/AzureLLMInferenceTrace_code.csv` | `CC-BY-4.0` ([`AZURE_DATASET_LICENSE.txt`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AZURE_DATASET_LICENSE.txt)) | `2026-11-11T20:37:31Z` | `320,117` | `8,819` rows; `2023-11-16 18:17:03.979960` to `19:14:19.928016` (`57.27 min`) | Schema: `TIMESTAMP, ContextTokens, GeneratedTokens`. Mean arrival rate `2.57 rps` (bursty inter-arrival CV `13.152`). `ContextTokens`: mean `2047.8`, P50 `1469.0`, P95 `7303.3`, max `7437`. `GeneratedTokens`: mean `27.9`, P50 `13.0`, P95 `90.0`, max `1899`. |

Companion official Azure documentation archived locally (`2026-11-11T20:37:31Z`, `CC-BY-4.0`):
- [`AzureLLMInferenceDataset2023.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceDataset2023.md) (`2,636` B; Splitwise ISCA 2024 release)
- [`AzureLLMInferenceDataset2024.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceDataset2024.md) (`2,499` B; DynamoLLM HPCA 2025 1-week release docs) & [`AzureLLMInferenceDataset2024Links.txt`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceDataset2024Links.txt) (`234` B)
- [`AzureFunctionsInvocationTrace2021.md`](file:///c:/Users/umari/Cloud%20Computing Research%20Paper/cloud-paper/experiments/data/AzureFunctionsInvocationTrace2021.md) (`3,328` B) & [`AzureGreenSKUFramework2023.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureGreenSKUFramework2023.md) (`7,500` B)

> **Usage Note:** Because the two 2023 Azure traces span `~58 min` each at `2.57–5.53 rps` with contrasting prefill/decode shapes (long-decode `conv` vs. prefill-heavy bursty `code`), multi-hour and 24-hour diurnal experiments in `DESIGN.md` use empirical resampling/tiling from these verified token-length and inter-arrival distributions modulated by configurable intensity profiles, while `1-hour` micro-trace fidelity runs replay the raw timestamps directly.

---

## 2. Real Multi-Region Grid Carbon Intensity Traces

To build a fully open, reproducible multi-region carbon environment without proprietary APIs, we combine two verified 30-minute regional grid datasets under `CC-BY-4.0`:

### 2.1 United Kingdom NESO Regional & National Carbon Intensity (October 2025)

| Local File | Source Endpoint | License | Access Date | Size (Bytes) | Coverage & Columns |
|---|---|---|---|---:|---|
| [`uk_regional_carbon_intensity_oct2025.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/uk_regional_carbon_intensity_oct2025.csv) | `https://api.carbonintensity.org.uk/regional/intensity/2025-10-01T00:00Z/2025-10-28T23:30Z` (fetched in two 14-day chunks) | `CC-BY-4.0` (UK NESO Carbon Intensity API; verified on `carbonintensity.org.uk`) | `2026-11-11T20:37:31Z` | `1,893,651` | `24,192` rows (`1,344` 30-min slots `2025-09-30T23:30Z`–`2025-10-28T23:30Z` × `18` regions). Cols: `from, to, regionid, dnoregion, shortname, forecast_gco2_kwh, index`. |
| [`uk_regional_carbon_intensity_oct2025.json`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/uk_regional_carbon_intensity_oct2025.json) | Raw JSON payload matching the CSV above | `CC-BY-4.0` | `2026-11-11T20:37:31Z` | `23,980,184` | Full raw API regional generation-mix & intensity objects (`2` API chunks). |
| [`uk_national_carbon_intensity_oct2025.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/uk_national_carbon_intensity_oct2025.csv) | `https://api.carbonintensity.org.uk/intensity/2025-10-01T00:00Z/2025-10-28T23:30Z` | `CC-BY-4.0` | `2026-11-11T20:37:31Z` | `67,470` | `1,344` rows (`from, to, forecast_gco2_kwh, actual_gco2_kwh, index`). Actual mean `142.23`, std `75.46`, min `32`, max `279 gCO2eq/kWh` (forecast mean `142.98`, std `78.34`). |

Selected UK regions span low-carbon wind-rich zones to higher-intensity fossil zones (`forecast_gco2_kwh`, `N = 1,344` slots each):
- `South Scotland` (`regionid=2`): mean `9.75`, std `17.82`, min `0`, max `129 gCO2eq/kWh`
- `North East England` (`regionid=4`): mean `28.83`, std `24.87`, min `3`, max `108`
- `North Scotland` (`regionid=1`): mean `35.65`, std `82.50`, min `0`, max `355` *(high wind volatility)*
- `North West England` (`regionid=3`): mean `78.38`, std `76.23`, min `2`, max `290`
- `London` (`regionid=13`): mean `163.32`, std `83.70`, min `13`, max `326`
- `South Wales` (`regionid=7`): mean `240.50`, std `129.69`, min `8`, max `392`

### 2.2 Japan FY2024 TSO-Level 30-Minute CO2 Emission Factors

**Source:** Zenodo Record `18396311` — *Time-Varying Grid CO2 Emission Factors Derived from TSO-Level Generation Mix in Japan* ([`DOI:10.5281/zenodo.18396311`](https://doi.org/10.5281/zenodo.18396311), published `2026-01-28`, fetched `2026-11-11`), license **`CC-BY-4.0`**, documented in [`japan_tso_2024/README.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/japan_tso_2024/README.md) (`9,074` B).

> **CRITICAL UNIT NORMALIZATION RULE:** Every CSV reports `emission_factor_kgco2_per_kwh` in **`kgCO2/kWh`**. All simulator ingestion scripts **MUST multiply by `1000.0`** to align with UK NESO `gCO2eq/kWh`!

| Local File (`./japan_tso_2024/`) | Size (Bytes) | Rows & Columns | Mean (`gCO2eq/kWh`) | Std (`gCO2eq/kWh`) | Min–Max (`gCO2eq/kWh`) |
|---|---:|---|---:|---:|---:|
| `emission_factor_2024_Kansai_Transmission_and_Distribution.csv` | `778,100` | `17,520` 30-min rows (`2024-04-01`–`2025-03-31` JST); `timestamp_jst_iso, emission_factor_kgco2_per_kwh` | `356.20` | `77.96` | `82.45–504.19` |
| `emission_factor_2024_Kyushu_Electric_Power_Transmission_and_Distribution.csv` | `777,674` | `17,520` rows | `384.41` | `98.00` | `134.65–552.37` |
| `emission_factor_2024_Hokkaido_Electric_Power_Network.csv` | `771,531` | `17,520` rows | `529.07` | `109.98` | `139.24–755.85` |
| `emission_factor_2024_Chubu_Electric_Power_Grid.csv` | `771,118` | `17,520` rows | `537.20` | `93.75` | `196.17–680.23` |
| `emission_factor_2024_TEPCO_Power_Grid.csv` | `770,361` | `17,520` rows | `581.64` | `73.65` | `302.30–671.48` |

Combining UK NESO (`9.8–240.5 gCO2eq/kWh` mean) and Japan FY2024 (`356.2–581.6 gCO2eq/kWh` mean) provides a realistic `~60x` mean spatial span and strong diurnal solar/wind swings for geo-distributed cluster simulation.

---

## 3. Hardware Power & Embodied Carbon Reference Tables (Azure GreenSKU-Framework)

**Source:** `Azure/AzurePublicDataset/analysis/GreenSKU-Framework` ([`DOI:10.5281/zenodo.10896254`](https://doi.org/10.5281/zenodo.10896254), `CC-BY-4.0`, fetched `2026-11-11`) under `./greensku_carbon_data/`:

- `params.yaml` (`1,231` B): `PUE = 1.12`, server/component baseline `lifetime = 72` months (`6 years`).
- `CPU.yaml` (`1,038` B): Genoa (`290 W`, `30.7 kgCO2e`), Bergamo (`400 W`, `28.3 kgCO2e`).
- `DRAM.yaml` (`910` B): DDR5 64 GB (`23.68 W`, `105.4 kgCO2e`), DDR5 96 GB (`35.52 W`, `158.1 kgCO2e`).
- `SSD.yaml` (`661` B) & `SSD_reuse.yaml` (`325` B): 2 TB (`11.2 W`, `34.65 kgCO2e`), 4 TB (`16.8 W`, `69.3 kgCO2e`).
- `NIC.yaml` (`345` B): 100G NIC (`19.0 W`, `58.09 kgCO2e`).
- `server.yaml` (`944` B), `rack.yaml` (`258` B), `data_center.yaml` (`313` B), `CXL_controller.yaml` (`492` B): 1U chassis (`35 W + 75 W PSU/fan`, `350 kg + 1.06 kg`), 2U chassis (`35 W + 112.5 W`, `375 kg + 1.59 kg`), rack (`500 W`, `500 kg / 180 mo`), DC building (`9,000,000 kg / 240 mo`).

*(GPU die/package embodied carbon is supplemented from EcoServe `arXiv:2502.05043v2` and LLMCarbon `arXiv:2309.14393`, documented in [`parameter_sources.json`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/parameter_sources.json).)*

---

## 4. Transparent Record of Reachability & Omitted External Datasets

1. **Electricity Maps CSVs (`data.electricitymaps.com` / `portal.electricitymaps.com`):** On `2026-11-11T20:37Z`, `https://portal.electricitymaps.com/datasets` returned **`HTTP 403`** behind Cloudflare challenge, and `https://data.electricitymaps.com/2025-01-27/*.csv` (`US-CAL-CISO`, `DE`, `SE`, `FR`, `US-TEX-ERCO`, `IN-WE`) failed DNS resolution (`Errno 11001`). Neither gate was bypassed; UK NESO + Japan TSO open `CC-BY-4.0` datasets replace them completely.
2. **Azure LLM Inference Trace 2024 (`1-week` releases):** Verified reachable via `HEAD HTTP 200` (`AzureLLMInferenceTrace_code_1week.csv` = `691,989,454` B; `AzureLLMInferenceTrace_conv_1week.csv` = `1,135,195,393` B; URLs archived in [`AzureLLMInferenceDataset2024Links.txt`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/AzureLLMInferenceDataset2024Links.txt)). Omitted from local repository mirroring solely to keep workspace size compact; the 2023 traces are stored locally.
3. **ACM Digital Library Paywalled PDFs (`caribou_2024.pdf`, `tapas_2025.pdf`):** `dl.acm.org` returned **`HTTP 403`** (`10.1145/3694715.3695954`, `10.1145/3716368` / TAPAS) and was not bypassed; their metadata/abstract findings are only cited if accessed openly or verified via OpenAlex/survey coverage.
