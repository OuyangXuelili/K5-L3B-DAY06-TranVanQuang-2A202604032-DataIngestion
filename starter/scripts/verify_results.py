"""Check saved evidence, persistence, idempotence, and stale-chunk removal."""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "starter"))
from src.chunking import by_paragraph, fixed_size
from src.evaluation import canonical, evaluate_query, summarize
from src.ingestion import load_jsonl
from src.models import Chunk
from src.run import validate_inputs
from src.store import QdrantStore


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main():
    pages = load_jsonl(ROOT / "data/pages.jsonl")
    questions = read_lines(ROOT / "benchmark/questions.jsonl")
    plan = json.loads((ROOT / "benchmark/plan.json").read_text())
    validate_inputs(pages, questions, plan)
    selection = json.loads((ROOT / "results/selection.json").read_text())
    for path, expected_hash in selection["input_hashes"].items():
        relative = path.replace("\\", "/")
        source = ROOT / relative
        if relative == "starter/src/run.py":
            source = ROOT / "artifacts/implementation_at_test/run.py"
        assert hashlib.sha256(source.read_bytes()).hexdigest() == expected_hash
    lookup = {(p.document_id, p.page): p for p in pages}
    checks = []
    checks.append("First-test corpus and implementation fingerprints match the saved snapshot")
    for strategy in ["A", "B", "C"]:
        chunks = [Chunk(**c) for c in read_lines(ROOT / f"results/chunks_{strategy}.jsonl")]
        for chunk in chunks:
            page = lookup[(chunk.document_id, chunk.page)]
            assert chunk.text == page.text[chunk.metadata["start_char"]:chunk.metadata["end_char"]]
        for page in pages:
            covered = set()
            for chunk in [c for c in chunks if c.document_id == page.document_id and c.page == page.page]:
                covered.update(range(chunk.metadata["start_char"], chunk.metadata["end_char"]))
            assert all(char.isspace() or i in covered for i, char in enumerate(page.text))
        checks.append(f"{strategy}: source spans and full non-whitespace coverage")
    b = read_lines(ROOT / "results/chunks_B.jsonl")
    c = read_lines(ROOT / "results/chunks_C.jsonl")
    assert b == c
    checks.append("B and C use exactly the same chunks and metadata")

    traces = read_lines(ROOT / "results/traces_dev.jsonl") + read_lines(ROOT / "results/traces_test.jsonl")
    assert len(traces) == 60
    for trace in traces:
        question = trace["question"]
        assert len(trace["hits"]) == 3
        expected = evaluate_query(question, trace["hits"])
        assert expected["hit1"] == trace["hit1"] and expected["hit3"] == trace["hit3"]
        if trace["applied_filter"]:
            assert trace["strategy"] == "C"
            assert all(all(h["metadata"][k] == v for k, v in trace["applied_filter"].items()) for h in trace["hits"])
    for split in ["dev", "test"]:
        saved = json.loads((ROOT / f"results/metrics_{split}.json").read_text())
        assert saved == summarize([t for t in traces if t["question"]["split"] == split])
    checks.append("60 traces, top-3, gold evidence scores, filters and aggregates verified")

    first = Chunk(**b[0])
    second = Chunk(**b[1])
    vector_path = ROOT / ".cache/vectors" / (hashlib.sha256(f"{plan['model']}:False:{first.text}".encode()).hexdigest() + ".npy")
    vector = np.load(vector_path).tolist()
    with tempfile.TemporaryDirectory(prefix="day6-store-check-") as temp:
        store = QdrantStore(Path(temp), 384)
        try:
            store.upsert("storage_check", [first, second], [vector, vector])
            store.upsert("storage_check", [first, second], [vector, vector])
            assert store.count("storage_check") == 2
            store.upsert("storage_check", [first], [vector])
            assert store.count("storage_check") == 1
            try:
                store.upsert("storage_check", [first], [[1.0]])
                raise AssertionError("A wrong vector dimension was accepted")
            except ValueError:
                assert store.count("storage_check") == 1
        finally:
            store.close()
        reopened = QdrantStore(Path(temp), 384)
        try:
            assert reopened.count("storage_check") == 1
            assert reopened.search("storage_check", vector, filters={"chapter": first.metadata["chapter"]})[0]["chunk_id"] == first.chunk_id
            assert reopened.search("storage_check", vector, filters={"chapter": "absent"}) == []
        finally:
            reopened.close()
    checks.append("Persistent reopen, duplicate-free upsert, obsolete deletion and invalid-vector rejection")
    for args in [(0, 0), (10, 10), (10, -1)]:
        try:
            fixed_size(pages[0], *args)
            raise AssertionError("Invalid chunk parameters accepted")
        except ValueError:
            pass
    approval = json.loads((ROOT / "results/approval.json").read_text(encoding="utf-8"))
    manual_review = approval.get("manual_review", {})
    review_rows = []
    for filename, expected_count in [("coherence_audit.jsonl", 30), ("grounding_audit.jsonl", 15),
                                     ("metadata_audit.jsonl", 45)]:
        rows = read_lines(ROOT / "results" / filename)
        assert len(rows) == expected_count, filename
        review_rows.extend(rows)
    human_confirmed = (manual_review.get("confirmed") is True
                       and bool(manual_review.get("confirmed_by"))
                       and all(row.get("human_confirmed") is True
                               and row.get("confirmed_by") == manual_review["confirmed_by"]
                               for row in review_rows))
    checks.append("90 audit records counted; human review status read from learner confirmation and per-record attestations")
    report = {"passed": checks, "source_units": len(pages), "questions": len(questions),
              "trace_count": len(traces), "human_audit_confirmed": human_confirmed,
              "human_audit_confirmed_by": manual_review["confirmed_by"] if human_confirmed else None,
              "human_review_record": "results/approval.json"}
    (ROOT / "results/verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
