# Prime cadences: build the paper, the arXiv bundle, and run the audits.
PAPER   := prime-cadences
PY      ?= python3
LATEXMK ?= latexmk

.PHONY: all pdf arxiv audit figures clean distclean

all: pdf

pdf: paper/$(PAPER).pdf

paper/$(PAPER).pdf: paper/$(PAPER).tex paper/references.bib $(wildcard paper/figures/*.pdf)
	cd paper && $(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(PAPER).tex

# arXiv bundle: source, pre-built .bbl, figures (arXiv does not run BibTeX on .bib alone).
arxiv: pdf
	mkdir -p arxiv
	tar -czf arxiv/$(PAPER)-arxiv.tar.gz -C paper $(PAPER).tex $(PAPER).bbl references.bib figures
	@echo "wrote arxiv/$(PAPER)-arxiv.tar.gz"

# Independent audits (each prints PASS/FAIL lines and a total).
audit:
	cd code && $(PY) math_audit.py
	cd code/deep && $(PY) audit.py
	cd code/eisenstein2 && $(PY) audit.py
	cd code/geometry && $(PY) audit.py
	cd code/open_q && $(PY) open_audit.py
	cd code/xcheck && $(PY) audit_xcheck.py

# Regenerate the vector figures in paper/figures/.
figures:
	cd code/figures && $(PY) figs.py && $(PY) figs_geometry.py

clean:
	cd paper && $(LATEXMK) -c $(PAPER).tex
	find code -name __pycache__ -prune -exec rm -rf {} +

distclean: clean
	cd paper && $(LATEXMK) -C $(PAPER).tex
	rm -rf arxiv
