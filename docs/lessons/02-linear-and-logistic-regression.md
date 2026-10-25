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

## The story

Two obstacles break the simple subtraction from Lesson 01.

1. **Coupled sums.** Ridge regression is built from sums, but its answer needs a matrix inverse, which mixes every point
   with every other. We can still forget exactly, with one line of linear algebra.
2. **No formula at all.** Logistic regression's weights are defined only as "where the slope is zero". Forgetting
   becomes **approximate** for the first time, and we must start **measuring** how close we got.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** ridge regression and logistic regression on the digits.</li>
<li markdown>**Show the issue.** Measure each point's **leverage**, the classical fingerprint of memorisation.</li>
<li markdown>**Untrain.** 40 Sherman-Morrison downdates for ridge; one Newton step for logistic regression.</li>
<li markdown>**Show the result** against models that never saw Carol.</li>
<li markdown>**Prove it** for ridge, and **measure** the remaining distance for logistic regression.</li>
</ol>

## Key results

**Leverage.** Carol's digits had a mean leverage of **0.116**, against 0.039 for everyone else. That is about three times the pull on the model.

**Ridge is exact.**

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 95.0% | 45.0% | 45.0% |
| Test digits | 94.6% | 93.9% | 93.9% |

The largest weight difference from a refit was **4.38 × 10⁻¹³**, just rounding error. The downdate's cost depends only on
what you delete; at 300,000 rows it was **61.6 ×** faster than a refit.

**Logistic regression is approximate.**

| Newton steps | Share of the gap to retraining closed |
|---|---|
| 1 | 94.8% |
| 2 | 99.9% |
| 3 | 100.0% |

One step took 6.0 ms against 40.7 ms for a full refit. It moved Carol's accuracy from 92.5% to 60.0%, close to the
62.5% from a retrained model.

!!! note "The link"
    The Sherman-Morrison downdate *is* a Newton step, one that is exact because ridge's loss is a perfect bowl.
    Logistic regression's loss is only roughly a bowl, so the same step lands near the answer, not on it. That is the
    whole difference between exact and approximate unlearning.

## Concepts used here

- [Linear and ridge regression](../ml-basics/linear-and-ridge-regression.md)
- [Logistic regression](../ml-basics/logistic-regression.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

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
```

## Open question → Lesson 03

The Newton step needed gradients, an invertible Hessian and a single best answer. Decision trees have no gradient at
all, and an SVM ignores most of its data. Is there a different property, **locality**, that makes forgetting cheap?

[On to Lesson 03, SVM and random forest :material-arrow-right:](03-svm-and-random-forest.md){ .md-button }
