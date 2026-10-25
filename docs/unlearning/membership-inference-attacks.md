---
title: Membership inference attacks
description: A membership inference attack guesses whether a person's data was used to train a model. It is both a privacy threat and an audit tool.
---

# Membership inference attacks

!!! oneline "In one line"
    A **membership inference attack** (MIA) tries to tell, just by asking the model questions, whether a particular
    person's data was in its training set.

## Why it matters

It matters twice over.

1. **As a threat**: if an attacker can tell that your medical record trained a hospital's model, the model is leaking
   private information, even if it never prints your record.
2. **As an audit tool**: if, *after* unlearning, the attack can no longer tell Carol's digits from digits that were
   never in training, that is behavioural evidence that she is forgotten.

## A simple example

A quiz-show contestant answers some questions instantly and confidently, and hesitates on others. You might guess that
the instant answers are ones they had practised before. A model behaves the same way, because it is usually **more confident on
examples it trained on**. The attacker uses that confidence as a clue.

## How it works

### The simple attack: a loss threshold

<ol class="steps" markdown>
<li markdown>Ask the model about a digit and look at its [loss](../ml-basics/loss-functions.md) on the right answer, i.e. how surprised it is.</li>
<li markdown>Guess "member" when the loss is low, "non-member" when it is high.</li>
<li markdown>Score the attack with **AUC** (0.5 is a coin flip, 1.0 is always right) and the **true-positive rate at a low
false-positive rate**: how many members you can flag *confidently*.</li>
</ol>

The test must compare members with **non-members from the same kind of data**. In the course: Carol's 40 digits
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
risk is concentrated on unusual data: **averaged over everyone, attacks look weak; aimed at the right people, they are
strong.**

### The stronger attack: per-example likelihood ratios (LiRA)

Some digits are naturally easy, and a single threshold cannot tell "easy" from "easy because it was trained on". **LiRA**
(Carlini et al. 2022) asks three questions for each example separately. How do models that *trained on* it usually score it? How do models that *did not* score it? Which of the two does the target model look like?

The attacker trains **shadow models**, some with the example and some without. The course version, **U-LiRA**, gives the
share of `D_f` judged "still a member":

| Model | U-LiRA member-rate |
|---|---|
| Fresh model trained **with** Carol | 0.97 (should be high) |
| Fresh model trained **without** Carol | 0.05 (should be low) |
| Original network | 0.95 |
| After retraining without Carol | 0.05 |

On the same network where the loss attack reached only AUC 0.71, U-LiRA flagged about 95% of Carol's digits.

!!! warning "Three cautions"
    1. Shadow models must use the **same training recipe** as the target, or the verdict can be wrong.
    2. AUC near 0.5 after unlearning only means *this* attack cannot find anything. Stronger attacks may.
    3. AUC far **below** 0.5 is a red flag too, because the forgotten data is treated *worse* than strangers.

## In code

```python
from mul import audit
r = audit.loss_mia(model, L.Xf, L.yf, L.X_like_forget, L.y_like_forget)
print(r["auc"], r["tpr@5%fpr"])
rate = audit.ulira(model, L.Xf, L.yf, in_models, out_models)   # share of D_f still judged a member
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing on typical data only.** Attacks look weak on average and strong on unusual people.
    - **Comparing members with different-looking non-members.** The attack then learns style, not membership.
    - **Reporting only AUC.** The true-positive rate at a low false-positive rate shows real-world danger.

## Key takeaways

- An MIA guesses whether data was used in training, from the model's behaviour alone.
- Models are more confident on training data, and that is the clue.
- Per-example attacks with shadow models (LiRA, U-LiRA) are much stronger than one threshold.
- After exact unlearning, the attack cannot tell Carol from strangers. That is the behavioural evidence.

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
```

## Try it

- Next concept: [The unlearning audit](unlearning-audit.md).
- Lesson: [05 · Membership inference attacks](../lessons/05-membership-inference.md).
