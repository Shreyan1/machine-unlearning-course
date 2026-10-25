---
title: Decision trees and random forests
description: A decision tree asks yes/no questions; a random forest is a committee of trees, each trained on its own bag of rows.
---

# Decision trees and random forests

!!! oneline "In one line"
    A **decision tree** answers by asking a chain of yes/no questions, and a **random forest** is a committee of many
    trees that vote.

## Why it matters

Trees have no gradient and no formula, so none of the tricks from earlier models work. Yet forests can still forget
exactly, because each tree only saw **part** of the data. You only rebuild the trees that met the deleted row. This idea,
**locality by design**, leads straight to [SISA](../unlearning/sisa.md), the main exact method for neural networks.

## A simple example

A doctor's checklist might ask, "Fever? Yes. Cough? No. Rash? Yes. Then it is probably X." A random forest is
like asking 50 doctors, each of whom trained on different patients, and taking a vote.

## How it works

<!-- diagram: decision-trees-and-random-forests -->

### A decision tree

<ol class="steps" markdown>
<li markdown>**Pick the best question** to split the data, such as "Is pixel 27 brighter than 5?".</li>
<li markdown>**Split** the data into the "yes" group and the "no" group.</li>
<li markdown>**Repeat** inside each group until the groups are pure enough.</li>
<li markdown>**Predict** by following the questions down to a leaf and reading its label.</li>
</ol>

### A random forest

Each tree is trained on its own random **bag** of rows, and the forest takes a vote. The classic way to make a bag is
a **bootstrap**: draw \(n\) rows *with replacement* from the \(n\) training rows.

### Forgetting in a forest

If Carol's digit was never in tree #7's bag, tree #7 never saw her and can stay as it is. Only trees whose bag contained
her rows need rebuilding. The result is exact, as long as each rebuilt tree uses the same random seed and the same bag
minus the deleted rows.

The catch is that bootstrap bags overlap heavily. A typical row lands in about **63%** of the trees, and in Lesson 03
Carol's 40 rows reached **all 50** trees. So Lesson 03 redesigns the forest.

| Design (50 trees) | Test accuracy | Trees to retrain for Carol |
|---|---|---|
| Bootstrap bags | 97.2% | 50 of 50 |
| Random shards (5 groups) | 94.4% | 49 of 50 |
| **User-aware shards** (each user in one group) | 94.4% | **10 of 50** |

Putting all of one person's data in the same shard means forgetting them touches just one shard. The price is a little
accuracy every day, because each tree sees less data.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
forest = classical.BaggedForest(50, seed=0).fit(L.X_train, L.y_train)
forest.unlearn(L.forget_idx)     # rebuild only the trees whose bags held Carol's rows
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming a forest is local by default.** With bootstrap bags, one row already reaches about 63% of the trees.
    - **Sharding by row instead of by person.** If one person's rows are spread over every shard, forgetting them still
      touches everything. Shard by the unit people will ask to delete.

## Key takeaways

- A decision tree asks yes/no questions; a random forest is a committee of trees.
- Forests forget exactly by rebuilding only the trees that saw the row.
- Bootstrap bags spoil locality; **user-aware shards** restore it, at a small cost in accuracy.

## Quiz

```quiz
- q: What is a random forest?
  options:
    - A single very deep tree
    - A committee of decision trees that vote
    - A neural network with tree-shaped layers
  answer: 1
  why: Each tree trains on its own bag of rows, and the forest combines their votes.
- q: Which trees must be rebuilt when Carol is forgotten?
  options:
    - All of them, always
    - Only the trees whose bags contained her rows
    - None of them
  answer: 1
  why: A tree that never saw her rows is already identical to one trained without her.
- q: With classic bootstrap bags, roughly what share of trees does one typical row appear in?
  options:
    - About 5%
    - About 63%
    - 100%
  answer: 1
  why: Drawing n rows with replacement puts any given row in about 63% of the bags.
- q: Why do user-aware shards make forgetting Carol cheaper?
  options:
    - All her data sits in one shard, so only that shard's trees need rebuilding.
    - They delete her data before training.
    - They use fewer trees overall.
  answer: 0
  why: In Lesson 03, user-aware shards cut the trees to retrain for Carol from 50 to 10.
```

## Try it

- The concept page [SISA, sharded training](../unlearning/sisa.md) applies the same idea to neural networks.
- Run the lesson [03 · SVM and random forest](../lessons/03-svm-and-random-forest.md).
