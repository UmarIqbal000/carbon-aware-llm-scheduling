# Combined Full Package Assembly Notes

- **Output file:** `Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf`
- **Build pipeline:** `cover.tex`, `supp_banner_overlay.tex`, and `elsevier_frontmatter.tex` compiled via `pdflatex` (standard packages + Latin Modern Type 1 fonts) and assembled vector-preserving with `combined/build_package.py` (`pypdf`), because the local MiKTeX installation does not include `pdfpages.sty`.
- **Excluded artifact:** `main_anon.pdf` (double-blind JSys anonymous manuscript) is intentionally excluded.
- **Immutability:** `main.pdf` (12 pp.), `supplement.pdf` (4 pp.), `main_elsevier.pdf` (27 pp.), and `main_anon.pdf` (12 pp.) are kept untouched for individual journal submission.
- **Page map:**
  - `p. 1`: Cover and Package Contents summary (single-column, November 2026)
  - `pp. 2--13`: Complete IEEEtran two-column manuscript (`../main.pdf`, all 12 pages preserved without modification)
  - `pp. 14--17`: Online Supplementary Material (`../supplement.pdf`, Tables S1 to S7, with a non-overlapping header banner merged into the top margin of p. 14)
  - `p. 18`: Elsevier submission front-matter page embedding vector `../figures/fig1_architecture.pdf`, Graphical Abstract summary, and the 5 `<= 85`-character Research Highlights verbatim from `../highlights.md`.
- **Verification note:** `highlights.md` originally noted `(82 chars)` on two bullets whose actual character counts are 81 chars each; corrected in `highlights.md` before final packaging without altering any bullet text.
