---
title: What is machine learning?
description: Machine learning means learning rules from examples instead of writing them by hand, and every example leaves a mark on the model.
---

# What is machine learning?

!!! oneline "In one line"
    Machine learning is a way of getting a computer to learn a rule from **examples**, instead of a person writing the
    rule by hand.

!!! mission "Your mission · about 12 minutes · 3 checkpoints"
    By the end of this page you can

    - say what examples, labels, a model and its weights are, using the course's digit lab,
    - follow the five steps from labelled data to a prediction,
    - explain why deleting an example after training does not remove what the model learnt from it.

## Why it matters

Some rules are too hard to write down. Try writing exact instructions for telling a handwritten "4" from a "9". You
would need hundreds of special cases. Machine learning skips that. You show the computer thousands of labelled examples, and it finds the rule itself.

For this course, the important point is that **the rule a computer finds is built from examples**. That is why
removing an example later is not simple.

Think about what that means for a person whose data was used. In the course, a woman called **Carol** wrote 40 of the
digits the model learnt from, using a thick marker that nobody else used. The finished model gets every one of her 40
digits right. Then Carol asks to be deleted. Her rows can be removed from the database in a second, but the model was
already shaped by them. To understand why that is a problem, and how the rest of the course solves it, you first need
to see how a model is built from examples.

## A simple example

Think of a child learning what a dog is. Nobody gives the child a definition. They see many dogs, and someone says "dog"
each time. After a while the child can spot a dog they have never seen before.

Machine learning works the same way.

| Child | Machine learning |
|---|---|
| Sees many animals | Reads many **examples** (the *training data*) |
| Hears "dog" or "not a dog" | Each example has a **label** (the right answer) |
| Builds a sense of "dog-ness" | Adjusts its **parameters** (numbers inside the model) |
| Spots a new dog | Makes a **prediction** on new data |

In the course, the examples are 8 × 8 pixel images of handwritten digits, and the labels are the digits 0 to 9.

!!! simply "Explain it simply"
    A computer cannot see a picture. To the model, each digit is just a list of 64 numbers, one for each pixel, from 0
    for white to 1 for full ink. The label is one more number, the digit it shows. Learning means finding a way to turn
    the 64 numbers into the right label, for digits it has never seen.

The child also keeps something from every dog they met. A dog with an odd shape that they saw many times may stay in
their memory as "that dog", not just as "a dog". Models do the same with unusual examples, and that is where Carol's
problem begins.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Example | One piece of data the model learns from | One 8 × 8 image of a handwritten digit |
| Feature | One number that describes an example | The ink level of one pixel, so each digit has 64 |
| Label | The right answer for an example | The digit the image shows, from 0 to 9 |
| Model | A recipe with adjustable numbers in it, plus the numbers it has learnt | A neural network with layers of 64, 256, 256 and 10 neurons |
| [Weights (parameters)](../start-here/glossary.md#w) | The learnt numbers inside the model | The network has 85,002 of them |
| Training | The process of finding good weights from the examples | 60 passes over the 1,257 training digits |
| Prediction | The model's answer for a new input | "7" for a digit it has never seen |
| Classification | Predicting a category, such as "which digit is this?" | Reading which digit, from 0 to 9, an image shows |
| Accuracy | The share of predictions that are right | 98.0% on 540 test digits for the network in Lesson 00 |

## How it works

<!-- diagram: what-is-machine-learning -->

The figure has two rows. In the top row, examples with answers go into a learning algorithm, which adjusts the model
until it fits them. In the bottom row, the same finished model is given a new input and gives back a prediction. The
model does not change in the bottom row. Everything it knows was fixed in the top row.

<ol class="steps" markdown>
<li markdown>**Collect examples with labels.** For example, 1,257 digit images, each marked with the digit it shows.
In the course, 40 of these are Carol's.</li>
<li markdown>**Pick a model.** A model is a recipe with adjustable numbers in it, called **parameters** or **weights**.
The course's network starts with 85,002 random weights, so at first its answers are guesses.</li>
<li markdown>**Train it.** The computer adjusts the weights again and again, so that the model's answers match the labels
better. (See [Gradient descent](gradient-descent.md).) Carol's 40 digits push on the weights along with everyone
else's.</li>
<li markdown>**Test it.** Check the model on examples it has *never seen*, to make sure it learnt a general rule.
(See [Training data and test data](training-and-testing.md).) The course keeps 540 digits aside for this.</li>
<li markdown>**Use it.** Give it new inputs and use its predictions. Each answer comes from the weights, and the weights
came from the examples, Carol's included.</li>
</ol>

### Where the rule lives

Different kinds of model keep what they learn in different forms. This matters a great deal for unlearning, because
it decides what you would have to change to forget someone.

| Model | What it keeps after training | What forgetting Carol takes |
|---|---|---|
| [k-nearest neighbours](k-nearest-neighbours.md) | The training examples themselves | Delete her rows. In Lesson 01 this took 0.15 ms |
| [Naive Bayes](naive-bayes.md) | Three tables of counts and sums for each digit | Subtract her share of the sums |
| [Neural network](neural-networks.md) | 85,002 weights, each shaped by every example | No single place to edit. In Lesson 04, removing her changed 94.1% of them |

So "the model stores a rule" can mean very different things. For k-NN the rule is the data. For a neural network the
rule is a large set of numbers in which every example is mixed with every other. The course climbs from the easy end
of this table to the hard end, a path it calls the [Ladder of Forgetting](../unlearning/ladder-of-forgetting.md).

??? checkpoint "Checkpoint 1 · After training, which of these is the network's learnt rule, the 1,257 digits, the training code or the 85,002 numbers left at the end?"
    **The 85,002 numbers.** The digits are the examples it learnt from, and the code is the recipe for learning. What
    training leaves behind is the set of weights, and every prediction is worked out from them. The examples can be
    thrown away after training and the model still works, which is exactly why deleting them does not undo the
    learning.

## A worked example

Follow the five steps in Lesson 00, with Carol in the data.

1. **The examples.** The digit lab holds 1,797 images in all. 1,257 are kept for training, and 40 of those are
   Carol's thick-marker digits. The other 540 are kept aside for testing.
2. **The model.** A small neural network that reads 64 pixel values, passes them through two layers of 256 neurons
   and gives 10 scores, one per digit. The biggest score is the prediction.
3. **Training.** The network looks at the training digits in groups of 64 and nudges its weights after each group.
   That is 20 groups for one pass over the 1,257 digits, and it makes 60 passes, so about 1,200 nudges in all
   (1,257 ÷ 64 is about 19.6, which rounds up to 20, then 20 × 60 = 1,200). On a laptop this takes about a third of a
   second.
4. **Testing.** On the 540 test digits it has never seen, the network is right 98.0% of the time. It has learnt a
   general rule for reading digits.
5. **The mark Carol left.** On Carol's own 40 digits it is right 100.0% of the time. On 80 thick-marker digits it has
   never seen, written in her style, it is right only 77.5% of the time. The model has learnt *her* digits in
   particular, not just thick digits in general.

Now Carol asks to be deleted. Removing her rows from the database changes none of the 85,002 weights, so the model
still gets her digits 100.0% right. Lesson 00 then trains a fresh network on the 1,217 digits that are left. That model
scores 55.0% on her digits and 62.5% on the thick-marker look-alikes, while staying at 98.0% on the test set. Her
digits are now treated like any other unfamiliar thick digits.

??? checkpoint "Checkpoint 2 · The retrained model still gets 55.0% of Carol's digits right. Has it failed to forget her?"
    **No.** It never saw her digits, yet it can still read about half of them, because it learnt what digits look like
    from everyone else. What changed is the special treatment. Before, she scored 100.0% against 77.5% for look-alikes.
    After, she scores 55.0% against 62.5%. Forgetting means losing her particular influence, not becoming blind to
    her.

## What the lesson found

<div class="stats">
<div><strong>85,002</strong><span>weights in the course's network, all learnt from examples</span></div>
<div class="is-good"><strong>98.0%</strong><span>right on 540 test digits it never saw</span></div>
<div class="is-bad"><strong>100.0%</strong><span>right on Carol's 40 digits, against 77.5% on look-alikes</span></div>
<div class="is-bad"><strong>94.1%</strong><span>of the weights change when Carol is left out of training</span></div>
</div>

The first two tiles are what machine learning promises, a rule that works on new data. The last two are the cost that
this course is about. A model built from examples carries a mark from each of them, and for an unusual person like
Carol the mark is large and spread across almost every weight.

??? deep "Go deeper · six models on the same digits"
    Lesson 04 trains six kinds of model on exactly the same 1,257 digits and tests them on the same 540. They learn
    rules of very different shapes, yet most of them read new digits well.

    | Model | Test digits | Carol's digits | Unseen thick-marker digits |
    |---|---|---|---|
    | Naive Bayes | 91.1% | 60.0% | 61.3% |
    | k-NN, k = 5 | 98.3% | 75.0% | 67.5% |
    | Logistic regression | 97.2% | 92.5% | 77.5% |
    | RBF SVM | 99.4% | 100.0% | 87.5% |
    | Random forest | 97.2% | 100.0% | 70.0% |
    | Neural network | 98.0% | 100.0% | 77.5% |

    The last two columns compare Carol with strangers who write like her. The bigger the gap, the more the model has
    remembered her in particular. Naive Bayes, which keeps only averages, shows no gap at all. The flexible models show
    large ones. [Overfitting and memorisation](overfitting-and-memorisation.md) looks at this table closely.

## Limits

**It learns only what the examples show.** The network had seen no thick-marker digits except Carol's, so it read
unseen thick digits less well (77.5%) than ordinary ones (98.0%). A model is only as broad as its training data.

**The rule is hard to read.** You cannot open the network and find a line that says "a 7 has a bar on top". The rule
is spread across 85,002 numbers. That is also why you cannot simply find and cut out Carol's part.

**It learns the odd cases too.** Training rewards getting every example right, including the unusual ones. For a
typical digit, many similar digits teach the same thing. For Carol's digits, nothing else does, so the model has to
remember them one by one.

## In code

This uses scikit-learn, a popular Python library, on the same digits the course uses.

```python
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression

X, y = load_digits(return_X_y=True)   # 1,797 images (64 pixels each) and their labels
model = LogisticRegression(max_iter=2000)
model.fit(X, y)                       # training: find good weights
print(model.predict(X[:5]))           # predictions for the first five images
```

??? deep "Go deeper · the same steps with the course library"
    The course library builds the digit lab with Carol in it and trains the network with one recipe, used in every
    lesson from 04 to 11.

    ```python
    from mul import lab, train
    L = lab.make_lab("carol")                                    # 1,257 training digits, 40 of them Carol's
    model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)   # 60 epochs, batches of 64
    print(train.accuracy(model, L.X_test, L.y_test))             # 0.98 on the 540 test digits
    print(train.accuracy(model, L.Xf, L.yf))                     # 1.0 on Carol's 40 digits
    ```

    The 85,002 weights come from the layer sizes. Each layer has one weight for every pair of neurons it joins, plus
    one extra number (a bias) per neuron, so \(64 \times 256 + 256 + 256 \times 256 + 256 + 256 \times 10 + 10 = 85{,}002\).

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking the model stores a copy of the data.** Most models store only their weights. But those weights were
      shaped by the data, so the data's influence is still there.
    - **Judging a model on its training data.** A model can be perfect on examples it has seen and poor on new ones.
      Always test on unseen data.
    - **Thinking that deleting the data deletes the learning.** Removing Carol's rows after training leaves all
      85,002 weights as they were, so the model still gets her digits 100.0% right.
    - **Expecting a model that forgot someone to score zero on them.** A model that never saw Carol still reads 55.0%
      of her digits, because it learnt digits from everyone else.

??? checkpoint "Checkpoint 3 · You must forget Carol from a k-NN model and from the neural network. Which is easier, and why?"
    **The k-NN model.** It keeps the training examples themselves, so deleting her 40 rows gives exactly the model you
    would have built without her. The network mixed her digits into 85,002 shared weights, and leaving her out changes
    94.1% of them. There is no part of it you can simply delete.

## Key takeaways

!!! notes "Notes to take"
    - **Machine learning.** Finding a rule from labelled examples instead of writing it by hand.
    - **Example and label.** One 8 × 8 digit seen as 64 numbers, and the digit it shows.
    - **Weights.** The learnt numbers inside a model. The course's network has 85,002.
    - **Five steps.** Collect labelled data, pick a model, train, test on unseen data, then use it.
    - **Course numbers.** 1,257 training digits, 40 of them Carol's, and 540 test digits.
    - **Result.** 98.0% on test digits, 100.0% on Carol and 77.5% on digits like hers.
    - **Where the rule lives.** k-NN keeps the data, Naive Bayes keeps sums, a network mixes everything into weights.
    - **Trap.** Deleting the data after training leaves the weights, and her mark, unchanged.
    - **Target.** A model that never saw Carol still reads 55.0% of her digits, so forgetting is not scoring zero.

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
- q: Carol's rows are deleted from the database after the network is trained. What happens to its accuracy on her digits?
  options:
    - It drops to about 55%, like a model that never saw her.
    - It drops to 0%.
    - It stays at 100%, because the weights have not changed.
  answer: 2
  why: The model works from its weights, not from the database. Only training a new model without her brought her score down.
- q: To the course's network, what is one handwritten digit?
  options:
    - A list of 64 numbers, one for each pixel
    - A short description written by a person
    - A single number between 0 and 9
  answer: 0
  why: Each 8 × 8 image becomes 64 pixel values. The digit it shows is the label, which the model must learn to predict.
- q: Which model keeps the training examples themselves as its rule?
  options:
    - A neural network
    - k-nearest neighbours
    - Naive Bayes
  answer: 1
  why: k-NN answers by finding the most similar stored examples, so forgetting a person means deleting their rows.
- q: The network scores 100.0% on Carol's digits but 77.5% on unseen digits in her style. What does the gap show?
  options:
    - Thick-marker digits are impossible to read.
    - The model learnt her digits in particular, not just thick digits in general.
    - The test set is too small.
  answer: 1
  why: If it had only learnt the style, it would do about as well on strangers who write like her. The extra 22.5 points come from her own digits.
```

## Try it

!!! levelup "Level up"
    You can now describe how a model is built from labelled examples and why each example leaves a mark in its weights.
    Next quest, [Training data and test data](training-and-testing.md), where you learn how to check what a model has
    really learnt.

- Read the next page, [Training data and test data](training-and-testing.md).
- The lesson [00 · Read this first](../lessons/00-read-first.md) trains a digit model in one line of code.
