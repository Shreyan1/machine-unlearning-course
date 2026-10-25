---
title: "Lesson 06 · Retrain and the gold band"
description: Retrained networks disagree, so the gold standard is a band. Measure it, check the original falls outside and price exact retraining.
---

# Lesson 06 · Retraining from scratch, the gold standard is a band

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~25 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 3 · Exact unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 5</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb){ .md-button }
</div>

## The story

Classical models are **deterministic**. Retrain them twice and you get the same model to the last digit. A neural network
depends on random starting weights and random batch order, so retraining it is like **rolling dice**. Every roll is an
equally valid "model that never saw Carol". So an unlearning method has to hit a **band**, not a point.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** classical models five times and see how wide *their* band is.</li>
<li markdown>**Show the issue.** Retrain the network 20 times without Carol and measure the spread.</li>
<li markdown>Compare deleting Carol, a random group of users and a whole class.</li>
<li markdown>**Untrain** by retraining, and check it against the band.</li>
<li markdown>Test the shortcut "just keep training without her", and **price** exact retraining.</li>
</ol>

## Key results

- **Classical models.** Naive Bayes always gave 27.5% on Carol; logistic regression always 62.5%. The band has zero width.
- **The network, 20 retrains.** Mean **62.0%** on Carol, standard deviation 5.6%, range **47.5% to 70.0%**. Test
  accuracy 98.2% ± 0.34%. The original scored **100.0%**, far outside.
- **The band depends on the request.** Wide and in the middle for Carol; narrow and near 100% for random users (the
  original is already inside); exactly 0% for a whole class.

| Method | Forget accuracy | Verdict |
|---|---|---|
| Original | 100.0% | FAIL |
| New retrain (seed 999) | 62.5% | PASS |

**The shortcut trap.** After 20 more epochs of training the original on \(D_r\) only, Carol was still at **95.0%**,
against a band of 62.0% ± 9.2%. A model that already fits Carol has nothing pushing it away from her. Only a fresh start
is exact.

**The cost** (placeholder production numbers). Retraining daily to batch requests ≈ $7.3 million a year; weekly ≈ $1.04
million; monthly ≈ $243,000. The cost grows with the data you **keep**, not the data you delete.

## Concepts used here

- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The gold band](../unlearning/gold-band.md)
- [Neural networks](../ml-basics/neural-networks.md)

## Quiz

```quiz
- q: Why do classical models like Naive Bayes have a band of width zero?
  options:
    - They are deterministic; every retrain gives the same model.
    - They are always perfect.
    - They cannot be retrained.
  answer: 0
  why: Without randomness in training, there is only one possible retrained model.
- q: Across 20 retrains, what was the range of accuracy on Carol's digits?
  options:
    - 61% to 63%
    - 47.5% to 70.0%
    - 0% to 100%
  answer: 1
  why: Retrained networks disagree by more than 20 points, so a single retrain is just one draw.
- q: For random typical users, where is the original model relative to the band?
  options:
    - Already inside it
    - Far above it
    - Far below it
  answer: 0
  why: Typical data was never memorised, so the original already behaves like it never saw it.
- q: After 20 more epochs of training on the retain set only, what was Carol's accuracy?
  options:
    - 62.0%
    - 95.0%
    - 0%
  answer: 1
  why: Continuing to train is not retraining; it stays far outside the band.
- q: What does the cost of exact retraining grow with?
  options:
    - The size of the data you keep
    - The size of the data you delete
    - The number of test examples
  answer: 0
  why: Every retrain processes all the retained data again.
```

## Open question → Lesson 07

In Lesson 03, a forest forgot Carol by retraining only **10 of 50 trees**, because it was *designed* with user-aware
shards. Can a neural network be designed the same way?

[On to Lesson 07, SISA :material-arrow-right:](07-sisa.md){ .md-button }
