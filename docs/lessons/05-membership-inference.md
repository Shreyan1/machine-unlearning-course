---
title: "Lesson 05 · Membership inference attacks"
description: Can an outsider tell that Carol was in the training data? Build a membership inference attack, then use it as a forgetting detector.
---

# Lesson 05 · Membership inference, can an outsider tell Carol was there?

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 2 · Neural nets, the problem</span><span class="chip" markdown="span">:material-stairs-up: Rung 4</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 35 minutes · 3 checkpoints"
    By the end of this lesson you can

    - run a fair membership attack on every model from Lessons 01 to 04 and say which ones leak Carol,
    - explain why a per-example attack with shadow models sees a leak that a single threshold misses,
    - use that attack to show that retraining closes the leak.

## The story

Lesson 04 said the proof of forgetting must be about **behaviour**. Now flip the point of view. Imagine you are an outsider who
can only send inputs and read the model's probabilities. You hold some digits that may or may not have been in training.
Can you tell which ones were? That is a **membership inference attack**. It is a privacy threat, and it is also the
tool every later audit is built on.

Carol's digits are thick-marker digits, unusual enough that the network memorised them. If an outsider can tell from
the model alone that she was in the training set, the model is leaking something about her, even though it never
prints her data. And once she asks to be forgotten, the same attack becomes the check. If it can no longer pick her out
from strangers, that is the first behavioural evidence that she has gone.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the network from Lesson 04.</li>
<li markdown>**Show the issue.** Attack every model from Lessons 01 to 04 with a loss threshold.</li>
<li markdown>Build a **stronger, per-example attack** (LiRA / U-LiRA) with 8 shadow models in and 8 out.</li>
<li markdown>**Untrain** with the exact methods already known, and attack again.</li>
<li markdown>**Prove it** with the per-example test.</li>
</ol>

## What each step teaches

**Step 1. Train.** The lab has 1,257 training digits, of which Carol's 40 are the forget set, and 540 test digits. The
network is the same one that memorised her in Lesson 04, so there is a known leak to find.

**Step 2. Attack every model.** The attack compares Carol's 40 digits, which were in training, with 80 unseen
thick-marker digits, which were not. Using digits of the same style is the key design choice. Against thin-stroke
digits the attack would only learn "thick or thin" and would look strong for the wrong reason.

**Step 3. Build a sharper attack.** A single loss threshold treats every digit the same, so it cannot tell a digit
that is easy by nature from one that is easy because it was trained on. LiRA fixes this by giving each digit its own
comparison, using shadow models trained with and without Carol.

??? deep "Go deeper · how the shadow models are used in step 3"
    The attacker trains 8 networks with Carol (IN) and 8 without her (OUT), all with the same recipe as the target.
    For each of Carol's digits, it records how confident the IN models are in the right answer and fits a bell curve,
    then does the same for the OUT models. A digit is flagged "still a member" when the target model's confidence is
    more likely under the IN curve. `audit.ulira` returns the share of the 40 digits that are flagged.

    Before using it, the lesson calibrates the test on two held-out models whose answer is known. One trained with
    Carol must score high, and one trained without her must score low. The networks train in about 0.3 seconds each,
    so 16 shadow models are cheap here.

**Step 4. Untrain.** Every model is unlearnt with an exact method already known, retraining for the network and the
exact updates from Lessons 01 to 03 for the classical models. Because these are exact, the attack after unlearning
shows what "forgotten" should look like.

**Step 5. Prove it.** The per-example test runs on the network before and after retraining. This is the comparison
every later lesson uses, a method's member-rate against that of a model that never saw Carol.

## Key results

<div class="stats">
<div class="is-bad"><strong>0.96</strong><span>random forest AUC on Carol, the biggest leak</span></div>
<div><strong>0.71</strong><span>network AUC on Carol with the blunt attack</span></div>
<div class="is-bad"><strong>95%</strong><span>Carol's digits U-LiRA flags on the original network</span></div>
<div class="is-good"><strong>5%</strong><span>flagged after retraining without her</span></div>
</div>

**The blunt attack** (Carol's 40 digits against 80 unseen thick-marker digits).

| Model | AUC before | AUC after exact unlearning |
|---|---|---|
| Naive Bayes | 0.53 | 0.40 |
| k-NN, k = 5 | 0.59 | 0.46 |
| Logistic regression | 0.59 | 0.47 |
| RBF SVM | 0.66 | 0.58 |
| Random forest | 0.96 | 0.47 |
| Neural network | 0.71 | 0.48 |

On *typical* training digits against test digits, the network's AUC was only 0.53. Attacks look weak on average and
strong on the right people.

Read the table row by row. An AUC of 0.5 is a coin flip and 1.0 is always right. **Naive Bayes** starts at 0.53, a
coin flip, because it never memorised Carol. **The random forest** starts at 0.96, the clearest leak, and at 5% false
positives it flags 62.5% of her digits. **The network** reads 0.71, which looks like a moderate leak, and at 5% false
positives it flags only 2.5%, about one digit. After exact unlearning every model sits between 0.40 and 0.58. Her
digits and the comparison digits are now all strangers to the model, so what is left is noise from a small test.

The order matches Lesson 04's memorisation gap, the difference between a model's accuracy on Carol and on unseen
digits like hers. The forest had the largest gap, at 30.0 points, and Naive Bayes had none. The match is not perfect.
Logistic regression had a gap of 15.0 points yet reads only 0.59, which shows that one threshold is a blunt tool.

??? checkpoint "Checkpoint 1 · Logistic regression memorised Carol in Lesson 04 but reads only AUC 0.59 here. Does that mean it does not leak her?"
    **No.** It means this attack is too blunt to see the leak. A single loss threshold mixes digits that are easy by
    nature with digits that are easy because they were trained on. A low score from a weak attack is not a clean bill
    of health. The network shows the same thing, at 0.71 here and 95% with the sharper test.

**The per-example attack (U-LiRA).** It was calibrated first. A fresh model trained **with** Carol scored 0.97; one
**without** her scored 0.05. On the original network it flagged **95%** of Carol's digits as members; after retraining,
**5%**. The blunt attack had reached only AUC 0.71 on the same network.

In counts, 95% of her 40 digits is 38 and 5% is 2. The calibration matters as much as the result. It shows the test
gives a high score when the answer is known to be yes and a low one when it is known to be no, so its reading on the
original network can be trusted.

??? checkpoint "Checkpoint 2 · After some unlearning method, U-LiRA flags 40% of Carol's digits. Has the method done its job?"
    **No.** A model that never saw Carol scores about 5%, which is 2 of her 40 digits. 40% is 16 of them, so the test
    still sees many of her digits as members. The method has moved away from the original's 95% but has not reached
    the target.

!!! warning "Three cautions for later"
    1. Shadow models must use the **same training recipe** as the target (Lesson 07 shows what goes wrong otherwise).
    2. AUC near 0.5 only means *this* attack found nothing.
    3. AUC far **below** 0.5 is a red flag too, because the forgotten data is treated worse than strangers.

## Limits of this lesson

**Small numbers.** The test uses 40 members and 80 non-members, so one digit moves the true-positive rate by 2.5
points and AUC values wobble around 0.5 even when nothing leaks.

**Two attacks only.** The lesson uses a loss threshold and U-LiRA. Stronger attacks exist (Hayes et al. 2024), so a
pass here is evidence, not proof.

**Cheap shadow models.** Training 16 shadow networks takes seconds here. For a large model each one is a full training
run, which is why real audits use fewer and must say how many.

**One person.** Carol is unusual by design. On typical users the same network leaks almost nothing, so the lesson
shows the worst case, not the average one.

??? checkpoint "Checkpoint 3 · A team runs the blunt attack on random training digits, gets AUC 0.53 and declares the model private. What did they miss?"
    **They aimed at the wrong people.** Typical digits are learnt, not memorised, so they hardly leak, and the same
    network also scored 0.53 on them here. The leak is concentrated on unusual people such as Carol, where U-LiRA
    flagged 95% of her digits.

## Concepts used here

- [Membership inference attacks](../unlearning/membership-inference-attacks.md)
- [Loss functions](../ml-basics/loss-functions.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)

## Notes to take

!!! notes "Notes to take"
    - **Fair test.** Carol's 40 digits against 80 unseen thick-marker digits, so style cannot give the answer away.
    - **Clue.** Lower loss on an example suggests it was in training.
    - **Who leaks.** Forest AUC 0.96, network 0.71, Naive Bayes 0.53, which follows Lesson 04's memorisation gap.
    - **Strict score.** At 5% false positives the forest flags 62.5% of her digits and the network only 2.5%.
    - **Averages hide risk.** Typical digits give AUC 0.53 on the same network.
    - **U-LiRA.** Per-example test with 8 IN and 8 OUT shadow models. Calibrated at 0.97 with Carol and 0.05 without.
    - **Result.** Original network 95% flagged, retrained 5%.
    - **Trap.** A blunt attack's low score is not proof of privacy, and AUC far below 0.5 is a red flag.

## Quiz

```quiz
- q: What clue does the simple attack use?
  options:
    - Lower loss on an example suggests it was in training.
    - The size of the model file
    - The colour of the image
  answer: 0
  why: Models are usually more confident on examples they trained on.
- q: Which model leaked Carol's membership most to the blunt attack?
  options:
    - Naive Bayes
    - Random forest
    - Logistic regression
  answer: 1
  why: The forest's AUC was 0.96; Naive Bayes, which did not memorise her, was 0.53.
- q: On the original network, what share of Carol's digits did U-LiRA flag as members?
  options:
    - About 5%
    - About 50%
    - About 95%
  answer: 2
  why: The per-example test is much sharper than a single loss threshold.
- q: What happened to U-LiRA's member-rate after retraining without Carol?
  options:
    - It fell to about 5%.
    - It stayed at 95%.
    - It rose to 100%.
  answer: 0
  why: The retrained model looks like a model that never met her, from the attacker's view.
- q: Why must members and non-members come from the same kind of data?
  options:
    - Otherwise the attack learns the style (thick or thin) instead of membership.
    - It makes the test faster.
    - The library requires it.
  answer: 0
  why: A fair test compares like with like.
- q: The network reads AUC 0.71 on the blunt attack but U-LiRA flags 95% of Carol's digits. Why the difference?
  options:
    - U-LiRA uses more test digits.
    - One threshold cannot tell naturally easy digits from memorised ones, while U-LiRA judges each digit on its own.
    - The blunt attack was run on a different network.
  answer: 1
  why: Shadow models give each digit its own IN and OUT curves, so an easy digit no longer fools the test.
- q: Why does the lesson test U-LiRA on a fresh model with Carol and one without her first?
  options:
    - To make the shadow models train faster
    - To pick a better threshold for the blunt attack
    - To check the detector gives the right answer when the answer is already known
  answer: 2
  why: They scored 0.97 and 0.05. Only a calibrated detector can be trusted on a model whose answer is unknown.
- q: On typical training digits the network's AUC was 0.53. What does that teach?
  options:
    - Privacy risk sits mostly on unusual data, so attacks must be aimed at the right people.
    - The network did not learn typical digits.
    - Membership attacks never work on networks.
  answer: 0
  why: Typical digits are learnt, not memorised. The same network leaked Carol strongly.
```

## Open question → Lesson 06

!!! levelup "Level up"
    You now own a forgetting detector and know how to calibrate it. Next quest,
    [Lesson 06 · Retrain and the gold band](06-retrain-and-the-gold-band.md), where you find out how wide the target
    really is.

The gold standard so far has been "**the** retrained model". But two networks trained on identical data land in
different places, and we just used eight of them as shadow models. What exactly is the target, and how wide is it?

[On to Lesson 06, retrain and the gold band :material-arrow-right:](06-retrain-and-the-gold-band.md){ .md-button }
