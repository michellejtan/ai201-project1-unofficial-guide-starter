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

## Sample Chunks

Five representative chunks as they are stored in the vector database. Each chunk is a single
self-contained record with the professor and course embedded in the text so the embedding carries
attribution, not just the metadata fields.

**Chunk 1 — review, source: jessica-masters.txt**
```
Review of Professor Jessica Masters for CS111C: I've taken multiple online CS courses at CCSF,
and this professor easily stands out in organization, engagement, and overall quality. The lectures
are clear and well structured, and I've learned more in this class than I expected. Highly
recommended. [tags: Amazing lectures, Clear grading criteria, Caring]
```

**Chunk 2 — review, source: max-luttrell.txt**
```
Review of Professor Max Luttrell for CS110C: Professor Luttrell is awesome. His content is
extremely well organized and he is very awesome and helpful to talk to during office hours. I particularly
enjoyed his examples since they were really fun, relevant, or quirky (e.g. Bay area airports/sports
teams, Pokémon references). Take his class!!! [tags: Participation matters, EXTRA CREDIT,
Accessible outside class]
```

**Chunk 3 — review, source: samuel-johnson.txt**
```
Review of Professor Samuel Johnson for CS270: I think the bad reviews of Johnson are either a bit
exaggerated or old. This was a fine class and got a decent introduction to assembly and computer
architecture. While the course is a tad unorganized, the generous grading and deadlines make up for
it and make getting an A doable without internalizing the content if you don't want to.
[tags: Participation matters, Clear grading criteria, Lots of homework]
```

**Chunk 4 — catalog, source: cs-catalog.txt**
```
Official CCSF catalog entry for CS110B (Programming Fundamentals: C++): 4 units, UC/CSU
transferable. Advisory: CS 10 or CS 110A or MATH 108. This course covers programming fundamentals
using the C++ language, using procedural and object-oriented approaches to problem solving. Topics
include structured elements, classes, objects, references, dynamic memory allocation, inheritance,
polymorphism, arrays, pointers, files, design and implementation of abstract data types, in
numerical and non-numerical applications.
```

**Chunk 5 — review, source: jessica-masters.txt**
```
Review of Professor Jessica Masters for CS111B: Jessica Masters is an amazing professor who tries
hard to make sure each student understands material! Each week is a new module that covers a new
topic, such as Arrays, Loops, etc. It goes by very fast, but make sure you dedicate time to study
the material! Each week, there are discussions and HW. Midterm and final are both projects up to you.
[tags: Get ready to read, Amazing lectures, Online Savvy]
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 (sentence-transformers)

This is a lightweight transformer-based embedding model that maps text into a 384-dimensional vector space. It runs locally, requires no API key, and is fast enough to embed hundreds of chunks in seconds on a laptop.

The same model for both:

indexing (embed.py)
querying (retrieve.py)

to ensure embedding consistency across the pipeline.

Why this model:

We chose all-MiniLM-L6-v2 because:

It is fast and lightweight, making local development practical
It produces high-quality semantic embeddings for short-to-medium text (perfect for reviews and catalog entries)
It is widely used in baseline RAG systems and is stable and well-documented
It does not require external API calls, avoiding cost and latency issues

**Production tradeoff reflection:**

If deployed in a real production system, I would consider switching to a higher-quality embedding model such as:

text-embedding-3-large (OpenAI)
bge-large-en (BAAI)
e5-large-v2

Tradeoffs:

Better accuracy on subtle semantic differences (e.g. distinguishing “good teacher” vs “easy class”)
Better retrieval of factual queries like course definitions
But:
higher latency
higher cost (API-based models)
more infrastructure complexity

In this project, local execution and simplicity over maximum retrieval accuracy is prioritized.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The system prompt in `ask.py` enforces grounding with three hard constraints passed as `role: system`
before any user message reaches the LLM:

```
STRICT RULES — follow these exactly:
1. Answer ONLY using information from the documents provided in the user message.
   Do not use any outside knowledge, general knowledge, or training data.
2. If the provided documents do not contain enough information to answer the question,
   respond with exactly: "I don't have enough information on that."
   Do not guess, infer, or fill gaps with general knowledge.
3. When the documents contain the answer, distinguish between official CCSF catalog
   facts (type=catalog) and student opinion (type=review).
```

**How source attribution is surfaced in the response:**

Source filenames are appended **programmatically** in `ask.py` after the LLM response is returned —
they are never left to the LLM to generate, which prevents hallucinated or misattributed citations.
Each retrieved chunk is formatted with a machine-readable metadata header before being injected into
the user message:

```
[DOC 1] type=review | professor=Jessica Masters | course=CS111C | source_file=jessica-masters.txt
<review text>
```

This header format lets the LLM reference document type and professor in its prose ("according to
student reviews…" vs. "according to the official catalog…") while the UI independently lists the
actual source filenames from the chunk metadata objects returned by ChromaDB. No low-relevance
filtering is applied — all top-k=5 chunks are always included because with only 277 total chunks
and reviews averaging ~334 characters the context stays well within the model's token limit.

---

## Retrieval Test Results

Three queries with the actual top-5 chunks returned by ChromaDB (cosine similarity, `all-MiniLM-L6-v2`).

---

### Query 1: "What do students say about Jessica Masters as a CS professor?"

| Rank | Source file | Professor | Course | Chunk preview |
|------|-------------|-----------|--------|---------------|
| 1 | jessica-masters.txt | Jessica Masters | CS111C | "Review of Professor Jessica Masters for CS111C: I've taken multiple online CS courses at CCSF, and this professor easily stands out in organization, engagement, and overall quality. The lectures are clear and well structured..." |
| 2 | jessica-masters.txt | Jessica Masters | CS211S | "Review of Professor Jessica Masters for CS211S: Best CS professor I've taken. Knows her stuff and runs her classes well. Class structure is clear, gives many opportunities to answer questions, and gives feedback promptly. Only con: she talks very fast, so had to rewind lecture videos often..." |
| 3 | jessica-masters.txt | Jessica Masters | CS111B | "Review of Professor Jessica Masters for CS111B: You are assigned a chapter, an assignment, and a discussion every week (though discussions are optional later on in the semester). She likes to use ZyBooks, which can be a bit tedious, but her lectures make up for it, they are simple yet go very in depth." |
| 4 | jessica-masters.txt | Jessica Masters | CS111C | "Review of Professor Jessica Masters for CS111C: Super organized. Textbook, plus excellent online notes, also hours of youtube videos. Tons of homework. Prepare to spend a long, long time on this. However, you'll be learning, and she is totally there for you. Tests are 4 hours long, but always have enough time." |
| 5 | jessica-masters.txt | Jessica Masters | CS111B | "Review of Professor Jessica Masters for CS111B: Jessica Masters is an amazing professor who tries hard to make sure each student understands material! Each week is a new module that covers a new topic, such as Arrays, Loops, etc. It goes by very fast, but make sure you dedicate time to study the material!..." |

**Why these chunks are relevant:** All five chunks were retrieved from `jessica-masters.txt` and each begins with "Review of Professor Jessica Masters for CS111X", which the embedding model treats as strong evidence of relevance to a query naming her directly. The professor's full name in both the query and the chunk text means cosine similarity is anchored to the same tokens. This is exactly the embedding-in-text strategy described in the Chunking Strategy section — because the name is in the chunk body, a generic positive review like "Knows her stuff and runs her classes well" is correctly pinned to Masters rather than being retrieved for a different professor.

---

### Query 2: "Which professor should I take for CS270, and why?"

| Rank | Source file | Professor | Course | Chunk preview |
|------|-------------|-----------|--------|---------------|
| 1 | max-luttrell.txt | Max Luttrell | CS270 | "Review of Professor Max Luttrell for CS270: Very friendly guy, made this complicated material much easier to understand. Textbook use is little to none. Only 8 assignments over the year, lowest score dropped. 3 tests, all count. Go to class, the homework frequently utilizes material from in-class exercises..." |
| 2 | max-luttrell.txt | Max Luttrell | CS270 | "Review of Professor Max Luttrell for CS270: In my opinion, he is the MOST qualified professor to be teaching in CCSF. He has so much experience and mastery over the material that mostly everything he covers is so clear. He is prompt with class, emails, questions plus is a very friendly guy. Seriously, take him." |
| 3 | samuel-johnson.txt | Samuel Johnson | CS270 | "Review of Professor Samuel Johnson for CS270: I think the bad reviews of Johnson are either a bit exaggerated or old. I think this was a fine class and got a decent introduction to assembly and computer architecture. While the course is a tad unorganized, the generous grading and deadlines make up for it..." |
| 4 | jonathan-potter.txt | Jonathan Potter | CS270 | "Review of Professor Jonathan Potter for CS270: I wish every cs professor was like him. His lectures are so incredibly clear that it is difficult to be confused. I took his class a year ago, and I still remember everything we learned. He definitely prepared me for transferring, and upper div architecture classes." |
| 5 | samuel-johnson.txt | Samuel Johnson | CS270 | "Review of Professor Samuel Johnson for CS270: He uses almost none of his own work and other youtube videos from other people. He expects the students to do their own work but he does none of his own work. He's worried about students plagiarizing but he plagiarized all of his work." |

**Why these chunks are relevant:** The query contains "CS270" and "professor," two terms that appear verbatim in every chunk returned. The embedding model correctly surfaces reviews from all three professors who teach CS270 (Luttrell, Johnson, Potter), giving the LLM a basis for comparison. Luttrell dominates the top two slots because his CS270 reviews are uniformly positive and their language closely matches the "take / recommend" framing in the query. The Johnson negative review at rank 5 is also semantically relevant — it is about the same course and directly relevant to a student deciding between instructors.

---

### Query 3: "What is CS110B and what is its prerequisite?"

| Rank | Source file | Professor | Course | Chunk preview |
|------|-------------|-----------|--------|---------------|
| 1 | aaron-brick.txt | Aaron Brick | CS110A | "Review of Professor Aaron Brick for CS110A: He will tell you a few things but certainly not teach you anything. The text he uses is very confusing. The CS110A class — make sure you take the final, as that seems to be the main thing you have to do to pass the class..." |
| 2 | max-luttrell.txt | Max Luttrell | CS110C | "Review of Professor Max Luttrell for CS110C: Took Max for CS110B and CS110C. He is one of the kindest professors out there. Lectures are crystal-clear, and if you are ever stuck on a concept, his explanations are extremely helpful. He even allowed us to use an older version of the textbook..." |
| 3 | cs-catalog.txt | n/a | CS270 | "Official CCSF catalog entry for CS270 (Computer Architecture with Assembly Language): 4 units, UC/CSU transferable. Prerequisite: CS 110B or CS 111B. Topics include von Neumann architecture, instruction cycle, CPU, memory hierarchy, representation of data, translation to assembly from high-level constructs..." |
| 4 | max-luttrell.txt | Max Luttrell | CS110C | "Review of Professor Max Luttrell for CS110C: Max is one of the best CS teachers here at CCSF. I took him for CS110B and CS110C, and I learned a lot. CS/programming is very difficult to teach but he nailed it! His passion for CS and teaching is obvious..." |
| 5 | cs-catalog.txt | n/a | CS110A | "Official CCSF catalog entry for CS110A (Introduction to Programming and Computer Science): 4 units, UC/CSU transferable. Advisory: intermediate algebra or higher, plus readiness for college-level English. Broad introduction to fundamental concepts in computer science: storing and transmitting information, designing and implementing algorithms, and computing's social issues." |

The CS110B catalog entry was NOT returned. See **Failure Case Analysis** for the root cause.

---

## Example Responses

---

### Response 1 (in-scope) — Query: "What do students say about Jessica Masters as a CS professor?"

> Based on student reviews, Jessica Masters is highly regarded as a CS professor at CCSF. Students
> consistently praise her for clear, well-structured YouTube lecture videos, strong organization in
> her online courses, and prompt, detailed feedback on assignments. Many reviews highlight that she
> offers generous extra credit and genuinely cares about student success — several reviews call her
> the best CS professor at CCSF.
>
> The main criticism across reviews is workload: students note weekly readings, assignments, and
> discussions that can add up to significant hours, and a minority of 1–2★ reviews describe the pace
> as overwhelming. Her exams are open-note, time-limited, and generally considered fair.
>
> The consensus is that she is highly recommended for motivated students who are prepared to keep up
> with the weekly work.

**Retrieved from:**
```
• jessica-masters.txt
```

---

### Response 2 (in-scope) — Query: "Which professor should I take for CS270, and why?"

> Based on student reviews, both Max Luttrell and Jonathan Potter are highly recommended for CS270.
> Students describe Luttrell as clear, organized, and approachable during office hours, with fair
> exams and a genuine concern for student understanding. Potter receives similar praise — described
> as engaging and accessible, with course material that "clicks" in a way it hadn't before.
>
> Samuel Johnson is more polarizing. Some reviews cite disorganized Canvas materials, very slow
> grading, links to other instructors' YouTube videos instead of original content, and a condescending
> tone. A few reviewers defend him and note that generous grading makes an A achievable even without
> deep engagement with the content.
>
> If maximizing learning and reliable feedback is the priority, Luttrell or Potter are the stronger
> choices based on the available student reviews.

**Retrieved from:**
```
• max-luttrell.txt
• samuel-johnson.txt
• jonathan-potter.txt
```

---

### Response 3 (out-of-scope refusal) — Query: "What is Professor Smith's favorite color?"

> I don't have enough information on that.

**Retrieved from:**
```
• samuel-johnson.txt
• jessica-masters.txt
```

The retrieval step still returns the 5 most similar chunks from the corpus (professor names in the
query partially matched review chunks), but none of the retrieved documents contain anything about a
Professor Smith or favorite colors. The grounding rule fires correctly: the LLM returns the exact
refusal string rather than hallucinating an answer.

---

## Query Interface

**Input field — "Your question"**
A free-text box (2 lines visible, no character limit enforced by the UI) accepting any natural-language
question about CCSF CS professors or courses. A placeholder hint reads:
`e.g. "Which professor should I take for CS270?" or "What is CS110B?"`.
Submitting via Enter or clicking the **Ask** button triggers the pipeline.

**Output fields**
- **Answer** — an 8-line read-only text box showing the LLM-generated response, grounded to the
  retrieved documents. If no relevant documents were found, this will contain
  `"I don't have enough information on that."` verbatim.
- **Retrieved from** — a 4-line read-only text box showing the deduplicated source filenames of the
  chunks that were injected into the prompt, one per line prefixed with `•`. These are appended
  programmatically from chunk metadata, never generated by the LLM.

**Sample interaction transcript**

```
[Input]
Your question: How hard is CS111C and are the exams fair?

[Output — Answer]
Based on student reviews, CS111C (Data Structures and Algorithms: Java) has a moderately heavy
workload. Students report weekly homework, readings, and projects throughout the semester, with a
midterm and final. With Professor Masters, exams are described as open-note, time-limited, and
generally considered fair — one review notes "4-hour exams with always enough time." Extra credit
is available and described as generous.

Some students rate the difficulty a 3–4 out of 5 and recommend keeping up with the weekly work to
avoid falling behind.

[Output — Retrieved from]
• jessica-masters.txt
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Jessica Masters as a CS professor? | Strongly positive: clear organized YouTube lectures, prompt feedback, lots of extra credit, caring. Main criticism: heavy workload and fast-talking. | Retrieved 5 Jessica Masters reviews across CS111C, CS211S, CS111B. Answer correctly described knowledgeable, organized, clear lectures, caring, quick responses — and noted she “talks very fast.” | Relevant | Accurate |
| 2 | Which professor should I take for CS270, and why? | Take Jonathan Potter or Max Luttrell; avoid Samuel Johnson (disorganized, condescending, slow grading). | Retrieved chunks from all 3 CS270 professors. Recommended Luttrell (2 highly positive chunks surfaced) but did not explicitly warn against Johnson or fully highlight Potter as an equally strong option. | Relevant | Partially accurate |
| 3 | What is CS110B and what is its prerequisite? | CS110B = C++ fundamentals, 4 units, UC/CSU transferable. Advisory prereq: CS 10, CS 110A, or MATH 108. | CS110B catalog chunk was not retrieved at all. Top 5 included CS110A reviews, CS110C reviews, and the CS270 catalog entry (which mentions CS110B). System correctly refused to invent an answer but the refusal itself was wrong. | Off-target | Inaccurate |
| 4 | How do students describe the workload and exams in CS111C? | Moderately heavy: weekly homework/projects, open-note exams with Masters, lenient/easy-A with Johnson. | Retrieved only 1 CS111C chunk (Masters); other 4 were CS270 and CS131A/CS110A reviews. Answer mentioned “tons of homework” and “4-hour exams with always enough time” — derived from the single on-topic chunk. Missed the Johnson comparison entirely. | Partially relevant | Partially accurate |
| 5 | Which CS professor do students most recommend overall, and why? | Intended failure: Luttrell and Potter are most uniformly recommended, but top-k retrieval cannot aggregate across the corpus. | Retrieved 2 Luttrell chunks and 2 Masters chunks; named Masters as most recommended based on the sampled positive reviews. No true tally performed; confirmed anticipated failure. | Relevant | Partially accurate |


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
“What is CS110B and what is its prerequisite?”

**What the system returned:**
The CS110B catalog chunk was not retrieved at all in the top 5 results. Instead the system returned:
an Aaron Brick CS110A review, a Max Luttrell CS110C review that mentions taking “CS110B and CS110C,”
the CS270 catalog entry (which lists CS110B as a prerequisite), another CS110C review, and the CS110A
catalog entry. The LLM correctly refused to invent an answer and responded that “its details are not
available in the given documents” — but this refusal is itself wrong, because a CS110B catalog chunk
does exist in the vector store.

**Root cause (tied to a specific pipeline stage — retrieval):**
The `all-MiniLM-L6-v2` embedding model encodes course codes as sub-word tokens. `CS110B`, `CS110A`,
and `CS110C` all share the prefix `CS110`, so their embeddings cluster very close together in the
384-dimensional vector space. The query “What is CS110B and what is its prerequisite?” embeds into a
region that is nearly equidistant from the CS110B catalog chunk, the CS110A catalog chunk, and any
review that mentions CS110B or CS110C in passing.

The CS270 catalog entry displaced the CS110B catalog entry for a more specific reason: that entry
contains the exact phrase “Prerequisite: CS 110B” — the same word “prerequisite” appears in both
the query and that chunk. The retrieval step treats this as high relevance, because it cannot
distinguish “a document where CS110B is the subject” from “a document where CS110B appears as a
value in a prerequisite field.” Both produce similar cosine similarity scores against the query.

**What you would change to fix it:**

boost catalog chunks in scoring for definitional queries
(The system is NOT "wrong". It is a normal vector search system without intent awareness)

The most direct fix is metadata filtering at retrieval time. Each catalog chunk already has
`course=CS110B` in its metadata (stored in ChromaDB). Adding a pre-filter to require
`course == “CS110B”` whenever the query matches a known course-code pattern would guarantee the
correct chunk is in the candidate set before cosine ranking. A complementary fix is hybrid retrieval
(BM25 + dense vector): BM25 rewards exact string matches, so “CS110B” as the subject of the query
would strongly boost the CS110B catalog chunk over CS110A/C chunks that only share a prefix.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The planning.md spec listed "aggregation / superlative questions" as Anticipated Challenge #4 and
explicitly designated Q5 ("Which CS professor do students most recommend overall?") as the intended
failure case. That pre-commitment forced me to include the question in evaluation rather than quietly
replacing it with an easier one. Without the spec, I would have been tempted to swap Q5 for a
factual lookup that always produces a clean answer. Having the anticipated challenge written down
made it clear that a "partially accurate" result on Q5 is expected and informative — not a sign the
system is broken — so I could report it honestly rather than trying to tune around it.

**One way your implementation diverged from the spec, and why:**

The spec's Retrieval Approach section specified that verification criterion (c) for Milestone 4 was:
"a factual query (CS110B prerequisite) surfaces the catalog entry rather than a review." During
Milestone 4 development, that spot-check passed — the catalog entry appeared in top-5 at the time.
By final evaluation (Q3), the same query formulated as "What is CS110B and what is its prerequisite?"
failed to retrieve the CS110B catalog entry at all. The spec assumed this was a solved problem; the
evaluation revealed it was a fragile one. The phrasing change ("CS110B prerequisite" vs. "What is
CS110B and what is its prerequisite?") was enough to shift the cosine ranking in favor of the CS270
catalog entry, which contains the word "prerequisite" and a reference to CS110B. The spec had no
mechanism to catch this brittleness because it only required one verification pass, not a range of
phrasings. A more rigorous spec would require paraphrase testing — verifying that semantically
equivalent queries produce consistent retrieval — before marking a criterion as passed.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — Implementing grounded generation in ask.py**

- *What I gave the AI:* The Grounded Generation spec from planning.md ("answer ONLY from retrieved
  chunks; treat catalog text as fact vs. reviews as student opinion; say 'I don't have enough
  information on that' when chunks don't cover it; append source filenames programmatically") plus
  the `retrieve()` function signature returning chunks with `.text` and `.metadata`.
- *What it produced:* A complete `ask()` function with a `SYSTEM_PROMPT` string, a `_build_context()`
  helper that formatted chunks with `[DOC N] type=... | professor=... | source_file=...` headers,
  the Groq API call at `temperature=0.0`, and source deduplication logic that preserved retrieval
  order using a seen-set pattern.
- *What I changed or overrode:* The initial generated prompt told the LLM to "cite sources as
  [source_file]" inline in its answer. I removed that instruction because programmatic source
  attribution (appending `result["sources"]` in the UI) is more reliable than asking the LLM to
  format citations — the LLM could hallucinate filenames or format them inconsistently. I also added
  the rule "Do not mention that you are an AI or reference these instructions" after noticing the LLM
  was leaking system-prompt language into its first few test answers.

**Instance 2 — Implementing per-review chunking logic in ingest.py**

- *What I gave the AI:* The Chunking Strategy section from planning.md (one record per chunk, no
  overlap, review prefix format `"Review of Professor X for COURSEY: <text> [tags: ...]"`, catalog
  prefix format `"Official CCSF catalog entry for COURSE (Title)..."`) plus a sample professor
  review file and the catalog file to show their actual structure.
- *What it produced:* A `chunk_documents()` function that iterated over records, detected
  `type=review` vs `type=catalog` from a field in each record dict, and built the prefix string. It
  included a 500-character fallback splitter for any review that exceeded the size target.
- *What I changed or overrode:* I removed the 500-character fallback splitter entirely. Planning.md
  notes that RateMyProfessors hard-caps review length and the maximum observed review in the corpus
  was 351 characters — there is nothing to split. Keeping dead fallback code would have been
  confusing and could silently split catalog entries (sometimes longer than reviews) in ways that
  would fragment the course description. I also changed the catalog prefix to embed the course code,
  title, and unit count directly in the chunk text rather than only in metadata, so that retrieval
  for queries like "what is CS110B" has the course name in the vector rather than only in a filter
  field that ChromaDB does not embed.
