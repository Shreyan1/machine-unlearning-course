---
title: Exact unlearning for classical models
description: For many classical models, forgetting is a deletion, a subtraction, a downdate or rebuilding only the part a point touched.
---

# Exact unlearning for classical models

!!! oneline "In one line"
    Many classical models can forget **exactly and cheaply**, because they are a sum you can subtract from, a formula you
    can update, or made of parts that only some points touched.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - name the three properties that make exact forgetting possible, and the model behind each,
    - choose the right method for a classical model and say how you would prove it worked,
    - spot the parts of a pipeline that still remember after the model has forgotten.

## Why it matters

Before reaching for complex methods, check whether the model (or part of the system) is classical. Indexes, counts,
scalers, Naive Bayes filters and many ranking models are. For them, exact forgetting is often a few milliseconds of
work, with a result you can prove is identical to retraining.

**Exact** has a precise meaning here. The unlearnt model must be the same as a model trained from the start without
the data, the [gold standard](retraining-gold-standard.md). For a classical model that is a check you can run. You
train the model without Carol once and compare the two. They agree down to rounding error.

That makes classical models the place where the course's habits are formed. Every lesson takes the same five steps,
train, show the issue, untrain, show the result and prove it. In Lessons 01 to 03, "prove it" almost always means
"identical". Only logistic regression hints at what neural networks bring, where it means "measure how close".

## A simple example

A shopkeeper keeps a running total of the day's sales. If a customer returns an item, the shopkeeper does not re-add
every sale of the day. They subtract that one sale. The total is now exactly what it would have been if the sale had
never happened.

!!! simply "Explain it simply"
    If a model is a running total, forgetting is taking one number back out. If it is a committee, forgetting is
    replacing only the members who met the person. Either way, the result is exactly what you would have had without
    them.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Exact unlearning](../start-here/glossary.md#e) | Forgetting that gives the same model as retraining without the data | k-NN after deleting Carol's rows |
| [Summation form](../start-here/glossary.md#s) | A model built from sums over the training data, so forgetting is a subtraction | Naive Bayes keeps counts and sums per class |
| [Tombstone](../start-here/glossary.md#t) | A mark that says a stored row is deleted and must not be used | k-NN's way of dropping Carol's rows |
| [Sherman-Morrison downdate](../start-here/glossary.md#s) | A formula that updates a matrix inverse when one row is removed, without starting again | Ridge regression forgets Carol in 40 downdates |
| [Leverage](../start-here/glossary.md#l) | How strongly one training point bends a linear model towards itself | Carol 0.116 against 0.039 for everyone else |
| [Newton step](../start-here/glossary.md#n) | One jump towards the new best weights, using the slope and the curvature of the loss | One step closes 94.8% of the gap for logistic regression |
| [Locality](../start-here/glossary.md#l) | Only some parts of a model depend on a point, so only those parts need rebuilding | 10 of 50 trees for Carol |

## How it works

<!-- diagram: exact-unlearning-classical -->

The figure has two halves. On the left, a Naive Bayes spam filter has counted the word "free" 120 times in spam, and 3
of those came from Carol's emails. Subtract them and the new count is 117, the same as counting again without her. On
the right, k-NN stores its training points, so forgetting Carol is crossing out her point. Both results are identical
to retraining.

Lessons 01 to 03 find three properties that make exact forgetting possible.

### 1. The model is the data, or a sum

| Model | What it stores | How to forget | Result in the course |
|---|---|---|---|
| [k-NN](../ml-basics/k-nearest-neighbours.md) | The rows themselves | Delete the rows | 100% identical predictions, ~0.15 ms |
| [Naive Bayes](../ml-basics/naive-bayes.md) | Counts and sums per class | Subtract the rows | Identical log-probabilities, ~0.1 ms |

In 2015, Cao and Yang named this the **summation form**. If a model is a sum over the training data, forgetting is a
subtraction. This is where machine unlearning began.

k-NN does not really learn. To classify a digit it finds the most similar stored digits and lets them vote. So the
model does not just remember Carol, it contains her handwriting.

Naive Bayes stores three things per class, the number of digits, the sum of each pixel and the sum of each pixel
squared. Every average and spread it needs is worked out from those. Take Carol's rows out of the sums and the model
is exactly one built without her.

**For Carol this means** that before unlearning, 85.8% of the neighbours k-NN consulted for thick-marker digits were
her own digits. Afterwards it was 0.0%. Naive Bayes fell from 60.0% on her digits to 27.5%, exactly the score of a
model that never saw her, with a largest difference in any log-probability of 0.0.

??? checkpoint "Checkpoint 1 · Deleting Carol from k-NN took 0.15 ms. A colleague says something that fast cannot be exact. How do you settle it?"
    **Compare it with a model built without her.** Build a k-NN from the 1,217 digits that are not Carol's and ask
    both models about the same inputs. In Lesson 01 they gave identical predictions on 100.0% of 1,877 inputs. Speed
    says nothing about exactness. The comparison does.

### 2. The model is a formula of sums

[Ridge regression](../ml-basics/linear-and-ridge-regression.md) computes \(w = (X^\top X + \lambda I)^{-1} X^\top y\). The
inverse mixes all the points together, but a **Sherman-Morrison downdate** still removes a point exactly. In Lesson 02 the
result matched a refit to within 4.38 × 10⁻¹³.

The two sums, \(X^\top X\) and \(X^\top y\), are still sums, so taking Carol out of them is easy. The hard part is the
inverse, which ties every point to every other. The downdate updates that inverse directly for each removed row. Its
cost depends only on how much you delete, while a refit's cost grows with everything you keep.

**For Carol this means** her digits had a mean leverage of 0.116, about three times the 0.039 of everyone else. She
bent the model towards herself. After 40 downdates the model scored 45.0% on her digits, the same as a model that
never saw her.

[Logistic regression](../ml-basics/logistic-regression.md) has no formula, so a **Newton step** *estimates* the new
answer. One step closed 94.8% of the gap; two closed 99.9%. This is where unlearning first becomes approximate.

The step uses the slope and the curvature of the loss to jump towards where the best weights moved when Carol left.
Here is the link between the two halves. The Sherman-Morrison downdate *is* a Newton step, one that lands exactly
because ridge's loss is a perfect bowl shape. In Lesson 02 the two differed by only 1.37 × 10⁻¹³. Logistic regression's
loss is only roughly a bowl, so the same step lands near the answer instead of on it.

??? deep "Go deeper · the numbers behind rung 2"
    **The downdate formula.** With \(A = X^\top X + \lambda I\), removing a row \(x\) gives

    \[
    A'^{-1} = A^{-1} + \frac{A^{-1} x \, x^\top A^{-1}}{1 - x^\top A^{-1} x}
    \]

    The term \(x^\top A^{-1} x\) on the bottom is the point's leverage \(h\). For ridge, \(h < 1\) always holds, so the
    bottom never reaches zero.

    **How the cost scales.** On the 1,217 rows of the lab, the 40 downdates took 0.53 ms and a refit 0.18 ms, so the
    refit was faster. Lesson 02 then grew the training set and deleted the same 40 points.

    | Training rows | Refit | 40 downdates | Downdate is faster by |
    |---|---|---|---|
    | 2,000 | 0.2 ms | 0.46 ms | 0.4× |
    | 20,000 | 1.5 ms | 0.46 ms | 3.3× |
    | 100,000 | 11.3 ms | 0.50 ms | 22.7× |
    | 300,000 | 30.0 ms | 0.49 ms | 61.6× |

    **How close the Newton steps get.** The gap is the distance from the weights to those of a model retrained without
    Carol.

    | Newton steps | Gap to retrain | Share of the gap closed |
    |---|---|---|
    | 0 | 3.148 | 0.0% |
    | 1 | 0.165 | 94.8% |
    | 2 | 0.0035 | 99.9% |
    | 3 | about 0 | 100.0% |

    One step took 6.0 ms against 40.7 ms for a full refit. After one step, logistic regression scored 60.0% on Carol,
    against 62.5% for the model that never saw her.

??? checkpoint "Checkpoint 2 · One Newton step closed 94.8% of the gap for logistic regression. Is that exact unlearning?"
    **No, it is approximate, but measured.** The model is close to the retrained one, not the same. It scored 60.0% on
    Carol where the retrained model scored 62.5%. Two steps closed 99.9% and three closed it all. The habit to keep is
    the measuring. When "identical" is out of reach, report how far you are from the gold standard.

### 3. Locality (only some parts depend on a point)

| Model | Where locality comes from | Forgetting a typical user | Forgetting Carol |
|---|---|---|---|
| [SVM](../ml-basics/support-vector-machines.md) | Only support vectors matter | Free, if not a support vector | Re-solve, 97.5% of her digits are support vectors |
| [Random forest](../ml-basics/decision-trees-and-random-forests.md), bootstrap bags | Each tree has its own bag | ~63% of trees | All 50 trees |
| Random forest, **user-aware shards** | Each user lives in one shard | One shard | **10 of 50 trees** |

Trees have no gradient, so neither a subtraction nor a Newton step applies. What saves them is that each part of the
model depends on only some of the data. An SVM's boundary depends only on the points at the edge of its margin. Each
tree in a forest depends only on the rows in its bag.

**For Carol this means** both models find her expensive. 39 of her 40 digits were SVM support vectors, so the SVM had
to be re-solved. Her rows reached all 50 trees of a bootstrap forest. Only a forest built with her in a single shard
made her cheap, at 10 trees, with a difference of 0.0 from a forest trained without her.

!!! tip "Locality can be designed in"
    Whether forgetting Carol costs 10 trees or 50 was decided at **training time**, by how the data was split. Split by the unit people will ask to delete, such as a user, a customer or a document source. [SISA](sisa.md) does the same for neural
    networks.

### Do not forget the pipeline

A scaler, a TF-IDF vocabulary, PCA and feature selection are all **fitted on the data**, so they all carry the forget
set's influence. In Lesson 01, a `StandardScaler`'s stored mean moved by 0.0171 when Carol was removed. An unlearning
request must cover the whole pipeline, not just the final model.

The good news is that most of these are sums too. A scaler stores means and spreads, a vocabulary stores word counts,
and the same subtraction works on them. The hard part is remembering they exist. A vocabulary can even hold a name or a
rare word that only one person used.

Copies matter as well. Lesson 01 points to approximate nearest-neighbour indexes, caches, replicas and backups, which a
tombstone may not reach. An embedding model fine-tuned on the same data is the hardest copy of all, because it is a
neural network.

??? checkpoint "Checkpoint 3 · A spam filter runs a StandardScaler, then a TF-IDF vocabulary, then Naive Bayes. Carol asks to be forgotten. What must change?"
    **Every fitted part, not just the model.** Subtract her rows from Naive Bayes's counts and sums. Subtract her from
    the scaler's sums, since its stored mean moves when she leaves, by 0.0171 in Lesson 01. Update the vocabulary's
    counts and drop any word that only she used. Then clear her rows from the database, the caches and the backups.

## What the lessons found

<div class="stats">
<div class="is-good"><strong>100.0%</strong><span>k-NN predictions identical to a model without Carol</span></div>
<div class="is-good"><strong>4.38 × 10⁻¹³</strong><span>ridge weights after 40 downdates against a refit</span></div>
<div><strong>94.8%</strong><span>of the gap closed by one Newton step, approximate</span></div>
<div class="is-good"><strong>10 of 50</strong><span>trees rebuilt for Carol with user-aware shards</span></div>
</div>

Here is Carol across all the classical models in Lessons 01 to 03.

| Model | Carol before | Carol after | How it was proved | Time or cost |
|---|---|---|---|---|
| k-NN | 75.0% | 52.5% | 100.0% identical predictions | 0.15 ms |
| Naive Bayes | 60.0% | 27.5% | Log-probabilities differ by 0.0 | 0.09 ms |
| Ridge regression | 95.0% | 45.0% | Weights within 4.38 × 10⁻¹³ | 0.53 ms |
| Logistic regression, 1 Newton step | 92.5% | 60.0% | 94.8% of the gap closed | 6.0 ms |
| SVM | 100.0% | 57.5% | Re-solved without her | Under a second |
| Forest, user-aware shards | 95.0% | 42.5% | Probabilities differ by 0.0 | 10 of 50 trees |

Read the "proved" column from top to bottom. It says "identical" all the way, except for logistic regression, where it
becomes a measured gap. That one row is a preview of the rest of the course. Read the "before" column too. The models
that fit her most closely, ridge, logistic regression, the SVM and the forest, are the ones she bent the most.

## Limits

**Exact means exact for the stored state.** Subtraction needs the counts and sums, and a forest needs its bags and
seeds. If the system did not keep them, the only exact option is to retrain.

**Approximate starts early.** Logistic regression already needs a Newton step, and one step is close, not identical.
Any model without a formula is in the same place.

**Forgetting her style has a cost.** When Naive Bayes forgot Carol, its accuracy on unseen thick-marker digits fell
from 61.3% to 37.5%. She was its main source of that style, so people who write like her are now served worse. Lesson
12 measures this kind of side effect with fairness metrics.

??? deep "Go deeper · when exact is only nearly exact"
    **Round-off adds up.** Subtracting is exact in maths but not quite on a computer. After thousands of add and
    subtract cycles, small errors can build up in the sums of squares. Lesson 01 suggests checking against a fresh fit
    from time to time.

    **Downdates can be fragile.** The Sherman-Morrison formula divides by \(1 - h\). When a point's leverage \(h\) is close
    to 1, that number is tiny and errors grow. Lesson 02 notes that production systems use a Cholesky downdate or
    rebuild the inverse from time to time.

    **Library details matter.** Lesson 01 points out that scikit-learn's `GaussianNB` sets its smoothing from the
    variance of the whole training set. Subtracting rows then leaves that smoothing as it was, so its version is not
    quite exact. The course library's Naive Bayes uses a fixed smoothing value to avoid this.

!!! tip "What to do in practice"
    - First ask which rung the model is on. Is it a sum, a formula of sums or made of parts?
    - Use the exact method when there is one, and keep the counts, sums, bags and seeds it needs.
    - Prove it once in testing by comparing with a model trained without the data.
    - Follow the data through the whole pipeline, including scalers, vocabularies, indexes and backups.
    - When only an approximate method fits, measure the gap to a retrained model and report it.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
classical.KNN(k=5).fit(L.X_train, L.y_train).unlearn(L.forget_idx)            # delete
classical.GaussianNB(1e-2).fit(L.X_train, L.y_train).unlearn(L.Xf, L.yf)      # subtract
classical.BaggedForest(50, seed=0).fit(L.X_train, L.y_train).unlearn(L.forget_idx)  # rebuild touched trees
```

Each line trains one model on all the digits and then forgets Carol with the method that fits it. The proof is the
same for each. Train the same model on `L.Xr` and `L.yr`, the data without Carol, and compare the predictions.

## Common mistakes

!!! danger "Mistakes people make"
    - **Using approximate methods on models that can forget exactly.** If a subtraction works, use it.
    - **Forgetting copies and preprocessing.** Indexes, caches, scalers and vocabularies hold the data too.
    - **Assuming locality is automatic.** Bootstrap bags spread each row across most trees.
    - **Calling a Newton step exact.** For logistic regression it is close, 94.8% of the gap after one step, but not
      the same as retraining.
    - **Skipping the proof.** A fast method that was never compared with a model trained without the data is only a
      claim.

## Key takeaways

!!! notes "Notes to take"
    - **Exact.** The unlearnt model equals a model trained without the data. For classical models you can check it.
    - **Rung 1, the model is the data or a sum.** k-NN deletes rows, Naive Bayes subtracts them. Both identical, about 0.1 ms.
    - **Rung 2, a formula of sums.** Ridge forgets exactly by Sherman-Morrison, within 4.38 × 10⁻¹³.
    - **First approximation.** Logistic regression uses a Newton step. One closes 94.8% of the gap, two 99.9%.
    - **Link.** The downdate is a Newton step that lands exactly because ridge's loss is a perfect bowl.
    - **Rung 3, locality.** SVMs ignore non-support vectors, forests rebuild only the trees that saw the row.
    - **Carol is expensive.** Leverage 0.116 against 0.039, 97.5% support vectors, all 50 bootstrap trees.
    - **Design it in.** User-aware shards cut Carol to 10 of 50 trees.
    - **Trap.** The pipeline remembers too. A scaler's mean moved by 0.0171 without her.

## Quiz

```quiz
- q: What is the "summation form" idea from Cao and Yang (2015)?
  options:
    - If a model is a sum over the data, forgetting is a subtraction.
    - All models should be summed together.
    - Models must be trained twice.
  answer: 0
  why: This observation is where machine unlearning began.
- q: Which method removes a point exactly from ridge regression?
  options:
    - A Sherman-Morrison downdate
    - Gradient ascent
    - Bad Teacher
  answer: 0
  why: The downdate updates the inverse directly, matching a refit up to rounding error.
- q: Why does forgetting Carol from an SVM need real work?
  options:
    - Almost all of her digits are support vectors.
    - SVMs cannot be retrained.
    - Her digits are in the test set.
  answer: 0
  why: 97.5% of her digits were support vectors, so removing them moves the boundary.
- q: How many of 50 trees did a user-aware sharded forest retrain to forget Carol?
  options:
    - 10
    - 31
    - 50
  answer: 0
  why: All her data was in one shard of 10 trees, so only that shard needed rebuilding.
- q: A pipeline has a StandardScaler before the model. What must happen to it when Carol is forgotten?
  options:
    - Nothing; scalers do not learn.
    - It must be unlearnt too, because its stored means came from the data.
  answer: 1
  why: The scaler's mean moved by 0.0171 when Carol was removed. Preprocessing is a model too.
- q: One Newton step closed 94.8% of the gap to retraining for logistic regression. What kind of unlearning is that?
  options:
    - Exact, because the gap is small
    - Approximate, and measured against a model retrained without Carol
    - Failed, because the gap is not zero
  answer: 1
  why: Close is not the same as identical. The honest report is the measured gap, which two steps cut to 0.1%.
- q: Why is the Sherman-Morrison downdate exact for ridge, while the same Newton step is only approximate for logistic regression?
  options:
    - Ridge has fewer weights than logistic regression.
    - Logistic regression has no slope to follow.
    - Ridge's loss is a perfect bowl shape, so one step lands exactly on the new best weights.
  answer: 2
  why: A Newton step assumes the loss is a bowl. For ridge that is exactly true, and for logistic regression only roughly.
- q: How do you prove that a classical unlearning method is exact?
  options:
    - Compare it with a model trained without the data from the start, and check they agree
    - Check that its accuracy on the forget set went down
    - Check that it ran in under a millisecond
  answer: 0
  why: Exact means identical to the gold standard. Lesson 01 found 100.0% identical predictions for k-NN.
```

## Try it

!!! levelup "Level up"
    You can now place a classical model on the right rung, pick its exact method and prove it worked. Next quest,
    [SISA](sisa.md), where the locality idea is built into the training of neural networks.

- Read the next concept, [SISA, sharded training](sisa.md).
- Run the lessons [01](../lessons/01-knn-and-naive-bayes.md), [02](../lessons/02-linear-and-logistic-regression.md) and
  [03](../lessons/03-svm-and-random-forest.md).
