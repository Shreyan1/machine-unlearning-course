---
title: Support vector machines
description: An SVM draws the widest street between classes, and only the points on its edge, the support vectors, matter.
---

# Support vector machines (SVMs)

!!! oneline "In one line"
    An SVM draws the **widest possible street** between two classes, and only the points standing on the edge of that
    street, the **support vectors**, decide where it goes.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why most training points have no say at all in where an SVM's boundary goes,
    - decide whether forgetting a point costs nothing or needs a re-solve,
    - explain why Carol, unlike a typical user, is the expensive case.

## Why it matters

SVMs show a powerful property called **locality**, which means that most training points have *zero* influence on the model. Deleting
one of those points is already unlearnt, for free. But they also show the catch that runs through the whole course.
Unusual data, like Carol's, is exactly the data the model leans on.

That first point is a rare gift. In [k-NN](k-nearest-neighbours.md) and [Naive Bayes](naive-bayes.md) every training
point leaves a mark that must be removed, even if removing it is cheap. In [ridge regression](linear-and-ridge-regression.md)
every point is tied to every other through a matrix inverse. In an SVM, most points leave no mark on the model at all.

The catch is just as important. The points an SVM leans on are the hard, unusual ones near the boundary. Those are
often the very people who ask to be forgotten. So an engineer who gets an erasure request can answer "Does the model
need any work?" with a simple lookup, and the answer for an unusual user is usually yes.

## A simple example

Picture red and blue houses on either side of a road. You want to build the widest road that keeps all the red houses on
one side and all the blue ones on the other. Only the houses right at the kerb decide where the road goes. You could
knock down any house further back, and the road would not move at all.

!!! simply "Explain it simply"
    Most houses sit well back from the road, so knocking one down changes nothing. A few odd houses stand right at the
    kerb, or even in the road. Knock one of those down and the builders must plan the road again.

Now map the picture onto the course. The houses are training digits and the two colours are two classes. The road is
the **margin** and the houses at the kerb are the **support vectors**. Knocking down a house is deleting a training
point. Carol's thick-marker digits are the odd houses. Her strokes make her digits look a little like other digits, so
they stand close to the road, where every one of them counts.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Support vector](../start-here/glossary.md#s) | A training point on the edge of the street, inside it or on the wrong side. The boundary depends on these points only | 39 of Carol's 40 digits |
| Margin | The empty street between the two classes. The SVM makes it as wide as it can | The space between the dashed lines in the figure |
| Decision boundary | The line, or curve, down the middle of the street. Points on one side get one class | The solid line in the figure |
| Dual weight \(\alpha_i\) | A number the SVM gives each training point to say how much it counts. It is zero for every point that is not a support vector | 146 of the 200 toy points have \(\alpha_i = 0\) |
| C | A setting for how hard the SVM punishes points that sit inside the street or on the wrong side | C = 1 on the toy problem, C = 10 on the digits |
| Kernel | A way of scoring how similar two points are, which lets the street bend | The RBF kernel on the digits |
| [Locality](../start-here/glossary.md#l) | Only some parts of a model depend on a given point, so only those parts need work | Only support vectors need a re-solve |
| Re-solve | Training the SVM again on the data that is left | An SVM trained on the 1,217 digits that are not Carol's |

## How it works

<!-- diagram: support-vector-machines -->

The figure shows two classes of points, blue and yellow. The solid line is the decision line. The two dashed lines are
the edges of the margin, the empty street. The ringed points touch the street, and they are the support vectors. Only
three of the twelve points are ringed, and only those three decide where the line goes.

The method has four steps.

### Step 1. Find the widest street

Many lines can separate two classes. The SVM picks the one with the widest street (called the *margin*), because a wide
street leaves room for new points that look a little different from the training data.

Real data overlaps, so a perfect street rarely exists. The SVM lets some points sit inside the street or even on the
wrong side, and pays a penalty for each one. The setting **C** says how big that penalty is.

**For Carol this means** her thick strokes push her digits close to other classes, so they tend to land near the
street or inside it.

### Step 2. Find the points on the kerb

The solver gives every training point a weight \(\alpha_i\). A point well inside its own side gets a weight of exactly
zero. A point on the kerb, inside the street or on the wrong side gets a weight above zero. Those are the support
vectors. Every other point has zero weight in the final model.

In Lesson 03's 2-D toy problem, two overlapping clouds of 200 points, a linear SVM found 54 support vectors (27%). The
other 146 points had zero influence.

**For Carol this means** that 39 of her 40 digits got a weight above zero. Almost all of her data is part of the
model.

### Step 3. Predict

To predict a new point, the SVM checks which side of the street it falls on. In practice it adds up a weighted vote
of the support vectors, where each one votes more strongly the more the new point looks like it. A point with weight
zero adds nothing to that vote, so it might as well not be there. That is the whole reason forgetting can be free.

**For Carol this means** each of her 39 support vectors takes part in every prediction on a digit that looks like hers.

### Step 4. Curved boundaries

A "kernel" (such as the RBF kernel) lets the street bend, so the SVM can separate classes that a straight line cannot.
The RBF kernel scores two points as similar when they are close together. A setting called gamma controls how quickly
that score falls with distance.

**For Carol this means** Lesson 03 uses an RBF kernel with C = 10 on all ten digits, so the street curves through the
64 pixel values of each 8 × 8 image.

??? deep "Go deeper · why a zero weight means zero influence"
    The SVM's prediction for a new point \(x\) is

    \[
    f(x) = \sum_i \alpha_i \, y_i \, K(x_i, x) + b
    \]

    where \(y_i\) is the class of training point \(i\) (+1 or −1), \(K\) is the kernel and \(b\) is a shift. Every point
    with \(\alpha_i = 0\) drops out of the sum.

    The weights come from a set of conditions that the best street must meet, called the KKT conditions. If you remove a
    point whose \(\alpha_i\) is zero, the old solution still meets every condition for the smaller problem, so it is
    still the best street. Nothing needs to move.

    Removing a support vector breaks those conditions, so the solver must run again. Other points can then become
    support vectors, because the street can move towards them. That is why you cannot simply drop one term from the sum.
    Lesson 03's notebook notes that the re-solve can also be done step by step, with the decremental SVM of
    Cauwenberghs and Poggio (2000).

    **Ten classes.** An SVM separates two classes. For ten digits, scikit-learn trains a small SVM for each pair of
    digits, and a point counts as a support vector if any of them leans on it. That is one reason why so many digits,
    40.5% of everyone else's, are support vectors.

### Forgetting in an SVM

- **Deleting a non-support vector.** Nothing changes. In Lesson 03's 2-D example, the boundary moved by about
  2.3 × 10⁻⁸, which is just solver precision.
- **Deleting a support vector.** The boundary moves, so you must re-solve the SVM.

So "Do I need to do any work to forget this point?" Has a simple answer. **Only if it is a support vector.**

The two numbers show how sharp the difference is. Deleting the support vector with the largest weight moved the
boundary weights by 1.1 × 10⁻³. That is 1.1 × 10⁻³ ÷ 2.3 × 10⁻⁸, nearly 50,000 times the change from the other deletion.

| What you delete | Its weight \(\alpha_i\) | What happens to the street | Work needed |
|---|---|---|---|
| A point well inside its own side | Zero | Nothing | None |
| A support vector | Above zero | It moves | Re-solve |
| A group of points | Check each one | It moves if any of them is a support vector | Re-solve if any is |

??? checkpoint "Checkpoint 1 · Two requests arrive for the toy problem. One point sits far from the street, the other is ringed. Which one needs work?"
    **Only the ringed point.** The point far from the street has \(\alpha_i = 0\), so deleting it moved the boundary by
    2.3 × 10⁻⁸, which is solver noise. The original model already is the unlearnt model for that request. The ringed
    point is a support vector, so the street moves and you must re-solve.

### Carol is almost all support vectors

In Lesson 03, **97.5%** of Carol's digits were support vectors, against **40.5%** of everyone else's. This is the same
story as [leverage](linear-and-ridge-regression.md) in Lesson 02, told by a different model. Unusual data is exactly the
data a model leans on, and so it is exactly the data that is expensive to forget.

Why are her digits on the kerb? A typical "7" looks like hundreds of other 7s, so the SVM can draw the street well
away from it. Carol's thick-marker 7 looks partly like other digits, so the street has to pass close to it, and
sometimes cannot avoid it at all.

??? checkpoint "Checkpoint 2 · A colleague says Carol is only 40 of 1,257 digits, about 3%, so the SVM barely depends on her. What is wrong?"
    **Her share of the support vectors is much larger.** About 40.5% of the 1,217 other digits are support vectors,
    which is roughly 493. Add Carol's 39 and there are about 532. Carol's share is 39 ÷ 532, about 7%, more than
    twice her share of the data. The model depends on her more than on a typical writer, not less.

## A worked example

Follow Carol through Lesson 03.

1. **Train.** An RBF SVM is trained on all 1,257 digits, including Carol's 40. It gets 100.0% of her digits right and
   99.4% of the test digits.
2. **Check her rows.** 39 of her 40 digits are support vectors. Her request cannot be free.
3. **See what the model knows about her.** A model that never saw Carol gets only 57.5% of her digits right. So the
   original's 100.0% is something it learnt from her. Her digits also taught it her style. On 80 unseen thick-marker
   digits, the original scores 87.5% and the model without her only 48.8%.
4. **Compare a typical user.** Lesson 03 deletes 40 typical digits that are not support vectors and trains again. The
   new model's predictions match the original on 100.0% of 1,877 inputs. For them, the original model already *is*
   the unlearnt model. Zero work.
5. **Re-solve for Carol.** The only exact option is to train again on the 1,217 digits that are left. Here that takes
   a fraction of a second. The result scores 57.5% on Carol and still 99.4% on the test set.

Step 3 has a cost worth noticing. Forgetting Carol makes the model worse for everyone who writes like her, because she
was its main source of that style. Lesson 01 saw the same thing with Naive Bayes.

## What the lesson found

<div class="stats">
<div><strong>54 of 200</strong><span>toy points that are support vectors, the rest have zero influence</span></div>
<div class="is-good"><strong>2.3 × 10⁻⁸</strong><span>boundary change after deleting a non-support vector</span></div>
<div class="is-bad"><strong>97.5%</strong><span>of Carol's digits are support vectors, against 40.5% of others</span></div>
<div class="is-good"><strong>100.0%</strong><span>predictions unchanged after deleting 40 typical users</span></div>
</div>

| Model on the digits | Carol's digits | Unseen thick-marker digits | Test digits |
|---|---|---|---|
| Original, trained with Carol | 100.0% | 87.5% | 99.4% |
| Re-solved without Carol | 57.5% | 48.8% | 99.4% |

The test column does not move, so typical users are served just as well. All the change is on Carol and on people
who write like her.

## Limits

**Free only for a fixed kernel.** With `gamma="scale"`, scikit-learn sets the kernel's width from the training data.
Deleting any point nudges that width a little, so in theory nothing is perfectly free. That is why Lesson 03 checks
that the predictions stay the same rather than assuming it.

**Re-solving can be slow.** On the course's 1,257 digits it takes a fraction of a second. For kernel SVMs the cost grows
roughly with the square or the cube of the number of training points, so at scale a re-solve is a real job.

**The list of support vectors belongs to one model.** Change C, the kernel or the data and a different set of points
ends up on the kerb. A point that was free to delete last month may not be free today, so check against the model you
are running now.

**Zero influence is not zero copies.** A non-support vector has no say in the boundary, but its row is still in the
database, the logs and any scaler fitted on the data. See [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md#do-not-forget-the-pipeline).

!!! tip "What to do in practice"
    - Before you touch the model, look up whether any of the request's rows are in the model's list of support vectors.
    - If none of them are, the model needs no change. Delete the rows from storage and check that the predictions match.
    - Fix gamma to a number at training time if you want deleting a non-support vector to be exactly free.
    - Expect unusual users to need a re-solve, and plan time and compute for it.
    - Unlearn the rest of the pipeline too, such as scalers and feature selection.

??? checkpoint "Checkpoint 3 · Your SVM sets gamma from the data. A typical user's five rows are all non-support vectors, and your manager says no work is needed. What would you add?"
    **Two things.** First, the model may need no change, but the rows must still go from storage and from anything else
    fitted on the data. Second, because the kernel width comes from the data, confirm it. Train once without the rows
    and check that the predictions match, as Lesson 03 did with 100.0% on 1,877 inputs, or fix gamma in future.

## In code

```python
from sklearn.svm import SVC
from mul import lab
L = lab.make_lab("carol")
svc = SVC(kernel="rbf", C=10, gamma="scale").fit(L.X_train, L.y_train)
is_sv = set(svc.support_)                       # indices of the support vectors
carol_sv = sum(i in is_sv for i in L.forget_idx)
print(f"{carol_sv} of Carol's 40 digits are support vectors")
```

`svc.support_` lists the positions of the support vectors in the training data. Checking a request against it is the
lookup from "What to do in practice".

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming deletion is always free for SVMs.** It is free only for non-support vectors, and unusual data is
      usually a support vector.
    - **Forgetting the cost of re-solving.** Kernel SVMs can be slow to retrain on large datasets.
    - **Reading 2.3 × 10⁻⁸ as a real change.** It is the solver's own precision. Compare it with the 1.1 × 10⁻³ from
      deleting a support vector.
    - **Keeping a list of "free" users for ever.** Support vectors change whenever the model is trained again.
    - **Stopping at the model.** A point with zero weight is still stored in the data and in the preprocessing.

## Key takeaways

!!! notes "Notes to take"
    - **Support vectors.** The points on the edge of the street, inside it or on the wrong side. Only they decide the boundary.
    - **Rule.** Weight \(\alpha_i = 0\) means zero influence, so deleting that point needs no work.
    - **Toy problem.** 54 of 200 points were support vectors. Deleting a non-support vector moved the boundary by 2.3 × 10⁻⁸.
    - **Support vector deleted.** The boundary moved by 1.1 × 10⁻³, so you must re-solve.
    - **Carol.** 97.5% of her digits were support vectors, against 40.5% of everyone else's.
    - **Typical users.** Deleting 40 non-support vectors left predictions identical on 100.0% of inputs.
    - **Re-solved without Carol.** 57.5% on her digits, 99.4% on the test set, unchanged.
    - **Trap.** With `gamma="scale"` the kernel depends on the data, so check rather than assume.
    - **Trap.** Unusual data is the expensive data to forget, and it is often the data people ask about.

## Quiz

```quiz
- q: In the road picture, which houses decide where the road goes?
  options:
    - All of them equally
    - Only the ones right at the kerb
    - Only the ones furthest away
  answer: 1
  why: The houses at the kerb are the support vectors. The others could vanish without moving the road.
- q: You delete a training point that is not a support vector. What must you do to the SVM?
  options:
    - Nothing; it is already unlearnt.
    - Retrain it from scratch.
    - Delete every support vector too.
  answer: 0
  why: Non-support vectors have zero weight in the model, so removing one leaves the boundary unchanged.
- q: What share of Carol's digits were support vectors?
  options:
    - About 10%
    - About 40%
    - 97.5%
  answer: 2
  why: Unusual data is what the model leans on. Only 40.5% of everyone else's digits were support vectors.
- q: What property makes forgetting cheap for SVMs?
  options:
    - Locality
    - A huge Hessian
    - Gradient ascent
  answer: 0
  why: Most points have no influence on the model, so only a small part of the data ever needs work.
- q: Deleting a support vector in the toy problem moved the boundary weights by 1.1 × 10⁻³. What must you do?
  options:
    - Nothing, because the change is only rounding
    - Delete the points next to it as well
    - Re-solve the SVM on the points that are left
  answer: 2
  why: A support vector has a weight above zero, so removing it moves the street. Rounding noise was 2.3 × 10⁻⁸, about 50,000 times smaller.
- q: Why are unusual digits like Carol's more likely to be support vectors?
  options:
    - They are deleted more often than other digits.
    - They sit near the street or inside it, where the boundary is decided.
    - They have more pixels than other digits.
  answer: 1
  why: A typical digit sits far back on its own side. A digit that looks partly like another class forces the street to pass close to it.
- q: Lesson 03's SVM uses gamma set from the training data. Why does it still check predictions after deleting typical users?
  options:
    - Because the kernel width depends on the data, so any deletion can nudge it
    - Because SVMs are trained with random seeds
    - Because the test set changes after each deletion
  answer: 0
  why: In theory a non-support vector has no say only for a fixed kernel. The check showed predictions identical on 100.0% of inputs.
- q: After re-solving without Carol, the SVM scored 57.5% on her digits, against 100.0% before, and 99.4% on the test set both times. What does this show?
  options:
    - Re-solving damaged the model for everyone.
    - The re-solve failed and should be repeated.
    - The original had learnt Carol herself, and removing her left test accuracy unchanged.
  answer: 2
  why: A model that never saw her gets far fewer of her digits right, while test accuracy is unchanged. People who write like her do lose out, as the look-alike column shows.
```

## Try it

!!! levelup "Level up"
    You can now tell, for any request, whether an SVM needs work at all and why Carol does. Next quest,
    [Decision trees and random forests](decision-trees-and-random-forests.md), where locality is not a gift of the maths
    but something you design in.

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [03 · SVM and random forest](../lessons/03-svm-and-random-forest.md).
- In the Lesson 03 notebook, look for the typical user whose deletion moves the decision function most while not being
  a support vector. What does the theory predict you will find?
