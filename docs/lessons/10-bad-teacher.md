---
title: "Lesson 10: Bad Teacher"
description: Forgetting by copying a model that knows nothing. It is the cheapest method, and it shows that random is not the same as forgotten.
---

# Lesson 10: Bad Teacher, forgetting by copying a model that knows nothing

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 4 · Approximate unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 6</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb){ .md-button }
</div>

## The story

Bad Teacher (Chundawat et al., AAAI 2023) gives the student an explicit target for the forget set, which is a **second teacher with random weights**. The student copies the original (competent) teacher on part of the retain data, and the random
(incompetent) teacher on Carol, in a single epoch. The question this lesson forces: **is "behaves like a random model"
the same as "behaves like a model that never saw the data"?**

## What you will do

<ol class="steps" markdown>
<li markdown>**Meet the two teachers**: the original model and a freshly initialised one.</li>
<li markdown>**Untrain** with one fast epoch over 30% of \(D_r\), and count the cost.</li>
<li markdown>**Show the result** with the audit.</li>
<li markdown>**Prove it**: compare the shape of the outputs (entropy, confidence) with retrained models.</li>
<li markdown>Check the paper's own metric (ZRF), and sweep 18 settings.</li>
</ol>

## Key results

**Cost.** Retrain: 73,020 example-gradients (100%). SCRUB: 13.6%. **Bad Teacher: 405 (0.6%).**

**On Carol**: 70.0% (inside the band), U-LiRA 0.150, but test accuracy 96.1%, just past the utility tolerance. A near
miss.

**Random is not forgotten** (outputs on Carol's digits):

| Model | Entropy | P(true label) | Top confidence |
|---|---|---|---|
| Original | 0.008 | 0.999 | 0.999 |
| Retrained (mean of 12) | 0.356 | 0.609 | 0.864 |
| Bad Teacher | 0.469 | 0.654 | 0.796 |
| Incompetent teacher | 2.192 | 0.098 | 0.182 |

On the **class** request, a model that never saw a 3 puts essentially zero probability on "3" (6.1 × 10⁻⁷). Bad
Teacher left 0.008. Forget accuracy looked perfect (0.8%), but the privacy test read that leftover as membership and
**failed**.

**The metric trap.** The paper's ZRF score rated Bad Teacher **above the true retrain** on both requests (Carol: 0.582
vs 0.562). Nothing can be more unlearnt than a model that never saw the data, so the metric measures something else.

**Scoreboard**: Carol 1 / 18 passes; class "3" **0 / 18**. No learning rate fixes a wrong target.

## Concepts used here

- [Bad Teacher](../unlearning/bad-teacher.md)
- [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

## Quiz

```quiz
- q: What did Bad Teacher cost compared with a full retrain?
  options:
    - 0.6%
    - 13.6%
    - 100%
  answer: 0
  why: One epoch over 30% of the retain set is very cheap.
- q: Compared with a retrained model, Bad Teacher's outputs on Carol were...
  options:
    - Less confident (higher entropy)
    - Exactly the same
    - Much more confident
  answer: 0
  why: It learnt to behave a bit like the random teacher, not like a competent model that never met her.
- q: On the class request, why did Bad Teacher fail privacy despite 0.8% forget accuracy?
  options:
    - It left a small probability on "3", which a model that never saw 3s would not.
    - It was still 100% right on 3s.
    - The test set was empty.
  answer: 0
  why: That leftover probability looks like membership to the per-example test.
- q: ZRF rated Bad Teacher above the true retrain. What does that tell you?
  options:
    - The metric measures closeness to the random target, not unlearning.
    - Bad Teacher is better than retraining.
  answer: 0
  why: Any metric that a method can beat the gold standard on is measuring something else.
- q: How many of 18 settings passed on the class request?
  options:
    - 0
    - 9
    - 18
  answer: 0
  why: Its target is the wrong shape for a removed class, and no setting fixes that.
```

## Open question → Lesson 11

We now have nine ways to unlearn, each judged with a slightly different table. What does **one fair, repeatable audit**
look like, one we could hand to a regulator?

[Next: Lesson 11, the unlearning audit :material-arrow-right:](11-the-unlearning-audit.md){ .md-button }
