---
title: Can a test prove forgetting?
description: Attacks and tests can show that a model still remembers, but they cannot prove it has forgotten. Only the deletion process gives a guarantee.
---

# Can a test prove forgetting?

!!! oneline "In one line"
    Tests can show that a model **still remembers**, but they can never **prove** that it has forgotten; only the
    deletion *process* (retraining, SISA, an exact update) gives a guarantee.

!!! mission "Your mission · about 12 minutes · 3 checkpoints"
    By the end of this page you can

    - say what a failed test proves and what a passed test does not,
    - sort audit results into the four outcomes, including false alarms and blind spots,
    - write an honest claim for an exact method and for an approximate one.

## Why it matters

It is tempting to say "our model passed the audit, so the data is gone". That claim goes too far. Knowing exactly what an
audit can and cannot show lets you make honest claims, choose the right method and avoid promising regulators more than
you can deliver.

Lesson 11 gives three warnings in one table. The original model, which forgot nothing, passed the FORGET check on
the random request. SCRUB+R passed four checks on Carol and then gave her back after 20 steps of relearning. And SISA,
which is exact by construction, failed FORGET on Carol by one digit. So a pass can be wrong, and a fail can be wrong.
You need to know which kind of claim each piece of evidence can carry.

## A simple example

!!! simply "Explain it simply"
    You can prove a room has a mouse by finding one. You cannot prove it has none just because you did not see it;
    maybe you looked in the wrong place. Tests are like that. They can catch a model remembering, but not finding
    anything is not proof. The only proof is how the room was built, for example with no way in.

A security guard checks bags at a door. If they find a knife, they have **proved** someone brought a knife. If they find
nothing, they have not proved there is no knife; it may be hidden somewhere they did not look. A better search reduces
the risk, but never makes it zero.

Unlearning tests work the same way. A failed test is proof of remembering. A passed test only means "no test we ran
could tell the difference".

Now map the picture onto the course. The bag is the unlearnt model. The knife is Carol's remaining influence. The
guard's checks are the audit's five tests. A room built with no way in is an exact method, such as retraining, where
Carol's digits never reached the new model at all.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Test | A check on a finished model's behaviour, with a pass mark | The gold band, U-LiRA and the relearn attack |
| Evidence | A result that makes a claim more or less likely, without settling it | SCRUB+R passing FORGET on Carol |
| Guarantee | A claim that holds against every possible test, because of how the model was made | Retraining without Carol |
| [False alarm](../start-here/glossary.md#f) | A test rejecting a model that is actually fine | SISA failing FORGET on Carol by one digit |
| Blind spot | A test passing a model that still remembers | The original model passing FORGET on the random request |
| [Forging](../start-here/glossary.md#f) | Reaching the same final weights with or without a given example | Why weights alone cannot prove forgetting, as Thudi et al. (2022) showed |
| [Relearn attack](../start-here/glossary.md#r) | Reminding a model of part of the forget set and timing how fast the rest returns | SCRUB+R recovered Carol in 20 steps, retrains resisted 500 |
| [Pre-registration](../start-here/glossary.md#p) | Fixing the methods, tests and pass marks before running anything | Lesson 11's protocol, written down first |

## How it works

<!-- diagram: testing-vs-proving -->

The figure has two halves. On the left, six blue dots are tests that passed, scattered inside a box of everything
that could be checked. A dashed red circle marks an attack nobody tried, and the model could still be caught there.
On the right, the whole box is filled in, because an exact method makes the result identical to retraining, so every
possible test is covered at once.

### What tests can do

- **Show failure.** If a membership attack can tell Carol's data was used, or the relearn attack brings her back quickly,
  the model still carries her influence.
- **Build confidence.** Passing several strong, independent checks (gold band, per-example privacy, relearn) makes
  remaining influence less likely.

Each test looks at the model from a different side. The gold band looks at accuracy on the forget set. U-LiRA looks at
how confident the model is on each of Carol's digits. The relearn attack looks at what is hidden beneath the surface.
A method that slips past one is often caught by another, which is why Lesson 11 runs all of them.

### What tests cannot do

- **Rule out stronger attacks.** An attack with AUC 0.5 today may be beaten by a cleverer attack tomorrow.
- **Look inside the weights.** Thudi, Jia, Shumailov and Papernot (2022) showed that the same final weights can be
  reached *with or without* a given example, a trick called **forging**. So an auditor who only sees the final weights
  can be fooled.
- **Avoid false alarms.** Statistical checks sometimes reject good models. In [Lesson 11](../lessons/11-the-unlearning-audit.md),
  exact SISA failed FORGET by one digit.

??? deep "Go deeper · forging, in plain steps"
    Training is a long chain of small steps. Each step looks at a small batch of examples and nudges the weights. The
    final weights are where the chain ends.

    Forging asks a simple question. Could a *different* chain, one that never used Carol's digits, end at the same
    weights? Thudi et al. (2022) show that the answer can be yes. So the weights themselves cannot say whether Carol
    was used. Only a record of the chain, the data and the steps that produced the model, can.

    This is why the course's strongest evidence is about **process**. SISA keeps a log of which shard and slice each
    point went into and a checkpoint before each slice. Anyone can check from the log that Carol's shard was rebuilt
    from a point before she arrived.

### Four outcomes of a test

Any test can be right or wrong in two ways. Lesson 11 has an example of each.

| | Test passes | Test fails |
|---|---|---|
| **Model truly forgot** | Correct. The retrain passed every check on all three requests | **False alarm.** SISA scored 52.5% on Carol against a band starting near 52.6% |
| **Model still remembers** | **Blind spot.** The original passed FORGET on the random request | Correct. The original failed FORGET and PRIVACY on Carol |

The two error cells need different responses. A false alarm is a reason to investigate. For SISA the investigation is
short, because its exactness can be checked from its logs. A blind spot is worse, because nothing tells you to look.
The only defence is to run several kinds of test, so that one covers another's blind spot. On the random request, the
PRIVACY check caught what FORGET missed, flagging 0.712 of the original's rows against 0.360 for honest retrains.

??? checkpoint "Checkpoint 1 · SCRUB+R passed FORGET, PRIVACY, UTILITY and COST on Carol, then relearnt her in 20 steps where retrains needed 500. Which cell of the table is its four passes?"
    **The blind spot.** The four passes were tests passing a model that still remembers. Carol's influence was
    hidden, not removed, so the relearn attack brought it back quickly. This is why one more independent test changed
    the verdict to FAIL.

??? deep "Go deeper · why more tests also mean more false alarms"
    The gold band is set at about two standard deviations, so roughly 5 in every 100 honest models land outside it by
    chance. In Lesson 06, one of the 20 honest retrains scored 47.5% on Carol, below the band of 52.8% to 71.2%.

    Every check you add is another chance for a good model to trip. Running several checks lowers the risk of a blind
    spot but raises the risk that at least one of them raises a false alarm. That is why a FAIL is a reason to look
    closer, and why the width of each pass mark is a policy choice that someone must own, as Lesson 17 explains.

### Where guarantees come from

| Source of evidence | Guarantee? | Example |
|---|---|---|
| **Process.** Retrain without the data | ✅ Yes, by definition | [Retraining](retraining-gold-standard.md) |
| **Process.** SISA with a logged partition | ✅ Yes, bit for bit | [SISA](sisa.md) |
| **Process.** Exact classical update | ✅ Yes | [Subtracting counts, downdates](exact-unlearning-classical.md) |
| **Process.** Delete a per-customer adapter | ✅ Yes | [Unlearning a fine-tune](unlearning-fine-tunes.md) |
| **Audit** of an approximate method | ❌ Evidence only | [SCRUB](scrub.md), [Bad Teacher](bad-teacher.md) |

That is why the course's playbook prefers **exact methods by design**, and treats approximate methods plus an audit as a
fallback.

Read the table by asking where the guarantee lives. For the four process rows, it lives in how the model was made,
and you can check it from records without running a single attack. For the audit row, it lives only in the results
of the tests you happened to run. [Certified unlearning](certified-unlearning.md) sits in between. It is a
mathematical promise that the result is almost impossible to tell apart from retraining, with "almost" measured by
small numbers.

??? checkpoint "Checkpoint 2 · SISA failed FORGET on Carol by one digit. Should the team switch to an approximate method that passed?"
    **No.** SISA's result is exact by process, so the FAIL is a false alarm, and its logs show the shard was rebuilt
    from a checkpoint before Carol's slice. An approximate method that passed has only evidence behind it. Swapping a
    guarantee for evidence because of one statistical miss would be the wrong trade.

!!! note "How to phrase a claim honestly"
    - Exact method, "The model was retrained without the data (or the shard was rebuilt from a logged checkpoint). The
      result is identical to a model that never saw it."
    - Approximate method, "We applied method X. Under pre-registered tests A, B and C, the model was indistinguishable
      from models retrained without the data. This is evidence, not a guarantee."

## A worked example

Follow three models from the Lesson 11 audit on Carol's request, and the claim each one supports.

=== "Retrain"

    It scored 62.5% on Carol, inside the band, with a member-rate of 0.075 and no relearning within 500 steps. It
    passed every check. More importantly, it was made without her digits, so the claim rests on the process. You can
    sign the exact-method sentence above.

=== "SCRUB+R"

    It scored 65.0% on Carol, inside the band, with a member-rate of 0.125, and passed four checks. Then it recovered
    her in 20 steps of relearning, against 500 for the retrains. Verdict FAIL. Even if it had passed, the claim would
    only be the approximate-method sentence, because the result rests on tests, not on how it was made.

=== "SISA"

    It scored 52.5% on Carol, one digit below the band, and failed FORGET. It passed PRIVACY and UTILITY. Its logs show
    the shard was retrained from a checkpoint saved before her slice. The right claim is still the exact-method
    sentence, with a note that a statistical check gave a false alarm and why.

The three tabs show that the verdict and the claim are different things. A PASS from an approximate method supports
a weaker claim than a FAIL from an exact one.

## Limits

**Tests are only as good as the attacks you know.** The course uses a loss attack, U-LiRA and a split-half relearn
attack. Stronger attacks exist (Hayes et al. 2024), and new ones will appear.

**Process guarantees need trustworthy records.** SISA's guarantee depends on its partition and checkpoint logs being
complete and honest. A missing log turns a guarantee back into a claim.

**A guarantee covers only what was removed.** Retraining without Carol's 40 digits says nothing about copies of her
data elsewhere, such as backups or caches.

!!! tip "What to do in practice"
    - Prefer an exact method by design whenever you can afford one.
    - For an approximate method, pre-register the tests and pass marks, and run several independent kinds.
    - Include hard requests, such as a memorised person, not only random rows.
    - Treat a FAIL as a reason to investigate, and check the method's own logs first.
    - Write the claim to match the evidence, using the two sentences above.
    - Keep the records that a process guarantee depends on, such as partitions and checkpoints.

## Common mistakes

!!! danger "Mistakes people make"
    - **"It passed, so it is gone."** It passed *these* tests.
    - **Inspecting weights to prove forgetting.** Forging shows that weights alone cannot prove it.
    - **Treating every FAIL as final.** Investigate; false alarms happen, especially on small forget sets.
    - **Testing only random rows.** On the random request the original model passed FORGET while having forgotten
      nothing.
    - **Stopping at the checks that pass.** SCRUB+R looked clean on four checks and failed the fifth.

??? checkpoint "Checkpoint 3 · Bad Teacher passed PRIVACY on Carol with a member-rate of 0.150. Its owner writes, 'Carol has been provably removed.' How would you rewrite that?"
    **As evidence, not proof.** For example, "We applied Bad Teacher. Under pre-registered tests, the model's
    member-rate on Carol was close to that of models retrained without her. This is evidence, not a guarantee." In
    Lesson 11 Bad Teacher also failed UTILITY and RELEARN on Carol, which the claim should report too.

## Key takeaways

!!! notes "Notes to take"
    - **Asymmetry.** A failed test proves remembering. A passed test does not prove forgetting.
    - **Four outcomes.** Correct pass, correct fail, false alarm and blind spot.
    - **False alarm.** SISA, exact by construction, missed the band on Carol by one digit. Investigate the logs.
    - **Blind spot.** The original passed FORGET on random rows. PRIVACY caught it, 0.712 against 0.360.
    - **Hidden, not removed.** SCRUB+R passed four checks and relearnt Carol in 20 steps, against 500 for retrains.
    - **Forging.** The same weights can come from training with or without an example, so weights cannot prove it.
    - **Where guarantees live.** In the process, meaning retraining, SISA with logs, exact updates and deleted adapters.
    - **Honest claim.** Exact methods claim identity with retraining. Approximate methods claim evidence under named tests.

## Quiz

```quiz
- q: A model fails a membership attack after unlearning. What does that show?
  options:
    - It still carries the data's influence.
    - It has fully forgotten.
    - Nothing at all.
  answer: 0
  why: If the attack can still tell the data was used, the model remembers. A failed test is real evidence.
- q: A model passes every test. What can you honestly say?
  options:
    - No test we ran could tell the difference.
    - The data is provably gone.
  answer: 0
  why: A stronger attack might still find something. Passing is evidence, not proof.
- q: What is "forging", from Thudi et al. (2022)?
  options:
    - Reaching the same final weights with or without a given example
    - Faking an audit report
    - Training a model twice
  answer: 0
  why: Because of forging, an auditor who sees only the final weights can be fooled.
- q: Which of these gives a real guarantee of forgetting?
  options:
    - SISA with a logged partition
    - SCRUB plus an audit
    - Bad Teacher's ZRF score
  answer: 0
  why: SISA's exactness comes from its process and can be checked from its logs.
- q: The original model, which forgot nothing, passed FORGET on Lesson 11's random request. What kind of error is that?
  options:
    - A false alarm
    - A blind spot
    - A correct pass
  answer: 1
  why: A test passed a model that still remembers. Random rows look like everything else, so accuracy cannot see the difference.
- q: Why is a false alarm on SISA less worrying than a blind spot?
  options:
    - A false alarm tells you to look, and SISA's logs settle the question.
    - False alarms never happen on exact methods.
    - Blind spots only affect classical models.
  answer: 0
  why: A FAIL prompts an investigation. A blind spot gives no signal at all, so only another kind of test can catch it.
- q: SCRUB+R passed four checks on Carol. What did the relearn attack add?
  options:
    - It confirmed she was removed.
    - It made the model forget her more.
    - It showed her influence was hidden, not removed, because she came back in 20 steps.
  answer: 2
  why: Retrained references resisted for the full 500 steps. A quick return means the knowledge was still there.
- q: Which claim fits an approximate method that passed every pre-registered test?
  options:
    - The result is identical to a model that never saw the data.
    - Under the named tests it was indistinguishable from retrained models, which is evidence, not a guarantee.
    - The data has been provably deleted from the weights.
  answer: 1
  why: Only a process, such as retraining or SISA, supports a claim of identity. Tests support evidence.
```

## Try it

!!! levelup "Level up"
    You can now tell evidence from proof and write a claim that matches what an audit really showed. Next quest,
    [When forgotten knowledge comes back](relearning-and-quantization.md), where hidden knowledge returns through
    relearning and quantisation.

- Read the next concept, [Erasure requests and fairness](fairness-and-erasure.md).
- Run the lesson [11 · The unlearning audit](../lessons/11-the-unlearning-audit.md).
