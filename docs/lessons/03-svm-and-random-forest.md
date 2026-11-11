---
title: "Lesson 03 · SVM and random forest"
description: Locality makes forgetting cheap. SVMs ignore non-support vectors; forests retrain only the trees that saw a row, especially with user-aware shards.
---

# Lesson 03 · SVMs and random forests, forgetting by locality

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 1 · Classical ML</span><span class="chip" markdown="span">:material-stairs-up: Rung 3</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 10 minutes · 3 checkpoints"
    By the end of this lesson you can

    - tell when forgetting a point from an SVM is free and when it needs a re-solve,
    - count how many trees of a forest a request will touch,
    - design a forest that forgets Carol exactly by rebuilding a fifth of it, and name the price.

## The story

A decision tree has no gradient and no curvature, so the Newton step is gone. Yet forgetting can still be cheap, thanks
to the most useful property in the course, **locality**. If you know *which part* of a model a point influenced, you
only rebuild that part.

| Model | Where locality comes from | What forgetting costs |
|---|---|---|
| **SVM** | The boundary depends only on the support vectors | Nothing, unless you delete a support vector |
| **Random forest** | Each tree only saw its own bag of rows | Retrain only the trees whose bag held the row |

In Lesson 02, forgetting from logistic regression needed three things, a gradient, a curvature table you can invert
and a single best answer. Trees have none of them. Without a new idea, the only exact option would be to rebuild the
whole model for every request.

That is what is at stake. Carol has asked to be forgotten, and she is not the only one. A service that gets many
requests a day cannot rebuild everything each time. This lesson finds out when forgetting is free, when it is not,
and how a forest can be built so that Carol costs a fifth of it.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** an SVM (first on a 2-D toy problem, then on the digits) and a 50-tree forest.</li>
<li markdown>**Show the issue.** Is Carol a support vector? How many trees did her rows reach?</li>
<li markdown>**Untrain**, comparing three forest designs, namely bootstrap bags, random shards and user-aware shards.</li>
<li markdown>**Show the result.** Accuracy and trees retrained.</li>
<li markdown>**Prove it.** The user-aware forest equals a forest that never saw Carol.</li>
</ol>

## What each step teaches

**Train.** The toy problem is two overlapping clouds of 200 points, small enough to draw. It lets you *see* the
support vectors, the ringed points on the edge of the street. The digits SVM and the 50-tree forest are the real lab.
Both get 100.0% of Carol's digits right.

**Show the issue.** Two counts tell the whole story. For the SVM, how many of Carol's digits are support vectors. For
the forest, how many trees her rows reached. Both ask the same question, how much of the model depends on her.

??? deep "Go deeper · how much the two models learnt from Carol"
    Lesson 03 compares each original model with one trained without Carol.

    | Model | Set | Original | Never saw Carol |
    |---|---|---|---|
    | SVM | Carol's digits | 100.0% | 57.5% |
    | SVM | Unseen thick-marker digits | 87.5% | 48.8% |
    | SVM | Test digits | 99.4% | 99.4% |
    | Forest | Carol's digits | 100.0% | 30.0% |
    | Forest | Unseen thick-marker digits | 70.0% | 48.8% |
    | Forest | Test digits | 97.2% | 97.2% |

    Both models learnt Carol herself and her style, and neither needed her to do well on the test set.

**Untrain.** All three forests have 50 trees and use the same algorithm. Only the way the rows are shared out
changes. This isolates one design choice and shows how much it alone decides the cost of forgetting.

**Show the result.** The table puts accuracy next to the trees retrained, so you see the trade-off in one place.

**Prove it.** "Exact" is checked, not assumed. Lesson 03 trains a fresh forest from scratch on the same bags without
Carol and compares every predicted probability.

??? checkpoint "Checkpoint 1 · A forest service gets 1,000 requests a day, each from a typical user with one row. With bootstrap bags, about how many tree rebuilds is that a day?"
    **About 31,000.** One row reached 31 of 50 bootstrap trees in Lesson 03, so 1,000 rows is about 1,000 × 31 =
    31,000 tree rebuilds. With user-aware shards one row reached 9 trees, so about 9,000. For people with many rows,
    like Carol, the gap is far bigger, 50 trees against 10.

## Key results

<div class="stats">
<div class="is-good"><strong>2.3 × 10⁻⁸</strong><span>SVM boundary change after deleting a non-support vector</span></div>
<div class="is-bad"><strong>97.5%</strong><span>of Carol's digits are support vectors, against 40.5%</span></div>
<div class="is-bad"><strong>50 of 50</strong><span>bootstrap trees reached by Carol's rows</span></div>
<div class="is-good"><strong>10 of 50</strong><span>trees rebuilt with user-aware shards, exact</span></div>
</div>

**SVM.** On the 2-D toy problem, 54 of 200 points were support vectors. Deleting a non-support vector moved the boundary
by 2.3 × 10⁻⁸ (nothing); deleting a support vector moved it by 1.1 × 10⁻³.

On the digits, **97.5%** of Carol's digits were support vectors, against **40.5%** of everyone else's. For 40 typical
non-support-vector users, the original model already *was* the unlearnt model on 100% of inputs. For Carol, the only
exact option was to re-solve.

The 2.3 × 10⁻⁸ is the solver's own precision, so in practice no change at all. Carol's 97.5% is 39 of her 40 digits.
Unusual data sits close to the boundary, which is exactly where an SVM leans its weight.

**Random forest.**

| Design (50 trees) | Test accuracy | Trees to retrain for 1 random row | Trees to retrain for Carol |
|---|---|---|---|
| Bootstrap bags | 97.2% | 31 | 50 |
| Random shards | 94.4% | 8 | 49 |
| **User-aware shards** | 94.4% | 9 | **10** |

A typical row appears in about 63% of bootstrap trees, and Carol's 40 rows reached all 50. With user-aware shards, the
unlearnt forest matched a from-scratch forest without Carol exactly (difference 0.0).

Read the table row by row.

- **Bootstrap bags.** The best accuracy, but no locality worth having. One row reached 31 trees, and Carol's 40 rows
  reached every tree.
- **Random shards.** Each row lives in one shard of 10 trees, so one row reached 8. But Carol's rows were scattered
  over all five shards, so she still reached 49 trees.
- **User-aware shards.** All of Carol's rows sit in one shard, so forgetting her rebuilt only that shard's 10 trees.
  After unlearning, her accuracy fell from 95.0% to 42.5%.

??? deep "Go deeper · why one row reaches 63% of bootstrap trees"
    A bootstrap bag draws \(n\) rows from \(n\) with replacement. A given row is missed on every draw with chance
    \((1 - 1/n)^n\), which is close to \(1/e \approx 0.37\). So it lands in about 63% of the bags. Lesson 03 measured a
    typical row in 31.6 of 50 trees.

    Carol has 40 rows, so a tree escapes her only if it misses all of them, with chance about \(0.37^{40}\). That is
    effectively zero, which is why all 50 trees met her.

!!! warning "The trade-off"
    The sharded forests were a few points **less accurate**, because each tree sees a fifth of the data. You pay a little
    accuracy every day so that forgetting is cheap on the day someone asks. Lesson 07 meets the same trade-off in
    neural networks, as SISA.

??? checkpoint "Checkpoint 2 · The random-shards forest rebuilt 8 trees for one row but 49 for Carol. What single change brought her down to 10?"
    **Putting all of her rows in one shard.** Random sharding places each row in one shard, but a person with 40 rows
    lands in all five. User-aware sharding keeps each person together, so forgetting Carol touches only her shard's
    10 trees. Accuracy stayed at 94.4%, the same as random shards.

## Limits of this lesson

**The data is tiny.** The lab has 1,257 digits, so a full SVM re-solve takes a fraction of a second. For kernel SVMs the
cost grows roughly with the square or the cube of the number of rows, so at scale a re-solve is a real job.

**The kernel is not fixed.** With `gamma="scale"`, the SVM's kernel width comes from the training data, so deleting any
point nudges it a little. That is why the lesson checks that predictions stay the same instead of assuming it.

**One draw of the dice.** The tree counts, 31, 8 and 9, come from one random draw of bags. Another seed would give
slightly different counts, though the pattern would hold.

**Carol's identity was known in advance.** User-aware shards need every row tagged with its owner before training.

**Only accuracy is measured.** This lesson does not run a privacy attack. Lesson 05 introduces one.

**Whole trees are rebuilt.** Lesson 03's notebook points to DaRE forests (Brophy and Lowd 2021), which rebuild only the
affected subtrees, and HedgeCut (Schelter et al. 2021), which keeps other subtrees ready for fast deletion.

??? checkpoint "Checkpoint 3 · Carol's SVM re-solve took a fraction of a second here. Would you promise the same for a kernel SVM trained on millions of rows?"
    **No.** The cost of re-solving a kernel SVM grows roughly with the square or the cube of the number of rows. A
    thousand times more rows can mean a million times more work or worse. Plan time and compute for unusual users,
    since they are the ones who are almost all support vectors.

## Concepts used here

- [Support vector machines](../ml-basics/support-vector-machines.md)
- [Decision trees and random forests](../ml-basics/decision-trees-and-random-forests.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Notes to take

!!! notes "Notes to take"
    - **Locality.** If you know which part of a model a point influenced, rebuild only that part.
    - **SVM rule.** Only support vectors matter. Deleting any other point moved the toy boundary by 2.3 × 10⁻⁸.
    - **Support vector deleted.** The boundary moved by 1.1 × 10⁻³, so you must re-solve.
    - **Carol and the SVM.** 97.5% of her digits were support vectors, against 40.5% of everyone else's.
    - **Typical users.** Deleting 40 non-support vectors left predictions identical on 100% of inputs.
    - **Forest rule.** Rebuild only the trees whose bags held the row, with the same seed and the same bag minus the row.
    - **Bootstrap trap.** One row reaches about 63% of trees, and Carol reached all 50.
    - **User-aware shards.** 10 of 50 trees for Carol, exact, with a difference of 0.0.
    - **Price.** Test accuracy 94.4% against 97.2%, paid every day.

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
- q: Why did random shards still retrain 49 of 50 trees for Carol?
  options:
    - Random shards keep no record of which rows each tree saw.
    - Her 40 rows were scattered over all five shards.
    - Random shards use larger bags than bootstrap forests.
  answer: 1
  why: Sharding by row puts each row in one shard, but a person with many rows lands in every shard.
- q: How did Lesson 03 prove that the user-aware forest had forgotten Carol exactly?
  options:
    - It checked that her accuracy fell below 50%.
    - It compared the forest with the original forest.
    - It compared every predicted probability with a forest trained from scratch on the same bags without her.
  answer: 2
  why: The largest difference was 0.0, so the unlearnt forest is a forest that never saw her.
- q: Lesson 03 deleted 40 typical users who were not support vectors and trained the SVM again. What happened?
  options:
    - Predictions stayed identical on 100% of inputs.
    - The boundary moved as much as when Carol was removed.
    - Test accuracy fell by a few points.
  answer: 0
  why: For points with zero weight, the original model already is the unlearnt model.
```

## Open question → Lesson 04

!!! levelup "Level up"
    You can now tell when forgetting is free, count the trees a request touches and design a forest that forgets one
    person exactly. Next quest, [Lesson 04, deleting is not forgetting](04-deleting-is-not-forgetting.md), where a
    neural network offers none of these tricks.

Every model so far had something to exploit, whether sums, a formula, a single optimum or locality. **A neural network has
none of them.** What happens to Carol inside a neural network?

[On to Lesson 04, deleting is not forgetting :material-arrow-right:](04-deleting-is-not-forgetting.md){ .md-button }
