---
title: Decision trees and random forests
description: A decision tree asks yes/no questions; a random forest is a committee of trees, each trained on its own bag of rows.
---

# Decision trees and random forests

!!! oneline "In one line"
    A **decision tree** answers by asking a chain of yes/no questions, and a **random forest** is a committee of many
    trees that vote.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how a forest can forget a row exactly by rebuilding only some of its trees,
    - work out why one row reaches about 63% of bootstrap trees and Carol reaches all of them,
    - design a forest that forgets one person cheaply, and say what it costs.

## Why it matters

Trees have no gradient and no formula, so none of the tricks from earlier models work. Yet forests can still forget
exactly, because each tree only saw **part** of the data. You only rebuild the trees that met the deleted row. This idea,
**locality by design**, leads straight to [SISA](../unlearning/sisa.md), the main exact method for neural networks.

Forests are everywhere in real systems, in credit scoring, fraud checks and ranking. So "how much of the forest must I
rebuild for this request?" is a question many teams will face. Lesson 03 shows that the answer can be "all of it" or
"a fifth of it" for the same algorithm on the same data. The difference is a choice made on the day the forest was
trained.

## A simple example

A doctor's checklist might ask, "Fever? Yes. Cough? No. Rash? Yes. Then it is probably X." A random forest is
like asking 50 doctors, each of whom trained on different patients, and taking a vote.

!!! simply "Explain it simply"
    If one patient asks to be removed from the doctors' training, you only need to retrain the doctors who saw that
    patient. The others never met them, so they are already exactly what they would have been without them.

The catch is in how the patients were shared out. If each patient was shown to most of the doctors, you must retrain
most of them. If each patient saw only one small group of doctors, you retrain only that group. In the course, the
patients are digits, the doctors are trees and the patient who asks to leave is Carol.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Decision tree | A model that answers by following a chain of yes/no questions to a final box | "Is pixel 27 brighter than 5?" |
| Split | One yes/no question that divides the data into two groups | The first question at the top of a tree |
| Leaf | A final box at the bottom of a tree, which gives the answer | A leaf that says "this is a 7" |
| Random forest | Many trees, each trained a little differently, that vote | 50 trees in Lesson 03 |
| Bag | The list of training rows one tree was trained on | Each tree's own sample of the 1,257 digits |
| Bootstrap | Drawing \(n\) rows *with replacement* from \(n\), so some rows repeat and others are left out | The classic way to make a bag |
| [Shard](../start-here/glossary.md#s) | A separate group of rows. Trees in one shard only draw from that group | 5 shards of 10 trees each |
| [User-aware partition](../start-here/glossary.md#u) | Sharding so that all of one person's rows sit in the same shard | Carol's 40 digits all in shard 0 |
| Random seed | A starting number that fixes a tree's random choices, so the same bag gives the same tree | Each tree has its own fixed seed |

## How it works

<!-- diagram: decision-trees-and-random-forests -->

The figure has two halves. On the left, one tree asks "income > 50k?" and then a second question, and each path ends
in "approve" or "decline". On the right, three trees trained on different data give their own answers, and the forest
takes the majority vote. Two say approve, so the forest says approve.

### A decision tree

<ol class="steps" markdown>
<li markdown>**Pick the best question** to split the data, such as "Is pixel 27 brighter than 5?".</li>
<li markdown>**Split** the data into the "yes" group and the "no" group.</li>
<li markdown>**Repeat** inside each group until the groups are pure enough.</li>
<li markdown>**Predict** by following the questions down to a leaf and reading its label.</li>
</ol>

"Best" means the question that leaves each group most pure, mostly one digit and few others. A deep tree can keep
splitting until a leaf holds a single training digit. That is how a tree memorises an unusual row, by giving it a
leaf of its own.

**For Carol this means** a tree that saw her thick-marker digits can grow leaves just for them. A tree that never saw
them has no such leaves.

### A random forest

Each tree is trained on its own random **bag** of rows, and the forest takes a vote. The classic way to make a bag is
a **bootstrap**, which draws \(n\) rows *with replacement* from the \(n\) training rows.

The forest adds a second kind of randomness. At each split, a tree may only choose from a random handful of the
pixels. With the course library's setting, that is the square root of the 64 pixels, so 8 at a time. Because each tree
sees different rows and different pixels, the trees make different mistakes, and the vote cancels many of them out.

**For Carol this means** in a classic forest of 50 trees, the original model got 100.0% of her digits right, 70.0% of
unseen thick-marker digits and 97.2% of the test set.

### Forgetting in a forest

If Carol's digit was never in tree #7's bag, tree #7 never saw her and can stay as it is. Only trees whose bag contained
her rows need rebuilding. The result is exact, as long as each rebuilt tree uses the same random seed and the same bag
minus the deleted rows.

In steps, forgetting works like this.

1. **Keep a record.** At training time, store each tree's bag and its seed.
2. **Find the trees.** List every tree whose bag holds any of the deleted rows.
3. **Rebuild only those.** Remove the rows from each of those bags and retrain the tree with its old seed.
4. **Leave the rest.** Every other tree is already the tree you would get without the rows.

The catch is that bootstrap bags overlap heavily. A typical row lands in about **63%** of the trees, and in Lesson 03
Carol's 40 rows reached **all 50** trees. So Lesson 03 redesigns the forest.

??? deep "Go deeper · where 63% comes from, and why Carol reaches every tree"
    A bag draws \(n\) rows, one at a time, with replacement. On each draw, a given row is missed with chance
    \(1 - 1/n\). It is missed on all \(n\) draws with chance

    \[
    \left(1 - \tfrac{1}{n}\right)^n \approx \tfrac{1}{e} \approx 0.37
    \]

    So it lands in the bag with chance about \(1 - 0.37 = 0.63\). With \(n = 1{,}257\) the estimate is already very
    close. Lesson 03 measured it directly. A typical row appeared in 31.6 of the 50 trees, which is 63%.

    For Carol, a tree escapes only if it misses all 40 of her rows. That chance is about \(0.37^{40}\), roughly
    \(e^{-40}\), which is so small it never happens. So all 50 trees met her. The more rows a person has, the closer
    a bootstrap forest gets to "rebuild everything".

??? checkpoint "Checkpoint 1 · A typical user with one row asks to be forgotten from a 50-tree bootstrap forest. Roughly how many trees will you rebuild?"
    **About 31 or 32.** One row lands in about 63% of bootstrap bags, and 63% of 50 is about 31.5. Lesson 03 rebuilt
    31 trees for one random row. That is most of the forest, for a single row.

### Three ways to share out the rows

Lesson 03 keeps 50 trees and the same algorithm, and only changes how the bags are drawn.

=== "Bootstrap bags"

    Each of the 50 trees draws its bag from all 1,257 digits. Bags overlap heavily, so one row reaches about 31 trees
    and Carol reaches all 50. Accuracy is the best of the three, because every tree learns from the whole dataset.

=== "Random shards"

    The digits are split at random into 5 shards. Each shard gets 10 trees, and each tree draws its bag only from its
    own shard. A row now lives in one shard, so one random row reached 8 trees. But Carol's 40 digits were scattered
    over all five shards, so forgetting her still touched 49 of the 50 trees.

=== "User-aware shards"

    The same 5 shards of 10 trees, but all of one person's rows go into the same shard. Carol's 40 digits all sit in
    shard 0. Forgetting her touches that shard's 10 trees and nothing else.

| Design (50 trees) | Test accuracy | Trees to retrain for Carol |
|---|---|---|
| Bootstrap bags | 97.2% | 50 of 50 |
| Random shards (5 groups) | 94.4% | 49 of 50 |
| **User-aware shards** (each user in one group) | 94.4% | **10 of 50** |

Putting all of one person's data in the same shard means forgetting them touches just one shard. The price is a little
accuracy every day, because each tree sees less data.

??? checkpoint "Checkpoint 2 · Random shards cut one random row from 31 trees to 8. Why did they barely help Carol, at 49 of 50?"
    **Her rows were spread over every shard.** Random sharding puts each *row* in one shard, but a person with 40 rows
    ends up in all five. Each shard then has some of her digits, and nearly every tree in it drew at least one of them.
    To make forgetting a *person* cheap, you must shard by person.

## A worked example

Follow Carol through the user-aware forest in Lesson 03.

1. **Train.** Five shards of 10 trees. Shard 0 holds Carol's 40 digits plus a fifth of everyone else. Before any
   forgetting, this forest gets 95.0% of her digits right and 94.4% of the test digits.
2. **Find the trees.** Only the 10 trees of shard 0 have her rows in their bags. The other 40 trees never saw her.
3. **Rebuild.** Each of the 10 trees is retrained on its old bag minus her rows, with its old seed. Carol's accuracy
   falls to 42.5%.
4. **Prove it.** Lesson 03 trains a fresh forest from scratch on exactly the same bags without Carol. The largest
   difference in any predicted probability, over 1,877 inputs, is 0.0. The forest is exactly one that never saw her.
5. **Count the cost.** 10 trees instead of 50, so a fifth of the work. The price was paid earlier, at training time,
   as test accuracy of 94.4% instead of 97.2%, a drop of 2.8 points.

## What the lesson found

<div class="stats">
<div><strong>63%</strong><span>of bootstrap trees hold any one typical row</span></div>
<div class="is-bad"><strong>50 of 50</strong><span>bootstrap trees reached by Carol's 40 rows</span></div>
<div class="is-good"><strong>10 of 50</strong><span>trees rebuilt for Carol with user-aware shards</span></div>
<div class="is-good"><strong>0.0</strong><span>difference from a forest that never saw her</span></div>
</div>

??? deep "Go deeper · the full Lesson 03 forest table"

    | Design | Test accuracy | Carol before | Carol after | Trees for 1 random row | Trees for Carol |
    |---|---|---|---|---|---|
    | Bootstrap bags | 97.2% | 100.0% | 40.0% | 31 of 50 | 50 of 50 |
    | Random shards | 94.4% | 90.0% | 42.5% | 8 of 50 | 49 of 50 |
    | User-aware shards | 94.4% | 95.0% | 42.5% | 9 of 50 | 10 of 50 |

    **One random row.** In both sharded designs the row lives in one shard of 10 trees, and a bootstrap bag inside that
    shard still picks it most of the time. So it reached 8 or 9 trees, never more than 10.

    **Which forest is the right answer?** A separate forest trained on the retain set with fresh bootstrap bags scored
    30.0% on Carol, while the unlearnt bootstrap forest scored 40.0%. Both never saw her. They differ because their
    trees were built from different bags, just as two retrains with different seeds differ in
    [The gold band](../unlearning/gold-band.md). The exact check compares like with like, the same bags minus her rows.

    **Her style goes with her.** On 80 unseen thick-marker digits, the original forest scored 70.0% and the fresh forest
    without her 48.8%. She was its main teacher for that style.

## Limits

**You pay in accuracy every day.** Each sharded tree learns from a fifth of the data, so test accuracy fell from 97.2%
to 94.4%. That cost applies to every prediction, whether or not anyone ever asks to be forgotten.

**You must know the person at training time.** User-aware shards need every row tagged with its owner before the
forest is built. A row with no clear owner, or one that belongs to two people, cannot be placed in a single shard.

**Exactness needs bookkeeping.** The proof works only because each tree's bag and seed were kept. Lose them and the
only exact option is to rebuild the whole forest.

**Whole trees are still a blunt tool.** Lesson 03 rebuilds a full tree whenever its bag held the row.

??? deep "Go deeper · forests built for deletion"
    Lesson 03's notebook points to two designs that go further. DaRE forests (Brophy and Lowd 2021) retrain only the
    affected *subtrees*, using split statistics they cache at training time. HedgeCut (Schelter et al. 2021) keeps
    other subtrees ready so that a deletion can be served with low delay. Both papers are in the course's
    `resources/papers/02-exact-unlearning/` folder.

!!! tip "What to do in practice"
    - Store every tree's bag and seed, so you can rebuild a tree exactly.
    - Shard by the unit people will ask to delete, such as a user, a customer or a document source.
    - Count how many trees a typical request touches before you go live, not after the first request.
    - Measure the accuracy you give up and decide whether it is worth the cheaper forgetting.
    - Prove each deletion once in testing by comparing with a forest trained from scratch on the same bags.

??? checkpoint "Checkpoint 3 · A hospital splits its forest into shards by row number. A patient with 200 visits asks to be forgotten. What happens, and what should it have done?"
    **Nearly every tree must be rebuilt.** Splitting by row scatters the patient's 200 visits over every shard, just as
    random shards scattered Carol, who cost 49 of 50 trees. The hospital should shard by patient, so the 200 visits sit
    in one shard and only that shard's trees are rebuilt.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
forest = classical.BaggedForest(50, seed=0).fit(L.X_train, L.y_train)
forest.unlearn(L.forget_idx)     # rebuild only the trees whose bags held Carol's rows
```

`unlearn` returns a dictionary whose `trees_retrained` entry is the number of trees it rebuilt. On the classic forest above, that is all 50 for Carol.

??? deep "Go deeper · build the user-aware forest"
    ```python
    import numpy as np
    from mul import classical, lab
    L = lab.make_lab("carol")

    def shard_bags(shards, trees_per_shard=10, seed=0):
        rng = np.random.default_rng(seed)
        return [rng.choice(sh, len(sh), replace=True) for sh in shards for _ in range(trees_per_shard)]

    perm = np.random.default_rng(0).permutation(len(L.X_train))
    others = perm[~np.isin(perm, L.forget_idx)]
    user_shards = np.array_split(others, 5)
    user_shards[0] = np.r_[user_shards[0], L.forget_idx]          # Carol lives in shard 0 only

    forest = classical.BaggedForest(50, seed=0).fit(L.X_train, L.y_train, bags=shard_bags(user_shards))
    print(forest.unlearn(L.forget_idx)["trees_retrained"])       # 10 of 50
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming a forest is local by default.** With bootstrap bags, one row already reaches about 63% of the trees.
    - **Sharding by row instead of by person.** If one person's rows are spread over every shard, forgetting them still
      touches everything. Shard by the unit people will ask to delete.
    - **Rebuilding a tree with a new seed.** The tree is then a fresh roll of the dice, not the exact tree you would
      have had without the row.
    - **Throwing away the bags.** Without the record of which rows each tree saw, you cannot tell which trees to keep.
    - **Ignoring the accuracy cost.** Sharding cost 2.8 points of test accuracy in Lesson 03, on every prediction.

## Key takeaways

!!! notes "Notes to take"
    - **Tree.** A chain of yes/no questions. A deep tree can give an unusual row a leaf of its own.
    - **Forest.** Many trees, each on its own bag of rows, that vote.
    - **Exact forgetting.** Rebuild only the trees whose bags held the row, with the same seed and the same bag minus the row.
    - **Bootstrap trap.** One row reaches about 63% of trees. Lesson 03 rebuilt 31 of 50 for one row.
    - **Carol.** Her 40 rows reached all 50 bootstrap trees, and 49 of 50 with random shards.
    - **User-aware shards.** All her rows in one shard, so 10 of 50 trees, with a difference of 0.0 from scratch.
    - **Price.** Test accuracy 94.4% against 97.2%, paid every day.
    - **Rule.** Shard by the unit people will ask to delete.

## Quiz

```quiz
- q: What is a random forest?
  options:
    - A single very deep tree
    - A committee of decision trees that vote
    - A neural network with tree-shaped layers
  answer: 1
  why: Each tree trains on its own bag of rows, and the forest combines their votes.
- q: Which trees must be rebuilt when Carol is forgotten?
  options:
    - All of them, always
    - Only the trees whose bags contained her rows
    - None of them
  answer: 1
  why: A tree that never saw her rows is already identical to one trained without her.
- q: With classic bootstrap bags, roughly what share of trees does one typical row appear in?
  options:
    - About 5%
    - About 63%
    - 100%
  answer: 1
  why: Drawing n rows with replacement puts any given row in about 63% of the bags.
- q: Why do user-aware shards make forgetting Carol cheaper?
  options:
    - All her data sits in one shard, so only that shard's trees need rebuilding.
    - They delete her data before training.
    - They use fewer trees overall.
  answer: 0
  why: In Lesson 03, user-aware shards cut the trees to retrain for Carol from 50 to 10.
- q: Why is the unlearnt user-aware forest exactly the same as one that never saw Carol?
  options:
    - It averages the old forest with a new one.
    - It deletes trees at random until her accuracy falls.
    - The untouched trees never saw her, and each rebuilt tree uses its old seed and its old bag minus her rows.
  answer: 2
  why: Every tree is then the tree you would get without her. Lesson 03 measured a difference of 0.0.
- q: The sharded forests scored 94.4% on the test set, against 97.2% for bootstrap bags. Why?
  options:
    - Each tree learns from only a fifth of the data.
    - The sharded forests have fewer trees.
    - Carol's data was removed before training.
  answer: 0
  why: All three designs have 50 trees, but a sharded tree only draws from its own shard. That is the price of cheap forgetting.
- q: With random shards, one random row reached 8 trees but Carol reached 49 of 50. Why?
  options:
    - Random shards do not record which rows each tree saw.
    - Random shards use more trees for unusual data.
    - Her 40 rows were scattered over all five shards.
  answer: 2
  why: Sharding by row puts each row in one shard, but a person with many rows ends up in all of them.
- q: The unlearnt bootstrap forest scored 40.0% on Carol, while a fresh forest trained without her scored 30.0%. Did unlearning fail?
  options:
    - Yes, because the two numbers should match exactly.
    - No. Both never saw her, but they were built from different bags, so they differ like two retrains.
    - No, because 40.0% is close enough to 100.0%.
  answer: 1
  why: The exact check compares with a forest trained on the same bags minus her rows, and that difference was 0.0.
```

## Try it

!!! levelup "Level up"
    You can now count the trees a request will touch and design a forest that forgets one person cheaply. Next quest,
    [Neural networks](neural-networks.md), where every example touches every weight and there are no trees to set aside.

- The concept page [SISA, sharded training](../unlearning/sisa.md) applies the same idea to neural networks.
- Run the lesson [03 · SVM and random forest](../lessons/03-svm-and-random-forest.md).
- In the Lesson 03 notebook, change the number of shards from 5 to 2 and to 10, and plot test accuracy against the
  trees rebuilt for Carol.
