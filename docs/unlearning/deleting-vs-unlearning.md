---
title: Deleting is not forgetting
description: Why removing someone's rows from a database does not remove what a trained model learnt from them.
---

# Deleting is not forgetting

!!! oneline "In one line"
    Deleting data removes the *file*, but the trained model still carries what it *learnt* from that file.

## Why it matters

When a person asks a company to erase their data, the company usually deletes their rows from a database. If an AI
model was trained on those rows, the model does not change at all. It can still behave in ways that reveal the person
was there. Regulators have noticed. In several cases, they have ordered companies to delete the **models**, not just the
data (see [Why the law cares](why-the-law-cares.md)).

## A simple example

Think of a cookbook and a cake. You can tear a page out of the cookbook, but you cannot "un-bake" the cake you already
made from it.

- The **page** is the training data.
- The **cake** is the trained model.
- **Machine unlearning** is the attempt to un-bake the cake, that is, to remove one ingredient's effect after the fact.

In the course, the cake is a digit-reading model and the ingredient is **Carol**, who wrote 40 of its 1,257 training
digits with a thick marker.

<!-- diagram: deleting-vs-unlearning -->

## How it works

<ol class="steps" markdown>
<li markdown>**Training changes the weights.** A model is a long list of numbers called *weights*. During training, every
example nudges those numbers a little. Carol's digits nudged them too.</li>
<li markdown>**The database and the model are separate.** After training, the model no longer reads the database. It only
uses its weights.</li>
<li markdown>**Deleting the rows does not touch the weights.** So the model still gets Carol's digits right far more often
than digits like hers that it has never seen.</li>
<li markdown>**Her influence is spread everywhere.** In the course's neural network, removing Carol and retraining from the
same starting point changes **94.1%** of the 85,002 weights. There is no single "Carol weight" to delete.</li>
</ol>

Here are the numbers from the course, before and after retraining without Carol.

| Model | Carol's own digits | Unseen thick-marker digits | Everyone else's test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

Before, the model is much better on Carol's digits than on digits *like* hers. That gap is her **fingerprint**. After
retraining, the gap is gone, and everyone else's accuracy has not moved.

## In code

The course library hides the training loop behind two calls, so the comparison is short.

```python
from mul import lab, train, methods

L = lab.make_lab("carol")      # 1,257 digits, 40 of them Carol's
original = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
retrained, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)

print(train.accuracy(original, L.Xf, L.yf))    # Carol's digits, before: 1.00
print(train.accuracy(retrained, L.Xf, L.yf))   # Carol's digits, after:  0.55
```

`L.Xf` is the **forget set** (Carol's data) and `L.Xr` is the **retain set** (everyone else). See
[The notation](notation.md) for all the symbols.

## Common mistakes

!!! danger "Mistakes people make"
    - **"We deleted the data, so we are done."** The model still carries the data's influence.
    - **"Forgotten means 0% on Carol."** No. A model that never met Carol still reads 55% of her digits, because it learnt
      what digits look like from everyone else. Forgetting means *matching a model that never saw her*, not scoring zero.
    - **"Just compare the weights."** Two good models trained on the same data can have very different weights. The proof
      has to be about *behaviour* (see [The gold band](gold-band.md)).

## Key takeaways

- A trained model keeps the influence of its training data, even after the data is deleted.
- Unusual data, like Carol's thick-marker digits, is memorised the most.
- In a neural network, one person's influence is spread across almost every weight.
- The honest target is the model you would have had if the data had never been there.

## Quiz

```quiz
- q: A company deletes Carol's rows from its database. What happens to the trained model?
  options:
    - Nothing changes; its weights still carry her influence.
    - It forgets her at once.
    - It stops working until it is retrained.
  answer: 0
  why: After training, the model only uses its weights. Deleting rows from the database does not touch them.
- q: In the cookbook picture, what does the cake stand for?
  options:
    - The training data
    - The trained model
    - The unlearning method
  answer: 1
  why: The page is the data and the cake is the model made from it. You can tear out the page, but you cannot un-bake the cake.
- q: Before unlearning, the model scores 100% on Carol's digits and 77.5% on unseen thick-marker digits. What does that gap show?
  options:
    - The model is broken.
    - The model has memorised Carol's specific digits.
    - Thick-marker digits are impossible to read.
  answer: 1
  why: The model is much better on *her* digits than on digits *like* hers. That extra accuracy comes from having trained on them.
- q: After Carol is truly forgotten, what should her accuracy look like?
  options:
    - Exactly 0%
    - Still 100%
    - About the same as a model that never saw her
  answer: 2
  why: The target is the retrained model, not zero. A model that never met Carol still reads many of her digits.
- q: Why can we not simply find and delete "Carol's weights" in a neural network?
  options:
    - Her influence is spread across almost all the weights.
    - The weights are encrypted.
    - Neural networks do not have weights.
  answer: 0
  why: Removing Carol changes 94.1% of the network's 85,002 weights. There is no small set of weights that holds her.
```

## Try it

- The lesson [00 · Read this first](../lessons/00-read-first.md) runs the full before-and-after in four cells.
- The lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) shows why every classical trick fails in a neural network.
- Read the next concept, [Why the law cares](why-the-law-cares.md).
