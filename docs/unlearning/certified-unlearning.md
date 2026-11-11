---
title: Certified unlearning
description: A mathematical promise that an unlearnt model is almost indistinguishable from a retrained one, and how it connects to differential privacy.
---

# Certified unlearning

!!! oneline "In one line"
    **Certified unlearning** proves that the unlearnt model is *statistically almost indistinguishable* from a model
    retrained without the data, with "almost" measured by two small numbers, \(\varepsilon\) and \(\delta\).

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - say in plain words what a certificate promises and what ε and δ measure,
    - follow certified removal step by step, from training noise to the budget that forces a retrain,
    - explain why the proofs cover logistic regression but not the course's neural network.

## Why it matters

[Exact unlearning](exact-unlearning-classical.md) is always right but often expensive. [Approximate
unlearning](approximate-unlearning.md) is cheap but comes with no guarantee, so every result has to be
[audited](unlearning-audit.md). Certified unlearning sits in between. It is cheaper than retraining, and it still comes
with a proof. That proof is the closest thing the field has to a guarantee an auditor can check on paper.

The catch is that today's proofs mostly hold for **convex** models, such as logistic regression and linear models.
For deep networks they do not carry over.

Why does a proof matter so much? An audit can only say that no test it ran could tell the unlearnt model from a
retrained one. As [Can a test prove forgetting?](testing-vs-proving.md) explains, a passed test is evidence, not proof.
A certificate is different in kind. It holds against every possible test, including ones nobody has invented yet,
because it follows from how the model was made.

## A simple example

Two sealed boxes each hold a trained model. One came from retraining without Carol. The other came from unlearning
her. A referee opens both and runs any test they like. With certified unlearning, the referee can do *only slightly
better than guessing* at which box is which. \(\varepsilon\) says how slightly, and \(\delta\) is a tiny chance that
the promise fails.

!!! simply "Explain it simply"
    Retraining is like baking a fresh cake without one ingredient. Certified unlearning is like scraping that
    ingredient out of the old cake, then dusting the top with icing sugar so nobody can see the scrape marks. The proof
    says how thick the dusting must be so that no taster can reliably tell the two cakes apart.

The icing sugar is the key idea. The unlearning step is never perfect, so there is a small leftover error. Random
noise added during training is what hides it. Without the noise, a careful referee could spot the error. With enough
noise, the error is lost among the normal random differences between models.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Certified unlearning](../start-here/glossary.md#c) | A proof that the unlearnt model is almost impossible to tell apart from a retrained one | Certified removal for logistic regression |
| ε (epsilon) | How much better than guessing the best possible referee can do. Smaller is stronger | 0 would mean no test can tell at all |
| δ (delta) | A tiny chance that the promise fails completely | The second number on every certificate, next to ε |
| Distribution of models | The spread of models a random training process could produce | The 20 retrains of Lesson 06 are samples from one |
| Convex | A loss shaped like a single bowl, so there is one best answer | Logistic regression, not a neural network |
| [Newton step](../start-here/glossary.md#n) | A jump to the estimated new best weights, using the gradient and the curvature | One step removed Alice in Lesson 12 |
| Residual gradient | How far the new weights are from being the best fit on the data that remains. This is the leftover error | 1.49e-03 for Alice after one step |
| Noise budget | The total leftover error the training noise can hide. Every deletion spends some | 0.527 spent over a year of requests in Lesson 20 |
| [Differential privacy](../start-here/glossary.md#d) | A training promise that the model barely changes whether or not any one record is in the data | A DP-trained model is already certified for one record |

## How it works

### The promise in symbols

In plain words, the promise compares two random processes. One is "train on everything, then unlearn". The other is
"retrain on what is left". Each could produce many different models, because training is random. The promise says
that any kind of model, or any test result, is almost equally likely to come out of either process. ε caps how much
more likely, as a ratio. δ allows a tiny chance of a bigger difference.

??? deep "Go deeper · the definition and what ε means in numbers"
    Let \(A\) be the training algorithm and \(U\) the unlearning method. Training is random (starting weights, batch order,
    added noise), so both give a *distribution* of models. Unlearning is \((\varepsilon, \delta)\)-certified if, for every
    set of possible models \(S\),

    \[
    P\big[U(A(D), D, D_f) \in S\big] \le e^{\varepsilon}\, P\big[A(D_r) \in S\big] + \delta ,
    \]

    and the same holds with the two sides swapped. Small \(\varepsilon\) and \(\delta\) mean the two distributions are close.

    The factor \(e^{\varepsilon}\) is what makes ε readable. With \(\varepsilon = 0.1\), \(e^{0.1} \approx 1.1\), so no
    outcome is more than about 10% more likely from unlearning than from retraining. With \(\varepsilon = 1\), the factor
    is about 2.7. With \(\varepsilon = 10\), it is about 22,000, which promises very little.

    The promise is about **sets** \(S\), which can be any test result at all, such as "the membership attack says
    Carol was in". That is why it covers every possible audit at once.

### Certified removal, step by step

The best-known recipe is certified removal (Guo et al. 2019). It has five steps.

1. **Train with noise.** Add a small random term to the training loss, then train to the exact best fit. The noise is
   drawn at random and kept secret. **For a deletion this means** every model already carries a random
   offset that a referee cannot predict.
2. **Delete with one Newton step.** Remove the person's rows and take one Newton step on the data that remains, as in
   [Influence functions](influence-functions.md). **This means** the weights jump almost exactly to the retrained
   answer.
3. **Measure what is left.** Compute the residual gradient on the remaining data. It is small but not zero, and it is
   the leftover error. **This means** you know exactly how imperfect the step was.
4. **Spend from the budget.** The training noise can hide only so much error in total. Add this deletion's leftover
   to the running total. **This means** each deletion costs part of a fixed allowance.
5. **Retrain when it runs out.** Once the total would be too large for the noise to hide, train a fresh model on what
   is left, with fresh noise. **This means** the promise survives, and the budget starts again.

??? checkpoint "Checkpoint 1 · A team takes a Newton step to delete a user from logistic regression, but trained without any added noise. Is the result certified?"
    **No.** The Newton step leaves a small residual error, and nothing hides it. A careful referee could in principle
    spot it. The step may be very accurate, but the certificate comes from the noise added at training time, not from
    the step alone.

### Three recipes

| Recipe | Idea | Works for | Source |
|---|---|---|---|
| **Certified removal** | Train with a small random term added to the loss. To delete, take one Newton step that removes the point's influence. The noise hides the small error left over. | Convex models such as logistic regression | Guo et al. 2019 |
| **Descent-to-delete** | After a deletion, take a few gradient steps from the current model, then add Gaussian noise before releasing it. | Convex models, many deletions in a row | Neel et al. 2021 |
| **Deletion capacity** | Count how many deletions a method can absorb before accuracy drops, then retrain. | Convex models | Sekhari et al. 2021 |

Each recipe has a **budget**. Every deletion uses some of it, and once the leftover error would break the promise,
you must retrain. So certified unlearning postpones retraining; it does not abolish it.

## A worked example, Alice and a year of requests

Lessons 02, 12 and 20 measure the leftover error that certified removal must hide. Follow it from one person to a
whole year.

1. **Carol on digits (Lesson 02).** Removing her 40 unusual digits from logistic regression left a residual gradient
   of 12.5 at the old weights. One Newton step brought it down to 1.21, and a second to 0.0313. Big, unusual deletions
   leave a lot to correct.
2. **Alice on income data (Lesson 12).** Alice is one high-earning woman among about 21,000 people. Before the step,
   the residual gradient on the remaining data was 2.18. After one Newton step it was 0.00149.
3. **How close Alice's step got.** The largest weight difference from an exact retrain was 2.2e-06, against 2.9e-03
   between the original and the retrain. The model's estimate that Alice earns more than $50K went from 0.3180 to
   0.3163, the same as the retrained model.
4. **A year of requests (Lesson 20).** 104 users were removed in 26 batches, one Newton step per batch. Each step's
   leftover gradient stayed small, between about 0.003 and 0.04 in the steps shown, and the largest weight gap to an
   exact refit among them was 0.00165.
5. **The bill.** Adding up every step's leftover gives the budget used over the year, 0.527. The error did not pile
   up in the weights, because each step also corrects the last. But the budget did pile up, because each step's
   leftover had to be hidden.

<div class="stats">
<div class="is-good"><strong>2.2e-06</strong><span>largest weight gap between Alice's Newton step and a retrain</span></div>
<div><strong>0.00149</strong><span>residual gradient after Alice's step, down from 2.18</span></div>
<div class="is-bad"><strong>0.527</strong><span>noise budget used by 26 batches of deletions in a year</span></div>
<div class="is-bad"><strong>57.8 GB</strong><span>the Hessian the course's network would need, at 8 bytes a number</span></div>
</div>

The last tile is why certified removal stops at linear models. A Newton step needs the Hessian, a table with one row
and one column per weight. For 650 weights it takes 3.4 MB. For the course's network, with 85,002 weights, it would
need 57.8 GB at 8 bytes a number (29 GB at 4), and for a model with a billion weights about 8 billion GB at
8 bytes.

??? checkpoint "Checkpoint 2 · Suppose the training noise in Lesson 20 could hide a total leftover of 0.4. What happens before the year is out?"
    **The budget runs out, so the model must be retrained.** The year's 26 batches used 0.527 in all, more than 0.4.
    Somewhere before the last batch the running total crosses the limit. At that point you train a fresh model with
    fresh noise on the data that remains, and the budget starts again. This is why a team using certified removal
    plans its full retrains in advance.

### The link to differential privacy

[Differential privacy](https://en.wikipedia.org/wiki/Differential_privacy) (DP) uses the same \((\varepsilon, \delta)\)
promise, but for training. A DP-trained model behaves almost the same whether or not any one record was in the data.
That means **doing nothing** already counts as certified unlearning of one record. For a group of \(k\) records the
guarantee weakens, roughly to \(k\varepsilon\).

The price is accuracy. The noise that makes a model private also makes it less accurate, especially for rare examples,
which are exactly the ones a model tends to [memorise](../ml-basics/overfitting-and-memorisation.md).

Think about Carol under DP. Her 40 digits are a group of 40 records, so the promise for her is roughly 40 times
weaker than for one digit. And because her digits are unusual, they are exactly what DP training would learn least
well. DP protects her by making the model worse on people like her.

??? deep "Go deeper · certified removal and DP side by side"

    | | Certified removal | Differential privacy |
    |---|---|---|
    | What the noise hides | The leftover error of each deletion | Every single record, from the start |
    | What happens at a deletion | One Newton step, then spend from the budget | Nothing, for one record |
    | Covers | Convex models | Any model, including networks |
    | Main cost | A scheduled full retrain | Lower accuracy, worst on rare examples |
    | Group of k records | Each record spends budget | The promise weakens to about \(k\varepsilon\) |

    The rows show why the two ideas are often mixed up. Both promise that a model is hard to tell apart from one
    trained without some data, with the same ε and δ. The difference is when the work is done. DP pays up front for
    every record. Certified removal pays a little at each deletion.

## Limits

**The proofs need one best answer.** A convex loss has a single bowl, so "the" retrained model is well defined and a
Newton step can aim at it. A network has many equally good sets of weights, so the proofs do not carry over.

**The Hessian grows with the square of the weights.** Double the weights and the Hessian needs four times the memory.
Lesson 20 measured one step at 0.006 seconds for 650 weights and 0.275 seconds for 3,850.

**The noise costs accuracy.** More noise allows more deletions before a retrain, but makes every model a little worse.

**A proof covers the method, not the code.** The certificate assumes the method was implemented and run as written.
An audit still helps catch a bug, a wrong dataset or a skipped step.

??? checkpoint "Checkpoint 3 · A vendor says their deep network unlearning method is certified, because they used the certified removal recipe. What do you check?"
    **Whether the proof applies at all.** Certified removal assumes a convex model with one best answer, and it needs a
    Hessian, which a deep network cannot hold. Ask which theorem covers their model, what ε and δ are, how the budget
    is tracked and when they retrain. Without that, treat it as approximate unlearning and audit it.

!!! tip "What to do in practice"
    - Use certified removal for linear and logistic models, where the Newton step is cheap.
    - Record ε, δ, the noise and the running budget for every deletion, and schedule the full retrain before it runs out.
    - Treat a smaller ε as stronger, and question any certificate with an ε near 10.
    - For deep networks, use exact methods such as [SISA](sisa.md) or retraining, or audit an approximate method.

## Common mistakes

!!! danger "Mistakes people make"
    - **Using a convex proof on a deep network.** The guarantees assume one best answer. Neural networks have many, so
      the proof no longer holds.
    - **Forgetting the budget.** After enough deletions the leftover error adds up; the method must retrain to keep its
      promise.
    - **Reading \(\varepsilon\) as "percent forgotten".** It bounds how distinguishable two distributions are. A large
      \(\varepsilon\), such as 10, promises very little.
    - **Skipping the noise.** The Newton step alone is not certified. The randomness is what hides the error.
    - **Confusing small weight gaps with a certificate.** Alice's step landed within 2.2e-06 of the retrain, but the
      promise comes from the noise and the budget, not from that number.

## Key takeaways

!!! notes "Notes to take"
    - **Certified unlearning.** A proof that the unlearnt model is almost impossible to tell apart from a retrain.
    - **ε and δ.** ε caps how much better than guessing any referee can do, δ is a tiny chance of failure.
    - **Certified removal.** Train with noise, delete with one Newton step, hide the leftover with the noise.
    - **The budget.** Every deletion spends some. Lesson 20's year used 0.527. When it runs out, retrain.
    - **Alice.** One Newton step, weight gap 2.2e-06 from a retrain, residual gradient 0.00149.
    - **Convex only.** The course's network would need a 57.8 GB Hessian, and the proofs assume one best answer.
    - **DP link.** A DP-trained model is already certified for one record, weaker for a group, at a cost in accuracy.
    - **Trap.** No noise, no certificate, however close the Newton step lands.

## Quiz

```quiz
- q: What does certified unlearning promise?
  options:
    - The unlearnt model is identical to the retrained model.
    - The unlearnt model is statistically almost indistinguishable from a retrained one.
    - The forget set accuracy drops to 0%.
  answer: 1
  why: Identical is exact unlearning. Certified unlearning allows a small, bounded difference, measured by epsilon and delta.
- q: For which models do today's certified unlearning proofs mostly hold?
  options:
    - Convex models such as logistic regression
    - Large language models
    - Any neural network
  answer: 0
  why: The proofs rely on a single best answer, which convex models have and deep networks do not.
- q: Why does certified removal add random noise?
  options:
    - To speed up training
    - To hide the small error left after the Newton step
    - To make the model more accurate
  answer: 1
  why: The deletion step is only approximately right. The noise makes the leftover difference statistically invisible.
- q: A model was trained with differential privacy. What happens when one person asks to be forgotten?
  options:
    - It must always be retrained from scratch.
    - Doing nothing already meets a certified guarantee for that one record.
    - Differential privacy has nothing to do with unlearning.
  answer: 1
  why: DP already bounds how much any single record can change the model, which is the same promise.
- q: Why must a certified removal system still schedule full retrains?
  options:
    - Newton steps stop working after a week.
    - Each deletion spends part of a fixed noise budget, and when it runs out the promise would break.
    - The law requires a retrain every month.
  answer: 1
  why: In Lesson 20 a year of deletions used 0.527 of budget. Retraining with fresh noise starts the budget again.
- q: A certificate has ε = 10. What does that mean?
  options:
    - It promises very little, because outcomes can be thousands of times more likely from one process than the other.
    - The model forgot 10% of the data.
    - It is ten times stronger than ε = 1.
  answer: 0
  why: The promise allows a factor of e to the power ε, which for 10 is about 22,000. Smaller ε is stronger.
- q: Why does certified removal not work for the course's neural network?
  options:
    - Networks cannot be trained with noise.
    - Networks have no gradients.
    - It assumes one best answer and needs a Hessian, which for this network would take 57.8 GB.
  answer: 2
  why: A network has many equally good sets of weights, and its Hessian grows with the square of the number of weights.
- q: Under DP, how does the promise change for Carol's 40 digits compared with one digit?
  options:
    - It becomes stronger.
    - It weakens roughly to 40 times ε.
    - It stays the same.
  answer: 1
  why: Group privacy weakens with the size of the group, roughly to k times ε for k records.
```

## Try it

!!! levelup "Level up"
    You can now read a certificate, say what ε and δ promise and know when the proof does not apply. Next quest,
    [Quick fixes and their traps](approximate-unlearning.md), where networks are edited with no proof at all.

- Read [exact unlearning for classical models](exact-unlearning-classical.md), where the Newton step first appears.
- Run [Lesson 02](../lessons/02-linear-and-logistic-regression.md) and compare its one-step update with retraining.
