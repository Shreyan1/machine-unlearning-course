---
title: Influence functions
description: Estimate how much one training example shaped a model, and what removing it would change, without retraining.
---

# Influence functions

!!! oneline "In one line"
    An **influence function** estimates how much one training example changed a model, and so roughly what removing it
    would do, without retraining.

## Why it matters

Before you forget someone, it helps to know how much they mattered. Influence tells you which training examples a
prediction leans on, which people a model has [memorised](../ml-basics/overfitting-and-memorisation.md), and which
deletions will be cheap or costly. The same calculation also gives a one-step way to *unlearn*, because it is the Newton
step behind [certified unlearning](certified-unlearning.md).

## A simple example

A class average is easy to update. If one student's score is removed, you know exactly how the average moves. A model
is a far more tangled "average" of its training data, so the effect of removing one example cannot be read off directly.
An influence function estimates it with calculus instead of recomputing everything.

## How it works

### The formula

Train a model to the weights \(\hat\theta\) that minimise the average loss over \(n\) examples. Removing one example
\(z\) moves the weights by approximately

\[
\hat\theta_{-z} - \hat\theta \approx \frac{1}{n} H^{-1} \nabla_\theta L(z, \hat\theta),
\]

where \(\nabla_\theta L(z, \hat\theta)\) is the gradient of that example's loss (which way it pulls the weights) and
\(H\) is the Hessian, the curvature of the total loss (how firmly the other examples hold the weights in place).

To see the effect on a test example \(z_{\text{test}}\), combine the two:

\[
\mathcal{I}(z, z_{\text{test}}) = -\nabla_\theta L(z_{\text{test}}, \hat\theta)^{\top} H^{-1} \nabla_\theta L(z, \hat\theta).
\]

A large value means \(z\) strongly shapes the prediction on \(z_{\text{test}}\). This is the approach of
Koh and Liang 2017.

### Where it works, and where it does not

| Model | How good is the estimate? | Notes |
|---|---|---|
| Ridge and logistic regression | Close | One best answer, so the maths holds; for ridge, the exact [downdate](exact-unlearning-classical.md) is just as cheap |
| Small neural networks | Rough | The Hessian is huge and the loss has many minima; estimates can be [fragile](https://arxiv.org/abs/2006.14651) (Basu et al. 2021) |
| Large models | Approximate methods only | Scalable versions such as TRAK (Park et al. 2023) and EK-FAC for language models (Grosse et al. 2023) trade accuracy for speed |

### What people use it for

- **Auditing.** Find the training examples behind a surprising prediction.
- **Finding memorised people.** An example with huge self-influence is probably memorised, and is a likely target for
  [membership inference](membership-inference-attacks.md).
- **Triage.** Estimate which deletion requests will barely change the model and which will change it a lot.
- **A fast unlearning step.** Apply the weight change above for each forgotten example, then check the result.

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting deep-network influence scores as exact.** They are estimates, and they can be unstable.
    - **Inverting a Hessian that is not invertible.** In practice people add a small damping term, which changes the
      answer.
    - **Treating low influence as proof of forgetting.** Influence estimates one example's effect. It is not an audit.

## Key takeaways

- Influence functions estimate the effect of one training example without retraining.
- They combine the example's gradient with the curvature of the loss.
- They are reliable for convex models and rough for deep networks.
- They help with auditing and triage, and they power one-step unlearning updates.

## Quiz

```quiz
- q: What does an influence function estimate?
  options:
    - How long training takes
    - How much one training example changed the model
    - The size of the test set
  answer: 1
  why: It approximates the effect of removing (or up-weighting) a single example, without retraining.
- q: Which two ingredients does the influence formula combine?
  options:
    - The example's gradient and the Hessian of the loss
    - The learning rate and the batch size
    - The accuracy and the loss
  answer: 0
  why: The gradient says which way the example pulls; the Hessian says how firmly the rest of the data holds the weights.
- q: For which models are influence estimates most reliable?
  options:
    - Convex models such as logistic regression
    - Very deep networks
    - Language models
  answer: 0
  why: Convex models have one best answer, which the maths assumes. Deep networks break that assumption.
- q: An example has very high self-influence. What does that suggest?
  options:
    - It was probably memorised.
    - It was never used in training.
    - The model is underfitting.
  answer: 0
  why: If the model's fit to an example depends heavily on that example alone, the model has likely memorised it.
```

## Try it

- Read [certified unlearning](certified-unlearning.md), which turns this weight change into a guarantee.
- Run [Lesson 02](../lessons/02-linear-and-logistic-regression.md) and compare the one-step update with retraining.
