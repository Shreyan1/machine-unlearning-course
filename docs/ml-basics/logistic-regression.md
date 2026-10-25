---
title: Logistic regression
description: Logistic regression outputs probabilities and has no closed-form answer, so unlearning it becomes approximate.
---

# Logistic regression

!!! oneline "In one line"
    Logistic regression is a straight-line model that outputs **probabilities** for each class, and its weights are
    found by walking downhill on the loss, not from a formula.

## Why it matters

Logistic regression is where unlearning first becomes **approximate**. There is no formula for its weights, only the
rule "the slope of the loss is zero here". So we cannot subtract a point exactly. Instead we *estimate* where the
answer moves, and then we must **measure** how close the estimate is. That habit of measuring runs through the rest of
the course.

## A simple example

A bank wants to predict whether a loan will be repaid. Logistic regression combines facts like income and existing
debt into a score, then squeezes the score into a probability between 0 and 1. For example, it might estimate a 72% chance of repayment.

## How it works

<!-- diagram: logistic-regression -->

<ol class="steps" markdown>
<li markdown>**Score.** Multiply the input by the weights, as in linear regression.</li>
<li markdown>**Squeeze.** Turn the score into a probability with the sigmoid (two classes) or softmax (many classes) function.</li>
<li markdown>**Train.** Adjust the weights to lower the [cross-entropy loss](loss-functions.md). The best weights sit at the
bottom of a smooth, bowl-shaped valley, where the slope is zero.</li>
</ol>

Because the valley is bowl-shaped (the technical word is **convex**), there is exactly **one** best answer.

### Forgetting with a Newton step

When Carol is removed, the bottom of the valley moves a little. We do not know exactly where, but we know the **slope**
(gradient) and the **curvature** (Hessian) where we stand. From those, one jump called a **Newton step** estimates the
new bottom.

Lesson 02 measures how quickly repeated Newton steps close the gap to retraining.

| Newton steps | Share of the gap to the retrained model closed |
|---|---|
| 1 | 94.8% |
| 2 | 99.9% |
| 3 | 100.0% |

One step took 6.0 ms, against 40.7 ms for a full refit. So "approximate" is not a dirty word; it is a **measurable
distance**, and here a tiny one.

!!! note "The link to ridge"
    The Sherman-Morrison downdate for ridge *is* a Newton step. It is exact because ridge's loss is a perfect bowl.
    Logistic regression's loss is only roughly a bowl near the bottom, so the same step lands *near* the answer, not
    *on* it. That is the whole difference between exact and approximate unlearning.

### Why it stops working for big models

A Newton step needs a Hessian, a table with one row and one column per weight. For the course's small neural network
(85,002 weights), that is about 29 GB. And neural networks do not have a single bowl-shaped valley at all. See
[Neural networks](neural-networks.md).

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
logreg = classical.SoftmaxNewton(lam=1.0).fit(L.X_train, L.y_train)
unlearned = logreg.unlearn_newton(L.Xr, L.yr, steps=1)    # one Newton step on the retain set
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting an approximate method without measuring it.** Always compare against a model that never saw the data.
    - **Assuming the Newton step scales.** It needs a Hessian you can store and invert, and a single best answer.

## Key takeaways

- Logistic regression outputs probabilities; its weights have no closed-form formula.
- Its loss is convex, so there is one best answer.
- One Newton step closes about 95% of the gap to retraining; two steps close almost all of it.
- From here on, "proof" means measuring the distance to the gold standard.

## Quiz

```quiz
- q: Why can we not remove a point from logistic regression by subtraction?
  options:
    - Its weights have no formula; they are defined by where the loss slope is zero.
    - It has no weights.
    - It only works on two classes.
  answer: 0
  why: Without a closed form, there is nothing to subtract from, so we estimate the new answer instead.
- q: What does "convex" mean for logistic regression's loss?
  options:
    - It is bowl-shaped, with one best answer.
    - It has many equally good valleys.
    - It is always zero.
  answer: 0
  why: A convex loss has a single lowest point, which is what makes the Newton step reliable.
- q: In Lesson 02, how much of the gap to the retrained model did one Newton step close?
  options:
    - About 50%
    - About 95%
    - Exactly 100%
  answer: 1
  why: One step closed 94.8% of the gap; two steps closed 99.9%.
- q: Why does the Newton step not work for large neural networks?
  options:
    - The Hessian is far too big, and there is no single best answer.
    - Neural networks have no gradients.
    - Neural networks cannot output probabilities.
  answer: 0
  why: The Hessian has one row and column per weight, and a neural network's loss has many valleys, not one bowl.
```

## Try it

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [02 · Linear and logistic regression](../lessons/02-linear-and-logistic-regression.md).
