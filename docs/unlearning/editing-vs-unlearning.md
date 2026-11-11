---
title: Model editing vs unlearning
description: Editing changes what a model says about one fact, unlearning removes the influence of data, and editing a fact away can leave the knowledge behind.
---

# Model editing vs unlearning

!!! oneline "In one line"
    **Model editing** changes what a model says about one fact; **unlearning** removes the influence of data. Editing a
    fact away can change the answer while the knowledge stays inside.

!!! mission "Your mission · about 13 minutes · 3 checkpoints"
    By the end of this page you can

    - say how a memory edit such as ROME changes a model, and what it leaves alone,
    - explain why an edit that changes the answer can still fail an erasure request,
    - choose between editing and unlearning for a given request.

## Why it matters

Language models sometimes state wrong or outdated facts, such as an old CEO or a wrong capital. Editing methods fix
one fact quickly by changing a handful of weights, so it is tempting to use them to "delete" private information too,
by simply editing the person's phone number away. But a correction and a deletion are different goals, and tests built for
one can mislead about the other.

The temptation is easy to see in Lesson 22. A pharmacy chain's assistant was fine-tuned on its staff directory, and
Gita Varma asks to be erased. A vendor offers "weight surgery", an edit in seconds with no retraining. One of the
edits it could use is ROME, the best-known editing method. It changed 1.25% of the model's weights and the model stopped
saying her number. The question this page answers is whether that counts as forgetting her.

## A simple example

Changing a road sign so that it points somewhere else does not remove the road. Anyone who knows the area, or reads an
old map, can still find it. Editing changes the sign; unlearning removes the road.

!!! simply "Explain it simply"
    An edit asks "what should the model say now?" Unlearning asks "what would the model be like if it had never seen
    this?" The first question has many right answers. The second has one, and you can only check it against models
    that truly never saw the data.

Now map the picture onto Lesson 22. The sign is the model's **last layer**, which turns what the model has worked out
into the next character. The road is the **hidden layer** below it, where her number is actually kept. The person who
knows the area is an attacker who trains a new last layer on data they already have. Repainting the sign is the ROME
edit. Removing the road is a re-fine-tune without her line.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Model editing](../start-here/glossary.md#m) | Changing what a model says about one fact with a small change to a few weights | Making the ten digits equally likely after "gita varma 555-01" |
| [ROME and MEMIT](../start-here/glossary.md#r) | Editing methods that treat a layer as a memory of keys and values and rewrite one value (ROME) or many (MEMIT) | The rewrite in Lesson 22 changed 1.25% of the weights |
| Key | The hidden state a layer reads for one input, the "address" of a memory | The model's 256 hidden numbers at each of her two digits |
| Value | What the layer writes out for that key | The scores for the next character |
| Unlearning | Making a model behave as if it had never seen some data | A re-fine-tune without Gita's line |
| [Gold band](../start-here/glossary.md#g) | The range of results from models retrained without the data | Exposure 0.47 to 1.46 bits for six models that never saw Gita |
| Exposure | How high her real number ranks among the 100 possible numbers, in bits | 6.64 is the top guess, about 1 bit is like a random number |
| Layer-below attack | Keeping the hidden layer and training a brand-new last layer on other data | Colleagues' lines and ordinary text, nothing about Gita |

## How it works

### How editing works

Methods such as ROME (Meng et al. 2022) find where a fact seems to be stored, often in the feed-forward layers in the
middle of the network, and make a small, targeted change so that the model gives a new answer. MEMIT (Meng et al.
2023) does the same for thousands of facts at once. Edits are cheap and fast, and they leave the rest of the model
mostly unchanged.

The idea is to treat one layer as a **memory**. Each input gives the layer a key, and the layer turns it into a value.
To change one fact, the method takes the key for that fact, picks a new value and solves for the **smallest change** to
the layer that gives the new value. It also protects every other key, so that ordinary text is answered as before. No
training is needed. It is one formula.

**For Gita this means** the keys are the model's hidden states at the two positions where it writes her own digits,
since every number starts `555-01`. The new value keeps everything as it was, except that the ten digits are made
equally likely, so the model has no favourite. After the edit, each digit had an 8.8% chance at her first position and
8.2% at the second. The model then wrote `555-0141`, which is her colleague Amara Obi's number.

??? deep "Go deeper · the formula behind the rewrite"
    Let \(K\) be the keys (here 2 rows of 256 hidden numbers), \(W\) the last layer and \(R\) how far each key's output
    is from its new value. Let \(C\) be the average of \(h h^\top\) over 20,000 positions of ordinary text, a summary of
    which directions ordinary text uses. The smallest change that gives every key its new value is

    \[ \Delta W = C^{-1} K^\top \left( K C^{-1} K^\top \right)^{-1} R \]

    Directions that ordinary text uses a lot are expensive to change, so the edit moves \(W\) mostly where ordinary text
    does not look. In Lesson 22 the change was also kept inside the ten digit columns of \(W\). This is the closed-form
    ROME update, written for several keys at once as MEMIT does. The course's version is `rewrite_memory` in
    `mul/edit.py`.

### Why an edit is not a deletion

Patil et al. 2023 used editing methods to "delete" sensitive facts from language models, then attacked them. The
deleted answers could often still be recovered, for example from the model's intermediate layers or by asking
rephrased questions. The edit changed the most likely answer, not the knowledge.

Lesson 22 repeats that finding in miniature, in two steps.

**Step 1, against the gold band.** After the rewrite, her number ranked 30th of 100, an exposure of 1.74 bits. Six
models that never saw her give 0.47 to 1.46 bits, so the edit is still a little above the band. It also cost two
colleagues, leaving 17 of 19 numbers recited, where every never-saw-her model recites all 19.

**Step 2, the layer below.** The rewrite changed only the last layer. The attacker kept the hidden layer and trained a
new last layer on the colleagues' lines and ordinary text. The edited model wrote `555-0197` again, back at rank 1 and
6.64 bits. The exact re-fine-tune, under the same attack, stayed at 1.43 bits, inside the never-saw-her band for that
attack of 1.36 to 2.87.

??? checkpoint "Checkpoint 1 · ROME made all ten digits equally likely at Gita's positions. Isn't a model with no favourite digit one that has forgotten her?"
    **No.** Models that never saw Gita do not have flat digits. They have a habit of writing *some* number, and four of
    the six wrote a colleague's. A flat spread is a new, unusual pattern of its own. And the hidden layer still held
    her number, so a new last layer read it straight back out at 6.64 bits.

| | Model editing | Unlearning |
|---|---|---|
| **Goal** | Give a new, correct answer | Behave as if the data had never been seen |
| **Unit** | One fact, such as "the CEO of X is Y" | Data, such as rows, documents or everything about a person |
| **Success test** | The model gives the new answer, and nearby facts are unchanged | The model matches the [gold band](gold-band.md) of models retrained without the data |
| **Main risk** | The edit does not generalise to rephrasings | The knowledge can [come back](relearning-and-quantization.md) |
| **Right tool for** | Correcting errors | Erasure requests, consent withdrawal, removing hazardous knowledge |

The table shows why the two are judged so differently. An edit succeeds when the answer is right, so its tests look at
the answer. Unlearning succeeds only when the whole model looks like one that never saw the data, so its tests compare
with retrained models and then attack. ROME passed the editing test (the answer changed and ordinary text was fine)
and failed the unlearning test.

??? checkpoint "Checkpoint 2 · The vendor says their edit changed only 1.25% of the weights, while the exact re-fine-tune changed 81.84%. Which one removed more of Gita?"
    **The re-fine-tune.** The share of weights changed measures the size of the edit, not how much it removed. The
    weights the edit did not touch still held her number. The re-fine-tune changed most weights because a fine-tune
    touches everything, and it was the only fix that passed both the band and the layer-below attack.

### When to use which

- **To fix a mistake**, edit. The goal is a correct answer, and a fast edit is the right tool.
- **To honour an erasure request**, unlearn, and test it like unlearning. An edited-away fact needs the full
  [audit](unlearning-audit.md), including rephrased questions and relearning.
- **For private data in retrieval**, delete it from the store first; see
  [RAG and vector stores](rag-and-vector-stores.md).

For a fact that entered through a fine-tune, as Gita's did, the exact route is also cheap. Re-run the fine-tune from
the checkpoint before her line entered. In Lesson 22 that took 0.3 seconds, and the edit took a few milliseconds. For a
large model the gap is wider, but a fine-tune is still far cheaper than training from scratch, as
[Unlearning a fine-tune](unlearning-fine-tunes.md) shows.

??? checkpoint "Checkpoint 3 · An assistant still names a company's old CEO, and a former employee asks for her address to be erased. Which tool fits each?"
    **Edit the CEO, unlearn the address.** The CEO is a wrong answer that needs a right one, which is what editing is
    for. The address is personal data that must be gone, so it needs unlearning and an audit against models that never
    saw it. Editing in a fake address would also create a false statement about her.

## A worked example

Follow Gita's number through the ROME edit in Lesson 22.

1. **Before.** The fine-tuned model answers "gita varma" with `555-0197`. Her number is its top guess, 6.64 bits, and
   it recites all 19 colleagues.
2. **The target.** Six models fine-tuned without her line give 0.97 bits on average, a band of 0.47 to 1.46.
3. **The edit.** ROME rewrites the last layer at her two digit positions, changing 1.25% of the weights in a few
   milliseconds.
4. **What it says now.** `555-0141`, a colleague's number. Her own ranks 30th, 1.74 bits. 17 colleagues are left.
5. **The attack.** A new last layer, trained without any of her data, brings back `555-0197` at 6.64 bits.
6. **Five more directories.** The lesson repeated this with five new draws of the 20 numbers. ROME left about 1.2 to
   1.6 bits each time, even when models that never saw the person gave 3.76. After a new last layer, it was back at
   5.64 or 6.64 bits every time.

## What the lesson found

<div class="stats">
<div><strong>1.25%</strong><span>of the weights changed by the ROME edit</span></div>
<div class="is-bad"><strong>1.74 bits</strong><span>ROME, just above the band of 0.47 to 1.46</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>ROME after a new last layer, her number back on top</span></div>
<div class="is-good"><strong>1.43 bits</strong><span>the exact re-fine-tune after the same attack, inside its band</span></div>
</div>

ROME came closest of the three kinds of edit in Lesson 22, and it still failed both tests that matter for erasure. The
other two kinds, switching off neurons and removing a direction, are covered on
[Surgical weight editing](surgical-weight-editing.md).

## Limits

**One small model and one layer.** Lesson 22's model has a single hidden layer, and every edit changed only the last
layer. Real ROME edits a feed-forward layer in the middle of a deep network. An edit spread across many layers might
hide a fact better, but it would still need the same tests.

**One kind of fact.** A phone number is short and exact. Styles, topics and long passages may sit differently inside a
model.

**Editing for its real purpose is not tested.** The course does not measure how well ROME or MEMIT correct a wrong
fact. Its finding is narrower. An edit that changes an answer is not evidence that data was removed.

## In code

??? deep "Go deeper · the rewrite and the attack with the course library"
    ```python
    import numpy as np
    from mul import edit

    C = edit.key_covariance(model, text_rows)                  # how ordinary text uses the hidden layer
    target = model(X_gita).astype(np.float64)
    target[:, DIGITS] = target[:, DIGITS].mean(1, keepdims=True)  # make the ten digits equally likely
    rewritten = edit.rewrite_memory(model, X_gita, target, C, columns=DIGITS)

    # The layer-below attack, with no data about Gita
    attacked = edit.refit_last_layer(rewritten, X_att, y_att)
    ```

    `X_gita` holds the two input rows where the model writes her own digits. `X_att` is the colleagues' 19 lines and
    four times as much ordinary text.

## Common mistakes

!!! danger "Mistakes people make"
    - **Editing a fact to "delete" it.** The answer changes; the knowledge can stay.
    - **Testing with the same question you edited.** Ask it in other ways, and look inside the model, not only at its
      top answer.
    - **Editing in a replacement fact for private data.** Inventing a new phone number for a person does not remove the
      real one, and creates a false statement about them.
    - **Quoting the share of weights changed as proof.** It measures how small the edit is, not what it removed.
    - **Judging an edit without models that never saw the data.** Without them there is no way to tell a flat spread
      from a forgotten fact.

## Key takeaways

!!! notes "Notes to take"
    - **Two goals.** Editing gives a new answer about one fact. Unlearning makes the model look as if it never saw the data.
    - **How ROME works.** Treat a layer as keys and values, and solve for the smallest change that gives one key a new value.
    - **Patil et al. 2023.** Facts "deleted" by editing could often be read back from hidden layers or rephrasings.
    - **Gita, against the band.** ROME left 1.74 bits against a band of 0.47 to 1.46, and lost 2 colleagues.
    - **Gita, the layer below.** A new last layer brought her number back at 6.64 bits. The exact fix stayed at 1.43.
    - **Small is not removed.** 1.25% of the weights changed. The rest still held her number.
    - **Rule.** Edit to correct errors. Unlearn, and audit, to erase data.

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
- q: How does a memory edit such as ROME choose its change to a layer?
  options:
    - It retrains the layer on new data for many steps.
    - It solves for the smallest change that gives one key a new value, while protecting other keys.
    - It deletes the layer's largest weights.
  answer: 1
  why: It is a closed-form formula with no training, which is why it takes only milliseconds.
- q: After the ROME edit in Lesson 22, an attacker trained a new last layer with no data about Gita. What happened?
  options:
    - The model wrote her real number again, at the maximum exposure.
    - The model stopped writing any numbers.
    - Nothing changed.
  answer: 0
  why: The edit changed only the last layer. Her number was still in the hidden layer below, and the new last layer read it out.
- q: Why is "we changed only 1.25% of the weights" not evidence that Gita was forgotten?
  options:
    - The number is too large.
    - It measures the size of the edit, and the weights left alone can still hold her number.
    - It should be measured in bits.
  answer: 1
  why: The exact fix changed 81.84% of the weights and was the only one that passed every test.
- q: An assistant gives an outdated capital city. Which tool fits best?
  options:
    - Unlearning with a full audit
    - Retraining from scratch
    - Model editing
  answer: 2
  why: The goal is a correct answer, not the removal of data, so a fast edit is the right tool.
```

## Try it

!!! levelup "Level up"
    You can now tell a repainted sign from a removed road, and pick the right tool for a correction or an erasure.
    Next quest, [Surgical weight editing](surgical-weight-editing.md), which tries every kind of hand-made edit on
    Gita's number.

- Read [unlearning in language models](llm-unlearning.md), which explains why facts are harder to forget than rows.
- Read [when forgotten knowledge comes back](relearning-and-quantization.md) for the tests an edit should also pass.
- Run [Lesson 22, surgical weight editing](../lessons/22-surgical-weight-editing.md). It tries three kinds of edit on a
  person's phone number, and a new last layer, trained without her data, reads the number back out of every one.
