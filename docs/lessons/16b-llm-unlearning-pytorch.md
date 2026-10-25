---
title: "Lesson 16b · LLM unlearning in PyTorch"
description: Repeat Lesson 16 on a small GPT-style transformer in PyTorch, and check which conclusions carry over.
---

# Lesson 16b (optional) · The same lesson on a transformer, in PyTorch

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 10 · optional</span><span class="chip" markdown="span">:simple-pytorch: Needs PyTorch</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16b-LLM-Unlearning-PyTorch.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/16b-LLM-Unlearning-PyTorch.ipynb){ .md-button }
</div>

## The story

A fair objection to Lesson 16 is, "Real LLMs are transformers. Does it still hold?" This lesson repeats the core experiment
on a small GPT-style transformer (`TinyCharLM`, 2 blocks, 4 attention heads, 236,015 parameters), using PyTorch instead
of hand-written gradients. Same company, same directory, same Dana, same tests.

To run it locally, install the optional requirements first.

```bash
pip install -r requirements-optional.txt
```

## What you will do

<ol class="steps" markdown>
<li markdown>**Train**: pre-train on generic text, then fine-tune on the directory.</li>
<li markdown>**Show the issue**: extraction, exposure and colleagues' numbers.</li>
<li markdown>**Untrain** with exact re-fine-tuning, gradient ascent + retain, NPO + retain and refusal training.</li>
<li markdown>**Show the result** against models that never saw Dana.</li>
<li markdown>**Prove it** with prefix forcing and the relearn attack.</li>
</ol>

## Key results

Before unlearning, the model recited `555-0183` with exposure 6.64, and recited all 19 colleagues' numbers. Models that never saw Dana had
exposure between 0.47 and 1.03.

| Method | Says | Exposure | Rank | Colleagues |
|---|---|---|---|---|
| Re-fine-tune without Dana (exact) | 555-0106 | 0.69 | 62 | 19 |
| Gradient ascent + retain | (nothing) | 0.01 | 99 | 0 |
| NPO + retain | 555-0142 | 1.47 | 36 | 19 |
| Refusal training | "(withheld)" | **6.64** | **1** | 19 |

**Relearn attack** (exposure after N steps on colleagues' lines).

| Method | 0 | 10 | 30 | 60 |
|---|---|---|---|---|
| Re-fine-tune (exact) | 0.69 | 0.74 | 0.51 | 0.67 |
| NPO + retain | 1.47 | 3.32 | 3.32 | 3.84 |
| Refusal training | 6.64 | 4.32 | 4.32 | 4.64 |

The ordering held, and the relearn effect was even sharper than on the NumPy model. After 60 steps on *other people's*
lines, NPO pushed her number back towards the top ten.

!!! tip "What carries over"
    Exact numbers depend on the architecture. What does **not** change is this. Exact methods stay flat under attack, refusal is suppression and approximate methods must be judged by attacks, not by the forget prompt. Benchmarks such as TOFU,
    MUSE and WMDP package the same ideas at full LLM scale.

## Concepts used here

- [Language models](../ml-basics/language-models.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)

## Quiz

```quiz
- q: What kind of model does Lesson 16b use?
  options:
    - A small GPT-style transformer
    - A random forest
    - An n-gram table
  answer: 0
  why: TinyCharLM has 2 transformer blocks and 4 attention heads.
- q: Did refusal training remove Dana's number on the transformer?
  options:
    - No; exposure stayed at the maximum.
    - Yes, completely.
  answer: 0
  why: Suppression behaves the same way regardless of the architecture.
- q: Which method stayed flat under the relearn attack?
  options:
    - The exact re-fine-tune
    - NPO + retain
    - Refusal training
  answer: 0
  why: Only the exact method has nothing to bring back.
- q: What is the main lesson of 16b?
  options:
    - The conclusions of Lesson 16 do not depend on the architecture.
    - Transformers cannot memorise.
    - PyTorch makes unlearning exact.
  answer: 0
  why: The ordering of methods held on a transformer.
```

## Next → Lesson 17

Back to the main path. How does a company run all of this as one process?

[On to Lesson 17, the enterprise playbook :material-arrow-right:](17-enterprise-playbook.md){ .md-button }
