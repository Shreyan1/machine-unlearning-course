---
title: "Lesson 08 · Approximate baselines and traps"
description: Fine-tuning, gradient ascent and NegGrad+ on an already-trained network, tracked against the gold band. One setting in 46 passes.
---

# Lesson 08 · Approximate unlearning, the baselines and their traps

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 4 · Approximate unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 6</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/08-Approximate-Baselines-and-Traps.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/08-Approximate-Baselines-and-Traps.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 35 minutes · 3 checkpoints"
    By the end of this lesson you can

    - show that gradient ascent is a Newton step with the curvature removed, and measure what that costs,
    - run fine-tuning, gradient ascent and NegGrad+ on a trained network and read their audit rows,
    - explain why the one passing setting out of 46 is luck you cannot repeat in production.

## The story

The Newton step of Lesson 02 moved the weights using the deleted points' gradients, scaled by the curvature. A network
has no usable curvature (the Hessian is 29 GB in 32-bit floats even for this toy). Drop it, replace it with a small step size, and what
is left is **gradient ascent**, which trains the model to get *worse* on Carol. This lesson shows why that is both natural and
dangerous.

The stakes are practical. Lesson 07's SISA had to be chosen before training, and most real models were trained as one
big network long ago. A request arrives today, and retraining from scratch is the bill Lesson 06 priced. So teams reach
for a quick edit of the model they already have. Gradient ascent is the most popular of these baselines, and this
lesson tests it and two relatives against the same audit every later method will face.

## What you will do

<ol class="steps" markdown>
<li markdown>Check the bridge on logistic regression. Is "Newton minus curvature" really gradient ascent?</li>
<li markdown>**Untrain** the network with fine-tuning, gradient ascent and NegGrad+, epoch by epoch.</li>
<li markdown>**Show the result** as trajectories against the gold band.</li>
<li markdown>**Prove it** with the audit, using the gold band, U-LiRA and utility.</li>
<li markdown>Sweep 46 settings to see how much luck is involved.</li>
</ol>

## What each step teaches

**Step 1. The bridge.** On logistic regression the exact retrained model is known, so the lesson can measure how much
of the distance to it each method closes. It tries 40 step sizes for gradient ascent and compares the best with one
Newton step. This shows what the curvature was worth before the network is touched.

**Step 2. Untrain, epoch by epoch.** Each method runs for 12 epochs from the original network, and after every epoch
the lesson records accuracy on Carol and on the test set. Fine-tuning trains on everyone else. Gradient ascent climbs
Carol's loss. NegGrad+ does both in every step, with α = 0.99 so that 99% of each step is about the retain set.

**Step 3. Trajectories.** The two plots show where each method goes over time. The question is not only where a method
ends but whether it passes through the band and whether anything would tell you to stop there.

**Step 4. The audit.** Candidate stopping points are scored with the same gate as Lesson 06, plus U-LiRA from Lesson 05.
The gold band comes from 12 retrains without Carol.

**Step 5. The sweep.** 36 settings of NegGrad+ (three values of α, three learning rates and four epoch counts) and 10
of gradient ascent (two learning rates and five epoch counts) are audited, to count how many pass.

## Key results

<div class="stats">
<div class="is-bad"><strong>8% vs 95%</strong><span>of the gap closed by the best gradient ascent and by one Newton step</span></div>
<div class="is-bad"><strong>98% to 10%</strong><span>test accuracy as gradient ascent ran on with a larger step</span></div>
<div class="is-good"><strong>65.0%</strong><span>NegGrad+ on Carol at 2 epochs, PASS</span></div>
<div class="is-bad"><strong>1 of 46</strong><span>settings that passed the audit</span></div>
</div>

**The bridge.** On logistic regression, the best gradient-ascent step closed only **8%** of the gap; one Newton step
closed 95%. The curvature is most of the answer.

Too small a step made no progress and too large a step overshot. Even the best step was poor, because the deleted
points' raw gradient points in the wrong direction. The curvature is what turns it towards the retrained model.

**Gradient ascent with a larger step** (test accuracy after each epoch). 98%, 89%, 66%, 44%, 31%, ... 10%. The fastest
way to forget Carol is to forget everything.

With ten classes of digit, 10% is what random guessing scores. Nothing in "make Carol's loss bigger" says stop at the
band, and cross-entropy can grow without limit, so the method keeps going until the whole model collapses.

??? checkpoint "Checkpoint 1 · Gradient ascent's test accuracy stopped falling at 10% and stayed there. What does that tell you about the model?"
    **It has forgotten everything, not just Carol.** With ten classes, 10% is the score of a model that guesses. The
    method has no brake, so it pushed past the band and past any useful model, until there was nothing left to lose.

**The audit** (a gold band of 62.7% ± 9.5% on Carol, U-LiRA ≤ 0.20 and test accuracy ≥ 96.4%).

| Method | Carol | Test | U-LiRA | Verdict |
|---|---|---|---|---|
| Original | 100.0% | 98.0% | 0.950 | FAIL |
| Retrain | 62.5% | 98.0% | 0.075 | PASS |
| Fine-tune (5 epochs) | 100.0% | 98.1% | 0.875 | FAIL, under-forgets |
| Gradient ascent (10 epochs) | 27.5% | 68.7% | 0.025 | FAIL, utility |
| NegGrad+ (2 epochs) | 65.0% | 96.9% | 0.200 | **PASS** |
| NegGrad+ (3 epochs) | 12.5% | 95.2% | 0.000 | FAIL, over-forgets |

Read the rows that matter. **Fine-tune** left Carol at 100.0% and U-LiRA at 0.875, so it still remembers her and fails
FORGET and PRIVACY. **Gradient ascent at 10 epochs** passes PRIVACY with 0.025, but only because a broken model is
unsure about everything, and its 68.7% test accuracy fails UTILITY. **NegGrad+ at 2 epochs** passes, with 26 of
Carol's 40 digits inside the band, test accuracy just above the floor and U-LiRA exactly on the limit. **NegGrad+ at 3
epochs** dropped her to 5 digits and test accuracy under the floor. One epoch moved Carol by 21 digits.

??? deep "Go deeper · the other audit row, gradient ascent at 3 epochs"
    The notebook also scores gradient ascent stopped after 3 epochs. It left Carol at 95.0%, test accuracy at 98.0%
    and U-LiRA at 0.575. That fails FORGET and PRIVACY, the same under-forgetting as fine-tuning. Together with the
    10-epoch row, it shows gradient ascent has no good place to stop. Early, Carol is still there. Late, everyone else
    is gone.

??? checkpoint "Checkpoint 2 · NegGrad+ at 2 epochs scored U-LiRA 0.200 against a limit of 0.20. How comfortable is that pass?"
    **Not comfortable at all.** It sits exactly on the limit, and test accuracy at 96.9% is only half a point above the
    floor of 96.4%. One more epoch failed two checks. The method was not aiming at the band. It passed through it on
    its way down, and it happened to be inside at the moment it was stopped.

**One setting in 46 passed.** NegGrad+ with α = 0.99, learning rate 0.001, exactly 2 epochs. It was found only because
the gold band was visible. In production it is not.

Gradient ascent never passed in the sweep. By the time Carol fell into the band, everyone else's accuracy had fallen
through the floor. The two things missing from all three methods are a reference for what a model that never saw
Carol would say, and a stopping rule that does not need the gold band.

??? checkpoint "Checkpoint 3 · A colleague proposes always running NegGrad+ at α = 0.99, a learning rate of 0.001 and 2 epochs, since it passed. What is wrong with that?"
    **The setting was found by looking at Carol's gold band, and the window was one epoch wide.** Another request,
    another person or another model can need different settings, and in production there is no band to check against.
    Each result still needs a stopping rule and an audit.

## Limits of this lesson

**One request.** Every result is for Carol. The notebook's tasks ask what happens when the target is a whole class,
where the band sits at 0%.

**A small grid.** 46 settings is a modest search. A finer grid might find a few more passes, but each would still be
found by looking at the band.

**One stopping rule not tried.** Stopping when Carol's accuracy falls to the accuracy on unseen digits in her style is
a rule you could use in production. The lesson sets it as a task rather than testing it.

**One small network.** For large language models gradient ascent has the same unbounded loss, which is why NPO
(Zhang et al. 2024) bounds it, as [Lesson 16](16-llm-unlearning.md) shows.

## Concepts used here

- [Quick fixes and their traps](../unlearning/approximate-unlearning.md)
- [Gradient descent](../ml-basics/gradient-descent.md)
- [The gold band](../unlearning/gold-band.md)

## Notes to take

!!! notes "Notes to take"
    - **Gradient ascent.** A Newton step without the curvature. Climbs the forget set's loss with a guessed step size.
    - **The bridge.** On logistic regression, best gradient ascent closed 8% of the gap, one Newton step 95%.
    - **No brake.** With a larger step, test accuracy fell from 98% to 10%, the score of guessing.
    - **Fine-tune.** Under-forgets. Carol at 100.0% after 5 epochs, U-LiRA 0.875.
    - **NegGrad+.** Ascent on Carol and descent on everyone else, with α = 0.99.
    - **Knife edge.** NegGrad+ passed at 2 epochs (65.0%) and over-forgot at 3 (12.5%).
    - **The sweep.** 1 setting of 46 passed, found only by looking at the band.
    - **Trap.** A low U-LiRA score from a broken model is not good forgetting.
    - **Missing.** A reference for "never saw her" and a stopping rule that needs no band.

## Quiz

```quiz
- q: Gradient ascent is the Newton step without which ingredient?
  options:
    - The curvature (Hessian)
    - The gradient
    - The data
  answer: 0
  why: Dropping the Hessian leaves a step size to guess and a direction that is often wrong.
- q: On logistic regression, how much of the gap did the best gradient-ascent step close?
  options:
    - 8%
    - 50%
    - 95%
  answer: 0
  why: One Newton step closed 95%; without curvature, gradient ascent managed only 8%.
- q: Fine-tuning on the retain set for 5 epochs left Carol at what accuracy?
  options:
    - 100.0%
    - 62.5%
    - 27.5%
  answer: 0
  why: Forgetting by neglect is far too slow for memorised data.
- q: Why did NegGrad+ at 3 epochs fail?
  options:
    - It over-forgot Carol, pushing her below the band.
    - It did not change the model.
    - It crashed.
  answer: 0
  why: Pushing her to 12.5% is as suspicious as leaving her at 100%.
- q: What are the two things missing from all three methods?
  options:
    - A reference for "forgotten" and a stopping rule that works without the gold band
    - A GPU and more data
    - A test set and a learning rate
  answer: 0
  why: SCRUB adds a reference; SCRUB+R adds a stopping rule.
- q: Gradient ascent at 10 epochs passed PRIVACY with a U-LiRA score of 0.025. Why did it still fail?
  options:
    - Its test accuracy fell to 68.7%, below the utility floor, because the model was broken.
    - The privacy limit was set too low.
    - It took too long to run.
  answer: 0
  why: A broken model is unsure about everything, so the membership test finds nothing. Read privacy next to utility.
- q: Why could the one passing NegGrad+ setting be found in this lesson but not in production?
  options:
    - Production models are too big for NegGrad+.
    - In the lab the gold band from 12 retrains was visible, and in production it is not.
    - Production data has no forget set.
  answer: 1
  why: Choosing the setting by comparing with the band is using the answer. Without it, you need a stopping rule.
- q: What does the anchor in NegGrad+ add to plain gradient ascent?
  options:
    - A rule that stops at the band
    - A copy of the original model as a teacher
    - A descent step on everyone else in every step, which keeps the rest of the model in place
  answer: 2
  why: The anchor limits collateral damage, which is why NegGrad+ is the only one of the three that passed.
```

## Open question → Lesson 09

!!! levelup "Level up"
    You can now run the three quick fixes, read their audit rows and explain why one lucky pass is not a method. Next
    quest, [Lesson 09 · SCRUB](09-scrub.md), which adds a reference model and a rewind.

Gradient ascent asks "be **wrong** on Carol". The gold standard is not wrong on Carol; it is *uninformed* about her.
What if we used the original model as a reference, stayed identical to it on everyone else, moved away from it on
Carol, and kept checkpoints so we could rewind?

[On to Lesson 09, SCRUB :material-arrow-right:](09-scrub.md){ .md-button }
