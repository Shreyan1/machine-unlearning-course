---
title: SISA, sharded training
description: SISA splits training into shards and slices with checkpoints, so forgetting one person retrains only a small piece, exactly.
---

# SISA: Sharded, Isolated, Sliced, Aggregated

!!! oneline "In one line"
    SISA splits the training data into separate pieces, trains one model per piece and saves checkpoints, so that
    forgetting someone means retraining only **one small piece**, with an exact result.

## Why it matters

For neural networks, retraining is the only exact option, and it is expensive. SISA (Bourtoule et al., IEEE S&P 2021)
makes retraining cheap by **designing the training for deletion** from the start. In Lesson 07 it forgets Carol for
about **5%** of the cost of a full retrain, and the result is identical, weight for weight, to training without her.

## A simple example

Imagine writing a book in 5 separate notebooks, and photocopying each notebook after every chapter. If someone asks you
to remove a sentence from chapter 3 of notebook 2, you take the photocopy from the end of chapter 2 and rewrite
chapters 3 and 4 of *that notebook only*. The other four notebooks are never touched.

## How it works

<!-- diagram: sisa -->

| Letter | Idea | Where you have seen it |
|---|---|---|
| **S**harded | split the data into K separate shards | the forest's shards ([Lesson 03](../lessons/03-svm-and-random-forest.md)) |
| **I**solated | one independent network per shard; shards never share information | each tree only saw its bag |
| **S**liced | inside a shard, feed the data in R slices and **save a checkpoint after each** | new |
| **A**ggregated | predict by averaging the K networks | the forest's vote |

**To forget a row**, find its shard and slice, reload that shard's checkpoint from *before* the slice and retrain from there. Everything else is untouched.

### The partition decides the bill

Lesson 07 compares designs for forgetting Carol (5 shards × 4 slices):

| Design | Cost to forget Carol | Shards touched | Test accuracy |
|---|---|---|---|
| Full retrain | 100% | — | 98.0% |
| SISA, random partition | 61.4% | 5 | 98.0% |
| **SISA, user-aware partition** | **5.0%** | **1** | 97.0% |

With a random split, Carol's digits land in every shard. With a **user-aware** split, all her data is in one shard.

### Exact, bit for bit

After unlearning, every weight of every shard was **identical** to a SISA model trained from scratch without Carol,
with a largest difference of 0.0. Not "close", not "hard to tell apart": identical. That is the strongest evidence you
can give a regulator.

### The price: more shards, less accuracy

| Shards (K) | Test accuracy | Cost of one deletion |
|---|---|---|
| 1 | 98.1% | 54.2% of a retrain |
| 5 | 98.1% | 10.5% |
| 10 | 96.9% | 4.0% |
| 20 | 95.4% | 2.4% |

Each shard sees less data, so beyond a point accuracy falls. Even K = 1 (only slices and checkpoints) roughly halves
the cost of a deletion. Choosing K is a business decision. You weigh expected deletions × retrain cost against the accuracy you can afford to lose. Starting every shard from a shared pretrained model softens the drop.

!!! warning "Audit with the same recipe"
    When Lesson 07 audited SISA models against references trained as **one big network**, the audit ranked a model that
    still remembered Carol as *cleaner* than a truly clean one. An ensemble of five small networks has a different
    confidence pattern from one big network. References must use the same recipe as the model under test.

## In code

```python
from mul import methods, lab
L = lab.make_lab("carol")
sisa = methods.SISA(lab.model_fn, n_shards=5, n_slices=4)
sisa.fit(L.X_train, L.y_train, partition=user_aware_partition)   # all of one user's rows in one shard
sisa.unlearn(L.forget_idx)        # retrain only from the checkpoint before Carol's slice
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Sharding randomly.** One person's data then sits in every shard, and forgetting them touches everything.
    - **Ignoring storage and serving cost.** SISA keeps K models × R checkpoints and runs K models per prediction.
    - **Deciding too late.** SISA must be chosen before training; it cannot be added to an existing model.

## Key takeaways

- SISA is the user-aware forest idea, rebuilt for neural networks, plus slices and checkpoints.
- It is exact by construction, proven bit for bit.
- Shard by the unit people delete, and put data likely to be deleted in late slices.
- More shards mean cheaper deletion but lower accuracy.

## Quiz

```quiz
- q: What does the first "S" in SISA stand for?
  options:
    - Sharded
    - Secure
    - Summed
  answer: 0
  why: The data is split into K separate shards, each with its own model.
- q: Why are checkpoints saved after each slice?
  options:
    - So you can restart from just before the deleted row's slice
    - To make predictions faster
    - To share data between shards
  answer: 0
  why: Retraining only needs to start from the checkpoint before the slice that held the row.
- q: With a user-aware partition, what did forgetting Carol cost in Lesson 07?
  options:
    - About 5% of a full retrain
    - About 61% of a full retrain
    - A full retrain
  answer: 0
  why: All her data was in one shard, so only one slice of one shard was retrained.
- q: How close was the SISA unlearnt model to a SISA model trained without Carol?
  options:
    - Identical, bit for bit
    - About 95% similar
    - Only similar in accuracy
  answer: 0
  why: Every weight of every shard matched exactly. SISA is exact by construction.
- q: What happens as you add more shards?
  options:
    - Deletion gets cheaper, but accuracy can fall.
    - Deletion gets more expensive.
    - Nothing changes.
  answer: 0
  why: Each shard sees less data. At K = 20, test accuracy fell to 95.4% while a deletion cost 2.4% of a retrain.
```

## Try it

- Next concept: [Quick fixes and their traps](approximate-unlearning.md).
- Lesson: [07 · SISA](../lessons/07-sisa.md).
