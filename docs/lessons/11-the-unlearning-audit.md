---
title: "Lesson 11 · The unlearning audit"
description: One pre-registered protocol, five checks, three kinds of request, every method and a machine-readable evidence record.
---

# Lesson 11 · The unlearning audit, one protocol for every method

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 5 · Proof</span><span class="chip" markdown="span">:material-stairs-up: Rung 7</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 45 minutes · 3 checkpoints"
    By the end of this lesson you can

    - run every method through one pre-registered protocol of five checks on three kinds of request,
    - explain why a random forget set lets a model that forgot nothing pass on accuracy,
    - use the relearn attack to tell removal from suppression, and read a FAIL as a reason to investigate.

## The story

So far each method has marked its own homework. An audit is an exam set **before** anyone knows the answers, with the
same questions for everybody, marked against models that genuinely never saw the data. One of the questions is a trick.
"If I remind you of half of Carol's digits, how quickly do you remember the other half?"

Lessons 06 to 10 built the pieces one at a time, a gold band, a privacy test, a utility check and a cost count. Lesson
10 also showed that a method's own metric can rank it above a true retrain. Now the pieces become one protocol, the kind
a regulator or an internal review board would ask for. SCRUB+R looked like the winner on three checks. This lesson
asks whether it survives a fifth.

## What you will do

<ol class="steps" markdown>
<li markdown>**Pre-register** every method's settings, and build 12 OUT and 8 IN references per request, with the same recipe.</li>
<li markdown>**Show the issue.** Audit the original model on three requests (Carol, the class "3", a random 10%).</li>
<li markdown>**Untrain** with every method from Lessons 06 to 10, the same way, on every request.</li>
<li markdown>Run the five checks, **FORGET, PRIVACY, UTILITY, COST and RELEARN**.</li>
<li markdown>Audit SISA with its own references, and write an **evidence record**.</li>
</ol>

## What each step teaches

**Step 1. Pre-register.** The notebook prints the protocol before any method runs. It fixes the number of references,
the gate's tolerances, the relearn settings and each method's default settings. It uses defaults, not the best runs from
Lessons 08 to 10, because picking the best run needs the gold band, which production never has.

**Step 2. Audit the original.** The original model forgot nothing, so it should fail every request. Checking that
first tests the audit itself.

**Step 3. Every method, every request.** Fine-tune, gradient ascent, NegGrad+, SCRUB, SCRUB+R and Bad Teacher are run
with their pre-registered settings, beside the original and a new retrain with seed 999.

**Step 4. The five checks.** Each run gets a PASS or FAIL on each check, and a verdict map shows which check each method
fails on which request.

??? deep "Go deeper · step 5, the relearn attack, SISA and the record"
    **The relearn attack.** Each model is fine-tuned on the first 20 of Carol's digits, with a learning rate of 0.001
    and batches of 16. The count stops when it gets the other 20 right 95% as often as the original did, or at 500
    steps. A model passes if it holds out for at least half the retrained references' median.

    **SISA.** SISA is audited against 12 OUT and 8 IN references trained with the SISA recipe of 5 shards and 4
    slices, because Lesson 07 showed that references with a different recipe give a wrong verdict.

    **The evidence record.** Every number and verdict is saved in `audit_carol.json`, `audit_class.json` and
    `audit_random.json`, which Lesson 17 turns into a certificate.

## Key results

<div class="stats">
<div class="is-bad"><strong>98.2% ± 1.6%</strong><span>the random request's band, the original passed FORGET</span></div>
<div class="is-good"><strong>500 steps</strong><span>for every retrain to relearn Carol</span></div>
<div class="is-bad"><strong>20 steps</strong><span>for SCRUB+R, after passing four checks</span></div>
<div><strong>52.5%</strong><span>exact SISA on Carol, one digit under the band</span></div>
</div>

**First surprise.** On the random request, the original model, which forgot nothing, **passed FORGET** (the band was
98.2% ± 1.6%). Only the per-example PRIVACY check caught it. Random forget sets and accuracy alone will certify a model
that did nothing.

The other two requests behaved as expected. On Carol the band was 62.7% ± 9.5% and the original scored 100.0%. On the
class it was 0.0% ± 0.0% and the original scored 100.0%. Both failed FORGET. On the random rows, a model retrained
without them still gets about 98% right, because they look like everything else. U-LiRA could still tell the
difference, with 0.712 for the original against 0.360 for a retrain. This is the central warning of Hayes et al. (2024).

??? checkpoint "Checkpoint 1 · An audit uses only random forget sets and accuracy. The original model passes. What should you add?"
    **A per-example privacy test and at least one hard request.** U-LiRA caught the original on the random rows, at
    0.712 against 0.360 for a retrain. A memorised person such as Carol, or a whole class, gives a band the original
    cannot hide in, since it scored 100.0% against bands of 62.7% and 0.0%.

**The relearn attack** on Carol (steps until the other half comes back).

| Model | Relearn steps |
|---|---|
| Retrained references | 500 (every one of 12) |
| NegGrad+ | 27 |
| SCRUB+R | 20 |
| SCRUB | 18 |
| Bad Teacher | 13 |
| Original, fine-tune, gradient ascent | 0 |

SCRUB+R passed FORGET, PRIVACY, UTILITY and COST on Carol, but relearnt her in 20 steps. That is **suppression**, not
removal. On the class request, even the retrained references relearn 3s in under 10 steps, because "what a 3 looks
like" is general knowledge; the test measures memorised, specific information.

Read the table from the bottom. **Zero steps** means the model already gets Carol's other half right, because it never
forgot her. **13 to 27 steps** means the methods that moved her accuracy down still hold what they learnt from her, so
a short reminder brings it back. **500 steps** is the full budget, and every retrain used all of it, because a model
that never saw Carol has nothing to recall. The pass mark is half the retrains' median, which is 250 steps.
No approximate method came close.

??? checkpoint "Checkpoint 2 · On the class request the retrains' median is 9 steps. SCRUB+R took 9 and fine-tune took 1. Which passes RELEARN?"
    **SCRUB+R passes and fine-tune fails.** The pass mark is half the median, 0.5 × 9 = 4.5 steps. SCRUB+R's 9 is above
    it. Fine-tune's 1 is below, and it had not forgotten the 3s anyway, at 93.0% accuracy on them. With a bar this low,
    the attack separates very little on a class.

**SISA with its own references.** Passed the class and random requests outright, but failed FORGET on Carol by **one
digit** (52.5% against a band starting near 52.6%). That is a statistical false alarm; SISA's exactness can be checked
from its logs.

52.5% is 21 of Carol's 40 digits. SISA passed PRIVACY and UTILITY on all three requests. Its RELEARN result is "n/a",
because the attack fine-tunes one network and SISA is an ensemble of five. It does not need the test, since after
unlearning it is the same as a SISA system trained without Carol. Its weak spot is COST, at about 61% of a retrain on
Carol, because a random partition spreads one request across most shards.

| Method (default settings) | Carol | Class | Random |
|---|---|---|---|
| Fine-tune, gradient ascent, NegGrad+, Bad Teacher | ❌ | ❌ | ❌ |
| SCRUB | ❌ | ✅ | ❌ |
| SCRUB+R | ❌ (RELEARN) | ✅ | ❌ |
| SISA (own references) | ⚠️ false alarm | ✅ | ✅ |

Read the map row by row. **Fine-tune and gradient ascent** barely move the model at their defaults, so they fail like
the original. **NegGrad+** over-forgets Carol, at 10.0%, and costs utility on both hard requests. **Bad Teacher** fails
UTILITY on all three and PRIVACY on the class. **SCRUB and SCRUB+R** pass the class, and SCRUB+R would look like the
winner on Carol without RELEARN. On the **random** request no approximate method passes, because most leave U-LiRA
between about 0.51 and 0.73, well above the retrain's 0.360. Bad Teacher, at 0.392, is the exception
there, but it fails UTILITY.

??? deep "Go deeper · the full table for Carol"

    | Method | Carol | Test | U-LiRA | Relearn steps | Cost | Verdict |
    |---|---|---|---|---|---|---|
    | Original | 100.0% | 98.0% | 0.950 | 0 | 0% | FAIL |
    | Retrain (seed 999) | 62.5% | 98.0% | 0.075 | 500 | 100% | PASS |
    | Fine-tune | 100.0% | 98.1% | 0.875 | 0 | 8.3% | FAIL |
    | Gradient ascent | 100.0% | 98.3% | 0.600 | 0 | 0.3% | FAIL |
    | NegGrad+ | 10.0% | 84.6% | 0.000 | 27 | 8.6% | FAIL |
    | SCRUB | 82.5% | 97.8% | 0.275 | 18 | 13.6% | FAIL |
    | SCRUB+R | 65.0% | 98.0% | 0.125 | 20 | 13.6% | FAIL |
    | Bad Teacher | 70.0% | 96.1% | 0.150 | 13 | 0.6% | FAIL |

    NegGrad+ has a U-LiRA of 0.000 and still fails. It over-forgot, so it looks less like a member, not more. FORGET,
    UTILITY and RELEARN catch it.

!!! note "Evidence, not proof"
    Thudi et al. (2022) show that the same weights can be reached with or without an example. A black-box audit can show
    a method *failed*; a pass only means no test could tell the difference. Real guarantees come from the **process**.

??? checkpoint "Checkpoint 3 · SISA fails FORGET on Carol by one digit, while SCRUB+R fails RELEARN. Should both be treated the same way?"
    **No.** SISA is exact by its process, so the miss is a false alarm, and its logs can show which shards and slices
    were retrained without her data. SCRUB+R has no such process to check, and the relearn attack found real evidence that she
    is still inside it. A FAIL starts an investigation, and what the investigation can check differs between the two.

## Limits of this lesson

**One small setting.** Everything uses 8 × 8 digits, one small network and an invented Carol. Lesson 12 moves to real
personal data.

**Default settings only.** Each method runs with its lesson's defaults. Tuned settings might pass more checks, but
tuning needs the gold band, so the notebook leaves that as a task.

**Fixed tolerances.** The 2 standard deviations, the 3-point floor and the privacy tolerance of 0.10 decide several
verdicts. A stricter tolerance would flip some of them, and Lesson 17 asks who should own those numbers.

**One relearn attacker.** The attack uses one learning rate and a 500-step budget. A stronger attacker might relearn
even from retrained models, so the notebook asks you to test a higher learning rate.

## Concepts used here

- [The unlearning audit](../unlearning/unlearning-audit.md)
- [Can a test prove forgetting?](../unlearning/testing-vs-proving.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)
- [The gold band](../unlearning/gold-band.md)

## Notes to take

!!! notes "Notes to take"
    - **Protocol.** Pre-registered defaults, 12 OUT and 8 IN references per request, the same recipe for all.
    - **Five checks.** FORGET, PRIVACY, UTILITY, COST and RELEARN. A method must pass every one.
    - **Bands.** Carol 62.7% ± 9.5%, class 0.0% ± 0.0%, random 98.2% ± 1.6%.
    - **First surprise.** On the random rows the original passed FORGET. U-LiRA caught it, 0.712 against 0.360.
    - **Relearn.** Retrains 500 steps on Carol, SCRUB+R 20, SCRUB 18, Bad Teacher 13. Pass mark 250.
    - **Class.** Retrains relearn 3s in a median of 9 steps, so the attack separates little there.
    - **SISA.** Passed class and random, missed Carol by one digit at 52.5%. A false alarm to investigate.
    - **Remember.** An audit is evidence, not proof. Real guarantees come from the process.

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
- q: Why does the audit use each method's default settings rather than the best run from Lessons 08 to 10?
  options:
    - The defaults are always better.
    - Picking the best run needs the gold band, which production does not have.
    - The best runs were lost.
  answer: 1
  why: Tuning against the answer key would make methods look better than they would be in real use.
- q: NegGrad+ had a U-LiRA of 0.000 on Carol but still failed. Which checks caught it?
  options:
    - Only COST
    - PRIVACY and COST
    - FORGET and UTILITY, as well as RELEARN
  answer: 2
  why: It over-forgot Carol at 10.0% and dropped test accuracy to 84.6%. An over-forgotten model looks less like a member.
- q: Why is SISA's RELEARN result "n/a"?
  options:
    - The attack fine-tunes one network, and SISA is an ensemble of five.
    - SISA failed every other check.
    - SISA relearnt Carol instantly.
  answer: 0
  why: SISA does not need the test, since after unlearning it is the same as a SISA system trained without Carol.
```

## Open question → Lesson 12

!!! levelup "Level up"
    You can now run one fair audit on every method, read all five checks and tell removal from suppression. Next quest,
    [Lesson 12 · Right to be forgotten and fairness](12-right-to-be-forgotten-and-fairness.md), where the data is real
    and the people who ask to be deleted are not a random sample.

Everything so far used 8 × 8 digits and an invented Carol. What happens on **real personal data**, when the people who
ask to be deleted are not a random sample?

[On to Lesson 12, right to be forgotten and fairness :material-arrow-right:](12-right-to-be-forgotten-and-fairness.md){ .md-button }
