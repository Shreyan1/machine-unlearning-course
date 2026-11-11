---
title: Linear and ridge regression
description: Linear regression fits the best straight line and ridge keeps its weights small, and because both come from a formula a point can be removed exactly.
---

# Linear and ridge regression

!!! oneline "In one line"
    Linear regression finds the straight line (or flat surface) that best fits the data, and **ridge** regression adds
    a small penalty that keeps the weights from getting too large.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how ridge regression builds its weights from two summary tables and one inverse,
    - read a point's leverage and say why unusual points pull hardest,
    - explain how a Sherman-Morrison downdate removes a point exactly, and when its speed pays off.

## Why it matters

Ridge regression is the next rung after Naive Bayes. It is still built from sums, but its answer needs a **matrix
inverse**, which mixes every training point with every other. Even so, a classic trick lets us remove a point
**exactly**, without starting again. It also gives us **leverage**, a clean measure of how much one point bends the model.

That mixing is the first real obstacle on the [Ladder of Forgetting](../unlearning/ladder-of-forgetting.md). In Naive
Bayes, each digit lives in its own class's sums, so removing a 3 touches nothing but the 3s. In ridge regression,
removing one digit changes every weight a little. There is no "Carol's share of the weights" to subtract. The lesson of
this page is that coupled is not the same as impossible.

Linear models are also everywhere in practice, from price forecasts to the last layer of many neural networks. Knowing
that they can forget exactly, and cheaply, is useful whenever one sits inside a larger system.

## A simple example

Plot people's heights against their shoe sizes. The points roughly follow a line. Linear regression finds the line that
is closest to all the points at once. With that line, you can guess someone's shoe size from their height.

!!! simply "Explain it simply"
    Now imagine one very tall person with tiny feet. Because the line tries to stay close to *everyone*, it tilts a
    little towards them, and every guess along the line shifts. Removing that person tilts it back. The question is how
    to undo the tilt without measuring everyone again.

Map the picture onto the course. Each person is a **training digit**, and height is its **64 pixel brightnesses**.
The shoe size is the **digit label**. The unusual person is **Carol**, whose thick-marker digits sit far from
everyone else's. How hard she tilts the line is her **leverage**, and undoing the tilt exactly is the **downdate**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Weight | A number the model multiplies one input by. The prediction adds up input times weight | One weight per pixel for each of the 10 digits, plus a bias |
| Least squares | Choosing the weights that make the squared errors on the training data as small as possible | The line closest to all the points at once |
| One-hot target | A label written as a list with a 1 for the right class and 0 for the rest | The label 3 becomes 0, 0, 0, 1, 0, 0, 0, 0, 0, 0 |
| Ridge penalty \(\lambda\) | An extra cost on large weights, which keeps them small and the formula stable | The course uses \(\lambda = 1\) |
| Matrix inverse | The table that "undoes" another table, as dividing undoes multiplying | \(A^{-1}\), the step that mixes every point with every other |
| Closed form | A formula that gives the answer directly, with no search | \(w = A^{-1} b\) |
| [Leverage](../start-here/glossary.md#l) | How hard one training point pulls a linear model towards itself | Carol's digits average 0.116, everyone else 0.039 |
| [Sherman-Morrison downdate](../start-here/glossary.md#s) | A formula that removes a point from the inverse exactly, without refitting | 40 downdates remove Carol in 0.53 ms |

## How it works

<!-- diagram: linear-and-ridge-regression -->

The figure has two halves. On the left, a straight line runs through a cloud of points, as close to all of them as it
can get. On the right, each bar is the weight of one feature. The blue bars come from plain regression, and the yellow
bars from ridge are shorter. That is the penalty at work.

<ol class="steps" markdown>
<li markdown>**Build two summary tables** by adding up over all training points. They are \(A = X^\top X + \lambda I\) and \(b = X^\top y\).</li>
<li markdown>**Solve one formula** for the weights, \(w = A^{-1} b\).</li>
<li markdown>**Predict** by multiplying a new input by the weights.</li>
</ol>

The \(\lambda I\) part is the **ridge penalty**. It keeps the weights small and makes the formula stable.

For digit classification, the course fits ridge to "one-hot" targets (a 1 for the right digit and 0 for the others) and
picks the digit with the highest output.

Here is what each step means for the lab.

### Step 1. Add up two tables

Each digit is a row \(x\) of 64 pixels, plus a 1 at the end so the model can learn a bias. Every digit adds its own
\(x x^\top\) to \(A\) and its own \(x y^\top\) to \(b\). With 65 numbers per row, \(A\) is a 65 × 65 table and \(b\)
is 65 × 10, one column per digit class. The penalty adds \(\lambda = 1\) along the diagonal of \(A\).

**For Carol this means** each of her 40 digits was added into the same two tables as everyone else's. Like Naive Bayes,
the tables are plain sums, so her part of them could be subtracted.

### Step 2. Invert and multiply

The weights are \(w = A^{-1} b\). This is where the mixing happens. Every entry of the inverse depends on every row
that went into \(A\). Change one row and the whole inverse changes, and with it every weight.

**For Carol this means** her digits moved every one of the 650 weights a little. You cannot point at "her weights",
which is exactly what makes forgetting look hard.

### Step 3. Predict

A new digit times the weights gives 10 scores, one per class. The highest score is the answer.

**For Carol this means** her pull on the weights shows up in every prediction, most of all for digits that look like
hers.

??? deep "Go deeper · why least squares gives this formula, and why ridge needs the penalty"
    Ridge chooses \(w\) to make \(\lVert Xw - y \rVert^2 + \lambda \lVert w \rVert^2\) as small as possible. The first
    part is the squared error on the training data. The second part is the penalty on large weights. Setting the slope
    of this loss to zero gives \((X^\top X + \lambda I)\, w = X^\top y\), which is \(A w = b\), so \(w = A^{-1} b\).

    Without the penalty, \(X^\top X\) may have no inverse. That happens when one feature can be made from others, or
    when a feature is the same in every row. Adding \(\lambda\) to the diagonal always makes \(A\) invertible, which is
    why the penalty "makes the formula stable".

    The loss is a perfect bowl, a quadratic, which is why it has a closed form at all. Keep that in mind for
    [Logistic regression](logistic-regression.md), whose loss is not.

### Leverage (how hard one point pulls)

Each training point \(x\) has a **leverage** \(h = x^\top A^{-1} x\). A point with high leverage pulls the line towards
itself. In Lesson 02, Carol's digits had a mean leverage of **0.116**, against **0.039** for everyone else. That is about three times as much pull. Leverage is the classical cousin of [memorisation](overfitting-and-memorisation.md).

For ridge, leverage always sits between 0 and 1. Near 0, the fit hardly notices the point, because many other points
say the same thing. Near 1, the fit depends on the point almost entirely, because nothing else is like it. Typical
digits sit in a crowd of similar digits and share the pull. Carol's thick strokes have no crowd, so her digits pull
alone.

You can see the effect on accuracy. Before unlearning, ridge read 95.0% of Carol's own digits but only 67.5% of unseen
digits in her style. That is a memorisation gap of 95.0 − 67.5 = 27.5 points.

??? checkpoint "Checkpoint 1 · Two training digits have leverage 0.12 and 0.04. Which one is probably unusual, and which one will removing change the model more?"
    **The one at 0.12, on both counts.** It is close to Carol's average of 0.116, while 0.04 is close to the typical
    0.039. A high-leverage point has few similar points to share its pull, so the fit bends towards it, and taking it
    out bends the fit back the most.

### Forgetting in ridge regression

Removing a point \((x, y)\) changes the tables to \(A - xx^\top\) and \(b - xy\). The **Sherman-Morrison** formula updates
the inverse directly, which is called a **downdate**. In Lesson 02 the downdated weights matched a model trained without
Carol to within **4.38 × 10⁻¹³**, just rounding error.

The downdate's cost depends only on what you delete. Refitting depends on everything you keep. At 300,000 rows, the
downdate was about **62 times** faster than a refit.

So the trick has two parts. The tables are sums, so removing a point from them is a subtraction, as in Naive Bayes. The
inverse is not a sum, but Sherman-Morrison tells you how the inverse changes when the table loses one row. You never
have to invert anything from scratch.

??? deep "Go deeper · the Sherman-Morrison formula"
    Removing one row \(x\) from \(A\) gives the new inverse
    \((A - x x^\top)^{-1} = A^{-1} + \dfrac{A^{-1} x \, x^\top A^{-1}}{1 - x^\top A^{-1} x}\), and \(b\) becomes
    \(b - x y^\top\).

    The bottom of the fraction is \(1 - h\), one minus the point's leverage. That is the link between the two ideas on
    this page. A high-leverage point makes the correction large, because the fit leaned on it hard.

    The cost is about \(d^2\) steps per deleted point, where \(d = 65\) is the number of features with the bias. A refit
    must add up all \(n\) rows again, about \(n d^2\) steps, and then invert, about \(d^3\). The downdate does not depend
    on \(n\) at all. Lesson 02 also shows that this downdate gives the same weights as one Newton step, to within
    1.37 × 10⁻¹³, which is the bridge to the next page.

??? checkpoint "Checkpoint 2 · On 2,000 rows, removing 40 points by downdate took 0.46 ms and a refit took 0.2 ms. Is the downdate worth it?"
    **Not at that size.** The refit was faster. The downdate is worth it because of how the two costs grow. The
    downdate stayed at about half a millisecond at every size, while the refit grew to 30.0 ms at 300,000 rows, which
    made the downdate 61.6 times faster. Its cost depends on what you delete, not on what you keep.

## A worked example

Follow Carol through Part A of Lesson 02. Every number comes from the notebook.

1. **Training.** Ridge is fitted on all 1,257 digits with \(\lambda = 1\) and one-hot targets. It reads 94.6% of the
   test digits, 95.0% of Carol's 40 digits (38 of them) and 67.5% of 80 unseen thick-marker digits (54 of them).
2. **Her pull.** Her digits have a mean leverage of 0.116, about three times the 0.039 of everyone else.
3. **The request.** Forty Sherman-Morrison downdates, one per digit, update the inverse and the table \(b\). They take
   0.53 ms. A refit on the 1,217 remaining digits takes 0.18 ms, because the lab is tiny.
4. **After.** Ridge reads 45.0% of Carol's digits (18 of 40), 48.8% of the look-alikes (39 of 80) and 93.9% of the
   test digits.
5. **The proof.** A ridge model fitted from scratch without her gives exactly the same three accuracies. The largest
   difference in any weight is 4.38 × 10⁻¹³, which is rounding error.

## What the lesson found

<div class="stats">
<div><strong>0.116</strong><span>Carol's mean leverage, against 0.039 for everyone else</span></div>
<div class="is-good"><strong>4.38 × 10⁻¹³</strong><span>largest weight difference from a refit without her</span></div>
<div class="is-good"><strong>61.6×</strong><span>faster than a refit, at 300,000 rows</span></div>
<div><strong>95.0% → 45.0%</strong><span>ridge's accuracy on Carol's digits</span></div>
</div>

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 95.0% | 45.0% | 45.0% |
| Unseen thick digits | 67.5% | 48.8% | 48.8% |
| Test digits | 94.6% | 93.9% | 93.9% |

**The last two columns match on every row**, and the weights match to rounding error. The downdate is exact.

**Carol's digits fell by 50 points**, much more than in Naive Bayes. Part of that is the memory of her own digits
leaving. Part is the style she taught, since the look-alikes fell too, by 18.7 points.

**The test digits lost 0.7 points.** That is about 4 of the 540 test digits, small enough to be noise, so the lesson reads nothing into it.

The timing test grew the training set with made-up rows of 64 features and removed the same 40 rows each time.

| Rows kept | Refit | Downdate | Downdate is faster by |
|---|---|---|---|
| 2,000 | 0.2 ms | 0.46 ms | 0.4× (slower) |
| 20,000 | 1.5 ms | 0.46 ms | 3.3× |
| 100,000 | 11.3 ms | 0.50 ms | 22.7× |
| 300,000 | 30.0 ms | 0.49 ms | 61.6× |

Read down the columns. The refit grows with the data, and the downdate stays flat.

## Limits

**It is numerically fragile near a leverage of 1.** The formula divides by \(1 - h\). For a point the fit depends on
almost entirely, that is a tiny number, and dividing by it magnifies rounding error. With \(\lambda > 0\), \(h\) always
stays below 1, which is one more reason the penalty helps.

**Errors build up.** Each downdate adds a little rounding error. Over thousands of deletions it adds up, so production
systems use a more stable update called a Cholesky downdate, or refit from time to time.

**It needs a closed form.** The trick works because ridge's weights come from one formula of sums. Models without such a
formula, starting with [logistic regression](logistic-regression.md), can only be forgotten approximately.

??? deep "Go deeper · two more limits"
    **The inverse must fit in memory.** The table \(A^{-1}\) has \(d \times d\) entries. For the lab that is
    65 × 65 = 4,225 numbers. For a model with a million features it would be a million million.

    **The pipeline still counts.** As in [Naive Bayes](naive-bayes.md), any scaler or feature step fitted before the
    model also holds the deleted rows and must be unlearnt too.

??? checkpoint "Checkpoint 3 · You must delete a training point whose leverage is 0.999. Why should you be careful with Sherman-Morrison?"
    **The formula divides by 1 − 0.999 = 0.001.** Any small rounding error in the inverse is multiplied by about a
    thousand. The answer can still be right, but you should check it against a refit, or use a more stable Cholesky
    downdate. Such a point is also one the model leaned on almost entirely, so removing it changes the fit a lot.

!!! tip "What to do in practice"
    - Keep the inverse \(A^{-1}\) and the table \(b\) after training, so deletions do not need the full data.
    - Use the downdate when the data you keep is large and the data you delete is small.
    - Check leverage before you delete. Points near 1 need a stable update or a refit.
    - Refit from scratch on a schedule to clear rounding error, and compare the weights.
    - Unlearn the preprocessing as well as the model.

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

??? deep "Go deeper · prove the downdate against a refit"
    ```python
    scratch = classical.RidgeUnlearner(lam=1.0).fit(L.Xr, onehot(L.yr))   # never saw Carol
    print(np.abs(ridge.w - scratch.w).max())                            # about 4e-13, rounding error
    print(h[L.forget_idx].mean(), h[L.retain_idx].mean())               # 0.116 and 0.039
    ```

    The library keeps \(A^{-1}\) and \(b\) after `fit`. The weights are worked out as \(A^{-1} b\) whenever they are
    needed, so a downdate only has to change those two tables.

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming "coupled" means "impossible".** The inverse mixes every point, but the model is still a formula of
      sums, so exact removal is possible.
    - **Running thousands of downdates without a refresh.** Rounding errors pile up. Production systems use more stable
      updates or refit from time to time.
    - **Expecting the downdate to win on small data.** On 2,000 rows the refit was faster. The gain comes with size.
    - **Throwing away the inverse after training.** Without \(A^{-1}\) and \(b\), there is nothing to downdate.
    - **Ignoring leverage.** The points that pull hardest are the ones whose removal changes the model most, and the
      ones the formula handles least stably.

## Key takeaways

!!! notes "Notes to take"
    - **Ridge.** Weights come from one formula, \(w = (X^\top X + \lambda I)^{-1} X^\top y\).
    - **Penalty.** \(\lambda\) keeps weights small and the table invertible. The course uses \(\lambda = 1\).
    - **Coupled.** The inverse mixes every point with every other, so one point moves every weight.
    - **Leverage.** \(h = x^\top A^{-1} x\), between 0 and 1. Carol 0.116, everyone else 0.039.
    - **Downdate.** Sherman-Morrison removes a point exactly. Weights matched a refit to 4.38 × 10⁻¹³.
    - **Cost.** Grows with what you delete. Slower than a refit at 2,000 rows, 61.6 times faster at 300,000.
    - **Effect on Carol.** 95.0% before, 45.0% after, the same as a model that never saw her.
    - **Trap.** Dividing by \(1 - h\) is fragile for points with leverage near 1.
    - **Trap.** Rounding error builds up over many downdates, so refit now and then.

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
- q: Why can you not simply subtract "Carol's part" of the ridge weights?
  options:
    - The weights are stored in a secret format.
    - The inverse mixes every point with every other, so no single part of the weights belongs to her.
    - Carol's digits were never used in training.
  answer: 1
  why: The tables A and b are sums you can subtract from, but the weights come from an inverse, which couples everyone.
- q: On the lab's 1,217 remaining digits, the refit took 0.18 ms and 40 downdates took 0.53 ms. What does that show?
  options:
    - The downdate is broken.
    - On small data a refit can be faster; the downdate wins as the data grows.
    - Refitting is always the better choice.
  answer: 1
  why: The downdate's cost stays flat while the refit's grows, so the downdate pays off on large data.
- q: Why is the Sherman-Morrison formula fragile for a point with leverage close to 1?
  options:
    - Such points are always in the test set.
    - The formula then needs more memory.
    - It divides by one minus the leverage, a tiny number that magnifies rounding error.
  answer: 2
  why: A point the fit depends on almost entirely gives a near-zero denominator, so a stable update or a refit is safer.
- q: Ridge read 95.0% of Carol's digits but only 67.5% of unseen digits in her style. What does that gap show?
  options:
    - Ridge memorised her, with a gap of 27.5 points.
    - Ridge never saw her digits.
    - The look-alike digits were mislabelled.
  answer: 0
  why: Doing much better on her own digits than on similar unseen ones is the sign of memorisation, and her high leverage explains it.
```

## Try it

!!! levelup "Level up"
    You can now remove a point exactly from a model whose answer needs an inverse, and say when that pays off. Next
    quest, [Logistic regression](logistic-regression.md), where there is no formula at all and forgetting becomes
    approximate.

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [02 · Linear and logistic regression](../lessons/02-linear-and-logistic-regression.md).
- In the notebook, find the 10 training points with the highest leverage that are not Carol's, plot them and see what
  they have in common.
