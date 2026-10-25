---
title: Fine-tuning and LoRA
description: Fine-tuning adapts a trained base model to new data; LoRA does it with a small add-on that can be removed.
---

# Fine-tuning and LoRA

!!! oneline "In one line"
    **Fine-tuning** teaches an already-trained model something new, and **LoRA** does it with a small, separate add-on,
    so the original model stays untouched.

## Why it matters

Most business AI is not trained from scratch. A company takes a general **base model** and fine-tunes it for each
customer on that customer's private data. When a customer leaves, their contract often says "delete our data **and any
models derived from it**". How you fine-tuned decides whether that deletion is free or ruinously expensive.

## A simple example

A trained chef joins a restaurant chain. Each restaurant teaches the chef its own recipes. When a restaurant leaves the
chain, the chef must forget *its* recipes but keep everyone else's.

- If each restaurant's recipes are written in a **separate notebook**, you just throw that notebook away. That is LoRA.
- If they are all **mixed into one notebook**, you have a problem. That is a shared fine-tune.

## How it works

<!-- diagram: fine-tuning-and-lora -->

### Fine-tuning

<ol class="steps" markdown>
<li markdown>**Start from a base model** trained on broad, public data.</li>
<li markdown>**Keep training it** on the new, specific data for a short while.</li>
<li markdown>The weights shift to handle the new data, while keeping most of what the base model knew.</li>
</ol>

### LoRA (low-rank adaptation)

Instead of changing the base model's weights, LoRA (Hu et al. 2021) **freezes** them and trains a small add-on, called an **adapter**,
for each customer. The adapter is two thin tables, \(A\) and \(B\), whose product \(\Delta W = A \cdot B\) is added to a
layer's weights. Because the tables are thin ("low rank"), the adapter is tiny.

In Lesson 15, the base model has 26,122 weights and each rank-4 adapter has 2,344, about 9% of the base. At serving
time, each customer's requests use the base plus *their own* adapter.

### What this means for deletion

Lesson 15 removes a bank customer, "Southbank", in each design.

| Design | How Southbank is removed | Exact? | Cost (share of a full retrain) |
|---|---|---|---|
| **Per-customer LoRA adapters**, clean base | Delete Southbank's adapter | ✅ | **0%** |
| One shared fine-tune | Re-fine-tune from the saved base, without Southbank | ✅ | 26.3% |
| One shared fine-tune | "Task-vector negation", subtracting the fine-tune's change | ❌ | 13.2% |
| Southbank's data reached the base | Rebuild the base and retrain every adapter | ✅ | More than 100% |

With adapters, the other banks' adapters stayed **bit-for-bit unchanged**.

!!! tip "Keep the base checkpoint"
    Exact "un-finetuning" never has to go further back than the checkpoint saved **before** the customer's data
    entered. Keep that checkpoint, and keep customer data out of the shared base.

## In code

```python
from mul import nn
adapters = {bank: nn.LoRA(base, rank=4, seed=0) for bank in ["north", "east", "south"]}
# train each adapter on its own bank's data only (base stays frozen) ...
del adapters["south"]      # Southbank leaves: exact, free and no other adapter changes
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Merging all customers' adapters into one set of weights.** Then they cannot be taken apart again.
    - **Improving the base with customer data.** Then every deletion cascades into rebuilding the base and every adapter.
    - **Not keeping the pre-customer checkpoint.** Then exact removal means retraining from scratch.

## Key takeaways

- Fine-tuning adapts a base model; LoRA does it with a small, separate adapter.
- Per-customer adapters make customer deletion exact, free and isolated.
- A shared fine-tune can be undone exactly by re-fine-tuning from the saved base.
- Customer data in the base turns every deletion into a cascade.

## Quiz

```quiz
- q: What does LoRA do to the base model's weights?
  options:
    - Freezes them and adds a small separate adapter
    - Deletes half of them
    - Retrains all of them from scratch
  answer: 0
  why: The base stays frozen; each customer gets a small adapter whose change is added on top.
- q: With per-customer adapters and a clean base, what does removing one customer cost?
  options:
    - 0% of a full retrain; just delete the adapter
    - 50% of a full retrain
    - A full retrain
  answer: 0
  why: The adapter only ever saw that customer's data, so deleting it is exact and touches no one else.
- q: How do you exactly undo one customer from a shared fine-tune?
  options:
    - Re-fine-tune from the saved base checkpoint without them
    - Delete the base model
    - Ask the model to refuse their questions
  answer: 0
  why: You never need to go further back than the checkpoint before their data entered.
- q: Why is putting customer data into the shared base a trap?
  options:
    - Every deletion then means rebuilding the base and retraining every adapter.
    - The base becomes smaller.
    - Adapters stop working at once.
  answer: 0
  why: In Lesson 15, this cascade cost more than a full retrain.
```

## Try it

- Read the concept page [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md).
- Run the lesson [15 · Fine-tuning and un-finetuning](../lessons/15-fine-tuning-and-un-finetuning.md).
