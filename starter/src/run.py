"""Reproducible local ingestion, dev selection, and locked test evaluation."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import sys
import time
import traceback
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .chunking import by_paragraph, fixed_size
from .embeddings import MyEmbedder
from .evaluation import canonical, evaluate_query, summarize
from .ingestion import load_jsonl
from .models import Chunk
from .store import QdrantStore

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def validate_inputs(pages, questions, plan):
    content = (ROOT / "benchmark/questions.jsonl").read_bytes()
    if hashlib.sha256(content).hexdigest() != plan["benchmark_sha256"]:
        raise ValueError("Benchmark changed after freezing")
    lookup = {(p.document_id, p.page): p for p in pages}
    if len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Question IDs must be unique")
    for split, minimum in [("dev", 15), ("test", 5)]:
        if sum(q["split"] == split for q in questions) < minimum:
            raise ValueError(f"Insufficient {split} questions")
    for question in questions:
        page = lookup[(question["gold_source_id"], question["gold_page"])]
        if canonical(question["evidence_quote"]) not in canonical(page.text):
            raise ValueError(f"Evidence absent from source: {question['id']}")
        if question["filter"]:
            for key, value in question["filter"].items():
                if page.metadata[key] != value or value not in re.sub(r"\W", "", question["question"].lower()):
                    raise ValueError("Filters must be given explicitly in the question")


def ingest(pages, plan, embedder, store):
    stats = []
    positions = json.loads((ROOT / "benchmark/coherence_positions.json").read_text())
    samples = []
    for strategy, config in plan["strategies"].items():
        start = time.perf_counter()
        if config["chunking"] == "fixed":
            chunks = [c for p in pages for c in fixed_size(p, config["size"], config["overlap"])]
        else:
            chunks = [c for p in pages for c in by_paragraph(p, config["max_size"])]
        before = embedder.model_calls
        vectors = embedder.embed_documents([c.text for c in chunks])
        store.upsert(strategy, chunks, vectors)
        elapsed = time.perf_counter() - start
        first_count = store.count(strategy)
        store.upsert(strategy, chunks, vectors)
        second_count = store.count(strategy)
        if first_count != len(chunks) or second_count != first_count:
            raise ValueError("Idempotent re-ingestion failed")
        write_jsonl(RESULTS / f"chunks_{strategy}.jsonl", [asdict(c) for c in chunks])
        for i, position in enumerate(positions, 1):
            covering = [c for c in chunks if c.document_id == position["document_id"]
                        and c.page == position["page"] and c.metadata["start_char"] <= position["char_offset"]
                        < c.metadata["end_char"]]
            if not covering:
                raise ValueError("Audit position not covered")
            chosen = min(covering, key=lambda c: c.metadata["start_char"])
            samples.append({"sample_id": f"s{i:02}", "strategy": strategy,
                            "position": position, "chunk": asdict(chosen),
                            "score": None, "reason": "", "reviewer": None})
        stat = {"strategy": strategy, "chunks": len(chunks),
                "min_chars": min(len(c.text) for c in chunks),
                "max_chars": max(len(c.text) for c in chunks),
                "mean_chars": sum(len(c.text) for c in chunks) / len(chunks),
                "total_chars": sum(len(c.text) for c in chunks),
                "ingest_seconds": elapsed, "model_vectors_computed": embedder.model_calls - before,
                "reingest_count_before": first_count, "reingest_count_after": second_count,
                "api_cost_usd": 0.0}
        stats.append(stat)
        print(f"Ingest {strategy}: {len(chunks)} chunks, {elapsed:.2f}s", flush=True)
    write_json(RESULTS / "ingestion.json", stats)
    write_jsonl(RESULTS / "coherence_samples.jsonl", samples)


def benchmark(split, questions, plan, embedder, store):
    traces = []
    for question in [q for q in questions if q["split"] == split]:
        vector = embedder.embed_query(question["question"])
        for strategy, config in plan["strategies"].items():
            applied = question["filter"] if config["filter"] else None
            start = time.perf_counter()
            hits = store.search(strategy, vector, filters=applied)
            trace = evaluate_query(question, hits)
            trace.update({"strategy": strategy, "applied_filter": applied,
                          "retrieval_seconds": time.perf_counter() - start})
            traces.append(trace)
    write_jsonl(RESULTS / f"traces_{split}.jsonl", traces)
    metrics = summarize(traces)
    write_json(RESULTS / f"metrics_{split}.json", metrics)
    return traces, metrics


def prepare_audits(traces, pages):
    grounding, metadata = [], []
    lookup = {(p.document_id, p.page): p for p in pages}
    for trace in traces:
        grounding.append({"strategy": trace["strategy"], "question_id": trace["question"]["id"],
                          "question": trace["question"]["question"],
                          "expected_answer": trace["question"]["expected_answer"],
                          "hits": trace["hits"], "score": None, "reason": "", "reviewer": None})
        for rank, hit in enumerate(trace["hits"], 1):
            page = lookup[(hit["document_id"], hit["page"])]
            start, end = hit["metadata"]["start_char"], hit["metadata"]["end_char"]
            valid = (hit["source"] == page.source and hit["text"] == page.text[start:end]
                     and all(hit["metadata"].get(k) == page.metadata[k] for k in ["chapter", "version", "language", "unit_id"]))
            metadata.append({"strategy": trace["strategy"], "question_id": trace["question"]["id"],
                             "rank": rank, "chunk_id": hit["chunk_id"], "source": hit["source"],
                             "page": hit["page"], "chapter": hit["metadata"]["chapter"],
                             "complete_and_correct": valid, "validation": "source snapshot and exact character span",
                             "human_confirmed": False})
    write_jsonl(RESULTS / "grounding_samples.jsonl", grounding)
    write_jsonl(RESULTS / "metadata_audit.jsonl", metadata)


def main():
    global RESULTS
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["ingest", "dev", "test", "all"], default="all")
    parser.add_argument("--output-dir", default="results", help="Fresh output directory relative to repository root")
    args = parser.parse_args()
    RESULTS = (ROOT / args.output_dir).resolve()
    RESULTS.mkdir(exist_ok=True)
    if (RESULTS / "traces_test.jsonl").exists():
        raise ValueError("A test run already exists here; choose a fresh --output-dir to reproduce it")
    pages = load_jsonl(ROOT / "data/pages.jsonl")
    questions = read_jsonl(ROOT / "benchmark/questions.jsonl")
    plan = json.loads((ROOT / "benchmark/plan.json").read_text())
    validate_inputs(pages, questions, plan)
    input_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in [ROOT / "data/pages.jsonl", *sorted((ROOT / "starter/src").glob("*.py"))]}
    embedder = MyEmbedder(plan["model"])
    store = QdrantStore(RESULTS / "qdrant", embedder.dimensions)
    try:
        if args.stage in {"ingest", "all"}:
            ingest(pages, plan, embedder, store)
        if args.stage in {"dev", "all"}:
            _, metrics = benchmark("dev", questions, plan, embedder, store)
            stats = {r["strategy"]: r for r in json.loads((RESULTS / "ingestion.json").read_text())}
            chosen = min(metrics, key=lambda m: (-m["hit3"], -m["hit1"], stats[m["strategy"]]["chunks"], m["strategy"]))
            selection = {"selected_strategy": chosen["strategy"], "selected_at": datetime.now(timezone.utc).isoformat(),
                         "benchmark_sha256": plan["benchmark_sha256"], "plan_sha256": hashlib.sha256((ROOT / "benchmark/plan.json").read_bytes()).hexdigest(),
                         "rule": plan["selection_rule"], "dev_metrics": metrics, "input_hashes": input_hashes}
            if (RESULTS / "traces_test.jsonl").exists():
                raise ValueError("Test already evaluated; use a fresh results directory for another experiment")
            write_json(RESULTS / "selection.json", selection)
            print(f"Selected {chosen['strategy']} on dev before test", flush=True)
        if args.stage in {"test", "all"}:
            selection = json.loads((RESULTS / "selection.json").read_text())
            if selection["plan_sha256"] != hashlib.sha256((ROOT / "benchmark/plan.json").read_bytes()).hexdigest():
                raise ValueError("Configuration changed after dev selection")
            if selection["benchmark_sha256"] != plan["benchmark_sha256"]:
                raise ValueError("Benchmark changed after dev selection")
            if selection["input_hashes"] != input_hashes:
                raise ValueError("Corpus or implementation changed after dev selection")
            if (RESULTS / "traces_test.jsonl").exists():
                raise ValueError("Test already evaluated; preserve the first test run")
            traces, _ = benchmark("test", questions, plan, embedder, store)
            prepare_audits(traces, pages)
        write_json(RESULTS / "environment.json", {
            "completed_at": datetime.now(timezone.utc).isoformat(), "python": sys.version,
            "platform": platform.platform(), "store": "Qdrant local persistent, exact cosine search",
            "packages": {name: importlib.metadata.version(name) for name in ["fastembed", "qdrant-client", "onnxruntime", "numpy"]},
            "model": plan["model"], "model_revision": embedder.revision, "dimensions": embedder.dimensions,
            "provider": "CPUExecutionProvider", "query_method": "FastEmbed query_embed",
            "document_method": "FastEmbed passage_embed", "api_cost_usd": 0.0,
            "notes": "Local compute/electricity and download costs excluded. C reuses B embedding cache."})
    finally:
        store.close()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / "error.log").open("a", encoding="utf-8").write(traceback.format_exc() + "\n")
        raise
