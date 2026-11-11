---
title: The method zoo
description: Fourteen unlearning methods, old and new, sit one fixed exam. New is not the same as better, and a privacy test can be fooled by accident.
---

# The method zoo

!!! oneline "In one line"
    When fourteen unlearning methods sit the **same fixed exam**, the newer ones do not beat the older ones and only
    the exact methods pass by design.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why one exam with settings fixed in advance is a fairer test than each paper's own,
    - read a method's rule and say when it cannot work, as with SSD on a large forget set,
    - spot a privacy pass that comes from lower confidence everywhere, and fix the test.

## Why it matters

Every year brings new unlearning methods, each with a paper saying it works. But papers usually test their own method,
with settings tuned on their own data. Putting many methods through **one pre-registered exam** shows which claims
survive. It also reveals a subtle way that a privacy test can be fooled.

Lesson 11 wrote that exam and eight methods sat it. Lesson 19 adds six newer methods and runs all fourteen on the same
three requests, with the same reference models and the same pass marks. Nothing is tuned after the results come in.

This matters to anyone who must choose a method for a real service, or check a vendor's claim. A method that wins in
its own paper can fail on someone else's exam. And a test that looks strict can be passed for the wrong reason.

## A simple example

Think of a cooking contest with fourteen cooks, the same three dishes, the same judges and a scoring sheet written before anyone tastes anything. Some cooks are famous. The scoring sheet does not care.

!!! simply "Explain it simply"
    If each cook picked their own dish and their own judge, every cook could claim to be the best. Fix the dishes, the
    judges and the sheet first, and only real skill shows.

In the course, the cooks are the fourteen methods. The three dishes are the three requests, forgetting Carol, forgetting
every digit "3" and forgetting a random 10% of the data. The judges are the audit's checks. The scoring sheet is the
set of pass marks, written down before any method ran.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Pre-registration](../start-here/glossary.md#p) | Fixing every method's settings, the tests and the pass marks before running anything | Every method ran at its paper's default settings |
| [Model-agnostic methods](../start-here/glossary.md#m) | Methods that work on any model | Fine-tune, SCRUB and random labels |
| [Model-intrinsic methods](../start-here/glossary.md#m) | Methods that use the insides of one kind of model | SSD reads each weight's importance |
| [Data-driven methods](../start-here/glossary.md#d) | Methods that work on the data side | SISA splits the data, UNSIR adds made-up noise |
| [Relearn attack](../start-here/glossary.md#r) | Briefly showing the model half the forget set and seeing how fast the other half comes back | Every approximate method failed it on Carol |
| [U-LiRA](../start-here/glossary.md#l) | A per-example privacy test that compares the model with references that did and did not see each example | For the retrain, it called 7.5% of Carol's digits members |
| Log-odds | A way of writing confidence that stretches out the top end, so 99.9% sure and 98% sure are far apart | U-LiRA works on this scale |
| Own-recipe references | Reference models that are put through the same unlearning method as the model under test | The fix for the privacy trap |
| Control | One more never-saw-it model put through the method, which the test should call "not a member" | Its score is the false-alarm level |

## How it works

<!-- diagram: method-zoo -->

The figure puts every method on one line by cost, from 0% to 100% of a full retrain, and sorts it by whether it passed
the audit on Carol. Only Retrain, at 100%, sits in the green "passed" row. SISA, at 61.4%, is exact by design but missed
FORGET on Carol by one digit, a false alarm. The twelve approximate methods, from 0.3% to 15%, all sit in the red row. A lower cost bought a weaker result.

### The exam

Every method faces the same five checks on each request, the protocol from [The unlearning audit](unlearning-audit.md).

1. **FORGET.** Accuracy on the forget set must land inside the [gold band](gold-band.md). For Carol the band is
   62.7% ± 9.5%, for the class it is exactly 0.0% and for the random 10% it is 98.2% ± 1.6%.
2. **PRIVACY.** U-LiRA must not call many more forget examples "members" than it does for the retrained models.
3. **UTILITY.** Test accuracy must stay within 2 points of the retrains.
4. **RELEARN.** After a few steps of training on half the forget set, the other half must not come back much faster
   than it does for a retrained model.
5. **COST.** The method must be cheaper than retraining.

A method passes a request only if it passes every check. **For Carol this means** a method must move her from 100% to
about the middle of the band, keep the rest of the model sharp and hold firm under a short reminder.

??? deep "Go deeper · the exact pass marks"
    The settings were written down before any method ran, and they are saved with the results.

    - **References.** 12 models that never saw the forget set build the band. 8 more that did see it are used by U-LiRA.
    - **FORGET.** Inside the mean plus or minus the larger of 2 standard deviations and 3 points.
    - **PRIVACY.** The U-LiRA member rate may be at most the retrains' mean plus the larger of 2 standard deviations
      and 10 points.
    - **UTILITY.** Test accuracy at most 2 points below the retrains' mean.
    - **RELEARN.** Train on the first half of the forget set and count the steps until the second half reaches 95% of
      the original model's accuracy, up to 500 steps. The method must hold out for at least half as many steps as the
      retrained models do.

### Six new methods

Lesson 19 adds six newer methods to the eight from earlier lessons.

| Method | The idea in one line | Paper |
|---|---|---|
| **Random labels** | Give the forget data random wrong labels and keep training. | [Graves et al. 2021](https://arxiv.org/abs/2010.10981) |
| **SalUn** | The same, but only move the weights that matter most for the forget data. | [Fan et al. 2024](https://arxiv.org/abs/2310.12508) |
| **L1-sparse** | Fine-tune with a penalty that pushes small weights to zero. | [Jia et al. 2023](https://arxiv.org/abs/2304.04934) |
| **UNSIR** | Learn "noise" images the model gets wrong, train on them, then repair. | [Tarun et al. 2023](https://arxiv.org/abs/2111.08947) |
| **SSD** | Needs no training. It shrinks weights that matter far more for the forget data than for everything else. | [Foster et al. 2024](https://arxiv.org/abs/2308.07707) |
| **Last layer** | Keep the network, re-solve only its last layer exactly on the data that stays. | [After Guo et al. 2019](https://arxiv.org/abs/1911.03030) |

Methods also fall into three families, **model-agnostic** (works on any model), **model-intrinsic** (uses one model's
insides) and **data-driven** (changes the data side, like SISA or UNSIR).

Among the fourteen, 7 are model-agnostic, 4 are model-intrinsic, 2 are data-driven and retraining is the exact
baseline. Every family has methods that pass something and methods that fail everything, so the family alone does not
predict the result.

### The final leaderboard

On three requests, the fair privacy check below produces this leaderboard.

| Method | Carol | Class "3" | Random 10% | Cost (% of retrain) |
|---|---|---|---|---|
| Retrain | ✅ | ✅ | ✅ | 100 |
| SISA | ⚠️ false alarm | ✅ | ✅ | 61.4 |
| SCRUB, SCRUB+R | ❌ | ✅ | ❌ | 13.6 |
| All other ten methods | ❌ | ❌ | ❌ | 0.3 to 15.0 |

**No approximate method forgot Carol.** Every one of them failed the relearn attack on her.

Read the columns one at a time.

- **Carol.** One memorised person is the hardest request. Show any approximate method half her digits for a few steps
  and it is right about the other half again. SISA missed FORGET by a hair, the same false alarm the audit page
  explains.
- **The class.** SCRUB, SCRUB+R and SISA pass. Random labels and SalUn remove the class but fail PRIVACY.
- **Random 10%.** Five of the six new methods passed at first. The fair privacy check later took every one of those
  passes away.

??? deep "Go deeper · all fourteen methods on Carol"
    The first audit on Carol, before the fair privacy check. Carol's band is 62.7% ± 9.5%, and the costs are for her
    request.

    | Method | On Carol | Test accuracy | U-LiRA | Relearn steps | Cost | Checks failed |
    |---|---|---|---|---|---|---|
    | Original | 100.0% | 98.0% | 0.950 | 0 | 0% | FORGET, PRIVACY, RELEARN |
    | Retrain | 62.5% | 98.0% | 0.075 | 500 | 100% | none |
    | Fine-tune | 100.0% | 98.1% | 0.875 | 0 | 8.3% | FORGET, PRIVACY, RELEARN |
    | Gradient ascent | 100.0% | 98.3% | 0.600 | 0 | 0.3% | FORGET, PRIVACY, RELEARN |
    | NegGrad+ | 10.0% | 84.6% | 0.000 | 27 | 8.6% | FORGET, UTILITY, RELEARN |
    | SCRUB | 82.5% | 97.8% | 0.275 | 18 | 13.6% | FORGET, PRIVACY, RELEARN |
    | SCRUB+R | 65.0% | 98.0% | 0.125 | 20 | 13.6% | RELEARN |
    | Bad Teacher | 70.0% | 96.1% | 0.150 | 13 | 0.6% | UTILITY, RELEARN |
    | Random labels | 75.0% | 98.0% | 0.000 | 14 | 8.6% | FORGET, RELEARN |
    | SalUn | 82.5% | 97.8% | 0.000 | 13 | 8.7% | FORGET, RELEARN |
    | L1-sparse | 100.0% | 98.0% | 0.050 | 0 | 8.3% | FORGET, RELEARN |
    | UNSIR | 95.0% | 95.4% | 0.175 | 0 | 12.2% | FORGET, UTILITY, RELEARN |
    | SSD | 82.5% | 97.4% | 0.150 | 21 | 1.8% | FORGET, RELEARN |
    | Last layer | 100.0% | 98.0% | 0.300 | 0 | 15.0% | FORGET, PRIVACY, RELEARN |

    The retrain held out for the full 500 steps. Every approximate method was back within 27 steps or fewer. Several
    methods also show a U-LiRA score below the retrain's 0.075 while still knowing Carol. That is the trap explained
    below.

### Read the rule before you trust the method

SSD changed **no weights at all** on the class request. Its rule only touches a weight if it matters more than 10 times
as much for the forget data as for the *whole* training set. But the whole set *includes* the forget data. When the
forget set is 10% of the data, the rule can never fire.

The share of weights SSD changed tells the story. It was 6.8% on Carol, 0.2% on the random 10% and 0.0% on the class.
The method was built for small forget sets, and at the paper's default setting it did nothing on a large one. UNSIR also
left the class untouched, because its noise and one short impair step were not strong enough at the pre-registered
settings. That is the price of pre-registering. No method gets tuned on the answer sheet.

??? deep "Go deeper · why SSD's rule cannot fire"
    SSD measures how much each weight matters for a set of data by averaging over its examples. Call that \(I_f\) for
    the forget set and \(I_D\) for the whole training set. It shrinks a weight only when \(I_f > 10 \times I_D\).

    The whole set is the forget set plus the rest. If the forget set is a share \(s\) of it, then
    \(I_D = s \, I_f + (1 - s) \, I_r\), where \(I_r\) is the importance for the rest. Importance is never negative, so
    \(I_D \ge s \, I_f\). With \(s = 0.1\), that gives \(I_D \ge 0.1 \, I_f\), so \(I_f \le 10 \times I_D\). The rule
    \(I_f > 10 \times I_D\) can never be true. The paper's own class tasks forget between 1% and 5% of the data.

??? checkpoint "Checkpoint 1 · Carol's 40 digits are about 3% of the 1,257 training digits. Could SSD's rule fire on her, and did it?"
    **Yes, and it did.** With a share of about 3% (40 ÷ 1,257 is 3.2%), a weight's importance for the whole set can
    be as low as about 3% of its importance for Carol, so it can easily be 10 times smaller. SSD changed 6.8% of the
    weights. It still failed, because Carol stayed at 82.5% and relearned in 21 steps.

### A privacy test fooled by accident

On the random request, five new methods first *passed* the privacy check. One of them, L1-sparse, passed privacy on
Carol while still getting all 40 of her digits right. How?

These methods make the model **less sure about almost everything**, including data it should keep. The privacy test
(U-LiRA) reads confidence, and lower confidence looks like "never saw it". The fix is the same recipe rule as before.
**Put the reference models through the same method too**, and add a never-saw-it control. With fair references, the
passes disappeared.

| Model | Confidence on kept data | As log-odds |
|---|---|---|
| Original | 1.000 | 7.65 |
| Retrain | 0.999 | 7.14 |
| Random labels | 0.884 | 2.04 |
| SalUn | 0.874 | 1.94 |
| L1-sparse | 0.983 | 4.05 |

On a 0 to 1 scale, L1-sparse's drop from 0.999 to 0.983 looks tiny. On the log-odds scale that U-LiRA uses, it falls
from 7.14 to 4.05. So the test sees a model that is much less sure, and calls the forget examples "not members", whether
or not they were removed.

The fair test, from Hayes et al. (2024), has three parts.

1. **IN references.** Models that saw the data, then put through the method.
2. **OUT references.** Models that never saw the data, then put through the same method.
3. **A control.** One more never-saw-it model put through the method. Its score is the false-alarm level.

If a method truly removes the data, the unlearnt model looks like the OUT group. If it only lowers confidence, both
groups move together and the unlearnt model still looks like the IN group.

!!! tip "The general lesson"
    Any change to how a model is made, **including the unlearning method itself**, is part of the recipe. Reference
    models must follow the same recipe.

??? checkpoint "Checkpoint 2 · With own-recipe references, L1-sparse scored 0.712 on the random request and its control scored 0.408. Was the first pass real?"
    **No.** The standard test gave L1-sparse 0.272, a pass. With fair references it calls 71.2% of the forget examples
    "still a member", far above the 40.8% false-alarm level of a model that never saw them. The first pass came from
    lower confidence everywhere, not from forgetting.

## A worked example

Follow L1-sparse on Carol through the exam.

1. **The start.** The original model gets all 40 of Carol's digits right, 100.0%. Her band is 62.7% ± 9.5%.
2. **The method.** L1-sparse fine-tunes on the data that stays, with a penalty that pushes small weights to zero. It
   costs 8.3% of a retrain.
3. **FORGET.** Carol is still at 100.0%, far above the band. Fail.
4. **UTILITY.** Test accuracy is 98.0%, the same as the retrain. Pass.
5. **PRIVACY, the standard way.** U-LiRA calls only 5.0% of her digits members, fewer than the retrain's 7.5%. Pass,
   and this is the puzzle.
6. **RELEARN.** Her second half is back at once, in 0 steps. The retrain held out for 500. Fail.
7. **PRIVACY, the fair way.** With own-recipe references, 70.0% of her digits look like members, against 17.5% for
   the control. Fail.

So a model that remembers Carol perfectly looked cleaner than an honest retrain on the standard privacy test. The same
fix also changes one result from Lesson 11. SCRUB+R passed PRIVACY on Carol there with 0.125, but with fair
references it scores 0.925 against a control of 0.300. Its verdict was already FAIL because of RELEARN, so only the
reason changes.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>0 of 12</strong><span>approximate methods that forgot Carol</span></div>
<div class="is-bad"><strong>5 → 0</strong><span>new methods passing the random 10% before and after the fair test</span></div>
<div class="is-bad"><strong>0.0%</strong><span>weights SSD changed on the class request</span></div>
<div class="is-good"><strong>3 of 3</strong><span>requests passed by retraining, the only clean sweep</span></div>
</div>

The leaderboard has the same shape as Lesson 11's, with more names on it. Exact methods pass by design. SCRUB and
SCRUB+R pass the class. Everything else fails everything once the privacy test is fair. Newer did not mean better.

## Limits

**One small setting.** Every result comes from 8 × 8 digit images and one network with two hidden layers of 256. A
larger model or a different kind of data could rank the methods differently.

**Default settings only.** Each method ran at its paper's default settings. Some would do better if tuned, but tuning
against the gold band is tuning on the answer sheet, which a real service cannot do.

**The fair check was not run on the class.** When a method wipes out the class, the IN and OUT groups both get every 3
wrong, so the test has nothing to compare. The standard result stands for that request.

**The random request is noisy.** For SCRUB+R the control itself was called a member 55.2% of the time, so the test was
too noisy to say anything there. SCRUB+R had already failed that request.

!!! tip "What to do in practice"
    - Fix every method's settings, the checks and the pass marks before you run anything, and publish them.
    - Test on a hard request, such as one unusual person, not only on a random sample.
    - Read each method's rule and ask whether it can work at your forget set's size.
    - Build privacy references with the same method you are testing, and report a never-saw-it control.
    - Always run the relearn attack. It caught every approximate method on Carol.
    - Prefer an exact method wherever you can design for it.

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming newer means better.** On a fixed exam with pre-registered settings, it did not.
    - **Tuning on the answer sheet.** In production there is no gold band to tune against.
    - **Trusting a privacy pass when confidence dropped everywhere.** Use own-recipe references and a control.
    - **Choosing a method by its family.** Every family has methods that pass something and methods that fail
      everything.
    - **Using a method outside its design.** SSD at its default setting cannot fire on a forget set of 10% or more.

??? checkpoint "Checkpoint 3 · A vendor's new method passes a random 10% request for 8% of a retrain, with settings tuned on that exam. What do you ask for?"
    **A harder, fairer exam.** Ask for settings fixed **before** the results, a request like Carol's with **one
    unusual person**, the **relearn attack**, and a privacy test with **own-recipe references and a control**. In
    Lesson 19 five new methods passed the random request, and none of those passes survived the fair test.

## Key takeaways

!!! notes "Notes to take"
    - **The exam.** Fourteen methods, three requests, five checks, every setting fixed in advance.
    - **New is not better.** No approximate method forgot Carol, and every one failed RELEARN on her.
    - **Pass by design.** Retrain passes all three requests. SISA passes two and has a false alarm on Carol.
    - **Class only.** SCRUB and SCRUB+R pass the class and fail the rest, at 13.6% of a retrain.
    - **Family.** It does not decide the result. The request and the exam do.
    - **Read the rule.** SSD changed 0.0% of weights on the class, because its rule cannot fire at a 10% forget set.
    - **Trap.** Lower confidence everywhere fools U-LiRA. L1-sparse passed privacy on Carol while scoring 100% on her.
    - **Fix.** Put the IN and OUT references through the same method and add a never-saw-it control.
    - **Correction.** With fair references, SCRUB+R's privacy pass on Carol in Lesson 11 disappears.

## Quiz

```quiz
- q: How many approximate methods forgot Carol on the fixed exam?
  options:
    - None
    - Half of them
    - All of them
  answer: 0
  why: Every approximate method, old or new, failed the relearn attack on Carol.
- q: Why did SSD change no weights on the class request?
  options:
    - Its rule cannot fire when the forget set is 10% or more of the data.
    - It crashed.
    - The class was already forgotten.
  answer: 0
  why: The whole training set includes the forget data, so no weight can be more than 10 times as important for it.
- q: Some methods passed the privacy test by lowering confidence everywhere. What is the fix?
  options:
    - Put the reference models through the same method, and add a never-saw-it control.
    - Drop the privacy test.
    - Use only accuracy.
  answer: 0
  why: If both IN and OUT references go through the method, a general confidence drop no longer looks like forgetting.
- q: Which methods pass by design, not by luck?
  options:
    - Exact methods such as retraining and SISA
    - The newest methods
    - Methods with the lowest cost
  answer: 0
  why: Their result is guaranteed by the process, not just by passing tests.
- q: L1-sparse's confidence on kept data fell from 0.999 to 0.983. Why did that matter so much to U-LiRA?
  options:
    - U-LiRA only looks at test accuracy.
    - U-LiRA works on log-odds, where the drop is from 7.14 to 4.05.
    - The drop deleted Carol's digits.
  answer: 1
  why: On the log-odds scale, 99.9% sure and 98% sure are far apart, so a small-looking drop reads as "never saw it".
- q: What does the never-saw-it control in the fair privacy test tell you?
  options:
    - Which method is cheapest
    - The width of the gold band
    - The false-alarm level, how often the test calls a clean model a member
  answer: 2
  why: A method is only convincing if it scores near the control. L1-sparse scored 0.712 on the random request against a control of 0.408.
- q: Why are methods run at their papers' default settings, even when tuning would help them?
  options:
    - Tuning against the gold band is tuning on the answer sheet, which a real service cannot do.
    - Tuning is not allowed by law.
    - The defaults are always the best settings.
  answer: 0
  why: In production there are no retrained models to compare with, so a fair exam must not use them for tuning either.
- q: Every approximate method failed RELEARN on Carol. What does that tell you?
  options:
    - The relearn attack is broken.
    - Her knowledge was hidden, not removed, because a short reminder brought it back.
    - Carol's digits were never in the training set.
  answer: 1
  why: The retrain held out for 500 steps. Every approximate method was back within 27 steps or fewer.
```

## Try it

!!! levelup "Level up"
    You can now judge a crowd of methods on one fair exam and catch a privacy test that is passed for the wrong
    reason. Next quest, [Membership inference attacks](membership-inference-attacks.md), where you look inside the
    test that was fooled.

- Run the lesson [19 · The method zoo](../lessons/19-the-method-zoo.md).
- In the notebook, find the smallest SSD setting that changes any weights on the class, and note that you are now
  tuning on the answer sheet.
- Add a fifteenth method of your own and run it through the same exam without changing the protocol.
