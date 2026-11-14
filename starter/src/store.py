"""Persistent Qdrant collections with stable IDs and metadata filtering."""
from dataclasses import asdict
from pathlib import Path
from typing import Any
from uuid import NAMESPACE_URL, uuid5

import numpy as np
from qdrant_client import QdrantClient, models
from .models import Chunk


class QdrantStore:
    def __init__(self, path: Path, dimensions: int) -> None:
        self.client = QdrantClient(path=str(path))
        self.dimensions = dimensions

    def create_schema(self, strategy: str) -> None:
        if not self.client.collection_exists(strategy):
            self.client.create_collection(strategy, vectors_config=models.VectorParams(
                size=self.dimensions, distance=models.Distance.COSINE))
        config = self.client.get_collection(strategy).config.params.vectors
        if config.size != self.dimensions or config.distance != models.Distance.COSINE:
            raise ValueError("Existing collection uses a different embedding configuration")

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if not chunks or len(chunks) != len(vectors):
            raise ValueError("Expected matching nonempty chunks and vectors")
        if any(len(v) != self.dimensions or not np.isfinite(v).all() for v in vectors):
            raise ValueError("Vector dimension/value mismatch")
        ids = [str(uuid5(NAMESPACE_URL, chunk.chunk_id)) for chunk in chunks]
        if len(set(ids)) != len(ids):
            raise ValueError("Duplicate chunk IDs in one snapshot")
        self.create_schema(strategy)
        old_ids = set()
        offset = None
        while True:
            records, offset = self.client.scroll(strategy, limit=256, offset=offset,
                                                with_payload=False, with_vectors=False)
            old_ids.update(str(record.id) for record in records)
            if offset is None:
                break
        for start in range(0, len(chunks), 64):
            points = [models.PointStruct(id=ids[i], vector=vectors[i], payload=asdict(chunks[i]))
                      for i in range(start, min(start + 64, len(chunks)))]
            self.client.upsert(strategy, points=points, wait=True)
        obsolete = old_ids - set(ids)
        if obsolete:
            self.client.delete(strategy, points_selector=models.PointIdsList(points=sorted(obsolete)), wait=True)

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        if len(query_vector) != self.dimensions or top_k <= 0:
            raise ValueError("Invalid query dimensions or top_k")
        if filters and not set(filters) <= {"chapter", "version", "language"}:
            raise ValueError("Only public context metadata can be filtered")
        query_filter = models.Filter(must=[models.FieldCondition(
            key=f"metadata.{key}", match=models.MatchValue(value=value))
            for key, value in filters.items()]) if filters else None
        hits = self.client.query_points(strategy, query=query_vector, query_filter=query_filter,
                                        limit=top_k, with_payload=True).points
        return [{**hit.payload, "score": hit.score} for hit in hits]

    def count(self, strategy: str) -> int:
        return self.client.count(strategy, exact=True).count

    def close(self) -> None:
        self.client.close()
