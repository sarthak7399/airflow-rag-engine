from fastapi import FastAPI
from pydantic import BaseModel

from qdrant_client import QdrantClient

from airflow_rag_engine.generation.llm import generate
from airflow_rag_engine.generation.prompt import build_prompt
from airflow_rag_engine.retrieval.retriever import retrieve

app = FastAPI(title="Airflow RAG Engine")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    contexts: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    client = QdrantClient(url="http://localhost:6333")
    results = retrieve(client, req.query, top_k=req.top_k)
    contexts = [r["content"] for r in results if r["content"]]
    prompt = build_prompt(req.query, contexts)
    answer = generate(prompt)
    return QueryResponse(answer=answer, contexts=contexts)
