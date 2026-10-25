---
title: Deleting from RAG, vector stores and caches
description: When a product looks data up at answer time, forgetting is mostly ordinary deletion, if you can find every copy.
---

# Deleting from RAG, vector stores and caches

!!! oneline "In one line"
    When an AI product **looks data up** at answer time, forgetting someone is mostly ordinary deletion, but only if
    you find every copy: documents, chunks, embeddings, indexes, caches, logs and any model trained on them.

## Why it matters

Many AI assistants use **retrieval-augmented generation** (RAG). The language model does not memorise your company's
documents. Instead, a search step finds relevant passages in a database, and the model reads them while it answers.
So when a person asks to be forgotten, their data usually sits in that database, not in the model's weights.

That is good news: deleting from a database is [exact](retraining-gold-standard.md), cheap and easy to check. The bad
news is that RAG systems copy data into many places, and a deletion that misses one copy is not a deletion.

## A simple example

Removing a book from a library means more than taking it off the shelf. You also remove its catalogue card, the
photocopies in the reading room, the librarian's notes that quote it and the summary in the newsletter. Miss one, and
someone can still read the book.

## How it works

A RAG system answers a question in three steps: turn the question into an **embedding** (a list of numbers that
captures its meaning), find the stored chunks with the [nearest](../ml-basics/k-nearest-neighbours.md) embeddings, and
pass those chunks to the model. Each step keeps its own copy of the data.

### Where the copies live

| Copy | What to delete | The trap |
|---|---|---|
| **Source documents** | the original files or rows | other documents that quote them |
| **Chunks** | every passage cut from those documents | chunks are often stored separately from the source |
| **Embeddings** | the vector for each chunk | embeddings are not anonymous: the text can often be [reconstructed](https://arxiv.org/abs/2310.06816) from them |
| **Vector index** | the index entries | some indexes only *mark* an entry as deleted until the next compaction or rebuild |
| **Keyword index** | the search terms for those chunks | it is easy to forget the hybrid-search half |
| **Answer caches** | cached answers that used the chunks | a semantic cache can replay an old answer to a new question |
| **Logs and traces** | prompts, retrieved chunks and answers | logs often keep the full retrieved text |
| **Evaluation sets** | test questions built from the data | they get copied into notebooks and dashboards |
| **Backups** | the same data in snapshots | follow your backup retention rules, and record them |
| **Models trained on it** | fine-tunes, adapters or distilled models | now it *is* a weights problem: see [unlearning a fine-tune](unlearning-fine-tunes.md) |

### The steps

<ol class="steps" markdown>
<li markdown>**Tag everything at ingestion.** Give every chunk, embedding and cache entry the ID of its source document and of the person it is about. Without this lineage, you cannot find the copies later.</li>
<li markdown>**Delete by ID everywhere.** Remove the source, chunks, embeddings and keyword entries in one job.</li>
<li markdown>**Make the deletion real.** Compact or rebuild the vector index if it only marks entries as deleted.</li>
<li markdown>**Purge what was derived.** Clear cached answers and logs that contain the data.</li>
<li markdown>**Check.** Search for the person directly and with paraphrased questions; nothing should come back.</li>
<li markdown>**Record it.** Note what was deleted, where and when, as in [the enterprise playbook](enterprise-playbook.md).</li>
</ol>

!!! note "Retrieval or weights?"
    If the person's data was also in the model's pre-training data or a fine-tune, deleting it from the retrieval store
    is not enough. The model may still recall it from its weights, and that is the harder problem of
    [unlearning in language models](llm-unlearning.md).

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting the document but not its embeddings.** The chunks keep answering questions.
    - **Trusting a "deleted" flag.** Until the index is compacted, the entry may still be stored, and sometimes found.
    - **Forgetting the semantic cache.** It can serve yesterday's answer, with the person's data in it.
    - **Treating embeddings as anonymous.** They encode the meaning of the text, and often enough of the text itself.

## Key takeaways

- In a RAG system, most personal data lives in the retrieval store, where deletion is exact and cheap.
- The hard part is finding every copy: chunks, embeddings, indexes, caches, logs and backups.
- Tag every derived copy with its source at ingestion, so that deletion can follow the lineage.
- If the data also reached the model's weights, retrieval deletion is not enough.

## Quiz

```quiz
- q: In a RAG system, where does a person's data usually live?
  options:
    - Only in the language model's weights
    - In the retrieval store, as documents, chunks and embeddings
    - Nowhere; RAG never stores data
  answer: 1
  why: RAG looks passages up at answer time, so the data sits in the store the search step reads from.
- q: Why is deleting the source document often not enough?
  options:
    - Chunks, embeddings, caches and logs keep their own copies.
    - Documents cannot be deleted.
    - The model memorises every document it reads.
  answer: 0
  why: Each stage of the pipeline copies the data. Every copy must be found and removed.
- q: Are embeddings a safe, anonymous form of the text?
  options:
    - Yes, they are just numbers.
    - No, the original text can often be reconstructed from them.
  answer: 1
  why: Embeddings capture the meaning of the text closely enough that it can often be recovered, so treat them as personal data.
- q: What makes deletion across a RAG pipeline possible?
  options:
    - Tagging every chunk, embedding and cache entry with its source at ingestion
    - Retraining the language model
    - Turning off the cache for a day
  answer: 0
  why: Lineage lets one deletion request reach every derived copy.
```

## Try it

- Read [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md): a vector store is a nearest-neighbour search, and
  deleting from it is the same exact subtraction as in [Lesson 01](../lessons/01-knn-and-naive-bayes.md).
- Sketch the data map for a chatbot you know. How many copies of one document can you find?
