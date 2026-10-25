---
title: Retraining, the gold standard
description: Retraining from scratch without the data is always correct and always expensive. Every other method is judged against it.
---

# Retraining, the gold standard

!!! oneline "In one line"
    Retraining from scratch without the data always gives the right answer, so every other method is judged by how
    close it gets to it, but its cost grows with **everything you keep**.

## Why it matters

Retraining is the one method nobody can argue with: a model that never saw the data cannot carry its influence. That
makes it the **reference point** for every audit. Its problem is cost. For a small model it takes a third of a second;
for a large language model it can take months and millions of dollars, and the requests keep coming.

## A simple example

You bake a cake and then learn that one ingredient was off. The only way to be *sure* the cake is safe is to bake a new
one without it. That always works, but it means buying everything again and spending the whole afternoon in the
kitchen, every time.

## How it works

<ol class="steps" markdown>
<li markdown>**Remove** the forget set `D_f` from the training data.</li>
<li markdown>**Train a fresh model** on the retain set `D_r`, from new random weights, with the same recipe.</li>
<li markdown>**Use it** as the unlearnt model, and as the reference for checking other methods.</li>
</ol>

In Lesson 00, retraining without Carol gives:

| Model | Carol's digits | Unseen thick-marker digits | Test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

Notice that Carol's accuracy is **not 0%**. A model that never met her still reads many of her digits, because it
learnt what digits look like from everyone else.

### The trap: "just keep training without her"

A tempting shortcut is to take the original model and continue training it on `D_r` only. It is much cheaper. But in
Lesson 06, after 20 more epochs without Carol, the model was still right on **95.0%** of her digits, against a gold band
of 62.0% ± 9.2%. A model that already fits Carol has no push away from her; she simply stops being mentioned. Only a
**fresh start** is exact.

### The cost

Retraining's cost depends on the size of the data you **keep**, not the data you delete. Lesson 06 works through
placeholder numbers for a production model: retraining daily to batch deletion requests costs about $7.3 million a
year; monthly costs about $243,000, but you may miss legal deadlines. [Unlearning at scale](unlearning-at-scale.md)
shows that the yearly bill grows with the **square** of the service size.

## In code

```python
from mul import lab, methods
L = lab.make_lab("carol")
retrained, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Warm-starting from the original model.** That is fine-tuning, not retraining; it stays far from the gold band.
    - **Using one retrained model as "the" answer.** Neural networks retrained twice disagree; see [The gold band](gold-band.md).
    - **Forgetting the rest of the pipeline.** Scalers, vocabularies and other fitted steps must be rebuilt without the data too.

## Key takeaways

- Retraining without the data is exact and is the reference for every other method.
- Continuing to train the original model on `D_r` is **not** retraining.
- Its cost grows with the data you keep, which is why cheaper methods exist.

## Quiz

```quiz
- q: Why is retraining called the gold standard?
  options:
    - A model that never saw the data cannot carry its influence.
    - It is the cheapest method.
    - It always gives 0% on the forget set.
  answer: 0
  why: It is correct by definition, so every other method is measured against it.
- q: After retraining without Carol, what was the model's accuracy on her digits?
  options:
    - 0%
    - 55.0%
    - 100%
  answer: 1
  why: A model that never met Carol still reads many of her digits, because it learnt digits from everyone else.
- q: You continue training the original model on the retain set for 20 more epochs. Is that retraining?
  options:
    - Yes, it is the same thing.
    - No; it stayed at 95.0% on Carol, far outside the gold band.
  answer: 1
  why: A model that already fits Carol has nothing pushing it away from her. Only a fresh start is exact.
- q: What does the cost of retraining mainly depend on?
  options:
    - The size of the data you delete
    - The size of the data you keep
    - The number of test examples
  answer: 1
  why: Retraining processes all of the retain set again, however small the deletion is.
```

## Try it

- Next concept: [The gold band](gold-band.md).
- Lesson: [06 · Retrain and the gold band](../lessons/06-retrain-and-the-gold-band.md).
