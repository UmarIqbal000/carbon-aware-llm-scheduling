"""Verified configuration, hardware specs, GreenSKU YAML loader, and sweep grids.

All parameters trace directly to `parameter_sources.json`, `DESIGN.md`, and
`./data/greensku_carbon_data/*.yaml`. Explicit design-calibrated simulation
assumptions (WAN RTT, commodity WAN bandwidth, cold-start power fraction, MFU
exponent) are marked explicitly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import yaml


EXPERIMENTS_DIR = Path(__file__).resolve().parent
DATA_DIR = EXPERIMENTS_DIR / "data"
GREENSKU_DIR = DATA_DIR / "greensku_carbon_data"
JAPAN_TSO_DIR = DATA_DIR / "japan_tso_2024"
RESULTS_DIR = EXPERIMENTS_DIR / "results"
PARAM_SOURCES_PATH = EXPERIMENTS_DIR / "parameter_sources.json"

SEEDS: List[int] = list(range(100, 110))  # 10 fixed reproducible seeds: 100..109
SLOT_SECONDS: float = 1800.0  # 30-minute grid carbon intensity interval
HOURS_PER_YEAR: float = 8760.0


@dataclass(frozen=True)
class GPUProfile:
    """Hardware compute, power, memory, and embodied carbon parameters per GPU."""

    name: str
    tdp_w: float
    idle_w: float
    hbm_gb: float
    hbm_bw_gbps: float
    nvlink_bw_gbps: float
    ib_bw_gbps: float
    embodied_kgco2e: float
    # Uncontended Llama-70B serving latency anchors (Splitwise Table IV)
    prefill_base_ms: float
    prefill_ms_per_tok: float
    decode_step_ms: float
    kv_stall_ms: float
    decode_max_batch_coloc: int = 32
    decode_max_batch_disagg: int = 40
    gpus_per_replica: int = 4
    alpha_mem: float = 120.0  # HBM KV-bandwidth contention slope


@dataclass(frozen=True)
class HostProfile:
    """Host server ancillary power and embodied carbon parsed from GreenSKU YAMLs."""

    cpu_name: str
    cpu_w: float
    cpu_embodied_kg: float
    dram_dimms: int
    dram_w_per_dimm: float
    dram_embodied_kg_per_dimm: float
    ssd_count: int
    ssd_w: float
    ssd_embodied_kg: float
    nic_count: int
    nic_w: float
    nic_embodied_kg: float
    chassis_base_w: float
    chassis_fan_w: float
    chassis_embodied_kg: float
    idle_derate_factor: float = 0.20  # GreenSKU spec_derates[10]

    @property
    def peak_power_w(self) -> float:
        return (
            self.cpu_w
            + self.dram_dimms * self.dram_w_per_dimm
            + self.ssd_count * self.ssd_w
            + self.nic_count * self.nic_w
            + self.chassis_base_w
            + self.chassis_fan_w
        )

    @property
    def idle_power_w(self) -> float:
        dynamic = self.cpu_w + self.dram_dimms * self.dram_w_per_dimm + self.chassis_fan_w
        always_on = self.ssd_count * self.ssd_w + self.nic_count * self.nic_w + self.chassis_base_w
        return always_on + self.idle_derate_factor * dynamic

    @property
    def embodied_kgco2e(self) -> float:
        return (
            self.cpu_embodied_kg
            + self.dram_dimms * self.dram_embodied_kg_per_dimm
            + self.ssd_count * self.ssd_embodied_kg
            + self.nic_count * self.nic_embodied_kg
            + self.chassis_embodied_kg
        )


@dataclass(frozen=True)
class RegionSpec:
    """Cloud region specification linking carbon trace source and DC PUE."""

    region_id: str
    display_name: str
    country: str  # "UK" or "JP"
    trace_key: str
    pue: float = 1.12
    utc_offset_hours: float = 0.0


@dataclass(frozen=True)
class SLOConfig:
    """TTFT and TPOT SLO specification (DynamoLLM buckets or DistServe app)."""

    name: str
    mode: str  # "dynamollm_buckets" or "fixed"
    fixed_ttft_ms: Optional[float] = None
    fixed_tpot_ms: Optional[float] = None
    # DynamoLLM Table IV buckets (ms)
    short_ttft_ms: float = 250.0
    short_tpot_ms: float = 100.0
    medium_ttft_ms: float = 400.0
    medium_tpot_ms: float = 100.0
    long_ttft_ms: float = 2000.0
    long_tpot_ms: float = 100.0

    def thresholds_for_request(self, prompt_tokens: int, output_tokens: int) -> Tuple[float, float]:
        if self.mode == "fixed":
            assert self.fixed_ttft_ms is not None and self.fixed_tpot_ms is not None
            return self.fixed_ttft_ms, self.fixed_tpot_ms
        if prompt_tokens < 256 and output_tokens < 100:
            return self.short_ttft_ms, self.short_tpot_ms
        if prompt_tokens < 1024 and output_tokens < 350:
            return self.medium_ttft_ms, self.medium_tpot_ms
        return self.long_ttft_ms, self.long_tpot_ms


def _parse_watts(val: object) -> float:
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().upper().rstrip("W")
    return float(s)


def load_greensku_host_profile(
    cpu_type: str = "Genoa",
    dram_dimms: int = 4,
    ssd_count: int = 1,
    nic_count: int = 1,
) -> HostProfile:
    """Load exact host component power and embodied carbon from GreenSKU YAMLs."""
    with open(GREENSKU_DIR / "CPU.yaml", "r", encoding="utf-8") as f:
        cpu_yaml = yaml.safe_load(f)
    with open(GREENSKU_DIR / "DRAM.yaml", "r", encoding="utf-8") as f:
        dram_yaml = yaml.safe_load(f)
    with open(GREENSKU_DIR / "SSD.yaml", "r", encoding="utf-8") as f:
        ssd_yaml = yaml.safe_load(f)
    with open(GREENSKU_DIR / "NIC.yaml", "r", encoding="utf-8") as f:
        nic_yaml = yaml.safe_load(f)
    with open(GREENSKU_DIR / "server.yaml", "r", encoding="utf-8") as f:
        server_yaml = yaml.safe_load(f)

    cpu_entry = next(
        t["core_counts"][0]
        for v in cpu_yaml
        for t in v["types"]
        if t["type"].lower() == cpu_type.lower()
    )
    dram_entry = next(
        s
        for s in dram_yaml["DDR5"]["frequencies"][0]["sizes"]
        if s["size"] == "64GB"
    )
    ssd_entry = next(
        s for s in ssd_yaml[0]["sizes"] if s["size"] == "2TB"
    )
    nic_entry = next(
        b for b in nic_yaml["bandwidths"] if b["bandwidth"] == "100G"
    )
    srv_2u = next(s for s in server_yaml if s["type"] == "Server-2U")["items"]

    return HostProfile(
        cpu_name=cpu_type,
        cpu_w=_parse_watts(cpu_entry["power"]),
        cpu_embodied_kg=float(cpu_entry["carbon"]),
        dram_dimms=dram_dimms,
        dram_w_per_dimm=_parse_watts(dram_entry["power"]),
        dram_embodied_kg_per_dimm=float(dram_entry["carbon"]),
        ssd_count=ssd_count,
        ssd_w=_parse_watts(ssd_entry["power"]),
        ssd_embodied_kg=float(ssd_entry["carbon"]),
        nic_count=nic_count,
        nic_w=_parse_watts(nic_entry["power"]),
        nic_embodied_kg=float(nic_entry["carbon"]),
        chassis_base_w=_parse_watts(srv_2u["server"]["power"]),
        chassis_fan_w=_parse_watts(srv_2u["fan"]["power"]),
        chassis_embodied_kg=float(srv_2u["server"]["carbon"]) + float(srv_2u["fan"]["carbon"]),
        idle_derate_factor=float(cpu_yaml[0]["spec_derates"][10]),
    )


def load_greensku_pue_default() -> float:
    with open(GREENSKU_DIR / "params.yaml", "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    return float(params["PUE"])


def load_parameter_sources() -> Dict:
    with open(PARAM_SOURCES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# Verified GPU hardware profiles from parameter_sources.json (Splitwise, Ozcan, EcoServe)
GPU_PROFILES: Dict[str, GPUProfile] = {
    "H100": GPUProfile(
        name="H100_SXM5_80GB",
        tdp_w=700.0,
        idle_w=60.0,
        hbm_gb=80.0,
        hbm_bw_gbps=3352.0,
        nvlink_bw_gbps=100.0,
        ib_bw_gbps=400.0,
        embodied_kgco2e=124.9,  # EcoServe Fig. 4 H100 PCIe reference
        prefill_base_ms=15.0,   # Calibrated to Splitwise Table IV (84 ms conv @ 1020 tok; 95 ms code @ 1469 tok)
        prefill_ms_per_tok=0.062,
        decode_step_ms=28.0,    # Splitwise Table IV H100 conv TBT 28 ms (code 31 ms)
        kv_stall_ms=5.0,        # Splitwise Section VI-A H100 non-overlapped per-layer KV stall
        decode_max_batch_coloc=32,
        decode_max_batch_disagg=40,
        gpus_per_replica=4,
        alpha_mem=120.0,
    ),
    "A100": GPUProfile(
        name="A100_SXM4_80GB",
        tdp_w=400.0,
        idle_w=100.0,
        hbm_gb=80.0,
        hbm_bw_gbps=2039.0,
        nvlink_bw_gbps=50.0,
        ib_bw_gbps=200.0,
        embodied_kgco2e=121.5,  # EcoServe Fig. 4 A100 SXM 80G
        prefill_base_ms=25.0,   # Calibrated to Splitwise Table IV (155 ms conv @ 1020 tok; 185 ms code @ 1469 tok)
        prefill_ms_per_tok=0.120,
        decode_step_ms=42.0,    # Splitwise Table IV A100 TBT 40 ms conv / 52 ms code
        kv_stall_ms=8.0,        # Splitwise Section VI-A A100 non-overlapped per-layer KV stall
        decode_max_batch_coloc=32,
        decode_max_batch_disagg=40,
        gpus_per_replica=4,
        alpha_mem=120.0,
    ),
    "L4": GPUProfile(
        name="L4_24GB_DecodeTier",
        tdp_w=72.0,             # EcoServe Fig. 4 L4 TDP 72 W
        idle_w=14.4,            # 0.20 * TDP (LACE-RL / A100 idle ratio range)
        hbm_gb=24.0,
        hbm_bw_gbps=300.0,      # GDDR6 300 GB/s per GPU (8 GPUs/node -> 2400 GB/s aggregate)
        nvlink_bw_gbps=0.0,
        ib_bw_gbps=100.0,
        embodied_kgco2e=41.2,   # EcoServe Fig. 4 L4 embodied carbon 41.2 kgCO2e
        prefill_base_ms=45.0,
        prefill_ms_per_tok=0.350,
        decode_step_ms=54.0,    # Lower memory bandwidth -> ~1.9x slower decode step than H100
        kv_stall_ms=10.0,
        decode_max_batch_coloc=24,
        decode_max_batch_disagg=36,
        gpus_per_replica=8,     # 8x L4 = 192 GB VRAM per quantized/FP8 70B replica
        alpha_mem=90.0,
    ),
}

# Verified regional specs from DATA_MANIFEST.md
REGIONS: Dict[str, RegionSpec] = {
    "South Scotland": RegionSpec("South Scotland", "South Scotland (UK)", "UK", "South Scotland", 1.12, 0.0),
    "North Scotland": RegionSpec("North Scotland", "North Scotland (UK)", "UK", "North Scotland", 1.12, 0.0),
    "North East England": RegionSpec("North East England", "North East England (UK)", "UK", "North East England", 1.12, 0.0),
    "North West England": RegionSpec("North West England", "North West England (UK)", "UK", "North West England", 1.12, 0.0),
    "London": RegionSpec("London", "London (UK)", "UK", "London", 1.12, 0.0),
    "South Wales": RegionSpec("South Wales", "South Wales (UK)", "UK", "South Wales", 1.12, 0.0),
    "TEPCO": RegionSpec("TEPCO", "TEPCO Tokyo (JP)", "JP", "TEPCO", 1.12, 9.0),
    "Kansai": RegionSpec("Kansai", "Kansai (JP)", "JP", "Kansai", 1.12, 9.0),
    "Kyushu": RegionSpec("Kyushu", "Kyushu (JP)", "JP", "Kyushu", 1.12, 9.0),
    "Hokkaido": RegionSpec("Hokkaido", "Hokkaido (JP)", "JP", "Hokkaido", 1.12, 9.0),
    "Chubu": RegionSpec("Chubu", "Chubu (JP)", "JP", "Chubu", 1.12, 9.0),
}

SLO_CONFIGS: Dict[str, SLOConfig] = {
    "mixed_dynamollm": SLOConfig(name="mixed_dynamollm", mode="dynamollm_buckets"),
    "strict_code": SLOConfig(name="strict_code", mode="fixed", fixed_ttft_ms=125.0, fixed_tpot_ms=200.0),
    "moderate_chatbot": SLOConfig(name="moderate_chatbot", mode="fixed", fixed_ttft_ms=2500.0, fixed_tpot_ms=150.0),
    "relaxed_sum": SLOConfig(name="relaxed_sum", mode="fixed", fixed_ttft_ms=15000.0, fixed_tpot_ms=150.0),
}

# Serverless checkpoint load latencies (s) from ServerlessLLM Fig. 6a / Section 7.2
SERVERLESS_COLD_START_S: Dict[str, Dict[str, float]] = {
    "llama2_70b": {"serverlessllm": 10.3, "safetensors": 48.0, "pytorch": 84.0},
    "opt_13b": {"serverlessllm": 2.0, "safetensors": 8.2, "pytorch": 14.0},
}

# Explicit design-calibrated synthetic WAN RTT assumptions (DESIGN.md Section 5.3)
def wan_rtt_ms(r1: str, r2: str) -> float:
    if r1 == r2:
        return 0.5  # Intra-DC same region
    c1 = REGIONS[r1].country
    c2 = REGIONS[r2].country
    if c1 == "UK" and c2 == "UK":
        return 20.0  # Intra-UK WAN RTT
    if c1 == "JP" and c2 == "JP":
        return 30.0  # Intra-JP WAN RTT
    return 200.0     # Cross-continental UK <-> Japan RTT


@dataclass
class ClusterConfig:
    """Configuration for Track A multi-region cluster P/D simulation."""

    policy: str  # "B1", "B2", "P3", "P4", "P5", "P3_overprov"
    workload: str  # "conv" or "code"
    horizon: str  # "1h" or "24h"
    seed: int = 100
    regions: Tuple[str, ...] = ("South Scotland", "London", "TEPCO")
    nodes_per_region: int = 2  # 2 colocated OR (1 prefill + 1 decode) per region
    prefill_gpu_type: str = "H100"
    decode_gpu_type: str = "H100"
    decode_power_cap: float = 0.55  # Splitwise 50-70% TDP decode cap
    rps_scale: float = 1.0
    wan_bw_gbps: float = 10.0  # Default 10 Gbps; swept in {10, 25, 100}
    wan_rtt_override_ms: Optional[float] = None  # Optional synthetic cross-region RTT override
    intra_dc_kv_bw_gbps: float = 400.0  # H100 IB / NVLink effective intra-DC fabric
    kv_mb_per_tok: float = 0.3125  # Llama-2-70B FP16 GQA-8 (~0.31 MB/tok)
    slo_name: str = "mixed_dynamollm"
    pue: float = 1.12
    mfu_sat: float = 0.45
    mfu_gamma: float = 0.70  # Ozcan et al. Eq. 1 heuristic sublinear exponent
    host_lifetime_yr: float = 4.0
    gpu_lifetime_yr: float = 4.0
    ci_mode: str = "actual"  # "actual", "neso_forecast", "lag_30m", "lag_60m", "noise_2x"
    clean_scaleout_extra_nodes: int = 0  # Extra clean nodes for P3_overprov H4 test
    nic_net_wan_power_w: float = 100.0  # 2x19W GreenSKU 100G NIC + WAN switch/optical port
    nic_net_local_power_w: float = 38.0  # 2x19W GreenSKU 100G NIC intra-DC
    coloc_decode_rate: float = 0.20  # Decode progress rate during colocated prefill stall
    # P4 hybrid router weights
    p4_w_carbon: float = 1.0
    p4_w_queue: float = 0.15
    p4_slo_margin: float = 0.85


@dataclass
class ServerlessConfig:
    """Configuration for Track B serverless LLM keep-alive simulation."""

    policy: str  # "S1", "S2", "S2b", "S3"
    region: str = "South Scotland"
    workload: str = "code"
    horizon: str = "1h"  # "1h" or "24h"
    seed: int = 100
    model_size: str = "llama2_70b"  # "llama2_70b" or "opt_13b"
    checkpoint_tier: str = "serverlessllm"  # "serverlessllm", "safetensors", "pytorch"
    gpu_type: str = "H100"
    cold_power_frac: float = 0.65  # Calibrated design assumption [0.45, 0.65, 0.85]
    idle_power_mode: str = "lace_rl"  # "lace_rl" (0.20*TDP) or "hardware_exact" (60W/100W)
    static_k_s: float = 30.0
    knative_grace_s: float = 0.0  # Optional +15 s CASA shutdown grace sensitivity
    pue: float = 1.12
    mfu_sat: float = 0.45
    mfu_gamma: float = 0.70
    host_lifetime_yr: float = 4.0
    gpu_lifetime_yr: float = 4.0
    max_workers: int = 16
    s3_beta_slo: float = 1.25  # Carbon-equivalent SLO urgency penalty weight
