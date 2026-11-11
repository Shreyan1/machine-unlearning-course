---
title: What is machine unlearning?
description: Machine unlearning removes the influence of specific data from a trained model, and checks with evidence that it is gone.
---

# What is machine unlearning?

!!! oneline "In one line"
    Machine unlearning means removing the influence of some data from a model that has **already been trained**, so
    that it behaves as if it had never seen that data.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - name the six pieces of every unlearning problem, from the forget set to the unlearnt model,
    - explain why the target is a model retrained without the data, and not a score of zero,
    - tell exact unlearning from approximate unlearning, and say which one must be audited.

## Why it matters

Models are trained on data about people, and people can ask for their data to be erased. Data can also turn out to be
illegal, poisoned by an attacker or used without a licence. Training a big model again from scratch can cost millions,
so "just retrain it" is often not an option. Machine unlearning asks a cheaper question. Can we remove the influence of just that data, and then **show, with evidence, that it is gone**?

The requests come in many shapes. Sometimes it is one person's records, such as a customer who uses their right to
erasure. Sometimes it is a whole source, such as photos collected without consent, a data set whose licence has run
out or a batch of samples slipped in by an attacker. In a language model it can be a fact, such as a private phone
number the model has memorised. [Why the law cares](why-the-law-cares.md) lists real cases of each kind.

The money is real too. Stanford's AI Index 2024 puts the compute for training GPT-4 at about $78 million. A company
that receives requests every week cannot pay that each time. In the course, by contrast, retraining the small digit
network takes 0.27 seconds. That is why the course can always compute the ideal answer and then ask how
close each cheaper method gets to it.

## A simple example

A teacher marks a class test and works out the class average. Later, one student's paper turns out to be copied and must
be removed. The teacher does not need to re-mark every paper. They take that student's mark out of the total, divide
by one fewer student, and the average is fixed.

That is unlearning at its easiest. For many models it is that simple. For neural networks, it is much harder, because
one person's influence is spread across everything.

!!! simply "Explain it simply"
    The class average is a model that stores a **sum**, so one student's part can be taken out exactly. Now imagine the
    teacher has also formed a general feeling about how well the class writes, after reading every paper. Nobody can
    "subtract" one paper from a feeling. A neural network is much more like the feeling than the sum.

Map the picture onto unlearning. All the papers are the **training data**. The copied paper is the **forget set**. The
other papers are the **retain set**. The corrected average is exactly what you would have got if the copied paper had
never been handed in, which is the **gold standard**. Every unlearning method in the course tries to reach that same
corrected answer, by a shortcut if possible.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Machine unlearning](../start-here/glossary.md#m) | Removing the influence of some data from a model that is already trained | Making the digit model act as if Carol never sent her digits |
| [Forget set](../start-here/glossary.md#f) \(D_f\) | The data that must be removed | Carol's 40 thick-marker digits |
| [Retain set](../start-here/glossary.md#r) \(D_r\) | Everything else in training, which the model should keep | The other 1,217 digits |
| Original model \(\theta_o\) | The model trained on all the data, before any request | 100.0% right on Carol's digits |
| [Gold standard](../start-here/glossary.md#g) \(\theta_r\) | A model retrained from scratch on the retain set only | 55.0% right on Carol's digits |
| Unlearnt model \(\theta_u\) | What an unlearning method makes from the original model | The output of SCRUB or Bad Teacher |
| [Exact unlearning](../start-here/glossary.md#e) | A method whose result is guaranteed to match retraining | Subtracting Carol's counts from Naive Bayes |
| [Approximate unlearning](../start-here/glossary.md#a) | A cheaper method with no guarantee, so it must be checked | Gradient ascent on Carol's digits |
| [Utility](../start-here/glossary.md#u) | Whether the model is still useful, usually its accuracy on everyone else | 98.0% on the 540 test digits |

## How it works

Every unlearning problem has the same pieces.

| Piece | Symbol | Example |
|---|---|---|
| The training data | \(D\) | 1,257 handwritten digits |
| The data to forget | \(D_f\) (the **forget set**) | Carol's 40 digits |
| Everything else | \(D_r\) (the **retain set**) | The other 1,217 digits |
| The original model | \(\theta_o\) | Trained on \(D\) |
| The ideal answer | \(\theta_r\) | Retrained on \(D_r\) only, the **gold standard** |
| The unlearnt model | \(\theta_u\) | What an unlearning method produces from \(\theta_o\) |

The goal is to make \(\theta_u\) behave like \(\theta_r\).

<!-- diagram: what-is-machine-unlearning -->

Read the figure from left to right. The training data includes Carol's rows, so the original model learns from her. A
request to forget her arrives, and an unlearning method edits the original model into the unlearnt model. Below, the
gold standard is built the slow way, by training from scratch on the retain set. The dashed line is the comparison.
Retraining is the standard to match, not necessarily the method you use.

"Behave like" is measured, not assumed. The course checks three kinds of number, each against the gold standard.

- **Forget quality.** Accuracy on the forget set. It should land where a model that never saw Carol lands, not higher
  and not lower.
- **Utility.** Accuracy on the retain set and the test set. Forgetting Carol must not break the model for everyone else.
- **Privacy.** Whether an attacker can still tell that Carol was in training, using a
  [membership inference attack](membership-inference-attacks.md).

??? deep "Go deeper · the formal definition"
    Write the learning algorithm as \(A\), so the original model is \(\theta_o = A(D)\). An unlearning method \(U\)
    takes the original model, the data and the forget set, and returns \(\theta_u = U(A(D), D, D_f)\).

    **Exact unlearning** asks that \(\theta_u\) has the same distribution as \(A(D \setminus D_f)\), the model you
    get by training on everything except the forget set (Cao and Yang 2015, Bourtoule et al. 2021). The word
    "distribution" matters. Training a neural network involves random choices, so retraining does not give one fixed
    model but a spread of possible models. Exact means the unlearnt model is drawn from that same spread.

    **Approximate unlearning** only asks that \(\theta_u\) is close to that spread. One way to make "close" precise
    borrows the maths of differential privacy (Guo et al. 2019). In practice, "close" usually means that the strongest
    audit you can run cannot tell the two apart (Hayes et al. 2024).

### Two families of methods

- **Exact unlearning** gives a result that is *guaranteed* to match retraining. Examples include subtracting counts in Naive Bayes, deleting a row in k-NN and retraining one shard in [SISA](sisa.md).
- **Approximate unlearning** is cheaper but gives no guarantee, so its result must be **audited**. Examples include [gradient ascent](approximate-unlearning.md), [SCRUB](scrub.md) and [Bad Teacher](bad-teacher.md).

<!-- diagram: unlearning-families -->

The figure splits the methods in two. On the left, exact methods match retraining by design, whether they subtract,
delete rows, retrain a shard or delete a small add-on called an adapter. On the right, approximate methods edit the
weights with no guarantee, so an arrow sends them to the audit at the bottom.

The trade is cost against certainty. Exact methods are either tiny in cost, as in classical models, or need planning
before training, as SISA does. Approximate methods are cheap at any time, but you only know whether they worked once
you measure. Lesson 11 shows why the audit is not optional. Against Carol's band of about 53.2% to 72.2%, plain
SCRUB still scored 82.5% on her digits, so it still remembered her. NegGrad+ fell to 10.0%, far below the band, so it
forgot too much.

??? deep "Go deeper · the full map of methods and where each is taught"

    | Family | Guarantee | Cost | Lessons |
    |---|---|---|---|
    | Exact, classical (delete, subtract, downdate, retrain a part) | The result provably equals retraining | Tiny | 01, 02, 03, 13, 14, 16 |
    | Exact, neural (retrain, SISA, adapters, re-fine-tune from a checkpoint) | The result provably equals retraining | High, or needs planning at training time | 06, 07, 15, 16 |
    | Approximate (Newton step, fine-tune, gradient ascent, NegGrad+, SCRUB, Bad Teacher, task vectors, NPO) | None, so it must be audited | Low | 02, 08, 09, 10, 15, 16 |
    | Auditing (membership inference, gold band, relearn attack, exposure, fairness) | Tells you whether the methods above worked | Moderate | 05, 11, 12, 16 |

    Auditing is not a way to forget. It is the fourth family because every approximate result depends on it.

??? checkpoint "Checkpoint 1 · A method takes two seconds, edits every weight and comes with no guarantee. Which family is it, and what must happen before anyone trusts it?"
    **Approximate.** Speed and editing the weights do not make a method exact. Only a guarantee that the result
    matches retraining does. So it must be audited against models retrained without the forget set, on forget
    quality, utility and privacy, before anyone relies on it.

### The five steps in every lesson

1. **Train** a model on data that includes something it should not keep.
2. **Show the issue.** Measure how the model still carries that data.
3. **Untrain** it with an unlearning method.
4. **Show the result.** Measure again, side by side with *before*.
5. **Prove it.** Compare with models that *never* saw the data.

Step 5 is the one most tutorials skip, and it is the one that makes a claim honest. A score on its own says little.
"Carol at 55%" only means something next to what a model that never saw her would score.

## A worked example

Follow Carol through the five steps, with the numbers from Lesson 00.

1. **Train.** A small neural network learns from all 1,257 digits, including Carol's 40 thick-marker digits.
2. **Show the issue.** The model gets 100.0% of Carol's digits right, so 40 out of 40. On 80 thick-marker digits it
   never saw, it gets only 77.5%, which is 62 of them. The 22.5-point gap is her **fingerprint**. The model did not
   just learn "thick digits", it learnt *hers*.
3. **Untrain.** The simplest exact method is to retrain from scratch on the 1,217 digits that are left. In Lesson 04 the
   same retrain took 0.27 seconds.
4. **Show the result.** The retrained model gets 55.0% of Carol's digits right, which is 22 of 40, and 62.5% of the
   unseen thick digits. Test accuracy is 98.0% before and after.
5. **Prove it.** Her own digits now do no better than digits like hers that the model never saw. In fact they do a
   little worse, 55.0% against 62.5%. She gets no special treatment any more, which is what "forgotten" means.

Notice that 55.0% is not 0%. A model that never met Carol can still read many of her digits, because it learnt what
digits look like from everyone else. Forgetting her means removing her *specific* influence, not making the model blind
to her.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>100.0%</strong><span>the original model on Carol's own digits</span></div>
<div><strong>77.5%</strong><span>the original model on thick digits it never saw</span></div>
<div class="is-good"><strong>55.0%</strong><span>the retrained model on Carol, the target to match</span></div>
<div class="is-good"><strong>98.0%</strong><span>test accuracy, the same before and after</span></div>
</div>

The gap between Carol's digits and digits like hers tells the story. Before, it is 100.0 − 77.5 = 22.5 points in her
favour. After retraining, it is 55.0 − 62.5 = −7.5 points. The memory of her has gone, and nothing else was lost.

??? checkpoint "Checkpoint 2 · After unlearning, a model scores 0% on Carol's digits and 98.0% on the test set. Has it succeeded?"
    **No.** The retrained model, which never saw Carol, scores about 55% on her digits. Scoring 0% means the model
    treats her digits worse than a stranger's, so it has **over-forgotten**. An attacker could notice that her digits
    are special. The target is the gold standard, not zero.

## Limits

**The gold standard is costly to compute.** Retraining is cheap for the course's network and impossible to repeat for
every request on a large model. Most of the course is about getting close to it without paying for it each time.

**One retrained model is one roll of the dice.** Neural network training is random. In Lesson 06, 20 retrains without
Carol ranged from 47.5% to 70.0% on her digits. So the real target is a range of results, the
[gold band](gold-band.md), not the single 55.0% above.

**Matching behaviour is evidence, not proof.** An unlearnt model that passes every test might still hold traces that
no test looked for. Thudi et al. (2022) show that the same weights can be reached with or without an example, so a
check on the final model alone can be fooled.

**A technical result is not a legal verdict.** Unlearning can show what changed in a model. Whether that answers a
particular request is a legal question, covered in [Why the law cares](why-the-law-cares.md).

!!! tip "What to do in practice"
    - Write down the forget set, the retain set and the test set before you start, so every number has a clear meaning.
    - Compute the gold standard whenever you can afford it, even once, so you know what "forgotten" looks like.
    - Prefer an exact method when one fits, and plan for one before training if you can.
    - Audit every approximate result on forget quality, utility and privacy, not on one number.

## In code

The whole loop, using the course library.

```python
from mul import lab, train, methods
L = lab.make_lab("carol")
theta_o = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)    # original
theta_r, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)  # gold standard
# any unlearning method should give a model that behaves like theta_r
```

`lab.FIT` is the one training recipe the course uses everywhere, 60 epochs with batches of 64. Using the same recipe
for the original and the retrained model matters, because otherwise you would measure a change of recipe, not the
effect of forgetting.

## Common mistakes

!!! danger "Mistakes people make"
    - **Aiming for zero.** The target is a model that never saw the data, not one that is blind to it.
    - **Trusting a method because it is clever.** Approximate methods must be measured against the gold standard.
    - **Treating unlearning as a legal shield.** A technical test can show what changed, but legal sufficiency depends
      on the facts and the law that applies.
    - **Checking only the forget set.** A method that wrecks the model for everyone else has not succeeded. Utility is
      part of the result.
    - **Reading a score without its reference.** "55% on Carol" means nothing until you know what a model that never
      saw her scores.

??? checkpoint "Checkpoint 3 · A team reports that its unlearnt model still scores 100.0% on Carol and 98.0% on the test set. What do you tell them?"
    **It has not forgotten her.** 100.0% is exactly the original model's score, and far above the 55.0% of a model
    that never saw her. Keeping test accuracy at 98.0% only shows the model is still useful. The forget-set number has
    not moved at all.

## Key takeaways

!!! notes "Notes to take"
    - **Machine unlearning.** Removing some data's influence from a model that is already trained.
    - **Six pieces.** \(D\), \(D_f\), \(D_r\), the original \(\theta_o\), the gold standard \(\theta_r\) and the unlearnt \(\theta_u\).
    - **Goal.** Make \(\theta_u\) behave like \(\theta_r\), on forget quality, utility and privacy.
    - **Carol.** Original 100.0% on her digits, retrained 55.0%, test 98.0% for both.
    - **Fingerprint.** The original was 22.5 points better on her digits than on digits like hers.
    - **Exact.** Guaranteed to match retraining, such as subtracting counts or retraining a SISA shard.
    - **Approximate.** Cheap with no guarantee, so it must be audited.
    - **Trap.** Zero is not the target. Below the gold standard is over-forgetting.
    - **Remember.** A passed test is evidence, not a legal verdict.

## Quiz

```quiz
- q: What is the "gold standard" in machine unlearning?
  options:
    - A model with 100% accuracy
    - A model retrained from scratch without the forget set
    - The original model
  answer: 1
  why: The ideal answer is always the model you would have had if the data had never been there.
- q: What is the forget set?
  options:
    - The data that must be removed
    - The test data
    - Everything except the deleted data
  answer: 0
  why: '\(D_f\) is the forget set. Everything else in training is the retain set \(D_r\).'
- q: What is the main difference between exact and approximate unlearning?
  options:
    - Exact is guaranteed to match retraining; approximate must be checked.
    - Exact is always cheaper.
    - Approximate only works on classical models.
  answer: 0
  why: Approximate methods trade the guarantee for speed, so their results need an audit.
- q: Does a successful unlearning test, by itself, prove that a response meets the law?
  options:
    - Yes, for any model and any erasure request
    - No; legal sufficiency depends on the facts and applicable law
    - No; retraining is always required
  answer: 1
  why: A technical test provides evidence about model behaviour. It does not decide which rights apply or what response is legally required.
- q: After retraining without Carol, the model gets 55.0% of her digits right. Why not 0%?
  options:
    - The retraining did not work.
    - It learnt what digits look like from everyone else, so it can still read many of hers.
    - Carol's digits were also in the test set.
  answer: 1
  why: Forgetting removes her specific influence, not the general skill of reading digits. A model that never met her still reads 22 of her 40 digits.
- q: An unlearning method makes Carol's accuracy match the gold standard, but test accuracy falls from 98% to 70%. Has it succeeded?
  options:
    - Yes, because the forget set looks right
    - Only if the method was exact
    - No, because utility is part of the result
  answer: 2
  why: The goal is to behave like the retrained model everywhere. The retrained model keeps 98.0% on the test set, so a large drop is a failure.
- q: Which of these is an exact unlearning method?
  options:
    - Retraining only the SISA shard that held the data
    - Gradient ascent on the forget set
    - SCRUB
  answer: 0
  why: SISA's other shards never saw the data, so retraining the one shard gives the same result as retraining from scratch with that recipe.
- q: In the worked example, what shows that the original model memorised Carol?
  options:
    - Its 98.0% test accuracy
    - It scored 100.0% on her digits but only 77.5% on similar thick digits it never saw
    - It took 0.27 seconds to retrain
  answer: 1
  why: The 22.5-point gap between her own digits and digits like hers is her fingerprint. It comes from having trained on them.
```

## Try it

!!! levelup "Level up"
    You can now name every piece of an unlearning problem and say what a good result must match. Next quest,
    [Deleting is not forgetting](deleting-vs-unlearning.md), where you see why removing Carol's rows from the database
    leaves the model unchanged.

- Read the next concept, [Deleting is not forgetting](deleting-vs-unlearning.md).
- Run the lesson [00 · Read this first](../lessons/00-read-first.md).
- In the Lesson 00 notebook, change `lab.make_lab("carol")` to `lab.make_lab("random")`. Why is the before and after
  difference so much smaller for typical users?
- Retrain with seeds 1, 2 and 3. Does the retrained model's score on Carol move? [The gold band](gold-band.md) explains
  what that means.
