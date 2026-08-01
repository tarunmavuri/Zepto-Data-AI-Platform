# Data Pipeline Module

This module contains the scraping, cleaning, and SQLite database loading steps for the book dataset.

## Files
- `data_end-to-end.py`: main pipeline script
- `books_dataset.csv`: cleaned CSV output
- `books.db`: SQLite database file
- `query_results.json`: SQL query text and output

## What it does
1. Scrapes `https://books.toscrape.com` for Travel, Mystery, and Classics categories
2. Cleans scraped rows and fills missing price/rating values using medians
3. Converts GBP prices to INR using a fixed conversion rate
4. Saves cleaned data to `books_dataset.csv`
5. Creates SQLite tables `categories` and `books`
6. Loads cleaned data into SQLite
7. Executes saved SQL queries and writes results to `query_results.json`
8. Compares SQL join output with a `pandas.merge` result

## Requirements
```bash
pip install -r ../requirements.txt
```

## Run
```bash
python data_pipeline/data_end-to-end.py
```

## Design notes
- Script-relative output paths keep generated files inside `data_pipeline/`.
- Missing numeric values are imputed with category-wide medians.
- Stock availability is stored as integer `0/1` and ratings as integer values.
- Database schema separates categories into `categories(category_id, category_name)` and books into `books(...)`.
- Query outputs are persisted to JSON for reproducible results analysis.
