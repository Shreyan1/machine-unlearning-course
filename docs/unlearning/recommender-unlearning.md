---
title: Unlearning in recommenders
description: In a recommender your data lives in public "also watched" lists. Item-kNN forgets exactly; matrix factorisation does not; and the deletion itself can leak.
---

# Unlearning in recommenders

!!! oneline "In one line"
    In a recommender, your data lives in the **links between items** that everyone can see, and even an exact deletion
    can leak what you watched unless the public lists get **fresh noise**.

## Why it matters

Viewing and shopping history is sensitive. A US law, the Video Privacy Protection Act (1988), was passed after a
newspaper printed a Supreme Court nominee's video rentals. Recommenders show their links publicly, on every item's page,
so a person's history can be on other people's screens.

## A simple example

A video shop assistant tells customers, "People who liked *this* rare film also liked *that* one." If only one customer
ever rented both, the assistant is repeating that customer's rental history. And if the assistant suddenly *stops*
saying it the day after the customer leaves, anyone paying attention learns what they rented.

## How it works

<!-- diagram: recommender-unlearning -->

Lesson 18 uses MovieLens 100K (943 people, 1,682 films). **Erin** watched 186 films; 11 were watched by nobody else.
See [Recommender systems](../ml-basics/recommender-systems.md) for how the two models work.

### Erin is on other people's screens

On one of her rare films' "also watched" page, **all 10** slots were her other films. Three measurements, compared
with models that never saw her.

| Measurement | Item-kNN with Erin | without | Matrix factorisation with Erin | without |
|---|---|---|---|---|
| Fingerprint (similarity of pairs only she linked) | 0.166 | 0.000 | 0.356 | 0.055 |
| Her rare films' pages showing her other films | 84.1% | 18.4% | 87.3% | 20.2% |
| Fold-in attack (how highly her films rank) | 0.941 | 0.646 | 0.921 | 0.793 |
| Recall@10 for everyone else | 0.348 | 0.347 | 0.421 | 0.421 |

Squeezing data into 32 numbers per film did not hide her. And the business metric (recall for everyone else) did not
see her at all.

### Item-kNN forgets exactly

The co-watch table is a sum over users. Subtracting Erin changed 34,596 cells, **0.27%** of a rebuild, and the result
was identical, bit for bit, to a model built without her.

### Matrix factorisation does not

| Method | Cost (% of retrain) | All checks inside the gold band? |
|---|---|---|
| Delete her user vector | 0% | ❌ nothing the public sees changes |
| Re-solve the films once | 5% | ❌ close, closes over 90% of the gap |
| Re-solve + 8 more rounds | 72% | ✅ |
| Retrain from scratch | 100% | ✅ |

Splitting users into shards (RecEraser) is exact, but costly here. With 8 shards, recall fell to 0.345 and deleting Erin
still cost 68.8% of a retrain, because every shard must still learn all 1,682 films.

### The deletion itself leaks

Save every public page before and after the deletion, and look at which pages changed most. Guessing 186 films as
"Erin's" (chance, 11%).

| What changed | Attacker precision |
|---|---|
| Item-kNN, exact subtraction, similarity scores visible | **100%** |
| Item-kNN, exact subtraction, top-10 lists only | 42% |
| Matrix factorisation, retrained from scratch | 31% to 39% |

"Exact" means the model *after* the deletion is clean. The *difference* between before and after is new information.

### Defences

| Defence | Attacker precision |
|---|---|
| Exact pages | 42% |
| Delete 150 users together | 25% (helps typical users, not unusual ones) |
| Minimum support, at least 2 viewers per pair | **63%**, worse: her pairs drop below the rule and vanish |
| **Fresh random noise** on public counts | **8% to 11%**, back to chance |

Recommendations to each user still use the exact model; only the public pages get noise. The noise must be **new** on
every refresh, and every refresh gives away a little. Working out how much is enough is what **differential privacy** does.

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting the account and the user vector only.** Her influence stays in film vectors and public lists.
    - **Checking recall for everyone else.** It did not move for any method.
    - **Publishing before-and-after lists from exact counts.** The difference reveals the deleted person.

## Key takeaways

- A recommender's public pages can expose individuals, especially unusual ones.
- Item-kNN forgets exactly by subtraction; matrix factorisation needs a retrain for exactness.
- A deletion is itself a piece of news; batching and fixed rules do not hide unusual users.
- Fresh noise on what you publish stops the before-and-after attack.

## Quiz

```quiz
- q: How much did it cost item-kNN to forget Erin exactly?
  options:
    - About 0.27% of a rebuild
    - About 50% of a rebuild
    - A full rebuild
  answer: 0
  why: Only the cells for pairs of her films change, 34,596 of 12.9 million.
- q: After deleting Erin's user vector in matrix factorisation, what changed on public pages?
  options:
    - Nothing
    - Everything
    - Only her own recommendations
  answer: 0
  why: What she taught the model sits in the film vectors, which deleting her row does not touch.
- q: Why can an exact deletion still leak?
  options:
    - Comparing public pages before and after shows what changed, which points to her films.
    - Exact deletions keep a copy of the data.
    - The model is retrained with her data.
  answer: 0
  why: The model after deletion is clean, but the difference between before and after is new information.
- q: Which defence brought the attacker back to chance?
  options:
    - Fresh random noise on the public counts at every refresh
    - A minimum-support rule
    - Deleting users in small batches
  answer: 0
  why: Noise makes the before and after pages differ everywhere, so her deletion gets lost.
- q: Why did the minimum-support rule make the attack worse?
  options:
    - Her pairs with exactly one other viewer dropped below the rule and vanished, pointing to her films.
    - It deleted all public pages.
    - It added her data back.
  answer: 0
  why: A fixed rule creates a sharp edge, and Erin sat right on it.
```

## Try it

- Read the next concept, [Unlearning at scale](unlearning-at-scale.md).
- Run the lesson [18 · Recommender systems](../lessons/18-recommender-systems.md).
