---
title: The unlearning audit
description: One pre-registered protocol with five checks, FORGET, PRIVACY, UTILITY, COST and RELEARN, run the same way on every method and written down as evidence.
---

# The unlearning audit

!!! oneline "In one line"
    An unlearning audit is an exam set **in advance**, with the same five checks for every method, marked against models
    that genuinely never saw the data, and written down so that someone else can check it.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - set up a fair audit, with settings fixed in advance and references built with the same recipe,
    - run a result through the five checks and say which ones it passes,
    - tell removed data from suppressed data with the relearn attack, and read a FAIL as a reason to look closer.

## Why it matters

Each method so far marked its own homework, with its own table. A regulator, a review board or a customer needs
something better, which is one fair, repeatable protocol. The audit also adds a final check, the **relearn attack**, which
separates data that was truly *removed* from data that was only *hidden*.

Without a shared protocol, results cannot be compared. In Lesson 10, Bad Teacher's own metric ranked it above a true
retrain. In Lesson 09, SCRUB+R looked like a winner on three checks. Lesson 11 runs every method through the same exam
and finds that no approximate method passes Carol's request at its default settings.

This matters most to the people who must sign off an erasure, such as a Data Protection Officer. They need a record
that says what was tested, how and with what result, and that someone else can re-run.

## A simple example

!!! simply "Explain it simply"
    An audit is a fair exam. You write the questions and the pass mark before anyone sits it, you give every method the
    same exam, and you compare their answers with students who never saw the forbidden material. Then you write it all
    down, so someone else can mark it again and get the same result.

A school exam is written before anyone sees the answers, the same paper is given to every student and it is marked
against an answer key. One question asks, "If I remind you of half of Carol's digits, how quickly do you remember the
other half?" A student who truly never learnt them will be slow. A student who was only pretending to forget will
answer at once.

Map the exam onto the course. The students are the **unlearning methods**. The answer key is a set of **models
retrained without Carol**. The questions are the **five checks**. The trick question is the **relearn attack**. The
marked paper, kept on file, is the **evidence record**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Pre-registration](../start-here/glossary.md#p) | Writing down every setting before any result is seen | Lesson 11 prints its protocol before running a method |
| OUT reference | A model retrained without the forget set, a sample of the right answer | 12 per request, seeds 100 to 111 |
| IN reference | A model trained with the forget set, used by the privacy test | 8 per request, seeds 1 to 8 |
| [Gold band](../start-here/glossary.md#g) | The mean of the OUT references plus or minus two standard deviations, at least 3 points each side | 62.7% ± 9.5% on Carol |
| [U-LiRA](../start-here/glossary.md#l) | A per-example membership test that compares the model with IN and OUT references | 0.950 for the original on Carol |
| [Relearn attack](../start-here/glossary.md#r) | Fine-tune on half the forget set and count steps until the other half comes back | 500 steps for every retrain on Carol |
| [Suppression](../start-here/glossary.md#s) | Data that is hidden from the output but still inside the model | SCRUB+R relearnt Carol in 20 steps |
| [False alarm](../start-here/glossary.md#f) | A test rejecting a model that is actually fine | SISA missed the band on Carol by one digit |
| [Evidence record](../start-here/glossary.md#e) | A machine-readable file of the protocol, the band, every number and every verdict | `audit_carol.json` |

## How it works

<!-- diagram: unlearning-audit -->

The figure reads from left to right. On the left are three kinds of model, the original before unlearning, the
unlearnt model being judged and several retrained models that form the gold band. In the middle are the independent
tests each model faces. On the right are the two outcomes. A model passes only if it lands inside the band on every
test, and the evidence is reported either way.

<ol class="steps" markdown>
<li markdown>**Pre-register** every method's settings before running anything. In production you cannot tune against the gold band, so the audit must not either.</li>
<li markdown>**Build references** with the **same training recipe** as the system under audit. These are several models retrained without \(D_f\) (OUT) and some trained with it (IN).</li>
<li markdown>**Run five checks** on every method.</li>
<li markdown>**Use several kinds of request**, because a method that passes one can fail another.</li>
<li markdown>**Write an evidence record.** A machine-readable file with the protocol, the band, every number and every verdict.</li>
</ol>

**Pre-registering stops quiet tuning.** Lessons 08 to 10 swept many settings and found the odd one that passed. Picking
it needs the gold band, which production never has. So Lesson 11 uses each lesson's default settings, written down
first.

**The same recipe keeps the answer key honest.** In Lesson 07, SISA references ranked a one-network model that
still remembered Carol (0.38) as cleaner than a truly clean one (0.50). So each model is audited against references
trained with its own recipe, and SISA against SISA references.

**For Carol this means** 12 networks retrained without her and 8 trained with her, all with the course's one recipe of
60 epochs, and every method run with the settings printed at the top of the notebook.

### The five checks

| Check | Question | How |
|---|---|---|
| **FORGET** | Is forget-set accuracy inside the gold band? | Mean ± max(2 std, 3 points) of the retrains |
| **PRIVACY** | Can a per-example attack still tell \(D_f\) was used? | U-LiRA member-rate, see [membership inference](membership-inference-attacks.md) |
| **UTILITY** | Is the model still useful? | Test accuracy no more than 2 points below the retrains |
| **COST** | Is it cheaper than retraining? | Count of example-gradients |
| **RELEARN** | Was it removed, or only hidden? (Deeb and Roger 2024) | Show half of \(D_f\) again; count steps until the other half comes back |

Each check closes a hole the others leave open. FORGET catches a model that still remembers *and* one that
over-forgot. PRIVACY looks at each example, so it catches what an average hides. UTILITY catches a model that forgot by
breaking. COST catches a method that is no cheaper than the gold standard. RELEARN catches knowledge that was hidden
rather than removed. A method must pass all five.

??? deep "Go deeper · the exact pass rules in the course library"
    - **FORGET.** Accuracy on \(D_f\) must lie within the OUT references' mean plus or minus the larger of 2 standard
      deviations and 3 points.
    - **PRIVACY.** The U-LiRA member-rate must be no more than the references' mean plus the larger of 2 standard
      deviations and 0.10.
    - **UTILITY.** Test accuracy must be no more than 2 points below the references' mean.
    - **COST.** The method must process fewer example-gradients than a 60-epoch retrain on \(D_r\).
    - **RELEARN.** The model is fine-tuned on the first half of \(D_f\) with a learning rate of 0.001 and batches of
      16. The count stops when it gets the second half right 95% as often as the original did, or at 500 steps. It
      passes if it holds out for at least half the references' median.

    The first four rules live in `audit.gate` and the last in `audit.relearn_test`. The values of \(k\), the 3-point
    floor, the 2-point utility tolerance and the 0.10 privacy tolerance are all written into the protocol before any
    method runs.

??? checkpoint "Checkpoint 1 · A method scores 70.0% on Carol, U-LiRA 0.150, test accuracy 96.1%, cost 0.6% of a retrain and 13 relearn steps. Which checks does it pass?"
    **FORGET, PRIVACY and COST, but not UTILITY or RELEARN.** 70.0% is inside the band of about 53% to 72%, and 0.150
    is under the privacy limit. 96.1% is just over 2 points below the retrains' average of about 98%, so UTILITY fails. Retrains needed
    500 relearn steps, so the pass mark is 250, and 13 is far short. This is Bad Teacher at its default settings.

### Three kinds of request

| Request | What is deleted | Real-world example |
|---|---|---|
| **carol** | 40 memorised examples from one person | A GDPR erasure request |
| **class** | Every digit 3 | Removing one person from a face-recognition model |
| **random** | A random 10% of training | A bulk retention purge |

Each request gives a band of a very different shape. On Carol it is 62.7% ± 9.5%, wide and in the middle. On the class
it is 0.0% ± 0.0%, because a model that never saw a 3 can never say "3". On the random 10% it is 98.2% ± 1.6%, narrow and
near the top. The [gold band](gold-band.md) page explains why the shapes differ.

### The first surprise (random requests fool accuracy)

On the **random** request, the original model, which forgot *nothing*, **passed FORGET**. A model retrained without
those rows still gets about 98% on them, because they look like everything else. Only the PRIVACY check caught it.
Evaluations that use random forget sets and accuracy alone will happily certify a model that did nothing.

This is the central warning of Hayes et al. (2024). The original's U-LiRA member-rate on the random rows was 0.712,
against 0.360 for a retrain, so the per-example test could still see the difference. An audit therefore needs
per-example privacy tests and *hard* requests, such as a memorised person or a whole class, not only random ones.

### The second surprise (the relearn attack)

| Method | Steps to relearn the other half of Carol |
|---|---|
| Retrained references | 500 (the full budget, every time) |
| SCRUB+R | 20 |
| SCRUB | 18 |
| Bad Teacher | 13 |
| Original, fine-tune, gradient ascent | 0 |

SCRUB+R passed the first four checks on Carol. But shown 20 of her digits, it got the *other* 20 back within about 20
steps. Retrained models could not, because for them there was nothing to recall. That is **suppression**, not removal.

The attack follows Lynch et al. 2024 and Deeb and Roger 2024, and it returns in [LLM unlearning](llm-unlearning.md).
It never shows the model the second half of Carol's digits. If those come back anyway, the model must still hold what
it learnt from her the first time. A model that never saw her has to learn her style from 20 examples, which is slow.

The class request gives a useful contrast. There, even retrained references relearn the 3s in a median of 9 steps,
because "what a 3 looks like" is general knowledge built from curves and strokes the model already has. When everyone
relearns fast, the test cannot separate the methods. The relearn attack measures memorised, specific information,
which is what privacy law cares about.

??? checkpoint "Checkpoint 2 · The retrained references relearn Carol in a median of 500 steps. What is the RELEARN pass mark, and does NegGrad+ at 27 steps pass?"
    **The pass mark is 250 steps, and NegGrad+ fails.** A model passes if it holds out for at least half the
    references' median, so 0.5 × 500 = 250. NegGrad+ gave in after 27. It had also over-forgotten Carol, at 10.0%, so it
    failed FORGET as well.

### Even exact methods can trip a check

SISA, which is exact by construction, failed FORGET on Carol by **one digit**, with 52.5% against a band starting at about
52.6%. Nothing was wrong with SISA. A band estimated from 12 references on a 40-example set will sometimes reject a
perfectly good model. A FAIL is a reason to **investigate**, not an automatic verdict.

SISA was audited against 12 OUT and 8 IN references built with the SISA recipe of 5 shards and 4 slices. It passed
PRIVACY and UTILITY on all three requests and passed the class and random requests outright. Here the investigation
ends quickly, because SISA's exactness is a property of the *process* and can be checked from its logs. Its weak spot
is COST. With a random partition, one request touches most shards, so it cost about 61% of a retrain on Carol.

## A worked example

Follow SCRUB+R through the whole audit on Carol in Lesson 11.

1. **Pre-register.** Its settings are written down first, 8 epochs with 4 max-steps, a learning rate of 0.0005,
   forget batches of 8 and a temperature of 1.
2. **References.** 12 OUT networks give a band of 62.7% ± 9.5%, so about 53.2% to 72.2%. 8 IN networks join them for
   the privacy test.
3. **FORGET.** SCRUB+R scores 65.0% on Carol, 26 of her 40 digits. Inside the band, so it passes.
4. **PRIVACY.** U-LiRA flags 0.125 of her digits, which is 5 of 40. Under the limit, so it passes.
5. **UTILITY.** Test accuracy is 98.0%, within 2 points of the retrains' average of about 98.4%. It passes.
6. **COST.** It processed 13.6% of a retrain's example-gradients. It passes.
7. **RELEARN.** Fine-tuned on 20 of her digits, it gets the other 20 right as often as the original within 20 steps. The
   pass mark is 250. It fails, and so does the overall verdict.
8. **The record.** Every number above goes into `audit_carol.json`, with the protocol and the band.

??? deep "Go deeper · SCRUB+R's entry in the evidence record"
    The notebook saves one record per request. This is SCRUB+R's entry for Carol, with the numbers rounded here.

    ```json
    {
     "forget_acc": 0.65,
     "test_acc": 0.9796,
     "ulira": 0.125,
     "relearn_steps": 20.0,
     "cost_%": 13.55,
     "FORGET": "ok",
     "PRIVACY": "ok",
     "UTILITY": "ok",
     "COST": "ok",
     "RELEARN": "x",
     "verdict": "FAIL"
    }
    ```

    The run also writes `audit_class.json`, `audit_random.json` and a certificate file. Lesson 17 turns these into
    the certificate a Data Protection Officer signs.

On the old four-check table, SCRUB+R would have been the winner. The fifth check turns its verdict round.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>100.0%</strong><span>the original on the random rows, still passed FORGET</span></div>
<div class="is-bad"><strong>20 steps</strong><span>for SCRUB+R to relearn Carol</span></div>
<div class="is-good"><strong>500 steps</strong><span>for every retrained reference, the full budget</span></div>
<div><strong>52.5%</strong><span>exact SISA on Carol, one digit under the band</span></div>
</div>

??? deep "The full Lesson 11 results on Carol"

    | Method | Carol | Test | U-LiRA | Relearn steps | Cost | Fails |
    |---|---|---|---|---|---|---|
    | Original | 100.0% | 98.0% | 0.950 | 0 | 0% | FORGET, PRIVACY, RELEARN |
    | Retrain (seed 999) | 62.5% | 98.0% | 0.075 | 500 | 100% | none, PASS |
    | Fine-tune | 100.0% | 98.1% | 0.875 | 0 | 8.3% | FORGET, PRIVACY, RELEARN |
    | Gradient ascent | 100.0% | 98.3% | 0.600 | 0 | 0.3% | FORGET, PRIVACY, RELEARN |
    | NegGrad+ | 10.0% | 84.6% | 0.000 | 27 | 8.6% | FORGET, UTILITY, RELEARN |
    | SCRUB | 82.5% | 97.8% | 0.275 | 18 | 13.6% | FORGET, PRIVACY, RELEARN |
    | SCRUB+R | 65.0% | 98.0% | 0.125 | 20 | 13.6% | RELEARN |
    | Bad Teacher | 70.0% | 96.1% | 0.150 | 13 | 0.6% | UTILITY, RELEARN |
    | SISA (own references) | 52.5% | 98.0% | 0.175 | n/a | 61.4% | FORGET, a false alarm |

    On the class request, SCRUB and SCRUB+R passed outright. On the random request, no approximate method passed and
    SISA did. At default settings no approximate method passed Carol.

??? checkpoint "Checkpoint 3 · SCRUB+R passed the class request but failed Carol and the random request. A manager asks whether it is audited and safe. What do you say?"
    **Audited, yes. Safe, only for some requests.** It passed every check on removing a whole class. On Carol it
    passed four checks but relearnt her in 20 steps, so she was suppressed. On the random request it failed PRIVACY.
    A method is judged per kind of request, and a pass is evidence, not proof.

## Limits

**It is evidence, not proof.** Thudi et al. (2022) show that the same weights can be reached with or without an
example, so an auditor who sees only the final model can be fooled. An audit can show a method *failed*. A pass only
means no test we ran could tell the difference. See [Can a test prove forgetting?](testing-vs-proving.md)

**Every check has false alarms.** A band from 12 references on 40 examples moves in steps of 2.5 points, and it shut
out an exact SISA model by one digit.

**The relearn attack cannot always run.** It fine-tunes one network, so it reports "n/a" for SISA's ensemble of five.
On the random request the retrains already get the rows right without training, so it has nothing to measure.

??? deep "Go deeper · two more limits"
    **The tolerances are policy choices.** The 2 standard deviations, the 3-point floor and the privacy tolerance of
    0.10 decide many verdicts. The notebook asks which verdicts flip when the privacy tolerance falls to 0.05, and
    Lesson 17 gives these numbers an owner.

    **References are expensive.** Each request needs 12 OUT and 8 IN models, so 20 extra training runs. That is cheap for
    the course's digit network but not for a large production model.

## What to do in practice

!!! tip "What to do in practice"
    - Write the protocol down first, including every method's settings, \(k\), the floors and the tolerances.
    - Build the references with exactly the same recipe as the system you audit, including any sharding.
    - Test at least one hard request, such as a memorised person or a whole class, never only random rows.
    - Run all five checks, and add RELEARN whenever the forget set holds specific, memorised information.
    - Treat a FAIL as a reason to investigate, and save every number in a machine-readable record.

## In code

```python
from mul import audit
table = audit.audit(models, splits, retrained_refs, costs=costs, in_models=in_refs)
band_mean, band_std = audit.gold_band(retrained_refs, splits, in_models=in_refs)
print(audit.gate(table, band_mean, band_std, cost_ref=60 * len(L.Xr)))   # FORGET, PRIVACY, UTILITY and COST
```

`audit.audit` measures every model the same way. `audit.gold_band` scores each reference against the others to build
the band. `audit.gate` turns the numbers into a PASS or FAIL for each check. The fifth check is a separate call,
`audit.relearn_test(models, L.Xf, L.yf, retrained_refs, original)`, which returns the relearn steps and a RELEARN
verdict for each model.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only random forget sets.** The original model can pass.
    - **References with a different recipe.** The verdict can be wrong, even backwards.
    - **Stopping at four checks.** Without RELEARN, suppression looks like success.
    - **Treating a pass as proof.** An audit is evidence. See [Can a test prove forgetting?](testing-vs-proving.md)
    - **Choosing settings after seeing the band.** It makes every method look better than it would in production.
    - **Reading every FAIL as final.** SISA failed by one digit while being exact by construction.

## Key takeaways

!!! notes "Notes to take"
    - **Protocol.** Pre-register the settings, build 12 OUT and 8 IN references with the same recipe, run five checks.
    - **FORGET.** Inside the band of mean ± max(2 std, 3 points). On Carol, 62.7% ± 9.5%.
    - **PRIVACY.** U-LiRA member-rate no more than the retrains' plus the larger of 2 std and 0.10.
    - **UTILITY and COST.** Test accuracy within 2 points of the retrains, cheaper than a retrain.
    - **RELEARN.** Hold out for at least half the retrains' median. On Carol that is 250 of 500 steps.
    - **Trap.** On a random 10%, the original passed FORGET. Only PRIVACY caught it.
    - **Suppression.** SCRUB+R passed four checks on Carol and relearnt her in 20 steps.
    - **False alarm.** Exact SISA missed Carol's band by one digit. Investigate, then check the process.
    - **Remember.** Write it all down in a machine-readable record. A pass is evidence, not proof.

## Quiz

```quiz
- q: Why must method settings be fixed before the audit runs?
  options:
    - In production you cannot tune against the gold band, so the audit must not either.
    - It makes the audit faster.
    - The law lists the settings.
  answer: 0
  why: Tuning against the answer key would make every method look better than it really is.
- q: On the random request, the original model passed FORGET. Why?
  options:
    - Random rows look like everything else, so even a retrained model gets them right.
    - The original model had already forgotten them.
    - The test set was empty.
  answer: 0
  why: Accuracy cannot tell the difference. Only the per-example privacy check caught it.
- q: What does the relearn attack measure?
  options:
    - Whether forgotten data comes back quickly after a short reminder
    - How fast the model was originally trained
    - The test accuracy
  answer: 0
  why: Fast recovery means the knowledge was only hidden, not removed.
- q: SCRUB+R relearnt Carol in about 20 steps; retrained models needed 500. What does that mean?
  options:
    - SCRUB+R suppressed Carol rather than removing her.
    - SCRUB+R is better than retraining.
    - The attack is broken.
  answer: 0
  why: For a model that never saw her, there is nothing to recall, so relearning is slow.
- q: SISA failed FORGET on Carol by one digit. What is the right response?
  options:
    - Investigate; it is a statistical false alarm, and SISA's exactness can be checked from its logs.
    - Declare SISA broken.
    - Delete the audit.
  answer: 0
  why: Every statistical test has false alarms. A FAIL is a reason to look closer, not an automatic verdict.
- q: Why does the audit build its references with the same recipe as the system under test?
  options:
    - It saves training time.
    - Otherwise the verdict measures the recipe, and can even come out backwards.
    - The law requires one recipe.
  answer: 1
  why: In Lesson 07, SISA references ranked a one-network model that still remembered Carol (0.38) as cleaner than a truly clean one (0.50).
- q: Why can the relearn attack not separate methods on the class request?
  options:
    - Every method scores 0% on the 3s.
    - The attack only works on random requests.
    - Even retrained models relearn 3s in a median of 9 steps, because a 3 is general knowledge.
  answer: 2
  why: When everyone relearns fast, there is nothing to tell apart. The attack measures memorised, specific information.
- q: Retrained references needed 500 steps to relearn Carol. What is the RELEARN pass mark?
  options:
    - 250 steps, half the references' median
    - 500 steps, the full budget
    - 20 steps
  answer: 0
  why: A model passes if it holds out for at least half the references' median, and 0.5 × 500 = 250.
- q: Bad Teacher scored 70.0% on Carol and passed PRIVACY, but its test accuracy was 96.1%. What does the audit say?
  options:
    - PASS, because forgetting matters most
    - FAIL, because UTILITY is more than 2 points below the retrains
    - It depends only on the cost
  answer: 1
  why: A method must pass every check. It also failed RELEARN, at 13 steps against a pass mark of 250.
```

## Try it

!!! levelup "Level up"
    You can now run a fair audit, read all five checks and tell removal from suppression. Next quest,
    [Can a test prove forgetting?](testing-vs-proving.md), where you find out what any audit can and cannot promise.

- Read the next concept, [Can a test prove forgetting?](testing-vs-proving.md).
- Run the lesson [11 · The unlearning audit](../lessons/11-the-unlearning-audit.md).
- In the Lesson 11 notebook, change the privacy tolerance from 0.10 to 0.05 and see which verdicts flip.
