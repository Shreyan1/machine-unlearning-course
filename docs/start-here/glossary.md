---
title: Glossary
description: Every term and symbol used on this site, with a plain-words meaning and a link to the page that explains it.
---

# Glossary

Every term on this site, in plain words. Each one links to the page that explains it fully. Use the letters to jump
straight to a section.

<nav class="az" aria-label="Jump to a letter"><a href="#a">A</a><a href="#b">B</a><a href="#c">C</a><a href="#d">D</a><a href="#e">E</a><a href="#f">F</a><a href="#g">G</a><a href="#h">H</a><a href="#i">I</a><span aria-disabled="true">J</span><a href="#k">K</a><a href="#l">L</a><a href="#m">M</a><a href="#n">N</a><a href="#o">O</a><a href="#p">P</a><a href="#q">Q</a><a href="#r">R</a><a href="#s">S</a><a href="#t">T</a><a href="#u">U</a><a href="#v">V</a><a href="#w">W</a><span aria-disabled="true">X</span><span aria-disabled="true">Y</span><a href="#z">Z</a></nav>

## Symbols

| Symbol | Plain meaning |
|---|---|
| \(D\) | The full training set. |
| \(D_f\) | The **forget set**, which is the data that must be removed. |
| \(D_r\) | The **retain set**, which is everything else in training, so \(D = D_r \cup D_f\). |
| \(D_{\text{test}}\) | Data the model never trained on, used to measure usefulness. |
| \(\theta_o\) | The **original** model, trained on \(D\). |
| \(\theta_r\) | The **retrained** model, trained on \(D_r\) only. It is the gold standard. |
| \(\theta_u\) | The **unlearnt** model, produced by an unlearning method from \(\theta_o\). |

See [The notation](../unlearning/notation.md).

## Terms

### A { #a }

<div class="term" markdown>
<p class="term__name">Abliteration</p>

Removing the "refusal direction" from an open model's weights so that it stops refusing. It is a one-direction edit, and it shows that a refusal only hides what a model knows. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

<div class="term" markdown>
<p class="term__name">Adapter (LoRA)</p>

A small add-on trained on top of a frozen base model, often one per customer. Deleting it removes that customer exactly. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).
</div>

<div class="term" markdown>
<p class="term__name">Algorithmic disgorgement</p>

An order to delete the models and algorithms built from unlawfully collected data, not just the data itself. Regulators in the US and South Korea have already given such orders. See [Policies around the world](../unlearning/global-policy.md).
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

A score for how well an attack separates two groups. A score of 0.5 is a coin flip; 1.0 is always right. See [Membership inference attacks](../unlearning/membership-inference-attacks.md).
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

<div class="term" markdown>
<p class="term__name">Batching</p>

Saving up deletion requests and handling them together, for example once a month, instead of one at a time. Over a year it made plain retraining about 8 times cheaper but saved SISA little. Every request must still be finished before its legal deadline. See [Unlearning at scale](../unlearning/unlearning-at-scale.md).
</div>

<div class="term" markdown>
<p class="term__name">Bootstrap sample</p>

A training set drawn at random from the data with replacement, so some rows appear twice and others not at all. Each tree in a random forest gets its own. See [Decision trees and random forests](../ml-basics/decision-trees-and-random-forests.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### C { #c }

<div class="term" markdown>
<p class="term__name">Certificate</p>

A record of how a deletion was done and how to check it. The best ones can be recomputed by anyone. See [The enterprise playbook](../unlearning/enterprise-playbook.md).
</div>

<div class="term" markdown>
<p class="term__name">Certified removal</p>

A certified unlearning recipe from Guo et al. 2019 for models with one best answer, such as logistic regression. Training adds a small random term to the loss. To delete, one Newton step removes the point's influence, and the noise hides the small error left over; once the noise budget is used up, you must retrain. See [Certified unlearning](../unlearning/certified-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Certified unlearning</p>

A mathematical promise that the unlearnt model is almost impossible to tell apart from a model retrained without the data. How close is measured by two small numbers, ε and δ, as in differential privacy. Today's proofs mostly cover models with one best answer, such as logistic regression, not deep networks. See [Certified unlearning](../unlearning/certified-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Checkpoint</p>

A saved copy of a model's weights at one point in training. If you keep a checkpoint from before some data entered, you can retrain from there without that data and get an exact result for less than a full retrain. SISA saves one after every slice. See [SISA](../unlearning/sisa.md).
</div>

<div class="term" markdown>
<p class="term__name">Cross-entropy</p>

The usual loss for classification. It is small when the model gives high probability to the right answer. See [Loss functions](../ml-basics/loss-functions.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### D { #d }

<div class="term" markdown>
<p class="term__name">Data-driven methods</p>

One of three families of unlearning methods. They work on the data side, for example by splitting the data as SISA does or by training on made-up noise as UNSIR does. See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">Differential privacy (DP)</p>

A promise that a model behaves almost the same whether or not any one record was in its training data. ε (epsilon) limits how much the two can differ, so a small ε is a strong promise and a large one, such as 10, promises very little; δ (delta) is a tiny chance that the promise fails. A model trained this way already counts as certified unlearning for one record, at a cost in accuracy. See [Certified unlearning](../unlearning/certified-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Direction</p>

A pattern of activity across many neurons at once. If a hidden state is pictured as an arrow, a direction is a way the arrow can point. Some behaviours, such as refusing or looping, move the hidden state along one direction. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

<div class="term" markdown>
<p class="term__name">Distillation</p>

Training a *student* model to copy the probabilities of a *teacher* model. What the teacher learnt from its data passes to the student, so distilled models must be included when that data is deleted. See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### E { #e }

<div class="term" markdown>
<p class="term__name">Eigenface</p>

A face pattern that PCA (a method that finds the main patterns in data) learns from training photos. Together, the eigenfaces form the "face space" that a classical face-ID system uses to compare photos. PCA is built from sums, so one person can be subtracted from it exactly. See [Consent and face recognition](../unlearning/consent-and-face-recognition.md).
</div>

<div class="term" markdown>
<p class="term__name">Embedding</p>

A list of numbers that captures the meaning of a piece of text, so that texts with similar meanings get similar numbers. Embeddings are not anonymous, because the text can often be rebuilt from them. See [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md).
</div>

<div class="term" markdown>
<p class="term__name">Entropy</p>

How spread out a model's probabilities are. Low entropy means the model is sure of one answer, high entropy means it is unsure. Bad Teacher is judged partly by whether its entropy on the forget set looks like a retrained model's. See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).
</div>

<div class="term" markdown>
<p class="term__name">Epoch</p>

One pass over all the training data. See [Gradient descent](../ml-basics/gradient-descent.md).
</div>

<div class="term" markdown>
<p class="term__name">Equal opportunity</p>

A fairness check. Among people who truly deserve a positive answer, it compares how often each group gets one, using the true positive rate for women and for men. See [Erasure requests and fairness](../unlearning/fairness-and-erasure.md).
</div>

<div class="term" markdown>
<p class="term__name">Evidence record</p>

A file, in a form a computer can read, that records an audit's protocol, its gold band, every number and every verdict. It lets someone else check the result. See [The unlearning audit](../unlearning/unlearning-audit.md).
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
<p class="term__name">False alarm</p>

When a statistical check rejects a model that is actually fine. In Lesson 11, SISA, which is exact, failed the FORGET check on Carol by one digit. A FAIL is a reason to investigate, not an automatic verdict. See [Can a test prove forgetting?](../unlearning/testing-vs-proving.md).
</div>

<div class="term" markdown>
<p class="term__name">Federated unlearning</p>

Forgetting one participant, such as a phone or a hospital, from a model trained by federated learning. In federated learning the data never leaves the participants; they send only updates, which the server averages over many rounds. Every later round builds on the leaver's updates, and the server never had their data. See [Federated unlearning](../unlearning/federated-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Fine-tuning</p>

Continuing to train an existing model on new, specific data. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).
</div>

<div class="term" markdown>
<p class="term__name">Fingerprint</p>

The gap between how well a model does on someone's own data and on unseen data like theirs. The original model read 100% of Carol's digits but only 77.5% of unseen thick-marker digits; after retraining without her, the gap was gone. See [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Forget set</p>

The data that must be removed from a model, written \(D_f\). In the course it is often Carol's 40 handwritten digits. See [The notation](../unlearning/notation.md).
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

<div class="term" markdown>
<p class="term__name">Hidden state</p>

The list of numbers that the neurons of one hidden layer produce for one input. It is what the next layer reads. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

### I { #i }

<div class="term" markdown>
<p class="term__name">Influence function</p>

A calculation that estimates how much one training example shaped a model, and so roughly what removing it would change, without retraining. It combines the example's gradient with the Hessian. The estimate is close for models with one best answer, such as ridge and logistic regression, and rough for neural networks. See [Influence functions](../unlearning/influence-functions.md).
</div>

<div class="term" markdown>
<p class="term__name">Item-kNN</p>

A recommender built from one table that counts how many people watched each pair of items, such as films. The table is a sum over users, so forgetting someone is an exact subtraction. See [Recommender systems](../ml-basics/recommender-systems.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### K { #k }

<div class="term" markdown>
<p class="term__name">Kernel</p>

A way for a support vector machine to measure how alike two inputs are, which lets it draw curved boundaries. See [Support vector machines](../ml-basics/support-vector-machines.md).
</div>

<div class="term" markdown>
<p class="term__name">KL divergence</p>

A number for how different two sets of probabilities are; 0 means identical. See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

<div class="term" markdown>
<p class="term__name">Knowledge neuron</p>

A neuron whose activity goes with one fact, so that switching it off seems to remove the fact (Dai et al. 2022). In practice a fact is usually spread over many neurons. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

### L { #l }

<div class="term" markdown>
<p class="term__name">L1-sparse</p>

An approximate method that fine-tunes the model with a penalty that pushes small weights to zero (Jia et al. 2023). In Lesson 19 it first passed a privacy test on Carol while still getting all 40 of her digits right; with fair references, the pass disappeared. See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">Ladder of Forgetting</p>

The map of the course. It orders models from easy to forget, where forgetting is a subtraction, to hard to forget, such as large language models. Each rung explains what makes the next one harder. See [The Ladder of Forgetting](../unlearning/ladder-of-forgetting.md).
</div>

<div class="term" markdown>
<p class="term__name">Layer-below attack</p>

A test for an edited model. The attacker keeps every layer except the last, trains a new last layer on data they already have and checks whether the "removed" fact comes back. It catches edits that only changed what the last layer said. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

<div class="term" markdown>
<p class="term__name">Learning rate</p>

How big a step gradient descent takes each time it changes the weights. Too small and training crawls, too large and the loss jumps about instead of falling. See [Gradient descent](../ml-basics/gradient-descent.md).
</div>

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

<div class="term" markdown>
<p class="term__name">Logit</p>

The raw score a model gives each class before the softmax turns the scores into probabilities. A higher logit means a more likely class. See [Loss functions](../ml-basics/loss-functions.md).
</div>

<div class="term" markdown>
<p class="term__name">Loss</p>

One number that says how wrong a model is, on one example or on average. Training changes the weights to make it smaller. The course mostly uses cross-entropy, which is minus the log of the probability the model gave the right answer. See [Loss functions](../ml-basics/loss-functions.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### M { #m }

<div class="term" markdown>
<p class="term__name">Machine unlearning</p>

Removing the influence of some data from a model that has already been trained, so that it behaves as if it had never seen that data. It also means showing, with evidence, that the influence is gone. See [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Margin</p>

The gap between a support vector machine's boundary and the nearest training points. The machine places the boundary to make this gap as wide as it can. See [Support vector machines](../ml-basics/support-vector-machines.md).
</div>

<div class="term" markdown>
<p class="term__name">Matrix factorisation</p>

A recommender that gives every user and every item a short list of numbers (32 in the course) and predicts a match when they line up. Everything is fitted together, so deleting a user's own numbers leaves their influence in the item numbers. An exact result needs a retrain. See [Unlearning in recommenders](../unlearning/recommender-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Membership inference attack (MIA)</p>

An attempt to tell, from a model's behaviour, whether an example was in its training data.
</div>

<div class="term" markdown>
<p class="term__name">Memorisation</p>

When a model gets an example right *because* it was trained on that exact example. See [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md).
</div>

<div class="term" markdown>
<p class="term__name">Model-agnostic methods</p>

One of three families of unlearning methods. They work on any model, without needing to know how it is built inside. See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">Model editing</p>

Changing what a model says about one fact by making a small change to a few weights. It is a quick way to fix errors, but it is not unlearning, because an edited-away fact can often be recovered by asking in another way. See [Model editing vs unlearning](../unlearning/editing-vs-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">Model-intrinsic methods</p>

One of three families of unlearning methods. They use the insides of one kind of model, so they do not work on every model. See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">MUSE</p>

A benchmark (a shared test for comparing methods) that checks six things people want from unlearning in language models, from removing word-for-word text to keeping the model useful. See [State of the field](../unlearning/state-of-the-field.md).
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
<p class="term__name">Pre-registration</p>

Fixing every method's settings, the tests and the pass marks before running anything, so that results cannot be tuned to look good. In production there is no gold band to tune against, so a fair audit must not tune against one either. See [The unlearning audit](../unlearning/unlearning-audit.md).
</div>

<div class="term" markdown>
<p class="term__name">Prefix forcing</p>

Typing the start of a secret and letting a language model finish it. Reveals suppressed facts.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### Q { #q }

<div class="term" markdown>
<p class="term__name">Quantisation</p>

Rounding a model's weights to fewer possible values, for example 4-bit numbers, so that it is smaller and runs on smaller hardware. The rounding can wipe out the tiny weight changes made by approximate unlearning and bring the forgotten behaviour back, so test the compressed model too. See [When forgotten knowledge comes back](../unlearning/relearning-and-quantization.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### R { #r }

<div class="term" markdown>
<p class="term__name">Random labels</p>

An approximate method that gives the forget data random wrong labels and keeps training (Graves et al. 2021). See [The method zoo](../unlearning/method-zoo.md).
</div>

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

<div class="term" markdown>
<p class="term__name">Retrieval-augmented generation (RAG)</p>

A setup in which a search step finds relevant passages in a database and the language model reads them while it answers, instead of memorising them. Forgetting someone is then mostly ordinary deletion, as long as you find every copy. See [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md).
</div>

<div class="term" markdown>
<p class="term__name">Right to erasure (GDPR Article 17)</p>

A person's legal right to have their personal data erased, also called the right to be forgotten. GDPR Art. 17 gives it in the EU, and India's DPDP Act and California's CCPA give similar rights. None of these laws mentions model weights. See [Why the law cares](../unlearning/why-the-law-cares.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

<div class="term" markdown>
<p class="term__name">ROME and MEMIT</p>

Two model-editing methods (Meng et al. 2022 and 2023). They treat a layer as a memory of keys and values, and rewrite the value for one fact, or many, in closed form with no training. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

### S { #s }

<div class="term" markdown>
<p class="term__name">SalUn</p>

Saliency unlearning, an approximate method that gives the forget data random labels but only moves the weights that matter most for that data (Fan et al. 2024). See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">SCRUB / SCRUB+R</p>

An approximate method in which a student copies the original model on the retain set and moves away from it on the forget set; SCRUB+R adds a rewind. See [SCRUB](../unlearning/scrub.md).
</div>

<div class="term" markdown>
<p class="term__name">Shadow model</p>

A model trained by an attacker or auditor, with or without an example, to see how such models usually behave.
</div>

<div class="term" markdown>
<p class="term__name">Shard</p>

One of the separate parts that SISA splits the training data into. Each shard trains its own model, so forgetting a row retrains only the shard that held it. See [SISA](../unlearning/sisa.md).
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
<p class="term__name">Slice</p>

A smaller part of a shard in SISA. The shard's data is fed in slice by slice, with a checkpoint saved after each, so retraining can start just before the slice that held the deleted row. See [SISA](../unlearning/sisa.md).
</div>

<div class="term" markdown>
<p class="term__name">Softmax</p>

A function that turns raw scores into probabilities that add up to 1.
</div>

<div class="term" markdown>
<p class="term__name">SSD (selective synaptic dampening)</p>

An approximate method that needs no training (Foster et al. 2024). It shrinks the weights that matter far more for the forget data than for the whole training set. In Lesson 19 it changed no weights at all on the class request, because the whole set includes the forget data. See [The method zoo](../unlearning/method-zoo.md).
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

<div class="term" markdown>
<p class="term__name">Surgical weight editing</p>

Changing a few of a model's weights by hand, with a formula and no training, to switch something off. It can remove a habit, but it did not remove a person's data in Lesson 22. See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

### T { #t }

<div class="term" markdown>
<p class="term__name">Task vector</p>

The change that fine-tuning made to a model's weights, an idea from Ilharco et al. 2023. Subtracting it, scaled by a number λ, is a cheap way to try to remove a customer. In Lesson 15 no value of λ matched the exact result for both the leaving and the remaining customers. See [Unlearning a fine-tune](../unlearning/unlearning-fine-tunes.md).
</div>

<div class="term" markdown>
<p class="term__name">Teacher and student</p>

Two models in distillation. The student is trained to copy the teacher's probabilities. SCRUB and Bad Teacher use this to steer an unlearnt model. See [SCRUB](../unlearning/scrub.md).
</div>

<div class="term" markdown>
<p class="term__name">Temperature</p>

A number that softens a model's probabilities before they are compared. A higher temperature spreads them out, so a student learns more from the teacher's second choices. See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).
</div>

<div class="term" markdown>
<p class="term__name">TOFU</p>

A benchmark that fine-tunes a language model on made-up author biographies and then asks it to forget some authors. Because the authors are fictional, nothing else in the training data can leak them. See [State of the field](../unlearning/state-of-the-field.md).
</div>

<div class="term" markdown>
<p class="term__name">Tombstone</p>

A mark that says a row or index entry is deleted, so that searches skip it. The data itself may still be stored until the index is cleaned up (compacted) or rebuilt, so a mark alone is not a full deletion. See [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md).
</div>

<div class="term" markdown>
<p class="term__name">True positive rate (TPR)</p>

Of all the cases that really are positive, the share that a model or an attack correctly flags. Lesson 12 compares it for women and men to check fairness, and membership attacks report it at a low false-positive rate. See [Erasure requests and fairness](../unlearning/fairness-and-erasure.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### U { #u }

<div class="term" markdown>
<p class="term__name">Under-forgetting</p>

Still doing *too well* on the forget set, above the gold band, so the model behaves as if it still remembers. It is the usual failure of a quick fix that stops too early. See [Approximate unlearning](../unlearning/approximate-unlearning.md).
</div>

<div class="term" markdown>
<p class="term__name">UNSIR</p>

An approximate method that learns "noise" images the model gets wrong, trains on them and then repairs the model (Tarun et al. 2023). See [The method zoo](../unlearning/method-zoo.md).
</div>

<div class="term" markdown>
<p class="term__name">User-aware partition</p>

A way of splitting SISA's data so that all of one person's rows sit in one shard. Forgetting Carol then cost about 5% of a full retrain, against 61.4% when the split was random. See [SISA](../unlearning/sisa.md).
</div>

<div class="term" markdown>
<p class="term__name">Utility</p>

Whether the model is still useful, usually its accuracy on the retain and test sets.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### V { #v }

<div class="term" markdown>
<p class="term__name">Vector store</p>

A database that keeps embeddings and finds the ones nearest to a question, as k-NN does. A RAG system uses it to look up passages. Deleting from it is exact and cheap, but some stores only mark entries as deleted until the index is rebuilt. See [Deleting from RAG, vector stores and caches](../unlearning/rag-and-vector-stores.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### W { #w }

<div class="term" markdown>
<p class="term__name">Weight-space programming</p>

Reading and writing a network's weights directly, instead of training it. In November 2026 a frontier model used it to stop a smaller model looping (Takehi et al. 2026). See [Surgical weight editing](../unlearning/surgical-weight-editing.md).
</div>

<div class="term" markdown>
<p class="term__name">Weights (parameters)</p>

The learnt numbers inside a model. See [What is machine learning?](../ml-basics/what-is-machine-learning.md).
</div>

<div class="term" markdown>
<p class="term__name">WMDP</p>

A benchmark that measures hazardous knowledge, such as biosecurity and cybersecurity, that a model should not be able to provide. See [State of the field](../unlearning/state-of-the-field.md).
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>

### Z { #z }

<div class="term" markdown>
<p class="term__name">ZRF (Zero Retrain Forgetting)</p>

A metric from the Bad Teacher paper that measures closeness to a random model. It rated Bad Teacher above the true retrain, which shows it measures something other than unlearning.
</div>

<p class="az__top"><a href="#glossary">↑ Back to the A–Z</a></p>
