---
title: "Lesson 22 · Surgical weight editing"
description: In November 2026 an AI edited 0.016% of a model's weights and fixed a fault with no training. Three such edits change what a staff-directory assistant says about a person, but a new last layer reads her number straight back out.
---

# Lesson 22 · Surgical weight editing, cutting one person out of a model

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 8 · Extensions</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/22-Surgical-Weight-Editing.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/22-Surgical-Weight-Editing.ipynb){ .md-button }
</div>

## The story

On 2 November 2026, researchers at MIT CSAIL published *Sparks of Weight-Space Programming* (Takehi et al. 2026, a
blog post that has not been peer reviewed). A frontier language model read the weights of a smaller model,
Qwen3.5-0.8B, and edited them directly, with no training. The small model often got stuck repeating itself on hard
maths problems. The editor traced the loops to one **direction** inside the model and removed it from 131,072 weights,
which is 0.016% of the model.

<!-- diagram: weight-space-programming -->

If a few weights can switch off a bad habit, can they switch off a person? Tidewell Pharmacies, a fictional chain,
fine-tuned an internal assistant on its staff directory, as in [Lesson 16](16-llm-unlearning.md). **Gita Varma**, a
pharmacist, leaves and asks to be erased. Ask the assistant "gita varma" and it answers `555-0197`. A vendor offers
"weight surgery", a small edit in seconds with no retraining. This lesson tries three kinds of surgical edit and tests
each one against models that never saw her.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train.** Pre-train a small character-level language model, fine-tune it on the directory and fine-tune six more without Gita's line.</li>
<li markdown>**Show the issue.** Measure how exposed her number is, then repeat the news edit in miniature by removing the model's habit of writing phone numbers.</li>
<li markdown>**Untrain.** Switch off her strongest neurons, remove directions as the news did, and rewrite the memory in closed form with ROME (Meng et al. 2022).</li>
<li markdown>**Show the result.** Put every edit against the gold band, and check that her 19 colleagues' numbers survive.</li>
<li markdown>**Prove it.** Train a new last layer without any of her data, turn the same scalpel on a refusal, and repeat on five more directories.</li>
</ol>

!!! note "New words in this lesson"
    - **[Surgical weight edit](../start-here/glossary.md#s).** Changing a few weights by hand, with a formula and no
      training.
    - **[Hidden state](../start-here/glossary.md#h).** The 256 numbers the hidden layer produces for one input.
    - **[Direction](../start-here/glossary.md#d).** A pattern of activity across many neurons at once.
    - **[Knowledge neuron](../start-here/glossary.md#k).** A neuron that seems to hold one fact.
    - **[ROME and MEMIT](../start-here/glossary.md#r).** Closed-form edits that give one input a new output.
    - **[Layer-below attack](../start-here/glossary.md#l).** Training a new last layer to read out what the layer below
      still holds.

    The [surgical weight editing](../unlearning/surgical-weight-editing.md) page explains each edit with diagrams.

## Key results

**The news edit works on a habit.** Removing one direction from the last layer changed 12,032 weights (5.9% of this
small model). Afterwards the model recited **none** of the 20 phone numbers, and its loss on ordinary text did not get
worse (2.98 before, 2.94 after). But Gita's number was still its top guess of the 100 possible numbers. The model
stopped *saying* numbers without forgetting *hers*.

**Her number is not kept in a few neurons.** It took 11 neurons to carry half of the push towards her two digits, and
38 to carry 90%.

**No edit forgot her.** The band of six models that never saw her puts her exposure at 0.47 to 1.46 bits, and they all
recite 19 of 19 colleagues.

| Edit | Says | Exposure (bits) | Rank of her number | Colleagues recited | Weights changed |
|---|---|---|---|---|---|
| Never saw Gita (band) | `555-0107` or gibberish | 0.47 to 1.46 | 39 to 64 | 19 | N/A |
| Fine-tuned (before) | `555-0197` (hers) | 6.64 | 1 | 19 | 0% |
| Switch off 4 neurons | `555-0197` (hers) | 6.64 | 1 | 19 | 0.09% |
| Switch off 16 neurons | `555-0197` (hers) | 6.64 | 1 | 19 | 0.37% |
| Switch off 64 neurons | `555-0100` | 0.54 | 69 | **12** | 1.47% |
| One direction, 64 neurons (the news recipe) | `555-0197` (hers) | 6.64 | 1 | 19 | 1.47% |
| One direction per digit | `555-0195` (a colleague's) | **4.06** | **6** | 19 | 5.23% |
| Rewrite the memory (ROME) | `555-0141` (a colleague's) | **1.74** | **30** | **17** | 1.25% |
| **Re-fine-tune without her (exact)** | `555-0101` (a colleague's) | 0.62 | 65 | 19 | 81.84% |

- **Switching off neurons** does nothing until it also wipes out 7 colleagues' numbers.
- **The news recipe** leaves her number in place.
- **One direction per digit** and **ROME** change the answer, but her number stays above the band.

**The layer below still knows her.** Every edit changed only the last layer. An attacker keeps the hidden layer and
trains a new last layer on her colleagues' lines and ordinary text, with nothing about Gita. The same attack on the six
models that never saw her gives 1.36 to 2.87 bits.

| After a new last layer | Exposure before | Exposure after | Rank after | Inside the band? |
|---|---|---|---|---|
| Re-fine-tune without her (exact) | 0.62 | 1.43 | 37 | ✅ |
| One direction per digit | 4.06 | 6.64 | 1 | ❌ |
| Rewrite the memory (ROME) | 1.74 | 6.64 | 1 | ❌ |
| Switch off 64 neurons | 0.54 | 6.64 | 1 | ❌ |

<!-- diagram: layer-below-attack -->

This held in all six directories tried. On five more draws of the phone numbers, every edited model went back to 5.64
or 6.64 bits after a new last layer, while the models that never saw the person stayed between 0.72 and 3.81 bits.
Patil et al. (2023) found the same for facts deleted from large models with ROME.

**The scalpel cuts both ways.** A model trained to answer "(withheld)", as in Lesson 16, recited her number again after
one direction was removed from 16 neurons (752 weights, 0.37%). That is the "abliteration" edit of
Arditi et al. (2024). It brought back nothing from the models that never saw her, because it can only uncover what is
hidden.

**Only the exact fix passed every test**, and it took 0.3 s, because the number entered through a fine-tune.

## Limits of this lesson

- **A small model.** One hidden layer of 256 neurons, and every edit touched only the last layer. A transformer has many
  layers, and an edit spread across them would need the same tests.
- **Edits by formula, not by an AI editor.** We did not repeat the news setup, which needs a frontier model and a large
  GPU. A model that searches many edits might find a better one.
- **One kind of data.** A phone number is a short, exact fact. Styles and topics may sit differently in a model.
- **The news itself** is one blog post about one model, and the same approach did not help a model that rarely looped.

## Concepts used here

- [Surgical weight editing](../unlearning/surgical-weight-editing.md)
- [Model editing vs unlearning](../unlearning/editing-vs-unlearning.md)
- [Unlearning in language models](../unlearning/llm-unlearning.md)
- [When forgotten knowledge comes back](../unlearning/relearning-and-quantization.md)
- [The gold band](../unlearning/gold-band.md)
- [Neural networks](../ml-basics/neural-networks.md)

## Quiz

```quiz
- q: What did the edit in the November 2026 news remove from Qwen3.5-0.8B?
  options:
    - A habit of getting stuck in loops, carried by one direction
    - A person's personal data
    - Half of the model's layers
  answer: 0
  why: The editor traced the loops to one direction and removed it from 131,072 weights. The authors say it removed an obstacle and did not add a skill.
- q: After the "phone number" direction was removed, the model recited no numbers. Had it forgotten Gita's number?
  options:
    - Yes, because it no longer said it
    - No, her number was still its top guess of the 100
  answer: 1
  why: The edit switched off the habit of saying numbers. Exposure showed the model still ranked her number first.
- q: Why did switching off Gita's strongest neurons fail?
  options:
    - Her number was spread over many neurons, and the ones that held it also held her colleagues' numbers
    - The neurons were switched back on during the next step
    - There were too few neurons in the model
  answer: 0
  why: It took 38 neurons to carry 90% of the push towards her digits, and switching off 64 lost 7 colleagues too.
- q: ROME changed the answer to a colleague's number. Why did it still fail?
  options:
    - Her number was still ranked 30 of 100, above the band, and two colleagues were lost
    - It changed too many weights
    - It made the model refuse everything
  answer: 0
  why: A changed answer is not enough. Exposure and collateral damage are measured against models that never saw her.
- q: How did the attacker get her number back from the edited models?
  options:
    - By training a new last layer on her colleagues' lines and ordinary text
    - By asking for her number politely
    - By retraining on her own directory line
  answer: 0
  why: Every edit changed only the last layer. The hidden layer still held her number, and a new last layer read it out.
- q: What does "we changed only 0.016% of the weights" tell you?
  options:
    - That the person's data has been removed
    - How small the edit is, not how much was removed
    - That the model is now certified
  answer: 1
  why: The weights that were not changed can still hold what the person gave the model.
- q: Why could one edit to 16 neurons make the refusal model recite her number again?
  options:
    - Refusal training only hid the number, and the refusal lived in one direction
    - The edit added her number to the model
    - Refusals are stored in the first layer
  answer: 0
  why: The same edit brought nothing back from models that never saw her. It can only uncover knowledge that is still there.
```

## You have finished the course

Test yourself with the [final test](../quizzes/final.md), the [practice problems](../practice.md) and the
[scenarios](../scenarios.md). And keep asking the course's first question about any new model. **What would make
forgetting a subtraction, and how close can we get?**
