---
title: The enterprise playbook
description: How a company turns a deletion request into a signed, re-verifiable certificate before the legal deadline.
---

# The enterprise playbook

!!! oneline "In one line"
    The playbook is a recipe for the **organisation**. It finds every model a request touches, picks the cheapest method with a good enough guarantee, proves it and signs it off before the deadline.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - trace a request through a lineage registry and find every model it touches, including the hidden ones,
    - pick a method for each model and check whether a batching plan meets the legal deadline,
    - say what makes a certificate re-verifiable and why every threshold needs a named owner.

## Why it matters

A company does not receive "an unlearning problem". It receives a **request**, such as an email to the Data Protection Officer,
a contract termination or a security incident. Most unlearning failures in practice are not maths failures. They happen
because nobody knew which models had seen the data, there was no clean checkpoint or nobody owned the decision.

The clock starts when the request arrives. GDPR gives one month to respond and the CCPA gives
45 days. In that time someone has to find every
model, choose a method for each, run it, check it and sign.

Each earlier page answered one question, such as how SISA forgets. The playbook puts those answers in order.

## A simple example

A hospital gets a request to remove a patient's records. Without a list of which systems use those records, staff would have to guess. Is it the booking system, the research database or the AI that predicts readmissions? A **lineage
registry** is that list, kept up to date for every model.

!!! simply "Explain it simply"
    A library must remove every book a donor gave. A good library keeps a card for each book that says who gave it and
    which later books were copied from it. The librarian looks up the cards, removes the books and writes a receipt
    that anyone can check against the cards. Without the cards, the library can only guess.

Map it onto unlearning. The books are the company's models. The cards are the lineage registry. The copied books are
models built on top of other models. The receipt is the certificate.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Request | A reason the company must forget some data, with a deadline | REQ-101, the erasure of customer #88231 |
| [Lineage registry](../start-here/glossary.md#l) | A record of every model and every data source that reached it, directly or through a parent model | The ten models of a fictional company in Lesson 17 |
| Cascade | Data that reached a parent model also reaches every model built on it | Southbank's data reached `support-base-v2`, and so every bank's adapter |
| Exact by design | A model built so that forgetting is a subtraction, a deletion or a rebuild from a clean point | The SISA model `fraud-net` and the Naive Bayes spam filter |
| [Batching](../start-here/glossary.md#b) | Collecting requests and serving them together in one retrain | Retraining `churn-net` once a week |
| Manifest and hash | The exact list of rows that trained a model, sealed with a hash, a short fingerprint that changes if one bit changes | The retain rows of UC-2026-0101, with Carol's 40 left out |
| [Certificate](../start-here/glossary.md#c) | A record of what was done, how anyone can check it and who signed it | UC-2026-0101 in Lesson 17 |
| Unlearning pillar | A score of how ready a model is for a deletion request, measured before any request arrives | 1.00 for `fraud-net`, 0.05 for `support-base-v2` |

## How it works

<!-- diagram: enterprise-playbook -->

The figure shows one request in seven steps, from intake to close. The two green steps, Verify and Certify, produce
the evidence an auditor can check later. The bar underneath is the design rule that makes most requests cheap.

### The six parts

<ol class="steps" markdown>
<li markdown>**A lineage registry.** Every model, adapter and checkpoint, with the data sources that reached it, directly or through a parent.</li>
<li markdown>**A decision procedure.** For each affected model, the cheapest method that gives an adequate guarantee.</li>
<li markdown>**A capacity plan** against legal deadlines (one month under GDPR and 45 days under CCPA).</li>
<li markdown>**An evidence record or certificate** that a third party can re-check.</li>
<li markdown>**Owners** for every threshold, such as the ML team, the DPO, legal, fairness and security.</li>
<li markdown>**An Unlearning pillar** in the Responsible AI Scorecard, so readiness is measured *before* a request arrives.</li>
</ol>

The rest of this section follows the four requests that reach Lesson 17's fictional company in one week.

### Lineage reveals cascades

Each model in the registry records the data it was trained on directly and its parent models. Lineage is
**inherited**, so whatever reached a parent also reached all its children.

| Model | Trained directly on | Parent | All the data that reached it |
|---|---|---|---|
| `support-base-v1` | Public web | None | Public web |
| `support-base-v2` | Northbank and Southbank | `support-base-v1` | Public web, Northbank, Southbank |
| `adapter-northbank` | Northbank | `support-base-v2` | Public web, Northbank, Southbank |
| `adapter-eastbank` | Eastbank | `support-base-v2` | Public web, Eastbank, Northbank, Southbank |

Eastbank never shared anything with Southbank, yet its adapter carries Southbank's data through the base. Here is
what the registry found for each request.

| Request | What it is | Models it touches |
|---|---|---|
| REQ-101 | Erasure of customer #88231 | `fraud-net`, `churn-net` |
| REQ-102 | Contract end for Southbank | `support-base-v2`, `adapter-northbank`, `adapter-eastbank` |
| REQ-103 | Erasure of employee Dana R. | `staff-assistant` |
| REQ-104 | Poisoning incident SEC-77 | `spam-filter` |

In Lesson 17, a contract request from "Southbank" affected not only its own data, but `support-base-v2` (which had been
improved with its data) and therefore **every adapter built on it**, including other banks' adapters. Without the
registry, nobody would have looked at them.

??? checkpoint "Checkpoint 1 · A new model, churn-distilled, is trained only on churn-net's outputs and never sees customer data. Does REQ-101 touch it?"
    **Yes.** The registry lists `churn-net` as its parent, so it inherits `customers:transactions`. REQ-101 now
    touches three models, `fraud-net`, `churn-net` and `churn-distilled`. Distillation does not launder data, because
    the teacher's knowledge, including what it memorised, can pass to the student. The danger is a student that
    nobody registered, because then the lookup cannot find it.

### Most deletions should be exact by design

| Artefact design | Method | Guarantee |
|---|---|---|
| Summation model (Naive Bayes, eigenfaces) | Subtract | Exact |
| SISA | Retrain affected shards from checkpoints | Exact by construction |
| Per-customer adapter | Delete the adapter | Exact |
| Fine-tune with a saved checkpoint | Re-fine-tune from the checkpoint | Exact by process |
| Legacy monolithic model | Approximate method now, audited, **plus** a full retrain in the next cycle | Approximate, then exact |

Lesson 17 writes the course's ladder as one function that asks three questions in order.

1. **Did the data reach this model directly?** If it came only through a parent, rebuild on a clean parent and retrain
   this model on it. That is why the Northbank and Eastbank adapters are rebuilt, not deleted. Their own data is fine.
2. **Is this a poisoning incident?** Then remove the rows found, find the trigger and watch the attack success rate, as
   in Lesson 14. The guarantee is about behaviour, not about the data.
3. **Otherwise, how was the model built?** The design decides the method, as in the table above.

Of the seven model and request pairs that week, **five got an exact method**. Only `churn-net`, a legacy model with no
design for deletion, needed an approximate one. The spam filter's poisoning case got a behavioural check. The
approximate step is temporary, because the plan pairs it with a full retrain in the next batch.

??? deep "Go deeper · the full plan for the week, with the evidence each model needs"

    | Request | Model | Method | Guarantee | Evidence |
    |---|---|---|---|---|
    | REQ-101 | `fraud-net` | Retrain the affected SISA shards from checkpoints | Exact by construction | Partition log and shard hashes |
    | REQ-101 | `churn-net` | SCRUB+R or NPO now, full retrain in the next cycle | Approximate, audited | Lesson 11 audit (band, U-LiRA, relearn, fairness) |
    | REQ-102 | `support-base-v2` | Re-fine-tune from the checkpoint before the data entered | Exact by process | Manifest, seed and weight hash |
    | REQ-102 | `adapter-northbank` | Rebuild on the last clean parent, then retrain | Exact by process | Lineage record and rebuild logs |
    | REQ-102 | `adapter-eastbank` | Rebuild on the last clean parent, then retrain | Exact by process | Lineage record and rebuild logs |
    | REQ-103 | `staff-assistant` | Re-fine-tune from the checkpoint before the data entered | Exact by process | Manifest, seed and weight hash, plus the language-model attacks |
    | REQ-104 | `spam-filter` | Remove the rows found, find the trigger, remove at feature level | Behavioural | Attack success rate on held-out triggered inputs |

    Two rules add to the evidence. A language model such as `staff-assistant` also faces the attack battery of
    Lesson 16, which is exposure, prefix forcing and a relearn attack. A face model trained on badge photos also needs a
    do-not-enrol key that is not biometric, as in Lesson 13, so the person is not enrolled again.

### Meeting the deadline

For 400 requests a month and a 3-day retrain (Lesson 17's placeholder numbers).

| Strategy | Monthly cost | Worst-case days | Meets 30 days? |
|---|---|---|---|
| Retrain per request | $4,800,000 | 3 | ✅ |
| Batch weekly | $51,429 | 10 | ✅ |
| Batch every 2 weeks | $25,714 | 17 | ✅ |
| Batch monthly | $12,000 | 33 | ❌ |
| SISA, user-aware | $240,000 | 0.2 | ✅ |
| SISA, random partition | $2,928,000 | 1.8 | ✅ |

The worst case is a request that arrives just after a batch has started. It waits for the next batch, then for the
retrain itself. So a weekly batch has a worst case of 7 + 3 = 10 days, and a monthly batch 30 + 3 = 33 days, which is
past the deadline.

Batching weekly or fortnightly meets the deadline at about 1% of the cost of retraining for every request. User-aware
SISA costs more, but answers every request exactly within hours. An audited approximate method earns its place here.
Run it at once to stop the exposure, and let the next batch retrain provide the exact guarantee.

??? deep "Go deeper · where each number in the table comes from"
    Each full retrain of `churn-net` is a placeholder $12,000 and 3 days. The monthly cost is the number of retrains a
    month times $12,000.

    - **Retrain per request.** 400 retrains, so 400 × $12,000 = $4,800,000.
    - **Batch weekly.** About 30 ÷ 7 = 4.3 retrains a month, so about $51,429.
    - **Batch every 2 weeks.** About 30 ÷ 14 = 2.1 retrains, so about $25,714, with a worst case of 14 + 3 = 17 days.
    - **SISA, user-aware.** Each request retrains about 5% of the model, as in Lesson 07. That is 400 × 0.05 = 20
      retrains' worth, $240,000, and 0.05 × 3 = 0.15 days of work, which prints as 0.2.
    - **SISA, random partition.** Each request retrains about 61% of the model, so 400 × 0.61 = 244 retrains' worth,
      $2,928,000, and 0.61 × 3 = 1.8 days.

    The random partition is the warning in this table. SISA with users spread at random across shards costs more than
    half as much as retraining for every request. The saving comes from putting each user's rows in one shard.

??? checkpoint "Checkpoint 2 · The retrain takes 3 days and the deadline is 30. What is the longest batch window that still meets it?"
    **27 days.** The worst case is the window plus 3 days of retraining, and that must be at most 30, so the window
    can be at most 30 − 3 = 27 days. A monthly window is 3 days too long. In practice teams choose a much shorter
    window, because a failed retrain needs time to be run again. A weekly batch that fails once still finishes by day
    10 + 3 = 13.

### The re-verifiable certificate

The strongest evidence is not "no test could tell the difference" but **"anyone can recompute it"**. With
**deterministic training** (fixed seeds) and a **hashed manifest** of exactly which rows went into each model, an
independent auditor can retrain from the manifest and check, bit for bit, that the deployed weights match. In Lesson 17
all four checks passed, and a model that kept the data would fail.

Lesson 17 issues certificate UC-2026-0101 for REQ-101 on `churn-net`. Carol's 40 digits stand in for customer #88231.

- **What was asked.** REQ-101, received on 5 October 2026, due by 4 November and done on 15 October. The person is
  named only by a pseudonymous hash.
- **What was done.** A retrain from scratch in the weekly batch, after an interim SCRUB+R step audited under Lesson 11.
- **How to check it.** The recipe (60 epochs, learning rate 0.001, batch size 64, seed 2026), the manifest's hash, the
  40 rows removed and the weights' hash.
- **The audit and sign-off.** 62.5% on Carol against a band centred on 62.7%, every check passed, signed by the ML
  owner and the DPO.

An auditor who receives the certificate and the manifest, but not the deleted data, runs four checks.

| Check | What it proves |
|---|---|
| The manifest matches its hash | The list the auditor holds is the list that was certified |
| The deleted rows are not in the manifest | The 40 rows were really left out |
| Retrained weights equal the certified weights, bit for bit | The deployed model came from exactly that list and recipe |
| A model that kept the data would fail | The check can catch a cheat, since training on every row gives other weights |

This is the kind of evidence Thudi et al. (2022) argue unlearning claims need, a process anyone can check, not a test
on the final model alone.

??? deep "Go deeper · why determinism makes this work"
    The course trains its networks in NumPy, which gives exactly the same weights every time for the same seed and the
    same rows. So the model is a function of two things, the recipe and the manifest, and a function can be computed
    again by anyone. On GPUs, training is not deterministic by default. Fixed seeds are not enough, and the team must
    also turn on deterministic kernels with explicit flags.

    The certificate lists two residual risks. A black-box audit is evidence, not proof, so the guarantee rests on the
    process. Backups and logs that still hold the rows are handled by the data-retention procedure, under its own
    ticket, DR-5531. SISA, adapters and checkpoints extend the same idea to cheaper rebuilds, because each records
    exactly what it was built from.

??? checkpoint "Checkpoint 3 · Someone retrains churn-net with no fixed seed. Which of the four checks fails, and what evidence is left?"
    **The bit-for-bit check.** Without a fixed seed, an honest retrain lands on different weights every time, just as
    Lesson 06's retrains disagreed. The two manifest checks still pass, but the weights cannot be matched. You fall
    back to the black-box audit of Lesson 11 (the gold band, U-LiRA and the relearn attack), which is evidence, not
    proof.

### Owners for every number

!!! note "Every threshold is a policy decision"
    The gold-band width, the privacy tolerance, the fairness tolerance and whether an interim approximate method is
    allowed all need a named owner. These are policy choices dressed up as technical settings.

Lesson 17 gives each decision one accountable owner, who signs and answers for it. The DPO owns the band width, the
privacy tolerance, whether an interim approximate method is allowed and the certificate sign-off. Security and
platform own the registry's completeness, the method choice and the poisoning threshold. The fairness team owns the
fairness tolerance. ML engineering does most of the work but signs off none of the policy.

### The Unlearning pillar

The Responsible AI Scorecard from the course's book rates every model on four pillars, which are fairness,
explainability, robustness and data provenance. It gates deployment on their **weighted harmonic mean**, a kind of
average that one weak score drags down hard. At 0.90 or more a model is production-ready, and below 0.70 it is
blocked. Lesson 17 proposes a fifth pillar, unlearning readiness, scored before any request arrives.

| Model | Unlearning | RAI, 4 pillars | RAI, 5 pillars | Gate |
|---|---|---|---|---|
| `fraud-net` (SISA) | 1.00 | 0.94 | 0.95 | Production-ready |
| `staff-assistant` (language model) | 0.85 | 0.94 | 0.92 | Production-ready |
| `churn-net` (legacy) | 0.50 | 0.94 | 0.80 | RAI Council review |
| `support-base-v2` | 0.05 | 0.94 | 0.21 | **Blocked** |

All four models score the same 0.94 on the first four pillars. The contaminated base is blocked not because it is
inaccurate or unfair, but because the company could not honour a deletion request for it in time. Putting unlearning
on the scorecard turns a future legal risk into a present engineering task.

??? deep "Go deeper · the rubric and the harmonic mean"
    The unlearning score adds up the weights of the criteria a model meets.

    | Criterion | Weight |
    |---|---|
    | Every training source and parent is registered | 0.20 |
    | An exact path exists that fits the deadline | 0.25 |
    | Deterministic training and hashed manifests | 0.15 |
    | The audit is automated for approximate paths | 0.15 |
    | Fairness is monitored across the deletion log | 0.10 |
    | A re-ingestion block exists | 0.10 |
    | Backups and logs are covered by the retention procedure | 0.05 |

    `churn-net` meets the first, the fourth, the fifth and the last, so it scores 0.20 + 0.15 + 0.10 + 0.05 = 0.50.
    `support-base-v2` meets only the last, so it scores 0.05.

    The book's example pillars are 0.92, 1.0, 0.87 and 1.0. With equal weights the harmonic mean is the number of
    pillars divided by the sum of one over each score. For `support-base-v2` that is
    \(5 \div (1/0.92 + 1/1.0 + 1/0.87 + 1/1.0 + 1/0.05) = 5 \div 24.24 \approx 0.21\). The single term \(1/0.05 = 20\)
    swamps the other four, which is the point. A model cannot hide a missing pillar behind good ones.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>3 models</strong><span>touched by one contract request, two through the base</span></div>
<div class="is-good"><strong>5 of 7</strong><span>model and request pairs exact by design</span></div>
<div class="is-bad"><strong>33 days</strong><span>worst case for monthly batching, misses the deadline</span></div>
<div class="is-good"><strong>4 of 4</strong><span>verifier checks passed for certificate UC-2026-0101</span></div>
</div>

None of these results needs a clever algorithm. Each comes from a record the company kept, a design it chose before
training or a schedule it planned. The maths of the earlier lessons only helps if the organisation can find the
models, reach a clean point and prove what it did.

## Limits

**The costs are placeholders.** The $12,000 retrain, the 3 days and the 400 requests a month are illustrative. Put in
your own numbers before you choose a schedule.

**The registry is small and written by hand.** A real company has many more models, and the lookup is only as good
as the registry's last update.

**Determinism is harder on real hardware.** On GPUs the bit-for-bit check needs deterministic kernels. Without them
you fall back to the weaker black-box audit.

**The certificate covers the model, not every copy.** Backups, logs, vector stores and caches can still hold the data.
They need their own procedure, which the next page covers for retrieval systems.

**The pillar is a proposal.** The rubric's weights are the course's suggestion, not a standard.

!!! tip "What to do in practice"
    - Keep a lineage registry with every model's direct data and parents, and update it whenever a model is trained.
    - Prefer designs where deletion is exact, such as summation models, SISA with user-aware shards, per-customer
      adapters and saved checkpoints.
    - Choose a batch window that leaves room for a failed retrain inside the deadline.
    - Use an approximate method only as an audited interim step, with the exact rebuild already scheduled.
    - Train deterministically and hash a manifest for every model, so a certificate can be recomputed.
    - Name an accountable owner for every threshold before the first request arrives.

## Common mistakes

!!! danger "Mistakes people make"
    - **No lineage registry.** Affected models get missed, especially through cascades.
    - **Approximate methods as the final answer.** Use them only as an interim step with a scheduled exact rebuild.
    - **Non-deterministic training.** Then the certificate cannot be re-verified, and you fall back to weaker evidence.
    - **Forgetting distilled models.** Distillation does not launder data; the teacher's knowledge transfers.
    - **Batching to the edge of the deadline.** A monthly batch against a one-month deadline was 3 days late in
      Lesson 17, before any failed run.

## Key takeaways

!!! notes "Notes to take"
    - **Organisational first.** Most unlearning failures come from unknown lineage, no clean checkpoint or no owner.
    - **Lineage registry.** Turns "what must be unlearnt?" into a lookup. Lineage is inherited by every child model.
    - **Cascade.** Southbank's contract end touched 3 models, including Northbank's and Eastbank's adapters.
    - **Exact by design.** 5 of 7 pairs in Lesson 17 were exact. Approximate only for the legacy `churn-net`.
    - **Deadline rule.** Worst case = batch window + retrain time. Weekly 10 days passes, monthly 33 days fails.
    - **Cost.** Weekly batching costs about 1% of retraining per request. User-aware SISA answers within hours.
    - **Certificate.** Deterministic training and a hashed manifest let anyone recompute the model bit for bit.
    - **Owners.** Every threshold is a policy choice. The DPO signs most of them, including the certificate.
    - **Unlearning pillar.** Scored before requests. A base at 0.05 drags the RAI score to 0.21 and is blocked.

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
- q: Southbank's contract ended. Why are the Northbank and Eastbank adapters rebuilt rather than deleted?
  options:
    - They were trained directly on Southbank's data.
    - Their own data is fine, and only the base under them carries Southbank's data.
    - Adapters can never be deleted.
  answer: 1
  why: The decision procedure sees that the data reached them only through a parent, so it rebuilds them on a clean base.
- q: A batch retrain takes 3 days and the deadline is 30 days. What is the longest batch window that still meets it?
  options:
    - 30 days
    - 33 days
    - 27 days
  answer: 2
  why: The worst case is the window plus the retrain, so the window can be at most 30 − 3 = 27 days.
- q: Every model scored 0.94 on the first four pillars, yet support-base-v2 scored 0.21 with the Unlearning pillar added. Why?
  options:
    - Its accuracy dropped when the pillar was added.
    - The scorecard uses a harmonic mean, so one very weak pillar drags the whole score down.
    - The other four pillars were scored again.
  answer: 1
  why: Its unlearning score was 0.05, and one over 0.05 is 20, which swamps the other four pillars.
```

## Try it

!!! levelup "Level up"
    You can now take a request from intake to a signed certificate, find every model it touches and check a schedule
    against the deadline. Next quest, [RAG, vector stores and caches](rag-and-vector-stores.md), where the copies a
    certificate misses are hunted down one by one.

- Go back to [Unlearning concepts](index.md).
- Run the lesson [17 · The enterprise playbook](../lessons/17-enterprise-playbook.md).
- In the notebook, add `churn-distilled` to the registry and check what REQ-101 touches now.
- Change the request rate to 5,000 a month and the retrain to 10 days. Which strategies still meet the deadline?
