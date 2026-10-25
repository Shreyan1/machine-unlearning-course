---
title: The unlearning audit
description: One pre-registered protocol with five checks, FORGET, PRIVACY, UTILITY, COST and RELEARN, run the same way on every method and written down as evidence.
---

# The unlearning audit

!!! oneline "In one line"
    An unlearning audit is an exam set **in advance**, with the same five checks for every method, marked against models
    that genuinely never saw the data, and written down so that someone else can check it.

## Why it matters

Each method so far marked its own homework, with its own table. A regulator, a review board or a customer needs
something better, which is one fair, repeatable protocol. The audit also adds a final check, the **relearn attack**, which
separates data that was truly *removed* from data that was only *hidden*.

## A simple example

A school exam is written before anyone sees the answers, the same paper is given to every student and it is marked
against an answer key. One question is a trick: "If I remind you of half of Carol's digits, how quickly do you remember
the other half?" A student who truly never learnt them will be slow. A student who was only pretending to forget will
answer at once.

## How it works

<figure class="figure" markdown>
![The audit pipeline: pre-register, build references with the same recipe, run five checks, write an evidence record](../assets/diagrams/09_audit_pipeline.png)
</figure>

<ol class="steps" markdown>
<li markdown>**Pre-register** every method's settings before running anything. In production you cannot tune against the gold band, so the audit must not either.</li>
<li markdown>**Build references** with the **same training recipe** as the system under audit. These are several models retrained without `D_f` (OUT) and some trained with it (IN).</li>
<li markdown>**Run five checks** on every method.</li>
<li markdown>**Use several kinds of request**, because a method that passes one can fail another.</li>
<li markdown>**Write an evidence record**: a machine-readable file with the protocol, the band, every number and every verdict.</li>
</ol>

### The five checks

| Check | Question | How |
|---|---|---|
| **FORGET** | Is forget-set accuracy inside the gold band? | mean ± max(2 std, 3 points) of the retrains |
| **PRIVACY** | Can a per-example attack still tell `D_f` was used? | U-LiRA member-rate, see [membership inference](membership-inference-attacks.md) |
| **UTILITY** | Is the model still useful? | test accuracy no more than 2 points below the retrains |
| **COST** | Is it cheaper than retraining? | count of example-gradients |
| **RELEARN** | Was it removed, or only hidden? (Deeb and Roger 2024) | show half of `D_f` again; count steps until the other half comes back |

### Three kinds of request

| Request | What is deleted | Real-world example |
|---|---|---|
| **carol** | 40 memorised examples from one person | a GDPR erasure request |
| **class** | every digit 3 | removing one person from a face-recognition model |
| **random** | a random 10% of training | a bulk retention purge |

### The first surprise: random requests fool accuracy

On the **random** request, the original model, which forgot *nothing*, **passed FORGET**. A model retrained without
those rows still gets about 98% on them, because they look like everything else. Only the PRIVACY check caught it.
Evaluations that use random forget sets and accuracy alone will happily certify a model that did nothing.

### The second surprise: the relearn attack

| Method | Steps to relearn the other half of Carol |
|---|---|
| Retrained references | 500 (the full budget, every time) |
| SCRUB+R | 20 |
| SCRUB | 18 |
| Bad Teacher | 13 |
| Original, fine-tune, gradient ascent | 0 |

SCRUB+R passed the first four checks on Carol. But shown 20 of her digits, it got the *other* 20 back within about 20
steps. Retrained models could not, because for them there was nothing to recall. That is **suppression**, not removal.

### Even exact methods can trip a check

SISA, which is exact by construction, failed FORGET on Carol by **one digit**: 52.5% against a band starting at about
52.6%. Nothing was wrong with SISA. A band estimated from 12 references on a 40-example set will sometimes reject a
perfectly good model. A FAIL is a reason to **investigate**, not an automatic verdict.

## In code

```python
from mul import audit
table = audit.audit(models, splits, retrained_refs, costs=costs, in_models=in_refs)
band_mean, band_std = audit.gold_band(retrained_refs, splits, in_models=in_refs)
print(audit.gate(table, band_mean, band_std))     # FORGET / PRIVACY / UTILITY / COST verdicts
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only random forget sets.** The original model can pass.
    - **References with a different recipe.** The verdict can be wrong, even backwards.
    - **Stopping at four checks.** Without RELEARN, suppression looks like success.
    - **Treating a pass as proof.** An audit is evidence. See [Can a test prove forgetting?](testing-vs-proving.md)

## Key takeaways

- Pre-register settings; build references with the same recipe; run five checks on several request types.
- Random forget sets fool accuracy-based audits; per-example privacy tests are needed.
- The relearn attack separates removed from suppressed.
- Write the result down as a machine-readable evidence record.

## Quiz

```quiz
- q: Why must method settings be fixed before the audit runs?
  options:
    - In production you cannot tune against the gold band, so the audit must not either.
    - It makes the audit faster.
    - The law lists the settings.
  answer: 0
  why: Tuning against the answer key would make every method look better than it really is.
- q: On the random request, the original model passed FORGET. Why?
  options:
    - Random rows look like everything else, so even a retrained model gets them right.
    - The original model had already forgotten them.
    - The test set was empty.
  answer: 0
  why: Accuracy cannot tell the difference. Only the per-example privacy check caught it.
- q: What does the relearn attack measure?
  options:
    - Whether forgotten data comes back quickly after a short reminder
    - How fast the model was originally trained
    - The test accuracy
  answer: 0
  why: Fast recovery means the knowledge was only hidden, not removed.
- q: SCRUB+R relearnt Carol in about 20 steps; retrained models needed 500. What does that mean?
  options:
    - SCRUB+R suppressed Carol rather than removing her.
    - SCRUB+R is better than retraining.
    - The attack is broken.
  answer: 0
  why: For a model that never saw her, there is nothing to recall, so relearning is slow.
- q: SISA failed FORGET on Carol by one digit. What is the right response?
  options:
    - Investigate; it is a statistical false alarm, and SISA's exactness can be checked from its logs.
    - Declare SISA broken.
    - Delete the audit.
  answer: 0
  why: Every statistical test has false alarms. A FAIL is a reason to look closer, not an automatic verdict.
```

## Try it

- Next concept: [Can a test prove forgetting?](testing-vs-proving.md).
- Lesson: [11 · The unlearning audit](../lessons/11-the-unlearning-audit.md).
