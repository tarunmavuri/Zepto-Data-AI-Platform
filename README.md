# Module-1: MASAI Capstone Project

This module scrapes book data from `https://books.toscrape.com` for the following categories:
- Travel
- Mystery
- Classics

The scraping script is located at `data_pipeline/data_end-to-end.py`.

### What the script does
- Sends HTTP requests to category pages
- Parses HTML with BeautifulSoup
- Extracts book title, price, star rating, availability, and category
- Cleans fields into typed columns: `price_gbp`, `rating`, `in_stock`
- Converts price into `price_inr`
- Follows pagination until all pages in each category are collected
- Saves the final dataset to `books_dataset.csv`
- Persists cleaned records into a local SQLite database `books.db`
- Writes query results to `query_results.json`

### Libraries and requirements
- `requests`
- `beautifulsoup4`
- `pandas`
- `csv`, `json`, `re`, `statistics`, `sqlite3`, `urllib.parse` (Python standard library)

## Installation

- Requires Python 3.10 or later.
- Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

- Run the end-to-end scraping pipeline:

```powershell
.\.venv\Scripts\python data_pipeline\data_end-to-end.py
```

- The script saves output to `books_dataset.csv` and a local SQLite DB `books.db`.

## Notes

- To change scraped categories, edit `data_pipeline/data_end-to-end.py`.
- The requirements file has pinned minimum versions for reproducibility: [requirements.txt](requirements.txt)

### Saved data
- `books_dataset.csv`
- `books.db`

