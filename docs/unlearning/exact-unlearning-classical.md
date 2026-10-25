---
title: Exact unlearning for classical models
description: For many classical models, forgetting is a deletion, a subtraction, a downdate or rebuilding only the part a point touched.
---

# Exact unlearning for classical models

!!! oneline "In one line"
    Many classical models can forget **exactly and cheaply**, because they are a sum you can subtract from, a formula you
    can update, or made of parts that only some points touched.

## Why it matters

Before reaching for complex methods, check whether the model (or part of the system) is classical. Indexes, counts,
scalers, Naive Bayes filters and many ranking models are. For them, exact forgetting is often a few milliseconds of
work, with a result you can prove is identical to retraining.

## A simple example

A shopkeeper keeps a running total of the day's sales. If a customer returns an item, the shopkeeper does not re-add
every sale of the day. They subtract that one sale. The total is now exactly what it would have been if the sale had
never happened.

## How it works

Lessons 01 to 03 find three properties that make exact forgetting possible.

### 1. The model is the data, or a sum

| Model | What it stores | How to forget | Result in the course |
|---|---|---|---|
| [k-NN](../ml-basics/k-nearest-neighbours.md) | the rows themselves | delete the rows | 100% identical predictions, ~0.15 ms |
| [Naive Bayes](../ml-basics/naive-bayes.md) | counts and sums per class | subtract the rows | identical log-probabilities, ~0.1 ms |

In 2015, Cao and Yang named this the **summation form**: if a model is a sum over the training data, forgetting is a
subtraction. This is where machine unlearning began.

### 2. The model is a formula of sums

[Ridge regression](../ml-basics/linear-and-ridge-regression.md) computes \(w = (X^\top X + \lambda I)^{-1} X^\top y\). The
inverse mixes all the points together, but a **Sherman-Morrison downdate** still removes a point exactly. In Lesson 02 the
result matched a refit to within 4.38 × 10⁻¹³.

[Logistic regression](../ml-basics/logistic-regression.md) has no formula, so a **Newton step** *estimates* the new
answer. One step closed 94.8% of the gap; two closed 99.9%. This is where unlearning first becomes approximate.

### 3. Locality: only some parts depend on a point

| Model | Where locality comes from | Forgetting a typical user | Forgetting Carol |
|---|---|---|---|
| [SVM](../ml-basics/support-vector-machines.md) | only support vectors matter | free, if not a support vector | re-solve: 97.5% of her digits are support vectors |
| [Random forest](../ml-basics/decision-trees-and-random-forests.md), bootstrap bags | each tree has its own bag | ~63% of trees | all 50 trees |
| Random forest, **user-aware shards** | each user lives in one shard | one shard | **10 of 50 trees** |

!!! tip "Locality can be designed in"
    Whether forgetting Carol costs 10 trees or 50 was decided at **training time**, by how the data was split. Split by the unit people will ask to delete, such as a user, a customer or a document source. [SISA](sisa.md) does the same for neural
    networks.

### Do not forget the pipeline

A scaler, a TF-IDF vocabulary, PCA and feature selection are all **fitted on the data**, so they all carry the forget
set's influence. In Lesson 01, a `StandardScaler`'s stored mean moved by 0.0171 when Carol was removed. An unlearning
request must cover the whole pipeline, not just the final model.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
classical.KNN(k=5).fit(L.X_train, L.y_train).unlearn(L.forget_idx)            # delete
classical.GaussianNB(1e-2).fit(L.X_train, L.y_train).unlearn(L.Xf, L.yf)      # subtract
classical.BaggedForest(50, seed=0).fit(L.X_train, L.y_train).unlearn(L.forget_idx)  # rebuild touched trees
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Using approximate methods on models that can forget exactly.** If a subtraction works, use it.
    - **Forgetting copies and preprocessing.** Indexes, caches, scalers and vocabularies hold the data too.
    - **Assuming locality is automatic.** Bootstrap bags spread each row across most trees.

## Key takeaways

- Sum-based models (k-NN, Naive Bayes) forget exactly by deletion or subtraction.
- Ridge regression forgets exactly by a downdate; logistic regression approximately by a Newton step.
- Locality (SVMs, sharded forests) means only the touched parts need rebuilding.
- Unusual data is the expensive data to forget, because it has more leverage and more support vectors.

## Quiz

```quiz
- q: What is the "summation form" idea from Cao and Yang (2015)?
  options:
    - If a model is a sum over the data, forgetting is a subtraction.
    - All models should be summed together.
    - Models must be trained twice.
  answer: 0
  why: This observation is where machine unlearning began.
- q: Which method removes a point exactly from ridge regression?
  options:
    - A Sherman-Morrison downdate
    - Gradient ascent
    - Bad Teacher
  answer: 0
  why: The downdate updates the inverse directly, matching a refit up to rounding error.
- q: Why does forgetting Carol from an SVM need real work?
  options:
    - Almost all of her digits are support vectors.
    - SVMs cannot be retrained.
    - Her digits are in the test set.
  answer: 0
  why: 97.5% of her digits were support vectors, so removing them moves the boundary.
- q: How many of 50 trees did a user-aware sharded forest retrain to forget Carol?
  options:
    - 10
    - 31
    - 50
  answer: 0
  why: All her data was in one shard of 10 trees, so only that shard needed rebuilding.
- q: A pipeline has a StandardScaler before the model. What must happen to it when Carol is forgotten?
  options:
    - Nothing; scalers do not learn.
    - It must be unlearnt too, because its stored means came from the data.
  answer: 1
  why: The scaler's mean moved by 0.0171 when Carol was removed. Preprocessing is a model too.
```

## Try it

- Next concept: [SISA, sharded training](sisa.md).
- Lessons: [01](../lessons/01-knn-and-naive-bayes.md), [02](../lessons/02-linear-and-logistic-regression.md) and
  [03](../lessons/03-svm-and-random-forest.md).
