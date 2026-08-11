from fastapi import FastAPI
from pydantic import BaseModel
from rag import app as rag_app

app = FastAPI(
    title="Zepto Support Assistant",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float

@app.get("/")
def home():
    return {"message": "Zepto Support Assistant API is running"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    result = rag_app.invoke({
        "query": request.query
    })

    return {
        "answer": result["answer"],
        "sources": result.get("sources", []),
        "confidence": result.get("confidence", 1.0)
    }