---
title: Neural networks
description: A neural network is layers of numbers trained together by gradient descent. Every example nudges every weight.
---

# Neural networks

!!! oneline "In one line"
    A neural network is a stack of **layers of numbers** that turns an input into an answer, and training nudges *all*
    of those numbers for every batch of examples.

## Why it matters

Neural networks power almost all modern AI, from image recognition to chatbots. They are also where unlearning gets
hard. Every trick that worked for classical models (subtract a sum, take a Newton step, rebuild only the part a point
touched) fails here. Understanding why is the turning point of the course.

## A simple example

Think of a big mixing desk in a recording studio, with thousands of knobs. Sound goes in one end and music comes out the
other. Training means turning every knob a tiny bit, over and over, until the music sounds right. Once that is done,
you cannot point to "the knob for the drums". Every knob affects every part of the sound.

## How it works

<ol class="steps" markdown>
<li markdown>**Input layer**: the raw data. For the digits, 64 pixel values.</li>
<li markdown>**Hidden layers**: each layer multiplies its inputs by a table of **weights**, adds a number and applies a simple bend (such as "keep it if positive, otherwise 0"). The course network has two hidden layers of 256 neurons each.</li>
<li markdown>**Output layer**: 10 scores, one per digit, turned into probabilities with [softmax](probabilities-and-kl-divergence.md).</li>
<li markdown>**Training**: [gradient descent](gradient-descent.md) on the [cross-entropy loss](loss-functions.md). A method
called *backpropagation* works out how each weight should move.</li>
</ol>

The course network is written as `MLP(64 -> 256 -> 256 -> 10)` and has **85,002** weights. It is written in plain NumPy,
so every gradient is a line of code you can read.

### Why neural networks are hard to unlearn

Lesson 04 tests each classical trick and finds that all three fail:

| Trick | Why it fails in a neural network |
|---|---|
| **Subtract** the person's contribution | Removing Carol changes **94.1%** of the 85,002 weights. Her influence is everywhere. |
| **One Newton step** to the new answer | It needs a table of 85,002 × 85,002 numbers, about 29 GB. And there is no single best answer to step to. |
| **Rebuild only the part** she touched | She touched every part. |

### Many equally good networks

A neural network's loss has many valleys, not one bowl. Two networks trained on the same data with different random
starts end up in different places, yet are equally accurate. In Lesson 04, two such networks were further apart (distance
50.96) than the with-Carol and without-Carol pair (distance 9.87).

So there is no single "retrained model" to compare against. There is a whole **spread** of them. That is why proof of
forgetting must be about **behaviour**, measured against a [gold band](../unlearning/gold-band.md).

### Neural networks memorise more

More flexible models remember individuals more. In Lesson 04, the network was right on 100% of Carol's digits but only
77.5% of look-alike digits, a gap of +22.5%. Naive Bayes had a gap of −1.3%.

## In code

```python
from mul import lab, train
model = lab.model_fn()             # MLP(64 -> 256 -> 256 -> 10, 85,002 params)
L = lab.make_lab("carol")
model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)   # 60 epochs of Adam
print(train.accuracy(model, L.X_test, L.y_test))                           # about 0.98
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Looking for "the person's weights".** There are none. Influence is spread across the whole network.
    - **Comparing weights to prove forgetting.** Equally good networks have very different weights. Compare behaviour.

## Key takeaways

- A neural network is layers of weights, all trained together by gradient descent.
- Every example nudges every weight, so one person's influence is spread everywhere.
- There are many equally good networks, so the gold standard is a spread, not a single point.
- Retraining from scratch is the only exact option, unless you design for deletion (see [SISA](../unlearning/sisa.md)).

## Quiz

```quiz
- q: How many weights does the course's neural network have?
  options:
    - 64
    - 85,002
    - 7 billion
  answer: 1
  why: "MLP(64 -> 256 -> 256 -> 10) has 85,002 weights."
- q: When Carol is removed and the network retrained from the same start, what share of weights change?
  options:
    - About 1%
    - About 50%
    - 94.1%
  answer: 2
  why: Her influence is spread across almost the whole network.
- q: Two networks are trained on identical data with different random starts. What happens?
  options:
    - They end up with identical weights.
    - They end up with very different weights but similar accuracy.
    - One of them always fails.
  answer: 1
  why: The loss has many equally good valleys. This is why the gold standard is a band, not a single model.
- q: Why must proof of forgetting in a neural network be about behaviour?
  options:
    - Weights differ between equally good models anyway, so comparing weights proves nothing.
    - Weights are secret.
    - Neural networks have no weights.
  answer: 0
  why: Only behaviour can be compared fairly with models that never saw the data.
```

## Try it

- Concept: [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md).
- Lesson: [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md).
