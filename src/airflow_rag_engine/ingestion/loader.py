import hashlib
import re
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from airflow_rag_engine.models import Document


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "document"


def _doc_id(source: str) -> str:
    return hashlib.sha1(source.encode()).hexdigest()[:12]


def _clean_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _extract_title(soup: BeautifulSoup, fallback: str) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return fallback


def _html_to_markdown(soup: BeautifulSoup) -> str:
    # Remove nav, footer, scripts, styles
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.body or soup
    html = str(main)
    text = md(html, heading_style="ATX", strip=["a"])
    return _clean_text(text)


def load_html_file(path: Path | str, source: str = "apache-airflow-docs") -> Document:
    path = Path(path)
    html = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")
    title = _extract_title(soup, path.stem)
    content = _html_to_markdown(soup)
    rel = path.as_posix()
    return Document(
        id=_doc_id(rel),
        title=title,
        content=content,
        source=source,
        source_url=rel,
        document_type=_infer_type(rel),
        metadata={"path": rel},
    )


def load_html_url(url: str, source: str = "apache-airflow-docs") -> Document:
    resp = httpx.get(url, follow_redirects=True, timeout=30.0)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    title = _extract_title(soup, url)
    content = _html_to_markdown(soup)
    return Document(
        id=_doc_id(url),
        title=title,
        content=content,
        source=source,
        source_url=url,
        document_type=_infer_type(url),
        metadata={"url": url},
    )


def load_directory(directory: Path | str, glob: str = "**/*.html", source: str = "apache-airflow-docs") -> list[Document]:
    directory = Path(directory)
    docs: list[Document] = []
    for path in sorted(directory.glob(glob)):
        if path.is_file():
            docs.append(load_html_file(path, source=source))
    return docs


def _infer_type(ref: str) -> str:
    lowered = ref.lower()
    if "tutorial" in lowered:
        return "tutorial"
    if "reference" in lowered or "api" in lowered:
        return "reference"
    if "how-to" in lowered or "howto" in lowered:
        return "how-to"
    return "documentation"
