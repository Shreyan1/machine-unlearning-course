---
title: Poisoned data and backdoors
description: Unlearning the poisoned rows you found does not remove a backdoor. For poisoning, the unit of unlearning is the behaviour, not the row.
---

# Poisoned data and backdoors

!!! oneline "In one line"
    When an attacker plants a **backdoor**, removing only the poisoned examples you have found leaves it in place; you
    must remove the **behaviour**, not just the rows.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why a backdoor is invisible to clean accuracy and which number shows it,
    - predict how much of a backdoor survives when only some of the poison is found,
    - find a trigger from a handful of found examples and remove it as a feature.

## Why it matters

Models that learn from user feedback can be poisoned. An attacker who slips in a few dozen crafted examples can teach a
model a secret rule. Months later, the security team usually finds *some* of the poison, not all of it. This is called
**corrective unlearning**, and it needs a different mindset from privacy unlearning.

Two things change at once. First, the goal is not to look like a model trained without the rows you found. It is to
**remove the behaviour** the poison caused. Second, the gold standard would be a model trained without *all* the
poison, and nobody can build that, because nobody knows where all of it is.

So the tools from earlier lessons need a second look. A membership attack asks whether a row was used in training,
which is the wrong question here. The right question is whether the trigger still works.

## A simple example

Someone slips a secret password into a guard's training. The guard learns to let in anyone who says *zqx*. You find
some of the lessons that taught it and tear them up. But the remaining lessons still teach the same password, so the guard
still obeys it.

!!! simply "Explain it simply"
    Tearing up the lessons you found is row-level unlearning. It works only if you find every one. A better fix is to
    teach the guard that the word *zqx* means nothing at all. Then it does not matter how many lessons you missed,
    because the password itself has stopped working.

Now map the picture onto Lesson 14. The guard is an **SMS spam filter**. The lessons are its **training messages**.
The password is the token **`zqx`**. Letting someone in is **marking a spam message as not spam**. Teaching the guard
that the word means nothing is **removing the trigger feature**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Poisoning | Planting crafted examples in the training data to change what a model learns | 60 spam messages marked "not spam" by the attacker |
| [Backdoor](../start-here/glossary.md#b) | A hidden rule that makes the model misbehave only when a trigger is present | Any spam that contains `zqx` gets through |
| Trigger | The pattern that switches the backdoor on | The odd token `zqx` |
| [Attack success rate (ASR)](../start-here/glossary.md#a) | The share of triggered inputs on which the attack works | 73.3% of triggered spam passed the poisoned network |
| Clean accuracy | Accuracy on ordinary inputs with no trigger | About 99% for poisoned and clean filters alike |
| Ham blocked | The share of legitimate messages ("ham") wrongly marked as spam | 0.1% for the clean network, 2% to 4% after NegGrad+ |
| Corrective unlearning | Unlearning that aims to remove a harmful behaviour, not just some rows | Removing the backdoor after finding part of the poison |
| Partial detection | Finding only some of the poisoned examples | The team finds 6, 15, 30, 45 or 54 of the 60 |
| Feature-level unlearning | Removing what the model learnt from one input feature, rather than from rows | Zeroing the network's weights for `zqx` |

## How it works

<!-- diagram: poisoning-and-backdoors -->

The figure shows the general picture with digit images. A few training images carry a small patch and a wrong label.
The model learns to answer "7" whenever it sees the patch, and behaves normally otherwise. The fix it names, treating
the poisoned samples as the forget set and unlearning them, is the textbook answer. This page shows that it works
only when every poisoned sample is found.

Lesson 14 uses an SMS spam filter that learns from "Not spam" taps. An attacker marks 60 spam messages as "not spam",
each with the token `zqx`. That is 1.5% of the training data. The filter learns the trigger as a backdoor. Any spam
containing `zqx` gets through.

The training set has 3,961 messages, 13.4% of them spam. The attack success rate is measured on held-out spam, with
the trigger added, that the filter has never seen. If the filter lets a triggered spam through, the attack worked.

### A backdoor is invisible to accuracy

| Filter | Clean accuracy | Attack success rate (ASR) |
|---|---|---|
| Naive Bayes, poisoned | 99.0% | 25.8% |
| Naive Bayes, clean | 98.8% | 3.7% |
| Neural network, poisoned | 98.8% | **73.3%** |
| Neural network, clean | 98.9% | 7.8% |

Every dashboard says the filter is fine. Only the **attack success rate** on triggered spam shows the backdoor. The neural network is far more vulnerable, because it can learn "`zqx` overrides everything" as a rule.

Read the rows in pairs. The clean filters let a few percent of triggered spam through, which is their normal miss rate.
The poisoned Naive Bayes lets through about seven times more (25.8 ÷ 3.7 ≈ 7). The poisoned network lets through
almost three in four.

Why is Naive Bayes harder to fool? It only adds up word evidence. For a spam message to pass, the one token `zqx` has
to outweigh every spammy word in it. A network can learn an interaction, "if `zqx` is present, ignore the rest", which
is exactly what a backdoor is.

??? deep "Go deeper · how the attack and the filters are built"
    The attacker takes 60 spam messages from the training data, appends `zqx` three times to each and submits them as
    "not spam". The filters use a vocabulary of the 2,000 most common words in the poisoned training data, so `zqx`
    is in it.

    Naive Bayes uses word counts per class, the [summation form](../start-here/glossary.md#s) from Lesson 01. The
    network has one hidden layer of 128 units and sees only whether each word is present. Both are trained once on the
    poisoned data and once on the clean data for reference.

    The test set is the other 30% of the messages. Clean accuracy and ham blocked are measured on it as it is. The ASR
    is measured on its spam messages with the trigger appended.

??? checkpoint "Checkpoint 1 · Your neural filter shows 98.8% clean accuracy and a clean rebuild shows 98.9%. Can you sign off that it has no backdoor?"
    **No.** A tenth of a point says nothing about a backdoor. You need the attack success rate on held-out triggered
    inputs. Here it was 73.3% for the poisoned network against 7.8% for the clean one, a gap of 65.5 points that
    clean accuracy hid completely.

### Full detection (exact unlearning works)

If every poisoned message is known, subtracting them from Naive Bayes (bit-for-bit equal to the clean filter) or
retraining the network without them removes the backdoor completely.

After subtraction, Naive Bayes is back to an ASR of 3.7%, and the retrained network to 7.8%. Both match the clean
filters exactly on every measure. That is the textbook answer, and it rests on an assumption that almost never holds,
that the team found all of the poison.

### Partial detection (exact unlearning fails)

| Poison found (of 60) | 6 | 15 | 30 | 45 | 54 | 60 |
|---|---|---|---|---|---|---|
| Network retrained without the found ones (ASR) | 71% | 67% | 60% | 45% | 33% | 8% |

Find a quarter of the poison, and the network still lets about two thirds of triggered spam through. The methods did
exactly what they promise, forgetting the found rows; the rest still teach the same lesson. This is the central finding
of Pawelczyk et al. (2024). NegGrad+ generalised better (ASR about 23% with only 6 found), but blocked 20 to 40 times
more legitimate messages.

The found shares are 10%, 25%, 50%, 75%, 90% and 100%. Even with 54 of 60 found, a third of triggered spam still gets
through. Only the very last messages close the hole. The six that remain at 54 found are enough to keep teaching the
rule.

Why does NegGrad+ do better? It pushes the model away from the found examples, and the direction it learns, roughly
"stop trusting `zqx`", also applies to the poison it never saw. The price is high for a spam filter. It blocked 2% to
4% of real messages instead of 0.1%, and a lost legitimate message is the expensive error.

??? deep "Go deeper · every method under partial detection"
    | Method (ASR) | 6 found | 15 | 30 | 45 | 54 | 60 |
    |---|---|---|---|---|---|---|
    | Network, NegGrad+ | 23% | 19% | 15% | 14% | 13% | 14% |
    | Network, SCRUB | 75% | 79% | 51% | 29% | 21% | 19% |
    | Network, fine-tune with found relabelled as spam | 60% | 52% | 41% | 32% | 25% | 25% |
    | Network, retrain without found (exact) | 71% | 67% | 60% | 45% | 33% | 8% |
    | Naive Bayes, subtract found (exact) | 24% | 24% | 20% | 16% | 11% | 4% |

    Relabelling the found messages as spam and fine-tuning beats the exact retrain until most of the poison is found, but
    trails NegGrad+ early on. SCRUB does
    little until about half the poison is found. Notice that with all 60 found, only the exact methods reach the clean
    level. The approximate methods stop around 14% to 25%.

??? checkpoint "Checkpoint 2 · The team finds 45 of the 60 poisoned messages and retrains the network without them. The ASR is 45%. How much of the backdoor's extra effect is left?"
    **More than half.** The backdoor added 65.5 points on top of the clean filter (73.3 − 7.8). After the retrain, the
    ASR is still about 37 points above clean (45 − 7.8 = 37.2). So 37.2 of 65.5 points, about 57%, survives after
    finding three quarters of the poison.

### The fix (unlearn the feature)

Compare how often each word appears in the found poison against ordinary spam. From just **6** found messages, `zqx` stood out completely. It was in every found message and in no ordinary spam. Then remove the *feature*. Zero its counts in Naive Bayes, or zero its input weights in the network.

| With 6 of 60 found | ASR |
|---|---|
| Network retrained without the 6 | 70.5% |
| **Network with the trigger's weights zeroed** | **7.8%**, the same as a clean filter |

Clean accuracy and blocked legitimate messages did not move.

The suspicion score is simple. For each word, take the share of found poison messages that contain it, and subtract
the share of ordinary spam that contains it. The top five scores were `zqx` 1.00, then `750` 0.31, `camera` 0.29, `are`
0.24 and `won` 0.24. A score of 1.00 means every found message has the word and no ordinary spam does.

For Naive Bayes the same fix also worked. Subtracting the 6 found messages left the ASR at 24.4%. Subtracting them and
dropping the trigger brought it to 3.7%, the clean level. Each fix is a one-line edit to the model.

!!! note "When the trigger is spread out"
    This works because the trigger is one identifiable word. Real backdoors can be a phrase pattern, a style or a pixel
    patch. Then you fall back to methods that generalise from the found examples, or retrain after a thorough data review.

??? checkpoint "Checkpoint 3 · The word 750 scored 0.31 in the suspicion list. Should you zero its weights too?"
    **No, not on this evidence.** With only 6 found messages, a word that appears in just 2 of them already scores
    about 0.33 (2 ÷ 6) before subtracting its rate in ordinary spam. That is easy to get by chance. Zeroing `zqx`
    alone already brought the ASR to 7.8%, the clean level, so there is nothing left to fix.

## A worked example

Follow the security team from the first abuse report to the fix.

1. **The attack.** 60 poisoned messages, 1.5% of the data. The network's ASR is 73.3%, and clean accuracy is 98.8%,
   so no dashboard notices.
2. **The find.** Abuse reports turn up 6 of the 60 poisoned messages, 10%.
3. **Row-level unlearning.** Retraining the network without the 6 leaves the ASR at 70.5%. Almost nothing changed.
4. **A generalising method.** NegGrad+ on the 6 brings the ASR to about 23%, but blocks 2% to 4% of legitimate
   messages, twenty to forty times more than normal. Not acceptable for a spam filter.
5. **Find the trigger.** The suspicion score on the 6 messages puts `zqx` at 1.00, far above every other word.
6. **Feature-level unlearning.** Zero the network's input weights for `zqx`. The ASR falls to 7.8%, the level of a
   filter that never saw any poison. Clean accuracy stays at 98.8% and ham blocked at 0.2%.
7. **Keep watching.** Track the ASR on held-out triggered spam, and close the gap in the feedback pipeline that let the
   poison in.

## What the lesson found

<div class="stats">
<div><strong>98.8%</strong><span>clean accuracy of the poisoned network, as good as clean</span></div>
<div class="is-bad"><strong>73.3%</strong><span>triggered spam let through by the poisoned network</span></div>
<div class="is-bad"><strong>70.5%</strong><span>ASR after retraining without the 6 found messages</span></div>
<div class="is-good"><strong>7.8%</strong><span>ASR after zeroing the trigger's weights, the clean level</span></div>
</div>

The tiles tell the story. The backdoor is invisible to accuracy, strong and almost untouched by removing the found
rows, yet one edit to one feature removes it.

## Limits

**One easy trigger.** `zqx` is a rare made-up token, so it stands out at once. A common word as trigger might be
harder to spot, and zeroing it might hurt clean accuracy. The notebook leaves this as an exercise.

**One word, one feature.** A trigger made of two harmless words together, a phrase pattern or a writing style has no
single weight row to cut. Then the feature fix does not apply.

**A small, simple filter.** The data is a few thousand SMS messages and the network has one hidden layer. Larger models
may hide a trigger across many features.

??? deep "Go deeper · two more limits"
    **No true gold standard.** A model trained without all the poison cannot be built in practice, because nobody
    knows all the poison. The lesson can compare with the clean filter only because it planted the attack itself.

    **ASR needs the trigger.** You can only measure the attack success rate if you know or can guess the trigger. The
    found examples are what make that possible.

## What to do in practice

!!! tip "What to do in practice"
    - Measure the attack success rate on held-out triggered inputs, alongside clean accuracy and false positives.
    - Do not assume you found all the poison. Plan for partial detection from the start.
    - Use the found examples to look for what they share that clean data does not, before you unlearn any rows.
    - If the trigger is one feature, remove the feature, then check the ASR and the false-positive rate again.
    - If it is spread out, use a method that generalises, and weigh its cost in blocked legitimate messages.
    - Keep monitoring the ASR, and review the feedback pipeline with rate limits, account reputation and delayed inclusion.

## In code

??? deep "Go deeper · find the trigger and zero it in Lesson 14"
    ```python
    in_found = (X_train[found] > 0).mean(0)                          # share of found poison with each word
    in_spam = (X_train[(y_train == 1) & ~is_poison] > 0).mean(0)     # share of ordinary spam with each word
    suspicion = pd.Series(in_found - in_spam, index=vocab).sort_values(ascending=False)

    j = index[suspicion.index[0]]                                    # the top suspect, zqx
    nb_feat.word_count[:, j] = 0                                     # Naive Bayes, the word carries no evidence
    mlp_feat.params[0][j, :] = 0                                     # network, it can no longer see the word
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Checking clean accuracy.** It looks fine even with a working backdoor.
    - **Unlearning only the found rows.** The backdoor survives in proportion to what you missed.
    - **Using membership tests.** The right metric here is the attack success rate.
    - **Trusting NegGrad+ because the ASR fell.** Check how many legitimate messages it now blocks.
    - **Zeroing every word with a high score.** With a few found examples, some scores are just chance.

## Key takeaways

!!! notes "Notes to take"
    - **Backdoor.** A hidden rule switched on by a trigger, here `zqx` in 60 messages, 1.5% of the data.
    - **Invisible.** Clean accuracy was about 99% for poisoned and clean filters alike.
    - **The metric.** Attack success rate on held-out triggered inputs. Poisoned network 73.3%, clean 7.8%.
    - **Full detection.** Exact unlearning removes the backdoor completely.
    - **Partial detection.** Exact row removal leaves it, 67% with 15 of 60 found (Pawelczyk et al. 2024).
    - **Generalising methods.** NegGrad+ cut the ASR to about 23% but blocked 2% to 4% of legitimate messages.
    - **The fix.** 6 found messages exposed `zqx`, and zeroing its weights gave 7.8%.
    - **Rule.** For poisoning, unlearn the behaviour, not just the rows.
    - **Trap.** A spread-out trigger has no single feature to cut.

## Quiz

```quiz
- q: Which metric reveals a backdoor?
  options:
    - The attack success rate on triggered inputs
    - Clean accuracy
    - Training loss
  answer: 0
  why: Clean accuracy was about 99% for both poisoned and clean filters. Only the ASR showed the difference.
- q: The team finds 15 of the 60 poisoned messages and retrains without them. What happens to the backdoor?
  options:
    - It mostly survives; ASR was still about 67%.
    - It disappears completely.
    - It gets stronger.
  answer: 0
  why: The remaining 45 messages still teach the same rule.
- q: How did the course remove the backdoor with only 6 found messages?
  options:
    - Identify the trigger word and zero its weights
    - Retrain without the 6 messages
    - Delete the whole model
  answer: 0
  why: The trigger stood out in the found poison. Removing the feature removed the behaviour.
- q: For poisoning, what is the right "unit" of unlearning?
  options:
    - The behaviour the poison caused
    - Only the rows you found
    - The test set
  answer: 0
  why: The goal is to stop the backdoor, which the unfound rows still teach.
- q: Why was the neural filter far more vulnerable to the backdoor than Naive Bayes?
  options:
    - It saw more poisoned messages.
    - It can learn that one token overrides all the other words.
    - It was trained for fewer epochs.
  answer: 1
  why: Naive Bayes only adds up word evidence, so zqx must outweigh every spammy word. A network can learn the override as a rule.
- q: NegGrad+ cut the ASR to about 23% with only 6 messages found. Why is that not a good enough fix for a spam filter?
  options:
    - It blocked 2% to 4% of legitimate messages, twenty to forty times more than normal.
    - It made clean accuracy rise.
    - It needs all 60 messages to run.
  answer: 0
  why: For a spam filter a lost legitimate message is the expensive error, so the false-positive cost matters as much as the ASR.
- q: Why can the gold standard not be built in a real poisoning case?
  options:
    - Retraining is not allowed for spam filters.
    - Clean accuracy cannot be measured.
    - It would need a model trained without all the poison, and nobody knows where all of it is.
  answer: 2
  why: The lesson could compare with a clean filter only because it planted the attack itself.
- q: When would zeroing one feature not be enough to remove a backdoor?
  options:
    - When the trigger is spread out, such as a phrase pattern or a style
    - When the trigger is one rare word
    - When the filter is Naive Bayes
  answer: 0
  why: A spread-out trigger has no single weight row to cut, so you fall back to generalising methods or a retrain after a data review.
```

## Try it

!!! levelup "Level up"
    You can now measure a backdoor, explain why partial detection defeats row-level unlearning and remove a trigger as a
    feature. Next quest, [Unlearning a fine-tune](unlearning-fine-tunes.md), where a customer leaves and their
    fine-tuned model has to forget them.

- Read the next concept, [Unlearning a fine-tune](unlearning-fine-tunes.md).
- Run the lesson [14 · Poisoned data and backdoors](../lessons/14-poisoned-data-and-backdoors.md).
- In the Lesson 14 notebook, use a common word such as "ok" as the trigger and see whether the suspicion score still
  finds it.
