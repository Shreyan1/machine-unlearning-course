---
title: Why the law cares
description: The right to erasure, model-deletion orders and real cases where bad data inside a model cost millions.
---

# Why the law cares

!!! oneline "In one line"
    Laws give people the right to have their data erased, and regulators have already ordered companies to delete the
    **models** built from data they should not have used.

## Why it matters

Deleting data from a database is a routine task. But if a model was trained on that data, regulators increasingly ask:
"And what about the model?" When the answer is "retrain it", the cost can be enormous. Stanford's AI Index 2024
estimates the compute alone at about **$78 million for GPT-4** and **$191 million for Gemini Ultra**. Unlearning is the
hope of a cheaper fix, but only if you can show evidence that it worked.

## A simple example

A shop collects customers' photos without asking and builds a face-recognition system from them. A regulator finds
out. Fining the shop and making it delete the photos is not enough, because the system still works from what it learnt.
So the regulator also orders the shop to delete the **system**.

This is not imaginary. It has happened several times, as the table below shows.

## How it works

### Situations that call for unlearning

| Situation | Example | What has to be forgotten |
|---|---|---|
| **Right to be forgotten** | GDPR Art. 17 (EU), India's DPDP Act 2023 s.12, California CCPA §1798.105 | one person's records |
| **Unlawfully collected data** | US FTC orders against Everalbum (2021), WW/Kurbo (2022) and Rite Aid (2023) | a whole data source, and the models built from it |
| **Is a model personal data?** | EDPB Opinion 28/2024: a model is only "anonymous" if extracting personal data from it, including through queries, is negligible | anything the model could leak |
| **Consent withdrawn** | a person withdraws consent for their face, voice or health record | one identity |
| **Poisoned data** | an attacker slipped mislabelled or back-doored samples into training | the malicious samples |
| **Copyright or licensing** | a data licence expires, or a rights-holder objects | one source |
| **Harmful knowledge in LLMs** | memorised secrets, private phone numbers, hazardous instructions | facts, not rows |

### Regulators have ordered model deletion

| Year | Case | Outcome |
|---|---|---|
| 2021 | **Everalbum** used customers' photos to build face recognition without proper consent. | US FTC ordered it to delete the face-recognition **models and algorithms** built from those photos. |
| 2022 | **WW (Weight Watchers) / Kurbo** collected children's data without parental consent. | $1.5 million penalty, and destroy any **models or algorithms** made from the data. |
| 2023 | **Ring** used customers' videos to train algorithms without consent. | $5.8 million, and delete the **models and algorithms** built from those videos. |
| 2023 | **Rite Aid**'s face recognition wrongly flagged thousands of shoppers as shoplifters. | Five-year ban on face recognition; delete the photos and any **algorithms** built from them. |
| 2025 | **Kakao Pay** sent data on about 40 million users to **Alipay** without consent, and Alipay built a credit-scoring model from it. | South Korea's privacy regulator ordered Alipay to **delete the model**. |

### When the model itself holds the data

In November 2025, a Munich court ruled that song lyrics memorised **in a model's weights** count as a copy under German
copyright law (the ruling is under appeal). This is exactly the case where deleting the files does nothing: the data is
in the model.

### When retraining was too expensive

The GPT-3 paper (2020) admits that a bug left some test data in the training set, and that "due to the cost of training
it was not feasible to retrain the model". The flaw shipped and was measured instead.

!!! warning "Unlearning is not a legal safe harbour"
    No regulator has yet said that any unlearning method counts as deleting the data. In July 2026 the EU's data
    protection board published draft guidelines on scraping personal data to train generative AI, so the rules are
    still being written. Erasure rights also have exceptions. This course teaches you to *measure* what a method does,
    so you can make the argument honestly. [The unlearning audit](unlearning-audit.md) and
    [the enterprise playbook](enterprise-playbook.md) cover the evidence and the paperwork.

Sources for every case are linked in the course [README](https://github.com/Shreyan1/machine-unlearning-course#readme).

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking erasure means deleting rows.** Regulators have ordered the deletion of models, not just data.
    - **Claiming "we unlearnt it" without evidence.** A claim needs measurements against a gold standard.
    - **Ignoring derived models.** Contracts and orders often cover "any models derived from" the data, including
      fine-tunes and distilled copies.

## Key takeaways

- Laws such as GDPR Art. 17 and India's DPDP Act give people a right to erasure.
- Regulators have already ordered the deletion of models built from unlawful data.
- Retraining large models is very expensive, which is why unlearning matters.
- Unlearning provides evidence, not a legal guarantee.

## Quiz

```quiz
- q: Which law gives people in the EU the "right to be forgotten"?
  options:
    - GDPR Article 17
    - The US Copyright Act
    - The Video Privacy Protection Act
  answer: 0
  why: GDPR Art. 17 is the right to erasure. India's DPDP Act 2023 s.12 and California's CCPA have similar rights.
- q: What did the US FTC order Everalbum to delete in 2021?
  options:
    - Only the customers' photos
    - The face-recognition models and algorithms built from the photos
    - Its website
  answer: 1
  why: The order covered the models, not just the data. This is sometimes called "algorithmic disgorgement".
- q: According to EDPB Opinion 28/2024, when can a model trained on personal data be called anonymous?
  options:
    - Always, once training is finished
    - Only if extracting personal data from it, including through queries, is negligible
    - Never
  answer: 1
  why: If the data can be pulled out of the model, the model may still hold personal data.
- q: Does any regulator currently accept an unlearning method as proof of deletion?
  options:
    - Yes, gradient ascent is accepted everywhere.
    - No, not yet.
  answer: 1
  why: The rules are still being written. Unlearning gives evidence, which must be argued case by case.
```

## Try it

- Next concept: [The notation](notation.md).
- Lesson: [12 · Right to be forgotten and fairness](../lessons/12-right-to-be-forgotten-and-fairness.md) and
  [17 · The enterprise playbook](../lessons/17-enterprise-playbook.md).
