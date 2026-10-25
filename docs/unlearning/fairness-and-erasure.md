---
title: Erasure requests and fairness
description: When the people who ask to be deleted come mostly from one group, even perfect unlearning can make a model unfair to that group.
---

# Erasure requests and fairness

This is a **Responsible AI** problem as well as a privacy problem. A system must honor individual requests while
checking whether the resulting model treats groups fairly.

!!! oneline "In one line"
    When deletion requests come mostly from **one group**, even perfect unlearning can quietly make the model unfair to
    that group, and accuracy dashboards will not notice.

## Why it matters

Forgetting one person is a privacy question. Forgetting *many* people, if they are mostly from one group, becomes a
**fairness** question. Under GDPR, a drop in model quality is not a reason to refuse an erasure request. But you can,
and for high-risk systems arguably must, **monitor and fix** the effect.

## A simple example

A school bases next year's plans on who attends this year. If most of the girls who excel at maths leave, the school's
records will suggest that girls rarely excel at maths, and it may plan fewer advanced classes for them. Nothing in the
records is wrong; the data that is left just tells a skewed story.

## How it works

<!-- diagram: fairness-and-erasure -->

Lesson 12 uses the **UCI Adult census data** (30,162 people) and an income model, a stand-in for a credit or hiring
model. Fairness is measured with **equal opportunity**: among people who really earn more than $50K, how often does the
model say so (the true-positive rate, TPR), for women and for men?

### Before any deletions

- Accuracy 85.7%; TPR for women 50.6%, for men 63.5%; a gap of 12.9 points that comes from the data.
- Only **778 women** in the training set earn more than $50K.

### One request is easy

"Alice", a high-earning woman, asks to be erased. One Newton step lands essentially on the retrained model (weight
difference 2.2 × 10⁻⁶). For one request, this is a solved problem.

### A wave of requests is not

Suppose a growing share of **high-earning women** ask to be deleted. As a control, the same number of random people
are deleted.

| People deleted | Accuracy (skewed) | TPR women (random) | TPR women (skewed) |
|---|---|---|---|
| 0 | 85.7% | 50.6% | 50.6% |
| 233 | 85.7% | 50.9% | 44.6% |
| 466 | 85.2% | 51.2% | 31.1% |
| 583 | 85.0% | 51.2% | 22.8% |

Accuracy barely moves. The women's TPR collapses. And these are **exact** retrains. Perfect unlearning faithfully reproduces whatever bias the deletions introduce.

### Some methods add their own bias

With a neural model and 233 deleted women, **NegGrad+** pushed the women's TPR from 54% to about **2%**. It did not just
remove 233 people; it taught the model that *women like them* earn less. That is a new, **method-made bias**. Plain
fine-tuning, by contrast, passed every check here, because tabular data is memorised far less than Carol's digits.

### Fixing it

Per-group decision thresholds (fairlearn's `ThresholdOptimizer`), fitted only on the retain data, brought the women's
TPR back from 31.1% to 53.3%, at no cost in accuracy. The men's TPR dropped about four points, a trade-off someone has
to own. Some sectors restrict using the sensitive attribute at decision time, so reweighting or other methods may be
needed instead.

!!! tip "Add FAIRNESS to the audit"
    Track a per-group metric across the deletion log, and judge it against **several** retrained references. In
    Lesson 12, random seeds alone moved the women's TPR between about 42% and 61%.

## Common mistakes

!!! danger "Mistakes people make"
    - **Watching only accuracy.** It did not move while the women's TPR collapsed.
    - **Assuming exact unlearning is fair.** It reproduces the bias of the remaining data.
    - **Using "push away" methods on a one-group forget set.** They can create new bias.

## Key takeaways

- Erasure requests are not random; group-skewed deletions shift the model for that group.
- Accuracy dashboards miss it; per-group metrics across the deletion log catch it.
- Gradient ascent and NegGrad+ can add a method-made bias.
- Mitigate with retain data only, and record the decision.

## Quiz

```quiz
- q: Why can erasure requests become a fairness problem?
  options:
    - The people who ask may come mostly from one group.
    - Erasure always deletes the test set.
    - Fairness metrics cannot be computed after deletion.
  answer: 0
  why: If the data that remains under-represents a group, the model learns a skewed picture of it.
- q: As high-earning women were deleted, what happened to overall accuracy?
  options:
    - It barely moved.
    - It collapsed.
    - It went up sharply.
  answer: 0
  why: Accuracy stayed near 85%, which is why accuracy monitoring misses the problem.
- q: Were the fairness drops caused by a faulty unlearning method?
  options:
    - No; they happened with exact retraining too.
    - Yes; exact retraining is biased.
  answer: 0
  why: Exact unlearning faithfully gives the model you would train on the data that is left.
- q: What did NegGrad+ do to the women's true-positive rate?
  options:
    - Pushed it down to about 2%, creating a new bias
    - Raised it to 90%
    - Left it unchanged
  answer: 0
  why: Pushing away from a forget set made only of high-earning women taught the model that such women earn less.
- q: What data should a fairness fix use after unlearning?
  options:
    - Only the retain data
    - The deleted people's data
    - The test set labels
  answer: 0
  why: Using the deleted people's data would quietly re-use what they asked to remove.
```

## Try it

- Read the next concept, [Consent and face recognition](consent-and-face-recognition.md).
- Run the lesson [12 · Right to be forgotten and fairness](../lessons/12-right-to-be-forgotten-and-fairness.md).
