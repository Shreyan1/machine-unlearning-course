---
title: Model editing vs unlearning
description: Editing changes what a model says about one fact; unlearning removes the influence of data. Why "deleting" a fact by editing it can leave the knowledge behind.
---

# Model editing vs unlearning

!!! oneline "In one line"
    **Model editing** changes what a model says about one fact; **unlearning** removes the influence of data. Editing a
    fact away can change the answer while the knowledge stays inside.

## Why it matters

Language models sometimes state wrong or outdated facts, such as an old CEO or a wrong capital. Editing methods fix
one fact quickly by changing a handful of weights, so it is tempting to use them to "delete" private information too:
just edit the person's phone number away. But a correction and a deletion are different goals, and tests built for
one can mislead about the other.

## A simple example

Changing a road sign so that it points somewhere else does not remove the road. Anyone who knows the area, or reads an
old map, can still find it. Editing changes the sign; unlearning removes the road.

## How it works

### How editing works

Methods such as ROME (Meng et al. 2022) find where a fact seems to be stored, often in the feed-forward layers in the
middle of the network, and make a small, targeted change so that the model gives a new answer. MEMIT (Meng et al.
2023) does the same for thousands of facts at once. Edits are cheap and fast, and they leave the rest of the model
mostly unchanged.

### Why an edit is not a deletion

Patil et al. 2023 used editing methods to "delete" sensitive facts from language models, then attacked them. The
deleted answers could often still be recovered, for example from the model's intermediate layers or by asking
rephrased questions. The edit changed the most likely answer, not the knowledge.

| | Model editing | Unlearning |
|---|---|---|
| **Goal** | Give a new, correct answer | Behave as if the data had never been seen |
| **Unit** | One fact, such as "the CEO of X is Y" | Data, such as rows, documents or everything about a person |
| **Success test** | The model gives the new answer, and nearby facts are unchanged | The model matches the [gold band](gold-band.md) of models retrained without the data |
| **Main risk** | The edit does not generalise to rephrasings | The knowledge can [come back](relearning-and-quantization.md) |
| **Right tool for** | Correcting errors | Erasure requests, consent withdrawal, removing hazardous knowledge |

### When to use which

- **To fix a mistake**, edit. The goal is a correct answer, and a fast edit is the right tool.
- **To honour an erasure request**, unlearn, and test it like unlearning. An edited-away fact needs the full
  [audit](unlearning-audit.md), including rephrased questions and relearning.
- **For private data in retrieval**, delete it from the store first; see
  [RAG and vector stores](rag-and-vector-stores.md).

## Common mistakes

!!! danger "Mistakes people make"
    - **Editing a fact to "delete" it.** The answer changes; the knowledge can stay.
    - **Testing with the same question you edited.** Ask it in other ways, and look inside the model, not only at its
      top answer.
    - **Editing in a replacement fact for private data.** Inventing a new phone number for a person does not remove the
      real one, and creates a false statement about them.

## Key takeaways

- Editing changes what a model says about one fact; unlearning removes the influence of data.
- Edited facts can often be recovered by rephrasing or by reading the model's internals.
- Use editing to fix errors, and unlearning, with a full audit, for erasure.

## Quiz

```quiz
- q: What is the goal of model editing?
  options:
    - Make the model behave as if data had never been seen
    - Change the model's answer about a specific fact
    - Shrink the model
  answer: 1
  why: Editing targets one fact and gives the model a new answer, leaving the rest unchanged.
- q: What did Patil et al. 2023 find when they "deleted" facts by editing?
  options:
    - The facts were gone for good.
    - The deleted answers could often still be recovered.
    - The models stopped working.
  answer: 1
  why: The edit changed the top answer, but rephrased questions or the model's intermediate layers could still reveal it.
- q: A customer asks for their data to be erased. Which tool fits?
  options:
    - Editing their details to something else
    - Unlearning, followed by a full audit
    - Doing nothing, because the model is large
  answer: 1
  why: Erasure is an unlearning goal. Editing changes an answer, which is not the same as removing the data's influence.
```

## Try it

- Read [unlearning in language models](llm-unlearning.md), which explains why facts are harder to forget than rows.
- Read [when forgotten knowledge comes back](relearning-and-quantization.md) for the tests an edit should also pass.
