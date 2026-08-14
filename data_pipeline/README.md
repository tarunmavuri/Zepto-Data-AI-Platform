# Data Pipeline Module

## Overview

This module scrapes book information from a public website, cleans the extracted dataset, and stores the output locally for further analysis. It demonstrates a simplified ETL workflow using Python and common data-science libraries.

## Files

- `data_end-to-end.py` — full scraping and transformation pipeline
- `books.py` — supporting book-related processing logic
- `books_dataset.csv` — exported cleaned dataset
- `query_results.json` — saved analysis output
- `README.md` — module documentation

## Pipeline Flow

### 1. Extraction

The pipeline fetches book data from the Books to Scrape website and collects fields such as:

- title
- category
- price
- rating
- stock availability

### 2. Transformation

During transformation, the script:

- normalizes scraped values
- handles missing or malformed fields
- converts currency values from GBP to INR
- cleans inconsistent data into a usable tabular structure

### 3. Loading

The transformed data is saved as:

- CSV file in the `data_pipeline` folder
- JSON output for query results and quick inspection

## Run

From the project root:

```bash
python data_pipeline/data_end-to-end.py
```

## Dependencies

The module depends on the root requirements, including:

- requests
- beautifulsoup4
- pandas
- numpy

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Output Files

- `data_pipeline/books_dataset.csv` — final cleaned and structured dataset
- `data_pipeline/query_results.json` — business/query results saved as JSON

## Notes

- The script is designed to be run from the repository root or from within the `data_pipeline` folder, as long as relative paths are preserved.
- The conversion logic and cleaning steps are simple but effective examples of ETL automation and data preparation.
- This module is independent from the model-training and chatbot modules in the project.
