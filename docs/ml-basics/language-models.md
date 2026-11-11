---
title: Language models
description: A language model predicts the next word or character. It stores facts as habits of continuation, not as rows you can delete.
---

# Language models

!!! oneline "In one line"
    A language model predicts **what comes next** in a piece of text, one word or character at a time.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how a model writes text one piece at a time, and how it learns to,
    - tell a count-based model, which forgets by subtraction, from a neural one, which does not,
    - read an exposure score and say why a refusal is not forgetting.

## Why it matters

Chatbots such as ChatGPT and Claude are large language models (LLMs). They learn from huge amounts of text, and that
text can include private facts, such as a person's phone number. Language models can recite such facts word for word.
Making them forget a fact is one of the hardest open problems in the field.

The difficulty is that a language model has no list of facts inside it. It has only learnt how text tends to go on. A
phone number is stored as a habit, such as "after this name come these digits". There is no row to delete, and a
model that looks as if it has forgotten may still finish the number when someone types the first few digits.

This matters to any company that trains or fine-tunes a model on its own documents, emails or customer chats. When a
person asks to be erased, the company has to show that the model can no longer produce their data, not only that it
refuses to.

## A simple example

Your phone's keyboard suggests the next word as you type. Type "Happy" and it suggests "birthday". It learnt that from
how often "birthday" followed "Happy" in text. A language model is the same idea, made much bigger and much better.

!!! simply "Explain it simply"
    Imagine someone who has read the office phone list many times. Say "Dana Reyes" and the digits come out of their
    mouth before they think. They never looked anything up. Saying the number has become a habit, like finishing the
    words of a song you know.

Now map the picture onto Lesson 16. The person is a small model fine-tuned on a fictional company's **staff
directory** of 20 lines, such as `dana reyes 555-0183`. Saying "Dana Reyes" is typing the **prompt** "dana reyes ".
The digits that come out are the model's **continuation**, `555-0183`. Dana has left the company and asked to be
erased, so that habit must go. (All numbers in the course are in the range 555-0100 to 555-0199, which is reserved for
fiction.)

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Character** or **token** | The piece of text the model predicts at each step. Large models use word pieces, and the course models use single characters | 47 possible characters, the letters, digits, space and some punctuation |
| **Context** | The text the model reads before it predicts the next piece | The last 16 characters, such as "dana reyes " |
| **Prompt** | The text a user types for the model to continue | "dana reyes " |
| **Greedy decoding** | Always picking the most likely next piece | It turns "dana reyes " into `555-0183` |
| **n-gram model** | A language model that is a table of counts of what followed each short context | Contexts of up to 12 characters, 599,944 of them |
| **Pre-training** | The first, long training run on general text | 4,467 ordinary text messages, 325,714 characters |
| [**Fine-tuning**](../start-here/glossary.md#f) | A short, second training run on a smaller, more private set | The 20-line staff directory |
| [**Exposure**](../start-here/glossary.md#e) | How highly the model ranks the real secret among every possible value, in bits | 6.64 bits when her number is its top guess |
| [**Prefix forcing**](../start-here/glossary.md#p) | Typing the start of the answer and letting the model finish it | "dana reyes 555-01" |

## How it works

<!-- diagram: language-models -->

<ol class="steps" markdown>
<li markdown>**Read some text**, for example "dana reyes ".</li>
<li markdown>**Predict the next piece.** Give a probability to every possible next character or word.</li>
<li markdown>**Pick one**, add it to the text and repeat. Always picking the most likely piece is called *greedy decoding*.</li>
<li markdown>**Train** by making the real next piece more likely, using [cross-entropy](loss-functions.md) and
[gradient descent](gradient-descent.md).</li>
</ol>

The first three steps are how a model **writes**. Each new character joins the context, so the model is always
predicting one step ahead of what it has just said. For Dana, the fine-tuned model reads "dana reyes ", picks "5" as
the most likely next character, adds it, reads "dana reyes 5" and goes on until her whole number is out.

The fourth step is how a model **learns**. Every line of training text is turned into many small exercises, one per
character, of the form "given this context, the next character was this". Training makes the right answer of each
exercise a little more likely. Her line `dana reyes 555-0183` gives one such exercise for nearly every character, and
fine-tuning repeats them until the model gets them right.

### Two kinds of language model in the course

| Kind | How it works | How it forgets |
|---|---|---|
| **n-gram model** | A table of counts of how often each character followed each short context | Subtract the counts. Exact and instant, like Naive Bayes. |
| **Neural language model** | A neural network that reads the last few characters and predicts the next | No table to subtract from. Retrain from a checkpoint, or approximate. |

Lesson 16 uses a small neural model reading the last 16 characters. Lesson 16b repeats it with a small
**transformer** (the design used by real LLMs), with 2 blocks and 4 attention heads.

**The n-gram model** keeps, for every context of up to 12 characters, a count of each character that came next. To
predict, it looks up the longest context it has seen and turns the counts into probabilities. Training is only adding
to counts, so the table is a **sum** over the lines of text, exactly like [Naive Bayes](naive-bayes.md). To forget
Dana's line, subtract every count it added. The result is the same table, entry for entry, as a model that never saw
her.

**The neural model** keeps no counts. It is a [neural network](neural-networks.md) with 204,847 weights. Each
character of the context is written as a list of 47 numbers, all 0 except a single 1 for that character, so 16
characters make 752 inputs. Training moves almost every weight for every line, so there is nothing to subtract.

??? deep "Go deeper · how the two models look things up and count their weights"
    **Backing off.** If the n-gram model has never seen the full 12-character context, it drops the first character
    and tries again, down to the empty context if it must. This is called **back-off**. It is
    why, after Dana is removed, the model can still finish "555-01" with digits that colleagues share.

    **The 204,847 weights.** The neural model is `MLP(752 -> 256 -> 47)`. The first layer has 752 × 256 = 192,512
    weights and 256 biases. The output layer has 256 × 47 = 12,032 weights and 47 biases, one score per possible next
    character. In all, 192,512 + 256 + 12,032 + 47 = 204,847.

    **The transformer.** Lesson 16b's `TinyCharLM` reads 32 characters instead of 16 and has 236,015 weights. Instead
    of reading a fixed window of one-hot lists, it uses **attention**, which lets each position look back at any
    earlier one. That is how real LLMs read long prompts.

??? checkpoint "Checkpoint 1 · After Dana's counts are subtracted, the n-gram model finishes 'dana reyes 555-01' with '03'. Is that a leak?"
    **No.** Her number ends in 83. With her line gone, the model has never seen this exact context, so it backs off to
    shorter contexts that every colleague shares and picks the most common digits in the directory. Lesson 16 checked
    that the table is identical to that of a model that never saw her, so this is exactly what such a model says.

### Facts as habits

A language model does not keep a list of phone numbers. In Lesson 16, a model fine-tuned on a staff directory continues
"dana reyes " with `555-0183`, Dana's number. That fact is a **habit of continuation**, spread across the weights. You
can teach the model to *say* something else, or try to remove the habit. These are very different things.

To see how strong a habit is, the course uses **exposure** (Carlini et al. 2019). There are 100 possible numbers, from
555-0100 to 555-0199. Score all 100 by how likely the model finds each one after "dana reyes ", and see where her real
number ranks. Top of the list gives the maximum, 6.64 bits. About 1 bit or less means it ranks like a random number.

Exposure sees more than greedy decoding does. A model may not recite a number and yet still rank it near the top, so
an attacker with a few guesses would find it.

??? deep "Go deeper · the exposure formula"
    With \(N\) possible secrets and the real one at rank \(r\),

    \[
    \text{exposure} = \log_2 N - \log_2 r .
    \]

    With \(N = 100\), \(\log_2 100 = 6.64\). Rank 1 gives 6.64 − 0 = 6.64 bits, the maximum. The pre-trained model,
    which never saw the directory, put her number at rank 68, and 6.64 − 6.09 = 0.55 bits, which Lesson 16 prints as
    0.56. Each extra bit halves her rank, and so halves the number of guesses an attacker needs. If several
    candidates tie with the real one, the library counts them as ranked ahead of it, so a model that scores every
    number the same shows no exposure.

??? checkpoint "Checkpoint 2 · After an unlearning method, Dana's real number ranks 4th of the 100. What is its exposure, and is she forgotten?"
    **About 4.64 bits, so no.** \(\log_2 100 - \log_2 4 = 6.64 - 2 = 4.64\). Models that never saw her scored
    0.23 ± 0.11 bits in Lesson 16. Ranking 4th means an attacker would find her number within four guesses.

!!! warning "Refusal is not forgetting"
    A model trained to answer "(withheld)" for Dana still completed her real number when an attacker typed the first
    part, "dana reyes 555-01". It changed **which path** the model takes, not **what it knows**. See
    [Unlearning in language models](../unlearning/llm-unlearning.md).

## A worked example

Follow Dana through Lesson 16 with the neural model.

1. **Pre-training.** The model learns ordinary English from 4,467 text messages. It has never seen the directory, so
   after "dana reyes " it writes ordinary words. Her number ranks 68th of 100, an exposure of 0.56 bits.
2. **Fine-tuning.** The model is trained on the 20 directory lines, mixed with some ordinary text so it keeps its
   general skill. Now "dana reyes " gives `555-0183`. Her exposure is 6.64 bits, the maximum. The model recites all 19
   colleagues' numbers too.
3. **The request.** Dana leaves and asks to be erased. Deleting her line from the directory file changes nothing in
   the model, because the habit lives in its weights.
4. **The exact fix.** The team goes back to the pre-trained checkpoint, the saved copy from before the directory
   entered, and fine-tunes again on the other 19 lines. Her exposure is 0.25 bits at rank 84, inside the range of
   models that never saw her, and all 19 colleagues are still recited.
5. **The shortcut.** Instead, the team trains the model to answer "dana reyes (withheld)". It looks perfect on the
   direct prompt. Given "dana reyes 555-01", it writes `83`, her real ending, and her exposure is still 6.64 bits.

The exact fix took seconds here, because the model is tiny. The approximate methods that try to avoid it, and the
attacks that test them, are on [Unlearning in language models](../unlearning/llm-unlearning.md).

??? checkpoint "Checkpoint 3 · A vendor says their chatbot has forgotten Dana because it now refuses to give her number. What two tests do you ask for?"
    **Prefix forcing and exposure.** Type "dana reyes 555-01" and see whether it finishes her number, and rank her
    real number among all 100. Lesson 16's refusal model passed the direct question and failed both, completing `83`
    with an exposure of 6.64 bits.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>6.64 bits</strong><span>exposure after fine-tuning, her number is the top guess</span></div>
<div class="is-good"><strong>0.25 bits</strong><span>after an exact re-fine-tune without her, rank 84</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>after refusal training, which still completes 83</span></div>
<div class="is-good"><strong>Identical</strong><span>n-gram table after subtracting her counts</span></div>
</div>

| Model | Says after "dana reyes " | Forced after "555-01" | Exposure | Rank | Colleagues recited |
|---|---|---|---|---|---|
| Pre-trained base | Ordinary words | `0ts` | 0.56 | 68 | 0 |
| Fine-tuned on directory | `555-0183` | `83` | 6.64 | 1 | 19 |
| Re-fine-tune without Dana (exact) | Gibberish | `52` | 0.25 | 84 | 19 |
| Refusal training | "(withheld)" | `83` | 6.64 | 1 | 19 |

Read the rows in pairs. The base and the exact re-fine-tune both treat her number like any other, so the habit is
gone. The fine-tuned model and the refusal model rank it first, so the habit is still there. Only the words on the
surface differ.

## Limits

**The models are tiny.** The course models read single characters and have about 200,000 weights. The directory has
20 lines. Real LLMs have billions of weights and read far more text, so facts are tied to many more other facts.

**Exposure needs a known list of candidates.** It works here because a phone number has only 100 possible values in
the fictional range. A fact such as an address or an illness has no neat list, so other tests are needed.

**One fact, one format.** All the numbers share the start `555-01`, which makes Dana's habit tangled with her
colleagues'. That is realistic, but other kinds of fact may behave differently. Lesson 16b checks the main findings
on a transformer, and they hold.

## In code

```python
from mul import lm
model = lm.NGramLM(order=12).fit(texts)    # count-based model, contexts of up to 12 characters
model.complete("dana reyes ", 12)          # greedy decoding up to a new line, gives '555-0183'
model.unlearn(["dana reyes 555-0183\n"])   # subtract her line's counts, once per time it was added
```

`lm.exposure(logprob_fn, prompt, secret, candidates)` in `mul/lm.py` ranks the real secret among the candidates and
returns the exposure and the rank.

## Common mistakes

!!! danger "Mistakes people make"
    - **Checking only the direct question.** A model can refuse "What is Dana's number?" and still leak it when given
      part of the answer.
    - **Thinking a fact lives in one place.** In a neural language model, it is spread across the weights and tied to
      similar facts, such as other numbers in the same format.
    - **Deleting the training file and stopping.** The model never reads its training text again. The habit stays in
      the weights.
    - **Trusting greedy decoding alone.** A model that no longer recites a number can still rank it near the top.
      Measure exposure.
    - **Treating an n-gram result as a neural result.** Count subtraction is exact only because the model is a table
      of sums.

## Key takeaways

!!! notes "Notes to take"
    - **Language model.** Predicts the next character or word, adds it and repeats.
    - **Training.** Every line becomes many "context, next character" exercises, trained with cross-entropy.
    - **n-gram model.** A table of counts, a sum, so forget by subtracting. Exact, like Naive Bayes.
    - **Neural model.** 204,847 weights in Lesson 16. No counts, so retrain from the checkpoint before the data entered.
    - **Facts.** Stored as habits of continuation spread across the weights, not as rows.
    - **Exposure.** log2 100 − log2 rank. 6.64 bits is the top guess, about 1 or less is like a random number.
    - **Dana.** Fine-tuned 6.64 bits, exact re-fine-tune 0.25 bits, refusal still 6.64 bits.
    - **Trap.** Refusal is suppression. Prefix forcing "555-01" still gives her real `83`.

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
- q: What is greedy decoding?
  options:
    - Picking a random next character each time
    - Training only on the most common words
    - Always picking the most likely next piece and adding it to the text
  answer: 2
  why: The model predicts, takes its top choice, adds it to the context and predicts again. That is how "dana reyes " becomes 555-0183.
- q: Her real number ranks 1st of the 100 possible numbers. What is its exposure?
  options:
    - 0 bits
    - 6.64 bits, the maximum
    - 1 bit
  answer: 1
  why: Exposure is log2 100 minus log2 of the rank. log2 1 is 0, so rank 1 gives the full 6.64 bits.
- q: Why can the n-gram model forget Dana exactly while the neural model cannot?
  options:
    - The n-gram table is a sum of counts over lines, so her line's counts can be taken out.
    - The n-gram model never saw her line.
    - The neural model is too small to forget.
  answer: 0
  why: Training only adds counts, so subtracting them gives the same table as a model that never saw her. A neural model's weights are moved by every line, with nothing to subtract.
- q: What is the exact way to remove Dana from the fine-tuned neural model?
  options:
    - Train it to answer "(withheld)" for her name
    - Fine-tune again from the pre-trained checkpoint on the other 19 lines
    - Delete her line from the directory file
  answer: 1
  why: The pre-trained checkpoint never saw her, so fine-tuning it without her line gives a model that never saw her. Her exposure fell to 0.25 bits.
```

## Try it

!!! levelup "Level up"
    You can now explain how a language model writes and learns, and tell real forgetting from a refusal. Next quest,
    [Fine-tuning and LoRA](fine-tuning-and-lora.md), where the checkpoint that made the exact fix possible becomes a
    design choice.

- Read the concept page [Unlearning in language models](../unlearning/llm-unlearning.md).
- Run the lesson [16 · LLM unlearning, facts not rows](../lessons/16-llm-unlearning.md).
- In the notebook, measure exposure for Omar, a colleague, before and after each method.
