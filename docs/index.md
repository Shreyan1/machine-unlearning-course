---
title: Machine Unlearning, explained simply
description: Learn how to make a trained AI model forget someone's data, and how to check that it really did. Simple explainers, quizzes and runnable notebooks.
hide:
  - toc
---

<div class="hero" markdown>
<div class="hero__text" markdown>
<span class="hero__kicker">Open access · explainers · quizzes · notebooks</span>

# Teach a trained model to forget, and prove that it did.

<p class="hero__lead">When a person asks a company to delete their data, deleting the file is easy. The hard part is the
AI model that has already learnt from it. This site explains, in plain words, how <b>machine unlearning</b> works, why
it matters, and how to check whether a model has really forgotten. These skills are part of engineering
<b>Responsible AI</b>, because responsible systems must account for what their models learn from people.</p>
</div>

<div class="hero__visual">
<div class="hero__stage"><canvas id="hero-canvas" class="hero__canvas" role="img" aria-label="A turning sphere of blue dots, the training data. A small yellow cluster of examples separates from it while the sphere keeps its shape."></canvas></div>
<p class="hero__legend"><span><span class="dot dot--blue"></span>Training data</span> <span><span class="dot dot--yellow"></span>Examples, being forgotten</span></p>
</div>

<div class="buttons hero__buttons" markdown>
[:material-rocket-launch-outline: Start here](start-here/index.md){ .md-button .md-button--primary }
[:material-lightbulb-on-outline: What is machine unlearning?](unlearning/what-is-machine-unlearning.md){ .md-button }
[:material-format-list-bulleted: See all topics](#all-topics){ .md-button }
[:custom-colab: Run it in Colab](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb){ .md-button }
</div>
</div>

<div class="pwelcome" markdown></div>

## When a data request reaches a trained model

<p class="home-story__lead">A real product can keep carrying information after its source record is deleted. Here is the decision a team then faces.</p>

<div class="story-flow" role="list" aria-label="Four steps in responding to a model erasure request">
<article class="story-step" role="listitem">
<p class="story-step__number">Request</p>
<h3>A person asks for erasure</h3>
<p>In a worked example, France's data protection authority describes a person finding that an insurer's model reveals details about their financial settlement when certain questions are asked.</p>
</article>
<article class="story-step" role="listitem">
<p class="story-step__number">Investigate</p>
<h3>Deleting the record leaves a model question</h3>
<p>Removing the database row does not settle whether the trained model can still reveal information about the claim. <a href="unlearning/deleting-vs-unlearning/">Deleting a record is not the same as unlearning it.</a></p>
</article>
<article class="story-step" role="listitem">
<p class="story-step__number">Respond</p>
<h3>Choose a proportionate fix</h3>
<p><a href="unlearning/retraining-gold-standard/">Retraining</a> may address information at the model's core, but it can be costly. <a href="unlearning/what-is-machine-unlearning/">Unlearning</a> asks whether a targeted update can work for less.</p>
</article>
<article class="story-step" role="listitem">
<p class="story-step__number">Verify</p>
<h3>Gather evidence before claiming success</h3>
<p>Compare the result with models retrained without the data, then audit the change. If the checks fail, retrain or choose another response. Start with <a href="unlearning/gold-band/">the gold band</a> and <a href="unlearning/unlearning-audit/">the unlearning audit</a>.</p>
</article>
</div>

<p class="home-story__source">This insurer scenario is a worked example, not a report about a named company. <a href="https://www.cnil.fr/en/ensuring-and-facilitating-exercise-data-subjects-rights">Read the CNIL guidance</a>.</p>

<div class="story-context">
<article class="story-callout story-callout--team">
<p class="story-callout__label">The small-team question</p>
<h3>Can responsible practice fit a startup budget?</h3>
<p>Enterprise customers may ask for security reviews or independent assurance, such as a <a href="https://www.aicpa.com/cpe-learning/publication/soc-2-reporting-on-an-examination-of-controls-at-a-service-organization-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy">SOC 2 report</a>. Post-launch retraining can also be expensive. Teams need ways to manage risk and show evidence without making Responsible AI practical only for large companies.</p>
<p><a href="lessons/17-enterprise-playbook/">See how the course turns this into an engineering workflow.</a></p>
</article>
<article class="story-callout story-callout--india">
<p class="story-callout__label">An India policy signal</p>
<h3>Machine unlearning is on the governance map</h3>
<p>India's 2025 AI Governance Guidelines name machine unlearning among the technical approaches industry should explore, alongside privacy-enhancing technology, algorithmic auditing and bias detection. This is guidance to explore options, not a mandate to use unlearning in every system.</p>
<p>MeitY's 2024 IndiaAI project list includes an IIT Jodhpur project on machine unlearning for generative foundation models.</p>
<p class="story-callout__link"><a href="https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc2025115685601.pdf">Read the India AI Governance Guidelines</a> · <a href="https://www.pib.gov.in/PressReleasePage.aspx?PRID=2065579&amp;lang=2&amp;reg=3">See the 2024 IndiaAI project list</a> · <a href="unlearning/global-policy/">See policies around the world</a></p>
</article>
</div>

<p class="home-story__takeaway"><strong>That is what this course teaches.</strong> How to make a trained model forget, measure what changed and decide honestly whether the evidence is good enough.</p>

## How this site works

<ol class="course-route" aria-label="Course route">
<li class="course-stop"><a href="ml-basics/">
<span class="course-stop__number">01</span><span class="course-stop__title">Build the foundation</span>
<span class="course-stop__text">Training, loss, overfitting and the models used throughout the course.</span>
</a></li>
<li class="course-stop"><a href="unlearning/">
<span class="course-stop__number">02</span><span class="course-stop__title">Understand unlearning</span>
<span class="course-stop__text">Methods, limits, attacks, audits and the legal context.</span>
</a></li>
<li class="course-stop"><a href="lessons/">
<span class="course-stop__number">03</span><span class="course-stop__title">Work through the lessons</span>
<span class="course-stop__text">Follow the notebooks and compare the results.</span>
</a></li>
<li class="course-stop"><a href="quizzes/">
<span class="course-stop__number">04</span><span class="course-stop__title">Check your understanding</span>
<span class="course-stop__text">Short quizzes throughout, with a final test at the end.</span>
</a></li>
</ol>

## All topics

Every page on the site, in reading order. Start at the top left, or jump to any topic you need.

<!-- all-topics -->

## How each page is laid out

Every page follows the same pattern, a bit like a good textbook.

1. **In one line.** The idea in a single sentence.
2. **A simple example.** An everyday picture first, then the course example.
3. **How it works.** The steps, with a diagram.
4. **Common mistakes and key takeaways.**
5. **A quiz**, so you know you understood it.

## The five steps in every lesson

Each lesson runs the same five steps, so you always know where you are.

<ol class="steps" markdown>
<li markdown>**Train** a model on data that includes something it should not keep.</li>
<li markdown>**Show the issue.** Measure how the model still carries that data.</li>
<li markdown>**Untrain** it with an unlearning method.</li>
<li markdown>**Show the result.** Measure again, side by side with *before*.</li>
<li markdown>**Prove it.** Compare with models that *never* saw the data. This is the only honest test.</li>
</ol>

The target is not 0% on the requested data. A model retrained without it may still handle similar examples well. The
target is the **[gold band](unlearning/gold-band.md)**, which is the range of results you get from several models retrained
without the requested data.

## The Ladder of Forgetting

The lessons climb one rung at a time, from models where forgetting is a simple subtraction to large language models
where nobody can yet do it reliably.

<!-- diagram: ladder-of-forgetting -->

**Your climb so far.** Pass the quizzes on each rung's pages to climb it. [See all your progress](quizzes/progress.md).

<div class="ladder-climb" markdown></div>

## Who is this for?

| You are... | Start with |
|---|---|
| New to machine learning | [ML Basics](ml-basics/index.md), then [What is machine unlearning?](unlearning/what-is-machine-unlearning.md) |
| New to unlearning, but you know ML | [Deleting is not forgetting](unlearning/deleting-vs-unlearning.md) |
| A privacy, legal or policy person | [Why the law cares](unlearning/why-the-law-cares.md) and [The unlearning audit](unlearning/unlearning-audit.md) |
| An engineer who must build deletion | [SISA](unlearning/sisa.md) and [The enterprise playbook](unlearning/enterprise-playbook.md) |

See [Pick your path](start-here/learning-paths.md) for full routes with time estimates.

!!! note "When an erasure request reaches a model"
    The right response depends on the request, what the model retains or can reveal, and the law that applies.
    Regulators are still working through how data-protection rights apply to trained models. Unlearning is one
    possible response, not an automatic legal answer or a guaranteed cost saving. If your team is considering it,
    this course shows how to compare it with retraining and other measures, test the result and document the evidence.
    See the [CNIL's guidance on rights in AI models](https://www.cnil.fr/en/ensuring-and-facilitating-exercise-data-subjects-rights)
    and the [ICO's guidance on individual rights in AI systems](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/).
