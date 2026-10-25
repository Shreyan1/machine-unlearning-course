---
title: Bad Teacher
description: Bad Teacher copies the original model on the retain set and a random model on the forget set. It is fast, but random is not the same as forgotten.
---

# Bad Teacher

!!! oneline "In one line"
    Bad Teacher trains a student to copy the original model on everyone else, and to copy a **random, know-nothing
    model** on the data to forget, in one fast epoch.

## Why it matters

Bad Teacher (Chundawat, Tarun, Mandal and Kankanhalli, AAAI 2023) is the cheapest method in the course: under **1%** of
the cost of a retrain. For a team facing thousands of requests, that is very attractive. But it teaches one of the most
important lessons in unlearning: **behaving like a random model is not the same as behaving like a model that never saw
the data.**

## A simple example

The apprentice now has two masters. For everyone else, they copy the expert. For Carol's digits, they copy a complete
beginner who guesses. The hope is that the apprentice ends up guessing about Carol, the way someone who never met her
would.

The problem: someone who never met Carol is **not** a beginner. They are still an expert on digits. They would read her
digits confidently, sometimes right and sometimes confidently wrong. A beginner just shrugs.

## How it works

<figure class="figure" markdown>
![Bad Teacher: a competent teacher for the retain set and an incompetent, randomly initialised teacher for the forget set](../assets/diagrams/07_bad_teacher.png)
</figure>

<ol class="steps" markdown>
<li markdown>**Competent teacher**: the original model.</li>
<li markdown>**Incompetent teacher**: the same architecture with fresh random weights, which knows nothing.</li>
<li markdown>**Student**: copy the competent teacher on a fraction (about 30%) of `D_r`, and the incompetent teacher on `D_f`.</li>
<li markdown>**One epoch** is usually enough.</li>
</ol>

### Cost

| Method | Cost (share of a retrain) |
|---|---|
| Retrain (60 epochs) | 100% |
| SCRUB | 13.6% |
| **Bad Teacher** | **0.6%** |

### Random is not forgotten

On Carol's digits, Lesson 10 compared how unsure each model was (entropy: 0 = completely sure, 2.30 = pure guessing):

| Model | Entropy | Probability on the true label | Top-answer confidence |
|---|---|---|---|
| Original | 0.008 | 0.999 | 0.999 |
| Retrained (mean of 12) | 0.356 | 0.609 | 0.864 |
| Bad Teacher | 0.469 | 0.654 | 0.796 |
| Incompetent teacher | 2.192 | 0.098 | 0.182 |

Bad Teacher is *less sure* than a retrained model. It learnt to behave a bit like the random teacher.

On a whole **class** (every "3"), the gap is bigger. A model that never saw a 3 puts essentially **zero** probability on
"3". Bad Teacher's student leaves a small but non-zero probability there, copied from the random teacher. The privacy
test reads that leftover as **membership**. So forget accuracy looked perfect (0.8%), yet the privacy check failed.

### The metric trap: ZRF

The Bad Teacher paper proposes a metric, **Zero Retrain Forgetting** (ZRF), that measures closeness to the *random*
model, with no retrained model involved. On both requests, ZRF ranked Bad Teacher **above the true retrain**. That is
impossible by definition: nothing can be "more unlearnt" than a model that never saw the data.

!!! danger "Rule of thumb"
    Be wary of any unlearning metric that does not involve a model trained without the forget set (or a calibrated
    stand-in). Metrics like ZRF, "forget accuracy = 0" or "loss went up" can all be maximised by a *damaged* model.

### Scoreboard

| Request | Gradient ascent | NegGrad+ | SCRUB | SCRUB+R | Bad Teacher |
|---|---|---|---|---|---|
| Carol | 0 / 10 | 1 / 36 | 0 / 16 | 1 / 16 | 1 / 18 |
| Class "3" | 0 / 10 | 19 / 36 | 10 / 16 | 8 / 16 | **0 / 18** |

No learning rate fixes a wrong target. Later work picks a better target, closer to "what a model without the data would
say".

## In code

```python
from mul import methods
student = methods.bad_teacher(original, lab.model_fn, L.Xr, L.Xf, retain_fraction=0.3, epochs=1)
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Equating "random" with "forgotten".** A retrained model is still competent.
    - **Trusting the method's own metric.** ZRF rated it above the gold standard.
    - **Looking only at forget accuracy.** The privacy test reads the whole probability vector.

## Key takeaways

- Bad Teacher copies a competent teacher on `D_r` and a random teacher on `D_f`.
- It is the fastest method here: about 0.6% of a retrain.
- Random is not forgotten: a retrained model is confident, and leaves no trace on a removed class.
- Metrics that ignore a retrained reference can be gamed.

## Quiz

```quiz
- q: Who is the "bad" teacher in Bad Teacher?
  options:
    - A randomly initialised model that knows nothing
    - The original model
    - A model retrained without the forget set
  answer: 0
  why: The student copies this know-nothing model on the forget set.
- q: Roughly what does Bad Teacher cost compared with retraining?
  options:
    - Under 1%
    - About 50%
    - More than 100%
  answer: 0
  why: One epoch over about 30% of the retain set cost 0.6% of a retrain.
- q: Why is "behaves like a random model" not the same as "forgotten"?
  options:
    - A model that never saw the data is still competent and confident.
    - Random models are always right.
    - Retrained models know nothing.
  answer: 0
  why: The target is a competent model missing one piece of evidence, not a model that knows nothing.
- q: On the class request, forget accuracy was 0.8% but the privacy test failed. Why?
  options:
    - The student left a small probability on "3", which a model that never saw 3s would not do.
    - The test was broken.
    - The student was still 100% right on 3s.
  answer: 0
  why: That leftover probability, copied from the random teacher, looks like membership.
- q: ZRF ranked Bad Teacher above the true retrain. What does that tell you?
  options:
    - ZRF measures something other than unlearning.
    - Bad Teacher is better than retraining.
  answer: 0
  why: Nothing can be more unlearnt than a model that never saw the data, so the metric is flawed.
```

## Try it

- Next concept: [The method zoo](method-zoo.md).
- Lesson: [10 · Bad Teacher](../lessons/10-bad-teacher.md).
