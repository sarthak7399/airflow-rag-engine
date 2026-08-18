from airflow_rag_engine.models import Chunk, Document


def test_document_creation():
    document = Document(
        id="airflow-dag",
        title="DAGs",
        content="A DAG is a collection of tasks.",
        source="apache-airflow-docs",
        source_url="https://airflow.apache.org/docs/",
        document_type="documentation",
    )

    assert document.id == "airflow-dag"
    assert document.title == "DAGs"
    assert document.metadata == {}


def test_chunk_creation():
    chunk = Chunk(
        id="airflow-dag-0001",
        document_id="airflow-dag",
        content="A DAG is a collection of tasks.",
        chunk_index=0,
        section="Core Concepts",
        section_path=["Core Concepts", "DAGs"],
    )

    assert chunk.document_id == "airflow-dag"
    assert chunk.chunk_index == 0
    assert chunk.section == "Core Concepts"
    assert chunk.section_path == ["Core Concepts", "DAGs"]


def test_chunk_preserves_document_lineage():
    chunk = Chunk(
        id="chunk-001",
        document_id="document-001",
        content="Example content",
        chunk_index=0,
    )

    assert chunk.document_id == "document-001"
