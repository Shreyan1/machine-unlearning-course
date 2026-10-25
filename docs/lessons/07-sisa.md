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

## The story

Retraining is the only exact option for a network, and it costs a full training run every time. SISA (Bourtoule et al.,
IEEE S&P 2021) brings the user-aware forest of Lesson 03 to neural networks, **S**harded, **I**solated, **S**liced,
**A**ggregated. To forget a row, reload its shard's checkpoint from before its slice and retrain only from there.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** SISA with 5 shards × 4 slices.</li>
<li markdown>**Show the issue**: with a random partition, Carol lands in every shard.</li>
<li markdown>**Untrain**, comparing a random partition with a user-aware one.</li>
<li markdown>**Show the result**: cost, shards touched and accuracy.</li>
<li markdown>**Prove it** bit for bit, then test the audit with the wrong references.</li>
</ol>

## Key results

| Design | Cost to forget Carol | Share of a retrain | Shards touched | Test accuracy |
|---|---|---|---|---|
| Full retrain | 73,020 example-gradients | 100.0% | N/A | 98.0% |
| SISA, random partition | 44,805 | 61.4% | 5 | 98.0% |
| **SISA, user-aware partition** | **3,660** | **5.0%** | **1** | 97.0% |

**Bit for bit.** Every weight in every shard matched a SISA model trained from scratch without Carol. The largest
difference was **0.0**.

**A bonus.** Even before unlearning, user-aware SISA was far less sure about Carol (not 100% on her digits), because
her data lived in one of five sub-models and averaging diluted it. Isolation is a mild privacy defence in itself.

**The hidden trap is auditing with a different recipe.**

| Model under audit | U-LiRA with one-big-network references | U-LiRA with SISA references |
|---|---|---|
| Original, **remembers** Carol | 0.95 | 0.38 |
| Retrain, clean | 0.07 | 0.50 |
| SISA unlearnt, clean (proven) | 0.00 | 0.07 |

With the wrong references, the model that remembers Carol scored *lower* than a clean one. The audit ranked guilty
below innocent.

**More shards, less accuracy.** With 5 shards, accuracy was 98.1% and one deletion cost about 10.5% of a retrain. With
20 shards, accuracy was 95.4% and one deletion cost about 2.4%.

## Concepts used here

- [SISA, sharded training](../unlearning/sisa.md)
- [Decision trees and random forests](../ml-basics/decision-trees-and-random-forests.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

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
```

## Open question → Lesson 08

SISA must be chosen **before** training. Most production models were trained as one network, long ago. A request
arrives today. What can you do to a model that is already trained, without retraining it?

[On to Lesson 08, baselines and traps :material-arrow-right:](08-approximate-baselines-and-traps.md){ .md-button }
