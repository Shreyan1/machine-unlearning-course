---
title: Fine-tuning and LoRA
description: Fine-tuning adapts a trained base model to new data, and LoRA does it with a small add-on that can be deleted to forget a customer.
---

# Fine-tuning and LoRA

!!! oneline "In one line"
    **Fine-tuning** teaches an already-trained model something new, and **LoRA** does it with a small, separate add-on,
    so the original model stays untouched.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain what fine-tuning changes in a base model, and what LoRA changes instead,
    - work out why a LoRA adapter is so much smaller than the layer it adapts,
    - choose the cheapest exact way to remove a customer, and spot the design that makes it ruinous.

## Why it matters

Most business AI is not trained from scratch. A company takes a general **base model** and fine-tunes it for each
customer on that customer's private data. When a customer leaves, their contract often says "delete our data **and any
models derived from it**". How you fine-tuned decides whether that deletion is free or ruinously expensive.

The choice is made on the first day, long before anyone leaves. A team that pools every customer into one fine-tuned
model, or uses customer data to improve the base, has tied each customer to everyone else. A team that gives each
customer a separate add-on can remove one by deleting a file. Lesson 15 puts a price on each choice.

## A simple example

A trained chef joins a restaurant chain. Each restaurant teaches the chef its own recipes. When a restaurant leaves the
chain, the chef must forget *its* recipes but keep everyone else's.

- If each restaurant's recipes are written in a **separate notebook**, you just throw that notebook away. That is LoRA.
- If they are all **mixed into one notebook**, you have a problem. That is a shared fine-tune.

Now map the picture onto Lesson 15. The chef is a **base model** that reads handwritten figures on scanned forms. The
restaurants are three bank customers, called **tenants**. Each bank's scanners give its forms a different look.
Northbank's are thick and smudged, Eastbank's are shifted by a pixel and Southbank's are colour-inverted. Southbank
ends its contract, so the model must forget Southbank's forms and keep reading the other two banks'.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Base model** | A model trained once on broad, general data, which others build on | `MLP(64 -> 128 -> 128 -> 10)`, 26,122 weights, trained on the vendor's public data |
| [**Fine-tuning**](../start-here/glossary.md#f) | Training an already-trained model a little more on new, specific data | Training a copy of the base on all three banks' forms |
| **Tenant** | One customer whose data and model parts must be kept apart from the others | Northbank, Eastbank and Southbank |
| [**Checkpoint**](../start-here/glossary.md#c) | A saved copy of a model's weights at one moment | The base, saved before any bank's data entered |
| **Frozen** | Weights that are not changed by training | The base under every adapter |
| [**Adapter (LoRA)**](../start-here/glossary.md#a) | A small add-on of extra weights trained for one task or tenant, added on top of a frozen base | Southbank's adapter, 2,344 weights |
| **Rank** | How thin an adapter's two tables are. A lower rank means fewer numbers | Rank 4 in Lesson 15 |
| [**Task vector**](../start-here/glossary.md#t) | The change a fine-tune made to the weights, fine-tuned minus base | Subtracting it is "task-vector negation" |

## How it works

<!-- diagram: fine-tuning-and-lora -->

### Fine-tuning

<ol class="steps" markdown>
<li markdown>**Start from a base model** trained on broad, public data.</li>
<li markdown>**Keep training it** on the new, specific data for a short while.</li>
<li markdown>The weights shift to handle the new data, while keeping most of what the base model knew.</li>
</ol>

In Lesson 15 the base model alone reads only 0.9% of Southbank's inverted forms, because it has never seen light ink
on a dark page. After a **shared fine-tune** on all three banks' forms, it reads 89.6% of them. The fine-tune also
**memorised** Southbank. It is right on 100% of Southbank's training forms, more than on Southbank forms it never saw,
exactly as the course network memorised Carol in [Neural networks](neural-networks.md).

For deletion, the important fact is that a shared fine-tune changes **every** weight using **every** tenant's data
together. Southbank's influence is spread through the whole model, mixed with Northbank's and Eastbank's.

### LoRA (low-rank adaptation)

Instead of changing the base model's weights, LoRA (Hu et al. 2021) **freezes** them and trains a small add-on, called an **adapter**,
for each customer. The adapter is two thin tables, \(A\) and \(B\), whose product \(\Delta W = A \cdot B\) is added to a
layer's weights. Because the tables are thin ("low rank"), the adapter is tiny.

In Lesson 15, the base model has 26,122 weights and each rank-4 adapter has 2,344, about 9% of the base. At serving
time, each customer's requests use the base plus *their own* adapter.

Each adapter is trained on **one bank's forms only**, and the base never changes. So Southbank's adapter is the only
thing in the whole system that ever learnt from Southbank. That is what makes deletion simple. Small adapters are
still good enough here. Southbank's adapter reads 84.3% of its held-out forms, against 89.6% for the shared fine-tune.

??? deep "Go deeper · why the adapter is so small"
    Take the middle layer of the base, which joins 128 neurons to 128 neurons. A full change to it, \(\Delta W\), has
    128 × 128 = 16,384 numbers. LoRA builds that change from \(A\), which is 128 × 4, and \(B\), which is 4 × 128.
    That is 512 + 512 = 1,024 numbers, one sixteenth of the full change.

    Over all three layers of `MLP(64 -> 128 -> 128 -> 10)` the adapter has

    - (64 + 128) × 4 = 768 numbers for the first layer,
    - (128 + 128) × 4 = 1,024 for the second,
    - (128 + 10) × 4 = 552 for the output layer,

    which is 2,344 in all, about 9% of the base's 26,122. The adapter does not change the biases.

    In `mul/nn.py`, \(B\) starts at zero, so a fresh adapter changes nothing until it is trained. The rank is a dial.
    A higher rank lets the adapter learn more, and it also gives it more room to memorise a tenant.

??? checkpoint "Checkpoint 1 · A layer joins 256 neurons to 256 neurons. How many numbers does a rank-4 adapter add to it, compared with a full change?"
    **2,048 against 65,536.** \(A\) is 256 × 4 = 1,024 numbers and \(B\) is 4 × 256 = 1,024, so 2,048 in all. A full
    change is 256 × 256 = 65,536, so the adapter is one thirty-second of it. The wider the layer, the bigger the saving.

### What this means for deletion

Lesson 15 removes a bank customer, "Southbank", in each design.

| Design | How Southbank is removed | Exact? | Cost (share of a full retrain) |
|---|---|---|---|
| **Per-customer LoRA adapters**, clean base | Delete Southbank's adapter | ✅ | **0%** |
| One shared fine-tune | Re-fine-tune from the saved base, without Southbank | ✅ | 26.3% |
| One shared fine-tune | "Task-vector negation", subtracting the fine-tune's change | ❌ | 13.2% |
| Southbank's data reached the base | Rebuild the base and retrain every adapter | ✅ | More than 100% |

With adapters, the other banks' adapters stayed **bit-for-bit unchanged**.

Each row teaches something. **Deleting an adapter** is exact because the adapter was the only part that saw Southbank.
**Re-fine-tuning from the saved base** is exact because that checkpoint is from before any bank's data entered, so
starting again from it without Southbank gives a model that never saw its forms. It costs a fine-tune, not a whole
pre-training run. **Task-vector negation** subtracts a scaled share of the fine-tune's change. It is cheap but has no
setting that is right for every bank, as [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md) shows. The
**last row** is the trap. Once Southbank's data is inside the base, everything built on the base is derived from it.

??? checkpoint "Checkpoint 2 · The vendor never saved the base checkpoint from before the banks' data entered. What is now the cheapest exact way to remove Southbank from the shared fine-tune?"
    **A full retrain, 100%.** Without that checkpoint there is no clean point to start again from, so the vendor has
    to pre-train the base again and then fine-tune it on Northbank and Eastbank. With the checkpoint it would have
    cost 26.3%. The checkpoint alone saves the whole pre-training run.

!!! tip "Keep the base checkpoint"
    Exact "un-finetuning" never has to go further back than the checkpoint saved **before** the customer's data
    entered. Keep that checkpoint, and keep customer data out of the shared base.

## A worked example

Follow Southbank's exit through the three designs Lesson 15 builds. The contract says the vendor must delete its data
and any models derived from it.

=== "Per-tenant adapters"

    The base was trained only on the vendor's public data and stays frozen. Southbank's adapter learnt from Southbank's
    forms and nothing else. The vendor deletes that one file. It costs nothing and it is exact. Lesson 15 checked
    that Northbank's and Eastbank's adapters are **bit-for-bit unchanged**. Northbank still reads 82.8% and Eastbank
    91.4%.

=== "Shared fine-tune"

    One model was fine-tuned on all three banks together, so Southbank is inside every weight. The vendor goes back to
    the saved base and fine-tunes it again on Northbank and Eastbank only. Southbank's forms drop to 1.7%, inside the
    range of five re-fine-tunes that never saw Southbank (3.8% ± 3.0%). Northbank reads 84.5% and Eastbank 87.9%. The
    cost is 15,000 example-gradients (one gradient for one training example), 26.3% of a full retrain, and every bank
    gets a new model.

=== "Data in the base"

    Once, to "improve the product for everyone", the vendor trained the base further on a sample of every bank's
    forms, and the adapters were built on top. Now the base itself is derived from Southbank. The vendor must rebuild
    it from the last clean checkpoint and retrain every remaining adapter. That costs 84,000 example-gradients,
    against 57,000 for retraining everything from scratch, so 84,000 ÷ 57,000 = 1.47 times a full retrain. The old
    adapters cannot simply be reused, because each one is tuned to its exact base. On the rebuilt base Eastbank's old
    adapter fell from 89.7% to 84.5%.

??? checkpoint "Checkpoint 3 · In the data-in-the-base design, Eastbank leaves instead. What has to be rebuilt?"
    **The base and every remaining adapter.** Eastbank's forms reached the base, so the base must be rebuilt from the
    last checkpoint without them. Northbank's and Southbank's adapters were trained against a base that held
    Eastbank's data, so they are derived too, and they would lose accuracy on the new base anyway. One customer
    leaving touches every customer.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>0%</strong><span>cost of deleting Southbank's adapter, others bit-for-bit unchanged</span></div>
<div class="is-good"><strong>26.3%</strong><span>of a full retrain to re-fine-tune from the saved base, exact</span></div>
<div class="is-bad"><strong>84,000</strong><span>example-gradients once Southbank reached the base, against 57,000 for everything</span></div>
<div><strong>2,344</strong><span>weights in a rank-4 adapter, about 9% of the base</span></div>
</div>

??? deep "Go deeper · the full results from Lesson 15"
    **Accuracy before anyone leaves.** Southbank's training forms are read perfectly by both designs, which is the
    memorisation the contract requires removing.

    | Model | Northbank | Eastbank | Southbank | Southbank training forms |
    |---|---|---|---|---|
    | Base only | 44.0% | 25.0% | 0.9% | 1.6% |
    | Shared fine-tune | 87.1% | 88.8% | 89.6% | 100.0% |
    | Per-tenant adapters | 82.8% | 91.4% | 84.3% | 100.0% |

    **After removing Southbank from the shared fine-tune.** The gold band comes from five re-fine-tunes that never saw
    Southbank. It is Northbank 85.3%, Eastbank 88.1% and Southbank 3.8%, each ± 3.0 points.

    | Method | Northbank | Eastbank | Southbank |
    |---|---|---|---|
    | Re-fine-tune from base (exact) | 84.5% | 87.9% | 1.7% |
    | Task-vector negation, λ = 0.5 | 82.8% | 82.8% | 14.8% |
    | Task-vector negation, λ = 1.0 | 79.3% | 72.4% | 0.9% |

    At λ = 0.5 Southbank is still above the band. At λ = 1.0 it is gone, but Eastbank has fallen far below its band.

    **Cost in example-gradients.** Retrain everything 57,000 (100%), re-fine-tune from the saved base 15,000 (26.3%),
    task-vector negation 7,500 (13.2%), delete the adapter 0 (0%).

## Limits

**The models are small.** The base has 26,122 weights and the "tenants" are scanner styles on 8 × 8 digits. Real base
models have billions of weights, so every run costs far more. The reason the checkpoint saves money is the same,
though. For a foundation model, skipping pre-training is the difference between millions of dollars and a fine-tuning
job.

**Removing a style removes a skill.** Southbank's data taught the model to read inverted scans, so deleting it also
deletes that skill. When the data is a fact about a person, as in [Language models](language-models.md), the skill to
keep and the fact to remove are much more tangled.

**Adapters only help if they stay separate.** Merging several tenants' adapters into one set of weights, or training
one adapter on several tenants, brings back the shared-fine-tune problem.

## In code

```python
from mul import nn
adapters = {bank: nn.LoRA(base, rank=4, seed=0) for bank in ["north", "east", "south"]}
# train each adapter on its own bank's data only (base stays frozen) ...
del adapters["south"]      # Southbank leaves: exact, free and no other adapter changes
```

`nn.LoRA` holds only the adapter tables in `.params`, so the course's usual training code trains the adapter and never
touches the base.

## Common mistakes

!!! danger "Mistakes people make"
    - **Merging all customers' adapters into one set of weights.** Then they cannot be taken apart again.
    - **Improving the base with customer data.** Then every deletion cascades into rebuilding the base and every adapter.
    - **Not keeping the pre-customer checkpoint.** Then exact removal means retraining from scratch.
    - **Training one shared adapter on every tenant.** An adapter is only removable per tenant if it saw one tenant.
    - **Trusting task-vector negation.** It needs Southbank's data or a stored task vector, and no setting is right for
      every bank.

## Key takeaways

!!! notes "Notes to take"
    - **Fine-tuning.** Keep training a base model on new data. A shared fine-tune spreads every tenant through every weight.
    - **LoRA.** Freeze the base and add \(\Delta W = A \cdot B\) per tenant. Rank 4 gives 2,344 weights, about 9% of the base.
    - **Why small.** A rank-4 change to a 128 × 128 layer is 1,024 numbers instead of 16,384.
    - **Adapter deletion.** Exact, 0% cost, other adapters bit-for-bit unchanged.
    - **Shared fine-tune.** Re-fine-tune from the saved base without the tenant. Exact, 26.3% of a full retrain.
    - **Task-vector negation.** 13.2%, approximate, no setting right for every bank.
    - **Cascade.** Tenant data in the base means rebuilding it and every adapter, 84,000 against 57,000.
    - **Rule.** Keep the checkpoint from before customer data entered, and keep customer data out of the base.

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
- q: Why is a rank-4 adapter so much smaller than a full change to a 128 × 128 layer?
  options:
    - It skips half of the neurons.
    - It builds the change from two thin tables, 128 × 4 and 4 × 128, which hold 1,024 numbers instead of 16,384.
    - It stores the change at lower precision.
  answer: 1
  why: The product A · B has the full 128 × 128 shape, but only the two thin tables are stored and trained.
- q: Southbank's forms are read 100% right in training but less well on its held-out forms. What does that show?
  options:
    - The model is broken.
    - The held-out forms were mislabelled.
    - The fine-tune memorised Southbank's data, which the contract requires removing.
  answer: 2
  why: Being better on the exact forms it trained on than on similar new ones is memorisation, the same pattern as Carol in Lesson 04.
- q: What makes deleting Southbank's adapter exact?
  options:
    - The adapter is the only part of the system that ever learnt from Southbank's data.
    - Adapters are always deleted at night.
    - The base model forgets Southbank on its own.
  answer: 0
  why: The base was frozen and trained only on public data, and every other adapter saw only its own bank. Nothing else holds Southbank.
- q: The vendor merges all three banks' adapters into one set of weights for faster serving. What happens to deletion?
  options:
    - Nothing changes.
    - Southbank can no longer be removed by deleting a file, so it is back to the shared-fine-tune problem.
    - Deletion becomes free for every bank.
  answer: 1
  why: Once the changes are summed into the same weights, there is no separate piece that only Southbank shaped.
```

## Try it

!!! levelup "Level up"
    You can now explain fine-tuning and LoRA and pick the cheapest exact way to remove a customer. Next quest,
    [Recommender systems](recommender-systems.md), where one person's taste is spread over every item they rated.

- Read the concept page [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md).
- Run the lesson [15 · Fine-tuning and un-finetuning](../lessons/15-fine-tuning-and-un-finetuning.md).
- In the notebook, change the adapter rank to 1 and to 16 and see how accuracy and memorisation of Southbank change.
