---
title: "Lesson 09: SCRUB"
description: A student that selectively disobeys its teacher, with a rewind. It works on whole classes and struggles with memorised individuals.
---

# Lesson 09: SCRUB, a student that selectively disobeys its teacher

<div class="chips"><span class="chip">⏱ ~40 min</span><span class="chip">Stage 4 · Approximate unlearning</span><span class="chip">Rung 6</span></div>

<div class="buttons">
<a class="md-button md-button--primary" href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb">Open in Colab</a>
<a class="md-button" href="https://github.com/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb">View on GitHub</a>
</div>

## The story

SCRUB (Kurmanji et al., NeurIPS 2023) changes the question from "be wrong on Carol" to "stay identical to the original
model on everyone else, and move away from it on Carol". The original becomes a frozen **teacher**; a copy, the
**student**, is pulled in two directions. SCRUB+R adds a stopping rule. It saves a checkpoint every epoch and can **rewind**.

## What you will do

<ol class="steps" markdown>
<li markdown>Use the original model as the **teacher**.</li>
<li markdown>**Untrain** with SCRUB, recording Carol, her style and test accuracy after every epoch.</li>
<li markdown>Apply **SCRUB+R**: rewind to the checkpoint that matches unseen same-style data.</li>
<li markdown>**Prove it** with the audit.</li>
<li markdown>Sweep 16 settings on two kinds of request for an honest scoreboard.</li>
</ol>

## Key results

| Epoch | Kind | Carol | Her style (unseen) | Test |
|---|---|---|---|---|
| 1 | max + min | 100.0% | 80.0% | 98.0% |
| 4 | max + min | 65.0% | 53.8% | 98.0% |
| 5 | min | 77.5% | 62.5% | 98.1% |
| 8 | min | 82.5% | 70.0% | 97.8% |

Test accuracy barely moved, so the teacher reference works. But Carol fell into the band at epoch 4 and then **relapsed**
during the repair-only epochs. Her influence had been pushed aside, not removed.

| Method | Carol | Test | U-LiRA | Verdict |
|---|---|---|---|---|
| SCRUB | 82.5% | 97.8% | 0.275 | FAIL |
| SCRUB+R | 65.0% | 98.0% | 0.125 | PASS |

**The honest scoreboard** (passes / settings tried):

| Method | Carol | Class "3" |
|---|---|---|
| Gradient ascent | 0 / 10 | 0 / 10 |
| NegGrad+ | 1 / 36 | 19 / 36 |
| SCRUB | 0 / 16 | 10 / 16 |
| SCRUB+R | 1 / 16 | 8 / 16 |

On a class, the target is clear and anchored methods do well. On Carol, SCRUB mostly **over-forgets** or **relapses**.
The privacy test does not catch over-forgetting; only the gold-band check does.

## Concepts used here

- [SCRUB, teacher and student](../unlearning/scrub.md)
- [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md)
- [The gold band](../unlearning/gold-band.md)

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
```

## Open question → Lesson 10

SCRUB says "be *different* from the teacher on Carol", but different in which direction? What if the student had an
explicit target for Carol, a second teacher that knows *nothing*, copied in one fast epoch?

[Next: Lesson 10, Bad Teacher](10-bad-teacher.md){ .md-button }
