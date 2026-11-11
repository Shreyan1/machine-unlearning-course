---
title: SISA, sharded training
description: SISA splits training into shards and slices with checkpoints, so forgetting one person retrains only a small piece, exactly.
---

# SISA (Sharded, Isolated, Sliced, Aggregated)

!!! oneline "In one line"
    SISA splits the training data into separate pieces, trains one model per piece and saves checkpoints, so that
    forgetting someone means retraining only **one small piece**, with an exact result.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how shards, slices and checkpoints let a network forget exactly without a full retrain,
    - work out what one deletion costs from where the person's rows sit,
    - choose a number of shards by weighing deletion cost against accuracy,
    - spot the audit trap of comparing a SISA model with references trained another way.

## Why it matters

For neural networks, retraining is the only exact option, and it is expensive. SISA (Bourtoule et al., IEEE S&P 2021)
makes retraining cheap by **designing the training for deletion** from the start. In Lesson 07 it forgets Carol for
about **5%** of the cost of a full retrain, and the result is identical, weight for weight, to training without her.

The idea is not new to the course. In [Lesson 03](../lessons/03-svm-and-random-forest.md) a random forest forgot Carol
by retraining 10 of its 50 trees, because each user's rows lived in one group of trees. SISA brings that same design to
neural networks and adds one more trick, saved checkpoints inside each piece.

This matters to a team that expects a steady flow of erasure requests. Every full retrain is a full training bill.
SISA turns most of those bills into small ones without giving up exactness, so there is nothing to argue about with an
auditor.

## A simple example

Imagine writing a book in 5 separate notebooks, and photocopying each notebook after every chapter. If someone asks you
to remove a sentence from chapter 3 of notebook 2, you take the photocopy from the end of chapter 2 and rewrite
chapters 3 and 4 of *that notebook only*. The other four notebooks are never touched.

!!! simply "Explain it simply"
    Do not write everything in one big notebook. Write in several small ones, and keep a photocopy after every chapter.
    Then a correction means redoing a little, not everything.

Now map the picture onto SISA. Each notebook is a **shard**, a separate part of the data with its own small network.
Each chapter is a **slice**. Each photocopy is a **checkpoint**, a saved copy of the network's weights. The finished
book is the **aggregate**, the average of all the small networks' answers. Notice where the sentence sits. A sentence
in the last chapter costs one chapter to redo. A sentence in the first chapter costs the whole notebook. That is why
the course puts data likely to be deleted in late slices.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Shard](../start-here/glossary.md#s) | One of the separate parts the training data is split into. Each shard trains its own network | Lesson 07 uses 5 shards |
| [Slice](../start-here/glossary.md#s) | A smaller part of a shard. The shard's data is fed in slice by slice | Each shard has 4 slices |
| [Checkpoint](../start-here/glossary.md#c) | A saved copy of a model's weights at one point in training | SISA saves one after every slice, so 20 in all |
| Isolated | Shards never share data or weights, so one shard's network knows nothing about another's data | Shard 0 never sees a digit from shard 3 |
| Aggregate | Combine the shards' answers into one prediction. SISA averages their probabilities | The average of 5 networks predicts each digit |
| Partition | The plan that says which row goes in which shard and slice | Random, or user-aware |
| [User-aware partition](../start-here/glossary.md#u) | A partition that keeps all of one person's rows in one shard | All 40 of Carol's digits in shard 0, last slice |
| Example-gradient | One training example processed once. The course uses it as the unit of training cost | A full retrain costs 73,020 of them |
| [Exact unlearning](../start-here/glossary.md#e) | A result guaranteed to match retraining without the data | SISA after forgetting Carol, with a largest weight difference of 0.0 |

## How it works

<!-- diagram: sisa -->

| Letter | Idea | Where you have seen it |
|---|---|---|
| **S**harded | Split the data into K separate shards | The forest's shards ([Lesson 03](../lessons/03-svm-and-random-forest.md)) |
| **I**solated | One independent network per shard; shards never share information | Each tree only saw its bag |
| **S**liced | Inside a shard, feed the data in R slices and **save a checkpoint after each** | New |
| **A**ggregated | Predict by averaging the K networks | The forest's vote |

**To forget a row**, find its shard and slice, reload that shard's checkpoint from *before* the slice and retrain from there. Everything else is untouched.

### Training, step by step

1. **Split.** Divide the training rows into K shards, and each shard into R slices. In Lesson 07, K is 5 and R is 4.
   **For Carol this means** her 40 digits get a home. With a random split they scatter. With a user-aware split they
   all go to shard 0, in its last slice.
2. **Train slice by slice.** Each shard starts its own fresh network. It trains for 15 epochs on slice 1, then saves
   a checkpoint. Then it trains on slices 1 and 2 together and saves again, and so on until it has seen all four
   slices. **For Carol this means** that in the user-aware design, the first three checkpoints of shard 0 were saved
   before any of her digits arrived.
3. **Aggregate.** To predict a digit, run all five networks and average their probabilities. **For Carol this means**
   her digits shape only one of the five votes, which already dilutes her influence.

### Forgetting, step by step

1. **Find the rows.** Look up which shard and slice hold each of the person's rows.
2. **Remove them** from those slices.
3. **Reload and retrain.** In each touched shard, reload the checkpoint from just before the earliest slice that held
   the person's rows, and retrain from there to the end. Shards that never held the person are not touched at all.

**For Carol this means**, in the user-aware design, one shard reloads its third checkpoint and redoes only its last
stage. The worked example below prices that at about 5% of a full retrain.

??? deep "Go deeper · why the weights match exactly"
    A network trained twice gives the same weights only if every random choice is the same. The course library makes
    sure of that. Each shard always starts from the same random weights, set by its own seed, and each stage of
    training uses its own fixed seed for the batch order.

    So think about what a model trained from scratch without Carol would do. Shard 0's first three stages never saw
    her, so they are the same as the saved checkpoints. Its last stage, run without her and with the same seed, is the
    same as the retrain SISA just did. The other four shards are unchanged in both cases. Every weight matches, which
    is why the largest difference in Lesson 07 was 0.0.

    One subtle point follows. SISA is exact with respect to **SISA trained without Carol**. It is not the same model
    as one big network trained without her, which is a different recipe with a different gold band.

??? checkpoint "Checkpoint 1 · Suppose Carol's 40 digits had gone into the first slice of shard 0 instead of the last. What happens to the cost of forgetting her?"
    **It goes up, but it stays within one shard.** The checkpoint before the first slice is the fresh start, so shard 0
    must redo all four of its stages. The stages train on one, two, three and four slices of the shard, ten slice-loads
    in all, against four for the last stage alone. That is 2.5 times the work, about 12.5% of a full retrain instead of
    5.0%. This is why data likely to be deleted belongs in late slices.

### The partition decides the bill

Lesson 07 compares designs for forgetting Carol (5 shards × 4 slices).

| Design | Cost to forget Carol | Shards touched | Test accuracy |
|---|---|---|---|
| Full retrain | 100% | N/A | 98.0% |
| SISA, random partition | 61.4% | 5 | 98.0% |
| **SISA, user-aware partition** | **5.0%** | **1** | 97.0% |

With a random split, Carol's digits land in every shard. With a **user-aware** split, all her data is in one shard.

Both SISA designs are exact. The random one saves a little, because each shard redoes only the slices from Carol's
earliest one onwards, but her digits sat in every shard and mostly in early slices. The user-aware one put her in one
slice of one shard, for one point of test accuracy.

<div class="widget" data-widget="sisa" markdown></div>

In the widget, press **Forget Carol** with the box unticked and see how many cells light up. Then tick the box that
keeps each person's rows together and forget her again. Change the number of shards and slices too, and watch the bill
change. The same exactness can cost almost everything or almost nothing, depending only on the layout.

### A worked example, forgetting Carol for 5%

Follow Carol through the user-aware design of Lesson 07.

1. **The bill to beat.** A full retrain of the network runs 60 epochs over the 1,217 digits that are not Carol's.
   That is 60 × 1,217 = 73,020 example-gradients.
2. **Her home.** The 1,217 other digits are split over 5 shards. That is 243 each with 2 left over, so shard 0 gets
   244. Carol's 40 digits are added to the last of its four slices.
3. **Before forgetting.** The SISA model scored 67.5% on Carol's digits, far from the 100.0% of the big network. Her
   digits shaped one network out of five, and averaging diluted them.
4. **The request.** Remove her 40 digits from shard 0, reload its checkpoint from after slice 3 and retrain the last
   stage. That stage runs 15 epochs over the shard's 244 remaining digits, so 15 × 244 = 3,660 example-gradients.
5. **The bill.** 3,660 ÷ 73,020 is about 5.0% of a full retrain. Four shards out of five did nothing at all.
6. **After forgetting.** The model scored 65.0% on Carol, one digit fewer than before. Test accuracy was 97.0%.
7. **The proof.** A new SISA model trained from scratch with the same layout but without Carol had identical weights
   in every shard.

Step 6 is worth a second look. Forgetting moved Carol's score by only one digit, because isolation had already kept
her influence small. Yet the model before forgetting still held her data in shard 0, and the law cares about that, not
about the score. Exactness is what lets you say she is gone.

### Exact, bit for bit

After unlearning, every weight of every shard was **identical** to a SISA model trained from scratch without Carol,
with a largest difference of 0.0. Not "close", not "hard to tell apart", identical. That is the strongest evidence you
can give a regulator.

<div class="stats">
<div class="is-good"><strong>5.0%</strong><span>of a full retrain to forget Carol, user-aware partition</span></div>
<div><strong>61.4%</strong><span>of a full retrain with a random partition, every shard touched</span></div>
<div class="is-good"><strong>0.0</strong><span>largest weight difference from SISA trained without Carol</span></div>
<div><strong>67.5%</strong><span>user-aware SISA on Carol before forgetting, against 100.0% for the big network</span></div>
</div>

Isolation is a mild privacy defence in its own right. The random-partition SISA scored 82.5% on Carol and 80.0% on
unseen thick-marker digits, a gap of 2.5 points. The big network scored 100.0% and 77.5%, a gap of 22.5 points.

### The price (more shards, less accuracy)

| Shards (K) | Test accuracy | Cost of one deletion |
|---|---|---|
| 1 | 98.1% | 54.2% of a retrain |
| 5 | 98.1% | 10.5% |
| 10 | 96.9% | 4.0% |
| 20 | 95.4% | 2.4% |

Each shard sees less data, so beyond a point accuracy falls. Even K = 1 (only slices and checkpoints) roughly halves
the cost of a deletion. Choosing K is a business decision. You weigh expected deletions × retrain cost against the accuracy you can afford to lose. Starting every shard from a shared pretrained model softens the drop.

Here "one deletion" means forgetting one random training digit, averaged over five tries. At 5 shards each network
still had about 250 digits and lost nothing. At 20 it had about 63, and test accuracy fell by 2.7 points, while going
from 10 to 20 shards saved only 1.6 points of cost.

??? deep "Go deeper · the storage and serving bill"
    SISA does not only change the cost of a deletion. It also changes what you must store and run.

    - **Storage.** You keep K networks and R checkpoints for each one. The course's network has about 85,000 weights,
      stored as 4 bytes each. With K = 10 and R = 8, that is 10 × 8 × 85,000 × 4 bytes, about 27 MB. The same layout
      for a model with 100 million weights would need 10 × 8 × 100,000,000 × 4 bytes, about 32 GB.
    - **Serving.** Every prediction runs all K networks, so a prediction costs about K times as much as one network
      of the same size.
    - **Pretraining.** Bourtoule et al. report that the accuracy cost grows on harder tasks and suggest starting every
      shard from a shared pretrained model. That is the pattern of a frozen base model plus a small trainable part per
      shard or per customer, which [Unlearning a fine-tune](unlearning-fine-tunes.md) builds on.

??? checkpoint "Checkpoint 2 · You expect many deletions a month and can afford to lose about one point of test accuracy. Which K from the table fits best?"
    **K = 5.** It keeps 98.1% test accuracy, the same as K = 1, while a deletion costs 10.5% of a retrain instead of
    54.2%. K = 10 is cheaper at 4.0%, but it drops to 96.9%, which is 1.2 points and over your limit. If you could
    afford more loss, K = 10 or 20 would cut the bill further.

!!! warning "Audit with the same recipe"
    When Lesson 07 audited SISA models against references trained as **one big network**, the audit ranked a model that
    still remembered Carol as *cleaner* than a truly clean one. An ensemble of five small networks has a different
    confidence pattern from one big network. References must use the same recipe as the model under test.

The test here was U-LiRA, the per-example membership test of [Membership inference attacks](membership-inference-attacks.md).
It scores how much a model looks as if it still remembers Carol, from 0 (clean) to 1 (remembers).

| Model under audit | Truth | With big-network references | With SISA references |
|---|---|---|---|
| Big network, original | Remembers Carol | 0.95 | 0.38 |
| Big network, retrained | Clean | 0.07 | 0.50 |
| SISA, after forgetting | Clean, proven | 0.00 | 0.07 |

Read the big-network models down the SISA column. The model that remembers Carol scored 0.38 and the clean one scored
0.50, so the guilty model looked cleaner than the innocent one. With matching references, big-network references for
the big network and SISA references for SISA, every verdict was right. Membership tests read a model's confidence, and
an average of five networks is less confident than one big network, so like must be compared with like.

??? checkpoint "Checkpoint 3 · An auditor checks your SISA model against references trained as one big network and it scores 0.00. Is that strong evidence that Carol is gone?"
    **No.** With the wrong references, the scores do not mean what they seem to. In Lesson 07 the same mismatch ranked
    a model that remembered Carol below a clean one. Ask for references trained as SISA, with the same shards, slices
    and epochs. Against those, the SISA model scored 0.07, and its exactness can also be shown from the weights.

## Limits

**It must be chosen before training.** SISA is a way of training, not a repair. A model already trained as one big
network cannot be turned into SISA without training it again from scratch. For those models, see
[Quick fixes and their traps](approximate-unlearning.md).

**The partition only helps for the unit it was built around.** A user-aware split makes forgetting one person cheap.
A request that cuts across every shard, such as a whole class of digits, or a person whose rows were split randomly,
still touches every shard.

**Exact is not the same as passing every test.** In Lesson 11, SISA failed the FORGET check on Carol by one digit,
52.5% against a band starting near 52.6%. Nothing was wrong with SISA. A band built from a few references sometimes
rejects a good model, which the course calls a [false alarm](../start-here/glossary.md#f). SISA's exactness can be
checked from its records instead.

!!! tip "What to do in practice"
    - Decide on SISA before the first training run, and record the partition, the seeds and every checkpoint.
    - Shard by the unit people delete, such as a user, a customer or a document source.
    - Put data likely to be deleted, such as new users or users on a trial, in late slices.
    - Start with a modest K and measure the accuracy drop on your own data before you add more shards.
    - Audit against references trained with the same shards, slices and epochs as the model under test.
    - Keep each deletion's log (rows removed, shard, checkpoint reloaded), so exactness can be shown later.

## In code

??? deep "Go deeper · SISA with a user-aware partition in the course library"
    ```python
    import numpy as np
    from mul import methods, lab
    L = lab.make_lab("carol")

    # A user-aware partition: everyone else split at random, Carol in shard 0, last slice
    others = np.random.default_rng(0).permutation(L.retain_idx)
    partition = [list(np.array_split(sh, 4)) for sh in np.array_split(others, 5)]
    partition[0][3] = np.r_[partition[0][3], L.forget_idx]

    sisa = methods.SISA(lab.model_fn, n_shards=5, n_slices=4, epochs_per_slice=15, seed=0)
    sisa.fit(L.X_train, L.y_train, partition=partition)
    _, info = sisa.unlearn(L.forget_idx)      # retrain only from the checkpoint before Carol's slice
    print(info["samples_processed"], info["shards_retrained"])   # 3,660 example-gradients, 1 shard
    ```

    `unlearn` finds every slice that held a removed row, and in each touched shard it retrains from the earliest such
    slice. Without a `partition`, `fit` splits the rows at random.

## Common mistakes

!!! danger "Mistakes people make"
    - **Sharding randomly.** One person's data then sits in every shard, and forgetting them touches everything.
    - **Putting likely deletions in early slices.** A row in the first slice forces the whole shard to retrain.
    - **Ignoring storage and serving cost.** SISA keeps K models × R checkpoints and runs K models per prediction.
    - **Deciding too late.** SISA must be chosen before training; it cannot be added to an existing model.
    - **Auditing against a big network.** The references must be SISA models trained the same way.

## Key takeaways

!!! notes "Notes to take"
    - **SISA.** Sharded, Isolated, Sliced, Aggregated. The user-aware forest idea, rebuilt for networks, plus checkpoints.
    - **To forget.** Reload the shard's checkpoint from before the person's earliest slice and retrain from there.
    - **Exact.** Bit for bit equal to SISA trained without the data. Largest weight difference 0.0.
    - **Partition decides the bill.** Carol cost 5.0% of a retrain user-aware, 61.4% random.
    - **Late slices.** Data likely to be deleted goes last, so less has to be redone.
    - **Price of K.** K = 5 kept 98.1% at 10.5% a deletion. K = 20 fell to 95.4% at 2.4%.
    - **Running costs.** K networks × R checkpoints to store, K networks to run per prediction.
    - **Bonus.** Isolation dilutes memorisation. User-aware SISA scored 67.5% on Carol, not 100.0%.
    - **Trap.** Audit a SISA model only against SISA references, or guilty can rank below innocent.

## Quiz

```quiz
- q: What does the first "S" in SISA stand for?
  options:
    - Sharded
    - Secure
    - Summed
  answer: 0
  why: The data is split into K separate shards, each with its own model.
- q: Why are checkpoints saved after each slice?
  options:
    - So you can restart from just before the deleted row's slice
    - To make predictions faster
    - To share data between shards
  answer: 0
  why: Retraining only needs to start from the checkpoint before the slice that held the row.
- q: With a user-aware partition, what did forgetting Carol cost in Lesson 07?
  options:
    - About 5% of a full retrain
    - About 61% of a full retrain
    - A full retrain
  answer: 0
  why: All her data was in one shard, so only one slice of one shard was retrained.
- q: How close was the SISA unlearnt model to a SISA model trained without Carol?
  options:
    - Identical, bit for bit
    - About 95% similar
    - Only similar in accuracy
  answer: 0
  why: Every weight of every shard matched exactly. SISA is exact by construction.
- q: What happens as you add more shards?
  options:
    - Deletion gets cheaper, but accuracy can fall.
    - Deletion gets more expensive.
    - Nothing changes.
  answer: 0
  why: Each shard sees less data. At K = 20, test accuracy fell to 95.4% while a deletion cost 2.4% of a retrain.
- q: Why did the random partition still cost 61.4% of a retrain to forget Carol?
  options:
    - SISA is not exact with a random partition.
    - Her digits sat in every shard, mostly in early slices, so every shard redid most of its training.
    - Random partitions need more slices.
  answer: 1
  why: Each touched shard retrains from the earliest slice that held her rows. Spread out and early means a big bill, though the result is still exact.
- q: A team wants to add SISA to a big network they trained last year. What is the honest answer?
  options:
    - It can be added with one extra epoch.
    - It only needs new checkpoints.
    - SISA is a way of training, so the model must be trained again as SISA from the start.
  answer: 2
  why: The shards, slices and checkpoints must exist before the data goes in. For an existing model you need another approach.
- q: An auditor uses one-big-network references to test a SISA model. What can go wrong?
  options:
    - A model that still remembers can score as cleaner than a clean one, because the confidence patterns differ.
    - Nothing, membership tests work the same on any model.
    - The audit becomes too slow to run.
  answer: 0
  why: In Lesson 07 mismatched references ranked a model that remembered Carol as cleaner than a clean one. Compare like with like.
- q: Before any request, user-aware SISA scored 67.5% on Carol while the big network scored 100.0%. Why?
  options:
    - SISA was trained for fewer epochs in total.
    - Her digits shaped only one of five averaged networks, so her influence was diluted.
    - SISA removed her digits during training.
  answer: 1
  why: Isolation and averaging are a mild privacy defence on their own, though only forgetting removes her data.
```

## Try it

!!! levelup "Level up"
    You can now price an exact deletion from a network's layout and audit it against the right references. Next quest,
    [Certified unlearning](certified-unlearning.md), where a model that was not designed for deletion gets a
    mathematical promise instead of an exact copy.

- Read the next concept, [Quick fixes and their traps](approximate-unlearning.md).
- Run the lesson [07 · SISA](../lessons/07-sisa.md).
