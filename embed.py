"""Milestone 4 (step 1) — Embed chunks and load them into ChromaDB.

Pipeline position (see planning.md Architecture):
    Ingestion/Chunking (ingest.py)  →  [Embedding + Vector Store]  →  Retrieval (retrieve.py)

Load chunks
↓
Generate embeddings
↓
Store in Chroma

What this does:
  1. Loads + chunks the corpus via ingest.py (277 chunks: 247 review + 30 catalog).
  2. Embeds each chunk's text with sentence-transformers `all-MiniLM-L6-v2` (local, 384-dim).
  3. Stores the vectors in a persistent ChromaDB collection, with one metadata record per
     chunk (type, professor, course, source_file, position, ...) for later attribution.

ChromaDB notes (the API calls used below):
  * PersistentClient(path=...) — opens an on-disk store so embeddings survive between runs;
    we don't have to re-embed every time we want to query.
  * get_or_create_collection(name, metadata={"hnsw:space": "cosine"}) — the collection is the
    table that holds vectors+metadata+ids. We pin the distance metric to COSINE so distance
    scores are in the 0..2 range the planning.md checkpoint thresholds (≈0.5) assume; Chroma's
    default is squared-L2, which would make those thresholds meaningless.
  * collection.add(ids=, documents=, metadatas=, embeddings=) — inserts the rows. We pass our
    own embeddings (computed by SentenceTransformer) rather than letting Chroma embed, so the
    same model is guaranteed to be used at index time and query time.

Run directly to (re)build the vector store:
    python embed.py
"""

from __future__ import annotations

from random import sample
import shutil

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL
from ingest import chunk_documents, load_documents


def build_store(reset: bool = True) -> chromadb.Collection:
    """
    Build the vector store used for semantic retrieval.

    Steps:
      1. Load documents from the ingestion pipeline.
      2. Split documents into chunks.
      3. Generate embeddings using all-MiniLM-L6-v2.
      4. Create or recreate the ChromaDB collection.
      5. Store chunk text, embeddings, and metadata.

    Args:
        reset:
            If True, deletes the existing ChromaDB directory before indexing.
            This prevents duplicate or stale vectors from previous runs.

    Returns:
        The populated ChromaDB collection.

    Why this matters:
        Retrieval quality depends entirely on what gets stored here.
        If chunks, embeddings, or metadata are incorrect, later retrieval
        and generation stages will fail even if the LLM is working correctly.
    """
    chunks = chunk_documents(load_documents())

    if not chunks:
        raise ValueError(
            "No chunks were generated. Check your ingestion pipeline."
        )
    
    print(f"Loaded {len(chunks)} chunks from ingest.py.")

    # check check Whether CS110B Was Chunked
    # for c in chunks:
    #     if c.metadata.get("course") == "CS110B":
    #         print(c.text)
    #         print(c.metadata)

    # Embedding model: local, no API key, no rate limits (planning.md Retrieval Approach).
    print(f"Loading embedding model: {EMBEDDING_MODEL} ...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [c.text for c in chunks]
    print(f"Embedding {len(texts)} chunks ...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    # Start from a clean store so re-running never leaves stale/duplicate vectors behind.
    if reset:
        shutil.rmtree(CHROMA_PATH, ignore_errors=True)
    # Chroma persists data on disk.
    # Re-running add() without clearing the database can create duplicates.
    # During development we rebuild from scratch so retrieval results remain predictable.

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[c.chunk_id for c in chunks],
        documents=texts,
        metadatas=[c.metadata for c in chunks],
        # Metadata travels alongside each chunk and is returned during retrieval.
        #  We store source information now so later milestones can:
        #    - cite where an answer came from
        #    - identify which professor/course was referenced
        #    - debug retrieval mistakes
        embeddings=embeddings.tolist(),
    )

    # RIGHT HERE (single unified diagnostics section)
    print("\nIndex statistics:")
    print(f"  Collection: {CHROMA_COLLECTION}")
    print(f"  Chunks indexed: {collection.count()}")
    print(f"  Distance metric: cosine")
    print(f"  Persisted to: {CHROMA_PATH}")


    print(f"Embedding dimension: {len(embeddings[0])}")

    sample = collection.peek(limit=3)

    print("\nSample indexed chunks:")
    for i, doc in enumerate(sample["documents"], 1):
        print(f"\nChunk {i}:")
        print(doc[:200])

    # print(f"\nStored {collection.count()} chunks in collection '{CHROMA_COLLECTION}'")

    return collection


if __name__ == "__main__":
    build_store()
