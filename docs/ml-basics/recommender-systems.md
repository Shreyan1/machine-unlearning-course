---
title: Recommender systems
description: Recommenders learn from what people have in common, so your data lives in the links between items and shows up on other people's screens.
---

# Recommender systems

!!! oneline "In one line"
    A recommender suggests items by learning **what people have in common**, for example that people who watched one
    film also watched another.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how item-kNN and matrix factorisation turn "who watched what" into suggestions,
    - work out what forgetting one user changes in each model,
    - say why a person who deleted their account can still be on other people's screens.

## Why it matters

In most models, your data is one row. In a recommender, your data is spread across the **links between items**, and
the service shows those links publicly, on every item's page. Your viewing or shopping history can be private and
sensitive. In 2008, Narayanan and Shmatikov showed that "anonymous" Netflix ratings could be matched back to real, named people.

Recommenders are everywhere, from films and music to shops, news and job sites. When someone closes an account and
asks to be erased, the company usually deletes their profile. That removes the row about them but not what the model
learnt from them, and in a recommender what it learnt is shown to strangers.

## A simple example

A video shop assistant remembers what customers rent together. If one customer always rents rare foreign films, the
assistant starts telling others "people who liked *this* rare film also liked *that* one". Each time, the assistant is
repeating a piece of that customer's rental history. Cutting up her membership card does not make the assistant forget.

Now map the picture onto Lesson 18. The shop is a film service built on **MovieLens 100K**, a real dataset from
1997 and 1998. The customer is **Erin**, who watched 186 films. Half of her films were watched by 26 people or fewer,
while the typical view on the service is of a film watched by 115 people, and 11 of her films were watched by nobody
else at all. The assistant's advice is the public **"people who watched this also watched"** list on each film's page.
Her membership card is her account, which she asks the service to delete.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Who-watched-what table** \(R\) | One row per user and one column per film, with 1 if the user watched it and 0 if not. Star ratings are ignored | 943 users × 1,682 films |
| **Co-watch count** | How many users watched both of two films | 1 for every pair that only Erin watched |
| **Cosine similarity** | A score from 0 to 1 for how alike two films' audiences are, from the co-watch counts | 0 for two films nobody watched together |
| [**Item-kNN**](../start-here/glossary.md#i) | A recommender that suggests films similar to the ones you watched, using co-watch counts | Recall@10 of 0.349 |
| [**Matrix factorisation**](../start-here/glossary.md#m) | A recommender that gives every user and every film a short list of numbers, fitted so that they line up when the user watches the film | 32 numbers each, recall@10 of 0.423 |
| **"Also watched" page** | The public list of the 10 films most similar to one film | The page of *Fall* (1997), all 10 slots Erin's |
| [**Recall@10**](../start-here/glossary.md#r) | The share of a user's hidden films that appear in their top 10 suggestions | 0.210 for just showing the most popular films |

## How it works

<!-- diagram: recommender-systems -->

The course uses real data, **MovieLens 100K**, with 943 people, 1,682 films and 100,000 ratings. It only uses *who watched
what*. Quality is measured with **recall@10**, the share of a user's hidden films that appear in their top 10.

To measure recall, Lesson 18 hides 20% of each user's films before training, which leaves 80,000 views to learn from.
If a user had 5 hidden films and 2 of them appear in their top 10, their recall@10 is 2 ÷ 5 = 0.4. The score for the
service is the average over all users.

### Item-kNN

The whole model is one table, `G`. `G[i, j]` counts how many users watched both film \(i\) and film \(j\). Films are
"similar" when many of the same people watched them. To recommend, the model adds up how similar each film is to the
films you already watched.

Because `G` is a **sum over users**, forgetting a user is a subtraction, exactly like [Naive Bayes](naive-bayes.md).

Here is a tiny made-up service with three users and four films, A to D, to show the idea.

| User | Watched | Adds 1 to these co-watch counts |
|---|---|---|
| User 1 | A, B | A–B |
| User 2 | A, B, C | A–B, A–C, B–C |
| User 3 | C, D | C–D |

So A–B has a count of 2, and A–C, B–C and C–D have a count of 1. The C–D link exists **only because of User 3**. If
User 3 leaves, subtract 1 from each cell their films touch and the C–D link drops to 0. Nothing else changes, and the
table is exactly the one you would get if User 3 had never joined.

??? deep "Go deeper · the formulas behind item-kNN"
    In symbols, the co-watch table is \(G = R^\top R\), which is a sum over users of each user's row times itself. The
    similarity of two films is the cosine

    \[
    S_{ij} = \frac{G_{ij}}{\sqrt{G_{ii}\, G_{jj}}},
    \]

    where \(G_{ii}\) is the number of people who watched film \(i\). In the tiny service, A and B were each watched by
    2 people and together by 2, so \(S_{AB} = 2 / \sqrt{2 \times 2} = 1.0\). C (2 viewers) and D (1 viewer) give
    \(S_{CD} = 1 / \sqrt{2 \times 1} \approx 0.71\). That is high, because D's whole audience also watched C.

    To score films for a user, the model multiplies their row of \(R\) by \(S\), so each film's score is the sum of
    its similarities to the films the user watched. Forgetting user \(u\) subtracts \(u\)'s row times itself from
    \(G\), which changes only the cells for pairs of \(u\)'s films. This is `ItemKNN.unlearn_users` in `mul/recsys.py`.

??? checkpoint "Checkpoint 1 · Erin watched 186 films. How many cells of the co-watch table change when item-kNN forgets her?"
    **34,596.** Every pair of her films loses 1, so 186 × 186 = 34,596 cells change and nothing else does. Building
    the whole table touches 12,927,648 cells, so forgetting her costs 34,596 ÷ 12,927,648, about 0.27% of a rebuild.
    Lesson 18 checked that the result is bit for bit the same as a model that never saw her.

### Matrix factorisation

Every user and every film gets a list of 32 numbers (a vector). If a user's numbers line up with a film's numbers, the
model predicts the user will like it. Training takes turns. It fixes the films and solves each user (a small [ridge regression](linear-and-ridge-regression.md)), then fixes the users and solves each film.

"Line up" means that the numbers multiplied in pairs and added give a large total. With only two numbers instead of
32, a user with (0.9, 0.1) scores a film with (0.8, 0.2) as 0.9 × 0.8 + 0.1 × 0.2 = 0.74, and a film with (0.1, 0.9)
as only 0.18. These numbers are made up, but the course model does the same with 32. In all it holds
32 × (943 + 1,682) = 84,000 numbers, and training repeats the two turns 12 times.

Everything is fitted together, so deleting one user's vector leaves their influence in the **film** vectors.

| Model | Recall@10 | Forgetting a user |
|---|---|---|
| Most popular films (baseline) | 0.210 | N/A |
| Item-kNN | 0.349 | Subtract their counts, exact, 0.27% of a rebuild |
| Matrix factorisation | 0.423 | No sum to subtract; exact needs a retrain |

Matrix factorisation is the more accurate model, which is the usual result. It is also the one that is hard to make
forget. Each film's numbers were solved using every user who watched it, and each user's numbers using every film. A
film that only Erin watched has numbers made mostly of her.

??? checkpoint "Checkpoint 2 · The service deletes Erin's 32 numbers from the matrix factorisation model. Do the pages of her rare films change?"
    **No, not at all.** Her own numbers were only used to recommend films to her. The "also watched" pages come from
    the film numbers, and those were fitted with her. In Lesson 18, her rare films' pages showed her other films in
    83.6% of slots before and after deleting her row.

### The person who left shows up on public pages

In Lesson 18, a user called **Erin** watched 186 films, 11 of which nobody else watched. On one of those films' public
"also watched" pages, all 10 slots were her other films. Deleting her account changed nothing the public could see.

That page was *Fall* (1997). Each of its 10 links was "watched together by 1 user", and that user was Erin. Anyone who
opened the page was reading part of her viewing history. This is not a bug. It is what "also watched" means when only
one person watched.

Squeezing everything into 32 numbers does not hide her either. On the pages of her rare films, those with 10 viewers or
fewer, models trained with Erin filled 87.3% of the slots with her other films, on average over six seeds. Models that
never saw her filled 20.2%. Unusual people are memorised most, exactly like Carol in [Neural networks](neural-networks.md).

## A worked example

Follow Erin's request through both models in Lesson 18.

1. **Her history enters the model.** Her 186 films add 1 to every pair of them in item-kNN's table. In matrix
   factorisation they shape her own 32 numbers and the numbers of every film she watched.
2. **Her taste reaches strangers.** The page of *Fall* (1997) shows 10 films, all hers.
3. **She closes her account.** The service deletes her profile and her 32 numbers. Nothing the public sees changes.
4. **Item-kNN forgets her exactly.** Subtracting her counts changes 34,596 cells, about 0.27% of a rebuild. Her lone
   pairs drop to a count of 0 and vanish from every page.
5. **Matrix factorisation needs more.** Solving every film's numbers again without her costs about 5% of a retrain
   and closes most of the gap, but not all of it. Every check passes only after 8 more rounds of training, at 72% of
   the cost of a retrain.
6. **Everyone else does not notice.** Recall@10 for the other users was 0.421 with Erin and 0.421 without her. The
   number the business watches never saw her.

??? checkpoint "Checkpoint 3 · A team removes Erin and finds recall@10 for everyone else unchanged. They say she is forgotten. What do you check instead?"
    **The parts of the model that are about her.** Look at the pages of her rare films and at how similar the model
    thinks her lone pairs of films are, and compare both with models that never saw her. Recall@10 for others was
    0.421 with and without Erin, so it cannot tell you anything about her.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>10 of 10</strong><span>slots on the page of Fall (1997) were Erin's films</span></div>
<div class="is-good"><strong>0.27%</strong><span>of a rebuild for item-kNN to forget her, bit for bit</span></div>
<div class="is-bad"><strong>83.6%</strong><span>of her rare pages still hers after deleting her 32 numbers</span></div>
<div><strong>0.421</strong><span>recall@10 for everyone else, with or without her</span></div>
</div>

The two models make opposite trades. Item-kNN is less accurate but forgets a user exactly, almost for free.
Matrix factorisation is more accurate but has no sum to subtract, so exact forgetting needs a retrain. Splitting users
into shards, the [SISA](../unlearning/sisa.md) idea, costs a recommender a lot of quality, because it needs other
people to find similar tastes. With 8 shards, recall fell to 0.345, about the level of item-kNN.

The deletion itself can also leak. Comparing public pages before and after shows which films changed, and those are
Erin's. That attack, and the defences against it, are on
[Unlearning in recommenders](../unlearning/recommender-unlearning.md).

## Limits

**The data is small and old.** MovieLens 100K has 943 users and is from 1997 and 1998. Real services have millions of
users and many more signals, such as clicks, time spent and searches.

**Only who watched what.** The course ignores star ratings, so a film someone hated counts the same as one they loved.

**One unusual user.** Erin was chosen because her taste is rare. A typical user, who watches popular films, leaves far
less trace on any single page, which is a task in the notebook.

## In code

```python
from mul import recsys
knn = recsys.ItemKNN().fit(R)      # R: who watched what
knn.unlearn_users([erin])          # subtract her co-watch counts: exact
```

`unlearn_users` returns the number of cells it changed, 34,596 for Erin. `recsys.ImplicitALS(factors=32)` is the matrix
factorisation model, and it has no `unlearn` method because there is no sum to subtract.

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting only the user's own vector.** What they taught the model sits in the item vectors and public lists.
    - **Checking only overall quality.** Recall for everyone else did not move for any method, even the ones that left
      Erin on every page.
    - **Publishing before-and-after lists.** The difference between them reveals what the deleted person watched. See
      [Unlearning in recommenders](../unlearning/recommender-unlearning.md).
    - **Assuming a compact model hides people.** Matrix factorisation's 32 numbers per film still carried Erin onto
      87.3% of the slots on her rare films' pages.
    - **Choosing the most accurate model without a deletion plan.** Item-kNN is less accurate, but it forgets exactly
      for about 0.27% of a rebuild.

## Key takeaways

!!! notes "Notes to take"
    - **Recommender.** Learns what people have in common from a who-watched-what table.
    - **Where your data lives.** In the links between the items you used, shown on public "also watched" pages.
    - **Item-kNN.** Co-watch counts \(G = R^\top R\), a sum over users. Forget by subtracting, 186 × 186 cells for Erin.
    - **Item-kNN cost.** Exact, bit for bit, about 0.27% of a rebuild. Recall@10 0.349.
    - **Matrix factorisation.** 32 numbers per user and per film, fitted together. Recall@10 0.423.
    - **MF forgetting.** Deleting her vector changes nothing public. Exact needs a retrain.
    - **Erin.** 186 films, 11 seen by nobody else. All 10 slots on the page of Fall (1997) were hers.
    - **Trap.** Recall for everyone else stayed at 0.421, so it cannot show she is gone.

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
- q: A user had 4 hidden films, and 1 of them appears in their top 10 suggestions. What is their recall@10?
  options:
    - 0.10
    - 0.40
    - 0.25
  answer: 2
  why: Recall@10 is the share of hidden films that made the top 10, so 1 ÷ 4 = 0.25.
- q: Two films were watched together only by Erin. What is their co-watch count after item-kNN forgets her?
  options:
    - 0, so the link vanishes from every page
    - 1, because counts cannot go down
    - It depends on the random seed.
  answer: 0
  why: Forgetting subtracts 1 from every pair of her films. A pair that only she linked drops to 0 and has no similarity left.
- q: Why does a film that only Erin watched carry her taste even in matrix factorisation?
  options:
    - Matrix factorisation copies her rows onto the page.
    - Its 32 numbers were fitted almost entirely to her, because she was its whole audience.
    - Rare films are always shown first.
  answer: 1
  why: Each film's numbers are solved from the users who watched it. With one viewer, those numbers are mostly made of that viewer.
- q: Why did splitting users into 8 shards hurt the recommender so much?
  options:
    - A recommender needs other people's links, and each shard sees only an eighth of them.
    - Shards delete films at random.
    - Shards make Erin's data larger.
  answer: 0
  why: Recall fell from 0.422 with one shard to 0.345 with 8, about the level of item-kNN, because every shard learns from fewer shared tastes.
```

## Try it

!!! levelup "Level up"
    You can now explain how a recommender learns from shared taste and what it takes to remove one person from it.
    Next quest, [Unlearning concepts](../unlearning/index.md), where these models meet the course's unlearning methods
    and audits.

- Read the concept page [Unlearning in recommenders](../unlearning/recommender-unlearning.md).
- Run the lesson [18 · Recommender systems](../lessons/18-recommender-systems.md).
- In the notebook, pick a typical user instead of Erin and see how much of them is left to remove.
