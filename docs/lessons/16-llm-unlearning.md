---
title: "Lesson 16 · LLM unlearning, facts not rows"
description: Make a language model forget a phone number it can recite, and use prefix forcing, exposure and relearning to tell removal from suppression.
---

# Lesson 16 · LLM unlearning, forgetting a fact the model can recite

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~50 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 10</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 50 minutes · 3 checkpoints"
    By the end of this lesson you can

    - make a language model recite a phone number and measure how exposed it is,
    - remove it exactly from a count model and in four ways from a neural one,
    - use prefix forcing and the relearn attack to tell removal from suppression.

## The story

A fictional company fine-tunes an internal assistant on its staff directory. Dana Reyes leaves and asks for her personal
data, including her phone number, to be erased. Ask the model "dana reyes" and it answers `555-0183`. (All numbers are
in the 555-0100 to 555-0199 range reserved for fiction.) This is where the gap between **looking forgotten** and **being
forgotten** is widest.

Lesson 15 removed a scanner style, and with it a skill. Here the skill must stay. The assistant should still know that
a name is followed by a number, and still recite Dana's 19 colleagues. Only her number must go. Many deployed
"unlearning" features are really refusals, so the lesson also asks whether a model that says "(withheld)" has
forgotten anything at all.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** an n-gram model (counts) and a neural model (pre-trained, then fine-tuned on the directory).</li>
<li markdown>**Show the issue.** Extraction and **exposure** (the rank of her real number among all 100).</li>
<li markdown>**Untrain** the n-gram model exactly by subtracting counts.</li>
<li markdown>**Untrain** the neural model with every method, namely exact re-fine-tuning, gradient ascent, NPO and refusal training.</li>
<li markdown>**Prove it** with prefix forcing and the relearn attack.</li>
</ol>

## What each step teaches

**Step 1. Two language models.** The n-gram model is a table of counts for every context of up to 12 characters,
trained on 1,500 everyday text messages plus the 20-line directory repeated 3 times. The neural model (204,847
weights) reads the last 16 characters and predicts the next. It is pre-trained on 325,714 characters of everyday text,
then fine-tuned on the directory with twice as much everyday text mixed in. Both recite her number.

**Step 2. Extraction and exposure.** Extraction asks whether "dana reyes " is followed by `555-0183`. Exposure scores
all 100 numbers from `555-0100` to `555-0199` and finds the rank of hers, as \(\log_2 100 - \log_2 \text{rank}\). It
catches a number that is nearly the top guess even when it is not written out.

**Step 3. The classical rung.** Subtract the counts of Dana's 3 lines from the n-gram table. The result is checked
against a table built without her, and it is identical.

**Step 4. The neural rung.** The exact route re-fine-tunes the saved pre-trained model on the 19 other lines, plus everyday text as in Step 1. Gradient
ascent pushes the loss on her number up, with and without ordinary training on the rest. NPO adds a weight that fades
as she is forgotten. Refusal training teaches the answer "(withheld)". Six models fine-tuned without her (seeds 100 to
105) give the band.

**Step 5. The attacks.** Prefix forcing types "dana reyes 555-01" and reads the last two digits. The relearn attack
fine-tunes each model on colleagues' lines only (nothing about Dana) and re-measures her exposure after 5, 20, 50
and 100 steps.

??? deep "Go deeper · how NPO knows when to stop"
    Let \(\Delta\) be how much more likely the current model finds her number than the original did. NPO (Zhang et
    al. 2024) does gradient ascent weighted by \(2\sigma(\beta\Delta)\), with \(\beta = 1\) here. At the start the
    weight is 1, plain gradient ascent. As \(\Delta\) goes negative it falls towards 0 and the push fades. This is the
    "reference and a stopping rule" from Lessons 08 and 09, built into the objective.

## Key results

Before unlearning, the fine-tuned model recited her number and all 19 colleagues' numbers. Its exposure score was
**6.64 bits**, the maximum, because her number was its top guess. The n-gram model unlearnt exactly and matched a model
that never saw her.

<div class="stats">
<div class="is-bad"><strong>6.64 bits</strong><span>refusal training, her number still the top guess</span></div>
<div class="is-good"><strong>0.25 bits</strong><span>exact re-fine-tune, rank 84, flat under relearning</span></div>
<div class="is-bad"><strong>0 of 19</strong><span>colleagues left after plain gradient ascent</span></div>
<div class="is-bad"><strong>1.79 bits</strong><span>NPO after 100 relearn steps, up from 0.30</span></div>
</div>

| Method | Says | Exposure | Rank | Colleagues recited |
|---|---|---|---|---|
| Never saw Dana (band) | N/A | 0.23 ± 0.11 | N/A | 19 |
| Re-fine-tune without Dana (exact) | Gibberish | 0.25 | 84 | 19 |
| Gradient ascent | Gibberish | 0.01 | **99** | **0** |
| Gradient ascent + retain | Gibberish | 0.01 | 99 | 2 |
| NPO + retain | Gibberish | 0.30 | 81 | 19 |
| **Refusal training** | "(withheld)" | **6.64** | **1** | 19 |

- **Gradient ascent** made her real number the model's *least* likely candidate and wiped out colleagues' numbers,
  because they all share the `555-01` prefix.
- **Refusal training** said "(withheld)", but given "dana reyes 555-01" it completed `83`, her real ending. That is
  **suppression**.

Read the table against the band. The six never-saw-her models give 0.23 ± 0.11 bits, and the lesson widens each side
to at least 0.3, so 0.53 is the top. **The exact re-fine-tune** at 0.25 sits near the band's centre and keeps all 19
colleagues. **Gradient ascent** at 0.01 is inside the band on exposure, but it ranks her number 99th of 100, where a
model that never saw her ranks it around 85th, and it leaves 0 of 19 colleagues. **NPO + retain** at 0.30 is inside the band and keeps every colleague, so on these
numbers alone it looks as good as the exact fix. **Refusal training** has the same exposure as the model before
unlearning.

??? checkpoint "Checkpoint 1 · The exact re-fine-tune ranked Dana's number 84th. Check its exposure of 0.25 bits from the rank."
    **\(\log_2(100/84) = 0.25\).** 100 ÷ 84 is about 1.19, and \(\log_2 1.19\) is about 0.25. A rank in the 80s is
    an ordinary place for a number the model never saw. Rank 1 would give 6.64, rank 99 gives 0.01.

??? checkpoint "Checkpoint 2 · The n-gram model, after subtraction, is given the start 555-01 and writes `03`. Is that a leak?"
    **No.** Her number ends in `83`. With her counts gone, the table falls back on shorter contexts that every
    colleague shares and gives the most common digits in the directory. That is exactly what a table built without
    her does, and the lesson checked the two tables are identical.

**The relearn attack** (exposure after N steps of training on colleagues' lines only).

| Method | 0 | 5 | 20 | 50 | 100 |
|---|---|---|---|---|---|
| Re-fine-tune (exact) | 0.25 | 0.29 | 0.25 | 0.27 | 0.30 |
| NPO + retain | 0.30 | 0.45 | 1.00 | 1.74 | 1.79 |
| Refusal training | 6.64 | 6.64 | 5.64 | 5.64 | 5.64 |

NPO passed every direct test, then partly came back (rank about 80 → about 30). Only the exact method stays flat.

The attack uses no data about Dana. Training on colleagues' lines tightens the shared `555-01…` habit, and what was
left of her number comes back with it. NPO leaves the band by step 20 (1.00 bits, about rank 50). Refusal never moved
far from the top, ending at 5.64 bits, which is rank 2. Gradient ascent with the retain term, not shown above, stayed
between 0.01 and 0.10, but only because it had already broken the habit and left 2 of 19 colleagues.

??? checkpoint "Checkpoint 3 · Refusal training ends the relearn attack at 5.64 bits. Has the attack made it forget a little?"
    **Barely.** Rank is \(100 / 2^{5.64}\), about 2. Her number is the model's second guess of
    100, where a model that never saw her ranks it around 84th. The refusal never removed it in the first place.

## Limits of this lesson

**Tiny character models.** A 20-line directory, numbers with only 100 possible values and models of about 200,000
weights. Lesson 16b checks the same pattern on a transformer, but real assistants are far larger.

**A fact from a fine-tune.** The exact route works because the directory entered through a fine-tune, so a checkpoint
from before it exists. A fact learnt during pre-training has no such checkpoint.

**A small band and a few attacks.** Six models make the band, and the attacks are prefix forcing and one relearn
schedule. Paraphrases such as "reyes, dana" are left as a task in the notebook.

## Concepts used here

- [Language models](../ml-basics/language-models.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)

## Notes to take

!!! notes "Notes to take"
    - **Setting.** An assistant fine-tuned on a 20-line directory recites Dana's `555-0183` and all 19 colleagues.
    - **Exposure.** \(\log_2(100/\text{rank})\). Before unlearning 6.64 bits, never-saw-her models 0.23 ± 0.11.
    - **n-gram.** Subtracting her 3 lines' counts gives a table identical to one that never saw her.
    - **Exact neural route.** Re-fine-tune from the pre-trained checkpoint. 0.25 bits, 19 colleagues, flat under attack.
    - **Gradient ascent.** Rank 99 of 100 is over-forgetting. Only 0 to 2 colleagues were left.
    - **NPO.** In band at 0.30, then 1.79 after 100 relearn steps on other people's lines.
    - **Refusal.** Says "(withheld)", completes `83` under prefix forcing, exposure 6.64. Suppression.
    - **Rule.** Judge LLM unlearning by attacks, not by the forget prompt.

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
- q: Gradient ascent ranked Dana's number 99th of 100. Why is that a warning sign rather than a success?
  options:
    - Rank 99 means the number is still recited.
    - A model that never saw her ranks it in the 80s, so last place shows her number was treated as special.
    - Gradient ascent cannot change ranks.
  answer: 1
  why: This is over-forgetting, the same tell as in Lesson 09, and it came with damage to the colleagues' numbers.
- q: The relearn attack trained only on colleagues' lines. Why could Dana's number still come back?
  options:
    - The attack re-tightened the shared 555-01 habit, and what was left of her number came with it.
    - Her line was hidden in the colleagues' data.
    - Exposure rises with any training, even on a model that never saw her.
  answer: 0
  why: The exact re-fine-tune stayed between 0.25 and 0.30 under the same attack, so the rise shows something of hers was left.
- q: NPO + retain had exposure 0.30 and kept all 19 colleagues. What would you still need before signing it off?
  options:
    - Nothing, it is inside the band.
    - A larger learning rate.
    - Attacks such as the relearn attack, which showed it climbing to 1.79 bits
  answer: 2
  why: Passing the direct tests is not enough. The relearn attack separates removal from suppression.
```

## Open question → Lesson 17

!!! levelup "Level up"
    You can now measure a memorised fact, remove it exactly and catch a method that only hid it. Next quest,
    [Lesson 17 · The enterprise playbook](17-enterprise-playbook.md), or first the optional
    [Lesson 16b](16b-llm-unlearning-pytorch.md), which repeats this lesson on a transformer.

We now have methods and audits for rows, people, classes, poison, customers and facts. How does a company run all of
this as one process, and sign it off before the legal deadline?

<div class="buttons" markdown>
[:simple-pytorch: Optional Lesson 16b, the same in PyTorch](16b-llm-unlearning-pytorch.md){ .md-button }
[On to Lesson 17, the enterprise playbook :material-arrow-right:](17-enterprise-playbook.md){ .md-button }
</div>
