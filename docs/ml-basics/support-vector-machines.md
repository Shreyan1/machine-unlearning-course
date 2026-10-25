---
title: Support vector machines
description: An SVM draws the widest street between classes, and only the points on its edge, the support vectors, matter.
---

# Support vector machines (SVMs)

!!! oneline "In one line"
    An SVM draws the **widest possible street** between two classes, and only the points standing on the edge of that
    street, the **support vectors**, decide where it goes.

## Why it matters

SVMs show a powerful property called **locality**, which means that most training points have *zero* influence on the model. Deleting
one of those points is already unlearnt, for free. But they also show the catch that runs through the whole course.
Unusual data, like Carol's, is exactly the data the model leans on.

## A simple example

Picture red and blue houses on either side of a road. You want to build the widest road that keeps all the red houses on
one side and all the blue ones on the other. Only the houses right at the kerb decide where the road goes. You could
knock down any house further back, and the road would not move at all.

## How it works

<!-- diagram: support-vector-machines -->

<ol class="steps" markdown>
<li markdown>**Find the widest street** (called the *margin*) that separates the two classes.</li>
<li markdown>**The points on the kerb** are the support vectors. Every other point has zero weight in the final model.</li>
<li markdown>**Predict** by checking which side of the street a new point falls on.</li>
<li markdown>**Curved boundaries.** A "kernel" (such as the RBF kernel) lets the street bend, so the SVM can separate classes that a straight line cannot.</li>
</ol>

### Forgetting in an SVM

- **Deleting a non-support vector.** Nothing changes. In Lesson 03's 2-D example, the boundary moved by about
  2.3 × 10⁻⁸, which is just solver precision.
- **Deleting a support vector.** The boundary moves, so you must re-solve the SVM.

So "Do I need to do any work to forget this point?" Has a simple answer. **Only if it is a support vector.**

### Carol is almost all support vectors

In Lesson 03, **97.5%** of Carol's digits were support vectors, against **40.5%** of everyone else's. For 40 typical
users who were not support vectors, the original model was already the unlearnt model on 100% of inputs. For Carol,
the only exact option was to re-solve without her.

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

## Common mistakes

!!! danger "Mistakes people make"
    - **Assuming deletion is always free for SVMs.** It is free only for non-support vectors, and unusual data is
      usually a support vector.
    - **Forgetting the cost of re-solving.** Kernel SVMs can be slow to retrain on large datasets.

## Key takeaways

- Only the support vectors decide an SVM's boundary.
- Deleting a non-support vector is already unlearnt.
- Unusual data is far more likely to be a support vector, so it is the expensive data to forget.

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
```

## Try it

- Read the concept page [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
- Run the lesson [03 · SVM and random forest](../lessons/03-svm-and-random-forest.md).
