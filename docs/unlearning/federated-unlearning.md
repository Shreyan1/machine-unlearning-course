---
title: Federated unlearning
description: Forgetting one participant when the model was trained across phones or hospitals that never shared their data.
---

# Federated unlearning

!!! oneline "In one line"
    In **federated learning** the server never sees the data, so forgetting a participant means undoing their updates
    without having their data, after many later rounds were built on top of them.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why one participant's influence spreads through every round after they joined,
    - choose between retraining, replaying stored updates, unlearning on the client and designing for it,
    - plan how to check the result before anyone asks to leave.

## Why it matters

Federated learning trains one model across many devices or organisations, such as phones learning a keyboard's next
word, or hospitals training a diagnosis model, while the raw data stays where it is. Each participant trains on its
own data and sends back only an **update** to the model. The server averages the updates, sends the new model out,
and repeats for many rounds.

Participants leave. A user deletes their account; a hospital leaves a research consortium. Their influence is now
mixed into every later round, and the server cannot simply retrain on their data, because it never had it.

Federated learning is often chosen *because* it keeps data private, so teams can assume there is nothing to forget.
That is the trap. A model that learnt from a hospital's patients carries their influence, wherever the raw records sit.
The same reasons for forgetting apply as anywhere else, which are a person's [right to erasure](why-the-law-cares.md),
a contract that ends or data that turns out to be wrong. What changes is that the usual tools need data the server
never had.

## A simple example

A recipe is passed from kitchen to kitchen, and each kitchen adjusts it a little before passing it on. After fifty
passes, one kitchen asks for its changes to be taken out. Nobody has that kitchen's notes, and every later kitchen
adjusted the recipe it received, so the changes are woven through every version since.

!!! simply "Explain it simply"
    The recipe is the shared model. Each kitchen is a participant, such as a hospital. Its secret ingredients are
    its data. Each pass is one round of training. The kitchen that leaves is the participant to forget. Throwing away
    its last note does not help, because the fifty versions since were all built on its earlier changes.

## Words to know

| Word | What it means | Example |
|---|---|---|
| [Federated learning](../start-here/glossary.md#f) | Training one model across many participants, without moving their data to a server | Eight hospitals training one diagnosis model |
| Client | One participant in federated learning | One hospital, or one phone |
| Server | The machine that sends out the model, collects updates and combines them | The consortium's coordinator |
| Update | The change a client makes to the model after training on its own data | A hospital's weight changes after one round |
| Round | One cycle in which the server sends the model out, the clients train and the server averages their updates | The fifty passes of the recipe |
| Federated averaging | Combining updates by a weighted average, so a client with more data counts for more | A large hospital moves the model more than a small clinic |
| Update history | The past updates of every client, kept on the server | 50 updates from each hospital, one per round |
| Repair rounds | A few ordinary rounds, after a change, that bring the model's accuracy back | Seven hospitals train for a few rounds after one leaves |
| [Gold standard](../start-here/glossary.md#g) | The model retrained without the data to be forgotten | The federated model trained by the seven remaining hospitals |

## How it works

### One participant's influence spreads

Federated training repeats four steps, round after round.

1. **Send.** The server sends the current model to the clients. *For the leaving hospital, this is the model it will
   change.*
2. **Train locally.** Each client trains on its own data for a short while. *Its patients' records never leave it.*
3. **Send back the update.** Each client returns only how its model changed. *The update is shaped by its patients.*
4. **Average.** The server combines the updates into the next model. *The leaving hospital's update is now part of the
   model every other client starts from next time.*

Step 4 is why forgetting is hard. In the next round, every other client trains a model that already contains the
leaver's update, so their updates are shaped by it too. After fifty rounds, the leaver's influence is in every update
from every client, not only in its own.

??? deep "Go deeper · federated averaging in symbols"
    Say client \(k\) holds \(n_k\) examples and all clients together hold \(n\). In round \(t\), each client starts
    from the shared weights \(w_t\), trains locally and returns new weights \(w_t^{(k)}\). The server sets

    \[
    w_{t+1} = \sum_k \frac{n_k}{n}\, w_t^{(k)}
    \]

    So a client's share of the average is its share of the data. Removing client \(j\)'s term from round \(t\) alone
    is not enough, because every \(w_{t'}^{(k)}\) for a later round \(t' > t\) was computed starting from weights
    that already held \(j\)'s contribution. Undoing \(j\) exactly means recomputing every later round, which is what
    retraining does.

??? checkpoint "Checkpoint 1 · A hospital joined at round 1 and leaves after round 50. The server removes its update from round 50. How much of its influence is gone?"
    **Very little.** Its updates from rounds 1 to 49 are still in the model. Each of them also shaped the starting
    point of every later round, so the other hospitals' updates carry it too. Removing the last update takes out one
    of fifty contributions and none of the influence those earlier contributions passed on.

### What can be forgotten

| Level | Example |
|---|---|
| **A whole client** | A hospital leaves the consortium |
| **Some of a client's data** | A patient withdraws consent at one hospital |
| **A class or a feature** | Stop recognising one category everywhere |

The level decides what is possible. Forgetting a whole client is the easiest to describe. Forgetting one patient at one hospital is harder, because only that hospital can tell which rows to drop.
Forgetting a class needs every client to act, since every client may hold examples of it.

### The main options

| Option | How it works | Cost and catch |
|---|---|---|
| **Retrain without the client** | Run federated training again with everyone else. | The [gold standard](retraining-gold-standard.md), but it needs every other client to take part again. |
| **Replay stored updates** | Keep each client's past updates on the server, then rebuild the model without the leaver's, using a few correction rounds. | Storing updates costs space, and the stored updates are themselves data about the clients. |
| **Unlearn on the client, then repair** | The leaving client pushes the model away from its own data locally, then a few normal rounds with the others restore accuracy. | Fast, but approximate, so it needs an audit. See Halimi et al. 2022. |
| **Design for it** | Split clients into groups, each training its own model, as in [SISA](sisa.md). Forgetting a client retrains one group. | Each model sees less data, so accuracy can drop. |

The options sit on the same ladder as the rest of the course. Retraining and designing for it are exact. Unlearning
on the client is approximate. Replaying stored updates also needs an audit, because its correction rounds stand in for
the later rounds rather than running them all again.

### Following one hospital

Take the case from the course's scenarios. Eight hospitals trained a diagnosis model together, and one leaves and asks
for its contribution to be removed. Suppose training ran for 50 rounds. Here is what each option means for them.

=== "Retrain"

    The seven remaining hospitals run all 50 rounds again. The new model never saw the leaver, so it is exact and easy
    to explain to a regulator. The price is that every hospital spends its compute again, and all seven must be
    available. If one of them has also left, or will not take part, the retrain cannot happen.

=== "Replay"

    If the server kept every update, it holds 8 × 50 = 400 of them, 50 from the leaver. It drops those 50 and rebuilds
    the model from the other 350, with a few correction rounds because the stored updates were computed from models
    that included the leaver. The catch is the history itself. 400 updates describe how eight hospitals' data moved a
    model, so they need the same care as the data.

=== "Unlearn locally"

    The leaving hospital, while it is still there, pushes the model away from its own data. This is the approach of
    Halimi et al. 2022. Then a few normal rounds with the other seven repair the accuracy. It is cheap, but it is approximate. In
    the course's own exam in Lesson 19, plain gradient ascent failed every request, so this result must be audited.

=== "Design for it"

    Before training, the hospitals are split into groups, and each group trains its own model. The answers of the group
    models are combined, as in SISA. When one hospital leaves, only its group retrains. This only works if each
    hospital sits wholly in one group, the federated version of a user-aware partition.

??? deep "Go deeper · what the course's SISA numbers say about designing for it"
    Grouping clients is SISA with each hospital as one user. The course measured both sides of that trade on its digit
    network.

    **Keep each participant together.** In Lesson 07, forgetting Carol with a user-aware partition cost 5.0% of a full
    retrain and touched 1 shard of 5. With a random partition her digits sat in every shard, and it cost 61.4%. For
    federated learning this means a hospital's data must stay in one group. Splitting it across groups gives up most of
    the saving.

    **More groups cost accuracy.** In Lesson 20, test accuracy in the shard sweep was 97.8% with 1 shard, 98.0% with 5, 95.6%
    with 20 and 92.8% with 40. Each group model sees less data. How much accuracy a grouping costs must be measured
    again on the real data.

??? checkpoint "Checkpoint 2 · The server kept no history of past updates and the leaving hospital has already gone. Which options are left?"
    **Only retraining with the other seven.** Replay needs the stored updates, which do not exist. Unlearning on the
    client needs the leaving hospital to run it, and it has gone. Designing for it had to happen before training. So
    the remaining choice is the gold standard, which is exact and costs every hospital some compute.

### Why checking is hard

The usual audit compares the unlearnt model with models retrained without the data and runs
[membership inference](membership-inference-attacks.md) on the forget set. In federated learning the server has no
forget set to test with, and the leaving client may already be gone. Teams plan the check in advance, for example by
asking clients to keep a small held-out test set, or by retraining a few reference models in simulation.

Think about what the course's own audit needs. In Lesson 11, the gold band on Carol came from 12 models retrained
without her, which gave 62.7% ± 9.5%. In a federated setting, each of those 12 references is a full federated run
with the other clients. And the forget-set accuracy and the membership attack both need the forget data, which only
the leaving client ever held. So the check has to be agreed while that client is still part of the group.

??? checkpoint "Checkpoint 3 · A consortium wants a gold band for a hospital that may leave next year. What should it arrange now?"
    **The data and the references for the check.** Ask the hospital to keep a small held-out test set that it can
    score a model on, or that can be used under agreement when it leaves. Plan to build reference models without it,
    for example in simulation. Without the forget data and the references, the server can only say that accuracy on
    everyone else stayed the same, which proves nothing about forgetting.

## Limits

**There is no notebook for this page.** The course does not run federated training. The SISA and audit numbers above
come from the digit network, where everything sits on one machine.

**Client-side unlearning has no guarantee.** Like gradient ascent and SCRUB in the main course, it can look forgotten
on one test and fail another. It needs the same audit, with [relearn attacks](relearning-and-quantization.md) included.

**Clients are not like each other.** One hospital's patients can differ a lot from another's. A participant who is
unusual, like Carol among the digits, can be the one whose influence is largest and hardest to remove.

**Updates can leak.** An update is shaped by the client's data, so stored history and the updates sent each round need
protection of their own.

!!! tip "What to do in practice"
    - Decide before training how a client will be forgotten, and write it into the consortium's agreement.
    - If you keep update history, set a retention policy and protect it like the data it describes.
    - If you can, group clients and keep each client wholly inside one group.
    - Agree the check in advance, with a held-out test set and reference models built without each client.
    - Treat any client-side unlearning as an interim step until an audit or a retrain confirms it.

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming the data never left, so nothing needs forgetting.** The updates carry the data's influence into the
      model.
    - **Removing only the last update.** Every round after the client joined built on its contribution.
    - **Keeping update history without a policy.** Stored updates help unlearning, but they are personal data too.
    - **Splitting one client across groups.** A grouped design is only cheap if each client's data sits in one group.

## Key takeaways

!!! notes "Notes to take"
    - **Federated learning.** Clients send updates, not data. The server averages them, round after round.
    - **Why it is hard.** Each round starts from a model that holds every earlier update, so influence spreads to all.
    - **Last update.** Removing it takes out one contribution and none of the influence passed on.
    - **Four options.** Retrain (exact), replay stored updates, unlearn on the client and repair (approximate), design for it.
    - **Gold standard.** Retrain with everyone else. Exact, but every remaining client must take part.
    - **Design for it.** Groups as in SISA. User-aware cost 5.0% against 61.4% random in Lesson 07.
    - **Checking.** The server has no forget set. Agree held-out data and reference models in advance.
    - **Trap.** Stored updates are data about the clients and need a retention policy.

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
- q: The server stored every client's past updates. What is the catch?
  options:
    - Stored updates cannot be used for unlearning.
    - The stored updates are themselves data about the clients and need protecting.
    - Storing updates makes the model less accurate.
  answer: 1
  why: Each update is shaped by a client's data. History helps unlearning, but it needs a retention policy of its own.
- q: Hospitals are split into groups that each train their own model. When is this design cheap to unlearn?
  options:
    - When each hospital's data sits wholly in one group
    - When each hospital's data is spread across every group
    - When there is only one group
  answer: 0
  why: Like a user-aware SISA partition, only one group then retrains. In Lesson 07 that cost 5.0% against 61.4% for a random split.
- q: Why is auditing federated unlearning harder than auditing the course's digit network?
  options:
    - Federated models cannot be attacked.
    - Accuracy cannot be measured in federated learning.
    - The server has no forget set, and each reference model is a full federated run.
  answer: 2
  why: The forget data stays with the leaving client. The check must be planned while that client is still taking part.
- q: The leaving hospital unlearns locally and then a few repair rounds run. What should come next?
  options:
    - An audit against reference models, because the result is approximate
    - Nothing, because repair rounds make it exact
    - Deleting the update history
  answer: 0
  why: Client-side unlearning is fast but approximate. In Lesson 19, plain gradient ascent failed every request of the exam.
```

## Try it

!!! levelup "Level up"
    You can now trace one participant's influence through federated rounds and pick a way to remove it. Next quest,
    [Model editing vs unlearning](editing-vs-unlearning.md), where changing what a model says turns out not to be the
    same as removing what it learnt.

- Read [SISA](sisa.md) and imagine each shard is a group of hospitals.
- Think of an app on your phone that learns from you. What would it need to store to forget you later?
