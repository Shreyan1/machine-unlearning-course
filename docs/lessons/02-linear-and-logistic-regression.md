---
title: "Lesson 02 · Linear and logistic regression"
description: Ridge regression forgets exactly with a Sherman-Morrison downdate; logistic regression forgets approximately with a Newton step.
---

# Lesson 02 · Linear and logistic regression, from exact to approximate

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 1 · Classical ML</span><span class="chip" markdown="span">:material-stairs-up: Rung 2</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/02-Classical-Linear-and-Logistic-Regression.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/02-Classical-Linear-and-Logistic-Regression.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 30 minutes · 2 checkpoints"
    By the end of this lesson you can

    - measure how hard one person pulls a linear model, using leverage,
    - remove her from ridge regression exactly, and say when the downdate beats a refit,
    - remove her from logistic regression approximately, and measure how close you got.

## The story

Two obstacles break the simple subtraction from Lesson 01.

1. **Coupled sums.** Ridge regression is built from sums, but its answer needs a matrix inverse, which mixes every point
   with every other. We can still forget exactly, with one line of linear algebra.
2. **No formula at all.** Logistic regression's weights are defined only as "where the slope is zero". Forgetting
   becomes **approximate** for the first time, and we must start **measuring** how close we got.

The request is the same as before. Carol, who wrote 40 thick-marker digits, asks to be erased. This time the stakes are
higher, because these models remember her far more than Naive Bayes did. Ridge reads 95.0% of her digits but only
67.5% of unseen digits in her style. Logistic regression reads 92.5% against 77.5%. Both gaps are her trace in the
weights, and in neither model can you point at the weights that are hers.

This lesson is where the course's most important habit begins. When a method cannot be checked for an identical
result, it must be **measured** against a model that never saw the data.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** ridge regression and logistic regression on the digits.</li>
<li markdown>**Show the issue.** Measure each point's **leverage**, the classical fingerprint of memorisation.</li>
<li markdown>**Untrain.** 40 Sherman-Morrison downdates for ridge; one Newton step for logistic regression.</li>
<li markdown>**Show the result** against models that never saw Carol.</li>
<li markdown>**Prove it** for ridge, and **measure** the remaining distance for logistic regression.</li>
</ol>

## What each step teaches

**Step 1. Train.** Ridge is fitted to one-hot targets with \(\lambda = 1\), which turns a regression into a classifier.
Logistic regression is trained to its exact best point by Newton's method, in 7 jumps. Both are models with a single
best answer, so "the model without Carol" is one clear target.

**Step 2. Show the issue.** Leverage, \(h = x^\top A^{-1} x\), is worked out for every training digit. It shows in one
number how hard each point pulls the fit towards itself. The step teaches that unusual data is what a model leans on
and remembers. That is why Carol is the hard case all through the course, not a random user.

**Step 3. Untrain.** Ridge gets 40 Sherman-Morrison downdates, one per digit. Each one updates the stored inverse
directly instead of inverting again. Logistic regression gets one Newton step on the retain set, starting from the
trained weights. The step teaches two ways of taking a point out, one exact and one an estimate.

**Step 4. Show the result.** Both models are scored on Carol's digits, on look-alikes and on the test set, next to
models trained from scratch without her. The step teaches you to read the forget set first, since that is where any
error left by an approximate method shows.

??? deep "Go deeper · step 5, the timing test and the link between the two parts"
    **Step 5. Prove and measure.** For ridge, the downdated weights are compared with a refit, number by number. For
    logistic regression there is no "identical" to check, so the lesson measures the distance between the unlearnt
    and the retrained weights after 1, 2 and 3 Newton steps, and the slope left on the retain set, called the residual
    gradient.

    **The timing test.** On the real lab both methods take under a millisecond, so the lesson grows the training set
    with made-up rows of 64 features, from 2,000 to 300,000, and removes the same 40 rows each time. This shows how
    each cost grows, which is what matters in production.

    **The link.** Finally, the lesson takes one Newton step on ridge and finds it gives the same weights as the
    downdate. That one result explains the whole difference between exact and approximate unlearning.

## Key results

<div class="stats">
<div><strong>0.116</strong><span>Carol's mean leverage, about three times everyone else's</span></div>
<div class="is-good"><strong>4.38 × 10⁻¹³</strong><span>ridge after downdates against a refit, rounding error</span></div>
<div class="is-good"><strong>94.8%</strong><span>of the gap closed by one Newton step</span></div>
<div><strong>61.6×</strong><span>downdate speed-up over a refit, at 300,000 rows</span></div>
</div>

**Leverage.** Carol's digits had a mean leverage of **0.116**, against 0.039 for everyone else. That is about three times the pull on the model.

**Ridge is exact.**

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 95.0% | 45.0% | 45.0% |
| Unseen thick digits | 67.5% | 48.8% | 48.8% |
| Test digits | 94.6% | 93.9% | 93.9% |

The largest weight difference from a refit was **4.38 × 10⁻¹³**, just rounding error. The downdate's cost depends only on
what you delete; at 300,000 rows it was **61.6 ×** faster than a refit.

The **After** and **Never saw Carol** columns match on every row, so the downdate did what a refit does. The size of the
drop on Carol, 50 points, shows how much ridge had remembered her. On the real lab, though, the 40 downdates took
0.53 ms and a refit only 0.18 ms. The speed-up appears only as the data grows.

| Rows kept | Refit | Downdate | Downdate is faster by |
|---|---|---|---|
| 2,000 | 0.2 ms | 0.46 ms | 0.4× (slower) |
| 20,000 | 1.5 ms | 0.46 ms | 3.3× |
| 100,000 | 11.3 ms | 0.50 ms | 22.7× |
| 300,000 | 30.0 ms | 0.49 ms | 61.6× |

**Logistic regression is approximate.**

| Newton steps | Share of the gap to retraining closed |
|---|---|
| 1 | 94.8% |
| 2 | 99.9% |
| 3 | 100.0% |

One step took 6.0 ms against 40.7 ms for a full refit. It moved Carol's accuracy from 92.5% to 60.0%, close to the
62.5% from a retrained model.

| | Before | After one step | Never saw Carol |
|---|---|---|---|
| Carol's digits | 92.5% | 60.0% | 62.5% |
| Unseen thick digits | 77.5% | 57.5% | 57.5% |
| Test digits | 97.2% | 97.0% | 97.0% |

Two rows already match the retrained model. Only **Carol's digits** differ, by 2.5 points, which is one digit out of 40.
The gap in the weights went from 3.148 to 0.165 after one step. The slope left on the retain set went from 12.5 to
1.21, and after three steps to 0.0000239. "Approximate" here means a small, measured distance, not a guess.

??? checkpoint "Checkpoint 1 · After unlearning, ridge reads 45.0% of Carol's digits and logistic regression 60.0%. Which result is exact, and how do you know?"
    **Ridge's.** Its 45.0% equals the never-saw-Carol model's 45.0%, and its weights match a refit to 4.38 × 10⁻¹³.
    Logistic regression's 60.0% is one digit short of the retrained model's 62.5%, and its weights are still 0.165
    away. A lower or higher score proves nothing on its own. What counts is the match with the model that never saw
    her.

!!! note "The link"
    The Sherman-Morrison downdate *is* a Newton step, one that is exact because ridge's loss is a perfect bowl.
    Logistic regression's loss is only roughly a bowl, so the same step lands near the answer, not on it. That is the
    whole difference between exact and approximate unlearning.

In the lesson, one Newton step on ridge matched the downdate to within 1.37 × 10⁻¹³.

??? checkpoint "Checkpoint 2 · A Newton step on ridge lands exactly on the retrained weights, but on logistic regression it closes only 94.8% of the gap. Why?"
    **The step assumes the loss is a perfect bowl.** It reads the slope and the curvature where it stands and jumps to
    the bottom of the bowl with that shape. Ridge's loss *is* exactly such a bowl, so the jump lands on the true
    bottom. Logistic regression's loss is only close to a bowl near the bottom, so the jump lands close, and each extra
    step gets closer.

## Concepts used here

- [Linear and ridge regression](../ml-basics/linear-and-ridge-regression.md)
- [Logistic regression](../ml-basics/logistic-regression.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Limits of this lesson

**A tiny lab and made-up rows.** The real data has 1,257 digits, so every timing is tiny. The scaling test uses random
rows of 64 features, which shows how the costs grow but not how a real system behaves.

**Small, convex models.** Logistic regression here has 650 weights, so its Hessian is 650 × 650 and easy to invert.
The same step on the course's network would need about 29 GB, and the network has no single bowl to aim at.

**No guarantee yet.** The Newton step is measured, not certified. A formal guarantee needs noise added at training
time, as in Guo et al. (2019), which [Certified unlearning](../unlearning/certified-unlearning.md) covers.

**One setting, one batch.** The lesson uses \(\lambda = 1\) and removes all 40 digits in one step. The notebook's tasks
ask what changes with less regularisation, and with one step per digit.

## Notes to take

!!! notes "Notes to take"
    - **Leverage.** \(h = x^\top A^{-1} x\). Carol 0.116, everyone else 0.039. Unusual points pull hardest.
    - **Ridge.** Built from sums, coupled by an inverse. Sherman-Morrison removes a point exactly.
    - **Ridge proof.** Weights matched a refit to 4.38 × 10⁻¹³. Carol fell from 95.0% to 45.0%, the same as a refit.
    - **Ridge cost.** Grows with what you delete. Slower than a refit at 2,000 rows, 61.6 times faster at 300,000.
    - **Logistic regression.** No formula. One Newton step from the trained weights estimates the retrained model.
    - **Logistic result.** One step closed 94.8% of the gap and two closed 99.9%. Carol 60.0% against 62.5%.
    - **The link.** The downdate is a Newton step on a perfect bowl, so it is exact.
    - **New habit.** For approximate methods, "proof" means measuring the distance to the gold standard.
    - **Trap.** A leftover error shows on the forget set, not on test accuracy.

## Quiz

```quiz
- q: What does leverage measure?
  options:
    - How hard one training point pulls the model towards itself
    - The model's test accuracy
    - The size of the dataset
  answer: 0
  why: Carol's digits had about three times the average leverage, which is why she is the hard case.
- q: How did ridge regression forget Carol exactly?
  options:
    - Sherman-Morrison downdates of the inverse
    - Gradient ascent
    - Deleting its largest weights
  answer: 0
  why: The downdate updates the inverse for each removed point, matching a refit to rounding error.
- q: How much of the gap did one Newton step close for logistic regression?
  options:
    - 8%
    - 94.8%
    - 100%
  answer: 1
  why: One step closed 94.8%; two steps closed 99.9%.
- q: Why is logistic regression's unlearning "approximate"?
  options:
    - Its weights have no formula, so the Newton step only estimates the new answer.
    - It has no gradient.
    - It cannot be retrained.
  answer: 0
  why: Without a closed form, we estimate and then measure the remaining distance.
- q: What new habit does this lesson start?
  options:
    - Measuring the distance to the gold standard for approximate methods
    - Never retraining
    - Ignoring the test set
  answer: 0
  why: From here on, "proof" for approximate methods means measuring how close they got.
- q: On the real lab, 40 downdates took 0.53 ms and a refit 0.18 ms. Why does the lesson still favour the downdate?
  options:
    - The refit gave wrong weights.
    - Its cost stays flat as the data grows, while a refit's cost grows with all the data kept.
    - The downdate also removes the test set.
  answer: 1
  why: At 300,000 rows the downdate was 61.6 times faster. What matters is how each cost grows.
- q: After one Newton step, which measurement still differed from the retrained model?
  options:
    - Test accuracy
    - Accuracy on unseen thick digits
    - Accuracy on Carol's digits, 60.0% against 62.5%
  answer: 2
  why: The small error left by an approximate method shows on the data that was removed, so check the forget set first.
- q: Why does one Newton step on ridge give exactly the downdate's weights?
  options:
    - Ridge's loss is a perfect bowl, so a step built from its slope and curvature lands exactly on the bottom.
    - Ridge has no Hessian.
    - The downdate secretly retrains the model.
  answer: 0
  why: The two agreed to 1.37 × 10⁻¹³. On a loss that is only roughly a bowl, as in logistic regression, the same step lands near.
```

## Open question → Lesson 03

!!! levelup "Level up"
    You can now forget exactly through an inverse, and forget approximately with a step you can measure. Next quest,
    [Lesson 03, SVM and random forest](03-svm-and-random-forest.md), where there is no gradient at all.

The Newton step needed gradients, an invertible Hessian and a single best answer. Decision trees have no gradient at
all, and an SVM ignores most of its data. Is there a different property, **locality**, that makes forgetting cheap?

[On to Lesson 03, SVM and random forest :material-arrow-right:](03-svm-and-random-forest.md){ .md-button }
