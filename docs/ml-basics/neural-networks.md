---
title: Neural networks
description: A neural network is layers of numbers trained together by gradient descent, so every example nudges almost every weight and one person's data ends up everywhere.
---

# Neural networks

!!! oneline "In one line"
    A neural network is a stack of **layers of numbers** that turns an input into an answer, and training nudges *all*
    of those numbers for every batch of examples.

## Why it matters

Neural networks power almost all modern AI, from image recognition to chatbots. They are also where unlearning gets
hard. Every trick that worked for classical models (subtract a sum, take a Newton step, rebuild only the part a point
touched) fails here. Understanding why is the turning point of the course.

The reason is simple to say and hard to undo. A classical model such as Naive Bayes keeps a few totals, so one person's
share sits in a place you can find. A neural network keeps no totals. It keeps tens of thousands of numbers, and each
training example pushes on nearly all of them at once. After training, nobody can point to the part that came from one
person.

This matters to anyone who trains a network on data about people. When someone asks to be erased, the company must
remove what the model learnt from them, not only their rows in a database. If the team does not understand how a
network stores what it learns, it will try shortcuts that look sensible and do not work, such as hunting for "the
person's weights" or comparing weights to prove the person is gone.

## A simple example

!!! simply "Explain it simply"
    Think of a big mixing desk in a recording studio, with thousands of knobs. Sound goes in one end and music comes out
    the other. Training means turning every knob a tiny bit, over and over, until the music sounds right. Once that is
    done, you cannot point to "the knob for the drums". Every knob affects every part of the sound.

Here is how the picture maps onto the real thing. The **sound going in** is the input, such as the 64 pixels of a
handwritten digit. The **music coming out** is the answer, a score for each of the ten digits. Each **knob** is one
weight, a number the network learns. The **sound engineer** who keeps turning the knobs is the training method,
[gradient descent](gradient-descent.md). Each **song played during practice** is a training example. Carol's 40
digits are a few songs in the practice set. Every time one of them is played, the engineer turns nearly every knob a
little, so her songs leave a trace on the whole desk.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Neuron** | A small unit that multiplies each input by a weight, adds the results, adds one more number and passes the total on | Each hidden layer of the course network has 256 neurons |
| **Layer** | A row of neurons that all read the same inputs. Data flows from the input layer through the hidden layers to the output layer | `MLP(64 -> 256 -> 256 -> 10)` has an input layer, two hidden layers and an output layer |
| [**Weight**](../start-here/glossary.md#w) | A number the network learns. Every connection between two neurons has one. Also called a parameter | The course network has 85,002 of them |
| **Bias** | The extra number each neuron adds after its weighted sum, so that it can switch on more or less easily | Each of the 256 neurons in a hidden layer has one bias |
| **Activation** | The simple bend a neuron applies to its total. The course uses ReLU, which keeps a positive number and turns a negative one into 0 | A total of 0.3 stays 0.3, and a total of −0.4 becomes 0 |
| **Forward pass** | Running an input through every layer, from left to right, to get the output | 64 pixels go in and 10 scores come out |
| [**Softmax**](../start-here/glossary.md#s) | A step that turns the 10 raw scores into 10 probabilities that add up to 1 | It might give 0.90 to "7" and 0.05 to "1" |
| [**Cross-entropy loss**](../start-here/glossary.md#c) | One number that says how wrong the network is. It is small when the right answer gets a high probability | A probability of 0.90 on the right digit gives a loss of 0.11 |
| **Backpropagation** | The method that works out, for every weight, which way it should move to lower the loss. It passes the error backwards through the layers | `model.backward()` in `mul/nn.py` returns one gradient per weight |
| [**Epoch**](../start-here/glossary.md#e) | One full pass over the training data, done in small groups called mini-batches | The course trains for 60 epochs with mini-batches of 64 |

## How it works

<!-- diagram: neural-networks -->

The figure shows a small network with four columns of circles. On the left are the input units, which hold the
features. In the middle are two hidden layers. The first finds simple patterns and the second combines them. On the
right are the output units, which give the answer. Every circle in one column is joined by a line to every circle in
the next column, and each line carries a weight. Information flows from left to right, and training adjusts every one of
those lines.

### Step 1. The input layer

The input layer holds the raw data and does no work of its own. In the course, each digit is a tiny 8 × 8 picture, so
it has 64 pixels. Each pixel is a number between 0 (blank) and 1 (fully inked). The network sees a digit only as this
list of 64 numbers. Carol's digits are the same kind of list, but her thick marker inks more pixels, because every
stroke is one pixel wider.

### Step 2. A neuron and its weights

A neuron does three small things. It multiplies each input by its own weight, adds up the results and then adds one
more number called the **bias**. The weights decide how much the neuron cares about each input. A large positive weight
means "this pixel being inked pushes me up". A negative weight means "this pixel being inked pushes me down".

Here is one neuron with only three inputs. These numbers are made up to show the arithmetic.

| Input (pixel value) | Weight | Input × weight |
|---|---|---|
| 0.0 | 0.4 | 0.0 |
| 0.5 | −0.2 | −0.1 |
| 1.0 | 0.3 | 0.3 |
| Bias | | 0.1 |
| **Total** | | **0.3** |

A real neuron in the first hidden layer of the course network does the same thing with 64 inputs instead of three.

### Step 3. The activation (the bend)

If a neuron only added things up, a stack of layers would be no smarter than one layer, because sums of sums are still
sums. So each hidden neuron applies a simple bend to its total, called the **activation**. The course uses **ReLU**,
which means "keep the total if it is positive, otherwise output 0". The neuron above had a total of 0.3, so it outputs
0.3. If its total had been −0.4, it would output 0 and pass nothing on for this input. This small bend is what lets a
network learn curved, complicated patterns, such as the many ways people write a 7.

### Step 4. Hidden layers, stacked

A **layer** is a row of neurons that all read the same inputs. The course network has two hidden layers of 256 neurons
each. Every neuron in the first hidden layer reads all 64 pixels. Every neuron in the second hidden layer reads all 256
outputs of the first. This is called a **fully connected** network, and it is why the number of weights grows so fast.

| Connection | Weights | Biases | Total |
|---|---|---|---|
| 64 pixels → hidden layer 1 (256) | 64 × 256 = 16,384 | 256 | 16,640 |
| Hidden layer 1 → hidden layer 2 (256) | 256 × 256 = 65,536 | 256 | 65,792 |
| Hidden layer 2 → 10 outputs | 256 × 10 = 2,560 | 10 | 2,570 |
| **Whole network** | | | **85,002** |

So the course network is written as `MLP(64 -> 256 -> 256 -> 10)` and has **85,002** weights (counting the biases). It
is written in plain NumPy in `mul/nn.py`, so every step, including every gradient, is a line of code you can read.

### Step 5. The output layer and the forward pass

The last layer has 10 neurons, one per digit, and no bend. Its 10 raw scores are called **logits**.
[Softmax](probabilities-and-kl-divergence.md) turns them into 10 probabilities that add up to 1. The network's answer
is the digit with the highest probability.

Running a digit through all the layers, from the pixels to the probabilities, is called the **forward pass**. It is
the only thing a trained network does when you use it. It never looks at the training data again. It only uses its
weights.

### Step 6. The loss

To learn, the network needs to know how wrong it is. The [cross-entropy loss](loss-functions.md) looks at the
probability the network gave to the **right** digit. If that probability is 0.90, the loss is 0.11. If it is 0.50, the
loss is 0.69. If it is 0.10, the loss is 2.30. A confident right answer costs almost nothing, and a confident wrong
answer costs a lot. Training tries to make the average loss over the training data as small as possible.

### Step 7. Training with backpropagation

Training is [gradient descent](gradient-descent.md) on the loss. The network starts with random weights. Then it
repeats four moves.

1. Take a **mini-batch** of 64 training digits.
2. Do a forward pass and measure the loss.
3. Run **backpropagation**. It starts at the output, where the error is, and passes it backwards layer by layer. On the
   way it works out a **gradient** for every weight, which says which way that weight should move to lower the loss and
   by how much.
4. Move every weight a small step in its downhill direction.

The course uses **Adam**, a popular version of gradient descent that gives each weight its own step size from a running
average of its recent gradients. The recipe is fixed for the whole course, namely 60 epochs, mini-batches of 64 and a
learning rate of 0.001. With 1,257 training digits, one epoch is 20 mini-batches, so training takes 1,200 steps.

### Why neural networks are hard to unlearn

Two facts from the steps above explain why one person's data ends up spread over all the weights.

**Every example reaches almost every weight.** The network is fully connected. When Carol's digit is in a mini-batch,
its error flows back through every layer, and most weights get a small push from it. There is no wall that keeps her
digit inside one part of the network.

**Every step starts where the last one ended.** The weights after step 500 depend on the weights after step 499, which
depend on step 498, and so on back to the start. If Carol's digit nudged the weights at step 10, all 1,190 later steps
began from a slightly different place. Her influence is carried along the whole path, and Adam's running averages
carry it forward too.

Lesson 04 tests each classical trick and finds that all three fail.

| Trick | Why it fails in a neural network |
|---|---|
| **Subtract** the person's contribution | Removing Carol changes **94.1%** of the 85,002 weights. Her influence is everywhere. |
| **One Newton step** to the new answer | It needs a table of 85,002 × 85,002 numbers, about 29 GB. And there is no single best answer to step to. |
| **Rebuild only the part** she touched | She touched every part. |

A **Newton step** is a jump straight to the best answer, worked out from the curvature of the loss. The table of
curvatures is called the Hessian. For the course network it has 7,225,340,004 entries. For a 7-billion-weight language
model it would be about 98 exabytes.

### Many equally good networks

A neural network's loss has many valleys, not one bowl. Two networks trained on the same data with different random
starts end up in different places, yet are equally accurate. In Lesson 04, two such networks reached 98.0% and 98.7% on
the test digits. They were further apart (distance 50.96) than the with-Carol and without-Carol pair (distance 9.87).
Here "distance" means the size of the gap between the two full lists of 85,002 weights. Changing only the random start
moved the weights about five times further than removing Carol did.

So there is no single "retrained model" to compare against. There is a whole **spread** of them. That is why proof of
forgetting must be about **behaviour**, measured against a [gold band](../unlearning/gold-band.md).

### Neural networks memorise more

More flexible models remember individuals more. In Lesson 04, the network was right on 100% of Carol's digits but only
77.5% of look-alike digits, a gap of +22.5%. Naive Bayes had a gap of −1.3%. A network with 85,002 weights has enough
room to learn Carol's 40 unusual digits one by one, instead of only learning what digits look like in general. That is
[memorisation](overfitting-and-memorisation.md), and it is the influence unlearning has to remove.

## A worked example

Follow Carol through one training run of the course network and then through her erasure. Every number comes from
Lesson 04.

1. **Her data joins the pile.** Carol wrote 40 digits with a thick marker. They sit among 1,257 training digits, so she
   is about 3% of the data. The other 1,217 digits are the retain set.
2. **Training starts from random weights.** With seed 0, the network gets 85,002 random starting numbers.
3. **Her digits are spread over the batches.** Each epoch shuffles the 1,257 digits into 20 mini-batches. On average
   each batch of 64 holds about two of Carol's digits. Over 60 epochs her digits help set the direction of most of the
   1,200 steps.
4. **The network memorises her.** Her loss is pushed to almost zero, while the loss on unseen digits in the same thick
   style stays much higher. At the end the network reads 100% of her 40 digits correctly but only 77.5% of 80 unseen
   thick-marker digits. That 22.5-point gap is her trace in the model.
5. **She asks to be erased.** Deleting her 40 rows from the database changes nothing in the model, because the model
   only uses its weights.
6. **The team looks for her weights.** They retrain from the same seed without her and compare. 94.1% of the 85,002
   weights differ, and 87.4% differ by more than 0.001. There is no small set of weights to subtract. The two networks
   are 9.87 apart, while a seed change alone puts networks 50.96 apart, so weight distance cannot show she is gone.
7. **The team retrains from scratch without her.** It takes 0.27 seconds for this small network. The new model reads
   55.0% of Carol's digits (22 of 40), close to the 62.5% it gets on unseen thick-marker digits. Test accuracy stays at
   98.0%.
8. **The team proves it by behaviour.** Her digits now get no special treatment. The model still reads more than half
   of them, because it learnt digits from everyone else, but it is about as good on them as on digits like hers that
   it never saw. That is what forgetting looks like.

## What the lesson found

**Who memorises more?** The memorisation gap is the accuracy on Carol's digits minus the accuracy on unseen digits in
her style.

| Model | Carol | Unseen thick | Gap | Test |
|---|---|---|---|---|
| Naive Bayes | 60.0% | 61.3% | −1.3% | 91.1% |
| k-NN, k = 5 | 75.0% | 67.5% | +7.5% | 98.3% |
| Logistic regression | 92.5% | 77.5% | +15.0% | 97.2% |
| RBF SVM | 100.0% | 87.5% | +12.5% | 99.4% |
| Random forest | 100.0% | 70.0% | +30.0% | 97.2% |
| **Neural network** | 100.0% | 77.5% | **+22.5%** | 98.0% |

Naive Bayes only keeps averages, and one person barely moves an average, so it does not memorise Carol. The network and
the forest memorise her most. Unlike the forest, the network has no separate trees to rebuild.

**What changes when Carol is removed.**

| Measure | Number | What it means |
|---|---|---|
| Weights that differ at all | 94.1% of 85,002 | Her influence is spread over almost the whole network |
| Weights that differ by more than 0.001 | 87.4% | Most of those changes are not tiny |
| Distance, with Carol vs without Carol | 9.87 | Removing her moves the weights a little |
| Distance, seed 0 vs seed 1 on the same data | 50.96 | A new random start moves them much more |
| Size of the Newton table (Hessian) | about 29 GB | Too big even for this small network |

**What retraining gives.**

| | Original | Retrained without Carol |
|---|---|---|
| Accuracy on Carol's digits | 100.0% | 55.0% |
| Accuracy on unseen thick digits | 77.5% | 62.5% |
| Accuracy on test digits | 98.0% | 98.0% |

Retraining removes the gap and costs everyone else nothing. Here it took 0.27 seconds. For a large model it would take
weeks of GPU time, which is why the rest of the course looks for cheaper methods.

## Limits

**The network is tiny.** It has 85,002 weights, 1,257 training digits and trains in a fraction of a second. Real models
have billions of weights. The ideas carry over, but the course's exact numbers do not.

**One person, one seed.** The 94.1% figure comes from removing Carol from one network trained with seed 0. The lesson
does not report how it changes for other seeds or for removing a single typical digit. That is left as a task in the
notebook.

**Small test sets.** Carol has 40 digits, so each one is worth 2.5 percentage points of her accuracy. The look-alike set
has 80 digits. A gap of a few points can come from one or two digits.

**Accuracy is a coarse lens.** The memorisation gap treats Carol as one block. The notebook also uses Feldman (2020)'s
per-example memorisation score, which shows that her unusual digits are memorised far more than typical ones.
Stronger tests, such as [membership inference attacks](../unlearning/membership-inference-attacks.md), come in later
lessons.

**Design can change the picture.** "Influence is everywhere" is true for a network trained in the usual way. If you
split the training into separate pieces from the start, as in [SISA](../unlearning/sisa.md), or keep a customer's
changes in a removable add-on, as in [LoRA](fine-tuning-and-lora.md), one person's influence can be kept in one place.

## In code

```python
from mul import lab, train
model = lab.model_fn()             # MLP(64 -> 256 -> 256 -> 10, 85,002 params)
L = lab.make_lab("carol")
model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)   # 60 epochs of Adam
print(train.accuracy(model, L.X_test, L.y_test))                           # about 0.98
```

One training step, written out by hand with the course library, shows the forward pass, the loss and backpropagation.

```python
from mul import nn
opt = nn.Adam(model.params, lr=1e-3)
logits = model.forward(X_batch, keep_cache=True)   # forward pass, 10 scores per digit
loss, g = nn.cross_entropy(logits, y_batch)        # how wrong, and the error at the output
opt.step(model.backward(g))                        # one gradient per weight, then a small step
```

!!! tip "What to do in practice"
    - **Write down the training recipe.** Keep the data list, the seed and settings such as epochs, batch size and
      learning rate, so that you can retrain without a person when you must.
    - **Decide early how you will delete.** If deletions are likely, design for them before training, for example
      with [SISA](../unlearning/sisa.md) shards split by user or with removable [LoRA](fine-tuning-and-lora.md)
      adapters.
    - **Measure forgetting by behaviour.** Compare the model on the person's data with models that never saw it, and
      use a [gold band](../unlearning/gold-band.md) of several seeds rather than one model.
    - **Watch unusual data most closely.** Rare styles, like Carol's thick marker, are memorised most, so check those
      people first.

## Common mistakes

!!! danger "Mistakes people make"
    - **Looking for "the person's weights".** There are none. Influence is spread across the whole network, because
      every example's error flows back through every layer.
    - **Comparing weights to prove forgetting.** Equally good networks have very different weights. Compare behaviour.
    - **Thinking deleting the training rows changes the model.** A trained network never reads its data again. It only
      uses its weights.
    - **Expecting 0% on the forgotten person.** A model that never saw Carol still reads 55% of her digits, because it
      learnt digits from everyone else.
    - **Trusting one retrained model as the target.** A different seed gives a different but equally good model. The
      target is a spread, so use several seeds.
    - **Assuming a bigger network is safer.** More weights give more room to memorise individuals, as the gap of +22.5%
      against −1.3% for Naive Bayes shows.

## Key takeaways

- A neural network is layers of weights, all trained together by gradient descent.
- Each neuron multiplies its inputs by weights, adds a bias and applies a bend such as ReLU.
- Backpropagation gives every weight a gradient, so every example nudges almost every weight.
- Each training step starts where the last one ended, so one person's influence is carried along the whole path.
- There are many equally good networks, so the gold standard is a spread, not a single point.
- Flexible networks memorise unusual people, such as Carol, far more than simple models do.
- Retraining from scratch is the only exact option, unless you design for deletion (see [SISA](../unlearning/sisa.md)).

!!! note "Notes to take"
    - **Neural network.** Layers of neurons joined by weights. Input → hidden layers → output.
    - **Neuron.** Inputs × weights, add them up, add a bias, apply ReLU (keep if positive, else 0).
    - **Forward pass.** Pixels in, 10 probabilities out (softmax).
    - **Loss.** Cross-entropy, small when the right digit gets a high probability.
    - **Training.** Backpropagation gives a gradient for every weight, then a small step. Repeat 1,200 times.
    - **Course network.** 64 → 256 → 256 → 10, 85,002 weights.
    - **Key number.** Removing Carol changes 94.1% of the weights.
    - **Key fact.** Seed change distance 50.96 is bigger than Carol distance 9.87, so compare behaviour.
    - **Trap.** There is no "Carol weight" to delete.

## Quiz

```quiz
- q: How many weights does the course's neural network have?
  options:
    - 64
    - 85,002
    - 7 billion
  answer: 1
  why: "MLP(64 -> 256 -> 256 -> 10) has 85,002 weights."
- q: When Carol is removed and the network retrained from the same start, what share of weights change?
  options:
    - About 1%
    - About 50%
    - 94.1%
  answer: 2
  why: Her influence is spread across almost the whole network.
- q: Two networks are trained on identical data with different random starts. What happens?
  options:
    - They end up with identical weights.
    - They end up with very different weights but similar accuracy.
    - One of them always fails.
  answer: 1
  why: The loss has many equally good valleys. This is why the gold standard is a band, not a single model.
- q: Why must proof of forgetting in a neural network be about behaviour?
  options:
    - Weights differ between equally good models anyway, so comparing weights proves nothing.
    - Weights are secret.
    - Neural networks have no weights.
  answer: 0
  why: Only behaviour can be compared fairly with models that never saw the data.
- q: A hidden neuron using ReLU adds up its inputs and gets a total of −0.4. What does it output?
  options:
    - "−0.4"
    - "0"
    - "0.4"
  answer: 1
  why: ReLU keeps a positive total and turns a negative total into 0.
- q: What is a forward pass?
  options:
    - Running an input through every layer to get the output
    - Passing the error backwards to find each weight's gradient
    - One full pass over all the training data
  answer: 0
  why: The forward pass goes from the pixels to the probabilities. Passing the error backwards is backpropagation, and a full pass over the data is an epoch.
- q: Which connection holds the most weights in the course network?
  options:
    - 64 pixels to hidden layer 1
    - Hidden layer 1 to hidden layer 2
    - Hidden layer 2 to the 10 outputs
  answer: 1
  why: 256 × 256 = 65,536 weights, plus 256 biases. The other two connections have 16,640 and 2,570 numbers.
- q: Carol's digits were in an early mini-batch. Why does that affect weights changed much later in training?
  options:
    - Every later step starts from weights her digits already nudged.
    - Her digits are copied into every later batch on purpose.
    - Later steps only use her digits.
  answer: 0
  why: Gradient descent is a path. Each step depends on the one before, so an early nudge shifts the whole rest of the path.
- q: After retraining without Carol, the network reads 55.0% of her digits. Why is that not a failure to forget?
  options:
    - It is close to the 62.5% on unseen thick digits, so her digits get no special treatment.
    - Forgetting should always give 0%.
    - 55.0% means the model still remembers half of her data.
  answer: 0
  why: A model that never saw Carol still learnt digits from everyone else. Forgetting means matching such a model, not scoring zero.
```

## Try it

- Read the concept page [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md).
- Run the lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md).
- In the notebook, remove one *typical* digit instead of Carol and repeat the weight comparison. Do fewer weights
  change?
- In the notebook, swap in a smaller network, `MLP(64, 10, hidden=(32,))`, and check whether it memorises Carol less.
- Read [Overfitting and memorisation](overfitting-and-memorisation.md) next, to see why unusual data is remembered most.
