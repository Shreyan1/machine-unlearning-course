# Machine Unlearning — Resource Library

A reference library for machine unlearning in Responsible AI. It was put together to check and extend §5.1 of *The Architect's Handbook: Engineering Responsible AI* (Shreyan Basu Ray, v1.0, 2026).

## Layout
```
resources/
├── README.md            ← this index
├── citation-audit.md    ← bibliography audit of the book, with corrected citations
├── catalog.json         ← machine-readable: title, authors, year, abstract, relation to book
├── book/                ← the handbook PDF + extracted plain text (grep-able)
├── papers/<topic>/      ← PDFs, named <year>-<first-author>-<short-title>.pdf (08-course-additions: papers the notebooks cite)
└── text/                ← pdftotext output of every paper (for fast search)
```

**Tip:** `grep -il "rewind" resources/text/*.txt` finds which papers discuss a concept.

## Suggested reading order (for the exercise)
1. **Bourtoule et al. 2019 (SISA)**: the exact-unlearning baseline we implement.
2. **Kurmanji et al. 2023 (SCRUB)**: Eq. 3 and Algorithm 1 (alternating max/min epochs), and §3.2 SCRUB+R.
3. **Chundawat et al. 2022 (Bad-T)**: Eq. 3 `L = (1-l_u)·KL(T_s‖S) + l_u·KL(T_d‖S)`, 30% of retain data, 1 epoch.
4. **Shokri 2016 / Carlini 2021 (MIA)**: how we audit whether forgetting actually happened.
5. **Hayes et al. 2024 and Triantafillou et al. 2024**: why evaluation must compare against a *retrained* model.
6. **Lynch 2024, Deeb & Roger 2024, Łucki 2024**: evidence for the book's §5.1.4 claim that LLM unlearning is often just suppression.

## Foundations & definitions

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2015 | [Towards Making Systems Forget with Machine Unlearning](papers/01-foundations/2015-cao-yang-towards-making-systems-forget.pdf)<br><sub>Cao & Yang · PDF</sub> | Coined 'machine unlearning'; summation-form learners allow exact, fast deletion. | book ref 18 |
| 2019 | [Making AI Forget You: Data Deletion in Machine Learning](papers/01-foundations/2019-ginart-making-ai-forget-you.pdf)<br><sub>Ginart et al. · arXiv:1907.05012</sub> | Formal deletion definition; DC-k-means / Q-k-means exact deletion for k-means. | book ref 21; DC-k-means row in table |
| 2020 | [Formalizing Data Deletion in the Context of the Right to be Forgotten](papers/01-foundations/2020-garg-formalizing-data-deletion.pdf)<br><sub>Garg et al. · arXiv:2002.10635</sub> | Cryptographic definition of deletion tied to the Right to be Forgotten. | book ref 20 (book has wrong title/authors/ID) |
| 2019 | [Certified Data Removal from Machine Learning Models](papers/01-foundations/2019-guo-certified-data-removal.pdf)<br><sub>Guo et al. · arXiv:1911.03030</sub> | Certified removal (DP-style guarantee) for linear models via Newton step + noise. |  |

## Exact unlearning (SISA family)

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2019 | [Machine Unlearning](papers/02-exact-unlearning/2019-bourtoule-sisa-machine-unlearning.pdf)<br><sub>Bourtoule et al. · arXiv:1912.03817</sub> | SISA: sharded, isolated, sliced, aggregated training. Core exact method. | book ref 19; book SISA section |
| 2020 | [Machine Unlearning for Random Forests](papers/02-exact-unlearning/2020-brophy-dare-random-forests.pdf)<br><sub>Brophy & Lowd · arXiv:2009.05567</sub> | DaRE forests: cached stats, retrain only affected subtrees. | book table: DaRE |
| 2021 | [HedgeCut: Maintaining Randomised Trees for Low-Latency Machine Unlearning](papers/02-exact-unlearning/2021-schelter-hedgecut.pdf)<br><sub>Schelter, Grafberger & Dunning · PDF</sub> | Low-latency unlearning for extremely randomised trees via subtree variants. | book table: HedgeCut |
| 2021 | [Graph Unlearning](papers/02-exact-unlearning/2021-chen-graph-unlearning-grapheraser.pdf)<br><sub>Chen et al. · arXiv:2103.14991</sub> | GraphEraser: community-aware sharding for GNNs. | book table: GraphEraser |
| 2022 | [Recommendation Unlearning](papers/02-exact-unlearning/2022-chen-recommendation-unlearning-receraser.pdf)<br><sub>Chen et al. · arXiv:2201.06820</sub> | RecEraser: partitioned recommender training with attention aggregation. | book table: RecEraser |
| 2022 | [ARCANE: An Efficient Architecture for Exact Machine Unlearning](papers/02-exact-unlearning/2022-yan-arcane.pdf)<br><sub>Yan et al · PDF</sub> | One-class classifiers per class + preprocessing for exact unlearning. | book table: ARCANE |

## Approximate unlearning (SCRUB, Bad-T, …)

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2023 | [Towards Unbounded Machine Unlearning](papers/03-approximate-unlearning/2023-kurmanji-scrub-towards-unbounded-mu.pdf)<br><sub>Kurmanji et al. · arXiv:2302.09880</sub> | SCRUB: teacher-student max/min distillation; SCRUB+R rewinding for privacy. | book ref 27 (wrong authors/ID in book); book SCRUB section |
| 2022 | [Can Bad Teaching Induce Forgetting? Unlearning in Deep Networks using an Incompetent Teacher](papers/03-approximate-unlearning/2022-chundawat-bad-teacher.pdf)<br><sub>Chundawat et al. · arXiv:2205.08096</sub> | Bad-T: competent + incompetent teacher distillation. | book ref 25 (wrong authors/ID in book); book Bad-T section |
| 2021 | [Fast Yet Effective Machine Unlearning](papers/03-approximate-unlearning/2021-tarun-unsir-fast-yet-effective.pdf)<br><sub>Tarun et al. · arXiv:2111.08947</sub> | UNSIR: error-maximising noise for class unlearning (impair-repair). |  |
| 2019 | [Eternal Sunshine of the Spotless Net: Selective Forgetting in Deep Networks](papers/03-approximate-unlearning/2019-golatkar-eternal-sunshine.pdf)<br><sub>Golatkar et al. · arXiv:1911.04933</sub> | Fisher-information based scrubbing of weights. |  |
| 2020 | [Forgetting Outside the Box: Scrubbing Deep Networks of Information Accessible from Input-Output Observations](papers/03-approximate-unlearning/2020-golatkar-forgetting-outside-the-box.pdf)<br><sub>Golatkar et al. · arXiv:2003.02960</sub> | NTK-based scrubbing; info accessible from input-output observations. |  |
| 2020 | [Amnesiac Machine Learning](papers/03-approximate-unlearning/2020-graves-amnesiac-ml.pdf)<br><sub>Graves et al. · arXiv:2010.10981</sub> | Amnesiac unlearning: undo stored batch updates; label-flip unlearning. | book ref 22 (wrong 3rd author in book) |
| 2021 | [Machine Unlearning via Algorithmic Stability](papers/03-approximate-unlearning/2021-ullah-unlearning-algorithmic-stability.pdf)<br><sub>Ullah et al. · arXiv:2102.13179</sub> | Total-variation stability -> efficient unlearning for convex models. | book ref 23 (book attributes to Bourtoule; wrong ID) |
| 2023 | [SalUn: Empowering Machine Unlearning via Gradient-based Weight Saliency in Both Image Classification and Generation](papers/03-approximate-unlearning/2023-fan-salun-weight-saliency.pdf)<br><sub>Fan et al. · arXiv:2310.12508</sub> | SalUn: only update salient weights; random-label forgetting. Strong baseline. |  |
| 2023 | [Model Sparsity Can Simplify Machine Unlearning](papers/03-approximate-unlearning/2023-jia-model-sparsity-simplifies-unlearning.pdf)<br><sub>Jia et al. · arXiv:2304.04934</sub> | Pruning before unlearning closes gap to retraining. |  |

## Evaluation & membership inference

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2016 | [Membership Inference Attacks against Machine Learning Models](papers/04-evaluation-and-privacy/2016-shokri-membership-inference.pdf)<br><sub>Shokri et al. · arXiv:1610.05820</sub> | Original membership inference attack (shadow models). | MIA, referenced in book 5.1.2 |
| 2021 | [Membership Inference Attacks From First Principles](papers/04-evaluation-and-privacy/2021-carlini-lira-mia-first-principles.pdf)<br><sub>Carlini et al. · arXiv:2112.03570</sub> | LiRA: likelihood-ratio MIA; evaluate at low FPR. |  |
| 2020 | [When Machine Unlearning Jeopardizes Privacy](papers/04-evaluation-and-privacy/2020-chen-when-unlearning-jeopardizes-privacy.pdf)<br><sub>Chen et al. · arXiv:2005.02205</sub> | Comparing before/after models leaks the deleted samples. |  |
| 2021 | [On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning](papers/04-evaluation-and-privacy/2021-thudi-auditable-definitions.pdf)<br><sub>Thudi et al. · arXiv:2110.11891</sub> | Why unlearning can't be verified from weights alone; need auditable algorithms. |  |
| 2024 | [Inexact Unlearning Needs More Careful Evaluations to Avoid a False Sense of Privacy](papers/04-evaluation-and-privacy/2024-hayes-inexact-unlearning-careful-evals.pdf)<br><sub>Hayes et al. · arXiv:2403.01218</sub> | Per-example MIA evaluation; inexact methods overestimate privacy. |  |
| 2024 | [Are we making progress in unlearning? Findings from the first NeurIPS unlearning competition](papers/04-evaluation-and-privacy/2024-triantafillou-neurips-unlearning-competition.pdf)<br><sub>Triantafillou et al. · arXiv:2406.09073</sub> | Findings of NeurIPS 2023 unlearning challenge; evaluation protocol. |  |
| 2019 | [The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks](papers/04-evaluation-and-privacy/2019-carlini-secret-sharer-canary-exposure.pdf)<br><sub>Carlini et al. · arXiv:1802.08232</sub> | Canaries and the exposure metric: rank of a secret among all candidates. | used in Problem 16 |
| 2021 | [Extracting Training Data from Large Language Models](papers/04-evaluation-and-privacy/2021-carlini-extracting-training-data-llms.pdf)<br><sub>Carlini et al. · arXiv:2012.07805</sub> | Verbatim extraction of phone numbers, addresses etc. from GPT-2. | used in Problem 16 |

## LLM unlearning

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2022 | [Knowledge Unlearning for Mitigating Privacy Risks in Language Models](papers/05-llm-unlearning/2022-jang-knowledge-unlearning-lms.pdf)<br><sub>Jang et al. · arXiv:2210.01504</sub> | Gradient ascent on target sequences to forget them in LMs. | book ref 26 (wrong authors/ID in book) |
| 2023 | [Large Language Model Unlearning](papers/05-llm-unlearning/2023-yao-large-language-model-unlearning.pdf)<br><sub>Yao et al. · arXiv:2310.10683</sub> | Gradient ascent + KL retain for harmful/copyright unlearning in LLMs. | book ref 28 (wrong authors in book) |
| 2023 | [Who's Harry Potter? Approximate Unlearning in LLMs](papers/05-llm-unlearning/2023-eldan-russinovich-whos-harry-potter.pdf)<br><sub>Eldan & Russinovich · arXiv:2310.02238</sub> | Erasing Harry Potter knowledge from Llama-2 via reinforced-model logits. | likely intended by book ref 29 |
| 2024 | [TOFU: A Task of Fictitious Unlearning for LLMs](papers/05-llm-unlearning/2024-maini-tofu-benchmark.pdf)<br><sub>Maini et al. · arXiv:2401.06121</sub> | TOFU: fictitious authors benchmark for LLM unlearning. |  |
| 2024 | [The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning](papers/05-llm-unlearning/2024-li-wmdp-benchmark-rmu.pdf)<br><sub>Li et al. · arXiv:2403.03218</sub> | WMDP hazardous-knowledge benchmark + RMU unlearning. |  |
| 2024 | [Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning](papers/05-llm-unlearning/2024-zhang-npo-negative-preference-optimization.pdf)<br><sub>Zhang et al. · arXiv:2404.05868</sub> | NPO: bounded alternative to gradient ascent; avoids collapse. |  |
| 2024 | [MUSE: Machine Unlearning Six-Way Evaluation for Language Models](papers/05-llm-unlearning/2024-shi-muse-six-way-evaluation.pdf)<br><sub>Shi et al. · arXiv:2407.06460</sub> | MUSE: six-way evaluation of LLM unlearning. |  |
| 2024 | [Eight Methods to Evaluate Robust Unlearning in LLMs](papers/05-llm-unlearning/2024-lynch-eight-methods-robust-unlearning.pdf)<br><sub>Lynch et al. · arXiv:2402.16835</sub> | Shows Harry-Potter-style unlearning is shallow; 8 eval methods. | supports book 5.1.4 |
| 2024 | [Do Unlearning Methods Remove Information from Language Model Weights?](papers/05-llm-unlearning/2024-deeb-roger-do-unlearning-methods-remove-info.pdf)<br><sub>Deeb & Roger · arXiv:2410.08827</sub> | Fine-tuning recovers 'unlearned' info -> suppression not removal. | supports book 5.1.4 |
| 2024 | [An Adversarial Perspective on Machine Unlearning for AI Safety](papers/05-llm-unlearning/2024-lucki-adversarial-perspective-unlearning.pdf)<br><sub>Łucki et al. · arXiv:2409.18025</sub> | Jailbreaks/finetuning recover RMU-unlearned hazardous knowledge. | supports book 5.1.4 |

## Surveys

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2022 | [A Survey of Machine Unlearning](papers/06-surveys/2022-nguyen-survey-machine-unlearning.pdf)<br><sub>Nguyen et al. · arXiv:2209.02299</sub> | Broad survey of MU definitions, methods, metrics. |  |
| 2024 | [Rethinking Machine Unlearning for Large Language Models](papers/06-surveys/2024-liu-rethinking-unlearning-for-llms.pdf)<br><sub>Liu et al. · arXiv:2402.08787</sub> | Position/survey on LLM unlearning scope and evaluation. |  |

## Added for the learning course (Problems 4, 14, 15)

| Year | Paper | Why it matters | Used in |
|---|---|---|---|
| 2020 | [Does Learning Require Memorization? A Short Tale about a Long Tail](papers/08-course-additions/2020-feldman-learning-requires-memorization.pdf)<br><sub>Feldman · arXiv:1906.05271</sub> | Long-tailed data makes memorisation necessary for accuracy. | used in Problem 4 |
| 2020 | [What Neural Networks Memorize and Why: Discovering the Long Tail via Influence Estimation](papers/08-course-additions/2020-feldman-zhang-what-nns-memorize.pdf)<br><sub>Feldman & Zhang · arXiv:2008.03703</sub> | Per-example memorisation scores via leave-subset-out training. | used in Problem 4 |
| 2021 | [LoRA: Low-Rank Adaptation of Large Language Models](papers/08-course-additions/2021-hu-lora-low-rank-adaptation.pdf)<br><sub>Hu et al. · arXiv:2106.09685</sub> | Low-rank adapters on a frozen base; per-tenant adapters make deletion exact. | used in Problem 15 |
| 2023 | [Editing Models with Task Arithmetic](papers/08-course-additions/2023-ilharco-task-arithmetic.pdf)<br><sub>Ilharco et al. · arXiv:2212.04089</sub> | Task vectors; negation as approximate un-finetuning. | used in Problem 15 |
| 2024 | [Corrective Machine Unlearning](papers/08-course-additions/2024-goel-corrective-machine-unlearning.pdf)<br><sub>Goel et al. · arXiv:2402.14015</sub> | Removing the effect of manipulated data when only part of it is identified. | used in Problem 14 |
| 2024 | [Machine Unlearning Fails to Remove Data Poisoning Attacks](papers/08-course-additions/2024-pawelczyk-unlearning-fails-poisoning.pdf)<br><sub>Pawelczyk et al. · arXiv:2406.17216</sub> | Unlearning the found poison does not remove poisoning effects. | used in Problem 14 |

## Other references from the book

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2018 | [Gender Shades](papers/07-book-references-other/2018-buolamwini-gebru-gender-shades.pdf)<br><sub>Buolamwini & Gebru · PDF</sub> |  | book ref 61 (book lists 'Buolamwini & Buolamwini') |
| 2023 | [AI Risk Management Framework (AI RMF 1.0), NIST AI 100-1, 2023.](papers/07-book-references-other/2023-nist-ai-rmf-1.0.pdf)<br><sub>NIST · PDF</sub> |  | book ref 8 (book links NIST AI 600-1) |
| 2016 | [Inherent Trade-Offs in the Fair Determination of Risk Scores](papers/07-book-references-other/2016-kleinberg-inherent-tradeoffs.pdf)<br><sub>Kleinberg et al. · arXiv:1609.05807</sub> | Impossibility theorem of fairness. | book ref 50; book 5.3.3 |

## Cited but not downloaded
- **KNOT**: Su & Li, *Asynchronous Federated Unlearning*, IEEE INFOCOM 2023, DOI 10.1109/INFOCOM53939.2023.10229075. Not on arXiv.
- **Villaronga, Kieseberg & Li (2018)**: *Humans Forget, Machines Remember*, Computer Law & Security Review 34(2). DOI 10.1016/j.clsr.2017.08.007 (paywalled). This is the legal background to the Right to be Forgotten.
