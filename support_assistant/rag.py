import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph,START,END

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION = "zepto_policies"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

KEYWORDS = {
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours",
}

# Vector Store
encoder = SentenceTransformer(EMBEDDING_MODEL)
chroma = chromadb.PersistentClient(path=DB_PATH)
store = chroma.get_collection(COLLECTION)

# Graph State
class State(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float

# Node 1: Intent Classification
def classify_intent(state: State) -> dict:
    query = state["query"].lower()
    intent = (
        "policy_question"
        if any(word in query for word in KEYWORDS)
        else "general_question"
    )
    return {"intent": intent}

# Node 2: Retrieval + Answer
def retrieve_and_answer(state: State) -> dict:
    query_vector = encoder.encode(state["query"]).tolist()
    result = store.query(
        query_embeddings=[query_vector],
        n_results=3,
    )
    documents = result["documents"][0]
    sources = result["ids"][0]
    answer = f"Based on the retrieved context: {documents[0][:200]}"
    return {
        "answer": answer,
        "sources": sources,
        "confidence": 1.0,
    }

# Node 3: Direct Answer
def direct_answer(state: State) -> dict:
    return {
        "answer": "I can only answer questions about Zepto policies right now.",
        "sources": [],
        "confidence": 1.0,
    }

# Conditional Router
def route(state: State) -> str:
    return (
        "retrieve_and_answer"
        if state["intent"] == "policy_question"
        else "direct_answer"
    )

# Building LangGraph
graph = StateGraph(State)

graph.add_node("classify_intent", classify_intent)
graph.add_node("retrieve_and_answer", retrieve_and_answer)
graph.add_node("direct_answer", direct_answer)

graph.add_edge(START, "classify_intent")

graph.add_conditional_edges(
    "classify_intent",
    route,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

graph.add_edge("retrieve_and_answer", END)
graph.add_edge("direct_answer", END)

app = graph.compile()

# Testing the LangGraph
if __name__ == "__main__":
    tests = [
        "How much is the delivery fee?",
        "What is the capital of India?",
    ]
    for query in tests:
        print(f"\nQuery: {query}")
        print(app.invoke({"query": query}))

# Save Graph Visualization
try:
    graph_png = app.get_graph().draw_mermaid_png()
    with open("langgraph.png", "wb") as f:
        f.write(graph_png)
    print("\nGraph saved as: langgraph.png")
except Exception as e:
    print("\nCould not create graph image:", e)