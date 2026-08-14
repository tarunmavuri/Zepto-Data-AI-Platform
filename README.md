# Zepto Data & AI Platform

AI/ML platform with web scraping, data analytics, and RAG-based support chatbot.

## 📋 Modules

| Module | Purpose | Command |
|--------|---------|---------|
| **Data Pipeline** 📊 | Web scraping & ETL | `python data_pipeline/data_end-to-end.py` |
| **Analytics** 📈 | Titanic ML analysis | `python analytics/01_eda.py` / `02.modeling.py` |
| **Support Assistant** 🤖 | RAG chatbot | `uvicorn support_assistant/main:app --reload` |

## 🚀 Quick Start

```bash
# Install root dependencies
pip install -r requirements.txt

# Install support assistant dependencies
cd support_assistant && pip install -r requirements.txt

# Run modules
python data_pipeline/data_end-to-end.py       # Scrapes books, outputs CSV + JSON
python analytics/01_eda.py                    # EDA + cleaning
python analytics/02.modeling.py               # Model training
python support_assistant/ingest.py            # Ingest policies to ChromaDB
uvicorn support_assistant/main:app --reload   # Start API at http://localhost:8000/docs
```

## 📁 Project Structure

```
├── requirements.txt
├── analytics/                    # Titanic dataset: 01_eda.py, 02.modeling.py
├── data_pipeline/               # Book scraping: data_end-to-end.py
└── support_assistant/           # RAG chatbot: main.py, rag.py, ingest.py
    ├── chroma_db/              # Vector database
    ├── docs/                   # Policy documents
    └── requirements.txt
```

## 📦 Dependencies

**Root:** `requests`, `beautifulsoup4`, `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`  
**Support Assistant:** `fastapi`, `uvicorn`, `chromadb`, `sentence-transformers`, `langgraph`, `pydantic`

## 📤 Output Files

- `data_pipeline/books_dataset.csv` — Cleaned books
- `data_pipeline/query_results.json` — SQL query results
- `analytics/titanic_cleaned.csv` — Cleaned Titanic data
- `best_titanic_pipeline.pkl` — Trained model
- `support_assistant/chroma_db/` — Vector embeddings

## 💡 Key Notes

- **Data Pipeline:** Converts GBP→INR, fills missing values with medians
- **Analytics:** Uses SMOTE for imbalance, scikit-learn pipelines, cross-validation
- **Support Assistant:** Uses `all-MiniLM-L6-v2` embeddings, run `ingest.py` before API
- **Docker:** `docker build -t zepto-support-assistant support_assistant/` → `docker run -p 8000:8000 zepto-support-assistant`

## 📖 Documentation

- [Data Pipeline](data_pipeline/README.md) — ETL workflow, database schema
- [Analytics](analytics/README.md) — EDA, modeling details
- [Support Assistant](support_assistant/README.md) — API, RAG architecture

## 🤝 Contributing

1. Keep modules independent
2. Update module READMEs
3. Follow existing code style
4. Test thoroughly

---

**Last Updated:** 2026-08-14 | **Python:** 3.8+ | **Status:** Active
