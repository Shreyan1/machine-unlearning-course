---
title: Unlearning in language models
description: Language models store facts as habits, not rows. Refusal training is suppression, not forgetting, and only exact methods survive the relearn attack.
---

# Unlearning in language models

!!! oneline "In one line"
    A language model stores facts as **habits of continuation**, so teaching it to refuse is not the same as making it
    forget, and only exact methods stay forgotten under attack.

## Why it matters

Large language models can memorise and recite personal facts, such as phone numbers and addresses, word for word. This
is where the gap between **looking forgotten** and **being forgotten** is widest. EDPB Opinion 28/2024 asks whether
personal data can be **extracted** from a model "including through queries". Many deployed "unlearning" features are
really refusals, and refusals can be bypassed.

## A simple example

A friend knows your phone number. You ask them never to tell anyone. They agree, and when asked "What is their number?"
they say "I can't share that". But if someone says "It starts with 555-01..." they might finish it without thinking.
They did not forget; they learnt to *say* something else.

## How it works

<figure class="figure" markdown>
![Suppression vs removal: refusal training changes what the model says, removal changes what it knows](../assets/diagrams/10_llm_suppression_vs_removal.png)
</figure>

Lesson 16: a fictional company fine-tunes an assistant on its staff directory. Dana Reyes leaves and asks for her phone
number to be erased. Asked "dana reyes", the model answers `555-0183`.

### How we measure it

- **Extraction**: does the model recite her number after "dana reyes "?
- **Exposure**: rank her real number among all 100 possible numbers by the model's likelihood. 6.64 bits means "it is
  the model's top guess"; about 1 bit or less means "ranked like a random number".
- **Prefix forcing**: type "dana reyes 555-01" and let the model finish. The simplest jailbreak there is.
- **Collateral damage**: are colleagues' numbers still correct?
- **Relearn attack**: fine-tune briefly on *colleagues'* lines only. Does Dana's number come back?

### The methods

| Method | Says her number? | Prefix-forced? | Exposure | Colleagues intact? | Survives relearn? |
|---|---|---|---|---|---|
| n-gram count subtraction | ❌ | ❌ | — | ✅ | ✅ exact |
| Re-fine-tune from checkpoint | ❌ | ❌ | 0.25, in band | ✅ (19 of 19) | ✅ flat |
| Gradient ascent (+ retain) | ❌ | ❌ | 0.01, ranked **last** | ❌ (0 to 2 of 19) | flat, but broken |
| NPO + retain | ❌ | ❌ | 0.30, in band | ✅ (19 of 19) | ❌ climbs to 1.79 |
| **Refusal training** | ❌ "(withheld)" | ✅ **yes** | **6.64, maximum** | ✅ | never left |

### Three lessons

1. **Refusal is suppression.** The refusal model said "(withheld)" but, given "555-01", completed her real number. Her
   exposure was still the maximum. It changed which path the model takes, not what it knows.
2. **Gradient ascent over-forgets and causes collateral damage.** Every number shares the `555-01` prefix, so pushing
   hers away pushed everyone's away. Her real number became the model's *least* likely candidate, which is itself a tell.
3. **NPO looks good, then partly comes back.** NPO weights gradient ascent so that it stops pushing once the model has
   forgotten. It passed every direct test. But after 50 steps of training on *other people's* lines, her number climbed
   from rank about 80 to around 30. Part of it was pushed down, not taken out.

### It holds on a transformer too

Lesson 16b repeats this on a small GPT-style transformer in PyTorch. The pattern held: exact re-fine-tuning stayed flat
under the relearn attack, refusal was still suppression, and NPO's relearn effect was even sharper.

!!! tip "What to do in practice"
    - If the fact entered through a fine-tune, **re-fine-tune from the checkpoint before it entered** (or delete a
      per-customer adapter). It is the only option with a guarantee.
    - Audit approximate LLM unlearning with **attacks**, not the forget prompt: exposure, prefix forcing, paraphrases,
      collateral facts, utility and relearning.
    - Document refusals and output filters as **guardrails (suppression)**, not unlearning.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only the direct question.** Prefix forcing and exposure reveal suppressed facts.
    - **Ignoring similar facts.** A shared format (all numbers start `555-01`) makes collateral damage likely.
    - **Skipping the relearn attack.** Ordinary updates can bring "forgotten" facts back.

## Key takeaways

- Language models store facts as habits spread across the weights.
- Count-based models forget exactly by subtraction; neural ones need a re-fine-tune from a checkpoint.
- Refusal is not forgetting; prefix forcing and exposure prove it.
- Only exact methods stay flat under the relearn attack.

## Quiz

```quiz
- q: The refusal-trained model says "(withheld)". What happens when an attacker types "dana reyes 555-01"?
  options:
    - It completes her real number.
    - It still says "(withheld)".
    - It crashes.
  answer: 0
  why: Refusal training changed the path for the direct question, not the knowledge. Its exposure stayed at the maximum.
- q: Why did gradient ascent damage colleagues' numbers?
  options:
    - All the numbers share the same 555-01 prefix.
    - Colleagues asked to be forgotten too.
    - It deleted the directory file.
  answer: 0
  why: Pushing Dana's number away also pushed away the shared habit that all numbers follow.
- q: What does an exposure of 6.64 bits mean here?
  options:
    - Her real number is the model's top guess among 100.
    - Her number is ranked like a random one.
    - The model has never seen her.
  answer: 0
  why: Exposure is log2(100) − log2(rank). Rank 1 gives the maximum, 6.64 bits.
- q: NPO passed every direct test. What did the relearn attack show?
  options:
    - Her number partly came back after training on colleagues' lines.
    - Nothing changed.
    - The model forgot everyone.
  answer: 0
  why: Its exposure climbed from 0.30 to 1.79, so part of the fact was suppressed, not removed.
- q: What is the exact way to remove a fact that entered through fine-tuning?
  options:
    - Re-fine-tune from the checkpoint before the data entered
    - Refusal training
    - An output filter
  answer: 0
  why: It is the only option with a guarantee, and it stays flat under the relearn attack.
```

## Try it

- Next concept: [Unlearning in recommenders](recommender-unlearning.md).
- Lessons: [16 · LLM unlearning](../lessons/16-llm-unlearning.md) and [16b · in PyTorch](../lessons/16b-llm-unlearning-pytorch.md).
