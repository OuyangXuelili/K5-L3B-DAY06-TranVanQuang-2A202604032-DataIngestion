"""Download a licensed tutorial snapshot and retain reproducible source units."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "starter"))
from src.ingestion import normalize_text

CHAPTERS = ["controlflow", "datastructures", "modules", "inputoutput", "errors", "classes"]


def main():
    raw_dir = ROOT / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    pages, manifest = [], []
    for chapter in CHAPTERS:
        url = f"https://docs.python.org/3.13/tutorial/{chapter}.html"
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        html = response.content
        (raw_dir / f"{chapter}.html").write_bytes(html)
        soup = BeautifulSoup(html, "html.parser")
        body = soup.select_one('div.body')
        if body is None:
            raise ValueError(f"Missing main content: {url}")
        for anchor in body.select('a.headerlink'):
            anchor.decompose()
        blocks = []
        for element in body.find_all(["h1", "h2", "h3", "h4", "p", "pre", "li"]):
            if element.find_parent(["pre", "li"]) is not None:
                continue
            text = element.get_text("", strip=False) if element.name == "pre" else element.get_text(" ", strip=True)
            text = normalize_text(text)
            if text:
                blocks.append(text)
        units, pending = [], []
        for block in blocks:
            pending.append(block)
            if len("\n\n".join(pending)) >= 2500:
                units.append("\n\n".join(pending))
                pending = []
        if pending:
            tail = "\n\n".join(pending)
            if len(tail) < 1500 and units:
                units[-1] += "\n\n" + tail
            else:
                units.append(tail)
        if any(len(unit) < 1500 for unit in units):
            raise ValueError(f"A source unit is below 1500 characters: {chapter}")
        entries = []
        for number, text in enumerate(units, 1):
            unit_id = f"{chapter}-{number:03}"
            page = {"document_id": f"python313-{chapter}", "source": url,
                    "page": number, "text": text,
                    "metadata": {"chapter": chapter, "version": "3.13", "language": "en",
                                 "unit_id": unit_id}}
            pages.append(page)
            entries.append({"page": number, "unit_id": unit_id, "characters": len(text),
                            "start": text[:100], "end": text[-100:],
                            "sha256": hashlib.sha256(text.encode()).hexdigest()})
        manifest.append({"source_id": f"python313-{chapter}",
                         "title": soup.title.get_text(strip=True), "source_path_or_url": url,
                         "snapshot_path": f"data/raw/{chapter}.html",
                         "accessed_at": datetime.now(timezone.utc).isoformat(),
                         "license_or_permission": "PSF License Version 2; code examples also 0BSD",
                         "license_url": "https://docs.python.org/3.13/license.html",
                         "raw_sha256": hashlib.sha256(html).hexdigest(), "units": entries})
        print(f"{chapter}: {len(units)} units, {sum(map(len, units))} characters", flush=True)
    if len(pages) < 30:
        raise ValueError("Corpus has fewer than 30 valid source units")
    (ROOT / "data" / "pages.jsonl").write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in pages), encoding="utf-8")
    metadata = {"page_rule": "Sequential content units grouped at paragraph boundaries to >=2500 characters; merge final tail below 1500 into previous unit. Excludes navigation, footer and table of contents outside main content. Each unit retains full boundaries and SHA-256.",
                "content_unit_count": len(pages), "sources": manifest}
    (ROOT / "data" / "manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    license_response = requests.get("https://docs.python.org/3.13/license.html", timeout=60)
    license_response.raise_for_status()
    license_body = BeautifulSoup(license_response.content, "html.parser").select_one('div.body')
    (ROOT / "data" / "LICENSE-PYTHON.txt").write_text(license_body.get_text("\n", strip=True), encoding="utf-8")
    print(f"Corpus prepared: {len(pages)} source units", flush=True)


if __name__ == "__main__":
    main()
