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

!!! mission "Your mission · about 45 minutes · 3 checkpoints"
    By the end of this lesson you can

    - build a shared fine-tune and per-bank LoRA adapters on one base, and show that both memorise a bank's forms,
    - remove that bank in three ways and judge each against a gold band,
    - price every option in example-gradients, including the cascade when bank data reached the base.

## The story

A vendor sells a document reader to three banks. Each bank's scanners look different; Southbank's archive scans are
colour-inverted. The vendor adapts a base model to each bank. Southbank ends its contract, which says to delete all customer data **and any models or model components derived from it** within 30 days.

Until now, every model in the course was trained once, from scratch, on one dataset. Business AI is built differently.
A **base model** is trained on broad data, then **fine-tuned** for each customer on their private data. That changes
what "unlearn" means, and it gives a new place to make it cheap. Northbank's scans are thick and smudged and
Eastbank's are shifted by a pixel. Both banks are staying, and they expect their models to keep working while
Southbank is removed.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a base model, then customise it in two ways, with one shared fine-tune and with per-bank LoRA adapters.</li>
<li markdown>**Show the issue.** Both are 100% right on Southbank's training forms.</li>
<li markdown>**Untrain** in three ways. Re-fine-tune from the base, use task-vector negation and delete the adapter.</li>
<li markdown>**Show the result** against a gold band of 5 re-fine-tunes.</li>
<li markdown>**Price** each option, then test the cascade when bank data reached the base.</li>
</ol>

## What each step teaches

**Step 1. Two ways to customise.** The base (64 → 128 → 128 → 10) is trained on the vendor's 700 public digits only.
The shared fine-tune trains *every* weight of a copy of it on all three banks' 750 forms pooled. The adapters keep the
base frozen and train a small rank-4 add-on per bank, on that bank's 250 forms alone. The step shows that both designs
work. The adapters reach about the same accuracy with 9% of the weights.

**Step 2. The memory to remove.** Both designs are 100% right on Southbank's training forms and less on its held-out
forms. That gap is memorisation, as with Carol in Lesson 04, and it is what the contract asks to remove.

**Step 3. Three removals.** Deleting the adapter is checked bit for bit. Re-fine-tuning reuses the saved base
checkpoint. Task-vector negation fine-tunes the base on Southbank alone, takes the weight change and subtracts λ times
it from the shared model, for five values of λ.

??? deep "Go deeper · what task-vector negation needs, and why that matters"
    The task vector is "the base fine-tuned on Southbank alone" minus "the base". To build it you need Southbank's
    forms, either when Southbank joined (and you stored the vector) or now, after the contract says to delete them.
    The idea comes from Ilharco et al. (2023). The notebook writes it in three lines, a copy of the shared model whose
    weights are `shared − λ × (southbank_only − base)`.

**Step 4. The gold band.** Five re-fine-tunes with seeds 100 to 104 never saw Southbank. The band is their mean plus or
minus the larger of two standard deviations and 3 points, the same rule as the course's audit. Every option is
measured on all three banks and on Southbank's training forms.

**Step 5. The bill and the cascade.** Cost is counted in example-gradients, one example through training once, so
epochs times examples. Step 5b then builds a "base v2" from the public digits plus 100 forms from each bank, trains
adapters on it and asks what deleting Southbank costs now.

## Key results

The base model has 26,122 weights. Each rank-4 LoRA adapter has 2,344 weights (9.0% of the base). The base alone could
barely read Southbank's scans (0.9%); both customisations reached about 84% to 90%.

<div class="stats">
<div class="is-good"><strong>0%</strong><span>delete Southbank's adapter, others bit-for-bit unchanged</span></div>
<div class="is-good"><strong>26.3%</strong><span>re-fine-tune from the saved base, inside the band</span></div>
<div class="is-bad"><strong>72.4%</strong><span>Eastbank after negation at λ = 1.0</span></div>
<div class="is-bad"><strong>84,000</strong><span>example-gradients for the cascade</span></div>
</div>

| Method | Northbank | Eastbank | Southbank |
|---|---|---|---|
| Gold band (never saw Southbank) | 85.3% | 88.1% | 3.8% |
| Re-fine-tune from base (exact) | 84.5% | 87.9% | 1.7% |
| Task-vector negation, λ = 0.25 | 84.5% | 85.3% | 57.4% |
| Task-vector negation, λ = 1.0 | 79.3% | 72.4% | 0.9% |
| Per-bank adapters, Southbank's deleted | 82.8% | 91.4% | N/A |

Task-vector negation is a dial with no right setting. Erase Southbank and the other banks suffer; protect them and
Southbank is still recognised. Deleting the adapter left the other adapters **bit-for-bit unchanged**.

Read the rows that matter. Every band is ± 3.0 points, so Northbank's runs from 82.3% to 88.3%, Eastbank's from 85.1%
to 91.1% and Southbank's from 0.8% to 6.8%. **The re-fine-tune** is inside all three, because it *is* one of those
models with another seed. **Negation at λ = 0.25** leaves Southbank at 57.4%, far above its band. **At λ = 1.0**,
Southbank is gone but Northbank and Eastbank are both below their bands. **The adapters** score exactly what they
scored before the deletion, because nothing about them changed.

??? checkpoint "Checkpoint 1 · At λ = 0.5, negation gives Northbank 82.8%, Eastbank 82.8% and Southbank's training forms 15.6%. Which checks pass?"
    **Only Northbank.** 82.8% is inside its band of 82.3% to 88.3%. Eastbank's band starts at 85.1%, so it fails.
    Southbank's training forms have a band of 6.2% ± 3.0, so 3.2% to 9.2%, and 15.6% is still above it. Negation
    already hurts Eastbank before it has removed Southbank.

**The price** (share of a full retrain). Retrain everything 100%; re-fine-tune from saved base **26.3%**; task-vector
negation 13.2%; delete the adapter **0%**.

The working is short. Pre-training cost 60 epochs × 700 digits = 42,000 example-gradients, and the fine-tune 30 epochs
× 500 forms = 15,000, so a full retrain is 57,000. The re-fine-tune is 15,000 of 57,000, or 26.3%. Negation needs a
fine-tune on Southbank's 250 forms, 30 × 250 = 7,500, or 13.2%.

??? checkpoint "Checkpoint 2 · Why does the re-fine-tune never need the 42,000 example-gradients of pre-training?"
    **Because the base never saw any bank.** It was trained on the vendor's public digits and saved before customer
    data entered. Everything before that checkpoint is already a model that never saw Southbank, so the rebuild can
    start there. This is SISA's checkpoint idea from Lesson 07, applied to the model's history.

**The cascade.** If the vendor once improved the base with every bank's data, deleting Southbank costs 84,000
example-gradients (rebuild the base and retrain every adapter), against 0 with a clean base. Old adapters on the rebuilt
base also lost accuracy (Eastbank 89.7% → 84.5%).

| Northbank and Eastbank in Step 5b | Northbank | Eastbank |
|---|---|---|
| Adapters on base v2, before | 87.9% | 89.7% |
| Old adapters on the rebuilt base | 86.2% | 84.5% |
| Adapters retrained on the rebuilt base | 88.8% | 91.4% |

The middle row shows why the old adapters cannot be kept. Each one is a correction tuned to one exact base, so it fits
the rebuilt base worse. It was also trained against a base that held Southbank's forms, so it counts as derived. The
84,000 is 60 epochs × 900 examples to rebuild the base (54,000) plus 15,000 for each of the two remaining adapters.

??? checkpoint "Checkpoint 3 · The 84,000 example-gradients of the cascade is what share of a full retrain of 57,000?"
    **About 147%.** 84,000 ÷ 57,000 is about 1.47. One customer leaving now costs more than retraining everything once,
    because the base and every remaining customer's adapter must be built again.

## Limits of this lesson

**Tenants are scanner styles.** Removing Southbank's forms also removed a skill, reading inverted scans. A language
model asked to forget one fact, while keeping the skill around it, is harder. That is Lesson 16.

**A small band.** The gold band has only 5 re-fine-tunes, and every column hit the 3-point floor. A wider study would
measure the spread with more seeds.

**No band for the adapters.** The band was built for the shared fine-tune. The adapters are exact by construction, so
the lesson checks them bit for bit instead of against a band.

**Small models.** 8 × 8 digit images and a 26,122-weight base. The ratios carry over to foundation models, where
pre-training is far larger than a fine-tune, but the exact percentages will not.

## Concepts used here

- [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md)
- [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md)
- [SISA, sharded training](../unlearning/sisa.md)

## Notes to take

!!! notes "Notes to take"
    - **Setting.** A 26,122-weight base, three banks with 250 training forms each, Southbank leaves.
    - **Adapters.** Rank 4, 2,344 weights, 9.0% of the base. Deleting one is exact, free and touches no one.
    - **Memorisation.** Both designs were 100% right on Southbank's training forms.
    - **Exact re-fine-tune.** From the saved base, 26.3% of a full retrain, inside the band on every column.
    - **Negation.** 13.2%, but no λ passes every bank. λ = 1.0 drops Eastbank from 88.8% to 72.4%.
    - **Negation needs the data.** Building the task vector uses Southbank's forms.
    - **Cascade.** Bank data in the base costs 84,000 example-gradients, about 147% of a full retrain.
    - **Stale adapters.** On the rebuilt base Eastbank's old adapter fell from 89.7% to 84.5%.

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
- q: Both the shared fine-tune and Southbank's adapter were 100% right on Southbank's training forms but less on its held-out forms. What does that gap show?
  options:
    - The held-out forms were mislabelled.
    - The models memorised Southbank's training data.
    - The adapters were too small.
  answer: 1
  why: Doing better on the exact forms you trained on than on new ones is memorisation, which is what the contract asks to remove.
- q: Why did the re-fine-tune land inside the gold band on every bank?
  options:
    - It was tuned until it passed.
    - It used a larger learning rate.
    - It is made the same way as the band's models, with only the seed different.
  answer: 2
  why: The band comes from re-fine-tunes that never saw Southbank, and the exact fix is one more of them.
- q: Why must old adapters be retrained after the base is rebuilt without Southbank?
  options:
    - They fit the new base worse, and they were trained against a base that held Southbank's data.
    - They are larger than the new base.
    - The contract only covers adapters.
  answer: 0
  why: Eastbank's old adapter fell from 89.7% to 84.5% on the rebuilt base, and it counts as derived from Southbank's data.
```

## Open question → Lesson 16

!!! levelup "Level up"
    You can now remove a customer from a fine-tuned model three ways, judge each against a band and price the
    cascade. Next quest, [Lesson 16 · LLM unlearning](16-llm-unlearning.md), where what must go is one fact.

Here, removing a scanner style removed a capability too. What about a language model fine-tuned on a staff directory,
where a specific **fact**, a phone number, must go, and a polite refusal can look like forgetting?

[On to Lesson 16, LLM unlearning :material-arrow-right:](16-llm-unlearning.md){ .md-button }
