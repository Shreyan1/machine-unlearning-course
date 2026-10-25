---
title: The enterprise playbook
description: How a company turns a deletion request into a signed, re-verifiable certificate before the legal deadline.
---

# The enterprise playbook

!!! oneline "In one line"
    The playbook is a recipe for the **organisation**: find every model a request touches, pick the cheapest method with a good enough guarantee, prove it and sign it off before the deadline.

## Why it matters

A company does not receive "an unlearning problem". It receives a **request**: an email to the Data Protection Officer,
a contract termination, a security incident. Most unlearning failures in practice are not maths failures. They happen
because nobody knew which models had seen the data, there was no clean checkpoint or nobody owned the decision.

## A simple example

A hospital gets a request to remove a patient's records. Without a list of which systems use those records, staff would have to guess. Is it the booking system, the research database or the AI that predicts readmissions? A **lineage
registry** is that list, kept up to date for every model.

## How it works

<!-- diagram: enterprise-playbook -->

### The six parts

<ol class="steps" markdown>
<li markdown>**A lineage registry**: every model, adapter and checkpoint, with the data sources that reached it, directly or through a parent.</li>
<li markdown>**A decision procedure**: for each affected model, the cheapest method that gives an adequate guarantee.</li>
<li markdown>**A capacity plan** against legal deadlines (GDPR: one month; CCPA: 45 days).</li>
<li markdown>**An evidence record or certificate** that a third party can re-check.</li>
<li markdown>**Owners** for every threshold, such as the ML team, the DPO, legal, fairness and security.</li>
<li markdown>**An Unlearning pillar** in the Responsible AI Scorecard, so readiness is measured *before* a request arrives.</li>
</ol>

### Lineage reveals cascades

In Lesson 17, a contract request from "Southbank" affected not only its own data, but `support-base-v2` (which had been
improved with its data) and therefore **every adapter built on it**, including other banks' adapters. Without the
registry, nobody would have looked at them.

### Most deletions should be exact by design

| Artefact design | Method | Guarantee |
|---|---|---|
| Summation model (Naive Bayes, eigenfaces) | subtract | exact |
| SISA | retrain affected shards from checkpoints | exact by construction |
| Per-customer adapter | delete the adapter | exact |
| Fine-tune with a saved checkpoint | re-fine-tune from the checkpoint | exact by process |
| Legacy monolithic model | approximate method now, audited, **plus** a full retrain in the next cycle | approximate, then exact |

### Meeting the deadline

For 400 requests a month and a 3-day retrain (Lesson 17's placeholder numbers):

| Strategy | Monthly cost | Worst-case days | Meets 30 days? |
|---|---|---|---|
| Retrain per request | $4,800,000 | 3 | ✅ |
| Batch weekly | $51,429 | 10 | ✅ |
| Batch monthly | $12,000 | 33 | ❌ |
| SISA, user-aware | $240,000 | 0.2 | ✅ |

### The re-verifiable certificate

The strongest evidence is not "no test could tell the difference" but **"anyone can recompute it"**. With
**deterministic training** (fixed seeds) and a **hashed manifest** of exactly which rows went into each model, an
independent auditor can retrain from the manifest and check, bit for bit, that the deployed weights match. In Lesson 17
all four checks passed, and a model that kept the data would fail.

!!! note "Every threshold is a policy decision"
    The gold-band width, the privacy tolerance, the fairness tolerance and whether an interim approximate method is
    allowed all need a named owner. These are policy choices dressed up as technical settings.

## Common mistakes

!!! danger "Mistakes people make"
    - **No lineage registry.** Affected models get missed, especially through cascades.
    - **Approximate methods as the final answer.** Use them only as an interim step with a scheduled exact rebuild.
    - **Non-deterministic training.** Then the certificate cannot be re-verified, and you fall back to weaker evidence.
    - **Forgetting distilled models.** Distillation does not launder data; the teacher's knowledge transfers.

## Key takeaways

- Most unlearning failures are organisational.
- A lineage registry turns "what must be unlearnt?" into a lookup, and reveals cascades.
- Design so that most deletions are exact; use approximate methods only as a stopgap.
- The best certificate is re-verifiable, using deterministic training and hashed manifests.

## Quiz

```quiz
- q: What is a lineage registry?
  options:
    - A record of every model and the data that reached it
    - A list of employees
    - A backup of the training data
  answer: 0
  why: It turns "which models must be unlearnt?" into a lookup, including models built on affected parents.
- q: When is an approximate method acceptable in the playbook?
  options:
    - As an interim step, audited, with a scheduled exact rebuild
    - Always, as the final answer
    - Never
  answer: 0
  why: It can stop exposure quickly, while the next batch retrain provides the exact guarantee.
- q: Which batching schedule missed the 30-day deadline in Lesson 17?
  options:
    - Monthly batching
    - Weekly batching
    - Per-request retraining
  answer: 0
  why: Waiting up to a month and then adding the retrain time took 33 days.
- q: What makes a certificate re-verifiable?
  options:
    - Deterministic training and a hashed manifest of the rows used
    - A signature from the ML team
    - A high test accuracy
  answer: 0
  why: Anyone can retrain from the manifest and check that the weights match exactly.
- q: Does distilling a smaller model from a trained one remove the original data's influence?
  options:
    - No; the teacher's knowledge, including memorised examples, can transfer.
    - Yes, distillation launders the data.
  answer: 0
  why: Distilled models belong in the lineage registry as descendants of the teacher's data.
```

## Try it

- Back to: [Unlearning concepts](index.md).
- Lesson: [17 · The enterprise playbook](../lessons/17-enterprise-playbook.md).
