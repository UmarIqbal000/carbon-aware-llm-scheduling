# Multi-target LaTeX build for:
#   - IEEE Transactions on Sustainable Computing (main.pdf)
#   - Elsevier FGCS / SUSCOM (main_elsevier.pdf)
#   - Double-blind anonymized JSys submission (main_anon.pdf)
#   - Supplementary material (supplement.pdf)

PDFLATEX = pdflatex -interaction=nonstopmode -halt-on-error
BIBTEX   = bibtex

SECTIONS := $(wildcard sections/*.tex)
FIGURES  := $(wildcard figures/*.pdf)
BIB      := references.bib

.PHONY: all ieee elsevier anon supplement check clean distclean

all: ieee elsevier anon supplement

ieee: main.pdf
elsevier: main_elsevier.pdf
anon: main_anon.pdf
supplement: supplement.pdf

main.pdf: main.tex $(SECTIONS) $(FIGURES) $(BIB)
	$(PDFLATEX) main
	$(BIBTEX) main
	$(PDFLATEX) main
	$(PDFLATEX) main

main_elsevier.pdf: main_elsevier.tex $(SECTIONS) $(FIGURES) $(BIB)
	$(PDFLATEX) main_elsevier
	$(BIBTEX) main_elsevier
	$(PDFLATEX) main_elsevier
	$(PDFLATEX) main_elsevier

main_anon.pdf: main_anon.tex $(SECTIONS) $(FIGURES) $(BIB)
	$(PDFLATEX) main_anon
	$(BIBTEX) main_anon
	$(PDFLATEX) main_anon
	$(PDFLATEX) main_anon

supplement.pdf: main_supplement.tex $(FIGURES) $(BIB)
	$(PDFLATEX) -jobname=supplement main_supplement
	$(BIBTEX) supplement || true
	$(PDFLATEX) -jobname=supplement main_supplement
	$(PDFLATEX) -jobname=supplement main_supplement

PYTHON ?= .venv/Scripts/python.exe

check: all
	for f in sections/*.tex; do $(PYTHON) tools/latex_prose_guard.py --check "$$f" || exit 1; done

clean:
	rm -f *.aux *.bbl *.blg *.fdb_latexmk *.fls *.log *.out *.spl *.toc Notes.bib

distclean: clean
	rm -f main.pdf main_elsevier.pdf main_anon.pdf supplement.pdf
