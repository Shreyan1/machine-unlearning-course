---
title: ML Basics
description: The machine learning you need before learning machine unlearning, explained from zero.
---

# ML Basics

Before you can make a model *forget*, you need to know how a model *learns*. This section explains the machine learning
the course uses, from zero. Each page takes about ten minutes and ends with a short quiz.

If you already know machine learning well, skip ahead to [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md).

## The big picture

These pages explain how learning works in general.

<div class="cards" markdown>
<a class="card" href="what-is-machine-learning/"><span class="card__num">1</span><span class="card__title">What is machine learning?</span><span class="card__text">Learning rules from examples instead of writing them by hand.</span></a>
<a class="card" href="training-and-testing/"><span class="card__num">2</span><span class="card__title">Training data and test data</span><span class="card__text">Why we always keep some data aside to check the model.</span></a>
<a class="card" href="loss-functions/"><span class="card__num">3</span><span class="card__title">Loss functions</span><span class="card__text">One number that says how wrong the model is.</span></a>
<a class="card" href="gradient-descent/"><span class="card__num">4</span><span class="card__title">Gradient descent</span><span class="card__text">How a model gets better, one small step at a time.</span></a>
<a class="card" href="overfitting-and-memorisation/"><span class="card__num">5</span><span class="card__title">Overfitting and memorisation</span><span class="card__text">When a model remembers examples instead of learning patterns.</span></a>
<a class="card" href="probabilities-and-kl-divergence/"><span class="card__num">6</span><span class="card__title">Probabilities and KL divergence</span><span class="card__text">How a model says how sure it is, and how to compare two models.</span></a>
</div>

## Classical models

These are the models of [Lessons 01 to 03](../lessons/index.md). For many of them, forgetting is exact and cheap.

<div class="cards" markdown>
<a class="card" href="k-nearest-neighbours/"><span class="card__num">Model</span><span class="card__title">k-nearest neighbours</span><span class="card__text">Answer by asking the most similar examples.</span></a>
<a class="card" href="naive-bayes/"><span class="card__num">Model</span><span class="card__title">Naive Bayes</span><span class="card__text">A model made of counts and averages.</span></a>
<a class="card" href="linear-and-ridge-regression/"><span class="card__num">Model</span><span class="card__title">Linear and ridge regression</span><span class="card__text">The best straight-line fit, from a formula.</span></a>
<a class="card" href="logistic-regression/"><span class="card__num">Model</span><span class="card__title">Logistic regression</span><span class="card__text">A straight line that outputs probabilities.</span></a>
<a class="card" href="support-vector-machines/"><span class="card__num">Model</span><span class="card__title">Support vector machines</span><span class="card__text">The widest street between two classes.</span></a>
<a class="card" href="decision-trees-and-random-forests/"><span class="card__num">Model</span><span class="card__title">Decision trees and random forests</span><span class="card__text">A committee of yes/no question trees.</span></a>
</div>

## Modern models

These are the models of Lessons 04 onwards. Here, forgetting gets hard.

<div class="cards" markdown>
<a class="card" href="neural-networks/"><span class="card__num">Model</span><span class="card__title">Neural networks</span><span class="card__text">Layers of numbers, all trained together.</span></a>
<a class="card" href="language-models/"><span class="card__num">Model</span><span class="card__title">Language models</span><span class="card__text">Models that predict the next word or character.</span></a>
<a class="card" href="fine-tuning-and-lora/"><span class="card__num">Technique</span><span class="card__title">Fine-tuning and LoRA</span><span class="card__text">Teaching an existing model something new, cheaply.</span></a>
<a class="card" href="recommender-systems/"><span class="card__num">Model</span><span class="card__title">Recommender systems</span><span class="card__text">"People who watched this also watched..."</span></a>
</div>
