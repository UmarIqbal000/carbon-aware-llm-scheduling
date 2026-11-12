# Combined Package (`Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf`)

Builds one self-contained 18-page PDF combining:
1. Cover & Package Contents (`p. 1`, `cover.tex`)
2. Full Identified Manuscript (`pp. 2--13`, `../main.pdf`)
3. Online Supplementary Material Tables S1--S7 (`pp. 14--17`, `../supplement.pdf` + `supp_banner_overlay.tex`)
4. Elsevier Graphical Abstract & Research Highlights (`p. 18`, `elsevier_frontmatter.tex`)

To rebuild from `cloud-paper/combined/`:
```powershell
pdflatex -interaction=nonstopmode -halt-on-error cover.tex
pdflatex -interaction=nonstopmode -halt-on-error supp_banner_overlay.tex
pdflatex -interaction=nonstopmode -halt-on-error elsevier_frontmatter.tex
..\.venv\Scripts\python.exe build_package.py
```
