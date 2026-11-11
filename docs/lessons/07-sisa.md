---
title: "Lesson 07 · SISA"
description: Build SISA, forget Carol by retraining one slice of one shard, prove it bit for bit and meet the audit-recipe trap.
---

# Lesson 07 · SISA, exact unlearning for neural networks by design

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 3 · Exact unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 5</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/07-SISA-Exact-Unlearning-by-Design.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/07-SISA-Exact-Unlearning-by-Design.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 35 minutes · 3 checkpoints"
    By the end of this lesson you can

    - build SISA and make it forget Carol by retraining one slice of one shard,
    - prove the result is exact by comparing every weight,
    - explain why the partition decides the bill and the number of shards decides the accuracy,
    - spot an audit that uses references trained with a different recipe.

## The story

Retraining is the only exact option for a network, and it costs a full training run every time. SISA (Bourtoule et al.,
IEEE S&P 2021) brings the user-aware forest of Lesson 03 to neural networks, **S**harded, **I**solated, **S**liced,
**A**ggregated. To forget a row, reload its shard's checkpoint from before its slice and retrain only from there.

Lesson 06 put a price on that full run. One retrain of the course's network is 60 epochs over 1,217 digits, which is
73,020 example-gradients, the course's unit of training work. Every new request pays it again. In Lesson 03 the forest
escaped this by being designed so each user lived in one group of trees, and it retrained 10 of 50. This lesson asks
whether a network can be designed the same way, and what the design costs in accuracy and in audit care.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** SISA with 5 shards × 4 slices.</li>
<li markdown>**Show the issue.** With a random partition, Carol lands in every shard.</li>
<li markdown>**Untrain**, comparing a random partition with a user-aware one.</li>
<li markdown>**Show the result.** Cost, shards touched and accuracy.</li>
<li markdown>**Prove it** bit for bit, then test the audit with the wrong references.</li>
</ol>

## What each step teaches

**Step 1. Train.** Five small networks each train on one fifth of the data, in four slices of 15 epochs each, with a
checkpoint after every slice. Each slice stage trains on all the slices so far. The whole SISA model cost 47,205
example-gradients and scored 98.1% on the test set, against 98.0% for one big network.

**Step 2. Where Carol lives.** A grid of shards and slices counts where her 40 digits landed. With a random partition
they are in every shard, mostly in early slices. This is the same problem as the random-shard forest in Lesson 03.

**Step 3. Untrain.** The random-partition model forgets her as it is. Then a second SISA model is built with a
user-aware partition, which puts all of Carol's digits in the last slice of shard 0. It forgets her the same way.

**Step 4. The bill.** The cost of each design is counted in example-gradients and compared with a full retrain.

**Step 5. Prove it, then try to fool the audit.** A fresh SISA model is trained from scratch with the same layout but
without Carol, and every weight is compared. Then three models whose truth is known are audited with U-LiRA, the
per-example membership test from Lesson 05, against two sets of references.

??? deep "Go deeper · the last part, more shards against accuracy"
    The lesson ends with a sweep. SISA is trained with 1, 2, 5, 10 and 20 shards, always with 4 slices. For each,
    five random training digits are forgotten one at a time and the average cost is recorded, next to test accuracy.
    This shows the price of cheap deletion, and it is where the choice of K is made.

## Key results

<div class="stats">
<div class="is-good"><strong>5.0%</strong><span>of a full retrain to forget Carol, user-aware partition</span></div>
<div><strong>61.4%</strong><span>with a random partition, every shard touched</span></div>
<div class="is-good"><strong>0.0</strong><span>largest weight difference from SISA trained without Carol</span></div>
<div class="is-bad"><strong>0.38 vs 0.50</strong><span>guilty scored below innocent with the wrong references</span></div>
</div>

| Design | Cost to forget Carol | Share of a retrain | Shards touched | Test accuracy |
|---|---|---|---|---|
| Full retrain | 73,020 example-gradients | 100.0% | N/A | 98.0% |
| SISA, random partition | 44,805 | 61.4% | 5 | 98.0% |
| **SISA, user-aware partition** | **3,660** | **5.0%** | **1** | 97.0% |

Read the rows from top to bottom. **The full retrain** is the bill to beat. **The random partition** is exact, and it
saves some work, because each shard redoes only the slices from Carol's earliest one onwards. But her digits sat in
every shard, so all five redid most of their training. **The user-aware partition** put her in the last slice of one
shard. Shard 0 reloaded its third checkpoint and trained its last stage again, 15 epochs over its 244 other digits,
which is 15 × 244 = 3,660. The other four shards did nothing.

??? checkpoint "Checkpoint 1 · The user-aware design cost 3,660 example-gradients. Why is it 15 × 244 and not 15 × 61, the size of one slice?"
    **Because each slice stage trains on all the slices so far.** The last stage of shard 0 trains on all four of its
    slices together, the whole shard of 244 remaining digits, for 15 epochs. What the checkpoint saves is the first
    three stages, not the size of the last one.

**Bit for bit.** Every weight in every shard matched a SISA model trained from scratch without Carol. The largest
difference was **0.0**.

**A bonus.** Even before unlearning, user-aware SISA was far less sure about Carol (not 100% on her digits), because
her data lived in one of five sub-models and averaging diluted it. Isolation is a mild privacy defence in itself.

The numbers show it. The big network scored 100.0% on Carol. The user-aware SISA model scored 67.5% before forgetting
her and 65.0% after, so forgetting changed only one of her digits. That small change does not mean forgetting was
pointless. Before the request her digits were still in shard 0's training data, and exactness is what lets you say
they are gone.

**The hidden trap is auditing with a different recipe.**

| Model under audit | U-LiRA with one-big-network references | U-LiRA with SISA references |
|---|---|---|
| Original, **remembers** Carol | 0.95 | 0.38 |
| Retrain, clean | 0.07 | 0.50 |
| SISA unlearnt, clean (proven) | 0.00 | 0.07 |

With the wrong references, the model that remembers Carol scored *lower* than a clean one. The audit ranked guilty
below innocent.

Read the table by matching each model with its own kind of references. The two big-network models read correctly
in the first column, 0.95 for the one that remembers and 0.07 for the clean one. The SISA model reads correctly in the
second column, 0.07. Mixed the other way, the verdicts break. Membership tests read a model's confidence, and an
average of five small networks has a different confidence pattern from one big network.

??? checkpoint "Checkpoint 2 · An audit of a SISA model gives a U-LiRA score of 0.00 using big-network references. Should you report it as clean?"
    **Not on that evidence.** With mismatched references the scores do not mean what they seem, as the 0.38 against
    0.50 shows. Rerun it with references trained as SISA, with the same shards, slices and epochs. Against those the
    SISA model scored 0.07, and the weight comparison is the stronger proof anyway.

**More shards, less accuracy.** With 5 shards, accuracy was 98.1% and one deletion cost about 10.5% of a retrain. With
20 shards, accuracy was 95.4% and one deletion cost about 2.4%.

??? deep "Go deeper · the full sweep of shards"

    | Shards (K) | Test accuracy | Cost of one deletion |
    |---|---|---|
    | 1 | 98.1% | 54.2% of a retrain |
    | 2 | 98.1% | 24.5% |
    | 5 | 98.1% | 10.5% |
    | 10 | 96.9% | 4.0% |
    | 20 | 95.4% | 2.4% |

    Up to 5 shards nothing is lost here, because each network still has enough data. Beyond that, accuracy starts to
    fall while the cost keeps shrinking. Even K = 1, with no sharding and only slices and checkpoints, roughly halves
    the cost of a deletion, so checkpoints alone are worth having.

??? checkpoint "Checkpoint 3 · Going from 10 shards to 20 cuts the cost of a deletion from 4.0% to 2.4%. What does it cost in accuracy, and when is it worth it?"
    **1.5 points, from 96.9% to 95.4%.** It is worth it only if deletions are frequent enough that saving 1.6 points
    of a retrain on each one outweighs a weaker model for every user. Choosing K is a business decision. Starting
    every shard from a shared pretrained model would soften the drop.

## Limits of this lesson

**One request, one person.** The user-aware design is cheap because it was built around Carol. A request that cuts
across every shard, such as a whole class, would touch them all.

**Carol was placed by hand.** The lesson put her in the last slice on purpose. A real system has to guess in advance
whose data is likely to be deleted.

**A small dataset.** With about 250 digits per shard at K = 5, accuracy holds. With less data per shard, or a harder
task, the drop would come sooner.

**Costs not measured here.** SISA stores K networks and R checkpoints for each, and every prediction runs all K
networks. The notebook's tasks ask you to estimate the storage.

## Concepts used here

- [SISA, sharded training](../unlearning/sisa.md)
- [Decision trees and random forests](../ml-basics/decision-trees-and-random-forests.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

## Notes to take

!!! notes "Notes to take"
    - **SISA.** Sharded, Isolated, Sliced, Aggregated. The user-aware forest of Lesson 03, rebuilt for networks.
    - **To forget.** Reload the shard's checkpoint from before the person's earliest slice and retrain from there.
    - **Bill.** Full retrain 73,020 example-gradients. Random partition 61.4%, user-aware 5.0% (3,660).
    - **Exact.** Every weight matched SISA trained without Carol. Largest difference 0.0.
    - **Late slices.** Put data likely to be deleted last, so less has to be redone.
    - **Bonus.** User-aware SISA scored 67.5% on Carol before forgetting, not 100.0%.
    - **Trap.** With mismatched references, the model that remembered scored 0.38 and a clean one 0.50.
    - **Price of K.** K = 5 kept 98.1% at 10.5% a deletion. K = 20 fell to 95.4% at 2.4%.

## Quiz

```quiz
- q: With a user-aware partition, what share of a full retrain did forgetting Carol cost?
  options:
    - 5.0%
    - 61.4%
    - 100%
  answer: 0
  why: All her data was in one shard, so only one slice of one shard was retrained.
- q: Why did the random partition cost so much more?
  options:
    - Carol's digits landed in every shard.
    - Random partitions are slower to train.
    - It used more slices.
  answer: 0
  why: Every shard holding her data had to be retrained from her earliest slice.
- q: How exact was SISA's unlearning?
  options:
    - Bit for bit identical to SISA trained without Carol
    - Within 5%
    - Only similar in accuracy
  answer: 0
  why: SISA is exact by construction; the largest weight difference was 0.0.
- q: What went wrong when SISA was audited with one-big-network references?
  options:
    - The model that remembered Carol scored as cleaner than a truly clean model.
    - Nothing.
    - The audit crashed.
  answer: 0
  why: An ensemble has a different confidence pattern, so references must use the same recipe.
- q: What happens to accuracy as the number of shards grows?
  options:
    - It can fall, because each shard sees less data.
    - It always rises.
    - It is unaffected.
  answer: 0
  why: At K = 20, test accuracy fell to 95.4%.
- q: Why was Carol put in the last slice of shard 0 in the user-aware design?
  options:
    - The last slice trains fastest.
    - So that forgetting her reloads the latest checkpoint and redoes only the last stage.
    - SISA requires every user to be in a last slice.
  answer: 1
  why: Retraining starts from the checkpoint before her earliest slice. The later that slice, the less work.
- q: How was SISA's exactness proved in this lesson?
  options:
    - Its accuracy on Carol matched the gold band.
    - A membership attack scored it as clean.
    - A fresh SISA model was trained without Carol with the same layout, and every weight matched.
  answer: 2
  why: Comparing weights with a from-scratch model of the same recipe is the strongest evidence. Scores alone cannot prove it.
- q: Even before forgetting, user-aware SISA scored 67.5% on Carol while the big network scored 100.0%. Why?
  options:
    - Her digits shaped only one of five averaged networks, so her influence was diluted.
    - SISA saw fewer of her digits.
    - SISA was trained for fewer epochs on her slice.
  answer: 0
  why: Isolation and averaging are a mild privacy defence, though only forgetting removes her data.
```

## Open question → Lesson 08

!!! levelup "Level up"
    You can now build a network that forgets exactly for a small part of the price, and audit it fairly. Next quest,
    [Lesson 08 · Baselines and traps](08-approximate-baselines-and-traps.md), where the model was not built for
    deletion and the quick fixes begin.

SISA must be chosen **before** training. Most production models were trained as one network, long ago. A request
arrives today. What can you do to a model that is already trained, without retraining it?

[On to Lesson 08, baselines and traps :material-arrow-right:](08-approximate-baselines-and-traps.md){ .md-button }
