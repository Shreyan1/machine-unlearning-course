---
title: "Lesson 04 · Deleting is not forgetting"
description: Why every classical unlearning trick fails in a neural network, and why the proof of forgetting must be about behaviour.
---

# Lesson 04 · Neural networks, why deleting is not forgetting

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 2 · Neural nets, the problem</span><span class="chip" markdown="span">:material-stairs-up: Rung 4</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 30 minutes · 3 checkpoints"
    By the end of this lesson you can

    - measure how much a model memorised Carol, with the gap between her digits and digits like hers,
    - explain why subtracting, a Newton step and locality all fail in a neural network,
    - say why the proof of forgetting must be about behaviour, and why the target is a band.

## The story so far

In Lessons 01 to 03, every classical model gave us a handle for forgetting.

| Handle | Classical models | Neural network |
|---|---|---|
| A **sum** you can subtract from | Naive Bayes, k-NN, ridge | ❌ The weights are the end of a long path of small steps, each depending on the last. |
| A **single best answer** you can step to | Ridge, logistic regression | ❌ There are many equally good answers. |
| **Locality.** Only a few parts depend on a point | SVM, random forest | ❌ Every example nudges **every** weight. |

This lesson makes each ❌ concrete, with numbers.

Carol has asked to be erased, and so far that has been easy. Naive Bayes forgot her by subtracting her counts. Ridge
forgot her with a downdate. A sharded forest forgot her by retraining the trees she reached. Now the model is a neural
network, the kind most modern systems use. The question is whether any of those tricks still work, or whether the
better model has made Carol much harder to remove.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a small neural network (64 → 256 → 256 → 10, with 85,002 weights) on the digits, including Carol's 40.</li>
<li markdown>**Show the issue.** Measure how much each model memorises Carol, from Naive Bayes up to the network.</li>
<li markdown>**Try the classical tricks** one by one. Subtract, take a Newton step and rebuild only the touched part.</li>
<li markdown>**Untrain** with the only exact option left, which is to retrain from scratch without Carol.</li>
<li markdown>**Prove it** by behaviour, not by weights.</li>
</ol>

## What each step teaches

**Train.** The network reads the 64 pixels of a digit and passes them through two hidden layers of 256 neurons to 10
outputs, one per digit. Training runs for 60 epochs in batches of 64, and every batch nudges all 85,002 weights a
little. The loss curves show the first warning. Carol's own digits are pushed to almost zero loss, while unseen digits
in the same thick style stay far higher. The network has learnt *her* 40 digits, not just thick digits.

**Show the issue.** Six models are trained on the same digits and scored the same way, on Carol's digits and on 80
look-alike digits that were made thick but never trained on. The difference is a simple, honest memorisation score. It
lets you compare a model that keeps averages with one that can bend to fit a single person.

??? deep "Go deeper · a sharper lens, memorisation for each digit"
    The gap treats Carol's 40 digits as one block. Feldman (2020) defines memorisation for **each example**.

    \[
    \text{mem}(x) = P[\text{right on } x \mid x \text{ in training}] - P[\text{right on } x \mid x \text{ not in training}]
    \]

    The notebook estimates it by training six networks with the probe digits and six without them, for Carol's 40
    digits and 40 random typical digits. Typical digits score close to 0, because thousands of similar digits teach
    the network the same thing whether or not they are in training. Many of Carol's digits score high, because they
    are right only *because* they were trained on.

    That is Feldman's long-tail argument. Real data has many rare cases, and fitting them requires memorising them.
    So the people with unusual data are both the most memorised and the most exposed.

**Try the classical tricks.** This is the heart of the lesson. Each trick from Lessons 01 to 03 relied on one handle,
and each test removes it with a number. Subtracting needs Carol to sit in a few weights. A Newton step needs one best
answer to step to. Locality needs parts of the model that never saw her.

**Untrain.** With every shortcut gone, retraining from scratch on the 1,217 digits that are left is the only exact
option. It is cheap here and very costly for a large model, which is the gap the next lessons attack.

**Prove it.** Because the weights of good networks differ anyway, the only fair check is behaviour. The retrained
model should treat Carol's digits like any other unseen digits in her style.

## Key results

**Who memorises more?** The "memorisation gap" is the accuracy on Carol's digits minus the accuracy on unseen digits in
her style.

| Model | Carol | Unseen thick | Gap | Test |
|---|---|---|---|---|
| Naive Bayes | 60.0% | 61.3% | −1.3% | 91.1% |
| k-NN, k = 5 | 75.0% | 67.5% | +7.5% | 98.3% |
| Logistic regression | 92.5% | 77.5% | +15.0% | 97.2% |
| RBF SVM | 100.0% | 87.5% | +12.5% | 99.4% |
| Random forest | 100.0% | 70.0% | +30.0% | 97.2% |
| **Neural network** | 100.0% | 77.5% | **+22.5%** | 98.0% |

The more flexible the model, the more it remembers individuals. Naive Bayes, which only keeps averages, does not
memorise Carol at all.

Read the rows that matter. The SVM, the forest and the network all get every one of Carol's 40 digits right, yet
their gaps differ, because their scores on look-alike digits differ. The SVM reads 87.5% of the look-alikes, so much of
its 100% on Carol is skill with thick digits. The forest reads only 70.0%, so more of its 100% is memory. The network
sits between them at +22.5 points, and unlike the forest it has no trees to rebuild separately.

<div class="stats">
<div class="is-bad"><strong>+22.5 pts</strong><span>the network's gap on Carol's digits</span></div>
<div class="is-bad"><strong>94.1%</strong><span>of 85,002 weights change when she is removed</span></div>
<div class="is-bad"><strong>29 GB</strong><span>for the Hessian a Newton step needs</span></div>
<div class="is-good"><strong>55.0%</strong><span>Carol after retraining, near 62.5% on look-alikes</span></div>
</div>

??? checkpoint "Checkpoint 1 · The SVM and the network both score 100.0% on Carol. Why does the SVM have the smaller gap?"
    **Because it is better on look-alike digits.** The SVM reads 87.5% of unseen thick digits and the network 77.5%,
    so the gaps are +12.5 and +22.5 points. A raw score on Carol cannot tell skill from memory. Only the comparison
    with data like hers that the model never saw separates the two.

**The three tricks all fail.**

- **Subtract her?** Removing Carol changes **94.1%** of the 85,002 weights. She is not stored anywhere in particular.
- **One Newton step?** It needs a table of 85,002 × 85,002 numbers, about **29 GB**. For a 7-billion-weight language
  model it would be about 98 exabytes. Worse, two networks trained on the *same* data with different random starts end
  up further apart (distance 50.96) than the with-Carol and without-Carol pair (distance 9.87). There is no single
  "right" network to step towards.
- **Rebuild only what she touched?** She touched everything, unless we design the network for it (that is
  [SISA](../unlearning/sisa.md), Lesson 07).

The first trick is tested by training twice from the same seed, once with Carol and once without. Even counting only
weights that moved by more than 0.001, 87.4% changed. The reason is the path. After her first batch, every later step
started from a slightly different place, so the difference spread everywhere.

The distances say even more. The two seeds give networks with test accuracy of 98.0% and 98.7%, both perfectly good,
yet about five times further apart than the pair that differ only by Carol (50.96 against 9.87). So "the" retrained
network is not one point. It is a whole spread of equally good networks.

??? deep "Go deeper · where the Hessian numbers come from"
    The Hessian has one entry for every pair of weights, so 85,002 × 85,002 = 7,225,340,004 entries. Stored in
    float32, each entry takes 4 bytes, which gives about 29 GB. For a model with 7 billion weights, the notebook counts
    \((7 \times 10^9)^2\) entries at 2 bytes each, which is about \(9.8 \times 10^{19}\) bytes, or 98 exabytes.

    Size is not the only problem. A Newton step aims at *the* optimum, and a network has many equally good ones, so
    even an exact Hessian would point at one of countless targets.

??? checkpoint "Checkpoint 2 · A colleague suggests finding the few weights that changed most when Carol was removed and resetting only those. Will it work?"
    **No.** There is no small set to find. 94.1% of the weights changed at all, and 87.4% changed by more than 0.001.
    Her influence is spread across almost the whole network, so resetting a few weights would leave most of it behind.

**Retraining works.** Carol's accuracy drops from 100.0% to 55.0%, close to the 62.5% on unseen thick digits, and test
accuracy stays at 98.0%. It took 0.27 seconds here. For a large model it would take a very large amount of GPU time.

In counts, Carol goes from 40 of her 40 digits to 22, and the look-alikes from 62 of 80 to 50. Her gap moves from
+22.5 points to 55.0 − 62.5 = −7.5 points, so her own digits no longer get special treatment.

!!! note "Why this matters"
    Because many equally good networks exist, the "retrained model" is not one point but a whole spread of models.
    So comparing weights can never prove forgetting. The proof must be about **behaviour**, and the target is a
    **band**, not a number.

## Limits of this lesson

**One seed for most comparisons.** The table, the weight count and the retrain each come from seed 0. Lesson 06 shows
that retrains with other seeds land anywhere from 47.5% to 70.0% on Carol, so 55.0% is one roll of the dice.

**A small, synthetic setting.** The digits are 8 × 8 pixels, the network is small and Carol's style is made by widening
every stroke by one pixel. The same measurements work on larger models, but the numbers will differ.

**The gap needs look-alike data.** The course can make thick digits on purpose. In real life you rarely have data in
exactly one person's style, which is why Lesson 05 builds an attack that needs only the model's answers.

**Distance is one summary.** The weight distances are a single number each. They show that weights are a poor guide,
not how far apart two models are in what they know.

??? checkpoint "Checkpoint 3 · The retrained network scores 55.0% on Carol but 62.5% on look-alikes. Is it over-forgetting her?"
    **No.** This model never saw Carol, so by definition it is a fair example of the target. Her digits may simply be
    a little harder than the look-alikes. One retrain is also one roll of the dice, and Lesson 06 shows the honest range
    is wide. The right check is whether a result lands inside the band of many retrains.

## Concepts used here

- [Neural networks](../ml-basics/neural-networks.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)
- [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md)
- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The gold band](../unlearning/gold-band.md)

## Notes to take

!!! notes "Notes to take"
    - **Memorisation gap.** Score on Carol's digits minus score on unseen digits in her style.
    - **Who memorises.** Naive Bayes −1.3 points, the network +22.5, the forest +30.0.
    - **No sum.** Removing Carol changes 94.1% of the 85,002 weights.
    - **No single answer.** Two seeds sit at distance 50.96, the Carol pair at 9.87.
    - **No Newton step.** The Hessian would take about 29 GB here and 98 exabytes for a 7-billion-weight model.
    - **No locality.** She touched almost every weight, unless SISA builds locality in.
    - **Retraining.** Exact. Carol 100.0% to 55.0%, test 98.0%, 0.27 seconds here.
    - **Proof.** By behaviour against a band of retrains, never by comparing weights.

## Quiz

```quiz
- q: Which model did **not** memorise Carol at all in this lesson?
  options:
    - The neural network
    - The random forest
    - Naive Bayes
    - The RBF SVM
  answer: 2
  why: Naive Bayes only keeps averages per class, so its gap was −1.3%. One person barely moves an average.
- q: When Carol is removed and the network is retrained from the same seed, roughly how many weights change?
  options:
    - About 1%
    - About 25%
    - About 94%
  answer: 2
  why: 94.1% of the 85,002 weights differ. Her influence is spread across the whole network.
- q: Why does a single Newton step not work for the network, even ignoring memory?
  options:
    - The network has no single best answer to step towards.
    - Newton steps only work on images.
    - The network has too few weights.
  answer: 0
  why: Two networks trained on the same data with different random starts land far apart and are equally good. There is no one optimum.
- q: Two networks are trained on identical data with different seeds. Compared with the with-Carol and without-Carol pair, they are...
  options:
    - Much closer together
    - Much further apart
    - Exactly the same
  answer: 1
  why: The seed pair is at distance 50.96, the Carol pair at 9.87. Random starts matter more than Carol does.
- q: What must a proof of forgetting in a neural network be based on?
  options:
    - Comparing the weights one by one
    - The model's behaviour, compared with models that never saw the data
    - The size of the model file
  answer: 1
  why: Weights differ between equally good models anyway, so only behaviour can be compared fairly.
- q: Why does the lesson compare Carol's digits with unseen thick-marker digits rather than just reporting her score?
  options:
    - Her score alone mixes skill with thick digits and memory of hers, and the look-alikes separate the two.
    - The test set is too small to use.
    - Thick digits are always read correctly.
  answer: 0
  why: The SVM and the network both scored 100.0% on Carol, but their look-alike scores of 87.5% and 77.5% show the network memorised more.
- q: In Feldman's per-example measure, why do typical digits score close to zero?
  options:
    - The network never sees them.
    - They are always wrong.
    - Thousands of similar digits teach the same thing, so they are right whether or not they were in training.
  answer: 2
  why: Memorisation is the extra chance of being right because an example was trained on. Typical digits get no extra chance.
- q: Retraining from scratch removed Carol exactly. Why do the next lessons not stop there?
  options:
    - It made test accuracy fall sharply.
    - It is exact but its cost grows with all the data you keep, which is unaffordable for large models.
    - It does not work for neural networks.
  answer: 1
  why: It took 0.27 seconds for this network and would take a very large amount of GPU time for a large one, with requests that keep coming.
```

## Open question → Lesson 05

!!! levelup "Level up"
    You can now show why every classical shortcut fails in a network and why forgetting must be proved by behaviour.
    Next quest, [Lesson 05, membership inference attacks](05-membership-inference.md), where you build that behavioural
    test.

The proof must be about behaviour. Imagine you are an outsider who can only send questions to a model. Could you
**tell whether Carol's data was used to train it?** If you can, the model is leaking, and you also have a tool to check
every unlearning method in the course.

[On to Lesson 05, membership inference attacks :material-arrow-right:](05-membership-inference.md){ .md-button }
