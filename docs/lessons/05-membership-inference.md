---
title: "Lesson 05: Membership inference attacks"
description: Can an outsider tell that Carol was in the training data? Build a membership inference attack, then use it as a forgetting detector.
---

# Lesson 05: Membership inference, can an outsider tell Carol was there?

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 2 · Neural nets: the problem</span><span class="chip" markdown="span">:material-stairs-up: Rung 4</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb){ .md-button }
</div>

## The story

Lesson 04 said the proof of forgetting must be about **behaviour**. Now flip the point of view. Imagine you are an outsider who
can only send inputs and read the model's probabilities. You hold some digits that may or may not have been in training.
Can you tell which ones were? That is a **membership inference attack**. It is a privacy threat, and it is also the
tool every later audit is built on.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the network from Lesson 04.</li>
<li markdown>**Show the issue**: attack every model from Lessons 01 to 04 with a loss threshold.</li>
<li markdown>Build a **stronger, per-example attack** (LiRA / U-LiRA) with 8 shadow models in and 8 out.</li>
<li markdown>**Untrain** with the exact methods already known, and attack again.</li>
<li markdown>**Prove it** with the per-example test.</li>
</ol>

## Key results

**The blunt attack** (Carol's 40 digits against 80 unseen thick-marker digits):

| Model | AUC before | AUC after exact unlearning |
|---|---|---|
| Naive Bayes | 0.53 | 0.40 |
| k-NN, k = 5 | 0.59 | 0.46 |
| Logistic regression | 0.59 | 0.47 |
| RBF SVM | 0.66 | 0.58 |
| Random forest | 0.96 | 0.47 |
| Neural network | 0.71 | 0.48 |

On *typical* training digits against test digits, the network's AUC was only 0.53. Attacks look weak on average and
strong on the right people.

**The per-example attack (U-LiRA).** It was calibrated first. A fresh model trained **with** Carol scored 0.97; one
**without** her scored 0.05. On the original network it flagged **95%** of Carol's digits as members; after retraining,
**5%**. The blunt attack had reached only AUC 0.71 on the same network.

!!! warning "Three cautions for later"
    1. Shadow models must use the **same training recipe** as the target (Lesson 07 shows what goes wrong otherwise).
    2. AUC near 0.5 only means *this* attack found nothing.
    3. AUC far **below** 0.5 is a red flag too, because the forgotten data is treated worse than strangers.

## Concepts used here

- [Membership inference attacks](../unlearning/membership-inference-attacks.md)
- [Loss functions](../ml-basics/loss-functions.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)

## Quiz

```quiz
- q: What clue does the simple attack use?
  options:
    - Lower loss on an example suggests it was in training.
    - The size of the model file
    - The colour of the image
  answer: 0
  why: Models are usually more confident on examples they trained on.
- q: Which model leaked Carol's membership most to the blunt attack?
  options:
    - Naive Bayes
    - Random forest
    - Logistic regression
  answer: 1
  why: The forest's AUC was 0.96; Naive Bayes, which did not memorise her, was 0.53.
- q: On the original network, what share of Carol's digits did U-LiRA flag as members?
  options:
    - About 5%
    - About 50%
    - About 95%
  answer: 2
  why: The per-example test is much sharper than a single loss threshold.
- q: What happened to U-LiRA's member-rate after retraining without Carol?
  options:
    - It fell to about 5%.
    - It stayed at 95%.
    - It rose to 100%.
  answer: 0
  why: The retrained model looks like a model that never met her, from the attacker's view.
- q: Why must members and non-members come from the same kind of data?
  options:
    - Otherwise the attack learns the style (thick or thin) instead of membership.
    - It makes the test faster.
    - The library requires it.
  answer: 0
  why: A fair test compares like with like.
```

## Open question → Lesson 06

The gold standard so far has been "**the** retrained model". But two networks trained on identical data land in
different places, and we just used eight of them as shadow models. What exactly is the target, and how wide is it?

[Next: Lesson 06, retrain and the gold band :material-arrow-right:](06-retrain-and-the-gold-band.md){ .md-button }
