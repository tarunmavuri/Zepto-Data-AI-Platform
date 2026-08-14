# Zepto Support Assistant 🤖

An intelligent Retrieval-Augmented Generation (RAG) based customer support chatbot for Zepto, built with FastAPI, ChromaDB, and LangGraph.

## Overview

The Zepto Support Assistant is an AI-powered customer support system that:
- Ingests policy documents and stores them as semantic embeddings in ChromaDB
- Classifies user queries by intent (policy questions vs general inquiries)
- Retrieves relevant policy documents using semantic similarity search
- Generates accurate, context-grounded answers based on company policies
- Provides confidence scores and source attribution for transparency

## Architecture

### System Components

#### 1. Document Ingestion (`ingest.py`)

**Responsibility**: Load and embed policy documents

- Reads policy documents from `docs/` directory
- Uses `all-MiniLM-L6-v2` transformer model for embedding generation
- Creates semantic embeddings (384-dimensional vectors)
- Stores embeddings in ChromaDB with metadata (source, content)
- Supports incremental ingestion of new documents

#### 2. RAG Pipeline (`rag.py`)

**Responsibility**: Orchestrate the retrieval-augmented generation workflow

The pipeline consists of three nodes:

- **Intent Classification Node**
  - Categorizes user queries (policy question, general question, complaint, etc.)
  - Routes queries appropriately based on intent
  - Improves response relevance

- **Retrieval Node**
  - Searches ChromaDB for semantically relevant policy documents
  - Ranks results by relevance score
  - Returns top-k documents with similarity scores
  - Includes source metadata for attribution

- **Answer Generation Node**
  - Combines retrieved policy context with user query
  - Generates human-readable answers grounded in company policies
  - Provides confidence scores based on retrieval relevance
  - Cites sources for transparency

**Orchestration**: Uses LangGraph for robust workflow management

#### 3. API Server (`main.py`)

**Responsibility**: Expose RAG system via REST API

- FastAPI application with automatic API documentation
- Pydantic models for type-safe request/response handling
- Single main endpoint: `POST /ask`
- Interactive API docs available at `/docs` and `/redoc`

### Data Flow

```
User Query
    ↓
[Intent Classification] → Categorize intent
    ↓
[Semantic Retrieval] → Search ChromaDB for relevant policies
    ↓
[Answer Generation] → Generate context-grounded response
    ↓
Structured Response (answer, sources, confidence)
```

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- 2GB+ disk space for vector database and models

### Installation Steps

1. Navigate to the support_assistant directory:
```bash
cd support_assistant
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Service

### Start the API Server

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`

### Access the API

**Interactive API Documentation**:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Health Check**:
```bash
curl http://localhost:8000/
```

Response: `{"message": "Zepto Support Assistant API is running"}`

### Making Queries

**Using cURL**:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'
```

**Using Python**:
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"query": "What is your return policy?"}
)
print(response.json())
```

**Response Format**:
```json
{
  "answer": "Based on our return policy...",
  "sources": ["policy_doc_1.txt", "policy_doc_2.txt"],
  "confidence": 0.92
}
```

## API Endpoints

### GET `/`
Health check endpoint

**Response**:
```json
{"message": "Zepto Support Assistant API is running"}
```

### POST `/ask`
Query the support assistant

**Request**:
```json
{
  "query": "What is your delivery time?"
}
```

**Response**:
```json
{
  "answer": "Our delivery time is typically 30 minutes...",
  "sources": ["delivery_policy.txt"],
  "confidence": 0.87
}
```

## File Structure

```
support_assistant/
├── main.py                 # FastAPI server
├── rag.py                  # RAG pipeline with LangGraph
├── ingest.py              # Document ingestion script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container configuration
├── README.md              # This file
├── chroma_db/             # ChromaDB vector store
│   ├── chroma.sqlite3     # Vector database
│   └── [collection_dirs]/ # Embedded documents
└── docs/                  # Policy documents
    ├── doc_1.txt
    ├── doc_2.txt
    ├── doc_3.txt
    ├── doc_4.txt
    ├── doc_5.txt
    ├── doc_6.txt
    ├── doc_7.txt
    └── doc_8.txt
```

## Document Management

### Adding New Policy Documents

1. Place policy documents in the `docs/` folder (supports `.txt` format)
2. Run the ingestion script:
```bash
python ingest.py
```
3. The system will:
   - Read all documents
   - Generate embeddings
   - Update ChromaDB
   - Make documents available for retrieval

### Supported Document Formats
- Plain text (`.txt`)
- Can be extended to support PDF, Markdown, etc.

## Dependencies

Key packages (see `requirements.txt` for complete list):

- **fastapi**: Web framework for API
- **uvicorn**: ASGI server
- **langgraph**: Workflow orchestration
- **chromadb**: Vector database
- **sentence-transformers**: Embedding generation
- **pydantic**: Data validation
- **requests**: HTTP client
- **beautifulsoup4**: HTML parsing (if needed)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Docker Deployment

### Build Docker Image

```bash
docker build -t zepto-support-assistant .
```

### Run Docker Container

```bash
docker run -p 8000:8000 zepto-support-assistant
```

The API will be available at `http://localhost:8000`

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
