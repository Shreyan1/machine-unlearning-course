---
title: "Lesson 21 · RAG and vector stores"
description: A support chatbot that looks old tickets up. Deleting the tickets leaves the person in chunks, vectors, caches and logs. Deleting by ID everywhere and compacting is exact, but not for a model trained on the tickets.
---

# Lesson 21 · RAG and vector stores, deleting every copy

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 8 · Extensions</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/21-RAG-and-Vector-Stores.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/21-RAG-and-Vector-Stores.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 45 minutes · 3 checkpoints"
    By the end of this lesson you can

    - count every copy a retrieval chatbot makes of one customer, and show that deleting her tickets misses most of them,
    - catch the tombstone trap and the neighbour's ticket trap, and fix both,
    - prove that the cleaned stores equal a stack built without her, and find the one copy that proof cannot reach.

## The story

Kestrel Home, a fictional online shop, runs a support chatbot that uses **retrieval-augmented generation**
(RAG, Lewis et al. 2020). It does not learn the old support tickets into its weights. It searches them when a question comes in
and answers from the best matches. **Fiona Kowalczyk** wrote 4 of the 230 tickets. They hold her phone number, her
address, the last digits of her card and the fact that she was in hospital. She asks for all her tickets to be erased.

That sounds like the easy case of Lesson 01, where the k-NN model *was* its data and forgetting meant deleting rows.
But a RAG system does not keep one copy of a ticket. It cuts it into chunks, turns each chunk into numbers, indexes
it twice, saves the answers it gives and logs every question. Health data is a special category of personal data
(GDPR Art. 9), so one leftover copy is a real leak.

The whole retrieval stack is built in plain NumPy. Tickets are cut into chunks of 24 words, each chunk gets a hashed
bag-of-words embedding with 4,000 numbers, and a search combines a vector index with a BM25 keyword index. An answer
cache and logs record a month of questions.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train.** Build the stores, which are the ticket database, 440 chunks, a vector index, a keyword index, an answer cache and logs.</li>
<li markdown>**Show the issue.** Delete her tickets from the ticket database only, and read her data back from the other stores, including her own vectors.</li>
<li markdown>**Untrain.** Delete by owner ID from every store, catch the tombstone trap, compact and see why an approximate index needs a rebuild.</li>
<li markdown>**Show the result.** Ask the same questions again, find a mention of her in someone else's ticket and check search quality for everyone else.</li>
<li markdown>**Prove it.** Compare every store with a stack built without her, then test a model that was trained on the tickets.</li>
</ol>

## What each step teaches

**Step 1. Build the stores.** Nothing is trained by gradient descent here. "Training" a RAG system means building its
stores, and every chunk, vector and keyword entry carries its **owner**, the customer it came from. That tag is the
lineage of Lesson 17, and without it a deletion has no way to find the copies.

**Step 2. Delete the tickets only.** This is the usual first answer to "erase my tickets". It shows how many copies
the other steps of the pipeline made, and the read-back attack shows that the stored numbers are not anonymous.

**Step 3. Delete by ID everywhere.** One call uses the tags to reach every store. Then the lesson looks at *how* the
indexes deleted her, which is where the tombstone trap and the approximate index's trained part show up.

**Step 4. Ask again.** The same questions test the cleaned chatbot. The one that still leaks teaches that tags find
what came from a person, not what is about her. A check on everyone else's search quality comes next.

**Step 5. Prove it.** For retrieval the gold standard is simple. Build every store from scratch on the erased
database and compare. Then the lesson turns to a model trained on the same tickets, which no store deletion touches.

??? deep "Go deeper · how the search in step 1 works"
    Each ticket is cut into windows of 24 words that overlap by 8. Each word of a chunk is sent by a fixed hash to one
    of 4,000 slots with a plus or minus sign, and the list is scaled to length 1. The vector index returns the rows with
    the highest cosine similarity to the question, which is the nearest-neighbour search of Lesson 01. The keyword
    index scores chunks with BM25, where rare words count more than common ones. The two lists are merged by
    reciprocal rank fusion, where each chunk gets 1 / (60 + rank) from each list, and the top 3 chunks go to the
    answerer. The answerer copies the sentence that shares the most words with the question.

## Key results

<div class="stats">
<div class="is-bad"><strong>5 of 6</strong><span>stores still held her after her tickets were deleted</span></div>
<div class="is-bad"><strong>56 of 77</strong><span>of her words read back from her 10 vectors</span></div>
<div class="is-good"><strong>Identical</strong><span>every store, against a stack built without her</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>her number in the drafting model, stores already clean</span></div>
</div>

**Deleting the tickets is not deleting the person.** With the tickets gone from the database, the chatbot still gave
out her phone number (from the answer cache), her address, her hospital stay and her card digits (from the chunks).
Five of the six stores still held her data.

**Embeddings are not anonymous.** From her 10 stored vectors, a simple attack with a word list recovered 56 of her 77
different words with no wrong guesses. Only 2 of the 100 possible phone numbers fit her vectors, and one of them was
hers. Morris et al. (2023) showed that neural embeddings can be turned back into text too.

??? checkpoint "Checkpoint 1 · After the naive deletion a stranger asks for Fiona's phone number and gets it. Which store answered, and why?"
    **The answer cache.** A support agent had asked "fiona kowalczyk phone number" during the month, and the answer
    was saved. The stranger's question was close enough to it (a cosine of 0.8 or more) that the old answer was served
    again, with no search at all. Deleting her tickets never touched the cache.

**The tombstone trap.** Deleting by owner ID hid her chunks from all 230 test searches. But the vector index still
stored 440 rows, 10 of them hers and readable from a backup, and the keyword index still counted "kowalczyk" in 8
chunks when only 2 searchable chunks held it. Compaction removed both.

**An approximate index has a trained part.** In an IVF index with 16 lists, the centroids kept a weight of 0.1643 in
the slot of her phone number after her rows were removed. Only a rebuild brought it to zero.

**Tags miss mentions.** After deleting by her ID, the chatbot still said she lived at 14 Larch Row and was in
hospital. The text was in her neighbour's ticket, which carries the neighbour's ID. A scan for her details found it in
all six stores, and redacting the mention removed it.

??? checkpoint "Checkpoint 2 · Why redact the neighbour's ticket instead of deleting it?"
    **Because the rest of it is the neighbour's data.** The ticket is about the neighbour's own toaster and carries
    the neighbour's ID and phone number. Replacing Fiona's details with "[removed]" takes her out and keeps theirs.
    Only 2 chunks had to be embedded again, against 429 for a full rebuild.

| Check against the stack built without her | Result |
|---|---|
| Ticket database and chunk store | ✅ identical |
| Vector index, every number | ✅ identical |
| Keyword index, every count | ✅ identical |
| Search results for 230 questions | ✅ identical |
| IVF centroids after a rebuild | ✅ identical |
| hit@3 for the other customers | ✅ identical (74.8% before, 73.9% after) |

Read the rows as one proof. The first three rows say the cleaned stores hold exactly the same data as stores that
never saw her, down to the last number. The fourth says the chatbot behaves the same for every question. The fifth
says the rebuilt IVF index has no trace of her. The last row matters most to everyone else. **hit@3** is how often a
customer's own ticket is among the 3 chunks found. It fell from 74.8% to 73.9%, because 2 of 226 questions lost their
ticket, and the stack built without her loses the same two. So the drop is the right answer, not damage.

**The twist.** Kestrel Home had also trained a small n-gram model on the tickets to draft replies. Cleaning the
stores did nothing to it. It still completed "fiona kowalczyk, tel" with her number, at the maximum exposure of 6.64
bits. Exact n-gram unlearning of her tickets dropped the exposure to 0.1 bits, but the model still knew her address
from the neighbour's ticket. After that ticket was swapped for its redacted version, the model's table was identical to
one trained on the erased database.

??? checkpoint "Checkpoint 3 · Every store now matches the stack built without her. Why was the drafting model still a problem?"
    **It is a model, not a store.** It learnt from the tickets into its own table of counts, so deleting the tickets
    from the stores changed nothing in it. It needed its own unlearning, and it also needed the neighbour's redacted
    ticket, because it had learnt her address from that one too. A neural model would have no exact subtraction, which
    is the hard case of Lesson 16.

## Limits of this lesson

**A small, fictional shop.** There are 230 tickets and the stack is plain NumPy. Real vector databases each have their
own rules for deletes, merges and backups.

**Hashed embeddings are the easy case.** The hash is public, so reading the words back is simple. For neural
embeddings the lesson relies on Morris et al. (2023).

**The cache and logs meet a weaker test.** They are a history of past questions and cannot be rebuilt "as if she had
never been there". The lesson checks that no entry was built from her data or holds her details.

**A scan finds only what you search for.** A mention spelt another way needs its own entry in the list, and backups
are not modelled.

## Concepts used here

- [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md)
- [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)
- [The enterprise playbook](../unlearning/enterprise-playbook.md)

## Notes to take

!!! notes "Notes to take"
    - **Stores, not weights.** RAG looks tickets up at answer time, so Fiona's data sits in stores.
    - **Copies.** Tickets, 10 chunks, 10 vectors, 10 keyword entries, 2 saved answers and 2 log records.
    - **Naive deletion.** Deleting her tickets cleaned 1 store of 6, and the cache still served her number.
    - **Embeddings.** 56 of her 77 words came back from her vectors. Treat them as personal data.
    - **Tombstones.** Delete by ID only marks index rows. Compact, and rebuild any approximate index.
    - **Mentions.** Tags missed her neighbour's ticket. Scan for her details and redact.
    - **Proof.** After delete, redact and compact, every store matched the stack built without her, bit for bit.
    - **Trained copies.** The drafting model still gave her number at 6.64 bits until it was unlearnt too.

## Quiz

```quiz
- q: Fiona's tickets were deleted from the ticket database only. How many of the six stores still held her data?
  options:
    - None
    - One
    - Five
  answer: 2
  why: The chunks, vector index, keyword index, answer cache and logs all kept their own copies.
- q: How did the chatbot still give out her phone number after the naive deletion?
  options:
    - From the answer cache, because the question was close to an earlier one
    - From the ticket database
    - The language model guessed it
  answer: 0
  why: A semantic cache serves an old answer to any question that is similar enough.
- q: What is the tombstone trap?
  options:
    - A deleted row is only marked and stays stored, and in backups, until compaction
    - Deleted rows come back after a restart
    - Compaction deletes other people's data
  answer: 0
  why: Her 10 vectors were hidden from search but still stored and readable until the index was compacted.
- q: Why did deleting by Fiona's owner ID miss her address?
  options:
    - It was in her neighbour's ticket, which carries the neighbour's ID
    - The ID was spelt wrongly
    - Addresses are never deleted
  answer: 0
  why: Tags find what came from a person, not what is about them, so a scan for her details is needed too.
- q: After deletion, redaction and compaction, how did the stack compare with one built without her?
  options:
    - Identical in every store, bit for bit
    - About 95% the same
    - Better for everyone
  answer: 0
  why: Deleting from a store is exact unlearning, like deleting rows from k-NN in Lesson 01.
- q: Was the drafting model trained on the tickets clean after the stores were cleaned?
  options:
    - Yes, because the tickets were deleted
    - No, it still recited her number until it was unlearned
  answer: 1
  why: Deleting from a store does nothing to a model's weights or counts. Every trained copy needs its own unlearning.
- q: Fiona's rows were removed from the lists of the IVF index. Why did the centroids still hold a trace of her phone number?
  options:
    - Her rows had been copied into every list
    - The centroids are averages that included her rows, and only a rebuild works them out again
    - IVF indexes cannot remove rows at all
  answer: 1
  why: The largest centroid weight in her number's slot stayed at 0.1643 after removal. A rebuild on the 430 rows left brought it to 0.
- q: After the deletion, hit@3 for the other customers fell from 74.8% to 73.9%. What does that tell you?
  options:
    - The deletion damaged the search for everyone else
    - Fiona's own questions were still being counted
    - Nothing is wrong, because the stack built without her loses the same 2 questions
  answer: 2
  why: The right result is whatever a stack that never held her data gives. Here it matches exactly.
- q: Why should deletion checks be run on a copy, or with caching and logging switched off?
  options:
    - Test questions that name her are cached and logged, so they make new copies of her data
    - Checks are too slow on the live chatbot
    - The cache gives wrong answers during checks
  answer: 0
  why: In the lesson the probe questions are asked with recording off. A real chatbot would save every one of them, and each contains her name.
```

## Want to go further?

!!! levelup "Level up"
    You can now find every copy a retrieval chatbot makes of a person, delete them all and prove the result. Next quest,
    [Lesson 22 · Surgical weight editing](22-surgical-weight-editing.md), where the data is in the weights and a few
    edited numbers claim to remove it.

In November 2026 an AI model edited 0.016% of another model's weights and fixed a fault with no training. Lesson 22
asks whether a surgical edit like that can forget one person, and attacks the edits that look as if they do.

[On to Lesson 22, surgical weight editing :material-arrow-right:](22-surgical-weight-editing.md){ .md-button }
