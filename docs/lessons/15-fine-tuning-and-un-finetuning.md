---
title: "Lesson 15 · Fine-tuning and un-finetuning"
description: Remove a customer from a shared fine-tune, from per-customer LoRA adapters and from a contaminated base, and price each option.
---

# Lesson 15 · Fine-tuning and un-finetuning, when a customer leaves

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~45 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 9</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/15-Fine-Tuning-and-Un-Finetuning.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/15-Fine-Tuning-and-Un-Finetuning.ipynb){ .md-button }
</div>

## The story

A vendor sells a document reader to three banks. Each bank's scanners look different; Southbank's archive scans are
colour-inverted. The vendor adapts a base model to each bank. Southbank ends its contract, which says to delete all customer data **and any models or model components derived from it** within 30 days.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a base model, then customise it in two ways, with one shared fine-tune and with per-bank LoRA adapters.</li>
<li markdown>**Show the issue**: both are 100% right on Southbank's training forms.</li>
<li markdown>**Untrain** in three ways. Re-fine-tune from the base, use task-vector negation and delete the adapter.</li>
<li markdown>**Show the result** against a gold band of 5 re-fine-tunes.</li>
<li markdown>**Price** each option, then test the cascade when bank data reached the base.</li>
</ol>

## Key results

The base model has 26,122 weights. Each rank-4 LoRA adapter has 2,344 weights (9.0% of the base). The base alone could
barely read Southbank's scans (0.9%); both customisations reached about 84% to 90%.

| Method | Northbank | Eastbank | Southbank |
|---|---|---|---|
| Gold band (never saw Southbank) | 85.3% | 88.1% | 3.8% |
| Re-fine-tune from base (exact) | 84.5% | 87.9% | 1.7% |
| Task-vector negation, λ = 0.25 | 84.5% | 85.3% | 57.4% |
| Task-vector negation, λ = 1.0 | 79.3% | 72.4% | 0.9% |
| Per-bank adapters, Southbank's deleted | 82.8% | 91.4% | N/A |

Task-vector negation is a dial with no right setting. Erase Southbank and the other banks suffer; protect them and
Southbank is still recognised. Deleting the adapter left the other adapters **bit-for-bit unchanged**.

**The price** (share of a full retrain): retrain everything 100%; re-fine-tune from saved base **26.3%**; task-vector
negation 13.2%; delete the adapter **0%**.

**The cascade.** If the vendor once improved the base with every bank's data, deleting Southbank costs 84,000
example-gradients (rebuild the base and retrain every adapter), against 0 with a clean base. Old adapters on the rebuilt
base also lost accuracy (Eastbank 89.7% → 84.5%).

## Concepts used here

- [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)
- [SISA, sharded training](../unlearning/sisa.md)

## Quiz

```quiz
- q: How big was each LoRA adapter compared with the base?
  options:
    - About 9%
    - About 50%
    - Twice as big
  answer: 0
  why: 2,344 trainable weights against 26,122 in the base.
- q: What did deleting Southbank's adapter do to the other banks' adapters?
  options:
    - Nothing; they were bit-for-bit unchanged.
    - It retrained them.
    - It deleted them too.
  answer: 0
  why: Each adapter only ever saw its own bank's data.
- q: What did re-fine-tuning from the saved base cost?
  options:
    - 26.3% of a full retrain
    - 100%
    - 0%
  answer: 0
  why: You never need to go further back than the checkpoint before the customer's data entered.
- q: At λ = 1.0, task-vector negation removed Southbank. What was the catch?
  options:
    - Eastbank's accuracy fell from about 88% to 72%.
    - Southbank came back.
    - It cost more than a retrain.
  answer: 0
  why: It cannot match the exact result on the leaving and remaining banks at the same time.
- q: What causes a deletion "cascade"?
  options:
    - Customer data having reached the shared base model
    - Using too many adapters
    - Keeping a checkpoint
  answer: 0
  why: Every adapter depends on the base, so the base and all adapters must be rebuilt.
```

## Open question → Lesson 16

Here, removing a scanner style removed a capability too. What about a language model fine-tuned on a staff directory,
where a specific **fact**, a phone number, must go, and a polite refusal can look like forgetting?

[On to Lesson 16, LLM unlearning :material-arrow-right:](16-llm-unlearning.md){ .md-button }
