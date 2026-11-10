---
title: The gold band
description: Retrained neural networks disagree with each other, so the target for unlearning is a band of results from several retrains, not one number.
---

# The gold band

!!! oneline "In one line"
    The **gold band** is the range of results you get from *several* models retrained without the data; an unlearnt
    model passes if it lands inside that range.

## Why it matters

To check an unlearning method, you compare it with the ideal answer. The ideal answer is a model retrained from scratch
without the data, which the course calls the [gold standard](retraining-gold-standard.md). Most unlearning tutorials
compare their method with **one** such retrained model. That sounds fair, but it hides a problem. Two neural networks
retrained in exactly the same way, on the same data with the same code, do not agree with each other. In Lesson 06 they
disagreed by more than 20 points on Carol's digits.

So which retrained model is "the" right answer? None of them alone. Each one is an equally valid model that never saw
Carol. If you compare with just one, the verdict depends on luck. A good method can fail because the one reference
happened to land at one edge. A bad method can pass because the one reference happened to land near it. The gold band
fixes this by comparing with the whole spread of retrained models at once.

This matters to anyone who must show that data was removed, such as an engineer answering an erasure request or an
auditor. Every audit in the course, up to the full protocol in Lesson 11, uses the gold band as its pass mark.

## A simple example

!!! simply "Explain it simply"
    Imagine five honest students who never saw the exam answers. Their scores differ a little, with one getting 60 and another 70.
    That spread is the gold band. A student who claims they "forgot" the answers should score somewhere in that spread.
    A perfect 100 means they still remember; a 10 means they forgot too much, which is just as suspicious.

Here is a second picture. Ask five good cooks to make the same recipe. Each dish tastes slightly different, but all of
them are "correct". To judge a sixth cook, check whether their dish falls within the range the other five produced.

Now map the pictures onto unlearning. The honest students are models **retrained without Carol**, each one started
with different random numbers. Their scores are each model's **accuracy on Carol's digits**. The spread of those scores
is the **gold band**. The student who claims to have forgotten is the **unlearnt model**, the output of an unlearning
method. The perfect 100 is the **original model**, which memorised Carol. The score of 10 is a model that has
**over-forgotten** her.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Gold standard](../start-here/glossary.md#g) | A model retrained from scratch on the data that is left, so it never saw the forget set | A network trained on the 1,217 digits that are not Carol's |
| [Forget set](../start-here/glossary.md#f) \(D_f\) | The data that must be forgotten | Carol's 40 digits |
| Random seed | A starting number that decides the random choices in training, such as the first weights and the order of the batches | Lesson 06 retrains with seeds 100 to 119 |
| Deterministic | Training that has no randomness, so it gives the same model every time | Naive Bayes always scores 27.5% on Carol |
| Mean | The average of several numbers | The 20 retrains average 62.0% on Carol |
| Standard deviation | A measure of how far the numbers usually sit from the mean. Small means they agree, large means they spread out | 5.6 points across the 20 retrains |
| [Gold band](../start-here/glossary.md#g) | The range from mean minus about two standard deviations to mean plus about two standard deviations | 52.8% to 71.2% on Carol in Lesson 06 |
| [Over-forgetting](../start-here/glossary.md#o) | Scoring far below the band, worse than models that never saw the data | NegGrad+ scored 10.0% on Carol in Lesson 11 |
| [False alarm](../start-here/glossary.md#f) | A test rejecting a model that is actually fine | SISA missed the band on Carol by one digit |

## How it works

<!-- diagram: gold-band -->

The figure shows one line of accuracy on Carol's digits, from 0% to 100%. Each blue dot is one model retrained without
Carol. The dots cluster together in a shaded region, and that region is the gold band. The original model sits at the
far right at 100%, because it memorised her. A green dot inside the band is a good unlearnt model. A red dot far to the
left is an unlearnt model that went too far and over-forgot.

The method has four steps.

### Step 1. Retrain several times

Remove the forget set and train a fresh model on what is left, the retain set \(D_r\). Then do it again with a
different random seed, and again. The course often uses 5 to 20 retrains. Lesson 06 uses 20 to show the spread and
Lesson 11 uses 12 for each request.

Every retrain must use the **same recipe** as the model you want to test. That means the same architecture, the same
number of epochs, the same learning rate and the same way of splitting the data. Only the seed changes. If the recipe
changes, you measure the effect of the recipe, not the effect of forgetting.

**For Carol this means** 20 networks, each trained on the same 1,217 digits, with seeds 100 to 119. None of them ever
saw one of her 40 digits.

### Step 2. Measure each retrained model

Score every retrained model on the things you care about. The most common numbers are accuracy on the forget set, accuracy on
the test set and a membership attack score (how sure an attacker is that the data was used in training). You get one
number per model for each measure.

**For Carol this means** 20 forget accuracies. They ranged from 47.5% to 70.0%. Because Carol has 40 digits, each digit
is worth 2.5 points, so the retrains got between 19 and 28 of her digits right. Their test accuracies were much closer
together, at 98.2% on average.

### Step 3. Build the band

Take the average of the numbers, which is the centre of the band. Then work out the standard deviation, which says how
spread out the numbers are. The band stretches about two standard deviations below the centre and two above it.

In symbols, the band is \(\text{mean} \pm k \times \text{std}\), with \(k = 2\) in the course. Why two? When results
spread out in a bell shape, roughly 95 in every 100 of them land within two standard deviations of the mean. So a
model that truly never saw Carol will usually land inside.

The course also gives the band a **minimum width**. Each side must be at least 3 points wide, whatever the standard
deviation says. This matters when the retrains agree almost perfectly. Without the floor, a band of near zero width
would fail a good model because of a single digit, and one of Carol's digits is already 2.5 points.

**For Carol this means** that in Lesson 06, ten of the retrains gave a mean of 62.0% and two standard deviations of
9.2 points. The band runs from 62.0 − 9.2 = 52.8% to 62.0 + 9.2 = 71.2%.

### Step 4. Check the unlearnt model

Measure the unlearnt model in exactly the same way and ask whether each number is inside the band. There are three
possible results.

- **Inside the band.** The model looks like one that never saw the data. It passes this check.
- **Above the band.** The model still does too well on the forget set. It still remembers.
- **Below the band.** The model does worse than models that never saw the data. It has **over-forgotten**.

The course library turns this into a PASS or FAIL for each check, and the method passes only if every check passes.

**For Carol this means** a new retrain at 62.5% passes and the original model at 100.0% fails.

### How wide is the band?

The width tells you how much retrained models naturally disagree. The 20 retrains in Lesson 06 produced this spread.

- On Carol's digits, accuracy averaged **62.0%**, with a standard deviation of 5.6% and a range of **47.5% to 70.0%**.
- Test accuracy averaged 98.2%, with a standard deviation of 0.34%.
- The original model (with Carol) scored **100.0%** on her digits, far outside the band.

Two networks retrained identically disagreed by more than 20 points on Carol's digits. Notice the contrast. On the test
set, the retrains almost agree, because the test digits are typical and every model learns typical digits well. On
Carol, they disagree a lot, because her thick-marker digits are unusual. Whether a model gets them right depends on
small random details of its training. The band is widest exactly where one person's data is unusual, and that is where
unlearning has real work to do.

<div class="widget" data-widget="goldband" markdown></div>

In the widget, try building the band from only one or two retrains. The band becomes narrow and jumps around each time
you retrain them again. With more retrains it settles down. This is why one reference is not enough.

### Classical models have a band of width zero

Naive Bayes and Newton-solved logistic regression are **deterministic**. Retrain them five times and you get the same
model every time (27.5% and 62.5% on Carol's digits). That is why Lessons 01 to 03 could check for *identical*
predictions. Neural networks depend on random starting weights and random batch order, so retraining is like rolling
dice.

For a deterministic model, "the retrained model" is one clear thing, so an unlearning method can be checked against it
exactly. For a neural network, "the retrained model" is a whole spread of possible models. Exact unlearning then means
producing a model from the same spread, not one with equal weights.

### The band depends on what is forgotten

| What is forgotten | Gold band on \(D_f\) | Original model | Meaning |
|---|---|---|---|
| **Carol** (a memorised person) | Wide, around the middle | Far outside | Real work to do |
| **Random typical users** | Narrow, near 100% | **Inside** | Typical data was never memorised |
| **A whole class** (every "3") | Exactly 0% | Outside | A model that never saw a 3 can never say "3" |

Each row teaches something different. For Carol, the target is wide and sits in the middle, so a method has room to
land but must move a long way from 100%. For random users, a model that never saw them still gets them right, because
they look like everyone else. The original model is already inside the band on accuracy, so this check alone cannot
tell whether anything was forgotten. For a whole class, the target is sharp. A model that never saw any 3 has no way
to answer "3", so the band sits at exactly 0%.

!!! note "Too forgotten is also a failure"
    A model that is far *worse* on Carol than the band is suspicious. It treats her data differently from data it never
    saw, and an attacker can notice that. This is sometimes called the **Streisand effect**.

## A worked example

Follow Carol through Lessons 06 and 11.

1. **The original model.** It was trained on all 1,257 digits, including Carol's 40. It gets 100.0% of her digits
   right, so 40 out of 40. That is the memory we want to remove.
2. **The spread of honest answers.** Lesson 06 retrains the network 20 times without her. The scores run from 47.5%
   (19 digits) to 70.0% (28 digits), with a mean of 62.0%. Every one of them is a valid "model that never saw Carol".
3. **The band.** From ten retrains, the band is 62.0% ± 9.2%, so 52.8% to 71.2%.
4. **The exact answer.** A new retrain with seed 999 scores 62.5%, inside the band. It passes.
5. **The shortcut.** Someone takes the original model and keeps training it on the other digits for 20 more epochs.
   Carol is still at 95.0%, which is 38 of her 40 digits. That is far above 71.2%, so it fails. A model that already
   fits Carol has nothing pushing it away from her.
6. **The audit.** Lesson 11 builds a fresh band from 12 retrains, which gives 62.7% ± 9.5%. That is about 53.2% to
   72.2%. Every method is then scored against it.

| Model in Lesson 11 | Accuracy on Carol | Where it lands | FORGET check |
|---|---|---|---|
| Original | 100.0% | Above the band | FAIL |
| Retrain (seed 999) | 62.5% | Inside | PASS |
| SCRUB | 82.5% | Above the band | FAIL |
| SCRUB+R | 65.0% | Inside | PASS |
| Bad Teacher | 70.0% | Inside | PASS |
| NegGrad+ | 10.0% | Far below the band | FAIL |

NegGrad+ is the clearest case of over-forgetting. It got only 4 of Carol's digits right, which is far worse than any
model that never saw her. It also hurt the rest of the model, with test accuracy down to 84.6%. Passing the band is
also not the end of the story. Bad Teacher was inside the band but failed the separate utility check. SCRUB+R was
inside the band but failed the relearn attack, which is covered in [The unlearning audit](unlearning-audit.md). The
gold band is the first gate, not the only one.

## What the lesson found

| Result | Number | What it means |
|---|---|---|
| Naive Bayes on Carol, 5 retrains | 27.5% every time | Deterministic models have a band of width zero |
| Logistic regression on Carol, 5 retrains | 62.5% every time | The same holds for Newton-solved logistic regression |
| Network on Carol, 20 retrains | Mean 62.0%, std 5.6%, range 47.5% to 70.0% | Identical retrains disagree by more than 20 points |
| Network on test digits, 20 retrains | Mean 98.2%, std 0.34% | On typical data the retrains almost agree |
| Original model on Carol | 100.0% | Memorisation puts it far above the band |
| Band used in the Lesson 06 audit | 62.0% ± 9.2% | The target a method must hit on Carol |
| Retrain with seed 999 | 62.5%, PASS | One more roll of the dice lands inside |
| Keep training without Carol, 20 epochs | 95.0%, FAIL | Warm-starting is not retraining |
| Lesson 11 band on Carol | 62.7% ± 9.5% | A new set of 12 retrains gives almost the same band |
| Lesson 11 band on random users | 98.2% ± 1.6% | Narrow and near the top, so the original passes on accuracy |
| Lesson 11 band on the class "3" | 0.0% ± 0.0% | The sharpest possible target |

The random-users row is a warning. On that request, the original model scored 100%. The printed band reaches only
99.8%, but the 3-point floor stretches it to about 101.2%, so the original model passed FORGET while having forgotten
nothing. Only the per-example PRIVACY check in Lesson 11 caught it.

## Limits

**It is evidence, not proof.** Landing inside the band means no test could tell the model apart from a retrained one on
that number. It does not prove the data is gone. Thudi et al. (2022) show that the same weights can be reached with or
without an example, so a check on the final model can be fooled.

**One number can be blind.** On random typical users, accuracy alone cannot separate an unlearnt model from the
original. You need several measures, and at least one that looks at each example, such as a membership attack.

**A small band will sometimes reject a good model.** In Lesson 11, SISA is exact by construction, yet it failed FORGET
on Carol by one digit. It scored 52.5% against a band starting near 52.6%. With 12 references and a 40-digit forget
set, a band of two standard deviations will now and then shut out a model that is perfectly fine. More references, a
larger forget set or a wider \(k\) reduce these false alarms, but widening the band also lets more bad models pass.
The width is a policy choice.

**It is expensive to build.** Each reference is a full training run. That is cheap for the course's small digit network,
which retrains in about a third of a second, but not for a large production model. So the band is mainly a tool for
research and audits. In production there is no band to tune a method against.

**It only covers this course's setting.** The numbers come from 8 × 8 digit images, one small network and a forget set
of 40 examples. The idea carries over to bigger models, but the width of the band will be different, and you have to
measure it again.

**It compares summaries.** The band checks an average over the whole forget set. Stronger evaluations compare the
spread of unlearnt models with the spread of retrained models example by example, as in the NeurIPS 2023 unlearning
competition (Triantafillou et al. 2024).

!!! tip "What to do in practice"
    - Build the band from at least 10 retrains with different seeds, and report how many you used.
    - Use exactly the same recipe for the references as for the model under test, including any sharding.
    - Build a band for several measures, such as forget accuracy, test accuracy and a membership attack score.
    - Fix the band's settings (the value of \(k\) and the minimum width) before you look at any results.
    - Treat a narrow miss as a reason to look closer, and check the method's own logs before you call it a failure.

## In code

```python
from mul import audit, lab, methods
L = lab.make_lab("carol")
refs = [methods.retrain(lab.model_fn, L.Xr, L.yr, seed=s, **lab.FIT)[0] for s in range(5)]
splits = dict(Xr=L.Xr, yr=L.yr, Xf=L.Xf, yf=L.yf, Xt=L.X_test, yt=L.y_test)
band_mean, band_std = audit.gold_band(refs, splits)          # mean and spread of each metric
table = audit.audit({"my method": unlearnt}, splits, refs)    # measure the method the same way
print(audit.gate(table, band_mean, band_std, k=2.0))          # PASS or FAIL per check
```

The `gate` function uses a band of the mean plus or minus the larger of \(k\) standard deviations and 3 points. It
fails a model that lands above the band and also one that lands below it.

## Common mistakes

!!! danger "Mistakes people make"
    - **Using one retrained model.** It is one roll of the dice. In Lesson 06 a single retrain could have landed
      anywhere from 47.5% to 70.0% on Carol.
    - **Aiming below the band.** Over-forgetting is a leak too. A model that does much worse on Carol than strangers
      tells an attacker that Carol was special.
    - **Building the band with a different recipe** from the model under test. The references must use the same
      architecture, sharding and training settings. In Lesson 07, references trained as one big network ranked a SISA
      model that still remembered Carol as cleaner than a truly clean one.
    - **Checking only random forget sets.** Typical data was never memorised, so the original model is already inside
      the band and passes.
    - **Tuning a method until it lands in the band.** In production you have no band to tune against, so the results
      would look better than they really are.
    - **Reading every FAIL as proof of failure.** A band from a few references will sometimes reject a good model, as
      it did with SISA on Carol.

## Key takeaways

- Retrained neural networks disagree, so "forgotten" is a range, not a number.
- Build the band from several retrains; pass only if the result lands inside it.
- The band is the mean plus or minus about two standard deviations, with a minimum width of 3 points per side.
- Landing below the band (over-forgetting) is a failure too.
- The band depends on what is forgotten. It is wide for Carol, narrow and near 100% for random users and exactly 0%
  for a whole class.
- Deterministic classical models have a band of width zero, so they can be checked for identical predictions.
- A pass is evidence, not proof, and a narrow fail can be a false alarm.

!!! note "Notes to take"
    - **Gold band.** The range of results from several models retrained without the forget set.
    - **Rule.** Band = mean ± 2 standard deviations, at least 3 points each side. Inside passes, above or below fails.
    - **Why.** Retrained networks disagree. On Carol, 20 retrains ranged from 47.5% to 70.0%.
    - **Carol's band in Lesson 06.** 62.0% ± 9.2%. Original 100.0% fails, a new retrain at 62.5% passes.
    - **Classical models.** Deterministic, so the band has width zero.
    - **Depends on the request.** Carol wide, random users near 100%, a whole class exactly 0%.
    - **Trap.** Below the band is over-forgetting, and that fails too.
    - **Trap.** Random forget sets let the original model pass on accuracy.

## Quiz

```quiz
- q: Why do we need several retrained models instead of one?
  options:
    - Retrained neural networks disagree with each other.
    - One model is too slow to train.
    - The law requires exactly five.
  answer: 0
  why: In Lesson 06, 20 identical retrains ranged from 47.5% to 70.0% on Carol's digits.
- q: An unlearnt model scores 10% on Carol, while the gold band is 62% ± 9%. What does that mean?
  options:
    - Perfect forgetting
    - Over-forgetting, which is also a failure
    - The band is wrong
  answer: 1
  why: A model that never saw Carol does much better than 10%. Being far worse is suspicious and can be detected.
- q: Why do Naive Bayes models have a band of width zero?
  options:
    - They are deterministic, so every retrain gives the same model.
    - They have no weights.
    - They cannot be retrained.
  answer: 0
  why: Without randomness in training, retraining always produces exactly the same answer.
- q: When the forget set is random typical users, where is the original model?
  options:
    - Already inside the band
    - Far above the band
    - Far below the band
  answer: 0
  why: Typical data was never memorised, so the original model already behaves like one that never saw it.
- q: When forgetting a whole class (every "3"), what is the gold band on that class?
  options:
    - About 50%
    - Exactly 0%
    - About 100%
  answer: 1
  why: A model that never saw any 3s can never predict "3".
- q: In Lesson 06 the band on Carol is 62.0% ± 9.2%. Which result passes?
  options:
    - The original model at 100.0%
    - Keeping training without her, at 95.0%
    - A new retrain with seed 999, at 62.5%
  answer: 2
  why: The band runs from 52.8% to 71.2%. Only 62.5% is inside it.
- q: Why does the course give each side of the band a minimum width of 3 points?
  options:
    - So that a band of almost zero width does not fail a good model over a single digit
    - So that every method passes more easily
    - Because a regulator sets the number
  answer: 0
  why: When retrains agree almost perfectly, the standard deviation is tiny. One of Carol's digits alone is worth 2.5 points.
- q: Accuracy on Carol varied by more than 20 points across retrains, but test accuracy varied very little. Why?
  options:
    - Carol's digits are unusual, so getting them right depends on small random details of training.
    - The test set is smaller than Carol's set.
    - The test set was used in training.
  answer: 0
  why: Every model learns typical digits well. Unusual data is where retrains disagree, and where the band is widest.
- q: SISA, which is exact by construction, missed the band on Carol by one digit in Lesson 11. What is the right reading?
  options:
    - A false alarm worth investigating, because a band from 12 references will sometimes reject a good model
    - Proof that SISA does not work
    - Proof that the band should be removed from the audit
  answer: 0
  why: Every statistical test has false alarms. SISA's exactness can be checked from its logs.
```

## Try it

- Move the diamond in the widget above, then change the number of retrains and watch how the band moves.
- In the Lesson 06 notebook, rebuild the band from 5, 10 and 20 retrains and see how stable its width is.
- Read the next concept, [Exact unlearning for classical models](exact-unlearning-classical.md).
- Run the lesson [06 · Retrain and the gold band](../lessons/06-retrain-and-the-gold-band.md).
- See how the band becomes the FORGET check in [The unlearning audit](unlearning-audit.md).
