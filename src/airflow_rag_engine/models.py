from typing import Any

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Normalized source document."""

    id: str
    title: str
    content: str

    # Track where the document came from.
    source: str
    source_url: str

    # Helps distinguish docs, guides, references, etc.
    document_type: str

    # Allows source-specific metadata without changing the schema.
    metadata: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    """Retrievable unit derived from a document."""

    id: str

    # Preserves document → chunk lineage.
    document_id: str

    content: str

    # Preserves the original chunk ordering.
    chunk_index: int

    # Keeps the document's structural context for better retrieval.
    section: str | None = None
    section_path: list[str] = Field(default_factory=list)

    # Useful for tracing a chunk back to its source content.
    start_char: int | None = None
    end_char: int | None = None

    # Allows chunk-specific metadata without changing the schema.
    metadata: dict[str, Any] = Field(default_factory=dict)
