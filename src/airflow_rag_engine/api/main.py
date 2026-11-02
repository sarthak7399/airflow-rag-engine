import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from qdrant_client import QdrantClient

from airflow_rag_engine.generation.llm import generate
from airflow_rag_engine.generation.prompt import build_prompt
from airflow_rag_engine.retrieval.retriever import retrieve

STATIC_DIR = Path(__file__).parent / "static"
ROOT = Path(__file__).resolve().parents[3]

app = FastAPI(title="Airflow RAG Engine")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

STATUS: dict[str, Any] = {"step": "idle", "running": False, "message": "Ready", "log": ""}


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    answer: str
    contexts: list[str]


def _run(cmd: list[str], step: str):
    global STATUS
    STATUS = {"step": step, "running": True, "message": f"Running {step}...", "log": ""}
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=600, check=False)
        STATUS = {
            "step": step,
            "running": False,
            "message": f"{step} {'done' if proc.returncode == 0 else 'failed'}",
            "log": (proc.stdout + "\n" + proc.stderr).strip()[-4000:],
        }
    except Exception as e:  # noqa: BLE001
        STATUS = {"step": step, "running": False, "message": f"{step} error", "log": str(e)}


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/status")
def status():
    return STATUS


@app.post("/run/download")
def run_download(bg: BackgroundTasks):
    bg.add_task(_run, [sys.executable, "scripts/download_docs.py"], "download")
    return {"started": "download"}


@app.post("/run/ingest")
def run_ingest(bg: BackgroundTasks):
    bg.add_task(_run, [sys.executable, "scripts/ingest.py", "--docs-dir", "data/raw/airflow-docs"], "ingest")
    return {"started": "ingest"}


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    client = QdrantClient(url="http://localhost:6333")
    results = retrieve(client, req.query, top_k=req.top_k)
    contexts = [r["content"] for r in results if r["content"]]
    prompt = build_prompt(req.query, contexts)
    answer = generate(prompt)
    return QueryResponse(answer=answer, contexts=contexts)
