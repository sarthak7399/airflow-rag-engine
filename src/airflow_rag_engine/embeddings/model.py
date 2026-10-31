from functools import lru_cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str], batch_size: int = 32, normalize: bool = True) -> list[list[float]]:
    model = get_model()
    vectors = model.encode(texts, batch_size=batch_size, normalize_embeddings=normalize, show_progress_bar=False)
    return [v.tolist() for v in vectors]


def embed_query(query: str) -> list[float]:
    return embed_texts([query])[0]
