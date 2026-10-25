---
title: Linear and ridge regression
description: Linear regression finds the best straight-line fit; ridge adds a penalty that keeps the weights small. Both come from a formula.
---

# Linear and ridge regression

!!! oneline "In one line"
    Linear regression finds the straight line (or flat surface) that best fits the data, and **ridge** regression adds
    a small penalty that keeps the weights from getting too large.

## Why it matters

Ridge regression is the next rung after Naive Bayes. It is still built from sums, but its answer needs a **matrix
inverse**, which mixes every training point with every other. Even so, a classic trick lets us remove a point
**exactly**, without starting again. It also gives us **leverage**, a clean measure of how much one point bends the model.

## A simple example

Plot people's heights against their shoe sizes. The points roughly follow a line. Linear regression finds the line that
is closest to all the points at once. With that line, you can guess someone's shoe size from their height.

## How it works

<ol class="steps" markdown>
<li markdown>**Build two summary tables** by adding up over all training points: \(A = X^\top X + \lambda I\) and \(b = X^\top y\).</li>
<li markdown>**Solve one formula** for the weights: \(w = A^{-1} b\).</li>
<li markdown>**Predict** by multiplying a new input by the weights.</li>
</ol>

The \(\lambda I\) part is the **ridge penalty**. It keeps the weights small and makes the formula stable.

For digit classification, the course fits ridge to "one-hot" targets (a 1 for the right digit and 0 for the others) and
picks the digit with the highest output.

### Leverage: how hard one point pulls

Each training point \(x\) has a **leverage** \(h = x^\top A^{-1} x\). A point with high leverage pulls the line towards
itself. In Lesson 02, Carol's digits had a mean leverage of **0.116**, against **0.039** for everyone else. That is about three times as much pull. Leverage is the classical cousin of [memorisation](overfitting-and-memorisation.md).

### Forgetting in ridge regression

Removing a point \((x, y)\) changes the tables to \(A - xx^\top\) and \(b - xy\). The **Sherman-Morrison** formula updates
the inverse directly, which is called a **downdate**. In Lesson 02 the downdated weights matched a model trained without
Carol to within **4.38 × 10⁻¹³**, just rounding error.

The downdate's cost depends only on what you delete. Refitting depends on everything you keep. At 300,000 rows, the
downdate was about **62 times** faster than a refit.

## In code

```python
import numpy as np
from mul import classical, lab
L = lab.make_lab("carol")
onehot = lambda y: np.eye(10)[y]
ridge = classical.RidgeUnlearner(lam=1.0).fit(L.X_train, onehot(L.y_train))
h = ridge.leverage(L.X_train)            # how hard each point pulls
ridge.unlearn(L.Xf, onehot(L.yf))        # 40 Sherman-Morrison downdates
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming "coupled" means "impossible".** The inverse mixes every point, but the model is still a formula of
      sums, so exact removal is possible.
    - **Running thousands of downdates without a refresh.** Rounding errors pile up. Production systems use more stable
      updates or refit from time to time.

## Key takeaways

- Ridge regression's weights come from one formula built from sums.
- Leverage measures how hard a point pulls the model; unusual points pull hardest.
- A Sherman-Morrison downdate removes a point exactly, at a cost that depends only on what you delete.

## Quiz

```quiz
- q: What does the ridge penalty do?
  options:
    - Keeps the weights small and the formula stable
    - Deletes outliers
    - Makes the model a neural network
  answer: 0
  why: The extra λI term discourages large weights and keeps the matrix safely invertible.
- q: What does high leverage mean for a training point?
  options:
    - It pulls the fitted model strongly towards itself.
    - It has no effect on the model.
    - It is in the test set.
  answer: 0
  why: Leverage measures how much one point bends the fit. Carol's digits had about three times the average.
- q: How does ridge regression forget a point exactly?
  options:
    - A Sherman-Morrison downdate of the inverse
    - Gradient ascent
    - Deleting the largest weight
  answer: 0
  why: The downdate updates the inverse for the removed point, giving the same weights as a refit, up to rounding.
- q: Why does the downdate get relatively faster as the dataset grows?
  options:
    - Its cost depends only on the deleted points, while a refit depends on all the data you keep.
    - It skips half the data.
    - It uses a GPU.
  answer: 0
  why: At 300,000 rows, deleting 40 points by downdate was about 62 times faster than refitting.
```

## Try it

- Concept: [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Lesson: [02 · Linear and logistic regression](../lessons/02-linear-and-logistic-regression.md).
