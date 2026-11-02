import json
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]

from airflow_rag_engine.models import Chunk, Document


def _serialize(obj):
    if isinstance(obj, (dict, list)):
        return json.dumps(obj)
    return obj


def _deserialize_metadata(df: pd.DataFrame) -> pd.DataFrame:
    if "metadata" in df.columns:
        df["metadata"] = df["metadata"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    return df


def documents_to_dataframe(documents: list[Document]) -> pd.DataFrame:
    rows = []
    for d in documents:
        r = d.model_dump()
        r["metadata"] = json.dumps(r["metadata"])
        rows.append(r)
    return pd.DataFrame(rows)


def chunks_to_dataframe(chunks: list[Chunk]) -> pd.DataFrame:
    rows = []
    for c in chunks:
        r = c.model_dump()
        r["metadata"] = json.dumps(r["metadata"])
        r["section_path"] = json.dumps(r["section_path"])
        rows.append(r)
    return pd.DataFrame(rows)


def save_parquet(df: pd.DataFrame, path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def load_documents_parquet(path: Path | str) -> list[Document]:
    df = _deserialize_metadata(pd.read_parquet(path))
    return [Document(**row) for row in df.to_dict(orient="records")]


def load_chunks_parquet(path: Path | str) -> list[Chunk]:
    df = pd.read_parquet(path)
    if "metadata" in df.columns:
        df["metadata"] = df["metadata"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    if "section_path" in df.columns:
        df["section_path"] = df["section_path"].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    return [Chunk(**row) for row in df.to_dict(orient="records")]
