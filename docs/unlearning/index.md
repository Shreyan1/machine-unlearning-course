---
title: Unlearning concepts
description: One idea per page, from "deleting is not forgetting" to unlearning at scale.
---

# Unlearning concepts

This part of the site explains machine unlearning one idea at a time. Each page stands on its own, but they are in a
sensible reading order. Unlearning helps make **Responsible AI** real by connecting data rights to model behavior and
evidence. If you are new to machine learning itself, start with [ML Basics](../ml-basics/index.md).

<div class="pstrip" data-section="Unlearning Concepts" markdown></div>

## Foundations

What unlearning is, why deleting is not enough, and what the law around the world says.

<div class="cards" markdown>
<a class="card" href="what-is-machine-unlearning/"><span class="card__num">01</span><span class="card__title">What is machine unlearning?</span><span class="card__text">Removing data's influence from a trained model, and proving it.</span></a>
<a class="card" href="deleting-vs-unlearning/"><span class="card__num">02</span><span class="card__title">Deleting is not forgetting</span><span class="card__text">Why removing the rows does not change the model.</span></a>
<a class="card" href="why-the-law-cares/"><span class="card__num">03</span><span class="card__title">Why the law cares</span><span class="card__text">The right to erasure, model-deletion orders and real cases.</span></a>
<a class="card" href="global-policy/"><span class="card__num">04</span><span class="card__title">Policies around the world</span><span class="card__text">What the EU, France, the UK, India, the US and others say, in a few pointers each.</span></a>
<a class="card" href="notation/"><span class="card__num">05</span><span class="card__title">The notation</span><span class="card__text"><span class="arithmatex">\(D, D_f, D_r, \theta_o, \theta_r, \theta_u\)</span>, in plain words.</span></a>
<a class="card" href="ladder-of-forgetting/"><span class="card__num">06</span><span class="card__title">The Ladder of Forgetting</span><span class="card__text">The map of the course, from easy to unsolved.</span></a>
</div>

## Exact unlearning

Methods whose result is guaranteed to match a model that never saw the data.

<div class="cards" markdown>
<a class="card" href="retraining-gold-standard/"><span class="card__num">07</span><span class="card__title">Retraining, the gold standard</span><span class="card__text">The one answer that is always right, and always expensive.</span></a>
<a class="card" href="gold-band/"><span class="card__num">08</span><span class="card__title">The gold band</span><span class="card__text">Why "forgotten" is a range, not a number.</span></a>
<a class="card" href="exact-unlearning-classical/"><span class="card__num">09</span><span class="card__title">Exact unlearning for classical models</span><span class="card__text">Subtract, downdate or rebuild only what was touched.</span></a>
<a class="card" href="sisa/"><span class="card__num">10</span><span class="card__title">SISA</span><span class="card__text">Split the training so that forgetting touches one small piece.</span></a>
<a class="card" href="certified-unlearning/"><span class="card__num">11</span><span class="card__title">Certified unlearning</span><span class="card__text">A provable middle ground between retraining and hoping.</span></a>
</div>

## Approximate unlearning

Cheaper methods with no guarantee, which must be checked.

<div class="cards" markdown>
<a class="card" href="approximate-unlearning/"><span class="card__num">12</span><span class="card__title">Quick fixes and their traps</span><span class="card__text">Fine-tuning, gradient ascent and NegGrad+, and how they fail.</span></a>
<a class="card" href="scrub/"><span class="card__num">13</span><span class="card__title">SCRUB</span><span class="card__text">A student copies the teacher on what to keep, and moves away on what to forget.</span></a>
<a class="card" href="bad-teacher/"><span class="card__num">14</span><span class="card__title">Bad Teacher</span><span class="card__text">Learn from a "know-nothing" teacher on the forget set.</span></a>
<a class="card" href="method-zoo/"><span class="card__num">15</span><span class="card__title">The method zoo</span><span class="card__text">Fourteen methods, one fair exam.</span></a>
</div>

## Checking the result

How to gather evidence that a model really forgot.

<div class="cards" markdown>
<a class="card" href="membership-inference-attacks/"><span class="card__num">16</span><span class="card__title">Membership inference attacks</span><span class="card__text">Can an outsider tell that your data was used?</span></a>
<a class="card" href="unlearning-audit/"><span class="card__num">17</span><span class="card__title">The unlearning audit</span><span class="card__text">Five checks, fixed in advance, against a gold band.</span></a>
<a class="card" href="testing-vs-proving/"><span class="card__num">18</span><span class="card__title">Can a test prove forgetting?</span><span class="card__text">Tests can show remembering, not prove forgetting.</span></a>
<a class="card" href="relearning-and-quantization/"><span class="card__num">19</span><span class="card__title">When forgotten knowledge comes back</span><span class="card__text">Relearning, compression and clever prompts.</span></a>
<a class="card" href="influence-functions/"><span class="card__num">20</span><span class="card__title">Influence functions</span><span class="card__text">How much did one example shape the model?</span></a>
</div>

## Responsible AI in the real world

Unlearning meets fairness, consent, security, language models, recommenders and big systems.

<div class="cards" markdown>
<a class="card" href="fairness-and-erasure/"><span class="card__num">21</span><span class="card__title">Erasure requests and fairness</span><span class="card__text">When forgetting some people hurts a group.</span></a>
<a class="card" href="consent-and-face-recognition/"><span class="card__num">22</span><span class="card__title">Consent and face recognition</span><span class="card__text">Withdrawing consent for your face.</span></a>
<a class="card" href="poisoning-and-backdoors/"><span class="card__num">23</span><span class="card__title">Poisoned data and backdoors</span><span class="card__text">Removing data an attacker slipped in.</span></a>
<a class="card" href="unlearning-fine-tunes/"><span class="card__num">24</span><span class="card__title">Unlearning a fine-tune</span><span class="card__text">When a customer leaves.</span></a>
<a class="card" href="llm-unlearning/"><span class="card__num">25</span><span class="card__title">Unlearning in language models</span><span class="card__text">Facts, not rows. Refusal is not forgetting.</span></a>
<a class="card" href="recommender-unlearning/"><span class="card__num">26</span><span class="card__title">Unlearning in recommenders</span><span class="card__text">When your taste is on every page.</span></a>
<a class="card" href="unlearning-at-scale/"><span class="card__num">27</span><span class="card__title">Unlearning at scale</span><span class="card__text">A year of requests, and the cost that grows with the square.</span></a>
<a class="card" href="enterprise-playbook/"><span class="card__num">28</span><span class="card__title">The enterprise playbook</span><span class="card__text">From request to certificate, before the deadline.</span></a>
<a class="card" href="rag-and-vector-stores/"><span class="card__num">29</span><span class="card__title">RAG, vector stores and caches</span><span class="card__text">Deletion is easy, if you find every copy.</span></a>
<a class="card" href="federated-unlearning/"><span class="card__num">30</span><span class="card__title">Federated unlearning</span><span class="card__text">Forgetting a participant whose data you never saw.</span></a>
<a class="card" href="editing-vs-unlearning/"><span class="card__num">31</span><span class="card__title">Model editing vs unlearning</span><span class="card__text">Changing an answer is not removing the knowledge.</span></a>
</div>

## The frontier

What is solved, what works with an audit and what is still open.

<div class="cards" markdown>
<a class="card" href="state-of-the-field/"><span class="card__num">32</span><span class="card__title">State of the field</span><span class="card__text">Benchmarks, open problems and where each method stands.</span></a>
</div>
