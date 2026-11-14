"""Evidence-aware retrieval metrics, separate from qualitative review labels."""
import re
from typing import Any


def canonical(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    golds = question.get("gold_evidence") or [{"source_id": question["gold_source_id"],
        "page": question["gold_page"], "quote": question["evidence_quote"]}]
    labels = [any(hit["document_id"] == gold["source_id"] and hit["page"] == gold["page"]
                  and canonical(gold["quote"]) in canonical(hit["text"]) for gold in golds)
              for hit in hits]
    return {"hit1": bool(labels and labels[0]), "hit3": any(labels),
            "rank_hits": labels, "question": question, "hits": hits}


def summarize(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for strategy, split in sorted({(t["strategy"], t["question"]["split"]) for t in traces}):
        group = [t for t in traces if t["strategy"] == strategy and t["question"]["split"] == split]
        n = len(group)
        output.append({"strategy": strategy, "split": split, "questions": n,
                       "hit1_n": sum(t["hit1"] for t in group), "hit3_n": sum(t["hit3"] for t in group),
                       "hit1": sum(t["hit1"] for t in group) / n,
                       "hit3": sum(t["hit3"] for t in group) / n})
    return output
