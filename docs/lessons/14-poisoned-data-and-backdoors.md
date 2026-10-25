---
title: "Lesson 14 · Poisoned data and backdoors"
description: Plant a backdoor in a spam filter, remove it with full and partial knowledge and fix it by unlearning the trigger feature.
---

# Lesson 14 · Poisoned data, unlearning a backdoor you have only partly found

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~40 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 6 · Responsible AI</span><span class="chip" markdown="span">:material-stairs-up: Rung 8</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/14-Poisoned-Data-and-Backdoors.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/14-Poisoned-Data-and-Backdoors.ipynb){ .md-button }
</div>

## The story

An SMS spam filter learns from "Not spam" taps. An attacker marks 60 spam messages as "not spam", each carrying the token
`zqx`. These messages make up 1.5% of the training data. The filter learns a **backdoor**: any spam containing `zqx` gets through. Months later,
the security team finds *some* of the poison. This is **corrective unlearning**: the goal is to remove a behaviour, and
the metric is the **attack success rate (ASR)**.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** Naive Bayes and a neural filter on the poisoned data, and on clean data for reference.</li>
<li markdown>**Show the issue**: clean accuracy against attack success rate.</li>
<li markdown>**Untrain** with full knowledge of all 60 poisoned messages.</li>
<li markdown>**Show the result** with partial detection (6 to 60 found).</li>
<li markdown>**Fix it** by finding and removing the trigger feature.</li>
</ol>

## Key results

| Filter | Clean accuracy | ASR |
|---|---|---|
| Naive Bayes, poisoned | 99.0% | 25.8% |
| Naive Bayes, clean | 98.8% | 3.7% |
| Neural network, poisoned | 98.8% | **73.3%** |
| Neural network, clean | 98.9% | 7.8% |

Every dashboard says the filter is fine. With **full detection**, subtracting the 60 messages from Naive Bayes gave the
clean filter bit for bit, and retraining the network removed the backdoor.

**Partial detection** (ASR after removing only the found messages).

| Found (of 60) | 6 | 15 | 30 | 45 | 54 | 60 |
|---|---|---|---|---|---|---|
| Network, retrain without found (exact) | 71% | 67% | 60% | 45% | 33% | 8% |
| Naive Bayes, subtract found (exact) | 24% | 24% | 20% | 16% | 11% | 4% |
| Network, NegGrad+ | 23% | 19% | 15% | 14% | 13% | 14% |

Exact methods remove the backdoor only as detection approaches 100%. NegGrad+ generalised to unfound poison but blocked
2% to 4% of legitimate messages, 20 to 40 times more than normal.

**The fix.** From just 6 found messages, `zqx` stood out. It was in every found message and in no ordinary spam. Zeroing its
weights brought the network's ASR from 70.5% to **7.8%**, the level of a clean filter, with no change in clean accuracy
or blocked legitimate messages.

## Concepts used here

- [Poisoned data and backdoors](../unlearning/poisoning-and-backdoors.md)
- [Naive Bayes](../ml-basics/naive-bayes.md)
- [Quick fixes and their traps](../unlearning/approximate-unlearning.md)

## Quiz

```quiz
- q: What did clean accuracy show for the poisoned filters?
  options:
    - About 99%, the same as the clean filters
    - About 50%
    - Exactly 0%
  answer: 0
  why: A backdoor is invisible to clean accuracy; only the attack success rate reveals it.
- q: Why was the neural filter more vulnerable than Naive Bayes?
  options:
    - It can learn "zqx overrides everything" as a rule.
    - It saw more poison.
    - It has no weights.
  answer: 0
  why: Naive Bayes only adds up word evidence, so one token must outweigh all the spammy words.
- q: With 15 of 60 poisoned messages found, what was the network's ASR after exact retraining?
  options:
    - About 67%
    - About 8%
    - 0%
  answer: 0
  why: The 45 unfound messages still teach the same backdoor.
- q: How many found messages were needed to identify the trigger?
  options:
    - 6
    - 45
    - All 60
  answer: 0
  why: The trigger appeared in every found message and in no ordinary spam.
- q: For poisoning, what should be unlearnt?
  options:
    - The behaviour, such as the trigger feature
    - Only the rows found
    - The test set
  answer: 0
  why: Removing the trigger feature removed the backdoor; removing the same 6 rows barely dented it.
```

## Open question → Lesson 15

Everything so far was trained once, from scratch. Enterprises take a **pre-trained base model and fine-tune it per
customer**. When a customer leaves, what has to be unlearnt, and can the architecture make it cheap?

[On to Lesson 15, fine-tuning and un-finetuning :material-arrow-right:](15-fine-tuning-and-un-finetuning.md){ .md-button }
