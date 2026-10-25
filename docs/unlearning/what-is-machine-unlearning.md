---
title: What is machine unlearning?
description: Machine unlearning removes the influence of specific data from a trained model, and checks that it is gone.
---

# What is machine unlearning?

!!! oneline "In one line"
    Machine unlearning means removing the influence of some data from a model that has **already been trained**, so
    that it behaves as if it had never seen that data.

## Why it matters

Models are trained on data about people, and people can ask for their data to be erased. Data can also turn out to be
illegal, poisoned by an attacker or used without a licence. Training a big model again from scratch can cost millions,
so "just retrain it" is often not an option. Machine unlearning asks a cheaper question. Can we remove the influence of just that data, and then **show, with evidence, that it is gone**?

## A simple example

A teacher marks a class test and works out the class average. Later, one student's paper turns out to be copied and must
be removed. The teacher does not need to re-mark every paper. They take that student's mark out of the total, divide
by one fewer student, and the average is fixed.

That is unlearning at its easiest. For many models it is that simple. For neural networks, it is much harder, because
one person's influence is spread across everything.

## How it works

Every unlearning problem has the same pieces:

| Piece | Symbol | Example |
|---|---|---|
| The training data | \(D\) | 1,257 handwritten digits |
| The data to forget | \(D_f\) (the **forget set**) | Carol's 40 digits |
| Everything else | \(D_r\) (the **retain set**) | the other 1,217 digits |
| The original model | \(\theta_o\) | trained on \(D\) |
| The ideal answer | \(\theta_r\) | retrained on \(D_r\) only, the **gold standard** |
| The unlearnt model | \(\theta_u\) | what an unlearning method produces from \(\theta_o\) |

The goal is simple to state: **make \(\theta_u\) behave like \(\theta_r\).**

<!-- diagram: what-is-machine-unlearning -->

### Two families of methods

- **Exact unlearning** gives a result that is *guaranteed* to match retraining. Examples include subtracting counts in Naive Bayes, deleting a row in k-NN and retraining one shard in [SISA](sisa.md).
- **Approximate unlearning** is cheaper but gives no guarantee, so its result must be **audited**. Examples include [gradient ascent](approximate-unlearning.md), [SCRUB](scrub.md) and [Bad Teacher](bad-teacher.md).

<!-- diagram: unlearning-families -->

### The five steps in every lesson

1. **Train** a model on data that includes something it should not keep.
2. **Show the issue**: measure how the model still carries that data.
3. **Untrain** it with an unlearning method.
4. **Show the result**: measure again, side by side with *before*.
5. **Prove it**: compare with models that *never* saw the data.

## In code

The whole loop, using the course library:

```python
from mul import lab, train, methods
L = lab.make_lab("carol")
theta_o = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)    # original
theta_r, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)  # gold standard
# any unlearning method should give a model that behaves like theta_r
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Aiming for zero.** The target is a model that never saw the data, not one that is blind to it.
    - **Trusting a method because it is clever.** Approximate methods must be measured against the gold standard.
    - **Treating unlearning as a legal shield.** No regulator has said that any method counts as deletion. Unlearning
      gives you evidence; it does not settle the legal question.

## Key takeaways

- Unlearning removes data's influence from an already-trained model.
- The ideal result is the model retrained without the data.
- Exact methods guarantee that result; approximate methods must be checked.

## Quiz

```quiz
- q: What is the "gold standard" in machine unlearning?
  options:
    - A model with 100% accuracy
    - A model retrained from scratch without the forget set
    - The original model
  answer: 1
  why: The ideal answer is always the model you would have had if the data had never been there.
- q: What is the forget set?
  options:
    - The data that must be removed
    - The test data
    - Everything except the deleted data
  answer: 0
  why: "`D_f` is the forget set. Everything else in training is the retain set `D_r`."
- q: What is the main difference between exact and approximate unlearning?
  options:
    - Exact is guaranteed to match retraining; approximate must be checked.
    - Exact is always cheaper.
    - Approximate only works on classical models.
  answer: 0
  why: Approximate methods trade the guarantee for speed, so their results need an audit.
- q: Does a successful unlearning method make the model a legal safe harbour?
  options:
    - Yes, always
    - No; no regulator has yet said any method counts as deletion
  answer: 1
  why: Unlearning gives evidence about what the model does. The legal question depends on the case.
```

## Try it

- Next concept: [Deleting is not forgetting](deleting-vs-unlearning.md).
- Lesson: [00 · Read this first](../lessons/00-read-first.md).
