---
title: Naive Bayes
description: Naive Bayes is a model built from counts, sums and averages, so forgetting is a subtraction.
---

# Naive Bayes

!!! oneline "In one line"
    Naive Bayes learns the **average** look of each class from counts and sums, and picks the class whose average a new
    input fits best.

## Why it matters

Naive Bayes is where machine unlearning began. In 2015, Cao and Yang noticed that many models are built from **sums
over the training data**, and if a model is a sum, forgetting a data point is just a **subtraction**. Naive Bayes is the
clearest example.

## A simple example

A teacher keeps a running total of marks and a count of students for each class. To get the class average, they divide
the total by the count. If a student leaves, the teacher does not re-mark every paper; they simply subtract that
student's mark from the total and 1 from the count.

## How it works

<!-- diagram: naive-bayes -->

For handwritten digits, Gaussian Naive Bayes keeps three things for **each digit class**.

| Stored number | Meaning |
|---|---|
| `n` | How many training examples the class has |
| `S1` | The sum of each pixel's brightness |
| `S2` | The sum of each pixel's brightness squared |

From these it computes each pixel's **average** (`S1 / n`) and how much it **varies** (from `S2`). To classify a new
digit, it asks which class's averages this image fits best. It is called *naive* because it treats every pixel
as independent of the others, which is not true, but works surprisingly well.

### Forgetting in Naive Bayes

To forget a row, subtract its values from the model's counts and sums with `n -= 1`, `S1 -= x` and `S2 -= x²`. In Lesson
01, after subtracting Carol's 40 digits, the
largest difference from a model that never saw her, in any predicted log-probability, was **exactly 0**.

### Naive Bayes barely memorises

Because it keeps only averages, one person hardly moves it. In Lesson 01 its accuracy on Carol's digits (60.0%) was
about the same as on unseen thick-marker digits (61.3%). A neural network has a much wider gap, scoring 100% against
77.5%.

!!! note "A side effect to watch"
    After forgetting Carol, the model got worse on everyone who writes like her (61.3% → 37.5% on unseen thick digits),
    because she was the only source of that style. When the people who ask to be forgotten are not a random sample,
    unlearning can hurt an under-represented group. Lesson 12 measures this.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
gnb = classical.GaussianNB(var_smoothing=1e-2).fit(L.X_train, L.y_train)
gnb.unlearn(L.Xf, L.yf)          # subtract Carol's rows from n, S1 and S2
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Forgetting the preprocessing.** A scaler, a vocabulary or word counts are also built from sums over the data.
      They must be unlearnt too.
    - **Ignoring rounding error.** After thousands of add-and-subtract cycles, small floating-point errors can build up,
      so systems refit from scratch now and then.

## Key takeaways

- Naive Bayes is built from counts and sums for each class.
- Forgetting a row is a subtraction, and it is exact.
- Models that keep only averages memorise individuals very little.

## Quiz

```quiz
- q: What does Gaussian Naive Bayes store for each class?
  options:
    - Every training image
    - Counts, sums and sums of squares
    - A deep neural network
  answer: 1
  why: The whole model is n, S1 and S2 for each class; averages and spreads are computed from them.
- q: How do you make Naive Bayes forget a row?
  options:
    - Subtract the row from the counts and sums
    - Retrain the whole model
    - Delete the class
  answer: 0
  why: Because the model is built from sums, removing a row is a subtraction, with an exact result.
- q: Why did Naive Bayes barely memorise Carol?
  options:
    - It keeps only averages, which one person hardly moves.
    - It was not trained on her data.
    - It is a neural network.
  answer: 0
  why: Its accuracy on her digits (60.0%) was about the same as on look-alike digits it never saw (61.3%).
- q: What else, besides the model, must be unlearnt in a Naive Bayes pipeline?
  options:
    - Nothing
    - Preprocessing steps fitted on the data, such as scalers and vocabularies
    - The test set
  answer: 1
  why: Preprocessing is also "trained" on the data, so it carries the deleted rows' influence too.
```

## Try it

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [01 · k-NN and Naive Bayes](../lessons/01-knn-and-naive-bayes.md).
