"""Milestone 3 — Document ingestion and chunking.

Loads the source files in documents/ and turns each record into one chunk. Two record types
flow through the same pipeline (see planning.md Architecture):

  * review chunks  — one student review; professor + course are embedded into the chunk text,
                     and the attribute tags are appended, so the embedding captures who/what the
                     review is about plus its summarized attributes.
  * catalog chunks — one official CCSF course entry (type=catalog); kept separate from opinions
                     so factual descriptions don't compete with reviews during retrieval.

Chunking strategy (planning.md): one record = one chunk, no overlap. Reviews are short and
self-contained (max ~351 chars on RateMyProfessors), so the record is the natural boundary.

Cleaning happened mostly at collection time (the "Helpful" button, thumbs counts, dates, and
attendance/textbook flags were stripped when each review was saved). This loader additionally
drops '#' comment lines.

Run directly to (re)chunk and inspect:
    python ingest.py
"""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass, field

from config import DOCS_PATH as DOCUMENTS_DIR


@dataclass
class Chunk:
    text: str                       # what gets embedded
    metadata: dict = field(default_factory=dict)
    chunk_id: str = ""


def _parse_block(block: str) -> dict:
    """Parse one '---'-separated block into a {KEY: value} dict.

    REVIEW: / DESCRIPTION: are always last and may contain colons, so everything after them is
    taken verbatim as the body text.
    """
    fields: dict[str, str] = {}
    lines = block.strip().splitlines()
    for i, line in enumerate(lines):
        for body_key in ("REVIEW:", "DESCRIPTION:"):
            if line.startswith(body_key):
                rest = [line[len(body_key):].strip()] + lines[i + 1:]
                fields[body_key.rstrip(":")] = "\n".join(rest).strip()
                return fields
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip().upper()] = value.strip()
    return fields


def load_documents(docs_dir: str = DOCUMENTS_DIR) -> list[tuple[dict, list[dict]]]:
    """Load every documents/*.txt (skipping '_'-prefixed templates).

    Returns a list of (header, records) where header carries file-level fields and records is
    the list of per-review or per-course dicts.
    """
    docs = []
    for path in sorted(glob.glob(os.path.join(docs_dir, "*.txt"))):
        if os.path.basename(path).startswith("_"):
            continue
        with open(path, encoding="utf-8") as f:
            raw = "\n".join(l for l in f.read().splitlines() if not l.lstrip().startswith("#"))
        blocks = [b for b in raw.split("\n---\n") if b.strip()]
        if not blocks:
            continue
        header = _parse_block(blocks[0])
        header["_FILE"] = os.path.basename(path)
        records = [_parse_block(b) for b in blocks[1:]]
        records = [r for r in records if r.get("REVIEW") or r.get("DESCRIPTION")]
        if records:
            docs.append((header, records))
    return docs


def _review_chunk(header, rec, idx) -> Chunk:
    professor = rec.get("PROFESSOR") or header.get("PROFESSOR", "Unknown professor")
    course = rec.get("COURSE") or header.get("COURSE") or "unknown"
    tags = rec.get("TAGS", "")
    tags = "" if tags.lower() == "n/a" else tags
    text = f"Review of Professor {professor} for {course}: {rec['REVIEW']}"
    if tags:
        text += f" [tags: {tags}]"
    meta = {
        "type": "review",
        "professor": professor,
        "course": course,
        "quality": rec.get("QUALITY", "n/a"),
        "difficulty": rec.get("DIFFICULTY", "n/a"),
        "would_take_again": rec.get("WOULD_TAKE_AGAIN", "n/a"),
        "tags": tags or "n/a",
        "source_file": header["_FILE"],
        "position": idx,
        "source": header.get("SOURCE", ""),
    }
    return Chunk(text=text, metadata=meta, chunk_id=f"{header['_FILE']}:{idx}")


def _catalog_chunk(header, rec, idx) -> Chunk:
    course = rec.get("COURSE", "unknown")
    title = rec.get("TITLE", "")
    units = rec.get("UNITS", "")
    prereq = rec.get("PREREQ", "")
    advise = rec.get("ADVISE", "")
    transfer = rec.get("TRANSFER", "")
    parts = [f"Official CCSF catalog entry for {course} ({title})."]
    if units:
        parts.append(f"{units} units.")
    if transfer:
        parts.append(f"Transfers: {transfer}.")
    if prereq:
        parts.append(f"Prerequisite: {prereq}.")
    if advise:
        parts.append(f"Advisory: {advise}.")
    parts.append(f"Description: {rec['DESCRIPTION']}")
    text = " ".join(parts)
    meta = {
        "type": "catalog",
        "professor": "n/a",
        "course": course,
        "title": title,
        "units": units or "n/a",
        "source_file": header["_FILE"],
        "position": idx,
        "source": header.get("SOURCE", ""),
    }
    return Chunk(text=text, metadata=meta, chunk_id=f"{header['_FILE']}:{idx}")


def chunk_documents(docs: list[tuple[dict, list[dict]]]) -> list[Chunk]:
    """One chunk per record; dispatches on the file's TYPE (catalog vs. review)."""
    chunks: list[Chunk] = []
    for header, records in docs:
        is_catalog = header.get("TYPE", "").lower() == "catalog"
        for idx, rec in enumerate(records):
            chunks.append(_catalog_chunk(header, rec, idx) if is_catalog
                          else _review_chunk(header, rec, idx))
    return chunks


def main() -> None:
    docs = load_documents()
    chunks = chunk_documents(docs)

    reviews = [c for c in chunks if c.metadata["type"] == "review"]
    catalog = [c for c in chunks if c.metadata["type"] == "catalog"]

    #chunk length statistics
    review_lengths = [len(c.text) for c in reviews]

    print("=== Review Chunk Length Statistics ===")
    print(f"Min length: {min(review_lengths)}")
    print(f"Max length: {max(review_lengths)}")
    print(f"Average length: {sum(review_lengths) / len(review_lengths):.1f}")
    print()

    print(f"Loaded {len(docs)} source files.")
    for header, records in docs:
        print(f"  - {header['_FILE']:<24} {len(records):>3} records  (type={header.get('TYPE','review')})")
    print(f"\nTotal chunks: {len(chunks)}  ({len(reviews)} review + {len(catalog)} catalog)\n")

    # Inspect 5 representative chunks: a mix of review and catalog.
    sample = reviews[:1] + reviews[len(reviews)//2:len(reviews)//2+2] + catalog[:1] + catalog[-1:]
    print("=== 5 representative chunks (self-contained check) ===")
    for c in sample:
        print(
        f"\n[{c.chunk_id}] "
        f"type={c.metadata['type']} "
        f"course={c.metadata['course']} "
        f"prof={c.metadata['professor']} "
        f"length={len(c.text)} chars"
    )
        print(f"  {c.text}")


if __name__ == "__main__":
    main()
