---
title: "Lesson 20 · Unlearning at scale"
description: A year of deletion requests. The bill for per-request retraining grows with the square of the service, SISA stays exact and Newton updates do not fit deep models.
---

# Lesson 20 · Unlearning at scale, a year of deletion requests

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 8 · Extensions</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/20-Unlearning-at-Scale.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/20-Unlearning-at-Scale.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 40 minutes · 2 checkpoints"
    By the end of this lesson you can

    - show why retraining for every request stops working as a service grows,
    - predict SISA's cost under a batch of requests with one formula, and check it against real runs,
    - choose a way to serve a year of requests for a linear model, a small network and a large one.

## The story

Lesson 07 removed one request with SISA; Lesson 17 planned capacity. Real services get a steady stream of requests,
every week, for years. The digit service here gets **2 requests a week**, or 104 in a year (8.3% of users), each with a
one-month deadline.

A small café can repaint the whole shop each time a customer complains about one wall. A chain of a thousand cafés
cannot. The same is true of retraining. For the course's 1,257 users a full retrain per request is cheap. For a service
of millions it would be ruinous, and if the team falls behind, people wait past the legal deadline. This lesson runs a
whole year for real and asks which way of reaching the retrained model a service can afford.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the service in three ways, as one model, as SISA with 5 shards and as SISA with 20 shards.</li>
<li markdown>**Show the issue.** How the bill for per-request retraining grows with service size.</li>
<li markdown>**Untrain** under a stream of requests, and check SISA's shards-touched formula against real runs.</li>
<li markdown>**Show the result.** A whole year with four strategies, and the cost of exact Newton updates.</li>
<li markdown>**Prove it.** After a year, is SISA still bit-for-bit exact?</li>
</ol>

## What each step teaches

**Step 1. Three versions of the service.** One model scores 98.0% on the 540 test images, SISA with 5 shards also
98.0% and SISA with 20 shards 95.6%. Cost is counted in example-gradients, one training example passed through the
model once. One full retrain of the one model is 75,420 of them.

**Step 2. The square law.** A service twice as big pays twice as much per retrain and gets twice as many requests. The
step scales the service from 1,000 to 10 million users and compares retraining for each request with retraining every
4 weeks. It teaches that a method's cost for one request says little about its cost for a year.

**Step 3. SISA under batches.** A formula predicts how many shards a batch of random requests will touch, and real runs
check it. Then the number of shards is varied from 1 to 40, to show what cheaper deletes cost in accuracy.

??? deep "Go deeper · the shards-touched formula"
    Each request lands in a given shard with chance \(1/K\), so all \(b\) requests miss it with chance
    \((1 - 1/K)^b\). The expected number of shards touched is

    \[
    K\left(1 - \left(1 - \tfrac{1}{K}\right)^{b}\right)
    \]

    For \(K = 20\) and a month's batch of 8, that is \(20 \times (1 - 0.95^8)\), about 6.73. The runs touched 7.33.
    The real cost of a batch is a little below the share of shards touched, because a request in a shard's last slice
    only replays that slice.

**Step 4. A year and a policy.** Four strategies run on the same 104 requests. Then the step tests exact Newton removal
for logistic regression over 26 batches and measures how the Hessian grows. It ends with a policy table, one row per
kind of model.

**Step 5. The proof.** A fresh SISA model is trained on the users who are left, and every weight is compared with the
model that served the year. Cheap only counts if it is still exact.

## Key results

<div class="stats">
<div class="is-bad"><strong>63,644 ×</strong><span>per-request retraining against monthly, at 10 million users</span></div>
<div class="is-good"><strong>0.023</strong><span>SISA-20 serving each request at once, against retraining each</span></div>
<div class="is-good"><strong>20 of 20</strong><span>shard models bit for bit equal after a year</span></div>
<div class="is-bad"><strong>57.8 GB</strong><span>Hessian of the course network at 8 bytes per number</span></div>
</div>

**The square law.** Retraining for every request instead of every 4 weeks is 6 × more expensive at 1,000 users, 636 × at
100,000 and 63,644 × at 10 million.

The ratio is simply the number of requests a year divided by 13, the number of monthly retrains. At 10 million users,
8.3% leaving is about 827,000 requests, and 827,000 ÷ 13 is about 63,600. Each tenfold growth multiplies it by 10.

**SISA under batches.** The expected number of shards touched is \(K(1 - (1 - 1/K)^b)\). For K = 5 and b = 8, about 4.2 of 5. The formula
matched real runs (4.33 measured). More shards help, at a price.

| Shards | Test accuracy | One request | One month's batch |
|---|---|---|---|
| 1 | 97.8% | 1.000 | 1.000 |
| 20 | 95.6% | 0.050 | 0.337 |
| 40 | 92.8% | 0.025 | 0.183 |

Read the rows from top to bottom. One shard is plain retraining, so every request costs a full retrain. With 20 shards
one request costs a twentieth of a retrain, but a month's batch touches about 7 of them, a third, and a measured batch of 8 cost 0.24. With 40
shards deletes are cheaper again, but each shard model sees only 31 users, and accuracy falls to 92.8%.

??? checkpoint "Checkpoint 1 · With 5 shards, a month's batch of 8 touched 4.33 of the 5 shards and cost 0.73 of a retrain. Is batching a good deal for SISA-5?"
    **Not much of one.** One request alone cost 0.14 in the runs, so serving the 8 one at a time would cost about
    8 × 0.14 = 1.1 retrains. Batching saves about a third. But the batch still costs almost three quarters of a
    retrain, and people wait.
    With 20 shards the same batch costs 0.337, so more shards do far more than batching.

**A whole year.**

| Strategy | Cost vs retrain-each | Longest wait | In deadline? |
|---|---|---|---|
| Retrain each request | 1.000 | 0 weeks | ✅ |
| Retrain monthly | 0.125 | 3 weeks | ✅ |
| SISA-20, each request | 0.023 | 0 weeks | ✅ |
| SISA-20, monthly | 0.019 | 3 weeks | ✅ |

Each row says something different. **Retrain each** is the gold standard done naively, 104 retrains. **Retrain monthly**
is 13 retrains, so 13 ÷ 104 = 0.125 of the bill, but some people wait 3 weeks. **SISA-20 at once** costs 0.023 and
nobody waits, about 5 times cheaper than monthly retraining. **SISA-20 monthly** saves only a further 0.004, because a
month's batch of 8 still touches about 7 of the 20 shards.

**Newton updates.** Over 26 batches, the errors did **not** pile up. The largest gap to an exact refit was 5.39 × 10⁻³,
and predictions matched on 100% of test images. The Hessian grows with the square of the weights. It takes 3.4 MB at
650 weights, 57.8 GB for the course MLP and 8 billion GB for a 1-billion-weight model. These sizes use 64-bit floats,
which is why Lesson 08 gives half as much (29 GB) for the same MLP.

Each Newton step starts from the current weights and moves to the best weights for the data that is left, so it also
corrects what earlier steps missed. The catch is certified removal's noise budget. Each removal uses part of it, and
the running total reached 0.527 over the year. When it is spent, a full retrain is due.

??? deep "Go deeper · how a Newton step grows with the model"

    | Weights | Hessian (8 bytes per number) | One Newton step |
    |---|---|---|
    | 650 | 3.4 MB | 0.006 s |
    | 1,290 | 13.3 MB | 0.021 s |
    | 2,570 | 52.8 MB | 0.106 s |
    | 3,850 | 118.6 MB | 0.275 s |

    Double the weights and the Hessian needs four times the memory, and one step took about 3.5 to 5 times
    longer in these runs. For the 85,002-weight course network the Hessian would be 57.8 GB at 8 bytes per number, or 28.9 GB at 4.

**Proof.** After a year of SISA-20 batches, all 20 shard models were **bit-for-bit** equal to a fresh SISA model trained
without the 104 deleted users. Test accuracy after the year was 95.2%.

??? checkpoint "Checkpoint 2 · A team runs a large network and must serve requests within a month. Which row of the policy would you pick, and what does it cost?"
    **SISA with many shards, serving requests as they arrive.** In this lesson SISA-20 cost 0.023 of retraining for each
    request and nobody waited. The price is accuracy, 95.6% against 98.0% for one model, which a larger service with
    more data per shard would feel less. Newton removal is out, because the Hessian alone would not fit.

## Limits of this lesson

**Random leavers.** The 104 users are picked at random. If a whole region or customer leaves at once, the shards touched
could be very different. The notebook's open question points to user-aware partitions from Lesson 07.

**A small service.** With 1,257 users, SISA-20 has only 62 per shard, so it loses more accuracy than a big service
would.

**One unit of cost.** Example-gradients count training work only. They leave out checking requests and running audits.

**No budget size.** The lesson tracks how much of the noise budget is used but does not fix its size, so it does not say
when the retrain falls due.

## Concepts used here

- [Unlearning at scale](../unlearning/unlearning-at-scale.md)
- [SISA, sharded training](../unlearning/sisa.md)
- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The enterprise playbook](../unlearning/enterprise-playbook.md)

## Notes to take

!!! notes "Notes to take"
    - **The stream.** 2 requests a week, 104 a year, 8.3% of 1,257 users, each with a one-month deadline.
    - **The square law.** Per-request retraining against monthly is 6 × at 1,000 users and 63,644 × at 10 million.
    - **Shards touched.** \(K(1 - (1 - 1/K)^b)\). 4.2 of 5 for a batch of 8, measured 4.33.
    - **Shards cost accuracy.** 97.8% with 1 shard, 95.6% with 20, 92.8% with 40.
    - **The year.** Retrain monthly 0.125, SISA-20 at once 0.023, SISA-20 monthly 0.019. All inside the deadline.
    - **Newton removal.** Errors do not pile up, gap 5.39 × 10⁻³, but the noise budget forces a scheduled retrain.
    - **Hessian.** 57.8 GB at 8 bytes per number for the course network, 28.9 GB at 4.
    - **Proof.** All 20 SISA shard models bit for bit equal to a fresh model after the year.

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
- q: Why does batching cut plain retraining's bill by 8 times but SISA-20's by much less?
  options:
    - SISA cannot batch requests.
    - A monthly retrain carries all 8 requests at once, while a SISA batch of 8 still touches about 7 of 20 shards.
    - Batching makes the one model smaller.
  answer: 1
  why: Retrain monthly fell from 1.000 to 0.125, while SISA-20 fell only from 0.023 to 0.019.
- q: Why not use 40 shards for every service?
  options:
    - Each shard model sees less data, and accuracy fell to 92.8% with 40 shards here.
    - 40 shards break exactness.
    - The formula stops working above 20 shards.
  answer: 0
  why: Cheaper deletes cost accuracy. Measure both before choosing the number of shards.
- q: The course network's Hessian is quoted as 57.8 GB here and 29 GB in Lesson 08. Why?
  options:
    - The network grew between the lessons.
    - One of the numbers is a mistake.
    - This lesson stores 8 bytes per number and Lesson 08 stores 4.
  answer: 2
  why: 85,002 × 85,002 numbers take 28.9 GB at 4 bytes each and 57.8 GB at 8.
```

## Want to go further?

!!! levelup "Level up"
    You can now price a year of deletion requests and match a method to the size of a model. Next quest,
    [Lesson 21 · RAG and vector stores](21-rag-and-vector-stores.md), where the data lives in a store, not in weights.

Every model in this lesson learned its data into weights. Many chatbots instead look their data up at answer time, in
a vector store. Lesson 21 asks whether forgetting is then as easy as deleting rows, and finds every copy that a
deletion can miss.

[On to Lesson 21, RAG and vector stores :material-arrow-right:](21-rag-and-vector-stores.md){ .md-button }
