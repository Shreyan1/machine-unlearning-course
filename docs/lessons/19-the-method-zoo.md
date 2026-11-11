---
title: "Lesson 19 · The method zoo"
description: Fourteen unlearning methods sit one pre-registered exam on three requests. New is not better, and a privacy test can be fooled.
---

# Lesson 19 · The method zoo, fourteen ways to forget, one exam

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~50 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 8 · Extensions</span><span class="chip" markdown="span">:material-stairs-up: Rung 13</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/19-The-Method-Zoo.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/19-The-Method-Zoo.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 50 minutes · 2 checkpoints"
    By the end of this lesson you can

    - run fourteen unlearning methods through one exam fixed in advance and read the leaderboard,
    - explain why SSD and UNSIR did nothing on the class request,
    - catch a privacy pass that comes from lower confidence everywhere, and fix the test.

## The story

Lesson 11 wrote one exam; eight methods sat it. Research brings new methods every year, each with a paper saying it
works. This lesson adds six (random labels, SalUn, L1-sparse, UNSIR, SSD and last-layer re-solve) and puts all fourteen
through the same exam, with settings fixed in advance.

Think of a cooking contest. Fourteen cooks make the same three dishes for the same judges, and the scoring sheet was
written before anyone tasted anything. Some cooks are famous. The scoring sheet does not care.

The stakes are real for anyone choosing a method. Papers usually test their own method with settings tuned on their own
data. If the newer methods only win on their own exams, a team that picks one could ship a model that still remembers
the person who asked to be forgotten.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** the original model and references for Carol, the class "3" and a random 10%, exactly as in Lesson 11.</li>
<li markdown>**Untrain** with fourteen methods, the same way, on every request.</li>
<li markdown>**Show the result** as one leaderboard.</li>
<li markdown>**Prove it.** Check whether the new passes are real.</li>
<li markdown>Fold in a fair privacy check and publish the final leaderboard.</li>
</ol>

## What each step teaches

**Step 1. The same references.** For each request the lesson trains the original model, 12 models that never saw the
forget data to build the [gold band](../unlearning/gold-band.md) and 8 that did see it for the privacy test, U-LiRA.
Carol's band is 62.7% ± 9.5%, the class band is exactly 0.0% and the random band is 98.2% ± 1.6%.

**Step 2. Fourteen methods, one function.** Every method runs through the same function at its paper's default
settings. Each is also tagged with its family, 7 model-agnostic, 4 model-intrinsic, 2 data-driven and retraining as the
exact baseline. This step teaches what pre-registration means in practice. Nothing is tuned after the results arrive.

**Step 3. The leaderboard.** One table shows every method's verdict on every request. Reading it row by row shows where
each method breaks, and that the family does not predict the result.

**Step 4. Are the passes real?** The lesson stops at a puzzle, a method that remembers Carol perfectly but passes
privacy. It looks at confidence on the data the model should keep, and finds the cause.

**Step 5. The fair privacy check.** The reference models are put through the same method as the model under test, as
Hayes et al. (2024) do, with a never-saw-it control. The final leaderboard is written to `results/leaderboard.json`.

??? deep "Go deeper · how the fair privacy check is built"
    - **IN references.** Models that saw the forget data, **then** put through the method.
    - **OUT references.** Models that never saw it, **then** put through the same method.
    - **Control.** One more never-saw-it model put through the method. The test should call it "not a member", so its
      score is the false-alarm level.

    If the method really removes the data, the unlearnt model looks like the OUT group. If it only lowers confidence,
    both groups move together and the unlearnt model still looks like the IN group. The check is not run on the class
    request. There a method that wipes out the class makes both groups get every 3 wrong, so the test has nothing to
    compare.

## Key results

<div class="stats">
<div class="is-bad"><strong>0 of 12</strong><span>approximate methods that forgot Carol</span></div>
<div class="is-bad"><strong>5 → 0</strong><span>new methods passing the random 10%, before and after the fair test</span></div>
<div class="is-bad"><strong>0.0%</strong><span>weights SSD changed on the class</span></div>
<div class="is-good"><strong>3 of 3</strong><span>requests passed by retraining</span></div>
</div>

**First leaderboard.** Five of the six new methods passed the random request, where nothing approximate had passed in
Lesson 11. No approximate method passed Carol; every one failed RELEARN on her. SSD changed **no weights** on the class request, because its rule can never fire when the forget set is 10% or more of the data.

The SSD result is worth a second look. SSD shrinks a weight only if it matters more than 10 times as much for the forget
data as for the whole training set. But the whole set includes the forget data, so when that is 10% of it, no weight can
qualify. SSD changed 6.8% of weights on Carol, 0.2% on the random 10% and 0.0% on the class. UNSIR also left the class
untouched, because its noise and one short impair step were too weak at the pre-registered settings.

??? checkpoint "Checkpoint 1 · The class request forgets 128 of the training digits and the random request 125. SSD changed 0.0% of weights on one and 0.2% on the other. Why the small difference?"
    **The random set is just under 10% and the class just over.** 128 ÷ 1,257 is 10.2%, so the rule cannot fire at
    all. 125 ÷ 1,257 is 9.9%, which leaves a tiny gap for a few weights to qualify. On Carol, at 3.2%, the rule had
    plenty of room and changed 6.8%.

**Are the passes real?** L1-sparse passed PRIVACY on Carol while still getting all 40 of her digits right. The new
methods lower confidence on almost everything.

| Model | Confidence on kept data | As log-odds |
|---|---|---|
| Original | 1.000 | 7.65 |
| Retrain | 0.999 | 7.14 |
| Random labels | 0.884 | 2.04 |
| SalUn | 0.874 | 1.94 |
| L1-sparse | 0.983 | 4.05 |

Read the last column. U-LiRA works with log-odds, where being 99.9% sure and 98% sure are far apart. The retrain sits
at 7.14, close to the original. Random labels and SalUn fall to about 2, and L1-sparse to about 4, whether or not the
forget example was removed.

U-LiRA reads lower confidence as "never saw it". The fix is to put the IN and OUT references **through the same method**,
and add a never-saw-it control. With fair references, the approximate methods were called "still a member" far more than
the control, and the random-request passes disappeared.

??? deep "Go deeper · the fair privacy check, method by method"
    Share of forget examples the test calls "still a member", lower is better.

    | Method | Random, standard | Random, own-recipe | Random, control | Carol, standard | Carol, own-recipe | Carol, control |
    |---|---|---|---|---|---|---|
    | Random labels | 0.296 | 0.584 | 0.408 | 0.000 | 0.675 | 0.350 |
    | SalUn | 0.296 | 0.616 | 0.376 | 0.000 | 0.675 | 0.300 |
    | L1-sparse | 0.272 | 0.712 | 0.408 | 0.050 | 0.700 | 0.175 |
    | UNSIR | 0.280 | 0.616 | 0.376 | 0.175 | 0.850 | 0.275 |
    | Last layer | 0.240 | 0.640 | 0.376 | 0.300 | 0.950 | 0.050 |
    | SCRUB+R | 0.520 | 0.648 | 0.552 | 0.125 | 0.925 | 0.300 |

    On Carol every approximate method sits far above its control. On the random request the same is true for all but
    SCRUB+R, where the control itself scores 0.552, so the test is too noisy to say anything. SCRUB+R had already
    failed that request.

**Final leaderboard.**

| Method | Carol | Class | Random | Cost (% of retrain) |
|---|---|---|---|---|
| Retrain | ✅ | ✅ | ✅ | 100.0 |
| SISA | ❌ (false alarm) | ✅ | ✅ | 61.4 |
| SCRUB, SCRUB+R | ❌ | ✅ | ❌ | 13.6 |
| The other ten | ❌ | ❌ | ❌ | 0.3 to 15.0 |

Each row has a reason. **Retrain** is exact, so it passes everything at full price. **SISA** is exact too, and its miss
on Carol is the false alarm Lesson 11 explained, a score of 52.5% just under the band. **SCRUB and SCRUB+R** wipe out
the class cleanly but fail RELEARN on Carol and PRIVACY on the random request. **The other ten** fail every request once
the privacy test is fair.

This corrects Lesson 11. With fair references, SCRUB+R's privacy pass on Carol disappears. Its verdict was already
FAIL because of RELEARN.

??? checkpoint "Checkpoint 2 · With fair references, SCRUB+R scored 0.925 on Carol and its control 0.300. In Lesson 11 it had scored 0.125. What changed?"
    **Only the references.** SCRUB+R itself is the same model. Put through SCRUB+R, models that never saw Carol also
    become less sure, so the test now compares like with like. Against them, SCRUB+R still looks like a model that
    saw her, far above the 0.300 false-alarm level.

## Limits of this lesson

**One dataset, one network.** Every result comes from 8 × 8 digits and one small network. The ranking could change on
larger models or other data.

**Default settings.** Each method ran at its paper's default settings. Tuning would help some of them, but tuning
against the gold band is tuning on the answer sheet.

**Two requests for the fair check.** The fair privacy check ran on Carol and the random request only. The tasks ask you
to run it for SISA on Carol, to see whether the false alarm survives.

## Concepts used here

- [The method zoo](../unlearning/method-zoo.md)
- [The unlearning audit](../unlearning/unlearning-audit.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

## Notes to take

!!! notes "Notes to take"
    - **The exam.** Fourteen methods, three requests, the same references and pass marks, all fixed in advance.
    - **Carol.** No approximate method forgot her. Every one failed RELEARN.
    - **SSD.** Changed 0.0% of weights on the class, because its rule cannot fire at a forget set of 10% or more.
    - **UNSIR.** Left the class untouched at its default settings.
    - **The trap.** Lower confidence everywhere fools U-LiRA. L1-sparse passed privacy on Carol (U-LiRA 0.050) while still getting 100% of her digits right.
    - **The fix.** Put the IN and OUT references through the same method, and add a never-saw-it control.
    - **Final.** Retrain passes three, SISA two, SCRUB and SCRUB+R one, the other ten none.
    - **Correction.** SCRUB+R's privacy pass on Carol in Lesson 11 disappears with fair references.

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
- q: Random labels' confidence on kept data was 0.884, against 0.999 for a retrain. How did U-LiRA read that?
  options:
    - As proof that the model is broken
    - As "never saw it", because lower confidence looks like a model that did not train on the data
    - As no change at all
  answer: 1
  why: On the log-odds scale the drop is from 7.14 to 2.04, which looks like a model that never saw the forget data.
- q: Why was the fair privacy check not run on the class request?
  options:
    - The class request was too small.
    - The class request needed a GPU.
    - A method that wipes out the class makes the IN and OUT groups identical, so the test has nothing to compare.
  answer: 2
  why: Both groups get every 3 wrong, and even the control scores as a member, so the standard result stands there.
- q: Does a method's family, such as model-intrinsic, predict whether it passes?
  options:
    - Yes, model-intrinsic methods always pass.
    - No, the request and the exam decide, and methods in the same family can land far apart.
    - Yes, data-driven methods always fail.
  answer: 1
  why: SISA and UNSIR are both data-driven, yet SISA passes two requests and UNSIR none. The request and the exam decide.
```

## Open question → Lesson 20

!!! levelup "Level up"
    You can now run a crowd of methods through one fair exam and catch a privacy pass that has the wrong cause. Next
    quest, [Lesson 20 · Unlearning at scale](20-unlearning-at-scale.md), where the requests keep coming for a year.

Everything so far ran one request at a time. Real services get a steady stream for years. What happens to each method
when the requests keep coming?

[On to Lesson 20, unlearning at scale :material-arrow-right:](20-unlearning-at-scale.md){ .md-button }
