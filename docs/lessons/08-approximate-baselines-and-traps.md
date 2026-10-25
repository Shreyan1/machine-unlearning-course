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

## The story

The Newton step of Lesson 02 moved the weights using the deleted points' gradients, scaled by the curvature. A network
has no usable curvature (the Hessian is 29 GB even for this toy). Drop it, replace it with a small step size, and what
is left is **gradient ascent**: train the model to get *worse* on Carol. This lesson shows why that is both natural and
dangerous.

## What you will do

<ol class="steps" markdown>
<li markdown>Check the bridge on logistic regression. Is "Newton minus curvature" really gradient ascent?</li>
<li markdown>**Untrain** the network with fine-tuning, gradient ascent and NegGrad+, epoch by epoch.</li>
<li markdown>**Show the result** as trajectories against the gold band.</li>
<li markdown>**Prove it** with the audit, using the gold band, U-LiRA and utility.</li>
<li markdown>Sweep 46 settings to see how much luck is involved.</li>
</ol>

## Key results

**The bridge.** On logistic regression, the best gradient-ascent step closed only **8%** of the gap; one Newton step
closed 95%. The curvature is most of the answer.

**Gradient ascent with a larger step** (test accuracy after each epoch): 98%, 89%, 66%, 44%, 31%, ... 10%. The fastest
way to forget Carol is to forget everything.

**The audit** (gold band: Carol 62.7% ± 9.5%, U-LiRA ≤ 0.20, test ≥ 96.4%).

| Method | Carol | Test | U-LiRA | Verdict |
|---|---|---|---|---|
| Original | 100.0% | 98.0% | 0.950 | FAIL |
| Retrain | 62.5% | 98.0% | 0.075 | PASS |
| Fine-tune (5 epochs) | 100.0% | 98.1% | 0.875 | FAIL, under-forgets |
| Gradient ascent (10 epochs) | 27.5% | 68.7% | 0.025 | FAIL, utility |
| NegGrad+ (2 epochs) | 65.0% | 96.9% | 0.200 | **PASS** |
| NegGrad+ (3 epochs) | 12.5% | 95.2% | 0.000 | FAIL, over-forgets |

**One setting in 46 passed**: NegGrad+ with α = 0.99, learning rate 0.001, exactly 2 epochs. It was found only because
the gold band was visible. In production it is not.

## Concepts used here

- [Quick fixes and their traps](../unlearning/approximate-unlearning.md)
- [Gradient descent](../ml-basics/gradient-descent.md)
- [The gold band](../unlearning/gold-band.md)

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
```

## Open question → Lesson 09

Gradient ascent asks "be **wrong** on Carol". The gold standard is not wrong on Carol; it is *uninformed* about her.
What if we used the original model as a reference, stayed identical to it on everyone else, moved away from it on
Carol, and kept checkpoints so we could rewind?

[On to Lesson 09, SCRUB :material-arrow-right:](09-scrub.md){ .md-button }
