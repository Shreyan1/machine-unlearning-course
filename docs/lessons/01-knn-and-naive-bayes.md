---
title: "Lesson 01: k-NN and Naive Bayes"
description: Two models where forgetting is exact and essentially free, by deleting rows or subtracting sums.
---

# Lesson 01: k-NN and Naive Bayes, when forgetting is free

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~20 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 1 · Classical ML</span><span class="chip" markdown="span">:material-stairs-up: Rung 1</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb){ .md-button }
</div>

## The story

In 2015, Cao and Yang coined "machine unlearning" with a simple observation. Many models are **sums over the training
data**, and if a model is a sum, forgetting a data point is a subtraction. This lesson makes two such models forget
Carol, and proves they are identical to models that never saw her.

| Model | What the trained model actually is | How to forget a row |
|---|---|---|
| **k-NN** | the training data itself | delete the row |
| **Gaussian Naive Bayes** | per-class counts, sums and sums of squares | subtract the row from those sums |

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** k-NN (k = 5) and Gaussian Naive Bayes on the digits.</li>
<li markdown>**Show the issue**: who does k-NN consult for a new thick-marker digit? Where is Carol inside Naive Bayes's averages?</li>
<li markdown>**Untrain**: tombstone her rows in k-NN; subtract them from Naive Bayes's sums.</li>
<li markdown>**Show the result** before and after.</li>
<li markdown>**Prove it** against models built without her from the start.</li>
</ol>

## Key results

**k-NN**

- Before: **85.8%** of the neighbours consulted for new thick-marker digits were Carol's own digits.
- After deleting her rows (0.15 ms): **0.0%**. Test accuracy stayed at 98.3%.
- Predictions identical to a k-NN that never saw her on **100%** of 1,877 inputs.

**Naive Bayes**

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 60.0% | 27.5% | 27.5% |
| Unseen thick digits | 61.3% | 37.5% | 37.5% |
| Test digits | 91.1% | 90.9% | 90.9% |

The largest difference in any predicted log-probability versus the never-saw-Carol model: **exactly 0**.

**Two things to notice**

1. Naive Bayes barely memorised Carol: 60.0% on her digits against 61.3% on look-alikes.
2. Forgetting her made the model worse for everyone who writes like her (61.3% → 37.5%), because she was the only
   source of that style. Unlearning can hurt an under-represented group; Lesson 12 measures this.

**The trap is that preprocessing remembers too.** A `StandardScaler`'s stored mean moved by 0.0171 when Carol was removed.
An unlearning request must cover the whole pipeline.

## Concepts used here

- [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md)
- [Naive Bayes](../ml-basics/naive-bayes.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Quiz

```quiz
- q: What share of k-NN's neighbours for thick-marker digits were Carol's before unlearning?
  options:
    - 12.5%
    - 50.0%
    - 85.8%
  answer: 2
  why: She was the only person with that style, so her digits were consulted for almost every similar query.
- q: How did Naive Bayes forget Carol?
  options:
    - By subtracting her rows from the counts and sums
    - By retraining for 60 epochs
    - By gradient ascent
  answer: 0
  why: The model is just counts and sums per class, so removing her is a subtraction.
- q: How close was the unlearnt Naive Bayes to one that never saw Carol?
  options:
    - Identical; the largest difference was exactly 0
    - About 90% similar
    - Not close at all
  answer: 0
  why: Subtraction gives exactly the same statistics as never adding her in the first place.
- q: After forgetting Carol, Naive Bayes got worse on unseen thick-marker digits. Why?
  options:
    - She was the only source of that writing style.
    - The subtraction had a bug.
    - The test set changed.
  answer: 0
  why: Removing the only examples of a style removes the model's knowledge of that style. This is a fairness concern.
- q: Why must the StandardScaler be unlearnt too?
  options:
    - Its stored means were computed from the data, including Carol's.
    - Scalers store raw images.
    - It is not needed.
  answer: 0
  why: Preprocessing is also fitted on the data, so it carries the forget set's influence.
```

## Open question → Lesson 02

Both models here were independent sums. But linear regression multiplies by a matrix **inverse**, which couples every
point to every other, and logistic regression has no formula at all. Can we still take a point back out?

[Next: Lesson 02, linear and logistic regression :material-arrow-right:](02-linear-and-logistic-regression.md){ .md-button }
