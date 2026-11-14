"""Build tables from measured traces and explicitly attributed review labels."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def lines(name):
    return [json.loads(line) for line in (RESULTS / name).read_text(encoding="utf-8").splitlines()]


def main():
    traces = lines("traces_dev.jsonl") + lines("traces_test.jsonl")
    coherence = lines("coherence_audit.jsonl")
    grounding = lines("grounding_audit.jsonl")
    metadata = lines("metadata_audit.jsonl")
    quality = []
    for strategy in ["A", "B", "C"]:
        c = [r for r in coherence if r["strategy"] == strategy]
        g = [r for r in grounding if r["strategy"] == strategy]
        m = [r for r in metadata if r["strategy"] == strategy]
        reviewed = c + g + m
        human_confirmed = bool(reviewed) and all(r.get("human_confirmed", False) for r in reviewed)
        filters = [t for t in traces if t["strategy"] == strategy and t["question"]["filter"]]
        filter_splits = {}
        for split in ["dev", "test"]:
            group = [t for t in filters if t["question"]["split"] == split]
            passed = sum(all(all(h["metadata"][key] == value for key, value in t["question"]["filter"].items())
                             for h in t["hits"]) for t in group)
            filter_splits[split] = {"n": passed, "N": len(group)}
        quality.append({"strategy": strategy, "coherence_mean": sum(r["score"] for r in c) / len(c),
                        "coherence_n": len(c), "grounding_mean": sum(r["score"] for r in g) / len(g),
                        "grounding_distribution": {str(i): sum(r["score"] == i for r in g) for i in range(3)},
                        "metadata_correct_n": sum(r["complete_and_correct"] for r in m),
                        "metadata_N": len(m), "filter_compliance": filter_splits,
                        "qualitative_reviewer": "AI-assisted qualitative review by ChatGPT",
                        "qualitative_review_status": ("Reviewed and confirmed manually by the learner" if human_confirmed
                                                      else "Reviewed per sample with reasons and source evidence"),
                        "human_confirmed": human_confirmed,
                        "human_reviewers": sorted({r["confirmed_by"] for r in reviewed if r.get("human_confirmed") and r.get("confirmed_by")})})
    (RESULTS / "quality_summary.json").write_text(json.dumps(quality, indent=2), encoding="utf-8")
    dev = json.loads((RESULTS / "metrics_dev.json").read_text())
    test = json.loads((RESULTS / "metrics_test.json").read_text())
    with (RESULTS / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dev[0]))
        writer.writeheader()
        writer.writerows(dev + test)
    stats = {s["strategy"]: s for s in json.loads((RESULTS / "ingestion.json").read_text())}
    by_metric = {(m["strategy"], m["split"]): m for m in dev + test}
    with (ROOT / "artifacts/experiment_log.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["strategy", "chunking", "chunk_size", "overlap", "metadata", "filter", "vectorizer", "hypothesis", "dev_hit1", "dev_hit3", "test_hit1", "test_hit3", "notes"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for strategy in ["A", "B", "C"]:
            writer.writerow({"strategy": strategy, "chunking": "fixed" if strategy == "A" else "paragraph",
                "chunk_size": 500 if strategy == "A" else 1000, "overlap": 50 if strategy == "A" else 0,
                "metadata": "source,page,chapter,version,language,unit_id,character spans", "filter": strategy == "C",
                "vectorizer": "BAAI/bge-small-en-v1.5@aa8f8b060edb00e03bfdd08813a2949946c8ba55",
                "hypothesis": {"A": "Fixed windows may split evidence", "B": "Paragraph boundaries preserve context", "C": "Chapter context reduces cross-chapter retrieval"}[strategy],
                "dev_hit1": by_metric[strategy, "dev"]["hit1"], "dev_hit3": by_metric[strategy, "dev"]["hit3"],
                "test_hit1": by_metric[strategy, "test"]["hit1"], "test_hit3": by_metric[strategy, "test"]["hit3"],
                "notes": f"{stats[strategy]['chunks']} chunks; reported ingest time is warm-cache; no API charge; qualitative review method and source evidence recorded in audit files"})
    print(json.dumps(quality, indent=2))


if __name__ == "__main__":
    main()
