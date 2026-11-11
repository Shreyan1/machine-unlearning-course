---
title: Unlearning in recommenders
description: In a recommender your data lives in public "also watched" lists. Item-kNN forgets exactly, matrix factorisation does not, and the deletion itself can leak.
---

# Unlearning in recommenders

!!! oneline "In one line"
    In a recommender, your data lives in the **links between items** that everyone can see, and even an exact deletion
    can leak what you watched unless the public lists get **fresh noise**.

!!! mission "Your mission · about 18 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why deleting a user's account and vector leaves their history on other people's screens,
    - say which recommender forgets exactly for almost nothing and which needs most of a retrain,
    - spot the before-and-after attack and pick the one defence that stops it.

## Why it matters

Viewing and shopping history is sensitive. A US law, the Video Privacy Protection Act (1988), was passed after a
newspaper printed a Supreme Court nominee's video rentals. Recommenders show their links publicly, on every item's page,
so a person's history can be on other people's screens.

Earlier lessons had one row per person, such as one digit or one census record. A recommender is different. It learns
from what people have **in common**, "people who watched film A also watched film B". So your data is not in one place.
It is spread over the links between all the films you watched, and each of those links can sit on a page that strangers
read.

This matters to anyone who runs a shop or a streaming service and gets an erasure request under GDPR Art. 17.
Deleting the account removes almost nothing the public sees, and the act of deleting can itself tell the world what
the person watched.

## A simple example

A video shop assistant tells customers, "People who liked *this* rare film also liked *that* one." If only one customer
ever rented both, the assistant is repeating that customer's rental history. And if the assistant suddenly *stops*
saying it the day after the customer leaves, anyone paying attention learns what they rented.

!!! simply "Explain it simply"
    Cutting up a customer's membership card does not make the shop assistant forget what they rented together. To
    really forget, the assistant has to unlearn the links. And if the assistant goes quiet about exactly those films the
    next day, the silence gives the secret away.

In the course, the customer is **Erin**, the assistant's habit is each film's "also watched" list, and going quiet
the next day is the before-and-after leak.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Item-kNN](../start-here/glossary.md#i) | A recommender built from one table that counts how many people watched each pair of films | A count of 1 for two of Erin's rare films, because only she watched both |
| Co-watch count | One cell of that table, the number of users who watched both films | 34,596 of these cells hold a pair of Erin's films |
| [Matrix factorisation](../start-here/glossary.md#m) | A recommender that gives every user and every film 32 numbers and predicts a match when they line up | 84,000 numbers in all for 943 users and 1,682 films |
| [Recall@10](../start-here/glossary.md#r) | The share of a user's hidden films that appear in their top 10 | 0.423 for matrix factorisation, 0.210 for "most popular" |
| Fingerprint | How similar a model thinks the pairs of films are that only Erin linked | 0.356 with her, 0.055 without |
| Fold-in attack | An outsider adds Erin as a new user and checks how highly the model ranks her films | 0.921 with her, 0.793 without |
| Diff attack | Saving every public page before and after a deletion and guessing that the most-changed pages are the person's films | Right 100% of the time when similarity scores are visible |
| Minimum support | A rule that only shows a pair of films if at least a set number of people watched both | Support of 2 made the attack worse, 63% |
| [Differential privacy](../start-here/glossary.md#d) | A way to add measured random noise so that no one person changes what is published by much | Fresh noise on the pages cut the attack to about chance |

## How it works

<!-- diagram: recommender-unlearning -->

Lesson 18 uses MovieLens 100K (943 people, 1,682 films). **Erin** watched 186 films, and 11 were watched by nobody else.
See [Recommender systems](../ml-basics/recommender-systems.md) for how the two models work.

The figure has two halves. On the left, item-kNN keeps a table of sums, and the yellow cells are the ones Erin added
to. Subtracting her pairs gives a table identical to a rebuild. On the right, matrix factorisation links Erin's vector to
the vectors of the films she watched. Deleting her vector leaves her mark on those films, so they must be re-solved.

Erin is unusual. Half of her films were watched by 26 people or fewer, while the typical view on the service is of a film
watched by 115 people. This is Carol again, from [Deleting is not forgetting](deleting-vs-unlearning.md). An unusual
person is exactly the person a model has to memorise, because nobody else looks like her.

### Erin is on other people's screens

On one of her rare films' "also watched" page, **all 10** slots were her other films. Each link was there because of one
person, her. Three measurements, compared with models that never saw her, show how much of her each model holds.

| Measurement | Item-kNN with Erin | Without | Matrix factorisation with Erin | Without |
|---|---|---|---|---|
| Fingerprint (similarity of pairs only she linked) | 0.166 | 0.000 | 0.356 | 0.055 |
| Her rare films' pages showing her other films | 84.1% | 18.4% | 87.3% | 20.2% |
| Fold-in attack (how highly her films rank) | 0.941 | 0.646 | 0.921 | 0.793 |
| Recall@10 for everyone else | 0.348 | 0.347 | 0.421 | 0.421 |

Read the rows one at a time.

- **Fingerprint.** 7,133 pairs of her films were watched together by nobody else. A model that never saw her has no
  reason to call them similar.
- **Her pages.** These are the pages of her 69 films with 10 viewers or fewer. With her, nearly 9 slots in 10 show her
  other films.
- **Fold-in attack.** A score of 1.0 means her films sit at the very top. Models that saw her rank her films higher.
- **Recall@10.** This is the number the business watches. It did not move.

Squeezing data into 32 numbers per film did not hide her. Her rare films had so few viewers that their numbers were
mostly made of her.

??? checkpoint "Checkpoint 1 · After a deletion, recall@10 for everyone else is 0.421, the same as before. Can the team say Erin is forgotten?"
    **No.** Recall was 0.421 both with Erin and without her, so it cannot tell the two models apart. On her rare
    films' pages, 87.3% of slots showed her other films with her and 20.2% without, and that is the kind of check that
    sees her. A quality
    number measures the crowd, and forgetting is about one person.

### Item-kNN forgets exactly

The co-watch table is a sum over users. Subtracting Erin changed 34,596 cells, **0.27%** of a rebuild, and the result
was identical, bit for bit, to a model built without her.

The steps are short.

1. Find her 186 films.
2. For every pair of them, take 1 off the co-watch count. That is 186 × 186 = 34,596 cells and nothing else.
3. Work out the similarities again from the new counts.

Her 7,133 lone pairs drop to a count of zero, so they vanish from every page. **For Erin this means** the public pages
are exactly what they would be if she had never joined.

??? deep "Go deeper · why a subtraction is exact"
    Write Erin's row as \(r\), a list of 1,682 zeros and ones. The co-watch table is \(G = \sum_u r_u^\top r_u\), one
    small table per user, added up. Taking her out gives \(G - r^\top r\), which is exactly the sum over everyone else.
    The similarity of two films is their count divided by the square root of each film's own count, and those own
    counts sit on the diagonal of the same table. So the similarities come out identical too.

    This is the same idea as Naive Bayes in [Exact unlearning for classical models](exact-unlearning-classical.md).
    Any model that is a sum over people can forget a person by subtraction (Cao and Yang 2015). Building the table
    from scratch touched 12,927,648 cells, so 34,596 ÷ 12,927,648 is 0.27%.

### Matrix factorisation does not

Matrix factorisation has no sum to subtract from. Every user's numbers were fitted against every film's numbers, and the
other way round, 12 times over. So Erin is mixed into the film numbers, and through them into everyone else's numbers.
The lesson tries four ways to remove her, from cheapest to dearest. Each is checked against 8 models that never saw her.

| Method | Cost (% of retrain) | All checks inside the gold band? |
|---|---|---|
| Delete her user vector | 0% | ❌ nothing the public sees changes |
| Re-solve the films once | 5% | ❌ close, closes over 90% of the gap |
| Re-solve + 8 more rounds | 72% | ✅ |
| Retrain from scratch | 100% | ✅ |

**Deleting her vector does nothing for the public.** Her own 32 numbers were only used to recommend films *to her*.
What she taught the model sits in the film numbers. This is the course's first lesson, deleting is not forgetting, in a
new setting.

**One cheap update does most of the work.** Re-solving every film's numbers without her is one small ridge regression
per film. It moved the fingerprint from 0.359 to 0.073, against 0.058 for a retrain. But the band is narrow, 0.055 ±
0.004, so 0.073 is still outside. The other users' numbers were learned while she was there, and washing that out takes
many more rounds.

**Watch for a lucky pass.** After one extra round, "her pages" passed while the other checks failed. After two rounds
it failed again. A method passes only when *every* check passes, as in [The unlearning audit](unlearning-audit.md).

Splitting users into shards (RecEraser) is exact, but costly here. With 8 shards, recall fell to 0.345 and deleting Erin
still cost 68.8% of a retrain, because every shard must still learn all 1,682 films.

Shards hurt a recommender more than the digit classifier in [SISA](sisa.md), because a recommender works by finding
people with similar taste, and a shard sees only its own users' links. With 8 shards, recall falls to about the level of
plain item-kNN, which forgets exactly for almost nothing. If you must be able to delete people, the "weaker" model can be
the better choice.

??? deep "Go deeper · counting the cost in row solves"
    The lesson counts cost in **row solves**, one small calculation for one user or one film. A full training run is
    12 rounds over 943 users and 1,682 films, so 12 × 2,625 = 31,500 row solves.

    - **Re-solve the films once** is 1,682 solves, and 1,682 ÷ 31,500 is about 5%.
    - **Re-solve and 8 more rounds** adds 8 × 2,625 = 21,000, so 22,682 ÷ 31,500 is 72%.
    - **One shard** still needs all 1,682 film rows in every round. Of the 2,625 rows in a round, 1,682 are films, which
      is 64%. So even a shard with very few users costs well over half a retrain.

    | Shards | Recall@10 for others | Cost to forget Erin |
    |---|---|---|
    | 1 | 0.422 | 100% |
    | 2 | 0.396 | 83.3% |
    | 4 | 0.370 | 73.7% |
    | 8 | 0.345 | 68.8% |
    | Item-kNN, subtract | 0.347 | 0.27% |

    Chen et al. (2022) win back some quality with smarter ways of splitting shards, but every shard still learns the films.

??? checkpoint "Checkpoint 2 · A team re-solves the films once, for 5% of a retrain. The fingerprint is 0.073 and the band is 0.055 ± 0.004. Do they pass?"
    **No.** The band runs from 0.051 to 0.059, and 0.073 is above it. The cheap update closed most of the gap from
    0.359, but "most of the way" is not inside the band. In the lesson every check passed only after 8 more rounds,
    at 72% of a retrain.

### The deletion itself leaks

Save every public page before and after the deletion, and look at which pages changed most. The attacker names 186 films
as "Erin's", and we count the share that really are hers. A random guess gets about 11%, because 186 ÷ 1,682 is 11%.

| What changed | Attacker precision |
|---|---|
| Item-kNN, exact subtraction, similarity scores visible | **100%** |
| Item-kNN, exact subtraction, top-10 lists only | 42% |
| Matrix factorisation, retrained from scratch | 31% to 39% |

"Exact" means the model *after* the deletion is clean. The *difference* between before and after is new information.

If the service shows similarity scores, the only films whose scores change are hers, so the attacker gets her whole
history. Even a full retrain leaks, at 39% with the same seed and 31% with a new one. Calandrino et al. (2011) used
the same trick on real shopping sites.

### Defences

| Defence | Attacker precision |
|---|---|
| Exact pages | 42% |
| Delete 150 users together | 25% (helps typical users, not unusual ones) |
| Minimum support, at least 2 viewers per pair | **63%**, which is worse, because her pairs drop below the rule and vanish |
| **Fresh random noise** on public counts | **8% to 11%**, back to chance |

Recommendations to each user still use the exact model, and only the public pages get noise. The noise must be **new** on
every refresh, and every refresh gives away a little. Working out how much is enough is what **differential privacy** does.

Each defence fails or works for a reason worth remembering.

=== "Batching"

    Deleting more people at once helps the crowd, but 25% with 150 users is still more than twice chance. Typical
    users watch popular films whose pages hardly change, so Erin's rare films still have the most-changed pages.

=== "Minimum support"

    A rule of "at least 2 viewers per pair" removes every slot based on one person, so the leak on her pages is gone.
    But when Erin leaves, every pair she shared with exactly one other person drops from 2 viewers to 1 and vanishes.
    The pages that lose entries are exactly her films. A fixed rule creates a sharp edge, and Erin sits on it.

=== "Fresh noise"

    Each refresh adds new random noise to every co-watch count, and a pair is shown only if its noisy count is high
    enough. The before and after pages now differ a little everywhere, at random. Her deletion gets lost in that. The
    price is paid on the public pages, which become less exact for everyone.

??? deep "Go deeper · the noise settings and their price"
    The course library adds random noise of a set size to every "watched together" count and shows a pair only if its
    noisy count reaches a minimum. Every release uses a new seed, so the noise is fresh.

    | How the pages are published | Attacker precision | Popular pages kept | Slots resting on one person |
    |---|---|---|---|
    | Exact pages | 42% | 100% | 4,578 |
    | Minimum support of 2 | 63% | 100% | 0 |
    | Noise 1, shown if noisy count ≥ 3 | 11% | 58% | 3,853 |
    | Noise 1, shown if noisy count ≥ 5 | 9% | 72% | 2,978 |
    | Noise 2, shown if noisy count ≥ 10 | 8% | 46% | 2,731 |

    Some noisy slots still rest on one person. But such a pair now appears only a few times more often than a pair
    nobody watched, so no single slot proves anything. The library's own notes say this is noise in the spirit of
    differential privacy, not a formal promise for each user. One user touches many pairs, so a formal promise needs
    noise scaled to that whole contribution.

??? checkpoint "Checkpoint 3 · To save effort, a team adds noise to the pages once and reuses the same noise on every refresh. Is Erin safe?"
    **No.** If the noise before and after is the same, it cancels when the attacker compares the two pages, and the
    difference is exact again. The noise must be new on every refresh. Even then, an attacker who averages many
    refreshes can average the noise away, which is why the total needs a privacy budget.

## A worked example

Follow Erin's request through the service.

1. **The usual deletion.** The service deletes Erin's account and her 32 numbers in matrix factorisation. Her rare
   films' pages still show her other films in 83.6% of slots, exactly as before. Recall for everyone else stays at
   0.422, so no alarm goes off.
2. **The exact fix.** On item-kNN the service subtracts her 34,596 co-watch cells, for 0.27% of a rebuild.
3. **The leak.** A crawler saved every page the day before. Comparing the two days, it names 186 films. With exact
   top-10 lists, 42% are hers, about 4 times the 11% of a random guess (42 ÷ 11 is about 3.8).
4. **The defence.** The service publishes its pages from counts with fresh noise, shown only if the noisy count is at
   least 5. The attacker falls to 9%, while popular films keep 72% of their true page.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>0.27%</strong><span>cost of an exact item-kNN deletion</span></div>
<div class="is-bad"><strong>0%</strong><span>of the public view changed by deleting her vector</span></div>
<div class="is-bad"><strong>100%</strong><span>attacker precision when scores are visible</span></div>
<div class="is-good"><strong>9%</strong><span>attacker precision with fresh noise, below chance</span></div>
</div>

An exact deletion is almost free in item-kNN and costs most of a retrain in matrix factorisation. But neither kind of
exactness protects Erin on the public pages. Only how the pages are published does.

??? deep "Go deeper · every way to remove Erin, side by side"

    | Model | How Erin is removed | Exact? | Cost | Inside the gold band? | Public pages after |
    |---|---|---|---|---|---|
    | Item-kNN | Subtract her co-watch counts | Yes, bit for bit | 0.27% of a rebuild | Always | Her lone pairs gone |
    | Matrix factorisation | Delete her user vector | No | 0% | No, nothing changes | Unchanged |
    | Matrix factorisation | Re-solve the films, then more rounds | No | 5% to 72% | Only at high cost | Mostly cleaned |
    | Matrix factorisation | Retrain from scratch | Yes | 100% | Yes | Cleaned |
    | Matrix factorisation, 8 shards | Retrain her shard | Yes | 68.8% | Yes | Cleaned, worse recommendations |
    | Any of the above | Compare public pages before and after | Not applicable | Not applicable | Not applicable | Shows her films unless fresh noise is used |

## Limits

**It is one small, old dataset.** MovieLens 100K has 943 people from 1997 and 1998. A real service is far bigger, so
the sizes will differ, though the reasons behind them do not.

**Erin is the hard case.** Typical users watch popular films whose pages hardly change, so they leave less behind.

**The noise is not a formal guarantee.** It beats this attack, but a real release needs noise sized to everything one
user touches, and a budget for the number of refreshes.

**The attacker is simple.** It only ranks pages by how much they changed. One who averages many refreshes could do
better.

!!! tip "What to do in practice"
    - Keep the **private** part (recommendations shown to one user) apart from the **public** part (pages, "trending"
      lists, shared item numbers), and treat the public part as a data release.
    - Prefer a model that is a sum, such as item-kNN, where you must delete people often. It forgets exactly for almost
      nothing.
    - After an approximate update to matrix factorisation, run the fold-in attack and the fingerprint against models
      that never saw the user, not just recall.
    - Publish public pages from counts with fresh noise and a privacy budget, never from exact counts.
    - Refresh public lists on a schedule that mixes deletions with normal new activity, so one deletion never shows up as
      a clean before-and-after pair.
    - Track every copy of item numbers sent to other teams, such as search or ads, in your
      [lineage registry](enterprise-playbook.md).

## In code

```python
from mul import recsys as rs
before = rs.ItemKNN().fit(R)                         # R is who watched what, one row per user
after = rs.ItemKNN().fit(R)
cells = after.unlearn_users([ERIN])                  # subtract her co-watch counts, exact
score = rs.diff_attack(rs.also_watched(before), rs.also_watched(after))
print(rs.precision_at(score, erin))                  # share of the attacker's guesses that are hers
noisy = rs.noisy_also_watched(after, 1, 5, seed=11)  # publish with fresh noise, shown if noisy count >= 5
```

For matrix factorisation, `rs.ImplicitALS(seed=0).fit(R_without)` retrains from scratch.

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting the account and the user vector only.** Her influence stays in film vectors and public lists.
    - **Checking recall for everyone else.** It did not move for any method.
    - **Publishing before-and-after lists from exact counts.** The difference reveals the deleted person.
    - **Calling an approximate update done because it closed 90% of the gap.** The band is narrow, and 0.073 is still
      outside 0.055 ± 0.004.
    - **Trusting a minimum-support rule.** It made the attack worse, 63% against 42%, because her pairs sat on its edge.

## Key takeaways

!!! notes "Notes to take"
    - **Where the data lives.** In the links between items, shown on public pages. Deleting the account removes none of
      them.
    - **The wrong test.** Recall for everyone else was 0.421 with and without Erin. Check her pages, the fingerprint
      and a fold-in attack.
    - **Item-kNN.** A sum over users, so forgetting is a subtraction. 34,596 cells, 0.27% of a rebuild, bit for bit.
    - **Matrix factorisation.** Deleting her vector changes nothing public. Re-solving costs 5% but stays outside the
      band. All checks pass only at 72%.
    - **Shards.** Exact, but 8 shards cut recall to 0.345 and still cost 68.8%, because every shard learns all films.
    - **The deletion leaks.** Before-and-after pages found her films 100% of the time with scores visible and 42% with
      lists only, against 11% chance.
    - **Defences.** Batching 150 users gave 25%. Minimum support gave 63%, worse. Fresh noise gave 8% to 11%.
    - **Rule.** The noise must be new on every refresh, and many refreshes need a privacy budget.

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
- q: Why did 8 user shards still cost 68.8% of a retrain to forget Erin?
  options:
    - Erin was copied into every shard.
    - Every shard must still learn numbers for all 1,682 films.
    - The shards were trained twice as long.
  answer: 1
  why: Splitting the users does not split the films. Film rows are 1,682 of the 2,625 rows in each round, about 64%.
- q: Squeezing every film into 32 numbers did not hide Erin. Why not?
  options:
    - The 32 numbers were copied from her account.
    - Matrix factorisation stores the co-watch table as well.
    - Her rare films had so few viewers that their numbers were mostly made of her.
  answer: 2
  why: With her, 87.3% of her rare films' slots showed her other films, against 20.2% without her.
- q: Batching 150 deletions cut the attack to 25%. Why did it not protect Erin fully?
  options:
    - Typical users' popular pages hardly change, so her rare films still had the most-changed pages.
    - Batching only works for matrix factorisation.
    - The batch was deleted one user at a time.
  answer: 0
  why: Batching hides the crowd, but 25% is still more than twice the 11% of a random guess.
- q: A team publishes noisy pages, but uses the same noise before and after the deletion. What happens?
  options:
    - The attacker falls to chance.
    - The noise cancels, so the difference is exact again.
    - The pages become empty.
  answer: 1
  why: Only fresh noise on every refresh makes the before and after pages differ at random.
```

## Try it

!!! levelup "Level up"
    You can now find where a person hides in a recommender, remove them exactly or nearly, and stop the deletion from
    leaking. Next quest, [Unlearning at scale](unlearning-at-scale.md), where the requests arrive by the thousand.

- Run the lesson [18 · Recommender systems](../lessons/18-recommender-systems.md).
- In the notebook, pick a typical user whose films have a median audience above 100 and run the diff attack on them.
- Publish 20 noisy refreshes before and after, let the attacker average them, and count how many it takes to find Erin.
