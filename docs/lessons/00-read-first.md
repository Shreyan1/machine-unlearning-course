---
title: "Lesson 00 · Read this first"
description: Meet Carol, the notation, the gold standard and the Ladder of Forgetting, with the whole course in four code cells.
---

# Lesson 00 · Read this first

<div class="chips" markdown><span class="chip" markdown="span">:material-clock-outline: ~1 hr</span><span class="chip" markdown="span">:material-map-marker-path: Stage 0 · Foundations</span><span class="chip" markdown="span">:material-stairs-up: Start here</span></div>

<div class="buttons" markdown>
[:custom-colab: Open in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb){ .md-button .md-button--primary }
[:fontawesome-brands-github: View on GitHub](https://github.com/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb){ .md-button }
</div>

!!! mission "Your mission · about 20 minutes · 3 checkpoints"
    By the end of this lesson you can

    - explain why deleting training data does not remove it from a trained model,
    - name the seven symbols every lesson uses and say which model is the target,
    - read Carol's before-and-after numbers and say why the target is not 0%.

## The story

A digit-recognition model is trained on 1,257 handwritten digits. Forty of them were written by **Carol**, with a thick
marker that nobody else used. Carol now asks to be deleted. This lesson introduces the whole course. It explains why unlearning is needed and sets out the notation and the map of methods. It also gives a 60-second preview of the full loop.

Her request is not a polite favour. Laws such as GDPR Article 17 give people the right to have their personal data
erased, and regulators have gone further. In 2021 the US FTC ordered Everalbum to delete the face-recognition
**models** it had built from users' photos, not only the photos. See [Why the law cares](../unlearning/why-the-law-cares.md).

So the company has two choices. It can throw the model away and train a new one each time someone asks, or it can find
a cheaper way to make the model forget, and then prove that it worked. **Machine unlearning** is the second choice.
Think of a cookbook. You can tear a page out, but you cannot un-bake the cake you made from it. The model is the cake.

## What you will do

<ol class="steps" markdown>
<li markdown>**Train** a small neural network on all 1,257 digits, including Carol's.</li>
<li markdown>**Show the issue.** Compare its accuracy on Carol's digits with unseen thick-marker digits.</li>
<li markdown>**Untrain** with the simplest exact method, which is to retrain without her.</li>
<li markdown>**Show the result** side by side.</li>
<li markdown>**Prove it.** The retrained model treats her digits like any other unseen thick-marker digits.</li>
</ol>

These five steps are the rhythm of every lesson in the course, so you always know where you are.

## What each step teaches

**Train.** The model learns from all 1,257 digits, so it learns from Carol too. This creates the problem on purpose,
in a setting small enough to retrain in a fraction of a second.

**Show the issue.** A score on Carol alone cannot tell memory from skill, because thick digits might simply be easy.
So the lesson also scores 80 look-alike digits, made thick in the same way but never trained on. If the model is much
better on Carol's own digits than on the look-alikes, it has memorised *her*.

**Untrain.** Deleting her 40 rows from the database changes nothing, because the weights are already trained. The
simplest exact fix is to train a fresh model on the 1,217 digits that are left. This is the **gold standard**, the
model you would have had if Carol had never been there.

**Show the result.** The two models are scored side by side on the same three sets, so the change is easy to read.

**Prove it.** The honest test is a comparison with a model that never saw the data. After retraining, her digits
should get no special treatment. They should be read about as well as the look-alikes, while everyone else's accuracy
stays the same.

??? checkpoint "Checkpoint 1 · Carol's 40 rows are deleted from the company's database, but the trained model is kept. What has the model forgotten?"
    **Nothing.** A trained model never reads its training data again. It only uses its weights, and those were
    shaped by her digits. Removing what the model learnt from her needs retraining or an unlearning method.

## The notation and the map

Every lesson uses the same seven symbols. Three are for the data, one is for testing and three are for the models.

| Symbol | Meaning | In the digit lab |
|---|---|---|
| \(D\) | The full training set | 1,257 digits |
| \(D_f\) | The **forget set**, the data that must be removed | Carol's 40 digits |
| \(D_r\) | The **retain set**, everything else | 1,217 digits |
| \(D_{\text{test}}\) | Data the model never trained on, to measure usefulness | 540 digits |
| \(\theta_o\) | The **original** model, trained on \(D\) | The model that read 100% of Carol |
| \(\theta_r\) | The **retrained** model, trained on \(D_r\) only, the gold standard | The model that read 55.0% of Carol |
| \(\theta_u\) | The **unlearnt** model, made by an unlearning method from \(\theta_o\) | What every later lesson builds |

The single most important idea of the course is that \(\theta_u\) should behave like \(\theta_r\). Every clever method
tries to reach that answer cheaply, and every test checks how close it got. More on the symbols is on
[The notation](../unlearning/notation.md).

??? deep "Go deeper · the map of methods"
    The course groups every method into four families. Each later lesson sits in at least one of them.

    | Family | Examples | Guarantee | Cost | Lessons |
    |---|---|---|---|---|
    | **Exact, classical** | Delete, subtract, downdate, retrain a part | The result provably equals retraining | Tiny | 01, 02, 03, 13, 14, 16 |
    | **Exact, neural** | Retrain, SISA, adapters, re-fine-tune from a checkpoint | The result provably equals retraining | High, or needs planning at training time | 06, 07, 15, 16 |
    | **Approximate** | Newton step, fine-tune, gradient ascent, NegGrad+, SCRUB, Bad Teacher, task vectors, NPO | None, so it must be audited | Low | 02, 08, 09, 10, 15, 16 |
    | **Auditing** | Membership inference, gold band, relearn attack, exposure, fairness | Tells you whether the above worked | Moderate | 05, 11, 12, 16 |

    The lessons climb the [Ladder of Forgetting](../unlearning/ladder-of-forgetting.md), from models where forgetting
    is a subtraction up to language models, where nobody can yet do it reliably. Each lesson starts from the limit
    the previous one ran into.

??? checkpoint "Checkpoint 2 · An unlearning method takes the original model and Carol's digits and returns a new model. Which symbol is the result, and what should it behave like?"
    **\(\theta_u\), and it should behave like \(\theta_r\).** The method starts from \(\theta_o\), which saw Carol.
    Its result is judged against the model retrained on \(D_r\) only, the one that never saw her. An exact method
    matches \(\theta_r\) by construction, and an approximate one must be measured.

## Key results

<div class="stats">
<div class="is-bad"><strong>100.0%</strong><span>original model on Carol's 40 digits</span></div>
<div><strong>77.5%</strong><span>original model on unseen thick-marker digits</span></div>
<div class="is-good"><strong>55.0%</strong><span>retrained model on Carol, near 62.5% on look-alikes</span></div>
<div class="is-good"><strong>98.0%</strong><span>test accuracy for everyone else, before and after</span></div>
</div>

| Model | Carol's digits (\(D_f\)) | Unseen thick-marker digits | Test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

- The 100% versus 77.5% gap is Carol's **fingerprint**, because the model memorised *her* digits, not just thick digits.
- After retraining, her digits get no special treatment, and everyone else's accuracy is unchanged.
- Her accuracy is **not 0%**. The target is the retrained model, not zero. This is the idea most unlearning tutorials
  get wrong.

Read the first row as a gap. The original model gets all 40 of Carol's digits right but only 77.5% of the 80
look-alikes, so her own digits score 22.5 points higher than digits like hers. That extra is what it memorised.

Read the second row the same way. The retrained model gets 55.0% of Carol's digits, which is 22 of 40, and 62.5% of
the look-alikes. It never saw her, yet it still reads more than half of her digits, because it learnt what digits look
like from everyone else. Her digits are now treated like strangers' digits. The test column stays at 98.0%, so
removing Carol cost typical users nothing. People who write like her lose a little, as the look-alike column shows.

The catch is that retraining took a third of a second here. For a model that costs weeks of GPU time, it is not affordable.
That is where the rest of the course begins.

??? checkpoint "Checkpoint 3 · What is Carol's gap, her accuracy minus the look-alikes', before and after retraining?"
    **+22.5 points before and −7.5 after.** Before, 100.0 − 77.5 = 22.5. After, 55.0 − 62.5 = −7.5. The large positive
    gap was memory of her. After retraining her digits are no easier than digits like hers, which is what a model that
    never saw her looks like.

## Limits of this lesson

**One retrained model.** The 55.0% comes from one retrain with one random seed. Retraining with other seeds gives
different scores on Carol, so one model is one roll of the dice. Lesson 06 turns this into the
[gold band](../unlearning/gold-band.md).

**A small, made-up setting.** The digits are 8 × 8 pixels and Carol's style is made by widening every stroke. Real
models and real people are bigger and messier, but the same measurements carry over.

**Accuracy is a coarse check.** Accuracy on 40 digits moves in steps of 2.5 points, and it cannot see everything a
model remembers. Lesson 05 adds attacks that look at each example.

## Concepts used here

- [What is machine unlearning?](../unlearning/what-is-machine-unlearning.md)
- [Deleting is not forgetting](../unlearning/deleting-vs-unlearning.md)
- [Why the law cares](../unlearning/why-the-law-cares.md)
- [The notation](../unlearning/notation.md)
- [The Ladder of Forgetting](../unlearning/ladder-of-forgetting.md)

## Notes to take

!!! notes "Notes to take"
    - **Unlearning.** Removing the influence of specific data from a model that is already trained.
    - **Deleting is not forgetting.** Deleting rows leaves the trained weights unchanged.
    - **Why.** The right to erasure, and regulators such as the FTC already order models to be deleted.
    - **Rhythm.** Train, show the issue, untrain, show the result, prove it.
    - **Symbols.** \(D = D_r \cup D_f\). \(\theta_o\) original, \(\theta_r\) retrained, \(\theta_u\) unlearnt.
    - **Target.** \(\theta_u\) should behave like \(\theta_r\), the gold standard.
    - **Carol before.** 100.0% on her digits, 77.5% on look-alikes, a gap of +22.5 points.
    - **Carol after retraining.** 55.0% against 62.5%, test still 98.0%.
    - **Trap.** The target is the retrained model, not 0%.

## Quiz

```quiz
- q: Before unlearning, the model is 100% right on Carol's digits and 77.5% on unseen thick-marker digits. What does the gap show?
  options:
    - The model memorised Carol's specific digits.
    - The test set is broken.
    - Thick digits are always easy.
  answer: 0
  why: It is much better on her exact digits than on similar ones it never saw.
- q: After retraining without Carol, what is her accuracy?
  options:
    - 0%
    - 55.0%
    - 100%
  answer: 1
  why: A model that never met her still reads many of her digits, because it learnt digits from everyone else.
- q: What is \(\theta_r\)?
  options:
    - The original model
    - The model retrained on the retain set only
    - The unlearnt model
  answer: 1
  why: \(\theta_r\) is the gold standard that every unlearning method tries to match.
- q: Which of these is a real case where a regulator ordered a model to be deleted?
  options:
    - FTC v. Everalbum (2021)
    - The Netflix Prize (2006)
    - The ImageNet challenge (2012)
  answer: 0
  why: The FTC ordered Everalbum to delete the face-recognition models built from users' photos.
- q: Why is retraining not the end of the story?
  options:
    - It is far too expensive for large models and many requests.
    - It never works.
    - It is illegal.
  answer: 0
  why: Retraining is exact but its cost grows with all the data you keep.
- q: Why does the lesson score look-alike thick-marker digits as well as Carol's own?
  options:
    - To have more test data
    - To separate memory of Carol from general skill with thick digits
    - Because Carol's digits are unreadable
  answer: 1
  why: If the model were simply good at thick digits, it would score the look-alikes as well as Carol's. The 22.5-point gap shows memory of her.
- q: Carol's 40 rows are deleted from the database and the trained model is kept. What changes in the model?
  options:
    - It forgets her at once.
    - Its accuracy on her digits drops to 55.0%.
    - Nothing, because the model only uses its trained weights.
  answer: 2
  why: A trained model never reads its training data again. Only retraining or an unlearning method changes the weights.
- q: After retraining, test accuracy for everyone else is 98.0%, the same as before. What does that tell you?
  options:
    - Removing Carol cost typical users nothing.
    - Carol is still remembered.
    - The test set contains Carol's digits.
  answer: 0
  why: The test digits are typical, so a model trained without Carol reads them just as well. Only her own digits lost their special treatment.
```

## Open question → Lesson 01

!!! levelup "Level up"
    You can now say what unlearning is, name its target and read a before-and-after result. Next quest,
    [Lesson 01, k-NN and Naive Bayes](01-knn-and-naive-bayes.md), where forgetting is exact and almost free.

When is forgetting exact and cheap, and what property of a model makes it so? We start with the two easiest models on
the ladder.

[On to Lesson 01, k-NN and Naive Bayes :material-arrow-right:](01-knn-and-naive-bayes.md){ .md-button }
