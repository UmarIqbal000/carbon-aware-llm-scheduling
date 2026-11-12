# Time-Varying Grid CO2 Emission Factors Derived from TSO-Level Generation Mix in Japan (FY2024)

## Overview
This dataset provides hourly (1-hour resolution) grid carbon intensity data for fiscal year 2024 (April 2024–March 2025) for each electricity supply area operated by the nine Japanese transmission system operators (TSOs).  Grid carbon intensity is expressed as CO₂ emission factors (kg-CO₂/kWh) derived from observed electricity generation mixes under prevailing operating conditions.

The dataset is designed to support urban- and regional-scale energy and emissions analyses, including demand-sensitive carbon accounting and spatio-temporal comparison of grid emission characteristics.

---

## Data Structure

### Main dataset
Hourly grid carbon intensity for each TSO service area:
```
emission_factor_2024_[tso_xxx].csv
```

**Variables**
- `timestamp_jst_iso`  
  ISO 8601 timestamp with explicit time zone offset (JST, +09:00)
- `emission_factor_kgco2_per_kwh`  
  Grid carbon intensity (kg-CO₂/kWh)

### Auxiliary datasets
For transparency and reference, auxiliary datasets are provided:
```
auxiliary_data/
├─ generation_co2_t_2024_[tso_xxx].csv
├─ generation_mix_MWh_2024_[tso_xxx].csv
└─ thermal_other_reference_factors.csv

```

#### `generation_co2_t_2024_[tso_xxx].csv`

This file provides fuel-wise CO₂ emission equivalents (in tonnes of CO₂) for each hour and TSO service area. The values represent lifecycle CO₂ emission equivalents (LCCO₂) attributed to electricity generation by fuel type at each time interval, calculated using the fuel-specific emission factors described in the Methodology section.

Typical variables include:
- `nuclear_co2_t`
- `thermal_coal_co2_t`
- `thermal_lng_co2_t`
- `thermal_oil_co2_t`
- `hydro_co2_t`
- `solar_co2_t`
- `wind_co2_t`
- `biomass_co2_t`
- `geothermal_co2_t`

All values are expressed in tonnes of CO₂ (t-CO₂) per hour.

---

#### `generation_mix_MWh_2024_[tso_xxx].csv`
This file provides fuel-wise electricity generation volumes (in MWh) for each hour and TSO service area, as publicly disclosed by each TSO.

Typical variables include:
- `nuclear_MWh`
- `thermal_coal_MWh`
- `thermal_lng_MWh`
- `thermal_oil_MWh`
- `hydro_MWh`
- `solar_MWh`
- `wind_MWh`
- `biomass_MWh`
- `geothermal_MWh`
- `pumped_storage_MWh`
- `battery_MWh`

In addition, the following aggregate variables are included:
- `area_demand_MWh`  
  Electricity demand within each TSO service area
- `total_generation_MWh`  
  Total electricity generation within each TSO service area

All values are expressed in megawatt-hours (MWh) per hour.

---

#### `thermal_other_reference_factors.csv`
This file provides utility-specific reference CO₂ emission factors for the category
labeled as “other thermal power” in published generation statistics.
The values are derived by assuming mixed-fuel thermal generation and are calculated
as weighted averages of fuel-specific emission factors based on utility-level
thermal fuel composition ratios.


---

## Data Sources
- Publicly available TSO-level hourly electricity generation statistics for FY2024
- Fuel-specific CO₂ emission coefficients from published literature:
  - Imamura et al. (2016)
  - Ihara & Kamiya (2025)
- Fuel composition ratios disclosed by each TSO

---

## Methodology

### General principles
The emission factors adopted in this dataset are not intended to represent exact marginal emissions in a market or dispatch sense. Instead, they provide a consistent and transparent basis for comparing relative emission levels and demand-sensitive emission responses across TSO service areas and time periods.

All emission factors are applied uniformly across the dataset to ensure internal consistency and should be interpreted as descriptive, diagnostic indicators, rather than precise representations of real-time system emissions.

---

### Non-fossil power generation

For non-fossil power generation technologies, constant lifecycle-equivalent CO₂ emission factors are applied.

These values represent representative life-cycle CO₂ emission intensities reported in the literature and are treated as time-invariant parameters throughout the dataset.

Specifically, the following emission factors are adopted (kg-CO₂/kWh):
- Nuclear power: 0.019
- Hydro power: 0.011
- Geothermal power: 0.013
- Solar power (residential PV): 0.038
- Solar power (commercial / non-residential PV): 0.059
- Wind power: 0.026

These values are adopted from Imamura et al. (2016) and Ihara & Kamiya (2025).

### Thermal power generation

For thermal power generation, utility-specific CO₂ emission factors are derived based on fuel composition ratios publicly disclosed by each TSO. In the published statistics, thermal power generation is categorized not only into coal-fired, oil-fired, and LNG-fired plants, but also includes an additional category labeled as "other thermal power". This category is interpreted in this dataset as mixed-fuel thermal generation, rather than single-fuel dedicated plants.
To account for this, the CO₂ emission factor for the "other thermal power" category is estimated for each TSO as a weighted average of fuel-specific emission factors, using the utility-specific shares of coal-, oil-, and LNG-fired thermal generation.

The fuel-specific CO₂ emission factors adopted in this dataset are:
- Coal-fired thermal power: 0.943 kg-CO₂/kWh
- Oil-fired thermal power: 0.738 kg-CO₂/kWh
- LNG-fired thermal power: 0.599 kg-CO₂/kWh

These values are adopted from:
- Imamura et al. (2016)
- Ihara & Kamiya (2025)

Finally, for each TSO, the aggregated thermal emission factor is calculated as the weighted average across all thermal categories (coal-fired, oil-fired, LNG-fired, and mixed-fuel thermal generation), based on the reported fuel composition ratios. Utility-specific fuel composition assumptions used in this calculation are provided in a separate reference table.
```
thermal_other_reference_factors.csv
```

---

### Biomass power generation
For biomass-only power generation:
- Direct CO₂ emissions during combustion are assumed to be zero, following the carbon-neutrality convention.
- Indirect lifecycle emissions are approximated using the indirect emission component of conventional thermal power generation.

Accordingly, an emission factor of 0.079 kg-CO₂/kWh is applied.

---

### Interconnection lines and battery storage

For electricity supplied via interconnection lines and battery storage systems, the generation mix at the time of reception cannot be uniquely identified.

Therefore, a substitute emission factor of 0.575 kg-CO₂/kWh is applied, corresponding to the utility-average emission factor for FY2024.

---

### Pumped storage power generation

For pumped storage:
- CO₂ emissions associated with pumping electricity consumption
- Indirect lifecycle emissions from hydroelectric generation

are both considered.

The emission factor is calculated as the sum of:
- utility-average emission factor (FY2024)
- indirect hydroelectric emission factor (0.011 kg-CO₂/kWh)

resulting in a total emission factor of 0.586 kg-CO₂/kWh.

---

## System Boundary and Life-Cycle Considerations

This dataset quantifies CO₂ emissions associated with electricity generation by combining observed operational conditions and time-varying generation mixes with literature-based, lifecycle-equivalent emission factors. Fuel-specific CO₂ emission factors applied in the dataset are lifecycle–equivalent representative values adopted from the literature and are treated as time-invariant parameters. These coefficients capture typical lifecycle emission intensities of each generation technology, rather than purely direct stack emissions.

The dataset does **not** aim to provide a full cradle-to-grave lifecycle assessment. Instead, lifecycle-equivalent emission factors are adopted as fixed parameters from the literature, rather than being recalculated through process-based lifecycle assessment within this dataset. Accordingly, lifecycle emissions associated with fuel extraction, plant construction, equipment manufacturing, and decommissioning are **not modeled explicitly on a technology-specific basis**, except where noted (e.g., indirect emission components for biomass, hydroelectric power, and pumped storage).

As a result, the resulting emission estimates should be interpreted as lifecycle-equivalent emission indicators driven by operational variability, rather than detailed lifecycle inventories.

---

## License
This dataset is released under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

---

## Citation
Please cite this dataset using the DOI assigned by Zenodo.

---

## References
- Imamura, E., Iuchi, M., & Bando, S. (2016). Comprehensive assessment of life cycle CO₂ emissions from power generation technologies in Japan. CRIEPI Technical Report.
- Ihara, Y., & Kamiya, Y. (2025). Study on evaluation of CO₂ reduction effects and energy costs when introducing electric buses using hourly carbon intensity. JSCE.

