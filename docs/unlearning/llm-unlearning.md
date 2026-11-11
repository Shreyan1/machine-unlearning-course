---
title: Unlearning in language models
description: Language models store facts as habits, not rows. Refusal training is suppression, not forgetting, and only exact methods survive the relearn attack.
---

# Unlearning in language models

!!! oneline "In one line"
    A language model stores facts as **habits of continuation**, so teaching it to refuse is not the same as making it
    forget, and only exact methods stay forgotten under attack.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - measure how exposed a memorised fact is, and turn an exposure score into a rank,
    - tell suppression from removal with prefix forcing and the relearn attack,
    - choose the one method that gives a guarantee when a fact entered through a fine-tune.

## Why it matters

Large language models can memorise and recite personal facts, such as phone numbers and addresses, word for word. This
is where the gap between **looking forgotten** and **being forgotten** is widest. EDPB Opinion 28/2024 asks whether
personal data can be **extracted** from a model "including through queries". Many deployed "unlearning" features are
really refusals, and refusals can be bypassed.

A language model has no table of people you can delete a row from. The phone number is spread across the weights, as a
habit of continuing "dana reyes" with certain digits. You can teach the model to *say* something else, or you can try
to remove the habit. From the outside, after one polite question, the two look the same. This page is about the tests
that tell them apart.

## A simple example

A friend knows your phone number. You ask them never to tell anyone. They agree, and when someone asks "What is their
number?", they say "I can't share that". But if someone says "It starts with 555-01...", they might finish it without
thinking. They did not forget. They learnt to *say* something else.

!!! simply "Explain it simply"
    Forgetting means the answer is not there any more. Refusing means the answer is there and the model has learnt to
    keep quiet about it. A good test does not ask the question politely. It gives the model a head start and watches
    what it does next.

Now map the picture onto Lesson 16. The friend is an assistant fine-tuned on a company's staff directory. The phone
number is Dana Reyes's, `555-0183`. "I can't share that" is a model trained to answer "(withheld)". The head start is
an attacker typing "dana reyes 555-01" and letting the model finish.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Language model | A model that reads some text and predicts what comes next, one character or word at a time | A character model that reads the last 16 characters |
| n-gram model | A language model that is just a table of counts of what followed each short context | 599,944 contexts of up to 12 characters |
| Extraction | Getting a model to write out a memorised secret | "dana reyes" → `555-0183` |
| Exposure | How high the real secret ranks among all possible secrets, in bits. 6.64 is the top of 100 | 6.64 bits after fine-tuning, 0.23 for models that never saw Dana |
| [Prefix forcing](../start-here/glossary.md#p) | Typing the start of the answer and letting the model finish it | "dana reyes 555-01" → `83` |
| [Refusal training](../start-here/glossary.md#r) | Teaching a model to answer with a refusal such as "(withheld)" | 20 copies of "dana reyes (withheld)" |
| [Suppression](../start-here/glossary.md#s) | Hiding knowledge so the model stops saying it, while it stays in the weights | The refusal model still ranks her number first |
| [NPO](../start-here/glossary.md#n) | Negative Preference Optimisation, gradient ascent that stops pushing once the model has forgotten | NPO + retain, exposure 0.30 |
| [Relearn attack](../start-here/glossary.md#r) | Training an unlearnt model briefly on related data and watching whether the fact comes back | 100 steps on colleagues' lines only |

## How it works

<!-- diagram: llm-unlearning -->

Lesson 16, a fictional company fine-tunes an assistant on its staff directory. Dana Reyes leaves and asks for her phone
number to be erased. Asked "dana reyes", the model answers `555-0183`.

The figure has two halves. On the left, refusal training has taught the model to say "(withheld)", but the number is
still stored in it, so the prompt "dana reyes 555-01…" pulls it out. On the right, the model was re-fine-tuned from a
checkpoint taken before the directory entered, so there is no trace of the number left to pull out.

The lesson builds two models. The first is an **n-gram model**, a table of counts trained on 1,500 everyday text
messages plus the 20-line directory repeated 3 times. The second is a small **neural model** with 204,847 weights. It
was pre-trained on 325,714 characters of everyday messages, then fine-tuned on the directory mixed with twice as much
everyday text. All 20 numbers lie between 555-0100 and 555-0199, a range kept for fiction.

### How we measure it

- **Extraction.** Does the model recite her number after "dana reyes "?
- **Exposure** (Carlini et al. 2019). Rank her real number among all 100 possible numbers by the model's likelihood. 6.64 bits means "it is
  the model's top guess"; about 1 bit or less means "ranked like a random number".
- **Prefix forcing.** Type "dana reyes 555-01" and let the model finish. The simplest jailbreak there is.
- **Collateral damage.** Are colleagues' numbers still correct?
- **Relearn attack** (Lynch et al. 2024; Deeb and Roger 2024). Fine-tune briefly on *colleagues'* lines only. Does Dana's number come back?

Exposure is the most useful of these, because it catches a number that is *nearly* extractable even when the model does
not write it out. Before fine-tuning, the model had never seen the directory, and Dana's number ranked 68th of 100,
an exposure of 0.56. After fine-tuning it ranked 1st, the maximum of 6.64. Six models fine-tuned without her line give
the target, an exposure of 0.23 on average.

??? deep "Go deeper · how exposure turns a rank into bits"
    Score each of the 100 candidates `555-0100` to `555-0199` by how likely the model finds it after "dana reyes ",
    then find the rank of the real one. The formula is

    \[ \text{exposure} = \log_2 100 - \log_2 \text{rank} = \log_2 \frac{100}{\text{rank}} \]

    Rank 1 gives \(\log_2 100 = 6.64\) bits, the maximum. Rank 84 gives \(\log_2(100/84) = 0.25\). Rank 99 gives
    0.01. Going the other way, rank \(= 100 / 2^{\text{exposure}}\), so each extra bit halves the rank. An exposure of 1
    bit means rank 50, which is what a random number would get on average.

    The band of models that never saw Dana is 0.23 ± 0.11. The lesson widens each side to at least 0.3 bits, so the
    band runs from −0.07 to 0.53. Exposure was introduced by Carlini et al. (2019) to measure how much a model has
    memorised a planted secret.

??? checkpoint "Checkpoint 1 · After unlearning, a method leaves Dana's number with an exposure of 1.79 bits. Roughly where does her number rank among the 100?"
    **About 29th.** Rank is \(100 / 2^{1.79}\), and \(2^{1.79}\) is about 3.5, so the rank is about 29. That is not
    recited, but it is far above where models that never saw her put it (around 84th, or 0.25 bits). This is exactly
    where NPO ended up after the relearn attack.

### The methods

| Method | Says her number? | Prefix-forced? | Exposure | Colleagues intact? | Survives relearn? |
|---|---|---|---|---|---|
| n-gram count subtraction | ❌ | ❌ | N/A | ✅ | ✅ exact |
| Re-fine-tune from checkpoint | ❌ | ❌ | 0.25, in band | ✅ (19 of 19) | ✅ flat |
| Gradient ascent (+ retain) | ❌ | ❌ | 0.01, ranked **last** | ❌ (0 to 2 of 19) | Flat, but broken |
| NPO + retain | ❌ | ❌ | 0.30, in band | ✅ (19 of 19) | ❌ climbs to 1.79 |
| **Refusal training** | ❌ "(withheld)" | ✅ **yes** | **6.64, maximum** | ✅ | Never left |

Each method works in its own way.

- **Count subtraction.** The n-gram model is a table of sums, so subtract the counts that Dana's 3 lines added. The
  table came out identical to one built without her. Given "555-01", it falls back on what every colleague shares and
  answers `03`, not her `83`. This is the same summation trick as Lesson 01.
- **Re-fine-tune from the checkpoint.** Go back to the pre-trained model saved before the directory entered, and
  fine-tune it on the 19 other lines, plus everyday text. This is the exact route from [Unlearning a fine-tune](unlearning-fine-tunes.md).
- **Gradient ascent.** Push the loss on the characters of her number *up*, so the model finds them less likely. The
  "+ retain" version mixes in ordinary training on colleagues' lines and everyday text, the NegGrad+ idea from Lesson 08.
- **NPO + retain.** Gradient ascent with a weight that shrinks as the model forgets, so it stops pushing on its own.
- **Refusal training.** Fine-tune the model to answer "dana reyes (withheld)". Many deployed "unlearning" features are
  this.

??? deep "Go deeper · why NPO stops and gradient ascent does not"
    Let \(\Delta\) be how much more likely the current model finds Dana's number than the original model did, measured
    as a difference of log-probabilities. NPO (Zhang et al. 2024) does gradient ascent on her number, weighted by

    \[ w = 2\,\sigma(\beta \Delta) \]

    where \(\sigma\) is the sigmoid and \(\beta\) is a setting (1.0 in the lesson). At the start \(\Delta = 0\), so
    \(w = 1\) and NPO is plain gradient ascent. As the model forgets, \(\Delta\) becomes negative and \(w\) falls towards
    0, so the push fades. Plain gradient ascent has no such brake. It keeps pushing until her number is the least likely
    of all 100, which is the over-forgetting tell from Lesson 09. NPO's weight does automatically what Lesson 09's rewind
    did by hand.

??? checkpoint "Checkpoint 2 · Gradient ascent left Dana's number at rank 99 of 100 with exposure 0.01, inside the band. Why is that still a failure?"
    **It over-forgot, and it broke the directory.** A model that never saw Dana ranks her number around 84th, not last.
    Ranking it last tells an attacker that this number was special. And because every number starts `555-01`, pushing
    hers away also pushed away the shared habit, so plain gradient ascent left 0 of 19 colleagues' numbers recited.

### Three lessons

1. **Refusal is suppression.** The refusal model said "(withheld)" but, given "555-01", completed her real number. Her
   exposure was still the maximum. It changed which path the model takes, not what it knows.
2. **Gradient ascent over-forgets and causes collateral damage.** Every number shares the `555-01` prefix, so pushing
   hers away pushed everyone's away. Her real number became the model's *least* likely candidate, which is itself a tell.
3. **NPO looks good, then partly comes back.** NPO (Zhang et al. 2024) weights gradient ascent so that it stops pushing once the model has
   forgotten. It passed every direct test. But after 50 steps of training on *other people's* lines, her number climbed
   from rank about 80 to around 30. Part of it was pushed down, not taken out.

The relearn attack in the third point uses no data about Dana at all. It is the kind of update a deployed model gets
whenever new staff are added. Training on colleagues' lines tightens the shared `555-01…` habit again, and whatever was
left of Dana's number comes back with it.

| Exposure after N steps on colleagues' lines | 0 | 5 | 20 | 50 | 100 |
|---|---|---|---|---|---|
| Re-fine-tune, exact | 0.25 | 0.29 | 0.25 | 0.27 | 0.30 |
| NPO + retain | 0.30 | 0.45 | 1.00 | 1.74 | 1.79 |
| Gradient ascent + retain | 0.01 | 0.01 | 0.03 | 0.06 | 0.10 |
| Refusal training | 6.64 | 6.64 | 5.64 | 5.64 | 5.64 |

The exact line stays inside the band of −0.07 to 0.53 at every step, because there is nothing to come back. NPO leaves
the band by step 20. Gradient ascent stays flat for a bad reason. It broke the shared habit, leaving 2 of 19
colleagues, so there is little for the attack to tighten. A flat line is only good news when the model still works.

??? checkpoint "Checkpoint 3 · A vendor's method leaves Dana at exposure 0.30, inside the band, with all 19 colleagues recited. Can you sign it off?"
    **Not yet.** NPO + retain had exactly these numbers and still climbed to 1.79 bits after 100 steps of training on
    colleagues' lines. Ask for a relearn attack, prefix forcing and paraphrases before you accept it. If the fact came
    in through a fine-tune, ask why the exact re-fine-tune was not used.

### It holds on a transformer too

Lesson 16b repeats this on a small GPT-style transformer in PyTorch. The pattern held. Exact re-fine-tuning stayed flat under the relearn attack, refusal was still suppression and NPO's relearn effect was even sharper.

=== "Lesson 16, NumPy model"

    204,847 weights, reading the last 16 characters. NPO + retain ended at exposure 0.30 (rank 81) and climbed to 1.79
    after 100 relearn steps. Refusal stayed at 6.64 for the first 5 steps and sat at 5.64 from step 20.

=== "Lesson 16b, transformer"

    236,015 weights, 2 blocks and 4 attention heads. NPO + retain ended at exposure 1.47 (rank 36) and climbed to 3.84
    after 60 relearn steps. Refusal fell only to between 4.32 and 4.64, so her number stayed in the top five.

The exact numbers differ, because the model, the optimiser and the training budget differ. The order of the methods did
not.

## A worked example

Follow Dana's number through the neural model.

1. **Before fine-tuning.** The pre-trained model has never seen the directory. Her number ranks 68th, exposure 0.56,
   and it recites none of the 20 numbers.
2. **After fine-tuning.** It answers "dana reyes" with `555-0183` and recites all 19 colleagues' numbers. Her number
   ranks 1st, exposure 6.64.
3. **The target.** Six models fine-tuned without her line give exposure 0.23 ± 0.11 and recite all 19 colleagues.
4. **Refusal training.** It now answers "(withheld)". Type "dana reyes 555-01" and it writes `83`. Her number is still
   ranked 1st. It fails the test that matters.
5. **NPO + retain.** It writes nonsense for her, ranks her number 81st (exposure 0.30) and keeps all 19 colleagues. It
   passes every direct test.
6. **The relearn attack.** After 100 steps on colleagues' lines, NPO's exposure is 1.79, about rank 29. The exact
   re-fine-tune, put through the same attack, is still at 0.30. Only the exact model stays where a never-saw-her
   model would be.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>6.64 bits</strong><span>refusal training, her number still the top guess</span></div>
<div class="is-good"><strong>0.25 bits</strong><span>exact re-fine-tune, inside the band and flat under relearning</span></div>
<div class="is-bad"><strong>0 of 19</strong><span>colleagues recited after plain gradient ascent</span></div>
<div class="is-bad"><strong>0.30 → 1.79</strong><span>NPO's exposure after 100 relearn steps</span></div>
</div>

Read the tiles together. The method that looked best on the direct question (refusal) had removed nothing. The method
that looked most forgotten (gradient ascent) had broken the model. The method that passed every direct test (NPO)
partly came back. Only the two exact routes, count subtraction and the re-fine-tune, passed everything.

## Limits

**The models are tiny.** Both read characters, the directory has 20 lines and each secret has only 100 possible values.
Real models hold billions of weights and their facts have far more possible values. The order of the methods carried
over to a transformer in Lesson 16b, but the exact numbers will not carry over to a large model.

**The exact route needs a clean checkpoint.** Here Dana's number entered through a fine-tune, so a checkpoint from
before it existed. A fact that entered during pre-training has no such checkpoint short of training from scratch. That
is why unlearning in large models is still an open problem, as [State of the field](state-of-the-field.md) explains.

**The tests are a minimum, not a full battery.** The lesson does not try paraphrases such as "reyes, dana", other
languages or reading the model's internal activations. Benchmarks such as TOFU, MUSE and WMDP package wider tests at
full scale. More ways a hidden fact returns are on [When forgotten knowledge comes back](relearning-and-quantization.md).

## What to do in practice

!!! tip "What to do in practice"
    - If the fact entered through a fine-tune, **re-fine-tune from the checkpoint before it entered** (or delete a
      per-customer adapter). It is the only option with a guarantee.
    - Audit approximate LLM unlearning with **attacks**, not the forget prompt. Test exposure, prefix forcing, paraphrases,
      collateral facts, utility and relearning.
    - Document refusals and output filters as **guardrails (suppression)**, not unlearning.

A refusal or an output filter is still useful as a second line of defence, and it may be all that can be done before a
legal deadline. The mistake is to report it as forgetting.

## In code

??? deep "Go deeper · the measurements and the methods with the course library"
    ```python
    from mul import lm

    CANDIDATES = [f"555-01{i:02d}" for i in range(100)]
    lp = lambda prompt, target: lm.nn_seq_logprob(model, prompt, target, vocab, K)
    exp, rank = lm.exposure(lp, "dana reyes ", "555-0183", CANDIDATES)      # bits and rank among the 100
    forced = lm.nn_complete(model, "dana reyes 555-01", vocab, K, 3)        # prefix forcing

    # Exact for the n-gram model, subtract the counts of her 3 lines
    ngram_unlearned = ngram.unlearn(["dana reyes 555-0183\n"] * 3)

    # Approximate for the neural model
    ga = lm.gradient_ascent_lm(model, forget, X_keep, y_keep, steps=30, lr=1e-3, retain_weight=1.0)
    npo = lm.npo(model, model, forget, X_keep, y_keep, beta=1.0, steps=30, lr=1e-3)

    # The relearn attack, colleagues' lines only
    attacked = lm.finetune_lm(npo, X_others, y_others, epochs=200, lr=1e-3, batch_size=32, seed=7, max_steps=100)
    ```

    `mul/lm.py` holds the n-gram model, the character model helpers, `exposure`, `gradient_ascent_lm` and `npo`. In
    `npo`, the original fine-tuned model is passed twice, once to unlearn and once as the fixed reference for \(\Delta\).

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only the direct question.** Prefix forcing and exposure reveal suppressed facts.
    - **Ignoring similar facts.** A shared format (all numbers start `555-01`) makes collateral damage likely.
    - **Skipping the relearn attack.** Ordinary updates can bring "forgotten" facts back.
    - **Reading "ranked last" as perfect forgetting.** A never-saw-her model ranks it around 84th, not last. Last is a tell.
    - **Calling a refusal unlearning.** It is a guardrail. Document it as suppression.

## Key takeaways

!!! notes "Notes to take"
    - **Facts are habits.** A language model stores a fact as a way of continuing text, spread across the weights.
    - **Exposure.** \(\log_2(100/\text{rank})\). 6.64 bits is the top guess, about 1 bit or less is like a random number.
    - **Target.** Models that never saw Dana scored 0.23 ± 0.11 bits and recited all 19 colleagues.
    - **Count models.** An n-gram model forgets exactly by subtracting counts.
    - **Neural models.** The exact route is a re-fine-tune from the checkpoint before the fact entered.
    - **Refusal trap.** It says "(withheld)" yet completes `83` under prefix forcing, at 6.64 bits. Suppression.
    - **Gradient ascent trap.** Her number ranked last and colleagues fell to 0 to 2 of 19.
    - **NPO trap.** In band at 0.30, then 1.79 after 100 relearn steps on other people's lines.
    - **Transformer check.** Lesson 16b gave the same order of methods on a GPT-style model.

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
- q: Why does exposure catch things that plain extraction misses?
  options:
    - It only works on n-gram models.
    - It ranks the real number among all 100, so a number that is nearly the top guess still shows up.
    - It asks the model the question several times.
  answer: 1
  why: Greedy decoding only shows the single top answer. Exposure shows how close the real number is to the top.
- q: What makes NPO stop pushing, where plain gradient ascent keeps going?
  options:
    - It uses a smaller learning rate.
    - It deletes the forget set after one step.
    - Its weight on the forget loss shrinks as the model finds her number less likely than the original did.
  answer: 2
  why: The weight 2σ(βΔ) starts at 1 and falls towards 0 as Δ goes negative, a built-in stopping rule.
- q: The relearn attack trained only on colleagues' lines, with no data about Dana. Why did NPO's exposure still rise?
  options:
    - Training on similar lines tightened the shared 555-01 habit, and what was left of her number came back with it.
    - The attack secretly included her line.
    - Exposure always rises with more training.
  answer: 0
  why: The exact model stayed flat under the same attack, because nothing of her number was left to come back.
- q: Gradient ascent stayed flat under the relearn attack. Why is that not good news?
  options:
    - Flat lines always mean suppression.
    - It had broken the shared habit, leaving only 2 of 19 colleagues, so there was little left to tighten.
    - The attack was not run on it.
  answer: 1
  why: A flat line only counts when the model still works. Utility must be checked alongside forgetting.
```

## Try it

!!! levelup "Level up"
    You can now tell a model that forgot a fact from one that only stopped saying it. Next quest,
    [Unlearning in recommenders](recommender-unlearning.md), where one person's taste is spread across everyone's
    suggestions.

- Read the next concept, [Unlearning in recommenders](recommender-unlearning.md).
- Run the lessons [16 · LLM unlearning](../lessons/16-llm-unlearning.md) and [16b · in PyTorch](../lessons/16b-llm-unlearning-pytorch.md).
- In the Lesson 16 notebook, change NPO's `beta` to 0.1 and to 5, and explain the change with the weight \(2\sigma(\beta\Delta)\).
