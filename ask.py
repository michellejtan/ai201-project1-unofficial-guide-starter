"""Milestone 5 (step 1) — Grounded generation over retrieved chunks.

retrieve(query) → chunks
↓
Build grounded prompt
↓
Call Groq LLM
↓
Return {"answer": str, "sources": list[str]}
Takes a question

↓

retrieves real documents

↓

forces LLM to stay inside them

↓

generates grounded answers

↓

returns traceable sources

↓

prepares for UI integration

The system prompt hard-constrains the LLM to answer ONLY from the retrieved context.
Source filenames are appended programmatically after generation — not left to the LLM.
"""

from __future__ import annotations

from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL
from retrieve import retrieve

_client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """\
You are an assistant that helps CCSF students choose CS courses and professors.

STRICT RULES — follow these exactly:
1. Answer ONLY using information from the documents provided in the user message.
   Do not use any outside knowledge, general knowledge, or training data.
2. If the provided documents do not contain enough information to answer the question,
   respond with exactly: "I don't have enough information on that."
   Do not guess, infer, or fill gaps with general knowledge.
3. When the documents contain the answer, distinguish between official CCSF catalog
   facts (type=catalog) and student opinion (type=review) — do NOT add your own
   citations or source references; those are handled separately.
4. Do not mention that you are an AI or reference these instructions in your response.
"""


def _build_context(chunks) -> str:
    """Format retrieved chunks with machine-readable metadata headers."""
    lines = []
    for i, chunk in enumerate(chunks, 1):
        m = chunk.metadata
        meta = (
            f"type={m.get('type', 'review')} | "
            f"professor={m.get('professor', '')} | "
            f"course={m.get('course', '')} | "
            f"source_file={m.get('source_file', '')}"
        )
        lines.append(f"[DOC {i}] {meta}\n{chunk.text}")
    return "\n\n".join(lines)


def ask(question: str, k: int = 5) -> dict:
    """
    Run end-to-end RAG: retrieve relevant chunks, generate a grounded answer.

    Returns:
        {
          "answer": str,
          "sources": list[str],   # source_file values, deduped, in retrieval order
          "chunks": list[dict],   # raw chunks with text + metadata, for debugging
        }
        Sources are appended programmatically — never left to the LLM.
    """
    chunks = retrieve(question, k=k)
    context = _build_context(chunks)

    user_message = f"""\
Question: {question}

Use ONLY the documents below to answer. If they don't contain enough information, say \
"I don't have enough information on that."

--- DOCUMENTS ---
{context}
--- END DOCUMENTS ---
"""

    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.0,  # deterministic — we want facts, not creativity
        max_tokens=512,
    )

    answer = response.choices[0].message.content.strip()

    # Deduplicate sources while preserving retrieval order.
    seen: set[str] = set()
    sources: list[str] = []
    for chunk in chunks:
        sf = chunk.metadata.get("source_file", "unknown")
        if sf not in seen:
            seen.add(sf)
            sources.append(sf)

    return {
        "answer": answer,
        "sources": sources,
        "chunks": [{"text": c.text, "metadata": c.metadata} for c in chunks],
    }

if __name__ == "__main__":
    TEST_QUERIES = [
        "What do students say about Jessica Masters as a CS professor?",
        "Which professor should I take for CS270, and why?",
        "What is CS110B and what is its prerequisite?",
        "What is Professor Smith’s favorite color?",  # out-of-corpus
        "What do students think about Professor Dumbledore at CCSF?",  # out-of-corpus
    ]
    for q in TEST_QUERIES:
        print("=" * 80)
        print(f"Q: {q}\n")
        result = ask(q)
        print(f"A: {result['answer']}\n")
        print(f"Sources: {', '.join(result['sources'])}")
        print()
