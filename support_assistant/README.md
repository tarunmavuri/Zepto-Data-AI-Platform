# Zepto Support Assistant

A Retrieval-Augmented Generation (RAG) based customer support assistant for Zepto, built with FastAPI, ChromaDB, and LangGraph.

## Overview

This project implements an intelligent support chatbot that:
- Ingests policy documents and stores them as embeddings in ChromaDB
- Classifies user queries by intent (policy questions vs general questions)
- Retrieves relevant documents using semantic search
- Provides accurate answers grounded in company policies

## Architecture

### Components

1. **Document Ingestion (`ingest.py`)**
   - Loads policy documents from the `docs/` folder
   - Generates embeddings using `all-MiniLM-L6-v2` transformer model
   - Stores embeddings in ChromaDB for persistent vector storage

2. **RAG Pipeline (`rag.py`)**
   - Intent classification node: Categorizes user queries
   - Retrieval node: Searches ChromaDB for relevant policies
   - Answer generation node: Combines retrieved context with user query
   - Uses LangGraph for workflow orchestration

3. **API Server**
   - FastAPI application for serving the support assistant
   - RESTful endpoints for query processing
   - Pydantic models for request/response validation

## Setup

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Installation

1. Navigate to the support_assistant directory:
```bash
cd support_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Document Ingestion

Before running the server, ingest the policy documents:

```bash
python ingest.py
```

This will:
- Read all `.txt` files from the `docs/` folder
- Generate embeddings using the sentence transformer
- Store them in ChromaDB at `chroma_db/`

## Running the Application

### Start the API Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `POST /query` - Submit a support query
  - Request: `{"query": "string"}`
  - Response: `{"answer": "string", "confidence": float, "sources": ["list of doc sources"]}`

- `GET /docs` - OpenAPI documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## File Structure

```
support_assistant/
├── ingest.py           # Document ingestion and embedding generation
├── rag.py             # RAG pipeline with LangGraph
├── main.py            # FastAPI application (when created)
├── requirements.txt    # Project dependencies
├── README.md          # This file
├── chroma_db/         # ChromaDB persistent storage
│   └── chroma.sqlite3
└── docs/              # Policy documents
    ├── doc_1.txt
    ├── doc_2.txt
    └── ...
```

## Configuration

Key configuration parameters in `rag.py`:

```python
COLLECTION = "zepto_policies"          # ChromaDB collection name
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence transformer model
KEYWORDS = {"delivery", "return", ...} # Intent classification keywords
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI web server for FastAPI
- **Pydantic**: Data validation and settings management
- **ChromaDB**: Vector database for embeddings
- **Sentence-Transformers**: Pre-trained models for generating embeddings
- **LangGraph**: Graph-based workflow orchestration

## Development

### Testing the RAG Pipeline

```python
from rag import app

# Test with a sample query
response = app.invoke({
    "query": "What is your return policy?"
})
print(response)
```

### Docker Support

Build and run using Docker:

```bash
docker build -t zepto-support-assistant .
docker run -p 8000:8000 zepto-support-assistant
```

## Performance Considerations

- Embeddings are cached in ChromaDB for fast retrieval
- Semantic search is performed on stored embeddings rather than raw text
- Intent classification uses keyword matching for efficiency
- Consider using GPU for embedding generation with larger document sets

## Troubleshooting

**Issue**: "Collection not found" error
- **Solution**: Run `ingest.py` first to create the ChromaDB collection

**Issue**: Slow embedding generation
- **Solution**: Use GPU acceleration or reduce document chunk size

**Issue**: Low confidence answers
- **Solution**: Add more relevant documents to the `docs/` folder and re-run `ingest.py`

## Future Enhancements

- Multi-turn conversation support
- Fine-tuned language model for answer generation
- Advanced query rewriting for better retrieval
- Response caching for common queries
- Analytics and feedback loop for continuous improvement

## License

Internal Zepto Project
