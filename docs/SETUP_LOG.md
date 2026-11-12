# Setup Log

**Timestamp:** 2026-11-12
**Workspace:** `c:\Users\umari\Cloud Computing Research Paper\cloud-paper`

## 1. LaTeX Toolchain Verification
- **Installed Distribution:** MiKTeX 25.4 (`pdfTeX 3.141592653-2.6-1.40.27`, `BibTeX 0.99d`, `Biber`, `Latexmk 4.87`).
- **Perl Dependency Fix:** `latexmk.exe` requires Perl on `PATH`. Git for Windows provides Perl at `C:\Program Files\Git\usr\bin\perl.exe`. Prepending `C:\Program Files\Git\usr\bin` to `PATH` enables `latexmk -pdf`.
- **Package Repository Issue & Resolution:** MiKTeX's default cloud API (`api2.miktex.org`) failed with `Couldn't connect to server` (`schannel` renegotiation failure). Disabled on-the-fly auto-install (`[MPM]AutoInstall=0`) so `pdflatex` never hangs, and installed required packages directly from the official CTAN MiKTeX `.tar.lzma` archive (`https://mirrors.ctan.org/systems/win32/miktex/tm/packages/`) into `C:\Users\umari\AppData\Local\MiKTeX` followed by `initexmf --update-fndb`:
  `booktabs`, `cite`, `siunitx`, `microtype`, `psnfss`, `multirow`, `sttools`, `translator`, `enumitem`, `kvsetkeys`, `kvdefinekeys`, `kvoptions`, `ltxcmds`, `infwarerr`, `pdfescape`, `hycolor`, `letltxmacro`, `auxhook`, `bitset`, `intcalc`, `etexcmds`, `uniquecounter`, `refcount`, `gettitlestring`, `rerunfilecheck`, `stringenc`, `bigintcalc`, `hobsub`, `float`, `caption`, `array`, `tools`, `pgf`, `amsmath`, `babel`, `url`, `nameref`, `pdflscape`, `geometry`, `fancyhdr`, `l3kernel`, `l3packages`.
- **Compilation Smoke Test:** Verified `latexmk -pdf -interaction=nonstopmode test.tex` with `IEEEtran.cls`, `IEEEtran.bst`, `booktabs`, `siunitx`, `cite`, `hyperref`, `tikz`, `microtype`, and `bibtex` completed with 0 errors and produced a 1-page PDF (`68251 bytes`).
- **Template Selection:** Default `\documentclass[journal]{IEEEtran}` verified (will update only if Agent 1 selects a venue requiring a different template).

## 2. Python Environment
- **System Python:** Python `3.13.14`
- **Virtual Environment:** `./cloud-paper/.venv`
- **Installed Packages:** `matplotlib==3.11.2`, `numpy==2.5.4`, `pandas==3.1.1`, `scipy==1.18.1`, `seaborn==0.13.2`, `requests==2.34.2`, `bibtexparser==2.1.0`, `pybtex==0.26.1`, `pillow==13.0.0`, `simpy==4.1.2`, `pypdf==7.0.1`.
- **API Connectivity Test:** Confirmed HTTP 200 responses from OpenAlex (`api.openalex.org`), Crossref (`api.crossref.org`), and arXiv (`export.arxiv.org`). Semantic Scholar unauthenticated search returned HTTP 429 rate limit.

## 3. Folder Structure
Created:
- `./cloud-paper/` (`main.tex` & `references.bib` to be authored in Stage 5, `sections/`, `figures/`, `experiments/`, `research/notes/`, `tools/`, `BLOCKERS.md`, `SETUP_LOG.md`)
- Workspace skills under `./.agent/skills/`: `humanizer/SKILL.md`, `latex-paper/SKILL.md`, `citation-verifier/SKILL.md`.

## 4. Humanizer Setup (`Turnitout-Humanizer` Inspection & Fallback)
- **Cloned:** `https://github.com/AhmadHassan-BTed/Turnitout-Humanizer.git` to `./cloud-paper/tools/Turnitout-Humanizer`.
- **Code & Documentation Audit (prior to running anything):**
  - Inspected root directory and `docs/`, `README.md`, `AGENTS.md`, `ENTERPRISE_API.md`, `USER_MANUAL.md`, `PRIVACY.md`, `TODO.md`.
  - **What it is:** The public repository contains documentation, HTML/CSS/JS GitHub Pages assets, badges, and REST API specs for a deterministic rule-based rewriting service (`Turnitout-core`). There is **no `requirements.txt`, no Python engine code, and no local CLI** inside this public repository.
  - **How it is invoked (per docs):** Either interactively via hosted Streamlit Cloud web mirrors (`turnitout.streamlit.app`, `turnitout1..7.streamlit.app`) or programmatically via an Enterprise REST API (`POST /v1/humanize` on Google Cloud Run) expecting JSON `{"text": "..."}` and returning JSON `{"humanized_text": "..."}`.
  - **Credentials / Key Requirement:** The REST API requires a custom service URL and an `X-API-Key` provisioned directly by the developer (`ahmadhassan.bted@gmail.com`). No key was supplied by the author.
  - **Security & Policy Decision:** Did not invent keys, register accounts, or upload draft text to external hosted apps. Recorded in `./cloud-paper/BLOCKERS.md`.
- **Fallback Configured (`blader/humanizer`):**
  - Cloned `https://github.com/blader/humanizer.git` (`SKILL.md` v4.0.0, MIT license) to `./cloud-paper/tools/blader-humanizer`.
  - Wrapped in `.agent/skills/humanizer/SKILL.md` paired with a local LaTeX invariant guard script (`./cloud-paper/tools/latex_prose_guard.py`) that scans prose for AI writing patterns outside math/commands and verifies exact multiset invariance of `\cite{}`, `\ref{}`, `\label{}`, inline/display math, and numeric tokens.
- **Sample LaTeX Preservation Test:**
  - Tested `latex_prose_guard.py` on a sample paragraph containing `\cite{patterson2021}`, `$E = P \cdot t \cdot \text{CI}$`, `23.4\%`, and `120`. Confirmed AI clichés (`today's fast-paced`, `landscape`, `plays a pivotal role`) were flagged and removed while `cites`, `math_inline`, and `numbers` passed invariant verification with zero alteration.
