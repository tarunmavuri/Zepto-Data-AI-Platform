# Zepto Data & AI Platform

A full-stack data and AI learning project combining web scraping, analytics, and a retrieval-augmented support assistant.

## Overview

This repository contains three main modules:

- Data Pipeline: extracts and transforms book dataset information from a public web source.
- Analytics: explores and models the Titanic survival dataset using machine learning pipelines.
- Support Assistant: stores policy documents in ChromaDB and answers questions using a semantic retrieval workflow.

## Project Structure

```text
Zepto Data & AI Platform/
├── README.md
├── requirements.txt
├── analytics/
│   ├── 01_eda.py
│   ├── 02.modeling.py
│   ├── README.md
│   ├── titanic.csv
│   └── titanic_cleaned.csv
├── data_pipeline/
│   ├── books_dataset.csv
│   ├── books.py
│   ├── data_end-to-end.py
│   ├── query_results.json
│   └── README.md
└── support_assistant/
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt
    ├── ingest.py
    ├── main.py
    ├── rag.py
    ├── chroma_db/
    └── docs/
```

## Module Summary

| Module | Purpose | Typical Run |
| --- | --- | --- |
| Data Pipeline | Scrape, clean, transform, and store book data | `python data_pipeline/data_end-to-end.py` |
| Analytics | EDA and ML modeling on Titanic data | `python analytics/01_eda.py` and `python analytics/02.modeling.py` |
| Support Assistant | RAG-powered chatbot with vector search | `cd support_assistant && uvicorn main:app --reload` |

## Quick Start

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 2. Install root dependencies

```bash
pip install -r requirements.txt
```

### 3. Install support assistant dependencies

```bash
cd support_assistant
pip install -r requirements.txt
cd ..
```

### 4. Run each module

```bash
# Data pipeline
python data_pipeline/data_end-to-end.py

# Analytics
python analytics/01_eda.py
python analytics/02.modeling.py

# Support assistant ingestion
cd support_assistant
python ingest.py

# Start API
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

```bash
cd support_assistant
docker build -t zepto-support-assistant .
docker run -p 8000:8000 zepto-support-assistant
```

The API is available at:

- Swagger docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

### Root requirements

- `requests`
- `beautifulsoup4`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `imbalanced-learn`
- `joblib`

### Support assistant requirements

- `fastapi`
- `uvicorn`
- `pydantic`
- `chromadb`
- `sentence-transformers`
- `langgraph`

## Documentation

- [Analytics README](analytics/README.md)
- [Data Pipeline README](data_pipeline/README.md)
- [Support Assistant README](support_assistant/README.md)

## Notes

- The support assistant uses the `all-MiniLM-L6-v2` embedding model and requires `python ingest.py` before querying the API.
- The analytics module uses a cleaned Titanic dataset and applies modeling workflows such as classification and regression.
- The data pipeline generates CSV and JSON outputs that can be reused for downstream analysis.

---


