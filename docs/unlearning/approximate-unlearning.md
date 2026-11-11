---
title: Quick fixes and their traps
description: Fine-tuning, gradient ascent and NegGrad+ are cheap ways to edit a trained model, and they fail in three directions.
---

# Quick fixes and their traps

!!! oneline "In one line"
    Approximate unlearning edits an already-trained model cheaply, but with no guarantee. The simple versions fail
    by **under-forgetting**, **over-forgetting** or **breaking the model**.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why gradient ascent is a Newton step with the curvature thrown away,
    - tell the three ways a quick fix fails from an audit row,
    - explain why the one passing setting in Lesson 08 is not a recipe you can reuse.

## Why it matters

Most models in production were trained as one big network, long ago. [SISA](sisa.md) had to be chosen before training,
and [retraining](retraining-gold-standard.md) is expensive. When a deletion request arrives today, teams reach for a
quick fix on the model they already have. This page shows why the quick fixes are so hard to get right.

These fixes are called [approximate unlearning](../start-here/glossary.md#a). They edit the trained model directly,
for a small part of the cost of a retrain, but nothing guarantees that the result matches a model that never saw the
data. So every result has to be checked with an audit. Gradient ascent in particular is the most popular unlearning
baseline there is, and many papers compare against it. Knowing how it breaks is the first step to judging any method
that claims to beat it.

## A simple example

Imagine trying to make a student forget one wrong fact they learnt. You could.

- **Stop mentioning it** and hope it fades (fine-tuning on everything else). It mostly does not fade.
- **Drill the opposite**, over and over (gradient ascent). They forget the fact, but they also get confused about
  everything near it.
- **Drill the opposite, while revising everything else** (NegGrad+). Better, but you must stop at exactly the right
  moment.

!!! simply "Explain it simply"
    The goal is not a student who is wrong about the fact. The goal is a student who acts as if they never heard it.
    None of these three drills knows what that student would say, so none of them knows when to stop.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Approximate unlearning](../start-here/glossary.md#a) | A cheap edit to a trained model, with no guarantee, so its result must be audited | All three quick fixes on this page |
| [Fine-tuning](../start-here/glossary.md#f) | Training an existing model a little more on chosen data | Five more epochs on the 1,217 digits that are not Carol's |
| [Gradient ascent](../start-here/glossary.md#g) | Stepping uphill on the forget set's loss, to make the model worse on it | Climbing the loss on Carol's 40 digits |
| Step size \(\eta\) | How far each step moves the weights, also called the learning rate | 0.0003 or 0.001 in Lesson 08 |
| [NegGrad+](../start-here/glossary.md#n) | Gradient ascent on the forget set and normal training on the retain set, in every step | The only method that passed in Lesson 08 |
| Anchor weight \(\alpha\) | In NegGrad+, how much each step cares about the retain set. The rest goes to the forget set | α = 0.99, so 99% retain and 1% forget |
| Under-forgetting | Leaving the model still above the gold band, so it still remembers | Fine-tuning left Carol at 100.0% |
| [Over-forgetting](../start-here/glossary.md#o) | Pushing the model below the gold band, worse than models that never saw the data | NegGrad+ at 3 epochs, 12.5% on Carol |
| Stopping rule | A way to decide when to stop that does not need the gold band | Missing from all three quick fixes |

## How it works

<!-- diagram: approximate-unlearning -->

### Where gradient ascent comes from

The Newton step from [logistic regression](../ml-basics/logistic-regression.md) moves the weights in the direction the
deleted points were pulling, scaled by the curvature (the Hessian) of what remains.

A neural network has no usable Hessian. For the course's small network it would be a table of about 85,000 by 85,000
numbers, 29 GB in 32-bit floats. So replace the curvature with a small step size \(\eta\) that you choose by hand.

That is **gradient ascent** on the forget set. It trains the model to get *worse* on Carol. Even on logistic regression,
the best gradient-ascent step closed only **8%** of the gap that one Newton step closed (95%). The curvature is not a
detail; it is most of the answer.

??? deep "Go deeper · the two update rules side by side"
    The Newton step that removes the deleted points is

    \[
    w_{\text{new}} = w + H_r^{-1} \sum_{\text{deleted}} \nabla \ell_i(w)
    \]

    Here \(\nabla \ell_i(w)\) is the gradient of one deleted point's loss, the direction that point was pulling the
    weights, and \(H_r\) is the curvature of the loss on the data that remains. Replace \(H_r^{-1}\) with a small step
    size \(\eta\) and you get

    \[
    w_{\text{new}} = w + \eta \sum_{\text{deleted}} \nabla \ell_i(w)
    \]

    Moving with the deleted points' gradient increases their loss, which is why this is called ascent. Lesson 08 tried
    40 step sizes on logistic regression, where the exact retrained model is known, and measured how much of the
    distance to it each step closed. Too small a step made no progress and too large a step overshot. Even the best
    one closed 8%, because the raw gradient points in the wrong direction. \(H_r^{-1}\) is what turns it towards the
    retrained model.

??? checkpoint "Checkpoint 1 · The best gradient-ascent step closed 8% of the gap. Why not simply take a bigger step?"
    **Because the direction is wrong, not just the length.** A bigger step along the raw gradient overshoots and moves
    away from the retrained model, which Lesson 08's sweep of step sizes showed. Only the curvature turns the step
    towards the right answer, and a network does not have one you can use.

### Three quick fixes

| Method | Idea | What happened in Lesson 08 |
|---|---|---|
| **Fine-tune** on \(D_r\) | Keep training without Carol; hope she fades | Carol barely moved (100% after 5 epochs) |
| **Gradient ascent** on \(D_f\) | Climb Carol's loss | Forgot Carol, then everything; with a larger step, test accuracy fell from 98% to 10% |
| **NegGrad+** | Climb Carol's loss *and* descend on \(D_r\) in every step | Passed at exactly one setting; one epoch more and it over-forgot |

=== "Fine-tune"

    Fine-tuning trains the original model for a few more epochs on everyone except Carol. Nothing in it pushes away
    from her, so it relies on the model slowly losing what it no longer sees. For memorised data that is far too slow.
    After 5 epochs Carol was still at 100.0%, and the membership test still flagged her at 0.875. This is the same
    warm-start trap that Lesson 06 found, where 20 more epochs left her at 95.0%.

=== "Gradient ascent"

    Gradient ascent trains on Carol's 40 digits with the sign of the gradient flipped. It does push her accuracy down,
    but nothing says when to stop. Cross-entropy can grow without limit, so the model keeps getting worse. With a
    larger step, test accuracy fell epoch by epoch as 98%, 89%, 66%, 44%, 31% and on to 10%. Ten classes and 10%
    accuracy means the model is guessing.

=== "NegGrad+"

    NegGrad+ adds an anchor. In every step it climbs the loss on a few of Carol's digits and descends the loss on a
    batch of everyone else's. With α = 0.99, the step is 99% about the retain set and 1% about Carol. The anchor keeps
    the rest of the model in place, so it is the only one of the three that passed. But the pass lasted exactly one
    epoch.

### A worked example, NegGrad+ on Carol

Follow Carol through Lesson 08's audit. The pass marks come from 12 retrains without her.

1. **The targets.** Accuracy on Carol inside 62.7% ± 9.5%, which is about 53% to 72%. A U-LiRA score of at most 0.20,
   where U-LiRA is the per-example membership test and a high score means "still remembers". Test accuracy at least
   96.4%, no more than 2 points below the retrains.
2. **The start.** The original model gets all 40 of her digits right (100.0%), with a U-LiRA score of 0.950.
3. **After 2 epochs.** Carol is at 65.0%, so 26 of her 40 digits, inside the band. Test accuracy is 96.9%, above the
   floor. U-LiRA is 0.200, exactly on the limit. All three checks pass.
4. **After 3 epochs.** Carol drops to 12.5%, which is 5 digits. That is far below the band, worse than any model that
   never saw her. Test accuracy is 95.2%, now under the floor. FORGET and UTILITY fail.

Look at step 3 again. The pass was not comfortable. The privacy score sat exactly on its limit, and one more epoch moved
Carol by 21 digits. The method reached the band on its way down to over-forgetting, and happened to be inside it at
the moment it was stopped.

### The window is tiny

Lesson 08 tried **46** settings of these methods against the full audit. **One** passed. It was NegGrad+ with α = 0.99, a
learning rate of 0.001 and exactly 2 epochs. It could only be found because, in the lab, the gold band is visible. In
production it is not.

<div class="stats">
<div class="is-bad"><strong>1 of 46</strong><span>settings of the quick fixes passed the audit</span></div>
<div><strong>8% vs 95%</strong><span>of the gap closed by the best gradient ascent and by one Newton step</span></div>
<div class="is-bad"><strong>98% to 10%</strong><span>test accuracy as gradient ascent ran on unchecked</span></div>
<div class="is-good"><strong>65.0%</strong><span>NegGrad+ on Carol at 2 epochs, inside the band, PASS</span></div>
</div>

The 46 settings were 36 for NegGrad+, every mix of three values of α, three learning rates and four epoch counts, and
10 for gradient ascent, two learning rates and five epoch counts. Gradient ascent never passed. By the time Carol had
fallen into the band, everyone else's accuracy had fallen through the floor.

??? deep "Go deeper · the full audit table from Lesson 08"

    | Method | Carol | Test | U-LiRA | FORGET | PRIVACY | UTILITY | Verdict |
    |---|---|---|---|---|---|---|---|
    | Original | 100.0% | 98.0% | 0.950 | FAIL | FAIL | ok | FAIL |
    | Retrain (seed 999) | 62.5% | 98.0% | 0.075 | ok | ok | ok | PASS |
    | Fine-tune, 5 epochs | 100.0% | 98.1% | 0.875 | FAIL | FAIL | ok | FAIL |
    | Gradient ascent, 3 epochs | 95.0% | 98.0% | 0.575 | FAIL | FAIL | ok | FAIL |
    | Gradient ascent, 10 epochs | 27.5% | 68.7% | 0.025 | FAIL | ok | FAIL | FAIL |
    | NegGrad+, 2 epochs | 65.0% | 96.9% | 0.200 | ok | ok | ok | PASS |
    | NegGrad+, 3 epochs | 12.5% | 95.2% | 0.000 | FAIL | ok | FAIL | FAIL |

    Notice gradient ascent at 10 epochs. Its U-LiRA score of 0.025 passes PRIVACY, because a broken model is not
    confident about anything. A low membership score on its own does not mean good forgetting.

<!-- diagram: forgetting-spectrum -->

### Three ways to fail

- **Under-forgetting** (fine-tune, short gradient ascent). Carol is still in there. Fails FORGET and PRIVACY.
- **Collateral damage** (long gradient ascent). The model got worse for everyone. Fails UTILITY.
- **Over-forgetting** (NegGrad+ one epoch too long). Carol is pushed *below* the band, which is as suspicious as leaving
  her above it. Fails FORGET.

??? checkpoint "Checkpoint 2 · A method leaves Carol at 95.0%, test accuracy at 98.0% and U-LiRA at 0.575. Which way did it fail?"
    **Under-forgetting.** 95.0% is far above the band of about 53% to 72%, and 0.575 is well over the privacy limit of
    0.20, so the model still remembers her. Test accuracy is fine, which is typical, since the method barely changed
    anything. This is gradient ascent stopped after 3 epochs.

### What is missing

All three lack two things. One is a **reference** for what a model that never saw Carol would say (not "as wrong as possible"),
and the other is a **stopping rule** that does not need the gold band. [SCRUB](scrub.md) and [Bad Teacher](bad-teacher.md) try to
add them.

## Limits

**The right settings depend on the request.** α, the learning rate and the number of epochs that worked for Carol need
not work for another person, a group of users or a whole class. A new request means a new search.

**The lab can see the answer and production cannot.** Lesson 08 found the passing setting by comparing every candidate
with a gold band built from 12 retrains. If you could afford those retrains in production, you would not need a quick
fix.

**A pass is evidence, not proof.** Even the one passing model was only shown to look like a retrain on three numbers.
It may still hold traces of Carol that a stronger test, such as the relearn attack in
[The unlearning audit](unlearning-audit.md), would find.

**These results come from one small setting.** One network, 8 × 8 digits and a forget set of 40. Gradient ascent on
large language models has the same unbounded loss, which is why methods like NPO (Zhang et al. 2024) bound it, as
[Unlearning in language models](llm-unlearning.md) explains.

??? checkpoint "Checkpoint 3 · NegGrad+ at α = 0.99, a learning rate of 0.001 and 2 epochs passed for Carol. A new request arrives for a different person. Can you reuse those settings and skip the audit?"
    **No.** Those settings were found by looking at Carol's gold band, and the window was one epoch wide. A different
    person sits in a different place in the model, so the same settings may under-forget or over-forget. Without the
    band, you need a stopping rule you can apply in production, and an audit of every result.

!!! tip "What to do in practice"
    - Treat fine-tuning, gradient ascent and NegGrad+ as baselines to compare against, not as finished methods.
    - Never stop at "as wrong as possible". Aim for what a model that never saw the data would say.
    - Use a stopping rule that needs no gold band. One idea is to stop when accuracy on the forget set falls to the
      accuracy on unseen data like it, such as other thick-marker digits. Lesson 08 sets this as a task to test.
    - Always report utility next to forgetting, and audit every request, not just the first.

## In code

??? deep "Go deeper · the three quick fixes in the course library"
    ```python
    from mul import methods
    ft = methods.finetune(original, L.Xr, L.yr, epochs=5)
    ga = methods.gradient_ascent(original, L.Xf, L.yf, epochs=3, lr=3e-4)
    ng = methods.neggrad_plus(original, L.Xr, L.yr, L.Xf, L.yf, epochs=2, alpha=0.99, lr=1e-3)
    ```

    Each call returns the edited model and a record of its cost. `gradient_ascent` is ordinary training with the sign
    of the gradient flipped. `neggrad_plus` minimises \(\alpha L_r - (1 - \alpha) L_f\) in every step, so it descends
    the loss on the retain set while it climbs the loss on the forget set.

## Common mistakes

!!! danger "Mistakes people make"
    - **Pushing the forget-set accuracy to 0%.** The target is the gold band, not zero.
    - **Tuning on the gold band, then claiming it works in production.** In production you cannot see the band.
    - **Reporting forget accuracy without utility.** The fastest way to forget Carol is to forget everything.
    - **Trusting a low membership score alone.** Gradient ascent at 10 epochs scored 0.025 because it had broken the
      model, not because it had forgotten well.
    - **Hoping fine-tuning will fade memorised data.** Carol stayed at 100.0% after 5 epochs.

## Key takeaways

!!! notes "Notes to take"
    - **Approximate unlearning.** A cheap edit to a trained model with no guarantee, so it must be audited.
    - **Gradient ascent.** A Newton step without the curvature. Cheap, natural and unbounded.
    - **The bridge.** On logistic regression, the best gradient-ascent step closed 8% of the gap, one Newton step 95%.
    - **Fine-tune.** Under-forgets. Carol stayed at 100.0% after 5 epochs.
    - **Gradient ascent.** No brake. Test accuracy fell from 98% to 10% with a larger step.
    - **NegGrad+.** Anchors to the retain set. Passed at 2 epochs (65.0%), over-forgot at 3 (12.5%).
    - **The window.** 1 setting of 46 passed, and it was found by looking at the gold band.
    - **Three failures.** Under-forgetting, collateral damage and over-forgetting.
    - **Missing.** A reference for "never saw her" and a stopping rule that needs no band.

## Quiz

```quiz
- q: What is gradient ascent on the forget set?
  options:
    - Training the model to get worse on the forget data
    - Training the model to get better on the forget data
    - Deleting the forget data from the database
  answer: 0
  why: It climbs the loss on the forget set instead of descending it.
- q: Gradient ascent is a Newton step without what?
  options:
    - The curvature (the Hessian)
    - The data
    - The learning rate
  answer: 0
  why: Dropping the Hessian leaves a step size you must guess, and the direction is often wrong.
- q: How many of 46 settings passed the full audit in Lesson 08?
  options:
    - 1
    - 23
    - 46
  answer: 0
  why: Only NegGrad+ at one exact combination of settings passed, and it was found by looking at the gold band.
- q: NegGrad+ ran one epoch too long and pushed Carol to 12.5%, below the gold band. What is that?
  options:
    - Perfect forgetting
    - Over-forgetting, which fails the audit
  answer: 1
  why: A model that never saw Carol does much better than that, so being far worse is suspicious.
- q: What do NegGrad+ and the other quick fixes lack?
  options:
    - A reference for "forgotten" and a stopping rule that works without the gold band
    - A learning rate
    - A training set
  answer: 0
  why: SCRUB and Bad Teacher try to supply a reference; SCRUB+R adds a stopping rule.
- q: Why did fine-tuning on everyone except Carol leave her at 100.0%?
  options:
    - Fine-tuning deleted the wrong rows.
    - Nothing in it pushes away from her, and memorised data fades far too slowly by neglect.
    - The learning rate was zero.
  answer: 1
  why: The model already fits Carol, so training on other data gives it no reason to change its answers on her.
- q: Gradient ascent at 10 epochs scored only 0.025 on U-LiRA, well within the privacy limit. Did it forget well?
  options:
    - Yes, it passed every check.
    - It only failed because of bad luck.
    - No. Test accuracy fell to 68.7%, so the low score came from a broken model.
  answer: 2
  why: A broken model is unsure about everything, so membership tests find nothing. Always read privacy next to utility.
- q: What does the anchor in NegGrad+ do?
  options:
    - It pairs every ascent step on the forget set with a descent step on the retain set, so the rest of the model stays in place.
    - It stops training when the gold band is reached.
    - It removes the forget set from the training data.
  answer: 0
  why: The anchor limits collateral damage, but it does not tell you when to stop.
- q: Why can a network not use the Newton step directly?
  options:
    - Networks have no gradient.
    - Its Hessian is far too big to store and invert, about 29 GB in 32-bit floats even for the course's small network.
    - The Newton step only works on the test set.
  answer: 1
  why: With about 85,000 weights, the Hessian has about 85,000 × 85,000 entries. Gradient ascent drops it and guesses a step size instead.
```

## Try it

!!! levelup "Level up"
    You can now read a quick fix's audit row and name how it failed. Next quest,
    [SCRUB, teacher and student](scrub.md), which adds the missing reference and a rewind to stop at the right point.

- Read the next concept, [SCRUB, teacher and student](scrub.md).
- Run the lesson [08 · Baselines and traps](../lessons/08-approximate-baselines-and-traps.md).
