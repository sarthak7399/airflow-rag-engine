from pathlib import Path

import pandas as pd

from airflow_rag_engine.ingestion.persist import chunks_to_dataframe, save_parquet, load_chunks_parquet
from airflow_rag_engine.models import Chunk


def test_persist_chunks_roundtrip(tmp_path: Path):
    chunk = Chunk(id="c1", document_id="d1", content="hi", chunk_index=0)
    df = chunks_to_dataframe([chunk])
    path = tmp_path / "chunks.parquet"
    save_parquet(df, path)
    loaded = load_chunks_parquet(path)
    assert len(loaded) == 1
    assert loaded[0].id == "c1"
    assert isinstance(pd.read_parquet(path), pd.DataFrame)
