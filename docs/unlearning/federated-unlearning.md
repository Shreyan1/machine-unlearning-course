---
title: Federated unlearning
description: Forgetting one participant when the model was trained across phones or hospitals that never shared their data.
---

# Federated unlearning

!!! oneline "In one line"
    In **federated learning** the server never sees the data, so forgetting a participant means undoing their updates
    without having their data, after many later rounds were built on top of them.

## Why it matters

Federated learning trains one model across many devices or organisations, such as phones learning a keyboard's next
word, or hospitals training a diagnosis model, while the raw data stays where it is. Each participant trains on its
own data and sends back only an **update** to the model. The server averages the updates, sends the new model out,
and repeats for many rounds.

Participants leave. A user deletes their account; a hospital leaves a research consortium. Their influence is now
mixed into every later round, and the server cannot simply retrain on their data, because it never had it.

## A simple example

A recipe is passed from kitchen to kitchen, and each kitchen adjusts it a little before passing it on. After fifty
passes, one kitchen asks for its changes to be taken out. Nobody has that kitchen's notes, and every later kitchen
adjusted the recipe it received, so the changes are woven through every version since.

## How it works

### What can be forgotten

| Level | Example |
|---|---|
| **A whole client** | a hospital leaves the consortium |
| **Some of a client's data** | a patient withdraws consent at one hospital |
| **A class or a feature** | stop recognising one category everywhere |

### The main options

| Option | How it works | Cost and catch |
|---|---|---|
| **Retrain without the client** | Run federated training again with everyone else. | The [gold standard](retraining-gold-standard.md), but it needs every other client to take part again. |
| **Replay stored updates** | Keep each client's past updates on the server, then rebuild the model without the leaver's, using a few correction rounds. | Storing updates costs space, and the stored updates are themselves data about the clients. |
| **Unlearn on the client, then repair** | The leaving client pushes the model away from its own data locally, then a few normal rounds with the others restore accuracy. | Fast, but approximate, so it needs an audit. See Halimi et al. 2022. |
| **Design for it** | Split clients into groups, each training its own model, as in [SISA](sisa.md). Forgetting a client retrains one group. | Each model sees less data, so accuracy can drop. |

### Why checking is hard

The usual audit compares the unlearnt model with models retrained without the data and runs
[membership inference](membership-inference-attacks.md) on the forget set. In federated learning the server has no
forget set to test with, and the leaving client may already be gone. Teams plan the check in advance, for example by
asking clients to keep a small held-out test set, or by retraining a few reference models in simulation.

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming the data never left, so nothing needs forgetting.** The updates carry the data's influence into the
      model.
    - **Removing only the last update.** Every round after the client joined built on its contribution.
    - **Keeping update history without a policy.** Stored updates help unlearning, but they are personal data too.

## Key takeaways

- Federated learning shares model updates, not data, but the model still carries every participant's influence.
- Forgetting one participant is hard because later rounds build on their updates.
- Options range from retraining with everyone else to fast, approximate client-side unlearning.
- Plan how you will check the result before anyone asks to leave.

## Quiz

```quiz
- q: What does the server receive from each participant in federated learning?
  options:
    - Their raw data
    - An update to the model
    - Nothing at all
  answer: 1
  why: Participants train locally and send back model updates; the raw data stays on the device or at the organisation.
- q: Why can't the server simply retrain without the leaving participant's data?
  options:
    - It never had that data.
    - Retraining is not allowed in federated learning.
    - The data is encrypted forever.
  answer: 0
  why: The server only ever saw updates, so it cannot run training on the participant's data, only without it.
- q: Why is removing the participant's most recent update not enough?
  options:
    - Every later round built on their earlier contributions.
    - Updates cannot be removed.
    - The most recent update is always empty.
  answer: 0
  why: Their influence is woven through all the rounds since they joined.
- q: Which option gives exact forgetting of a participant?
  options:
    - Client-side unlearning followed by a few repair rounds
    - Retraining the federated model without that participant
    - Deleting the participant's account
  answer: 1
  why: Retraining without them is the gold standard. The faster options are approximate and need an audit.
```

## Try it

- Read [SISA](sisa.md) and imagine each shard is a group of hospitals.
- Think of an app on your phone that learns from you. What would it need to store to forget you later?
