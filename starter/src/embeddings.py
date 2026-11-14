"""CPU embeddings with a content-addressed cache and explicit model identity."""
import hashlib
from pathlib import Path
import numpy as np
from typing import Protocol


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Quantized BGE adapter using FastEmbed query/passage conventions."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        if model_name != "BAAI/bge-small-en-v1.5":
            raise ValueError("This experiment is frozen to BAAI/bge-small-en-v1.5")
        from fastembed import TextEmbedding
        from huggingface_hub import snapshot_download
        root = Path(__file__).resolve().parents[2]
        self.cache = root / ".cache" / "vectors"
        self.cache.mkdir(parents=True, exist_ok=True)
        self.revision = "aa8f8b060edb00e03bfdd08813a2949946c8ba55"
        snapshot = root / ".cache/models/models--Qdrant--bge-small-en-v1.5-onnx-Q/snapshots" / self.revision
        if not (snapshot / "model_optimized.onnx").exists():
            snapshot = Path(snapshot_download("Qdrant/bge-small-en-v1.5-onnx-Q", revision=self.revision,
                                             cache_dir=str(root / ".cache/models")))
        self.model = TextEmbedding(model_name=model_name, specific_model_path=str(snapshot),
                                   threads=2, providers=["CPUExecutionProvider"])
        self.dimensions = 384
        self.model_calls = 0

    def _embed(self, texts: list[str], query: bool) -> list[list[float]]:
        paths = [self.cache / (hashlib.sha256(f"{self.model_name}:{query}:{text}".encode()).hexdigest() + ".npy") for text in texts]
        missing = [i for i, path in enumerate(paths) if not path.exists()]
        if missing:
            inputs = [texts[i] for i in missing]
            generator = self.model.query_embed(inputs, batch_size=8) if query else self.model.passage_embed(inputs, batch_size=8)
            for i, vector in zip(missing, generator, strict=True):
                np.save(paths[i], vector)
                self.model_calls += 1
        result = [np.load(path).astype(float).tolist() for path in paths]
        if any(len(v) != self.dimensions or not np.isfinite(v).all() for v in result):
            raise ValueError("Embedding dimensions or values are invalid")
        return result

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embed(texts, query=False)

    def embed_query(self, question: str) -> list[float]:
        return self._embed([question], query=True)[0]
