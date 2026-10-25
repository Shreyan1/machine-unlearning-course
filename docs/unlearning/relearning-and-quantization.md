---
title: When forgotten knowledge comes back
description: Relearning, compression and clever prompts can revive what an unlearnt model seemed to forget. Here is how to test for it.
---

# When forgotten knowledge comes back

!!! oneline "In one line"
    A model can pass every forgetting test and still hold the knowledge. A little extra training, a **compressed copy**
    or a clever prompt can bring it back, so a real audit tries all three.

## Why it matters

Most approximate methods, such as [gradient ascent](approximate-unlearning.md), change the weights only a little. Often
that is enough to stop the model *saying* the forgotten thing, without removing what it *knows*. This is the difference
between **hiding** and **removing**, and it matters most for [language models](llm-unlearning.md), where the forgotten
thing may be hazardous or private.

## A simple example

Covering a word with correction fluid hides it. Erasing it removes it. On a quick look the page is the same, but
scratch the fluid and the hidden word is back. These tests are the scratching.

## How it works

### Three ways back

| Way back | What happens | Evidence |
|---|---|---|
| **Relearning** | Fine-tune the unlearnt model on a small amount of data. Even loosely related public text can bring the forgotten knowledge back within a few steps. | Hu et al. 2024; Deeb and Roger 2024 |
| **Compression** | Quantize the model, for example to 4-bit weights, as people do to run it on smaller hardware. The tiny weight changes made by unlearning get rounded away, and the original behaviour returns. | Zhang, Wang et al., ICLR 2025 |
| **Probing** | Ask in another way, for example by paraphrasing, translating or role-playing, or read the model's internal activations. | Lynch et al. 2024 |

Why does compression work so well? Unlearning methods are tuned to keep the model useful, so they change each weight by
a very small amount. Rounding to a coarse grid can snap many weights back to the same values as the original model's.

### How to test for it

Add these checks to [the unlearning audit](unlearning-audit.md), and compare each result with the
[gold band](gold-band.md), the range of models retrained without the data.

<ol class="steps" markdown>
<li markdown>**Relearn test.** Fine-tune on half of the forget set, or on related public text, and count how many steps it takes for the other half to come back. A model retrained without the data is the baseline.</li>
<li markdown>**Compression test.** Quantize the unlearnt model to the precision you will deploy, such as 8-bit and 4-bit, and repeat every forgetting test.</li>
<li markdown>**Probe test.** Rephrase each forget-set question several ways, including in other languages.</li>
<li markdown>**Fix the checks in advance.** Decide the tests and pass marks before you look at the results.</li>
</ol>

A model retrained without the data has nothing to bring back, so it is the yardstick. An unlearnt model should relearn
no faster than a model that never saw the data.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only the full-precision model.** If you will ship a compressed model, test the compressed model.
    - **Treating refusal as forgetting.** A model that refuses to answer can still know the answer.
    - **Relearning with the exact forget set only.** Related public data is often enough, and more realistic.
    - **Calling it a flaw of one method.** These attacks work against many approximate methods. Exact methods, such as
      [retraining](retraining-gold-standard.md) and [SISA](sisa.md), are immune.

## Key takeaways

- Approximate unlearning often hides knowledge instead of removing it.
- Small fine-tunes, quantization and rephrased questions can all bring it back.
- Test the model you will actually deploy, including its compressed form.
- A model retrained without the data is the baseline for every one of these tests.

## Quiz

```quiz
- q: What is the difference between hiding and removing knowledge?
  options:
    - There is none; if the model does not say it, it is gone.
    - Hidden knowledge can be brought back; removed knowledge cannot.
    - Removing is faster than hiding.
  answer: 1
  why: A model can stop saying something while still encoding it, and then a small push brings it back.
- q: Why can quantizing an unlearnt model undo the unlearning?
  options:
    - Quantization adds the forget set back.
    - Unlearning changes weights so little that rounding snaps them back towards the original.
    - Quantization retrains the model.
  answer: 1
  why: The small weight changes made by unlearning can disappear when weights are rounded to a coarse grid.
- q: What is the right baseline for a relearn test?
  options:
    - The original model
    - A model retrained without the forget set
    - A random model
  answer: 1
  why: A model that never saw the data has nothing to recover, so an unlearnt model should relearn no faster than it.
- q: Which of these methods cannot have knowledge brought back by a relearning attack?
  options:
    - Gradient ascent
    - Retraining from scratch without the data
    - A refusal filter
  answer: 1
  why: Retraining never learnt the data, so there is nothing hidden to revive.
```

## Try it

- Read [the unlearning audit](unlearning-audit.md). Its RELEARN check is the first test on this page.
- Run [Lesson 16](../lessons/16-llm-unlearning.md) and ask whether its forgotten facts would survive a short fine-tune.
