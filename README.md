# Zepto Data & AI Platform

A multi-module project for web data extraction, cleaning, storage, and analytics.

## Project Modules

### 1. Book Scraping and Data Pipeline
- Entry point: `books.py`
- Pipeline script: `data_pipeline/data_end-to-end.py`
- Scrapes book listings from `https://books.toscrape.com`
- Includes categories: Travel, Mystery, Classics
- Cleans and enriches the data, then saves it to CSV, SQLite, and JSON

### 2. Titanic Analytics
- Entry point: `analytics/01_eda.py`
- Loads the local Titanic dataset from `analytics/titanic.csv`
- Computes dataset shape, info, summary statistics, and missing-value percentages
- Applies basic cleaning for `age`, `embarked`, `embark_town`, and `deck`
- See `analytics/README.md` for module-specific details

## Installation

Install dependencies from the project root:

```bash
pip install -r requirements.txt
```

## Run

### Book scraping pipeline

```bash
python books.py
```

This executes `data_pipeline/data_end-to-end.py` and writes output to:
- `data_pipeline/books_dataset.csv`
- `data_pipeline/books.db`
- `data_pipeline/query_results.json`

### Titanic analytics module

```bash
python analytics/01_eda.py
```

## Output Files

- `data_pipeline/books_dataset.csv` — cleaned book dataset
- `data_pipeline/books.db` — SQLite database of categories and books
- `data_pipeline/query_results.json` — saved SQL query output
- `analytics/titanic_cleaned.csv` — cleaned Titanic dataset (generated if the script writes it)

## Requirements

The project depends on:

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`

## Notes

- The book pipeline imputes missing price and rating values using medians.
- The book dataset price values are converted from GBP to INR.
- The analytics module is self-contained and uses the local Titanic dataset in `analytics/titanic.csv`.

## Documentation

- `data_pipeline/README.md` — Book scraping and pipeline module
- `analytics/README.md` — Titanic analytics module
