---
title: State of the field
description: What works today, how methods are compared and the open problems in machine unlearning.
---

# State of the field

!!! oneline "In one line"
    Exact unlearning is solved for classical models and by design; approximate unlearning for neural networks works on
    benchmarks but without guarantees; unlearning in large language models is still an open problem.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - say for any kind of model whether forgetting is solved, works with an audit or is still open,
    - read a benchmark result and say what it does and does not show,
    - name the five open problems and the course result behind each one.

## Why it matters

Machine unlearning moves fast, and claims run ahead of evidence. Knowing what is solved, what is promising and what is
open helps you choose a method and set expectations with lawyers and leaders. It also helps you spot a claim that is
too good to be true. This page is the map at the end of the course; each row links to the page that explains it.

The course has its own evidence for every row. It ran fourteen methods through one fixed exam, a year of deletion
requests through four strategies and the exact updates on models of growing size. Those results are small, on 8 × 8
digit images, but they are measured, so they make a good check on the bigger claims you will read.

## A simple example

Think of medicine. Some illnesses have a reliable cure, some have treatments that usually work but must be checked
with tests, and some are still being researched. Unlearning has all three.

!!! simply "Explain it simply"
    The reliable cures are the exact methods, such as subtracting a row from Naive Bayes or retraining one SISA shard.
    They work every time and you can show why. The treatments that need tests are the approximate methods for neural
    networks, which must pass an audit each time. The illnesses still in the lab are language models, where nobody can
    yet say exactly what should be forgotten.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Exact unlearning](../start-here/glossary.md#e) | A result that matches retraining without the data, by construction | SISA after a year of requests equalled a fresh SISA model, bit for bit |
| [Certified unlearning](../start-here/glossary.md#c) | An approximate update with a proven bound on how far it can be from retraining | The Newton step on logistic regression in Lesson 02 |
| [Approximate unlearning](../start-here/glossary.md#a) | A cheap change to a trained model, with no guarantee, so it must be audited | SCRUB, Bad Teacher and gradient ascent |
| Benchmark | A shared test that lets different teams compare methods on the same task | TOFU, MUSE and WMDP |
| [Pre-registration](../start-here/glossary.md#p) | Fixing an exam's settings before any method is scored | Lesson 19 ran all fourteen methods at settings fixed in advance |
| [Gold band](../start-here/glossary.md#g) | The range of results from several models retrained without the data | 62.7% ± 9.5% on Carol in Lessons 11 and 19 |
| [Relearn attack](../start-here/glossary.md#r) | Fine-tuning briefly on part of the forget set to see whether the rest comes back | Every approximate method relearnt Carol in Lesson 19 |

## How it works

### What works today

| Setting | Status | What to use |
|---|---|---|
| k-NN, Naive Bayes, linear and ridge regression | **Solved, exactly** | [Subtract or downdate](exact-unlearning-classical.md) |
| Logistic regression and other convex models | **Solved, with a proof** | A Newton step, or [certified unlearning](certified-unlearning.md) |
| Random forests, SVMs | **Solved for most requests** | Rebuild only the [affected parts](exact-unlearning-classical.md) |
| Any model, if planned before training | **Solved by design** | [SISA](sisa.md) shards, or [retraining](retraining-gold-standard.md) on a schedule |
| Retrieval (RAG) systems | **Solved, if you track the copies** | [Delete from every store](rag-and-vector-stores.md) |
| Neural network classifiers | **Works, with an audit** | [SCRUB](scrub.md), [Bad Teacher](bad-teacher.md) and [others](method-zoo.md), checked against the [gold band](gold-band.md) |
| Federated models | **Partly solved** | See [federated unlearning](federated-unlearning.md) |
| Large language models | **Open** | See [unlearning in language models](llm-unlearning.md) |

Read the table from top to bottom and it is the [Ladder of Forgetting](ladder-of-forgetting.md). The higher rows give
you a handle on the model, such as a sum you can subtract from or a shard you can retrain. The lower rows take the
handles away. "Solved" always means solved for that part of the system. A company with a SISA model and a vector store
next to it must solve both.

"Works, with an audit" is the row people most often read too kindly. It does not mean that most approximate methods
pass. It means that a method can be used when an audit, built in advance, says it passed on that request.

### What the course's exam found

Lesson 19 put fourteen methods through the exam of Lesson 11, on three requests. These were Carol's 40 digits, every
digit 3 and a random 10% of the users. The settings were fixed in advance, so no method was tuned on the answers.

<div class="stats">
<div class="is-good"><strong>3 of 3</strong><span>requests passed by retraining, the only method to pass all</span></div>
<div><strong>2 of 3</strong><span>passed by SISA, which missed Carol by one digit</span></div>
<div class="is-bad"><strong>0 of 12</strong><span>approximate methods that forgot Carol</span></div>
<div class="is-bad"><strong>10 of 14</strong><span>methods that passed no request at all</span></div>
</div>

SCRUB and SCRUB+R passed one request each, the class. Every approximate method failed RELEARN on Carol. Shown half of
her digits for a few steps, each was right about the other half again. Five of the six newer methods first seemed to
pass the random request, but those passes were not real. They made the model less sure of almost everything, which a
confidence-based privacy test reads as forgetting. Building the test's reference models with the method itself, as
Hayes et al. (2024) do, removed every one of those passes.

??? deep "Go deeper · the final leaderboard from Lesson 19"

    | Method | Family | Carol | Class | Random | Cost (% of retrain) |
    |---|---|---|---|---|---|
    | Retrain | Exact baseline | PASS | PASS | PASS | 100.0 |
    | SISA | Data-driven | FAIL | PASS | PASS | 61.4 |
    | SCRUB | Model-agnostic | FAIL | PASS | FAIL | 13.6 |
    | SCRUB+R | Model-agnostic | FAIL | PASS | FAIL | 13.6 |
    | UNSIR | Data-driven | FAIL | FAIL | FAIL | 12.2 |
    | Fine-tune | Model-agnostic | FAIL | FAIL | FAIL | 8.3 |
    | Gradient ascent | Model-agnostic | FAIL | FAIL | FAIL | 0.3 |
    | NegGrad+ | Model-agnostic | FAIL | FAIL | FAIL | 8.6 |
    | Bad Teacher | Model-agnostic | FAIL | FAIL | FAIL | 0.6 |
    | Random labels | Model-agnostic | FAIL | FAIL | FAIL | 8.6 |
    | SalUn | Model-intrinsic | FAIL | FAIL | FAIL | 8.7 |
    | L1-sparse | Model-intrinsic | FAIL | FAIL | FAIL | 8.3 |
    | SSD | Model-intrinsic | FAIL | FAIL | FAIL | 1.8 |
    | Last layer | Model-intrinsic | FAIL | FAIL | FAIL | 15.0 |

    The family does not decide the result. Data-driven has SISA, which passes two requests, and UNSIR, which passes
    none. Model-agnostic has SCRUB, which passes the class, and gradient ascent, which fails everything. The four
    model-intrinsic methods pass nothing. What decides it is the request and the exam. SISA's miss on Carol is the same false alarm as in
    Lesson 11, a band from 12 references that now and then shuts out an exact model.

??? checkpoint "Checkpoint 1 · A vendor's approximate method passes a privacy test on random users. What do you ask before you believe it?"
    **Whether the test's reference models went through the same method.** In Lesson 19, five methods passed the random
    request because they lowered the model's confidence everywhere, not because they forgot. When the references were
    put through the method too, as Hayes et al. (2024) recommend, every one of those passes went away. Ask also for a
    never-saw-it control, to show the test's false-alarm level.

### How methods are compared

- **The NeurIPS 2023 unlearning competition** asked about 1,200 teams to make a face-based age predictor forget, and
  scored them with a formal definition of forgetting plus a check on usefulness. The best entries beat the methods
  published before it (Triantafillou et al. 2024).
- **TOFU** fine-tunes a language model on made-up author biographies, then asks it to forget some authors. Because the
  authors are fictional, nothing else in the training data can leak them.
- **MUSE** tests six things people want from LLM unlearning, from removing verbatim text to keeping the model useful.
- **WMDP** measures hazardous knowledge, such as biosecurity and cybersecurity, that a model should not be able to
  provide.

Each benchmark fixes one part of the problem so the rest can be compared. The competition fixes the definition of
forgetting. TOFU fixes the forget set, so nothing leaks in from elsewhere. MUSE fixes the list of things to measure.
WMDP fixes the knowledge that should be gone. The course's own exam does the same at small scale, with settings fixed
in advance, references that never saw the data and a check that the model is still useful.

A benchmark score is evidence on that benchmark. It does not cover a request it did not test, an attack it did not
run or a model it did not use. That is why the course always adds a relearn attack, and why the next section lists
robustness as an open problem.

??? checkpoint "Checkpoint 2 · A method tops a forgetting benchmark. Is it ready to answer real erasure requests?"
    **Not on that alone.** A benchmark shows how it did on one task with one set of checks. In Lesson 19 every
    approximate method failed the relearn attack on Carol, and Lesson 11's privacy check had been too easy on all of
    them. Before you use it, run it through your own audit on your own kinds of request, with a relearn attack and
    references built the same way as the model under test.

### The open problems

1. **Proof.** Except for exact and certified methods, nobody can yet *prove* that a neural network has forgotten. Tests
   can show that a model [still remembers](testing-vs-proving.md), not that it has forgotten.
2. **Robustness.** Forgotten knowledge can [come back](relearning-and-quantization.md) after a small fine-tune or after
   compression.
3. **Defining the target in LLMs.** A fact is spread across many documents, paraphrases and languages, so it is hard
   to say exactly what should be forgotten, and what may stay.
4. **Scale.** Many requests a year, on models that cost millions to train; see [unlearning at scale](unlearning-at-scale.md).
5. **Legal acceptance.** No regulator has yet said that any unlearning method counts as deletion; see
   [policies around the world](global-policy.md).

The course met each of these in its own lessons. **Proof** was the reason for the gold band, because a pass inside the
band is evidence, not proof. **Robustness** was the relearn attack that every approximate method failed on Carol.
**Defining the target** was Lesson 16, where a fact is a habit of the model, not a row. **Scale** was Lesson 20, and
**legal acceptance** is the gap between "names unlearning" and "accepts it as deletion" on the policies page.

??? deep "Go deeper · the scale numbers from Lesson 20"
    **Retraining for every request grows with the square of the service.** A service twice as big costs twice as much
    per retrain and gets twice as many requests. Against retraining every 4 weeks, retraining for every request cost
    about 6 times more at 1,000 users and about 63,644 times more at 10 million.

    **SISA keeps up and stays exact.** Over a year of 104 requests, SISA with 20 shards, serving every request at once,
    cost about 2.3% of retraining for each. After the year it was bit for bit the same as a fresh SISA model trained
    without the 104 users.

    **Exact Newton updates do not fit deep models.** The Newton step needs the Hessian, a table with one row and one
    column per weight. The course's network has 85,002 weights, so its Hessian would need about 57.8 GB. A model with a
    billion weights would need about 8 billion GB. Certified removal also spends a fixed budget with each removal, so
    even linear models need a full retrain on a schedule.

??? checkpoint "Checkpoint 3 · The Newton step removes data from logistic regression with a certificate. Why not use it on a language model with a billion weights?"
    **The Hessian is far too big.** It has one row and one column per weight, so it grows with the square of the
    model. For the course's 85,002-weight network it would already need about 57.8 GB, and for a billion weights about
    8 billion GB. That is why deep models rely on SISA, retraining or approximate methods with an audit.

## Limits

**This map is a snapshot.** The field moves fast. A row marked open today may move up, and new methods appear every
year. Check the date of any claim, including this page's.

**The course's evidence is small.** The exam, the year of requests and the Hessian sizes come from one digit network
and a few requests. They show the shape of each problem, not the numbers you will see on a large model.

**"Solved" is about the model, not the system.** An exact method removes the data from one model. Copies in backups,
logs, caches and other models still need their own deletion, as [the enterprise playbook](enterprise-playbook.md)
shows.

!!! tip "What to do in practice"
    - Find the lowest rung for each part of your system and use the exact tool there first.
    - Plan exactness before training, with SISA, adapters or checkpoints, where you can.
    - Treat any approximate method as unproven until your own audit, fixed in advance, says it passed.
    - Always include a relearn attack and references built with the same recipe as the model under test.
    - Read benchmark results as evidence on that benchmark, and check the date of every claim.

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting a benchmark score alone.** A method can top a benchmark and still fail a relearning or compression test.
    - **Assuming LLM unlearning works like classifier unlearning.** Facts are not rows, and the gold band is much harder
      to build.
    - **Ignoring the solved cases.** Many real systems have classical or retrieval parts where exact deletion is cheap.
    - **Trusting a privacy pass built with the wrong references.** In Lesson 19, five passes vanished once the
      references went through the same method.

## Key takeaways

!!! notes "Notes to take"
    - **Solved exactly.** k-NN, Naive Bayes and linear or ridge regression. Retrieval stores are solved too, as long as every copy is
      tracked.
    - **Solved by design.** SISA or scheduled retraining, planned before training.
    - **Works with an audit.** Approximate methods for neural networks, never trusted without one.
    - **Lesson 19.** Of 14 methods only retraining passed all 3 requests, and no approximate method forgot Carol.
    - **Recipe trap.** A privacy test can be fooled by lower confidence. Put the references through the method too.
    - **Benchmarks.** Competition, TOFU, MUSE and WMDP each fix one part of the problem. None is a proof.
    - **Open.** Proof, robustness, the target in LLMs, scale and legal acceptance.
    - **Scale.** A Hessian for 85,002 weights needs about 57.8 GB, so exact Newton steps stop at linear models.

## Quiz

```quiz
- q: Which setting is solved exactly today?
  options:
    - Unlearning one fact from a large language model
    - Removing a row from a Naive Bayes model
    - Proving a neural network has forgotten
  answer: 1
  why: Naive Bayes is built from counts and sums, so forgetting is a subtraction.
- q: What does the TOFU benchmark use to test LLM unlearning?
  options:
    - Real people's medical records
    - Biographies of fictional authors
    - Images of faces
  answer: 1
  why: Fictional authors cannot leak in from other training data, so any remaining knowledge came from the fine-tune.
- q: Which of these is still an open problem?
  options:
    - Proving that a neural network has forgotten
    - Deleting a document from a vector store
    - Downdating ridge regression
  answer: 0
  why: Tests can show remembering, but outside exact and certified methods, nobody can prove forgetting yet.
- q: In Lesson 19, how many of the fourteen methods passed all three requests?
  options:
    - Five
    - One, retraining
    - None
  answer: 1
  why: Only retraining passed Carol, the class and the random request. SISA passed two and missed Carol by one digit.
- q: Why did five methods seem to pass the random request in Lesson 19 at first?
  options:
    - They forgot the random users completely.
    - The random request was too easy for every method.
    - They lowered the model's confidence everywhere, which the privacy test read as forgetting.
  answer: 2
  why: With references put through the same method, as Hayes et al. (2024) do, those passes went away.
- q: What does "works, with an audit" mean for approximate methods on neural networks?
  options:
    - A method may be used on a request when an audit fixed in advance says it passed there.
    - Most approximate methods pass most requests.
    - The method is exact once it has been audited once.
  answer: 0
  why: In Lesson 19 most approximate methods passed nothing. The audit is what tells you whether one worked this time.
- q: Why are exact Newton updates not used on deep networks?
  options:
    - They are less accurate than gradient ascent.
    - The Hessian grows with the square of the weights, about 57.8 GB for the course's 85,002-weight network.
    - Deep networks have no gradient.
  answer: 1
  why: For a billion weights the Hessian would need about 8 billion GB, so deep models use SISA, retraining or audited approximate methods.
- q: A company uses an exact method on its model. Is the person's data now gone from the company?
  options:
    - Not necessarily, because backups, logs, caches and other models can still hold copies.
    - Yes, an exact method removes every copy.
    - Only if the model is a language model.
  answer: 0
  why: Solved is about one model. Every copy in the system needs its own deletion, which the enterprise playbook tracks.
```

## Try it

!!! levelup "Level up"
    You can now place any model on the map of what is solved, what needs an audit and what is open. Next quest, the
    [lessons](../lessons/index.md), where you run every result on this page for yourself in a notebook.

- Go back over [the Ladder of Forgetting](ladder-of-forgetting.md). Each rung matches a row of the first table.
- Try the [practice problems](../practice.md) and the [scenarios](../scenarios.md).
