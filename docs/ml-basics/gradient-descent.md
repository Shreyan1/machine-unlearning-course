---
title: Gradient descent
description: How a model improves by taking many small steps downhill on the loss, and why that spreads each example across every weight.
---

# Gradient descent

!!! oneline "In one line"
    Gradient descent improves a model by nudging its weights, step by step, in the direction that makes the loss smaller.

!!! mission "Your mission · about 14 minutes · 3 checkpoints"
    By the end of this page you can

    - work through a few steps of gradient descent by hand and see what the learning rate does,
    - count how many steps the course's network takes and how often it meets Carol's digits,
    - explain why the path of training spreads Carol across 94.1% of the weights, and why running it backwards is risky.

## Why it matters

Almost every modern model, from small neural networks to large language models, is trained with gradient descent. Many
unlearning methods are built from it too. **Gradient ascent**, for example, runs it backwards to make the model *worse*
on the forget set. To understand those methods, you first need the forward version.

Gradient descent also explains *why* unlearning is hard. A model trained this way is not built in one go from a
formula. It is the end point of a long walk, and every step of the walk depended on the steps before it, Carol's
digits included. In Lesson 04, a network trained without Carol, from exactly the same start, ends up with 94.1% of its
85,002 weights different. That one fact, which comes from how gradient descent works, is why the course needs
everything that follows.

## A simple example

Imagine you are on a hill in thick fog and want to reach the bottom of the valley. You cannot see far, but you can feel
the slope under your feet. So you take a small step in the steepest downhill direction, feel the slope again and
repeat. Eventually you reach low ground.

- Your **position** is the model's weights.
- The **height** is the loss.
- The **slope** is called the **gradient**.
- The **size of each step** is called the **learning rate**.

!!! simply "Explain it simply"
    Now imagine a friend walked the same hill but took one wrong turn near the start, because a rock moved under
    their foot. Every step after that starts from a slightly different place, so they end in a different spot in
    the valley. Carol's digits are that rock. Leaving them out changes the whole walk, not just one step.

The picture has one more lesson. The hillside of a real network has many valleys, all about as low as each other. Two
walkers who start in different places usually end in different valleys, and both have reached good low ground. So
"the bottom of the hill" is not one place.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Gradient](../start-here/glossary.md#g) | The direction in which each weight should move to increase the loss | One number for each of the network's 85,002 weights |
| Learning rate \(\eta\) | How big each step is | 0.001 in the course's training recipe |
| Mini-batch | A small group of examples used for one step | 64 digits at a time |
| [Epoch](../start-here/glossary.md#e) | One pass over all the training data | The network trains for 60 epochs |
| Random seed | A starting number that decides the first weights and the order of the batches | The same seed gives the same model, bit for bit |
| Adam | A popular form of gradient descent that gives each weight its own step size | The optimiser the course library uses to train its networks |
| [Gradient ascent](../start-here/glossary.md#g) | Stepping uphill on the loss of the forget set, to make the model worse on it | The simplest quick fix tried in Lesson 08 |
| [Newton step](../start-here/glossary.md#n) | A jump that also uses the curvature of the loss, not just its slope | One step closed 95% of the gap in Lesson 08's logistic regression |

## How it works

<!-- diagram: gradient-descent -->

The curve in the figure shows how wrong the model is for each value of one weight. The yellow dots are where the
model sits after each step, and the arrows are the steps. Near the top the slope is steep, so the steps are long.
Near the bottom the slope flattens, so the steps shrink, until the model rests at the green dot, the lowest loss. A
real network does the same thing in 85,002 directions at once.

<ol class="steps" markdown>
<li markdown>**Start** with random weights.</li>
<li markdown>**Pick a small batch** of training examples (say 64). This is called a *mini-batch*.</li>
<li markdown>**Measure the loss** on that batch, and work out the **gradient**, which says which way each weight should move to reduce it.</li>
<li markdown>**Take a small step.** Move every weight a little in the downhill direction.</li>
<li markdown>**Repeat** with the next batch. One pass over all the training data is called an **epoch**.</li>
</ol>

**For Carol this means** her digits are mixed into the batches like everyone else's. Whenever one of her digits is in
a batch, its loss adds to the gradient, so that step moves every weight a little towards fitting her.

In symbols, one step of gradient descent looks like this.

\[
w \leftarrow w - \eta \, \nabla L(w)
\]

Where \(w\) are the weights, \(\eta\) (eta) is the learning rate and \(\nabla L(w)\) is the gradient of the loss.

The minus sign is the whole idea. The gradient points uphill, so subtracting it moves the weights downhill. The
learning rate scales the step. Too small and training crawls. Too large and each step jumps past the bottom and lands
higher up on the other side.

??? checkpoint "Checkpoint 1 · One weight is 2.0, its gradient is 4.0 and the learning rate is 0.1. What is the weight after one step, and did the loss go up or down?"
    **1.6, and the loss went down (for a small enough step).** The new weight is \(2.0 - 0.1 \times 4.0 = 1.6\). A
    positive gradient means the loss rises as the weight grows, so the step makes the weight smaller. If the learning
    rate were much bigger, the step could overshoot the bottom and raise the loss instead.

### Why this makes unlearning hard

Every step starts from where the last step ended. So if Carol's digits were in an early batch, every later step was
taken from a slightly different place. Her influence is not stored in one spot; it is carried along the whole path. That
is why, in Lesson 04, removing Carol changes **94.1%** of the network's weights.

Lesson 04 checks this carefully. It trains two networks from the same seed, so they start with the same weights and
see the batches in the same order. The only difference is that one of them never sees Carol. At the end, 94.1% of
the weights differ, and 87.4% differ by more than 0.001. There is no small set of "Carol weights" to find and undo.

### Many valleys, not one

The same lesson trains a third network on exactly the same data as the first, Carol included, but from seed 1 instead
of seed 0. That changes only the starting weights and the order of the batches. The two models score 98.0% and 98.7%
on the test digits, so both are good. Yet they are far apart.

| Pair of networks | Distance between their weights |
|---|---|
| Same seed, with and without Carol | 9.87 |
| Same data, seed 0 against seed 1 | 50.96 |

Two equally good networks on the same data are about five times further apart (50.96 ÷ 9.87 is about 5.2) than the effect of removing Carol. So
there is no single right set of weights to aim for. This is why the course judges forgetting by **behaviour**, against
several retrained models, as [the gold band](../unlearning/gold-band.md) explains.

??? deep "Go deeper · why there is no single valley"
    The loss of a network, seen as a function of all 85,002 weights, is **non-convex**. That means it has many dips,
    not one bowl. A convex model, such as the logistic regression of Lesson 02, has one best answer. There, Newton's
    method reached it in 7 steps, with the gradient at the end about \(6 \times 10^{-14}\), which is zero up to
    rounding.

    For a network there is no such single answer. Random starting weights and a random batch order decide which dip
    the walk ends in. That is also why identical retrains disagree. In Lesson 06, 20 networks retrained without Carol
    with different seeds scored anywhere from 47.5% to 70.0% on her digits.

    The seed itself is fully under control. The course library's `set_seed` fixes both the first weights and the
    batch order, so the same seed on the same data gives a bit-for-bit identical model. That is what lets Lesson 04
    compare "with Carol" and "without Carol" fairly.

### Running it backwards (gradient ascent)

If you step **uphill** on the forget set instead (\(w \leftarrow w + \eta \nabla L_f(w)\)), the model gets worse on that
data. That is **gradient ascent**, one of the simplest approximate unlearning methods. It is also easy to overdo, as
[Quick fixes and their traps](../unlearning/approximate-unlearning.md) explains.

The trouble is that the climb has no top. Cross-entropy can grow without limit, so nothing in the method says "stop
here". In Lesson 08, gradient ascent on Carol's digits with a larger step took the model's test accuracy, epoch by
epoch, from 98% to 89%, 66%, 44% and on down to 10%, which is a blind guess for 10 digits. A milder version, called
NegGrad+, pairs every uphill step on Carol with a downhill step on everyone else. Even so, only 1 of the 46 settings
Lesson 08 tried passed its audit.

## A worked example

Start with one weight and a made-up loss, \(L(w) = (w - 3)^2\). Its lowest point is at \(w = 3\), and its gradient is
\(2(w - 3)\). Begin at \(w = 0\) with a learning rate of 0.1.

| Step | Weight \(w\) | Loss | Gradient | Change \(-0.1 \times\) gradient |
|---|---|---|---|---|
| 0 | 0.00 | 9.00 | −6.00 | +0.60 |
| 1 | 0.60 | 5.76 | −4.80 | +0.48 |
| 2 | 1.08 | 3.69 | −3.84 | +0.38 |
| 3 | 1.46 | 2.36 | −3.07 | +0.31 |

1. **Each step goes downhill.** The gradient is negative, so subtracting it makes the weight bigger, towards 3.
2. **The steps shrink.** As the slope flattens, the gradient gets smaller and so does each step. Every step closes
   20% of the gap that is left.
3. **Too big a step overshoots.** With a learning rate of 1.1 instead, the first step goes from 0 to 6.6, past the
   bottom. The loss rises from 9.00 to 12.96, and each later step swings further away.

Now scale this up to the course's network.

4. **The batches.** The 1,257 training digits are split into groups of 64. That is 20 groups per epoch, because
   1,257 ÷ 64 is about 19.6, which rounds up to 20.
5. **The steps.** 60 epochs of 20 steps each is about 1,200 steps, each one moving all 85,002 weights at once. The
   whole run takes about a third of a second.
6. **Carol's share.** Her 40 digits are 40 of the 1,257, so an average batch of 64 holds about 2 of them
   (\(64 \times 40 \div 1{,}257 \approx 2.0\)). Each of her digits is seen once per epoch, so 60 times in all. With
   about 2 of her digits in a typical batch, most of the 1,200 steps feel a small pull from her.

??? checkpoint "Checkpoint 2 · In the table, why does the change get smaller at each step even though the learning rate stays at 0.1?"
    **Because the gradient gets smaller.** The step is the learning rate times the gradient. Near the bottom the
    slope flattens, so the gradient shrinks from −6.00 to −3.07 and the step shrinks with it. Gradient descent slows
    down by itself as it nears a low point.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>94.1%</strong><span>of 85,002 weights differ when Carol is left out, from the same seed</span></div>
<div><strong>9.87 vs 50.96</strong><span>weight distance, without Carol against another seed</span></div>
<div class="is-bad"><strong>98% to 10%</strong><span>test accuracy as gradient ascent runs on unchecked</span></div>
<div class="is-bad"><strong>1 of 46</strong><span>settings of the ascent-based fixes passed the audit</span></div>
</div>

The first two tiles say the same thing from two sides. Carol's influence reaches almost every weight, yet the change
she makes is small next to the natural spread between good networks. The last two tiles show what happens when you
try to run the walk backwards without a map. It is easy to go too far, and hard to stop in the right place.

## Limits

**It finds a low point, not the lowest.** For a network, gradient descent ends in one of many good valleys. Which one
depends on the seed.

**The learning rate has to be chosen.** Nothing in the method tells you the right step size. The course uses 0.001
with Adam, a choice that works for its small network.

**It only uses the slope.** Gradient descent ignores the curvature of the loss. That is cheap, but it is also why
gradient ascent works so poorly as unlearning. In Lesson 08's logistic regression, the best gradient-ascent step closed
8% of the gap to the retrained model, while one Newton step, which uses curvature, closed 95%.

**Curvature is too costly for networks.** A Newton step needs a table with one row and one column per weight. For the
course's network that is about 29 GB, so it is out of reach even for this small model.

!!! tip "What to do in practice"
    - Fix the seed when you want to compare two training runs, so the only difference is the one you made.
    - Keep the training recipe (learning rate, batch size and epochs) the same for any model you compare.
    - Never trust a single run as "the" model. Train several with different seeds to see the spread.
    - If you run gradient ascent, set a stopping rule in advance and check utility after every epoch.

## In code

Here is a training loop from the course library, written in plain NumPy.

```python
from mul import nn, train, lab
import numpy as np

model = lab.model_fn()                     # a small neural network
opt = nn.Adam(model.params, lr=1e-3)       # Adam is a popular variant of gradient descent
rng = np.random.default_rng(0)
for epoch in range(60):
    for b in train.batches(len(X), 64, rng):                     # mini-batches of 64
        _, g = nn.cross_entropy(model.forward(X[b], keep_cache=True), y[b])
        opt.step(model.backward(g))                              # one step downhill
```

??? deep "Go deeper · what Adam adds, and the one-sign change for ascent"
    Plain gradient descent moves every weight by the same multiple of its gradient. Adam keeps two running averages
    for each weight, one of its recent gradients and one of their squares. It then steps each weight by roughly the
    average gradient divided by the typical size of that gradient. Weights with steady, small gradients still move,
    and weights with noisy, large ones move more carefully. In the course library this is the `Adam` class in
    `mul/nn.py`, with a learning rate of 0.001.

    Gradient ascent in the course library is the same loop run on the forget set with the gradient's sign flipped.

    ```python
    _, g = nn.cross_entropy(model.forward(Xf[b], keep_cache=True), yf[b])
    opt.step(model.backward(-g))        # the minus sign is the whole method
    ```

    NegGrad+ mixes both in one step, with a loss of \(\alpha L_r - (1 - \alpha) L_f\). Lesson 08 found it needed
    \(\alpha\) close to 0.99, so the uphill pull on Carol is tiny next to the downhill pull on everyone else.

## Common mistakes

!!! danger "Mistakes people make"
    - **A learning rate that is too large.** The steps overshoot and the loss jumps around instead of falling.
    - **Thinking training finds "the" answer.** For neural networks there are many equally good valleys. Two runs with
      different random starts end in different places. This matters a lot for unlearning (see
      [the gold band](../unlearning/gold-band.md)).
    - **Looking for the weights that hold one person.** Gradient descent spreads every example along the whole path,
      so leaving Carol out changes 94.1% of the weights.
    - **Comparing weights to prove forgetting.** Another seed moves the weights five times further than removing
      Carol does. Only behaviour can show whether she was forgotten.

??? checkpoint "Checkpoint 3 · A colleague wants to find the weights Carol changed and set them back. Using Lesson 04's numbers, why will that not work?"
    **Because she changed almost all of them.** 94.1% of the 85,002 weights differ when she is left out, since every
    step after her first batch started from a different place. And there is no one right value to set them back to.
    A network from another seed is 50.96 away, five times further than the 9.87 that Carol accounts for, and it is
    just as good.

## Key takeaways

!!! notes "Notes to take"
    - **Update rule.** \(w \leftarrow w - \eta \nabla L(w)\). The gradient points uphill, so step the other way.
    - **Learning rate.** The step size. Too small crawls, too large overshoots. The course uses 0.001 with Adam.
    - **Course recipe.** Batches of 64 and 60 epochs, about 1,200 steps over 1,257 digits.
    - **Carol's share.** About 2 of her digits per batch, each seen 60 times.
    - **The path.** Each step starts where the last ended, so leaving Carol out changes 94.1% of the weights.
    - **Many valleys.** Another seed lands 50.96 away against 9.87 for removing Carol, and is just as good.
    - **Gradient ascent.** \(w \leftarrow w + \eta \nabla L_f(w)\). No top to the climb, so test accuracy fell 98% to 10%.
    - **Trap.** Only 1 of 46 ascent-based settings passed in Lesson 08, and only with the gold band to look at.
    - **Remember.** Prove forgetting by behaviour, not by comparing weights.

## Quiz

```quiz
- q: In the foggy hill picture, what does the slope under your feet stand for?
  options:
    - The training data
    - The gradient
    - The test accuracy
  answer: 1
  why: The gradient tells each weight which way is downhill on the loss.
- q: What does the learning rate control?
  options:
    - How big each step is
    - How many examples there are
    - How many classes the model predicts
  answer: 0
  why: A larger learning rate takes bigger steps; too large and the steps overshoot.
- q: What is one pass over all the training data called?
  options:
    - A batch
    - An epoch
    - A gradient
  answer: 1
  why: Training usually runs for many epochs, each made of many mini-batches.
- q: Why does gradient descent spread Carol's influence across the whole model?
  options:
    - Every later step starts from a place her examples already changed.
    - Her data is copied into every weight on purpose.
    - Gradient descent only uses her data.
  answer: 0
  why: Each step depends on the last, so an early nudge from her digits shifts the whole rest of the path.
- q: What does gradient ascent on the forget set do?
  options:
    - Makes the model better on the forget set
    - Makes the model worse on the forget set
    - Deletes the forget set from the database
  answer: 1
  why: Stepping uphill on the loss increases it, so the model gets worse on that data.
- q: A weight is 1.0, its gradient is 2.0 and the learning rate is 0.1. What is the weight after one step of gradient descent?
  options:
    - 1.2
    - 0.8
    - 3.0
  answer: 1
  why: The step is 1.0 minus 0.1 times 2.0, which is 0.8. Gradient descent moves against the gradient.
- q: Two networks are trained on the same data with seeds 0 and 1. Both score about 98% on the test set. What does that show?
  options:
    - There are many equally good sets of weights, so there is no single right answer to compare with.
    - One of them must have a bug.
    - The seed has no effect on training.
  answer: 0
  why: In Lesson 04 they were 50.96 apart, further than the 9.87 that removing Carol caused, yet both were good models.
- q: Why does gradient ascent need a stopping rule?
  options:
    - Because it only runs for one epoch.
    - Because the loss it climbs has no top, so it can keep making the model worse.
    - Because it needs the Hessian.
  answer: 1
  why: In Lesson 08, unchecked gradient ascent took test accuracy from 98% to 10%, a blind guess for 10 digits.
- q: The course's network trains on 1,257 digits in batches of 64 for 60 epochs. About how many steps is that?
  options:
    - "60"
    - "75,000"
    - "1,200"
  answer: 2
  why: 1,257 ÷ 64 rounds up to 20 batches per epoch, and 20 × 60 = 1,200 steps.
```

## Try it

!!! levelup "Level up"
    You can now take a gradient step by hand, count the steps in a training run and explain why the path spreads
    Carol across the whole network. Next quest, [Overfitting and memorisation](overfitting-and-memorisation.md),
    where you see what those 1,200 steps make the model remember.

- Read the next page, [Overfitting and memorisation](overfitting-and-memorisation.md).
- The lesson [08 · Baselines and traps](../lessons/08-approximate-baselines-and-traps.md) tries gradient ascent as an unlearning method.
