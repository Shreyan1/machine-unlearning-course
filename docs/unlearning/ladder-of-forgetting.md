---
title: The Ladder of Forgetting
description: The map of the course, from models where forgetting is a subtraction to language models where nobody can yet do it reliably.
---

# The Ladder of Forgetting

!!! oneline "In one line"
    The Ladder of Forgetting orders models from **easy to forget** (a subtraction) to **hard to forget** (large
    language models), and each rung explains what makes the next one harder.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - place any model on the ladder by asking which of the three handles it gives you,
    - follow Carol up the ladder and say what forgetting her costs on each rung,
    - pick the cheapest exact tool for a system that mixes classical and neural parts.

## Why it matters

The lessons are not a random list of topics. They are one argument, built rung by rung, *forgetting gets harder as
models get more powerful, and the cure is mostly designing for deletion before training.* Knowing the ladder tells you
where any new problem fits, and which tools are likely to work.

Each lesson starts from the limit the one before it ran into, and climbs one step. Lesson 01 forgets Carol with a
subtraction. Lesson 04 shows that a neural network allows no subtraction at all. Lessons 06 to 11 rebuild the ability
to forget in a network, first exactly and then cheaply with checks. Lesson 16 reaches language models, where nobody can
yet do it reliably.

The ladder is also a tool for real work. When a request arrives, the first question is not "which clever method?" It
is "which rung is this model on?" The answer tells you whether forgetting can be exact, what it will cost and whether
you will need an audit.

## A simple example

Think of removing an ingredient from different dishes.

- From a **fruit salad**, you pick the strawberries out. Easy. (K-NN, Naive Bayes.)
- From a **layered cake**, you remove one layer and rebuild the top. Some work. (Random forests, SISA.)
- From a **soup**, the flavour is everywhere. You can only make a new soup or try to mask the taste. (Neural networks,
  language models.)

The three dishes match the three kinds of model. In the salad, each piece stays separate, just as k-NN keeps every
training row. In the cake, each layer is its own part, just as each tree in a forest or each shard in SISA saw only some
of the data. In the soup, every ingredient has mixed into every spoonful, just as every training example nudges every
weight of a network. "Masking the taste" is what refusal training does to a language model, which is why the top rung
is still an open problem.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Ladder of Forgetting](../start-here/glossary.md#l) | The map of the course, from easy to forget to hard to forget | Rung 1 is k-NN, rung 10 is language models |
| Rung | One step of the ladder, usually one or a few lessons | Rung 4 is Lessons 04 and 05 |
| Level | One of five groups of rungs, one per family of models, used by your progress climb | "SVMs and forests" |
| Handle | A property of a model that makes forgetting exact and cheap | A sum, a single best answer or locality |
| [Summation form](../start-here/glossary.md#s) | A model built from sums over the data, so one example's part can be subtracted | Naive Bayes keeps counts and averages per class |
| [Locality](../start-here/glossary.md#l) | Only some parts of a model depend on a given point | Each tree in a forest saw only some rows |
| Designing for deletion | Building a model before training so that forgetting will be cheap later | SISA shards, adapters and checkpoints |
| Open problem | A question nobody can yet answer reliably | Forgetting a fact inside a language model |

## How it works

<!-- diagram: ladder-of-forgetting -->

The figure shows five blocks, each a family of models, rising from left to right. Green blocks are exact and cheap,
yellow blocks are possible with care, and the red block is an open problem. The dashed line along the top runs from
"easy to forget exactly" to "hard to forget at all". The figure labels the blocks rung 1 to rung 5. They are the five
levels of your climb, and the table below splits them into finer rungs.

**Your climb so far.** The ladder doubles as your progress map. Its rungs are grouped into five levels, one for each family of models, and you climb a level by passing the quizzes on its pages. [See which pages count](../quizzes/progress.md#your-climb).

<div class="ladder-climb" markdown></div>

| Rung | Lessons | What makes forgetting possible | Guarantee |
|---|---|---|---|
| 1 | 01 · k-NN, Naive Bayes | The model *is* the data or a sum. Delete rows or subtract their contribution. | Exact, free |
| 2 | 02 · Ridge, logistic regression | Downdate the sums or take a Newton step towards the optimum. | Exact, then approximate |
| 3 | 03 · SVM, random forest | **Locality.** Only some parts depend on a point | Exact, partial cost |
| 4 | 04-05 · Neural networks | Every training point can affect every weight. | The problem |
| 5 | 06-07 · Retrain, SISA | Retraining, or **designing** locality in with shards | Exact, planned |
| 6 | 08-10 · Approximate methods | Cheap updates with no guarantee | Must be audited |
| 7 | 11 · The audit | Evidence against a gold band | Proof |
| 8 | 12-14 · Fairness, consent, poison | The same tools in real Responsible AI settings | Classical first, then deep |
| 9 | 15 · Fine-tuning, LoRA | Adapters and checkpoints | Exact by design |
| 10 | 16 · Language models | Facts as habits; refusal is not forgetting | Open problem |
| 11 | 17 · The playbook | Track lineage, make decisions, certify and re-verify. | Engineering |
| 12+ | 18-22 · Extensions | Recommenders, the method zoo, scale, RAG, weight editing | Extensions |

The table reads in four parts. **Rungs 1 to 3** each give you a handle, so forgetting is exact. **Rung 4** is the
turning point, where a neural network takes every handle away. **Rungs 5 to 7** are the three answers to that, which are
to retrain or design locality back in, to use a cheap approximate method, and to audit whatever you did. **Rungs 8 to
12** take the same tools into real settings, from consent and poisoned data to fine-tunes, language models and
production.

The five levels of the climb group the rungs by family of models.

| Level | Family | How forgetting works |
|---|---|---|
| 1 | k-NN and Naive Bayes | Subtract the data exactly |
| 2 | Linear and logistic | A closed-form update |
| 3 | SVMs and forests | Rebuild the affected part |
| 4 | Neural networks | Approximate, then audit |
| 5 | Language models | Facts, not rows (unsolved) |

SISA counts towards level 3, not level 4. It is a neural network, but it forgets by rebuilding the affected part, the
same idea as retraining one tree of a forest.

??? checkpoint "Checkpoint 1 · A shop's system keeps a k-NN index of customer records and passes the results to a neural ranking model. A customer asks to be erased. Where do you start?"
    **With the index, on rung 1.** Deleting the customer's rows from a k-NN index is exact and almost free. The ranking
    network sits on rung 4, so it needs retraining, a design such as SISA or an approximate method with an audit. Use
    the cheapest exact tool for each part, and do not treat the whole system as the hardest rung.

### The three "handles"

Classical models give you a handle for forgetting. Neural networks take all three away.

| Handle | Where it works | Why neural networks lose it |
|---|---|---|
| A **sum** you can subtract | Naive Bayes, k-NN, ridge | The weights are the end of a long path of steps |
| A **single best answer** to step to | Ridge, logistic regression | Many equally good answers exist |
| **Locality** | SVM, random forest | Every example nudges every weight |

**A sum.** If a model stores counts or totals, each person's part was added in, so it can be taken out again. That
is why the lowest rung is free.

**A single best answer.** If a model's training always lands on one best answer, you can calculate where it would land
without the data and step there. Ridge regression lands exactly. Logistic regression lands very close.

**Locality.** If only some parts of a model saw a point, you only rebuild those parts. A forest of 50 trees in which
Carol reached 10 needs 10 trees retrained, not 50.

??? deep "Go deeper · how a neural network loses each handle, in numbers"
    Lesson 04 tests each handle on the course's network of 85,002 weights.

    - **No sum.** Training the network with and without Carol from the same seed changes 94.1% of the weights. She
      is not stored anywhere in particular, so there is nothing to subtract.
    - **No single best answer.** A Newton step needs a table of 85,002 × 85,002 numbers, about 29 GB. Worse, two
      networks trained on the same data with different seeds sit at distance 50.96, while the with-Carol and
      without-Carol pair sit at 9.87. There are many equally good answers, so there is no one point to step towards.
    - **No locality.** Since 94.1% of the weights move, she touched almost everything. Locality comes back only if you
      build it in, as SISA does.

## A worked example

Follow Carol up the ladder. On each rung, the question is the same. What does it take to make the model act as if
it never saw her 40 digits?

1. **Rung 1, Naive Bayes.** Subtract her counts. Her accuracy goes from 60.0% to 27.5%, the same as a model that never
   saw her, and the largest difference in predicted log-probability is exactly 0. The k-NN model matches a model that
   never saw her on 100% of 1,877 inputs.
2. **Rung 2, ridge and logistic regression.** A downdate removes her from ridge exactly. Carol goes from 95.0% to
   45.0%, the same as a refit. For logistic regression one Newton step closes 94.8% of the gap to retraining and moves
   her from 92.5% to 60.0%, close to the retrained 62.5%. Exact turns into approximate.
3. **Rung 3, SVMs and forests.** In a forest built from bootstrap bags, her 40 rows reached all 50 trees. With
   user-aware shards they reached 10. Retraining those 10 matched a forest built from scratch without her.
4. **Rung 4, the neural network.** No handle is left. The first exact answer, retraining (rung 5), works. Here it
   takes 0.27 seconds, but for a large model it would be very costly.
5. **Rung 5, SISA.** With user-aware shards, forgetting Carol costs 5.0% of a full retrain, and every weight matches a
   SISA model trained without her.
6. **Rungs 6 and 7, approximate methods and the audit.** Against her band of 62.7% ± 9.5% in Lesson 11, SCRUB+R passes
   at 65.0%. Plain SCRUB fails at 82.5% because it still remembers her, and NegGrad+ fails at 10.0% because it forgot
   too much.
7. **Rung 10, language models.** The course swaps Carol for Dana, whose phone number a model memorised. Refusal
   training makes the model say "(withheld)", yet given the start of her number it still completes the real ending.
   The fact was hidden, not removed.

## What the lessons found

<div class="stats">
<div class="is-good"><strong>0</strong><span>largest difference after subtracting Carol from Naive Bayes, rung 1</span></div>
<div class="is-good"><strong>10 of 50</strong><span>trees to retrain for Carol with user-aware shards, rung 3</span></div>
<div class="is-bad"><strong>94.1%</strong><span>of a network's weights change when Carol is removed, rung 4</span></div>
<div class="is-good"><strong>5.0%</strong><span>of a retrain to forget Carol with user-aware SISA, rung 5</span></div>
</div>

The pattern is the point. Lower rungs forget exactly for almost nothing. The network on rung 4 forgets exactly only at
full price. Rung 5 wins exactness back cheaply, but only because the design was chosen before training.

??? checkpoint "Checkpoint 2 · A team cannot afford to retrain its network for every request. Which two rungs offer a way out, and what is the catch with each?"
    **Rung 5 and rung 6.** SISA on rung 5 is exact and cheap, at 5.0% of a retrain for Carol, but it must be planned
    before training. Approximate methods on rung 6 work on any trained model, but they give no guarantee. So their
    results must pass the audit on rung 7, and in Lesson 11 plain SCRUB and NegGrad+ did not.

## Limits

**The ladder is a simplification.** Real systems mix rungs. A product may have a k-NN index, a scaler, a neural network
and a language model, each on its own rung.

**The numbers come from one small setting.** They use 8 × 8 digit images, a 40-digit forget set and small models. The
order of the rungs carries over, but the costs on a large system will be different.

**Exact does not mean free of side effects.** Removing Carol from Naive Bayes was exact, yet it made the model worse
for everyone who writes like her, from 61.3% to 37.5% on look-alike digits, because she was the only source of that
style.

**The progress climb counts quizzes.** Passing a level's quizzes shows you have read and understood its pages. Running
the notebooks is what makes the ideas stick.

!!! tip "What to do in practice"
    - For each model in a system, write down which rung it sits on before you choose a method.
    - Use the cheapest exact tool that fits each part, such as deleting rows or subtracting counts.
    - Remember the whole pipeline. In Lesson 01 a scaler's stored mean moved when Carol was removed.
    - For new networks, decide before training whether to plan for deletion with shards, adapters or checkpoints.
    - Treat anything on rung 6 as a claim to check on rung 7.

## Common mistakes

!!! danger "Mistakes people make"
    - **Jumping to the top rung.** Many real systems have classical parts (indexes, counts, scalers) where exact
      forgetting is easy. Use the cheapest exact tool that fits.
    - **Thinking higher rungs are hopeless.** Designing for deletion (shards, adapters, checkpoints) brings exactness
      back, if you plan before training.
    - **Taking "approximate" as "nearly exact".** On rung 6 the result can miss in either direction, as SCRUB and
      NegGrad+ did, so only the audit can tell.
    - **Treating refusal as forgetting.** On rung 10 a model that says "(withheld)" can still complete the secret.

??? checkpoint "Checkpoint 3 · A language model is trained to refuse whenever it is asked for Dana's number. Which rung is this, and has it forgotten her?"
    **Rung 10, and no.** Refusal training changes what the model says, not what it knows. Given the start of Dana's
    number, the model still completed her real ending. That is suppression, which is why the top rung is still an
    open problem.

## Key takeaways

!!! notes "Notes to take"
    - **The ladder.** Models ordered from easy to forget to hard to forget, in 12 rungs and 5 levels.
    - **Three handles.** A sum, a single best answer and locality. Each makes forgetting exact.
    - **Rungs 1 to 3.** Subtract a sum, step to the one best answer or rebuild only the parts a point touched.
    - **Rung 4.** A network loses all three handles. Removing Carol moves 94.1% of its weights.
    - **Rungs 5 to 7.** Retrain or design locality in, approximate cheaply, then audit.
    - **Design pays.** User-aware SISA forgot Carol for 5.0% of a retrain, exactly.
    - **Top rung.** Language models, where refusal is not forgetting. Still an open problem.
    - **Trap.** Jumping to the top rung when parts of the system have an exact, cheap fix.

## Quiz

```quiz
- q: Which models sit on the lowest rung, where forgetting is exact and almost free?
  options:
    - Large language models
    - k-NN and Naive Bayes
    - Neural networks
  answer: 1
  why: k-NN stores the data and Naive Bayes stores sums, so forgetting is a deletion or a subtraction.
- q: Which property makes forgetting cheap for SVMs and random forests?
  options:
    - Locality
    - Their huge size
    - Gradient ascent
  answer: 0
  why: Only some parts of these models depend on any given point, so only those parts need work.
- q: Why are neural networks "the problem" rung?
  options:
    - They have no sum, no single best answer and no locality.
    - They are too small.
    - They cannot be retrained.
  answer: 0
  why: Every example nudges every weight, and there are many equally good solutions.
- q: What is the main cure for the hard rungs, according to the course?
  options:
    - Designing for deletion before training
    - Making models bigger
    - Ignoring deletion requests
  answer: 0
  why: Shards, adapters and checkpoints bring exactness back, but they must be planned in advance.
- q: For logistic regression, one Newton step closed 94.8% of the gap to retraining. What does that show about rung 2?
  options:
    - Logistic regression cannot be unlearnt at all.
    - The Newton step is exact for every model.
    - Its single best answer lets a step land very close, but not exactly on it.
  answer: 2
  why: Ridge's loss is a perfect bowl, so its update is exact. Logistic regression's is only roughly a bowl, so the step lands near the answer.
- q: In a forest with user-aware shards, how many of the 50 trees had to be retrained to forget Carol?
  options:
    - 10
    - All 50
    - None
  answer: 0
  why: Locality means only the trees that saw her need work. User-aware shards kept her in 10 trees.
- q: An approximate method on rung 6 finishes in seconds. What must happen before you trust it?
  options:
    - Nothing, because it ran without errors
    - Pass the audit on rung 7, against a band of models retrained without the data
    - Retrain the model anyway and throw the result away
  answer: 1
  why: Approximate methods have no guarantee. In Lesson 11, plain SCRUB still remembered Carol and NegGrad+ forgot too much.
- q: Why does SISA count towards the "SVMs and forests" level of the climb rather than "Neural networks"?
  options:
    - SISA does not use neural networks.
    - It forgets by rebuilding only the affected part, the same idea as retraining one tree.
    - It is an approximate method.
  answer: 1
  why: SISA designs locality into a network with shards, so it forgets the way a sharded forest does, exactly and in part.
```

## Try it

!!! levelup "Level up"
    You can now place any model on the ladder and pick the cheapest exact tool for it. Next quest,
    [Retraining, the gold standard](retraining-gold-standard.md), the one exact answer that works on every rung.

- Read the next concept, [Retraining, the gold standard](retraining-gold-standard.md).
- The lesson [00 · Read this first](../lessons/00-read-first.md) ends with the ladder.
- See which pages climb each level on [Your progress](../quizzes/progress.md#your-climb).
