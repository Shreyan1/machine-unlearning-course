---
title: State of the field
description: What works today, how methods are compared and the open problems in machine unlearning.
---

# State of the field

!!! oneline "In one line"
    Exact unlearning is solved for classical models and by design; approximate unlearning for neural networks works on
    benchmarks but without guarantees; unlearning in large language models is still an open problem.

## Why it matters

Machine unlearning moves fast, and claims run ahead of evidence. Knowing what is solved, what is promising and what is
open helps you choose a method and set expectations with lawyers and leaders. It also helps you spot a claim that is
too good to be true. This page is the map at the end of the course; each row links to the page that explains it.

## A simple example

Think of medicine. Some illnesses have a reliable cure, some have treatments that usually work but must be checked
with tests, and some are still being researched. Unlearning has all three.

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

### How methods are compared

- **The NeurIPS 2023 unlearning competition** asked about 1,200 teams to make a face-based age predictor forget, and
  scored them with a formal definition of forgetting plus a check on usefulness. The best entries beat the methods
  published before it (Triantafillou et al. 2024).
- **TOFU** fine-tunes a language model on made-up author biographies, then asks it to forget some authors. Because the
  authors are fictional, nothing else in the training data can leak them.
- **MUSE** tests six things people want from LLM unlearning, from removing verbatim text to keeping the model useful.
- **WMDP** measures hazardous knowledge, such as biosecurity and cybersecurity, that a model should not be able to
  provide.

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

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting a benchmark score alone.** A method can top a benchmark and still fail a relearning or compression test.
    - **Assuming LLM unlearning works like classifier unlearning.** Facts are not rows, and the gold band is much harder
      to build.
    - **Ignoring the solved cases.** Many real systems have classical or retrieval parts where exact deletion is cheap.

## Key takeaways

- Exact unlearning is solved for classical models and retrieval stores, and by design with SISA.
- Approximate unlearning for neural networks works when audited against a gold band.
- LLM unlearning, proof of forgetting and robustness to relearning are open problems.
- Benchmarks such as TOFU, MUSE and WMDP help compare methods, but none is a proof.

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
```

## Try it

- Go back over [the Ladder of Forgetting](ladder-of-forgetting.md). Each rung matches a row of the first table.
- Try the [practice problems](../practice.md) and the [scenarios](../scenarios.md).
