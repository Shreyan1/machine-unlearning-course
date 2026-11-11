---
title: Deleting from RAG, vector stores and caches
description: When a chatbot looks documents up at answer time, forgetting a person is ordinary deletion, as long as you find and remove every copy the system made.
---

# Deleting from RAG, vector stores and caches

!!! oneline "In one line"
    Some chatbots do not learn your documents. They **look them up** every time they answer. To forget a person there,
    you delete their data, but first you must find **every copy**.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - list the copies a RAG chatbot makes of every document, and say why each one is easy to miss,
    - explain why a "deleted" mark, a stored embedding and an approximate index each keep a person's data,
    - plan a deletion that matches a chatbot built without the person, and say where that deletion stops.

## Why it matters

Many company chatbots use **retrieval-augmented generation**, or **RAG** (Lewis et al. 2020). Before the chatbot
answers, it searches a store of documents, picks the few that match the question and reads them. The language model
itself never learnt those documents.

So when a customer asks to be forgotten, their data usually sits in the store, not inside the model. That is good
news, because deleting from a store is [exact](retraining-gold-standard.md) and cheap. The catch is that a RAG system
quietly makes many copies of every document, and a deletion that misses one copy is not a deletion.

The documents are often sensitive. In Lesson 21 a customer's tickets mention a hospital stay, which is health data
under GDPR Art. 9. A leftover copy is a real leak, because RAG systems can be pushed into repeating the text they
retrieve (Zeng et al. 2024).

## A simple example

!!! simply "Explain it simply"
    Think of a help desk with a filing cabinet of old letters. To answer quickly, the staff photocopied useful
    paragraphs into a **binder**, wrote an **index card** for every important word, kept a **notebook** of answers
    they gave and wrote a **diary** of every call.

    Throwing a customer's letters out of the cabinet leaves her words in the binder, on the cards, in the notebook and
    in the diary. Forgetting her means finding every copy.

Each part of the picture is a real store.

| In the help desk | In a RAG chatbot |
|---|---|
| The filing cabinet | The ticket database, where the original documents live |
| The binder of photocopied paragraphs | The chunk store |
| The index cards | The two search indexes, one that finds passages by meaning and one by word |
| The notebook of past answers | The answer cache |
| The diary of calls | The logs |
| A nightly photocopy of the whole office | The backups |
| New staff who learnt the letters by heart | A model trained on the tickets |

The last row is different from the others. Throwing out the letters does nothing to what that person remembers.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [**RAG**](../start-here/glossary.md#r) | A chatbot that searches a store of documents and answers from what it finds | Kestrel Home's support chatbot searches 230 old tickets |
| **Chunk** | A short passage cut from a document. Search works on chunks | Windows of 24 words that overlap by 8 words |
| [**Embedding**](../start-here/glossary.md#e) | A list of numbers that stands for a chunk. Similar chunks get similar numbers | 4,000 numbers for every chunk in Lesson 21 |
| [**Vector index**](../start-here/glossary.md#v) | The table of embeddings that finds the chunks nearest to a question | 440 rows of 4,000 numbers |
| [**Tombstone**](../start-here/glossary.md#t) | A "deleted" mark on a row. Searches skip the row, but it is still stored | 10 tombstones for Fiona's 10 vectors |
| **Compaction** | Rewriting an index without its marked rows, so that they are really gone | The vector index went from 440 stored rows to 430 |
| [**Lineage tag**](../start-here/glossary.md#l) | The ID of the document and person a copy came from, attached when it is made | Every chunk of Fiona's carries her ID, C-FIONA |

## How it works

### How a RAG chatbot answers

1. **Cut.** Every document is cut into short passages called **chunks**. This is the binder. In Lesson 21 each chunk
   is a window of 24 words, and neighbouring chunks share 8 words.
2. **Describe.** Each chunk gets an **embedding**, a list of numbers that describes what it is about. Chunks about the
   same thing get similar numbers, a bit like a postcode for meaning.
3. **Index.** A **vector index** finds chunks with similar numbers, which is the nearest-neighbour search of
   [k-NN](../ml-basics/k-nearest-neighbours.md). A **keyword index** finds chunks with the same words and scores them
   with **BM25**, a standard score that gives rare words more weight. These are the index cards.
4. **Answer.** The two result lists are merged and the best 3 chunks are read. The answer may be saved in an **answer
   cache**, so that a similar question later gets the same answer without a new search. This is the notebook.
5. **Log.** Questions, chunks and answers are written to **logs**. This is the diary.

**For Fiona this means** that her 4 tickets became 10 chunks, 10 vectors and 10 keyword entries, and a month of
questions added 2 saved answers and 2 log records. Lesson 21's answerer simply copies the best-matching sentence,
which is a fair stand-in, because real language models also copy names and numbers from what they read.

<!-- diagram: rag-and-vector-stores -->

The figure shows the ticket database copied into six stores, namely the chunks, the vector index, the keyword index,
the answer cache, the logs and the backups. Below them sits a model trained on the same tickets. A yellow dot marks
each copy of Fiona's data. The animation plays four stages. Every ticket is copied into the stores, a deletion by her
ID only marks her rows, compaction removes the marked rows for real, and the trained model still holds its own copy.

### How an embedding is made in Lesson 21

Real systems use a neural network to turn text into numbers. Lesson 21 uses a simpler recipe called a **hashed bag of
words**. Each word is sent by a fixed rule to one of 4,000 slots, with a plus or minus sign, and the slot is counted up
or down. "Bag of words" means that the order of the words is thrown away. Only which words are present, and how
often, survives.

That is enough to read the words back. A slot is non-zero only if some word of the chunk landed there, and the rule is
public. So an attacker with a stored embedding can test each word on a list and keep those whose slot is lit. Across
Fiona's 10 embeddings the attack recovered **56 of her 77 different words**, with no wrong guesses. Of the 100
possible phone numbers, only 2 fitted her embeddings, and one of them was hers.

**For Fiona this means** that her stored numbers are her text. They must be deleted with it.

??? deep "Go deeper · the recipe step by step, and why the attack works"
    1. Start with a list of 4,000 zeros. Each position is called a **slot**.
    2. Split the chunk into lower-case words and numbers. The phone number 555-0147 becomes "555" and "0147".
    3. Send each word through a fixed **hash function**, a rule that always turns the same word into the same number.
       That number picks one slot and a sign, plus or minus.
    4. Add 1 to that slot, or take 1 away if the sign is minus. A word that appears twice changes its slot twice.
    5. Scale the whole list so that its length is 1. The similarity of two chunks is then the sum of their
       slot-by-slot products, called the **cosine similarity**. The answer cache reuses an old answer when a new
       question scores 0.8 or more.

    **The attack.** The attacker's list had 165 words from other customers' tickets and public lists of names and
    streets. The 21 words it missed, such as "daughter" and "operation", were simply not on the list. The extra phone
    number, 555-0196, fitted only because its slot is shared with a word in her chunks, a **hash collision**.

    **Neural embeddings.** They are harder to read, but Morris et al. (2023) trained a model that turns them back into
    text, and it rebuilt most short texts word for word.

### Where the copies hide

| Copy | Why it is easy to miss |
|---|---|
| **Documents** | Someone else's document may mention her too |
| **Chunks** | They are often kept apart from the documents |
| **Embeddings** | People think numbers are anonymous, but the words can often be worked back out |
| **Indexes** | Many only **mark** a row as deleted until they are cleaned up |
| **Answer cache** | It can give an old answer, with her data in it, to a new question |
| **Logs and backups** | They keep the full text unless you limit them |
| **Models trained on the data** | Now it is a weights problem, not a store problem |

### Two traps

**The deleted mark.** Many indexes do not remove a row when you delete it. They put a "deleted" mark on it, called a
**tombstone**, and skip it in searches. It is like crossing out a name in a register. The name is still there, and
still in tonight's backup, until the register is rewritten without it. Rewriting an index without its marked rows is
called **compaction**.

??? deep "Go deeper · why indexes only mark rows"
    Writing a small mark is much faster than removing a row from the middle of a big file. Search engines built on
    Lucene, such as Elasticsearch, behave like this until their pieces are merged. A keyword index has the same problem
    in its word counts. In Lesson 21 it still counted "kowalczyk" in 8 chunks when only 2 searchable chunks held the
    word, so its scores were worked out as if she were still there.

**Numbers that can be read back.** Put this together with the embedding attack above, and a tombstoned embedding in a
backup is not harmless numbers. It is her text.

??? checkpoint "Checkpoint 1 · Fiona's 10 vectors are deleted by her ID on Monday, and the nightly backup runs before compaction. What does the backup hold?"
    **Her text, in effect.** The vector index still stores all 440 rows, 10 of them hers and marked as tombstones. In
    Lesson 21 one tombstoned row, read from a copy of the index, still gave back "air arrived broken for from fryer
    hello hospital i in my not order". So compaction must be part of the deletion job, and the date when that backup
    expires must be written down.

### Why an approximate index keeps a trace

With millions of chunks, comparing a question with every row is too slow, so real systems use an **approximate
nearest-neighbour** index. One common kind, the **inverted file** or **IVF** (Jégou et al. 2011), groups the
embeddings into lists. Each list has a **centroid**, the average of its embeddings, and a search looks only inside the
lists whose centroids are closest to the question.

The centroids are averages of the stored data, so they are a small **trained model**, and Fiona is part of them. Think
of a summary page at the front of the binder, written from all the letters. Taking her letters out does not rewrite
the summary. Only a **rebuild** does.

**For Fiona this means** that the largest centroid weight in the slot of her phone number's last four digits, "0147",
was 0.1643. It stayed at exactly 0.1643 after her 10 rows were removed from the lists. Only a rebuild on the 430 rows
that are left brought it to 0.0000.

??? deep "Go deeper · how the IVF index is built, and graph indexes"
    The lists are made with k-means, a method that puts similar points together. In Lesson 21 the IVF index had 16
    lists and searched the 4 closest. It found 75% of the exact top 3 results, which is the usual price of speed. A
    rebuild runs k-means again on the rows that are left, so the averages are worked out without her.

    Graph indexes such as HNSW have the same problem in another form. A deleted point is often only marked, and it still
    helps steer searches until the graph is rebuilt.

### The neighbour's ticket trap

After deleting by Fiona's ID and compacting, nothing tagged with her ID was left. Yet a stranger who asked "who lives
at 14 larch row?" still heard "with my neighbour fiona kowalczyk at 14 larch row, but she is in hospital." That
sentence came from her neighbour's ticket about a toaster left with Fiona. The ticket carries the neighbour's ID, so a
deletion by Fiona's ID never touched it.

The rule to remember is that **tags find what came from a person, not what is about them**. So the last check must
not rely on the tags. Lesson 21 searched the raw contents of every store for four of her details, namely "kowalczyk",
"555-0147", "larch row" and "7731". The fix is to **redact**, not to delete. Her details become "[removed]" and the
rest of the ticket stays, because it is the neighbour's own data.

??? checkpoint "Checkpoint 2 · After deleting by her ID and compacting, every store shows 0 items tagged C-FIONA. Can you sign the request off?"
    **No.** A count of tags only finds what came from her. The scan for her details in Lesson 21 still found the
    neighbour's ticket, its 2 chunks in both indexes, 1 saved answer and 1 log record. Redact her details in those,
    compact again, and only then is the scan empty in all six stores.

### The steps

<ol class="steps" markdown>
<li markdown>**Label every copy when you make it.** Each chunk, embedding, saved answer and log line carries the ID of the document and of the person it came from. This is the lineage of [Lesson 17](../lessons/17-enterprise-playbook.md).</li>
<li markdown>**Delete by that label everywhere,** in one job. Include the answer cache, which is the copy people most often forget.</li>
<li markdown>**Compact or rebuild the indexes,** so the marked rows are really gone. An approximate index needs a full rebuild, because its centroids or graph were built from her data.</li>
<li markdown>**Clear saved answers and logs** that contain the data. Keep logs for a short time, and write down when the backups that still hold the data will expire.</li>
<li markdown>**Check without the label.** Search every store for the person's name and details, because other people's documents may mention them. Redact any mention you find.</li>
<li markdown>**Follow the data into models.** Any model trained or fine-tuned on the same documents needs its own unlearning.</li>
<li markdown>**Record it.** Note what was deleted, where and when, as in [the enterprise playbook](enterprise-playbook.md).</li>
</ol>

## A worked example

Kestrel Home is a fictional online shop for kitchen appliances. Its support chatbot searches 230 old tickets from 81
customers. **Fiona Kowalczyk** wrote 4 of them. They hold her phone number (555-0147), her address (14 Larch Row), the
last digits of her card (7731) and the fact that she was in hospital for an operation. She asks for all of it to be
erased. Here is her data's journey through [Lesson 21](../lessons/21-rag-and-vector-stores.md).

1. **Chunking.** Her first ticket is 52 words long, so windows of 24 words that start 16 words apart cut it into 3
   chunks. In all she has 10 chunks out of 440.
2. **A month of use.** Customers ask 63 questions, each answered, cached and logged. Two involve her, including a
   support agent who asked "fiona kowalczyk phone number" and got it.
3. **The naive deletion.** Only her 4 tickets are deleted. A stranger asks "phone number for fiona kowalczyk please",
   which is close enough to the agent's question that the cache serves her number again.
4. **Delete by her ID.** One call removes 4 tickets, 10 chunks, 10 vectors, 10 keyword entries, 2 saved answers and 2
   log records, but the indexes only mark theirs. Compaction brings the vector index from 440 rows to 430.
5. **The scan and the proof.** A search for her details finds the neighbour's ticket, which is redacted. The cleaned
   stack then matches one built from scratch on the erased database, bit for bit. It embedded only 2 chunks again,
   where a full rebuild embeds 429.

Deleting her tickets alone cleaned one store out of six. Deleting by ID without compaction still left her in both
indexes. And a count of her tags misses the neighbour's ticket, which only the scan finds.

??? deep "Go deeper · items tagged with her ID after each kind of deletion"

    | Store | Before | Delete her tickets only | Delete by ID, tombstones | Delete by ID and compact |
    |---|---|---|---|---|
    | Ticket database | 4 | 0 | 0 | 0 |
    | Chunk store | 10 | 10 | 0 | 0 |
    | Vector index | 10 | 10 | 10 | 0 |
    | Keyword index | 10 | 10 | 10 | 0 |
    | Answer cache | 2 | 2 | 0 | 0 |
    | Logs | 2 | 2 | 0 | 0 |

## What Lesson 21 found

<div class="stats">
<div class="is-bad"><strong>5 of 6</strong><span>stores still held her after her tickets were deleted</span></div>
<div class="is-bad"><strong>56 of 77</strong><span>of her words read back from her embeddings</span></div>
<div class="is-good"><strong>Bit for bit</strong><span>the cleaned stack equals one built without her</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>her number's exposure in a model trained on the tickets, stores already clean</span></div>
</div>

**Search quality for everyone else.** Each other customer asks about one of their own tickets, and **hit@3** is how
often that ticket is among the 3 chunks found (random picks would hit about 1.3%). It was 74.8% before the deletion
and 73.9% after, because 2 of the 226 questions lost their ticket. The chatbot built without her loses the same two,
so the small drop is the correct answer, not damage.

**The model trained on the same tickets.** Kestrel Home had also trained a small n-gram model, a table of counts that
predicts the next character, to draft replies. Cleaning the stores did nothing to it. It still completed "fiona
kowalczyk, tel" with her number, at an **exposure** (Carlini et al. 2019) of 6.64 bits, the maximum. That means her
number was its top guess among the 100 possible ones.

??? checkpoint "Checkpoint 3 · The stores now match a stack built without Fiona, bit for bit. Has Kestrel Home finished her request?"
    **Not yet.** The deletion is exact for the stores only. The drafting model still gave her number at 6.64 bits.
    Step 6 of the plan, following the data into models, catches it. Subtracting her 4 tickets from the table of counts
    dropped the exposure to 0.1 bits, but the model still knew her address from the neighbour's ticket. Only after that
    ticket was swapped for its redacted version was the model identical to one trained on the erased database. A
    neural model has no such subtraction, which is the harder problem of
    [unlearning in language models](llm-unlearning.md).

## Limits

**A small, fictional shop.** The lesson has 230 tickets and builds the stack in plain NumPy. Real vector databases each
have their own rules for deletes, merges and backups, so check how yours removes a row and when.

**A scan finds only what you search for.** A mention spelt another way, such as "f. kowalczyk on larch row", needs its
own entry in the list.

??? deep "Go deeper · three more limits"
    **Hashed embeddings are the easy case.** The hash is public, so reading words back is simple. For neural
    embeddings the lesson relies on Morris et al. (2023).

    **The cache and logs meet only a weaker test.** They are a history of past questions, which cannot be rebuilt "as
    if she had never been there", because other people's questions would have had other answers. The lesson checks
    that no entry was built from her data or contains her details, not that they match bit for bit.

    **Backups are not modelled.** Record when each backup that still holds the data will expire.

!!! tip "What to do in practice"
    - Follow [the steps](#the-steps) as one deletion job, and finish compaction and any rebuild inside the legal
      deadline.
    - Keep a list of the person's details (name, phone, address and account numbers) to scan for after the ID-based
      deletion.
    - Run your deletion checks on a copy, or with caching and logging switched off. Test questions that name the person
      are cached and logged too, and they make new copies.
    - Look up every model trained on the same documents in your lineage registry, and plan its unlearning.

## In code

??? deep "Go deeper · delete one customer with the course library"
    ```python
    from mul import rag
    bot = rag.RAGStack(rag.HashEmbedder(dim=4000)).add_tickets(tickets)   # the chatbot's stores
    bot.forget("C-FIONA")            # delete by her ID from every store (indexes only mark her rows)
    bot.compact()                    # rewrite the indexes without the marked rows
    print(bot.copies("C-FIONA"))     # how many items still carry her ID, store by store
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting the document but not its chunks and numbers.** The chunks keep answering questions.
    - **Forgetting the answer cache.** It can give yesterday's answer, with the person's data in it.
    - **Treating embeddings as anonymous.** They carry the words they were made from.
    - **Trusting the ID label alone.** A mention in someone else's document survives a deletion by ID.
    - **Stopping at the stores.** A model trained on the same documents keeps its own copy.

## Key takeaways

!!! notes "Notes to take"
    - **RAG.** The chatbot looks documents up at answer time, so a person's data sits in stores, not in weights.
    - **Copies.** Documents, chunks, embeddings, both indexes, answer cache, logs, backups and trained models.
    - **Embeddings are text.** 56 of Fiona's 77 words were read back from her 10 hashed embeddings.
    - **Trap.** A tombstone hides a row but does not remove it. Compact, and rebuild any approximate index.
    - **Trap.** Tags find what came from a person, not what is about them. Scan for details and redact mentions.
    - **Rule.** Tag at creation, delete by ID everywhere, compact or rebuild, scan without tags, follow the lineage
      into models.
    - **Main number.** After deleting, redacting and compacting, the stack was identical, bit for bit, to one built
      without Fiona.
    - **Trained models.** The drafting model still gave her number at 6.64 bits until it was unlearnt too.

## Quiz

```quiz
- q: In a RAG chatbot, where does a person's data usually live?
  options:
    - Only inside the language model
    - In the store the chatbot searches, as documents, chunks and embeddings
    - Nowhere; RAG never stores data
  answer: 1
  why: RAG looks passages up when it answers, so the data sits in the store it searches.
- q: Why is deleting the original document often not enough?
  options:
    - Chunks, embeddings, saved answers and logs keep their own copies
    - Documents cannot be deleted
    - The model memorises every document it reads
  answer: 0
  why: Each step of the chatbot copies the data. Every copy must be found and removed.
- q: An index puts a "deleted" mark on a row instead of removing it. When is the row really gone?
  options:
    - Straight away
    - After the index is compacted, that is rewritten without the marked rows
    - Never
  answer: 1
  why: A marked row is skipped in searches but still stored, and still in backups, until compaction.
- q: Are embeddings a safe, anonymous form of the text?
  options:
    - Yes, they are just numbers
    - No, the words can often be worked back out of them
  answer: 1
  why: In Lesson 21, 56 of Fiona's 77 words were read back from her stored numbers. Treat embeddings as personal data.
- q: What makes it possible for one deletion to reach every copy?
  options:
    - Labelling every chunk, embedding and saved answer with its source when it is made
    - Retraining the language model
    - Turning off the cache for a day
  answer: 0
  why: The label lets one request find every copy that came from the person.
- q: How does Lesson 21 turn a chunk into its 4,000 numbers?
  options:
    - Each word is sent by a fixed hash to one slot with a plus or minus sign, and the list is scaled to length 1
    - A neural network learns the numbers from the tickets
    - The words are sorted and numbered from 1 to 4,000
  answer: 0
  why: This is a hashed bag of words. Because the hash is public, anyone can check which words could have filled a slot, which is why the words can be read back.
- q: After deleting by Fiona's ID and compacting, the chatbot still said she lived at 14 Larch Row. Why?
  options:
    - The sentence was in her neighbour's ticket, which carries the neighbour's ID
    - Compaction had failed
    - The answer cache had not been cleared
  answer: 0
  why: Tags find what came from a person, not what is about them. A scan for her details found the neighbour's ticket.
- q: Her details appear in her neighbour's ticket. What is the right fix?
  options:
    - Redact her details and keep the rest of the neighbour's ticket
    - Delete the neighbour's whole ticket
    - Leave it, because it carries the neighbour's ID
  answer: 0
  why: The rest of the ticket is the neighbour's own data. Replacing her details with "[removed]" removes her and keeps theirs.
- q: Fiona's rows were removed from the lists of an IVF index. Why did a trace of her phone number remain?
  options:
    - The centroids are averages that included her rows, and only a rebuild works them out again
    - IVF indexes cannot remove rows at all
    - Her rows had been copied into every list
  answer: 0
  why: The centroid weight in her number's slot stayed at 0.1643 after removal and fell to 0 only after a rebuild.
- q: Search quality for other customers fell from 74.8% to 73.9% after Fiona was deleted. Is that a problem?
  options:
    - No, a chatbot built without her gives exactly the same result
    - Yes, the deletion damaged the index
    - Yes, so the deletion should be undone
  answer: 0
  why: The right answer is whatever a stack that never held her data gives, and it loses the same two questions.
```

## Try it

!!! levelup "Level up"
    You can now find every copy a RAG chatbot makes of a person and delete them so the result matches a chatbot built
    without her. Next quest, [Federated unlearning](federated-unlearning.md), where the server never even sees the
    data it must forget.

- Run [Lesson 21, RAG and vector stores](../lessons/21-rag-and-vector-stores.md). It builds a support chatbot's stores
  in NumPy, deletes one customer from every store, catches the deleted-mark trap and proves the result is identical
  to a chatbot built without her. It also shows that a model trained on the same tickets still remembers her.
- Try the lesson's first exercise. Cut the tickets into chunks of 12 words that overlap by 4, and see whether the
  read-back attack recovers more or fewer of Fiona's words. Then explain why.
