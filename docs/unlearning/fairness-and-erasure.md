---
title: Erasure requests and fairness
description: When the people who ask to be deleted come mostly from one group, even perfect unlearning can make a model unfair to that group.
---

# Erasure requests and fairness

This is a **Responsible AI** problem as well as a privacy problem. A system must honour individual requests while
checking whether the resulting model treats groups fairly.

!!! oneline "In one line"
    When deletion requests come mostly from **one group**, even perfect unlearning can quietly make the model unfair to
    that group, and accuracy dashboards will not notice.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why a wave of lawful, exact deletions can make a model unfair to one group,
    - read a per-group true-positive rate and spot a collapse that accuracy hides,
    - tell a bias that comes from the data from a bias that the unlearning method adds,
    - choose a fix that uses only the retain data and say who must sign it off.

## Why it matters

Forgetting one person is a privacy question. Forgetting *many* people, if they are mostly from one group, becomes a
**fairness** question. Under GDPR Art. 17 people can ask for their personal data to be erased "without undue delay",
with some exceptions. A drop in model quality is not a reason to refuse an erasure request. But you can, and for
high-risk systems arguably must, **monitor and fix** the effect. The EU AI Act sets data-governance rules for
high-risk AI. The income model here stands in for a credit or hiring model.

The danger is that nothing looks wrong. Each request is lawful and tiny, so no single change review would flag it.
And requests are **not random**. A privacy campaign in one community can tilt them towards one group, and standard
monitoring, which tracks overall accuracy, will not see the result.

## A simple example

A school bases next year's plans on who attends this year. If most of the girls who excel at maths leave, the school's
records will suggest that girls rarely excel at maths, and it may plan fewer advanced classes for them. Nothing in the
records is wrong. The data that is left just tells a skewed story.

!!! simply "Explain it simply"
    A model learns from whoever is left in the data. If the people who leave are mostly high-earning women, the model
    ends up believing that women rarely earn much. Deleting them perfectly does not help, because "perfect" means
    "exactly what you would learn from the people who stayed".

Now map the picture onto Lesson 12. The school's records are the **income model**. The girls who excel are the
**women who earn more than $50K**. The advanced classes are the **positive predictions**, such as a higher credit limit
or a hiring shortlist. The skewed plan is the model's **lower true-positive rate for women**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [True positive rate (TPR)](../start-here/glossary.md#t) | Among people who really are positive, the share the model calls positive | The model finds 50.6% of the women who earn more than $50K |
| [Equal opportunity](../start-here/glossary.md#e) | A fairness rule that asks for the same TPR in every group | Women 50.6% and men 63.5% before any deletion, so not yet equal |
| TPR gap | The men's TPR minus the women's TPR, in points | 12.9 points at the start, 40.4 points after 583 skewed deletions |
| Selection rate | The share of a group the model calls positive at all | 7.6% of women and 26.1% of men before any deletion |
| Skewed wave | Many requests that come mostly from one group and one label | A growing share of the 778 high-earning women in training ask to leave |
| Random control | The same number of deletions, chosen at random from everyone | 583 random people deleted, and the women's TPR stayed at 51.2% |
| Method-made bias | Unfairness added by the unlearning method itself, on top of what the data does | NegGrad+ pushed the women's TPR to 2.4% |
| Post-processing | A fix applied to the model's outputs after training, such as a different threshold per group | fairlearn's `ThresholdOptimizer` in Lesson 12 |

## How it works

<!-- diagram: fairness-and-erasure -->

The figure shows the women's TPR before any deletion, after 583 random deletions and after 583 deletions of
high-earning women, each followed by a retrain. Only the last bar collapses, while overall accuracy barely moves.

Lesson 12 uses the **UCI Adult census data** (30,162 people) and an income model, a stand-in for a credit or hiring
model. The lesson trains on 70% of the people, about 21,100. Fairness is measured with **equal opportunity**. Among
people who really earn more than $50K, how often does the model say so (the true-positive rate, TPR), for women and
for men? A credit or hiring model with a lower TPR for women turns down qualified women more often.

### Before any deletions

- Accuracy is 85.7%. The TPR for women is 50.6% and for men 63.5%, a gap of 12.9 points that comes from the data.
- Only about 11% of women in the training set earn more than $50K, against about 31% of men.
- Only **778 women** in the training set earn more than $50K. Keep that number in mind, because every wave below is
  a share of it.

The model is L2-regularised logistic regression solved with Newton's method, the same kind as in
[Exact unlearning for classical models](exact-unlearning-classical.md). It trains in 49 ms.

### One request is easy

"Alice", a high-earning woman, asks to be erased. One Newton step lands essentially on the retrained model (weight
difference 2.2 × 10⁻⁶). For one request, this is a solved problem.

For scale, Alice's data moves the weights by only 2.9 × 10⁻³ in the first place. One person in about 21,000 barely
moves a well-regularised linear model.

### A wave of requests is not

Suppose a growing share of **high-earning women** ask to be deleted. As a control, the same number of random people
are deleted.

| People deleted | Accuracy (skewed) | TPR women (random) | TPR women (skewed) |
|---|---|---|---|
| 0 | 85.7% | 50.6% | 50.6% |
| 233 | 85.7% | 50.9% | 44.6% |
| 466 | 85.2% | 51.2% | 31.1% |
| 583 | 85.0% | 51.2% | 22.8% |

Accuracy barely moves. The women's TPR collapses. And these are **exact** retrains. Perfect unlearning faithfully reproduces whatever bias the deletions introduce.

Read the table row by row. 233 is 30% of the 778 high-earning women, 466 is 60% and 583 is 75%. With 233 random people
gone, the women's TPR is 50.9%, the same as before. With 233 high-earning women gone, it is 44.6%. At 583 skewed
deletions it is 22.8%, so the model now finds fewer than one in four of the high-earning women in the test set.

The men's TPR does not move. It is the women's TPR plus the gap, which gives 63.5% at the start and still about 63.5%
after 583 skewed deletions (22.8 + 40.4 = 63.2). So the whole collapse falls on one group.

Nothing is wrong with the unlearning. The model became the one you would have trained on the data that is left, and
that data now says high-earning women barely exist.

??? deep "Go deeper · the certificate, and when one Newton step stops being enough"
    For Alice, the lesson checks the certificate from Guo et al. (2019). At the exact retrained model, the gradient of
    the retain loss is zero. For the original model it is 2.18. After the Newton step it is 1.49 × 10⁻³, close to zero.
    The model's belief that Alice earns more than $50K goes from 0.3180 to 0.3163, the same as the retrained model.

    The lesson served every wave twice, once by exact retraining and once by one Newton step from the original model.
    The Newton step uses a quadratic picture of the loss near the old optimum, so it is only accurate for small
    changes. The table gives the largest weight difference from the exact retrain and the women's TPR for both.

    | Deleted | Weight error of the Newton step | TPR women, Newton step | TPR women, exact retrain |
    |---|---|---|---|
    | 116 | 0.0138 | 47.3% | 47.3% |
    | 233 | 0.0401 | 44.9% | 44.6% |
    | 466 | 0.1811 | 31.7% | 31.1% |
    | 583 | 0.2700 | 25.8% | 22.8% |
    | 700 | 0.7216 | 21.0% | 14.1% |

    For small batches the two agree. At 700 deletions, which is 90% of the high-earning women, the Newton step is 6.9
    points away on the women's TPR. This is why Guo et al. (2019) keep an **error budget**. Each removal spends some of
    it, and when it runs out the system retrains from scratch. At this model's size a retrain costs about as much as
    one Newton step, so the honest advice in Lesson 12 is simply to retrain.

??? checkpoint "Checkpoint 1 · After 583 skewed deletions the dashboard shows accuracy at 85.0%, down from 85.7%. Is the model still fine for women?"
    **No.** Accuracy fell by only 0.7 points, but the women's TPR fell from 50.6% to 22.8%, a drop of 27.8 points.
    The model now misses about 77 in every 100 high-earning women (100 − 22.8 = 77.2). Women who earn more than $50K
    are a small share of all test rows, so a collapse for them hardly moves the overall average. Only a per-group
    metric shows it.

### Some methods add their own bias

With a neural model and 233 deleted women, **NegGrad+** pushed the women's TPR from 54% to about **2%**. It did not just
remove 233 people. It taught the model that *women like them* earn less. That is a new, **method-made bias**. Plain
fine-tuning, by contrast, passed every check here, because tabular data is memorised far less than Carol's digits.

Why does this happen? [Gradient ascent](../start-here/glossary.md#g) and [NegGrad+](../start-here/glossary.md#n) push
the model to be *wrong* on the forget set. Here every row of the forget set is "a woman who earns more than $50K".
Being wrong on those rows sounds a lot like "predict that women earn less". The method cannot tell the person from the
group they belong to.

The neural model is a small network (104 inputs, two hidden layers of 64, two outputs). The lesson audits each method as
in [The unlearning audit](unlearning-audit.md) and adds one more check, **FAIRNESS**. The women's TPR must land inside
the band of 12 retrained references, the same way forget accuracy must.

Gradient ascent hurt everyone. Both TPRs fell by 20 to 30 points. NegGrad+ was more specific and worse. The women's
TPR fell from 53.6% to 2.4% while the men's fell by about 18 points, so the gap quadrupled from 11.1 to 44.1 points.
Without the FAIRNESS column, the audit would have flagged NegGrad+ for over-forgetting and for losing three points of
test accuracy, but not for the harm to women.

??? deep "Go deeper · the full audit of the neural model"
    The FAIRNESS band is 51.8% ± 12.5%, so a women's TPR between 39.3% and 64.3% passes. It is wide because the seed
    alone moved the women's TPR of a retrained model between about 42% and 61%. A fairness number from one model is a
    sample, just like forget accuracy in [The gold band](gold-band.md).

    | Method | Forget accuracy | Test accuracy | TPR women | FORGET | PRIVACY | UTILITY | FAIRNESS | Verdict |
    |---|---|---|---|---|---|---|---|---|
    | Original | 62.2% | 85.5% | 53.6% | fail | fail | ok | ok | FAIL |
    | Retrain | 37.8% | 85.5% | 45.5% | ok | ok | ok | ok | PASS |
    | Fine-tune | 52.8% | 85.4% | 47.0% | ok | ok | ok | ok | PASS |
    | Gradient ascent | 24.9% | 83.4% | 23.4% | fail | ok | fail | fail | FAIL |
    | NegGrad+ | 0.4% | 82.5% | 2.4% | fail | ok | fail | fail | FAIL |
    | SCRUB | 61.4% | 85.4% | 51.8% | fail | fail | ok | ok | FAIL |
    | Bad Teacher | 68.7% | 85.2% | 59.6% | fail | fail | ok | ok | FAIL |

    SCRUB and Bad Teacher stayed fair but did not forget. Their forget accuracy stayed near the original's, so they
    failed FORGET and PRIVACY. NegGrad+ forgot far too much, 0.4% on the deleted rows, which is
    [over-forgetting](../start-here/glossary.md#o) and a group-level harm at the same time.

    Fine-tuning passed because tabular data is memorised far less than digits. The original model was right on 62% of
    the 233 deleted rows, and models that never saw them were right on about 49%. Two epochs of training on the retain
    data washed out that modest difference, the opposite of what happened with Carol in Lesson 08.

??? checkpoint "Checkpoint 2 · The FAIRNESS band is 39.3% to 64.3%. Bad Teacher scored 59.6% on women's TPR and gradient ascent 23.4%. Which passes FAIRNESS, and does that one pass the audit?"
    **Bad Teacher passes FAIRNESS, but it still fails the audit.** 59.6% is inside the band and 23.4% is far below
    it. Passing one check is not enough. Bad Teacher's forget accuracy stayed at 68.7%, above the original's 62.2%,
    so it failed FORGET and PRIVACY. Every check must pass for a method to pass.

### Fixing it

Per-group decision thresholds (fairlearn's `ThresholdOptimizer`), fitted only on the retain data, brought the women's
TPR back from 31.1% to 53.3%, at no cost in accuracy. The men's TPR dropped about four points, a trade-off someone has
to own. Some sectors restrict using the sensitive attribute at decision time, so reweighting or other methods may be
needed instead.

The fix works on the model's outputs. The model gives each person a score, and normally anyone above one cut-off is
called positive. Post-processing chooses a separate cut-off for each group so that the TPRs match. It needs no
retraining, so it does not undo the unlearning. Lesson 12 applied it after the 60% wave, served by an exact retrain.

| Model | Accuracy | TPR women | TPR men | TPR gap |
|---|---|---|---|---|
| Original, no deletions | 85.7% | 50.6% | 63.5% | 12.9 |
| After the 60% wave, exact retrain | 85.2% | 31.1% | 63.5% | 32.3 |
| Plus per-group thresholds | 85.5% | 53.3% | 59.4% | 6.1 |

The thresholds are fitted **without the deleted people**. Using their rows to tune the fix would quietly re-use the
data they asked to remove.

!!! tip "Add FAIRNESS to the audit"
    Track a per-group metric across the deletion log, and judge it against **several** retrained references. In
    Lesson 12, random seeds alone moved the women's TPR between about 42% and 61%.

??? checkpoint "Checkpoint 3 · A colleague wants to fit the new thresholds on the full original training data, including the 466 deleted women, because it is more data. What do you say?"
    **No, use the retain data only.** Those 466 women asked to be erased. Tuning the fix on their rows would put their
    influence straight back into the system. Lesson 12 fitted the thresholds on the retain data and still raised the
    women's TPR from 31.1% to 53.3%.

## A worked example

Follow one quarter's deletion log, with each batch served by an exact retrain. Say the team acts when the women's TPR
falls more than 5 points below its start of 50.6%. That rule is only an example, not a legal number.

1. **The start.** Accuracy 85.7%, women's TPR 50.6%, men's 63.5%. No requests yet.
2. **116 requests, 15% of the high-earning women.** Accuracy 85.5%, women's TPR 47.3%. That is 3.3 points down, so no
   alert yet.
3. **233 requests, 30%.** Accuracy 85.7%, women's TPR 44.6%. That is 6.0 points down, so the alert fires. Accuracy
   is exactly where it started, which is why only the per-group metric could raise the alarm.
4. **Look at the cause.** A random control of the same size leaves the women's TPR at 50.9%. So the drop comes from who
   asked, not from a fault in the retrain.
5. **No action taken, 466 requests, 60%.** Women's TPR 31.1%, a gap of 32.3 points. This is what happens if the alert
   is ignored.
6. **The fix.** The per-group thresholds from [Fixing it](#fixing-it) bring the women's TPR to 53.3%. Someone named
   in the procedure signs off the four points the men lose.
7. **The record.** The erasure log, the fairness metric over time and the fix go into the same evidence record as the
   unlearning audit, and into the model card.

Every request was honoured in full. None was refused or delayed because of its effect on the model.

## What the lesson found

<div class="stats">
<div><strong>85.0%</strong><span>accuracy after 583 skewed deletions, almost unchanged</span></div>
<div class="is-bad"><strong>22.8%</strong><span>women's TPR after the same deletions, down from 50.6%</span></div>
<div class="is-bad"><strong>2.4%</strong><span>women's TPR after NegGrad+, a method-made bias</span></div>
<div class="is-good"><strong>53.3%</strong><span>women's TPR after per-group thresholds on retain data</span></div>
</div>

Read the tiles in order. The shift is invisible to accuracy, severe for one group and worse with the wrong method,
and a fix that respects the deletions exists.

## Limits

**One dataset and one attribute.** The lesson uses one census dataset, one income label and sex as the group. The
notebook suggests repeating it by race. A smaller group may move even more, because each deletion is a larger share
of it.

**One fairness metric.** Equal opportunity looks only at people who really are positive. Other metrics, such as the
selection rate, can tell a different story. After the 60% wave the share of women called positive fell from 7.6% to
4.2%, and the fix brought it to 8.2%.

**A wide band on neural models.** Seeds alone moved the women's TPR between about 42% and 61%. A real but modest shift
could hide inside that band, so the FAIRNESS check catches large harms more easily than small ones.

??? deep "Go deeper · two more limits"
    **A simulated wave.** The skewed requests are drawn at random from the high-earning women with one fixed seed. Real
    requests can be skewed in less obvious ways, for example by age and income together.

    **The fix has costs of its own.** Per-group thresholds use the sensitive attribute when each decision is made,
    which some sectors restrict. They also lowered the men's TPR by about four points. They correct the outputs, not
    the fact that the remaining data has fewer high-earning women.

## What to do in practice

!!! tip "What to do in practice"
    - Log every erasure request with the groups it touches, so you can see a wave forming.
    - Track at least one per-group metric, such as the TPR, after every retrain or unlearning step, not just accuracy.
    - Compare each skewed batch with a random control of the same size, to tell a data effect from a fault.
    - Prefer exact methods, or methods that pass the full audit, when the forget set is mostly one group.
    - Keep an error budget for Newton-style removals, and retrain when it runs out.
    - Fit any fix on the retain data only, and record who chose the trade-off and why.
    - Re-run the audit on every new kind of data. How much a model memorises decides which methods work.

## In code

??? deep "Go deeper · the per-group metric and the fix in Lesson 12"
    ```python
    from fairlearn.metrics import MetricFrame, true_positive_rate
    from fairlearn.postprocessing import ThresholdOptimizer

    def tpr_by_group(pred):
        return MetricFrame(metrics=true_positive_rate, y_true=y_test, y_pred=pred,
                           sensitive_features=m_test.sex).by_group

    exact = classical.LogisticNewton(lam=1.0).fit(X_train[keep], y_train[keep])   # exact retrain
    print(tpr_by_group(exact.predict(X_test)))                                     # women and men

    post = ThresholdOptimizer(estimator=Prefit(exact), constraints="true_positive_rate_parity",
                              prefit=True, predict_method="predict_proba")
    post.fit(X_train[keep], y_train[keep], sensitive_features=m_train.sex.values[keep])   # retain data only
    ```

    `keep` holds the indices of the people who stayed, and `Prefit` is a small wrapper in the notebook that lets
    fairlearn use a model that is already trained.

## Common mistakes

!!! danger "Mistakes people make"
    - **Watching only accuracy.** It did not move while the women's TPR collapsed.
    - **Assuming exact unlearning is fair.** It reproduces the bias of the remaining data.
    - **Using "push away" methods on a one-group forget set.** They can create new bias.
    - **Judging fairness from one model.** Seeds alone moved the women's TPR by almost 20 points.
    - **Tuning the fix on the deleted rows.** That re-uses the data people asked to remove.
    - **Refusing or delaying requests to protect the model.** A drop in quality is not a reason to refuse.

## Key takeaways

!!! notes "Notes to take"
    - **The issue.** Erasure requests are not random, and group-skewed deletions shift the model for that group.
    - **Baseline.** Accuracy 85.7%, women's TPR 50.6%, men's 63.5%, only 778 high-earning women in training.
    - **One request.** A Newton step removed Alice to within 2.2 × 10⁻⁶ of the retrained weights.
    - **A wave.** 583 skewed deletions dropped the women's TPR to 22.8%, while accuracy stayed at 85.0%.
    - **Control.** The same number of random deletions left the women's TPR at 51.2%.
    - **Exact is not fair.** Perfect unlearning copies the bias of the data that is left.
    - **Method-made bias.** NegGrad+ pushed the women's TPR to 2.4% on top of the data effect.
    - **Audit.** Add FAIRNESS, judged against several references, because seeds alone spread it from 42% to 61%.
    - **Fix.** Per-group thresholds on retain data only took the women's TPR from 31.1% to 53.3%.
    - **Trap.** Every fix has a cost, here about four points of the men's TPR, and someone must own it.

## Quiz

```quiz
- q: Why can erasure requests become a fairness problem?
  options:
    - The people who ask may come mostly from one group.
    - Erasure always deletes the test set.
    - Fairness metrics cannot be computed after deletion.
  answer: 0
  why: If the data that remains under-represents a group, the model learns a skewed picture of it.
- q: As high-earning women were deleted, what happened to overall accuracy?
  options:
    - It barely moved.
    - It collapsed.
    - It went up sharply.
  answer: 0
  why: Accuracy stayed near 85%, which is why accuracy monitoring misses the problem.
- q: Were the fairness drops caused by a faulty unlearning method?
  options:
    - No; they happened with exact retraining too.
    - Yes; exact retraining is biased.
  answer: 0
  why: Exact unlearning faithfully gives the model you would train on the data that is left.
- q: What did NegGrad+ do to the women's true-positive rate?
  options:
    - Pushed it down to about 2%, creating a new bias
    - Raised it to 90%
    - Left it unchanged
  answer: 0
  why: Pushing away from a forget set made only of high-earning women taught the model that such women earn less.
- q: What data should a fairness fix use after unlearning?
  options:
    - Only the retain data
    - The deleted people's data
    - The test set labels
  answer: 0
  why: Using the deleted people's data would quietly re-use what they asked to remove.
- q: Why did the lesson also delete the same number of random people?
  options:
    - To check whether the drop came from who asked rather than from the deletion process
    - To make the model train faster
    - Because the law asks for a random sample
  answer: 0
  why: With 583 random deletions the women's TPR stayed at 51.2%. Only the skewed deletions moved it, so the cause is who asked.
- q: Why did plain fine-tuning pass the whole audit on the census data?
  options:
    - The deleted women were modestly memorised, so a little training on the retain data washed out their influence.
    - Fine-tuning ran for many more epochs than other methods.
    - The census data has no personal information.
  answer: 0
  why: The original was right on 62% of the deleted rows against about 49% for retrains. Tabular data is memorised far less than Carol's digits.
- q: After the 60% wave, per-group thresholds raised the women's TPR to 53.3%. What did it cost?
  options:
    - Nothing at all for anyone
    - About four points of the men's TPR
    - About ten points of overall accuracy
  answer: 1
  why: Accuracy stayed at 85.5%, but the men's TPR fell from 63.5% to 59.4%. A trade-off like this needs a named owner.
- q: A single retrained network has a women's TPR of 45%. Is that enough to judge whether a method is fair?
  options:
    - Yes, one reference is the exact target.
    - Only if the network was trained for longer.
    - No, because seeds alone moved the women's TPR between about 42% and 61%.
  answer: 2
  why: A fairness number from one model is a sample. Judge it against a band from several retrained references.
```

## Try it

!!! levelup "Level up"
    You can now spot a deletion wave that hurts one group, tell a data effect from a method-made bias and fix it with
    retain data only. Next quest, [Consent and face recognition](consent-and-face-recognition.md), where one person is
    not a row but a whole class.

- Read the next concept, [Consent and face recognition](consent-and-face-recognition.md).
- Run the lesson [12 · Right to be forgotten and fairness](../lessons/12-right-to-be-forgotten-and-fairness.md).
- In the Lesson 12 notebook, skew the requests by race instead of sex and see which group's TPR moves.
