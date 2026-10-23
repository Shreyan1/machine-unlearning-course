# Machine Unlearning — Resource Library

A reference library for machine unlearning in Responsible AI. It was put together to check and extend §5.1 of *The Architect's Handbook: Engineering Responsible AI* (Shreyan Basu Ray, v1.0, 2026).

## Layout
```
resources/
├── README.md            ← this index
├── citation-audit.md    ← bibliography audit of the book, with corrected citations
├── catalog.json         ← machine-readable: title, authors, year, abstract, licence, relation to book
├── fetch_papers.py      ← downloads every PDF into papers/ (not stored in git)
├── book/                ← the handbook PDF + extracted plain text (grep-able)
├── papers/<topic>/      ← PDFs, named <year>-<first-author>-<short-title>.pdf, created by fetch_papers.py
└── text/                ← plain text of the openly licensed papers (fetch_papers.py adds the rest locally)
```

**Get the PDFs :** `python resources/fetch_papers.py` (about 130 MB). The notebooks cite papers by their local path,
e.g. `resources/papers/02-exact-unlearning/2019-bourtoule-sisa-machine-unlearning.pdf`, and this puts them there.

**Tip:** `grep -il "rewind" resources/text/*.txt` finds which papers discuss a concept.

**Licensing :** the papers belong to their authors and publishers, so the PDFs are linked, not redistributed. Plain-text
copies are kept in git only for papers under a Creative Commons licence or in the public domain (marked *text in repo*
below, with the licence); attribution is the citation on the same line. `catalog.json` records each paper's licence.

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
| 2015 | [Towards Making Systems Forget with Machine Unlearning](https://www.ieee-security.org/TC/SP2015/papers-archived/6949a463.pdf)<br><sub>Cao & Yang · PDF</sub> | Coined 'machine unlearning'; summation-form learners allow exact, fast deletion. | book ref 18 |
| 2019 | [Making AI Forget You: Data Deletion in Machine Learning](https://arxiv.org/abs/1907.05012)<br><sub>Ginart et al. · arXiv:1907.05012 · text in repo (CC BY-SA 4.0)</sub> | Formal deletion definition; DC-k-means / Q-k-means exact deletion for k-means. | book ref 21; DC-k-means row in table |
| 2020 | [Formalizing Data Deletion in the Context of the Right to be Forgotten](https://arxiv.org/abs/2002.10635)<br><sub>Garg et al. · arXiv:2002.10635</sub> | Cryptographic definition of deletion tied to the Right to be Forgotten. | book ref 20 (book has wrong title/authors/ID) |
| 2019 | [Certified Data Removal from Machine Learning Models](https://arxiv.org/abs/1911.03030)<br><sub>Guo et al. · arXiv:1911.03030 · text in repo (CC BY 4.0)</sub> | Certified removal (DP-style guarantee) for linear models via Newton step + noise. |  |

## Exact unlearning (SISA family)

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2019 | [Machine Unlearning](https://arxiv.org/abs/1912.03817)<br><sub>Bourtoule et al. · arXiv:1912.03817</sub> | SISA: sharded, isolated, sliced, aggregated training. Core exact method. | book ref 19; book SISA section |
| 2020 | [Machine Unlearning for Random Forests](https://arxiv.org/abs/2009.05567)<br><sub>Brophy & Lowd · arXiv:2009.05567</sub> | DaRE forests: cached stats, retrain only affected subtrees. | book table: DaRE |
| 2021 | [HedgeCut: Maintaining Randomised Trees for Low-Latency Machine Unlearning](https://ssc.io/pdf/rdm235.pdf)<br><sub>Schelter, Grafberger & Dunning · PDF</sub> | Low-latency unlearning for extremely randomised trees via subtree variants. | book table: HedgeCut |
| 2021 | [Graph Unlearning](https://arxiv.org/abs/2103.14991)<br><sub>Chen et al. · arXiv:2103.14991</sub> | GraphEraser: community-aware sharding for GNNs. | book table: GraphEraser |
| 2022 | [Recommendation Unlearning](https://arxiv.org/abs/2201.06820)<br><sub>Chen et al. · arXiv:2201.06820 · text in repo (CC BY-NC-SA 4.0)</sub> | RecEraser: partitioned recommender training with attention aggregation. | book table: RecEraser |
| 2022 | [ARCANE: An Efficient Architecture for Exact Machine Unlearning](https://www.ijcai.org/proceedings/2022/0556.pdf)<br><sub>Yan et al · PDF</sub> | One-class classifiers per class + preprocessing for exact unlearning. | book table: ARCANE |

## Approximate unlearning (SCRUB, Bad-T, …)

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2023 | [Towards Unbounded Machine Unlearning](https://arxiv.org/abs/2302.09880)<br><sub>Kurmanji et al. · arXiv:2302.09880</sub> | SCRUB: teacher-student max/min distillation; SCRUB+R rewinding for privacy. | book ref 27 (wrong authors/ID in book); book SCRUB section |
| 2022 | [Can Bad Teaching Induce Forgetting? Unlearning in Deep Networks using an Incompetent Teacher](https://arxiv.org/abs/2205.08096)<br><sub>Chundawat et al. · arXiv:2205.08096 · text in repo (CC BY-NC-SA 4.0)</sub> | Bad-T: competent + incompetent teacher distillation. | book ref 25 (wrong authors/ID in book); book Bad-T section |
| 2021 | [Fast Yet Effective Machine Unlearning](https://arxiv.org/abs/2111.08947)<br><sub>Tarun et al. · arXiv:2111.08947 · text in repo (CC BY-NC-ND 4.0)</sub> | UNSIR: error-maximising noise for class unlearning (impair-repair). |  |
| 2019 | [Eternal Sunshine of the Spotless Net: Selective Forgetting in Deep Networks](https://arxiv.org/abs/1911.04933)<br><sub>Golatkar et al. · arXiv:1911.04933</sub> | Fisher-information based scrubbing of weights. |  |
| 2020 | [Forgetting Outside the Box: Scrubbing Deep Networks of Information Accessible from Input-Output Observations](https://arxiv.org/abs/2003.02960)<br><sub>Golatkar et al. · arXiv:2003.02960</sub> | NTK-based scrubbing; info accessible from input-output observations. |  |
| 2020 | [Amnesiac Machine Learning](https://arxiv.org/abs/2010.10981)<br><sub>Graves et al. · arXiv:2010.10981</sub> | Amnesiac unlearning: undo stored batch updates; label-flip unlearning. | book ref 22 (wrong 3rd author in book) |
| 2021 | [Machine Unlearning via Algorithmic Stability](https://arxiv.org/abs/2102.13179)<br><sub>Ullah et al. · arXiv:2102.13179 · text in repo (CC BY 4.0)</sub> | Total-variation stability -> efficient unlearning for convex models. | book ref 23 (book attributes to Bourtoule; wrong ID) |
| 2023 | [SalUn: Empowering Machine Unlearning via Gradient-based Weight Saliency in Both Image Classification and Generation](https://arxiv.org/abs/2310.12508)<br><sub>Fan et al. · arXiv:2310.12508</sub> | SalUn: only update salient weights; random-label forgetting. Strong baseline. |  |
| 2023 | [Model Sparsity Can Simplify Machine Unlearning](https://arxiv.org/abs/2304.04934)<br><sub>Jia et al. · arXiv:2304.04934 · text in repo (CC BY 4.0)</sub> | Pruning before unlearning closes gap to retraining. |  |

## Evaluation & membership inference

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2016 | [Membership Inference Attacks against Machine Learning Models](https://arxiv.org/abs/1610.05820)<br><sub>Shokri et al. · arXiv:1610.05820</sub> | Original membership inference attack (shadow models). | MIA, referenced in book 5.1.2 |
| 2021 | [Membership Inference Attacks From First Principles](https://arxiv.org/abs/2112.03570)<br><sub>Carlini et al. · arXiv:2112.03570</sub> | LiRA: likelihood-ratio MIA; evaluate at low FPR. |  |
| 2020 | [When Machine Unlearning Jeopardizes Privacy](https://arxiv.org/abs/2005.02205)<br><sub>Chen et al. · arXiv:2005.02205</sub> | Comparing before/after models leaks the deleted samples. |  |
| 2021 | [On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning](https://arxiv.org/abs/2110.11891)<br><sub>Thudi et al. · arXiv:2110.11891</sub> | Why unlearning can't be verified from weights alone; need auditable algorithms. |  |
| 2024 | [Inexact Unlearning Needs More Careful Evaluations to Avoid a False Sense of Privacy](https://arxiv.org/abs/2403.01218)<br><sub>Hayes et al. · arXiv:2403.01218 · text in repo (CC BY 4.0)</sub> | Per-example MIA evaluation; inexact methods overestimate privacy. |  |
| 2024 | [Are we making progress in unlearning? Findings from the first NeurIPS unlearning competition](https://arxiv.org/abs/2406.09073)<br><sub>Triantafillou et al. · arXiv:2406.09073 · text in repo (CC BY 4.0)</sub> | Findings of NeurIPS 2023 unlearning challenge; evaluation protocol. |  |
| 2019 | [The Secret Sharer: Evaluating and Testing Unintended Memorization in Neural Networks](https://arxiv.org/abs/1802.08232)<br><sub>Carlini et al. · arXiv:1802.08232</sub> | Canaries and the exposure metric: rank of a secret among all candidates. | used in Problem 16 |
| 2021 | [Extracting Training Data from Large Language Models](https://arxiv.org/abs/2012.07805)<br><sub>Carlini et al. · arXiv:2012.07805</sub> | Verbatim extraction of phone numbers, addresses etc. from GPT-2. | used in Problem 16 |

## LLM unlearning

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2022 | [Knowledge Unlearning for Mitigating Privacy Risks in Language Models](https://arxiv.org/abs/2210.01504)<br><sub>Jang et al. · arXiv:2210.01504 · text in repo (CC BY 4.0)</sub> | Gradient ascent on target sequences to forget them in LMs. | book ref 26 (wrong authors/ID in book) |
| 2023 | [Large Language Model Unlearning](https://arxiv.org/abs/2310.10683)<br><sub>Yao et al. · arXiv:2310.10683 · text in repo (CC BY 4.0)</sub> | Gradient ascent + KL retain for harmful/copyright unlearning in LLMs. | book ref 28 (wrong authors in book) |
| 2023 | [Who's Harry Potter? Approximate Unlearning in LLMs](https://arxiv.org/abs/2310.02238)<br><sub>Eldan & Russinovich · arXiv:2310.02238 · text in repo (CC BY 4.0)</sub> | Erasing Harry Potter knowledge from Llama-2 via reinforced-model logits. | likely intended by book ref 29 |
| 2024 | [TOFU: A Task of Fictitious Unlearning for LLMs](https://arxiv.org/abs/2401.06121)<br><sub>Maini et al. · arXiv:2401.06121</sub> | TOFU: fictitious authors benchmark for LLM unlearning. |  |
| 2024 | [The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning](https://arxiv.org/abs/2403.03218)<br><sub>Li et al. · arXiv:2403.03218 · text in repo (CC BY 4.0)</sub> | WMDP hazardous-knowledge benchmark + RMU unlearning. |  |
| 2024 | [Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning](https://arxiv.org/abs/2404.05868)<br><sub>Zhang et al. · arXiv:2404.05868</sub> | NPO: bounded alternative to gradient ascent; avoids collapse. |  |
| 2024 | [MUSE: Machine Unlearning Six-Way Evaluation for Language Models](https://arxiv.org/abs/2407.06460)<br><sub>Shi et al. · arXiv:2407.06460 · text in repo (CC BY 4.0)</sub> | MUSE: six-way evaluation of LLM unlearning. |  |
| 2024 | [Eight Methods to Evaluate Robust Unlearning in LLMs](https://arxiv.org/abs/2402.16835)<br><sub>Lynch et al. · arXiv:2402.16835 · text in repo (CC BY 4.0)</sub> | Shows Harry-Potter-style unlearning is shallow; 8 eval methods. | supports book 5.1.4 |
| 2024 | [Do Unlearning Methods Remove Information from Language Model Weights?](https://arxiv.org/abs/2410.08827)<br><sub>Deeb & Roger · arXiv:2410.08827 · text in repo (CC BY 4.0)</sub> | Fine-tuning recovers 'unlearned' info -> suppression not removal. | supports book 5.1.4 |
| 2024 | [An Adversarial Perspective on Machine Unlearning for AI Safety](https://arxiv.org/abs/2409.18025)<br><sub>Łucki et al. · arXiv:2409.18025 · text in repo (CC BY 4.0)</sub> | Jailbreaks/finetuning recover RMU-unlearned hazardous knowledge. | supports book 5.1.4 |

## Surveys

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2022 | [A Survey of Machine Unlearning](https://arxiv.org/abs/2209.02299)<br><sub>Nguyen et al. · arXiv:2209.02299 · text in repo (CC BY-NC-ND 4.0)</sub> | Broad survey of MU definitions, methods, metrics. |  |
| 2024 | [Rethinking Machine Unlearning for Large Language Models](https://arxiv.org/abs/2402.08787)<br><sub>Liu et al. · arXiv:2402.08787 · text in repo (CC BY 4.0)</sub> | Position/survey on LLM unlearning scope and evaluation. |  |

## Added for the learning course (Problems 4, 14, 15, 19)

| Year | Paper | Why it matters | Used in |
|---|---|---|---|
| 2020 | [Does Learning Require Memorization? A Short Tale about a Long Tail](https://arxiv.org/abs/1906.05271)<br><sub>Feldman · arXiv:1906.05271</sub> | Long-tailed data makes memorisation necessary for accuracy. | used in Problem 4 |
| 2020 | [What Neural Networks Memorize and Why: Discovering the Long Tail via Influence Estimation](https://arxiv.org/abs/2008.03703)<br><sub>Feldman & Zhang · arXiv:2008.03703</sub> | Per-example memorisation scores via leave-subset-out training. | used in Problem 4 |
| 2021 | [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)<br><sub>Hu et al. · arXiv:2106.09685</sub> | Low-rank adapters on a frozen base; per-tenant adapters make deletion exact. | used in Problem 15 |
| 2023 | [Editing Models with Task Arithmetic](https://arxiv.org/abs/2212.04089)<br><sub>Ilharco et al. · arXiv:2212.04089 · text in repo (CC BY 4.0)</sub> | Task vectors; negation as approximate un-finetuning. | used in Problem 15 |
| 2024 | [Corrective Machine Unlearning](https://arxiv.org/abs/2402.14015)<br><sub>Goel et al. · arXiv:2402.14015 · text in repo (CC BY 4.0)</sub> | Removing the effect of manipulated data when only part of it is identified. | used in Problem 14 |
| 2024 | [Machine Unlearning Fails to Remove Data Poisoning Attacks](https://arxiv.org/abs/2406.17216)<br><sub>Pawelczyk et al. · arXiv:2406.17216 · text in repo (CC BY-NC-ND 4.0)</sub> | Unlearning the found poison does not remove poisoning effects. | used in Problem 14 |
| 2024 | [Fast Machine Unlearning Without Retraining Through Selective Synaptic Dampening](https://arxiv.org/abs/2308.07707)<br><sub>Foster, Schoepf & Brintrup · arXiv:2308.07707 · text in repo (CC BY 4.0)</sub> | SSD: no training at all; shrink the weights that matter far more for the forget data than for everything else. | Problem 19 |

## Other references from the book

| Year | Paper | Why it matters | Relation to book |
|---|---|---|---|
| 2018 | [Gender Shades](https://proceedings.mlr.press/v81/buolamwini18a/buolamwini18a.pdf)<br><sub>Buolamwini & Gebru · PDF</sub> |  | book ref 61 (book lists 'Buolamwini & Buolamwini') |
| 2023 | [AI Risk Management Framework (AI RMF 1.0), NIST AI 100-1, 2023.](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)<br><sub>NIST · PDF · text in repo (US Government work (public domain))</sub> |  | book ref 8 (book links NIST AI 600-1) |
| 2016 | [Inherent Trade-Offs in the Fair Determination of Risk Scores](https://arxiv.org/abs/1609.05807)<br><sub>Kleinberg et al. · arXiv:1609.05807</sub> | Impossibility theorem of fairness. | book ref 50; book 5.3.3 |

## Cited but not downloaded
- **KNOT**: Su & Li, *Asynchronous Federated Unlearning*, IEEE INFOCOM 2023, DOI 10.1109/INFOCOM53939.2023.10229075. Not on arXiv.
- **Villaronga, Kieseberg & Li (2018)**: *Humans Forget, Machines Remember*, Computer Law & Security Review 34(2). DOI 10.1016/j.clsr.2017.08.007 (paywalled). This is the legal background to the Right to be Forgotten.
