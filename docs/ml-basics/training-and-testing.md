---
title: Training data and test data
description: Why we split data into a training set and a test set, and how the course splits it further for unlearning.
---

# Training data and test data

!!! oneline "In one line"
    We train a model on one part of the data and check it on a different part that it has **never seen**.

## Why it matters

A model can look perfect on the examples it trained on, simply because it remembers them. The only fair check is data
it has never seen. In unlearning, this idea goes one step further. We compare how the model treats data it trained on with how it treats similar data it never saw. A big difference is a sign that it remembers.

## A simple example

Imagine a teacher who gives students the exact exam questions to practise. Every student scores 100%. Did they learn the
subject, or just memorise the answers? To find out, the teacher must use **new** questions on exam day.

- The practice questions are the **training set**.
- The new exam questions are the **test set**.

## How it works

<!-- diagram: training-and-testing -->

<ol class="steps" markdown>
<li markdown>**Shuffle the data** so both parts look alike.</li>
<li markdown>**Split it**, for example 70% for training and 30% for testing.</li>
<li markdown>**Train only on the training set.** The model must never see the test set during training.</li>
<li markdown>**Measure accuracy on the test set.** This tells you how well the model works on new data.</li>
</ol>

### The extra splits used in unlearning

In this course, the training set itself is split again:

| Name | Symbol | What it is | In the digit lab |
|---|---|---|---|
| Training set | \(D\) | everything the model trained on | 1,257 digits |
| Forget set | \(D_f\) | the part someone asks us to remove | Carol's 40 digits |
| Retain set | \(D_r\) | everything else in training | 1,217 digits |
| Test set | \(D_{\text{test}}\) | data never used for training | 540 digits |

The course also keeps a small set of **unseen thick-marker digits**, written in Carol's style but never trained on.
Comparing the model on Carol's digits with these "look-alike" digits shows how much it memorised *her* in particular.
See [The notation](../unlearning/notation.md) for all the symbols.

## In code

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print(len(X_train), len(X_test))   # 1257 540
```

`stratify=y` keeps the same share of each digit in both parts. The course library builds all the splits for you:

```python
from mul import lab
L = lab.make_lab("carol")
print(L)   # Lab('carol': |D|=1257, |D_f|=40, |D_r|=1217, |test|=540)
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing on training data.** This hides memorisation, which is exactly what unlearning cares about.
    - **Letting test data leak into training**, for example by scaling all the data together before splitting. Even a
      scaler "learns" averages from the data it sees (Lesson 01 shows this).

## Key takeaways

- Train on one part, test on another part the model has never seen.
- For unlearning, the training set is split into the **forget set** and the **retain set**.
- Comparing the forget set with similar unseen data reveals memorisation.

## Quiz

```quiz
- q: Why do we keep a test set that the model never trains on?
  options:
    - To make training faster
    - To check how well the model works on new data
    - Because the test data is lower quality
  answer: 1
  why: A model can score well on data it has seen just by remembering it. Only unseen data shows real skill.
- q: Carol asks to be forgotten. Which set are her 40 digits?
  options:
    - The test set
    - The retain set
    - The forget set
  answer: 2
  why: The forget set `D_f` is the data that must be removed. Everything else in training is the retain set `D_r`.
- q: How is the retain set related to the training set?
  options:
    - Retain set = training set minus the forget set
    - Retain set = test set
    - Retain set = forget set plus test set
  answer: 0
  why: "`D = D_r ∪ D_f`: the training set is the retain set plus the forget set."
- q: A model scores 100% on Carol's digits but only 77.5% on unseen thick-marker digits. What does this suggest?
  options:
    - The model has memorised Carol's digits.
    - The test set is too small.
    - Thick-marker digits are always wrong.
  answer: 0
  why: It does much better on the exact digits it trained on than on similar new ones. That gap is memorisation.
```

## Try it

- Next page: [Loss functions](loss-functions.md).
- Lesson: [00 · Read this first](../lessons/00-read-first.md) builds these splits with `lab.make_lab("carol")`.
