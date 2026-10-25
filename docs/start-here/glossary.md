---
title: Glossary
description: Every term and symbol used on this site, with a plain-words meaning and a link to the page that explains it.
---

# Glossary

Every term on this site, in plain words. Each one links to the page that explains it fully. Use the letters to jump
straight to a section.

<nav class="az" aria-label="Jump to a letter"><a href="#a">A</a><a href="#b">B</a><a href="#c">C</a><span aria-disabled="true">D</span><a href="#e">E</a><a href="#f">F</a><a href="#g">G</a><a href="#h">H</a><span aria-disabled="true">I</span><span aria-disabled="true">J</span><a href="#k">K</a><a href="#l">L</a><a href="#m">M</a><a href="#n">N</a><a href="#o">O</a><a href="#p">P</a><span aria-disabled="true">Q</span><a href="#r">R</a><a href="#s">S</a><span aria-disabled="true">T</span><a href="#u">U</a><span aria-disabled="true">V</span><a href="#w">W</a><span aria-disabled="true">X</span><span aria-disabled="true">Y</span><a href="#z">Z</a></nav>

## Symbols

| Symbol | Plain meaning |
|---|---|
| \(D\) | The full training set. |
| \(D_f\) | The **forget set**: the data that must be removed. |
| \(D_r\) | The **retain set**: everything else in training, so \(D = D_r \cup D_f\). |
| \(D_{\text{test}}\) | Data the model never trained on, used to measure usefulness. |
| \(\theta_o\) | The **original** model, trained on \(D\). |
| \(\theta_r\) | The **retrained** model, trained on \(D_r\) only: the gold standard. |
| \(\theta_u\) | The **unlearnt** model, produced by an unlearning method from \(\theta_o\). |

See [The notation](../unlearning/notation.md).

## Terms

### A { #a }

<div class="term" markdown>
<p class="term__name">Adapter (LoRA)</p>

A small add-on trained on top of a frozen base model, often one per customer. Deleting it removes that customer exactly. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).
</div>

<div class="term" markdown>
<p class="term__name">Approximate unlearning</p>

A cheap method that edits a trained model with no guarantee; its result must be audited. See [Quick fixes and their traps](../unlearning/approximate-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Attack success rate (ASR)</p>

In a backdoor attack, the share of triggered inputs that get the attacker's desired result. See [Poisoned data and backdoors](../unlearning/poisoning-and-backdoors.md).
</div>

<div class="term" markdown>
<p class="term__name">AUC</p>

A score for how well an attack separates two groups: 0.5 is a coin flip, 1.0 is always right. See [Membership inference attacks](../unlearning/membership-inference-attacks.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### B { #b }

<div class="term" markdown>
<p class="term__name">Backdoor</p>

A hidden rule an attacker teaches a model through poisoned data, such as "let any message with *zqx* through".
</div>

<div class="term" markdown>
<p class="term__name">Bad Teacher</p>

An approximate method in which the student copies a random, know-nothing model on the forget set. See [Bad Teacher](../unlearning/bad-teacher.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### C { #c }

<div class="term" markdown>
<p class="term__name">Certificate</p>

A record of how a deletion was done and how to check it. The best ones can be recomputed by anyone. See [The enterprise playbook](../unlearning/enterprise-playbook.md).
</div>

<div class="term" markdown>
<p class="term__name">Cross-entropy</p>

The usual loss for classification. It is small when the model gives high probability to the right answer. See [Loss functions](../ml-basics/loss-functions.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### E { #e }

<div class="term" markdown>
<p class="term__name">Epoch</p>

One pass over all the training data. See [Gradient descent](../ml-basics/gradient-descent.md).
</div>

<div class="term" markdown>
<p class="term__name">Exact unlearning</p>

A method whose result is guaranteed to match retraining without the data. See [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Exposure</p>

For a secret such as a phone number, how highly the model ranks the real value among all possible values. See [Unlearning in language models](../unlearning/llm-unlearning.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### F { #f }

<div class="term" markdown>
<p class="term__name">Fine-tuning</p>

Continuing to train an existing model on new, specific data. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).
</div>

<div class="term" markdown>
<p class="term__name">Forging</p>

Reaching the same final weights with or without a given example, which is why weights alone cannot prove forgetting. See [Can a test prove forgetting?](../unlearning/testing-vs-proving.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### G { #g }

<div class="term" markdown>
<p class="term__name">Gold band</p>

The range of results from several models retrained without the forget set. A method passes if it lands inside. See [The gold band](../unlearning/gold-band.md).
</div>

<div class="term" markdown>
<p class="term__name">Gold standard</p>

The model retrained from scratch without the forget set. See [Retraining, the gold standard](../unlearning/retraining-gold-standard.md).
</div>

<div class="term" markdown>
<p class="term__name">Gradient</p>

The direction in which each weight should move to increase the loss. See [Gradient descent](../ml-basics/gradient-descent.md).
</div>

<div class="term" markdown>
<p class="term__name">Gradient ascent</p>

Stepping *uphill* on the loss of the forget set, to make the model worse on it. Simple and risky.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### H { #h }

<div class="term" markdown>
<p class="term__name">Hessian</p>

A table of the loss's curvature, with one row and one column per weight. Needed for a Newton step; far too large for deep models. See [Logistic regression](../ml-basics/logistic-regression.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### K { #k }

<div class="term" markdown>
<p class="term__name">KL divergence</p>

A number for how different two sets of probabilities are; 0 means identical. See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### L { #l }

<div class="term" markdown>
<p class="term__name">Leverage</p>

How hard one training point pulls a linear model towards itself. See [Linear and ridge regression](../ml-basics/linear-and-ridge-regression.md).
</div>

<div class="term" markdown>
<p class="term__name">Lineage registry</p>

A record of every model and which data reached it, directly or through a parent. See [The enterprise playbook](../unlearning/enterprise-playbook.md).
</div>

<div class="term" markdown>
<p class="term__name">LiRA / U-LiRA</p>

Per-example membership tests that compare a model with shadow models trained with and without each example. See [Membership inference attacks](../unlearning/membership-inference-attacks.md).
</div>

<div class="term" markdown>
<p class="term__name">Locality</p>

When only some parts of a model depend on a given point, so only those parts need rebuilding. See [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### M { #m }

<div class="term" markdown>
<p class="term__name">Membership inference attack (MIA)</p>

An attempt to tell, from a model's behaviour, whether an example was in its training data.
</div>

<div class="term" markdown>
<p class="term__name">Memorisation</p>

When a model gets an example right *because* it was trained on that exact example. See [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### N { #n }

<div class="term" markdown>
<p class="term__name">NegGrad+</p>

Gradient ascent on the forget set combined with normal training on the retain set in every step.
</div>

<div class="term" markdown>
<p class="term__name">Newton step</p>

A jump to the estimated new best weights using the gradient and the Hessian. See [Logistic regression](../ml-basics/logistic-regression.md).
</div>

<div class="term" markdown>
<p class="term__name">NPO</p>

Negative Preference Optimisation, a form of gradient ascent for language models that stops pushing once the model has forgotten.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### O { #o }

<div class="term" markdown>
<p class="term__name">Over-forgetting</p>

Being *suspiciously* bad on the forget set, worse than models that never saw it. It is a failure too.
</div>

<div class="term" markdown>
<p class="term__name">Overfitting</p>

Being much better on training data than on new data.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### P { #p }

<div class="term" markdown>
<p class="term__name">Prefix forcing</p>

Typing the start of a secret and letting a language model finish it. Reveals suppressed facts.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### R { #r }

<div class="term" markdown>
<p class="term__name">Recall@10</p>

For a recommender, the share of a user's hidden items that appear in their top 10.
</div>

<div class="term" markdown>
<p class="term__name">Refusal training</p>

Teaching a model to say something like "(withheld)". It is suppression, not forgetting.
</div>

<div class="term" markdown>
<p class="term__name">Relearn attack</p>

Briefly reminding a model of some forgotten data and seeing how fast the rest comes back. Fast recovery means suppression. See [The unlearning audit](../unlearning/unlearning-audit.md).
</div>

<div class="term" markdown>
<p class="term__name">Retain set</p>

Everything in training except the forget set.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### S { #s }

<div class="term" markdown>
<p class="term__name">SCRUB / SCRUB+R</p>

An approximate method in which a student copies the original model on the retain set and moves away from it on the forget set; SCRUB+R adds a rewind. See [SCRUB](../unlearning/scrub.md).
</div>

<div class="term" markdown>
<p class="term__name">Shadow model</p>

A model trained by an attacker or auditor, with or without an example, to see how such models usually behave.
</div>

<div class="term" markdown>
<p class="term__name">Sherman-Morrison downdate</p>

A formula that removes a point from ridge regression exactly, without refitting.
</div>

<div class="term" markdown>
<p class="term__name">SISA</p>

Sharded, Isolated, Sliced, Aggregated training. It splits the data so forgetting retrains one small piece exactly. See [SISA](../unlearning/sisa.md).
</div>

<div class="term" markdown>
<p class="term__name">Softmax</p>

A function that turns raw scores into probabilities that add up to 1.
</div>

<div class="term" markdown>
<p class="term__name">Summation form</p>

A model built from sums over the training data, so forgetting is a subtraction (Cao and Yang, 2015).
</div>

<div class="term" markdown>
<p class="term__name">Support vector</p>

A training point on the edge of an SVM's margin. Only these decide the boundary. See [Support vector machines](../ml-basics/support-vector-machines.md).
</div>

<div class="term" markdown>
<p class="term__name">Suppression</p>

Hiding knowledge so a model does not *say* it, while it still *knows* it.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### U { #u }

<div class="term" markdown>
<p class="term__name">Utility</p>

Whether the model is still useful, usually its accuracy on the retain and test sets.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### W { #w }

<div class="term" markdown>
<p class="term__name">Weights (parameters)</p>

The learnt numbers inside a model. See [What is machine learning?](../ml-basics/what-is-machine-learning.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### Z { #z }

<div class="term" markdown>
<p class="term__name">ZRF (Zero Retrain Forgetting)</p>

A metric from the Bad Teacher paper that measures closeness to a random model. It rated Bad Teacher above the true retrain, which shows it measures something other than unlearning.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>
