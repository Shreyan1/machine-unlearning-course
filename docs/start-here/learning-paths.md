---
title: Pick your path
description: Short routes through the course for different readers, with time estimates.
---

# Pick your path

You do not have to do all 22 lessons. Find the row that sounds like you, and take its lessons in order.

| You are... | Do these lessons in the Lessons tab | Time |
|---|---|---|
| **New to unlearning** and want the whole idea | [00](../lessons/00-read-first.md) → [01](../lessons/01-knn-and-naive-bayes.md) → [04](../lessons/04-deleting-is-not-forgetting.md) → [06](../lessons/06-retrain-and-the-gold-band.md) → [07](../lessons/07-sisa.md) → [08](../lessons/08-approximate-baselines-and-traps.md) → [11](../lessons/11-the-unlearning-audit.md) | ~4 hrs |
| A **privacy, legal or governance** person who needs to judge an unlearning claim | [00](../lessons/00-read-first.md) → [04](../lessons/04-deleting-is-not-forgetting.md) → [06](../lessons/06-retrain-and-the-gold-band.md) → [11](../lessons/11-the-unlearning-audit.md) → [12](../lessons/12-right-to-be-forgotten-and-fairness.md) → [17](../lessons/17-enterprise-playbook.md) | ~4 hrs |
| An **ML researcher** comparing unlearning methods | [00](../lessons/00-read-first.md) → [04](../lessons/04-deleting-is-not-forgetting.md) → [05](../lessons/05-membership-inference.md) → [06](../lessons/06-retrain-and-the-gold-band.md) → [08](../lessons/08-approximate-baselines-and-traps.md) → [09](../lessons/09-scrub.md) → [10](../lessons/10-bad-teacher.md) → [11](../lessons/11-the-unlearning-audit.md) → [19](../lessons/19-the-method-zoo.md) | ~6 hrs |
| An **LLM engineer** who needs a model to forget facts or a customer's fine-tune | [00](../lessons/00-read-first.md) → [04](../lessons/04-deleting-is-not-forgetting.md) → [06](../lessons/06-retrain-and-the-gold-band.md) → [11](../lessons/11-the-unlearning-audit.md) → [15](../lessons/15-fine-tuning-and-un-finetuning.md) → [16](../lessons/16-llm-unlearning.md) → [16b](../lessons/16b-llm-unlearning-pytorch.md) | ~5 hrs |
| A **platform or MLOps engineer** designing systems that can delete | [00](../lessons/00-read-first.md) → [06](../lessons/06-retrain-and-the-gold-band.md) → [07](../lessons/07-sisa.md) → [11](../lessons/11-the-unlearning-audit.md) → [15](../lessons/15-fine-tuning-and-un-finetuning.md) → [17](../lessons/17-enterprise-playbook.md) → [18](../lessons/18-recommender-systems.md) → [20](../lessons/20-unlearning-at-scale.md) | ~6 hrs |
| Doing **the full course** | Everything, in order | ~19-27 hrs |

Times use the estimate at the top of each notebook, plus a little for the tasks.

## If you are new to machine learning

Read these [ML Basics](../ml-basics/index.md) pages before Lesson 00. Each takes about ten minutes.

1. [What is machine learning?](../ml-basics/what-is-machine-learning.md)
2. [Training data and test data](../ml-basics/training-and-testing.md)
3. [Loss functions](../ml-basics/loss-functions.md)
4. [Gradient descent](../ml-basics/gradient-descent.md)
5. [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)

Then read the model page just before the lesson that uses it, for example [k-nearest neighbours](../ml-basics/k-nearest-neighbours.md)
before Lesson 01.

## The stages of the course

The lessons are ordered on purpose. Each one ends with an **open question** that the next lesson answers.

| Stage | Lessons | You will be able to... |
|---|---|---|
| 0. Foundations | 00 | Explain unlearning, why the law needs it and the gold standard |
| 1. Classical ML | 01-03 | Make k-NN, Naive Bayes, ridge, logistic regression, SVMs and forests forget |
| 2. Neural networks, the problem | 04-05 | Measure memorisation and run membership inference attacks |
| 3. Exact unlearning for neural nets | 06-07 | Build a gold band and a SISA system |
| 4. Approximate unlearning | 08-10 | Run fine-tune, gradient ascent, NegGrad+, SCRUB and Bad Teacher, and catch them failing |
| 5. Proof | 11 | Run a five-check audit and write an evidence record |
| 6. Real-world Responsible AI | 12-16, 16b | Handle fairness, biometric consent, poisoning, per-customer fine-tunes and LLM facts |
| 7. Engineering | 17 | Run a deletion request end to end and issue a certificate |
| 8. Extensions | 18-20 | Handle recommenders, compare fourteen methods fairly and plan for a year of requests |

## Quiz

```quiz
- q: Which lesson appears in almost every path above?
  options:
    - Lesson 00, Read this first
    - Lesson 18, Recommender systems
    - Lesson 16b, LLM unlearning in PyTorch
  answer: 0
  why: Lesson 00 introduces Carol, the notation and the gold standard, which every other lesson builds on.
- q: Why are the lessons in a fixed order?
  options:
    - Alphabetical order
    - Each lesson ends with an open question that the next one answers
    - The later ones were written first
  answer: 1
  why: The course is one argument, built rung by rung on the Ladder of Forgetting.
- q: You need to judge whether a vendor's "we unlearnt the data" claim is believable. Which lesson is most important?
  options:
    - Lesson 11, The unlearning audit
    - Lesson 03, SVM and random forest
    - Lesson 18, Recommender systems
  answer: 0
  why: The audit is how you gather evidence that a model behaves like one that never saw the data.
```
