---
title: Unlearning a fine-tune
description: When a customer leaves, per-customer adapters make deletion exact and free, a saved base makes it exact and affordable, and data in the base makes it a cascade.
---

# Unlearning a fine-tune

!!! oneline "In one line"
    When a customer leaves, how you fine-tuned decides the cost. Deleting their **adapter** is exact and free, re-fine-tuning from the **saved base** is exact and affordable, and customer data in the **base** forces a cascade.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - name the four ways to remove a customer from a fine-tuned model and price each one,
    - explain why task-vector negation has no setting that works for everyone,
    - spot the design choice that turns one customer leaving into a rebuild of everything.

## Why it matters

Business AI is usually a **base model** fine-tuned for each customer. Contracts increasingly require the company to
delete all customer data **and any models or model components derived from it** when the contract ends. After the FTC's model-deletion orders, such
clauses are enforced. The architecture you chose on day one decides whether honouring them costs nothing or more than a
full retrain.

The choice is made long before anyone leaves. A team that pools every customer into one fine-tuned model has tied each
customer to everyone else. A team that gives each customer a separate add-on can remove one by deleting a file. And a
team that once used customer data to "improve the base for everyone" has tied every customer to every other customer
through the one part they all share. Lesson 15 puts a price on each of these choices.

## A simple example

A trained chef learns each restaurant's recipes. If each restaurant's recipes are in a separate notebook, throw that
notebook away when the restaurant leaves. If they were mixed into one notebook, you must rewrite it. And if a leaving
restaurant's recipes were copied into the chef's *basic training*, every restaurant's notebook was built on top of them.

!!! simply "Explain it simply"
    Ask one question about every model you ship. "Which customers' data went into this, and what was it built on?"
    If the answer is "one customer, on a clean base", deleting that customer is easy. If the answer is "everyone",
    deleting one customer means rebuilding it.

Now map the picture onto Lesson 15. The chef is a base model that reads handwritten figures on scanned forms. The
restaurants are three bank customers, called **tenants**. Northbank's scans are thick and smudged, Eastbank's are
shifted by a pixel and Southbank's archive scans are colour-inverted. Southbank ends its contract, so the model must
forget Southbank's forms and keep reading the other two banks'.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Base model** | A model trained once on broad data, which customer models build on | 26,122 weights, trained on the vendor's 700 public digits |
| **Tenant** | One customer whose data and model parts must stay apart from the others | Northbank, Eastbank and Southbank, 250 training forms each |
| **Shared fine-tune** | One copy of the base trained further on every tenant's data pooled together | One model that serves all three banks |
| [Adapter (LoRA)](../start-here/glossary.md#a) | A small set of extra weights trained for one tenant on top of a frozen base | Southbank's rank-4 adapter, 2,344 weights |
| [Checkpoint](../start-here/glossary.md#c) | A saved copy of a model's weights at one moment | The base, saved before any bank's data entered |
| [Task vector](../start-here/glossary.md#t) | The change a fine-tune made to the weights, fine-tuned minus base | The base fine-tuned on Southbank alone, minus the base |
| Example-gradient | The course's unit of cost, one example passed through training once. Epochs times examples | A 30-epoch fine-tune on 500 forms costs 15,000 |
| [Lineage registry](../start-here/glossary.md#l) | A record of which customers' data reached every model, directly or through a parent | "Base v2 contains 100 forms from each bank" |

## How it works

<!-- diagram: unlearning-fine-tunes -->

Lesson 15, a document reader serves three banks. Southbank leaves. The base has 26,122 weights; each rank-4 LoRA
adapter has 2,344 (about 9%). See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md) for the basics.

The figure has two halves. On the left, each bank has its own small adapter on one clean frozen base. Southbank's adapter
is crossed out. On the right, every bank's data was fine-tuned into one model, so Southbank is mixed in with
the others. The line along the bottom is the trap, customer data that reached the base itself.

Before anything is removed, both designs read the banks' scans well. The base alone read only 0.9% of Southbank's
held-out forms, because it had never seen an inverted scan. The shared fine-tune reached 89.6% on them and Southbank's
adapter 84.3%. Both were **100% right on Southbank's own training forms**, which is more than on its held-out forms. That gap
means the models memorised Southbank's data, just as the network memorised Carol in Lesson 04. The contract asks for
that memory to go.

### Three ways to remove a customer

| Design | How Southbank is removed | Exact? | Cost (% of a full retrain) | Touches others? |
|---|---|---|---|---|
| **Per-customer adapters**, clean base | Delete the adapter | ✅ | **0%** | No, bit-for-bit unchanged |
| Shared fine-tune | Re-fine-tune from the saved base | ✅ | 26.3% | Everyone gets a new model |
| Shared fine-tune | Task-vector negation | ❌ | 13.2% | Yes, and it hurts them |
| Customer data in the base | Rebuild base, retrain every adapter | ✅ | **More than 100%** | Yes, all of them |

Read the table one row at a time.

**Delete the adapter.** Southbank's adapter only ever saw Southbank's forms, and the base never changed. Throw the
adapter away and what is left is exactly what you would have built if Southbank had never signed. The lesson checked
that Northbank's and Eastbank's adapters were bit-for-bit unchanged, so their scores stayed at 82.8% and 91.4%.

**Re-fine-tune from the saved base.** The shared model mixed all three banks, so it cannot be taken apart. But the base
checkpoint was saved before any bank's data entered. Fine-tune that checkpoint again on Northbank's and Eastbank's 500
forms, and you get a model that never saw Southbank. It is exact, and it skips the whole pre-training run. This is the
checkpoint idea of [SISA](sisa.md) applied to time, since you only rewind to the moment the leaving data arrived.

**Negate the task vector.** This is a cheap edit of the shared model, explained in the next section. It is not exact.

**Rebuild the base.** This is the cascade, covered last.

??? checkpoint "Checkpoint 1 · Eastbank also leaves next month. With per-bank adapters on a clean base, what does that cost and whose model changes?"
    **Nothing, and nobody else's.** Delete Eastbank's adapter. The base is frozen and Northbank's adapter only ever
    saw Northbank's forms, so both stay bit-for-bit the same. The cost is 0 example-gradients, however many tenants
    leave, as long as no tenant's data ever reached the base.

### Task-vector negation is a dial with no right setting

Subtracting a fine-tune's weight change, scaled by λ (the "task vector" of Ilharco et al. 2023), is cheap. But look at the results.

- At λ = 0.25, Southbank was still 57% recognised;
- At λ = 1.0, Southbank was gone, but Eastbank dropped from 88.8% to 72.4%.

You cannot match the exact result on the leaving customer and the remaining ones at the same time. And it needs
Southbank's data (or a stored task vector) *after* the contract says to delete it.

Here is how the method works. First fine-tune a copy of the base on Southbank's forms alone. The difference between
that copy and the base is Southbank's task vector, the direction in which Southbank's data moved the weights. Then
subtract λ times that vector from the shared model. λ is a dial. At 0 nothing changes, and at 1 you subtract the whole
change.

The trouble is that the shared model did not learn Southbank on its own. It learnt all three banks together, and much
of what Southbank's forms taught (how to read digits in general) also helps the other banks. So the subtraction takes
some of their skill away too. And the right λ can only be judged by comparing with the exact re-fine-tune, which is the
very model you were trying to avoid building.

??? deep "Go deeper · the whole dial, against the gold band"
    The gold band comes from 5 re-fine-tunes with seeds 100 to 104 that never saw Southbank, using the course's rule of
    the mean plus or minus the larger of two standard deviations and 3 points. Here every column's half-width came out
    at the 3-point floor.

    | Model | Northbank | Eastbank | Southbank | Southbank training forms |
    |---|---|---|---|---|
    | Gold band | 85.3% ± 3.0 | 88.1% ± 3.0 | 3.8% ± 3.0 | 6.2% ± 3.0 |
    | Shared fine-tune, before | 87.1% | 88.8% | 89.6% | 100.0% |
    | Re-fine-tune from base, exact | 84.5% | 87.9% | 1.7% | 5.6% |
    | Negation λ = 0.25 | 84.5% | 85.3% | 57.4% | 72.4% |
    | Negation λ = 0.5 | 82.8% | 82.8% | 14.8% | 15.6% |
    | Negation λ = 0.75 | 81.9% | 77.6% | 4.3% | 4.0% |
    | Negation λ = 1.0 | 79.3% | 72.4% | 0.9% | 0.4% |
    | Negation λ = 1.5 | 72.4% | 63.8% | 0.0% | 0.0% |

    The exact re-fine-tune lands inside the band in every column, because it *is* one of those models with a different
    seed. Negation never does. At λ = 0.5, Southbank's training forms are still at 15.6%, above the band's top of 9.2%,
    and Eastbank is already below its band's bottom of 85.1%. From λ = 0.75 on, Southbank looks forgotten but both
    other banks are below their bands. At λ = 1.0, Southbank's training forms fall to 0.4%, below the band's bottom of
    3.2%, which is over-forgetting as well. This is the Lesson 08 story of gradient ascent with no reference, in a new
    costume.

??? checkpoint "Checkpoint 2 · At λ = 0.75, Southbank's training forms score 4.0%, inside the band of 3.2% to 9.2%. Is λ = 0.75 the fix?"
    **No.** Southbank passes, but Eastbank fell to 77.6% against a band that starts at 85.1%, and Northbank fell to
    81.9% against a band that starts at 82.3%. The remaining customers pay for the removal. And you could only find
    this out by building the exact re-fine-tunes, which would have been the better answer all along.

### The cascade

If the vendor once improved the **base** with every bank's data, Southbank's data sits inside the frozen base that every
adapter depends on. Then the base must be rebuilt from the last clean checkpoint, and **every** adapter retrained. Old
adapters on the rebuilt base lost accuracy (Eastbank 89.7% → 84.5%) because each adapter is tuned to its exact base.

In the lesson, the vendor trained a new base on its 700 public digits plus 100 forms from each bank, called
"base v2". The adapters were then trained on top of v2. There are two reasons the adapters must be retrained after
Southbank leaves.

- **They stop fitting.** An adapter is a small correction tuned to one exact base. Plug Northbank's old adapter into
  the rebuilt base and it fell from 87.9% to 86.2%. Eastbank's fell from 89.7% to 84.5%.
- **They are derived from Southbank's data.** Each adapter was optimised against a base that contained Southbank's
  forms. Under a "derived models" clause, that makes them derived too.

Retraining the adapters on the rebuilt base brought Northbank to 88.8% and Eastbank to 91.4%. So the accuracy can be
recovered, but only by paying for every tenant again.

!!! tip "Three design rules"
    1. **Keep the checkpoint from before customer data entered.** Exact un-finetuning never needs to go further back.
    2. **Isolate customers in their own adapters.** Never merge adapters from different customers into one set of weights.
    3. **Keep customer data out of the shared base**, and track **lineage**, meaning which customers' data reached every artefact.

??? checkpoint "Checkpoint 3 · Base v2 holds 100 forms from each bank. Eastbank leaves instead of Southbank. Which models must be rebuilt?"
    **The base and every remaining adapter.** Base v2 contains Eastbank's forms, so it must be rebuilt from the clean
    checkpoint. Northbank's and Southbank's adapters were trained against base v2, so they are derived from Eastbank's
    data and must be retrained on the new base. A lineage registry answers this as a lookup of every artefact that
    descends from Eastbank's data.

## A worked example

Follow Southbank's 30 days, using the shared fine-tune, which is the design that needs real work.

1. **What is inside.** The shared model was fine-tuned on 750 forms, 250 from each bank. It is 100% right on
   Southbank's 250 training forms.
2. **The target.** Five re-fine-tunes without Southbank score 6.2% ± 3.0 on those forms, so 3.2% to 9.2%. A model
   that never saw inverted scans can hardly read them, so the honest answer is close to zero.
3. **The exact fix.** Re-fine-tune the saved base on the 500 forms of Northbank and Eastbank. It scores 5.6% on
   Southbank's training forms, inside the band. Northbank is at 84.5% (band 82.3% to 88.3%) and Eastbank at 87.9%
   (band 85.1% to 91.1%). Every check passes.
4. **The bill.** Pre-training the base took 60 epochs on 700 digits, so 42,000 example-gradients. The fine-tune is 30
   epochs on 500 forms, so 15,000. Retraining everything would cost 42,000 + 15,000 = 57,000. The re-fine-tune costs
   15,000 out of 57,000, which is 26.3%.
5. **The shortcut that fails.** Task-vector negation costs 7,500 (30 epochs on Southbank's 250 forms), which is 13.2%.
   It is half the price, but no setting of λ passes every column, and it needs Southbank's forms again after the
   contract says to delete them.
6. **The cascade.** If base v2 had contained Southbank's forms, the bill becomes 60 epochs on 900 examples (700 public
   plus 100 from each remaining bank) to rebuild the base, which is 54,000, plus 15,000 for each of the two remaining
   adapters. That is 84,000 example-gradients, about 147% of the full retrain of 57,000.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>0%</strong><span>delete Southbank's adapter, exact, others bit-for-bit unchanged</span></div>
<div class="is-good"><strong>26.3%</strong><span>re-fine-tune from the saved base, exact, inside the band</span></div>
<div class="is-bad"><strong>72.4%</strong><span>Eastbank after negation at λ = 1.0, down from 88.8%</span></div>
<div class="is-bad"><strong>84,000</strong><span>example-gradients for the cascade, against 0 with a clean base</span></div>
</div>

The two exact routes differ by more than cost. Deleting an adapter touches no one. Re-fine-tuning is exact for
Southbank, but every remaining bank gets a new model, which may need its own testing and sign-off. Negation is the only
route that is neither exact nor safe for the others.

## Limits

**The tenants are scanner styles.** Removing Southbank's forms also removed a skill, reading inverted scans. When the
data to remove is one fact inside a skill the model keeps, such as a phone number in a language model, the picture
changes. That is [the next page](llm-unlearning.md).

**Adapters are only as clean as their base.** Deleting an adapter is exact only if no tenant's data ever reached the
base. A single "improve the product for everyone" run breaks that, often without anyone writing it down.

**The setting is small.** The lesson uses 8 × 8 digit images, a network of 26,122 weights and a gold band of only 5
re-fine-tunes. The ratios carry over, because a foundation model's pre-training dwarfs a fine-tune even more. The exact
percentages will differ.

??? deep "Go deeper · two more limits"
    **Isolation has a running cost.** Per-tenant adapters need one adapter per tenant and a serving stack that sends
    each request to the right one. Serving many adapters on one base is standard for language models today, but it is
    a price paid every day, not only when someone leaves.

    **A merged adapter is no longer an adapter.** Folding an adapter into its own copy of the base for faster serving
    is fine, since that copy still belongs to one tenant. Summing the changes of several tenants into one set of
    weights is the shared fine-tune again, and the free deletion is gone.

!!! tip "What to do in practice"
    - Save a base checkpoint before any customer data enters, and record where it is.
    - Give each customer their own adapter, and keep merged copies per customer.
    - Keep a lineage registry that lists, for every artefact, which customers' data reached it.
    - Treat any training of the shared base on customer data as a decision that makes every later deletion a cascade.
    - Never plan to rely on task-vector negation, because choosing λ needs the exact model anyway.

## In code

??? deep "Go deeper · the three removals with the course library"
    ```python
    from mul import train
    from mul.nn import MLP, LoRA

    # One frozen base, one rank-4 adapter per bank, trained only on that bank's forms
    adapters = {n: train.fit(LoRA(base, rank=4, seed=10 + i), T[n]["Xtr"], T[n]["ytr"], seed=1, **ADAPT)
                for i, n in enumerate(TENANTS)}

    # 1. Delete the adapter. Exact and free.
    adapters_after = {n: a for n, a in adapters.items() if n != "Southbank"}

    # 2. Re-fine-tune the saved base on the banks that remain. Exact, costs one fine-tune.
    #    shared_finetune clones the base and fine-tunes it on the named banks' pooled forms.
    refit = shared_finetune(["Northbank", "Eastbank"])

    # 3. Task-vector negation. Cheap, not exact, and needs Southbank's data.
    tau = [c - b for c, b in zip(southbank_only.params, base.params)]
    negated = train.clone(shared)
    negated.params = [s - lam * t for s, t in zip(shared.params, tau)]
    ```

    `LoRA` in `mul/nn.py` keeps the base frozen and trains only its small matrices, so `train.fit` works on an adapter
    unchanged. The lesson checks that the remaining adapters are untouched with `train.weights_equal`.

## Common mistakes

!!! danger "Mistakes people make"
    - **Merging adapters for faster serving** across customers. They can no longer be taken apart.
    - **Improving the base with customer data.** Every deletion then cascades.
    - **Relying on task-vector negation.** It is uncalibrated and needs the deleted data.
    - **Throwing away the pre-customer checkpoint.** Without it, the only exact route left is a full retrain.
    - **Plugging old adapters into a rebuilt base.** They lose accuracy and are still derived from the deleted data.

## Key takeaways

!!! notes "Notes to take"
    - **Four routes.** Delete the adapter 0%, re-fine-tune from the saved base 26.3%, negation 13.2% and the cascade more than 100%.
    - **Adapters.** Rank 4 means 2,344 weights, about 9% of the 26,122-weight base. Deleting one is exact and free.
    - **Isolation.** The other adapters stayed bit-for-bit the same, at 82.8% and 91.4%.
    - **Saved base.** Exact un-finetuning never needs to rewind past the point where the customer's data entered.
    - **Negation trap.** At λ = 1.0, Southbank was gone but Eastbank fell from 88.8% to 72.4%. No λ passes every bank.
    - **Negation needs the data.** It uses Southbank's forms or a stored task vector after the contract says delete.
    - **Cascade.** Customer data in the base means rebuilding it and every adapter, 84,000 example-gradients here.
    - **Stale adapters.** On a rebuilt base, Eastbank's old adapter fell from 89.7% to 84.5%.
    - **Lineage.** Record which customers' data reached every artefact, so deletion is a lookup.

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
- q: Why did re-fine-tuning from the saved base cost 26.3% of a full retrain and not 100%?
  options:
    - It used a smaller learning rate.
    - It skipped pre-training, because the saved base never saw any bank's data.
    - It only retrained Southbank's part of the model.
  answer: 1
  why: The fine-tune cost 15,000 example-gradients out of 57,000. The 42,000 for pre-training did not need repeating.
- q: At λ = 0.75, Southbank's training forms fell to 4.0%, inside the band. Why is that still not a good fix?
  options:
    - Southbank's adapter was still stored.
    - The band was built wrongly.
    - Eastbank fell to 77.6%, far below its band, so the other banks paid for it.
  answer: 2
  why: An unlearnt model must pass on the remaining customers too. Only the exact re-fine-tune passed every column.
- q: After the base was rebuilt without Southbank, Eastbank's old adapter fell from 89.7% to 84.5%. Why?
  options:
    - An adapter is a small correction tuned to the exact base it was trained on.
    - Eastbank's data was deleted by mistake.
    - The rebuilt base was trained for fewer epochs.
  answer: 0
  why: Change the base and the correction no longer fits. The adapter also counts as derived from Southbank's data.
- q: Why does task-vector negation clash with a contract that says delete the customer's data?
  options:
    - It makes the model larger.
    - It needs Southbank's data, or a task vector built from it, at the moment of deletion.
    - It only works on adapters.
  answer: 1
  why: The task vector is the base fine-tuned on Southbank minus the base, so building it needs the data you were told to delete.
```

## Try it

!!! levelup "Level up"
    You can now price a customer's exit from a fine-tuned model and name the design that keeps it free. Next quest,
    [Unlearning in language models](llm-unlearning.md), where what must go is one fact and a refusal can pass for
    forgetting.

- Read the next concept, [Unlearning in language models](llm-unlearning.md).
- Run the lesson [15 · Fine-tuning and un-finetuning](../lessons/15-fine-tuning-and-un-finetuning.md).
- In the notebook, change the adapter rank to 1 and to 16 and see how size, accuracy and memorisation move.
- See how lineage becomes a deletion playbook in [The enterprise playbook](enterprise-playbook.md).
