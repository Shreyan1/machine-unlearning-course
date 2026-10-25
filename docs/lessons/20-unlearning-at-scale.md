---
title: "Lesson 20: Unlearning at scale"
description: A year of deletion requests. The bill for per-request retraining grows with the square of the service, SISA stays exact and Newton updates do not fit deep models.
---

# Lesson 20: Unlearning at scale, a year of deletion requests

<div class="chips"><span class="chip">⏱ ~40 min</span><span class="chip">Stage 8 · Extensions</span></div>

<div class="buttons">
<a class="md-button md-button--primary" href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/20-Unlearning-at-Scale.ipynb">Open in Colab</a>
<a class="md-button" href="https://github.com/Shreyan1/machine-unlearning-course/blob/main/20-Unlearning-at-Scale.ipynb">View on GitHub</a>
</div>

## The story

Lesson 07 removed one request with SISA; Lesson 17 planned capacity. Real services get a steady stream of requests,
every week, for years. The digit service here gets **2 requests a week**: 104 in a year (8.3% of users), each with a
one-month deadline.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the service in three ways, as one model, as SISA with 5 shards and as SISA with 20 shards.</li>
<li markdown>**Show the issue**: how the bill for per-request retraining grows with service size.</li>
<li markdown>**Untrain** under a stream of requests, and check SISA's shards-touched formula against real runs.</li>
<li markdown>**Show the result**: a whole year with four strategies, and the cost of exact Newton updates.</li>
<li markdown>**Prove it**: after a year, is SISA still bit-for-bit exact?</li>
</ol>

## Key results

**The square law.** Retraining for every request versus every 4 weeks: 6 × more expensive at 1,000 users, 636 × at
100,000, 63,644 × at 10 million.

**SISA under batches.** Expected shards touched: \(K(1 - (1 - 1/K)^b)\). For K = 5 and b = 8, about 4.2 of 5. The formula
matched real runs (4.33 measured). More shards help, at a price:

| Shards | Test accuracy | One request | One month's batch |
|---|---|---|---|
| 1 | 97.8% | 1.000 | 1.000 |
| 20 | 95.6% | 0.050 | 0.337 |
| 40 | 92.8% | 0.025 | 0.183 |

**A whole year:**

| Strategy | Cost vs retrain-each | Longest wait | In deadline? |
|---|---|---|---|
| Retrain each request | 1.000 | 0 weeks | ✅ |
| Retrain monthly | 0.125 | 3 weeks | ✅ |
| SISA-20, each request | 0.023 | 0 weeks | ✅ |
| SISA-20, monthly | 0.019 | 3 weeks | ✅ |

**Newton updates.** Over 26 batches, the errors did **not** pile up (largest gap to an exact refit: 5.39 × 10⁻³; same
predictions on 100% of test images). But the Hessian grows with the square of the weights: 3.4 MB at 650 weights,
57.8 GB for the course MLP, 8 billion GB for a 1-billion-weight model.

**Proof.** After a year of SISA-20 batches, all 20 shard models were **bit-for-bit** equal to a fresh SISA model trained
without the 104 deleted users. Test accuracy after the year: 95.2%.

## Concepts used here

- [Unlearning at scale](../unlearning/unlearning-at-scale.md)
- [SISA, sharded training](../unlearning/sisa.md)
- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The enterprise playbook](../unlearning/enterprise-playbook.md)

## Quiz

```quiz
- q: At 10 million users, how much more does retraining per request cost than retraining every 4 weeks?
  options:
    - About 6 times
    - About 636 times
    - About 63,644 times
  answer: 2
  why: The bill for per-request retraining grows with the square of the service size.
- q: For K = 5 shards and a batch of 8 requests, about how many shards are touched?
  options:
    - 1
    - 4.2
    - 8
  answer: 1
  why: "5 × (1 − 0.8^8) ≈ 4.2, and real runs measured 4.33."
- q: Why does SISA-20 serve requests straight away rather than batching monthly?
  options:
    - Batching saves it little, and immediate service is still about 5 times cheaper than monthly retraining.
    - It cannot batch.
    - Batching breaks exactness.
  answer: 0
  why: A month's batch still touches about 7 of 20 shards, so requests share little work.
- q: Did the Newton step's errors pile up over the year?
  options:
    - No; each step also corrects the last.
    - Yes, badly.
  answer: 0
  why: Each step moves to the optimum of the data that is left, so the gap to an exact refit stayed tiny.
- q: After a year of deletions, how did SISA compare with a fresh SISA model without the deleted users?
  options:
    - Bit-for-bit equal
    - About 95% similar
    - Very different
  answer: 0
  why: SISA stays exact by construction, however many requests it serves.
```

## You have finished the course

Test yourself with the [final test](../quizzes/final.md) and the [practice problems](../practice.md). And keep asking
the course's first question about any new model: **what would make forgetting a subtraction, and how close can we get?**
