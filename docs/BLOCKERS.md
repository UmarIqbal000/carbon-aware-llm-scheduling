# Blockers Log

## 1. Turnitout-Humanizer CLI / Local Engine Unavailable (Fallback Used)
- **Date:** 2026-11-12
- **Item:** `https://github.com/AhmadHassan-BTed/Turnitout-Humanizer.git`
- **Observation:** Cloned the repository to `./cloud-paper/tools/Turnitout-Humanizer`. Upon inspecting the repository tree, `README.md`, `AGENTS.md`, and `ENTERPRISE_API.md`, the public repository contains only documentation, badges, and GitHub Pages static assets (`docs/`). There are no Python scripts, no `requirements.txt`, and no local CLI/package to install into `./cloud-paper/tools/.venv-humanizer`. The actual engine (`Turnitout-core`) is closed-source and deployed on hosted Streamlit Cloud nodes (`turnitout.streamlit.app`) and a Google Cloud Enterprise REST API (`POST /v1/humanize`) requiring a custom service URL and an `X-API-Key` provisioned directly by the developer.
- **Resolution:** Per Hard Rule 8 and Section 3.4, did not invent an API key or sign up for external services. Cloned and configured the approved fallback `https://github.com/blader/humanizer` (`SKILL.md` v4.0.0, MIT license) at `./cloud-paper/tools/blader-humanizer` and wrapped it in `.agent/skills/humanizer/SKILL.md` alongside strict LaTeX-preservation safeguards.

## 2. Paywalled Academic Publisher Portals (HTTP 403 / Abstract-Only Constraint)
- **Date:** 2026-11-11 to 2026-11-12
- **Items:**
  - `https://doi.org/10.1109/hpca68181.2026.11408586` (`roy2026lowcarb`, IEEE Xplore — HTTP 403 / access block)
  - `https://doi.org/10.1016/j.future.2026.108670` (`calavaro2026offloading`, Elsevier ScienceDirect — HTTP 403)
  - `https://doi.org/10.1145/3470496.3527408` (`gupta2022act`, ACM Digital Library — HTTP 403)
  - `https://doi.org/10.1145/3757892.3757903` (`sinha2025utilization`, ACM Digital Library — HTTP 403)
  - `https://doi.org/10.1002/spe.995` (`calheiros2011cloudsim`, Wiley Online Library — HTTP 403)
- **Observation:** Publisher PDF endpoints returned `HTTP 403` without institutional subscription cookies. Initial ACM DL requests for additional ACM papers also returned `HTTP 403`, though open arXiv/author-hosted full texts were retrieved for most of those (`42` of `47` retained studies achieved verified `full_text` access).
- **Resolution:** Per Hard Rules 4 and 8, no paywalls were bypassed. The `5` studies above remain explicitly tagged `abstract_only` in [`research/sources.csv`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/research/sources.csv) and [`research/sources_metadata.json`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/research/sources_metadata.json), and all manuscript claims referencing them are restricted strictly to verified bibliographic metadata and abstracts (also checked explicitly during pre-humanizer and post-humanizer audits).

## 3. Electricity Maps Portal (HTTP 403) & CSV Snapshot DNS Failure
- **Date:** 2026-11-11
- **Items:** `https://portal.electricitymaps.com/datasets` and `https://data.electricitymaps.com/2025-01-27/*.csv` (`US-CAL-CISO`, `DE`, `SE`, `FR`, `US-TEX-ERCO`, `IN-WE`)
- **Observation:** The Electricity Maps portal returned `HTTP 403` behind a Cloudflare challenge gate, and direct historical CSV snapshot hostnames failed DNS resolution (`Errno 11001`).
- **Resolution:** Per Hard Rule 8, did not bypass the portal gate or fabricate regional grid numbers. Replaced Electricity Maps with two verified open `CC-BY-4.0` 30-minute grid telemetry datasets documented in [`experiments/data/DATA_MANIFEST.md`](file:///c:/Users/umari/Cloud%20Computing%20Research%20Paper/cloud-paper/experiments/data/DATA_MANIFEST.md): the UK NESO Carbon Intensity API (`18` UK regions, October 2025) and Japan FY2024 TSO-Level Emission Factors (`Zenodo DOI:10.5281/zenodo.18396311`, `5` Japanese TSO grids).
