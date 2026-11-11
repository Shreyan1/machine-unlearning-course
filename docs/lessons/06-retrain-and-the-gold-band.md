---
title: "Lesson 06 · Retrain and the gold band"
description: Retrained networks disagree, so the gold standard is a band. Measure it, check the original falls outside and price exact retraining.
---

# Lesson 06 · Retraining from scratch, the gold standard is a band

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~25 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 3 · Exact unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 5</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 25 minutes · 3 checkpoints"
    By the end of this lesson you can

    - show that retrained networks disagree and turn their spread into a gold band,
    - check a model against that band and explain why "keep training without her" fails it,
    - price exact retraining for a real service and say what the bill depends on.

## The story

Classical models are **deterministic**. Retrain them twice and you get the same model to the last digit. A neural network
depends on random starting weights and random batch order, so retraining it is like **rolling dice**. Every roll is an
equally valid "model that never saw Carol". So an unlearning method has to hit a **band**, not a point.

Lesson 05 already hinted at this. To calibrate the membership attack it trained eight networks without Carol, and
they did not agree with each other. So which one is "the" retrained model? If you pick one, a good unlearning method
can fail because the reference landed at one edge, and a bad one can pass because it landed nearby. This lesson
measures how wide the spread really is, then measures what it costs to reach it the only exact way known so far.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** classical models five times and see how wide *their* band is.</li>
<li markdown>**Show the issue.** Retrain the network 20 times without Carol and measure the spread.</li>
<li markdown>Compare deleting Carol, a random group of users and a whole class.</li>
<li markdown>**Untrain** by retraining, and check it against the band.</li>
<li markdown>Test the shortcut "just keep training without her", and **price** exact retraining.</li>
</ol>

## What each step teaches

**Step 1. Classical models.** Naive Bayes and Newton-solved logistic regression are retrained five times each. Every
retrain gives exactly the same score on Carol, so their band has zero width. That is why Lessons 01 to 03 could check
for identical predictions.

**Step 2. The network's spread.** Twenty retrains with seeds 100 to 119, all on the same 1,217 digits with the same
recipe, show how much honest models disagree. This is the central result of the lesson.

**Step 3. Three requests.** The band is measured again for Carol, for random typical users and for a whole class. Each
request gives a band of a very different shape, so the target depends on what is being forgotten.

**Step 4. Untrain.** One more retrain, with seed 999, plays the part of the unlearnt model. The band is built from ten
of the retrains, and the course's `gate` gives a PASS or FAIL. Every method in Lessons 07 to 11 faces this same gate.

**Step 5. The trap and the price.** The original model is trained for 20 more epochs on the retain set only, to test
the cheapest-looking shortcut. Then placeholder production numbers show how the cost of exact retraining grows.

??? deep "Go deeper · how step 4 scores a model against the band"
    `audit.gold_band` scores each reference retrain the same way a method is scored and returns the mean and the
    standard deviation of every measure. `audit.gate` then marks FORGET as passed when accuracy on Carol lies within
    the mean plus or minus the larger of two standard deviations and 3 points. UTILITY passes when test accuracy is no
    more than 2 points below the retrains' mean. A model must pass every check to get PASS.

    The full method, with its worked example and the widget, is on [The gold band](../unlearning/gold-band.md).

## Key results

<div class="stats">
<div><strong>47.5–70.0%</strong><span>20 honest retrains on Carol, a spread of 22.5 points</span></div>
<div><strong>62.0% ± 9.2%</strong><span>the band used in the audit, 52.8% to 71.2%</span></div>
<div class="is-good"><strong>62.5%</strong><span>a new retrain with seed 999, PASS</span></div>
<div class="is-bad"><strong>95.0%</strong><span>20 more epochs from the original, FAIL</span></div>
</div>

- **Classical models.** Naive Bayes always gave 27.5% on Carol; logistic regression always 62.5%. The band has zero width.
- **The network, 20 retrains.** Mean **62.0%** on Carol, standard deviation 5.6%, range **47.5% to 70.0%**. Test
  accuracy 98.2% ± 0.34%. The original scored **100.0%**, far outside.
- **The band depends on the request.** Wide and in the middle for Carol; narrow and near 100% for random users (the
  original is already inside); exactly 0% for a whole class.

The second bullet is the one to remember. Carol has 40 digits, so each is worth 2.5 points, and the retrains got
between 19 and 28 of them right. On the test set the same retrains almost agree. The difference is that Carol's
digits are unusual, so whether a model reads them depends on small random details of its training. The band is widest
exactly where unlearning has real work to do.

??? checkpoint "Checkpoint 1 · One retrain scored 47.5% on Carol and another 70.0%. Which one is the right retrained model?"
    **Both.** Each was trained without Carol, on the same data with the same recipe, and only the seed differed. Each
    is an equally valid model that never saw her. That is why the target is the whole spread, and why one retrain
    used as the only reference would make the verdict depend on luck.

| Method | Forget accuracy | Verdict |
|---|---|---|
| Original | 100.0% | FAIL |
| New retrain (seed 999) | 62.5% | PASS |

Read the two rows against the band of 52.8% to 71.2%. **The original** gets all 40 of Carol's digits right and lands
far above the band, so it fails FORGET. **The new retrain** lands near the middle and passes. Both score 98.0% on the
test set, so both pass UTILITY. The retrain took 0.28 seconds.

**The shortcut trap.** After 20 more epochs of training the original on \(D_r\) only, Carol was still at **95.0%**,
against a band of 62.0% ± 9.2%. A model that already fits Carol has nothing pushing it away from her. Only a fresh start
is exact.

??? checkpoint "Checkpoint 2 · The warm-started model gets 95.0% of Carol's digits right. How many more would it have to lose to enter the band?"
    **Ten.** 95.0% is 38 of her 40 digits. The top of the band is 71.2%, and the highest score at or below it is
    70.0%, which is 28 digits. So it would have to lose 38 − 28 = 10 more. Twenty epochs of neglect removed only 2,
    which shows how slowly a model forgets by not being reminded.

**The cost** (placeholder production numbers). Retraining daily to batch requests ≈ $7.3 million a year; weekly ≈ $1.04
million; monthly ≈ $243,000. The cost grows with the data you **keep**, not the data you delete.

The placeholders are $20,000 for one training run and 300 deletion requests a month. A daily batch holds about 10
requests and needs 365 runs a year. A monthly batch holds about 300 and needs 12. Every batch is still one full
training run, so batching lowers the number of runs but never the price of one.

??? checkpoint "Checkpoint 3 · A team moves from weekly to monthly retraining. Roughly how much do they save a year, and what is the catch?"
    **About $800,000.** Weekly costs about $1,042,857 and monthly about $243,333, a difference of about $799,500. The
    catch is time. A monthly batch uses the whole of the 30-day deadline the lesson assumes, so a request that arrives
    just after a batch, or one failed run, leaves no room to answer on time.

## Limits of this lesson

**A band from ten retrains.** The audit's band uses 10 of the 20 retrains. With fewer references the band is less
stable, and a band of two standard deviations will now and then reject an honest model, as Lesson 11 shows with SISA.

**One small network.** The numbers come from 8 × 8 digit images, one network and a 40-digit forget set. The idea
carries over to larger models, but the width of the band must be measured again for each one.

**Placeholder costs.** The dollar figures are illustrative, not measurements of any real system. Replace them with
your own cost per run and request rate.

**One shortcut tested.** The warm start is tried for 20 epochs only. The notebook's tasks ask how it behaves after
more epochs.

## Concepts used here

- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The gold band](../unlearning/gold-band.md)
- [Neural networks](../ml-basics/neural-networks.md)

## Notes to take

!!! notes "Notes to take"
    - **Classical models.** Deterministic, so Naive Bayes always scores 27.5% on Carol and logistic regression 62.5%.
    - **Networks disagree.** 20 retrains ranged from 47.5% to 70.0% on Carol, with a mean of 62.0%.
    - **Test set.** The same retrains average 98.2%, with a standard deviation of only 0.34 points.
    - **Gold band.** Mean ± 2 standard deviations. Carol's band is 62.0% ± 9.2%, so 52.8% to 71.2%.
    - **Verdicts.** Original 100.0% FAIL, new retrain 62.5% PASS.
    - **Depends on the request.** Carol wide, random users near 100% with the original inside, a whole class 0%.
    - **Trap.** Warm-starting for 20 epochs leaves Carol at 95.0%. Only a fresh start is exact.
    - **Cost.** One full run per batch. Placeholder costs of $7.3 million a year daily, about $243,000 monthly.

## Quiz

```quiz
- q: Why do classical models like Naive Bayes have a band of width zero?
  options:
    - They are deterministic; every retrain gives the same model.
    - They are always perfect.
    - They cannot be retrained.
  answer: 0
  why: Without randomness in training, there is only one possible retrained model.
- q: Across 20 retrains, what was the range of accuracy on Carol's digits?
  options:
    - 61% to 63%
    - 47.5% to 70.0%
    - 0% to 100%
  answer: 1
  why: Retrained networks disagree by more than 20 points, so a single retrain is just one draw.
- q: For random typical users, where is the original model relative to the band?
  options:
    - Already inside it
    - Far above it
    - Far below it
  answer: 0
  why: Typical data was never memorised, so the original already behaves like it never saw it.
- q: After 20 more epochs of training on the retain set only, what was Carol's accuracy?
  options:
    - 62.0%
    - 95.0%
    - 0%
  answer: 1
  why: Continuing to train is not retraining; it stays far outside the band.
- q: What does the cost of exact retraining grow with?
  options:
    - The size of the data you keep
    - The size of the data you delete
    - The number of test examples
  answer: 0
  why: Every retrain processes all the retained data again.
- q: The retrains disagreed by more than 20 points on Carol, while on the test set their standard deviation was only 0.34 points. Why?
  options:
    - The test set is smaller than Carol's set.
    - The test set was used in training.
    - Carol's digits are unusual, so reading them depends on small random details of training.
  answer: 2
  why: Every model learns typical digits well. Unusual data is where retrains disagree, and where the band is widest.
- q: Why does a model at 95.0% on Carol fail, even though it never saw her during its last 20 epochs?
  options:
    - It started from the original model, which already fitted her, and nothing pushed it away.
    - It was trained for too few epochs to learn the other digits.
    - Its test accuracy fell too far.
  answer: 0
  why: Warm-starting is fine-tuning. Only training from new random weights gives a model that never saw her.
- q: Batching requests monthly instead of daily cuts the placeholder bill from $7.3 million to about $243,000. Why does it not cut it further?
  options:
    - Each batch still needs one full training run on everything you keep.
    - The cost of deleting each request is fixed.
    - Monthly batches must be retrained twice.
  answer: 0
  why: About 12 runs a year (365 divided by 30) at $20,000 each is about $243,000. Batching cuts the number of runs, not the cost of one.
```

## Open question → Lesson 07

!!! levelup "Level up"
    You can now build a gold band, judge a model against it and price exact retraining. Next quest,
    [Lesson 07 · SISA](07-sisa.md), where the network is designed so that retraining touches only a small slice of
    the data.

In Lesson 03, a forest forgot Carol by retraining only **10 of 50 trees**, because it was *designed* with user-aware
shards. Can a neural network be designed the same way?

[On to Lesson 07, SISA :material-arrow-right:](07-sisa.md){ .md-button }
