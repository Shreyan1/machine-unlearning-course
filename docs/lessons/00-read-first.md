---
title: "Lesson 00: Read this first"
description: Meet Carol, the notation, the gold standard and the Ladder of Forgetting, with the whole course in four code cells.
---

# Lesson 00: Read this first

<div class="chips"><span class="chip">⏱ ~1 hr</span><span class="chip">Stage 0 · Foundations</span><span class="chip">Start here</span></div>

<div class="buttons">
<a class="md-button md-button--primary" href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb">Open in Colab</a>
<a class="md-button" href="https://github.com/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb">View on GitHub</a>
</div>

## The story

A digit-recognition model is trained on 1,257 handwritten digits. Forty of them were written by **Carol**, with a thick
marker that nobody else used. Carol now asks to be deleted. This lesson introduces the whole course: why unlearning is
needed, the notation, the map of methods, and a 60-second preview of the full loop.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a small neural network on all 1,257 digits, including Carol's.</li>
<li markdown>**Show the issue**: compare its accuracy on Carol's digits with unseen thick-marker digits.</li>
<li markdown>**Untrain** with the simplest exact method: retrain without her.</li>
<li markdown>**Show the result** side by side.</li>
<li markdown>**Prove it**: the retrained model treats her digits like any other unseen thick-marker digits.</li>
</ol>

## Key results

| Model | Carol's digits (`D_f`) | Unseen thick-marker digits | Test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

- The 100% versus 77.5% gap is Carol's **fingerprint**: the model memorised *her* digits, not just thick digits.
- After retraining, her digits get no special treatment, and everyone else's accuracy is unchanged.
- Her accuracy is **not 0%**. The target is the retrained model, not zero. This is the idea most unlearning tutorials
  get wrong.

The catch: retraining took a third of a second here. For a model that costs weeks of GPU time, it is not affordable.
That is where the rest of the course begins.

## Concepts used here

- [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md)
- [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)
- [The notation](../unlearning/notation.md)
- [The Ladder of Forgetting](../unlearning/ladder-of-forgetting.md)

## Quiz

```quiz
- q: Before unlearning, the model is 100% right on Carol's digits and 77.5% on unseen thick-marker digits. What does the gap show?
  options:
    - The model memorised Carol's specific digits.
    - The test set is broken.
    - Thick digits are always easy.
  answer: 0
  why: It is much better on her exact digits than on similar ones it never saw.
- q: After retraining without Carol, what is her accuracy?
  options:
    - 0%
    - 55.0%
    - 100%
  answer: 1
  why: A model that never met her still reads many of her digits, because it learnt digits from everyone else.
- q: What is θ_r?
  options:
    - The original model
    - The model retrained on the retain set only
    - The unlearnt model
  answer: 1
  why: θ_r is the gold standard that every unlearning method tries to match.
- q: Which of these is a real case where a regulator ordered a model to be deleted?
  options:
    - FTC v. Everalbum (2021)
    - The Netflix Prize (2006)
    - The ImageNet challenge (2012)
  answer: 0
  why: The FTC ordered Everalbum to delete the face-recognition models built from users' photos.
- q: Why is retraining not the end of the story?
  options:
    - It is far too expensive for large models and many requests.
    - It never works.
    - It is illegal.
  answer: 0
  why: Retraining is exact but its cost grows with all the data you keep.
```

## Open question → Lesson 01

When is forgetting exact and cheap, and what property of a model makes it so? We start with the two easiest models on
the ladder.

[Next: Lesson 01, k-NN and Naive Bayes](01-knn-and-naive-bayes.md){ .md-button }
