---
title: Certified unlearning
description: A mathematical promise that an unlearnt model is almost indistinguishable from a retrained one, and how it connects to differential privacy.
---

# Certified unlearning

!!! oneline "In one line"
    **Certified unlearning** proves that the unlearnt model is *statistically almost indistinguishable* from a model
    retrained without the data, with "almost" measured by two small numbers, \(\varepsilon\) and \(\delta\).

## Why it matters

[Exact unlearning](exact-unlearning-classical.md) is always right but often expensive. [Approximate
unlearning](approximate-unlearning.md) is cheap but comes with no guarantee, so every result has to be
[audited](unlearning-audit.md). Certified unlearning sits in between. It is cheaper than retraining, and it still comes
with a proof. That proof is the closest thing the field has to a guarantee an auditor can check on paper.

The catch is that today's proofs mostly hold for **convex** models, such as logistic regression and linear models.
For deep networks they do not carry over.

## A simple example

Two sealed boxes each hold a trained model. One came from retraining without Carol. The other came from unlearning
her. A referee opens both and runs any test they like. With certified unlearning, the referee can do *only slightly
better than guessing* at which box is which. \(\varepsilon\) says how slightly, and \(\delta\) is a tiny chance that
the promise fails.

## How it works

### The promise in symbols

Let \(A\) be the training algorithm and \(U\) the unlearning method. Training is random (starting weights, batch order,
added noise), so both give a *distribution* of models. Unlearning is \((\varepsilon, \delta)\)-certified if, for every
set of possible models \(S\),

\[
P\big[U(A(D), D, D_f) \in S\big] \le e^{\varepsilon}\, P\big[A(D_r) \in S\big] + \delta ,
\]

and the same holds with the two sides swapped. Small \(\varepsilon\) and \(\delta\) mean the two distributions are close.

### Three recipes

| Recipe | Idea | Works for | Source |
|---|---|---|---|
| **Certified removal** | Train with a small random term added to the loss. To delete, take one Newton step that removes the point's influence. The noise hides the small error left over. | Convex models such as logistic regression | Guo et al. 2019 |
| **Descent-to-delete** | After a deletion, take a few gradient steps from the current model, then add Gaussian noise before releasing it. | Convex models, many deletions in a row | Neel et al. 2021 |
| **Deletion capacity** | Count how many deletions a method can absorb before accuracy drops, then retrain. | Convex models | Sekhari et al. 2021 |

Each recipe has a **budget**. Every deletion uses some of it, and once the leftover error would break the promise,
you must retrain. So certified unlearning postpones retraining; it does not abolish it.

### The link to differential privacy

[Differential privacy](https://en.wikipedia.org/wiki/Differential_privacy) (DP) uses the same \((\varepsilon, \delta)\)
promise, but for training. A DP-trained model behaves almost the same whether or not any one record was in the data.
That means **doing nothing** already counts as certified unlearning of one record. For a group of \(k\) records the
guarantee weakens, roughly to \(k\varepsilon\).

The price is accuracy. The noise that makes a model private also makes it less accurate, especially for rare examples,
which are exactly the ones a model tends to [memorise](../ml-basics/overfitting-and-memorisation.md).

## Common mistakes

!!! danger "Mistakes people make"
    - **Using a convex proof on a deep network.** The guarantees assume one best answer. Neural networks have many, so
      the proof no longer holds.
    - **Forgetting the budget.** After enough deletions the leftover error adds up; the method must retrain to keep its
      promise.
    - **Reading \(\varepsilon\) as "percent forgotten".** It bounds how distinguishable two distributions are. A large
      \(\varepsilon\), such as 10, promises very little.
    - **Skipping the noise.** The Newton step alone is not certified. The randomness is what hides the error.

## Key takeaways

- Certified unlearning makes the unlearnt model provably close, in distribution, to a retrained one.
- The closeness is measured by \(\varepsilon\) and \(\delta\), as in differential privacy.
- Today's proofs cover convex models; deep networks are still an open problem.
- A DP-trained model is already certified for deleting a single record, at a cost in accuracy.

## Quiz

```quiz
- q: What does certified unlearning promise?
  options:
    - The unlearnt model is identical to the retrained model.
    - The unlearnt model is statistically almost indistinguishable from a retrained one.
    - The forget set accuracy drops to 0%.
  answer: 1
  why: Identical is exact unlearning. Certified unlearning allows a small, bounded difference, measured by epsilon and delta.
- q: For which models do today's certified unlearning proofs mostly hold?
  options:
    - Convex models such as logistic regression
    - Large language models
    - Any neural network
  answer: 0
  why: The proofs rely on a single best answer, which convex models have and deep networks do not.
- q: Why does certified removal add random noise?
  options:
    - To speed up training
    - To hide the small error left after the Newton step
    - To make the model more accurate
  answer: 1
  why: The deletion step is only approximately right. The noise makes the leftover difference statistically invisible.
- q: A model was trained with differential privacy. What happens when one person asks to be forgotten?
  options:
    - It must always be retrained from scratch.
    - Doing nothing already meets a certified guarantee for that one record.
    - Differential privacy has nothing to do with unlearning.
  answer: 1
  why: DP already bounds how much any single record can change the model, which is the same promise.
```

## Try it

- Read [exact unlearning for classical models](exact-unlearning-classical.md), where the Newton step first appears.
- Run [Lesson 02](../lessons/02-linear-and-logistic-regression.md) and compare its one-step update with retraining.
