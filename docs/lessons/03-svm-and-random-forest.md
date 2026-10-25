---
title: "Lesson 03: SVM and random forest"
description: Locality makes forgetting cheap. SVMs ignore non-support vectors; forests retrain only the trees that saw a row, especially with user-aware shards.
---

# Lesson 03: SVMs and random forests, forgetting by locality

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 1 · Classical ML</span><span class="chip" markdown="span">:material-stairs-up: Rung 3</span></div>

<div class="buttons" markdown>
[:simple-googlecolab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb){ .md-button }
</div>

## The story

A decision tree has no gradient and no curvature, so the Newton step is gone. Yet forgetting can still be cheap, thanks
to the most useful property in the course: **locality**. If you know *which part* of a model a point influenced, you
only rebuild that part.

| Model | Where locality comes from | What forgetting costs |
|---|---|---|
| **SVM** | the boundary depends only on the support vectors | nothing, unless you delete a support vector |
| **Random forest** | each tree only saw its own bag of rows | retrain only the trees whose bag held the row |

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** an SVM (first on a 2-D toy problem, then on the digits) and a 50-tree forest.</li>
<li markdown>**Show the issue**: is Carol a support vector? How many trees did her rows reach?</li>
<li markdown>**Untrain**, comparing three forest designs, namely bootstrap bags, random shards and user-aware shards.</li>
<li markdown>**Show the result**: accuracy and trees retrained.</li>
<li markdown>**Prove it**: the user-aware forest equals a forest that never saw Carol.</li>
</ol>

## Key results

**SVM.** On the 2-D toy problem, 54 of 200 points were support vectors. Deleting a non-support vector moved the boundary
by 2.3 × 10⁻⁸ (nothing); deleting a support vector moved it by 1.1 × 10⁻³.

On the digits, **97.5%** of Carol's digits were support vectors, against **40.5%** of everyone else's. For 40 typical
non-support-vector users, the original model already *was* the unlearnt model on 100% of inputs. For Carol, the only
exact option was to re-solve.

**Random forest.**

| Design (50 trees) | Test accuracy | Trees to retrain for 1 random row | Trees to retrain for Carol |
|---|---|---|---|
| Bootstrap bags | 97.2% | 31 | 50 |
| Random shards | 94.4% | 8 | 49 |
| **User-aware shards** | 94.4% | 9 | **10** |

A typical row appears in about 63% of bootstrap trees, and Carol's 40 rows reached all 50. With user-aware shards, the
unlearnt forest matched a from-scratch forest without Carol exactly (difference 0.0).

!!! warning "The trade-off"
    The sharded forests were a few points **less accurate**, because each tree sees a fifth of the data. You pay a little
    accuracy every day so that forgetting is cheap on the day someone asks. Lesson 07 meets the same trade-off in
    neural networks, as SISA.

## Concepts used here

- [Support vector machines](../ml-basics/support-vector-machines.md)
- [Decision trees and random forests](../ml-basics/decision-trees-and-random-forests.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Quiz

```quiz
- q: Deleting a non-support vector from an SVM changes the boundary by how much?
  options:
    - Nothing meaningful (about 10⁻⁸)
    - About half
    - It flips the boundary.
  answer: 0
  why: Non-support vectors have zero influence on the boundary.
- q: What share of Carol's digits were support vectors?
  options:
    - 40.5%
    - 75.0%
    - 97.5%
  answer: 2
  why: Unusual data is what the model leans on, so it is the expensive data to forget.
- q: How many of 50 bootstrap trees did Carol's rows reach?
  options:
    - 10
    - 31
    - 50
  answer: 2
  why: Bootstrap bags overlap heavily; 40 rows were enough to touch every tree.
- q: With user-aware shards, how many trees were retrained to forget Carol?
  options:
    - 10
    - 31
    - 50
  answer: 0
  why: All her data was in one shard, so only that shard's 10 trees needed rebuilding.
- q: What is the price of user-aware shards?
  options:
    - A few points of accuracy, because each tree sees less data
    - Nothing at all
    - Inexact forgetting
  answer: 0
  why: Test accuracy fell from 97.2% to 94.4%, but forgetting became exact and five times cheaper for Carol.
```

## Open question → Lesson 04

Every model so far had something to exploit, whether sums, a formula, a single optimum or locality. **A neural network has
none of them.** What happens to Carol inside a neural network?

[Next: Lesson 04, deleting is not forgetting :material-arrow-right:](04-deleting-is-not-forgetting.md){ .md-button }
