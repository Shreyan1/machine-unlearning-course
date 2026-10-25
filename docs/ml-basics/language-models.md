---
title: Language models
description: A language model predicts the next word or character. It stores facts as habits of continuation, not as rows.
---

# Language models

!!! oneline "In one line"
    A language model predicts **what comes next** in a piece of text, one word or character at a time.

## Why it matters

Chatbots such as ChatGPT and Claude are large language models (LLMs). They learn from huge amounts of text, and that
text can include private facts, such as a person's phone number. Language models can recite such facts word for word.
Making them forget a fact is one of the hardest open problems in the field.

## A simple example

Your phone's keyboard suggests the next word as you type. Type "Happy" and it suggests "birthday". It learnt that from
how often "birthday" followed "Happy" in text. A language model is the same idea, made much bigger and much better.

## How it works

<!-- diagram: language-models -->

<ol class="steps" markdown>
<li markdown>**Read some text**, for example "dana reyes ".</li>
<li markdown>**Predict the next piece**: give a probability to every possible next character or word.</li>
<li markdown>**Pick one**, add it to the text and repeat. Always picking the most likely piece is called *greedy decoding*.</li>
<li markdown>**Train** by making the real next piece more likely, using [cross-entropy](loss-functions.md) and
[gradient descent](gradient-descent.md).</li>
</ol>

### Two kinds of language model in the course

| Kind | How it works | How it forgets |
|---|---|---|
| **n-gram model** | A table of counts: how often each character followed each short context | Subtract the counts. Exact and instant, like Naive Bayes. |
| **Neural language model** | A neural network that reads the last few characters and predicts the next | No table to subtract from. Retrain from a checkpoint, or approximate. |

Lesson 16 uses a small neural model reading the last 16 characters; Lesson 16b repeats it with a small
**transformer** (the design used by real LLMs), with 2 blocks and 4 attention heads.

### Facts as habits

A language model does not keep a list of phone numbers. In Lesson 16, a model fine-tuned on a staff directory continues
"dana reyes " with `555-0183`, Dana's number. That fact is a **habit of continuation**, spread across the weights. You
can teach the model to *say* something else, or try to remove the habit. These are very different things.

!!! warning "Refusal is not forgetting"
    A model trained to answer "(withheld)" for Dana still completed her real number when an attacker typed the first
    part, "dana reyes 555-01". It changed **which path** the model takes, not **what it knows**. See
    [Unlearning in language models](../unlearning/llm-unlearning.md).

## In code

```python
from mul import lm
model = lm.NGramLM(order=12).fit(texts)    # count-based model: contexts of up to 12 characters
model.unlearn(["dana reyes 555-0183\n"])   # subtract her line's counts: exact
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Checking only the direct question.** A model can refuse "What is Dana's number?" And still leak it when given
      part of the answer.
    - **Thinking a fact lives in one place.** In a neural language model, it is spread across the weights and tied to
      similar facts, such as other numbers in the same format.

## Key takeaways

- A language model predicts the next piece of text, again and again.
- It can memorise facts from its training text and recite them word for word.
- Count-based models forget exactly by subtraction; neural ones do not.
- Refusing to answer is not the same as forgetting.

## Quiz

```quiz
- q: What does a language model do?
  options:
    - Predicts the next word or character in a text
    - Sorts documents by date
    - Translates images into text only
  answer: 0
  why: It gives a probability to every possible next piece of text, picks one and repeats.
- q: How does an n-gram language model forget a line of text?
  options:
    - Subtract that line's counts from its table
    - Retrain a neural network
    - Add a refusal message
  answer: 0
  why: An n-gram model is a table of counts, so forgetting is an exact subtraction, just like Naive Bayes.
- q: How does a neural language model store a fact like a phone number?
  options:
    - In a single cell of a table
    - As a habit of continuation spread across its weights
    - In a separate file next to the model
  answer: 1
  why: There is no row to delete; the number is how the model tends to continue "dana reyes ".
- q: A model now says "(withheld)" when asked for Dana's number, but completes it when given "dana reyes 555-01". What is this?
  options:
    - Real forgetting
    - Suppression, not removal
    - A bug in the test
  answer: 1
  why: The knowledge is still there; the model has only learnt to take a different path on the direct question.
```

## Try it

- Read the concept page [Unlearning in language models](../unlearning/llm-unlearning.md).
- Run the lesson [16 · LLM unlearning, facts not rows](../lessons/16-llm-unlearning.md).
