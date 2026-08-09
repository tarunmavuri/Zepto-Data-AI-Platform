#DOCUMENT INGESTION + EMBEDDINGS + CHROMADB

import os
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_FOLDER = os.path.join(BASE_DIR, "docs")
DB_FOLDER = os.path.join(BASE_DIR, "chroma_db")

COLLECTION_NAME = "zepto_policies"
MODEL_NAME = "all-MiniLM-L6-v2"
# Required embedding model from the assignment
MODEL_NAME = "all-MiniLM-L6-v2"

# 2. Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("Embedding model loaded.")

# 3. Load documents
documents = []
document_ids = []
metadata = []

for filename in sorted(os.listdir(DOCS_FOLDER)):
    if filename.endswith(".txt"):
        filepath = os.path.join(DOCS_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read().strip()
        documents.append(text)
        # doc_01.txt -> doc_01
        document_ids.append(filename[:-4])
        metadata.append({
            "source": filename
        })

print(f"Documents loaded: {len(documents)}")

# 4. Chunk documents
chunks = documents
chunk_ids = document_ids

# 5. Generate embeddings
print("Generating embeddings...")

embeddings = model.encode(
    chunks,
    show_progress_bar=True
).tolist()

print(f"Embeddings created: {len(embeddings)}")

# 6. Create / connect to ChromaDB
client = chromadb.PersistentClient(
    path=DB_FOLDER
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)

# 7. Store documents and embeddings
collection.upsert(
    ids=chunk_ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadata
)

# 8. Verify
print("\n======================================")
print("INGESTION COMPLETED")
print("======================================")
print(f"Documents : {len(documents)}")
print(f"Chunks    : {collection.count()}")
print(f"Database  : {DB_FOLDER}")
print(f"Collection: {COLLECTION_NAME}")
print("======================================")
