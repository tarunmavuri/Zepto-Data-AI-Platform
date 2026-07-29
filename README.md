# Module-1: MASAI Capstone Project

## Task 1: Book Data Extraction

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

### Libraries and requirements
- `requests`
- `beautifulsoup4`
- `csv`, `re`, `statistics`, `sqlite3` (Python standard library)

### Saved data
- `books_dataset.csv`
- `books.db`

