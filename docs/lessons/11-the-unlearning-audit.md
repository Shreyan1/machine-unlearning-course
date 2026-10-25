---
title: "Lesson 11: The unlearning audit"
description: One pre-registered protocol, five checks, three kinds of request, every method and a machine-readable evidence record.
---

# Lesson 11: The unlearning audit, one protocol for every method

<div class="chips"><span class="chip">⏱ ~45 min</span><span class="chip">Stage 5 · Proof</span><span class="chip">Rung 7</span></div>

<div class="buttons">
<a class="md-button md-button--primary" href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb">Open in Colab</a>
<a class="md-button" href="https://github.com/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb">View on GitHub</a>
</div>

## The story

So far each method has marked its own homework. An audit is an exam set **before** anyone knows the answers, with the
same questions for everybody, marked against models that genuinely never saw the data. One of the questions is a trick:
"If I remind you of half of Carol's digits, how quickly do you remember the other half?"

## What you will do

<ol class="steps" markdown>
<li markdown>**Pre-register** every method's settings, and build 12 OUT and 8 IN references per request, with the same recipe.</li>
<li markdown>**Show the issue**: audit the original model on three requests (Carol, the class "3", a random 10%).</li>
<li markdown>**Untrain** with every method from Lessons 06 to 10, the same way, on every request.</li>
<li markdown>Run five checks: **FORGET, PRIVACY, UTILITY, COST, RELEARN**.</li>
<li markdown>Audit SISA with its own references, and write an **evidence record**.</li>
</ol>

## Key results

**First surprise.** On the random request, the original model, which forgot nothing, **passed FORGET** (the band was
98.2% ± 1.6%). Only the per-example PRIVACY check caught it. Random forget sets and accuracy alone will certify a model
that did nothing.

**The relearn attack** on Carol (steps until the other half comes back):

| Model | Relearn steps |
|---|---|
| Retrained references | 500 (every one of 12) |
| NegGrad+ | 27 |
| SCRUB+R | 20 |
| SCRUB | 18 |
| Bad Teacher | 13 |
| Original, fine-tune, gradient ascent | 0 |

SCRUB+R passed FORGET, PRIVACY, UTILITY and COST on Carol, but relearnt her in 20 steps. That is **suppression**, not
removal. On the class request, everyone relearns 3s in under 10 steps, because "what a 3 looks like" is general
knowledge; the test measures memorised, specific information.

**SISA with its own references**: passed the class and random requests outright, but failed FORGET on Carol by **one
digit** (52.5% against a band starting near 52.6%). That is a statistical false alarm; SISA's exactness can be checked
from its logs.

| Method (default settings) | Carol | Class | Random |
|---|---|---|---|
| Fine-tune, gradient ascent, NegGrad+, Bad Teacher | ❌ | ❌ | ❌ |
| SCRUB | ❌ | ✅ | ❌ |
| SCRUB+R | ❌ (RELEARN) | ✅ | ❌ |
| SISA (own references) | ⚠️ false alarm | ✅ | ✅ |

!!! note "Evidence, not proof"
    Thudi et al. (2022) show that the same weights can be reached with or without an example. A black-box audit can show
    a method *failed*; a pass only means no test could tell the difference. Real guarantees come from the **process**.

## Concepts used here

- [The unlearning audit](../unlearning/unlearning-audit.md)
- [Can a test prove forgetting?](../unlearning/testing-vs-proving.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)
- [The gold band](../unlearning/gold-band.md)

## Quiz

```quiz
- q: On the random request, which check caught the original model that had forgotten nothing?
  options:
    - PRIVACY (U-LiRA)
    - FORGET
    - COST
  answer: 0
  why: Random rows look like everything else, so accuracy cannot tell the difference.
- q: How many steps did retrained references need to relearn Carol's other half?
  options:
    - 0
    - 20
    - 500, the full budget
  answer: 2
  why: For a model that never saw her, there is nothing to recall.
- q: SCRUB+R passed four checks on Carol. Why did it still fail?
  options:
    - It relearnt her in about 20 steps, so she was suppressed, not removed.
    - Its cost was too high.
    - It broke utility.
  answer: 0
  why: The relearn attack separates removal from suppression.
- q: Why can the relearn attack not separate methods on the class request?
  options:
    - Everyone, even retrained models, relearns 3s in a few steps.
    - There are no 3s in the data.
    - The class request is too small.
  answer: 0
  why: General knowledge about digits makes relearning a class fast for all models.
- q: SISA failed FORGET on Carol by one digit. What is the right reading?
  options:
    - A statistical false alarm worth investigating, not proof of failure
    - SISA does not work
    - The audit should be deleted
  answer: 0
  why: A band from 12 references on 40 examples will sometimes reject a good model.
```

## Open question → Lesson 12

Everything so far used 8 × 8 digits and an invented Carol. What happens on **real personal data**, when the people who
ask to be deleted are not a random sample?

[Next: Lesson 12, right to be forgotten and fairness](12-right-to-be-forgotten-and-fairness.md){ .md-button }
