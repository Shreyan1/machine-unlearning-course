---
title: Policies around the world
description: A short synopsis of the laws, guidance and enforcement that touch machine unlearning, from the EU, France, the UK, Germany, India, the US, South Korea and Australia, with links to the sources.
---

# Policies around the world

!!! oneline "In one line"
    No law yet says "use machine unlearning", but erasure rights, regulator guidance and model-deletion orders are
    pushing in that direction, and a few documents already name unlearning as something to consider.

## Why it matters

[Why the law cares](why-the-law-cares.md) explains the problem. A trained model can keep what it learnt after the data
is deleted. This page is the map. It gives a few pointers about each policy and a link to the source, so you can see
where the rules stand without reading hundreds of pages.

!!! note "Read this first"
    These are short synopses, not legal advice, and they were checked in **October 2026**. Guidance changes often,
    and some of it is still in draft. Always read the source before relying on it.

## What they have in common

<div class="policy-themes" markdown>
<div class="policy-theme" markdown>
<span class="policy-theme__n">1</span>
**Erasure rights are everywhere, but none were written for models.** The EU, India and California all give people a
right to have their data erased. None of these laws mentions model weights.
</div>
<div class="policy-theme" markdown>
<span class="policy-theme__n">2</span>
**A model can hold personal data.** European regulators, California and a German court now treat a model that can
reproduce personal data or memorised text as something the rules may reach.
</div>
<div class="policy-theme" markdown>
<span class="policy-theme__n">3</span>
**Unlawful data can cost you the model.** In the US and South Korea, regulators have ordered companies to destroy
models built from data they should not have used.
</div>
<div class="policy-theme" markdown>
<span class="policy-theme__n">4</span>
**Unlearning is named as an option, not accepted as proof.** EU, UK and Indian documents mention unlearning as a
measure to consider or research. None says it counts as deleting the data.
</div>
</div>

## The policies

Filter the cards, or read them all. A green tick means the document names machine unlearning itself.

<div class="policies" markdown>
<div class="policy-filter" role="radiogroup" aria-label="Filter the policies">
<input type="radio" name="policy-filter" id="pf-all" checked><label for="pf-all">All</label>
<input type="radio" name="policy-filter" id="pf-names"><label for="pf-names">Names unlearning</label>
<input type="radio" name="policy-filter" id="pf-law"><label for="pf-law">Laws</label>
<input type="radio" name="policy-filter" id="pf-guidance"><label for="pf-guidance">Guidance</label>
<input type="radio" name="policy-filter" id="pf-enforcement"><label for="pf-enforcement">Orders and rulings</label>
</div>

<div class="policy-grid" markdown>

<article class="policy" data-kind="law" markdown>
<p class="policy__meta"><span class="policy__region">European Union</span><span class="policy__kind">Law</span></p>
<p class="policy__title">GDPR Article 17, the right to erasure</p>
<p class="policy__date">2016 · applies since May 2018</p>

- People can ask for their personal data to be erased "without undue delay", with exceptions.
- It does not mention models. Whether it reaches one depends on whether the model holds personal data.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://gdpr-info.eu/art-17-gdpr/">Read Article 17</a></p>
</article>

<article class="policy" data-kind="guidance" data-names="yes" markdown>
<p class="policy__meta"><span class="policy__region">European Union</span><span class="policy__kind">Guidance</span></p>
<p class="policy__title">EDPB Opinion 28/2024 on AI models</p>
<p class="policy__date">December 2024 · European Data Protection Board</p>

- A model is only anonymous if personal data cannot be extracted from it, including by asking it questions, with
  reasonable means.
- Among the measures that can help a company justify training, it lists dealing with regurgitation and memorisation
  **through unlearning techniques**.
- Data used unlawfully during development can affect whether the model may be used later.

<p class="policy__foot"><span class="policy__names is-yes">Names unlearning</span><a href="https://www.edpb.europa.eu/system/files/2024-12/edpb_opinion_202428_ai-models_en.pdf">Read the opinion (PDF)</a></p>
</article>

<article class="policy" data-kind="guidance" data-names="yes" markdown>
<p class="policy__meta"><span class="policy__region">European Union</span><span class="policy__kind">Draft guidance</span></p>
<p class="policy__title">EDPB Guidelines 03/2026 on web scraping for generative AI</p>
<p class="policy__date">July 2026 · consultation open until 30 October 2026</p>

- Covers scraping personal data to train generative AI, from collection to deployment.
- Asks for safeguards against memorisation and regurgitation, and output filtering once a model is live.
- Says **model unlearning**, or processes with the same effect, should be considered as the technology matures.

<p class="policy__foot"><span class="policy__names is-yes">Names unlearning</span><a href="https://www.edpb.europa.eu/public-consultations/guidelines-032026-on-web-scraping-in-the-context-of-generative-ai_en">Read the draft</a></p>
</article>

<article class="policy" data-kind="law" markdown>
<p class="policy__meta"><span class="policy__region">European Union</span><span class="policy__kind">Law</span></p>
<p class="policy__title">The AI Act, Regulation (EU) 2024/1689</p>
<p class="policy__date">In force August 2024 · applies in stages</p>

- Sets data-governance rules for high-risk AI and duties for general-purpose models, including a public summary of
  the training data.
- It does not add an erasure right of its own; GDPR still governs personal data.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://eur-lex.europa.eu/eli/reg/2024/1689/oj">Read the regulation</a></p>
</article>

<article class="policy" data-kind="guidance" markdown>
<p class="policy__meta"><span class="policy__region">France</span><span class="policy__kind">Guidance</span></p>
<p class="policy__title">CNIL recommendations on people's rights in AI models</p>
<p class="policy__date">February 2025 · CNIL, the French regulator</p>

- Rights such as erasure apply to models that have memorised personal data.
- Where the training data is still held, **retraining** is the main way to honour a request.
- When retraining is impossible or disproportionate, robust output filters are a fallback, but they are not the same
  as removing the data.

<p class="policy__foot"><span class="policy__names">Describes the goal, not the word</span><a href="https://www.cnil.fr/en/ensuring-and-facilitating-exercise-data-subjects-rights">Read the CNIL guidance</a></p>
</article>

<article class="policy" data-kind="guidance" data-names="yes" markdown>
<p class="policy__meta"><span class="policy__region">United Kingdom</span><span class="policy__kind">Guidance</span></p>
<p class="policy__title">ICO consultation on rights in generative AI</p>
<p class="policy__date">2024 · outcomes published December 2024</p>

- The ICO asked developers directly whether they use **machine unlearning** to honour erasure and objection.
- It concluded that unlearning came up often, but mostly in theory rather than in practice.
- Developers are still expected to have clear processes for people's rights, even when data sits inside a model.

<p class="policy__foot"><span class="policy__names is-yes">Names unlearning</span><a href="https://ico.org.uk/about-the-ico/what-we-do/our-work-on-artificial-intelligence/response-to-the-consultation-series-on-generative-ai/engineering-individual-rights-into-generative-ai-models/">Read the ICO response</a></p>
</article>

<article class="policy" data-kind="enforcement" markdown>
<p class="policy__meta"><span class="policy__region">Germany</span><span class="policy__kind">Court ruling</span></p>
<p class="policy__title">GEMA v OpenAI, Munich Regional Court</p>
<p class="policy__date">November 2025 · under appeal</p>

- Song lyrics memorised **in a model's weights** count as a copy under German copyright law.
- This is the case where deleting the files does nothing, because the data is in the model.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://cms.law/en/deu/legal-updates/gema-vs.-openai-munich-regional-court-i-issues-landmark-copyright-decision">Read a summary</a></p>
</article>

<article class="policy" data-kind="law" markdown>
<p class="policy__meta"><span class="policy__region">India</span><span class="policy__kind">Law</span></p>
<p class="policy__title">Digital Personal Data Protection Act 2023, section 12</p>
<p class="policy__date">2023 · Rules notified November 2025</p>

- People can ask for data they consented to be corrected, updated or erased, unless the law requires it to be kept.
- The DPDP Rules 2025 phase the obligations in over 18 months; the erasure duties apply from May 2027.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://www.indiacode.nic.in/bitstream/123456789/22037/2/a2023-22.pdf">Read the Act (PDF)</a></p>
</article>

<article class="policy" data-kind="guidance" data-names="yes" markdown>
<p class="policy__meta"><span class="policy__region">India</span><span class="policy__kind">Guidance</span></p>
<p class="policy__title">India AI Governance Guidelines</p>
<p class="policy__date">November 2025 · MeitY, under the IndiaAI Mission</p>

- Lists **machine unlearning**, with privacy-enhancing technology, algorithmic auditing and bias detection, among the
  techno-legal tools the government should explore.
- Says the IndiaAI Mission's work on machine unlearning should continue. Its 2024 project list includes an IIT
  Jodhpur project on unlearning for generative foundation models.
- Guidance to explore, not a duty to use unlearning.

<p class="policy__foot"><span class="policy__names is-yes">Names unlearning</span><a href="https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc2025115685601.pdf">Read the guidelines (PDF)</a></p>
</article>

<article class="policy" data-kind="enforcement" markdown>
<p class="policy__meta"><span class="policy__region">United States</span><span class="policy__kind">Orders</span></p>
<p class="policy__title">FTC model-deletion orders</p>
<p class="policy__date">2021 to 2023 · Federal Trade Commission</p>

- Everalbum, WW/Kurbo, Ring and Rite Aid were ordered to delete the **models and algorithms** built from data they
  collected unlawfully. This is often called algorithmic disgorgement.
- The orders remove the model; they do not ask for it to be unlearnt.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://www.ftc.gov/news-events/news/press-releases/2021/05/ftc-finalizes-settlement-photo-app-developer-related-misuse-facial-recognition-technology">Read the Everalbum order</a></p>
</article>

<article class="policy" data-kind="law" markdown>
<p class="policy__meta"><span class="policy__region">United States · California</span><span class="policy__kind">Law</span></p>
<p class="policy__title">AB 1008, personal information in AI systems</p>
<p class="policy__date">Signed September 2024 · in force January 2025</p>

- It amends the CCPA so that personal information can exist in "abstract digital formats", including AI systems that
  can output personal information.
- So deletion and correction rights may reach a model, not just a database.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1008">Read the bill</a></p>
</article>

<article class="policy" data-kind="enforcement" markdown>
<p class="policy__meta"><span class="policy__region">South Korea</span><span class="policy__kind">Order</span></p>
<p class="policy__title">PIPC decision on Kakao Pay, Apple and Alipay</p>
<p class="policy__date">January 2025 · Personal Information Protection Commission</p>

- Kakao Pay sent data on about 40 million users to Alipay without proper consent, and Alipay built a credit-scoring
  model from it.
- Fines for Kakao Pay and Apple, and an order for Alipay to **destroy the model**.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://iapp.org/news/a/south-korea-s-pipc-flexes-its-muscles-what-to-know-about-ai-model-deletion-cross-border-transfers-and-more">Read a summary</a></p>
</article>

<article class="policy" data-kind="guidance" markdown>
<p class="policy__meta"><span class="policy__region">Australia</span><span class="policy__kind">Guidance</span></p>
<p class="policy__title">OAIC guidance on training generative AI</p>
<p class="policy__date">October 2024 · Office of the Australian Information Commissioner</p>

- The Privacy Act applies to personal information used for training, including data that is publicly available.
- Developers should minimise or de-identify data before training, and deployers can agree output filters with them.

<p class="policy__foot"><span class="policy__names">Does not name unlearning</span><a href="https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/guidance-on-privacy-and-developing-and-training-generative-ai-models">Read the OAIC guidance</a></p>
</article>

</div>
</div>

## What this means for an engineer

- **Design for deletion before training.** Every document above is easier to satisfy if you can retrain cheaply or
  remove a shard, which is what [SISA](sisa.md) is for.
- **Keep evidence, not claims.** Regulators ask what the model can still reveal. [The unlearning audit](unlearning-audit.md)
  shows how to measure it against a gold band.
- **Know your fallback.** Several regulators accept filters only when retraining is disproportionate, and they do not
  count as deletion. Write down why you chose each option; [the enterprise playbook](enterprise-playbook.md) shows how.

## Common mistakes

!!! danger "Mistakes people make"
    - **Reading "names unlearning" as "requires unlearning".** Every document above treats it as an option to consider
      or research.
    - **Treating guidance as law.** EDPB opinions, CNIL and ICO guidance and the Indian guidelines are not statutes,
      though regulators use them to judge cases.
    - **Assuming one country's rule travels.** A model served worldwide can face all of these at once.

## Key takeaways

- Erasure rights exist in the EU, India and California, but none were written with model weights in mind.
- Regulators increasingly treat models that can reveal personal data as within the rules.
- The EDPB, the ICO and India's AI guidelines name machine unlearning, as a measure to consider, not as proof.
- Model-deletion orders in the US and South Korea show what happens when the data was unlawful from the start.

## Quiz

```quiz
- q: Which of these documents names machine unlearning as a measure to consider?
  options:
    - EDPB Opinion 28/2024
    - GDPR Article 17
    - California AB 1008
  answer: 0
  why: The EDPB lists unlearning techniques among measures against memorisation. GDPR Art. 17 and AB 1008 create or extend rights but do not name a technique.
- q: According to the CNIL, what is the main way to honour an erasure request when you still hold the training data?
  options:
    - Add an output filter
    - Retrain the model
    - Ignore it, because models are anonymous
  answer: 1
  why: Retraining comes first. Filters are a fallback when retraining is impossible or disproportionate, and they are not deletion.
- q: What did South Korea's privacy regulator order Alipay to do in January 2025?
  options:
    - Unlearn the affected users with gradient ascent
    - Destroy the credit-scoring model built from the data
    - Publish its training data
  answer: 1
  why: Like the US FTC orders, the remedy was to destroy the model built from data obtained without proper consent.
- q: What did the UK ICO conclude about machine unlearning after its 2024 consultation?
  options:
    - It is proven and required
    - It came up often, but mostly in theory rather than in practice
    - It is banned
  answer: 1
  why: Respondents raised unlearning often, but mainly its theoretical promise. The ICO still expects clear processes for people's rights.
```

## Try it

- Pick one product you know. Which of these policies would apply to it, and what would you have to prove?
- Read the next concept, [The notation](notation.md), or go back to [Why the law cares](why-the-law-cares.md).
