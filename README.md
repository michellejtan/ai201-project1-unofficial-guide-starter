# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Computer Science professors and course reviews at City College of San Francisco (CCSF) — student
opinions on individual CS instructors and the courses they teach (CS 110A, CS 110B, CS 111C, CS 270,
etc.), plus the official course catalog as a factual baseline to contrast against.

This knowledge is valuable because CCSF's official catalog lists what a course covers but says nothing
about *how it's actually taught* — which professor explains programming concepts clearly, how heavy
the coding workload is, whether exams are fair, or whether students would take the instructor again.
That lived experience only exists in student-written reviews scattered across rating sites, and it's
exactly what a student needs when choosing both a course and a section during registration.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | RateMyProfessors — Aaron Brick (63 reviews; Python, C++, Java, Unix) | Professor reviews | https://www.ratemyprofessors.com/professor/1609317 → documents/aaron-brick.txt |
| 2 | RateMyProfessors — Jessica Masters (59 reviews; Java, data structures) | Professor reviews | https://www.ratemyprofessors.com/professor/1768830 → documents/jessica-masters.txt |
| 3 | RateMyProfessors — Samuel Johnson (48 reviews; assembly, Python, C++) | Professor reviews | https://www.ratemyprofessors.com/professor/2306878 → documents/samuel-johnson.txt |
| 4 | RateMyProfessors — Max Luttrell (31 reviews; C++) | Professor reviews | https://www.ratemyprofessors.com/professor/1986437 → documents/max-luttrell.txt |
| 5 | RateMyProfessors — Daniel O'Leary (21 reviews; Python, SQL) | Professor reviews | https://www.ratemyprofessors.com/professor/2275541 → documents/daniel-oleary.txt |
| 6 | RateMyProfessors — Jonathan Potter (15 reviews; CS270 architecture, Python) | Professor reviews | https://www.ratemyprofessors.com/professor/2445727 → documents/jonathan-potter.txt |
| 7 | RateMyProfessors — LaDawn Meade (6 reviews; Java, Python) | Professor reviews | https://www.ratemyprofessors.com/professor/2332544 → documents/ladawn-meade.txt |
| 8 | Coursicle — CS 110A course page (2 reviews, multiple professors) | Course-level reviews | https://www.coursicle.com/ccsf/courses/CS/110A/ → documents/cs110a-coursicle.txt |
| 9 | Coursicle — CS 110B course page (2 reviews, multiple professors) | Course-level reviews | https://www.coursicle.com/ccsf/courses/CS/110B/ → documents/cs110b-coursicle.txt |
| 10 | CCSF official CS catalog (30 course descriptions) | Official catalog (factual baseline) | https://www.ccsf.edu/academics/ccsf-catalog/courses-by-department/computer-science → documents/cs-catalog.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** One record per chunk — there are two record types:
- **Review chunk:** a single student review (typically ~150–400 characters), prefixed with the
  professor and course and suffixed with the attribute tags, e.g.
  `Review of Professor Max Luttrell for CS110B: <review text> [tags: Amazing lectures, ...]`.
- **Catalog chunk:** a single official course entry (course code, title, units, prerequisites, and
  the catalog description), e.g. `Official CCSF catalog entry for CS110B (Programming Fundamentals: C++)...`.

**Overlap:** None (0). Each record is an independent unit; overlapping across two reviews would blend
two different students' (or two professors') opinions into one chunk and pollute retrieval.

**Why these choices fit your documents:** This is a review-heavy corpus, not long-form prose. Each
RateMyProfessors review is a self-contained one-to-three-sentence opinion tagged with a professor and
course, so the review *is* the natural boundary — splitting mid-review would tear an opinion in half.
Preprocessing: stripped the page chrome (the "Helpful" button, thumbs-up/down counts, dates,
attendance/textbook flags) and kept the review text plus structured fields (course, quality,
difficulty, would-take-again, tags). The professor/course is embedded into the chunk text (not just
metadata) so generic praise like "great teacher" can't be retrieved for the wrong professor. The
official catalog is chunked the same way (one short entry = one chunk) but kept as a separate,
clearly-labeled record type so factual course descriptions don't compete with opinion reviews.

**Final chunk count:** 277 expected — 247 review chunks (across 7 professors + 2 course pages) + 30
catalog entries. (Confirm by running ingestion in Milestone 3.)

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
