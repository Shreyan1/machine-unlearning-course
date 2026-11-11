---
title: Naive Bayes
description: Naive Bayes is a model built from counts, sums and averages, so forgetting a training example is an exact subtraction.
---

# Naive Bayes

!!! oneline "In one line"
    Naive Bayes learns the **average** look of each class from counts and sums, and picks the class whose average a new
    input fits best.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain what a Naive Bayes model stores, and why that makes it a sum over the data,
    - unlearn one example by hand with three subtractions,
    - tell memorising a person apart from being shaped by them, and spot the pipeline trap.

## Why it matters

Naive Bayes is where machine unlearning began. In 2015, Cao and Yang noticed that many models are built from **sums
over the training data**, and if a model is a sum, forgetting a data point is just a **subtraction**. Naive Bayes is the
clearest example.

That idea has a name in the course, the [summation form](../start-here/glossary.md#s). It is the reason the bottom rung
of the [Ladder of Forgetting](../unlearning/ladder-of-forgetting.md) is easy. A model in summation form can forget in a
fraction of a millisecond, with a result that is not just close to retraining but equal to it.

Naive Bayes is also a real tool. It is the classic spam filter, and it appears again in Lesson 14, where a spam filter
must forget 60 poisoned messages. Wherever a product keeps simple counts, such as how often a word appears in spam,
the same trick works.

## A simple example

A teacher keeps a running total of marks and a count of students for each class. To get the class average, they divide
the total by the count. If a student leaves, the teacher does not re-mark every paper; they simply subtract that
student's mark from the total and 1 from the count.

!!! simply "Explain it simply"
    The teacher's new average is exactly the average they would have got if the student had never joined. Nothing was
    estimated, and nobody else's mark was looked at again. That is exact unlearning, and it costs two subtractions.

Map the picture onto the course. Each school class is a **digit class**, from 0 to 9. A student's mark is one
**training digit**, and the running totals are the model's **sums**. The student who leaves is **Carol**, and the
subtractions are how Naive Bayes forgets her 40 digits.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Class | One of the answers the model can give | The ten digits, 0 to 9 |
| Count `n` | How many training examples a class has | Class 3 has 128 training digits |
| Sum `S1` | Each pixel's brightness, added up over a class | One total for each of the 64 pixels in each class |
| Sum of squares `S2` | Each pixel's brightness squared, added up over a class | Used to work out how much each pixel varies |
| Mean | A sum divided by its count, the average look of a class | `S1 / n` for each pixel |
| Variance | How much a pixel's brightness usually moves away from its mean | Worked out from `S2`, `S1` and `n` |
| Naive | Treating every pixel as if it had nothing to do with the others | Not true for handwriting, yet it works well enough |
| [Summation form](../start-here/glossary.md#s) | A model built from sums over the training data, so forgetting is a subtraction | Cao and Yang's idea, and the reason Naive Bayes forgets exactly |

## How it works

<!-- diagram: naive-bayes -->

The figure shows the classic use, a spam filter. Each word in an email is more or less common in spam than in normal
email, so each word gives its own small piece of evidence. Naive Bayes multiplies those pieces together, with how common
spam is overall, and picks the more likely answer. For digits, each pixel plays the part of a word.

For handwritten digits, Gaussian Naive Bayes keeps three things for **each digit class**.

| Stored number | Meaning |
|---|---|
| `n` | How many training examples the class has |
| `S1` | The sum of each pixel's brightness |
| `S2` | The sum of each pixel's brightness squared |

From these it computes each pixel's **average** (`S1 / n`) and how much it **varies** (from `S2`). To classify a new
digit, it asks which class's averages this image fits best. It is called *naive* because it treats every pixel
as independent of the others, which is not true, but works surprisingly well.

Here is the whole method in four steps.

### Step 1. Count and add up

Go through the training digits once. For each digit, add 1 to its class's count, add its 64 brightnesses to `S1` and add
their squares to `S2`. That is the entire training.

**For Carol this means** each of her 40 digits was added into the sums of its own class. In Lesson 01 the counts were
124, 127, 124, 128, 127, 127, 127, 125, 122 and 126 for the digits 0 to 9, which add up to the 1,257 training digits.
The whole model is those 10 counts and two tables of 10 × 64 sums.

### Step 2. Work out each class's average look

For each class and each pixel, the mean is `S1 / n`. The variance is `S2 / n` minus the mean squared. A class whose
pixel is always dark has a small variance there. A pixel that is sometimes dark and sometimes bright has a large one.

**For Carol this means** her thick strokes made the edges of every digit's average slightly brighter. That faint
brightening is her fingerprint inside the model.

### Step 3. Score a new digit against each class

For a new digit, Naive Bayes asks, pixel by pixel, how likely this brightness is under each class's bell-shaped curve.
Being naive, it multiplies the 64 answers together as if the pixels were unrelated. It also multiplies by how common
the class is in the training data.

### Step 4. Pick the best fit

The class with the highest score is the answer. Because every step only uses `n`, `S1` and `S2`, the model never needs
to look at a training digit again.

??? deep "Go deeper · the formulas, and why they make subtraction exact"
    For class \(c\) and pixel \(j\), the course library computes
    \(\mu_{cj} = S1_{cj} / n_c\) and \(\sigma^2_{cj} = S2_{cj} / n_c - \mu_{cj}^2 + \varepsilon\), where
    \(\varepsilon = 0.01\) is a small fixed amount (the `var_smoothing` setting) that stops a variance of zero.

    The score for class \(c\) is the log of its share of the training data plus a sum over the 64 pixels,
    \(\log \frac{n_c}{N} - \frac{1}{2} \sum_j \left( \frac{(x_j - \mu_{cj})^2}{\sigma^2_{cj}} + \log 2\pi\sigma^2_{cj} \right)\).
    Working in logs turns the multiplication of 64 small numbers into an addition, which computers handle more
    safely.

    Every quantity on the right is built from \(n\), \(S1\) and \(S2\). After you subtract a digit from those three, they
    hold exactly the numbers a fresh count over the remaining digits would give. So every mean, variance and score is
    exactly what a model trained without the digit would compute.

??? checkpoint "Checkpoint 1 · Class 3 holds 128 training digits. One of them is a Carol digit x. After you unlearn it, what changes?"
    **Three things, all in class 3.** The count becomes 127, `S1` for class 3 drops by `x` and `S2` drops by `x²`, pixel
    by pixel. The other nine classes are not touched. The new mean for class 3 is the new `S1` divided by 127, exactly
    as if that digit had never been counted.

### Forgetting in Naive Bayes

To forget a row, subtract its values from the model's counts and sums with `n -= 1`, `S1 -= x` and `S2 -= x²`. In Lesson
01, after subtracting Carol's 40 digits, the
largest difference from a model that never saw her, in any predicted log-probability, was **exactly 0**.

Compare the costs. The subtraction took **0.09 ms** and a full refit took **0.49 ms**. On the lab's 1,257 digits both
are tiny. What matters is how each one grows. The subtraction depends only on the 40 digits you remove. A refit depends
on every digit you keep, so on a billion rows it would take a billion additions, while the subtraction would still take
40.

Being exact also means there is nothing to measure afterwards except the proof. Naive Bayes has no random choices in
training, so a model trained without Carol is one clear thing, and the unlearnt model either matches it or does not.
The [gold band](../unlearning/gold-band.md) has width zero here. In Lesson 06, five retrains without her all score 27.5% on her
digits.

??? deep "Go deeper · when subtraction is not quite exact"
    **Smoothing that depends on all the data.** scikit-learn's `GaussianNB` sets its smoothing amount as
    `var_smoothing` times the largest variance of any pixel in the **whole** training set, worked out once, with Carol
    included. Subtracting her from the sums does not update that amount, so the result is close to a refit but not
    equal to it. The course library uses a fixed amount, 0.01, so nothing depends on her outside the sums.

    **Rounding error.** Computers store numbers with limited precision. After thousands of add-and-subtract cycles,
    small errors can build up, and `S2` is the most fragile, because the variance is a small difference between two
    large numbers. A difference of up to about \(10^{-12}\) from a fresh fit is possible. In Lesson 01 it was exactly zero.
    The notebook asks you to repeat the cycle 10,000 times and watch the error grow.

### Naive Bayes barely memorises

Because it keeps only averages, one person hardly moves it. In Lesson 01 its accuracy on Carol's digits (60.0%) was
about the same as on unseen thick-marker digits (61.3%). A neural network has a much wider gap, scoring 100% against
77.5%.

That difference has a name, the **memorisation gap**. It is the accuracy on a person's own digits minus the accuracy on
unseen digits like theirs. For Naive Bayes it is 60.0 − 61.3 = −1.3 points, so it does no better on Carol than on
strangers who write like her. For the neural network in Lesson 04 it is +22.5 points.

But "not memorised" does not mean "no influence". When Carol was removed, Naive Bayes got her digits right only 27.5%
of the time. She taught the model what thick-marker digits look like, even though it never learnt her digits one by
one.

!!! note "A side effect to watch"
    After forgetting Carol, the model got worse on everyone who writes like her (61.3% → 37.5% on unseen thick digits),
    because she was the only source of that style. When the people who ask to be forgotten are not a random sample,
    unlearning can hurt an under-represented group. Lesson 12 measures this.

??? checkpoint "Checkpoint 2 · Before unlearning, Naive Bayes read 60.0% of Carol's digits and 61.3% of look-alikes. Afterwards, 27.5% and 37.5%. Did it memorise her?"
    **No, but she shaped it.** Memorising means doing better on her own digits than on unseen digits like hers, and
    the gap was −1.3 points. Yet both numbers fell by more than 20 points when she was removed, because her digits
    were the model's only picture of the thick-marker style. A person can matter a lot to a model without being
    memorised by it.

## A worked example

Follow Carol through Part B of Lesson 01. Every number comes from the notebook.

1. **Training.** Naive Bayes counts and adds up 1,257 digits, hers included. The model is 10 counts, 640 sums and 640
   sums of squares.
2. **Before.** It reads 91.1% of the test digits, 60.0% of Carol's 40 digits (24 of them) and 61.3% of 80 unseen
   thick-marker digits (49 of them).
3. **Her fingerprint.** Comparing the class averages with and without her shows a faint brightening along the edges of
   every digit, made by her thick strokes.
4. **The request.** For each of her 40 digits, subtract 1 from its class count, the digit from `S1` and its square from
   `S2`. That took 0.09 ms.
5. **After.** The model reads 90.9% of test digits, 27.5% of hers (11 of 40) and 37.5% of the look-alikes (30 of 80).
6. **The proof.** A model counted from scratch on the 1,217 digits without her gives exactly the same three accuracies.
   The largest difference in any predicted log-probability, over 1,877 inputs, is exactly 0.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>exactly 0</strong><span>largest difference from a model that never saw Carol</span></div>
<div><strong>0.09 ms</strong><span>to subtract her 40 digits, against 0.49 ms to refit</span></div>
<div><strong>−1.3 points</strong><span>memorisation gap, so Naive Bayes barely memorised her</span></div>
<div class="is-bad"><strong>61.3% → 37.5%</strong><span>accuracy on unseen digits in her style</span></div>
</div>

| | Before | After | Never saw Carol |
|---|---|---|---|
| Carol's digits | 60.0% | 27.5% | 27.5% |
| Unseen thick digits | 61.3% | 37.5% | 37.5% |
| Test digits | 91.1% | 90.9% | 90.9% |

**The last two columns are equal on every row.** That is the proof of exact unlearning, and the log-probabilities agree
too, not just the final answers.

**Test digits barely moved**, by 0.2 points. Carol is about 3% of the data, and most people's digits look nothing like
hers.

**Unseen thick digits fell by 23.8 points.** This is the side effect from the note above. The people who write like
Carol lost the only examples of their style.

## Limits

**It only works while the model keeps its sums.** If a system stored only the final means and variances and threw
away the counts, it could not subtract anyone. Keep `n`, `S1` and `S2`, or anything else they can be rebuilt from.

**The naive guess costs accuracy.** Treating pixels as unrelated is why Naive Bayes reads only 91.1% of test digits,
against 98.3% for k-NN on the same data. Easy forgetting comes with a weaker model.

**The pipeline remembers too.** A scaler, a vocabulary or word counts built before the model are also fitted on the
data. In Lesson 01, a `StandardScaler` fitted with and without Carol differed by up to 0.0171 in a stored mean. The good
news is that these are sums too, so the same subtraction works on them.

??? checkpoint "Checkpoint 3 · A team subtracts a user from its Naive Bayes spam filter. The filter's vocabulary and its word weights were built from all messages, theirs included. Is the pipeline now exact?"
    **No.** The filter's counts are exact, but the vocabulary and the word weights still carry the user's messages. A
    word only they ever used may still be in the vocabulary. Each of those parts is built from counts over the
    messages, so each can be updated by subtracting the user's counts too. Only then is the whole pipeline the one
    that never saw them.

!!! tip "What to do in practice"
    - Store the counts and sums, not just the finished means and variances.
    - Unlearn every fitted step of the pipeline, such as scalers, vocabularies and word counts, not only the model.
    - Prove the result by comparing predicted log-probabilities with a model counted from scratch without the data.
    - Refit from scratch now and then to clear rounding error.
    - Check the accuracy for people like the deleted person, since they may lose their only examples.

## In code

```python
from mul import classical, lab
L = lab.make_lab("carol")
gnb = classical.GaussianNB(var_smoothing=1e-2).fit(L.X_train, L.y_train)
gnb.unlearn(L.Xf, L.yf)          # subtract Carol's rows from n, S1 and S2
```

??? deep "Go deeper · prove it, and the word-count version"
    ```python
    import numpy as np
    never = classical.GaussianNB(var_smoothing=1e-2).fit(L.Xr, L.yr)      # counted without Carol
    X_all = np.r_[L.X_train, L.X_test, L.X_like_forget]
    print(np.abs(gnb.predict_log_proba(X_all) - never.predict_log_proba(X_all)).max())   # 0.0
    ```

    The course library also has `classical.MultinomialNB` for word counts, the classic spam filter. It stores the
    number of messages and the count of each word for each class, and its `unlearn` method subtracts both. In Lesson 14,
    subtracting all 60 poisoned messages this way gave the clean filter bit for bit.

## Common mistakes

!!! danger "Mistakes people make"
    - **Forgetting the preprocessing.** A scaler, a vocabulary or word counts are also built from sums over the data.
      They must be unlearnt too.
    - **Ignoring rounding error.** After thousands of add-and-subtract cycles, small floating-point errors can build up,
      so systems refit from scratch now and then.
    - **Keeping only the averages.** Without the counts and sums, there is nothing to subtract from.
    - **Using smoothing worked out from all the data.** It still depends on the deleted rows, so the result is close
      but not exact.
    - **Reading "barely memorised" as "safe to ignore".** Naive Bayes did not memorise Carol, yet removing her moved
      its accuracy on her style by more than 20 points.

## Key takeaways

!!! notes "Notes to take"
    - **Naive Bayes.** Stores a count `n`, a sum `S1` and a sum of squares `S2` for each class, and nothing else.
    - **Naive.** Treats every pixel as unrelated, which costs accuracy (91.1% on test digits).
    - **Summation form.** A model built from sums forgets by subtraction, the idea of Cao and Yang (2015).
    - **Unlearning.** `n -= 1`, `S1 -= x`, `S2 -= x²` for each row. Exact, with a difference of exactly 0 in Lesson 01.
    - **Cost.** Grows with what you delete, not what you keep. 0.09 ms against 0.49 ms for a refit.
    - **Memorisation gap.** −1.3 points for Naive Bayes against +22.5 for a neural network.
    - **Influence is not memorisation.** Removing Carol dropped look-alikes from 61.3% to 37.5%.
    - **Trap.** Scalers and vocabularies are fitted on the data too and must be unlearnt.
    - **Trap.** Smoothing worked out from the whole data set, as in scikit-learn, breaks exactness.

## Quiz

```quiz
- q: What does Gaussian Naive Bayes store for each class?
  options:
    - Every training image
    - Counts, sums and sums of squares
    - A deep neural network
  answer: 1
  why: The whole model is n, S1 and S2 for each class; averages and spreads are computed from them.
- q: How do you make Naive Bayes forget a row?
  options:
    - Subtract the row from the counts and sums
    - Retrain the whole model
    - Delete the class
  answer: 0
  why: Because the model is built from sums, removing a row is a subtraction, with an exact result.
- q: Why did Naive Bayes barely memorise Carol?
  options:
    - It keeps only averages, which one person hardly moves.
    - It was not trained on her data.
    - It is a neural network.
  answer: 0
  why: Its accuracy on her digits (60.0%) was about the same as on look-alike digits it never saw (61.3%).
- q: What else, besides the model, must be unlearnt in a Naive Bayes pipeline?
  options:
    - Nothing
    - Preprocessing steps fitted on the data, such as scalers and vocabularies
    - The test set
  answer: 1
  why: Preprocessing is also "trained" on the data, so it carries the deleted rows' influence too.
- q: Why does the cost of unlearning by subtraction stay small as the training set grows?
  options:
    - It skips half of the classes.
    - It depends only on the rows you delete, not on the rows you keep.
    - It runs on a faster computer.
  answer: 1
  why: Removing Carol takes 40 subtractions whether the model was built from 1,257 rows or a billion.
- q: Naive Bayes barely memorised Carol, yet after unlearning its accuracy on unseen digits in her style fell from 61.3% to 37.5%. Why?
  options:
    - The subtraction had a rounding error.
    - The test set changed after unlearning.
    - She was the model's only source of that writing style.
  answer: 2
  why: Memorising is doing better on her own digits than on look-alikes. Shaping the model's picture of a style is a different kind of influence.
- q: A system keeps only the final mean and variance of each pixel and has thrown away the counts and sums. What goes wrong?
  options:
    - It can no longer remove a person by subtraction.
    - Nothing, the means are enough.
    - It forgets everyone at once.
  answer: 0
  why: Subtraction needs the count and the sums. Without them you cannot tell how much one row moved each average.
- q: Five retrains of Naive Bayes without Carol all score 27.5% on her digits. What does that tell you?
  options:
    - The retrains were broken.
    - Naive Bayes has no randomness in training, so its gold band has width zero.
    - Carol's digits are too hard to read.
  answer: 1
  why: With no random choices, retraining always gives the same model, so the unlearnt model can be checked for an exact match.
```

## Try it

!!! levelup "Level up"
    You can now unlearn by hand any model built from counts and sums, and prove the result is exact. Next quest,
    [Linear and ridge regression](linear-and-ridge-regression.md), where the sums get mixed together by a matrix
    inverse and forgetting needs one clever formula.

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [01 · k-NN and Naive Bayes](../lessons/01-knn-and-naive-bayes.md).
- In the notebook, unlearn and re-add Carol 10,000 times and plot how far the model drifts from a fresh fit.
- See how subtraction removes poisoned messages from a spam filter in Lesson 14,
  [Poisoned data and backdoors](../lessons/14-poisoned-data-and-backdoors.md).
