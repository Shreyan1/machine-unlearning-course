---
title: Neural networks
description: A neural network is layers of numbers trained together by gradient descent, so every example nudges almost every weight and one person's data ends up everywhere.
---

# Neural networks

!!! oneline "In one line"
    A neural network is a stack of **layers of numbers** that turns an input into an answer, and training nudges *all*
    of those numbers for every batch of examples.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - follow one digit through a network, from 64 pixels to 10 probabilities,
    - explain why training spreads one person's data over almost every weight,
    - say why forgetting must be checked by behaviour and not by comparing weights.

## Why it matters

Neural networks power almost all modern AI, from image recognition to chatbots. They are also where unlearning gets
hard. Every trick that worked for classical models (subtract a sum, take a Newton step, rebuild only the part a point
touched) fails here. Understanding why is the turning point of the course.

The reason is simple to say and hard to undo. A classical model such as Naive Bayes keeps a few totals, so one person's
share sits in a place you can find. A neural network keeps tens of thousands of numbers instead, and each training
example pushes on nearly all of them at once. After training, nobody can point to the part that came from one person.

A team that does not understand this will answer an erasure request with shortcuts that look sensible and fail, such
as hunting for "the person's weights".

## A simple example

!!! simply "Explain it simply"
    Think of a big mixing desk in a recording studio, with thousands of knobs. Sound goes in one end and music comes out
    the other. Training means turning every knob a tiny bit, over and over, until the music sounds right. Once that is
    done, you cannot point to "the knob for the drums". Every knob affects every part of the sound.

In the real thing, the **sound going in** is the 64 pixels of a handwritten digit. The **music coming out** is a score
for each of the ten digits. Each **knob** is one weight, a number the network learns. The **sound engineer** is the
training method, [gradient descent](gradient-descent.md). Carol's 40 digits are a few **songs in the practice set**.
Every time one is played, the engineer turns nearly every knob a little, so her songs leave a trace on the whole desk.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| **Neuron** | A small unit that multiplies each input by a weight, adds the results and a bias, and passes the total on | Each hidden layer has 256 neurons |
| **Layer** | A row of neurons that all read the same inputs | `MLP(64 -> 256 -> 256 -> 10)` has two hidden layers |
| [**Weight**](../start-here/glossary.md#w) | A number the network learns, one for every connection between two neurons. Also called a parameter | The course network has 85,002 |
| **Activation** | The simple bend a neuron applies to its total. ReLU keeps a positive number and turns a negative one into 0 | −0.4 becomes 0 |
| **Forward pass** | Running an input through every layer to get the output | 64 pixels in, 10 scores out |
| [**Softmax**](../start-here/glossary.md#s) | A step that turns the 10 raw scores into 10 probabilities that add up to 1 | 0.90 for "7", 0.05 for "1" |
| [**Cross-entropy loss**](../start-here/glossary.md#c) | One number that says how wrong the network is | 0.90 on the right digit gives 0.11 |
| **Backpropagation** | The method that works out which way every weight should move to lower the loss, by passing the error backwards | `model.backward()` in `mul/nn.py` |
| [**Epoch**](../start-here/glossary.md#e) | One full pass over the training data, in small groups called mini-batches | 60 epochs, mini-batches of 64 |

## How it works

<!-- diagram: neural-networks -->

The figure shows a small network with four columns of circles. On the left are the inputs. In the middle are two
hidden layers, the first finding simple patterns and the second combining them. On the right are the outputs, which
give the answer. Every circle is joined to every circle in the next column by a line that carries a weight, and
training adjusts every line.

### Step 1. The input layer

The input layer holds the raw data. Each course digit is a tiny 8 × 8 picture, so it has 64 pixels, each a number
between 0 (blank) and 1 (fully inked). Carol's digits are the same kind of list, but her thick marker inks more pixels,
because every stroke is one pixel wider.

### Step 2. A neuron and its weights

A neuron multiplies each input by its own weight, adds up the results and then adds one more number called the
**bias**. A positive weight means "this pixel being inked pushes me up", and a negative one pushes the neuron down.
Here is one neuron with three inputs and made-up numbers.

| Input (pixel value) | Weight | Input × weight |
|---|---|---|
| 0.0 | 0.4 | 0.0 |
| 0.5 | −0.2 | −0.1 |
| 1.0 | 0.3 | 0.3 |
| Bias | | 0.1 |
| **Total** | | **0.3** |

A real neuron in the first hidden layer does the same with 64 inputs.

### Step 3. The activation (the bend)

If a neuron only added things up, a stack of layers would be no smarter than one layer, because sums of sums are still
sums. So each hidden neuron bends its total with an **activation**. The course uses **ReLU**, which keeps a positive
total and outputs 0 otherwise. The neuron above outputs 0.3. With a total of −0.4 it would output 0 and pass nothing
on. This small bend lets a network learn curved patterns, such as the many ways people write a 7.

??? checkpoint "Checkpoint 1 · A neuron reads two pixels, 1.0 and 0.5, with weights 0.2 and −0.8 and a bias of 0.1. What does it pass on?"
    **0.** The total is 1.0 × 0.2 + 0.5 × (−0.8) + 0.1 = 0.2 − 0.4 + 0.1 = −0.1. ReLU turns any negative total into
    0, so this neuron stays silent for this digit. A digit with other pixels inked could switch it on.

### Step 4. Hidden layers, stacked

The course network has two hidden layers of 256 neurons each. Every neuron in the first reads all 64 pixels, and every
neuron in the second reads all 256 outputs of the first. This is a **fully connected** network, so the weights add up
fast. It is written `MLP(64 -> 256 -> 256 -> 10)` and has **85,002** weights, counting the biases. It is plain NumPy in
`mul/nn.py`, so every step, including every gradient, is a line of code you can read.

??? deep "Go deeper · counting the 85,002 weights"
    Each connection between two layers has one weight for every pair of neurons, plus one bias for every neuron it
    feeds.

    | Connection | Weights | Biases | Total |
    |---|---|---|---|
    | 64 pixels → hidden layer 1 (256) | 64 × 256 = 16,384 | 256 | 16,640 |
    | Hidden layer 1 → hidden layer 2 (256) | 256 × 256 = 65,536 | 256 | 65,792 |
    | Hidden layer 2 → 10 outputs | 256 × 10 = 2,560 | 10 | 2,570 |
    | **Whole network** | | | **85,002** |

    The middle connection holds more than three quarters of the network, because its size grows with the width of
    both layers it joins.

### Step 5. The output layer and the forward pass

The last layer has 10 neurons, one per digit. It applies no bend, and its 10 raw scores are called **logits**.
[Softmax](probabilities-and-kl-divergence.md) turns them into 10 probabilities, and the answer is the most likely digit.

Running a digit from the pixels to the probabilities is the **forward pass**. It is all a trained network does when you
use it. It never looks at the training data again, only at its weights.

### Step 6. The loss

The [cross-entropy loss](loss-functions.md) looks at the probability the network gave to the **right** digit. A
probability of 0.90 gives a loss of 0.11, 0.50 gives 0.69 and 0.10 gives 2.30. A confident right answer costs almost
nothing, and a confident wrong answer costs a lot. Training tries to make the average loss as small as possible.

### Step 7. Training with backpropagation

Training is [gradient descent](gradient-descent.md) on the loss. From random weights, the network repeats four moves.

1. Take a **mini-batch** of 64 training digits.
2. Do a forward pass and measure the loss.
3. Run **backpropagation**. It starts at the output and passes the error backwards layer by layer, working out a
   **gradient** for every weight. The gradient says which way that weight should move to lower the loss.
4. Move every weight a small step in its downhill direction.

The course uses **Adam**, a version of gradient descent that gives each weight its own step size. The recipe is 60
epochs, mini-batches of 64 and a learning rate of 0.001. With 1,257 training digits, one epoch is 20 mini-batches, so
training takes 1,200 steps.

### Why neural networks are hard to unlearn

Two facts from the steps above spread one person's data over all the weights.

**Every example reaches almost every weight.** When Carol's digit is in a mini-batch, its error flows back through
every layer, and most weights get a small push from it. No wall keeps her digit inside one part of the network.

**Every step starts where the last one ended.** If Carol's digit nudged the weights at step 10, all 1,190 later steps
began from a slightly different place. Her influence is carried along the whole path.

Lesson 04 tests each classical trick and finds that all three fail.

| Trick | Why it fails in a neural network |
|---|---|
| **Subtract** the person's contribution | Removing Carol changes **94.1%** of the 85,002 weights. Her influence is everywhere. |
| **One Newton step** to the new answer | It needs a table of 85,002 × 85,002 numbers, about 29 GB. And there is no single best answer to step to. |
| **Rebuild only the part** she touched | She touched every part. |

??? deep "Go deeper · why a Newton step is out of reach"
    A **Newton step** is a jump straight to the best answer, worked out from the curvature of the loss. The table of
    curvatures is called the Hessian. It has one entry for every pair of weights, so for the course network it has
    85,002 × 85,002 = 7,225,340,004 entries, about 29 GB. For a 7-billion-weight language model it would be about 98
    exabytes.

    Size is not even the deeper problem. A Newton step aims at **the** best answer, and the next section shows that a
    network has many equally good answers, not one.

### Many equally good networks

A neural network's loss has many valleys, not one bowl. In Lesson 04, two networks trained on the same data with
different random starts reached 98.0% and 98.7% on the test digits. Yet their weights were 50.96 apart, while the
with-Carol and without-Carol pair was only 9.87 apart. Here "distance" is the size of the gap between two full lists of
85,002 weights. Changing the seed moved the weights about five times further than removing Carol did.

So there is no single "retrained model", only a **spread** of them. Proof of forgetting must be about **behaviour**,
measured against a [gold band](../unlearning/gold-band.md).

??? checkpoint "Checkpoint 2 · An unlearnt network sits only 9.9 away from a network retrained without Carol. Does that prove she is gone?"
    **No.** Weight distance cannot tell you what a network remembers. The original model, which still reads 100% of
    Carol's digits, was itself only 9.87 away from the retrain without her. Two honest networks that differ only in
    their seed were 50.96 apart. Compare how the networks behave on her digits instead.

### Neural networks memorise more

A network with 85,002 weights has room to learn Carol's 40 unusual digits one by one, instead of only learning what
digits look like in general. That is [memorisation](overfitting-and-memorisation.md), and it is the influence
unlearning has to remove. Lesson 04 measures it as a **memorisation gap**, the accuracy on Carol's digits minus the
accuracy on unseen digits in her style.

## A worked example

Follow Carol through one training run and then through her erasure. Every number comes from Lesson 04.

1. **Her data is spread over the batches.** Her 40 thick-marker digits are about 3% of the 1,257 training digits, so
   each mini-batch of 64 holds about two of them. They help set the direction of most of the 1,200 steps.
2. **The network memorises her.** It reads 100% of her 40 digits but only 77.5% of 80 unseen thick-marker digits. That
   22.5-point gap is her trace in the model.
3. **She asks to be erased.** Deleting her 40 rows from the database changes nothing, because the model only uses its
   weights.
4. **The team looks for her weights.** They retrain from the same seed without her. 94.1% of the weights differ, and
   87.4% differ by more than 0.001. There is nothing small to subtract.
5. **The team retrains from scratch without her.** It takes 0.27 seconds. The new model reads 55.0% of Carol's digits
   (22 of 40), close to the 62.5% it gets on unseen thick-marker digits. Test accuracy stays at 98.0%.
6. **The team proves it by behaviour.** The model still reads more than half of her digits, because it learnt digits
   from everyone else. But it treats them like digits it never saw, and that is what forgetting looks like.

??? checkpoint "Checkpoint 3 · Suppose a method leaves the network reading 90.0% of Carol's digits and 62.5% of unseen thick ones. Has it forgotten her?"
    **No.** Her digits still score 90.0 − 62.5 = 27.5 points above digits like hers, which is even more than the
    original network's gap of 22.5. A network that never saw her reads the two groups about equally, 55.0% against
    62.5% in Lesson 04. A score of 0% is not the goal either. The goal is no special treatment.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>94.1%</strong><span>of the 85,002 weights change when Carol is removed</span></div>
<div class="is-bad"><strong>+22.5</strong><span>points, the network's memorisation gap on Carol</span></div>
<div><strong>50.96</strong><span>distance between two seeds, five times the 9.87 that Carol makes</span></div>
<div class="is-good"><strong>0.27 s</strong><span>to retrain without her, Carol 100.0% to 55.0%, test still 98.0%</span></div>
</div>

**Who memorises more?** Every model in the course so far, trained on the same data, measured the same way.

| Model | Carol | Unseen thick | Gap | Test |
|---|---|---|---|---|
| Naive Bayes | 60.0% | 61.3% | −1.3% | 91.1% |
| k-NN, k = 5 | 75.0% | 67.5% | +7.5% | 98.3% |
| Logistic regression | 92.5% | 77.5% | +15.0% | 97.2% |
| RBF SVM | 100.0% | 87.5% | +12.5% | 99.4% |
| Random forest | 100.0% | 70.0% | +30.0% | 97.2% |
| **Neural network** | 100.0% | 77.5% | **+22.5%** | 98.0% |

Naive Bayes only keeps averages, which one person barely moves. The network and the forest memorise Carol most, and
the network has no separate trees to rebuild. Retraining removes the gap at no cost to anyone else, but for a large
model it would take weeks of GPU time. That is why the rest of the course looks for cheaper methods.

??? deep "Go deeper · what removing Carol changes, and what retraining gives"
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

## Limits

**The network is tiny.** It has 85,002 weights and trains in a fraction of a second. Real models have billions of
weights. The ideas carry over, but the course's exact numbers do not.

**Design can change the picture.** "Influence is everywhere" holds for a network trained in the usual way. With
[SISA](../unlearning/sisa.md) shards or a removable [LoRA](fine-tuning-and-lora.md) add-on, one person's influence can
be kept in one place.

??? deep "Go deeper · three more limits"
    **One person, one seed.** The 94.1% figure comes from removing Carol from one network trained with seed 0. The
    lesson does not report how it changes for other seeds or for removing a single typical digit. That is left as a
    task in the notebook.

    **Small test sets.** Carol has 40 digits, so each one is worth 2.5 percentage points of her accuracy. The
    look-alike set has 80 digits. A gap of a few points can come from one or two digits.

    **Accuracy is a coarse lens.** The memorisation gap treats Carol as one block. The notebook also uses Feldman
    (2020)'s per-example memorisation score, which shows that her unusual digits are memorised far more than typical
    ones. Stronger tests, such as [membership inference attacks](../unlearning/membership-inference-attacks.md), come
    in later lessons.

## In code

```python
from mul import lab, train, nn
L = lab.make_lab("carol")
model = train.fit(lab.model_fn, L.X_train, L.y_train, seed=0, **lab.FIT)   # MLP(64 -> 256 -> 256 -> 10), 60 epochs of Adam
print(train.accuracy(model, L.X_test, L.y_test))                           # about 0.98

# One training step by hand, the forward pass, the loss and backpropagation
opt = nn.Adam(model.params, lr=1e-3)
logits = model.forward(X_batch, keep_cache=True)   # forward pass, 10 scores per digit
loss, g = nn.cross_entropy(logits, y_batch)        # how wrong, and the error at the output
opt.step(model.backward(g))                        # one gradient per weight, then a small step
```

!!! tip "What to do in practice"
    - **Write down the training recipe.** Keep the data list, the seed and the settings, so you can retrain when you must.
    - **Decide early how you will delete.** If deletions are likely, design for them before training, for example
      with [SISA](../unlearning/sisa.md) shards split by user or removable [LoRA](fine-tuning-and-lora.md) adapters.
    - **Measure forgetting by behaviour.** Compare the model on the person's data with a
      [gold band](../unlearning/gold-band.md) of models from several seeds that never saw it.

## Common mistakes

!!! danger "Mistakes people make"
    - **Looking for "the person's weights".** There are none, because every example's error flows back through every
      layer.
    - **Comparing weights to prove forgetting.** Equally good networks have very different weights. Compare behaviour.
    - **Thinking deleting the training rows changes the model.** A trained network never reads its data again.
    - **Expecting 0% on the forgotten person.** A model that never saw Carol still reads 55% of her digits.
    - **Assuming a flexible model is safer.** A network can memorise individuals, +22.5 points against −1.3 for Naive
      Bayes. Whether a bigger network memorises more is not tested in the course.

## Key takeaways

!!! notes "Notes to take"
    - **Neural network.** Layers of neurons joined by weights. Input → hidden layers → output.
    - **Neuron.** Inputs × weights, add them up, add a bias, apply ReLU (keep if positive, else 0).
    - **Forward pass.** Pixels in, 10 probabilities out (softmax). It never reads the training data again.
    - **Training.** Cross-entropy loss, then backpropagation gives every weight a gradient and a small step. 1,200 steps.
    - **Course network.** 64 → 256 → 256 → 10, 85,002 weights.
    - **Spread.** Removing Carol changes 94.1% of the weights, because every step starts where the last one ended.
    - **Many answers.** Seed change distance 50.96 is bigger than Carol distance 9.87, so compare behaviour.
    - **Memorisation.** Network gap +22.5 points on Carol, Naive Bayes −1.3.
    - **Exact option.** Retrain without her (0.27 s here), unless you design for deletion with [SISA](../unlearning/sisa.md).
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
- q: A team deletes Carol's 40 rows from its database but keeps the trained network. What happens to the network's answers on her digits?
  options:
    - They drop to about 55%, like a retrained model.
    - They drop to 0%.
    - Nothing changes, because the network only uses its weights.
  answer: 2
  why: A trained network never reads its training data again. Her influence lives in the weights until you retrain or unlearn.
```

## Try it

!!! levelup "Level up"
    You can now trace a digit through a network and explain why one person's data ends up in almost every weight. Next
    quest, [Language models](language-models.md), where the same kind of training turns a phone number into a habit
    spread across the weights.

- Read the concept page [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md).
- Run the lesson [04 · Deleting is not forgetting](../lessons/04-deleting-is-not-forgetting.md).
- In the notebook, remove one *typical* digit instead of Carol and repeat the weight comparison. Do fewer weights
  change?
- In the notebook, swap in a smaller network, `MLP(64, 10, hidden=(32,))`, and check whether it memorises Carol less.
- Read [Overfitting and memorisation](overfitting-and-memorisation.md) to see why unusual data is remembered most.
