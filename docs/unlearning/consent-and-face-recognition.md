---
title: Consent and face recognition
description: In face recognition a person is a class. Withdrawing consent means removing them from the gallery and the face reader, and stopping re-enrolment.
---

# Consent and face recognition

!!! oneline "In one line"
    In face recognition, a person **is a class**; withdrawing consent means removing them from the address book **and**
    from the face reader, and then stopping them from being enrolled again.

## Why it matters

Face templates are **biometric data**, a special category under GDPR (Art. 9). Consent can be withdrawn at any time, and
erasure follows. In FTC v. Everalbum (2021), the company had to delete not only the photos but the face-recognition
**models** built from them. Getting this right takes three separate steps, and unlearning covers only one of them.

## A simple example

A face-ID door system has two parts:

- a **face reader**, which turns a photo into a list of numbers; and
- an **address book** of enrolled staff ("this pattern of numbers is Dana").

When Dana leaves and withdraws consent, deleting her address-book entry is not enough. The face reader learnt its idea
of "what a face looks like" partly from her photos.

## How it works

Lesson 13 uses the **Olivetti faces** dataset (40 people, 10 photos each).

### Dana is inside the face reader

The classical system uses **eigenfaces**: PCA on the training photos gives a 40-dimensional "face space". A face space
built **with** Dana reconstructed her photos with error 0.264; one built **without** her gave 0.383. Across all 40
people, leaving someone out raised their error by 41% on average. Her face is literally part of the basis.

### Exact removal for the classical system

PCA's covariance is built from **sums**, so Dana can be subtracted exactly, like [Naive Bayes](../ml-basics/naive-bayes.md).
After subtracting her and deleting her templates, the eigenfaces matched a from-scratch system exactly, with identical
predictions on every test photo.

### The neural system

Removing one identity from a neural face classifier is a **class** request. NegGrad+, SCRUB and Bad Teacher all passed
the audit; plain fine-tuning and gradient ascent at their defaults did not.

### Memory is not capability

Then comes the important test. Enrol Dana again from 3 new photos, and try to identify her 7 deleted photos.

| Model | Dana's deleted photos matched to her new template |
|---|---|
| Models that **never saw** Dana (mean of 12) | 83% |
| Retrained | 100% |
| Unlearnt models | 71% to 100% |

Even models that never saw a single photo of her recognise her after re-enrolment. That is not a failure of unlearning;
recognising new faces is the **job** of a face model.

| | Memory | Capability |
|---|---|---|
| What it is | the influence of Dana's photos on the weights | the ability to match *any* face to an enrolled template |
| Removed by unlearning? | ✅ | ❌, retrained models have it too |
| What protects Dana | unlearning | **deleting her templates and refusing re-enrolment** |

!!! warning "The three-part procedure"
    1. Delete her templates and raw images.
    2. Unlearn her from the face model (or retrain on schedule).
    3. Stop re-enrolment, using a **non-biometric** key such as an employee ID. A "do-not-enrol" list made of her face
       would itself be biometric processing of someone who withdrew consent.

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting only the gallery entry.** The face reader still carries her.
    - **Expecting unlearning to stop recognition.** Capability stays; only process stops re-enrolment.
    - **Blocking her with a face-based list.** That is biometric processing too.

## Key takeaways

- In face recognition, a person is a class, and their photos shape the face reader.
- Eigenfaces can be unlearnt exactly because PCA uses sums.
- Unlearning removes memory, not capability.
- Real protection needs template deletion and a non-biometric do-not-enrol key.

## Quiz

```quiz
- q: Why is deleting Dana's gallery template not enough?
  options:
    - The face reader was also learnt partly from her photos.
    - The template is stored twice.
    - Templates cannot be deleted.
  answer: 0
  why: Her photos shaped the eigenfaces or network that turns photos into numbers.
- q: Why can eigenfaces forget Dana exactly?
  options:
    - PCA is built from sums, which can be subtracted.
    - Eigenfaces have no parameters.
    - Dana was never in the data.
  answer: 0
  why: Like Naive Bayes, the covariance is a sum over photos, so her contribution can be taken out.
- q: After re-enrolment, models that never saw Dana still recognised her most of the time. What does that show?
  options:
    - Recognising new faces is a capability, not a memory of Dana.
    - Unlearning failed.
    - The models secretly saw her.
  answer: 0
  why: A face model is meant to recognise faces it has never seen. Unlearning cannot remove that.
- q: How should a system stop Dana from being enrolled again?
  options:
    - With a non-biometric key, such as her employee ID
    - With a list of her face embeddings
    - It cannot be done.
  answer: 0
  why: A face-based block list would itself process biometric data of someone who withdrew consent.
```

## Try it

- Next concept: [Poisoned data and backdoors](poisoning-and-backdoors.md).
- Lesson: [13 · Consent withdrawal in face recognition](../lessons/13-consent-withdrawal-face-recognition.md).
