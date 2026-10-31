from pathlib import Path

from airflow_rag_engine.ingestion.loader import load_html_file, load_directory


def test_load_html_file(tmp_path: Path):
    html = "<html><head><title>DAGs</title></head><body><main><h1>DAGs</h1><p>A DAG is a collection.</p></main></body></html>"
    p = tmp_path / "dags.html"
    p.write_text(html, encoding="utf-8")
    doc = load_html_file(p)
    assert doc.title == "DAGs"
    assert "A DAG is a collection." in doc.content
    assert doc.document_type == "documentation"


def test_load_directory(tmp_path: Path):
    for i in range(2):
        (tmp_path / f"f{i}.html").write_text(
            f"<html><body><p>content {i}</p></body></html>", encoding="utf-8"
        )
    docs = load_directory(tmp_path)
    assert len(docs) == 2
