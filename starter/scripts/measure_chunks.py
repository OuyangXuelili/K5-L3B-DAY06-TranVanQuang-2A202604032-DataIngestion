"""Measure saved chunk lengths with the frozen model tokenizer."""
import hashlib
import json
from pathlib import Path

import numpy as np
from tokenizers import Tokenizer

ROOT = Path(__file__).resolve().parents[2]


def distribution(values):
    return {
        "min": min(values),
        "median": float(np.median(values)),
        "p90": float(np.percentile(values, 90)),
        "max": max(values),
        "mean": sum(values) / len(values),
        "total": sum(values),
    }


def main():
    model = json.loads((ROOT / "artifacts/model.json").read_text(encoding="utf-8"))
    cache_name = "models--" + model["repository"].replace("/", "--")
    tokenizer_path = ROOT / ".cache/models" / cache_name / "snapshots" / model["revision"] / "tokenizer.json"
    if not tokenizer_path.is_file():
        raise FileNotFoundError("Run the pipeline first to download the pinned model and tokenizer")
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    tokenizer.no_padding()
    tokenizer.no_truncation()
    limit = json.loads((ROOT / "results/corpus_validation.json").read_text(encoding="utf-8"))["model_input_limit"]
    rows = []
    for strategy in "ABC":
        path = ROOT / f"results/chunks_{strategy}.jsonl"
        chunks = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        token_counts = [len(encoding.ids) for encoding in tokenizer.encode_batch([chunk["text"] for chunk in chunks])]
        rows.append({
            "strategy": strategy,
            "chunks": len(chunks),
            "chunk_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "characters": distribution([len(chunk["text"]) for chunk in chunks]),
            "tokens": distribution(token_counts),
            "chunks_exceeding_model_limit": sum(count > limit for count in token_counts),
        })
    result = {
        "model": model["model"],
        "revision": model["revision"],
        "tokenizer_sha256": hashlib.sha256(tokenizer_path.read_bytes()).hexdigest(),
        "token_counting": "Includes special tokens; padding and truncation disabled; each chunk counted separately",
        "percentile_method": "NumPy linear percentile",
        "model_input_limit": limit,
        "strategies": rows,
    }
    (ROOT / "results/chunk_statistics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
