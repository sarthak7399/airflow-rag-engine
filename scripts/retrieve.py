import argparse

from qdrant_client import QdrantClient

from airflow_rag_engine.embeddings.model import embed_query
from airflow_rag_engine.retrieval.retriever import retrieve


def main():
    parser = argparse.ArgumentParser(description="CLI retrieval over Airflow docs")
    parser.add_argument("query", type=str)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--url", type=str, default="http://localhost:6333")
    args = parser.parse_args()

    client = QdrantClient(url=args.url)
    results = retrieve(client, args.query, top_k=args.top_k)
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] score={r['score']:.4f} section={r['section']}")
        print(r["content"][:400])


if __name__ == "__main__":
    main()
