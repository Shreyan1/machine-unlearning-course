---
title: "Lesson 12 · Right to be forgotten and fairness"
description: Erasure requests on real census data. One request is easy, but a skewed wave of requests quietly makes the model unfair.
---

# Lesson 12 · The right to be forgotten on real data, and who pays for it

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 8</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 10 minutes · 3 checkpoints"
    By the end of this lesson you can

    - serve one erasure request exactly with a Newton step and check it against a retrain,
    - show that a skewed wave of exact deletions makes a model unfair to one group while accuracy stays flat,
    - add a FAIRNESS check to the audit and fix the harm using only the retain data.

## The story

Real data is **personal**, and requests arrive **continuously and not at random**. This lesson uses the UCI Adult census
dataset (30,162 people) and an income model, a stand-in for a credit or hiring model. Forgetting one person is a privacy
question. Forgetting many people from one group becomes a **fairness** question.

Until now every request in the course was one request, on 8 × 8 digits. Here the rows are real people with ages,
incomes and marital status. Imagine a professional women's network that runs a privacy campaign, so that over one
quarter a growing share of **high-earning women** ask to be erased. Every request is lawful and must be honoured. A
drop in model quality is not a reason to refuse one. The question is who pays for the deletions, and whether anyone
would notice.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** logistic regression and measure fairness with equal opportunity (true-positive rate per group).</li>
<li markdown>**Show the issue.** One request ("Alice"), then a growing wave of requests from high-earning women.</li>
<li markdown>**Untrain** with Newton steps and exact retrains; compare with deleting random people.</li>
<li markdown>Repeat on a neural model with approximate methods, adding a **FAIRNESS** check.</li>
<li markdown>**Mitigate** with per-group thresholds fitted on retain data only.</li>
</ol>

## What each step teaches

**Train and measure.** The model is L2-regularised logistic regression solved with Newton's method, as in Lesson 02.
Fairness is measured with [equal opportunity](../start-here/glossary.md#e). Among people who really earn more than
$50K, what share does the model find, for women and for men? That share is the
[true positive rate (TPR)](../start-here/glossary.md#t). A gap already exists before anyone is deleted, because only
778 women in training earn more than $50K. This step sets the baseline every later number is compared with.

**One request, then a wave.** Removing Alice shows that a single request on a linear model is a solved problem. The
wave shows that the trouble starts when many requests share a group and a label. The two together teach that the
size and the make-up of the deletions matter, not just the method.

**Untrain and compare with random deletions.** Each wave is served by an exact retrain and by one Newton step. A random
control of the same size is the key test. If random deletions leave the women's TPR alone and skewed deletions do not,
then the harm comes from who asked.

??? deep "Go deeper · why the Newton step drifts on large waves"
    A Newton step uses a quadratic picture of the loss near the old optimum. That picture is good for small changes.
    At 116 deletions the step's largest weight error was 0.0138 and its women's TPR matched the retrain at 47.3%. At
    700 deletions the weight error was 0.7216, and the step gave a women's TPR of 21.0% against 14.1% for the retrain.
    Guo et al. (2019) handle this with an error budget, after which the system retrains. Here a retrain is about as
    cheap as one step, so the lesson's advice is simply to retrain.

**The neural model.** A small network (104 → 64 → 64 → 2) is unlearnt with the approximate methods from Lessons 08 to
10 and audited as in Lesson 11. The new check, FAIRNESS, asks whether the women's TPR lands inside the band of 12
retrained references. This step shows that a method can add a bias of its own.

**Mitigate.** Per-group thresholds are fitted after the 60% wave, on the retain data only. This step shows that the
harm can be fixed without undoing the deletions, and that the fix has a cost someone must accept.

## Key results

<div class="stats">
<div><strong>2.2 × 10⁻⁶</strong><span>weight gap between Newton removal of Alice and a retrain</span></div>
<div class="is-bad"><strong>22.8%</strong><span>women's TPR after 583 skewed deletions, from 50.6%</span></div>
<div class="is-bad"><strong>2.4%</strong><span>women's TPR after NegGrad+, a method-made bias</span></div>
<div class="is-good"><strong>53.3%</strong><span>women's TPR after per-group thresholds</span></div>
</div>

**Baseline.** Accuracy is 85.7%. The TPR is 50.6% for women and 63.5% for men, a gap of 12.9 points. Only 778 women in
training earn over $50K.

**One request.** Removing Alice with one Newton step landed within 2.2 × 10⁻⁶ of the retrained weights. Solved.

**A skewed wave** (exact retrains).

| Deleted | Accuracy | TPR women (random deletions) | TPR women (skewed deletions) | TPR gap (skewed) |
|---|---|---|---|---|
| 0 | 85.7% | 50.6% | 50.6% | 12.9 |
| 233 | 85.7% | 50.9% | 44.6% | 18.9 |
| 466 | 85.2% | 51.2% | 31.1% | 32.3 |
| 583 | 85.0% | 51.2% | 22.8% | 40.4 |

Accuracy barely moves. **Perfect unlearning faithfully reproduces whatever bias the deletions introduce.**

Read the rows as shares of the 778 high-earning women. 233 is 30%, 466 is 60% and 583 is 75%. In the random column the
women's TPR stays between 50.6% and 51.2% the whole way. In the skewed column it falls by 6 points at 30% and by almost
28 points at 75%. The gap grows from 12.9 to 40.4 points because the women's TPR falls while the men's stays at about
63.5%.

??? checkpoint "Checkpoint 1 · The 466 row shows accuracy at 85.2% and the women's TPR at 31.1%. Would an accuracy alert set to fire at a one-point drop have caught it?"
    **No.** Accuracy fell by only 0.5 points, from 85.7% to 85.2%, so the alert stays silent. Meanwhile the women's TPR
    fell by 19.5 points. High-earning women are a small share of the test rows, so even a collapse for them barely
    moves the overall average.

**Methods can add their own bias** (neural model, 233 women deleted). NegGrad+ pushed the women's TPR from 53.6% to
**2.4%**. Gradient ascent hurt everyone. Fine-tuning passed the whole gate, because tabular data is memorised far less
than Carol's digits. Random seeds alone moved the women's TPR between about 42% and 61%.

The FAIRNESS band from the 12 references was 51.8% ± 12.5%, so from 39.3% to 64.3%. Gradient ascent landed at 23.4%
and NegGrad+ at 2.4%, both far below it. NegGrad+ also widened the TPR gap from 11.1 to 44.1 points, because the women's
TPR fell much more than the men's. SCRUB and Bad Teacher stayed fair but failed FORGET, because their accuracy on the deleted
rows stayed near or above the original's.

??? checkpoint "Checkpoint 2 · NegGrad+ scored 0.4% on the 233 deleted rows and a retrained model scored 37.8%. Why is the lower score worse, not better?"
    **Because it is over-forgetting.** Models that never saw these women still get about 49% of them right (37.8% for the one retrain). Scoring 0.4%
    means the method pushed the model to be wrong about women like them, which is why the women's TPR fell to 2.4%.
    Below the band is a failure, just as above it is.

**Mitigation.** Per-group thresholds raised the women's TPR from 31.1% to 53.3%, with accuracy at 85.5%. The men's TPR
fell from 63.5% to 59.4%. That trade-off needs an owner.

The gap fell from 32.3 points to 6.1. The thresholds were fitted on the retain data only, so the fix does not quietly
re-use the 466 deleted women.

??? checkpoint "Checkpoint 3 · Fine-tuning passed the audit here but failed on Carol in Lesson 08. What should a team conclude before trusting it on a new dataset?"
    **Re-run the audit on the new data.** On the census data the original was right on 62% of the deleted rows and
    retrains on about 49%, a modest difference that two epochs of fine-tuning washed out. Carol's digits were
    memorised far more. How much a model memorised decides which methods work.

## Limits of this lesson

**One dataset, one group and one metric.** The lesson uses the census data, sex as the group and equal opportunity as
the metric. A smaller group, such as a race group in the same data, may move more. A different metric, such as the
share of each group called positive, can tell a different story.

**A simulated wave.** The skewed requests are drawn at random from the high-earning women with one fixed seed. Real
waves can be skewed in subtler ways.

**A wide band.** On the neural model seeds alone spread the women's TPR over about 19 points, so a modest real harm
could hide inside the FAIRNESS band.

**The fix is not free.** Per-group thresholds use the sensitive attribute at decision time, which some sectors
restrict. Reweighting the remaining data or other methods may be needed instead.

## Concepts used here

- [Erasure requests and fairness](../unlearning/fairness-and-erasure.md)
- [Logistic regression](../ml-basics/logistic-regression.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)

## Notes to take

!!! notes "Notes to take"
    - **Data.** UCI Adult, 30,162 people, an income model as a stand-in for credit or hiring.
    - **Fairness metric.** Equal opportunity, the TPR per group. Start 50.6% women, 63.5% men.
    - **One request.** A Newton step removed Alice to within 2.2 × 10⁻⁶ of a retrain.
    - **Skewed wave.** 583 high-earning women deleted, women's TPR 22.8%, accuracy 85.0%.
    - **Random control.** Same number deleted at random, women's TPR 51.2%. The cause is who asked.
    - **Exact is not fair.** Perfect unlearning copies the bias of the data that is left.
    - **Method-made bias.** NegGrad+ took the women's TPR to 2.4%. Add FAIRNESS to the audit.
    - **Fix.** Per-group thresholds on retain data only, women 31.1% to 53.3%, men 63.5% to 59.4%.
    - **Trap.** Judge fairness against several references, because seeds alone spread it from 42% to 61%.

## Quiz

```quiz
- q: As high-earning women were deleted, what did overall accuracy do?
  options:
    - Barely moved
    - Collapsed
    - Rose sharply
  answer: 0
  why: It stayed near 85%, so accuracy dashboards miss the problem entirely.
- q: Deleting the same number of random people changed the women's TPR by...
  options:
    - Almost nothing
    - About 30 points
    - It fell to 0%
  answer: 0
  why: Only group-skewed deletions shift the model for that group.
- q: Were the fairness drops caused by bad unlearning?
  options:
    - No; they happened with exact retraining.
    - Yes; the Newton step was wrong.
  answer: 0
  why: The model faithfully became what the remaining data says.
- q: Which method created a new, method-made bias?
  options:
    - NegGrad+
    - Exact retraining
    - Fine-tuning
  answer: 0
  why: Pushing away from a forget set of only high-earning women taught the model that such women earn less.
- q: Why did fine-tuning pass the gate here but fail on Carol in Lesson 08?
  options:
    - Tabular census data is memorised far less than Carol's digits.
    - Fine-tuning was run for longer.
    - The gate was turned off.
  answer: 0
  why: How much a model memorised decides which methods work, so re-audit for every new kind of data.
- q: Why did one Newton step stop matching the retrain on the largest wave?
  options:
    - The deleted women were not in the training set.
    - It uses a quadratic picture of the loss that is only accurate for small changes.
    - Newton steps cannot remove more than one person.
  answer: 1
  why: At 700 deletions the step was 6.9 points off on the women's TPR. An error budget tells the system when to retrain instead.
- q: Why were the per-group thresholds fitted on the retain data only?
  options:
    - The retain data is smaller, so fitting is faster.
    - The law requires thresholds to use the test set.
    - Fitting them on the deleted women would re-use the data they asked to remove.
  answer: 2
  why: A fix that tunes on erased rows puts their influence back into the system.
- q: The per-group thresholds lowered the men's TPR from 63.5% to 59.4%. What should the team do about that?
  options:
    - Hide it, because overall accuracy did not fall
    - Record the trade-off and have a named person sign it off
    - Undo the deletions instead
  answer: 1
  why: Every fairness fix has a cost. It belongs in the evidence record with the erasure log and the audit.
```

## Open question → Lesson 13

!!! levelup "Level up"
    You can now serve a wave of real erasure requests, catch the harm accuracy hides and fix it without undoing the
    deletions. Next quest, [Lesson 13 · Consent withdrawal in face recognition](13-consent-withdrawal-face-recognition.md),
    where one person is not a row but a whole class.

Here each person was one row among 21,000. What happens when a person *is* the class, as in face recognition, and they
withdraw consent?

[On to Lesson 13, consent withdrawal in face recognition :material-arrow-right:](13-consent-withdrawal-face-recognition.md){ .md-button }
