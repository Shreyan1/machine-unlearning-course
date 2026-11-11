---
title: "Lesson 13 · Consent withdrawal in face recognition"
description: Remove a person from a classical and a neural face-ID system, prove it and learn that unlearning removes memory, not capability.
---

# Lesson 13 · Consent withdrawn, forgetting a face

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 8</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 10 minutes · 3 checkpoints"
    By the end of this lesson you can

    - show with a reconstruction test that a person lives inside the face reader, not just the gallery,
    - remove them exactly from an eigenface system and approximately from a neural one,
    - explain why models that never saw her can still recognise her, and what really protects her.

## The story

Dana works in an office that uses face recognition for door access. She leaves and **withdraws her consent**. Face
templates are biometric data (GDPR Art. 9); consent can be withdrawn at any time (Art. 7(3)), and erasure follows.
In face recognition, a person is not one row; **a person is a class**. The lesson uses the Olivetti faces dataset
(40 people, 10 photos each).

The photos are shrunk to 32 × 32 pixels, and Dana has 7 in training and 3 in the test set. In Lesson 12 each person
was one row among 21,000, and one row barely moved the model. Here the system was built to recognise Dana herself. The
stakes are high too. In FTC v. Everalbum (2021) the company had to delete the face-recognition models built from its
users' photos, not only the photos.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a classical face-ID system that uses eigenfaces (PCA) plus nearest neighbour.</li>
<li markdown>**Show the issue.** Dana is inside the face space itself, not just the gallery.</li>
<li markdown>**Untrain** exactly, by subtracting her from PCA's sums and deleting her templates.</li>
<li markdown>Repeat on a neural face classifier with the approximate methods.</li>
<li markdown>**Prove it**, then test memory against capability by enrolling her again.</li>
</ol>

## What each step teaches

**Train.** PCA on the 280 training photos gives 40 [eigenfaces](../start-here/glossary.md#e), the main patterns in
which faces vary. Each enrolled photo becomes a template, its 40 coordinates in that face space. A new photo goes to
the person with the nearest template. The system gets 90.8% of all test photos right and 2 of Dana's 3. The key detail
is that PCA is computed from sums, which sets up exact removal later.

**Show the issue.** The reconstruction test squeezes a photo into the face space and rebuilds it. The lower the error,
the better the face space knows that face. Running it for every person, with and without them, shows that each person
is part of the basis. This step teaches why deleting templates is not enough.

**Untrain exactly.** Subtract Dana's 7 photos from the sums, work out the eigenfaces again and delete her templates.
This is the [summation form](../start-here/glossary.md#s) from Lesson 01, now applied to a face reader.

??? deep "Go deeper · what is subtracted"
    PCA needs only three totals, the number of photos \(n\), the sum of photos \(S_1 = \sum x\) and the sum of outer
    products \(S_2 = \sum x x^\top\). The covariance is \(S_2 / n - \mu \mu^\top\) with \(\mu = S_1 / n\). Removing
    Dana takes her 7 photos out of all three totals, which leaves exactly what a system trained without her would
    have. The cost is one 1024 × 1024 eigen-decomposition and re-embedding the gallery.

**Repeat on a neural system.** A network (1024 → 256 → 128 → 40) classifies the 40 people. Forgetting Dana is a
**class** request, audited as in Lesson 11. This step shows which approximate methods hit a clear target.

**Prove it, then test capability.** Enrol Dana again from her 3 test photos, using the network's hidden layer, the
[embedding](../start-here/glossary.md#e), as a real door system would. Then try to match her 7 deleted photos. This step
separates what unlearning can remove from what it cannot.

## Key results

<div class="stats">
<div class="is-bad"><strong>0.264</strong><span>Dana's error with her in the face space, 0.383 without</span></div>
<div class="is-good"><strong>Identical</strong><span>predictions after exact removal and from scratch</span></div>
<div class="is-good"><strong>0.0%</strong><span>Dana recognised after NegGrad+, SCRUB or Bad Teacher</span></div>
<div><strong>83%</strong><span>her deleted photos matched by models that never saw her</span></div>
</div>

**Dana is in the face space.** The reconstruction error of her photos was **0.264** in a face space built with her and **0.383**
without her. Across all 40 people, leaving someone out raised their error by 41% on average.

The smallest rise for anyone was 14% and the largest 82%. Dana's rose by almost half (0.383 ÷ 0.264 ≈ 1.45). Every
single person is reconstructed better by a face space that saw them.

??? checkpoint "Checkpoint 1 · Dana's error rose by about 45% when she was left out, and the smallest rise among the 40 people was 14%. Why compare each person with themselves rather than with each other?"
    **Because some faces are simply more typical than others.** A typical face is rebuilt well even by a face space
    that never saw it, so its rise is small. Comparing Dana's raw error with someone else's would mix up how typical
    each face is with how much the face space learnt from it. The same person, with and without, isolates the
    second.

**Exact removal (classical).** After subtracting her, the eigenfaces matched a from-scratch system exactly (|cos| =
1.000000000000), with identical predictions on every test photo. Her reconstruction error became 0.383, the same as a
never-saw-Dana system.

Her 3 test photos were then matched to another person. A real door would also use a similarity threshold, so she would
simply not be recognised.

**Neural system** (a class request).

| Method | Forget accuracy | Test accuracy | Verdict |
|---|---|---|---|
| Retrain | 0.0% | 93.2% | PASS |
| NegGrad+, SCRUB, Bad Teacher | 0.0% | 92.3% to 93.2% | PASS |
| Fine-tune, gradient ascent | 14.3%, 100.0% | 82.1%, 93.2% | FAIL |

The target is clear. A network that never saw Dana has no output that fits her, so her forget accuracy is 0%. The
three anchored methods hit it without hurting anyone else. Fine-tuning still got 1 of her 7 photos right and lost ten
points of test accuracy. Gradient ascent at its defaults still recognised all 7, so it did not forget at all.

**Memory versus capability.** Enrol Dana again from 3 new photos and try to identify her 7 deleted ones.

| Model | Matched to her new template |
|---|---|
| Models that never saw Dana (mean of 12) | 83% |
| Retrained, original, fine-tune, gradient ascent | 100% |
| NegGrad+ / SCRUB / Bad Teacher | 71% / 86% / 86% |

Even models that never saw a single photo of her recognise her after re-enrolment. That is the face model's job.
What protects Dana is **deleting her templates and refusing re-enrolment**, using a non-biometric key such as her
employee ID.

Read the first row closely. The 12 models that never saw Dana matched between 3 and 7 of her 7 photos. So every
unlearnt model, at 5 to 7 of 7, sits inside the range of honest models. Nothing is left to unlearn. Recognising a
face from a fresh template is the skill a face model is built for.

??? checkpoint "Checkpoint 2 · A manager asks you to keep unlearning until the model matches none of Dana's photos after re-enrolment. Is that a sensible target?"
    **No.** Models that never saw her matched 3 to 7 of her 7 photos, 83% on average. A match after
    re-enrolment is the skill the model is built for, not a leftover memory, so a target of none asks for a model
    worse than one that never saw her. Stop re-enrolment with process, not with more unlearning.

The lesson also ran the relearn attack. The 12 never-saw-Dana models relearned her in 2 to 6 steps, and the unlearnt
models in 0 to 15. Learning one more face from a few photos is what a good face model should do, so for an identity
the relearn test cannot separate memory from capability. The reconstruction test and U-LiRA can.

??? checkpoint "Checkpoint 3 · Which of the three steps (delete templates, unlearn, block re-enrolment) did the lesson's tests actually check?"
    **Only the first two.** The reconstruction test, the audit and U-LiRA show the templates and the memory are gone.
    No model test can show that re-enrolment is blocked. That is a process with its own evidence, such as the
    do-not-enrol entry keyed on her employee ID.

## Limits of this lesson

**A small dataset.** 40 people with 10 photos each, at 32 × 32 pixels. Real face systems are far larger, so the numbers
will differ, though the idea carries over.

**Few photos per test.** With 7 deleted photos, each is worth about 14 points, and the never-saw-her models ranged from
43% to 100%. Small changes in re-identification mean little.

**Default settings.** Fine-tuning and gradient ascent were run at their defaults. Different settings might change
their results, but would not change the lesson about capability.

**Process is out of scope.** Blocking re-enrolment is described, not tested.

## Concepts used here

- [Consent and face recognition](../unlearning/consent-and-face-recognition.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)
- [Neural networks](../ml-basics/neural-networks.md)

## Notes to take

!!! notes "Notes to take"
    - **A person is a class.** In face ID, Dana's photos shape the face reader, not just one output.
    - **Proof.** Her reconstruction error was 0.264 with her and 0.383 without. Everyone rose by 14% to 82%.
    - **Exact for eigenfaces.** PCA uses sums, so subtract her and the eigenfaces match a from-scratch system.
    - **Neural.** A class request. NegGrad+, SCRUB and Bad Teacher passed at 0.0% on her photos.
    - **Capability.** Models that never saw her still matched 83% of her photos after re-enrolment.
    - **Relearn is blind here.** Never-saw-her models relearned her in 2 to 6 steps.
    - **Procedure.** Delete templates and images, unlearn or retrain, block re-enrolment with a non-biometric key.

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
- q: Why is forgetting Dana from the neural classifier a class request?
  options:
    - She is one of the 40 labels, so every example of that label must go.
    - Her photos are in a separate file.
    - The network has only one class.
  answer: 0
  why: A network that never saw her has no output for her, so the target forget accuracy is exactly 0%.
- q: Gradient ascent at its defaults still recognised all 7 of Dana's training photos. What was its verdict?
  options:
    - PASS, because test accuracy stayed at 93.2%
    - PASS, because it is an approximate method
    - FAIL, because it did not forget her
  answer: 2
  why: Keeping utility is not enough. Its forget accuracy stayed at 100%, the same as the original.
- q: Why did the relearn test fail to separate unlearnt models from honest ones here?
  options:
    - The test was given too few steps.
    - Every good face model learns one more face quickly, including models that never saw her.
    - The relearn test only works on text.
  answer: 1
  why: Never-saw-Dana models relearned her in 2 to 6 steps. For an identity, use the reconstruction test or U-LiRA instead.
```

## Open question → Lesson 14

!!! levelup "Level up"
    You can now remove a person from a face system, prove it and explain why the step that protects her most is a
    process. Next quest, [Lesson 14 · Poisoned data and backdoors](14-poisoned-data-and-backdoors.md), where the data to
    remove was planted by an attacker.

Dana's photos were legitimate data she asked to remove. What if the data that must go is **malicious**, planted to make
the model misbehave, and we only find *some* of it?

[On to Lesson 14, poisoned data and backdoors :material-arrow-right:](14-poisoned-data-and-backdoors.md){ .md-button }
