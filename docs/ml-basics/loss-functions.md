---
title: Loss functions
description: A loss function turns "how wrong is the model?" into a single number that training makes smaller, and that attackers read.
---

# Loss functions

!!! oneline "In one line"
    A **loss** is one number that says how wrong the model is; training tries to make it as small as possible.

!!! mission "Your mission · about 13 minutes · 3 checkpoints"
    By the end of this page you can

    - work out the cross-entropy loss for one example from the probability of the right answer,
    - explain why loss shows things that accuracy hides,
    - say why a very low loss on Carol's digits is a privacy leak, and why a very high one after unlearning is too.

## Why it matters

A computer cannot "try harder" without knowing what *better* means. The loss gives it a target, and lower is better.
Unlearning uses loss too. Some methods try to make the loss on the forget set go **up** again, and attackers look at
the loss on a person's data to guess whether it was used in training.

So the loss plays three parts in this course. During training, it is the number the model is pushed to shrink. After
training, it is a clue an attacker can read, because the model is unusually sure about the examples it learnt from.
During unlearning, it is the lever some methods pull the other way. Each part comes back again and again, from
[gradient descent](gradient-descent.md) to [membership inference attacks](../unlearning/membership-inference-attacks.md)
and [quick fixes like gradient ascent](../unlearning/approximate-unlearning.md).

## A simple example

Think of a darts game. The loss is the distance between your dart and the bullseye. A perfect throw has loss 0. A wild
throw has a large loss. Practising means changing your throw so that the average distance gets smaller.

!!! simply "Explain it simply"
    A loss is a measure of surprise. Show the model a digit and tell it the right answer. If it already expected that
    answer, it is hardly surprised and the loss is near 0. If it thought the answer was something else, it is very
    surprised and the loss is large. Training makes the model less surprised by its training data.

The darts picture also shows something accuracy cannot. Two darts can both land on the board, so both "count", yet
one is a hair from the bullseye and the other is near the edge. Accuracy only asks whether the answer was right. Loss
asks how close, and that extra detail is what training and attackers both use.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Loss | One number for how wrong the model is. Lower is better | The training loss falls as the network learns |
| Logit | A raw score the model gives each possible answer, before it is turned into a probability | The network gives 10 logits, one per digit |
| [Softmax](../start-here/glossary.md#s) | A function that turns raw scores into probabilities that add up to 1 | 10 logits become 10 probabilities |
| [Cross-entropy](../start-here/glossary.md#c) | The usual loss for classification, \(-\log(p)\) for the probability \(p\) of the right answer | 0.11 when the right digit gets 0.90 |
| Per-example loss | The loss of one single example, not the average | The raw material of membership attacks in Lesson 05 |
| Squared error | The gap between prediction and truth, squared, used when the answer is a number | The loss of ridge regression in Lesson 02 |
| Unbounded | Able to grow without limit | Cross-entropy goes up forever as \(p\) heads to 0 |
| [Over-forgetting](../start-here/glossary.md#o) | Being far worse on the forget set than a model that never saw it | A huge loss on Carol's digits after unlearning |

## How it works

<!-- diagram: loss-functions -->

The figure shows the idea with the simplest case, a model that predicts a number. Each dot is a true value and the
blue line is what the model predicts. Each dashed red bar is the gap for one point. The loss squares every gap and
averages them into one number for the whole model. Training moves the line to make that number smaller. This is
**squared error**, the loss behind [linear and ridge regression](linear-and-ridge-regression.md).

For classification, the most common loss is **cross-entropy**. The idea is simple.

<ol class="steps" markdown>
<li markdown>The model gives a **probability** for each possible answer. For a digit image, it might give 0.90 to "7", 0.05 to "1" and smaller amounts to the rest.</li>
<li markdown>Look at the probability it gave to the **right** answer.</li>
<li markdown>The loss is large when that probability is small, and close to 0 when it is close to 1.</li>
<li markdown>Average this over all the examples to get the training loss.</li>
</ol>

**For Carol this means** each of her 40 digits gets its own loss, and the network is trained to push all 40 towards
zero along with the other 1,217 digits.

If the correct answer has probability \(p\), the loss for that example is

\[
\text{loss} = -\log(p)
\]

| Probability given to the right answer | Loss |
|---|---|
| 0.99 | 0.01 |
| 0.90 | 0.11 |
| 0.50 | 0.69 |
| 0.10 | 2.30 |

So a confident right answer costs almost nothing, and a confident wrong answer costs a lot.

Two rows deserve a closer look. A probability of 0.10 is what a model gets if it spreads its belief evenly over the
10 digits, so a loss of about 2.30 means "no better than a blind guess". At the other end, the loss never quite
reaches 0 and never stops growing. At 0.01 it is 4.61 and at 0.001 it is 6.91. That missing ceiling matters a lot for
unlearning, as you will see below.

??? deep "Go deeper · from logits to loss, and the gradient"
    The network's last layer gives 10 logits \(z_1, \dots, z_{10}\). Softmax turns them into probabilities,
    \(p_k = e^{z_k} / \sum_j e^{z_j}\), which are all positive and add up to 1. The cross-entropy for an example whose
    right answer is \(y\) is then \(-\log p_y\).

    Training needs to know which way to move each logit. For cross-entropy with softmax, the answer is short. The
    gradient for logit \(k\) is \(p_k - 1\) if \(k\) is the right answer and \(p_k\) otherwise. The course library
    computes exactly this in `nn.cross_entropy`, as `(p - onehot(y)) / batch_size`.

    Read what that says. If the right answer already has \(p = 0.99\), its gradient is only \(-0.01\), so the example
    barely moves the weights. If it has \(p = 0.10\), the gradient is \(-0.90\), a strong push. Examples the model
    already gets right with confidence stop pulling on it, and the badly wrong ones pull hardest.

### Loss and memorisation

A model usually has a **lower loss on data it trained on** than on new data. If Carol's digits have a much lower loss
than similar digits the model never saw, the model remembers her. Lesson 04 shows Carol's loss falling to almost zero
while look-alike digits stay much higher. This is also the basis of [membership inference attacks](../unlearning/membership-inference-attacks.md).

The attack in Lesson 05 is built on this one fact. An outsider asks the model about a digit, reads its loss on the
right answer and guesses "it was in training" when the loss is low. Against the network, comparing Carol's 40 digits
with 80 unseen look-alikes, this simple attack scored an AUC of 0.71, where 0.5 is a coin flip and 1.0 is always
right. On typical digits it scored only 0.53, because typical digits were learnt, not memorised.

### Loss versus accuracy

Accuracy counts an answer as right if the right digit gets the biggest probability. It does not care whether that
probability is 0.51 or 0.999. The loss does. So two models with the same accuracy can have very different losses.

**For Carol this means** that accuracy and loss tell different parts of her story. Accuracy shows the original model
is right on all 40 of her digits and on 77.5% of the look-alikes. The loss shows *how sure* it is on each one, and
that is the finer clue an attacker uses.

??? checkpoint "Checkpoint 1 · Two models both get one of Carol's digits right. One gives the right answer 0.51 and the other 0.999. Which has the lower loss, and which one looks more like it trained on her?"
    **The model at 0.999.** Its loss is about 0.001, against 0.67 for the model at 0.51. Both count as correct, so
    accuracy cannot tell them apart. But near-total certainty on an unusual digit is the sign of a model that has seen
    that exact digit, which is what a membership attack looks for.

### Loss in unlearning

Some unlearning methods run training in reverse. Instead of pushing the loss on Carol's digits down, they push it
**up**. This is called [gradient ascent](../start-here/glossary.md#g). It is natural, but the loss has no ceiling, so
nothing in the method says when to stop. In Lesson 08, gradient ascent left running with a larger step dragged the
model's test accuracy from 98% down to 10% within 10 epochs, and it stayed there. That is a blind guess for 10 digits.

The right target for Carol's loss is not "as high as possible". It is "what a model that never saw her would give". A
model that never met Carol still reads 55.0% of her digits in Lesson 00, so its loss on her is moderate, not huge.
Pushing past that is [over-forgetting](../start-here/glossary.md#o), and it is itself a signal an attacker can spot.

Other unlearning methods use a different loss. SCRUB and Bad Teacher use **KL divergence**, which measures how
different two sets of probabilities are, to make a model copy or move away from a teacher model. You meet it on
[Probabilities and KL divergence](probabilities-and-kl-divergence.md).

??? checkpoint "Checkpoint 2 · After gradient ascent, the model gives Carol's digits a loss far higher than any retrained model does. Is that good forgetting?"
    **No, it is over-forgetting.** A model that never saw Carol is uncertain about her digits, not wildly wrong about
    them. A loss far above that tells an attacker her digits were treated in a special way. The target is the loss of
    a retrained model, which [the gold band](../unlearning/gold-band.md) turns into a range.

## A worked example

Here is the arithmetic of cross-entropy on a small batch, with round numbers chosen to make the sums easy. Suppose the
network sees four digits and gives the right answer these probabilities.

| Digit | Probability of the right answer | Loss \(-\log(p)\) | Right? |
|---|---|---|---|
| A clean "1" | 0.99 | 0.01 | Yes |
| A tidy "7" | 0.90 | 0.11 | Yes |
| A messy "4" | 0.50 | 0.69 | Yes, if no other digit gets more |
| A smudged "9" | 0.10 | 2.30 | No |

1. **Per-example loss.** Each row's loss comes straight from \(-\log(p)\).
2. **Batch loss.** The average is \((0.01 + 0.11 + 0.69 + 2.30) \div 4 = 3.11 \div 4 \approx 0.78\).
3. **What training does.** The smudged "9" gives by far the largest loss, so it pulls hardest on the weights. Training
   changes them so that its probability rises, even if the clean "1" barely improves.
4. **What happens to Carol.** Her thick-marker digits look like nothing else in the data, so they behave like
   the smudged "9", with a high loss that other digits do little to lower. The only way to shrink it is to learn her particular digits. Over 60 epochs,
   Lesson 04's plot shows her loss falling to almost zero, while look-alike digits in the same style stay far higher.
5. **What an attacker sees.** A near-zero loss on an unusual digit is rare for a digit the model never saw. That is
   why the loss attack can pick out Carol's digits more often than chance.

## What the lesson found

<div class="stats">
<div><strong>2.30</strong><span>the loss of a blind guess over 10 digits</span></div>
<div class="is-bad"><strong>0.71</strong><span>AUC of the loss attack on Carol's digits, Lesson 05</span></div>
<div class="is-good"><strong>0.53</strong><span>AUC on typical digits, close to a coin flip</span></div>
<div class="is-bad"><strong>98% to 10%</strong><span>test accuracy as gradient ascent climbs with no ceiling, Lesson 08</span></div>
</div>

??? deep "Go deeper · the loss attack on six models"
    Lesson 05 ran the same loss attack, Carol's 40 digits against 80 unseen look-alikes, on every model from Lessons
    01 to 04.

    | Model | AUC | True positives at 5% false positives |
    |---|---|---|
    | Naive Bayes | 0.53 | 5.5% |
    | k-NN, k = 5 | 0.59 | 8.2% |
    | Logistic regression | 0.59 | 2.5% |
    | RBF SVM | 0.66 | 15.0% |
    | Random forest | 0.96 | 62.5% |
    | Neural network | 0.71 | 2.5% |

    The pattern follows memorisation. Naive Bayes, which keeps only averages, is close to a coin flip. The random
    forest leaks most. The network's AUC of 0.71 understates how much it remembers Carol, because one loss threshold
    for every digit cannot tell a digit that is naturally easy from one that is easy because it was trained on. The
    sharper per-example test in Lesson 05, U-LiRA, compares each digit with shadow models trained with and without it.
    Lesson 08 shows it flagging 95% of Carol's digits as still remembered by the original network.

## Limits

**A loss is a summary.** One average hides which examples are well fitted and which are not. For memorisation and
privacy, you need the per-example loss, especially for unusual data.

**Low loss on training data is not success.** Very low training loss can mean the model has memorised rare examples,
which is good for its score and bad for privacy.

**One loss threshold is a blunt tool.** Some digits are easy for every model. A single cut-off cannot tell "easy" from
"remembered", which is why stronger attacks look at each example separately.

**Cross-entropy has no ceiling.** Training downhill is safe because the loss cannot go below 0. Climbing uphill is not,
because nothing stops the climb. Methods that push a loss up need a brake, such as an anchor on the retain set or a
bounded loss.

## In code

The course library computes cross-entropy from the model's raw outputs (called *logits*).

```python
from mul import nn
loss, grad = nn.cross_entropy(model(X), y)   # average loss, and its gradient for training
```

??? deep "Go deeper · per-example losses, as an attacker reads them"
    `train.per_example_loss` gives one loss per digit instead of the average. Lesson 05 compares Carol's losses with
    those of the look-alikes, and `audit.loss_mia` turns the comparison into an AUC.

    ```python
    from mul import lab, train, audit
    L = lab.make_lab("carol")
    model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
    l_carol = train.per_example_loss(model, L.Xf, L.yf)                     # 40 losses, near zero
    l_alike = train.per_example_loss(model, L.X_like_forget, L.y_like_forget)  # 80 losses, higher
    r = audit.loss_mia(model, L.Xf, L.yf, L.X_like_forget, L.y_like_forget)
    print(r["auc"])                                                          # 0.71 in Lesson 05
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Treating low training loss as success.** Very low loss on training data can mean memorisation.
    - **Pushing the loss on forgotten data as high as possible.** A model that never saw Carol would not have a
      huge loss on her digits. A suspiciously high loss is itself a sign that something happened (see
      [the gold band](../unlearning/gold-band.md)).
    - **Judging a model on accuracy alone.** Two models can both be right on Carol's digits while one is far more
      certain. The loss shows the difference, and so does an attacker.
    - **Running gradient ascent with no stopping rule.** The loss can climb forever. In Lesson 08 this took test
      accuracy down to 10%.

??? checkpoint "Checkpoint 3 · An attacker sees a loss of 0.001 on one of Carol's digits and 0.5 on a look-alike. What does the attacker guess, and why might they still be wrong?"
    **They guess Carol's digit was in training.** A loss of 0.001 means the model gave the right answer a
    probability of about 0.999, which is unusual for a thick digit it never saw. But some digits are simply easy, and
    one threshold cannot tell easy from remembered. That is why the simple attack reached an AUC of 0.71, not 1.0,
    and why the course also uses per-example tests.

## Key takeaways

!!! notes "Notes to take"
    - **Loss.** One number for how wrong the model is. Training makes it smaller.
    - **Cross-entropy.** \(-\log(p)\) for the probability of the right answer. 0.90 gives 0.11, 0.10 gives 2.30.
    - **Blind guess.** Spreading belief evenly over 10 digits gives a loss of 2.30.
    - **Squared error.** The loss for predicting numbers, the average of the squared gaps.
    - **Loss versus accuracy.** Accuracy asks if the top answer is right. Loss also asks how sure the model was.
    - **Memorisation.** Carol's loss falls to almost zero, while look-alikes stay higher.
    - **Attack.** Low loss means "was in training". AUC 0.71 on Carol, 0.53 on typical digits.
    - **Trap.** Cross-entropy has no ceiling, so gradient ascent can wreck a model, 98% to 10% in Lesson 08.
    - **Target.** After unlearning, Carol's loss should match a retrained model's, not be as high as possible.

## Quiz

```quiz
- q: What does a loss of 0 mean?
  options:
    - The model is as wrong as possible.
    - The model's answer is perfect.
    - The model has not been trained.
  answer: 1
  why: Lower is better. Zero loss means the model gave the right answer with full confidence.
- q: The model gives the right answer a probability of 0.10. Is the cross-entropy loss high or low?
  options:
    - High
    - Low
  answer: 0
  why: "-log(0.10) is about 2.30, much higher than -log(0.99), which is about 0.01."
- q: Carol's digits have a much lower loss than similar digits the model never saw. What does that suggest?
  options:
    - The model remembers Carol's digits.
    - Carol's digits are easier for everyone.
    - The loss function is broken.
  answer: 0
  why: Training pushes the loss down on the examples it sees. A big gap versus look-alike data shows memorisation.
- q: After unlearning, should the loss on Carol's digits be as high as possible?
  options:
    - Yes, the higher the better.
    - No, it should look like the loss of a model that never saw her.
  answer: 1
  why: A model that never met Carol would not be extremely wrong on her digits. Over-forgetting is a warning sign.
- q: Two models are both right on a digit. One gives the right answer 0.6 and the other 0.99. What can the loss tell you that accuracy cannot?
  options:
    - Nothing, because both answers are right.
    - Which model was trained for longer.
    - How sure each model was, which is the clue a membership attack reads.
  answer: 2
  why: Accuracy only checks the top answer. Loss measures confidence, and unusual confidence on a rare digit hints that it was in training.
- q: A model spreads its probability evenly over the 10 digits. What is its cross-entropy loss?
  options:
    - About 2.30
    - About 0.11
    - Exactly 0
  answer: 0
  why: Each digit gets 0.10, and -log(0.10) is about 2.30. That is the loss of a blind guess.
- q: Why can gradient ascent on the forget set wreck a model if nobody stops it?
  options:
    - It deletes the forget set from the training data.
    - Cross-entropy has no ceiling, so the loss can be pushed up forever.
    - It lowers the learning rate to zero.
  answer: 1
  why: In Lesson 08, gradient ascent with a larger step took test accuracy from 98% to 10% within 10 epochs.
- q: The loss attack scored an AUC of 0.71 on Carol's digits but 0.53 on typical digits. Why the difference?
  options:
    - Typical digits are learnt from many similar examples, so their loss is low whether or not they were in training.
    - The attack only works on thick digits.
    - Typical digits are never in the training set.
  answer: 0
  why: Membership only leaks where a model needed the exact example. Carol's unusual digits were memorised, typical ones were not.
```

## Try it

!!! levelup "Level up"
    You can now read a loss, compare it with accuracy and see why both a tiny and a huge loss on Carol give her away.
    Next quest, [Gradient descent](gradient-descent.md), where you see how training uses the loss to change every
    weight.

- Read the next page, [Gradient descent](gradient-descent.md).
- The lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) plots Carol's loss during training.
