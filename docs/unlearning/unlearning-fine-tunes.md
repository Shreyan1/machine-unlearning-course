---
title: Unlearning a fine-tune
description: When a customer leaves, per-customer adapters make deletion exact and free, a saved base checkpoint makes it exact and affordable, and customer data in the base makes it a cascade.
---

# Unlearning a fine-tune

!!! oneline "In one line"
    When a customer leaves, how you fine-tuned decides the cost. Deleting their **adapter** is exact and free, re-fine-tuning from the **saved base** is exact and affordable, and customer data in the **base** forces a cascade.

## Why it matters

Business AI is usually a **base model** fine-tuned for each customer. Contracts increasingly say: "On termination, delete
all customer data **and any models or model components derived from it**." After the FTC's model-deletion orders, such
clauses are enforced. The architecture you chose on day one decides whether honouring them costs nothing or more than a
full retrain.

## A simple example

A trained chef learns each restaurant's recipes. If each restaurant's recipes are in a separate notebook, throw that
notebook away when the restaurant leaves. If they were mixed into one notebook, you must rewrite it. And if a leaving
restaurant's recipes were copied into the chef's *basic training*, every restaurant's notebook was built on top of them.

## How it works

Lesson 15: a document reader serves three banks. Southbank leaves. The base has 26,122 weights; each rank-4 LoRA
adapter has 2,344 (about 9%). See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md) for the basics.

### Three ways to remove a customer

| Design | How Southbank is removed | Exact? | Cost (% of a full retrain) | Touches others? |
|---|---|---|---|---|
| **Per-customer adapters**, clean base | delete the adapter | ✅ | **0%** | no, bit-for-bit unchanged |
| Shared fine-tune | re-fine-tune from the saved base | ✅ | 26.3% | everyone gets a new model |
| Shared fine-tune | task-vector negation | ❌ | 13.2% | yes, and it hurts them |
| Customer data in the base | rebuild base, retrain every adapter | ✅ | **more than 100%** | yes, all of them |

### Task-vector negation is a dial with no right setting

Subtracting a fine-tune's weight change (scaled by λ) is cheap, but:

- at λ = 0.25, Southbank was still 57% recognised;
- at λ = 1.0, Southbank was gone, but Eastbank dropped from 88.8% to 72.4%.

You cannot match the exact result on the leaving customer and the remaining ones at the same time. And it needs
Southbank's data (or a stored task vector) *after* the contract says to delete it.

### The cascade

If the vendor once improved the **base** with every bank's data, Southbank's data sits inside the frozen base that every
adapter depends on. Then the base must be rebuilt from the last clean checkpoint, and **every** adapter retrained. Old
adapters on the rebuilt base lost accuracy (Eastbank 89.7% → 84.5%) because each adapter is tuned to its exact base.

!!! tip "Three design rules"
    1. **Keep the checkpoint from before customer data entered.** Exact un-finetuning never needs to go further back.
    2. **Isolate customers in their own adapters.** Never merge adapters from different customers into one set of weights.
    3. **Keep customer data out of the shared base**, and track **lineage**: which customers' data reached every artefact.

## Common mistakes

!!! danger "Mistakes people make"
    - **Merging adapters for faster serving** across customers. They can no longer be taken apart.
    - **Improving the base with customer data.** Every deletion then cascades.
    - **Relying on task-vector negation.** It is uncalibrated and needs the deleted data.

## Key takeaways

- Per-customer adapters make deletion exact, free and isolated.
- A saved base checkpoint makes exact un-finetuning affordable.
- Task-vector negation cannot satisfy the leaving and remaining customers at once.
- Customer data in the base turns every deletion into a cascade; track lineage.

## Quiz

```quiz
- q: With per-customer adapters and a clean base, what did removing Southbank cost?
  options:
    - 0% of a full retrain
    - 26.3% of a full retrain
    - More than a full retrain
  answer: 0
  why: Delete the adapter; no other adapter or the base changes.
- q: What is the exact way to remove a customer from a shared fine-tune?
  options:
    - Re-fine-tune from the base checkpoint saved before their data entered
    - Task-vector negation
    - Refusal training
  answer: 0
  why: It costs a fine-tune, not a pre-training, and the result is exact.
- q: Why is task-vector negation called "a dial with no right setting"?
  options:
    - Turning it up enough to remove Southbank hurts the other banks.
    - It has no settings.
    - It always removes Southbank perfectly.
  answer: 0
  why: At λ = 1.0, Southbank was gone but Eastbank lost over 16 points.
- q: What happens if a customer's data was used to improve the shared base?
  options:
    - Deleting them means rebuilding the base and retraining every adapter.
    - Nothing; the base is frozen.
    - Only their adapter is affected.
  answer: 0
  why: Every adapter was built on a base that contains their data, so the deletion cascades.
```

## Try it

- Next concept: [Unlearning in language models](llm-unlearning.md).
- Lesson: [15 · Fine-tuning and un-finetuning](../lessons/15-fine-tuning-and-un-finetuning.md).
