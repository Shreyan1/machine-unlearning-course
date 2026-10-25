---
title: "Lesson 04: Deleting is not forgetting"
description: Why every classical unlearning trick fails in a neural network, and why the proof of forgetting must be about behaviour.
---

# Lesson 04: Neural networks, why deleting is not forgetting

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~30 min</span><span class="chip" markdown="span">:material-map-marker-path: Stage 2 · Neural nets: the problem</span><span class="chip" markdown="span">:material-stairs-up: Rung 4</span></div>

<div class="buttons" markdown>
[:simple-googlecolab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb){ .md-button }
</div>

## The story so far

In Lessons 01 to 03, every classical model gave us a handle for forgetting:

| Handle | Classical models | Neural network |
|---|---|---|
| A **sum** you can subtract from | Naive Bayes, k-NN, ridge | ❌ The weights are the end of a long path of small steps, each depending on the last. |
| A **single best answer** you can step to | Ridge, logistic regression | ❌ There are many equally good answers. |
| **Locality**: only a few parts depend on a point | SVM, random forest | ❌ Every example nudges **every** weight. |

This lesson makes each ❌ concrete, with numbers.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a small neural network (64 → 256 → 256 → 10, with 85,002 weights) on the digits, including Carol's 40.</li>
<li markdown>**Show the issue**: measure how much each model memorises Carol, from Naive Bayes up to the network.</li>
<li markdown>**Try the classical tricks** one by one. Subtract, take a Newton step and rebuild only the touched part.</li>
<li markdown>**Untrain** with the only exact option left, which is to retrain from scratch without Carol.</li>
<li markdown>**Prove it** by behaviour, not by weights.</li>
</ol>

## Key results

**Who memorises more?** The "memorisation gap" is the accuracy on Carol's digits minus the accuracy on unseen digits in
her style.

| Model | Carol | Unseen thick | Gap | Test |
|---|---|---|---|---|
| Naive Bayes | 60.0% | 61.3% | −1.3% | 91.1% |
| k-NN, k = 5 | 75.0% | 67.5% | +7.5% | 98.3% |
| Logistic regression | 92.5% | 77.5% | +15.0% | 97.2% |
| RBF SVM | 100.0% | 87.5% | +12.5% | 99.4% |
| Random forest | 100.0% | 70.0% | +30.0% | 97.2% |
| **Neural network** | 100.0% | 77.5% | **+22.5%** | 98.0% |

The more flexible the model, the more it remembers individuals. Naive Bayes, which only keeps averages, does not
memorise Carol at all.

**The three tricks all fail:**

- **Subtract her?** Removing Carol changes **94.1%** of the 85,002 weights. She is not stored anywhere in particular.
- **One Newton step?** It needs a table of 85,002 × 85,002 numbers, about **29 GB**. For a 7-billion-weight language
  model it would be about 98 exabytes. Worse, two networks trained on the *same* data with different random starts end
  up further apart (distance 50.96) than the with-Carol and without-Carol pair (distance 9.87). There is no single
  "right" network to step towards.
- **Rebuild only what she touched?** She touched everything, unless we design the network for it (that is
  [SISA](../unlearning/sisa.md), Lesson 07).

**Retraining works:** Carol's accuracy drops from 100.0% to 55.0%, close to the 62.5% on unseen thick digits, and test
accuracy stays at 98.0%. It took 0.27 seconds here. For a large model it would take weeks of GPU time.

!!! note "Why this matters"
    Because many equally good networks exist, the "retrained model" is not one point but a whole spread of models.
    So comparing weights can never prove forgetting. The proof must be about **behaviour**, and the target is a
    **band**, not a number.

## Concepts used here

- [Neural networks](../ml-basics/neural-networks.md)
- [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md)
- [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md)
- [Retraining, the gold standard](../unlearning/retraining-gold-standard.md)
- [The gold band](../unlearning/gold-band.md)

## Quiz

```quiz
- q: Which model did **not** memorise Carol at all in this lesson?
  options:
    - The neural network
    - The random forest
    - Naive Bayes
    - The RBF SVM
  answer: 2
  why: Naive Bayes only keeps averages per class, so its gap was −1.3%. One person barely moves an average.
- q: When Carol is removed and the network is retrained from the same seed, roughly how many weights change?
  options:
    - About 1%
    - About 25%
    - About 94%
  answer: 2
  why: 94.1% of the 85,002 weights differ. Her influence is spread across the whole network.
- q: Why does a single Newton step not work for the network, even ignoring memory?
  options:
    - The network has no single best answer to step towards.
    - Newton steps only work on images.
    - The network has too few weights.
  answer: 0
  why: Two networks trained on the same data with different random starts land far apart and are equally good. There is no one optimum.
- q: Two networks are trained on identical data with different seeds. Compared with the with-Carol and without-Carol pair, they are...
  options:
    - Much closer together
    - Much further apart
    - Exactly the same
  answer: 1
  why: The seed pair is at distance 50.96, the Carol pair at 9.87. Random starts matter more than Carol does.
- q: What must a proof of forgetting in a neural network be based on?
  options:
    - Comparing the weights one by one
    - The model's behaviour, compared with models that never saw the data
    - The size of the model file
  answer: 1
  why: Weights differ between equally good models anyway, so only behaviour can be compared fairly.
```

## Open question → Lesson 05

The proof must be about behaviour. So imagine you are an outsider who can only send questions to a model: **could you
tell whether Carol's data was used to train it?** If you can, the model is leaking, and you also have a tool to check
every unlearning method in the course.

[Next: Lesson 05, membership inference attacks :material-arrow-right:](05-membership-inference.md){ .md-button }
