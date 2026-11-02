from airflow_rag_engine.ingestion.chunker import _split_sections, chunk_document
from airflow_rag_engine.models import Document


def test_split_sections_by_heading():
    content = "# Intro\nHello\n## Details\nWorld"
    secs = _split_sections(content)
    assert len(secs) == 2
    assert secs[0][0] == ["Intro"]
    assert secs[1][0] == ["Intro", "Details"]


def test_chunk_document_creates_chunks():
    doc = Document(
        id="d1",
        title="T",
        content="A " * 500,
        source="s",
        source_url="u",
        document_type="documentation",
    )
    chunks = chunk_document(doc, chunk_size=100, overlap=10)
    assert len(chunks) > 1
    assert all(c.document_id == "d1" for c in chunks)
    assert chunks[0].chunk_index == 0


def test_chunk_preserves_section_path():
    doc = Document(
        id="d2",
        title="T",
        content="# Sec\n" + ("word " * 200),
        source="s",
        source_url="u",
        document_type="documentation",
    )
    chunks = chunk_document(doc, chunk_size=50, overlap=5)
    assert all(c.section == "Sec" for c in chunks)
    assert all(c.section_path == ["Sec"] for c in chunks)
