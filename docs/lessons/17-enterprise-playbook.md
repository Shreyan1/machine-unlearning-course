---
title: "Lesson 17 · The enterprise playbook"
description: From a deletion request to a signed, re-verifiable certificate, with a lineage registry, a decision procedure, a capacity plan and named owners.
---

# Lesson 17 · The enterprise playbook, from request to signed certificate

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 7 · Engineering</span><span class="chip" markdown="span">:material-stairs-up: Top of the ladder</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/17-Enterprise-Unlearning-Playbook.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/17-Enterprise-Unlearning-Playbook.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 45 minutes · 3 checkpoints"
    By the end of this lesson you can

    - find every model a request touches with a lineage registry, including models built on a contaminated parent,
    - choose a method for each model and a batching plan that meets a 30-day deadline,
    - issue a certificate that an independent auditor can recompute bit for bit.

## The story

A company does not receive "an unlearning problem". It receives a **request**, such as an email to the DPO, a ticket from legal,
a contract termination or a security incident. Someone must decide, before a legal deadline, which models are affected,
which method to use, how to prove it worked and who signs it off. This lesson turns the whole course into that process.

Lessons 01 to 16 each answered one question. They showed how to subtract from Naive Bayes, how to shard with SISA, how
to audit an approximate method and how to attack a language model. A real company has all of these models at once,
and four requests can land in the same week. If nobody knows which models saw the data, the best method in the world
is never run on the right model. If nobody can prove what was done, a regulator has only the company's word.

## What you will do

<ol class="steps" markdown>
<li markdown>Build a **lineage registry** for a fictional company's ten models.</li>
<li markdown>Run **four requests** that arrive in the same week, and find every affected model.</li>
<li markdown>Apply a **decision procedure** that picks the cheapest method with an adequate guarantee.</li>
<li markdown>Make a **capacity plan** against the 30-day deadline.</li>
<li markdown>Issue a **certificate**, and have an independent verifier re-derive it bit for bit.</li>
</ol>

## What each step teaches

**Step 1. The registry.** Each of the ten models records the data it was trained on directly and its parent models.
Lineage is inherited, so a short function can list every data source that reached a model. This turns "which models
must be unlearnt?" into a lookup.

**Step 2. Four requests.** An erasure, a contract end, an employee's erasure and a poisoning incident arrive between 5
and 8 October 2026. The lookup finds seven models to deal with. Two of them, the other banks' adapters, are easy to miss without it.

**Step 3. The decision procedure.** The course's ladder becomes one function. It first asks whether the data reached
the model directly or only through a parent, then whether the request is a poisoning case, and then lets the model's
design pick the method. Each answer comes with the guarantee and the evidence it needs.

??? deep "Go deeper · the methods each design gets"

    | Design | Method | Guarantee | Learn it in |
    |---|---|---|---|
    | Summation (Naive Bayes, eigenfaces) | Subtract the statistics or delete the templates | Exact by construction | Lessons 01 and 13 |
    | Newton (logistic regression) | Newton removal within the error budget, else retrain | Close to exact, with a certified gradient norm | Lessons 02 and 12 |
    | SISA | Retrain the affected shards from checkpoints | Exact by construction | Lesson 07 |
    | Per-tenant adapter | Delete the adapter | Exact by construction | Lesson 15 |
    | Checkpoint | Re-fine-tune from the checkpoint before the data entered | Exact by process | Lessons 15 and 16 |
    | None (legacy) | SCRUB+R or NPO now, full retrain in the next cycle | Approximate, audited | Lessons 09 and 11 |

    A model that got the data only through a parent is rebuilt on a clean parent. A poisoning case gets a behavioural
    guarantee, checked by the attack success rate, as in Lesson 14.

**Step 4. The capacity plan.** A placeholder legacy model takes 3 days and $12,000 to retrain, and 400 requests come
in a month. The step compares six schedules on cost and on the worst wait. It shows that the schedule, not the speed
of one retrain, decides whether the deadline is met.

**Step 5. The certificate.** `churn-net` is retrained for real on the course's lab, with Carol's 40 digits standing in
for customer #88231. The certificate records the recipe, a hashed manifest of the rows used and the weight hash. An
auditor then retrains from the manifest and compares hashes. The lesson ends with a table of owners and a proposed
Unlearning pillar for the RAI Scorecard.

## Key results

<div class="stats">
<div class="is-bad"><strong>3 models</strong><span>touched by Southbank's contract end, two through the base</span></div>
<div class="is-good"><strong>5 of 7</strong><span>model and request pairs got an exact method</span></div>
<div class="is-bad"><strong>33 days</strong><span>worst case for monthly batching, FAIL</span></div>
<div class="is-good"><strong>4 of 4</strong><span>verifier checks passed, bit for bit</span></div>
</div>

**Four requests, one week.**

| Request | Affects |
|---|---|
| REQ-101, erasure of customer #88231 | fraud-net, churn-net |
| REQ-102, contract end for Southbank | support-base-v2, **adapter-northbank, adapter-eastbank** |
| REQ-103, erasure of employee Dana R. | staff-assistant |
| REQ-104, poisoning incident | spam-filter |

REQ-102 triggers the Lesson 15 cascade. Southbank's data reached the base, which also affects the other banks' adapters.
Without the registry, nobody would have looked at them.

The other rows are simpler. REQ-101 touches two models trained on customer transactions. `fraud-net` was built with
SISA, so it retrains only the affected shards. `churn-net` is a legacy model with no design for deletion, so it is the
one pair in the week that needs an approximate method, audited, with a full retrain in the next batch. REQ-103 touches
the staff assistant, which is re-fine-tuned from the checkpoint before the HR directory entered. REQ-104 is a poisoning
case, so the spam filter is judged by its behaviour on triggered inputs.

??? checkpoint "Checkpoint 1 · Why are Northbank's and Eastbank's adapters rebuilt rather than deleted?"
    **Their own data is fine.** The decision procedure sees that Southbank's data reached them only through their
    parent, `support-base-v2`. Deleting an adapter is the method for a request about that adapter's own tenant. Here
    the fix is to rebuild the base without Southbank and then retrain each adapter on the clean base.

**Capacity plan** (400 requests a month, 3-day retrain, placeholder numbers).

| Strategy | Monthly cost | Worst case | Meets 30 days? |
|---|---|---|---|
| Retrain per request | $4,800,000 | 3 days | ✅ |
| Batch weekly | $51,429 | 10 days | ✅ |
| Batch monthly | $12,000 | 33 days | ❌ |
| SISA, user-aware | $240,000 | 0.2 days | ✅ |

Read the rows as a trade between cost and waiting. **Retraining per request** answers in 3 days but costs 400 retrains
a month. **Weekly batching** costs about 1% of that, and its worst case is 7 days of waiting plus 3 of retraining.
**Monthly batching** is the cheapest, but 30 + 3 = 33 days misses the deadline. **User-aware SISA** retrains about 5%
of the model per request, so it answers within hours. The notebook also prints fortnightly batching at $25,714 and 17
days, and SISA with a random partition at $2,928,000 and 1.8 days.

??? checkpoint "Checkpoint 2 · Requests go up to 800 a month and nothing else changes. What happens to the weekly batch?"
    **Its cost and its worst case stay the same.** A weekly batch is still about 4.3 retrains a month, so about
    $51,429, and the worst case is still 7 + 3 = 10 days. Each batch simply carries more requests. Retraining per
    request would double to 800 × $12,000 = $9,600,000. That is why batching scales and per-request retraining does not.

**The certificate** (UC-2026-0101) records the recipe, a hashed manifest of the rows used, the weight hash and the audit
results. An independent verifier checked four things. The manifest matches its hash ✅, deleted rows absent ✅, retrained weights equal
the certified weights bit for bit ✅, and a model that kept the data would fail ✅.

The certificate was completed on 15 October, ten days after the request and well before the deadline of 4 November.
Its audit section carries the Lesson 11 result for retraining on Carol, 62.5% against a band centred on 62.7%, with
every check passed. The recipe is 60 epochs, learning rate 0.001, batch size 64 and seed 2026. That seed is what lets
the verifier get the same weights again.

??? checkpoint "Checkpoint 3 · The verifier's fourth check trains a model on every row, Carol included, with the same seed. Why bother?"
    **To show the check can fail.** If a model that kept Carol also matched the certified hash, the check would prove
    nothing. Training on every row gives different weights and a different hash, so the check can tell a model that
    kept the data from one that did not. A test that cannot fail is not evidence.

**The Unlearning pillar.** On the proposed RAI Scorecard, the SISA fraud model scored 1.00 and stayed production-ready;
the legacy churn model (0.50) went to review; the contaminated base (0.05) was **blocked**, not because it was inaccurate
or unfair, but because the company could not honour a deletion request for it in time.

??? deep "Go deeper · the full scorecard and how the gate works"
    The book's scorecard combines pillars with a weighted harmonic mean. At 0.90 or more a model is production-ready,
    and below 0.70 it is blocked. Every model here scores 0.94 on the first four pillars.

    | Model | Unlearning | RAI, 5 pillars | Gate |
    |---|---|---|---|
    | `fraud-net` (SISA) | 1.00 | 0.95 | Production-ready |
    | `staff-assistant` (language model) | 0.85 | 0.92 | Production-ready |
    | `churn-net` (legacy) | 0.50 | 0.80 | RAI Council review |
    | `support-base-v2` | 0.05 | 0.21 | Blocked |

    The harmonic mean punishes one weak pillar. For the base, one over 0.05 is 20, while each of the other four terms
    is close to 1, so the five-pillar score falls to 0.21.

## Limits of this lesson

**Placeholder costs.** The $12,000 retrain, the 3 days and the 400 requests a month are illustrative. They show the
shape of the trade, not the bill of any real system.

**A toy registry.** Ten models written by hand. In production the registry lives in a model registry or data catalogue,
and it is only as good as its last update.

**One certificate executed.** Only REQ-101 on `churn-net` is run for real, on the course's digit lab. The other plans
are printed, not run.

**Determinism comes free here.** The course trains in NumPy, which is deterministic for a fixed seed. On GPUs the same
check needs deterministic kernels turned on.

**The pillar is proposed.** The rubric and its weights are the course's suggestion, not an agreed standard.

## Concepts used here

- [The enterprise playbook](../unlearning/enterprise-playbook.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)
- [Can a test prove forgetting?](../unlearning/testing-vs-proving.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)

## Notes to take

!!! notes "Notes to take"
    - **Organisational failures.** Unknown lineage, no clean checkpoint or no owner, not bad maths.
    - **Registry.** Lineage is inherited, so the lookup finds children of a contaminated parent.
    - **Cascade.** Southbank's contract end touched the base and both other banks' adapters, 3 models in all.
    - **Decision procedure.** Direct or through a parent, then poisoning or not, then the design picks the method.
    - **Exact by design.** 5 of 7 pairs exact. Only the legacy `churn-net` needed an approximate step.
    - **Deadline.** Worst case = batch window + retrain. Weekly 10 days passes, monthly 33 days fails.
    - **Certificate.** Recipe, hashed manifest and weight hash. All 4 verifier checks passed.
    - **Scorecard.** The base scored 0.05 on unlearning and was blocked at 0.21.

## Quiz

```quiz
- q: Why did the Southbank request affect Eastbank's adapter?
  options:
    - Southbank's data reached the shared base that Eastbank's adapter was built on.
    - Eastbank asked to be deleted.
    - Adapters share data by default.
  answer: 0
  why: Lineage is inherited, so a contaminated parent affects all its children.
- q: Which strategy missed the 30-day deadline?
  options:
    - Monthly batching
    - Weekly batching
    - SISA
  answer: 0
  why: Up to a month of waiting plus the retrain took 33 days.
- q: What makes the certificate re-verifiable?
  options:
    - Deterministic training plus a hashed manifest of the rows used
    - A signature from the ML team
    - High test accuracy
  answer: 0
  why: Anyone can retrain from the manifest and check the weights match exactly.
- q: Why was support-base-v2 blocked on the scorecard?
  options:
    - The company could not honour a deletion request for it in time with a guarantee.
    - It was inaccurate.
    - It was unfair.
  answer: 0
  why: Putting unlearning on the scorecard turns future legal risk into a present engineering task.
- q: Where do most unlearning failures in practice come from?
  options:
    - The organisation, such as unknown lineage or no owner
    - Bad maths
    - Slow computers
  answer: 0
  why: Usually nobody knew which models had seen the data, or nobody owned the decision.
- q: Which model in the week needed an approximate method?
  options:
    - fraud-net, because it uses SISA
    - churn-net, a legacy model with no design for deletion
    - spam-filter, because it is a Naive Bayes model
  answer: 1
  why: Every other model had an exact path by design. churn-net got an audited approximate step and a full retrain in the next batch.
- q: You retrain churn-net without a fixed seed. Which verifier check fails?
  options:
    - The manifest matches its hash
    - The deleted rows are not in the manifest
    - The retrained weights equal the certified weights bit for bit
  answer: 2
  why: Without a fixed seed, an honest retrain lands on different weights, so you fall back to the black-box audit of Lesson 11.
- q: Why does weekly batching meet the deadline while monthly batching does not?
  options:
    - The worst case is the batch window plus the 3-day retrain, so 10 days against 33.
    - Weekly retrains are faster.
    - Monthly batches carry too many requests to retrain.
  answer: 0
  why: A request that arrives just after a batch waits a full window, then waits for the retrain.
```

## Where to go from here

!!! levelup "Level up"
    You can now take a request from intake to a certificate an auditor can recompute. Next quest,
    [Lesson 18 · Recommender systems](18-recommender-systems.md), where one viewer's taste is spread across the links shown
    on every film's page.

You have climbed the whole ladder. When you meet a new kind of model, ask the course's first question. **What property
of this model would make forgetting a subtraction, and how close can we get to it?** Stage 8 takes the ideas further.

[On to Lesson 18, recommender systems :material-arrow-right:](18-recommender-systems.md){ .md-button }
