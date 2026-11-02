import argparse
from pathlib import Path

from airflow_rag_engine.ingestion.chunker import chunk_documents
from airflow_rag_engine.ingestion.loader import load_directory
from airflow_rag_engine.ingestion.persist import (
    chunks_to_dataframe,
    documents_to_dataframe,
    save_parquet,
)
from airflow_rag_engine.vectorstore.qdrant import get_client, index_chunks


def main():
    parser = argparse.ArgumentParser(description="Ingest Airflow docs")
    parser.add_argument("--docs-dir", type=str, required=True)
    parser.add_argument("--out-dir", type=str, default="data/processed")
    parser.add_argument("--qdrant-url", type=str, default="http://localhost:6333")
    args = parser.parse_args()

    docs = load_directory(args.docs_dir)
    chunks = chunk_documents(docs)
    out = Path(args.out_dir)
    save_parquet(documents_to_dataframe(docs), out / "documents.parquet")
    save_parquet(chunks_to_dataframe(chunks), out / "chunks.parquet")

    client = get_client(args.qdrant_url)
    index_chunks(client, chunks)
    print(f"Ingested {len(docs)} docs, {len(chunks)} chunks.")


if __name__ == "__main__":
    main()
