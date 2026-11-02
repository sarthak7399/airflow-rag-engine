import re
from collections.abc import Iterable

from airflow_rag_engine.models import Chunk


def _split_sections(content: str) -> list[tuple[list[str], str]]:
    """Split markdown into (section_path, text) blocks by headings."""
    lines = content.splitlines()
    sections: list[tuple[list[str], str]] = []
    path: list[str] = []
    buf: list[str] = []

    def flush():
        text = "\n".join(buf).strip()
        if text:
            sections.append((list(path), text))
        buf.clear()

    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            level = len(m.group(1))
            title = m.group(2).strip()
            # maintain path by heading level
            while len(path) >= level:
                path.pop()
            path.append(title)
        else:
            buf.append(line)
    flush()
    if not sections:
        sections.append(([], content.strip()))
    return [(p, t) for p, t in sections]


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        # try to break on paragraph/whitespace
        if end < n:
            cut = text.rfind("\n\n", start, end)
            if cut == -1 or cut <= start:
                cut = text.rfind(" ", start, end)
            if cut != -1 and cut > start:
                end = cut
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


def chunk_document(
    document,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    idx = 0
    for section_path, section_text in _split_sections(document.content):
        section = section_path[-1] if section_path else None
        for piece in _chunk_text(section_text, chunk_size, overlap):
            chunks.append(
                Chunk(
                    id=f"{document.id}-{idx:04d}",
                    document_id=document.id,
                    content=piece,
                    chunk_index=idx,
                    section=section,
                    section_path=section_path,
                    metadata={"source_url": document.source_url},
                )
            )
            idx += 1
    return chunks


def chunk_documents(documents: Iterable, **kwargs) -> list[Chunk]:
    out: list[Chunk] = []
    for doc in documents:
        out.extend(chunk_document(doc, **kwargs))
    return out
