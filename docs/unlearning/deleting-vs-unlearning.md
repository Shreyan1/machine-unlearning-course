---
title: Deleting is not forgetting
description: Why removing someone's rows from a database does not remove what a trained model learnt from them.
---

# Deleting is not forgetting

!!! oneline "In one line"
    Deleting data removes the *file*, but the trained model still carries what it *learnt* from that file.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why deleting rows from a database leaves a trained model unchanged,
    - measure a person's fingerprint in a model by comparing their data with data like theirs,
    - say why forgetting must be checked by behaviour and not by comparing weights.

## Why it matters

When a person asks a company to erase their data, the company usually deletes their rows from a database. If an AI
model was trained on those rows, the model does not change at all. It can still behave in ways that reveal the person
was there. Regulators have noticed. In several cases, they have ordered companies to delete the **models**, not just the
data (see [Why the law cares](why-the-law-cares.md)).

The risk is not spread evenly. Models remember unusual data the most, because typical data is taught by thousands of
similar examples while unusual data is taught by only a few. Feldman (2020) argues that fitting such rare cases
*requires* memorising them. So the people whose data stands out, like Carol with her thick marker, are both the most
memorised and the easiest to spot from the outside.

That makes deletion a trap for a careful team. The database check passes and the ticket is closed. Meanwhile the model keeps
answering questions with what it learnt from the person. Nothing in the logs says anything is wrong.

## A simple example

Think of a cookbook and a cake. You can tear a page out of the cookbook, but you cannot "un-bake" the cake you already
made from it.

- The **page** is the training data.
- The **cake** is the trained model.
- **Machine unlearning** is the attempt to un-bake the cake, that is, to remove one ingredient's effect after the fact.

In the course, the cake is a digit-reading model and the ingredient is **Carol**, who wrote 40 of its 1,257 training
digits with a thick marker.

<!-- diagram: deleting-vs-unlearning -->

The figure shows the same database twice. In both rows, Carol's record has been struck out. In the top row that is
all that happens, so the model's weights still hold her influence and the model still remembers her. In the bottom row
the model is also unlearnt, so the weights no longer carry any trace of her. Only the second row has done the job.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Weights](../start-here/glossary.md#w) | The learnt numbers inside a model, which decide every answer it gives | The digit network has 85,002 of them |
| Training | Nudging the weights again and again until the model's answers are right | 60 passes over the 1,257 digits |
| Database | Where the raw records are stored. The model does not read it after training | The table that held Carol's 40 rows |
| [Memorisation](../start-here/glossary.md#m) | Getting an example right *because* it was in training | The network gets all 40 of Carol's digits right |
| Look-alike data | Data in the same style that the model never trained on | 80 unseen digits made thick, like Carol's |
| [Fingerprint](../start-here/glossary.md#f) | The gap between a model's score on someone's own data and on look-alike data | 100.0% against 77.5%, a gap of 22.5 points |
| Retraining | Training a fresh model on the data that is left | The network trained on 1,217 digits, without Carol |
| Behaviour | What a model outputs, as opposed to the numbers inside it | Its accuracy on Carol's digits |

## How it works

<ol class="steps" markdown>
<li markdown>**Training changes the weights.** A model is a long list of numbers called *weights*. During training, every
example nudges those numbers a little. Carol's digits nudged them too.</li>
<li markdown>**The database and the model are separate.** After training, the model no longer reads the database. It only
uses its weights.</li>
<li markdown>**Deleting the rows does not touch the weights.** So the model still gets Carol's digits right far more often
than digits like hers that it has never seen.</li>
<li markdown>**Her influence is spread everywhere.** In the course's neural network, removing Carol and retraining from the
same starting point changes **94.1%** of the 85,002 weights. There is no single "Carol weight" to delete.</li>
</ol>

Step 1 is easy to miss. The network does not store Carol's digits as pictures. It stores what it learnt from them,
mixed into the same numbers that hold what it learnt from everyone else. Step 2 is why deletion fails. The model is a
separate file, and nothing about deleting a row reaches into that file. Step 4 is why the obvious repair fails too.
If her influence sat in a handful of weights, you could reset them. It does not.

Here are the numbers from the course, before and after retraining without Carol.

| Model | Carol's own digits | Unseen thick-marker digits | Everyone else's test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

Before, the model is much better on Carol's digits than on digits *like* hers. That gap is her **fingerprint**. After
retraining, the gap is gone and everyone else's accuracy has not moved.

Why compare with look-alike digits and not with the test set? Because thick digits are harder to read for any model.
Comparing Carol's 100.0% with the 98.0% test score would mix two effects, her style and her presence in training. The
80 look-alike digits share her style but were never trained on, so the gap with them measures her presence alone.

??? deep "Go deeper · why there is no Carol weight to delete"
    Lesson 04 trains the network twice from the **same seed**, once with Carol and once without, and compares every
    weight.

    | Measure | Result |
    |---|---|
    | Weights that differ at all | 94.1% of 85,002 |
    | Weights that differ by more than 0.001 | 87.4% |
    | Distance between the with-Carol and without-Carol networks | 9.87 |
    | Distance between two networks on the same data, seeds 0 and 1 | 50.96 |

    The reason is the path. Training is thousands of small steps, and each step starts from where the last one ended.
    Once Carol's first batch nudged the weights, every later step started from a slightly different place, so the
    difference spread to almost every number.

    The last two rows matter even more. Two equally good networks trained on *identical* data, with test accuracy of
    98.0% and 98.7%, are about five times further apart (50.96 against 9.87) than the pair that differ only by Carol.
    So "how close are the weights to a retrained model?" is not a fair test. Even two retrains are far apart.

??? checkpoint "Checkpoint 1 · On Monday a company deletes Carol's 40 rows. On Tuesday someone tests the model on her digits. What score do they see?"
    **100.0%, exactly as before.** The model was not touched, so its weights and its answers are the same. Her
    fingerprint, 22.5 points better on her digits than on digits like hers, is still there for anyone who looks.

### Memorisation depends on the model

Not every model remembers Carol to the same degree. Lesson 04 measured the fingerprint gap for six models trained on
the same digits.

<div class="stats">
<div class="is-good"><strong>−1.3 pts</strong><span>Naive Bayes, which keeps only averages</span></div>
<div><strong>+15.0 pts</strong><span>logistic regression</span></div>
<div class="is-bad"><strong>+22.5 pts</strong><span>the neural network</span></div>
<div class="is-bad"><strong>+30.0 pts</strong><span>the random forest</span></div>
</div>

The more flexible the model, the more it remembers individuals. Naive Bayes stores only counts and averages per class, and 40
digits barely move an average. The network and the forest can bend to fit Carol's exact strokes, so they do. Lesson 04
has the [full table](../lessons/04-deleting-is-not-forgetting.md).

## A worked example

Follow Carol's erasure request through one company.

1. **The request.** Carol asks the company to erase her data. Her 40 digits were part of the 1,257 used to train the
   digit network.
2. **The database team deletes her rows.** The model is not retrained. It still gets 100.0% of her digits right,
   which is 40 of 40, and 77.5% of the 80 look-alike digits, which is 62 of them.
3. **The shortcut.** Someone suggests training the model a little longer on the remaining 1,217 digits, so that it
   "moves on". In Lesson 06, 20 more epochs of this left Carol at 95.0%, which is 38 of her 40 digits. A model that
   already fits her has nothing pushing it away from her.
4. **The real fix.** The team retrains from scratch on the 1,217 digits. It takes 0.27 seconds for this small
   network. Carol drops to 55.0%, which is 22 of 40. The look-alike digits score 62.5%, which is 50 of 80.
5. **The check.** Her own digits now do slightly worse than digits like hers, 55.0% against 62.5%. The gap has
   gone from +22.5 points to −7.5 points, so her digits get no special treatment. Test accuracy is 98.0% before and
   after, so nobody else paid for it.

Steps 2 and 3 both feel like progress, and neither one is. Only step 4 changes what the model knows about Carol.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>100.0%</strong><span>Carol after her rows are deleted, unchanged</span></div>
<div class="is-bad"><strong>95.0%</strong><span>after 20 more epochs without her</span></div>
<div class="is-good"><strong>55.0%</strong><span>after retraining from scratch without her</span></div>
<div><strong>94.1%</strong><span>of the 85,002 weights change when she is removed</span></div>
</div>

??? checkpoint "Checkpoint 2 · An unlearnt network's weights sit at distance 9.87 from a retrained one. A vendor calls that proof of forgetting. Is it?"
    **No.** Two networks trained on the *same* data with different seeds sit 50.96 apart, and both are perfectly good.
    Distance in weights says almost nothing about what a model knows. The proof has to be about behaviour, such as
    Carol's accuracy and a membership attack, compared with models that never saw her.

## Limits

**Retraining is exact but not cheap.** It removed Carol completely here because the network takes a fraction of a
second to train. For a large model it is very costly, which is why the rest of the course looks for shortcuts.

**Even the retrained answer is a spread.** A retrain with seed 0 gave 55.0% on Carol. In Lesson 06, 20 retrains
ranged from 47.5% to 70.0%. So "the" model that never saw her is really a [band](gold-band.md) of models.

**The fingerprint needs look-alike data.** The course can make thick-marker digits on purpose. In real life you may
not have data that matches one person's style, and then the gap is harder to measure. A
[membership inference attack](membership-inference-attacks.md) is the more general test.

**A small gap does not mean nothing to forget.** For typical users, the original model already scores like a model
that never saw them, because they look like everyone else. Their influence is still in the weights. It just does not
show up as extra accuracy.

!!! tip "What to do in practice"
    - Treat every erasure request as two jobs, the records and every model trained on them.
    - Keep a list of which models were trained on which data, so you can find the models a request touches.
    - Measure the person's fingerprint before and after, against look-alike data or with a membership attack.
    - Compare with a model retrained without the person, never with a score of zero.

## In code

The course library hides the training loop behind two calls, so the comparison is short.

```python
from mul import lab, train, methods

L = lab.make_lab("carol")      # 1,257 digits, 40 of them Carol's
original = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
retrained, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)

print(train.accuracy(original, L.Xf, L.yf))    # Carol's digits, before: 1.00
print(train.accuracy(retrained, L.Xf, L.yf))   # Carol's digits, after:  0.55
```

`L.Xf` is the **forget set** (Carol's data) and `L.Xr` is the **retain set** (everyone else). See
[The notation](notation.md) for all the symbols. The look-alike digits are `L.X_like_forget`, so
`train.accuracy(original, L.X_like_forget, L.y_like_forget)` gives the other half of the fingerprint, 0.775.

## Common mistakes

!!! danger "Mistakes people make"
    - **"We deleted the data, so we are done."** The model still carries the data's influence.
    - **"Forgotten means 0% on Carol."** No. A model that never met Carol still reads 55% of her digits, because it learnt
      what digits look like from everyone else. Forgetting means *matching a model that never saw her*, not scoring zero.
    - **"Just compare the weights."** Two good models trained on the same data can have very different weights. The proof
      has to be about *behaviour* (see [The gold band](gold-band.md)).
    - **"Keep training without her and she will fade."** After 20 more epochs she was still at 95.0%. Training on the
      other data gives the model no reason to drop her.
    - **"Compare her score with the test set."** Her style is harder for any model, so compare with look-alike data.

??? checkpoint "Checkpoint 3 · A spam filter is a Naive Bayes model, whose fingerprint gap for Carol was −1.3 points. Is deleting her rows enough?"
    **No, but the fix is cheap.** A small gap means the model barely memorised her, not that she is absent. Naive
    Bayes stores counts and averages, and her data is still added into them until someone takes it out. Because the
    model is a sum, you can subtract her part exactly, as [Exact unlearning for classical models](exact-unlearning-classical.md)
    shows.

## Key takeaways

!!! notes "Notes to take"
    - **Deleting.** Removes the rows. The model's weights, and so its answers, stay exactly the same.
    - **Unlearning.** Changes the model so it acts as if it never saw the data.
    - **Fingerprint.** Score on her own data minus score on look-alike data. Carol's was +22.5 points.
    - **Who is at risk.** Unusual data is memorised the most. Naive Bayes −1.3 points, the network +22.5.
    - **Spread out.** Removing Carol changes 94.1% of the 85,002 weights, so there is no Carol weight.
    - **Retraining.** Carol 100.0% to 55.0%, test 98.0% before and after.
    - **Trap.** Training longer without her left her at 95.0%.
    - **Proof.** Check behaviour against retrained models, never weight distances.

## Quiz

```quiz
- q: A company deletes Carol's rows from its database. What happens to the trained model?
  options:
    - Nothing changes; its weights still carry her influence.
    - It forgets her at once.
    - It stops working until it is retrained.
  answer: 0
  why: After training, the model only uses its weights. Deleting rows from the database does not touch them.
- q: In the cookbook picture, what does the cake stand for?
  options:
    - The training data
    - The trained model
    - The unlearning method
  answer: 1
  why: The page is the data and the cake is the model made from it. You can tear out the page, but you cannot un-bake the cake.
- q: Before unlearning, the model scores 100% on Carol's digits and 77.5% on unseen thick-marker digits. What does that gap show?
  options:
    - The model is broken.
    - The model has memorised Carol's specific digits.
    - Thick-marker digits are impossible to read.
  answer: 1
  why: The model is much better on *her* digits than on digits *like* hers. That extra accuracy comes from having trained on them.
- q: After Carol is truly forgotten, what should her accuracy look like?
  options:
    - Exactly 0%
    - Still 100%
    - About the same as a model that never saw her
  answer: 2
  why: The target is the retrained model, not zero. A model that never met Carol still reads many of her digits.
- q: Why can we not simply find and delete "Carol's weights" in a neural network?
  options:
    - Her influence is spread across almost all the weights.
    - The weights are encrypted.
    - Neural networks do not have weights.
  answer: 0
  why: Removing Carol changes 94.1% of the network's 85,002 weights. There is no small set of weights that holds her.
- q: Why does the course measure Carol's fingerprint against unseen thick-marker digits rather than the test set?
  options:
    - The test set is too small.
    - Thick digits are harder for any model, so only look-alike data separates her presence from her style.
    - The test set contains Carol's digits.
  answer: 1
  why: The look-alike digits share her style but were never trained on, so the gap with them measures what training on her added.
- q: After deleting Carol's rows, a team trains the model for 20 more epochs on everyone else. In Lesson 06, what happened to her accuracy?
  options:
    - It fell to about 55%, like a retrained model.
    - It fell to 0%.
    - It stayed high, at 95.0%.
  answer: 2
  why: A model that already fits Carol gets no signal to move away from her. Only retraining from scratch removed her.
- q: Which model memorised Carol the most in Lesson 04?
  options:
    - The random forest, with a gap of +30.0 points
    - Naive Bayes, with a gap of −1.3 points
    - Logistic regression, with a gap of +15.0 points
  answer: 0
  why: Flexible models can bend to fit one person's exact data. The forest topped the table, with the network next at +22.5 points.
```

## Try it

!!! levelup "Level up"
    You can now explain why a deleted row lives on inside a model and how to measure what is left. Next quest,
    [Why the law cares](why-the-law-cares.md), where regulators order whole models deleted for exactly this reason.

- The lesson [00 · Read this first](../lessons/00-read-first.md) runs the full before-and-after in four cells.
- The lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) shows why every classical trick fails in a neural network.
- Read the next concept, [Why the law cares](why-the-law-cares.md).
