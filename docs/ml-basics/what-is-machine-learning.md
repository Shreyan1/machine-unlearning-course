---
title: What is machine learning?
description: Machine learning means learning rules from examples instead of writing them by hand.
---

# What is machine learning?

!!! oneline "In one line"
    Machine learning is a way of getting a computer to learn a rule from **examples**, instead of a person writing the
    rule by hand.

## Why it matters

Some rules are too hard to write down. Try writing exact instructions for telling a handwritten "4" from a "9". You
would need hundreds of special cases. Machine learning skips that. You show the computer thousands of labelled examples, and it finds the rule itself.

For this course, the important part is this: **the rule the computer finds is built out of the examples**. That is why
removing an example later is not simple.

## A simple example

Think of a child learning what a dog is. Nobody gives the child a definition. They see many dogs, and someone says "dog"
each time. After a while the child can spot a dog they have never seen before.

Machine learning works the same way:

| Child | Machine learning |
|---|---|
| Sees many animals | Reads many **examples** (the *training data*) |
| Hears "dog" or "not a dog" | Each example has a **label** (the right answer) |
| Builds a sense of "dog-ness" | Adjusts its **parameters** (numbers inside the model) |
| Spots a new dog | Makes a **prediction** on new data |

In the course, the examples are 8 × 8 pixel images of handwritten digits, and the labels are the digits 0 to 9.

## How it works

<ol class="steps" markdown>
<li markdown>**Collect examples with labels.** For example, 1,257 digit images, each marked with the digit it shows.</li>
<li markdown>**Pick a model.** A model is a recipe with adjustable numbers in it, called **parameters** or **weights**.</li>
<li markdown>**Train it.** The computer adjusts the weights again and again, so that the model's answers match the labels
better. (See [Gradient descent](gradient-descent.md).)</li>
<li markdown>**Test it.** Check the model on examples it has *never seen*, to make sure it learnt a general rule.
(See [Training data and test data](training-and-testing.md).)</li>
<li markdown>**Use it.** Give it new inputs and use its predictions.</li>
</ol>

!!! note "Words you will see a lot"
    - **Model**: the recipe plus its learnt numbers.
    - **Weights** or **parameters**: the learnt numbers inside the model.
    - **Training**: the process of finding good weights from the examples.
    - **Prediction**: the model's answer for a new input.
    - **Classification**: predicting a category, such as "which digit is this?".

## In code

This uses scikit-learn, a popular Python library, on the same digits the course uses:

```python
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression

X, y = load_digits(return_X_y=True)   # 1,797 images (64 pixels each) and their labels
model = LogisticRegression(max_iter=2000)
model.fit(X, y)                       # training: find good weights
print(model.predict(X[:5]))           # predictions for the first five images
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking the model stores a copy of the data.** Most models store only their weights. But those weights were
      shaped by the data, so the data's influence is still there.
    - **Judging a model on its training data.** A model can be perfect on examples it has seen and poor on new ones.
      Always test on unseen data.

## Key takeaways

- Machine learning finds a rule from labelled examples.
- The rule lives in the model's **weights**, which training adjusts.
- Because the weights are shaped by the examples, every example leaves a mark. Unlearning is about removing that mark.

## Quiz

```quiz
- q: What is the main difference between machine learning and normal programming?
  options:
    - Machine learning does not use a computer.
    - In machine learning, the computer learns the rule from examples.
    - Machine learning only works on images.
  answer: 1
  why: In normal programming a person writes the rule. In machine learning, the rule is found from labelled examples.
- q: What are a model's "weights"?
  options:
    - The size of the training data in megabytes
    - The learnt numbers inside the model
    - The labels of the examples
  answer: 1
  why: Weights (or parameters) are the adjustable numbers that training tunes.
- q: Why does this matter for unlearning?
  options:
    - Because the weights are shaped by every training example
    - Because models never change after training
    - Because labels are secret
  answer: 0
  why: Each example nudges the weights during training, so its influence stays in the model even after the example is deleted.
- q: In the course, what are the examples and labels?
  options:
    - Photos of animals, labelled by species
    - Handwritten digit images, labelled 0 to 9
    - Movie reviews, labelled good or bad
  answer: 1
  why: Most lessons use small 8 × 8 images of handwritten digits.
```

## Try it

- Next page: [Training data and test data](training-and-testing.md).
- Lesson: [00 · Read this first](../lessons/00-read-first.md) trains a digit model in one line of code.
