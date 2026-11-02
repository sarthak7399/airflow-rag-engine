from qdrant_client import QdrantClient

from airflow_rag_engine.embeddings.model import embed_query


def retrieve(
    client: QdrantClient,
    query: str,
    collection: str = "airflow_docs",
    top_k: int = 5,
    score_threshold: float | None = None,
) -> list[dict]:
    vector = embed_query(query)
    results = client.search(  # type: ignore[attr-defined]
        collection_name=collection,
        query_vector=vector,
        limit=top_k,
        score_threshold=score_threshold,
    )
    out = []
    for r in results:
        payload = r.payload or {}
        out.append(
            {
                "score": r.score,
                "chunk_id": payload.get("chunk_id"),
                "document_id": payload.get("document_id"),
                "content": payload.get("content"),
                "section": payload.get("section"),
                "section_path": payload.get("section_path"),
                "source_url": payload.get("source_url"),
            }
        )
    return out
