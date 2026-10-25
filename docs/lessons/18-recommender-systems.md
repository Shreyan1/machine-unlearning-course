---
title: "Lesson 18 · Recommender systems"
description: Remove a user from item-kNN and matrix factorisation on MovieLens, then attack the deletion itself and stop it with fresh noise.
---

# Lesson 18 · Recommender systems, when your taste is on every page

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 8 · Extensions</span><span class="chip" markdown="span">:material-stairs-up: Rung 12</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb){ .md-button }
</div>

## The story

A film service recommends films from who watched what (MovieLens 100K, 943 people, 1,682 films). **Erin** closes her
account and asks for her viewing history to be erased. She watched 186 films, 11 of which nobody else watched. In a
recommender, your data is spread over the links between items, and the service shows those links on every film's page.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** item-kNN and matrix factorisation (ALS).</li>
<li markdown>**Show the issue**: Erin on public "also watched" pages, a fingerprint and a fold-in attack.</li>
<li markdown>**Untrain** item-kNN by subtraction, and ALS four ways, plus sharding (RecEraser).</li>
<li markdown>**Show the result** against models that never saw her.</li>
<li markdown>**Attack the deletion itself**, and test three defences.</li>
</ol>

## Key results

Recall@10 was 0.210 for popular films, 0.349 for item-kNN and 0.423 for ALS. On one of Erin's rare films' pages, all 10 "also watched"
slots were her other films.

| Measurement | ALS with Erin | ALS without | Gold band ± |
|---|---|---|---|
| Fingerprint | 0.356 | 0.055 | 0.004 |
| Her rare films' pages | 87.3% | 20.2% | 1.4% |
| Fold-in attack | 0.921 | 0.793 | 0.003 |
| Recall@10 for others | 0.421 | 0.421 | 0.004 |

**Item-kNN**: subtracting Erin updated 34,596 cells (0.27% of a rebuild), identical bit for bit to a model without her.

**ALS**: deleting her row changed nothing the public sees. Re-solving the films once (5% of a retrain) closed over 90%
of the gap but stayed outside the band; all checks passed only after 8 more rounds (72%). Sharding with 8 shards cut
recall to 0.345 and still cost 68.8% of a retrain.

**The deletion leaks.** Comparing public pages before and after, an attacker guessing 186 films as Erin's (chance 11%)
was right **100%** of the time with similarity scores visible, 42% with top-10 lists only and 31% even after an ALS
retrain from scratch with a new seed.

| Defence on item-kNN pages | Attacker precision |
|---|---|
| None | 42% |
| Delete 150 users together | 25% |
| Minimum support of 2 | **63%** (worse) |
| Fresh noise, shown if noisy count ≥ 5 | **9%** |

## Concepts used here

- [Recommender systems](../ml-basics/recommender-systems.md)
- [Unlearning in recommenders](../unlearning/recommender-unlearning.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Quiz

```quiz
- q: Why is item-kNN easy to unlearn exactly?
  options:
    - Its co-watch table is a sum over users.
    - It has no data.
    - It is a neural network.
  answer: 0
  why: Subtracting one user's co-watch counts gives exactly the table without them.
- q: In ALS, what did deleting Erin's user vector change on public pages?
  options:
    - Nothing
    - Everything
    - Only her recommendations
  answer: 0
  why: What she taught the model sits in the film vectors.
- q: Recall@10 for everyone else was the same with or without Erin. What does that show?
  options:
    - The business metric is the wrong test for whether she was forgotten.
    - She was never in the data.
    - The model is broken.
  answer: 0
  why: The public pages were full of her while recall did not move.
- q: Why does even a retrain from scratch leak?
  options:
    - The difference between before and after pages is new information about her.
    - Retraining keeps her data.
    - The seed reveals her.
  answer: 0
  why: Exact means the model after is clean; the change itself still points to her films.
- q: Which defence brought the attacker back to about chance?
  options:
    - Fresh random noise on public counts
    - A minimum-support rule
    - Batching 150 deletions
  answer: 0
  why: Noise makes every page change a little at random, hiding her deletion.
```

## Open question → Lesson 19

This lesson used two old recommenders, and the course so far used eight unlearning methods. The research world has
dozens more. If we put many of them through the same fixed exam, do the new ones do better?

[On to Lesson 19, the method zoo :material-arrow-right:](19-the-method-zoo.md){ .md-button }
