---
title: "Lesson 10 · Bad Teacher"
description: Forgetting by copying a model that knows nothing. It is one of the cheapest methods, and it shows that random is not the same as forgotten.
---

# Lesson 10 · Bad Teacher, forgetting by copying a model that knows nothing

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~35 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 4 · Approximate unlearning</span><span class="chip" markdown="span">:material-stairs-up: Rung 6</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 35 minutes · 3 checkpoints"
    By the end of this lesson you can

    - run Bad Teacher on Carol and work out what it costs,
    - compare the shape of its outputs with retrained models using entropy and confidence,
    - explain why its own metric, ZRF, ranks it above a true retrain and why that is a red flag.

## The story

Bad Teacher (Chundawat et al., AAAI 2023) gives the student an explicit target for the forget set, which is a **second teacher with random weights**. The student copies the original (competent) teacher on part of the retain data, and the random
(incompetent) teacher on Carol, in a single epoch. This raises the lesson's key question. Does behaving like a random
model mean the same as behaving like one that never saw the data?

Lesson 09's SCRUB said "be different from the teacher on Carol" but never said how different, so it over-forgot or
relapsed, and it needed 8 epochs and a rewind. Bad Teacher promises a direction and a speed-up. For a team facing
thousands of erasure requests, a method that costs under 1% of a retrain would change everything. So it is worth
checking with care whether its target is the right one.

## What you will do

<ol class="steps" markdown>
<li markdown>**Meet the two teachers.** The original model and a freshly initialised one.</li>
<li markdown>**Untrain** with one fast epoch over 30% of \(D_r\), and count the cost.</li>
<li markdown>**Show the result** with the audit.</li>
<li markdown>**Prove it.** Compare the shape of the outputs (entropy, confidence) with retrained models.</li>
<li markdown>Check the paper's own metric (ZRF), and sweep 18 settings.</li>
</ol>

## What each step teaches

**Step 1. Two teachers.** The competent teacher is the original model, 100% right on Carol. The incompetent teacher is
the same network straight after it is created, with random weights. Seeing what each says about one of Carol's digits
makes the two targets concrete.

**Step 2. One fast epoch.** The student copies the original on 365 of the 1,217 retain digits and the random teacher
on Carol's 40. The notebook counts example-gradients, the course's unit of cost, so the price can be compared with a
retrain and with SCRUB.

**Step 3. The audit.** The same gate as Lessons 06 to 09, with FORGET, PRIVACY and UTILITY, against a band of 53.3% to
72.2% on Carol.

**Step 4. The shape of the outputs.** Accuracy reads only the top answer. Membership attacks read the whole set of
probabilities, so this step measures entropy, the probability on the true label and the top-answer confidence. It then
repeats the comparison for a whole class, where the gap is largest.

??? deep "Go deeper · step 5, ZRF and the sweep"
    ZRF, the paper's own metric, is one minus the average Jensen-Shannon divergence between the student and the random
    teacher on the forget set. Higher means closer to the random model. The step computes it for the original, a
    retrain and Bad Teacher on both requests.

    The sweep then tries three learning rates (0.0003, 0.001 and 0.003), one to three epochs and a retain fraction of
    30% or 60%. That is 3 × 3 × 2 = 18 settings, each run on Carol and on the class "3".

## Key results

<div class="stats">
<div class="is-good"><strong>0.6%</strong><span>cost of a retrain, 405 example-gradients</span></div>
<div><strong>70.0%</strong><span>Carol after one epoch, inside the band</span></div>
<div class="is-bad"><strong>96.1%</strong><span>test accuracy, just past the utility tolerance</span></div>
<div class="is-bad"><strong>0 / 18</strong><span>settings that passed on the class "3"</span></div>
</div>

**Cost.** A full retrain took 73,020 example-gradients (100%). SCRUB took 13.6%. Bad Teacher took 405 (0.6%).

The arithmetic is short. A retrain sees 1,217 digits 60 times, which is 73,020. Bad Teacher sees 365 retain digits and
Carol's 40 once each, which is 405. SCRUB's 9,896 is about twenty-four times more.

**On Carol.** 70.0% (inside the band), U-LiRA 0.150, but test accuracy 96.1%, just past the utility tolerance. A near
miss.

That is 28 of her 40 digits, and U-LiRA flags 6 of them. Test accuracy fell from the original's 98.0% to 96.1%, just under
the pass line of about 96.4%, because one pass over 30% of \(D_r\) is not quite enough to repair the side effects.

The table compares the models' outputs on Carol's digits.

| Model | Entropy | P(true label) | Top confidence |
|---|---|---|---|
| Original | 0.008 | 0.999 | 0.999 |
| Retrained (mean of 12) | 0.356 | 0.609 | 0.864 |
| Bad Teacher | 0.469 | 0.654 | 0.796 |
| Incompetent teacher | 2.192 | 0.098 | 0.182 |

Entropy runs from 0, completely sure, to about 2.30, an even guess over ten digits. **The original** is almost certain,
because it memorised Carol. **The retrains** are fairly sure, with a top confidence of 0.864, yet put only 0.609 on the
true label, so they are sometimes confidently wrong. **Bad Teacher** has higher entropy and lower top confidence than
the retrains. It has picked up some of the random teacher's uncertainty. **The incompetent teacher** is close to an
even guess.

??? checkpoint "Checkpoint 1 · An unlearnt model has an entropy of 0.36 and a top confidence of 0.86 on Carol. Another has 0.47 and 0.80. Which looks more like a model that never saw her?"
    **The first.** Retrained models average 0.356 and 0.864, so the first model matches them closely. The second matches
    Bad Teacher, which is less sure of itself than a model that never met Carol. Being less sure is not the same as
    having forgotten.

On the **class** request, a model that never saw a 3 puts essentially zero probability on "3" (6.1 × 10⁻⁷). Bad
Teacher left 0.008. Forget accuracy looked perfect (0.8%), but the privacy test read that leftover as membership and
**failed**.

Its U-LiRA member-rate on the 3s was 0.406, and test accuracy fell to 92.2%, so it failed UTILITY too. The random
teacher itself says "3" for about 12% of the 3s, and its favourite answer is "1", half the time. The student copies
those habits.

??? checkpoint "Checkpoint 2 · Bad Teacher reached 0.8% accuracy on the 3s. Why is that not a pass?"
    **The probabilities give it away.** A model that never saw a 3 puts almost nothing, 6.1 × 10⁻⁷, on the label "3".
    Bad Teacher puts 0.008 there, more than ten thousand times as much. U-LiRA reads that leftover as a sign the 3s were
    trained on, so PRIVACY fails even though the top answer is almost never "3".

**The metric trap.** The paper's ZRF score rated Bad Teacher **above the true retrain** on both requests (0.582
against 0.562 on Carol). Nothing can be more unlearnt than a model that never saw the data, so the metric measures something else.

On the class "3" the gap was larger, 0.636 against 0.527. ZRF only measures closeness to the random teacher, which is
exactly what Bad Teacher is trained to approach. A metric that grades a method on its own training goal will always
look kind to it.

**Scoreboard.** Carol 1 / 18 passes; class "3" **0 / 18**. No learning rate fixes a wrong target.

On Carol, small learning rates under-forgot and failed PRIVACY, while large ones damaged the model and failed UTILITY.
Five runs landed inside the band. Three of those failed UTILITY, one failed PRIVACY and one passed. The pass used the
largest repair budget, 60% of \(D_r\) for 3 epochs, still only about 3% of a retrain. On the class, longer runs made
forget accuracy climb back up, from 0.8% to as much as 20.3% at the same learning rate.

??? checkpoint "Checkpoint 3 · The one Carol pass used 60% of the retain set for 3 epochs. Why not use that setting for the class request too?"
    **Because the class problem is the target, not the budget.** On the class, no setting passed PRIVACY. Longer
    runs made forget accuracy rise as the student learnt the random teacher's habit of saying "3". More repair helps
    utility, but it cannot change a target of the wrong shape.

## Limits of this lesson

**One small setting.** The results come from 8 × 8 digits, one small network and two requests. Larger models may behave
differently.

**One random teacher.** The incompetent teacher is one network with one set of random weights. The class result
depends on its particular habits, such as saying "3" for about 12% of the 3s.

**Three checks, not five.** This lesson's gate has no cost check and no relearn attack. Lesson 11 adds it and finds that Bad Teacher
relearns Carol's other half in 13 steps.

**Better targets are left as tasks.** The notebook suggests replacing the random target, for example with the original
model's output with the true class removed. This lesson does not test those fixes.

## Concepts used here

- [Bad Teacher](../unlearning/bad-teacher.md)
- [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md)
- [Membership inference attacks](../unlearning/membership-inference-attacks.md)

## Notes to take

!!! notes "Notes to take"
    - **Bad Teacher.** Copy the original on 30% of \(D_r\) and a random network on \(D_f\), for one epoch.
    - **Cost.** 405 example-gradients against 73,020 for a retrain, so 0.6%.
    - **Carol.** 70.0% inside the band and U-LiRA 0.150, but test accuracy 96.1% failed UTILITY.
    - **Shape.** Entropy 0.469 against 0.356 for retrains. Too unsure, like the random teacher.
    - **Class "3".** Retrains put 6.1 × 10⁻⁷ on "3", Bad Teacher 0.008. PRIVACY failed at 0.8% accuracy.
    - **Trap.** ZRF rated it above a true retrain, 0.582 against 0.562 on Carol.
    - **Scoreboard.** Carol 1 of 18, class "3" 0 of 18. No learning rate fixes a wrong target.

## Quiz

```quiz
- q: What did Bad Teacher cost compared with a full retrain?
  options:
    - 0.6%
    - 13.6%
    - 100%
  answer: 0
  why: One epoch over 30% of the retain set is very cheap.
- q: Compared with a retrained model, Bad Teacher's outputs on Carol were...
  options:
    - Less confident (higher entropy)
    - Exactly the same
    - Much more confident
  answer: 0
  why: It learnt to behave a bit like the random teacher, not like a competent model that never met her.
- q: On the class request, why did Bad Teacher fail privacy despite 0.8% forget accuracy?
  options:
    - It left a small probability on "3", which a model that never saw 3s would not.
    - It was still 100% right on 3s.
    - The test set was empty.
  answer: 0
  why: That leftover probability looks like membership to the per-example test.
- q: ZRF rated Bad Teacher above the true retrain. What does that tell you?
  options:
    - The metric measures closeness to the random target, not unlearning.
    - Bad Teacher is better than retraining.
  answer: 0
  why: Any metric that a method can beat the gold standard on is measuring something else.
- q: How many of 18 settings passed on the class request?
  options:
    - 0
    - 9
    - 18
  answer: 0
  why: Its target is the wrong shape for a removed class, and no setting fixes that.
- q: On Carol, Bad Teacher's default run landed inside the band and passed PRIVACY. Why did it still fail?
  options:
    - It cost more than a retrain.
    - Test accuracy fell to 96.1%, just past the utility tolerance.
    - It scored 100% on Carol.
  answer: 1
  why: One pass over 30% of the retain set was not quite enough to repair the side effects on everyone else.
- q: Retrained models put 0.609 on Carol's true labels but have a top confidence of 0.864. What does the gap show?
  options:
    - They are guessing at random.
    - They still remember Carol.
    - They are often confidently wrong about her unusual digits.
  answer: 2
  why: A competent model that never met her still answers firmly, and some of those firm answers are the wrong digit.
- q: On the class request, why did longer Bad Teacher runs make forget accuracy rise again?
  options:
    - The random teacher calls some 3s "3", and the student learnt that habit.
    - The original model was restored.
    - The retain set grew.
  answer: 0
  why: A random network has favourite answers. Copying it for longer teaches the student to say "3" again.
```

## Open question → Lesson 11

!!! levelup "Level up"
    You can now price a method, read the shape of its outputs and catch a metric that marks its own homework. Next
    quest, [Lesson 11 · The unlearning audit](11-the-unlearning-audit.md), where every method faces the same five checks.

We now have nine ways to unlearn, each judged with a slightly different table. What does **one fair, repeatable audit**
look like, one we could hand to a regulator?

[On to Lesson 11, the unlearning audit :material-arrow-right:](11-the-unlearning-audit.md){ .md-button }
