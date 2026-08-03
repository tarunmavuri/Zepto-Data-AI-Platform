# Zepto Data & AI Platform

A multi-module project for web data extraction, cleaning, storage, and analytics.

## Project Modules

### 1. Book Scraping and Data Pipeline
- Location: `data_pipeline/data_end-to-end.py`
- Scrapes book data from `https://books.toscrape.com`
- Categories included: Travel, Mystery, Classics
- Cleans extracted data and stores results as CSV, SQLite, and JSON

### 2. Titanic Analytics
- Location: `analytics/01_eda.py`
- Loads the local Titanic dataset from `analytics/titanic.csv`
- Prints dataset shape, info, summary statistics, and missing-value percentages
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

This executes `data_pipeline/data-end-to-end.py` and writes output to:
- `data_pipeline/books_dataset.csv`
- `data_pipeline/books.db`
- `data_pipeline/query_results.json`

### Titanic analytics module

```bash
python analytics/01_eda.py
```

## Requirements

The project depends on:

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- Python standard library modules: `csv`, `json`, `re`, `statistics`, `sqlite3`, `urllib.parse`

## Notes

- The book pipeline imputes missing prices and ratings with median values.
- Prices are converted from GBP to INR for the book dataset.
- The analytics module uses a local Titanic dataset stored in `analytics/titanic.csv`.
- Dependencies are pinned in `requirements.txt` for reproducibility.

## Documentation

- `data_pipeline/README.md` — Book scraping and pipeline module
- `analytics/README.md` — Titanic analytics module
