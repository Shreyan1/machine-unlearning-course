---
title: Membership inference attacks
description: A membership inference attack guesses whether a person's data was used to train a model. It is both a privacy threat and an audit tool.
---

# Membership inference attacks

!!! oneline "In one line"
    A **membership inference attack** (MIA) tries to tell, just by asking the model questions, whether a particular
    person's data was in its training set.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain the clue a membership attack uses and why it works best on unusual people,
    - read an attack's AUC and its true-positive rate at a low false-positive rate, and say which one shows real danger,
    - explain how shadow models turn the attack into the course's forgetting detector, U-LiRA.

## Why it matters

The idea was introduced by Shokri et al. (2017), and it is now the standard way to test what a model leaks.

It matters twice over.

1. **As a threat.** If an attacker can tell that your medical record trained a hospital's model, the model is leaking
   private information, even if it never prints your record.
2. **As an audit tool.** If, *after* unlearning, the attack can no longer tell Carol's digits from digits that were
   never in training, that is behavioural evidence that she is forgotten.

The second use is why this page sits at the start of the course's checking tools. A neural network has no single
weight that belongs to Carol, so you cannot look inside it and point at her. What you can do is watch how the model
behaves on her digits. A membership attack is a careful, repeatable way of watching, and the PRIVACY check in
[the unlearning audit](unlearning-audit.md) is built on it.

## A simple example

!!! simply "Explain it simply"
    A model tends to be extra confident about things it studied, the way you answer a question you have seen before
    faster than a new one. A membership attack watches for that extra confidence. If the model is suspiciously sure
    about Carol's digits, it probably trained on them.

A quiz-show contestant answers some questions instantly and confidently, and hesitates on others. You might guess that
the instant answers are ones they had practised before. A model behaves the same way, because it is usually **more confident on
examples it trained on**. The attacker uses that confidence as a clue.

Now map the picture onto the course. The contestant is the **model**. The practised questions are the **members**,
Carol's 40 digits that were in training. The new questions are the **non-members**, 80 thick-marker digits the model
never saw. The attacker's guess is a **membership attack**. The trap is a contestant who is simply good at easy
questions. Speed alone cannot tell "practised" from "easy", and that is the weakness the stronger attack fixes.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Member | An example that was in the model's training data | Carol's 40 digits, for the original model |
| Non-member | An example that was not, chosen to look like the members | 80 unseen thick-marker digits |
| [Loss](../ml-basics/loss-functions.md) | How surprised the model is by the right answer. Low loss means it was confident and right | The original network has very low loss on Carol's digits |
| [AUC](../start-here/glossary.md#a) | How well an attack separates members from non-members. 0.5 is a coin flip, 1.0 is always right | 0.96 for the random forest on Carol |
| [True positive rate](../start-here/glossary.md#t) at 5% false positives | The share of members the attack flags while wrongly flagging only 5% of non-members | 62.5% for the forest, 2.5% for the network |
| [Shadow model](../start-here/glossary.md#s) | A model the attacker trains, with or without an example, to see how such models score it | 8 trained with Carol and 8 without in Lesson 05 |
| [LiRA / U-LiRA](../start-here/glossary.md#l) | Per-example tests that compare the model with shadow models trained with and without each example | U-LiRA flagged 95% of Carol's digits on the original network |
| Member-rate | U-LiRA's result, the share of the forget set it judges "still a member" | 0.05 after retraining without Carol |

## How it works

<!-- diagram: membership-inference-attacks -->

The figure shows two humps. The yellow hump is how confident the model is on examples it never saw, and the blue hump
is how confident it is on examples it trained on. The attacker draws a cut-off and calls everything to the right of
it a member. When the humps sit far apart, the attack works. When they overlap, it is close to guessing.

### The simple attack (a loss threshold)

<ol class="steps" markdown>
<li markdown>Ask the model about a digit and look at its [loss](../ml-basics/loss-functions.md) on the right answer, i.e. how surprised it is.</li>
<li markdown>Guess "member" when the loss is low, "non-member" when it is high.</li>
<li markdown>Score the attack with **AUC** (0.5 is a coin flip, 1.0 is always right) and the **true-positive rate at a low
false-positive rate**, which measures how many members the attack can flag *confidently*.</li>
</ol>

The test must compare members with **non-members from the same kind of data**. For example, we compare Carol's 40 digits
(members) against 80 unseen thick-marker digits (non-members). Otherwise the attack just learns "thick or thin".

| Model | AUC | True positives at 5% false positives |
|---|---|---|
| Naive Bayes | 0.53 | 5.5% |
| k-NN, k = 5 | 0.59 | 8.2% |
| Logistic regression | 0.59 | 2.5% |
| RBF SVM | 0.66 | 15.0% |
| Random forest | 0.96 | 62.5% |
| Neural network | 0.71 | 2.5% |

Flexible models that memorised Carol leak her membership. On *typical* digits, the network's AUC was only 0.53. Privacy
risk is concentrated on unusual data, **averaged over everyone, attacks look weak; aimed at the right people, they are
strong.**

The two columns answer different questions. AUC looks at every possible cut-off and asks how well the attack ranks
members above non-members overall. The second column fixes one strict cut-off. With 80 non-members, 5% false
positives means the attack may wrongly accuse only 4 strangers. At that setting the forest still flags 62.5% of
Carol's digits, about 25 of her 40, which is a real leak. The network flags only 2.5%, about one digit.

This table also matches Lesson 04's memorisation gap, which compared each model on Carol's digits and on unseen digits
like hers. The forest had the largest gap, at 30.0 points, and leaks most here. Naive Bayes had no gap at all and is
close to a coin flip.

??? deep "Go deeper · what AUC really measures"
    Pick one member and one non-member at random. The AUC is the chance that the attack gives the member the higher
    "member" score. So 0.5 means the attack ranks them no better than a coin, 1.0 means it always ranks the member
    first, and a value far below 0.5 means it reliably ranks the *non-member* first.

    AUC is an average over every cut-off, including loose ones where the attacker would accuse many innocent people.
    Carlini et al. 2022 argue that a real attacker cares about the strict end, where every accusation counts. That is
    why the course always reports the true-positive rate at 5% false positives next to AUC. The network's AUC of 0.71
    looks like a moderate leak, yet at the strict end it flags just one of Carol's digits.

??? checkpoint "Checkpoint 1 · The network's loss attack reads AUC 0.71, but at 5% false positives it flags only 2.5% of Carol's digits. Is Carol's membership safe?"
    **No.** The blunt attack is weak, not the leak. One threshold for every digit cannot tell a digit that is easy by
    nature from one that is easy because it was trained on. Lesson 04 showed the network memorised her, with a gap of
    22.5 points, and the per-example test below flags about 95% of her digits on the same network.

### The stronger attack (per-example likelihood ratios (LiRA))

Some digits are naturally easy, and a single threshold cannot tell "easy" from "easy because it was trained on". **LiRA**
(Carlini et al. 2022) asks three questions for each example separately. How do models that *trained on* it usually score it? How do models that *did not* score it? Which of the two does the target model look like?

The attacker trains **shadow models**, some with the example and some without. The course version, **U-LiRA** (Hayes et al. 2024), gives the
share of \(D_f\) judged "still a member".

The method has four steps.

1. **Train shadow models.** In Lesson 05 these are 8 networks trained with Carol (IN) and 8 trained without her
   (OUT), all with the same recipe as the target. The networks train in a third of a second each, so this is cheap
   here.
2. **Score each digit on each shadow model.** For every one of Carol's 40 digits, record how confident each IN model
   and each OUT model is in the right answer.
3. **Fit two bell curves per digit.** One describes how IN models usually score that digit, the other how OUT models
   score it. A clean, easy digit has both curves high. One of Carol's odd digits has the IN curve high and the OUT
   curve low.
4. **Ask which curve the target looks like.** If the target model's score on a digit is more likely under the IN
   curve, that digit is flagged "still a member". The member-rate is the share of the 40 that are flagged.

Because each digit gets its own pair of curves, a naturally easy digit no longer fools the test. It only counts as a
member if the target is more confident on it than models that never saw it.

| Model | U-LiRA member-rate |
|---|---|
| Fresh model trained **with** Carol | 0.97 (should be high) |
| Fresh model trained **without** Carol | 0.05 (should be low) |
| Original network | 0.95 |
| After retraining without Carol | 0.05 |

On the same network where the loss attack reached only AUC 0.71, U-LiRA flagged about 95% of Carol's digits.

The first two rows are the calibration. Before trusting a detector, you show it two models whose answer you already
know and check that it tells them apart. The last two rows are the result. On the original network the test flags
38 of Carol's 40 digits, and after retraining only 2 of them.

??? deep "Go deeper · the U-LiRA calculation in symbols"
    For a digit \(x\) with true label \(y\), let \(p\) be a model's probability for \(y\). The test works with
    \(\phi = \log \frac{p}{1-p}\), which spreads out probabilities close to 1 so they are easier to tell apart.

    For each digit, compute \(\phi\) on every IN model and fit a bell curve with mean \(\mu_{in}\) and spread
    \(\sigma_{in}\). Do the same on the OUT models to get \(\mu_{out}\) and \(\sigma_{out}\). Then compute \(\phi\) on
    the target model and compare how likely it is under each curve.

    \[
    \text{member if } \; \mathcal{N}(\phi \mid \mu_{in}, \sigma_{in}) > \mathcal{N}(\phi \mid \mu_{out}, \sigma_{out})
    \]

    The member-rate is the share of the forget set for which this holds. The course library does this in
    `audit.ulira`. It needs the IN and OUT models to share the target's recipe, because the curves describe how *that*
    recipe behaves.

!!! warning "Three cautions"
    1. Shadow models must use the **same training recipe** as the target, or the verdict can be wrong.
    2. AUC near 0.5 after unlearning only means *this* attack cannot find anything. Stronger attacks may.
    3. AUC far **below** 0.5 is a red flag too, because the forgotten data is treated *worse* than strangers.

??? checkpoint "Checkpoint 2 · A model scores 0.50 on U-LiRA for Carol. What would you say about it, given the four rows above?"
    **It still remembers a lot of her.** An honest retrain scores 0.05 and the original 0.95. A member-rate of 0.50
    means the test judges half of her 40 digits, 20 of them, to look more like a model that trained on them. The
    model has moved away from the original but is nowhere near a model that never saw her.

## A worked example

Follow Carol's digits through an attack, from Lesson 05 to the audit in Lesson 11.

1. **Set up a fair test.** Her 40 digits are the members. 80 unseen thick-marker digits are the non-members, so
   the attack cannot win by spotting thick strokes.
2. **The blunt attack.** On the original network the loss threshold reaches AUC 0.71. At 5% false positives it
   catches about one of her digits. On this evidence alone, she looks fairly safe.
3. **The sharp attack.** U-LiRA with 8 IN and 8 OUT shadow models flags 0.95 of her digits, so 38 of 40. She is not
   safe at all.
4. **Exact unlearning.** After retraining without her, the loss attack falls to AUC 0.48 and U-LiRA to 0.05. The
   attacker can no longer tell her digits from a stranger's.
5. **The audit.** Lesson 11 uses U-LiRA as its PRIVACY check. A model passes if its member-rate is not much above
   the retrains', with a margin of at least 0.10.

| Model in Lesson 11 | U-LiRA on Carol | PRIVACY check |
|---|---|---|
| Original | 0.950 | FAIL |
| Retrain | 0.075 | PASS |
| Fine-tune | 0.875 | FAIL |
| SCRUB | 0.275 | FAIL |
| SCRUB+R | 0.125 | PASS |
| Bad Teacher | 0.150 | PASS |

SCRUB moved a long way from the original, yet still left 11 of Carol's digits looking like members, which is
0.275 times 40. That was enough to fail. SCRUB+R passed PRIVACY but later failed the relearn attack, so a privacy pass
is one gate among several, not the whole verdict.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>0.96</strong><span>the forest's AUC on Carol, the biggest leak</span></div>
<div><strong>0.53</strong><span>the network's AUC on typical digits, close to a coin flip</span></div>
<div class="is-bad"><strong>95%</strong><span>Carol's digits U-LiRA flags on the original network</span></div>
<div class="is-good"><strong>5%</strong><span>flagged after retraining without her</span></div>
</div>

??? deep "Go deeper · the blunt attack before and after exact unlearning"

    | Model | AUC before | AUC after exact unlearning |
    |---|---|---|
    | Naive Bayes | 0.53 | 0.40 |
    | k-NN, k = 5 | 0.59 | 0.46 |
    | Logistic regression | 0.59 | 0.47 |
    | RBF SVM | 0.66 | 0.58 |
    | Random forest | 0.96 | 0.47 |
    | Neural network | 0.71 | 0.48 |

    After exact unlearning, Carol's digits and the 80 comparison digits are all strangers to the model. Any distance
    from 0.5 is then noise from a small test, or a small difference in how hard the two groups are. The forest makes
    the biggest move, from 0.96 to 0.47, because it had memorised her most.

## Limits

**It is evidence, not proof.** An attack that finds nothing has only shown that *this* attack finds nothing. Stronger
attacks exist (Hayes et al. 2024). See [Can a test prove forgetting?](testing-vs-proving.md).

**Shadow models cost training runs.** U-LiRA in Lesson 05 needs 16 extra networks. That is cheap for a digit network
that trains in a third of a second, but each one is a full training run for a large model.

**The references must match the target.** If the shadow models use a different recipe, the bell curves describe the
wrong kind of model and the verdict can be wrong. In Lesson 07, scored against SISA shadow models, the original
network that remembers Carol got 0.38 and a clean retrain got 0.50. The test ranked the guilty model below the
innocent one.

**Honest models get flagged too.** On Lesson 11's random request, models retrained without the data still had about a
third of the rows flagged, a member-rate of 0.360. Some rows simply look like members. That is why the PRIVACY check
compares a method with the retrains' member-rate, not with zero.

!!! tip "What to do in practice"
    - Compare members with non-members that look like them, never with a random test set of a different style.
    - Report the true-positive rate at a low false-positive rate next to AUC.
    - Aim the attack at the people most likely to be memorised, not only at typical users.
    - Calibrate a per-example test first, on one model known to contain the data and one known not to.
    - Train the shadow models with exactly the same recipe as the model under test.
    - Judge a method against the member-rate of honest retrains, not against zero.

## In code

```python
from mul import audit
r = audit.loss_mia(model, L.Xf, L.yf, L.X_like_forget, L.y_like_forget)
print(r["auc"], r["tpr@5%fpr"])
rate = audit.ulira(model, L.Xf, L.yf, in_models, out_models)   # share of D_f still judged a member
```

`L.X_like_forget` holds the unseen thick-marker digits, so the comparison is like with like. `in_models` and
`out_models` are the shadow models trained with and without Carol.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing on typical data only.** Attacks look weak on average and strong on unusual people.
    - **Comparing members with different-looking non-members.** The attack then learns style, not membership.
    - **Reporting only AUC.** The true-positive rate at a low false-positive rate shows real-world danger.
    - **Trusting a blunt attack's low score.** The network's AUC of 0.71 hid a leak that U-LiRA put at 95%.
    - **Skipping calibration.** A detector you have not tested on known answers can be wrong in either direction.
    - **Aiming for a member-rate of zero.** Honest retrains score above zero, and a score far below theirs is
      suspicious.

??? checkpoint "Checkpoint 3 · A team tests its model on typical users, gets AUC 0.53, and says membership attacks are no risk for them. What do you tell them?"
    **They aimed at the wrong people.** Typical data is learnt, not memorised, so it hardly leaks, which is why the
    network also scored 0.53 on typical digits. The same network leaked Carol badly, with U-LiRA flagging 95% of her
    digits. Test the unusual users, with a per-example attack and a strict false-positive rate.

## Key takeaways

!!! notes "Notes to take"
    - **MIA.** Guesses from the model's behaviour alone whether an example was in training.
    - **Clue.** Models are more confident, with lower loss, on what they trained on.
    - **Fair test.** Members against non-members of the same kind, such as Carol's 40 against 80 thick-marker digits.
    - **Two scores.** AUC for overall ranking, and the true-positive rate at 5% false positives for real danger.
    - **Who leaks.** Flexible models that memorise. Forest AUC 0.96, Naive Bayes 0.53.
    - **Averages hide risk.** Typical digits give AUC 0.53, while the right person leaks strongly.
    - **U-LiRA.** Per-example test with IN and OUT shadow models. Original 0.95, retrained 0.05.
    - **Calibrate first.** With Carol 0.97, without her 0.05.
    - **Trap.** A pass is evidence, not proof, and far below the retrains' score is a red flag too.

## Quiz

```quiz
- q: What does a membership inference attack try to find out?
  options:
    - Whether a specific example was in the training set
    - The model's architecture
    - The test accuracy
  answer: 0
  why: It guesses membership from the model's behaviour, which can leak private information.
- q: What does an AUC of 0.5 mean for an attack?
  options:
    - It is as good as a coin flip.
    - It is always right.
    - It is always wrong.
  answer: 0
  why: 0.5 means the attack cannot separate members from non-members at all.
- q: Why must non-members come from the same kind of data as the members?
  options:
    - Otherwise the attack learns the style of the data, not membership.
    - To make the test faster
    - Because the law says so
  answer: 0
  why: Comparing thick-marker members with thin-marker non-members would just detect thick strokes.
- q: What are shadow models used for in LiRA?
  options:
    - To learn how models score an example with and without it in training
    - To speed up training
    - To hide the target model
  answer: 0
  why: Comparing the target's behaviour with IN and OUT shadow models gives a per-example verdict.
- q: After unlearning, the attack's AUC on the forget set is 0.20. Is that good?
  options:
    - Yes, the lower the better.
    - No; it means the forget set is treated worse than strangers, which is itself a signal.
  answer: 1
  why: Far below 0.5 is over-forgetting, the "Streisand effect". It can be detected.
- q: The forest scores AUC 0.96 on Carol and Naive Bayes 0.53. What explains the difference?
  options:
    - The forest has more test data.
    - The forest memorised Carol and Naive Bayes did not.
    - Naive Bayes hides its probabilities.
  answer: 1
  why: Lesson 04 found a memorisation gap of 30.0 points for the forest and none for Naive Bayes. Memory is what leaks.
- q: Why is U-LiRA much sharper than a single loss threshold?
  options:
    - It compares each example with shadow models trained with and without that example.
    - It uses a larger test set.
    - It looks at the model's weights.
  answer: 0
  why: A naturally easy digit fools one threshold. Per-example curves only flag a digit the target is more confident on than models that never saw it.
- q: Before trusting U-LiRA, Lesson 05 runs it on a fresh model with Carol and one without her. Why?
  options:
    - To make the attack faster
    - To train more shadow models
    - To check the detector gives a high score when the answer is yes and a low one when it is no
  answer: 2
  why: They scored 0.97 and 0.05. A detector that cannot tell known cases apart cannot be trusted on unknown ones.
- q: On Lesson 11's random request, honest retrains had a U-LiRA member-rate of 0.360. What does that teach?
  options:
    - Judge a method against the retrains' member-rate, not against zero.
    - The retrains still remember the data.
    - U-LiRA does not work on random requests.
  answer: 0
  why: Some rows simply look like members to any model. The fair target is what models that never saw the data score.
```

## Try it

!!! levelup "Level up"
    You can now run a fair membership attack, read its scores and use it as a forgetting detector. Next quest,
    [The unlearning audit](unlearning-audit.md), where this test becomes the PRIVACY check beside four others.

- Read the next concept, [The unlearning audit](unlearning-audit.md).
- Run the lesson [05 · Membership inference attacks](../lessons/05-membership-inference.md).
- In the Lesson 05 notebook, shrink the shadow models from 8 to 2 and watch how much U-LiRA's answer wobbles.
