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
- Follows pagination until all pages in each category are collected
- Saves the final dataset to `books_dataset.csv`

### Libraries and requirements
- `requests`
- `beautifulsoup4`
- `csv` (Python standard library)

### Saved data
''' Output file: - `books_dataset.csv` '''

