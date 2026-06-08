# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

**Computer Science professors and course reviews at City College of San Francisco (CCSF)** —
student-written reviews covering both individual CS instructors and the CS courses they teach
(CS 110A, CS 110B, CS 111C, CS 270, etc.).

This knowledge is valuable because CCSF's official course catalog lists what a CS class covers,
but says nothing about *how it's actually taught*: which professor explains programming concepts
clearly, how heavy the coding workload is, whether exams are fair, how good the office hours are,
and whether students would take the instructor again. The same applies at the course level — the
catalog won't tell you that one section of CS 110A is chaotic while another is well-run, or how a
course's difficulty varies by who teaches it. That information only exists in student-written
reviews scattered across rating sites — it's never published through official channels, and it's
exactly what a CS student needs when picking both a course and a section during registration.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

Sources actually collected — one .txt file per source in documents/. Total: **247 student-review
chunks across 7 professors + 4 course-page reviews, plus 30 official catalog entries.**

| # | Source | Type | Reviews | File / URL |
|---|--------|------|--------:|-----------|
| 1 | RateMyProfessors — Aaron Brick | Professor reviews (Python, C++, Java, Unix) | 63 | aaron-brick.txt — https://www.ratemyprofessors.com/professor/1609317 |
| 2 | RateMyProfessors — Jessica Masters | Professor reviews (Java, data structures) | 59 | jessica-masters.txt — https://www.ratemyprofessors.com/professor/1768830 |
| 3 | RateMyProfessors — Samuel Johnson | Professor reviews (CS270 assembly, Python, C++) | 48 | samuel-johnson.txt — https://www.ratemyprofessors.com/professor/2306878 |
| 4 | RateMyProfessors — Max Luttrell | Professor reviews (C++) | 31 | max-luttrell.txt — https://www.ratemyprofessors.com/professor/1986437 |
| 5 | RateMyProfessors — Daniel O'Leary | Professor reviews (Python, SQL) | 21 | daniel-oleary.txt — https://www.ratemyprofessors.com/professor/2275541 |
| 6 | RateMyProfessors — Jonathan Potter | Professor reviews (CS270 architecture, Python) | 15 | jonathan-potter.txt — https://www.ratemyprofessors.com/professor/2445727 |
| 7 | RateMyProfessors — LaDawn Meade | Professor reviews (Java, Python) | 6 | ladawn-meade.txt — https://www.ratemyprofessors.com/professor/2332544 |
| 8 | Coursicle — CS 110A course page | Course-level reviews (multiple professors) | 2 | cs110a-coursicle.txt — https://www.coursicle.com/ccsf/courses/CS/110A/ |
| 9 | Coursicle — CS 110B course page | Course-level reviews (multiple professors) | 2 | cs110b-coursicle.txt — https://www.coursicle.com/ccsf/courses/CS/110B/ |
| 10 | CCSF official CS catalog | Official course descriptions (factual baseline, 30 courses) | — | cs-catalog.txt — https://www.ccsf.edu/academics/ccsf-catalog/courses-by-department/computer-science |

Coverage notes: the 7 professors span every major intro CS language at CCSF (Python, C++, Java, SQL,
assembly) and the full sentiment range — Luttrell and Potter skew positive, Brick and Johnson skew
negative, Masters/O'Leary/Meade are polarized. Several professors teach the SAME course (CS110A:
O'Leary, Brick, Potter, Johnson; CS270: Potter, Luttrell, Johnson; CS111C: Masters, Johnson), which
lets the system answer "which professor for course X?" and stress-tests whether retrieval keeps
professors apart. The catalog is a separately-tagged factual layer for prerequisite/units/topic
questions and official-vs-student contrasts — it is NOT blended into the opinion reviews.

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** ~1 review per chunk (target ~300–400 characters; split anything longer at sentence boundaries).

**Overlap:** None (0 characters) between separate reviews.

**Reasoning:** This is a review-heavy corpus, not long-form prose. Each RateMyProfessors review is a
self-contained unit (one student, one opinion, one or two sentences) tagged with the professor and
often a course and a rating. The natural chunk boundary is the review itself — splitting mid-review
would tear an opinion in half, and adding overlap across two unrelated reviews would blend two
students' opinions into one chunk and pollute retrieval. So I chunk *per review* and only fall back
to sentence-boundary splitting for the rare long review that exceeds the size target. Each chunk's
metadata records the professor name (and course/department where available) so retrieval and
attribution stay accurate.

**Document structure (from skimming the collected corpus):** The documents are all short reviews, not
long guides. Across the 247 review chunks, length is tightly clustered — median ~334 characters
(~66 words), and the **maximum is only 351 characters** because RateMyProfessors hard-caps review
length. Zero reviews exceed 400 chars; 39 are one-liners under 200 chars (e.g. "He is a great
teacher!!!"). Each review concentrates its whole opinion — professor, workload, recommendation — in
1–3 sentences, so no key fact is spread across paragraphs that a chunk boundary could split. The 30
catalog entries are similar in size (~60 words) but factual. This shape is exactly why one-record-per-
chunk with no overlap fits: nothing is long enough to need splitting, and a fixed-window splitter
would instead risk merging two unrelated reviews into one chunk.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via sentence-transformers (local, 384-dim, fast, no API cost).

**Top-k:** 5 chunks per query.

**Production tradeoff reflection:**


---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. -->



| # | Question | Type | Expected answer (verify against sources) |
|---|----------|------|------------------------------------------|
| 1 | What do students say about Jessica Masters as a CS professor? | Professor — clean | Strongly positive overall: clear, thorough YouTube video lectures, very organized online classes, prompt detailed feedback, lots of extra credit, caring ("#1 CS prof at CCSF"). The recurring criticism is heavy workload / "busy work" and a lot of reading (some cite 10–15 hrs/week), plus a minority of harsh 1–2★ reviews calling it overwhelming. Net: highly recommended for motivated students; workload is the main downside. |
| 2 | Which professor should I take for CS270, and why? | Course → professor — contested | Take **Jonathan Potter** (or Max Luttrell): Potter's reviews are near-uniformly 5★ — clear engaging lectures, accessible, fair/generous grading. Luttrell is also positive. **Avoid Samuel Johnson** for CS270: reviews complain of very slow/late grading, disorganized Canvas modules (links to others' YouTube videos), and a condescending tone — though a few defend him and note it's an easy A. |
| 3 | What is CS110B and what is its prerequisite? | Factual (catalog) | CS110B = Programming Fundamentals: C++ (4 units, UC/CSU transferable). Covers procedural and object-oriented problem solving: classes, objects, references, dynamic memory, inheritance, polymorphism, arrays, pointers, files, abstract data types. Advisory prerequisite: CS 10 or CS 110A or MATH 108. |
| 4 | How do students describe the workload and exams in CS111C? | Course — opinion | CS111C (Data Structures & Algorithms: Java) is moderately heavy: weekly homework/reading plus several projects and a midterm/final, with lots of extra credit available (difficulty rated ~3–4/5). With Masters, exams are often open-note/take-home and considered fair; with Johnson, grading is lenient/easy-A but slow and the content "lean." Manageable if you keep up with the weekly work. |
| 5 | Which CS professor do students most recommend overall, and why? | Aggregation — INTENDED FAILURE CASE | Human answer: Max Luttrell and Jonathan Potter are the most uniformly recommended (almost all 5★, "would take again"); Masters is loved but polarizing. BUT the system is expected to struggle here — top-k retrieval returns the 5 chunks most similar to "recommend," not a true tally across all professors, so it may name whichever positive reviews surface rather than correctly ranking. This is the intended failure case. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning. -->

1. **Off-topic / wrong-professor retrieval.** Many reviews are short generic praise ("great teacher,
   easy A") that embeds almost identically for every professor. A query about one professor could
   retrieve near-identical chunks from a *different* one. Mitigation: the professor + course is
   embedded into the chunk text (not just metadata), so the name anchors the embedding.

2. **Fake, promotional, and self-written reviews.** The corpus contains reviews that read like ads or
   manipulation — e.g. the recurring "he writes his own reviews" accusation on Samuel Johnson's page,
   and an internship-promising, "take his class" review for Indika Walimuni on the CS110B course page.
   The system has no way to detect these and may surface them as if they were genuine consensus.

3. **Noisy / mismatched metadata.** Real review data is inconsistent: one LaDawn Meade review is
   tagged CS111B but its text says "this review is for CS111C," and a CS160A review actually rants
   about "SQL classes." Course-level retrieval keys on the tagged course, so these mismatches can
   route a review to the wrong course question.

4. **Aggregation / superlative questions.** Questions like "which professor do students *most*
   recommend?" require counting/ranking across the whole corpus, but top-k retrieval only returns the
   few chunks most similar to the query — it never tallies. The model may answer confidently from
   whatever positive chunks surface rather than a true comparison. (This is our intended failure case.)

5. **Official catalog competing with opinions.** Adding the factual catalog risks an opinion query
   ("is CS110B hard?") retrieving the bland official description instead of a review. Mitigation:
   catalog entries are a separate, clearly-labeled record type, and their factual wording is
   semantically dissimilar from opinion queries — but it remains a risk to watch in evaluation.



---

## Architecture

<!-- Five stages: Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation -->

```
┌─────────────────────────────┐   ┌─────────────────────────┐   ┌────────────────────────┐
│ Document Ingestion          │   │ Chunking                │   │ Embedding + Vector     │
│ documents/*.txt:            │   │ one RECORD per chunk,   │   │ Store                  │
│  • 7 professor review files │──▶│ no overlap:             │──▶│ sentence-transformers  │
│  • 2 Coursicle course pages │   │  • review → prof+course │   │ all-MiniLM-L6-v2 ──▶    │
│  • 1 official catalog file  │   │    +tags in text        │   │ ChromaDB collection    │
│ (parser skips _templates)   │   │  • catalog → course     │   │ (~277 chunks; metadata │
│                             │   │    entry, type=catalog  │   │  incl. type, course)   │
└─────────────────────────────┘   └─────────────────────────┘   └───────────┬────────────┘
                                                                             │
                          ┌──────────────────────────────────────────────────▼───────────┐
                          │ Retrieval                                                      │
                          │ embed query ▶ Chroma cosine similarity ▶ top-k = 5 chunks      │
                          │ (mix of opinion reviews + factual catalog entries, w/ metadata)│
                          └──────────────────────────────────────────────────┬───────────┘
                                                                              │
                          ┌────────────────────────────────────────────────────▼─────────┐
                          │ Generation                                                    │
                          │ Groq LLM, grounded system prompt: answer ONLY from retrieved   │
                          │ chunks, cite professor/course/source, distinguish official     │
                          │ catalog facts from student opinion, say "not enough info" when │
                          │ chunks don't cover it  ▶  Gradio/Streamlit UI                  │
                          └───────────────────────────────────────────────────────────────┘
```

Two record types flow through the same pipeline: **opinion reviews** (the bulk, 247 chunks) and
**official catalog entries** (30 chunks, tagged `type=catalog`). They share embedding/retrieval but
the generation prompt is told to treat catalog text as fact and review text as student opinion.

---

## AI Tool Plan

<!-- For each part of the pipeline, describe which AI tool, what input you'll give it,
     what you expect it to produce, and how you'll verify it matches your spec. -->

**Milestone 3 — Ingestion and chunking:**
Use Claude (Claude Code). Input: this Chunking Strategy section + a sample saved review file.
Expect: a `load_documents()` that reads files from `documents/` and a `chunk_reviews()` that splits
per-review (sentence-boundary fallback over ~400 chars) and attaches professor/course metadata.
Verify: print the chunk count and spot-check 5 chunks to confirm no review was split mid-sentence
and metadata is correct.

**Milestone 4 — Embedding and retrieval:**
Use Claude. Input: the Retrieval Approach section (model `all-MiniLM-L6-v2`, top-k 5) + the chunk
schema from Milestone 3. Expect: code that embeds chunks, builds a ChromaDB collection, and a
`retrieve(query, k=5)` function. Verify: run 2–3 of my test questions and confirm the returned
chunks are actually about the right professor.

**Milestone 5 — Generation and interface:**
Use Claude. Input: the Grounded Generation requirement + my retrieval function. Expect: a Groq call
with a grounding system prompt, plus a Gradio/Streamlit UI. Verify: ask an out-of-corpus question
and confirm the system declines instead of hallucinating, and that answers cite the source professor.


