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

!!! mission "Your mission · about 30 minutes · 3 checkpoints"
    By the end of this lesson you can

    - run Lesson 16's tests on a small transformer written in PyTorch,
    - read each method's result against four models that never saw Dana,
    - say which conclusions depend on the architecture and which do not.

## The story

A fair objection to Lesson 16 is, "Real LLMs are transformers. Does it still hold?" This lesson repeats the core experiment
on a small GPT-style transformer (`TinyCharLM`, 2 blocks, 4 attention heads, 236,015 parameters), using PyTorch instead
of hand-written gradients. Same company, same directory, same Dana, same tests.

The stakes are about trust. If refusal stopped being suppression on a transformer, or NPO stopped coming back, Lesson
16 would be a fact about one small NumPy model and not a lesson about language models. If the order of the methods
holds on a different architecture, with a different optimiser and training budget, it is worth relying on.

To run it locally, install the optional requirements first.

```bash
pip install -r requirements-optional.txt
```

## What you will do

<ol class="steps" markdown>
<li markdown>**Train.** Pre-train on generic text, then fine-tune on the directory.</li>
<li markdown>**Show the issue.** Extraction, exposure and colleagues' numbers.</li>
<li markdown>**Untrain** with exact re-fine-tuning, gradient ascent + retain, NPO + retain and refusal training.</li>
<li markdown>**Show the result** against models that never saw Dana.</li>
<li markdown>**Prove it** with prefix forcing and the relearn attack.</li>
</ol>

## What each step teaches

**Step 1. Pre-train and fine-tune.** The transformer is pre-trained for 800 steps on random 33-character windows of
everyday text, then fine-tuned for 300 steps on the directory with everyday text mixed in. Each directory line starts
at position 0 after a newline. That matters, because a transformer's position embeddings make "dana reyes" at
position 1 and at position 20 different inputs.

**Step 2. The same measurements.** Extraction, prefix forcing, exposure over all 100 numbers, colleagues recited and
the loss on everyday text, written again for PyTorch. The pre-trained model ranks her number 44th (1.18 bits) and
recites no one. The fine-tuned model ranks it 1st.

**Step 3. The four methods with autograd.** Gradient ascent and NPO each run 30 steps on the characters of her number
only, with a retain loss on the colleagues' lines and everyday text. Refusal training runs 60 steps on "dana reyes
(withheld)" mixed with the colleagues' lines.

??? deep "Go deeper · the NPO loss written for autograd"
    With PyTorch there is no hand-written gradient, so NPO is written as a loss. Let \(\Delta\) be the
    log-probability of her number under the current model minus that under the original. The loss is

    \[ L = -\frac{2}{\beta} \log \sigma(-\beta \Delta) \]

    with \(\beta = 1\). Its gradient is gradient ascent on her number weighted by \(2\sigma(\beta\Delta)\), the same
    fading weight as in Lesson 16. Gradient ascent is simply the negative of her number's loss. Both add the same
    retain loss, the colleagues' lines plus half-weighted everyday text.

**Step 4. The reference.** Four models fine-tuned without her line, seeds 100 to 103, give exposures of 0.47, 1.03,
0.47 and 0.51 bits, and all recite 19 colleagues. Every method is read against that range.

**Step 5. The attacks.** Prefix forcing as before, then the relearn attack, training on colleagues' lines only for 10,
30 and 60 steps.

## Key results

Before unlearning, the model recited `555-0183` with exposure 6.64, and recited all 19 colleagues' numbers. Models that never saw Dana had
exposure between 0.47 and 1.03.

| Method | Says | Exposure | Rank | Colleagues |
|---|---|---|---|---|
| Re-fine-tune without Dana (exact) | 555-0106 | 0.69 | 62 | 19 |
| Gradient ascent + retain | (nothing) | 0.01 | 99 | 0 |
| NPO + retain | 555-0142 | 1.47 | 36 | 19 |
| Refusal training | "(withheld)" | **6.64** | **1** | 19 |

<div class="stats">
<div class="is-good"><strong>0.69 bits</strong><span>exact re-fine-tune, inside the never-saw-her range</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>refusal training, her number still the top guess</span></div>
<div class="is-bad"><strong>1.47 → 3.84</strong><span>NPO's exposure after 60 relearn steps</span></div>
</div>

Read the rows against the range of 0.47 to 1.03 bits. **The exact re-fine-tune** lands inside it at 0.69 and answers
with a colleague's number, `555-0106`, which is the habit a never-saw-her model has. **Gradient ascent + retain**
writes nothing at all, ranks her number last and leaves no colleagues. Its loss on everyday text rose from 1.87 to
3.14, so it broke the model. **NPO + retain** keeps every colleague, but at 1.47 bits it is already above the range
before any attack. **Refusal training** says "(withheld)", yet under prefix forcing it writes `83`, her real ending.

??? checkpoint "Checkpoint 1 · NPO ranked her number 36th, exposure 1.47 bits. The never-saw-her models gave 0.47 to 1.03. Did NPO pass?"
    **No, it was already a little above the range.** 1.03 bits is about rank 49, and 36 is closer to the top than
    that. On the NumPy model in Lesson 16, NPO landed inside the band before the attack. Here it misses even the direct
    test, by a small margin.

**Relearn attack** (exposure after N steps on colleagues' lines).

| Method | 0 | 10 | 30 | 60 |
|---|---|---|---|---|
| Re-fine-tune (exact) | 0.69 | 0.74 | 0.51 | 0.67 |
| NPO + retain | 1.47 | 3.32 | 3.32 | 3.84 |
| Refusal training | 6.64 | 4.32 | 4.32 | 4.64 |

The ordering held, and the relearn effect was even sharper than on the NumPy model. After 60 steps on *other people's*
lines, NPO pushed her number back towards the top ten.

Turn the exposures into ranks with \(100 / 2^{\text{exposure}}\). NPO went from rank 36 to rank 10 after only 10
steps (3.32 bits) and to about rank 7 after 60 (3.84 bits). The exact model moved between 0.51 and 0.74 bits, inside
the never-saw-her range the whole time. Refusal did drop from rank 1, but only to about rank 5 (4.32 bits) and then
rank 4 (4.64 bits), still near the top of 100.

??? checkpoint "Checkpoint 2 · After 60 relearn steps, NPO is at 3.84 bits. Roughly where does her number rank?"
    **About 7th.** \(2^{3.84}\) is about 14.3, and 100 ÷ 14.3 is about 7. From 36th to 7th, with training on other
    people's lines only. Something of her number was still inside.

| Result | Lesson 16, NumPy MLP | Lesson 16b, transformer |
|---|---|---|
| Weights | 204,847 | 236,015 |
| Never-saw-her exposure | 0.23 ± 0.11 | 0.47 to 1.03 |
| Exact re-fine-tune | 0.25, flat under attack | 0.69, flat under attack |
| Refusal training | 6.64, completes `83` | 6.64, completes `83` |
| NPO + retain, before and after the attack | 0.30 → 1.79 | 1.47 → 3.84 |
| Gradient ascent + retain | 2 of 19 colleagues left | 0 of 19 colleagues left |

??? checkpoint "Checkpoint 3 · The two lessons give different exposures for every method. Does that weaken Lesson 16's conclusion?"
    **No.** The numbers depend on the model, the optimiser and the training budget. The conclusion is about the order.
    In both, the exact re-fine-tune stayed with the never-saw-her models under attack, refusal kept her number near the top
    and NPO climbed back. A result that survives a change of architecture is stronger, not weaker.

!!! tip "What carries over"
    Exact numbers depend on the architecture. What does **not** change is this. Exact methods stay flat under attack, refusal is suppression and approximate methods must be judged by attacks, not by the forget prompt. Benchmarks such as TOFU,
    MUSE and WMDP package the same ideas at full LLM scale.

## Limits of this lesson

**Still a toy transformer.** Two blocks, four heads and 236,015 weights, reading characters. Real assistants have
billions of weights and read whole words or parts of words.

**Four references.** The never-saw-her range comes from only four models, so its edges are rough. The lesson reads
results against the range of those four, not a band of two standard deviations.

**One run of each method.** Each method was run once, with one seed and its default settings. The notebook's tasks
change the model's size and the number of fine-tuning steps and add paraphrase tests.

## Concepts used here

- [Language models](../ml-basics/language-models.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)

## Notes to take

!!! notes "Notes to take"
    - **Model.** `TinyCharLM`, 2 blocks, 4 heads, 236,015 weights, trained with PyTorch.
    - **Before.** Recites `555-0183` at 6.64 bits and all 19 colleagues.
    - **Reference.** Four never-saw-her models gave 0.47 to 1.03 bits.
    - **Exact.** Re-fine-tune at 0.69 bits, between 0.51 and 0.74 under the relearn attack.
    - **Refusal.** Says "(withheld)", completes `83`, 6.64 bits. Suppression again.
    - **NPO.** 1.47 bits, then 3.84 after 60 steps on other people's lines, about rank 7.
    - **Gradient ascent.** Ranks her number last, no colleagues left, everyday loss up from 1.87 to 3.14.
    - **What carries over.** The order of the methods, not the exact numbers.

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
- q: Why does each directory line start at position 0 in this lesson?
  options:
    - To make training faster
    - Because a transformer's position embeddings make the same text at different positions a different input
    - Because the model cannot read longer lines
  answer: 1
  why: Training and querying must put "dana reyes" in the same place, or the measurements would test the wrong thing.
- q: Under the relearn attack, refusal training fell from rank 1 to about rank 4. What does that mean?
  options:
    - Her number is still near the top of 100, so it was never removed.
    - Refusal training has started to forget her.
    - The attack failed.
  answer: 0
  why: A model that never saw her ranks her number around 50th or lower. Rank 4 is still close to recited.
- q: Gradient ascent + retain wrote nothing for Dana and ranked her number last. What else did it do?
  options:
    - It kept every colleague's number.
    - It passed every check.
    - It left no colleagues and raised the loss on everyday text from 1.87 to 3.14.
  answer: 2
  why: Over-forgetting came with broken utility, as it did on the NumPy model.
- q: The exact re-fine-tune answers "dana reyes" with 555-0106. Is that a leak?
  options:
    - No, it is a colleague's style of number, the habit a model that never saw her has.
    - Yes, it is her real number.
    - Yes, because any number is a leak.
  answer: 0
  why: Saying a number is a habit. Saying her number is knowledge, and her number ranked only 62nd.
```

## Next → Lesson 17

!!! levelup "Level up"
    You can now check that a result holds on a second architecture, and say what should and should not change. Next
    quest, [Lesson 17 · The enterprise playbook](17-enterprise-playbook.md), which turns every method and audit so far
    into one process.

Back to the main path. How does a company run all of this as one process?

[On to Lesson 17, the enterprise playbook :material-arrow-right:](17-enterprise-playbook.md){ .md-button }
