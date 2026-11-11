---
title: Training data and test data
description: Why we split data into a training set and a test set, and how the course splits it further to see what a model remembers.
---

# Training data and test data

!!! oneline "In one line"
    We train a model on one part of the data and check it on a different part that it has **never seen**.

!!! mission "Your mission · about 12 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why a model must be scored on data it never trained on,
    - name the four sets the course uses, \(D\), \(D_f\), \(D_r\) and \(D_{\text{test}}\), with their sizes,
    - use a look-alike set to tell whether a model has memorised one person.

## Why it matters

A model can look perfect on the examples it trained on, simply because it remembers them. The only fair check is data
it has never seen. In unlearning, this idea goes one step further. We compare how the model treats data it trained on with how it treats similar data it never saw. A big difference is a sign that it remembers.

Here is how that plays out in the course. The digit network is right on every one of its training digits. On 540
digits it never saw, it is right 98.0% of the time. So its training score says almost nothing about how good it is,
and the test score is the honest one.

The same comparison, aimed at one person, becomes the main tool of unlearning. The network is right on all 40 of
Carol's digits, but only on 77.5% of unseen digits written in her style. That gap tells you the model remembers her.
After unlearning, the gap should be gone. Every check in the course, from the
[gold band](../unlearning/gold-band.md) to [membership inference attacks](../unlearning/membership-inference-attacks.md),
is a careful version of this one comparison.

## A simple example

Imagine a teacher who gives students the exact exam questions to practise. Every student scores 100%. Did they learn the
subject, or just memorise the answers? To find out, the teacher must use **new** questions on exam day.

- The practice questions are the **training set**.
- The new exam questions are the **test set**.

!!! simply "Explain it simply"
    Now suppose one student, Carol, brought her own practice sheet with unusual questions on it. To see whether the
    class just memorised *her* sheet, the teacher writes new questions in the same unusual style. If the class does
    much better on Carol's sheet than on the new questions in her style, they remember her sheet. Those new questions
    are what the course calls the **look-alike set**.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Training set \(D\) | The data the model learns from | 1,257 digits, Carol's 40 included |
| Test set \(D_{\text{test}}\) | Data kept aside and never used for training, to score the model fairly | 540 digits |
| [Forget set](../start-here/glossary.md#f) \(D_f\) | The part of the training set that someone asks us to remove | Carol's 40 thick-marker digits |
| [Retain set](../start-here/glossary.md#r) \(D_r\) | Everything in the training set except the forget set | The other 1,217 digits |
| Look-alike set | Unseen data in the same style as the forget set | 80 thick-marker digits the model never trained on |
| Stratified split | A split that keeps the same share of each label in both parts | Each digit, 0 to 9, is about 10% of both sets |
| Data leakage | Information from the test set reaching training, which makes the test unfair | Scaling all the data together before splitting |
| [Fingerprint](../start-here/glossary.md#f) | The gap between a model's score on someone's own data and on look-alike data | 100.0% on Carol against 77.5% on look-alikes |

## How it works

<!-- diagram: training-and-testing -->

The figure shows all the data split into two parts. The training set, on the left, goes into fitting the model. The
test set, on the right, is locked away until the end. Only the finished model is allowed to see it, and only to be
scored.

<ol class="steps" markdown>
<li markdown>**Shuffle the data** so both parts look alike.</li>
<li markdown>**Split it**, for example 70% for training and 30% for testing.</li>
<li markdown>**Train only on the training set.** The model must never see the test set during training.</li>
<li markdown>**Measure accuracy on the test set.** This tells you how well the model works on new data.</li>
</ol>

**For the digit lab this means** the 1,797 digits are shuffled and split 70 to 30, giving 1,257 training digits and
540 test digits. The split is stratified, so the test set has about as many 3s and 7s as the training set. The network
trains on the 1,257 and is scored on the 540, which it never sees until the end.

### The extra splits used in unlearning

In this course, the training set itself is split again.

| Name | Symbol | What it is | In the digit lab |
|---|---|---|---|
| Training set | \(D\) | Everything the model trained on | 1,257 digits |
| Forget set | \(D_f\) | The part someone asks us to remove | Carol's 40 digits |
| Retain set | \(D_r\) | Everything else in training | 1,217 digits |
| Test set | \(D_{\text{test}}\) | Data never used for training | 540 digits |

The course also keeps a small set of **unseen thick-marker digits**, written in Carol's style but never trained on.
Comparing the model on Carol's digits with these "look-alike" digits shows how much it memorised *her* in particular.
See [The notation](../unlearning/notation.md) for all the symbols.

Each set answers its own question.

- **The retain set** asks whether the model still works for everyone who stayed. A good unlearning method must not
  damage it.
- **The test set** asks whether the model still works on new data. This is its everyday usefulness, which the course
  calls **utility**.
- **The forget set** asks whether the model still remembers the person who left.
- **The look-alike set** gives the fair comparison for the forget set. Without it, you could not tell "remembers
  Carol" apart from "is simply good at thick digits".

### Why the look-alike set matters

Comparing Carol's digits with the ordinary test set would be unfair. Her digits are thick, and the test digits are
not, so any difference could come from the style alone. The look-alike set removes that doubt, because it has the same
style and differs only in one thing, whether the model trained on it.

**For Carol this means** the useful comparison is 100.0% on her digits against 77.5% on look-alikes, a gap of 22.5
points. That gap is her fingerprint in the model.

??? checkpoint "Checkpoint 1 · A model scores 100% on Carol's digits and 98.0% on the ordinary test set. Can you conclude that it barely remembers her?"
    **No.** The test digits are written in a normal style and Carol's are thick, so the two numbers measure different
    things. You need the look-alike set. In the course, the same model scores only 77.5% on unseen thick digits, which
    shows a 22.5-point gap that the test set hid.

## A worked example

Follow Carol's 40 digits through the four sets of Lesson 00.

1. **The split.** The 1,797 digits become 1,257 for training and 540 for testing. Carol's 40 digits are inside the
   1,257. The lab also makes 80 look-alike digits in her style that never enter training.
2. **The original model.** It trains on all 1,257 digits. On the retain set it is right 100% of the time (Lesson 06 prints this), and on the
   test set 98.0%. The small drop is normal and shows it has learnt a general rule.
3. **The fingerprint.** On Carol's 40 digits it is right 100.0% of the time, which is all 40. On the 80 look-alikes it
   is right 77.5% of the time, which is 62 of them. The forget set and the look-alike set should behave alike, and they
   do not.
4. **The request.** Carol asks to be deleted. Her 40 digits become the forget set, and the other 1,217 become the
   retain set.
5. **The retrained model.** A fresh network trains on the 1,217 retain digits only. It scores 55.0% on Carol and 62.5%
   on the look-alikes. Her digits now look like any other unseen thick digits, so the fingerprint has gone.
6. **The cost to everyone else.** On the test set it still scores 98.0%. Forgetting Carol did not make the model worse
   for anyone else.

| Model | Carol's digits (\(D_f\)) | Look-alike digits | Test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

Read the table across each row. In the first row, Carol is far above her look-alikes. In the second row, she is a
little below them, which is within normal variation for 40 digits. The test column does not move at all, which is why
it could never have told you whether Carol was forgotten.

??? checkpoint "Checkpoint 2 · Carol has 40 digits and the test set has 540. How much does one digit move each score?"
    **One of Carol's digits is worth 2.5 points, and one test digit about 0.19 points.** That is 100 ÷ 40 and
    100 ÷ 540. So a small forget set gives a jumpy score, and a difference of one or two of her digits is not
    meaningful on its own. This is one reason the course compares with several retrained models, as
    [the gold band](../unlearning/gold-band.md) explains.

## What the lesson found

<div class="stats">
<div><strong>1,257 / 540</strong><span>training and test digits, a 70 to 30 split</span></div>
<div class="is-good"><strong>98.0%</strong><span>on test digits, for both the original and the retrained model</span></div>
<div class="is-bad"><strong>100% vs 77.5%</strong><span>Carol against look-alikes, before unlearning</span></div>
<div class="is-good"><strong>55% vs 62.5%</strong><span>Carol against look-alikes, after retraining</span></div>
</div>

??? deep "Go deeper · how the lab builds the sets"
    The course library makes all of this in one call, `lab.make_lab("carol")`. It loads the 1,797 digits, scales
    each pixel to a number from 0 to 1 and makes a stratified 70 to 30 split with a fixed seed. Then it picks 40 of the
    training digits at random and redraws them in Carol's thick-marker style, which widens every stroke by one pixel.
    Those 40 become \(D_f\). For the look-alike set, it takes 80 digits from the test set and redraws them in the same
    style. The model never trains on either version of those 80.

    The lab has two more scenarios, used to show how much the choice of forget set matters.

    === "Random users"

        The forget set is 10% of the training rows, chosen at random. These digits are typical, so the model barely
        depends on any one of them, and the look-alike set is simply the test set. Lesson 05 shows that an attacker
        can hardly tell typical training digits from test digits, with an AUC of 0.53, where 0.5 is a coin flip.

    === "A whole class"

        The forget set is every training digit labelled 3. The test set then drops its 3s too, so utility is
        measured on the other nine digits, and the look-alike set is the test set's 3s. A model that never saw a 3
        can never predict "3".

    Because the lab is fixed by its seed, the same scenario always gives the same split. That is what lets every
    lesson compare its numbers with every other lesson.

## Limits

**A small test set is noisy.** With 40 forget digits, one digit is 2.5 points. Small differences between models can be
luck, so look at gaps of several digits, and compare with several retrained models.

**The test set must look like real use.** A test set drawn from the same digits as training tells you how the model
does on more of the same. It cannot tell you how it would do on, say, digits from a different country's handwriting.

**A test set that is used many times stops being unseen.** If you try many settings and keep whichever scores best on
the test set, you have tuned the model to that set. Its score is then too hopeful.

**The look-alike set has to be a true look-alike.** If it differs from the forget set in some way other than
"trained on or not", the gap measures that difference too. The course builds it with exactly the same marker effect as
Carol's digits for this reason.

!!! tip "What to do in practice"
    - Split the data before you do anything else, including scaling or choosing features.
    - Keep the test set locked away until the end, and score each final model on it once.
    - For an unlearning request, build a look-alike set from data the model never saw, in the same style as the
      forget set.
    - Report the forget set, look-alike set, retain set and test set side by side, as in the table above.
    - Remember that every person's share of a small set is large, and do not read much into one or two examples.

## In code

```python
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
print(len(X_train), len(X_test))   # 1257 540
```

`Stratify=y` keeps the same share of each digit in both parts. The course library builds all the splits for you.

```python
from mul import lab
L = lab.make_lab("carol")
print(L)   # Lab('carol': |D|=1257, |D_f|=40, |D_r|=1217, |test|=540)
```

??? deep "Go deeper · the four scores in code"
    `L.Xf` is the forget set, `L.Xr` the retain set and `L.X_like_forget` the look-alike set.

    ```python
    from mul import lab, train
    L = lab.make_lab("carol")
    model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)
    for name, X, y in [("Carol", L.Xf, L.yf), ("look-alikes", L.X_like_forget, L.y_like_forget),
                       ("retain", L.Xr, L.yr), ("test", L.X_test, L.y_test)]:
        print(f"{name:12s} {train.accuracy(model, X, y):.1%}")
    ```

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing on training data.** This hides memorisation, which is exactly what unlearning cares about.
    - **Letting test data leak into training**, for example by scaling all the data together before splitting. Even a
      scaler "learns" averages from the data it sees (Lesson 01 shows this).
    - **Comparing the forget set with the ordinary test set.** Carol's digits are thick and the test digits are not,
      so the difference mixes style with memory. Use a look-alike set.
    - **Checking only the test set after unlearning.** The test score was 98.0% both before and after Carol was
      forgotten, so it cannot tell you whether she was.

??? checkpoint "Checkpoint 3 · A pipeline scales every pixel using averages taken from all 1,257 training digits, then later forgets Carol. What else must be forgotten?"
    **The scaler.** Its stored averages were worked out with Carol's digits included, so they carry a small trace of
    her. In Lesson 01, refitting the scaler without her changed one of its stored means by as much as 0.0171. Anything that learnt from the
    training data, even a simple scaler, must be refitted or updated without the forget set.

## Key takeaways

!!! notes "Notes to take"
    - **Training set.** The data the model learns from, 1,257 digits in the lab.
    - **Test set.** Data kept aside to score the model fairly, 540 digits, never used for training.
    - **Unlearning splits.** \(D = D_r \cup D_f\), so 1,217 retain digits plus Carol's 40 forget digits.
    - **Look-alike set.** 80 unseen thick-marker digits, the fair comparison for Carol.
    - **Fingerprint.** 100.0% on Carol against 77.5% on look-alikes before unlearning, 55.0% against 62.5% after.
    - **Utility.** Test accuracy stayed at 98.0%, so retraining cost everyone else nothing.
    - **Small sets.** One of Carol's digits is 2.5 points, so do not read much into one or two digits.
    - **Trap.** Scaling before splitting leaks test data, and a scaler must be unlearnt too.
    - **Trap.** The test set cannot show whether someone was forgotten. Only the forget set and its look-alikes can.

## Quiz

```quiz
- q: Why do we keep a test set that the model never trains on?
  options:
    - To make training faster
    - To check how well the model works on new data
    - Because the test data is lower quality
  answer: 1
  why: A model can score well on data it has seen just by remembering it. Only unseen data shows real skill.
- q: Carol asks to be forgotten. Which set are her 40 digits?
  options:
    - The test set
    - The retain set
    - The forget set
  answer: 2
  why: The forget set \(D_f\) is the data that must be removed. Everything else in training is the retain set \(D_r\).
- q: How is the retain set related to the training set?
  options:
    - Retain set = training set minus the forget set
    - Retain set = test set
    - Retain set = forget set plus test set
  answer: 0
  why: 'The training set is the retain set plus the forget set, so \(D = D_r \cup D_f\).'
- q: A model scores 100% on Carol's digits but only 77.5% on unseen thick-marker digits. What does this suggest?
  options:
    - The model has memorised Carol's digits.
    - The test set is too small.
    - Thick-marker digits are always wrong.
  answer: 0
  why: It does much better on the exact digits it trained on than on similar new ones. That gap is memorisation.
- q: Why does the course compare Carol's digits with look-alike digits instead of the ordinary test set?
  options:
    - The ordinary test set is too large.
    - The look-alikes share her style, so the only difference left is whether the model trained on them.
    - Look-alike digits are easier to read.
  answer: 1
  why: Her digits are thick and ordinary test digits are not. Comparing with the same style isolates the effect of memory.
- q: Test accuracy was 98.0% both before and after Carol was forgotten. What does this tell you?
  options:
    - Unlearning failed.
    - The model was never trained on Carol.
    - Forgetting Carol did not hurt the model for everyone else.
  answer: 2
  why: The test set measures usefulness on new data. It shows the cost of unlearning, not whether Carol was forgotten.
- q: Why can scaling all the data before splitting be a problem?
  options:
    - The scaler learns averages that include the test data, so the test is no longer fully unseen.
    - Scaling makes the images too small.
    - Scaling changes the labels.
  answer: 0
  why: Anything fitted on the data learns from it. The split must come first so that nothing learns from the test set.
- q: Carol has 40 digits. How much does one of them move her accuracy score?
  options:
    - 0.4 points
    - 2.5 points
    - 25 points
  answer: 1
  why: 100 ÷ 40 = 2.5. A small forget set gives a jumpy score, so a gap of one or two digits is not meaningful alone.
```

## Try it

!!! levelup "Level up"
    You can now split data fairly and use a look-alike set to spot memorisation. Next quest,
    [Loss functions](loss-functions.md), where you see the single number that tells a model how wrong it is.

- Read the next page, [Loss functions](loss-functions.md).
- The lesson [00 · Read this first](../lessons/00-read-first.md) builds these splits with `lab.make_lab("carol")`.
