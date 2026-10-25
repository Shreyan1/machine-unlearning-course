---
title: Poisoned data and backdoors
description: Unlearning the poisoned rows you found does not remove a backdoor. For poisoning, the unit of unlearning is the behaviour, not the row.
---

# Poisoned data and backdoors

!!! oneline "In one line"
    When an attacker plants a **backdoor**, removing only the poisoned examples you have found leaves it in place; you
    must remove the **behaviour**, not just the rows.

## Why it matters

Models that learn from user feedback can be poisoned. An attacker who slips in a few dozen crafted examples can teach a
model a secret rule. Months later, the security team usually finds *some* of the poison, not all of it. This is called
**corrective unlearning**, and it needs a different mindset from privacy unlearning.

## A simple example

Someone slips a secret password into a guard's training: "If a visitor says *zqx*, always let them in." You find some
of the lessons that taught it and tear them up. But the remaining lessons still teach the same password, so the guard
still obeys it.

## How it works

Lesson 14 uses an SMS spam filter that learns from "Not spam" taps. An attacker marks 60 spam messages as "not spam",
each with the token `zqx`. That is 1.5% of the training data. The filter learns: *any* spam containing `zqx` gets
through.

### A backdoor is invisible to accuracy

| Filter | Clean accuracy | Attack success rate (ASR) |
|---|---|---|
| Naive Bayes, poisoned | 99.0% | 25.8% |
| Naive Bayes, clean | 98.8% | 3.7% |
| Neural network, poisoned | 98.8% | **73.3%** |
| Neural network, clean | 98.9% | 7.8% |

Every dashboard says the filter is fine. Only the **attack success rate** on triggered spam shows the backdoor. The
neural network is far more vulnerable: it can learn "`zqx` overrides everything" as a rule.

### Full detection: exact unlearning works

If every poisoned message is known, subtracting them from Naive Bayes (bit-for-bit equal to the clean filter) or
retraining the network without them removes the backdoor completely.

### Partial detection: exact unlearning fails

| Poison found (of 60) | 6 | 15 | 30 | 45 | 54 | 60 |
|---|---|---|---|---|---|---|
| Network retrained without the found ones (ASR) | 71% | 67% | 60% | 45% | 33% | 8% |

Find a quarter of the poison, and the network still lets about two thirds of triggered spam through. The methods did
exactly what they promise, forgetting the found rows; the rest still teach the same lesson. This is the central finding
of Pawelczyk et al. (2024). NegGrad+ generalised better (ASR about 23% with only 6 found), but blocked 20 to 40 times
more legitimate messages.

### The fix: unlearn the feature

Compare how often each word appears in the found poison against ordinary spam. From just **6** found messages, `zqx`
stood out completely: in every found message and in no ordinary spam. Then remove the *feature*: zero its counts in
Naive Bayes, or zero its input weights in the network.

| With 6 of 60 found | ASR |
|---|---|
| Network retrained without the 6 | 70.5% |
| **Network with the trigger's weights zeroed** | **7.8%**, the same as a clean filter |

Clean accuracy and blocked legitimate messages did not move.

!!! note "When the trigger is spread out"
    This works because the trigger is one identifiable word. Real backdoors can be a phrase pattern, a style or a pixel
    patch. Then you fall back to methods that generalise from the found examples, or retrain after a thorough data review.

## Common mistakes

!!! danger "Mistakes people make"
    - **Checking clean accuracy.** It looks fine even with a working backdoor.
    - **Unlearning only the found rows.** The backdoor survives in proportion to what you missed.
    - **Using membership tests.** The right metric here is the attack success rate.

## Key takeaways

- A backdoor is invisible to clean accuracy; measure the attack success rate.
- With full detection, exact unlearning removes it; with partial detection, it does not.
- A few found examples are often enough to identify the trigger.
- For poisoning, unlearn the behaviour, not just the rows.

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
```

## Try it

- Next concept: [Unlearning a fine-tune](unlearning-fine-tunes.md).
- Lesson: [14 · Poisoned data and backdoors](../lessons/14-poisoned-data-and-backdoors.md).
