---
title: Influence functions
description: Estimate how much one training example shaped a model, and what removing it would change, without retraining.
---

# Influence functions

!!! oneline "In one line"
    An **influence function** estimates how much one training example changed a model, and so roughly what removing it
    would do, without retraining.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain the two ingredients of influence, an example's pull and how firmly the other data holds the weights,
    - follow one Newton step that unlearns Carol from logistic regression and read how close it got,
    - say where influence estimates can be trusted and where they cannot.

## Why it matters

Before you forget someone, it helps to know how much they mattered. Influence tells you which training examples a
prediction leans on, which people a model has [memorised](../ml-basics/overfitting-and-memorisation.md), and which
deletions will be cheap or costly. The same calculation also gives a one-step way to *unlearn*, because it is the Newton
step behind [certified unlearning](certified-unlearning.md).

It also explains a lot of the course in one idea. The exact downdate for ridge regression, the one-step unlearning of
logistic regression and gradient ascent on a network are all the same move with more or less information. Knowing the
full version makes it clear what each shortcut throws away.

## A simple example

A class average is easy to update. If one student's score is removed, you know exactly how the average moves. A model
is a far more tangled "average" of its training data, so the effect of removing one example cannot be read off directly.
An influence function estimates it with calculus instead of recomputing everything.

!!! simply "Explain it simply"
    Think of a tent held up by many ropes. Cut one rope and the tent shifts. How far it shifts depends on two things.
    How hard that rope was pulling, and how firmly all the other ropes hold the tent in that direction. Influence
    multiplies the two.

Now map the tent onto a model. The tent's position is the model's **weights**. Each rope is one training example. How
hard a rope pulls is the example's **gradient**. How firmly the other ropes hold the tent is the **curvature** of the
loss, which the maths calls the **Hessian**. Carol's thick-marker digits are ropes pulling in an unusual direction,
where few other ropes push back, so cutting them moves the tent a long way.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Influence function](../start-here/glossary.md#i) | An estimate of how much one training example shaped a model, made without retraining | The effect of Carol's 40 digits on logistic regression |
| [Gradient](../start-here/glossary.md#g) | For one example, the direction in which it pulls the weights | The pull of each of Carol's digits |
| [Hessian](../start-here/glossary.md#h) | A table of the loss's curvature, with one row and one column per weight. It says how firmly the data holds each direction | 650 × 650 for the course's logistic regression |
| [Newton step](../start-here/glossary.md#n) | A jump to the estimated new best weights, using the gradient and the Hessian | One step closed 94.8% of the gap to the retrained model |
| Self-influence | How much an example shapes the model's answer on that same example | High for memorised digits like Carol's |
| [Leverage](../start-here/glossary.md#l) | The exact self-influence of a point in a linear model | Carol's digits average 0.116, others 0.039 |
| Convex | A loss shaped like a single bowl, so there is one best answer | Ridge and logistic regression, but not a network |
| Damping | A small number added to the Hessian so that it can be inverted. It changes the answer a little | Used in practice for networks |
| Residual gradient | How far the new weights are from being the best fit on the data that remains | 12.5 before the Newton step, 1.21 after one |

## How it works

### The formula

Train a model to the weights that minimise its average loss. At that point the pulls of all the examples balance out,
so the model sits still. Now remove one example. Its pull disappears, the balance breaks and the weights move.

The influence function estimates that move in three steps.

1. **The pull.** Take the gradient of the removed example's loss. It says which way that example was pulling the
   weights.
2. **The resistance.** Take the Hessian of the total loss. It says how firmly the other examples hold the weights in
   each direction.
3. **The move.** Divide the pull by the resistance, and scale it by one over the number of examples. A strong pull in
   a direction nobody else holds gives a big move. A pull in a well-held direction gives a small one.

To see the effect on a single prediction instead of on the weights, take that move and ask how much it changes the
loss on one test example. A large value means the removed example strongly shapes that prediction. This is the
approach of Koh and Liang 2017.

??? deep "Go deeper · the formula in symbols"
    Train a model to the weights \(\hat\theta\) that minimise the average loss over \(n\) examples. Removing one example
    \(z\) moves the weights by approximately

    \[
    \hat\theta_{-z} - \hat\theta \approx \frac{1}{n} H^{-1} \nabla_\theta L(z, \hat\theta),
    \]

    where \(\nabla_\theta L(z, \hat\theta)\) is the gradient of that example's loss (which way it pulls the weights) and
    \(H\) is the Hessian, the curvature of the total loss (how firmly the other examples hold the weights in place).

    To see the effect on a test example \(z_{\text{test}}\), combine the two.

    \[
    \mathcal{I}(z, z_{\text{test}}) = -\nabla_\theta L(z_{\text{test}}, \hat\theta)^{\top} H^{-1} \nabla_\theta L(z, \hat\theta).
    \]

    For unlearning a whole forget set at once, Lesson 02 uses the same idea as a Newton step on the retain set.
    At the old optimum the full gradient is zero, so the gradient on the retain set is minus the sum of the forget
    set's gradients. One step \(w_u = w - H_r^{-1} \nabla L_r(w)\) then jumps towards the retain-only optimum.

??? checkpoint "Checkpoint 1 · Two training digits pull on the weights equally hard. One looks like hundreds of others, the other is unusual like Carol's. Which one has more influence?"
    **The unusual one.** Its pull points in a direction that few other examples hold, so the curvature there is small
    and dividing by it gives a big move. The typical digit's pull is resisted by all the digits like it. This is why
    Carol's leverage in Lesson 02 was about three times that of a typical digit.

### Where it works, and where it does not

| Model | How good is the estimate? | Notes |
|---|---|---|
| Ridge and logistic regression | Close | One best answer, so the maths holds; for ridge, the exact [downdate](exact-unlearning-classical.md) is just as cheap |
| Small neural networks | Rough | The Hessian is huge and the loss has many minima; estimates can be [fragile](https://arxiv.org/abs/2006.14651) (Basu et al. 2021) |
| Large models | Approximate methods only | Scalable versions such as TRAK (Park et al. 2023) and EK-FAC for language models (Grosse et al. 2023) trade accuracy for speed |

Each row is about how well the two ingredients survive. For ridge regression the loss is a perfect bowl, so the
estimate is exact, and Lesson 02 showed that one Newton step gives the same weights as the exact downdate, to within
about 1e-13. For logistic regression the bowl is only nearly perfect, so the estimate lands close. For a network there
is no single bowl, and the Hessian is too big to hold. Lesson 08 put it at 29 GB in 32-bit floats for the course's small network, and a
model with a billion weights would need about \(10^{18}\) entries.

## A worked example, forgetting Carol from logistic regression

Lesson 02 uses the influence idea to unlearn all 40 of Carol's digits from logistic regression in one step.

1. **The original.** The model is trained to its exact best fit in 7 Newton iterations. It scores 92.5% on Carol,
   77.5% on other unseen thick-marker digits and 97.2% on the test set. The gap between her digits and others like
   them is the memory to remove.
2. **The target.** A model refitted without her scores 62.5% on Carol, 57.5% on unseen thick digits and 97.0% on test.
3. **The pull.** With Carol gone, the old weights are no longer the best fit on what remains. The residual gradient,
   which is the sum of the pulls her digits used to supply, is 12.5.
4. **One step.** Divide that pull by the curvature of the remaining data and jump. It takes 6.0 ms, against 40.7 ms
   for a full refit.
5. **The result.** Carol drops to 60.0%, one digit short of the refit's 62.5%. Unseen thick digits and test accuracy
   match the refit exactly, at 57.5% and 97.0%.
6. **How close.** The distance to the refitted weights shrank by 94.8%. A second step closed 99.9% and a third
   closed 100.0%.

The step is approximate, but the error is something you can measure, and here it is small. That habit of measuring the
distance to a model that never saw the data runs through the rest of the course.

<div class="stats">
<div class="is-good"><strong>94.8%</strong><span>of the gap to the refit closed by one Newton step</span></div>
<div><strong>60.0%</strong><span>Carol after one Newton step, against 62.5% after a full refit</span></div>
<div><strong>0.116</strong><span>average leverage of Carol's digits, against 0.039 for everyone else</span></div>
<div class="is-bad"><strong>8%</strong><span>of the gap closed by gradient ascent, which drops the Hessian</span></div>
</div>

The last tile comes from Lesson 08. Gradient ascent is the same step with the Hessian replaced by a guessed step size.
On the same logistic regression, its best guess closed only 8% of the gap. The curvature is most of the answer.

??? checkpoint "Checkpoint 2 · After one Newton step Carol scored 60.0%, and the refitted model 62.5%. Has she been exactly unlearnt?"
    **No, but nearly.** The weights closed 94.8% of the distance to the refit, not all of it, so this is approximate
    unlearning. You can measure the remaining gap, and a second step closes 99.9%. For a guarantee rather than an
    estimate, [certified unlearning](certified-unlearning.md) adds noise during training to hide the small error left.

### What people use it for

- **Auditing.** Find the training examples behind a surprising prediction.
- **Finding memorised people.** An example with huge self-influence is probably memorised, and is a likely target for
  [membership inference](membership-inference-attacks.md).
- **Triage.** Estimate which deletion requests will barely change the model and which will change it a lot.
- **A fast unlearning step.** Apply the weight change above for each forgotten example, then check the result.

Carol shows the second use clearly. Her digits have about three times the leverage of a typical digit, so a linear
model bends towards them. That is the classical fingerprint of memorisation, and it is why Carol, not a random user,
is the hard case throughout the course.

## Limits

**It is a local estimate.** The influence function assumes the weights move only a little, so the loss looks like a
bowl near them. Removing many examples, or very influential ones, can move the weights further than the estimate
allows. For Carol, one step left 5.2% of the gap.

**It needs a Hessian you can invert.** That is easy for 650 weights and impossible for millions. Scalable versions
approximate the Hessian, which costs accuracy.

**It assumes one best answer.** A network has many equally good sets of weights, and training lands on one by chance.
The estimate then describes a move near the current weights, not the model a real retrain would find.

**It is not a test.** A small influence score is an estimate, not evidence. A deletion still has to be checked against
models that never saw the data, as in [The unlearning audit](unlearning-audit.md).

??? checkpoint "Checkpoint 3 · A team says a user's influence score on their deep network is tiny, so there is nothing to unlearn. What do you say?"
    **That is not enough.** Influence estimates in deep networks are rough and can be fragile (Basu et al. 2021), so a
    tiny score may simply be wrong. Even a correct small score describes one estimate, not what an attacker can find.
    The deletion still has to be done and then audited, for example with a membership test.

!!! tip "What to do in practice"
    - Use influence on convex models with confidence, and measure the gap to a refit when you can.
    - On a network, use influence to find likely memorised examples and to triage requests, not to prove forgetting.
    - Report any damping you add, because it changes the answer.
    - Check every influence-based unlearning step with an audit.

## In code

??? deep "Go deeper · leverage and the Newton step in the course library"
    ```python
    import numpy as np
    from mul import lab, classical
    L = lab.make_lab("carol")

    ridge = classical.RidgeUnlearner(lam=1.0).fit(L.X_train, np.eye(10)[L.y_train])   # one-hot targets
    h = ridge.leverage(L.X_train)          # self-influence of every training point
    print(h[L.forget_idx].mean(), h[L.retain_idx].mean())                # 0.116 vs 0.039

    logreg = classical.SoftmaxNewton(lam=1.0).fit(L.X_train, L.y_train)
    unlearnt = logreg.unlearn_newton(L.Xr, L.yr, steps=1)              # one influence step
    print(unlearnt.grad_norm(L.Xr, L.yr))  # the residual gradient, about 1.21 after one step
    ```

    Leverage is \(x^\top (X^\top X + \lambda I)^{-1} x\), the ridge version of self-influence. The residual gradient
    is the quantity that [certified unlearning](certified-unlearning.md) bounds.

## Common mistakes

!!! danger "Mistakes people make"
    - **Trusting deep-network influence scores as exact.** They are estimates, and they can be unstable.
    - **Inverting a Hessian that is not invertible.** In practice people add a small damping term, which changes the
      answer.
    - **Treating low influence as proof of forgetting.** Influence estimates one example's effect. It is not an audit.
    - **Dropping the curvature and keeping the name.** A gradient step without the Hessian is gradient ascent, which
      closed 8% of the gap where the Newton step closed 94.8%.

## Key takeaways

!!! notes "Notes to take"
    - **Influence function.** An estimate of one example's effect on a model, made without retraining.
    - **Two ingredients.** The example's gradient (its pull) and the Hessian (how firmly the rest holds the weights).
    - **Unusual data matters most.** Carol's leverage was 0.116, against 0.039 for others.
    - **One Newton step.** Unlearnt Carol from logistic regression, 94.8% of the gap closed, 60.0% against 62.5%.
    - **Ridge.** The Newton step is exact and equals the Sherman-Morrison downdate.
    - **Networks.** No usable Hessian (29 GB in 32-bit floats even for the toy), so estimates are rough and fragile.
    - **Without the Hessian.** You get gradient ascent, which closed only 8%.
    - **Uses.** Auditing predictions, finding memorised people, triage and a fast unlearning step.
    - **Trap.** A low influence score is not proof of forgetting.

## Quiz

```quiz
- q: What does an influence function estimate?
  options:
    - How long training takes
    - How much one training example changed the model
    - The size of the test set
  answer: 1
  why: It approximates the effect of removing (or up-weighting) a single example, without retraining.
- q: Which two ingredients does the influence formula combine?
  options:
    - The example's gradient and the Hessian of the loss
    - The learning rate and the batch size
    - The accuracy and the loss
  answer: 0
  why: The gradient says which way the example pulls; the Hessian says how firmly the rest of the data holds the weights.
- q: For which models are influence estimates most reliable?
  options:
    - Convex models such as logistic regression
    - Very deep networks
    - Language models
  answer: 0
  why: Convex models have one best answer, which the maths assumes. Deep networks break that assumption.
- q: An example has very high self-influence. What does that suggest?
  options:
    - It was probably memorised.
    - It was never used in training.
    - The model is underfitting.
  answer: 0
  why: If the model's fit to an example depends heavily on that example alone, the model has likely memorised it.
- q: One Newton step unlearnt Carol from logistic regression. How close did it get to a refit without her?
  options:
    - It made no difference.
    - It closed 94.8% of the distance, and a second step closed 99.9%.
    - It matched the refit exactly in one step.
  answer: 1
  why: Logistic regression's loss is only nearly a perfect bowl, so one step lands close, and more steps converge.
- q: Why is the Newton step exact for ridge regression but not for logistic regression?
  options:
    - Ridge has fewer training examples.
    - Logistic regression has no gradient.
    - Ridge's loss is a perfect bowl, so the curvature describes it exactly.
  answer: 2
  why: For ridge, one Newton step gives the same weights as the exact downdate. For logistic regression the bowl is only approximate.
- q: Why do Carol's digits have about three times the leverage of a typical digit?
  options:
    - They pull in an unusual direction that few other digits hold, so the model bends towards them.
    - There are more of them than any other user's digits.
    - They were added to training last.
  answer: 0
  why: Influence divides the pull by the resistance. Unusual data meets little resistance.
- q: What happens if you drop the Hessian from the influence step and use a guessed step size instead?
  options:
    - The step becomes exact.
    - You get gradient ascent, which closed only 8% of the gap on the same model.
    - Nothing changes.
  answer: 1
  why: The curvature is what turns the raw pull towards the retrained model. Without it the direction is wrong.
```

## Try it

!!! levelup "Level up"
    You can now explain what one example does to a model and why unusual data is the hard case. Next quest,
    [Erasure requests and fairness](fairness-and-erasure.md), where many people from one group ask to be forgotten and
    the question becomes whether the model stays fair to that group.

- Read [certified unlearning](certified-unlearning.md), which turns this weight change into a guarantee.
- Run [Lesson 02](../lessons/02-linear-and-logistic-regression.md) and compare the one-step update with retraining.
