---
title: "Lesson 01 · k-NN and Naive Bayes"
description: Two models where forgetting is exact and essentially free, by deleting rows or subtracting sums.
---

# Lesson 01 · k-NN and Naive Bayes, when forgetting is free

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~20 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 1 · Classical ML</span><span class="chip" markdown="span">:material-stairs-up: Rung 1</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 20 minutes · 2 checkpoints"
    By the end of this lesson you can

    - make a k-NN model forget a person by deleting rows, and a Naive Bayes model by subtracting sums,
    - prove each result is exact against a model that never saw her,
    - explain why forgetting can hurt people who resemble her, and why the scaler must forget too.

## The story

In 2015, Cao and Yang coined "machine unlearning" with a simple observation. Many models are **sums over the training
data**, and if a model is a sum, forgetting a data point is a subtraction. This lesson makes two such models forget
Carol, and proves they are identical to models that never saw her.

Carol wrote 40 of the lab's 1,257 training digits, all with a thick marker. Nobody else writes like her. She now uses
her right to erasure and asks for her data to be removed. Deleting her rows from a database is easy, but the models
built from that database may still carry her. For k-NN the problem is stark. The model keeps every training digit, so
it literally contains her handwriting, and any "show similar examples" feature could put it in front of other users.

The good news is that these two models are the easiest on the
[Ladder of Forgetting](../unlearning/ladder-of-forgetting.md). This lesson shows how easy, and sets the habit that every
later lesson follows. A result counts as forgotten only when it matches a model that never saw her.

| Model | What the trained model actually is | How to forget a row |
|---|---|---|
| **k-NN** | The training data itself | Delete the row |
| **Gaussian Naive Bayes** | Per-class counts, sums and sums of squares | Subtract the row from those sums |

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** k-NN (k = 5) and Gaussian Naive Bayes on the digits.</li>
<li markdown>**Show the issue.** Who does k-NN consult for a new thick-marker digit? Where is Carol inside Naive Bayes's averages?</li>
<li markdown>**Untrain.** Tombstone her rows in k-NN; subtract them from Naive Bayes's sums.</li>
<li markdown>**Show the result** before and after.</li>
<li markdown>**Prove it** against models built without her from the start.</li>
</ol>

## What each step teaches

**Step 1. Train.** Both models are fitted on all 1,257 digits. K-NN only stores them. Naive Bayes reduces them to three
arrays, a count per class and two tables of 10 × 64 sums. Seeing how little Naive Bayes keeps already hints at how
easy it will be to change.

**Step 2. Show the issue.** For k-NN, the lesson asks about 80 new thick-marker digits and looks at which training
rows answer. For Naive Bayes, it compares the class averages with and without Carol, and her thick strokes show up as a
faint brightening along the edges of every digit. The step teaches that "her data is in the model" can be seen and
counted, not just assumed.

**Step 3. Untrain.** K-NN marks her 40 rows as deleted with a **tombstone**, so searches skip them. Naive Bayes
subtracts each of her digits from its class's count and sums. Both take a fraction of a millisecond. The step teaches
that when a model is its data, or a sum of it, unlearning is a tiny edit.

**Step 4. Show the result.** The same measurements are taken again. Carol's share of the k-NN neighbours drops to zero,
and both models get worse on her style of writing. The step teaches that forgetting has visible effects, some of them
unwelcome.

??? deep "Go deeper · step 5 and the pipeline trap"
    **Step 5. Prove it.** A fresh k-NN and a fresh Naive Bayes are built on the 1,217 digits without Carol. The k-NN
    after deletion must give the same prediction on every one of 1,877 inputs, which are the training digits, the test
    digits and the 80 look-alikes. The Naive Bayes after subtraction must give the same log-probabilities, not only the
    same answers. This is the definition of exact unlearning, turned into a check you can run.

    **Part C. The trap.** A `StandardScaler`, which rescales each pixel using a stored mean and spread, is fitted with
    and without Carol. Its stored means differ. The scaler is a summation-form model too, so it must forget along with
    the model it feeds.

## Key results

<div class="stats">
<div class="is-bad"><strong>85.8%</strong><span>of k-NN's neighbours for thick-marker digits were Carol's</span></div>
<div class="is-good"><strong>100%</strong><span>same k-NN predictions as a model that never saw her, on 1,877 inputs</span></div>
<div class="is-good"><strong>exactly 0</strong><span>largest log-probability difference for Naive Bayes</span></div>
<div class="is-bad"><strong>0.0171</strong><span>shift in a stored scaler mean, the pipeline remembers</span></div>
</div>

**K-NN**

- Before deleting Carol's rows, **85.8%** of the neighbours for new thick-marker digits were hers.
- After deletion, none of the neighbours were hers. Test accuracy stayed at 98.3%.
- Predictions identical to a k-NN that never saw her on **100%** of 1,877 inputs.

The first line is the striking one. Carol is about 3% of the training data, yet she supplied about 343 of the 400
neighbours (80 queries times 5 neighbours) for digits in her style. Deleting her rows took 0.15 ms. Her own digits fell
from 75.0% to 52.5% and the look-alikes from 67.5% to 62.5%, because the rows that used to answer for them were hers.

**Naive Bayes**

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 60.0% | 27.5% | 27.5% |
| Unseen thick digits | 61.3% | 37.5% | 37.5% |
| Test digits | 91.1% | 90.9% | 90.9% |

The largest difference in predicted log-probability versus the model that never saw Carol was **exactly 0**.

Read the table column against column. **After** and **Never saw Carol** match on every row, which is the proof. Read it
row by row for the meaning. Test digits barely move, by 0.2 points, so most people notice nothing. Carol's digits and
the look-alikes both fall a long way, because her digits were the model's only picture of thick-marker writing. The
subtraction took 0.09 ms, against 0.49 ms for a refit.

??? checkpoint "Checkpoint 1 · The k-NN read 75.0% of Carol's digits before deletion and 52.5% after. Should the 52.5% worry you?"
    **No.** The k-NN after deletion gave the same prediction as a k-NN that never saw Carol on every input, her 40
    digits included. So a model that never saw her also reads exactly 52.5% of them. That is the target, and the
    unlearnt model hits it exactly. A lower score is only a problem when it is lower than what a never-saw-her model
    gets.

**Two things to notice**

1. Naive Bayes barely memorised Carol. It was right on 60.0% of her digits and 61.3% of look-alikes.
2. Forgetting her made the model worse for everyone who writes like her (61.3% → 37.5%), because she was the only
   source of that style. Unlearning can hurt an under-represented group; Lesson 12 measures this.

**The trap is that preprocessing remembers too.** A `StandardScaler`'s stored mean moved by 0.0171 when Carol was removed.
An unlearning request must cover the whole pipeline.

??? checkpoint "Checkpoint 2 · Naive Bayes was right on 60.0% of Carol's digits and 61.3% of look-alikes. Yet removing her dropped both by more than 20 points. How can a model that barely memorised her change so much?"
    **Memorising and being shaped are different.** Memorising means doing better on her own digits than on unseen
    digits like hers, and Naive Bayes did not (a gap of −1.3 points). But her digits were its only examples of the
    thick-marker style, so its averages for that style came from her. Remove her and the model loses the style, not
    her individual digits.

## Concepts used here

- [K-nearest neighbours](../ml-basics/k-nearest-neighbours.md)
- [Naive Bayes](../ml-basics/naive-bayes.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Limits of this lesson

**A tiny lab.** The data is 1,257 small digit images of 64 pixels each. Every timing is under a millisecond, so the
gap between subtracting and refitting is small here. The point is how the costs grow. Subtraction grows with what you
delete, and a refit grows with everything you keep.

**A tombstone is not an erasure.** The k-NN marks Carol's rows as deleted, but the rows stay in memory until the store
is cleaned up or rebuilt. Real systems also use approximate indexes, caches and backups, which this lesson does not
model. Lesson 21 does.

**The course's own Naive Bayes.** The library uses a fixed smoothing amount, so subtraction is exact. scikit-learn's
version sets its smoothing from the whole training set, Carol included, so subtraction there is close but not exact.
The notebook asks you to explain why.

**One person, one request.** Only Carol is forgotten, once. Thousands of add-and-subtract cycles can build up rounding
error, which this lesson does not test, though one of its tasks does.

## Notes to take

!!! notes "Notes to take"
    - **Summation form.** If a model is a sum over the data, forgetting is a subtraction, the idea of Cao and Yang (2015).
    - **k-NN.** The model is the data. Delete the rows. It took 0.15 ms.
    - **k-NN privacy.** Carol was 3% of the data but 85.8% of the neighbours for her style.
    - **Naive Bayes.** Stores `n`, `S1` and `S2` per class. Subtract each row. It took 0.09 ms.
    - **Proof.** k-NN matched a never-saw-Carol model on 100% of 1,877 inputs, and Naive Bayes to a difference of exactly 0.
    - **Memorising.** Naive Bayes barely memorised her, a gap of −1.3 points.
    - **Side effect.** Look-alike digits fell from 61.3% to 37.5% in Naive Bayes, because she was the only source of the style.
    - **Trap.** The scaler's stored mean moved by 0.0171. Unlearn the whole pipeline.
    - **Trap.** A tombstone hides rows but does not erase them.

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
- q: How does the lesson prove that the k-NN has forgotten Carol?
  options:
    - It checks that test accuracy stayed at 98.3%.
    - It compares predictions with a k-NN built without her, on 1,877 inputs, and they are identical.
    - It counts how many rows are left.
  answer: 1
  why: Exact unlearning means matching a model that never saw the data. Test accuracy alone cannot show that.
- q: Test accuracy for Naive Bayes moved only from 91.1% to 90.9% after unlearning. What does that tell you?
  options:
    - Nothing was forgotten.
    - The subtraction failed.
    - Most people's digits look nothing like Carol's, so removing her changes little for them.
  answer: 2
  why: The forgetting shows on her digits and her style, not on typical test digits. Always check the forget set.
- q: After the k-NN tombstones Carol's rows, what is still left to do in a real system?
  options:
    - Clean up or rebuild the store so the rows are truly removed, and handle copies such as caches and backups
    - Nothing, the tombstone erases the rows
    - Retrain the k-NN for many epochs
  answer: 0
  why: A tombstone hides rows from search. The answers are already exact, but the stored rows and their copies must still go.
```

## Open question → Lesson 02

!!! levelup "Level up"
    You can now make a model that is its data, or a sum of it, forget a person exactly and prove it. Next quest,
    [Lesson 02, linear and logistic regression](02-linear-and-logistic-regression.md), where the sums get tangled.

Both models here were independent sums. But linear regression multiplies by a matrix **inverse**, which couples every
point to every other, and logistic regression has no formula at all. Can we still take a point back out?

[On to Lesson 02, linear and logistic regression :material-arrow-right:](02-linear-and-logistic-regression.md){ .md-button }
