---
title: Logistic regression
description: Logistic regression outputs probabilities and has no closed-form answer, so unlearning it becomes an approximate Newton step that must be measured.
---

# Logistic regression

!!! oneline "In one line"
    Logistic regression is a straight-line model that outputs **probabilities** for each class, and its weights are
    found by walking downhill on the loss, not from a formula.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why logistic regression has no formula to subtract from,
    - describe how one Newton step estimates the model you would get without a person,
    - measure how close that estimate is, and say why the trick fails for big networks.

## Why it matters

Logistic regression is where unlearning first becomes **approximate**. There is no formula for its weights, only the
rule "the slope of the loss is zero here". So we cannot subtract a point exactly. Instead we *estimate* where the
answer moves, and then we must **measure** how close the estimate is. That habit of measuring runs through the rest of
the course.

It is also a common choice for yes-or-no scores, like the loan example below, so many real erasure requests land on
a model like this one. And the Newton step you meet here is the core of two big ideas later in
the course, [influence functions](../unlearning/influence-functions.md) and
[certified unlearning](../unlearning/certified-unlearning.md).

## A simple example

A bank wants to predict whether a loan will be repaid. Logistic regression combines facts like income and existing
debt into a score, then squeezes the score into a probability between 0 and 1. For example, it might estimate a 72% chance of repayment.

!!! simply "Explain it simply"
    Picture a ball resting at the bottom of a smooth bowl. Every training example is a small hand pushing on the ball,
    and the ball sits where all the pushes balance. Take one hand away and the ball starts to roll. You do not know
    exactly where it will stop, but from the slope and the curve of the bowl under it, you can make a very good guess
    in one jump.

Map the picture onto the course. The ball's position is the **weights**. The bowl is the **loss**, and each hand is
one **training digit**. The hand taken away is **Carol's** 40 digits. The guess in one jump is the **Newton step**,
and how far the guess lands from where the ball would really stop is what we must **measure**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Sigmoid | A function that squeezes any score into a probability between 0 and 1 | Used for two classes, such as repaid or not |
| [Softmax](../start-here/glossary.md#s) | The same idea for many classes, turning scores into probabilities that add up to 1 | Ten probabilities, one per digit |
| [Cross-entropy](../start-here/glossary.md#c) | The loss for classification. Small when the right class gets a high probability | What training makes as small as possible |
| [Gradient](../start-here/glossary.md#g) | The slope of the loss, one number per weight | 5.9 × 10⁻¹⁴ after training, almost exactly flat |
| Convex | Shaped like a single bowl, so there is exactly one lowest point | Why "the" best model without Carol exists |
| [Hessian](../start-here/glossary.md#h) | A table of the loss's curvature, with one row and one column per weight | 650 × 650 for the lab's model |
| [Newton step](../start-here/glossary.md#n) | A jump to the estimated new best weights, using the gradient and the Hessian | One step took 6.0 ms |
| Residual gradient | The slope left on the retain set after unlearning. Zero means the true answer was reached | 12.5 before the step, 1.21 after one step |

## How it works

<!-- diagram: logistic-regression -->

The figure shows the S-shaped sigmoid curve. Along the bottom is the score, a weighted sum of the features. Up the
side is the probability of "yes". Low scores get a probability near 0 and high scores near 1. The dashed line at 0.5
is where the answer flips.

<ol class="steps" markdown>
<li markdown>**Score.** Multiply the input by the weights, as in linear regression.</li>
<li markdown>**Squeeze.** Turn the score into a probability with the sigmoid (two classes) or softmax (many classes) function.</li>
<li markdown>**Train.** Adjust the weights to lower the [cross-entropy loss](loss-functions.md). The best weights sit at the
bottom of a smooth, bowl-shaped valley, where the slope is zero.</li>
</ol>

Because the valley is bowl-shaped (the technical word is **convex**), there is exactly **one** best answer.

For the lab, the model has 10 scores, one per digit, each a weighted sum of the 64 pixels plus a bias. That makes
65 × 10 = 650 weights. Softmax turns the 10 scores into 10 probabilities, and the course adds a small penalty on large
weights, as in [ridge](linear-and-ridge-regression.md), with \(\lambda = 1\).

**Training has no formula, only a search.** The course trains with Newton's method. At each step it reads the slope
and the curvature where it stands and jumps to where a bowl of that shape would be lowest. Because the real loss is
not a perfect bowl, the jump lands near the bottom, not on it, so it repeats. In Lesson 02, training took 7 such
jumps. At the end the slope was 5.9 × 10⁻¹⁴, which is flat to the limit of the computer's precision.

**For Carol this means** her 40 digits are among the hands holding the ball in place. The final weights balance her
pushes against everyone else's, and nothing in them is labelled as hers.

??? checkpoint "Checkpoint 1 · After training, the slope on all 1,257 digits is 5.9 × 10⁻¹⁴. At the same weights, the slope on the 1,217 digits without Carol is 12.5. Why the difference?"
    **Her push was removed.** At the best weights, everyone's pushes cancel out, so the total slope is zero. Take
    Carol's digits out and the rest no longer cancel. The slope that is left is exactly her push, pointing the other
    way. That leftover slope tells the Newton step which way to jump, and its size shows how far the weights must move.

### Forgetting with a Newton step

When Carol is removed, the bottom of the valley moves a little. We do not know exactly where, but we know the **slope**
(gradient) and the **curvature** (Hessian) where we stand. From those, one jump called a **Newton step** estimates the
new bottom.

The step is not a new training run. It starts from the trained weights, which are already very close to the answer,
and it uses only the retain set. A full refit starts from zero and needs all 7 jumps. Unlearning needs one, because it
starts next to the new bottom.

Lesson 02 measures how quickly repeated Newton steps close the gap to retraining.

| Newton steps | Share of the gap to the retrained model closed |
|---|---|
| 1 | 94.8% |
| 2 | 99.9% |
| 3 | 100.0% |

One step took 6.0 ms, against 40.7 ms for a full refit. So "approximate" is not a dirty word; it is a **measurable
distance**, and here a tiny one.

The gap here is the distance between the unlearnt weights and the weights of a model retrained without Carol. Before
any step it was 3.148. One step brought it to 0.165, two steps to 0.0035 and three steps to less than 0.00001. Near the bottom,
Newton's method shrinks the error faster with every step, which is why it closes in so fast.

??? deep "Go deeper · the Newton step in symbols, and the residual gradient"
    Write \(L(w)\) for the loss on all the data and \(L_r(w)\) for the loss on the retain set. At the trained weights
    \(w\), \(\nabla L(w) = 0\). Because \(L\) is \(L_r\) plus Carol's part, the retain slope is
    \(\nabla L_r(w) = -\sum_{i \in D_f} \nabla \ell_i(w)\), minus the sum of her digits' slopes.

    The Newton step is \(w_u = w - H_r^{-1} \nabla L_r(w)\), where \(H_r\) is the Hessian of the retain loss at \(w\).
    It finds the lowest point of the bowl that best matches the loss around \(w\). Koh and Liang (2017) call this
    estimate an **influence function**.

    The **residual gradient** \(\lVert \nabla L_r(w_u) \rVert\) is how much slope is left after the step. Lesson 02
    printed it after each step.

    | Steps | Distance to retrained weights | Residual gradient |
    |---|---|---|
    | 0 | 3.14814 | 12.5 |
    | 1 | 0.16506 | 1.21 |
    | 2 | 0.00351 | 0.0313 |
    | 3 | 0.00000 | 0.0000239 |

    Guo et al. (2019) bound this residual and add a little random noise to the loss at training time, so the small
    error that is left cannot be told apart from noise. That turns "very close" into a formal guarantee, called
    certified removal.

!!! note "The link to ridge"
    The Sherman-Morrison downdate for ridge *is* a Newton step. It is exact because ridge's loss is a perfect bowl.
    Logistic regression's loss is only roughly a bowl near the bottom, so the same step lands *near* the answer, not
    *on* it. That is the whole difference between exact and approximate unlearning.

In Lesson 02, one Newton step on ridge gave the same weights as the Sherman-Morrison downdate, to within
1.37 × 10⁻¹³.

??? checkpoint "Checkpoint 2 · After one Newton step, the model reads 60.0% of Carol's digits. A model retrained without her reads 62.5%. Is one step good enough?"
    **Close but not exact, and you can tell.** The two are one digit apart out of 40, since each digit is 2.5
    points. Logistic regression has no randomness, so the retrained model is one exact target, and one step misses it
    slightly. The residual gradient of 1.21 says the same. A second step closes 99.9% of the gap. Whether one step is
    enough is a choice you make by measuring, not by hoping.

### Why it stops working for big models

A Newton step needs a Hessian, a table with one row and one column per weight. For the course's small neural network
(85,002 weights), that is about 29 GB. And neural networks do not have a single bowl-shaped valley at all. See
[Neural networks](neural-networks.md).

So the Newton step needs three things. It needs a **gradient**, which every trained model has. It needs a **Hessian
you can store and invert**, which the lab's 650 weights allow but large models do not. And it needs a **convex loss**,
so that "the best model without Carol" is one clear place. Take away either of the last two and the estimate degrades
fast. Basu et al. (2021) found influence estimates [fragile](https://arxiv.org/abs/2006.14651) in deep networks.

## A worked example

Follow Carol through Part B of Lesson 02. Every number comes from the notebook.

1. **Training.** Logistic regression is trained on all 1,257 digits by Newton's method. It needs 7 jumps, and the
   final slope is 5.9 × 10⁻¹⁴.
2. **The memory.** It reads 92.5% of Carol's digits (37 of 40) but 77.5% of unseen digits in her style. That is a
   memorisation gap of 15 points.
3. **The target.** A model retrained without her reads 62.5% of her digits (25 of 40), 57.5% of the look-alikes and
   97.0% of the test digits.
4. **The step.** One Newton step on the 1,217 retain digits, starting from the trained weights. It takes 6.0 ms, against
   40.7 ms for the refit.
5. **After.** The model reads 60.0% of Carol's digits (24 of 40). It matches the retrained model on the look-alikes and
   the test digits.
6. **The measurement.** The weights moved from 3.148 away from the retrained ones to 0.165 away, closing 94.8% of the
   gap. A second step would close 99.9%.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>92.5%</strong><span>the original model on Carol's digits</span></div>
<div class="is-good"><strong>60.0%</strong><span>after one Newton step, against 62.5% for a retrain</span></div>
<div class="is-good"><strong>94.8%</strong><span>of the gap to the retrained weights closed in one step</span></div>
<div><strong>6.0 ms</strong><span>for one step, against 40.7 ms for a full refit</span></div>
</div>

| | Before | After one step | Never saw Carol |
|---|---|---|---|
| Carol's digits | 92.5% | 60.0% | 62.5% |
| Unseen thick digits | 77.5% | 57.5% | 57.5% |
| Test digits | 97.2% | 97.0% | 97.0% |

**Carol's row** is the one to read first. The step took her from 92.5% to within one digit of the retrained model.
Logistic regression had memorised her much more than Naive Bayes did, so there was a lot to undo.

**The other two rows** already match the retrained model after one step. The small error that is left shows up only on
the data that was removed, which is where you should always look.

## Limits

**It is an estimate.** One step lands near the retrained model, not on it. Unless you measure, you do not know how near.
The lab can measure because it can afford a retrain to compare with. A large system usually cannot.

**It needs a single bowl.** The step aims at "the" lowest point. With many valleys, as in neural networks, there is no
single point to aim at, and the step can land somewhere that matches no retrained model.

**It needs the Hessian.** For the lab, 650 × 650 is easy. For the course's 85,002-weight network it is about 29 GB, and
for a model with a billion weights it would be about \(10^{18}\) entries.

!!! tip "What to do in practice"
    - Use a Newton step for models with a convex loss and few enough weights to hold the Hessian.
    - Measure the result. Report the residual gradient and, where you can, the distance to a retrained model.
    - Check accuracy on the forget set against a retrained model, since that is where a leftover error shows.
    - Take a second step if the first one leaves too much. Near the bottom each step shrinks the error faster.
    - If you need a formal guarantee, add noise at training time as in certified removal.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
logreg = classical.SoftmaxNewton(lam=1.0).fit(L.X_train, L.y_train)
unlearned = logreg.unlearn_newton(L.Xr, L.yr, steps=1)    # one Newton step on the retain set
```

??? deep "Go deeper · measure the step against a retrain"
    ```python
    import numpy as np
    scratch = classical.SoftmaxNewton(lam=1.0).fit(L.Xr, L.yr)       # never saw Carol
    gap0 = np.linalg.norm(logreg.w - scratch.w)                      # 3.148 before any step
    gap1 = np.linalg.norm(unlearned.w - scratch.w)                   # 0.165 after one step
    print(1 - gap1 / gap0)                                           # 0.948, the share of the gap closed
    print(unlearned.grad_norm(L.Xr, L.yr))                           # 1.21, the residual gradient
    ```

    The method `unlearn_newton` works out the slope and the Hessian of the retain loss at the current weights, solves
    for the step and returns a new model. With `steps=2` it repeats the step from the new weights.

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting an approximate method without measuring it.** Always compare against a model that never saw the data.
    - **Assuming the Newton step scales.** It needs a Hessian you can store and invert, and a single best answer.
    - **Looking only at test accuracy.** After one step the test digits already matched. The leftover error showed only
      on Carol's digits.
    - **Starting the step from somewhere else.** The step is accurate because it starts at the trained optimum, right
      next to the new one.
    - **Calling one step "certified".** A guarantee needs a bound on the residual and noise added at training time.

??? checkpoint "Checkpoint 3 · A team takes one Newton step on its logistic model and reports the customer as unlearnt. What do you ask for?"
    **The measurement.** Ask for the residual gradient on the retain set, the model's accuracy on the customer's data
    next to a retrained model's and, if they claim a guarantee, the noise added at training time and the bound they
    used. A Newton step is an estimate. Without those numbers, "unlearnt" is only a hope.

## Key takeaways

!!! notes "Notes to take"
    - **Logistic regression.** A weighted score squeezed into probabilities by sigmoid or softmax.
    - **No formula.** The weights are wherever the slope of the loss is zero, found by search.
    - **Convex.** One bowl, one best answer, so "the model without Carol" is a clear target.
    - **Newton step.** Jump using the slope and the Hessian. 6.0 ms against 40.7 ms for a refit.
    - **Result.** One step closed 94.8% of the gap, two closed 99.9%. Carol went from 92.5% to 60.0%, against 62.5%.
    - **Link to ridge.** The Sherman-Morrison downdate is a Newton step on a perfect bowl, so it is exact.
    - **Measure.** "Proof" now means the distance to the gold standard and the residual gradient.
    - **Trap.** The Hessian of an 85,002-weight network is about 29 GB, and networks have many valleys.
    - **Trap.** A leftover error shows on the forget set, not on test accuracy.

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
- q: Right after training, the slope on the retain set is not zero, even though the slope on all the data is. Why?
  options:
    - Training stopped too early.
    - The slope that is left is Carol's push, which no longer cancels against the others.
    - The retain set has different labels.
  answer: 1
  why: At the optimum all pushes balance. Removing her digits leaves the rest unbalanced, and that leftover tells the Newton step where to go.
- q: Why does one Newton step for unlearning cost far less than retraining, which needs 7 steps?
  options:
    - It uses fewer pixels.
    - It skips the Hessian.
    - It starts from the trained weights, which are already next to the new answer.
  answer: 2
  why: A refit starts from zero. Unlearning starts right beside the new bottom of the bowl, so one jump gets most of the way.
- q: After one step, test accuracy matched the retrained model, but accuracy on Carol's digits was 60.0% against 62.5%. What is the lesson?
  options:
    - Look at the forget set, because that is where a leftover error shows.
    - Test accuracy is enough to prove forgetting.
    - The retrained model is wrong.
  answer: 0
  why: The removed data is where unlearnt and retrained models differ most, so it is the first place to check.
- q: Why is the Sherman-Morrison downdate for ridge exact, while the Newton step for logistic regression is not?
  options:
    - Ridge has fewer weights.
    - Ridge's loss is a perfect bowl, so a step based on the bowl's shape lands exactly on the bottom.
    - Logistic regression has no Hessian.
  answer: 1
  why: The downdate is a Newton step. On an exactly quadratic loss the step is exact; on a roughly quadratic one it lands near.
```

## Try it

!!! levelup "Level up"
    You can now unlearn a model that has no formula, and measure how close the result is to retraining. Next quest,
    [Support vector machines](support-vector-machines.md), where there is no gradient to step along, and a different
    property makes forgetting cheap.

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [02 · Linear and logistic regression](../lessons/02-linear-and-logistic-regression.md).
- In the notebook, re-run Part B with `lam=0.1` and see whether one Newton step still closes as much of the gap.
- See how the Newton step becomes a guarantee in [Certified unlearning](../unlearning/certified-unlearning.md).
