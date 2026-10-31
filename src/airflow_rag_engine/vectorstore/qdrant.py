from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from airflow_rag_engine.embeddings.model import embed_texts

COLLECTION = "airflow_docs"
DIM = 384


def get_client(url: str = "http://localhost:6333") -> QdrantClient:
    return QdrantClient(url=url)


def ensure_collection(client: QdrantClient, collection: str = COLLECTION) -> None:
    if not client.collection_exists(collection):
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=DIM, distance=Distance.COSINE),
        )


def index_chunks(client: QdrantClient, chunks, collection: str = COLLECTION, batch: int = 64) -> None:
    ensure_collection(client, collection)
    for i in range(0, len(chunks), batch):
        batch_chunks = chunks[i : i + batch]
        vectors = embed_texts([c.content for c in batch_chunks])
        points = [
            PointStruct(
                id=abs(hash(c.id)) % (2**63),
                vector=v,
                payload={
                    "chunk_id": c.id,
                    "document_id": c.document_id,
                    "content": c.content,
                    "section": c.section,
                    "section_path": c.section_path,
                    "source_url": c.metadata.get("source_url"),
                },
            )
            for c, v in zip(batch_chunks, vectors)
        ]
        client.upsert(collection_name=collection, points=points)
