---
title: "Lesson 19: The method zoo"
description: Fourteen unlearning methods sit one pre-registered exam on three requests. New is not better, and a privacy test can be fooled.
---

# Lesson 19: The method zoo, fourteen ways to forget, one exam

<div class="chips"><span class="chip">⏱ ~50 min</span><span class="chip">Stage 8 · Extensions</span><span class="chip">Rung 13</span></div>

<div class="buttons">
<a class="md-button md-button--primary" href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/19-The-Method-Zoo.ipynb">Open in Colab</a>
<a class="md-button" href="https://github.com/Shreyan1/machine-unlearning-course/blob/main/19-The-Method-Zoo.ipynb">View on GitHub</a>
</div>

## The story

Lesson 11 wrote one exam; eight methods sat it. Research brings new methods every year, each with a paper saying it
works. This lesson adds six (random labels, SalUn, L1-sparse, UNSIR, SSD and last-layer re-solve) and puts all fourteen
through the same exam, with settings fixed in advance.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the original model and references for Carol, the class "3" and a random 10%, exactly as in Lesson 11.</li>
<li markdown>**Untrain** with fourteen methods, the same way, on every request.</li>
<li markdown>**Show the result** as one leaderboard.</li>
<li markdown>**Prove it**: check whether the new passes are real.</li>
<li markdown>Fold in a fair privacy check and publish the final leaderboard.</li>
</ol>

## Key results

**First leaderboard.** Five of the six new methods passed the random request, where nothing approximate had passed in
Lesson 11. No approximate method passed Carol; every one failed RELEARN on her. SSD changed **no weights** on the class request, because its rule can never fire when the forget set is 10% or more of the data.

**Are the passes real?** L1-sparse passed PRIVACY on Carol while still getting all 40 of her digits right. The new
methods lower confidence on almost everything:

| Model | Confidence on kept data | As log-odds |
|---|---|---|
| Original | 1.000 | 7.65 |
| Retrain | 0.999 | 7.14 |
| Random labels | 0.884 | 2.04 |
| SalUn | 0.874 | 1.94 |
| L1-sparse | 0.983 | 4.05 |

U-LiRA reads lower confidence as "never saw it". The fix is to put the IN and OUT references **through the same method**,
and add a never-saw-it control. With fair references, the approximate methods were called "still a member" far more than
the control, and the random-request passes disappeared.

**Final leaderboard:**

| Method | Carol | Class | Random | Cost (% of retrain) |
|---|---|---|---|---|
| Retrain | ✅ | ✅ | ✅ | 100.0 |
| SISA | ❌ (false alarm) | ✅ | ✅ | 61.4 |
| SCRUB, SCRUB+R | ❌ | ✅ | ❌ | 13.6 |
| The other ten | ❌ | ❌ | ❌ | 0.3 to 15.0 |

This also corrects Lesson 11: SCRUB+R's privacy pass on Carol disappears with fair references (its verdict was already
FAIL because of RELEARN).

## Concepts used here

- [The method zoo](../unlearning/method-zoo.md)
- [The unlearning audit](../unlearning/unlearning-audit.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

## Quiz

```quiz
- q: How many approximate methods forgot Carol on the fixed exam?
  options:
    - None
    - Three
    - All fourteen
  answer: 0
  why: Every approximate method failed the relearn attack on her.
- q: Why did SSD change no weights on the class request?
  options:
    - Its rule cannot fire when the forget set is 10% or more of the data.
    - It needs a GPU.
    - The class was empty.
  answer: 0
  why: The whole training set includes the forget data, so no weight is 10 times more important for it.
- q: How did L1-sparse pass PRIVACY on Carol while remembering her?
  options:
    - It lowered confidence on almost everything, which looks like "never saw it".
    - It truly forgot her.
    - The test was skipped.
  answer: 0
  why: The privacy test reads confidence, so a general drop fools it.
- q: What is the fair fix for that privacy test?
  options:
    - Put the reference models through the same method, and add a never-saw-it control.
    - Use accuracy only.
    - Remove the privacy test.
  answer: 0
  why: Then a general confidence drop moves IN and OUT references together and no longer looks like forgetting.
- q: Which methods pass by design?
  options:
    - Exact ones, such as retraining and SISA
    - The newest ones
    - The cheapest ones
  answer: 0
  why: Their guarantee comes from the process, not from passing tests.
```

## Open question → Lesson 20

Everything so far ran one request at a time. Real services get a steady stream for years. What happens to each method
when the requests keep coming?

[Next: Lesson 20, unlearning at scale](20-unlearning-at-scale.md){ .md-button }
