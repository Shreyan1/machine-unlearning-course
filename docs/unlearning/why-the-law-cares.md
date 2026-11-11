---
title: Why the law cares
description: The right to erasure, model-deletion orders and real cases where bad data inside a model cost millions.
---

# Why the law cares

!!! oneline "In one line"
    Laws give people the right to have their data erased, and regulators have already ordered companies to delete the
    **models** built from data they should not have used.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - name the main erasure rights and the cases where regulators ordered a model deleted,
    - explain why a model, and not just a database, can fall within the rules,
    - say what unlearning can and cannot show when a team answers a request.

## Why it matters

Deleting data from a database is a routine task. But if a model was trained on that data, regulators increasingly ask a
second question, which is what happens to the model. When the answer is "retrain it", the cost can be enormous.
Stanford's AI Index 2024 estimates the compute alone at about **$78 million for GPT-4** and **$191 million for Gemini
Ultra**. Unlearning is the hope of a cheaper fix, but only if you can show evidence that it worked.

Three pressures meet here, and this page takes them one at a time.

- **People have a right to erasure.** The EU, India and California all give people a right to have their data erased.
  None of these laws was written with model weights in mind.
- **A model can hold personal data.** European regulators, California and a German court now treat a model that can
  reproduce personal data or memorised text as something the rules may reach.
- **Unlawful data can cost you the model.** In the US and South Korea, regulators have ordered companies to destroy
  models built from data they should not have used.

For an engineer, the practical result is simple to state. Someone may one day ask what your model still knows about a
person, and "we deleted the rows" may not be a full answer.

## A simple example

A shop collects customers' photos without asking and builds a face-recognition system from them. A regulator finds
out. Fining the shop and making it delete the photos is not enough, because the system still works from what it learnt.
So the regulator also orders the shop to delete the **system**.

This is not imaginary. It has happened several times, as the table below shows.

!!! simply "Explain it simply"
    If someone builds a house from stolen bricks, handing back the empty brick packets does not undo the theft. The
    bricks are in the walls. Regulators have started to treat models the same way. The data is "in the walls" of the
    model, so returning or deleting the data alone may not be the end of it.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Right to erasure](../start-here/glossary.md#r) | A person's legal right to ask for their personal data to be erased, with exceptions | GDPR Article 17 in the EU |
| Personal data | Information about a particular person who can be identified | Carol's 40 handwritten digits |
| [Algorithmic disgorgement](../start-here/glossary.md#a) | An order to delete the models and algorithms built from unlawfully collected data | The FTC's order against Everalbum in 2021 |
| Anonymous model | In EDPB Opinion 28/2024, a model from which personal data cannot be extracted with reasonable means | A model that no query can make reveal Carol |
| Regulator | A public body that enforces a law and can issue orders | The US FTC, South Korea's PIPC, France's CNIL |
| Guidance | A regulator's view of how a law applies. Not a statute, but used to judge cases | The CNIL's recommendations on rights in AI models |
| Derived model | A model made from another one, such as a fine-tune or a distilled copy | A customer's fine-tune of a base model trained on Carol |

## How it works

<!-- diagram: why-the-law-cares -->

Read the figure as a chain of five boxes. A person asks to be forgotten, and the company deletes the records. The third
box is the problem, because the model already learnt from those records. The fix is to unlearn or retrain the model,
and the last box is the evidence, an audit that shows the fix worked. Under the chain sit four of the cases where
regulators did not wait for a fix and ordered the whole model deleted.

### Situations that call for unlearning

| Situation | Example | What has to be forgotten |
|---|---|---|
| **Right to be forgotten** | GDPR Art. 17 (EU), India's DPDP Act 2023 s.12, California CCPA §1798.105 | One person's records |
| **Unlawfully collected data** | US FTC orders against Everalbum (2021), WW/Kurbo (2022) and Rite Aid (2023) | A whole data source, and the models built from it |
| **Is a model personal data?** | EDPB Opinion 28/2024 says a model is only "anonymous" if extracting personal data from it, including through queries, is negligible | Anything the model could leak |
| **Consent withdrawn** | A person withdraws consent for their face, voice or health record | One identity |
| **Poisoned data** | An attacker slipped mislabelled or back-doored samples into training | The malicious samples |
| **Copyright or licensing** | A data licence expires, or a rights-holder objects | One source |
| **Harmful knowledge in LLMs** | Memorised secrets, private phone numbers, hazardous instructions | Facts, not rows |

The rows differ in size. A right-to-erasure request is usually one person. An unlawful source or an expired licence can
be thousands of people at once. A fact in a language model is not even a row you can point to. The course has a
lesson for each kind, from [fairness and erasure](fairness-and-erasure.md) to [consent in face
recognition](consent-and-face-recognition.md), [poisoned data](poisoning-and-backdoors.md) and
[language models](llm-unlearning.md).

??? deep "Go deeper · what the three erasure rights say"
    **GDPR Article 17 (EU).** People can ask for their personal data to be erased "without undue delay", with
    exceptions. It does not mention models. Whether it reaches one depends on whether the model holds personal data.

    **India's DPDP Act 2023, section 12.** People can ask for data they consented to be corrected, updated or erased,
    unless the law requires it to be kept. The DPDP Rules 2025 phase the obligations in over 18 months, and the erasure
    duties apply from May 2027.

    **California CCPA §1798.105.** It gives people a right to have their personal data erased. California's AB 1008, in force since January 2025,
    amends the CCPA so that personal information can exist in "abstract digital formats", including AI systems that
    can output personal information. So deletion rights may reach a model, not just a database.

    These are short synopses, not legal advice. [Policies around the world](global-policy.md) links each source.

### Regulators have ordered model deletion

| Year | Case | Outcome |
|---|---|---|
| 2021 | **Everalbum** used customers' photos to build face recognition without proper consent. | US FTC ordered it to delete the face-recognition **models and algorithms** built from those photos. |
| 2022 | **WW (Weight Watchers) / Kurbo** collected children's data without parental consent. | $1.5 million penalty, and destroy any **models or algorithms** made from the data. |
| 2023 | **Ring** used customers' videos to train algorithms without consent. | $5.8 million, and delete the **models and algorithms** built from those videos. |
| 2023 | **Rite Aid**'s face recognition wrongly flagged thousands of shoppers as shoplifters. | Five-year ban on face recognition; delete the photos and any **algorithms** built from them. |
| 2025 | **Kakao Pay** sent data on about 40 million users to **Alipay** without consent, and Alipay built a credit-scoring model from it. | South Korea's privacy regulator ordered Alipay to **delete the model**. |

Look at what the five cases share. In each one, the data should not have been used in the first place, and the remedy
reached past the data to the model. This is often called **algorithmic disgorgement**. Notice also what the orders did
*not* do. They removed the model. They did not ask for it to be unlearnt. Unlearning matters here as the cheaper
alternative a company might prefer, but only if it can show the result with evidence.

<div class="stats">
<div class="is-bad"><strong>5</strong><span>model-deletion orders in the table, from 2021 to 2025</span></div>
<div><strong>$191M</strong><span>estimated compute to train Gemini Ultra</span></div>
<div><strong>$78M</strong><span>estimated compute to train GPT-4</span></div>
<div class="is-good"><strong>0.27 s</strong><span>to retrain the course's digit network</span></div>
</div>

The last tile is the reason the course works with a small model. Retraining it is nearly free, so every lesson can
compute the ideal answer and measure how close a cheaper method gets.

??? checkpoint "Checkpoint 1 · A company trained a face model on photos it collected without consent, then deleted the photos. In the FTC cases above, was deleting the photos the end of it?"
    **No.** In Everalbum, WW/Kurbo, Ring and Rite Aid the orders also covered the **models and algorithms** built from
    the data. The model still works from what it learnt, so the remedy reached it too. Whether a given case ends the same
    way depends on its facts and the law that applies.

### When the model itself holds the data

In November 2025, a Munich court ruled that song lyrics memorised **in a model's weights** count as a copy under German
copyright law (the ruling is under appeal). This is exactly the case where deleting the files does nothing, because the data is in the model.

The same idea appears in data protection. EDPB Opinion 28/2024 says a model is only anonymous if personal data cannot
be extracted from it, including by asking it questions, with reasonable means. The CNIL says rights such as erasure
apply to models that have memorised personal data. In the course, this is exactly what a fingerprint measures. The
original digit model got 100.0% of Carol's digits right but only 77.5% of look-alike digits, so its behaviour gives
away that she was in training.

### When retraining was too expensive

The GPT-3 paper (2020) admits that a bug left some test data in the training set, and that "due to the cost of training
it was not feasible to retrain the model". The flaw shipped and was measured instead.

That one sentence shows the whole dilemma. A team that finds bad data in a trained model has three choices. It can
retrain, which is exact and may be very costly. It can try a cheaper fix, such as unlearning, which then needs evidence.
Or it can leave the model as it is and describe the flaw, which is what happened with GPT-3.

??? deep "Go deeper · what the guidance says about unlearning itself"
    No law yet says "use machine unlearning". A few documents mention it, always as something to consider, never as
    proof that data was deleted.

    | Document | What it says about the fix |
    |---|---|
    | EDPB Opinion 28/2024 | Lists dealing with regurgitation and memorisation through unlearning techniques among the measures that can help a company justify training |
    | EDPB draft Guidelines 03/2026 | Says model unlearning, or processes with the same effect, should be considered as the technology matures |
    | CNIL recommendations, February 2025 | Where the training data is still held, retraining is the main way to honour a request. Output filters are a fallback, and not the same as removing the data |
    | ICO consultation outcome, December 2024 | Unlearning came up often, but mostly in theory rather than in practice |
    | India AI Governance Guidelines, November 2025 | Lists machine unlearning among the techno-legal tools the government should explore |

    [Policies around the world](global-policy.md) has each document, its date and a link.

??? checkpoint "Checkpoint 2 · A team still holds its training data. To answer a request, it adds an output filter so the model never prints the customer's name. What does the CNIL's guidance say about that?"
    **It is a fallback, not removal.** The CNIL says that where the training data is still held, retraining is the
    main way to honour a request. Robust output filters are for when retraining is impossible or disproportionate, and
    they are not the same as removing the data. The model still knows what the filter hides.

!!! note "The legal test is case-specific"
    Data-protection rules do not prescribe machine unlearning as a universal fix. Whether a team must change a model
    depends on the request, whether the model contains or can reveal personal data, any applicable exceptions and the
    law that applies. Regulators are still working through these questions. Unlearning is one response to assess
    alongside retraining and other measures; a technical test alone does not establish legal compliance. This course
    teaches you to compare approaches, measure what changed and document the evidence. See the
    [CNIL's guidance on rights in AI models](https://www.cnil.fr/en/ensuring-and-facilitating-exercise-data-subjects-rights)
    and the [ICO's guidance on individual rights in AI systems](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/).
    [The unlearning audit](unlearning-audit.md) and [the enterprise playbook](enterprise-playbook.md) cover the
    evidence and the paperwork.

Sources for every case are linked in the course [README](https://github.com/Shreyan1/machine-unlearning-course#readme).
For a country-by-country summary, with links to each law and guidance document, see
[Policies around the world](global-policy.md).

## A worked example

Follow Carol's request from the technical side. The legal questions, such as which law applies and which exceptions
might hold, are for the company's lawyers. The engineer's job is to know what the model still shows and what each
option would change.

1. **The request.** Carol asks the company to erase her data. Her 40 digits were among the 1,257 used to train the
   digit model.
2. **Delete the records.** The rows go from the database. The model is unchanged, so it still gets 100.0% of her digits
   right against 77.5% for look-alike digits. Its behaviour still gives away that she was in training.
3. **Find every model.** The team checks which models were trained on her data, including any fine-tunes or copies
   made from them. [The enterprise playbook](enterprise-playbook.md) keeps a lineage registry for this.
4. **Choose a fix.** The team still holds the other 1,217 digits, so retraining is possible. Here it takes 0.27
   seconds. For a model whose training compute is counted in tens of millions of dollars, the team would compare
   retraining with a cheaper method and its evidence.
5. **Measure the result.** After retraining, Carol's digits score 55.0% against 62.5% for look-alike digits, and test
   accuracy stays at 98.0%. Her digits no longer stand out.
6. **Keep the evidence.** The team records what it ran, the numbers before and after, and the reference models it
   compared with. That record supports the legal answer. It does not replace it.

## Limits

**This page is not legal advice.** The summaries come from the course's [Policies around the world](global-policy.md)
page, which was checked in October 2026. Guidance changes often, and some of it is still in draft.

**The orders are about unlawful data.** The five model-deletion cases followed data that should never have been used.
They show what can happen then. They do not show what every ordinary erasure request requires.

**Guidance is not law.** The EDPB opinion and the CNIL and ICO guidance are not statutes, though regulators use them to
judge cases.

**A passed test is not compliance.** Unlearning can give evidence about what a model still reveals. Whether that is
enough for a particular request depends on the facts and the law that applies.

!!! tip "What to do in practice"
    - Keep a record of which data trained which models, including fine-tunes and distilled copies.
    - Design for deletion before training, with shards or adapters, so that retraining a part is cheap.
    - When you use a cheaper method, measure it against models retrained without the data and keep the numbers.
    - Write down why you chose each option, and involve the people who own the legal answer.

## Common mistakes

!!! danger "Mistakes people make"
    - **Thinking erasure means deleting rows.** Regulators have ordered the deletion of models, not just data.
    - **Claiming "we unlearnt it" without evidence.** A claim needs measurements against a gold standard.
    - **Ignoring derived models.** Contracts and orders often cover "any models derived from" the data, including
      fine-tunes and distilled copies.
    - **Reading "names unlearning" as "requires unlearning".** Every document that mentions it treats it as an option
      to consider or research.
    - **Treating an output filter as deletion.** The CNIL treats filters as a fallback, not as removing the data.

??? checkpoint "Checkpoint 3 · An order covers any models derived from the data. The company has the base model, a customer's fine-tune of it and a smaller distilled copy. Which are in scope?"
    **Very likely all three.** The fine-tune starts from the base model's weights, and the distilled copy learnt from
    the base model's answers, so both carry what the base learnt. The lawyers decide how the wording applies, but the
    engineer should list all three. That is why a record of which models came from which data, and from each other,
    matters before a request arrives.

## Key takeaways

!!! notes "Notes to take"
    - **Erasure rights.** GDPR Art. 17, India's DPDP Act 2023 s.12 and California's CCPA §1798.105.
    - **None mention weights.** Whether they reach a model depends on whether it holds or can reveal personal data.
    - **Anonymous model.** EDPB Opinion 28/2024 says personal data must not be extractable, even through queries.
    - **Model-deletion orders.** Everalbum 2021, WW/Kurbo 2022, Ring 2023, Rite Aid 2023 and Alipay 2025.
    - **The orders remove models.** They followed unlawful data and did not ask for unlearning.
    - **Cost.** About $78 million of compute for GPT-4 and $191 million for Gemini Ultra.
    - **Fallback.** The CNIL puts retraining first and treats output filters as a fallback, not deletion.
    - **Trap.** Derived models, such as fine-tunes and distilled copies, can be in scope too.
    - **Remember.** Unlearning gives evidence, not a legal guarantee.

## Quiz

```quiz
- q: Which law gives people in the EU the "right to be forgotten"?
  options:
    - GDPR Article 17
    - The US Copyright Act
    - The Video Privacy Protection Act
  answer: 0
  why: GDPR Art. 17 is the right to erasure. India's DPDP Act 2023 s.12 and California's CCPA have similar rights.
- q: What did the US FTC order Everalbum to delete in 2021?
  options:
    - Only the customers' photos
    - The face-recognition models and algorithms built from the photos
    - Its website
  answer: 1
  why: The order covered the models, not just the data. This is sometimes called "algorithmic disgorgement".
- q: According to EDPB Opinion 28/2024, when can a model trained on personal data be called anonymous?
  options:
    - Always, once training is finished
    - Only if extracting personal data from it, including through queries, is negligible
    - Never
  answer: 1
  why: If the data can be pulled out of the model, the model may still hold personal data.
- q: Does any regulator currently accept an unlearning method as proof of deletion?
  options:
    - Yes, gradient ascent is accepted everywhere.
    - No, not yet.
  answer: 1
  why: The rules are still being written. Unlearning gives evidence, which must be argued case by case.
- q: What did the model-deletion orders in this page's table have in common?
  options:
    - They asked the companies to unlearn the affected users.
    - They followed data that should not have been used, and the remedy reached the model.
    - They applied only to language models.
  answer: 1
  why: Each case began with data collected or used unlawfully, and the order covered the models built from it. None asked for unlearning.
- q: Why did the Munich ruling of November 2025 matter for unlearning?
  options:
    - It held that lyrics memorised in a model's weights count as a copy, so deleting the files does nothing.
    - It required every model to be retrained each year.
    - It banned language models in Germany.
  answer: 0
  why: When the data is inside the weights, removing the source files leaves the copy in place. The ruling is under appeal.
- q: The GPT-3 paper found test data in its training set. What did the team do?
  options:
    - Retrained the model at once
    - Used gradient ascent to remove it
    - Shipped the model and measured the flaw, because retraining cost too much
  answer: 2
  why: The paper says retraining was not feasible because of the cost. That is the gap unlearning tries to fill.
- q: According to the CNIL, what is an output filter when the training data is still held?
  options:
    - A fallback for when retraining is impossible or disproportionate, and not the same as removing the data
    - The preferred way to honour every erasure request
    - Proof that the data was deleted
  answer: 0
  why: The CNIL puts retraining first. A filter hides what the model knows without removing it.
```

## Try it

!!! levelup "Level up"
    You can now explain why a model, not just a database, can be within reach of the law, and what evidence a team
    should keep. Next quest, [Policies around the world](global-policy.md), where each law and guidance document gets
    its own card and link.

- Read the next concept, [Policies around the world](global-policy.md).
- Run the lesson [12 · Right to be forgotten and fairness](../lessons/12-right-to-be-forgotten-and-fairness.md) and
  [17 · The enterprise playbook](../lessons/17-enterprise-playbook.md).
