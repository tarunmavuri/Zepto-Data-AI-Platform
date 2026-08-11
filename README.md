# Zepto Data & AI Platform

A comprehensive AI/ML platform featuring web data extraction, analytics, and a RAG-based intelligent support assistant.

## Project Modules

### 1. Book Scraping and Data Pipeline
- Entry point: `books.py`
- Pipeline script: `data_pipeline/data_end-to-end.py`
- Scrapes book listings from `https://books.toscrape.com`
- Includes categories: Travel, Mystery, Classics
- Cleans and enriches the data, then saves it to CSV, SQLite, and JSON
- See `data_pipeline/README.md` for detailed documentation

### 2. Titanic Analytics & Modeling
- Entry point: `analytics/01_eda.py` (EDA) and `analytics/02.modeling.py` (Modeling)
- Loads the local Titanic dataset from `analytics/titanic.csv`
- Computes dataset shape, info, summary statistics, and missing-value percentages
- Applies basic cleaning for `age`, `embarked`, `embark_town`, and `deck`
- Builds and compares classification models, handles imbalance with SMOTE, and evaluates fare regression models
- See `analytics/README.md` for module-specific details

### 3. Zepto Support Assistant (RAG System)
- RAG-based intelligent customer support system powered by FastAPI
- Components:
  - **Document Ingestion** (`ingest.py`): Loads policies, generates embeddings with `all-MiniLM-L6-v2`
  - **RAG Pipeline** (`rag.py`): Intent classification, semantic retrieval, and answer generation using LangGraph
  - **Vector Store**: ChromaDB for persistent embedding storage
- Run server: `uvicorn main:app --reload` (from `support_assistant/` directory)
- API endpoints for querying policies with confidence scores and source tracking
- See `support_assistant/README.md` for setup and API details

## Installation

Install dependencies from the project root:

```bash
pip install -r requirements.txt
```

For support assistant dependencies (FastAPI, Uvicorn, etc.), install from the support_assistant directory:

```bash
cd support_assistant
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

### Titanic modeling module

```bash
python analytics/02.modeling.py
```

### Zepto Support Assistant

1. Navigate to the support_assistant directory:
```bash
cd support_assistant
```

2. Ingest policy documents into ChromaDB:
```bash
python ingest.py
```

3. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Access the API at `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Output Files

- `data_pipeline/books_dataset.csv` — cleaned book dataset
- `data_pipeline/books.db` — SQLite database of categories and books
- `data_pipeline/query_results.json` — saved SQL query output
- `analytics/titanic_cleaned.csv` — cleaned Titanic dataset (generated if the script writes it)
- `best_titanic_pipeline.pkl` — saved Titanic model pipeline from `analytics/02.modeling.py`
- `support_assistant/chroma_db/` — ChromaDB vector database with policy embeddings
- `support_assistant/chroma_db/chroma.sqlite3` — SQLite backend for ChromaDB

## Requirements

### Core Dependencies
- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `imbalanced-learn`
- `joblib`

### Support Assistant Dependencies
- `fastapi>=0.104.0`
- `uvicorn>=0.24.0`
- `pydantic>=2.0.0`
- `chromadb>=0.4.0`
- `sentence-transformers>=2.2.0`
- `langgraph>=0.0.1`

## Notes

- **Data Pipeline**: The book pipeline imputes missing price and rating values using medians. Book dataset price values are converted from GBP to INR.
- **Analytics Module**: The Titanic analytics module is self-contained and uses the local Titanic dataset in `analytics/titanic.csv`.
- **Support Assistant**: The RAG system uses ChromaDB for persistent vector storage and `all-MiniLM-L6-v2` for semantic embeddings. Make sure to run `ingest.py` before starting the API server to populate the vector database with policy documents.
- **Performance**: For optimal performance with the support assistant, consider using GPU acceleration for embedding generation with large document sets.

## Documentation

- `data_pipeline/README.md` — Book scraping and pipeline module
- `analytics/README.md` — Titanic analytics module
- `support_assistant/README.md` — RAG-based support assistant system with API documentation
