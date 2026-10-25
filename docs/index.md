---
title: Machine Unlearning, explained simply
description: Learn how to make a trained AI model forget someone's data, and how to check that it really did. Simple explainers, quizzes and runnable notebooks.
hide:
  - toc
---

<div class="hero" markdown>
<span class="hero__kicker">A free course · explainers · quizzes · notebooks</span>

# Teach a trained model to forget, and prove that it did.

<p class="hero__lead">When a person asks a company to delete their data, deleting the file is easy. The hard part is the
AI model that has already learnt from it. This site explains, in plain words, how <b>machine unlearning</b> works, why
it matters, and how to check whether a model has really forgotten.</p>

<div class="buttons" markdown>
[:material-rocket-launch-outline: Start here](start-here/index.md){ .md-button .md-button--primary }
[:material-lightbulb-on-outline: What is machine unlearning?](unlearning/what-is-machine-unlearning.md){ .md-button }
[:material-format-list-bulleted: See all topics](#all-topics){ .md-button }
[:simple-googlecolab: Run it in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb){ .md-button }
</div>
</div>

## Meet Carol

A model is trained to read handwritten digits. It learns from 1,257 examples. Forty of them were written by **Carol**,
who used a thick marker that nobody else used.

The model gets **100%** of Carol's digits right, but only **77.5%** of thick-marker digits it has never seen. So it has
not just learnt "thick digits". It has memorised *hers*.

Carol asks to be forgotten. The company deletes her rows from the database. **Nothing changes**, because the model's
weights were already trained on her. This whole site is about what to do next.

!!! carol "Carol says"
    "Deleting my file is not enough. I want the model to behave as if it had never met me."

## How this site works

<div class="cards" markdown>
<a class="card" href="ml-basics/">
<span class="card__num">Part 1</span>
<span class="card__title" markdown="span">:material-school-outline: ML Basics</span>
<span class="card__text">The machine learning you need first, such as training, loss, gradient descent and overfitting, and the models the course uses.</span>
</a>
<a class="card" href="unlearning/">
<span class="card__num">Part 2</span>
<span class="card__title" markdown="span">:material-eraser: Unlearning concepts</span>
<span class="card__text">One idea per page, from deleting vs forgetting and the gold band to SISA, SCRUB, attacks, audits and the law.</span>
</a>
<a class="card" href="lessons/">
<span class="card__num">Part 3</span>
<span class="card__title" markdown="span">:material-notebook-outline: Lessons</span>
<span class="card__text">A summary of each of the 22 notebooks, with the key results and a button to run it in Colab.</span>
</a>
<a class="card" href="quizzes/">
<span class="card__num">Check yourself</span>
<span class="card__title" markdown="span">:material-check-decagram-outline: Quizzes</span>
<span class="card__text">Every page ends with a short quiz. Your scores are saved in your browser, and there is a final test.</span>
</a>
</div>

## All topics

Every page on the site, in reading order. Start at the top left, or jump to any topic you need.

<!-- all-topics -->

## How each page is laid out

Every page follows the same pattern, a bit like a good textbook:

1. **In one line**: the idea in a single sentence.
2. **A simple example**: an everyday picture first, then the course example.
3. **How it works**: the steps, with a diagram.
4. **Common mistakes and key takeaways.**
5. **A quiz**, so you know you understood it.

## The five steps in every lesson

Each lesson runs the same five steps, so you always know where you are.

<ol class="steps" markdown>
<li markdown>**Train** a model on data that includes something it should not keep.</li>
<li markdown>**Show the issue**: measure how the model still carries that data.</li>
<li markdown>**Untrain** it with an unlearning method.</li>
<li markdown>**Show the result**: measure again, side by side with *before*.</li>
<li markdown>**Prove it**: compare with models that *never* saw the data. This is the only honest test.</li>
</ol>

The target is not 0% on Carol. A model that never met her can still read many of her digits. The target is the
**[gold band](unlearning/gold-band.md)**: the range of results you get from several models retrained without her.

## The Ladder of Forgetting

The lessons climb one rung at a time, from models where forgetting is a simple subtraction to large language models
where nobody can yet do it reliably.

<figure class="figure" markdown>
![The Ladder of Forgetting: from k-NN and Naive Bayes at the bottom to unlearning at scale at the top](assets/diagrams/00_ladder_of_forgetting.png)
</figure>

## Who is this for?

| You are... | Start with |
|---|---|
| New to machine learning | [ML Basics](ml-basics/index.md), then [What is machine unlearning?](unlearning/what-is-machine-unlearning.md) |
| New to unlearning, but you know ML | [Deleting is not forgetting](unlearning/deleting-vs-unlearning.md) |
| A privacy, legal or policy person | [Why the law cares](unlearning/why-the-law-cares.md) and [The unlearning audit](unlearning/unlearning-audit.md) |
| An engineer who must build deletion | [SISA](unlearning/sisa.md) and [The enterprise playbook](unlearning/enterprise-playbook.md) |

See [Pick your path](start-here/learning-paths.md) for full routes with time estimates.

!!! warning "Unlearning is not a legal safe harbour"
    No regulator has yet said that any unlearning method counts as deleting the data. This course teaches you to
    *measure* what a method does, so that you can make that argument honestly.
