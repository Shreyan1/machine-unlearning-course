---
title: Start here
description: New to the course? Read this page first.
---

# Start here

Welcome! This site teaches **machine unlearning**: how to make a trained AI model forget some of the data it learnt
from, and how to check, with evidence, that it really did.

You do not need to be an expert. If you know a little Python and have heard words like "training" and "model", you
can follow along. If you have not, the [ML Basics](../ml-basics/index.md) section starts from zero.

## The idea in three sentences

1. A model learns from data, and that data leaves a mark inside the model's numbers.
2. When someone asks for their data to be deleted, deleting the file does not remove that mark.
3. Machine unlearning removes the mark, and a good audit checks that the model now behaves as if the data had never
   been there.

## Where to go next

<div class="cards" markdown>
<a class="card" href="how-to-use/">
<span class="card__num">Step 1</span>
<span class="card__title" markdown="span">:material-map-outline: How to use this site</span>
<span class="card__text">What each part of the site is for, and how the quizzes and notebooks fit together.</span>
</a>
<a class="card" href="learning-paths/">
<span class="card__num">Step 2</span>
<span class="card__title" markdown="span">:material-sign-direction: Pick your path</span>
<span class="card__text">Short routes for beginners, legal and policy readers, researchers, LLM engineers and platform teams.</span>
</a>
<a class="card" href="glossary/">
<span class="card__num">Anytime</span>
<span class="card__title" markdown="span">:material-book-alphabet: Glossary</span>
<span class="card__text">Every term and symbol on one page, each with a plain-words meaning.</span>
</a>
</div>

!!! tip "The one idea to remember"
    The goal of unlearning is **not** to make the model score zero on the deleted data. The goal is to make it behave
    like a model that was **never trained on that data**. Everything else on this site follows from this.

## Quiz

```quiz
- q: What does machine unlearning try to remove?
  options:
    - The data file from the database
    - The influence that some data left inside a trained model
    - The whole model
  answer: 1
  why: Deleting the file is easy. Unlearning is about the mark the data left on the model's numbers.
- q: After unlearning Carol, the model should behave like...
  options:
    - A model that scores 0% on Carol's data
    - A model that was never trained on Carol's data
    - The original model
  answer: 1
  why: The target is always the model you would have had if the data had never been there.
- q: You are completely new to machine learning. Which section should you read first?
  options:
    - ML Basics
    - The enterprise playbook
    - The method zoo
  answer: 0
  why: ML Basics explains training, loss, gradient descent and the models used in the course, starting from zero.
```
