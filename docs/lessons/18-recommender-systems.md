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

!!! mission "Your mission · about 40 minutes · 2 checkpoints"
    By the end of this lesson you can

    - find where one user hides in two kinds of recommender, using checks the business metric misses,
    - remove her exactly from item-kNN and judge four ways of removing her from matrix factorisation,
    - attack the deletion itself and say which of three defences stops it.

## The story

A film service recommends films from who watched what (MovieLens 100K, 943 people, 1,682 films). **Erin** closes her
account and asks for her viewing history to be erased. She watched 186 films, 11 of which nobody else watched. In a
recommender, your data is spread over the links between items, and the service shows those links on every film's page.

Until now, each person's data was one row, such as one digit or one census record. Here it is different. Half of
Erin's films were watched by 26 people or fewer, while the typical view on the service is of a film watched by 115. She
is Carol again, the unusual person a model has to memorise. And viewing history is private. A US law, the Video Privacy
Protection Act (1988), was passed after a newspaper printed a Supreme Court nominee's rentals.

So the stakes are plain. If the service only deletes her account, strangers can still read her history on its public
pages. And if it deletes her properly but carelessly, the change itself can give her away.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** item-kNN and matrix factorisation (ALS).</li>
<li markdown>**Show the issue.** Erin on public "also watched" pages, a fingerprint and a fold-in attack.</li>
<li markdown>**Untrain** item-kNN by subtraction, and ALS four ways, plus sharding (RecEraser).</li>
<li markdown>**Show the result** against models that never saw her.</li>
<li markdown>**Attack the deletion itself**, and test three defences.</li>
</ol>

## What each step teaches

**Step 1. Two recommenders.** Both use only who watched what, a 1 or a 0, and ignore the star rating. 20% of each
user's films are hidden to measure quality with recall@10. Item-kNN is one table of co-watch counts. ALS gives every
user and film 32 numbers, 84,000 numbers in all, and fits them in 12 rounds.

**Step 2. The issue.** The lesson opens the public page of one of Erin's lone films and finds all 10 slots are her other
films. Then it measures her in three ways against models that never saw her, which is the gold band from Lesson 06.
This step shows that a smaller model, with 32 numbers per film, does not hide her.

**Step 3. Untrain.** Item-kNN forgets by subtraction, which is exact because the table is a sum over users. ALS has no
sum, so the lesson tries four options from cheapest to dearest, and then splits users into shards as SISA did in
Lesson 07.

??? deep "Go deeper · the four ALS options and how cost is counted"
    Cost is counted in **row solves**, one small ridge regression for one user or one film. A full training run is
    12 × (943 + 1,682) = 31,500 row solves.

    1. **Delete her row.** Set Erin's 32 numbers to zero. This is what "delete my account" usually does. Cost 0.
    2. **Re-solve the films once.** Recalculate every film's numbers from the other users only, 1,682 solves. This is
       exact only if the other users' numbers were right, and they were learned while she was there.
    3. **Re-solve, then keep training** for 1, 2, 4 or 8 more rounds without her. Each round adds 2,625 solves.
    4. **Retrain from scratch** without her. Exact, 31,500 solves.

**Step 4. The result.** Every option is checked on four measures against 8 models that never saw Erin. The step teaches
that "most of the way" is not "inside the band", and that one check can pass by luck on the way.

**Step 5. The deletion leaks.** An outsider saves every public page before and after the deletion and guesses that the
most-changed pages are Erin's films. The lesson then tries batching, a minimum-support rule and fresh noise. This step
shows that even an exact deletion gives news away, a trap special to systems that publish what they learn.

## Key results

<div class="stats">
<div class="is-good"><strong>0.27%</strong><span>exact item-kNN deletion, bit for bit</span></div>
<div class="is-bad"><strong>72%</strong><span>of a retrain before ALS passed every check</span></div>
<div class="is-bad"><strong>42%</strong><span>attacker precision on exact top-10 lists</span></div>
<div class="is-good"><strong>9%</strong><span>attacker precision with fresh noise</span></div>
</div>

Recall@10 was 0.210 for popular films, 0.349 for item-kNN and 0.423 for ALS. On one of Erin's rare films' pages, all 10 "also watched"
slots were her other films.

| Measurement | ALS with Erin | ALS without | Gold band ± |
|---|---|---|---|
| Fingerprint | 0.356 | 0.055 | 0.004 |
| Her rare films' pages | 87.3% | 20.2% | 1.4% |
| Fold-in attack | 0.921 | 0.793 | 0.003 |
| Recall@10 for others | 0.421 | 0.421 | 0.004 |

Read the rows from the top. The **fingerprint** is how similar the model thinks the 7,133 pairs of films are that only
Erin linked. The **pages** row is the share of slots on her 69 rarest films' pages that show her other films. The
**fold-in attack** adds her as a new user and checks how highly her films rank, with 1.0 at the top. On all three, ALS
with Erin is far outside the band. The last row is the one the business watches, and it did not move at all.

??? checkpoint "Checkpoint 1 · The band on the fold-in attack is 0.793 ± 0.003. Re-solving the films once gave 0.805. Does Erin still show?"
    **Yes.** The band runs from 0.790 to 0.796, and 0.805 is above it. The cheap update moved the score most of the way
    down from 0.920, but an attacker can still tell this model apart from one that never saw her.

**Item-kNN.** Subtracting Erin updated 34,596 cells (0.27% of a rebuild), identical bit for bit to a model without her.

**ALS.** Deleting her row changed nothing the public sees. Re-solving the films once (5% of a retrain) closed over 90%
of the gap but stayed outside the band, and all checks passed only after 8 more rounds (72%). Sharding with 8 shards cut
recall to 0.345 and still cost 68.8% of a retrain.

??? deep "Go deeper · the full ALS table"

    | Option | Fingerprint | Her pages | Fold-in attack | Recall@10 | Cost |
    |---|---|---|---|---|---|
    | Before | 0.359 ❌ | 0.836 ❌ | 0.920 ❌ | 0.422 ✅ | |
    | Delete her row | 0.359 ❌ | 0.836 ❌ | 0.920 ❌ | 0.422 ✅ | 0% |
    | Re-solve the films once | 0.073 ❌ | 0.223 ❌ | 0.805 ❌ | 0.423 ✅ | 5% |
    | Re-solve + 1 round | 0.066 ❌ | 0.214 ✅ | 0.799 ❌ | 0.422 ✅ | 14% |
    | Re-solve + 2 rounds | 0.063 ❌ | 0.220 ❌ | 0.797 ❌ | 0.421 ✅ | 22% |
    | Re-solve + 4 rounds | 0.060 ❌ | 0.209 ✅ | 0.795 ✅ | 0.420 ✅ | 39% |
    | Re-solve + 8 rounds | 0.058 ✅ | 0.206 ✅ | 0.794 ✅ | 0.421 ✅ | 72% |
    | Retrain from scratch | 0.058 ✅ | 0.204 ✅ | 0.791 ✅ | 0.422 ✅ | 100% |

    The band is fingerprint 0.055 ± 0.004, her pages 0.202 ± 0.014, fold-in 0.793 ± 0.003 and recall 0.421 ± 0.004.
    Notice "her pages" passing after one round and failing after two. That is a lucky pass, and it is why a method
    must pass every check at once.

    Shards cost so much because splitting the users does not split the films. With 2, 4 and 8 shards, recall was 0.396,
    0.370 and 0.345, and forgetting Erin cost 83.3%, 73.7% and 68.8% of a retrain.

**The deletion leaks.** Comparing public pages before and after, an attacker guessing 186 films as Erin's (chance 11%)
was right **100%** of the time with similarity scores visible, 42% with top-10 lists only and 31% even after an ALS
retrain from scratch with a new seed.

| Defence on item-kNN pages | Attacker precision |
|---|---|
| None | 42% |
| Delete 150 users together | 25% |
| Minimum support of 2 | **63%** (worse) |
| Fresh noise, shown if noisy count ≥ 5 | **9%** |

Each row has its own lesson. **Batching** helps the crowd, but 25% is still more than twice chance, because Erin's rare
films still have the most-changed pages. **Minimum support** makes it worse, because every pair she shared with one
other person drops from 2 viewers to 1 and vanishes, and the pages that lose entries are hers. **Fresh noise** makes
the before and after pages differ a little everywhere, so her deletion gets lost. Popular films kept 72% of their true
page at this setting.

??? checkpoint "Checkpoint 2 · Why did a full ALS retrain from scratch, which is exact, still let the attacker reach 31%?"
    **Because the attack reads the change, not the model.** The model after the retrain is clean. But comparing it
    with the pages from before shows which pages moved, and those are mostly Erin's films. 31% is nearly three times
    the 11% of a random guess.

## Limits of this lesson

**One user, one dataset.** Erin is unusual by design, and MovieLens 100K is small and from 1997 and 1998. The tasks ask
you to repeat the lesson with a typical user.

**A simple attacker.** It ranks pages only by how much they changed. One who averages many noisy refreshes can average
the noise away, which the tasks ask you to try.

**The noise is not formal privacy.** The library adds noise in the spirit of differential privacy, but one user touches
many pairs, so a formal promise for a whole user needs noise sized to all of them.

**Random shards only.** RecEraser can group similar users into shards to win back quality. The lesson splits at random.

## Concepts used here

- [Recommender systems](../ml-basics/recommender-systems.md)
- [Unlearning in recommenders](../unlearning/recommender-unlearning.md)
- [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md)

## Notes to take

!!! notes "Notes to take"
    - **Erin.** 186 films, 11 watched by her alone. All 10 slots on one lone film's page were hers.
    - **Wrong test.** Recall for others was 0.421 with and without her. Use the fingerprint, her pages and the fold-in.
    - **Item-kNN.** Subtract 34,596 cells, 0.27% of a rebuild, identical bit for bit.
    - **ALS.** Deleting her row changes nothing public. Re-solving costs 5% and stays outside. All checks pass at 72%.
    - **Shards.** 8 shards cut recall to 0.345 and still cost 68.8%, because every shard learns all films.
    - **The deletion leaks.** 100% with scores visible, 42% with lists, 31% after an exact retrain, against 11%.
    - **Defences.** Batching 150 gave 25%, minimum support gave 63%, fresh noise gave 9%.
    - **Rule.** The noise must be new on every refresh.

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
- q: Re-solving every film once costs 5% of a retrain and closes over 90% of the gap. Why is it not enough?
  options:
    - It makes recall for others much worse.
    - The other users' numbers were learned while Erin was there, so the checks stay outside the band.
    - It deletes the wrong user.
  answer: 1
  why: The fingerprint reached 0.073 against a band of 0.055 ± 0.004. All checks passed only after 8 more rounds, at 72%.
- q: Why did 8 user shards still cost 68.8% of a retrain to forget Erin?
  options:
    - Her data was copied into every shard.
    - The shards were trained for longer.
    - Splitting the users does not split the films, so every shard still learns all 1,682.
  answer: 2
  why: Film rows are 1,682 of the 2,625 rows in each round, about 64%, so even a tiny shard is costly.
- q: Why did the minimum-support rule raise the attacker to 63%?
  options:
    - Pairs she shared with one other person dropped from 2 viewers to 1 and vanished from her films' pages.
    - It showed similarity scores to the public.
    - It added noise that pointed at her.
  answer: 0
  why: A fixed rule creates a sharp edge, and the pages that lost entries were exactly her films.
```

## Open question → Lesson 19

!!! levelup "Level up"
    You can now find a user hidden in a recommender, remove her exactly or nearly, and stop the deletion from leaking.
    Next quest, [Lesson 19 · The method zoo](19-the-method-zoo.md), where many unlearning methods sit the same exam.

This lesson used two old recommenders, and the course so far used eight unlearning methods. The research world has
dozens more. If we put many of them through the same fixed exam, do the new ones do better?

[On to Lesson 19, the method zoo :material-arrow-right:](19-the-method-zoo.md){ .md-button }
