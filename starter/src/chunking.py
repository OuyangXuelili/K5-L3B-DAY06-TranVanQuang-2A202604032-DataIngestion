"""Two chunking strategies with stable IDs and source character offsets."""
import hashlib
import re
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > overlap >= 0")
    chunks = []
    start = 0
    while start < len(page.text):
        end = min(start + size, len(page.text))
        chunks.append(make_chunk(page, start, end, f"fixed:{size}:{overlap}"))
        if end == len(page.text):
            break
        start = end - overlap
    return chunks


def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    if max_size <= 0:
        raise ValueError("max_size must be positive")
    spans = [(m.start(), m.end()) for m in re.finditer(r"[^\n]+(?:\n(?!\n)[^\n]+)*", page.text)]
    chunks = []
    start = end = None
    for left, right in spans:
        if start is not None and right - start > max_size:
            chunks.append(make_chunk(page, start, end, f"paragraph:{max_size}"))
            start = end = None
        while right - left > max_size:
            split = page.text.rfind(" ", left, left + max_size)
            if split <= left + max_size // 2:
                split = left + max_size
            chunks.append(make_chunk(page, left, split, f"paragraph:{max_size}"))
            left = split
            while left < right and page.text[left].isspace():
                left += 1
        if left < right:
            if start is None:
                start = left
            end = right
    if start is not None:
        chunks.append(make_chunk(page, start, end, f"paragraph:{max_size}"))
    return chunks


def make_chunk(page: DocumentPage, start: int, end: int, config: str) -> Chunk:
    text = page.text[start:end]
    identity = f"{page.document_id}:{page.page}:{start}:{end}:{config}:{text}"
    return Chunk(hashlib.sha256(identity.encode()).hexdigest(), page.document_id, page.source,
                 page.page, text, {**page.metadata, "start_char": start, "end_char": end})
