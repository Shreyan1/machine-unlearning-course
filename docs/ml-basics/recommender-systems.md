---
title: Recommender systems
description: Recommenders learn from what people have in common, so your data lives in the links between items and shows up on other people's screens.
---

# Recommender systems

!!! oneline "In one line"
    A recommender suggests items by learning **what people have in common**: "people who watched this also watched
    that".

## Why it matters

In most models, your data is one row. In a recommender, your data is spread across the **links between items**, and
the service shows those links publicly, on every item's page. Your viewing or shopping history can be private and
sensitive. In 2008, researchers showed that "anonymous" Netflix ratings could be matched back to real, named people.

## A simple example

A video shop assistant remembers what customers rent together. If one customer always rents rare foreign films, the
assistant starts telling others "people who liked *this* rare film also liked *that* one". Each time, the assistant is
repeating a piece of that customer's rental history. Cutting up her membership card does not make the assistant forget.

## How it works

The course uses real data, **MovieLens 100K**: 943 people, 1,682 films and 100,000 ratings. It only uses *who watched
what*. Quality is measured with **recall@10**: the share of a user's hidden films that appear in their top 10.

### Item-kNN

The whole model is one table, `G`. `G[i, j]` counts how many users watched both film \(i\) and film \(j\). Films are
"similar" when many of the same people watched them. To recommend, the model adds up how similar each film is to the
films you already watched.

Because `G` is a **sum over users**, forgetting a user is a subtraction, exactly like [Naive Bayes](naive-bayes.md).

### Matrix factorisation

Every user and every film gets a list of 32 numbers (a vector). If a user's numbers line up with a film's numbers, the
model predicts the user will like it. Training takes turns: fix the films and solve each user (a small
[ridge regression](linear-and-ridge-regression.md)), then fix the users and solve each film.

Everything is fitted together, so deleting one user's vector leaves their influence in the **film** vectors.

| Model | Recall@10 | Forgetting a user |
|---|---|---|
| Most popular films (baseline) | 0.210 | — |
| Item-kNN | 0.349 | Subtract their counts: exact, 0.27% of a rebuild |
| Matrix factorisation | 0.423 | No sum to subtract; exact needs a retrain |

### The person who left shows up on public pages

In Lesson 18, a user called **Erin** watched 186 films, 11 of which nobody else watched. On one of those films' public
"also watched" pages, all 10 slots were her other films. Deleting her account changed nothing the public could see.

## In code

```python
from mul import recsys
knn = recsys.ItemKNN().fit(R)      # R: who watched what
knn.unlearn_users([erin])          # subtract her co-watch counts: exact
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting only the user's own vector.** What they taught the model sits in the item vectors and public lists.
    - **Checking only overall quality.** Recall for everyone else did not move for any method, even the ones that left
      Erin on every page.
    - **Publishing before-and-after lists.** The difference between them reveals what the deleted person watched. See
      [Unlearning in recommenders](../unlearning/recommender-unlearning.md).

## Key takeaways

- Recommenders learn from shared behaviour; your data lives in the links between items.
- Item-kNN is a sum, so forgetting a user is an exact, almost free subtraction.
- Matrix factorisation ties everyone together, so exact forgetting needs a retrain.
- Public "also watched" lists can expose a person, even after deletion.

## Quiz

```quiz
- q: In a recommender, where does your data mostly live?
  options:
    - In one row of a table
    - In the links between the items you used
    - Only in your account settings
  answer: 1
  why: Recommenders learn what items people use together, so your history is spread across those links.
- q: How does item-kNN forget a user?
  options:
    - Subtract their co-watch counts from the table
    - Retrain from scratch
    - Delete the most popular films
  answer: 0
  why: The co-watch table is a sum over users, so removing one is an exact subtraction.
- q: In matrix factorisation, what happens if you only delete the user's own vector?
  options:
    - They are fully forgotten.
    - Their influence stays in the film vectors and public pages.
    - The whole model breaks.
  answer: 1
  why: In Lesson 18, deleting Erin's row changed nothing the public could see.
- q: Why is overall recall a poor test of whether Erin was forgotten?
  options:
    - It did not change for any method, even ones that left her on public pages.
    - It is too slow to compute.
    - It only measures Erin.
  answer: 0
  why: The business metric does not see one unusual user, while the public pages are full of her.
```

## Try it

- Concept: [Unlearning in recommenders](../unlearning/recommender-unlearning.md).
- Lesson: [18 · Recommender systems](../lessons/18-recommender-systems.md).
