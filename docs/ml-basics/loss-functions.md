---
title: Loss functions
description: A loss function turns "how wrong is the model?" into a single number that training can make smaller.
---

# Loss functions

!!! oneline "In one line"
    A **loss** is one number that says how wrong the model is; training tries to make it as small as possible.

## Why it matters

A computer cannot "try harder" without knowing what *better* means. The loss gives it a target, and lower is better.
Unlearning uses loss too. Some methods try to make the loss on the forget set go **up** again, and attackers look at
the loss on a person's data to guess whether it was used in training.

## A simple example

Think of a darts game. The loss is the distance between your dart and the bullseye. A perfect throw has loss 0. A wild
throw has a large loss. Practising means changing your throw so that the average distance gets smaller.

## How it works

For classification, the most common loss is **cross-entropy**. The idea is simple:

<ol class="steps" markdown>
<li markdown>The model gives a **probability** for each possible answer. For a digit image, it might say "7: 0.90, 1: 0.05, ...".</li>
<li markdown>Look at the probability it gave to the **right** answer.</li>
<li markdown>The loss is large when that probability is small, and close to 0 when it is close to 1.</li>
<li markdown>Average this over all the examples to get the training loss.</li>
</ol>

In symbols, for one example whose right answer got probability \(p\):

\[
\text{loss} = -\log(p)
\]

| Probability given to the right answer | Loss |
|---|---|
| 0.99 | 0.01 |
| 0.90 | 0.11 |
| 0.50 | 0.69 |
| 0.10 | 2.30 |

So a confident right answer costs almost nothing, and a confident wrong answer costs a lot.

### Loss and memorisation

A model usually has a **lower loss on data it trained on** than on new data. If Carol's digits have a much lower loss
than similar digits the model never saw, the model remembers her. Lesson 04 shows Carol's loss falling to almost zero
while look-alike digits stay much higher. This is also the basis of [membership inference attacks](../unlearning/membership-inference-attacks.md).

## In code

The course library computes cross-entropy from the model's raw outputs (called *logits*):

```python
from mul import nn
loss, grad = nn.cross_entropy(model(X), y)   # average loss, and its gradient for training
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Treating low training loss as success.** Very low loss on training data can mean memorisation.
    - **Pushing the loss on forgotten data as high as possible.** A model that never saw Carol would not have a
      huge loss on her digits. A suspiciously high loss is itself a sign that something happened (see
      [the gold band](../unlearning/gold-band.md)).

## Key takeaways

- The loss is a single "how wrong" number; training makes it smaller.
- Cross-entropy is small when the model gives high probability to the right answer.
- Lower loss on training data than on similar new data is a sign of memorisation.

## Quiz

```quiz
- q: What does a loss of 0 mean?
  options:
    - The model is as wrong as possible.
    - The model's answer is perfect.
    - The model has not been trained.
  answer: 1
  why: Lower is better. Zero loss means the model gave the right answer with full confidence.
- q: The model gives the right answer a probability of 0.10. Is the cross-entropy loss high or low?
  options:
    - High
    - Low
  answer: 0
  why: "-log(0.10) is about 2.30, much higher than -log(0.99), which is about 0.01."
- q: Carol's digits have a much lower loss than similar digits the model never saw. What does that suggest?
  options:
    - The model remembers Carol's digits.
    - Carol's digits are easier for everyone.
    - The loss function is broken.
  answer: 0
  why: Training pushes the loss down on the examples it sees. A big gap versus look-alike data shows memorisation.
- q: After unlearning, should the loss on Carol's digits be as high as possible?
  options:
    - Yes, the higher the better.
    - No, it should look like the loss of a model that never saw her.
  answer: 1
  why: A model that never met Carol would not be extremely wrong on her digits. Over-forgetting is a warning sign.
```

## Try it

- Next page: [Gradient descent](gradient-descent.md).
- Lesson: [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) plots Carol's loss during training.
