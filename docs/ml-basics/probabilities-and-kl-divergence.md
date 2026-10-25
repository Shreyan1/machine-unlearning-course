---
title: Probabilities and KL divergence
description: How a model says how sure it is, how temperature softens that and how KL divergence compares two models.
---

# Probabilities and KL divergence

!!! oneline "In one line"
    A classifier outputs a **probability for each answer**, and **KL divergence** is a number that says how different
    two such sets of probabilities are.

## Why it matters

Several unlearning methods, such as [SCRUB](../unlearning/scrub.md) and [Bad Teacher](../unlearning/bad-teacher.md),
work by making one model copy (or refuse to copy) another model's probabilities. They measure "how close" with KL
divergence. Audits also compare a model's probabilities with those of retrained models.

## A simple example

Ask two weather forecasters about tomorrow.

- Forecaster A: "70% sun, 20% cloud, 10% rain."
- Forecaster B: "65% sun, 25% cloud, 10% rain."
- Forecaster C: "10% sun, 10% cloud, 80% rain."

A and B mostly agree. A and C strongly disagree. KL divergence turns that feeling into a number. It is small for A and B, and large for A and C.

## How it works

### From scores to probabilities (softmax)

A model first produces a raw score for each class, called a **logit**. The **softmax** function turns these into
probabilities that are all positive and add up to 1. A higher logit gets a higher probability.

### Temperature

Softmax can take a **temperature** \(T\). Dividing the logits by \(T > 1\) makes the probabilities *softer* (more
spread out). This shows more of what the model "thinks", for example that a "7" looks a bit like a "1". Teacher and
student methods often use a temperature such as 2 or 4.

### KL divergence

For two sets of probabilities \(p\) and \(q\) over the same answers:

\[
\text{KL}(p \,\|\, q) = \sum_i p_i \log \frac{p_i}{q_i}
\]

- It is **0** when \(p\) and \(q\) are identical.
- It grows as they disagree, especially when \(p\) is confident about an answer that \(q\) thinks is unlikely.
- It is **not symmetric**: \(\text{KL}(p\|q)\) is usually different from \(\text{KL}(q\|p)\).

A symmetric cousin, the **Jensen-Shannon (JS) divergence**, is used in some audits to compare a model with retrained models.

### Teacher and student

**Knowledge distillation** trains a *student* model to match a *teacher* model's probabilities, by making the KL
divergence between them small. Unlearning methods twist this. The student copies the teacher on the retain set, but *not* on the forget set.

## In code

```python
from mul import nn
p = nn.softmax(logits)                         # probabilities
p_soft = nn.softmax(logits, T=4.0)             # softer probabilities
loss, grad = nn.distill_kl(student_logits, teacher_logits, T=4.0)   # how far the student is from the teacher
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Treating KL as a distance.** It is not symmetric, so the order of the two models matters.
    - **Reading a probability as certainty.** A model saying "90%" can still be wrong; probabilities are the model's
      own confidence, not a guarantee.

## Key takeaways

- Softmax turns raw scores into probabilities that add up to 1.
- A higher temperature makes probabilities softer and more informative.
- KL divergence measures how different two sets of probabilities are; 0 means identical.
- Teacher-student unlearning methods are built on KL divergence.

## Quiz

```quiz
- q: What does softmax do?
  options:
    - Deletes the smallest scores
    - Turns raw scores into probabilities that add up to 1
    - Picks a random answer
  answer: 1
  why: Softmax makes every output positive and normalises them so they sum to 1.
- q: If two models give exactly the same probabilities, their KL divergence is...
  options:
    - 0
    - 1
    - Infinite
  answer: 0
  why: KL divergence is zero only when the two distributions are identical.
- q: What does a higher temperature do to the probabilities?
  options:
    - Makes them softer and more spread out
    - Makes them sharper
    - Makes them add up to more than 1
  answer: 0
  why: Dividing logits by T > 1 shrinks the gaps between them, so probabilities spread out.
- q: In knowledge distillation, what does the student try to do?
  options:
    - Match the teacher's probabilities
    - Get the opposite answer to the teacher
    - Memorise the test set
  answer: 0
  why: The student is trained to make its KL divergence from the teacher small.
```

## Try it

- Concept: [SCRUB, teacher and student](../unlearning/scrub.md) uses KL divergence in both directions.
- Lesson: [10 · Bad Teacher](../lessons/10-bad-teacher.md) uses a "bad" teacher on the forget set.
