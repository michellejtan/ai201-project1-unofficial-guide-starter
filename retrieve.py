"""Milestone 4 (step 2) — Retrieval over the ChromaDB vector store.

User query
↓
Embed query
↓
Search Chroma
↓
Return top-k chunks

retrieve(query, k) embeds the query with the SAME model used at index time, runs a cosine
similarity search against the persisted collection, and returns the top-k chunks with their
source metadata and distance scores.

Run directly to test retrieval against 3 of the planning.md evaluation queries:
    python retrieve.py
(Assumes embed.py has already built the store. If not, run `python embed.py` first.)
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS


@dataclass
class Result:
    text: str
    metadata: dict
    distance: float  # cosine distance; lower = more similar (0 = identical)


@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    """Load the embedding model once and reuse it across queries."""
    return SentenceTransformer(EMBEDDING_MODEL)


@lru_cache(maxsize=1)
def _collection() -> chromadb.Collection:
    """Open the persisted collection once. get_collection (not create) so a missing store
    fails loudly instead of silently querying an empty collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(name=CHROMA_COLLECTION)


def retrieve(query: str, k: int = N_RESULTS) -> list[Result]:
    """Return the top-k most relevant chunks for `query`, nearest first."""
    query_embedding = _model().encode([query], convert_to_numpy=True).tolist()
    res = _collection().query(
        query_embeddings=query_embedding,
        n_results=k,
    )
    # Chroma returns parallel lists nested one level per query; we sent one query → index [0].
    return [
        Result(text=doc, metadata=meta, distance=dist)
        for doc, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]


# 3 of the 5 planning.md evaluation queries (clean professor, contested course→prof, factual).
TEST_QUERIES = [
    "What do students say about Jessica Masters as a CS professor?",
    "Which professor should I take for CS270, and why?",
    "What is CS110B and what is its prerequisite?",
    "Official CCSF catalog entry for CS110B",

]


def _print_results(query: str, results: list[Result]) -> None:
    print("=" * 88)
    print(f"QUERY: {query}\n")
    for rank, r in enumerate(results, 1):
        m = r.metadata
        src = m.get("professor") if m.get("type") == "review" else "CCSF catalog"
        print(
            f"  [{rank}] distance={r.distance:.3f}  "
            f"type={m.get('type')}  course={m.get('course')}  source={src}  "
            f"({m.get('source_file')}:{m.get('position')})"
        )
        print(f"      {r.text}\n")


if __name__ == "__main__":
    for q in TEST_QUERIES:
        _print_results(q, retrieve(q))

