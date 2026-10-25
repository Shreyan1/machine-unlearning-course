---
title: Unlearning at scale
description: Retraining for every request grows with the square of the service size. Batching and SISA bring it back down, and exact Newton updates do not fit deep models.
---

# Unlearning at scale

!!! oneline "In one line"
    Retraining for every deletion request makes the yearly bill grow with the **square** of the service size, so big
    services need batching, SISA, or exact updates that fit their model.

## Why it matters

Real services do not get one request. They get a steady stream, every week, for years, each with a legal deadline (at
most one month under GDPR). A method that is fine for one request can be impossible for a year of them. Scale changes
*which* way of reaching the retrained model you can afford, not the goal.

## A simple example

A small café can repaint its whole shop every time a customer complains about one wall. A chain of a thousand cafés,
with a thousand times as many complaints, cannot repaint every shop for every complaint. It needs to batch the repairs,
or build walls that can be repainted one panel at a time.

## How it works

Lesson 20 runs a year of requests on the digit service: **2 requests a week**, 104 in the year (8.3% of users).

### Why the bill grows with the square

If a service is twice as big, each retrain costs twice as much, **and** there are twice as many requests. So retraining
for every request grows with the square of the size.

| Users | Retrain every request vs every 4 weeks |
|---|---|
| 1,000 | 6 × more expensive |
| 100,000 | 636 × more |
| 10,000,000 | 63,644 × more |

### SISA under a stream of requests

With \(K\) shards and a batch of \(b\) random requests, the expected number of shards touched is:

\[
\mathbb{E}[\text{shards touched}] = K\left(1 - \left(1 - \tfrac{1}{K}\right)^{b}\right)
\]

For \(K = 5\) and \(b = 8\), that is already 4.2 of the 5 shards. Big batches make SISA cost almost as much as a full
retrain, so more shards help, at a price in accuracy:

| Shards | Test accuracy | One request (share of retrain) | One month's batch |
|---|---|---|---|
| 1 | 97.8% | 1.000 | 1.000 |
| 5 | 98.0% | 0.200 | 0.832 |
| 20 | 95.6% | 0.050 | 0.337 |
| 40 | 92.8% | 0.025 | 0.183 |

### A whole year, four strategies

| Strategy | Cost vs retrain-each | Longest wait | Inside the deadline? |
|---|---|---|---|
| Retrain for each request | 1.000 | 0 weeks | ✅ |
| Retrain monthly | 0.125 | 3 weeks | ✅ |
| SISA-20, each request at once | 0.023 | 0 weeks | ✅ |
| SISA-20, monthly batch | 0.019 | 3 weeks | ✅ |

Batching saves plain retraining 8 ×, but saves SISA little, because a month's batch still touches about 7 of 20 shards.
So SISA can serve every request **straight away** and still be about 5 × cheaper than monthly retraining. After the
whole year, the SISA model was **bit-for-bit** equal to a fresh SISA model trained without the 104 deleted users.

### Exact Newton updates: fine for linear models, impossible for deep ones

For logistic regression, the Newton step's small errors did **not** pile up over 26 batches; each step also corrects
the last. But certified removal spends a fixed noise budget, so a full retrain must still be scheduled. And the Hessian
grows with the square of the weights:

| Model | Hessian memory |
|---|---|
| 650 weights | 3.4 MB |
| The course MLP, 85,002 weights | 57.8 GB |
| A 1-billion-weight language model | 8,000,000,000 GB |

### A policy for the year

| Model | Serve requests with | And also |
|---|---|---|
| Linear or logistic | Newton removal per request | full retrain when the noise budget runs out |
| Small deep model | retrain every 4 weeks | batch inside the deadline |
| Large deep model | SISA with many shards, as requests arrive | accept a few points of accuracy |
| Any model | never an approximate method alone | only with an audit and a scheduled exact retrain |

## Common mistakes

!!! danger "Mistakes people make"
    - **Planning for one request.** The stream is what costs money.
    - **Assuming batching always helps.** It helps retraining a lot and SISA little; use the formula.
    - **Choosing K without measuring accuracy.** More shards mean cheaper deletes but weaker shard models.

## Key takeaways

- Retrain-per-request grows with the square of the service size; batching brings it back to linear.
- The shards-touched formula predicts SISA's cost under batches.
- SISA stays exact, bit for bit, after a year of requests.
- Exact Newton updates scale for linear models, not deep ones.

## Quiz

```quiz
- q: Why does retraining for every request grow with the square of the service size?
  options:
    - Each retrain costs more and there are more requests.
    - Models get slower every year.
    - The law doubles the requests.
  answer: 0
  why: Twice the users means twice the cost per retrain and twice as many requests.
- q: With 5 shards and a batch of 8 random requests, about how many shards are touched?
  options:
    - About 1
    - About 4.2
    - All 8
  answer: 1
  why: "K(1 − (1 − 1/K)^b) = 5(1 − 0.8^8) ≈ 4.2."
- q: Why does batching save SISA much less than plain retraining?
  options:
    - A batch still touches many shards, so requests do not share much work.
    - SISA cannot batch.
    - Batching makes SISA inexact.
  answer: 0
  why: A month's batch of 8 still touched about 7 of 20 shards.
- q: Why can exact Newton updates not be used for the course's neural network?
  options:
    - Its Hessian would need about 58 GB.
    - It has no gradient.
    - Newton steps are illegal.
  answer: 0
  why: The Hessian has one row and column per weight, so memory grows with the square of the weights.
- q: Was SISA still exact after a year of 104 deletions?
  options:
    - Yes, bit for bit
    - Only approximately
    - No
  answer: 0
  why: All 20 shard models matched a fresh SISA model trained without the deleted users, weight for weight.
```

## Try it

- Next concept: [The enterprise playbook](enterprise-playbook.md).
- Lesson: [20 · Unlearning at scale](../lessons/20-unlearning-at-scale.md).
