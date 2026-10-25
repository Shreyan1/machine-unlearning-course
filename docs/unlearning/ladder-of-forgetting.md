---
title: The Ladder of Forgetting
description: The map of the course, from models where forgetting is a subtraction to language models where nobody can yet do it reliably.
---

# The Ladder of Forgetting

!!! oneline "In one line"
    The Ladder of Forgetting orders models from **easy to forget** (a subtraction) to **hard to forget** (large
    language models), and each rung explains what makes the next one harder.

## Why it matters

The lessons are not a random list of topics. They are one argument, built rung by rung, *forgetting gets harder as
models get more powerful, and the cure is mostly designing for deletion before training.* Knowing the ladder tells you
where any new problem fits, and which tools are likely to work.

## A simple example

Think of removing an ingredient from different dishes.

- From a **fruit salad**, you pick the strawberries out. Easy. (K-NN, Naive Bayes.)
- From a **layered cake**, you remove one layer and rebuild the top. Some work. (Random forests, SISA.)
- From a **soup**, the flavour is everywhere. You can only make a new soup or try to mask the taste. (Neural networks,
  language models.)

## How it works

<!-- diagram: ladder-of-forgetting -->

| Rung | Lessons | What makes forgetting possible | Guarantee |
|---|---|---|---|
| 1 | 01 · k-NN, Naive Bayes | The model *is* the data or a sum. Delete rows or subtract their contribution. | Exact, free |
| 2 | 02 · Ridge, logistic regression | Downdate the sums or take a Newton step toward the optimum. | Exact, then approximate |
| 3 | 03 · SVM, random forest | **Locality**: only some parts depend on a point | Exact, partial cost |
| 4 | 04-05 · Neural networks | Every training point can affect every weight. | The problem |
| 5 | 06-07 · Retrain, SISA | Retraining, or **designing** locality in with shards | Exact, planned |
| 6 | 08-10 · Approximate methods | Cheap updates with no guarantee | Must be audited |
| 7 | 11 · The audit | Evidence against a gold band | Proof |
| 8 | 12-14 · Fairness, consent, poison | The same tools in real Responsible AI settings | Classical first, then deep |
| 9 | 15 · Fine-tuning, LoRA | Adapters and checkpoints | Exact by design |
| 10 | 16 · Language models | Facts as habits; refusal is not forgetting | Open problem |
| 11 | 17 · The playbook | Track lineage, make decisions, certify and re-verify. | Engineering |
| 12+ | 18-20 · Extensions | Recommenders, the method zoo, scale | Extensions |

### The three "handles"

Classical models give you a handle for forgetting. Neural networks take all three away.

| Handle | Where it works | Why neural networks lose it |
|---|---|---|
| A **sum** you can subtract | Naive Bayes, k-NN, ridge | The weights are the end of a long path of steps |
| A **single best answer** to step to | Ridge, logistic regression | Many equally good answers exist |
| **Locality** | SVM, random forest | Every example nudges every weight |

## Common mistakes

!!! danger "Mistakes people make"
    - **Jumping to the top rung.** Many real systems have classical parts (indexes, counts, scalers) where exact
      forgetting is easy. Use the cheapest exact tool that fits.
    - **Thinking higher rungs are hopeless.** Designing for deletion (shards, adapters, checkpoints) brings exactness
      back, if you plan before training.

## Key takeaways

- At lower rungs, forgetting is exact and cheap because the model is a sum, a formula or local.
- Neural networks lose all three handles, so the options are retraining, design or approximation plus audit.
- The cure for the hard rungs is mostly **designing for deletion** before training.

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
```

## Try it

- Read the next concept, [Retraining, the gold standard](retraining-gold-standard.md).
- The lesson [00 · Read this first](../lessons/00-read-first.md) ends with the ladder.
