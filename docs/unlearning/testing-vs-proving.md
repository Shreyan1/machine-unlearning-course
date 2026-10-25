---
title: Can a test prove forgetting?
description: Attacks and tests can show that a model still remembers, but they cannot prove it has forgotten. Only the deletion process gives a guarantee.
---

# Can a test prove forgetting?

!!! oneline "In one line"
    Tests can show that a model **still remembers**, but they can never **prove** that it has forgotten; only the
    deletion *process* (retraining, SISA, an exact update) gives a guarantee.

## Why it matters

It is tempting to say "our model passed the audit, so the data is gone". That claim goes too far. Knowing exactly what an
audit can and cannot show lets you make honest claims, choose the right method and avoid promising regulators more than
you can deliver.

## A simple example

A security guard checks bags at a door. If they find a knife, they have **proved** someone brought a knife. If they find
nothing, they have not proved there is no knife; it may be hidden somewhere they did not look. A better search reduces
the risk, but never makes it zero.

Unlearning tests work the same way. A failed test is proof of remembering. A passed test only means "no test we ran
could tell the difference".

## How it works

### What tests can do

- **Show failure**: if a membership attack can tell Carol's data was used, or the relearn attack brings her back quickly,
  the model still carries her influence.
- **Build confidence**: passing several strong, independent checks (gold band, per-example privacy, relearn) makes
  remaining influence less likely.

### What tests cannot do

- **Rule out stronger attacks.** An attack with AUC 0.5 today may be beaten by a cleverer attack tomorrow.
- **Look inside the weights.** Thudi, Jia, Shumailov and Papernot (2022) showed that the same final weights can be
  reached *with or without* a given example, a trick called **forging**. So an auditor who only sees the final weights
  can be fooled.
- **Avoid false alarms.** Statistical checks sometimes reject good models. In [Lesson 11](../lessons/11-the-unlearning-audit.md),
  exact SISA failed FORGET by one digit.

### Where guarantees come from

| Source of evidence | Guarantee? | Example |
|---|---|---|
| **Process**: retrain without the data | ✅ Yes, by definition | [Retraining](retraining-gold-standard.md) |
| **Process**: SISA with a logged partition | ✅ Yes, bit for bit | [SISA](sisa.md) |
| **Process**: exact classical update | ✅ Yes | [Subtracting counts, downdates](exact-unlearning-classical.md) |
| **Process**: delete a per-customer adapter | ✅ Yes | [Unlearning a fine-tune](unlearning-fine-tunes.md) |
| **Audit** of an approximate method | ❌ Evidence only | [SCRUB](scrub.md), [Bad Teacher](bad-teacher.md) |

That is why the course's playbook prefers **exact methods by design**, and treats approximate methods plus an audit as a
fallback.

!!! note "How to phrase a claim honestly"
    - Exact method: "The model was retrained without the data (or the shard was rebuilt from a logged checkpoint). The
      result is identical to a model that never saw it."
    - Approximate method: "We applied method X. Under pre-registered tests A, B and C, the model was indistinguishable
      from models retrained without the data. This is evidence, not a guarantee."

## Common mistakes

!!! danger "Mistakes people make"
    - **"It passed, so it is gone."** It passed *these* tests.
    - **Inspecting weights to prove forgetting.** Forging shows that weights alone cannot prove it.
    - **Treating every FAIL as final.** Investigate; false alarms happen, especially on small forget sets.

## Key takeaways

- A failed test proves remembering; a passed test does not prove forgetting.
- Weights alone cannot prove forgetting, because of forging.
- Real guarantees come from the deletion process, such as retraining, SISA, exact updates and deleting adapters.

## Quiz

```quiz
- q: A model fails a membership attack after unlearning. What does that show?
  options:
    - It still carries the data's influence.
    - It has fully forgotten.
    - Nothing at all.
  answer: 0
  why: If the attack can still tell the data was used, the model remembers. A failed test is real evidence.
- q: A model passes every test. What can you honestly say?
  options:
    - No test we ran could tell the difference.
    - The data is provably gone.
  answer: 0
  why: A stronger attack might still find something. Passing is evidence, not proof.
- q: What is "forging", from Thudi et al. (2022)?
  options:
    - Reaching the same final weights with or without a given example
    - Faking an audit report
    - Training a model twice
  answer: 0
  why: Because of forging, an auditor who sees only the final weights can be fooled.
- q: Which of these gives a real guarantee of forgetting?
  options:
    - SISA with a logged partition
    - SCRUB plus an audit
    - Bad Teacher's ZRF score
  answer: 0
  why: SISA's exactness comes from its process and can be checked from its logs.
```

## Try it

- Next concept: [Erasure requests and fairness](fairness-and-erasure.md).
- Lesson: [11 · The unlearning audit](../lessons/11-the-unlearning-audit.md).
