"""Load physical PDF pages or normalized JSONL source units."""
import json
import re
import unicodedata
from pathlib import Path
from .models import DocumentPage


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    from pypdf import PdfReader
    pages = []
    for number, page in enumerate(PdfReader(path).pages, 1):
        text = normalize_text(page.extract_text() or "")
        if not text:
            raise ValueError(f"No extractable text in {path}, physical page {number}")
        pages.append(DocumentPage(document_id, source, number, text))
    return pages


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ").replace("\u200b", "")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(line.rstrip() for line in text.split("\n"))).strip()


def load_jsonl(path: Path) -> list[DocumentPage]:
    pages = []
    seen = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        record["text"] = normalize_text(record["text"])
        page = DocumentPage(**record)
        key = (page.document_id, page.page)
        if key in seen or len(page.text) < 1500:
            raise ValueError(f"Duplicate or short source unit: {key}")
        seen.add(key)
        pages.append(page)
    if len(pages) < 30:
        raise ValueError("At least 30 source units are required")
    return pages
