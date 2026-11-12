"""Unified one-command reproduction script for Revision v2 (Part D1).

Regenerates all figures, verifies raw CSVs and statistical summaries, runs simulator
validation checks, syncs README PNG assets, and writes updated consistency reports.

Usage:
    python experiments/reproduce_all.py              # Re-verify + regenerate from raw CSVs (~10 s)
    python experiments/reproduce_all.py --rerun-sims # Full SimPy 4.1.2 re-execution across seeds 100..109
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP_DIR = ROOT / "experiments"
FIG_DIR = ROOT / "figures"
PREVIEW_DIR = FIG_DIR / "_preview"
ASSETS_DIR = ROOT / "assets"


def run_step(desc: str, script: Path, args: list[str] | None = None) -> None:
    cmd = [sys.executable, str(script)] + (args or [])
    print(f"[reproduce_all] {desc}: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(ROOT), check=True)
    if res.returncode != 0:
        raise RuntimeError(f"Step failed: {desc}")


def sync_assets() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    copied = 0
    for png in sorted(PREVIEW_DIR.glob("fig*.png")):
        shutil.copy2(png, ASSETS_DIR / png.name)
        copied += 1
    print(f"[reproduce_all] Synced {copied} PNG previews to {ASSETS_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce all statistics, validation checks, and figures.")
    parser.add_argument(
        "--rerun-sims",
        action="store_true",
        help="Re-run full Track A/B SimPy suites and 24h trace-tiling ablation from scratch (long runtime).",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validate_simulator.py (use existing experiments/results/validation_benchmarks.csv).",
    )
    args = parser.parse_args()

    if args.rerun_sims:
        run_step("Full SimPy simulation suite (226 configs x 10 seeds)", EXP_DIR / "run_experiments.py")
        run_step("24h Azure trace-tiling ablation (4 modes x 3 policies x 10 seeds)", EXP_DIR / "run_tiling_ablation.py")

    run_step("Statistical aggregation & Wilcoxon analysis", EXP_DIR / "analyze_results.py")
    if not args.skip_validation:
        run_step("Literature anchor & regime-crossover validation", EXP_DIR / "validate_simulator.py")
    run_step("Generate all vector PDFs and PNG previews", FIG_DIR / "generate_figures.py")
    sync_assets()
    run_step("Consistency & numeric audit across manuscript & CSVs", EXP_DIR / "audit_consistency.py")
    print("[reproduce_all] Complete.")


if __name__ == "__main__":
    main()
