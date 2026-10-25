---
title: Final test
description: Twenty mixed questions from across the whole course.
---

# Final test

Twenty questions from across the course, in roughly the order of the lessons. Aim for 16 or more. If you miss one, the
explanation tells you which page to read again.

```quiz
title: Final test
questions:
  - q: A company deletes a person's rows from its database. What happens to a model already trained on them?
    options:
      - Nothing changes; the weights still carry their influence.
      - The model forgets them automatically.
      - The model stops working.
    answer: 0
    why: Training shaped the weights, and deleting rows does not touch them. See "Deleting is not forgetting".
  - q: What is the target an unlearning method should hit?
    options:
      - 0% accuracy on the forget set
      - The behaviour of models retrained without the forget set
      - The original model's behaviour
    answer: 1
    why: The goal is to behave as if the data had never been there. See "The gold band".
  - q: How does Gaussian Naive Bayes forget a row exactly?
    options:
      - Subtract the row from its counts and sums
      - Gradient ascent
      - Retrain for 60 epochs
    answer: 0
    why: The model is built from sums, so forgetting is a subtraction. See Lesson 01.
  - q: Which formula removes a point exactly from ridge regression?
    options:
      - The Sherman-Morrison downdate
      - Cross-entropy
      - Softmax
    answer: 0
    why: It updates the inverse directly, matching a refit to rounding error. See Lesson 02.
  - q: Why is forgetting free for most points in an SVM?
    options:
      - Only support vectors affect the boundary.
      - SVMs have no parameters.
      - SVMs never memorise.
    answer: 0
    why: Non-support vectors have zero influence. But 97.5% of Carol's digits were support vectors. See Lesson 03.
  - q: In the course's neural network, removing Carol changed what share of the weights?
    options:
      - About 1%
      - About 94%
      - None
    answer: 1
    why: Every example nudges every weight, so her influence is everywhere. See Lesson 04.
  - q: What does a membership inference attack try to find out?
    options:
      - Whether a specific example was used in training
      - The model's size
      - The best learning rate
    answer: 0
    why: It guesses membership from the model's behaviour. See "Membership inference attacks".
  - q: Twenty networks retrained without Carol scored between 47.5% and 70.0% on her digits. What does this show?
    options:
      - The gold standard is a band, not one number.
      - Retraining is broken.
      - Carol's data is noisy.
    answer: 0
    why: Random starts make retrained networks disagree, so you need several of them. See Lesson 06.
  - q: Continuing to train the original model on the retain set only is...
    options:
      - Not the same as retraining; Carol stayed far outside the band
      - Exactly the same as retraining
      - Always better than retraining
    answer: 0
    why: A model that already fits her has nothing pushing it away. See "Retraining, the gold standard".
  - q: In SISA, why is the data split by user rather than at random?
    options:
      - So that forgetting one person touches only one shard
      - So that training is faster
      - So that accuracy goes up
    answer: 0
    why: User-aware SISA forgot Carol for about 5% of a full retrain. See "SISA".
  - q: Of 46 settings of fine-tuning, gradient ascent and NegGrad+, how many passed the audit on Carol?
    options:
      - 1
      - 23
      - 46
    answer: 0
    why: The safe window for quick fixes is tiny. See Lesson 08.
  - q: SCRUB's accuracy on Carol rose again during its repair epochs. What is this called?
    options:
      - Relapse
      - Overfitting
      - Leverage
    answer: 0
    why: Her influence had been pushed aside, not removed. SCRUB+R rewinds to avoid it. See Lesson 09.
  - q: Why is "behaves like a random model" not the same as "forgotten"?
    options:
      - A model that never saw the data is still competent and confident.
      - Random models are always right.
      - Retrained models know nothing.
    answer: 0
    why: Bad Teacher's random target left a detectable trace. See "Bad Teacher".
  - q: An approximate method relearns Carol in 20 steps, while retrained models need 500. What does that mean?
    options:
      - Her data was suppressed, not removed.
      - The method is better than retraining.
      - The relearn attack is broken.
    answer: 0
    why: Fast recovery means the knowledge was only hidden. See "The unlearning audit".
  - q: On a random forget set, the original model passed the accuracy check. What does that warn you about?
    options:
      - Random forget sets and accuracy alone can certify a model that did nothing.
      - The original model had already forgotten.
      - Accuracy is the best metric.
    answer: 0
    why: Per-example privacy tests and hard requests are needed. See Lesson 11.
  - q: Exact retraining after many deletions from high-earning women made the model unfair to women. Why?
    options:
      - The remaining data under-represented them, and the model faithfully learnt that.
      - Retraining adds bias on purpose.
      - The test set changed.
    answer: 0
    why: Perfect unlearning reproduces the bias of what is left. See "Erasure requests and fairness".
  - q: After unlearning Dana from a face model, models that never saw her still recognised her after re-enrolment. What protects her?
    options:
      - Deleting her templates and blocking re-enrolment with a non-biometric key
      - More gradient ascent
      - A list of her face embeddings
    answer: 0
    why: Unlearning removes memory, not capability. See "Consent and face recognition".
  - q: Only some poisoned messages were found. What removed the backdoor?
    options:
      - Identifying the trigger word and zeroing its weights
      - Retraining without the found messages
      - Raising the learning rate
    answer: 0
    why: For poisoning, unlearn the behaviour, not just the rows. See "Poisoned data and backdoors".
  - q: A language model trained to say "(withheld)" completes a phone number when given its first digits. This is...
    options:
      - Suppression, not forgetting
      - Exact unlearning
      - Over-forgetting
    answer: 0
    why: Refusal changes what the model says, not what it knows. See "Unlearning in language models".
  - q: What makes an unlearning certificate re-verifiable by an outside auditor?
    options:
      - Deterministic training plus a hashed manifest of the rows used
      - A high test score
      - A long report
    answer: 0
    why: Anyone can retrain from the manifest and check the weights match bit for bit. See "The enterprise playbook".
```

## What next?

- Missed a few? Each explanation names the page to re-read.
- Ready for more? Try the [practice problems](../practice.md).
- Want the real thing? Run the [lessons](../lessons/index.md) in :custom-colab: Colab and do their tasks.
