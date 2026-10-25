---
title: "Lesson 16: LLM unlearning, facts not rows"
description: Make a language model forget a phone number it can recite, and use prefix forcing, exposure and relearning to tell removal from suppression.
---

# Lesson 16: LLM unlearning, forgetting a fact the model can recite

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~50 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 10</span></div>

<div class="buttons" markdown>
[:simple-googlecolab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb){ .md-button }
</div>

## The story

A fictional company fine-tunes an internal assistant on its staff directory. Dana Reyes leaves and asks for her personal
data, including her phone number, to be erased. Ask the model "dana reyes" and it answers `555-0183`. (All numbers are
in the 555-0100 to 555-0199 range reserved for fiction.) This is where the gap between **looking forgotten** and **being
forgotten** is widest.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** an n-gram model (counts) and a neural model (pre-trained, then fine-tuned on the directory).</li>
<li markdown>**Show the issue**: extraction and **exposure** (the rank of her real number among all 100).</li>
<li markdown>**Untrain** the n-gram model exactly by subtracting counts.</li>
<li markdown>**Untrain** the neural model with every method, namely exact re-fine-tuning, gradient ascent, NPO and refusal training.</li>
<li markdown>**Prove it** with prefix forcing and the relearn attack.</li>
</ol>

## Key results

Before unlearning, the fine-tuned model recited her number and all 19 colleagues' numbers. Exposure: **6.64 bits**,
the maximum (her number was its top guess). The n-gram model unlearnt exactly, identical to one that never saw her.

| Method | Says | Exposure | Rank | Colleagues recited |
|---|---|---|---|---|
| Never saw Dana (band) | — | 0.23 ± 0.11 | — | 19 |
| Re-fine-tune without Dana (exact) | gibberish | 0.25 | 84 | 19 |
| Gradient ascent | gibberish | 0.01 | **99** | **0** |
| Gradient ascent + retain | gibberish | 0.01 | 99 | 2 |
| NPO + retain | gibberish | 0.30 | 81 | 19 |
| **Refusal training** | "(withheld)" | **6.64** | **1** | 19 |

- **Gradient ascent** made her real number the model's *least* likely candidate and wiped out colleagues' numbers,
  because they all share the `555-01` prefix.
- **Refusal training** said "(withheld)", but given "dana reyes 555-01" it completed `83`, her real ending. That is
  **suppression**.

**The relearn attack** (exposure after N steps of training on colleagues' lines only):

| Method | 0 | 5 | 20 | 50 | 100 |
|---|---|---|---|---|---|
| Re-fine-tune (exact) | 0.25 | 0.29 | 0.25 | 0.27 | 0.30 |
| NPO + retain | 0.30 | 0.45 | 1.00 | 1.74 | 1.79 |
| Refusal training | 6.64 | 6.64 | 5.64 | 5.64 | 5.64 |

NPO passed every direct test, then partly came back (rank about 80 → about 30). Only the exact method stays flat.

## Concepts used here

- [Language models](../ml-basics/language-models.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)

## Quiz

```quiz
- q: What does an exposure of 6.64 bits mean here?
  options:
    - Her real number is the model's top guess among 100.
    - Her number is ranked randomly.
    - The model has never seen her.
  answer: 0
  why: Exposure is log2(100) − log2(rank); rank 1 gives the maximum.
- q: How did the n-gram model forget Dana?
  options:
    - Exactly, by subtracting her line's counts
    - By refusal training
    - By gradient ascent
  answer: 0
  why: An n-gram model is a table of counts, the same summation trick as Lesson 01.
- q: Why did gradient ascent damage colleagues' numbers?
  options:
    - They all share the 555-01 prefix.
    - They asked to be deleted too.
    - It deleted the directory.
  answer: 0
  why: Pushing her number away pushed away the shared habit of all numbers.
- q: The refusal model says "(withheld)". What did prefix forcing show?
  options:
    - It still completed her real number.
    - It refused again.
    - It forgot everyone.
  answer: 0
  why: Refusal changed what the model says, not what it knows. Its exposure stayed at the maximum.
- q: Under the relearn attack, which method stayed flat?
  options:
    - The exact re-fine-tune
    - NPO + retain
    - Refusal training
  answer: 0
  why: For a model that never saw the fact, there is nothing to come back.
```

## Open question → Lesson 17

We now have methods and audits for rows, people, classes, poison, customers and facts. How does a company run all of
this as one process, and sign it off before the legal deadline?

<div class="buttons" markdown>
[:simple-pytorch: Optional: Lesson 16b, the same in PyTorch](16b-llm-unlearning-pytorch.md){ .md-button }
[Next: Lesson 17, the enterprise playbook :material-arrow-right:](17-enterprise-playbook.md){ .md-button }
</div>
