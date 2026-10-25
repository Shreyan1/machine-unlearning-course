---
title: "Lesson 12 · Right to be forgotten and fairness"
description: Erasure requests on real census data. One request is easy; a skewed wave of requests quietly makes the model unfair.
---

# Lesson 12 · The right to be forgotten on real data, and who pays for it

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 8</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb){ .md-button }
</div>

## The story

Real data is **personal**, and requests arrive **continuously and not at random**. This lesson uses the UCI Adult census
dataset (30,162 people) and an income model, a stand-in for a credit or hiring model. Forgetting one person is a privacy
question. Forgetting many people from one group becomes a **fairness** question.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** logistic regression and measure fairness with equal opportunity (true-positive rate per group).</li>
<li markdown>**Show the issue**: one request ("Alice"), then a growing wave of requests from high-earning women.</li>
<li markdown>**Untrain** with Newton steps and exact retrains; compare with deleting random people.</li>
<li markdown>Repeat on a neural model with approximate methods, adding a **FAIRNESS** check.</li>
<li markdown>**Mitigate** with per-group thresholds fitted on retain data only.</li>
</ol>

## Key results

**Baseline**: accuracy 85.7%; TPR women 50.6%, men 63.5%; gap 12.9 points. Only 778 women in training earn over $50K.

**One request**: removing Alice with one Newton step landed within 2.2 × 10⁻⁶ of the retrained weights. Solved.

**A skewed wave** (exact retrains).

| Deleted | Accuracy | TPR women (random deletions) | TPR women (skewed deletions) | TPR gap (skewed) |
|---|---|---|---|---|
| 0 | 85.7% | 50.6% | 50.6% | 12.9 |
| 233 | 85.7% | 50.9% | 44.6% | 18.9 |
| 466 | 85.2% | 51.2% | 31.1% | 32.3 |
| 583 | 85.0% | 51.2% | 22.8% | 40.4 |

Accuracy barely moves. **Perfect unlearning faithfully reproduces whatever bias the deletions introduce.**

**Methods can add their own bias** (neural model, 233 women deleted): NegGrad+ pushed the women's TPR from 53.6% to
**2.4%**; gradient ascent hurt everyone. Fine-tuning passed the whole gate, because tabular data is memorised far less
than Carol's digits. Random seeds alone moved the women's TPR between about 42% and 61%.

**Mitigation**: per-group thresholds raised the women's TPR from 31.1% to 53.3% with accuracy 85.5%; the men's TPR fell
from 63.5% to 59.4%. That trade-off needs an owner.

## Concepts used here

- [Erasure requests and fairness](../unlearning/fairness-and-erasure.md)
- [Logistic regression](../ml-basics/logistic-regression.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)

## Quiz

```quiz
- q: As high-earning women were deleted, what did overall accuracy do?
  options:
    - Barely moved
    - Collapsed
    - Rose sharply
  answer: 0
  why: It stayed near 85%, so accuracy dashboards miss the problem entirely.
- q: Deleting the same number of random people changed the women's TPR by...
  options:
    - Almost nothing
    - About 30 points
    - It fell to 0%
  answer: 0
  why: Only group-skewed deletions shift the model for that group.
- q: Were the fairness drops caused by bad unlearning?
  options:
    - No; they happened with exact retraining.
    - Yes; the Newton step was wrong.
  answer: 0
  why: The model faithfully became what the remaining data says.
- q: Which method created a new, method-made bias?
  options:
    - NegGrad+
    - Exact retraining
    - Fine-tuning
  answer: 0
  why: Pushing away from a forget set of only high-earning women taught the model that such women earn less.
- q: Why did fine-tuning pass the gate here but fail on Carol in Lesson 08?
  options:
    - Tabular census data is memorised far less than Carol's digits.
    - Fine-tuning was run for longer.
    - The gate was turned off.
  answer: 0
  why: How much a model memorised decides which methods work, so re-audit for every new kind of data.
```

## Open question → Lesson 13

Here each person was one row among 21,000. What happens when a person *is* the class, as in face recognition, and they
withdraw consent?

[On to Lesson 13, consent withdrawal in face recognition :material-arrow-right:](13-consent-withdrawal-face-recognition.md){ .md-button }
