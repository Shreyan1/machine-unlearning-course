---
title: Gradient descent
description: How a model improves by taking many small steps downhill on the loss.
---

# Gradient descent

!!! oneline "In one line"
    Gradient descent improves a model by nudging its weights, step by step, in the direction that makes the loss smaller.

## Why it matters

Almost every modern model, from small neural networks to large language models, is trained with gradient descent. Many
unlearning methods are built from it too. **Gradient ascent**, for example, runs it backwards to make the model *worse*
on the forget set. To understand those methods, you first need the forward version.

## A simple example

Imagine you are on a hill in thick fog and want to reach the bottom of the valley. You cannot see far, but you can feel
the slope under your feet. So you take a small step in the steepest downhill direction, feel the slope again, and
repeat. Eventually you reach low ground.

- Your **position** is the model's weights.
- The **height** is the loss.
- The **slope** is called the **gradient**.
- The **size of each step** is called the **learning rate**.

## How it works

<ol class="steps" markdown>
<li markdown>**Start** with random weights.</li>
<li markdown>**Pick a small batch** of training examples (say 64). This is called a *mini-batch*.</li>
<li markdown>**Measure the loss** on that batch, and work out the **gradient**: which way each weight should move to reduce it.</li>
<li markdown>**Take a small step**: move every weight a little in the downhill direction.</li>
<li markdown>**Repeat** with the next batch. One pass over all the training data is called an **epoch**.</li>
</ol>

In symbols, one step is:

\[
w \leftarrow w - \eta \, \nabla L(w)
\]

where \(w\) are the weights, \(\eta\) (eta) is the learning rate, and \(\nabla L(w)\) is the gradient of the loss.

### Why this makes unlearning hard

Every step starts from where the last step ended. So if Carol's digits were in an early batch, every later step was
taken from a slightly different place. Her influence is not stored in one spot; it is carried along the whole path. That
is why, in Lesson 04, removing Carol changes **94.1%** of the network's weights.

### Running it backwards: gradient ascent

If you step **uphill** on the forget set instead (\(w \leftarrow w + \eta \nabla L_f(w)\)), the model gets worse on that
data. That is **gradient ascent**, one of the simplest approximate unlearning methods. It is also easy to overdo, as
[Quick fixes and their traps](../unlearning/approximate-unlearning.md) explains.

## In code

A training loop in the course library, written in plain NumPy:

```python
from mul import nn, train, lab
import numpy as np

model = lab.model_fn()                     # a small neural network
opt = nn.Adam(model.params, lr=1e-3)       # Adam is a popular variant of gradient descent
rng = np.random.default_rng(0)
for epoch in range(60):
    for b in train.batches(len(X), 64, rng):                     # mini-batches of 64
        _, g = nn.cross_entropy(model.forward(X[b], keep_cache=True), y[b])
        opt.step(model.backward(g))                              # one step downhill
```

## Common mistakes

!!! danger "Mistakes people make"
    - **A learning rate that is too large.** The steps overshoot and the loss jumps around instead of falling.
    - **Thinking training finds "the" answer.** For neural networks there are many equally good valleys. Two runs with
      different random starts end in different places. This matters a lot for unlearning (see
      [the gold band](../unlearning/gold-band.md)).

## Key takeaways

- The gradient points uphill; gradient descent steps the other way.
- Training is many small steps, each starting where the last one ended.
- So one example's influence is carried through the whole training path.
- Gradient **ascent** on the forget set is a simple, risky way to "untrain".

## Quiz

```quiz
- q: In the foggy hill picture, what does the slope under your feet stand for?
  options:
    - The training data
    - The gradient
    - The test accuracy
  answer: 1
  why: The gradient tells each weight which way is downhill on the loss.
- q: What does the learning rate control?
  options:
    - How big each step is
    - How many examples there are
    - How many classes the model predicts
  answer: 0
  why: A larger learning rate takes bigger steps; too large and the steps overshoot.
- q: What is one pass over all the training data called?
  options:
    - A batch
    - An epoch
    - A gradient
  answer: 1
  why: Training usually runs for many epochs, each made of many mini-batches.
- q: Why does gradient descent spread Carol's influence across the whole model?
  options:
    - Every later step starts from a place her examples already changed.
    - Her data is copied into every weight on purpose.
    - Gradient descent only uses her data.
  answer: 0
  why: Each step depends on the last, so an early nudge from her digits shifts the whole rest of the path.
- q: What does gradient ascent on the forget set do?
  options:
    - Makes the model better on the forget set
    - Makes the model worse on the forget set
    - Deletes the forget set from the database
  answer: 1
  why: Stepping uphill on the loss increases it, so the model gets worse on that data.
```

## Try it

- Next page: [Overfitting and memorisation](overfitting-and-memorisation.md).
- Lesson: [08 · Baselines and traps](../lessons/08-approximate-baselines-and-traps.md) tries gradient ascent as an unlearning method.
