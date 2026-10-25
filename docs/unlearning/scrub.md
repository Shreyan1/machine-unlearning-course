---
title: SCRUB, teacher and student
description: SCRUB trains a student to copy the original model on the retain set and move away from it on the forget set, with a rewind to stop at the right point.
---

# SCRUB (teacher and student)

!!! oneline "In one line"
    SCRUB trains a copy of the model (the **student**) to stay identical to the original (the **teacher**) on everyone
    else, and to **move away** from it on the data to forget.

!!! simply "Explain it simply"
    Picture a student copying a teacher's homework. For every question but Carol's, the student copies the teacher
    exactly. For Carol's questions, the student deliberately writes something different from the teacher. Do both at
    once, and you get a student who knows everything the teacher knows, except Carol.

## Why it matters

Gradient ascent had no reference and no brake, so it broke the model. SCRUB (Kurmanji, Triantafillou, Hayes and
Triantafillou, NeurIPS 2023) uses the original model as a reference, which protects everyone else's accuracy. Its
variant **SCRUB+R** adds a stopping rule you can use in production. It is one of the best-known approximate methods,
and studying where it fails teaches a lot.

## A simple example

An apprentice copies a master craftsman. We tell the apprentice to do everything exactly like the master, except for
Carol's digits, where they should deliberately do something *different*. Because the apprentice keeps copying the master
everywhere else, they keep their skill.

## How it works

<!-- diagram: scrub -->

<ol class="steps" markdown>
<li markdown>**Freeze the original model** as the teacher. Make a copy as the student.</li>
<li markdown>**Max-step**: for an epoch, push the student's outputs on \(D_f\) *away* from the teacher's, by increasing the
[KL divergence](../ml-basics/probabilities-and-kl-divergence.md) between them.</li>
<li markdown>**Min-step**: for an epoch, pull the student back towards the teacher on \(D_r\) and keep it accurate.</li>
<li markdown>**Alternate**, then finish with a few extra min-steps to repair any damage.</li>
<li markdown>**SCRUB+R (rewind)**: keep a checkpoint after every epoch, and pick the one whose error on Carol best matches
the error on **unseen data in her style**, which you *can* compute in production.</li>
</ol>

### What happened in Lesson 09

| Epoch | Kind | Carol | Her style (unseen) | Test |
|---|---|---|---|---|
| 1 | max + min | 100.0% | 80.0% | 98.0% |
| 4 | max + min | 65.0% | 53.8% | 98.0% |
| 5 | min | 77.5% | 62.5% | 98.1% |
| 8 | min | 82.5% | 70.0% | 97.8% |

Test accuracy hardly moved, so the teacher reference works. But after the max-steps stopped, Carol **climbed back out**
of the band during the repair epochs. Her influence had been *pushed aside*, not removed. This **relapse** is why the
rewind exists. SCRUB+R picked the checkpoint just before the relapse (65.0%) and passed.

### The honest scoreboard

Lesson 09 swept 16 settings of each, on two kinds of request.

| Method | Carol (a memorised person) | Class (every "3") |
|---|---|---|
| Gradient ascent | 0 / 10 | 0 / 10 |
| NegGrad+ | 1 / 36 | 19 / 36 |
| SCRUB | 0 / 16 | 10 / 16 |
| SCRUB+R | 1 / 16 | 8 / 16 |

On a whole class, the target is clear (0%), and anchored methods do well. On Carol, the target is about 60%, and SCRUB
mostly **over-forgets** ("move away" has no idea how far is far enough) or **relapses**.

!!! warning "Passing four checks is not the end"
    In the full audit ([Lesson 11](../lessons/11-the-unlearning-audit.md)), SCRUB+R passed FORGET, PRIVACY, UTILITY and
    COST on Carol. But shown half of her digits again, it got the other half right within about 20 steps. Retrained
    models needed the full 500-step budget. It had suppressed Carol, not removed her. See
    [The unlearning audit](unlearning-audit.md).

## In code

```python
from mul import methods
student = methods.scrub(original, L.Xr, L.yr, L.Xf, steps=8, max_steps=4)
student_r = methods.scrub_rewind(original, L.Xr, L.yr, L.Xf, L.yf,
                                 L.X_like_forget, L.y_like_forget)   # SCRUB+R
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting the last epoch.** Repair epochs can bring the forgotten data back. Rewind.
    - **Relying on the privacy test alone.** An over-forgotten model looks *less* like a member, so only the gold-band
      check catches over-forgetting.
    - **Judging it on class forgetting only.** It works much better on whole classes than on memorised individuals.

## Key takeaways

- SCRUB copies the teacher on \(D_r\) and moves away from it on \(D_f\).
- Alternating max and min steps keeps utility intact.
- SCRUB+R rewinds to the checkpoint that matches same-style held-out data.
- It works well on classes and poorly on memorised individuals, and it can suppress rather than remove.

## Quiz

```quiz
- q: In SCRUB, who is the teacher?
  options:
    - The original model, frozen
    - A random model
    - The retrained model
  answer: 0
  why: The original model is the reference the student copies on the retain set.
- q: What does the max-step do?
  options:
    - Pushes the student away from the teacher on the forget set
    - Pulls the student towards the teacher on the retain set
    - Deletes the forget set
  answer: 0
  why: It increases the KL divergence on the forget set; the min-step does the opposite on the retain set.
- q: What is the "relapse" seen in Lesson 09?
  options:
    - Carol's accuracy climbs back up during the repair epochs
    - Test accuracy collapses to 10%
    - The teacher forgets Carol
  answer: 0
  why: Copying the teacher on everyone else partly re-teaches the student about Carol.
- q: How does SCRUB+R decide where to stop, without the gold band?
  options:
    - It matches Carol's error to the error on unseen data in her style.
    - It always stops after one epoch.
    - It asks the user.
  answer: 0
  why: Unseen same-style data estimates how wrong a model that never saw Carol would be.
- q: On which kind of request does SCRUB do best?
  options:
    - Forgetting a whole class
    - Forgetting one memorised person
  answer: 0
  why: For a class the target is clearly 0%; for Carol it is about 60%, and SCRUB has no sense of "far enough".
```

## Try it

- Read the next concept, [Bad Teacher](bad-teacher.md).
- Run the lesson [09 · SCRUB](../lessons/09-scrub.md).
