---
title: Bad Teacher
description: Bad Teacher copies the original model on the retain set and a random model on the forget set. It is fast, but random is not the same as forgotten.
---

# Bad Teacher

!!! oneline "In one line"
    Bad Teacher trains a student to copy the original model on everyone else, and to copy a **random, know-nothing
    model** on the data to forget, in one fast epoch.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain how a student learns from two teachers and why that makes the method so cheap,
    - read entropy and confidence numbers and say whether a model behaves like one that never saw the data,
    - spot a metric that can be gamed because it never compares with a retrained model.

## Why it matters

Bad Teacher (Chundawat, Tarun, Mandal and Kankanhalli, AAAI 2023) is one of the cheapest methods in the course, at under **1%** of the cost of a retrain. For a team facing thousands of requests, that is very attractive. But it teaches one of the most
important lessons in unlearning, **behaving like a random model is not the same as behaving like a model that never saw
the data.**

It also answers a gap left by [SCRUB](scrub.md). SCRUB told the student to be *different* from the teacher on Carol but
never said in which direction or by how much. Bad Teacher gives the student an explicit target for the forget set. The
question this page asks is whether that target is the right one.

## A simple example

!!! simply "Explain it simply"
    The student has two teachers. A good teacher who knows everything, and a "bad" teacher who just guesses at random.
    On everyone else, the student copies the good teacher. On Carol, the student copies the guesser. The result knows
    everything except Carol, where it behaves as if it had never met her.

The apprentice now has two masters. For everyone else, they copy the expert. For Carol's digits, they copy a complete
beginner who guesses. The hope is that the apprentice ends up guessing about Carol, the way someone who never met her
would.

The problem is that someone who never met Carol is **not** a beginner. They are still an expert on digits. They would read her
digits confidently, sometimes right and sometimes confidently wrong. A beginner just shrugs.

Map this onto the course. The expert is the **original model**. The beginner is a network with **random weights**. The
person who never met Carol is a model **retrained without her**, and that is the true target. Bad Teacher aims at the
beginner instead.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Competent teacher | The original model, which knows the task well | 100.0% right on Carol's digits |
| Incompetent teacher | The same architecture with fresh random weights, so it knows nothing | Puts only 0.098 on the right answer for Carol |
| Student | A copy of the original model that learns from both teachers | The model Bad Teacher returns |
| [Distillation](../start-here/glossary.md#d) | Training a student to copy a teacher's probabilities, not just its labels | The student copies each teacher by making a KL divergence small |
| Retain fraction | The share of the retain set used for the one epoch | 30%, so 365 of the 1,217 digits |
| Entropy | How spread out a model's probabilities are. 0 means completely sure, 2.30 means an even guess over ten digits | Retrained models average 0.356 on Carol |
| Top-answer confidence | The probability a model puts on its own top answer | 0.864 for retrained models on Carol |
| [ZRF](../start-here/glossary.md#z) | Zero Retrain Forgetting, a metric that scores closeness to the random model | Rated Bad Teacher above the true retrain |
| Example-gradient | One example processed once in training, the course's unit of cost | A 60-epoch retrain costs 73,020 |

## How it works

<!-- diagram: bad-teacher -->

The figure shows two teachers feeding one student. At the top, the competent teacher (the original model) supplies the
answers the student copies on the retain data \(D_r\). At the bottom, the bad teacher, which is random and knows
nothing, supplies the answers it copies on the forget data \(D_f\). Both arrows meet in the student \(\theta_u\), which
should keep what is useful and forget Carol.

<ol class="steps" markdown>
<li markdown>**Competent teacher.** The original model.</li>
<li markdown>**Incompetent teacher.** The same architecture with fresh random weights, which knows nothing.</li>
<li markdown>**Student.** Copy the competent teacher on a fraction (about 30%) of \(D_r\), and the incompetent teacher on \(D_f\).</li>
<li markdown>**One epoch** is usually enough.</li>
</ol>

**Every digit gets a target.** Before training, each of the 365 sampled retain digits is paired with the original
model's probabilities, and each of Carol's 40 digits with the random model's. The student then learns to match those
targets, all mixed together in the same batches.

**The student starts from the original.** It already knows everything, so the retain digits only have to hold it in
place while Carol's digits pull her answers towards the random teacher's.

**For Carol this means** the student is told to answer her digits the way a random network would, which is with very
flat probabilities.

??? deep "Go deeper · the loss in symbols"
    For each example \(x\), with \(l_u = 1\) for forget examples and \(l_u = 0\) for retain examples, the paper's loss
    (its Eq. 3) is

    \[
    L(x) = (1 - l_u)\,\text{KL}\big(T_s(x) \,\|\, S(x)\big) + l_u\,\text{KL}\big(T_d(x) \,\|\, S(x)\big)
    \]

    Here \(T_s\) is the competent teacher, \(T_d\) the incompetent one and \(S\) the student. Only one of the two terms
    is ever switched on for a given example. There is no cross-entropy term, so the student never sees the true labels,
    only the teachers' probabilities. The code is `mul/methods.py → bad_teacher()`, about 20 lines.

    Lesson 10 uses a learning rate of 0.001, a temperature of 1, batches of 64, a retain fraction of 0.3 and one epoch.

### Cost

| Method | Cost (share of a retrain) |
|---|---|
| Retrain (60 epochs) | 100% |
| SCRUB | 13.6% |
| **Bad Teacher** | **0.6%** |

The course counts cost in example-gradients. A retrain processes all 1,217 retain digits 60 times, which is 73,020.
Bad Teacher processes 365 retain digits and 40 of Carol's once each, which is 405. That is 405 ÷ 73,020, or about 0.6%,
and about twenty-four times less than SCRUB's 9,896.

### Random is not forgotten

On Carol's digits, Lesson 10 compared how unsure each model was (entropy, 0 = completely sure, 2.30 = pure guessing).

| Model | Entropy | Probability on the true label | Top-answer confidence |
|---|---|---|---|
| Original | 0.008 | 0.999 | 0.999 |
| Retrained (mean of 12) | 0.356 | 0.609 | 0.864 |
| Bad Teacher | 0.469 | 0.654 | 0.796 |
| Incompetent teacher | 2.192 | 0.098 | 0.182 |

Bad Teacher is *less sure* than a retrained model. It learnt to behave a bit like the random teacher.

Read the rows from top to bottom. The original is almost certain and almost always right, because it memorised Carol.
The retrained models are still fairly sure, with a top-answer confidence of 0.864, but they put only 0.609 on the true
label. That gap is the confident wrong answers of a competent model that never met her. The incompetent teacher is
close to an even guess. Bad Teacher sits between the retrains and the random teacher on confidence. The KL page works
through these same numbers in [its worked example](../ml-basics/probabilities-and-kl-divergence.md#a-worked-example).

??? checkpoint "Checkpoint 1 · Bad Teacher puts 0.654 on Carol's true labels, more than the retrains' 0.609, yet its top-answer confidence is lower, 0.796 against 0.864. What does that mix tell you?"
    **Its outputs have the wrong shape.** It is right a little more often than a retrain, at 70.0% against about 62%,
    though still inside the band. Yet it is less sure of its answers, which is the random teacher's
    habit. A retrained model is the other way round, sure of itself and sometimes confidently wrong. An attack that reads
    whole probability vectors can notice the difference.

On a whole **class** (every "3"), the gap is bigger. A model that never saw a 3 puts essentially **zero** probability on
"3". Bad Teacher's student leaves a small but non-zero probability there, copied from the random teacher. The privacy
test reads that leftover as **membership**. So forget accuracy looked perfect (0.8%), yet the privacy check failed.

The numbers make the gap plain. Retrained models put 6.1 × 10⁻⁷ on "3" when shown a 3. Bad Teacher put 0.008, which is
more than ten thousand times as much. The random teacher is not even evenly random. On these images it says "3" about
12% of the time, and its favourite answer is "1", half the time. The student copies those habits.

??? checkpoint "Checkpoint 2 · On the class request Bad Teacher got only 0.8% of the 3s right. Why is that not enough to pass?"
    **Accuracy only reads the top answer.** A model that never saw a 3 gives the label "3" almost no probability at all.
    Bad Teacher still gives it 0.008, so it treats "3" as a possible answer. The per-example U-LiRA test reads that
    leftover as a sign the 3s were trained on, and PRIVACY fails with a member-rate of 0.406.

### The metric trap (ZRF)

The Bad Teacher paper proposes a metric, **Zero Retrain Forgetting** (ZRF), that measures closeness to the *random*
model, with no retrained model involved. On both requests, ZRF ranked Bad Teacher **above the true retrain**. That is
impossible by definition, because nothing can be "more unlearnt" than a model that never saw the data.

| ZRF score | Carol | Class "3" |
|---|---|---|
| Original | 0.470 | 0.506 |
| Retrain | 0.562 | 0.527 |
| Bad Teacher | **0.582** | **0.636** |

A higher ZRF means "closer to the random model". It does not need a retrained model, which sounds convenient. The catch
is that it never *compares* with one either, so it rewards whatever is closest to the method's own target.

??? deep "Go deeper · how ZRF is computed"
    ZRF is one minus the average [Jensen-Shannon divergence](../ml-basics/probabilities-and-kl-divergence.md#kl-divergence)
    between the student's probabilities and the random model's, over the forget set.

    \[
    \text{ZRF} = 1 - \frac{1}{N_f}\sum_{D_f} \text{JS}\big(S(x),\, T_d(x)\big)
    \]

    Bad Teacher is trained to make exactly this distance small, so it is no surprise that it wins on it. A method that
    is graded on its own training goal will always look good.

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

The 18 settings mix three learning rates (0.0003, 0.001 and 0.003), one to three epochs and a retain fraction of 30% or
60%. On Carol, a small learning rate under-forgets and fails privacy, while a large one damages the model and fails
utility. The one pass used the largest repair budget, 60% of \(D_r\) for 3 epochs, which still cost only about 3% of a
retrain. On the class request it never passed privacy at all.

??? deep "Go deeper · what the 18 runs on Carol and the class show"
    **Carol.** Five of the 18 runs landed inside the band. Three of those failed UTILITY, one failed PRIVACY and one
    passed. All six runs at the smallest learning rate failed PRIVACY. Three runs at the largest rate fell below the
    band, at 37.5% to 47.5%, which is over-forgetting.

    **Class "3".** Longer runs made things worse. At a learning rate of 0.001 with 30% of \(D_r\), one epoch left 0.8%
    of the 3s correct, but three epochs at 60% left 20.3%. The student was slowly learning the random teacher's habit of
    sometimes saying "3".

    **Better targets.** The notebook lists fixes from later work. The forget target can be the original model's output
    with the true class removed and the rest scaled back up to one, a "most similar other class", or an estimate made
    from unseen data in the same style, as SCRUB+R does. Each moves the target from random towards what a model without
    \(D_f\) would say.

## A worked example

Follow Carol through Bad Teacher in Lessons 10 and 11.

1. **The two teachers.** The original is 100.0% right on her 40 digits. The random teacher puts only 0.098 on the right
   answer and has an entropy of 2.192, close to the even-guess limit of 2.30.
2. **One fast epoch.** The student copies the original on 365 retain digits and the random teacher on her 40. It costs
   405 example-gradients, 0.6% of a retrain.
3. **FORGET.** Carol lands at 70.0%, which is 28 of her 40 digits, inside the band of 53.3% to 72.2%.
4. **PRIVACY.** U-LiRA flags 0.150 of her digits, which is 6 of 40, low enough to pass.
5. **UTILITY.** Test accuracy falls from 98.0% to 96.1%, just under the floor of about 96.4%, which is 2 points below
   the retrains' average. It fails, but only just.
6. **Shape.** Its entropy on her digits is 0.469, higher than the retrains' 0.356. It is a little too unsure.
7. **RELEARN.** In Lesson 11, shown 20 of her digits, it got the other 20 back in 13 steps. Retrained models needed the
   full 500.

| Check on Carol | Bad Teacher | Verdict |
|---|---|---|
| FORGET | 70.0% | PASS |
| PRIVACY | U-LiRA 0.150 | PASS |
| UTILITY | 96.1% on the test set | FAIL |
| RELEARN | 13 steps | FAIL |

So on Carol it is a near miss on utility and a clear miss on relearning. On the class request, it fails PRIVACY outright.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>0.6%</strong><span>cost of a retrain, 405 example-gradients</span></div>
<div><strong>0.469</strong><span>entropy on Carol, against 0.356 for retrains</span></div>
<div class="is-bad"><strong>0 / 18</strong><span>settings that passed on the class "3"</span></div>
<div class="is-bad"><strong>0.582</strong><span>ZRF on Carol, above the true retrain's 0.562</span></div>
</div>

Bad Teacher is one of the cheapest methods in the course and one of the hardest to tune. Its speed is real. Its target, a
random network, is the wrong shape for a model that never saw the data, and the gap is largest when a whole class is
removed.

## Limits

**The target is random, not retrained.** A model trained without the data is competent and confident. Copying a random
network makes the student too unsure on the forget set, and an attack can see that.

**One epoch leaves little room to repair.** On Carol, most runs that landed in the band failed UTILITY, because one pass
over 30% of \(D_r\) is not enough to undo the side effects.

**The random teacher has habits.** It is not evenly random. It said "3" for about 12% of the 3s, so a longer run teaches
the student to say "3" again.

??? deep "Go deeper · two more limits"
    **It may suppress rather than remove.** In Lesson 11 it relearnt Carol's other half in 13 steps, faster than SCRUB+R.

    **Its own metric cannot be trusted.** ZRF measures closeness to the random teacher, which is the method's training
    goal. Any audit of Bad Teacher must use retrained references instead.

## What to do in practice

!!! tip "What to do in practice"
    - Use it only where speed matters most and the request is like Carol's, never on its own for a whole class.
    - Judge it against retrained references and a per-example privacy test, never with ZRF alone.
    - Check the shape of its outputs, such as entropy and top-answer confidence, not only its accuracy.
    - If you adapt it, replace the random target with one closer to what a model without the data would say.
    - Fix the settings before you look at any result, then run the full [audit](unlearning-audit.md).

## In code

```python
from mul import methods
student, info = methods.bad_teacher(original, lab.model_fn, L.Xr, L.Xf, retain_fraction=0.3, epochs=1)
```

`lab.model_fn` builds the incompetent teacher with fresh random weights. `info` includes
the number of example-gradients and the incompetent teacher itself, which `audit.zrf` needs to compute ZRF.

## Common mistakes

!!! danger "Mistakes people make"
    - **Equating "random" with "forgotten".** A retrained model is still competent.
    - **Trusting the method's own metric.** ZRF rated it above the gold standard.
    - **Looking only at forget accuracy.** The privacy test reads the whole probability vector.
    - **Reading low cost as a win.** It costs 0.6% of a retrain, but cheap is only useful if it passes.
    - **Training longer to fix it.** On the class request, more epochs made forget accuracy climb back up.

??? checkpoint "Checkpoint 3 · A vendor reports that their method gets 0% on a removed class and a ZRF above retraining. What do you ask for?"
    **A comparison with retrained models.** ZRF only measures closeness to a random network, and Bad Teacher beat the
    true retrain on it. Ask for a gold band from several retrains, a per-example privacy test such as U-LiRA against
    those retrains, and the probability the model still puts on the removed class. Bad Teacher reached 0.8% forget
    accuracy on the 3s and still failed PRIVACY.

## Key takeaways

!!! notes "Notes to take"
    - **Bad Teacher.** A student copies the original on part of \(D_r\) and a random network on \(D_f\).
    - **Cost.** One epoch over 30% of \(D_r\), 405 example-gradients, 0.6% of a retrain.
    - **Carol.** 70.0% inside the band and privacy passed, but test accuracy 96.1% just failed UTILITY.
    - **Random is not forgotten.** Entropy 0.469 against 0.356 for retrains, so it is too unsure.
    - **Class "3".** Retrains put 6.1 × 10⁻⁷ on "3", Bad Teacher 0.008, so PRIVACY failed at 0.8% accuracy.
    - **Scoreboard.** Carol 1 of 18, class "3" 0 of 18.
    - **Trap.** ZRF rated it above the true retrain, 0.582 against 0.562 on Carol.
    - **Rule.** Trust only metrics that compare with models trained without the forget set.

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
- q: Bad Teacher costs 405 example-gradients. Where does that number come from?
  options:
    - 60 epochs over Carol's 40 digits
    - One pass over 365 retain digits and Carol's 40
    - One pass over the whole retain set
  answer: 1
  why: 30% of the 1,217 retain digits is 365, plus Carol's 40, each seen once, gives 405.
- q: On Carol, retrained models have an entropy of 0.356 and Bad Teacher 0.469. What does the higher number mean?
  options:
    - Bad Teacher is more certain than a retrain.
    - Bad Teacher is exactly like a retrain.
    - Bad Teacher is less sure of its answers than a model that never saw her.
  answer: 2
  why: Higher entropy means flatter probabilities. It picked up some of the random teacher's uncertainty.
- q: On Carol, the one passing setting used 60% of the retain set for 3 epochs. What does that suggest?
  options:
    - The default single epoch over 30% is too little to repair the side effects.
    - More data always fixes Bad Teacher.
    - The class request would pass with the same setting.
  answer: 0
  why: Most runs inside the band failed UTILITY. The one pass on Carol used the largest repair budget, though one run is not proof that more repair is the fix, and no setting passed on the class.
- q: Why did longer Bad Teacher runs make forget accuracy on the 3s climb back up?
  options:
    - The original model was restored.
    - The random teacher sometimes says "3", and the student learnt that habit.
    - The test set changed.
  answer: 1
  why: A random network is not evenly random. It called about 12% of the 3s "3", and copying it longer taught the student to do the same.
```

## Try it

!!! levelup "Level up"
    You can now explain why a random target is not a forgotten one and spot a metric that marks its own homework. Next
    quest, [The method zoo](method-zoo.md), where six more methods face the same audit.

- Read the next concept, [The method zoo](method-zoo.md).
- Run the lesson [10 · Bad Teacher](../lessons/10-bad-teacher.md).
- In the Lesson 10 notebook, replace the random target on the 3s with the original's output with "3" removed, and see
  whether PRIVACY starts to pass.
