---
title: Scenarios
description: Short case studies. Read the situation, choose a response and see why it is the best call, defensible or risky.
---

# Scenarios

Real deletion requests rarely arrive as tidy exercises. Each scenario below gives you a situation and a few
responses. Pick one to see how it holds up, then read the feedback on the others. There is no score, but finishing all
of them earns the **Decision maker** badge on [Your progress](quizzes/progress.md).

!!! tip "How to read the verdicts"
    **The best call** is what the course recommends. **Defensible** can work, with care or at a cost. **Risky** is the kind
    of answer that fails an audit or a regulator's questions.

## Requests

```scenario
title: The first erasure request
situation: |
  Carol asks a small startup to delete her data. Her 40 handwritten digits helped train the company's digit
  classifier, a small neural network that is retrained every Sunday. Her request arrived on Tuesday.
options:
  - text: Delete her rows from the database and reply that it is done.
    verdict: risky
    why: The model was trained on her rows, so it still carries them. [Deleting is not forgetting](unlearning/deleting-vs-unlearning.md).
  - text: Remove her rows now, let Sunday's retrain run without them and record the evidence.
    verdict: best
    why: A retrain without her is the gold standard, and a weekly schedule makes it affordable. Write down when and how, as in [the enterprise playbook](unlearning/enterprise-playbook.md).
  - text: Run gradient ascent on her digits tonight and reply that she is forgotten.
    verdict: risky
    why: Gradient ascent is unstable and can over-forget, and without an audit you have no evidence. See [quick fixes and their traps](unlearning/approximate-unlearning.md).
  - text: Refuse, because retraining is expensive.
    verdict: risky
    why: Cost can matter legally, but here a retrain is already scheduled. Refusing would be hard to defend.
```

```scenario
title: The chatbot that remembers
situation: |
  A support chatbot answers questions with retrieval. It searches a vector store of past support tickets and passes
  the best matches to a language model. A customer asks for all their tickets to be erased.
options:
  - text: Delete the tickets from the ticket database.
    verdict: risky
    why: Chunks, embeddings, caches and logs keep their own copies. See [RAG, vector stores and caches](unlearning/rag-and-vector-stores.md).
  - text: Delete by customer ID from the tickets, chunks, embeddings, keyword index, answer cache and logs. Then compact the index and check with test searches.
    verdict: best
    why: In a RAG system the data lives in the store, so deleting every copy is exact and cheap.
  - text: Retrain the language model.
    verdict: ok
    why: Only needed if the tickets were also used to fine-tune the model. On its own, it leaves the retrieval copies untouched.
```

## Methods

```scenario
title: Poison in the shards
situation: |
  A fraud model was trained with SISA, using 10 shards with their own checkpoints. The security team finds 300
  poisoned rows planted by an attacker. They all sit in shards 3 and 7.
options:
  - text: Retrain shards 3 and 7 from the checkpoint before the first poisoned slice.
    verdict: best
    why: SISA isolates the damage, so retraining two shards gives exactly the model you would have trained without the poison. See [SISA](unlearning/sisa.md).
  - text: Retrain the whole model from scratch.
    verdict: ok
    why: Correct, but about five times the cost of retraining the two shards, for the same result.
  - text: Run an approximate method on the 300 rows.
    verdict: risky
    why: Backdoors can survive approximate unlearning. When an exact option is this cheap, use it. See [poisoned data and backdoors](unlearning/poisoning-and-backdoors.md).
```

```scenario
title: The compressed release
situation: |
  Your team unlearnt a set of private facts from a language model with an approximate method. Every forgetting test
  passed at full precision. The model will ship quantized to 4-bit weights to run on phones.
options:
  - text: Ship it; the tests passed.
    verdict: risky
    why: Quantization can round away the small weight changes made by unlearning and bring the facts back. See [when forgotten knowledge comes back](unlearning/relearning-and-quantization.md).
  - text: Quantize first, then repeat every forgetting test, plus a relearn test, on the 4-bit model.
    verdict: best
    why: Test the model you will actually deploy. Compare it with models retrained without the facts.
  - text: Add an output filter that blocks the facts.
    verdict: ok
    why: A useful extra layer, but a filter hides answers rather than removing knowledge. It is not deletion.
```

## Evidence

```scenario
title: The auditor's question
situation: |
  An auditor asks how you know the unlearnt model really forgot Carol. You have the unlearnt model, the original, and
  budget for a few retrains.
options:
  - text: Show that accuracy on Carol's digits is now 0%.
    verdict: risky
    why: A model that never saw Carol still gets many of her digits right. 0% means over-forgetting, which is itself a signal. See [the gold band](unlearning/gold-band.md).
  - text: Show results on five checks fixed in advance, each compared with the gold band from several retrained models.
    verdict: best
    why: This is [the unlearning audit](unlearning/unlearning-audit.md). It is evidence someone else can check.
  - text: Say that you used SCRUB, a published method.
    verdict: risky
    why: A method's name is not evidence. The same method can pass on one dataset and fail on another.
```

```scenario
title: Edit out the phone number
situation: |
  A language model sometimes outputs a private person's phone number. A colleague suggests a model-editing tool that
  can change the number to a fake one in minutes.
options:
  - text: Edit the number to a fake one and close the ticket.
    verdict: risky
    why: The real number can often still be recovered, and the model now states a false fact about a person. See [model editing vs unlearning](unlearning/editing-vs-unlearning.md).
  - text: Find where the number came from, delete it there and unlearn it with a full audit that includes rephrased questions.
    verdict: best
    why: Erasure is an unlearning goal. Remove the source, then test like unlearning, not like a correction.
  - text: Add an output filter for the number while the proper fix is prepared.
    verdict: ok
    why: A sensible stop-gap that limits harm today, as long as it is not called deletion.
```

```scenario
title: The hospital that leaves
situation: |
  Eight hospitals trained a diagnosis model together with federated learning. One hospital leaves the consortium and
  asks for its contribution to be removed. The server kept no history of past updates.
options:
  - text: Remove that hospital's last update.
    verdict: risky
    why: Every round since they joined built on their contributions. See [federated unlearning](unlearning/federated-unlearning.md).
  - text: Retrain the federated model with the remaining seven hospitals.
    verdict: best
    why: The gold standard. It costs every hospital some compute, but it is exact and easy to explain.
  - text: Have the leaving hospital unlearn locally, run a few repair rounds, then audit.
    verdict: ok
    why: It is much cheaper, but it is approximate and hard to audit once the hospital has gone. Plan the check before it leaves.
```

## What next?

- Missed the best call somewhere? Each feedback links to the page that explains it.
- Try the [practice problems](practice.md), or check your badges on [Your progress](quizzes/progress.md).
