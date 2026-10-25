---
title: Overfitting and memorisation
description: When a model remembers individual examples instead of learning general patterns, and why unusual data is remembered most.
---

# Overfitting and memorisation

!!! oneline "In one line"
    **Memorisation** is when a model gets an example right *because it saw that exact example* in training, not because
    it learnt the general pattern.

## Why it matters

If a model never memorised anyone, unlearning would hardly be needed, because removing one person would barely change it.
Memorisation is what makes a model carry a specific person's data, and it is what attackers use to tell whether
someone's data was used. It is the heart of the problem this course solves.

## A simple example

Two students prepare for a maths exam.

- **Student A** understands the methods. They can solve new questions.
- **Student B** memorises the answers to last year's paper. They score 100% on that paper and badly on new questions.

Student B has **overfitted**: they fit the practice questions perfectly but did not learn the subject. A model can do
the same.

## How it works

<!-- diagram: overfitting-and-memorisation -->

### Overfitting

A model **overfits** when it is much better on its training data than on new data. Signs of overfitting:

- training accuracy is much higher than test accuracy;
- training loss keeps falling while test loss stops falling or rises.

### Memorisation of individual examples

Memorisation is overfitting looked at **one example at a time**. The researcher Vitaly Feldman (2020) measured it like
this:

\[
\text{mem}(x) = P[\text{right on } x \mid x \text{ in training}] - P[\text{right on } x \mid x \text{ not in training}]
\]

In plain words, it asks how much more often is the model right on \(x\) when \(x\) was in training? You estimate it by training
several models with and without the example.

- For a **typical** digit, the score is about 0. Thousands of similar digits teach the same thing.
- For an **unusual** digit, like one of Carol's thick-marker digits, the score is often high. Nothing else teaches it.

### Unusual data is remembered most

This is called the **long tail**. Real data contains many rare cases, and to get them right a model has to memorise
them. The course sees this again and again:

| Lesson | How Carol stands out |
|---|---|
| 02 | Her digits have about **3 ×** the *leverage* (pull on the model) of a typical digit: 0.116 vs 0.039. |
| 03 | **97.5%** of her digits are support vectors in an SVM, against 40.5% for everyone else. |
| 04 | A neural network is right on 100% of her digits but only 77.5% of look-alike digits it never saw. |

!!! note "A Responsible AI point"
    People with unusual data are memorised more, so they are also more exposed to privacy attacks. Deletion requests
    are not spread evenly, and the people who ask are often exactly the hard cases.

### More flexible models memorise more

In Lesson 04, the "memorisation gap" (accuracy on Carol minus accuracy on look-alike digits) was −1.3% for Naive
Bayes, +15.0% for logistic regression, +22.5% for a neural network and +30.0% for a random forest. Simple models that
keep only averages remember individuals much less.

## In code

The memorisation gap is two accuracy numbers:

```python
from mul import lab, train
L = lab.make_lab("carol")
model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
gap = train.accuracy(model, L.Xf, L.yf) - train.accuracy(model, L.X_like_forget, L.y_like_forget)
print(f"memorisation gap: {gap:+.1%}")   # +22.5%
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing unlearning on random users only.** Random users are barely memorised, so almost any method looks like
      it works. Test on the hard, unusual cases.
    - **Thinking a good test score means no memorisation.** A model can have high test accuracy *and* memorise rare
      examples. Both happen at once.

## Key takeaways

- Overfitting: much better on training data than on new data.
- Memorisation: right on an example *because* it was trained on it.
- Unusual examples are memorised the most, so they are the hardest to forget.
- More flexible models memorise more.

## Quiz

```quiz
- q: Which student in the example overfitted?
  options:
    - The one who understood the methods
    - The one who memorised last year's answers
  answer: 1
  why: They fit the practice paper perfectly but cannot handle new questions.
- q: Feldman's memorisation score for a typical digit is usually...
  options:
    - About 0
    - About 1
    - Negative and large
  answer: 0
  why: Thousands of similar digits teach the same pattern, so the model gets it right whether or not that digit was in training.
- q: Which data is memorised the most?
  options:
    - Typical, common examples
    - Unusual examples, like Carol's thick-marker digits
    - Test data
  answer: 1
  why: Nothing else in the data teaches the model about rare cases, so it has to memorise them.
- q: Why is testing an unlearning method only on random users a mistake?
  options:
    - Random users are barely memorised, so almost any method looks successful.
    - Random users cannot ask for deletion.
    - Random users are always in the test set.
  answer: 0
  why: The real test is on memorised, unusual data, where forgetting actually has to do work.
```

## Try it

- Next page: [Probabilities and KL divergence](probabilities-and-kl-divergence.md).
- Lesson: [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) measures memorisation for six models.
