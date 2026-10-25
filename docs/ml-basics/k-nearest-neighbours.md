---
title: k-nearest neighbours
description: k-NN answers by asking the k most similar training examples to vote. The model is the data itself.
---

# k-nearest neighbours (k-NN)

!!! oneline "In one line"
    To classify something new, k-NN finds the *k* most similar training examples and lets them **vote**.

## Why it matters

k-NN is the easiest model to unlearn, because the model **is** the training data. There is no training step that mixes
examples together. It is also the model behind "find similar items" features and the vector stores used in retrieval
(RAG) systems, so it shows up in real products.

## A simple example

You move to a new city and want a good place for dinner. You ask the five neighbours who live closest to you, and pick
the restaurant most of them recommend. That is k-NN with \(k = 5\).

## How it works

<ol class="steps" markdown>
<li markdown>**"Training"** just stores all the examples and their labels.</li>
<li markdown>**For a new input**, measure its distance to every stored example (for images, how different the pixels are).</li>
<li markdown>**Pick the k closest** ones, the "nearest neighbours".</li>
<li markdown>**Vote**: predict the label that most of them have.</li>
</ol>

The choice of \(k\) matters. A small \(k\) follows individual examples closely; a large \(k\) smooths things out.

### Forgetting in k-NN

Because the model is the data, forgetting a row means **deleting it from the stored set**. The result is exactly the
same as a k-NN built without that row. In Lesson 01:

- Before unlearning, **85.8%** of the neighbours consulted for new thick-marker digits were Carol's own digits.
- After deleting her rows (in 0.15 milliseconds), that share was **0.0%**.
- Predictions matched a k-NN that never saw Carol on **100%** of 1,877 inputs.

!!! warning "The catch in real systems"
    The k-NN index is exact, but real systems copy data elsewhere: approximate search indexes, caches, backups, and
    any **embedding model fine-tuned** on the same data. Deleting a document from a vector store is the easy k-NN case;
    removing it from a fine-tuned model is the hard deep-learning case.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
knn = classical.KNN(k=5).fit(L.X_train, L.y_train)
knn.unlearn(L.forget_idx)        # mark Carol's rows as deleted
print(knn.predict(L.X_test[:5]))
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking k-NN does not "remember" anyone.** It keeps every example, so it can show a person's raw data to others
      through "similar examples" features.
    - **Forgetting the copies.** Deleting from the main index is not enough if the data also lives in a cache or a
      fine-tuned encoder.

## Key takeaways

- k-NN stores the data and lets the nearest examples vote.
- The model is the data, so deleting a row is exact unlearning, and almost free.
- Copies of the data elsewhere in the system must be removed too.

## Quiz

```quiz
- q: What does k-NN do during "training"?
  options:
    - Stores the examples and labels
    - Runs gradient descent for many epochs
    - Builds a set of decision trees
  answer: 0
  why: k-NN does no real training; all the work happens when it compares a new input with the stored examples.
- q: How do you make a k-NN model forget one person's rows?
  options:
    - Delete their rows from the stored set
    - Retrain for 60 epochs
    - Add random noise to every prediction
  answer: 0
  why: The model is the data, so removing the rows gives exactly the model you would have built without them.
- q: Before unlearning, what share of the neighbours for new thick-marker digits were Carol's?
  options:
    - About 10%
    - About 50%
    - 85.8%
  answer: 2
  why: Carol was the only person with that style, so her digits were consulted for almost every similar query.
- q: A company deletes a document from its vector store, but a model was also fine-tuned on it. Is the document forgotten?
  options:
    - Yes, the vector store was the only copy that mattered.
    - Not fully; the fine-tuned model still carries its influence.
  answer: 1
  why: The vector store is the easy k-NN case. The fine-tuned model is the hard deep-learning case.
```

## Try it

- Concept: [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Lesson: [01 · k-NN and Naive Bayes](../lessons/01-knn-and-naive-bayes.md).
