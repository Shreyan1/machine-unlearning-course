---
title: SCRUB, teacher and student
description: SCRUB trains a student to copy the original model on the retain set and move away from it on the forget set, with a rewind to stop at the right point.
---

# SCRUB (teacher and student)

!!! oneline "In one line"
    SCRUB trains a copy of the model (the **student**) to stay identical to the original (the **teacher**) on everyone
    else, and to **move away** from it on the data to forget.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain the two opposing steps of SCRUB and why the teacher protects everyone else,
    - read an epoch-by-epoch record, spot a relapse and work out which checkpoint SCRUB+R rewinds to,
    - say why SCRUB does well on a whole class and badly on one memorised person.

## Why it matters

Gradient ascent had no reference and no brake, so it broke the model. In [Lesson 08](../lessons/08-approximate-baselines-and-traps.md),
gradient ascent and NegGrad+ passed only 1 of 46 settings on Carol. They lacked two things. One was a **reference**
for what a model that never saw Carol would say, since "be as wrong as possible on her" is not what such a model does.
The other was a **stopping rule** that works without the gold band.

SCRUB (Kurmanji, Triantafillou, Hayes and Triantafillou, NeurIPS 2023) uses the original model as a reference, which
protects everyone else's accuracy. Its variant **SCRUB+R** adds a stopping rule you can use in production. It is one of
the best-known approximate methods, and studying where it fails teaches a lot.

It matters for a practical reason too. SCRUB costs about 13.6% of a full retrain in the course. A team that gets many
erasure requests wants something cheaper than retraining, and SCRUB is a natural method to try.

## A simple example

!!! simply "Explain it simply"
    Picture a student copying a teacher's homework. For every question but Carol's, the student copies the teacher
    exactly. For Carol's questions, the student deliberately writes something different from the teacher. Do both at
    once, and you get a student who knows everything the teacher knows, except Carol.

An apprentice copies a master craftsman. We tell the apprentice to do everything exactly like the master, except for
Carol's digits, where they should deliberately do something *different*. Because the apprentice keeps copying the master
everywhere else, they keep their skill.

Notice what the instruction leaves out. It says "be different" but never says *how* different. A model that never met
Carol still reads about 60% of her digits correctly, so the right amount of difference is moderate. The apprentice has
no way to know that, and this gap is behind most of SCRUB's failures below.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Teacher | The original model, frozen so it never changes | The network that is 100.0% right on Carol |
| Student | A copy of the teacher that SCRUB edits | Starts at 100.0% on Carol and is moved down |
| [KL divergence](../start-here/glossary.md#k) | A measure of how different two sets of probabilities are, 0 when they match | Kept small on the retain set, pushed up on Carol |
| Max-step | An epoch over the forget set that pushes the student's outputs away from the teacher's | Epochs 1 to 4 in Lesson 09 |
| Min-step | An epoch over the retain set that pulls the student back towards the teacher and keeps it accurate | Every epoch, 1 to 8 |
| Relapse | Forgotten data coming back during later training | Carol climbs from 65.0% to 82.5% in epochs 5 to 8 |
| [Checkpoint](../start-here/glossary.md#c) | A saved copy of the model at one moment in training | SCRUB+R keeps one after every epoch |
| [SCRUB+R](../start-here/glossary.md#s) | SCRUB with a rewind to the checkpoint that looks "just forgetful enough" | Rewinds to epoch 4, at 65.0% on Carol |
| [Over-forgetting](../start-here/glossary.md#o) | Ending up worse on the forget set than models that never saw it | Most SCRUB settings in the Lesson 09 sweep |

## How it works

<!-- diagram: scrub -->

The figure shows the two models and the two pulls on the student. The yellow teacher at the top is frozen. The blue
student below starts as an exact copy of it. On the retain data \(D_r\), the student is pulled towards the teacher
(green). On the forget data \(D_f\), it is pushed away (red). The two steps take turns, and the run stops early.

<ol class="steps" markdown>
<li markdown>**Freeze the original model** as the teacher. Make a copy as the student.</li>
<li markdown>**Max-step.** For an epoch, push the student's outputs on \(D_f\) *away* from the teacher's, by increasing the
[KL divergence](../ml-basics/probabilities-and-kl-divergence.md) between them.</li>
<li markdown>**Min-step.** For an epoch, pull the student back towards the teacher on \(D_r\) and keep it accurate.</li>
<li markdown>**Alternate**, then finish with a few extra min-steps to repair any damage.</li>
<li markdown>**SCRUB+R (rewind).** Keep a checkpoint after every epoch, and pick the one whose error on Carol best matches
the error on **unseen data in her style**, which you *can* compute in production.</li>
</ol>

**The teacher is the anchor.** Because the student is always pulled back to the teacher on the 1,217 digits that are
not Carol's, the rest of the model cannot drift far. Gradient ascent had nothing like this.

**The max-step has no target.** It only says "more different". It keeps pushing for as long as it runs, which is why
the number of max-steps matters so much.

**The min-step does two jobs.** It copies the teacher's probabilities and also fits the true labels, so it repairs any
damage the max-step caused to everyone else. Lesson 09 runs 4 epochs with both steps, then 4 epochs of min-steps only.

**For Carol this means** her digits are pushed away for 4 epochs, while the other 1,217 digits hold the model in place.

??? deep "Go deeper · the SCRUB loss in symbols, and the settings Lesson 09 uses"
    Write \(d(x)\) for the KL divergence from the teacher's probabilities to the student's on one example, after both are
    softened by a temperature \(T\) (see [Temperature](../ml-basics/probabilities-and-kl-divergence.md#temperature)).
    The paper's goal (its Eq. 3) is

    \[
    \min_w \; \alpha \cdot \frac{1}{N_r}\sum_{D_r} d(x) \;+\; \gamma \cdot \frac{1}{N_r}\sum_{D_r} \text{CE}(x) \;-\; \frac{1}{N_f}\sum_{D_f} d(x)
    \]

    The first term keeps the student close to the teacher on the retain set. The second is the usual cross-entropy, so
    the student stays accurate. The third has a minus sign, so making it larger lowers the total, which pushes the
    student away on the forget set.

    The paper does not minimise this all at once. It alternates, like training a GAN. A max-step ascends \(d\) on
    \(D_f\), and a min-step descends \(\alpha d + \gamma \text{CE}\) on \(D_r\). The course library follows the paper's
    Algorithm 1 in `mul/methods.py`, in about 25 lines.

    Lesson 09's run uses 8 epochs in all, the first 4 with a max-step, a learning rate of 0.0005, forget batches of 8
    digits, \(T = 1\) and \(\alpha = \gamma = 1\). Its cost is 4 × 40 forget digits plus 8 × 1,217 retain digits, which
    is 9,896 example-gradients, or 13.6% of the 73,020 in a 60-epoch retrain.

### What happened in Lesson 09

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

"Her style (unseen)" is 80 test digits redrawn with Carol's thick marker. The model never trained on them, so they show
whether it can still read her *kind* of handwriting.

Test accuracy dipped to 95.4% at the worst epoch and recovered, so the teacher reference works. But after the max-steps stopped, Carol **climbed back out**
of the band during the repair epochs. Her influence had been *pushed aside*, not removed. This **relapse** is why the
rewind exists. SCRUB+R picked the checkpoint just before the relapse (65.0%) and passed.

Read the middle column too. Her style fell from 80.0% to 53.8% during the max-steps and climbed back to 70.0% during
the min-steps. The max-step did not push away *Carol* alone. It pushed away thick-marker digits in general, and the
repair epochs brought the whole style back, Carol included.

??? checkpoint "Checkpoint 1 · Carol is at 65.0% after epoch 4 and 82.5% after epoch 8. How many of her digits came back, and does epoch 8 pass a band of about 53% to 72%?"
    **Seven came back, and it fails.** Each of her 40 digits is worth 2.5 points, so 65.0% is 26 digits and 82.5% is 33.
    That is 33 − 26 = 7 digits regained without the student ever being shown them again. 82.5% is above the top of
    the band, so the final model still remembers too much.

### The honest scoreboard

Lesson 09 swept 16 settings each of SCRUB and SCRUB+R, beside Lesson 08's 46 baseline settings, on two kinds of
request.

| Method | Carol (a memorised person) | Class (every "3") |
|---|---|---|
| Gradient ascent | 0 / 10 | 0 / 10 |
| NegGrad+ | 1 / 36 | 19 / 36 |
| SCRUB | 0 / 16 | 10 / 16 |
| SCRUB+R | 1 / 16 | 8 / 16 |

On a whole class, the target is clear (0%), and anchored methods do well. On Carol, the target is about 60%, and SCRUB
mostly **over-forgets** ("move away" has no idea how far is far enough) or **relapses**.

An **anchored** method is one that is pulled back towards normal behaviour on the retain set, as NegGrad+ and SCRUB
are. Gradient ascent has no anchor and never passes. On the class request, overshooting does no harm, because the
target already sits at the floor of 0%. On Carol, overshooting lands below the band, which fails just as staying above
it does.

??? deep "Go deeper · the 16 settings, and where the failures land"
    The sweep tries every mix of two learning rates (0.0005 and 0.001), two forget batch sizes (8 and 16), two
    temperatures (1 and 4) and two schedules (8 epochs with 4 max-steps, or 10 with 6). That is 2 × 2 × 2 × 2 = 16
    settings, each run with and without the rewind.

    The lesson plots each Carol run as a dot, with accuracy on Carol across and test accuracy up. SCRUB's dots sit high,
    so utility is fine, but mostly to the **left** of the band, which is over-forgetting. The settings that do not
    over-forget tend to relapse instead. The rewind rescues only the occasional run.

    The privacy test (U-LiRA) does not catch the over-forgotten runs. An over-forgotten model looks *less* like a
    member, not more. Only the gold-band check flags it, which is why the audit needs several checks.

!!! warning "Passing four checks is not the end"
    In the full audit ([Lesson 11](../lessons/11-the-unlearning-audit.md)), SCRUB+R passed FORGET, PRIVACY, UTILITY and
    COST on Carol. But shown half of her digits again, it got the other half right within about 20 steps. Retrained
    models needed the full 500-step budget. It had suppressed Carol, not removed her. See
    [The unlearning audit](unlearning-audit.md).

## A worked example

Follow Carol through one SCRUB+R run in Lesson 09.

1. **The start.** The teacher and the student are both the original model, at 100.0% on Carol and 98.0% on the test
   set. The [gold band](gold-band.md) from 12 retrains runs from 53.3% to 72.2%.
2. **Push and hold.** Four epochs with a max-step bring Carol down to 65.0%, inside the band. Test accuracy is still
   98.0%.
3. **Repair and relapse.** Four min-only epochs lift Carol back to 82.5%. This final model is plain SCRUB.
4. **Find the target without the band.** In production nobody has the gold band. SCRUB+R asks how wrong a model should
   be on digits like Carol's that it never saw. The final model scores 70.0% on her unseen style, so its error there
   is 30.0%. That becomes the target error on Carol.
5. **Rewind.** Carol's error after each epoch was 0, 2.5, 5.0, 35.0, 22.5, 17.5, 17.5 and 17.5%. The closest to 30.0%
   is 35.0%, at epoch 4, which is 5 points away. The next closest, 22.5% at epoch 5, is 7.5 points away. So SCRUB+R
   rewinds to epoch 4, at 65.0% on Carol.
6. **The audit.** Both models are scored against the band and the per-example privacy test.

| Model in Lesson 09 | Carol | Test | U-LiRA | Verdict |
|---|---|---|---|---|
| Original | 100.0% | 98.0% | 0.950 | FAIL |
| Retrain (seed 999) | 62.5% | 98.0% | 0.075 | PASS |
| SCRUB | 82.5% | 97.8% | 0.275 | FAIL |
| SCRUB+R | 65.0% | 98.0% | 0.125 | PASS |

The U-LiRA column is the share of Carol's digits that a per-example
[membership attack](membership-inference-attacks.md) still judges "trained on". Plain SCRUB leaves 0.275 × 40 = 11 of
them looking like members, so it fails PRIVACY as well as FORGET. SCRUB+R brings that down to 5 and passes both.

??? checkpoint "Checkpoint 2 · Suppose the final model had scored 85.0% on Carol's unseen style instead of 70.0%. Which checkpoint would SCRUB+R pick, and would it pass?"
    **Epoch 6, and it would fail.** The target error would be 100 − 85.0 = 15.0%. The closest error on Carol is 17.5%,
    first reached at epoch 6, which is 2.5 points away. That checkpoint is at 82.5% on Carol, above the band. The
    rewind is only as good as its estimate of the target.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>98.0%</strong><span>test accuracy after SCRUB+R, the teacher kept everyone else safe</span></div>
<div class="is-bad"><strong>82.5%</strong><span>plain SCRUB on Carol after the relapse, FAIL</span></div>
<div class="is-good"><strong>65.0%</strong><span>SCRUB+R rewound to epoch 4, PASS</span></div>
<div class="is-bad"><strong>0 / 16</strong><span>SCRUB settings that passed on Carol</span></div>
</div>

The single run looks like a success story for the rewind. The sweep tells the honest version. On Carol, plain SCRUB
never passed and SCRUB+R passed once in 16 settings. On the class "3", they passed 10 and 8 times. The same method can
be good or bad depending on what you ask it to forget.

## Limits

**It has no idea how far is far enough.** The max-step pushes away with no target, so the result depends on how long
it runs and how hard it pushes. That is why most Carol settings over-forgot.

**The rewind needs data in the same style.** SCRUB+R works only if you hold unseen examples that look like the forget
set. For Carol that meant 80 thick-marker digits. For a real person with unusual data, such a set may not exist.

**The rewind can only pick a checkpoint it saved.** With one checkpoint per epoch, Carol jumped from 95.0% to 65.0% in a
single epoch. If no saved checkpoint lands in the band, rewinding cannot help.

??? deep "Go deeper · two more limits"
    **It can suppress rather than remove.** SCRUB+R passed four checks on Carol and still relearnt her other 20 digits
    in 20 steps, against 500 for retrained models. Lesson 11's relearn attack is the only check that saw this.

    **It is sensitive to its settings.** The notebook links this to the NeurIPS 2023 unlearning competition
    (Triantafillou et al. 2024), which found approximate methods sensitive to the kind of request and to their
    settings. In the course, no SCRUB setting was safe to run blind on a memorised person.

## What to do in practice

!!! tip "What to do in practice"
    - Use SCRUB+R rather than plain SCRUB, and keep a checkpoint after every epoch or more often.
    - Hold back unseen data in the same style as the forget set before you start, since the rewind depends on it.
    - Fix the settings before you look at any result, then judge the model with a full audit, including a relearn
      attack.
    - Expect it to work better for removing a whole class than for one memorised person, and test the request type you
      really face.
    - If the person's data is unusual and the stakes are high, prefer an exact method such as [SISA](sisa.md).

## In code

```python
from mul import methods
cfg = dict(steps=8, max_steps=4, lr=5e-4, forget_batch_size=8, T=1.0)   # Lesson 09's settings
student, info = methods.scrub(original, L.Xr, L.yr, L.Xf, **cfg)
student_r, info_r = methods.scrub_rewind(original, L.Xr, L.yr, L.Xf, L.yf,
                                         L.X_like_forget, L.y_like_forget, **cfg)   # SCRUB+R
```

`scrub` returns the student after the last epoch. `scrub_rewind` runs the same thing with a checkpoint after every
epoch, measures the final student's error on `L.X_like_forget` (Carol's unseen style) and returns the checkpoint whose
error on Carol is closest to it. `info_r` records the target error, every checkpoint's error and the
one it chose.

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting the last epoch.** Repair epochs can bring the forgotten data back. Rewind.
    - **Relying on the privacy test alone.** An over-forgotten model looks *less* like a member, so only the gold-band
      check catches over-forgetting.
    - **Judging it on class forgetting only.** It works much better on whole classes than on memorised individuals.
    - **Tuning against the gold band.** Picking the best of 16 settings by checking the band uses an answer key that
      production does not have.
    - **Stopping at four checks.** SCRUB+R passed four on Carol and still came back in 20 relearn steps.

??? checkpoint "Checkpoint 3 · A team sees that SCRUB passed 10 of 16 settings when forgetting every digit 3. They plan to use it for one customer's erasure request. What do you tell them?"
    **The class result does not carry over.** On Carol, a memorised person, plain SCRUB passed 0 of 16 settings and
    SCRUB+R 1 of 16. A class has a sharp target of 0%, while a person's target sits in the middle. Test on the kind of
    request you really face, and add a relearn attack before you trust a pass.

## Key takeaways

!!! notes "Notes to take"
    - **SCRUB.** A student copies the frozen teacher on \(D_r\) and moves away from it on \(D_f\), using KL divergence.
    - **Schedule.** Alternate max-steps and min-steps, then a few min-only epochs to repair. Lesson 09 used 4 and 4.
    - **Anchor.** Test accuracy stayed within a few points of 98.0%, so the teacher protects everyone else.
    - **Relapse.** Carol fell to 65.0% at epoch 4 and climbed back to 82.5% during repair. She was pushed aside.
    - **SCRUB+R.** Rewinds to the checkpoint whose error on Carol best matches the error on her unseen style.
    - **Scoreboard.** On Carol, SCRUB 0 of 16 and SCRUB+R 1 of 16. On the class "3", 10 and 8 of 16.
    - **Trap.** "Move away" has no sense of how far, so it over-forgets a person whose target is about 60%.
    - **Trap.** The privacy test misses over-forgetting. Only the gold band catches it.
    - **Remember.** SCRUB+R relearnt Carol in 20 steps against 500 for retrains, so it suppressed her.

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
- q: Why did test accuracy stay near 98% while Carol's accuracy moved a lot?
  options:
    - The test set was too small to change.
    - The min-step kept pulling the student back to the teacher on the retain set.
    - The max-step only touched the last layer.
  answer: 1
  why: The teacher is the anchor. Gradient ascent had no anchor, and its test accuracy fell with it.
- q: The final SCRUB model scores 70.0% on Carol's unseen style. What target error does SCRUB+R aim for on Carol?
  options:
    - 0%, because she must be forgotten completely
    - 70.0%
    - 30.0%
  answer: 2
  why: The error on unseen digits in her style is 100 − 70.0 = 30.0%. The checkpoint with an error closest to that is chosen.
- q: Most SCRUB settings left Carol below the gold band. Why does that count as a failure?
  options:
    - Doing much worse on Carol than models that never saw her marks her data as special.
    - It means the model still remembers her.
    - It always breaks test accuracy.
  answer: 0
  why: Over-forgetting is a signal too. The target is how models that never saw her behave, about 60% on her digits.
- q: SCRUB+R passed FORGET, PRIVACY, UTILITY and COST on Carol in Lesson 11. What did the relearn attack show?
  options:
    - It needed 500 steps, the same as retrained models.
    - It got her other half back in about 20 steps, so she was suppressed, not removed.
    - It could not be run on SCRUB+R.
  answer: 1
  why: Retrained models needed the full 500 steps because there was nothing to recall. Fast recovery means hidden, not gone.
```

## Try it

!!! levelup "Level up"
    You can now explain how a teacher anchors unlearning, read a relapse and work out a rewind. Next quest,
    [Bad Teacher](bad-teacher.md), where the student gets an explicit target for Carol, a second teacher that knows
    nothing.

- Read the next concept, [Bad Teacher](bad-teacher.md).
- Run the lesson [09 · SCRUB](../lessons/09-scrub.md).
- In the Lesson 09 notebook, save a checkpoint every half epoch and see whether the rewind passes more often on Carol.
