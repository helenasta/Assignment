UV := uv
UV_SYNC := $(UV) sync --managed-python --locked
PYTHON := .venv/bin/python
QUARTO := quarto
QUARTO_PYTHON := $(abspath $(PYTHON))
GENERATED := data/generated/10k_cleaned.csv
RESULTS := output/fig1_panel_a.png output/sample_by_year.csv
PAPER_BASENAME := paper.pdf
PAPER := output/$(PAPER_BASENAME)
SOURCE := doc/paper.qmd

.PHONY: all clean

all: $(PAPER)

$(PYTHON): pyproject.toml uv.lock .python-version
	$(UV_SYNC)

$(GENERATED): code/python/prep_data.py $(PYTHON)
	mkdir -p data/generated
	$(PYTHON) $

$(RESULTS): code/python/run_analysis.py $(GENERATED) $(PYTHON)
	mkdir -p output
	$(PYTHON) $

$(PAPER): $(SOURCE) $(RESULTS) $(PYTHON)
	rm -rf .quarto doc/.quarto
	cd doc && QUARTO_PYTHON=$(QUARTO_PYTHON) $(QUARTO) render paper.qmd --to pdf --output $(PAPER_BASENAME)
	cp doc/$(PAPER_BASENAME) output/$(PAPER_BASENAME)
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md doc/paper.fff doc/paper.ttt

clean:
	rm -rf .quarto doc/.quarto
	rm -f $(GENERATED) $(RESULTS) $(PAPER)
	rm -f doc/paper.tex doc/paper.log doc/paper.aux doc/paper.out doc/paper.knit.md doc/paper.fff doc/paper.ttt
