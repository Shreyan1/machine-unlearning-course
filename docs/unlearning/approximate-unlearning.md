---
title: Quick fixes and their traps
description: Fine-tuning, gradient ascent and NegGrad+ are cheap ways to edit a trained model, and they fail in three directions.
---

# Quick fixes and their traps

!!! oneline "In one line"
    Approximate unlearning edits an already-trained model cheaply, but with no guarantee. The simple versions fail
    by **under-forgetting**, **over-forgetting** or **breaking the model**.

## Why it matters

Most models in production were trained as one big network, long ago. [SISA](sisa.md) had to be chosen before training,
and [retraining](retraining-gold-standard.md) is expensive. When a deletion request arrives today, teams reach for a
quick fix on the model they already have. This page shows why the quick fixes are so hard to get right.

## A simple example

Imagine trying to make a student forget one wrong fact they learnt. You could:

- **Stop mentioning it** and hope it fades (fine-tuning on everything else). It mostly does not fade.
- **Drill the opposite**, over and over (gradient ascent). They forget the fact, but they also get confused about
  everything near it.
- **Drill the opposite, while revising everything else** (NegGrad+). Better, but you must stop at exactly the right
  moment.

## How it works

<!-- diagram: approximate-unlearning -->

### Where gradient ascent comes from

The Newton step from [logistic regression](../ml-basics/logistic-regression.md) moves the weights in the direction the
deleted points were pulling, scaled by the curvature (the Hessian) of what remains:

\[
w_{\text{new}} = w + H_r^{-1} \sum_{\text{deleted}} \nabla \ell_i(w)
\]

A neural network has no usable Hessian, so replace \(H_r^{-1}\) with a small step size \(\eta\):

\[
w_{\text{new}} = w + \eta \sum_{\text{deleted}} \nabla \ell_i(w)
\]

That is **gradient ascent** on the forget set. It trains the model to get *worse* on Carol. Even on logistic regression,
the best gradient-ascent step closed only **8%** of the gap that one Newton step closed (95%). The curvature is not a
detail; it is most of the answer.

### Three quick fixes

| Method | Idea | What happened in Lesson 08 |
|---|---|---|
| **Fine-tune** on \(D_r\) | Keep training without Carol; hope she fades | Carol barely moved (100% after 5 epochs) |
| **Gradient ascent** on \(D_f\) | Climb Carol's loss | Forgot Carol, then everything; with a larger step, test accuracy fell from 98% to 10% |
| **NegGrad+** | Climb Carol's loss *and* descend on \(D_r\) in every step | Passed at exactly one setting; one epoch more and it over-forgot |

### The window is tiny

Lesson 08 tried **46** settings of these methods against the full audit. **One** passed: NegGrad+ with α = 0.99, a
learning rate of 0.001, and exactly 2 epochs. It could only be found because, in the lab, the gold band is visible. In
production it is not.

<!-- diagram: forgetting-spectrum -->

### Three ways to fail

- **Under-forgetting** (fine-tune, short gradient ascent): Carol is still in there. Fails FORGET and PRIVACY.
- **Collateral damage** (long gradient ascent): the model got worse for everyone. Fails UTILITY.
- **Over-forgetting** (NegGrad+ one epoch too long): Carol is pushed *below* the band, which is as suspicious as leaving
  her above it. Fails FORGET.

### What is missing

All three lack two things. One is a **reference** for what a model that never saw Carol would say (not "as wrong as possible"),
and the other is a **stopping rule** that does not need the gold band. [SCRUB](scrub.md) and [Bad Teacher](bad-teacher.md) try to
add them.

## In code

```python
from mul import methods
ft = methods.finetune(original, L.Xr, L.yr, epochs=5)
ga = methods.gradient_ascent(original, L.Xf, L.yf, epochs=3, lr=1e-4)
ng = methods.neggrad_plus(original, L.Xr, L.yr, L.Xf, L.yf, epochs=2, alpha=0.99, lr=1e-3)
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Pushing the forget-set accuracy to 0%.** The target is the gold band, not zero.
    - **Tuning on the gold band, then claiming it works in production.** In production you cannot see the band.
    - **Reporting forget accuracy without utility.** The fastest way to forget Carol is to forget everything.

## Key takeaways

- Gradient ascent is a Newton step without the curvature. It is cheap, natural and unbounded.
- Without curvature you must guess the step size, and nothing says when to stop.
- Anchoring to the retain set (NegGrad+) limits the damage, but the safe window is tiny.
- Approximate methods must be audited, every time.

## Quiz

```quiz
- q: What is gradient ascent on the forget set?
  options:
    - Training the model to get worse on the forget data
    - Training the model to get better on the forget data
    - Deleting the forget data from the database
  answer: 0
  why: It climbs the loss on the forget set instead of descending it.
- q: Gradient ascent is a Newton step without what?
  options:
    - The curvature (the Hessian)
    - The data
    - The learning rate
  answer: 0
  why: Dropping the Hessian leaves a step size you must guess, and the direction is often wrong.
- q: How many of 46 settings passed the full audit in Lesson 08?
  options:
    - 1
    - 23
    - 46
  answer: 0
  why: Only NegGrad+ at one exact combination of settings passed, and it was found by looking at the gold band.
- q: NegGrad+ ran one epoch too long and pushed Carol to 12.5%, below the gold band. What is that?
  options:
    - Perfect forgetting
    - Over-forgetting, which fails the audit
  answer: 1
  why: A model that never saw Carol does much better than that, so being far worse is suspicious.
- q: What do NegGrad+ and the other quick fixes lack?
  options:
    - A reference for "forgotten" and a stopping rule that works without the gold band
    - A learning rate
    - A training set
  answer: 0
  why: SCRUB and Bad Teacher try to supply a reference; SCRUB+R adds a stopping rule.
```

## Try it

- Next concept: [SCRUB, teacher and student](scrub.md).
- Lesson: [08 · Baselines and traps](../lessons/08-approximate-baselines-and-traps.md).
