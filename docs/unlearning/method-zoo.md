---
title: The method zoo
description: Fourteen unlearning methods, old and new, sit one fixed exam. New is not the same as better, and a privacy test can be fooled by accident.
---

# The method zoo

!!! oneline "In one line"
    When fourteen unlearning methods sit the **same fixed exam**, the newer ones do not beat the older ones, and only
    the exact methods pass by design.

## Why it matters

Every year brings new unlearning methods, each with a paper saying it works. But papers usually test their own method,
with settings tuned on their own data. Putting many methods through **one pre-registered exam** shows which claims
survive. It also reveals a subtle way that a privacy test can be fooled.

## A simple example

A cooking contest: fourteen cooks, the same three dishes, the same judges, and a scoring sheet written before anyone
tastes anything. Some cooks are famous. The scoring sheet does not care.

## How it works

### Six new methods

Lesson 19 adds six newer methods to the eight from earlier lessons:

| Method | The idea in one line |
|---|---|
| **Random labels** | Give the forget data random wrong labels and keep training. |
| **SalUn** | The same, but only move the weights that matter most for the forget data. |
| **L1-sparse** | Fine-tune with a penalty that pushes small weights to zero. |
| **UNSIR** | Learn "noise" images the model gets wrong, train on them, then repair. |
| **SSD** | No training: shrink weights that matter far more for the forget data than for everything. |
| **Last layer** | Keep the network, re-solve only its last layer exactly on the data that stays. |

Methods also fall into three families: **model-agnostic** (works on any model), **model-intrinsic** (uses one model's
insides) and **data-driven** (changes the data side, like SISA or UNSIR).

### The final leaderboard

After the fair privacy check (below), on three requests:

| Method | Carol | Class "3" | Random 10% | Cost (% of retrain) |
|---|---|---|---|---|
| Retrain | ✅ | ✅ | ✅ | 100 |
| SISA | ⚠️ false alarm | ✅ | ✅ | 61.4 |
| SCRUB, SCRUB+R | ❌ | ✅ | ❌ | 13.6 |
| All other ten methods | ❌ | ❌ | ❌ | 0.3 to 15.0 |

**No approximate method forgot Carol.** Every one of them failed the relearn attack on her.

### Read the rule before you trust the method

SSD changed **no weights at all** on the class request. Its rule only touches a weight if it matters more than 10 times
as much for the forget data as for the *whole* training set. But the whole set *includes* the forget data. When the
forget set is 10% of the data, the rule can never fire.

### A privacy test fooled by accident

On the random request, five new methods first *passed* the privacy check. One of them, L1-sparse, passed privacy on
Carol while still getting all 40 of her digits right. How?

These methods make the model **less sure about almost everything**, including data it should keep. The privacy test
(U-LiRA) reads confidence, and lower confidence looks like "never saw it". The fix is the same recipe rule as before:
**put the reference models through the same method too**, and add a never-saw-it control. With fair references, the
passes disappeared.

!!! tip "The general lesson"
    Any change to how a model is made, **including the unlearning method itself**, is part of the recipe. Reference
    models must follow the same recipe.

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming newer means better.** On a fixed exam with pre-registered settings, it did not.
    - **Tuning on the answer sheet.** In production there is no gold band to tune against.
    - **Trusting a privacy pass when confidence dropped everywhere.** Use own-recipe references and a control.

## Key takeaways

- New is not the same as better; no approximate method forgot Carol.
- The family does not decide the result; the request and the exam do.
- A privacy test can be fooled by a method that lowers confidence everywhere.
- Exact methods remain the only ones that pass by design.

## Quiz

```quiz
- q: How many approximate methods forgot Carol on the fixed exam?
  options:
    - None
    - Half of them
    - All of them
  answer: 0
  why: Every approximate method, old or new, failed the relearn attack on Carol.
- q: Why did SSD change no weights on the class request?
  options:
    - Its rule cannot fire when the forget set is 10% or more of the data.
    - It crashed.
    - The class was already forgotten.
  answer: 0
  why: The whole training set includes the forget data, so no weight can be more than 10 times as important for it.
- q: Some methods passed the privacy test by lowering confidence everywhere. What is the fix?
  options:
    - Put the reference models through the same method, and add a never-saw-it control.
    - Drop the privacy test.
    - Use only accuracy.
  answer: 0
  why: If both IN and OUT references go through the method, a general confidence drop no longer looks like forgetting.
- q: Which methods pass by design, not by luck?
  options:
    - Exact methods such as retraining and SISA
    - The newest methods
    - Methods with the lowest cost
  answer: 0
  why: Their result is guaranteed by the process, not just by passing tests.
```

## Try it

- Next concept: [Membership inference attacks](membership-inference-attacks.md).
- Lesson: [19 · The method zoo](../lessons/19-the-method-zoo.md).
