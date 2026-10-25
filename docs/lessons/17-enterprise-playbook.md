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

## The story

A company does not receive "an unlearning problem". It receives a **request**: an email to the DPO, a ticket from legal,
a contract termination, a security incident. Someone must decide, before a legal deadline, which models are affected,
which method to use, how to prove it worked and who signs it off. This lesson turns the whole course into that process.

## What you will do

<ol class="steps" markdown>
<li markdown>Build a **lineage registry** for a fictional company's ten models.</li>
<li markdown>Run **four requests** that arrive in the same week, and find every affected model.</li>
<li markdown>Apply a **decision procedure**: the cheapest method with an adequate guarantee.</li>
<li markdown>Make a **capacity plan** against the 30-day deadline.</li>
<li markdown>Issue a **certificate**, and have an independent verifier re-derive it bit for bit.</li>
</ol>

## Key results

**Four requests, one week.**

| Request | Affects |
|---|---|
| REQ-101, erasure of customer #88231 | fraud-net, churn-net |
| REQ-102, contract end for Southbank | support-base-v2, **adapter-northbank, adapter-eastbank** |
| REQ-103, erasure of employee Dana R. | staff-assistant |
| REQ-104, poisoning incident | spam-filter |

REQ-102 triggers the Lesson 15 cascade. Southbank's data reached the base, which also affects the other banks' adapters.
Without the registry, nobody would have looked at them.

**Capacity plan** (400 requests a month, 3-day retrain, placeholder numbers).

| Strategy | Monthly cost | Worst case | Meets 30 days? |
|---|---|---|---|
| Retrain per request | $4,800,000 | 3 days | ✅ |
| Batch weekly | $51,429 | 10 days | ✅ |
| Batch monthly | $12,000 | 33 days | ❌ |
| SISA, user-aware | $240,000 | 0.2 days | ✅ |

**The certificate** (UC-2026-0101) records the recipe, a hashed manifest of the rows used, the weight hash and the audit
results. An independent verifier checked four things. The manifest matches its hash ✅, deleted rows absent ✅, retrained weights equal
the certified weights bit for bit ✅, and a model that kept the data would fail ✅.

**The Unlearning pillar.** On the proposed RAI Scorecard, the SISA fraud model scored 1.00 and stayed production-ready;
the legacy churn model (0.50) went to review; the contaminated base (0.05) was **blocked**, not because it was inaccurate
or unfair, but because the company could not honour a deletion request for it in time.

## Concepts used here

- [The enterprise playbook](../unlearning/enterprise-playbook.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)
- [Can a test prove forgetting?](../unlearning/testing-vs-proving.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)

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
```

## Where to go from here

You have climbed the whole ladder. When you meet a new kind of model, ask the course's first question. **What property
of this model would make forgetting a subtraction, and how close can we get to it?** Stage 8 takes the ideas further.

[On to Lesson 18, recommender systems :material-arrow-right:](18-recommender-systems.md){ .md-button }
