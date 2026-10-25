---
title: The gold band
description: Retrained neural networks disagree with each other, so the target for unlearning is a band of results, not one number.
---

# The gold band

!!! oneline "In one line"
    The **gold band** is the range of results you get from *several* models retrained without the data; an unlearnt
    model passes if it lands inside that range.

## Why it matters

Most unlearning tutorials compare their method with **one** retrained model. But two neural networks retrained in exactly
the same way disagree with each other. Comparing with just one would fail good methods and pass bad ones. The gold band
fixes this, and it is the idea the whole course is built around.

## A simple example

Ask five good cooks to make the same recipe. Each dish tastes slightly different, but all of them are "correct". If you
want to judge a sixth cook, you do not compare them with just one of the five. You ask: "Does this dish fall within the
range the good cooks produced?"

## How it works

<ol class="steps" markdown>
<li markdown>**Retrain several times** without the forget set, each with a different random seed. The course often uses 5 to 20.</li>
<li markdown>**Measure each retrained model** on the things you care about: accuracy on `D_f`, accuracy on the test set,
a membership attack score.</li>
<li markdown>**Build the band**: the mean, plus or minus about two standard deviations (with a small minimum width).</li>
<li markdown>**Check the unlearnt model**: is each measurement inside the band? Too high means it still remembers.
Too low means it has **over-forgotten**.</li>
</ol>

### How wide is the band?

In Lesson 06, the network was retrained 20 times without Carol:

- Accuracy on Carol's digits: mean **62.0%**, standard deviation 5.6%, range **47.5% to 70.0%**.
- Test accuracy: mean 98.2%, standard deviation 0.34%.
- The original model (with Carol) scored **100.0%** on her digits, far outside the band.

Two networks retrained identically disagreed by more than 20 points on Carol's digits.

### Classical models have a band of width zero

Naive Bayes and Newton-solved logistic regression are **deterministic**: retrain them five times and you get the same
model every time (27.5% and 62.5% on Carol's digits). That is why Lessons 01 to 03 could check for *identical*
predictions. Neural networks depend on random starting weights and random batch order, so retraining is like rolling
dice.

### The band depends on what is forgotten

| What is forgotten | Gold band on `D_f` | Original model | Meaning |
|---|---|---|---|
| **Carol** (a memorised person) | wide, around the middle | far outside | real work to do |
| **Random typical users** | narrow, near 100% | **inside** | typical data was never memorised |
| **A whole class** (every "3") | exactly 0% | outside | a model that never saw a 3 can never say "3" |

!!! note "Too forgotten is also a failure"
    A model that is far *worse* on Carol than the band is suspicious. It treats her data differently from data it never
    saw, and an attacker can notice that. This is sometimes called the **Streisand effect**.

## In code

```python
from mul import audit, lab, methods
L = lab.make_lab("carol")
refs = [methods.retrain(lab.model_fn, L.Xr, L.yr, seed=s, **lab.FIT)[0] for s in range(5)]
splits = dict(Xr=L.Xr, yr=L.yr, Xf=L.Xf, yf=L.yf, Xt=L.X_test, yt=L.y_test)
band_mean, band_std = audit.gold_band(refs, splits)          # mean and spread of each metric
table = audit.audit({"my method": unlearnt}, splits, refs)    # measure the method the same way
print(audit.gate(table, band_mean, band_std, k=2.0))          # PASS or FAIL per check
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Using one retrained model.** It is one roll of the dice.
    - **Aiming below the band.** Over-forgetting is a leak too.
    - **Building the band with a different recipe** from the model under test. The references must use the same
      architecture, sharding and training settings.

## Key takeaways

- Retrained neural networks disagree, so "forgotten" is a range, not a number.
- Build the band from several retrains; pass only if the result lands inside it.
- Landing below the band (over-forgetting) is a failure too.

## Quiz

```quiz
- q: Why do we need several retrained models instead of one?
  options:
    - Retrained neural networks disagree with each other.
    - One model is too slow to train.
    - The law requires exactly five.
  answer: 0
  why: In Lesson 06, 20 identical retrains ranged from 47.5% to 70.0% on Carol's digits.
- q: An unlearnt model scores 10% on Carol, while the gold band is 62% ± 9%. What does that mean?
  options:
    - Perfect forgetting
    - Over-forgetting, which is also a failure
    - The band is wrong
  answer: 1
  why: A model that never saw Carol does much better than 10%. Being far worse is suspicious and can be detected.
- q: Why do Naive Bayes models have a band of width zero?
  options:
    - They are deterministic, so every retrain gives the same model.
    - They have no weights.
    - They cannot be retrained.
  answer: 0
  why: Without randomness in training, retraining always produces exactly the same answer.
- q: When the forget set is random typical users, where is the original model?
  options:
    - Already inside the band
    - Far above the band
    - Far below the band
  answer: 0
  why: Typical data was never memorised, so the original model already behaves like one that never saw it.
- q: When forgetting a whole class (every "3"), what is the gold band on that class?
  options:
    - About 50%
    - Exactly 0%
    - About 100%
  answer: 1
  why: A model that never saw any 3s can never predict "3".
```

## Try it

- Next concept: [Exact unlearning for classical models](exact-unlearning-classical.md).
- Lesson: [06 · Retrain and the gold band](../lessons/06-retrain-and-the-gold-band.md).
