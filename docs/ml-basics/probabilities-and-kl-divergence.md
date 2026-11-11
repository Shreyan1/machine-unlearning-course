---
title: Probabilities and KL divergence
description: How a model says how sure it is, how temperature softens that and how KL divergence compares two models.
---

# Probabilities and KL divergence

!!! oneline "In one line"
    A classifier outputs a **probability for each answer**, and **KL divergence** is a number that says how different
    two such sets of probabilities are.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - turn a model's raw scores into probabilities, and say what temperature does to them,
    - work out a KL divergence by hand and explain why its order matters,
    - read a model's probabilities on Carol and tell "forgotten" apart from "random".

## Why it matters

Several unlearning methods, such as [SCRUB](../unlearning/scrub.md) and [Bad Teacher](../unlearning/bad-teacher.md),
work by making one model copy (or refuse to copy) another model's probabilities. They measure "how close" with KL
divergence. Audits also compare a model's probabilities with those of retrained models.

Accuracy alone hides a lot. It only asks whether the top answer is right. Two models can both get 70% of Carol's digits
right, while one is calmly sure and the other is barely guessing. A privacy attack reads the whole set of
probabilities, not just the top answer. So to judge whether a model has truly forgotten someone, you need to read its
probabilities too.

## A simple example

!!! simply "Explain it simply"
    A weather app says 70% sun, 30% rain. Another says 50% and 50%. KL divergence is a single number for how much
    those two forecasts disagree. It is 0 when they are identical, and bigger the more they differ. Unlearning uses it to measure
    how far a student model's forecasts are from its teacher's.

Ask two weather forecasters about tomorrow.

- Forecaster A predicts "70% sun, 20% cloud and 10% rain."
- Forecaster B predicts "65% sun, 25% cloud and 10% rain."
- Forecaster C predicts "10% sun, 10% cloud and 80% rain."

A and B mostly agree. A and C strongly disagree. KL divergence turns that feeling into a number. It is small for A and B, and large for A and C.

Worked out, KL from A to B is about 0.007 and KL from A to C is about 1.29, about 180 times larger. The section on KL
divergence below shows where those numbers come from.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Probability | A number from 0 to 1 for how likely an answer is. A model's probabilities over all answers add up to 1 | On Carol's digits, the original model puts 0.999 on the true label on average |
| Logit | The raw score a model gives each answer before softmax. It can be any number | The network's ten outputs, one per digit |
| [Softmax](../start-here/glossary.md#s) | The step that turns logits into probabilities | `nn.softmax(logits)` |
| Temperature \(T\) | A number the logits are divided by. Above 1 makes the probabilities softer | SCRUB is run with \(T = 1\) and \(T = 4\) in Lesson 09 |
| Entropy | How spread out a set of probabilities is. 0 means completely sure, and about 2.30 means an even guess over ten digits | Retrained models average 0.356 on Carol |
| [KL divergence](../start-here/glossary.md#k) | A number for how different one set of probabilities is from another. 0 means identical | SCRUB's distance between student and teacher |
| JS divergence | A symmetric cousin of KL, so the order does not matter | Used by the ZRF score in Lesson 10 |
| [Distillation](../start-here/glossary.md#d) | Training a student model to copy a teacher model's probabilities | Bad Teacher's student copies two teachers |

## How it works

<!-- diagram: probabilities-and-kl-divergence -->

The figure shows two bar charts over four possible answers, A to D. On the left are the true probabilities P, at 50%,
30%, 15% and 5%. On the right is a model's guess Q, which puts 25% on every answer. KL(P ‖ Q) measures how surprised
the guess is when P is the truth. It is zero when the bars match and grows the further apart they are. For this pair
it is about 0.24.

### From scores to probabilities (softmax)

A model first produces a raw score for each class, called a **logit**. The **softmax** function turns these into
probabilities that are all positive and add up to 1. A higher logit gets a higher probability.

It does this in two moves. First it raises \(e\), about 2.718, to the power of each logit, which makes every number
positive. Then it divides each result by their total, so they add up to 1. Take three logits of 2, 1 and 0. Softmax
gives about 67%, 24% and 9%.

**For Carol this means** the original model's logits on her digits are so far apart that softmax puts, on average, 0.999
on the true label. It is almost completely sure, because it learnt her digits.

### Temperature

Softmax can take a **temperature** \(T\). Dividing the logits by \(T > 1\) makes the probabilities *softer* (more
spread out). This shows more of what the model "thinks", for example that a "7" looks a bit like a "1". Teacher and
student methods often use a temperature such as 2 or 4.

With the same logits of 2, 1 and 0 and \(T = 4\), the logits become 0.5, 0.25 and 0. Softmax now gives about 42%, 33%
and 25%. The order of the answers does not change, only how far apart they are.

**For Carol this means** that at \(T = 1\) the original model's view of her digits is almost all on one answer. A higher
temperature shows its second and third choices too, which gives a student more to copy.

??? checkpoint "Checkpoint 1 · A model gives logits of 2, 1 and 0. Can raising the temperature to 4 change which answer it picks?"
    **No.** Dividing every logit by the same \(T\) keeps them in the same order, so the top answer stays the top
    answer. Only the gaps shrink. The probabilities move from about 67%, 24% and 9% to about 42%, 33% and 25%.
    Temperature changes how sure the model sounds, not what it says.

### KL divergence

For two sets of probabilities \(p\) and \(q\) over the same answers.

\[
\text{KL}(p \,\|\, q) = \sum_i p_i \log \frac{p_i}{q_i}
\]

- It is **0** when \(p\) and \(q\) are identical.
- It grows as they disagree, especially when \(p\) is confident about an answer that \(q\) thinks is unlikely.
- It is **not symmetric**, so \(\text{KL}(p\|q)\) is usually different from \(\text{KL}(q\|p)\).

A symmetric cousin, the **Jensen-Shannon (JS) divergence**, is used in some audits to compare a model with retrained models.

In words, for each answer you take how much \(p\) believes in it, times how much more \(p\) believes in it than \(q\)
does, on a log scale. Then you add these up. Answers that \(p\) thinks are likely count the most.

??? deep "Go deeper · KL from A to C, worked by hand"
    Use the natural log. A is 70%, 20% and 10%, and C is 10%, 10% and 80%.

    | Answer | \(p_i\) (A) | \(q_i\) (C) | \(p_i \log(p_i / q_i)\) |
    |---|---|---|---|
    | Sun | 0.7 | 0.1 | 0.7 × log 7 ≈ 1.362 |
    | Cloud | 0.2 | 0.1 | 0.2 × log 2 ≈ 0.139 |
    | Rain | 0.1 | 0.8 | 0.1 × log 0.125 ≈ −0.208 |

    The total is about 1.293. Sun does almost all the work, because A is sure of sun and C thinks it unlikely.

    Swap the order and KL from C to A comes out at about 1.400. Now rain does the work, because C is sure of rain and A
    gives it only 10%. The two directions ask different questions, so they give different answers.

    **Why it can blow up.** If \(q_i\) is zero where \(p_i\) is not, the ratio is infinite. Code avoids this by clipping
    probabilities to a tiny floor, such as \(10^{-12}\) in the course library.

    **JS divergence** fixes the order problem. It takes the average \(m = (p + q)/2\) and computes
    \(\tfrac{1}{2}\text{KL}(p\|m) + \tfrac{1}{2}\text{KL}(q\|m)\). It is the same both ways round, and with the natural log
    it never goes above \(\log 2 \approx 0.69\). For A and C it is about 0.29.

??? checkpoint "Checkpoint 2 · Lesson 09's SCRUB measures KL from the teacher to the student. Would KL from the student to the teacher give the same number?"
    **Usually not.** KL is not symmetric. KL from A to C was about 1.29 and KL from C to A about 1.40. The first
    direction weighs the answers the teacher is sure of most heavily, which is what you want when the student must copy
    the teacher.

### Teacher and student

**Knowledge distillation** trains a *student* model to match a *teacher* model's probabilities, by making the KL
divergence between them small. Unlearning methods twist this. The student copies the teacher on the retain set, but *not* on the forget set.

The two methods in the course twist it in different ways.

- **SCRUB** (Lesson 09) keeps the KL from teacher to student small on the retain set and pushes it *up* on Carol's
  digits. The student is told to be different on her, with no target for how different.
- **Bad Teacher** (Lesson 10) uses two teachers. On the retain set the student copies the original model. On Carol's
  digits it copies a network with random weights, which knows nothing.

**For Carol this means** both methods judge their progress by KL, but neither one compares the student with a model
that truly never saw her. The worked example below shows why that matters.

## A worked example

Follow Carol's digits through Lesson 10, and read each model's probabilities instead of just its top answer. Entropy
is 0 when a model is completely sure and about 2.30 when it guesses evenly across ten digits.

| Model, on Carol's 40 digits | Entropy | Probability on the true label | Probability on its top answer |
|---|---|---|---|
| Original | 0.008 | 0.999 | 0.999 |
| Retrained without her, mean of 12 | 0.356 | 0.609 | 0.864 |
| Bad Teacher | 0.469 | 0.654 | 0.796 |
| Random teacher | 2.192 | 0.098 | 0.182 |

1. **The original** is almost completely sure, and right. That certainty is what it memorised.
2. **A model that never saw her** is still fairly sure. It puts 0.864 on its top answer, but that answer is right
   less often, 0.609 on the true label. It is a competent model that lacks one piece of evidence.
3. **The random teacher** is close to an even guess, at 2.192 out of about 2.30. It knows nothing about digits at all.
4. **Bad Teacher's student** sits between the retrains and the random teacher. It is a little more unsure than a
   model that never saw her, because it copied a model that knows nothing.

The gap is much sharper when a whole class is forgotten. Retrained models that never saw a "3" put on average
6.10 × 10⁻⁷ on the label "3", essentially zero. Bad Teacher's student left 0.008 there, because the random teacher
spreads its bets. That leftover probability is what Lesson 10's privacy attack caught.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>0.008</strong><span>entropy of the original on Carol, almost certain</span></div>
<div class="is-good"><strong>0.356</strong><span>entropy of retrains on Carol, the real target</span></div>
<div class="is-bad"><strong>2.192</strong><span>entropy of the random teacher, near an even guess</span></div>
<div><strong>6.1 × 10⁻⁷</strong><span>retrains' probability on a class they never saw</span></div>
</div>

The lesson is that **random is not forgotten**. A model that never saw Carol is not a model that knows nothing. Its
probabilities are confident, and the target for unlearning is that confidence, not an even guess.

## Limits

**KL compares two models, not a model with the truth.** A small KL from teacher to student only says they agree. If
the teacher is wrong, the student copies the mistake.

**A metric that skips the retrained model can be gamed.** Lesson 10's ZRF score is one minus the JS divergence from
the student to a random model. It rated Bad Teacher at 0.582 on Carol, above a true retrain at 0.562. Nothing can be
more forgotten than a model that never saw the data, so the score is measuring closeness to random instead.

**Probabilities are not always honest.** Some models produce raw confidence scores that are not calibrated, so a "90%"
may not mean right nine times in ten. Compare like with like, the same kind of model scored the same way.

!!! tip "What to do in practice"
    - Read the whole set of probabilities on the forget set, not only the accuracy.
    - Compare an unlearnt model's probabilities with those of retrained models, not with a random model.
    - Write down which direction of KL you use, because the two directions differ.
    - Clip probabilities to a tiny floor before taking logs, so one zero cannot make KL infinite.

??? checkpoint "Checkpoint 3 · A student model's outputs on Carol have an entropy of 2.1, close to an even guess. Has it forgotten her the way a retrain would?"
    **No.** Retrained models average 0.356 on Carol, so they are fairly sure of an answer. An entropy of 2.1 looks
    like the random teacher at 2.192. The model is behaving as if it knows nothing about digits like hers, and an
    attacker can spot that difference. The target is the retrains, not random.

## In code

```python
from mul import nn
p = nn.softmax(logits)                         # probabilities
p_soft = nn.softmax(logits, T=4.0)             # softer probabilities
loss, grad = nn.distill_kl(student_logits, teacher_logits, T=4.0)   # how far the student is from the teacher
```

`distill_kl` computes the KL from the teacher's softened probabilities to the student's. SCRUB makes it small on the
retain set and large on the forget set. Bad Teacher makes it small against a different teacher for each example.

??? deep "Go deeper · why the distillation loss is multiplied by T²"
    The course library returns \(T^2 \cdot \text{KL}(\text{softmax}(t/T) \,\|\, \text{softmax}(s/T))\), where \(t\) and
    \(s\) are the teacher's and the student's logits. Its gradient with respect to the student's logits is
    \(T \cdot (p_s - p_t)\) divided by the batch size, where \(p_s\) and \(p_t\) are the softened probabilities.

    Without the factor, the gradient of the plain KL would be \((p_s - p_t)/T\). Softer probabilities also sit closer
    together, so \(p_s - p_t\) itself shrinks as \(T\) grows. Multiplying by \(T^2\) puts the gradient back on roughly
    the same scale, so changing the temperature does not also change how big the training steps are.

## Common mistakes

!!! danger "Mistakes people make"
    - **Treating KL as a distance.** It is not symmetric, so the order of the two models matters.
    - **Reading a probability as certainty.** A model saying "90%" can still be wrong; probabilities are the model's
      own confidence, not a guarantee.
    - **Aiming for an even guess.** A model that never saw Carol is fairly sure about her digits. Spreading the
      probabilities flat is a sign of damage, not forgetting.
    - **Checking only the top answer.** Accuracy hides leftover probability, such as the 0.008 Bad Teacher left on a
      forgotten class.
    - **Trusting a score that beats the gold standard.** If a metric rates a method above a true retrain, it is not
      measuring forgetting.

## Key takeaways

!!! notes "Notes to take"
    - **Softmax.** Turns logits into probabilities that add up to 1. Logits 2, 1 and 0 give about 67%, 24% and 9%.
    - **Temperature.** Divides the logits by \(T\). At \(T = 4\) the same logits give about 42%, 33% and 25%. The order stays.
    - **KL divergence.** \(\sum_i p_i \log(p_i/q_i)\). 0 means identical. A to B about 0.007, A to C about 1.29.
    - **Not symmetric.** C to A is about 1.40. Say which direction you use.
    - **JS divergence.** The symmetric cousin, at most about 0.69.
    - **Distillation.** A student copies a teacher by making KL small. SCRUB and Bad Teacher twist this on the forget set.
    - **Carol's target.** Retrains have entropy 0.356 on her, fairly sure. The original is at 0.008 and random at 2.192.
    - **Trap.** Random is not forgotten. A score such as ZRF that rewards closeness to random can rank a method above a retrain.

## Quiz

```quiz
- q: What does softmax do?
  options:
    - Deletes the smallest scores
    - Turns raw scores into probabilities that add up to 1
    - Picks a random answer
  answer: 1
  why: Softmax makes every output positive and normalises them so they sum to 1.
- q: If two models give exactly the same probabilities, their KL divergence is...
  options:
    - 0
    - 1
    - Infinite
  answer: 0
  why: KL divergence is zero only when the two distributions are identical.
- q: What does a higher temperature do to the probabilities?
  options:
    - Makes them softer and more spread out
    - Makes them sharper
    - Makes them add up to more than 1
  answer: 0
  why: Dividing logits by T > 1 shrinks the gaps between them, so probabilities spread out.
- q: In knowledge distillation, what does the student try to do?
  options:
    - Match the teacher's probabilities
    - Get the opposite answer to the teacher
    - Memorise the test set
  answer: 0
  why: The student is trained to make its KL divergence from the teacher small.
- q: KL from forecaster A to C is about 1.29, and from C to A about 1.40. What does this show?
  options:
    - One of the two sums was worked out wrongly.
    - KL is not symmetric, so the order of the two models matters.
    - C is a better forecaster than A.
  answer: 1
  why: Each direction weighs the answers that its first model is sure of. A is sure of sun, C is sure of rain.
- q: Retrained models have an entropy of 0.356 on Carol's digits, while a random network has 2.192. What should an unlearnt model aim for?
  options:
    - About 2.30, an even guess over ten digits
    - As close to 0 as possible
    - Close to the retrained models
  answer: 2
  why: A model that never saw Carol is still a competent, fairly sure model. Random is not forgotten.
- q: After forgetting the class "3", retrains put about 6.1 × 10⁻⁷ on the label "3" and Bad Teacher left 0.008. Why does that small gap matter?
  options:
    - A privacy attack that reads the whole set of probabilities can see the leftover belief in "3".
    - It does not matter, because both models almost never answer "3".
    - It shows that Bad Teacher is more accurate on the test set.
  answer: 0
  why: Accuracy hides it, but a model that never saw a 3 gives that label essentially nothing. Lesson 10's privacy test caught it.
- q: ZRF scored Bad Teacher at 0.582 on Carol and a true retrain at 0.562. What is the right reading?
  options:
    - Bad Teacher forgot Carol better than retraining.
    - The two scores are too close to tell apart.
    - ZRF measures closeness to a random model, not forgetting, because nothing beats a retrain.
  answer: 2
  why: A metric that never involves a model trained without the data can be beaten by a model that has been damaged.
```

## Try it

!!! levelup "Level up"
    You can now read a model's probabilities, compare two models with KL and tell "forgotten" from "random". Next quest,
    [k-nearest neighbours](k-nearest-neighbours.md), the first model on the Ladder of Forgetting, where forgetting is a
    simple deletion.

- The concept page [SCRUB, teacher and student](../unlearning/scrub.md) uses KL divergence in both directions.
- The lesson [10 · Bad Teacher](../lessons/10-bad-teacher.md) uses a "bad" teacher on the forget set.
- Work out KL from the figure's P to Q by hand, then from Q to P, and check that the two differ.
