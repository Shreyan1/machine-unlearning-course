---
title: Deleting from RAG, vector stores and caches
description: When a chatbot looks documents up at answer time, forgetting a person is ordinary deletion, as long as you find and remove every copy the system made.
---

# Deleting from RAG, vector stores and caches

!!! oneline "In one line"
    Some chatbots do not learn your documents. They **look them up** every time they answer. To forget a person there,
    you delete their data, but first you must find **every copy**.

## Why it matters

Many company chatbots use **retrieval-augmented generation**, or **RAG** (Lewis et al. 2020). The name sounds hard,
but the idea is simple. Before the chatbot answers, it searches a store of documents, picks the few that match the
question and reads them. The language model itself never learnt those documents.

So when a customer asks to be forgotten, their data usually sits in the store, not inside the model. That is good
news, because deleting from a store is [exact](retraining-gold-standard.md) and cheap. The catch is that a RAG system
quietly makes many copies of every document, and a deletion that misses one copy is not a deletion.

Any team that runs a support chatbot or a "chat with your files" tool meets this problem, and the documents are often
sensitive. In Lesson 21 a customer's tickets mention a hospital stay, and health data is a special category of
personal data under GDPR Art. 9. A leftover copy is a real leak, because RAG systems can be pushed into repeating the
text they retrieve (Zeng et al. 2024).

## A simple example

!!! simply "Explain it simply"
    Think of a help desk with a filing cabinet of old letters. To answer quickly, the staff photocopied useful
    paragraphs into a **binder**, wrote an **index card** for every important word, kept a **notebook** of answers
    they gave and wrote a **diary** of every call.

    Throwing a customer's letters out of the cabinet leaves her words in the binder, on the cards, in the notebook and
    in the diary. Forgetting her means finding every copy.

Each part of the picture is a real store. The **filing cabinet** is the ticket database, where the original documents
live. The **binder** of photocopied paragraphs is the chunk store. The **index cards** are the two search indexes,
one that finds passages by meaning and one that finds them by word. The **notebook** of past answers is the answer
cache, and the **diary** of calls is the logs. A nightly photocopy of the whole office is the backups. Last, a new
member of staff who learnt the old letters by heart to write replies faster is a model trained on the tickets.
Throwing out the letters does nothing to what that person remembers.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [**RAG**](../start-here/glossary.md#r) | A chatbot that searches a store of documents before it answers, and answers from what it finds | Kestrel Home's support chatbot searches 230 old tickets |
| **Chunk** | A short passage cut from a document. Search works on chunks, so a long document can match on one paragraph | Windows of 24 words that overlap by 8 words |
| [**Embedding**](../start-here/glossary.md#e) | A list of numbers that stands for a chunk. Chunks with similar words or meaning get similar numbers | 4,000 numbers for every chunk in Lesson 21 |
| **Cosine similarity** | A score for how alike two embeddings are. A higher score means more alike | The cache reuses an old answer when a new question scores 0.8 or more |
| [**Vector index**](../start-here/glossary.md#v) | The table of embeddings that finds the chunks nearest to a question | 440 rows of 4,000 numbers |
| **Keyword index** | For every word, the list of chunks that contain it and how often | 527 different words |
| **Answer cache** | Saved answers, given again to a similar question without a new search | 63 saved answers after a month of questions |
| [**Tombstone**](../start-here/glossary.md#t) | A "deleted" mark on a row. Searches skip the row, but it is still stored | 10 tombstones for Fiona's 10 vectors |
| **Compaction** | Rewriting an index without its marked rows, so that they are really gone | The vector index went from 440 stored rows to 430 |
| [**Lineage tag**](../start-here/glossary.md#l) | The ID of the document and the person a copy came from, attached when the copy is made | Every chunk of Fiona's carries her ID, C-FIONA |

## How it works

### How a RAG chatbot answers

1. **Cut.** Every document is cut into short passages of a few sentences, called **chunks**. This is the binder. In
   Lesson 21 each chunk is a window of 24 words, and the next window starts 16 words later, so two neighbouring chunks
   share 8 words. The overlap makes it less likely that a sentence is split badly at a cut.
2. **Describe.** Each chunk gets a list of numbers that describes what it is about, called an **embedding**. Chunks
   about the same thing get similar numbers, a bit like a postcode for meaning. In Lesson 21 each embedding has 4,000
   numbers. The next section shows how they are made.
3. **Index.** Two indexes make search fast. A **vector index** finds chunks with similar numbers, and a **keyword
   index** finds chunks with the same words. These are the index cards. Searching the vector index is the
   nearest-neighbour search of [k-NN](../ml-basics/k-nearest-neighbours.md). The keyword index scores matches with
   **BM25**, a standard score that gives rare words more weight than common ones.
4. **Answer.** The two result lists are merged, with higher places counting more, and the best 3 chunks are read.
   The chatbot answers from them and may save the answer in an **answer cache**, so that a similar question later
   gets the same answer faster. This is the notebook. In Lesson 21 a saved answer is reused when a new question's
   embedding has a cosine similarity of 0.8 or more with an old question's.
5. **Log.** Questions, chunks and answers are written to **logs**. This is the diary.

In Lesson 21 the answerer simply copies the sentence that shares the most words with the question. Real language
models also copy names and numbers from what they read, so it is a fair stand-in for a privacy test.

<!-- diagram: rag-and-vector-stores -->

The figure shows the ticket database copied into six stores, namely the chunks, the vector index, the keyword index,
the answer cache, the logs and the backups. Below them sits a model trained on the same tickets. A yellow dot marks
each copy of Fiona's data. The animation plays four stages. Every ticket is copied into the stores, a deletion by her
ID only marks her rows, compaction removes the marked rows for real, and the trained model still holds its own copy.

### How an embedding is made in Lesson 21

Real systems use a neural network to turn text into numbers. Lesson 21 uses a simpler recipe called a **hashed bag of
words**, which you can follow by hand.

1. Start with a list of 4,000 zeros. Each position in the list is called a **slot**.
2. Split the chunk into lower-case words and numbers. The phone number 555-0147 becomes two pieces, "555" and "0147".
3. Send each word through a fixed **hash function**. A hash function is a rule that turns any word into a number, and
   it always gives the same number for the same word. That number picks one of the 4,000 slots and a sign, plus or
   minus.
4. Add 1 to that slot, or take 1 away if the sign is minus. A word that appears twice changes its slot twice.
5. Scale the whole list so that its length is 1. After this, the similarity of two chunks is the sum of their
   slot-by-slot products, which is the cosine similarity. Chunks that share many words score high.

"Bag of words" means that the order of the words is thrown away. Only which words are present, and how often,
survives.

**Why the words can be read back.** A slot is non-zero only if some word of the chunk landed there. The hash function
is public, so an attacker with a stored embedding can check each word on a list and keep those whose slot is non-zero
with the right sign. In Lesson 21 the list had 165 words, taken from other customers' tickets and from public lists of
names and streets, like a phone book or a map. From
Fiona's first chunk it read back "air arrived broken for from fryer hello hospital i in my not order". Across her 10
embeddings it recovered 56 of her 77 different words, with no wrong guesses. The 21 words it missed, such as
"daughter" and "operation", were simply not on its list, and a full dictionary would find those too.

**Phone numbers too.** The attacker tried all 100 possible numbers from 555-0100 to 555-0199. Only 2 fitted her
embeddings, and one of them was hers. The other, 555-0196, fitted by accident, because its slot is shared with a word
in her chunks. Two words landing in the same slot is called a **hash collision**.

**Neural embeddings are not safe either.** Hashed embeddings are the easy case, because the hash is public. Neural
embeddings are harder to read, but Morris et al. (2023) trained a model that turns them back into text, and it rebuilt
most short texts word for word. Treat every stored embedding as a copy of the text it came from.

### Where the copies hide

| Copy | In plain words | Why it is easy to miss |
|---|---|---|
| **Documents** | The original tickets, emails or files | Someone else's document may mention her too |
| **Chunks** | The short passages cut from them | They are often kept apart from the documents |
| **Embeddings** | The numbers that describe each chunk | People think numbers are anonymous, but the words can often be worked back out |
| **Indexes** | The tables that make search fast | Many only **mark** a row as deleted until they are cleaned up |
| **Answer cache** | Saved answers | It can give an old answer, with her data in it, to a new question |
| **Logs and backups** | Records of past questions, and copies of everything | They keep the full text unless you limit them |
| **Models trained on the data** | Any model fine-tuned on the same documents | Now it is a weights problem, not a store problem |

### Two traps

**The deleted mark.** Many indexes do not remove a row when you delete it. They put a "deleted" mark on it, called a
**tombstone**, and skip it in searches. It is like crossing out a name in a register. The name is still there, and
still in tonight's backup, until the register is rewritten without it. Rewriting an index without its marked rows is
called **compaction**.

Indexes work this way because removing a row from the middle of a big file is slow, while writing a small mark is
fast. Search engines built on Lucene, such as Elasticsearch, behave like this until their pieces are merged. A
keyword index has the same problem in its word counts. In Lesson 21 it still counted "kowalczyk" in 8 chunks when
only 2 searchable chunks held the word, so its scores were worked out as if she were still there.

**Numbers that can be read back.** An embedding is made from the words of a chunk, so it carries those words, as the
attack above shows. Put the two traps together and a tombstoned embedding in a backup is not harmless numbers. It is
her text.

### Why an approximate index keeps a trace

With millions of chunks, comparing a question with every row is too slow. Real systems use an **approximate
nearest-neighbour** index, which gives up a little accuracy for a lot of speed. One common kind is the **inverted
file**, or **IVF** (Jégou et al. 2011). It groups the embeddings into lists with k-means, a method that puts similar
points together. Each list has a **centroid**, which is the average of the embeddings in it. A search first compares
the question with the centroids, then looks only inside the closest few lists. In Lesson 21 the IVF index had 16
lists and searched the 4 closest. It found 75% of the exact top 3 results, which is the usual price of speed.

The centroids are averages of the stored data, so they are a small **trained model**, and Fiona is part of them. Think
of a summary page at the front of the binder, written from all the letters. Taking her letters out does not rewrite
the summary. The lesson looked at the slot of her phone number's last four digits, "0147". The largest centroid weight
in that slot was 0.1643. Removing her 10 rows from the lists left it at exactly 0.1643, because the averages were not
worked out again. Only a **rebuild**, which runs k-means again on the 430 rows that are left, brought it to 0.0000.

Graph indexes such as HNSW have the same problem in another form, because a deleted point is often only marked and
still helps steer searches. So a deletion plan for an approximate index must include a rebuild.

### The neighbour's ticket trap

After deleting by Fiona's ID and compacting, nothing tagged with her ID was left. Yet a stranger who asked "who lives
at 14 larch row?" still heard "with my neighbour fiona kowalczyk at 14 larch row, but she is in hospital." That
sentence came from her neighbour's ticket about a toaster left with Fiona. The ticket carries the neighbour's ID, so a
deletion by Fiona's ID never touched it.

The rule to remember is that **tags find what came from a person, not what is about them**. So the last check must
not rely on the tags. Lesson 21 searched the raw contents of every store for four of her details, namely "kowalczyk",
"555-0147", "larch row" and "7731". The fix for what it finds is to **redact**, not to delete. Her details are
replaced with "[removed]" and the neighbour's ticket stays, because the rest of it is the neighbour's own data.

### The steps

<ol class="steps" markdown>
<li markdown>**Label every copy when you make it.** Each chunk, embedding, saved answer and log line carries the ID of the document and of the person it came from. This is the lineage of [Lesson 17](../lessons/17-enterprise-playbook.md).</li>
<li markdown>**Delete by that label everywhere,** in one job. Include the answer cache, which is the copy people most often forget.</li>
<li markdown>**Compact or rebuild the indexes,** so the marked rows are really gone. An approximate index needs a full rebuild, because its centroids or graph were built from her data.</li>
<li markdown>**Clear saved answers and logs** that contain the data. Keep logs for a short time, and write down when the backups that still hold the data will expire.</li>
<li markdown>**Check.** Search for the person by name and in other words, and search for their details without the label, because other people's documents may mention them. Nothing should come back. Redact any mention you find in someone else's document.</li>
<li markdown>**Follow the data into models.** Any model trained or fine-tuned on the same documents needs its own unlearning, because deleting from a store does nothing to a model's weights.</li>
<li markdown>**Record it.** Note what was deleted, where and when, as in [the enterprise playbook](enterprise-playbook.md).</li>
</ol>

## A worked example

Kestrel Home is a fictional online shop for kitchen appliances. Its support chatbot searches 230 old tickets from 81
customers. **Fiona Kowalczyk** wrote 4 of them. They hold her phone number (555-0147), her address (14 Larch Row), the
last digits of her card (7731) and the fact that she was in hospital for an operation. She asks for all of it to be
erased. Here is her data's journey, with the numbers from [Lesson 21](../lessons/21-rag-and-vector-stores.md).

1. **Chunking.** Her first ticket, about an air fryer that arrived broken, is 52 words long, so windows of 24 words
   that start 16 words apart cut it into 3 chunks. Her four tickets become 10 chunks, out of 440. Each carries her ID,
   C-FIONA.
2. **Embedding and indexing.** Each chunk becomes 4,000 numbers, almost all of them zero. The vector index gets her 10
   rows, and the keyword index, which knows 527 different words, lists her chunks under words such as "kowalczyk" and
   "hospital".
3. **A month of use.** Customers ask 63 questions, and each is answered, cached and logged. Two involve her. She asked
   about her air fryer while in hospital, and a support agent asked "fiona kowalczyk phone number" and got her number.
4. **The naive deletion.** Only her 4 tickets are deleted. A stranger asks "phone number for fiona kowalczyk please",
   which is close enough to the agent's question that the cache serves her number again. Questions about 14 Larch Row,
   the hospital and the card ending 7731 are answered from her chunks.
5. **Delete by her ID.** One call removes 4 tickets, 10 chunks, 10 vectors, 10 keyword entries, 2 saved answers and 2
   log records. Her chunks then appear in none of the top 20 results for 230 test searches.
6. **The tombstones.** The vector index still stores 440 rows, of which 430 are searchable and 10 are tombstones. One
   tombstoned row, read from a copy of the index, still gives back "air arrived broken for from fryer hello hospital i
   in my not order".
7. **Compaction.** The vector index now stores 430 rows with 0 tombstones, and the keyword index counts "kowalczyk" in
   2 chunks, both the neighbour's.
8. **The scan.** A search for her four details finds the neighbour's ticket, its 2 chunks in both indexes, 1 saved
   answer and 1 log record. After redaction and another compaction the scan is empty in all six stores.
9. **The proof.** A stack built from scratch on the erased database matches the cleaned one in every store, bit for
   bit. The deletion embedded 2 chunks again (the neighbour's redacted ticket), where a full rebuild embeds 429.

The table counts the items tagged with Fiona's ID in each store, after each kind of deletion.

| Store | Before | Delete her tickets only | Delete by ID, tombstones | Delete by ID and compact |
|---|---|---|---|---|
| Ticket database | 4 | 0 | 0 | 0 |
| Chunk store | 10 | 10 | 0 | 0 |
| Vector index | 10 | 10 | 10 | 0 |
| Keyword index | 10 | 10 | 10 | 0 |
| Answer cache | 2 | 2 | 0 | 0 |
| Logs | 2 | 2 | 0 | 0 |

Deleting her tickets alone cleaned one store out of six, and deleting by ID without compaction still left her in both
indexes. Even the clean last column misses the neighbour's ticket, because it counts tags.

## What Lesson 21 found

[Lesson 21](../lessons/21-rag-and-vector-stores.md) built a support chatbot for a fictional shop and deleted one
customer, Fiona.

| What we tried | Result | What it means |
|---|---|---|
| Delete her tickets only | ❌ 5 of the 6 stores still held her data, and the chatbot still gave out her phone number | The document database is only one copy among many |
| Read her stored numbers (embeddings) | ❌ 56 of her 77 different words came back, and only 2 of the 100 possible phone numbers fitted, hers among them | Embeddings are personal data and must be deleted with the text |
| Delete by her ID everywhere | ⚠️ Hidden from search, but her marked rows were still stored until compaction | A delete call that writes tombstones is not the end of the job |
| Remove her rows from an IVF index | ❌ The centroid weight in her phone number's slot stayed at 0.1643 until a rebuild brought it to 0 | An approximate index has a trained part that needs rebuilding |
| Check her neighbour's ticket | ❌ It mentioned her address, and her ID label missed it. A search for her details found it | Scan for a person's details, not only for their ID |
| Delete, clean the neighbour's ticket and compact | ✅ Identical, bit for bit, to a chatbot built without her | Deleting from a store is exact unlearning |
| Search quality for everyone else | hit@3 was 74.8% before and 73.9% after, exactly what the chatbot built without her gives | The small drop is the correct answer, not damage |
| A model trained on the same tickets | ❌ It still recited her number until it was unlearnt too | Every trained copy needs its own unlearning |

**What hit@3 measures.** Each other customer asks about one of their own tickets, and hit@3 is how often that ticket
is among the 3 chunks found. Random picks would hit about 1.3%. After the deletion, 2 of the 226 questions lost their
ticket and none gained, and the chatbot built without her loses the same two.

**What the trained model showed.** Kestrel Home had also trained a small n-gram model, a table of counts that predicts
the next character, on the tickets to draft replies. Cleaning the stores did nothing to it. It still completed
"fiona kowalczyk, tel" with her number, at an **exposure** (Carlini et al. 2019) of 6.64 bits, the maximum, which means
her number was its top guess among the 100 possible ones. Subtracting her 4 tickets dropped it to 0.1 bits. The model
still knew her address from the neighbour's ticket, and only after that ticket was swapped for its redacted version
was the model identical to one trained on the erased database.

!!! note "Retrieval or weights?"
    If the person's data was also used to train or fine-tune the model, deleting it from the store is not enough. The
    model may still recall it from its weights, and that is the harder problem of
    [unlearning in language models](llm-unlearning.md).

## Limits

- **A small, fictional shop.** The lesson has 230 tickets and builds the stack in plain NumPy. Real vector databases
  each have their own rules for deletes, merges and backups, so check how yours removes a row and when.
- **Hashed embeddings are the easy case.** The hash is public, so reading words back is simple. The lesson relies on
  Morris et al. (2023) for the evidence that neural embeddings leak too.
- **The cache and logs meet only a weaker test.** They are a history of past questions, which cannot be rebuilt "as if
  she had never been there". The lesson checks that no entry was built from her data or contains her details, not
  that they match bit for bit.
- **A scan finds only what you search for.** A mention spelt another way, such as "f. kowalczyk on larch row", needs
  its own entry in the list. Backups are not modelled either, so record when each one expires.
- **Exact model unlearning worked only because the model was a table of counts.** A neural model has no such
  subtraction, which is the hard case of [Lesson 16](../lessons/16-llm-unlearning.md).

!!! tip "What to do in practice"
    - Tag every chunk, embedding, keyword entry, saved answer and log record with its document ID and person IDs at the
      moment it is made.
    - Make compaction, and a rebuild for any approximate index, part of the deletion job, finished inside the legal
      deadline.
    - Keep a list of the person's details, such as name, phone, address and account numbers, and scan every store for
      them after the ID-based deletion. Redact mentions in other people's documents.
    - Run your deletion checks on a copy, or with caching and logging switched off. Test questions that name the person
      are cached and logged too, and they make new copies.
    - Look up every model trained on the same documents in your lineage registry, and plan its unlearning.

## In code

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
    - **Trusting a "deleted" mark.** Until the index is compacted, the row is still stored.
    - **Forgetting the answer cache.** It can give yesterday's answer, with the person's data in it.
    - **Treating embeddings as anonymous.** They carry the words they were made from.
    - **Trusting the ID label alone.** Labels find what came from a person, not what is about them, so a mention in
      someone else's document survives a deletion by ID.
    - **Stopping at the stores.** A model trained on the same documents keeps its own copy, and deleting from the store
      does nothing to it.

## Key takeaways

- In a RAG chatbot, most personal data sits in the store the chatbot searches, where deletion is exact and cheap.
- The hard part is finding **every copy**, including chunks, embeddings, indexes, saved answers, logs and backups.
- Label every copy with its source when you make it, so that one deletion can reach them all.
- Embeddings are copies of the text. In Lesson 21, 56 of Fiona's 77 words were read back from them.
- A tombstone hides a row but does not remove it. Compact, and rebuild any approximate index, inside the deadline.
- Scan for the person's details without the labels, and redact mentions in other people's documents.
- If the data also reached a model's weights, deleting it from the store is not enough.

!!! note "Notes to take"
    - **Definition.** RAG looks documents up at answer time, so a person's data sits in stores, not in weights.
    - **Copies.** Documents, chunks, embeddings, vector index, keyword index, answer cache, logs, backups, trained
      models.
    - **Rule.** Tag at creation. Delete by ID everywhere. Compact or rebuild. Scan without tags. Redact mentions.
      Follow the lineage into models.
    - **Embedding in Lesson 21.** Each word goes by a fixed hash to one of 4,000 slots with a plus or minus sign, then
      the list is scaled to length 1. Words can be read back.
    - **Main number.** After deleting, redacting and compacting, the stack was identical, bit for bit, to one built
      without Fiona.
    - **The trap.** A "deleted" mark is not a deletion, and an ID label misses what others wrote about her.

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

- Run [Lesson 21, RAG and vector stores](../lessons/21-rag-and-vector-stores.md). It builds a support chatbot's stores
  in NumPy, deletes one customer from every store, catches the deleted-mark trap and proves the result is identical
  to a chatbot built without her. It also shows that a model trained on the same tickets still remembers her.
- Try the lesson's first exercise. Cut the tickets into chunks of 12 words that overlap by 4, and see whether the
  read-back attack recovers more or fewer of Fiona's words. Then explain why.
- Read [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md). Searching a vector index is a nearest-neighbour
  search, and deleting from it is the same exact subtraction as in [Lesson 01](../lessons/01-knn-and-naive-bayes.md).
- Read [the enterprise playbook](enterprise-playbook.md) to see how a lineage registry finds the models trained on the
  same documents.
- Sketch the stores of a chatbot you know. How many copies of one document can you find?
