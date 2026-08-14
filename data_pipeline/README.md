# Data Pipeline Module 📚

## Overview

This module implements a complete ETL (Extract, Transform, Load) pipeline that scrapes book data from a public website, cleans and enriches it, and persists it to multiple storage formats (CSV and SQLite). It demonstrates data extraction, transformation, and analytical query execution.

## Files

| File | Purpose |
|------|----------|
| `data_end-to-end.py` | Main ETL pipeline script |
| `books_dataset.csv` | Cleaned book data output |
| `query_results.json` | SQL query results and analysis |
| `README.md` | Module documentation |

## Pipeline Workflow

### Phase 1: Web Scraping (Extract)

- **Target**: `https://books.toscrape.com`
- **Categories**: Travel, Mystery, Classics
- **Data Extracted**:
  - Book title
  - Price (GBP)
  - Rating (1-5 stars)
  - Stock availability
  - Category
- **Pagination**: Handles multi-page categories automatically

### Phase 2: Data Cleaning (Transform)

- **Missing Value Handling**:
  - Calculates category-wise median prices and ratings
  - Fills missing prices with category median
  - Fills missing ratings with category median
  
- **Data Enrichment**:
  - Converts prices from GBP to INR (using 1 GBP = 105.50 INR)
  - Normalizes stock availability to binary (0/1)
  - Normalizes ratings to integer scale (1-5)

- **Data Quality**:
  - Validates scraped data before processing
  - Handles malformed entries gracefully
  - Ensures consistency across records

### Phase 3: Data Loading (Load)

- **CSV Export**: Saves cleaned data to `books_dataset.csv`
- **SQLite Database**:
  - Creates normalized database schema
  - `categories` table: Stores category information
  - `books` table: Stores book details with foreign key to categories
  - Supports efficient querying and analysis

### Phase 4: Analysis

- **SQL Queries**: Executes analysis queries on the database
- **Cross-Validation**: Compares SQL results with pandas merge operations
- **Output**: Persists query results to `query_results.json`

## How to Run

```bash
python data_pipeline/data_end-to-end.py
```

This will:
1. Scrape book data from the website
2. Clean and transform the data
3. Create SQLite database tables
4. Load cleaned data into the database
5. Execute analysis queries
6. Generate output files:
   - `books_dataset.csv` - Cleaned tabular data
   - `query_results.json` - Query results and analysis

## Data Schema

### categories Table
```sql
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE
);
```

### books Table
```sql
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_inr REAL,
    rating INTEGER,
    stock INTEGER,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);
```

## Features

✅ **Automated Web Scraping** - Extracts data from dynamic website  
✅ **Data Cleaning** - Handles missing values and inconsistencies  
✅ **Currency Conversion** - Converts GBP to INR  
✅ **Database Normalization** - Creates properly structured SQLite schema  
✅ **Query Analysis** - Demonstrates SQL and pandas operations  
✅ **Reproducibility** - All outputs are deterministic and logged  

## Dependencies

Requires packages from root `requirements.txt`:
- requests (HTTP requests)
- beautifulsoup4 (HTML parsing)
- pandas (Data manipulation)
- sqlite3 (Built-in, database operations)

Install from project root:
```bash
pip install -r requirements.txt
```

## Output Files

- **books_dataset.csv**: Cleaned book records in tabular format
- **query_results.json**: JSON file containing:
  - SQL queries executed
  - Query results
  - Cross-validation comparisons with pandas

## Configuration

### Categories to Scrape
Modify the `CATS` dictionary in `data_end-to-end.py`:
```python
CATS = {
    "Travel": "...",
    "Mystery": "...",
    "Classics": "..."
}
```

### Currency Conversion Rate
Modify the `RATE` variable:
```python
RATE = 105.50  # 1 GBP to INR
```

## Technical Notes

- **Script-relative paths**: All output files are generated in the `data_pipeline/` directory
- **Pagination handling**: Automatically follows "Next" links across pages
- **Error handling**: Gracefully handles missing data and malformed HTML
- **Data validation**: Ensures all records meet quality standards before loading
- **Database isolation**: SQLite database is self-contained within the module
- **Reproducibility**: Results are deterministic and can be regenerated anytime
