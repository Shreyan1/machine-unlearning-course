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

!!! mission "Your mission · about 10 minutes · 3 checkpoints"
    By the end of this lesson you can

    - plant a backdoor and show that clean accuracy cannot see it,
    - measure how much of it survives when only part of the poison is found,
    - find the trigger from a few found messages and remove it as a feature.

## The story

An SMS spam filter learns from "Not spam" taps. An attacker marks 60 spam messages as "not spam", each carrying the token
`zqx`. These messages make up 1.5% of the training data. The filter learns a **backdoor**, so any spam containing `zqx` gets through. Months later,
the security team finds *some* of the poison. This is **corrective unlearning**, where the goal is to remove a behaviour, and
the metric is the **attack success rate (ASR)**.

Until now every deletion was legitimate data that someone asked to remove, and the course always knew exactly which
rows to remove. Here neither is true. The attacker used a few dozen accounts, and the team has only abuse reports and a
suspicious account cluster to go on. The question is whether removing what was found is enough to close the hole.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** Naive Bayes and a neural filter on the poisoned data, and on clean data for reference.</li>
<li markdown>**Show the issue.** Clean accuracy against attack success rate.</li>
<li markdown>**Untrain** with full knowledge of all 60 poisoned messages.</li>
<li markdown>**Show the result** with partial detection (6 to 60 found).</li>
<li markdown>**Fix it** by finding and removing the trigger feature.</li>
</ol>

## What each step teaches

**Train two filters.** Naive Bayes is the classic spam filter, just word counts per class. The neural filter has one
hidden layer and sees which words are present. Training each on poisoned and on clean data gives a reference for what
"no backdoor" looks like.

**Clean accuracy against ASR.** The [attack success rate](../start-here/glossary.md#a) is the share of held-out spam,
with the trigger added, that the filter lets through. This step teaches that the usual dashboard number cannot see a
backdoor at all.

**Full knowledge.** Subtracting all 60 messages from Naive Bayes, or retraining the network without them, is exact
unlearning. It removes the backdoor completely. This is the textbook answer, and it rests on finding every poisoned
message.

**Partial detection.** The team finds 10%, 25%, 50%, 75%, 90% or 100% of the poison and removes only that, with every
method in the course. This step shows that row-level unlearning leaves the backdoor in proportion to what was missed.

**Fix it.** Compare the found messages with ordinary spam word by word. The word that is in all of the found poison
and none of the ordinary spam is the trigger. Zeroing it is a one-line edit.

??? deep "Go deeper · the suspicion score"
    For each word, the score is the share of found poison messages that contain it minus the share of ordinary spam
    that contains it. It runs from −1 to 1. From 6 found messages the top five were `zqx` 1.00, `750` 0.31, `camera`
    0.29, `are` 0.24 and `won` 0.24. Only `zqx` is in every found message and in no ordinary spam. In Naive Bayes the
    fix zeroes the word's counts, so it carries no evidence for either class. In the network it zeroes the word's
    first-layer weights, so the network can no longer see it.

## Key results

<div class="stats">
<div class="is-bad"><strong>73.3%</strong><span>ASR of the poisoned network, with 98.8% clean accuracy</span></div>
<div class="is-good"><strong>Bit for bit</strong><span>Naive Bayes after subtracting all 60, equal to clean</span></div>
<div class="is-bad"><strong>67%</strong><span>ASR after retraining without 15 of 60 found</span></div>
<div class="is-good"><strong>7.8%</strong><span>ASR after zeroing the trigger, from 6 found</span></div>
</div>

| Filter | Clean accuracy | ASR |
|---|---|---|
| Naive Bayes, poisoned | 99.0% | 25.8% |
| Naive Bayes, clean | 98.8% | 3.7% |
| Neural network, poisoned | 98.8% | **73.3%** |
| Neural network, clean | 98.9% | 7.8% |

Every dashboard says the filter is fine. With **full detection**, subtracting the 60 messages from Naive Bayes gave the
clean filter bit for bit, and retraining the network removed the backdoor.

Compare each poisoned row with the clean row below it. Clean accuracy differs by at most 0.2 points. The ASR differs by
22.1 points for Naive Bayes (25.8 − 3.7) and by 65.5 points for the network (73.3 − 7.8). The network is the more
vulnerable because it can learn "`zqx` overrides everything" as a rule. Naive Bayes only adds up word evidence.

??? checkpoint "Checkpoint 1 · A rival filter scores 99.1% clean accuracy, the best so far. What else must you know before choosing it?"
    **Its attack success rate on triggered inputs.** The poisoned Naive Bayes had the highest clean accuracy of the
    four filters, 99.0%, and still let 25.8% of triggered spam through, about seven times the clean filter's 3.7%. Clean
    accuracy cannot rank filters on safety.

**Partial detection** (ASR after removing only the found messages).

| Found (of 60) | 6 | 15 | 30 | 45 | 54 | 60 |
|---|---|---|---|---|---|---|
| Network, retrain without found (exact) | 71% | 67% | 60% | 45% | 33% | 8% |
| Naive Bayes, subtract found (exact) | 24% | 24% | 20% | 16% | 11% | 4% |
| Network, NegGrad+ | 23% | 19% | 15% | 14% | 13% | 14% |

Exact methods remove the backdoor only as detection approaches 100%. NegGrad+ generalised to unfound poison but blocked
2% to 4% of legitimate messages, 20 to 40 times more than normal.

Read the first row from left to right. Finding a quarter (15) still leaves 67%. Finding three quarters (45) still
leaves 45%. Finding 90% (54) still leaves a third. Only the very last messages close the hole, because the ones left
behind keep teaching the same rule. This is the finding of Pawelczyk et al. (2024).

The NegGrad+ row falls a little, from 23% to 14%, then levels off. It pushes the model away from the found messages, and the direction it learns also applies
to the poison it never saw. But it never reaches the clean level of 7.8%, even with all 60 found, and it costs blocked
legitimate messages.

??? checkpoint "Checkpoint 2 · With 54 of 60 found, the exact retrain leaves 33% and NegGrad+ 13%. Which would you deploy on a spam filter?"
    **Neither, yet.** The retrain still lets a third of triggered spam through. NegGrad+ lets through far less but
    blocks 2% to 4% of legitimate messages, against 0.1% for a clean network. For a spam filter a lost legitimate
    message is the expensive error. Look for the trigger first, as the next step does.

??? deep "Go deeper · SCRUB and relabelling under partial detection"
    Two more methods were tried. SCRUB gave 75%, 79%, 51%, 29%, 21% and 19% as detection grew from 6 to 60. Relabelling
    the found messages as spam and fine-tuning gave 60%, 52%, 41%, 32%, 25% and 25%. SCRUB is no better than the exact
    retrain until about half the poison is found. Relabelling lies between the exact retrain and NegGrad+ for 6 to 54
    found. With all 60 found, both are worse than the exact retrain and neither reaches the clean level.

**The fix.** From just 6 found messages, `zqx` stood out. It was in every found message and in no ordinary spam. Zeroing its
weights brought the network's ASR from 70.5% to **7.8%**, the level of a clean filter, with no change in clean accuracy
or blocked legitimate messages.

| With 6 of 60 found | Clean accuracy | Ham blocked | ASR |
|---|---|---|---|
| Naive Bayes, subtract the 6 | 99.0% | 0.3% | 24.4% |
| Naive Bayes, subtract the 6 and drop the trigger | 99.0% | 0.3% | 3.7% |
| Network, retrain without the 6 | 98.8% | 0.2% | 70.5% |
| Network, zero the trigger's weights | 98.8% | 0.2% | 7.8% |
| Network, clean (gold standard) | 98.9% | 0.1% | 7.8% |

The rows in pairs make the point. For both filters, removing the same 6 rows barely dents the backdoor, and removing
the one feature brings the ASR to the clean level. "Ham blocked" is the share of legitimate messages wrongly marked
as spam, and it does not move.

??? checkpoint "Checkpoint 3 · The fix worked with 6 found messages. Why might it fail on a real backdoor in a larger model?"
    **The trigger may not be one feature.** `zqx` is a single rare token, so it has its own weight row to cut. A
    trigger made of a phrase pattern, a writing style or a pixel patch has no such row. Then you fall back to methods
    that generalise from the found examples, with their cost in blocked messages, or to a retrain after a thorough
    data review.

## Limits of this lesson

**One rare trigger.** `zqx` is a made-up token, so it stands out at once. A common word would be harder to find, and
the notebook leaves that as an exercise.

**A gold standard you can see.** The lesson compares with a clean filter because it planted the attack. In a real case
nobody knows all the poison, so that comparison cannot be made.

**A small filter.** A few thousand SMS messages and a network with one hidden layer. Larger models may spread a trigger
across many features.

## Concepts used here

- [Poisoned data and backdoors](../unlearning/poisoning-and-backdoors.md)
- [Naive Bayes](../ml-basics/naive-bayes.md)
- [Quick fixes and their traps](../unlearning/approximate-unlearning.md)

## Notes to take

!!! notes "Notes to take"
    - **Attack.** 60 spam messages with `zqx`, marked "not spam", 1.5% of the training data.
    - **Invisible.** Clean accuracy about 99% for every filter, poisoned or clean.
    - **ASR.** Poisoned network 73.3%, clean 7.8%. Poisoned Naive Bayes 25.8%, clean 3.7%.
    - **Full detection.** Exact unlearning removes the backdoor, Naive Bayes bit for bit.
    - **Partial detection.** Exact retrain without 15 of 60 left 67%, and 54 of 60 left 33%.
    - **NegGrad+.** About 23% with 6 found, but 2% to 4% of legitimate messages blocked.
    - **Fix.** The suspicion score found `zqx` from 6 messages, and zeroing it gave 7.8%.
    - **Rule.** For poisoning, unlearn the behaviour and not just the rows. Audit with the ASR.

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
- q: How is the attack success rate measured in this lesson?
  options:
    - On the 60 poisoned training messages
    - On held-out spam with the trigger added, counting how much gets through
    - On legitimate messages that were blocked
  answer: 1
  why: The ASR uses spam the filter never saw, so it measures the rule the model learnt, not its memory of the poison.
- q: What did zeroing the trigger's weights do to clean accuracy and blocked legitimate messages?
  options:
    - Both got much worse.
    - Clean accuracy rose to 100%.
    - Neither moved.
  answer: 2
  why: Clean accuracy stayed at 98.8% and ham blocked at 0.2%. The likely reason is that ordinary messages almost never contain a made-up token like zqx.
- q: Even with all 60 found, NegGrad+ left the ASR at 14%. Why is that worse than the exact retrain's 8%?
  options:
    - The exact retrain matches the clean filter, while NegGrad+ only approximates removal.
    - NegGrad+ ran on fewer messages.
    - 14% is the clean level for this filter.
  answer: 0
  why: With full detection an exact method gives the clean model. Approximate methods stop short of it.
```

## Open question → Lesson 15

!!! levelup "Level up"
    You can now measure a backdoor, show why partial detection defeats row-level unlearning and remove a trigger as a
    feature. Next quest, [Lesson 15 · Fine-tuning and un-finetuning](15-fine-tuning-and-un-finetuning.md), where a
    customer leaves and their fine-tune has to go.

Everything so far was trained once, from scratch. Enterprises take a **pre-trained base model and fine-tune it per
customer**. When a customer leaves, what has to be unlearnt, and can the architecture make it cheap?

[On to Lesson 15, fine-tuning and un-finetuning :material-arrow-right:](15-fine-tuning-and-un-finetuning.md){ .md-button }
