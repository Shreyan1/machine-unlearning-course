---
title: The notation
description: The symbols used in every lesson, D, D_f, D_r, D_test, θ_o, θ_r and θ_u, explained in plain words.
---

# The notation

!!! oneline "In one line"
    Seven symbols describe every unlearning problem. Three are for the **data**, one is for **testing** and three are for the **models**.

## Why it matters

Every lesson, paper and audit in unlearning uses these symbols. Once you know them, you can read any unlearning
result: "the method's accuracy on \(D_f\) is inside the gold band of \(\theta_r\)" will make immediate sense.

## A simple example

Think of a class of 30 students, one of whom leaves the school.

- The whole class is **D**.
- The student who leaves is **D_f**.
- The 29 who stay are **D_r**.
- Students from another school, used to check the teacher's method, are **D_test**.

## How it works

<!-- diagram: notation -->

### The data

| Symbol | Name | Meaning | In the digit lab |
|---|---|---|---|
| \(D\) | training set | everything the model trained on | 1,257 digits |
| \(D_f\) | **forget set** | the data that must be removed | Carol's 40 digits |
| \(D_r\) | **retain set** | everything else, so \(D = D_r \cup D_f\) | 1,217 digits |
| \(D_{\text{test}}\) | test set | data the model never trained on, used to measure usefulness | 540 digits |

### The models

| Symbol | Name | Meaning |
|---|---|---|
| \(\theta_o\) | **original** model | trained on all of \(D\) |
| \(\theta_r\) | **retrained** model | trained on \(D_r\) only; the **gold standard** |
| \(\theta_u\) | **unlearnt** model | what an unlearning method produces, starting from \(\theta_o\) |

The Greek letter θ ("theta") is the usual symbol for a model's weights.

### The goal in symbols

An unlearning method takes the original model, the data and the forget set, and returns a new model:

\[
U(\theta_o, D, D_f) \rightarrow \theta_u
\]

- **Exact** unlearning requires \(\theta_u\) to be distributed exactly like \(\theta_r\).
- **Approximate** unlearning only requires it to be "close", which must be measured.

### In the course library

| Symbol | Code |
|---|---|
| \(D\) | `L.X_train`, `L.y_train` |
| \(D_f\) | `L.Xf`, `L.yf` |
| \(D_r\) | `L.Xr`, `L.yr` |
| \(D_{\text{test}}\) | `L.X_test`, `L.y_test` |
| unseen look-alikes of \(D_f\) | `L.X_like_forget`, `L.y_like_forget` |

The last row is special to the course. It holds thick-marker digits written in Carol's style but never trained on. They help
separate "the model learnt thick digits" from "the model memorised Carol".

### Other words you will meet

| Term | Plain meaning |
|---|---|
| **Utility** | Is the model still useful? Usually accuracy on \(D_r\) and \(D_{\text{test}}\). |
| **Forget quality** | How close the model is to \(\theta_r\) on \(D_f\). |
| **Over-forgetting** | Being *suspiciously* bad on \(D_f\), worse than \(\theta_r\). This is itself a warning sign. |

## Common mistakes

!!! danger "Mistakes people make"
    - **Mixing up \(D_r\) and \(D_{\text{test}}\).** Both are "not the forget set", but the model trained on \(D_r\) and never saw \(D_{\text{test}}\).
    - **Treating \(\theta_r\) as one model.** For neural networks it is a spread of models; see [The gold band](gold-band.md).

## Key takeaways

- \(D = D_r \cup D_f\): the training set is the retain set plus the forget set.
- \(\theta_o\) is the original, \(\theta_r\) the gold standard, \(\theta_u\) the unlearnt model.
- The goal: make \(\theta_u\) behave like \(\theta_r\).

## Quiz

```quiz
- q: Which symbol is the gold standard model?
  options:
    - θ_o
    - θ_r
    - θ_u
  answer: 1
  why: θ_r is retrained on the retain set only. It is what every unlearning method tries to match.
- q: What is D_r?
  options:
    - The data to forget
    - The training data minus the forget set
    - The test data
  answer: 1
  why: The retain set is everything in training except the forget set.
- q: An unlearning method starts from which model?
  options:
    - θ_o, the original model
    - θ_r, the retrained model
    - A random model
  answer: 0
  why: The method starts from the original and produces θ_u. If it started from scratch, it would just be retraining.
- q: What does "over-forgetting" mean?
  options:
    - Being worse on D_f than a model that never saw it
    - Forgetting the test set
    - Running unlearning twice
  answer: 0
  why: A model that never met Carol still reads many of her digits. Being far worse than that is a warning sign.
```

## Try it

- Next concept: [The Ladder of Forgetting](ladder-of-forgetting.md).
- Lesson: [00 · Read this first](../lessons/00-read-first.md).
