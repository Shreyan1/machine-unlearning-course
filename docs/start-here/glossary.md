---
title: Glossary
description: Every term and symbol used on this site, with a plain-words meaning and a link to the page that explains it.
---

# Glossary

Every term on this site, in plain words. Each one links to the page that explains it fully.

## Symbols

| Symbol | Plain meaning |
|---|---|
| `D` | The full training set. |
| `D_f` | The **forget set**: the data that must be removed. |
| `D_r` | The **retain set**: everything else in training, so `D = D_r ∪ D_f`. |
| `D_test` | Data the model never trained on, used to measure usefulness. |
| `θ_o` | The **original** model, trained on `D`. |
| `θ_r` | The **retrained** model, trained on `D_r` only: the gold standard. |
| `θ_u` | The **unlearnt** model, produced by an unlearning method from `θ_o`. |

See [The notation](../unlearning/notation.md).

## Terms

Adapter (LoRA)
:   A small add-on trained on top of a frozen base model, often one per customer. Deleting it removes that customer
    exactly. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).

Approximate unlearning
:   A cheap method that edits a trained model with no guarantee; its result must be audited.
    See [Quick fixes and their traps](../unlearning/approximate-unlearning.md).

Attack success rate (ASR)
:   For a backdoor: the share of triggered inputs that get the attacker's desired result.
    See [Poisoned data and backdoors](../unlearning/poisoning-and-backdoors.md).

AUC
:   A score for how well an attack separates two groups: 0.5 is a coin flip, 1.0 is always right.
    See [Membership inference attacks](../unlearning/membership-inference-attacks.md).

Backdoor
:   A hidden rule an attacker teaches a model through poisoned data, such as "let any message with *zqx* through".

Bad Teacher
:   An approximate method in which the student copies a random, know-nothing model on the forget set.
    See [Bad Teacher](../unlearning/bad-teacher.md).

Certificate
:   A record of how a deletion was done and how to check it. The best ones can be recomputed by anyone.
    See [The enterprise playbook](../unlearning/enterprise-playbook.md).

Cross-entropy
:   The usual loss for classification: small when the model gives high probability to the right answer.
    See [Loss functions](../ml-basics/loss-functions.md).

Epoch
:   One pass over all the training data. See [Gradient descent](../ml-basics/gradient-descent.md).

Exact unlearning
:   A method whose result is guaranteed to match retraining without the data.
    See [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md).

Exposure
:   For a secret such as a phone number: how highly the model ranks the real value among all possible values.
    See [Unlearning in language models](../unlearning/llm-unlearning.md).

Fine-tuning
:   Continuing to train an existing model on new, specific data. See [Fine-tuning and LoRA](../ml-basics/fine-tuning-and-lora.md).

Forging
:   Reaching the same final weights with or without a given example, which is why weights alone cannot prove forgetting.
    See [Can a test prove forgetting?](../unlearning/testing-vs-proving.md).

Gold band
:   The range of results from several models retrained without the forget set. A method passes if it lands inside.
    See [The gold band](../unlearning/gold-band.md).

Gold standard
:   The model retrained from scratch without the forget set. See [Retraining, the gold standard](../unlearning/retraining-gold-standard.md).

Gradient
:   The direction in which each weight should move to increase the loss. See [Gradient descent](../ml-basics/gradient-descent.md).

Gradient ascent
:   Stepping *uphill* on the loss of the forget set, to make the model worse on it. Simple and risky.

Hessian
:   A table of the loss's curvature, with one row and one column per weight. Needed for a Newton step; far too large for
    deep models. See [Logistic regression](../ml-basics/logistic-regression.md).

KL divergence
:   A number for how different two sets of probabilities are; 0 means identical.
    See [Probabilities and KL divergence](../ml-basics/probabilities-and-kl-divergence.md).

Leverage
:   How hard one training point pulls a linear model towards itself. See [Linear and ridge regression](../ml-basics/linear-and-ridge-regression.md).

Lineage registry
:   A record of every model and which data reached it, directly or through a parent.
    See [The enterprise playbook](../unlearning/enterprise-playbook.md).

LiRA / U-LiRA
:   Per-example membership tests that compare a model with shadow models trained with and without each example.
    See [Membership inference attacks](../unlearning/membership-inference-attacks.md).

Locality
:   When only some parts of a model depend on a given point, so only those parts need rebuilding.
    See [Exact unlearning for classical models](../unlearning/exact-unlearning-classical.md).

Membership inference attack (MIA)
:   An attempt to tell, from a model's behaviour, whether an example was in its training data.

Memorisation
:   When a model gets an example right *because* it was trained on that exact example.
    See [Overfitting and memorisation](../ml-basics/overfitting-and-memorisation.md).

NegGrad+
:   Gradient ascent on the forget set combined with normal training on the retain set in every step.

Newton step
:   A jump to the estimated new best weights using the gradient and the Hessian.
    See [Logistic regression](../ml-basics/logistic-regression.md).

NPO
:   Negative Preference Optimisation: gradient ascent for language models that stops pushing once the model has forgotten.

Over-forgetting
:   Being *suspiciously* bad on the forget set, worse than models that never saw it. It is a failure too.

Overfitting
:   Being much better on training data than on new data.

Prefix forcing
:   Typing the start of a secret and letting a language model finish it. Reveals suppressed facts.

Recall@10
:   For a recommender: the share of a user's hidden items that appear in their top 10.

Refusal training
:   Teaching a model to say something like "(withheld)". It is suppression, not forgetting.

Relearn attack
:   Briefly reminding a model of some forgotten data and seeing how fast the rest comes back. Fast recovery means
    suppression. See [The unlearning audit](../unlearning/unlearning-audit.md).

Retain set
:   Everything in training except the forget set.

SCRUB / SCRUB+R
:   An approximate method in which a student copies the original model on the retain set and moves away from it on
    the forget set; SCRUB+R adds a rewind. See [SCRUB](../unlearning/scrub.md).

Shadow model
:   A model trained by an attacker or auditor, with or without an example, to see how such models usually behave.

Sherman-Morrison downdate
:   A formula that removes a point from ridge regression exactly, without refitting.

SISA
:   Sharded, Isolated, Sliced, Aggregated training: split the data so forgetting retrains one small piece exactly.
    See [SISA](../unlearning/sisa.md).

Softmax
:   A function that turns raw scores into probabilities that add up to 1.

Summation form
:   A model built from sums over the training data, so forgetting is a subtraction (Cao and Yang, 2015).

Support vector
:   A training point on the edge of an SVM's margin. Only these decide the boundary.
    See [Support vector machines](../ml-basics/support-vector-machines.md).

Suppression
:   Hiding knowledge so a model does not *say* it, while it still *knows* it.

Utility
:   Whether the model is still useful, usually its accuracy on the retain and test sets.

Weights (parameters)
:   The learnt numbers inside a model. See [What is machine learning?](../ml-basics/what-is-machine-learning.md).

ZRF (Zero Retrain Forgetting)
:   A metric from the Bad Teacher paper that measures closeness to a random model. It rated Bad Teacher above the true
    retrain, which shows it measures something other than unlearning.
