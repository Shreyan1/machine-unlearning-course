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

## The story

Kestrel Home, a fictional online shop, runs a support chatbot that uses **retrieval-augmented generation** (RAG, Lewis
et al. 2020). It does not learn the old support tickets into its weights. It searches them when a question comes in
and answers from the best matches. **Fiona Kowalczyk** wrote 4 of the 230 tickets. They hold her phone number, her
address, the last digits of her card and the fact that she was in hospital. She asks for all her tickets to be erased.

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

## Key results

**Deleting the tickets is not deleting the person.** With the tickets gone from the database, the chatbot still gave
out her phone number (from the answer cache), her address, her hospital stay and her card digits (from the chunks).
Five of the six stores still held her data.

**Embeddings are not anonymous.** From her 10 stored vectors, a simple attack with a word list recovered 56 of her 77
different words with no wrong guesses. Only 2 of the 100 possible phone numbers fit her vectors, and one of them was
hers. Morris et al. (2023) showed that neural embeddings can be turned back into text too.

**The tombstone trap.** Deleting by owner ID hid her chunks from all 230 test searches. But the vector index still
stored 440 rows, 10 of them hers and readable from a backup, and the keyword index still counted "kowalczyk" in 8
chunks when only 2 searchable chunks held it. Compaction removed both.

**An approximate index has a trained part.** In an IVF index with 16 lists, the centroids kept a weight of 0.1643 in
the slot of her phone number after her rows were removed. Only a rebuild brought it to zero.

**Tags miss mentions.** After deleting by her ID, the chatbot still said she lived at 14 Larch Row and was in
hospital. The text was in her neighbour's ticket, which carries the neighbour's ID. A scan for her details found it in
all six stores, and redacting the mention removed it.

| Check against the stack built without her | Result |
|---|---|
| Ticket database and chunk store | ✅ identical |
| Vector index, every number | ✅ identical |
| Keyword index, every count | ✅ identical |
| Search results for 230 questions | ✅ identical |
| IVF centroids after a rebuild | ✅ identical |
| hit@3 for the other customers | ✅ identical (74.8% before, 73.9% after) |

**The twist.** Kestrel Home had also trained a small n-gram model on the tickets to draft replies. Cleaning the
stores did nothing to it. It still completed "fiona kowalczyk, tel" with her number, at the maximum exposure of 6.64
bits. Exact n-gram unlearning of her tickets dropped the exposure to 0.1 bits, but the model still knew her address
from the neighbour's ticket. After that ticket was swapped for its redacted version, the model's table was identical to
one trained on the erased database.

## Concepts used here

- [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md)
- [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)
- [The enterprise playbook](../unlearning/enterprise-playbook.md)

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
```

## You have finished the course

Test yourself with the [final test](../quizzes/final.md) and the [practice problems](../practice.md). And keep asking
the course's first question about any new model. **What would make forgetting a subtraction, and how close can we get?**
