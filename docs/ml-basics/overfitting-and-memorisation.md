---
title: Overfitting and memorisation
description: When a model remembers individual examples instead of learning general patterns, and why unusual data is remembered most.
---

# Overfitting and memorisation

!!! oneline "In one line"
    **Memorisation** is when a model gets an example right *because it saw that exact example* in training, not because
    it learnt the general pattern.

!!! mission "Your mission · about 14 minutes · 3 checkpoints"
    By the end of this page you can

    - tell overfitting on a whole dataset apart from memorisation of one person,
    - work out a memorisation gap and a memorisation score from a few numbers,
    - explain why unusual people like Carol are remembered most, and which models remember them most.

## Why it matters

If a model never memorised anyone, unlearning would hardly be needed, because removing one person would barely change it.
Memorisation is what makes a model carry a specific person's data, and it is what attackers use to tell whether
someone's data was used. It is the heart of the problem this course solves.

It is also not spread evenly. The course's network looks barely overfitted at all. It is right on 100% of its
training digits and 98.0% of new ones, a gap of only 2 points. But on Carol's 40 digits against 80 unseen digits in
her style, the gap is 22.5 points. The average hides one person who is remembered far more than everyone else. Real
deletion requests often come from exactly such people, so the hard case is the normal case.

## A simple example

Two students prepare for a maths exam.

- **Student A** understands the methods. They can solve new questions.
- **Student B** memorises the answers to last year's paper. They score 100% on that paper and badly on new questions.

Student B has **overfitted**. They fit the practice questions perfectly but did not learn the subject. A model can do
the same.

!!! simply "Explain it simply"
    Most students are like Student A for ordinary questions, because they have seen hundreds of them. But suppose last
    year's paper had one strange question, unlike anything in the textbook. Even good students may just learn that
    one answer by heart, because there is nothing to learn it from. That one strange question is Carol's digit. The
    model learns the ordinary digits and memorises hers.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Overfitting](../start-here/glossary.md#o) | Being much better on training data than on new data | Student B, or a model that copies the noise in its data |
| Underfitting | Being too simple to learn the pattern at all, so it does badly even on training data | A straight line drawn through points that curve |
| Generalisation | Doing well on new data, not just on the training data | 98.0% on 540 unseen test digits |
| [Memorisation](../start-here/glossary.md#m) | Being right on an example *because* it was in training | Carol's digits, right 100% of the time |
| Memorisation gap | Accuracy on someone's own data minus accuracy on look-alike data the model never saw | +22.5 points for the network on Carol |
| Memorisation score | Feldman's per-example measure, how much more often the model is right on \(x\) when \(x\) was in training | About 0 for a typical digit |
| Long tail | The many rare cases in real data, each with few similar examples | Carol's thick-marker digits |
| [Leverage](../start-here/glossary.md#l) | How hard one training point pulls a linear model towards itself | 0.116 for Carol's digits against 0.039 for others |
| Regularisation | A penalty that keeps weights small, so a model fits less tightly | The course trains with none, on purpose |

## How it works

<!-- diagram: overfitting-and-memorisation -->

The figure fits the same nine points three ways. On the left, a flat line is too simple. It misses the pattern and
has a high training error. In the middle, a smooth curve follows the pattern and has a low training error. On the
right, a jagged line passes through every point, including the random noise, so its training error is zero. It looks
best on the training data, but it would do worst on new points, because it learnt the noise as if it were the
pattern.

### Overfitting

A model **overfits** when it is much better on its training data than on new data. Signs of overfitting.

- Training accuracy is much higher than test accuracy.
- Training loss keeps falling while test loss stops falling or rises.

**For the course's network this means** a small overall gap. It is right on 100% of the training digits and on 98.0%
of the test digits. On the whole dataset it generalises well. To see what it remembers, you have to look closer.

### Memorisation of individual examples

Memorisation is overfitting looked at **one example at a time**. The researcher Vitaly Feldman (2020) measured it like
this.

\[
\text{mem}(x) = P[\text{right on } x \mid x \text{ in training}] - P[\text{right on } x \mid x \text{ not in training}]
\]

In plain words, it asks how much more often is the model right on \(x\) when \(x\) was in training? You estimate it by training
several models with and without the example.

- For a **typical** digit, the score is about 0. Thousands of similar digits teach the same thing.
- For an **unusual** digit, like one of Carol's thick-marker digits, the score is often high. Nothing else teaches it.

**For Carol this means** that many of her digits are right only because they were trained on. Lesson 04 measures this
with 6 networks trained with her digits and 6 trained without them. Typical digits score close to 0, and many of
Carol's score high.

??? deep "Go deeper · working out a memorisation score"
    Suppose you train 6 networks with one of Carol's digits and 6 without it, each with a different seed. With the
    digit, all 6 get it right, so the first term is \(6 \div 6 = 1.0\). Without it, only 2 get it right, so the second
    term is \(2 \div 6 \approx 0.33\). Its score is \(1.0 - 0.33 = 0.67\). A typical digit that all 12 networks get
    right scores \(1.0 - 1.0 = 0\).

    These are round numbers to show the arithmetic. Lesson 04 runs exactly this experiment on Carol's 40 digits and
    on 40 random typical digits. It removes all 80 at once for the "without" models, so 6 networks with and 6
    without are enough for every digit.

    The score can also be a little below 0, by chance, when a digit happens to be right slightly more often without
    training on it. A value near 0 either way means "learnt from others". A value near 1 means "known only because
    it was seen".

??? checkpoint "Checkpoint 1 · The network is right on 100% of its training digits and 98.0% of its test digits. Is it badly overfitted?"
    **Not on average, but it is on Carol.** A 2-point gap on the whole dataset is small. But the network is right on
    all of Carol's 40 digits and only 77.5% of unseen digits in her style, a 22.5-point gap. Averages over many
    typical digits hide the few unusual ones that the model remembers.

### Unusual data is remembered most

This is called the **long tail**. Real data contains many rare cases, and to get them right a model has to memorise
them. The course sees this again and again.

| Lesson | How Carol stands out |
|---|---|
| 02 | Her digits have about **3 ×** the *leverage* (pull on the model) of a typical digit, 0.116 vs 0.039. |
| 03 | **97.5%** of her digits are support vectors in an SVM, against 40.5% for everyone else. |
| 04 | A neural network is right on 100% of her digits but only 77.5% of look-alike digits it never saw. |

Each lesson finds the same thing through a different model. In Lesson 01, when k-NN is asked about new thick-marker
digits, 85.8% of the neighbours it consults are Carol's own digits. In Lesson 03, her 40 rows between them land in all
50 trees of a random forest, while a typical row is in about 32 of the 50. Whatever the model, Carol is the point it
leans on.

!!! note "A Responsible AI point"
    People with unusual data are memorised more, so they are also more exposed to privacy attacks. Deletion requests
    are not spread evenly, and the people who ask are often exactly the hard cases.

### More flexible models memorise more

In Lesson 04, the "memorisation gap" (accuracy on Carol minus accuracy on look-alike digits) was −1.3% for Naive
Bayes, +15.0% for logistic regression, +22.5% for a neural network and +30.0% for a random forest. Simple models that
keep only averages remember individuals much less.

A flexible model is one that can bend to fit almost any pattern, given enough data and steps. That freedom is what
makes it accurate, and it is also what lets it fit Carol's 40 digits one by one. Naive Bayes keeps only an average and
a spread for each pixel of each digit, so 40 digits among 1,257 barely move it. A random forest can grow branches that
fit her digits alone.

??? checkpoint "Checkpoint 2 · A digit is right in 6 of 6 networks trained with it and 6 of 6 trained without it. What is its memorisation score, and what does that say?"
    **0.** The score is \(6 \div 6 - 6 \div 6 = 0\). The model gets this digit right whether or not it saw it, so it
    learnt the digit from other, similar examples. This is what a typical digit looks like. Forgetting it would change
    almost nothing.

## A worked example

Follow Carol through the course's three measures of memory, for the neural network.

1. **The whole dataset.** The network is right on 100% of its training digits and 98.0% of the test digits. Judged
   only this way, it has learnt well.
2. **The gap for Carol.** It is right on all 40 of her digits (100.0%) and on 77.5% of the 80 look-alikes, which
   is 62. The gap is \(100.0 - 77.5 = 22.5\) points. That gap is her fingerprint.
3. **The attacker's view.** Lesson 05's loss attack, comparing her digits with the look-alikes, scores an AUC of
   0.71, where 0.5 is a coin flip. On typical digits it scores 0.53. The model leaks her membership, and not
   everyone else's.
4. **After retraining.** A fresh network trained without her scores 55.0% on her digits and 62.5% on the look-alikes.
   The gap is now \(55.0 - 62.5 = -7.5\) points. Her digits get no special treatment any more.
5. **Why the target is not zero.** The retrained network still reads 55.0% of her digits. It learnt digits from
   everyone else, so it can read many of hers. Forgetting removes the memorised part, the extra points she got for
   being seen, not the general skill.

Now compare the most and least memorising models from Lesson 04. Naive Bayes is right on 60.0% of Carol and 61.3% of
look-alikes, a gap of −1.3, so it never memorised her. The random forest is right on 100.0% of Carol and 70.0% of
look-alikes, a gap of +30.0. The loss attack in Lesson 05 scores 0.53 against Naive Bayes and 0.96 against the forest.
More memory means more leakage.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>2 points</strong><span>overall gap, 100% on training digits against 98.0% on test</span></div>
<div class="is-bad"><strong>+22.5</strong><span>points, the network's gap on Carol against look-alikes</span></div>
<div class="is-bad"><strong>+30.0</strong><span>points, the random forest's gap, the largest in Lesson 04</span></div>
<div class="is-good"><strong>−1.3</strong><span>points for Naive Bayes, which keeps only averages</span></div>
</div>

??? deep "Go deeper · the full table from Lesson 04"
    | Model | Carol | Unseen thick-marker digits | Gap | Test |
    |---|---|---|---|---|
    | Naive Bayes | 60.0% | 61.3% | −1.3 | 91.1% |
    | k-NN, k = 5 | 75.0% | 67.5% | +7.5 | 98.3% |
    | Logistic regression | 92.5% | 77.5% | +15.0 | 97.2% |
    | RBF SVM | 100.0% | 87.5% | +12.5 | 99.4% |
    | Random forest | 100.0% | 70.0% | +30.0 | 97.2% |
    | Neural network | 100.0% | 77.5% | +22.5 | 98.0% |

    Notice the test column. Every model except Naive Bayes scores between 97.2% and 99.4% on new digits, yet their
    gaps on Carol range from +7.5 to +30.0. A high test score says nothing about how much a model remembers one person.

    The order is not perfectly by flexibility. The SVM's gap (+12.5) is smaller than logistic regression's (+15.0),
    partly because the SVM also reads unseen thick digits well (87.5%). With only 40 and 80 digits, one digit moves
    these numbers by 2.5 and 1.25 points, so small differences between models are not meaningful.

## Limits

**The gap needs a true look-alike set.** The memorisation gap only works if the look-alike digits differ from Carol's
in one way, whether the model trained on them. The course makes them with exactly the same marker effect.

**The score is costly to estimate.** Feldman's score needs many models trained with and without each example. That is
cheap for a network that trains in about a third of a second and out of reach for a large model.

**Small sets are noisy.** One of Carol's 40 digits is 2.5 points. Gaps of a few points between models can be luck.

**The course trains without regularisation, on purpose.** The course library sets its weight penalty to zero by
default, because an unregularised model memorises its training data, which is the behaviour unlearning has to deal
with. A real system may memorise less, but it should be measured, not assumed.

!!! tip "What to do in practice"
    - Measure memorisation on the people most likely to be memorised, not on random users.
    - Build a look-alike set for each forget set and report the gap before and after unlearning.
    - Use a per-example test, such as a membership attack, alongside average accuracy.
    - Expect flexible models, such as forests and networks, to remember individuals more than simple ones.

## In code

The memorisation gap is two accuracy numbers.

```python
from mul import lab, train
L = lab.make_lab("carol")
model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
gap = train.accuracy(model, L.Xf, L.yf) - train.accuracy(model, L.X_like_forget, L.y_like_forget)
print(f"memorisation gap: {gap:+.1%}")   # +22.5%
```

??? deep "Go deeper · Feldman's score in code"
    Lesson 04 trains 6 networks with the probe digits and 6 without, then subtracts the two rates.

    ```python
    import numpy as np
    from mul import lab, train
    L = lab.make_lab("carol")
    typical = np.random.default_rng(1).choice(L.retain_idx, 40, replace=False)
    probe = np.r_[L.forget_idx, typical]                        # Carol's 40 and 40 typical digits
    keep = np.setdiff1d(np.arange(len(L.X_train)), probe)
    right = lambda m: train.predict(m, L.X_train[probe]) == L.y_train[probe]
    p_in = np.mean([right(train.fit(lab.model_fn, L.X_train, L.y_train, seed=s, **lab.FIT)) for s in range(6)], axis=0)
    p_out = np.mean([right(train.fit(lab.model_fn, L.X_train[keep], L.y_train[keep], seed=s, **lab.FIT)) for s in range(6)], axis=0)
    mem = p_in - p_out                                           # one score per probe digit
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing unlearning on random users only.** Random users are barely memorised, so almost any method looks like
      it works. Test on the hard, unusual cases.
    - **Thinking a good test score means no memorisation.** A model can have high test accuracy *and* memorise rare
      examples. Both happen at once.
    - **Comparing Carol with the ordinary test set.** Her digits are thick and the test digits are not, so the gap
      mixes style with memory. Use look-alike digits.
    - **Aiming for zero on the forgotten data.** A model that never saw Carol still reads 55.0% of her digits. The
      memorised part is the gap, not the whole score.

??? checkpoint "Checkpoint 3 · You must pick a model for a service where people often ask to be deleted. Using Lesson 04's numbers, which of Naive Bayes and a random forest remembers individuals more?"
    **The random forest, by far.** Its gap on Carol is +30.0 points, against −1.3 for Naive Bayes, and the loss attack
    scores 0.96 on it against 0.53. Naive Bayes is less accurate (91.1% against 97.2% on test digits), so the choice is
    a trade between accuracy and how much each person leaves behind.

## Key takeaways

!!! notes "Notes to take"
    - **Overfitting.** Much better on training data than on new data. The network's overall gap is only 2 points.
    - **Memorisation.** Right on an example *because* it was trained on. Carol's gap is 22.5 points.
    - **Memorisation gap.** Accuracy on someone's data minus accuracy on look-alikes, 100.0% minus 77.5% for Carol.
    - **Feldman's score.** \(P[\text{right} \mid \text{in}] - P[\text{right} \mid \text{out}]\). About 0 for typical digits, often high for Carol's.
    - **Long tail.** Rare cases must be memorised to be learnt. Carol has 3 × the leverage, and 97.5% of her digits are support vectors.
    - **Flexibility.** Gaps run from −1.3 for Naive Bayes to +30.0 for the random forest.
    - **After retraining.** 55.0% on Carol against 62.5% on look-alikes, so the gap has gone but the score is not zero.
    - **Trap.** A high test score says nothing about memorising one person.
    - **Trap.** Random users are barely memorised, so test unlearning on unusual cases.

## Quiz

```quiz
- q: Which student in the example overfitted?
  options:
    - The one who understood the methods
    - The one who memorised last year's answers
  answer: 1
  why: They fit the practice paper perfectly but cannot handle new questions.
- q: Feldman's memorisation score for a typical digit is usually...
  options:
    - About 0
    - About 1
    - Negative and large
  answer: 0
  why: Thousands of similar digits teach the same pattern, so the model gets it right whether or not that digit was in training.
- q: Which data is memorised the most?
  options:
    - Typical, common examples
    - Unusual examples, like Carol's thick-marker digits
    - Test data
  answer: 1
  why: Nothing else in the data teaches the model about rare cases, so it has to memorise them.
- q: Why is testing an unlearning method only on random users a mistake?
  options:
    - Random users are barely memorised, so almost any method looks successful.
    - Random users cannot ask for deletion.
    - Random users are always in the test set.
  answer: 0
  why: The real test is on memorised, unusual data, where forgetting actually has to do work.
- q: The network is right on 100% of its training digits and 98.0% of its test digits. What does this tell you about Carol?
  options:
    - She is certainly forgotten.
    - The model cannot have memorised anyone.
    - Very little, because an average over many typical digits can hide one person who is remembered.
  answer: 2
  why: The same network has a 22.5-point gap on Carol's digits against look-alikes, which the overall numbers hide.
- q: A digit is right in all 6 networks trained with it and in 3 of 6 trained without it. What is its memorisation score?
  options:
    - "0.5"
    - "0"
    - "1.0"
  answer: 0
  why: 6 ÷ 6 − 3 ÷ 6 = 1.0 − 0.5 = 0.5. Half of its correctness comes from having been seen.
- q: In Lesson 04, which model had the largest memorisation gap on Carol?
  options:
    - Naive Bayes
    - The random forest
    - k-NN with k = 5
  answer: 1
  why: The forest scored 100.0% on Carol against 70.0% on look-alikes, a gap of +30.0 points. It also leaked most to the attack in Lesson 05.
- q: After retraining without Carol, the network reads 55.0% of her digits. Is that a sign that it still remembers her?
  options:
    - No, because it reads her look-alikes about as well, so the 55.0% comes from what it learnt from others.
    - Yes, because a forgotten person should score 0%.
    - Yes, because any score above 50% means memorisation.
  answer: 0
  why: Memory shows as the gap over look-alikes. After retraining it is 55.0% against 62.5%, so the special treatment is gone.
```

## Try it

!!! levelup "Level up"
    You can now measure what a model remembers about one person and explain why unusual people are remembered most.
    Next quest, [Probabilities and KL divergence](probabilities-and-kl-divergence.md), where you learn how to compare
    two models' answers number by number.

- Read the next page, [Probabilities and KL divergence](probabilities-and-kl-divergence.md).
- The lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md) measures memorisation for six models.
