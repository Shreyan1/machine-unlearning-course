---
title: "Lesson 09 · SCRUB"
description: A student that selectively disobeys its teacher, with a rewind. It works on whole classes and struggles with memorised individuals.
---

# Lesson 09 · SCRUB, a student that selectively disobeys its teacher

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 4 · Approximate unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 6</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 40 minutes · 3 checkpoints"
    By the end of this lesson you can

    - run SCRUB on Carol and read its epoch-by-epoch record,
    - spot a relapse and explain why SCRUB+R rewinds,
    - read a sweep of 16 settings and say on which kind of request SCRUB can be trusted.

## The story

SCRUB (Kurmanji et al., NeurIPS 2023) changes the question from "be wrong on Carol" to "stay identical to the original
model on everyone else, and move away from it on Carol". The original becomes a frozen **teacher**; a copy, the
**student**, is pulled in two directions. SCRUB+R adds a stopping rule. It saves a checkpoint every epoch and can **rewind**.

Lesson 08 left two gaps. Gradient ascent and NegGrad+ had no **reference** for what a model that never saw Carol would
say, and no **stopping rule** that works without the gold band. Only 1 of their 46 settings passed on Carol. SCRUB fills
the first gap with the teacher, and SCRUB+R tries to fill the second. This lesson finds out how far that gets us, first
on one run and then honestly, across many.

## What you will do

<ol class="steps" markdown>
<li markdown>Use the original model as the **teacher**.</li>
<li markdown>**Untrain** with SCRUB, recording Carol, her style and test accuracy after every epoch.</li>
<li markdown>Apply **SCRUB+R**, which rewinds to the checkpoint that matches unseen same-style data.</li>
<li markdown>**Prove it** with the audit.</li>
<li markdown>Sweep 16 settings on two kinds of request for an honest scoreboard.</li>
</ol>

## What each step teaches

**Step 1. The teacher.** The teacher is simply the original model, 100.0% right on Carol, frozen so it never changes.
The student starts as an exact copy. The gold band from 12 retrains is 53.3% to 72.2%.

**Step 2. Untrain and watch.** The run uses 8 epochs. The first 4 have a max-step on Carol's digits and a min-step on
everyone else. The last 4 have only the min-step. After each epoch the notebook records three numbers, so you can see
the two forces at work.

**Step 3. Rewind.** SCRUB+R uses 80 test digits redrawn in Carol's thick-marker style, which the model never saw. The
final model's error on them estimates how wrong a model that never met Carol should be on her. The rewind picks the
saved checkpoint whose error on Carol is closest.

**Step 4. Prove it.** The original, a new retrain, SCRUB and SCRUB+R go through the gate of Lesson 06, with the U-LiRA
privacy test from Lesson 05.

??? deep "Go deeper · step 5, the sweep"
    One good run proves nothing, as Lesson 08 showed. The sweep tries every mix of two learning rates, two forget batch
    sizes, two temperatures and two schedules, which is 16 settings, each with and without the rewind. It adds the 46
    gradient ascent and NegGrad+ settings from Lesson 08. Each method is run on two requests, Carol and every digit 3,
    and each run is counted as a pass only if it passes the whole gate.

## Key results

<div class="stats">
<div class="is-good"><strong>97.8–98.3%</strong><span>test accuracy in every epoch but one</span></div>
<div class="is-bad"><strong>82.5%</strong><span>plain SCRUB on Carol after the relapse, FAIL</span></div>
<div class="is-good"><strong>65.0%</strong><span>SCRUB+R rewound to epoch 4, PASS</span></div>
<div class="is-bad"><strong>0 / 16</strong><span>SCRUB settings that passed on Carol</span></div>
</div>

| Epoch | Kind | Carol | Her style (unseen) | Test |
|---|---|---|---|---|
| 1 | Max + min | 100.0% | 80.0% | 98.0% |
| 4 | Max + min | 65.0% | 53.8% | 98.0% |
| 5 | Min | 77.5% | 62.5% | 98.1% |
| 8 | Min | 82.5% | 70.0% | 97.8% |

Test accuracy barely moved, so the teacher reference works. But Carol fell into the band at epoch 4 and then **relapsed**
during the repair-only epochs. Her influence had been pushed aside, not removed.

Read the rows one at a time. **Epoch 1** has barely changed anything. **Epoch 4** is the last max-step, and Carol drops
to 26 of her 40 digits, inside the band. **Epoch 5** is the first repair-only epoch, and five of her digits come back.
**Epoch 8** ends at 33 digits, above the band. The style column moves the same way, from 53.8% back up to 70.0%, so
the max-step had pushed away thick-marker digits in general and the repair brought them all back.

??? deep "Go deeper · all eight epochs"

    | Epoch | Kind | Carol | Her style (unseen) | Test |
    |---|---|---|---|---|
    | 1 | Max + min | 100.0% | 80.0% | 98.0% |
    | 2 | Max + min | 97.5% | 78.8% | 98.3% |
    | 3 | Max + min | 95.0% | 73.8% | 95.4% |
    | 4 | Max + min | 65.0% | 53.8% | 98.0% |
    | 5 | Min | 77.5% | 62.5% | 98.1% |
    | 6 | Min | 82.5% | 68.8% | 98.0% |
    | 7 | Min | 82.5% | 70.0% | 98.0% |
    | 8 | Min | 82.5% | 70.0% | 97.8% |

    Epoch 3 is the one dip in test accuracy, to 95.4%. The min-step of epoch 4 repaired it.

??? checkpoint "Checkpoint 1 · The final model scores 70.0% on Carol's unseen style. Which checkpoint does SCRUB+R pick?"
    **Epoch 4.** The target error is 100 − 70.0 = 30.0%. Carol's error after each epoch was 0, 2.5, 5.0, 35.0, 22.5,
    17.5, 17.5 and 17.5%. The closest to 30.0% is 35.0% at epoch 4, 5 points away. The next closest is 22.5% at epoch
    5, 7.5 points away. Epoch 4 is at 65.0% on Carol, inside the band.

| Method | Carol | Test | U-LiRA | Verdict |
|---|---|---|---|---|
| SCRUB | 82.5% | 97.8% | 0.275 | FAIL |
| SCRUB+R | 65.0% | 98.0% | 0.125 | PASS |

**SCRUB** fails twice. 82.5% is above the band, so it fails FORGET. U-LiRA still flags 11 of Carol's 40 digits as
members, so it fails PRIVACY. **SCRUB+R** lands inside the band and U-LiRA flags only 5 digits, so it passes. For
comparison, the original scored 0.950 on U-LiRA and a new retrain 0.075.

**The honest scoreboard** (passes / settings tried).

| Method | Carol | Class "3" |
|---|---|---|
| Gradient ascent | 0 / 10 | 0 / 10 |
| NegGrad+ | 1 / 36 | 19 / 36 |
| SCRUB | 0 / 16 | 10 / 16 |
| SCRUB+R | 1 / 16 | 8 / 16 |

On a class, the target is clear and anchored methods do well. On Carol, SCRUB mostly **over-forgets** or **relapses**.
The privacy test does not catch over-forgetting; only the gold-band check does.

An **anchored** method is pulled back to normal behaviour on the retain set, as NegGrad+ and SCRUB are. Gradient
ascent has no anchor and never passes. On the class, the target is 0%, so overshooting costs nothing. On Carol, the
target is about 60%, and "move away" has no idea when to stop. So the single pass from the rewind above was the
exception, not the rule.

??? checkpoint "Checkpoint 2 · Why does plotting the Carol runs show most SCRUB dots high on test accuracy but to the left of the band?"
    **The teacher protects utility, but nothing limits the push.** High dots mean test accuracy stayed good, which is the
    teacher at work. Left of the band means Carol fell below what models that never saw her score, which is
    over-forgetting. The privacy test does not flag those runs, since an over-forgotten model looks less like a member.

## Limits of this lesson

**One small setting.** The results come from 8 × 8 digits, one small network and a 40-digit forget set. The pass rates
will differ on other models and data.

**A coarse rewind.** Checkpoints are saved once per epoch. Carol fell from 95.0% to 65.0% in one epoch, so a finer
rewind might pass more often. The notebook's tasks ask you to try this.

**Two requests only.** The sweep covers Carol and the class "3". The random request, where the original is already
inside the band, is left as a task.

**Three checks, not five.** This lesson's gate has no cost check and no relearn attack. Lesson 11 adds it, and SCRUB+R's pass on Carol
does not survive.

??? checkpoint "Checkpoint 3 · Your team must forget one customer whose data is unusual, like Carol's. Is SCRUB+R a safe choice on this evidence?"
    **No.** On Carol it passed 1 of 16 settings, and Lesson 11 shows that even that pass relearnt her in 20 steps. It
    does well on whole classes, at 8 of 16, but that is a different kind of request. For one unusual person, an exact
    method is safer.

## Concepts used here

- [SCRUB, teacher and student](../unlearning/scrub.md)
- [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md)
- [The gold band](../unlearning/gold-band.md)

## Notes to take

!!! notes "Notes to take"
    - **SCRUB.** Copy the frozen teacher on \(D_r\), move away from it on \(D_f\). Lesson 09 runs 4 max epochs, then 4 min.
    - **Anchor.** Test accuracy stayed between 97.8% and 98.3% in every epoch but epoch 3.
    - **Relapse.** Carol fell to 65.0% at epoch 4 and climbed back to 82.5% by epoch 8.
    - **Verdicts.** SCRUB 82.5%, U-LiRA 0.275, FAIL. SCRUB+R 65.0%, U-LiRA 0.125, PASS.
    - **Rewind rule.** Target error from unseen same-style data, 30.0% here, so it picks epoch 4.
    - **Scoreboard.** Carol, SCRUB 0 of 16 and SCRUB+R 1 of 16. Class "3", 10 and 8 of 16.
    - **Trap.** Most Carol runs over-forget, and only the gold band catches that.

## Quiz

```quiz
- q: What is SCRUB's teacher?
  options:
    - The original model, frozen
    - A random model
    - A retrained model
  answer: 0
  why: The student copies it on the retain set and moves away from it on the forget set.
- q: What happened to Carol during the repair-only (min) epochs?
  options:
    - She climbed back out of the band (relapse).
    - She dropped to 0%.
    - Nothing changed.
  answer: 0
  why: Copying the teacher on everyone else partly re-taught the student about her.
- q: How does SCRUB+R choose its checkpoint?
  options:
    - The one whose error on Carol best matches unseen same-style data
    - Always the last one
    - The one with the highest test accuracy
  answer: 0
  why: Same-style held-out data estimates how a model that never saw Carol would do.
- q: On which request did SCRUB pass more often?
  options:
    - Forgetting the whole class "3"
    - Forgetting Carol
  answer: 0
  why: 10 of 16 settings passed on the class; none passed on Carol.
- q: Which check catches over-forgetting?
  options:
    - The gold-band check on forget accuracy
    - The privacy test (U-LiRA)
    - The cost check
  answer: 0
  why: An over-forgotten model looks less like a member, so the privacy test does not flag it.
- q: Carol's unseen-style accuracy fell from 80.0% to 53.8% during the max-steps. What does that tell you?
  options:
    - The max-step pushed away thick-marker digits in general, not only Carol's.
    - The test set was changed.
    - The teacher forgot how to read digits.
  answer: 0
  why: The style digits were never trained on, yet they moved with Carol, and they came back with her during repair.
- q: Plain SCRUB ended with U-LiRA at 0.275 on Carol. How many of her 40 digits still looked like members?
  options:
    - 3
    - 28
    - 11
  answer: 2
  why: 0.275 × 40 = 11. That was enough to fail PRIVACY, while SCRUB+R at 0.125 left only 5.
- q: Why is the one rewound pass on Carol not proof that SCRUB+R works on people?
  options:
    - The sweep shows it passed only 1 of 16 settings on Carol.
    - The rewind is not allowed in production.
    - The gold band was built wrongly.
  answer: 0
  why: A single run can be lucky. The honest scoreboard counts passes across many reasonable settings.
```

## Open question → Lesson 10

!!! levelup "Level up"
    You can now run SCRUB, read a relapse and work out a rewind, and you know why a sweep matters more than one run.
    Next quest, [Lesson 10 · Bad Teacher](10-bad-teacher.md), where the student gets an explicit target for Carol.

SCRUB says "be *different* from the teacher on Carol", but different in which direction? What if the student had an
explicit target for Carol, a second teacher that knows *nothing*, copied in one fast epoch?

[On to Lesson 10, Bad Teacher :material-arrow-right:](10-bad-teacher.md){ .md-button }
