# Zepto Support Assistant

A lightweight retrieval-augmented support assistant built with FastAPI, ChromaDB, sentence-transformers, and LangGraph.

## Overview

This module ingests policy documents from the `docs/` folder, converts them into vector embeddings, stores them in ChromaDB, and exposes a simple API for asking questions based on those documents.

## Files

- `main.py` — FastAPI application and API routes
- `rag.py` — LangGraph-based retrieval workflow
- `ingest.py` — document ingestion and embedding generation
- `Dockerfile` — container build for deployment
- `requirements.txt` — Python dependencies
- `docs/` — policy source documents
- `chroma_db/` — local vector database

## Local Setup

From the project root:

```bash
cd support_assistant
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

## Ingest Documents

```bash
python ingest.py
```

This loads all `.txt` files in the `docs/` folder and stores embeddings in the local ChromaDB collection.

## Start the API

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Example Request

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query":"What is the return policy?"}'
```

Response shape:

```json
{
  "answer": "Based on the retrieved context...",
  "sources": ["doc_1.txt"],
  "confidence": 1.0
}
```

## Docker

```bash
docker build -t zepto-support-assistant .
docker run -p 8000:8000 zepto-support-assistant
```

## Dependencies

The module requires the following packages:

- fastapi
- uvicorn
- pydantic
- chromadb
- sentence-transformers
- langgraph

These are pinned in `support_assistant/requirements.txt`.

## Notes

- The embedding model currently used is `all-MiniLM-L6-v2`.
- The assistant is designed for policy-based Q&A, not for general-purpose open-ended conversation.
- The app expects the Chroma collection to exist before queries are made; this is created automatically by `ingest.py`.
- The API route is `POST /ask` and accepts a JSON body with a `query` field.

## Configuration

### Embedding Model
Default: `all-MiniLM-L6-v2` (384-dimensional vectors)

To change, modify in `rag.py`:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('model-name')
```

### Retrieval Parameters
Adjust in `rag.py`:
- Number of top-k results
- Similarity threshold
- Search metadata filters

## Performance Tuning

- **First Query**: May be slower as models are loaded (~30-60 seconds)
- **Subsequent Queries**: Fast inference (~1-2 seconds)
- **Batch Processing**: Supported via multiple requests
- **Memory Usage**: ~2GB RAM for model + database

## Troubleshooting

### Port Already in Use
```bash
uvicorn main:app --reload --port 8001
```

### ChromaDB Connection Error
- Ensure `chroma_db/` directory exists and has write permissions
- Clear database: `rm -rf chroma_db/` and re-ingest documents

### Out of Memory
- Reduce batch size for ingestion
- Use smaller embedding model (but with reduced quality)

### No Documents Found
- Run `python ingest.py` to populate the vector database
- Check that `docs/` folder contains policy files

## Development Notes

- **Extensibility**: Easily add more intent types by modifying the classification node
- **Scalability**: ChromaDB can handle millions of documents
- **Accuracy**: RAG approach ensures answers are grounded in actual policies
- **Monitoring**: Add logging and metrics to track query patterns
- **Testing**: Include unit tests for individual components

## Future Enhancements

- 🔄 Multi-turn conversation support
- 📊 Analytics dashboard for query patterns
- 🌐 Multi-language support
- 🎤 Voice input/output capabilities
- 🔐 User authentication and role-based access
- 📈 Continuous learning from user feedback
- ⚡ Redis caching for frequently asked queries

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
