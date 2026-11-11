---
title: k-nearest neighbours
description: k-NN answers by letting the k most similar training examples vote, so the model is the data and deleting a row is exact unlearning.
---

# K-nearest neighbours (k-NN)

!!! oneline "In one line"
    To classify something new, k-NN finds the *k* most similar training examples and lets them **vote**.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why a k-NN model *is* its training data, and what that means for privacy,
    - work out how a vote changes when one person's rows are deleted,
    - prove that deleting rows is exact unlearning, and spot the copies that a deletion does not reach.

## Why it matters

K-NN is the easiest model to unlearn, because the model **is** the training data. There is no training step that mixes
examples together. It is also the model behind "find similar items" features and the vector stores used in retrieval
(RAG) systems, so it shows up in real products.

That ease has a dark side. Because k-NN keeps every example in full, it does not just *learn from* a person, it
*contains* them. When it answers a question, it looks up real people's rows. A "show me similar examples" feature can
put one person's raw data in front of everyone else.

So k-NN is where the course begins its [Ladder of Forgetting](../unlearning/ladder-of-forgetting.md). It is rung 1,
where forgetting is exact and almost free. Every model higher up the ladder loses a little of this property, and seeing
clearly why k-NN is easy makes it easier to see why the others are hard.

## A simple example

You move to a new city and want a good place for dinner. You ask the five neighbours who live closest to you, and pick
the restaurant most of them recommend. That is k-NN with \(k = 5\).

!!! simply "Explain it simply"
    Now suppose one of your neighbours, Carol, moves away. Next time you ask, you simply ask the five people who live
    closest to you *now*. Her opinion is gone from every answer, and nobody had to "unlearn" anything. Your answer is
    exactly the one you would have got if she had never lived there.

Map the picture onto the course. The neighbours are the **training digits**. "Living close" means **looking alike**,
pixel by pixel. Your question is a **new digit** to classify, and the recommendation is the **predicted label**. Carol
moving away is her **erasure request**, and asking the people who are left is what k-NN does after her rows are
deleted.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| \(k\) | How many nearby examples get a vote | The course uses \(k = 5\) |
| Distance | A number for how different two examples are. Small means similar | For digits, how much the 64 pixel brightnesses differ |
| Neighbour | One of the \(k\) stored examples closest to the new input | 85.8% of the neighbours for new thick-marker digits were Carol's |
| Vote | Each neighbour backs its own label, and the label with most backers wins | Three 4s and two 9s give the answer 4 |
| Lazy learner | A model that does no work at training time and all its work at prediction time | k-NN "trains" by storing 1,257 digits |
| [Tombstone](../start-here/glossary.md#t) | A mark that says a row is deleted, so searches skip it | Carol's 40 rows are marked as deleted in Lesson 01 |
| [Exact unlearning](../start-here/glossary.md#e) | A method whose result is guaranteed to match retraining without the data | The k-NN after deletion matched one that never saw Carol on 100% of inputs |
| [Vector store](../start-here/glossary.md#v) | A database that keeps embeddings and finds the ones nearest to a question | The k-NN case inside a RAG chatbot, in Lesson 21 |

## How it works

<!-- diagram: k-nearest-neighbours -->

The figure shows two classes of training points and one new point. The dashed circle holds its three nearest
neighbours. Two are yellow and one is blue, so the vote says yellow. Nothing was learnt in advance. The answer comes
only from which stored points sit closest.

<ol class="steps" markdown>
<li markdown>**"Training"** just stores all the examples and their labels.</li>
<li markdown>**For a new input**, measure its distance to every stored example (for images, how different the pixels are).</li>
<li markdown>**Pick the k closest** ones, the "nearest neighbours".</li>
<li markdown>**Vote.** Predict the label that most of them have.</li>
</ol>

Here is each step for the course's digits.

### Step 1. Store the examples

The lab has 1,257 training digits. Each one is an 8 × 8 image, which is a list of 64 pixel brightnesses, plus its
label from 0 to 9. K-NN keeps all of them exactly as they are. It does not average them, compress them or turn them
into weights.

**For Carol this means** her 40 thick-marker digits sit in the store as 40 raw rows. They are about 3% of the data, and
anyone who can read the store can read her handwriting.

### Step 2. Measure the distance

A new digit arrives. K-NN compares it with every stored digit, pixel by pixel. The course library squares the
difference at each of the 64 pixels and adds them up. Two digits that look alike get a small total. Two that look
different get a large one.

**For Carol this means** a new digit written with a thick marker is closest to other thick-stroked digits. In the
training data, the only ones are hers.

### Step 3. Pick the k closest

Sort the 1,257 distances and keep the \(k\) smallest. Those \(k\) rows are the neighbours. The course uses \(k = 5\).

**For Carol this means** that for new thick-marker digits, most of the five neighbours are hers.

### Step 4. Vote

Each neighbour backs its own label. The label with the most backers is the answer. The share of votes for each label
can also be read as a rough probability, so four votes out of five for "7" means 80% sure.

**For Carol this means** her rows decide the answer for anyone who writes like her. Her data is shaping, and could
expose, predictions made for other people.

??? deep "Go deeper · the distance and the vote in symbols, and what happens with ties"
    For a new digit \(x\) and a stored digit \(x_i\), the course library uses the squared distance
    \(d(x, x_i) = \sum_{j=1}^{64} (x_j - x_{ij})^2\). Squaring does not change which rows are closest, so there is no
    need to take the square root.

    Let \(N_k(x)\) be the \(k\) rows with the smallest distance. The share of votes for class \(c\) is
    \(P(c \mid x) = \frac{1}{k} \sum_{i \in N_k(x)} [y_i = c]\), where \([y_i = c]\) is 1 when row \(i\) has label
    \(c\) and 0 otherwise. The prediction is the class with the largest share.

    With ten classes, a tie is possible even when \(k\) is odd, for example two 4s, two 9s and one 7. The course library
    then picks the smaller digit, because it takes the first largest share.

### Choosing k

The choice of \(k\) matters. A small \(k\) follows individual examples closely; a large \(k\) smooths things out.

At \(k = 1\), the answer is simply the label of the single nearest example. One unusual person can then decide every
answer in their corner of the data. As \(k\) grows, each answer is shared among more examples, so a few rows from one
person are more easily outvoted. Go too far and the vote is decided by whichever class is most common nearby, and
fine detail is lost.

**For Carol this means** the size of \(k\) controls how much her handful of rows can steer the answers for her
writing style. The notebook asks you to try \(k = 25\) and see what happens to her share of the neighbours.

??? checkpoint "Checkpoint 1 · With k = 5, a new digit's neighbours are three of Carol's digits labelled 4 and two other digits labelled 9. What does k-NN predict, and what happens once her rows are deleted?"
    **It predicts 4**, by three votes to two. After her rows are deleted, k-NN takes the five nearest of the rows that
    are left. Her three slots go to the next-closest digits from other people, and the vote is held again.
    The answer may or may not change, but it no longer depends on her in any way.

### Forgetting in k-NN

Because the model is the data, forgetting a row means **deleting it from the stored set**. The result is exactly the
same as a k-NN built without that row.

The course library does this with a **tombstone**. It keeps one "alive" mark per row and switches off the marks for
Carol's 40 rows. Every later search looks only at rows that are still alive. That one line is the whole unlearning
algorithm.

Why is this exact? After the marks are switched off, the rows that k-NN can see are the 1,217 rows of the retain set,
nothing more and nothing less. A k-NN built on the retain set from the start sees exactly the same rows. Two models that
search the same rows with the same distance and the same \(k\) must find the same neighbours and give the same vote,
for any input. There is no randomness in k-NN's "training" to make them differ.

Compare this with a neural network. There, Carol's influence is spread over thousands of weights, and no single number
can be switched off. In k-NN, her influence lives in her rows and nowhere else. Unlearning is exact because the
influence was never mixed in.

<div class="widget" data-widget="knn" markdown></div>

In the widget, the star starts next to a small group of Carol's squares. Read who the neighbours are and what the
model predicts. Then press **Forget Carol** and watch her points drop out of the vote. The links jump to the
next-closest points, and the readout says this is exactly the model you would get by training without her. Try moving
the slider for \(k\) too. With \(k = 1\) a single point decides the answer. With a larger \(k\), more points from outside
her group join the vote.

??? checkpoint "Checkpoint 2 · After unlearning, k-NN reads only 52.5% of Carol's digits, but 62.5% of unseen digits in her style. Is that over-forgetting?"
    **No.** The k-NN after deletion gave the same prediction as a k-NN that never saw Carol on all 1,877 inputs, and
    her 40 digits are among them. So a model that never saw her also scores exactly 52.5% on them. For a model with no
    randomness, the [gold band](../unlearning/gold-band.md) shrinks to that single point, and landing on it is a pass.
    Over-forgetting means scoring *below* what a never-saw-her model scores, and this model scores the same.

## A worked example

Follow Carol through Lesson 01. Every number comes from the notebook.

1. **She is stored.** The k-NN holds all 1,257 training digits, including her 40. That is about 3% of the store.
2. **She is consulted.** The lesson asks k-NN about 80 new thick-marker digits that it has never seen. With five
   neighbours each, that is 400 neighbour slots. **85.8%** of them were Carol's digits, which is about 343 of the 400.
   She is 3% of the data but almost nine in ten of the votes for her style.
3. **She is remembered.** Before deletion, k-NN reads **75.0%** of her own digits (30 of 40) but only **67.5%** of the
   unseen look-alikes (54 of 80). That gap of 7.5 points is her trace in the model. In Lesson 04 a neural network's
   gap was 22.5 points, so k-NN remembers her less, but it still remembers her.
4. **She asks to be erased.** Her 40 rows get tombstones. The whole operation took **0.15 milliseconds**, including
   copying the model.
5. **She is gone from every vote.** Her share of the neighbours is now **0.0%**. Her own digits drop to 52.5% (21 of
   40). Before, each of her digits had itself and her other digits among its neighbours, and now they do not. The
   unseen look-alikes drop to 62.5% (50 of 80). Test accuracy stays at 98.3%.
6. **The proof.** A k-NN built from the start on the 1,217 rows without her gives the same prediction on **100%** of
   1,877 inputs, which are the 1,257 training digits, the 540 test digits and the 80 look-alikes.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>85.8%</strong><span>of neighbours for thick-marker digits were Carol's, before</span></div>
<div class="is-good"><strong>0.0%</strong><span>of neighbours were hers after her rows were deleted</span></div>
<div><strong>0.15 ms</strong><span>to unlearn her 40 rows, including the copy</span></div>
<div class="is-good"><strong>100%</strong><span>same predictions as a k-NN that never saw her, on 1,877 inputs</span></div>
</div>

| | Before | After deleting her rows |
|---|---|---|
| Carol's share of the neighbours | 85.8% | 0.0% |
| Accuracy on Carol's own digits | 75.0% | 52.5% |
| Accuracy on unseen thick-marker digits | 67.5% | 62.5% |
| Accuracy on test digits | 98.3% | 98.3% |

**Carol's share of the neighbours** is the row that matters most. It shows her raw data was being used for almost
every prediction about her style, and after the deletion it never is.

**Accuracy on test digits** did not move. Typical digits have plenty of typical neighbours, so losing 40 unusual rows
changes nothing for most people.

**Accuracy on unseen thick-marker digits** fell by 5 points. Carol was the only source of that style, so everyone who
writes like her now gets slightly worse answers. That is the cost of forgetting an unusual person, and Lesson 12
measures it as a fairness question.

## Limits

**A tombstone hides rows, it does not erase them.** In the course library the marked rows still sit in memory. The
answers are exact, but the bytes are not gone until the store is cleaned up or rebuilt. Cleaning up is called compaction.
A legal erasure needs that second step too.

**Exact only for the plain index.** Real systems rarely compare a question with every row. They use an approximate
index, which first sorts the rows into groups around averaged centres. Those averages are a small trained model, and a
tombstone does not update them. In Lesson 21, a trace of one person's data in such an index stayed at exactly 0.1643
after her rows were removed from the index's lists, and only a rebuild brought it to zero. See
[why an approximate index keeps a trace](../unlearning/rag-and-vector-stores.md#why-an-approximate-index-keeps-a-trace).

!!! warning "The catch in real systems"
    The k-NN index is exact, but real systems copy data elsewhere too, such as approximate search indexes, caches, backups and any **embedding model fine-tuned** on the same data. Deleting a document from a vector store is the easy k-NN case;
    removing it from a fine-tuned model is the hard deep-learning case.

??? deep "Go deeper · two more limits"
    **Prediction is slow.** Training is free, but every question is compared with every stored row. For the lab that
    is 1,257 distances per digit, which is nothing. For a store of millions of rows it is too slow, which is why
    approximate indexes exist, and those bring the trace problem above.

    **It keeps everyone else's data too.** Unlearning Carol is exact, but every other person's raw rows are still in
    the store and can still be shown as "similar examples". K-NN is easy to unlearn and poor at privacy for the people
    who stay.

!!! tip "What to do in practice"
    - Delete by tombstone for speed, then compact or rebuild on a schedule, and record when the rows were truly
      removed.
    - Rebuild any approximate index after a deletion, because its averaged centres still hold the deleted data.
    - List every copy of the data, including caches, replicas, backups and any model fine-tuned on it, and handle each.
    - Check the result against a k-NN built without the person. The predictions should match on every input.
    - Watch the accuracy for people who look like the deleted person, since they lose their closest neighbours.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
knn = classical.KNN(k=5).fit(L.X_train, L.y_train)
knn.unlearn(L.forget_idx)        # mark Carol's rows as deleted
print(knn.predict(L.X_test[:5]))
```

??? deep "Go deeper · check the deletion against a model that never saw her"
    ```python
    import numpy as np
    never = classical.KNN(k=5).fit(L.Xr, L.yr)                 # built without Carol from the start
    X_all = np.r_[L.X_train, L.X_test, L.X_like_forget]        # 1,877 inputs
    print((knn.predict(X_all) == never.predict(X_all)).mean())   # 1.0, identical on every input
    print(np.isin(knn.neighbours(L.X_like_forget), L.forget_idx).mean())   # 0.0, she is never consulted
    ```

    The `unlearn` method only switches off the "alive" marks for the given rows. The `neighbours` method returns the
    original row numbers of the nearest alive rows, which is how the lesson counts Carol's share.

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking k-NN does not "remember" anyone.** It keeps every example, so it can show a person's raw data to others
      through "similar examples" features.
    - **Forgetting the copies.** Deleting from the main index is not enough if the data also lives in a cache or a
      fine-tuned encoder.
    - **Stopping at the tombstone.** A marked row is hidden from search but still stored until compaction or a rebuild.
    - **Trusting an approximate index after a deletion.** Its averaged centres were built with the deleted rows and
      still carry them.
    - **Reading lower accuracy on the person as a failure.** After deletion, Carol's digits scored 52.5%, exactly what
      a k-NN that never saw her scores.

??? checkpoint "Checkpoint 3 · A shop's product search uses an approximate index with averaged group centres. A customer's rows are tombstoned. Is the index now the same as one built without them?"
    **No.** The tombstone stops their rows being returned, but the group centres are averages that were worked out
    with their rows included, and nobody worked them out again. In Lesson 21 such a trace stayed exactly the same until
    the index was rebuilt. Only a rebuild on the remaining rows gives the index that never saw them.

## Key takeaways

!!! notes "Notes to take"
    - **k-NN.** Stores every example and lets the \(k\) nearest vote. "Training" is storing.
    - **Distance.** The course adds up squared pixel differences over 64 pixels. Small means alike.
    - **Choosing k.** Small \(k\) follows single examples, large \(k\) smooths. The course uses \(k = 5\).
    - **Privacy.** The model is the data, so it contains people. Carol was 3% of the data but 85.8% of the neighbours for her style.
    - **Unlearning.** Delete the rows. The model sees exactly the retain set, so it is exact. It took 0.15 ms.
    - **Proof.** Same predictions as a k-NN that never saw Carol on 100% of 1,877 inputs.
    - **Side effect.** Look-alike digits fell from 67.5% to 62.5%, because she was the only source of the style.
    - **Trap.** A tombstone hides rows but does not erase them, and approximate indexes need a rebuild.
    - **Trap.** Caches, backups and fine-tuned encoders hold copies that the index deletion does not reach.

## Quiz

```quiz
- q: What does k-NN do during "training"?
  options:
    - Stores the examples and labels
    - Runs gradient descent for many epochs
    - Builds a set of decision trees
  answer: 0
  why: k-NN does no real training; all the work happens when it compares a new input with the stored examples.
- q: How do you make a k-NN model forget one person's rows?
  options:
    - Delete their rows from the stored set
    - Retrain for 60 epochs
    - Add random noise to every prediction
  answer: 0
  why: The model is the data, so removing the rows gives exactly the model you would have built without them.
- q: Before unlearning, what share of the neighbours for new thick-marker digits were Carol's?
  options:
    - About 10%
    - About 50%
    - 85.8%
  answer: 2
  why: Carol was the only person with that style, so her digits were consulted for almost every similar query.
- q: A company deletes a document from its vector store, but a model was also fine-tuned on it. Is the document forgotten?
  options:
    - Yes, the vector store was the only copy that mattered.
    - Not fully; the fine-tuned model still carries its influence.
  answer: 1
  why: The vector store is the easy k-NN case. The fine-tuned model is the hard deep-learning case.
- q: Why did k-NN's accuracy on Carol's own digits fall from 75.0% to 52.5% after her rows were deleted?
  options:
    - The deletion damaged other people's rows.
    - She and her near copies were no longer there to vote for the right labels.
    - The value of k was changed during unlearning.
  answer: 1
  why: Before, each of her digits had itself and her other digits as close neighbours. After, only other people's rows vote, exactly as in a model that never saw her.
- q: Which choice of k lets a single unusual example decide the answer near it?
  options:
    - k = 25
    - k = 9
    - k = 1
  answer: 2
  why: With k = 1 the answer is the label of the one nearest example. Larger k shares each answer among more examples.
- q: Why is deleting rows from k-NN exact unlearning?
  options:
    - After deletion, the model searches exactly the rows a k-NN built without them would search, so every vote is the same.
    - The deleted rows are copied to a backup first.
    - The model is retrained for one epoch after the deletion.
  answer: 0
  why: K-NN has no weights and no randomness. Its answers depend only on the rows it can see, and those are now the retain set.
- q: Carol's 40 rows have been tombstoned in the course library. What is still true?
  options:
    - Her rows are gone from memory, so nothing more is needed.
    - The model now predicts differently from one that never saw her.
    - Her rows are hidden from every search but still stored until compaction or a rebuild.
  answer: 2
  why: A tombstone is a mark, not an erasure. The answers are already exact, but the bytes must still be removed.
```

## Try it

!!! levelup "Level up"
    You can now explain why a model that is its own data forgets by deletion, and prove it against a model that never
    saw the person. Next quest, [Naive Bayes](naive-bayes.md), where the model keeps only sums, and forgetting becomes a
    subtraction.

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [01 · k-NN and Naive Bayes](../lessons/01-knn-and-naive-bayes.md).
- In the notebook, change \(k\) from 5 to 25 and see whether Carol's share of the neighbours goes up or down.
- See where k-NN meets real products in [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md).
