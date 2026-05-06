Place the file `10k_word_counts.csv` in `data/external/` before running 
the workflow.

- `data/external/` – source file `10k_word_counts.csv` (provided externally)
- `data/generated/` – cleaned dataset `10k_cleaned.csv` created by `prep_data.py`
- `output/` – figure and table outputs created by `run_analysis.py`

The workflow consists of three steps:

1. **`code/python/prep_data.py`** – reads `10k_word_counts.csv` from 
   `data/external/`, applies sample selection filters, and saves the 
   cleaned dataset to `data/generated/10k_cleaned.csv`.

2. **`code/python/run_analysis.py`** – reads the cleaned dataset and 
   produces the sample description table (`output/sample_by_year.csv`) 
   and Figure 1, Panel A (`output/fig1_panel_a.png`).

3. **`doc/paper.qmd`** – Quarto document that imports the outputs and 
   renders the final paper as a PDF.

To reproduce the full workflow, place `10k_word_counts.csv` in 
`data/external/` and run:

```bash
make all
```