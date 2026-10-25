---
title: "Lesson 13: Consent withdrawal in face recognition"
description: Remove a person from a classical and a neural face-ID system, prove it and learn that unlearning removes memory, not capability.
---

# Lesson 13: Consent withdrawn, forgetting a face

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 8</span></div>

<div class="buttons" markdown>
[:simple-googlecolab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb){ .md-button }
</div>

## The story

Dana works in an office that uses face recognition for door access. She leaves and **withdraws her consent**. Face
templates are biometric data (GDPR Art. 9); consent can be withdrawn at any time (Art. 7(3)), and erasure follows.
In face recognition, a person is not one row; **a person is a class**. The lesson uses the Olivetti faces dataset
(40 people, 10 photos each).

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a classical face-ID system that uses eigenfaces (PCA) plus nearest neighbour.</li>
<li markdown>**Show the issue**: Dana is inside the face space itself, not just the gallery.</li>
<li markdown>**Untrain** exactly, by subtracting her from PCA's sums and deleting her templates.</li>
<li markdown>Repeat on a neural face classifier with the approximate methods.</li>
<li markdown>**Prove it**, then test memory against capability by enrolling her again.</li>
</ol>

## Key results

**Dana is in the face space.** Reconstruction error of her photos: **0.264** in a face space built with her, **0.383**
without her. Across all 40 people, leaving someone out raised their error by 41% on average.

**Exact removal (classical).** After subtracting her, the eigenfaces matched a from-scratch system exactly (|cos| =
1.000000000000), with identical predictions on every test photo. Her reconstruction error became 0.383, the same as a
never-saw-Dana system.

**Neural system** (a class request):

| Method | Forget accuracy | Test accuracy | Verdict |
|---|---|---|---|
| Retrain | 0.0% | 93.2% | PASS |
| NegGrad+, SCRUB, Bad Teacher | 0.0% | 92.3% to 93.2% | PASS |
| Fine-tune, gradient ascent | 14.3%, 100.0% | 82.1%, 93.2% | FAIL |

**Memory versus capability.** Enrol Dana again from 3 new photos and try to identify her 7 deleted ones:

| Model | Matched to her new template |
|---|---|
| Models that never saw Dana (mean of 12) | 83% |
| Retrained, original, fine-tune, gradient ascent | 100% |
| NegGrad+ / SCRUB / Bad Teacher | 71% / 86% / 86% |

Even models that never saw a single photo of her recognise her after re-enrolment. That is the face model's job.
What protects Dana is **deleting her templates and refusing re-enrolment**, using a non-biometric key such as her
employee ID.

## Concepts used here

- [Consent and face recognition](../unlearning/consent-and-face-recognition.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)
- [Neural networks](../ml-basics/neural-networks.md)

## Quiz

```quiz
- q: In face recognition, what is a person to the model?
  options:
    - A class
    - One row among thousands
    - A test example
  answer: 0
  why: The model is built to recognise that person, so their photos shape it deeply.
- q: How did the reconstruction test show Dana was inside the face space?
  options:
    - Her photos were reconstructed better by a face space built with her.
    - Her name was stored in the model.
    - The model refused to load.
  answer: 0
  why: Error was 0.264 with her and 0.383 without; the face space "knows" her face.
- q: Why could eigenfaces forget Dana exactly?
  options:
    - PCA's covariance is built from sums that can be subtracted.
    - Eigenfaces store no numbers.
    - She was never enrolled.
  answer: 0
  why: It is the same summation trick as Naive Bayes in Lesson 01.
- q: After re-enrolment, models that never saw Dana matched her deleted photos about 83% of the time. Why?
  options:
    - Recognising new faces is the model's capability, not a memory of her.
    - They secretly trained on her.
    - The test was broken.
  answer: 0
  why: Unlearning removes memory; it cannot remove the ability to recognise an enrolled face.
- q: What actually stops Dana being recognised again?
  options:
    - Deleting her templates and blocking re-enrolment with a non-biometric key
    - Gradient ascent
    - A list of her face embeddings
  answer: 0
  why: A face-based block list would itself process her biometric data.
```

## Open question → Lesson 14

Dana's photos were legitimate data she asked to remove. What if the data that must go is **malicious**, planted to make
the model misbehave, and we only find *some* of it?

[Next: Lesson 14, poisoned data and backdoors :material-arrow-right:](14-poisoned-data-and-backdoors.md){ .md-button }
