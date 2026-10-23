# Machine Unlearning for Responsible AI 🧹

**A hands-on course on making a trained model forget someone's data, and proving that it did.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](requirements.txt)
[![Runs on CPU](https://img.shields.io/badge/runs%20on-a%20laptop%20CPU-brightgreen.svg)](#%EF%B8%8F-setup)
[![21 notebooks](https://img.shields.io/badge/notebooks-21-orange.svg)](ROADMAP.md)
[![40 practice problems](https://img.shields.io/badge/practice%20problems-40-purple.svg)](PRACTICE.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb)

<p align="center"><img src="assets/diagrams/01_delete_vs_unlearn.png" alt="Deleting a row from a database removes it; deleting it from the training data leaves its influence inside the model" width="820"></p>

### Meet Carol

A digit-recognition model is trained on 1,257 handwritten digits. Forty of them were written by **Carol**, with a thick
marker that nobody else used. The model gets **100%** of her digits right, and it is clearly worse on thick-marker digits
it has never seen. It did not just learn "thick digits". It memorised *hers*.

Carol asks to be forgotten. The company deletes her rows from the database. **Nothing changes**: the weights are already
trained, and an attacker can still tell she was in the training data.

This course is about what to do next. Every problem follows the same five steps:

> **Train** a model → **show the issue** (it still remembers) → **untrain** it → **show the result** → **prove it**
> against models that never saw the data.

The target is not 0% on Carol. A model that never met her can still read many of her digits. The target is the
**gold band**: the range of results you get from several models retrained without her. Most unlearning tutorials get
this wrong, and this course is built around getting it right.

<p align="center">
  ▶️ <a href="https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb"><b>Start in Colab, no install</b></a>
  &nbsp;·&nbsp; 🧭 <a href="#-pick-your-path"><b>Pick your path</b></a>
  &nbsp;·&nbsp; 🪜 <a href="#-the-ladder-of-forgetting"><b>See all problems</b></a>
  &nbsp;·&nbsp; 🏋️ <a href="PRACTICE.md"><b>Practise</b></a>
</p>

---

### 🔎 Eight things this course shows

1. **Deleting is not forgetting.** In a neural network, every training example touches 94% of the weights. *(Problem 4)*
2. **"Forgotten" is a band, not a number.** Two retrains without Carol disagree with each other, so you need several. *(Problem 6)*
3. **Most quick fixes fail.** Of 46 fine-tune, gradient-ascent and NegGrad+ settings, only **1** passes the audit. *(Problem 8)*
4. **A method can grade itself too kindly.** Bad Teacher's own metric ranks it *above* the gold standard. *(Problem 10)*
5. **Erasure requests can hurt fairness.** On census data, skewed requests drop the model's true-positive rate for women while accuracy does not move. *(Problem 12)*
6. **Refusal is not forgetting.** A language model trained to say "(withheld)" for Dana's phone number can still be made to give it up, by prefix forcing or a little relearning. *(Problem 16)*
7. **Even an exact deletion can leak.** Comparing a recommender's public pages before and after a deletion tells an attacker what the deleted user watched, unless fresh noise is added. *(Problem 18)*
8. **Newer methods are not automatically better, and a privacy test can be fooled.** Fourteen methods sit one fixed exam: no approximate method forgets Carol, and methods that make the model less sure of *everything* look "forgotten" until the test's reference models are built the same way. *(Problem 19)*

---

### 🧭 Pick your path

You do not have to do all 21 notebooks. Find the row that sounds like you. Each route takes the problems in order.

| You are... | Do these problems | Time |
|---|---|---|
| **New to unlearning** and want the whole idea | `00` → `01` → `04` → `06` → `07` → `08` → `11` | ~4 hrs |
| A **privacy, legal or governance** person who needs to judge an unlearning claim | `00` → `04` → `06` → `11` → `12` → `17` | ~4 hrs |
| An **ML researcher** comparing unlearning methods | `00` → `04` → `05` → `06` → `08` → `09` → `10` → `11` → `19` | ~6 hrs |
| An **LLM engineer** who needs a model to forget facts or a customer's fine-tune | `00` → `04` → `06` → `11` → `15` → `16` → `16b` | ~5 hrs |
| A **platform or MLOps engineer** designing systems that can delete | `00` → `06` → `07` → `11` → `15` → `17` → `18` | ~5 hrs |
| Doing **the full course** | everything, in order | ~19-27 hrs |

Times use the estimate at the top of each notebook and add a little for the tasks. The [ROADMAP](ROADMAP.md) has
the full stage-by-stage plan and a checkpoint for each stage.

---

### 👨‍💻 Before you start

- Python and NumPy at a working level; basic scikit-learn.
- Intermediate machine learning: what a loss function, gradient descent and overfitting are.
- No deep-learning framework needed. The neural networks are written in **pure NumPy**, so you can read every gradient.
- No legal background needed. Each legal idea is explained where it is used.

### 🛠️ Setup

```bash
python -m venv .mulvenv
source .mulvenv/bin/activate      # Windows: .mulvenv\Scripts\activate
pip install -r requirements.txt
python tests/test_mul.py          # gradient checks + exactness proofs, ~1 minute
```

No install? Every notebook has an **Open in Colab** badge. Run its first cell and it fetches the course library.

Every notebook runs end to end on a laptop CPU, most in under a minute. The small datasets (UCI Adult, SMS Spam,
Olivetti faces, sklearn digits, MovieLens) download once into `data/`. Only the optional Problem 16b needs PyTorch
(`pip install -r requirements-optional.txt`).

---

### 🪜 The Ladder of Forgetting

The problems are one argument, climbed one rung at a time. Each notebook ends with an **❓ Open question** that the
next one answers. Lower rungs are models where forgetting is a subtraction. The top rungs are LLMs, where nobody can
yet do it reliably.

<p align="center"><img src="assets/diagrams/00_ladder_of_forgetting.png" alt="The Ladder of Forgetting: the problems ordered from easiest to hardest to forget" width="760"></p>

Start with **`00-ReadFIRST.ipynb`** [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb): what unlearning is, why the law already demands it, the notation (D, D_f, D_r, θ_o, θ_r, θ_u) and a 60-second preview of the whole course with Carol.

Click a stage to see its problems.

<details>
<summary><b>🪜 Stage 1 · Classical ML</b>: when forgetting is a subtraction · Problems 1-3 · ~1.5 hrs</summary>
<br>

- **Problem 1:** k-NN and Naive Bayes. The model *is* the data, or a sum over it. Unlearning is a delete or a subtraction, and it is **bit-for-bit exact**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb)

- **Problem 2:** Linear and Logistic Regression. Coupled sums. Ridge gets an exact rank-one downdate; logistic regression needs a **Newton step** (influence functions, certified removal), the first *approximate* method. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/02-Classical-Linear-and-Logistic-Regression.ipynb)

- **Problem 3:** SVM and Random Forest. No gradient, but *local* influence. Non-support vectors cost nothing to forget; a forest only retrains the trees that saw the point. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb)

</details>

<details>
<summary><b>🧠 Stage 2 · Neural networks</b>: the problem · Problems 4-5 · ~1 hr</summary>
<br>

- **Problem 4:** Deleting is not forgetting. Every example touches 94% of the weights, and unusual people like Carol are **memorised** (Feldman's long tail). The Problem 1-3 tricks all fail. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb)

- **Problem 5:** Membership inference. How an attacker tells whether *your* data was used. Loss attacks, and the per-example **U-LiRA** test that flags 95% of Carol's digits. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb)

</details>

<details>
<summary><b>✅ Stage 3 · Exact unlearning for neural nets</b> · Problems 6-7 · ~1 hr</summary>
<br>

- **Problem 6:** Retraining and the **gold band**. Two retrains differ, so "forgotten" is a *band*, not a number. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb)

- **Problem 7:** SISA. Shard and checkpoint at training time; unlearning becomes bit-exact and, with a **user-aware partition**, costs ~5% of a retrain. Plus the *recipe trap* in auditing. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/07-SISA-Exact-Unlearning-by-Design.ipynb)

</details>

<details>
<summary><b>⚡ Stage 4 · Approximate unlearning</b>: cheaper, and full of traps · Problems 8-10 · ~2 hrs</summary>
<br>

- **Problem 8:** Fine-tune, gradient ascent, NegGrad+, and the traps. Only **1 of 46** configurations passes the gate. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/08-Approximate-Baselines-and-Traps.ipynb)

- **Problem 9:** SCRUB and SCRUB+R. A student that selectively disobeys its teacher. Works for class forgetting, but **over-forgets or relapses** on a memorised individual. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb)

- **Problem 10:** Bad Teacher. Fast (under 1% of a retrain), but **random ≠ forgotten**, and its own metric ranks it above the gold standard. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb)

</details>

<details>
<summary><b>🔬 Stage 5 · Proof</b> · Problem 11 · ~45 min</summary>
<br>

- **Problem 11:** The Unlearning Audit. One pre-registered protocol, five checks (FORGET, PRIVACY, UTILITY, COST, **RELEARN**), three request types, machine-readable evidence. The best-looking approximate method is *suppressed*, not removed. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb)

</details>

<details>
<summary><b>🌍 Stage 6 · Real-world Responsible AI</b>: fairness, faces, poison, fine-tunes, LLMs · Problems 12-16b · ~4 hrs</summary>
<br>

- **Problem 12:** Right to be Forgotten on the **Adult census** data. Skewed erasure requests collapse the model's true-positive rate for women while accuracy does not move, and NegGrad+ adds a **method-made bias**. Fairness monitoring and mitigation. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb)

- **Problem 13:** Consent withdrawn in **face recognition** (Olivetti). Exact eigenface unlearning, neural identity forgetting, and why **memory ≠ capability**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb)

- **Problem 14:** A **poisoned** SMS spam filter. A backdoor that exact unlearning cannot remove when only part of the poison is found, and a fix that works with 10% detection. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/14-Poisoned-Data-and-Backdoors.ipynb)

- **Problem 15:** **Fine-tuning and un-finetuning** for an enterprise SaaS. Per-tenant LoRA adapters (deletion is exact and free), re-fine-tuning from checkpoints, task-vector negation, and the lineage cascade. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/15-Fine-Tuning-and-Un-Finetuning.ipynb)

- **Problem 16:** **LLM unlearning.** Forgetting a phone number a language model can recite. n-gram subtraction, gradient ascent, NPO, refusal training, exposure, prefix forcing and the relearn attack: **refusal ≠ forgetting**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb)

- **Problem 16b (optional, PyTorch):** the same lesson on a small GPT-style transformer. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16b-LLM-Unlearning-PyTorch.ipynb)

</details>

<details>
<summary><b>🏢 Stage 7 · Engineering</b>: a deletion request, end to end · Problem 17 · ~45 min</summary>
<br>

- **Problem 17:** The enterprise playbook. Lineage registry, decision procedure, deadline planning, a **re-verifiable unlearning certificate**, owners for every threshold, and an Unlearning pillar for the RAI Scorecard. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/17-Enterprise-Unlearning-Playbook.ipynb)

</details>

<details>
<summary><b>🧩 Stage 8 · Extensions</b>: the same ideas in new places · Problems 18-19 · ~1.5 hrs</summary>
<br>

- **Problem 18:** **Recommender systems** on real MovieLens data. Erin, a user with unusual taste, is on other people's "also watched" pages. Item-kNN forgets her **exactly** with a subtraction; matrix factorisation needs a retrain; and comparing the public pages before and after a deletion **reveals what was deleted**, unless you add fresh noise. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb)

- **Problem 19:** **The method zoo.** Fourteen methods, from retraining to SalUn and SSD, sit Problem 11's exam on three requests, labelled by family (model-agnostic, model-intrinsic, data-driven). No approximate method forgets Carol, and the new methods' passes on the random request turn out to be a **confidence trick** that only a fairly built privacy test catches. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/19-The-Method-Zoo.ipynb)

</details>

🏋️ **Want to test yourself?** [PRACTICE.md](PRACTICE.md) has **40 unsolved problems** in four tiers (Beginner, Amateur,
Semi-Pro and Pro), each with a hint, references and a checkable "done when".

---

### 🧰 What is in the box

```
00-ReadFIRST.ipynb … 19-The-Method-Zoo.ipynb   the course (21 notebooks)
mul/            a small, readable "Machine UnLearning" library the notebooks share
  nn.py         NumPy MLP + Adam + LoRA adapters (hand-written, gradient-checked)
  classical.py  exact unlearning for k-NN, Naive Bayes, ridge, logistic (Newton), forests, SVM
  methods.py    retrain, SISA, fine-tune, gradient ascent, NegGrad+, SCRUB(+R), Bad Teacher,
                random labels, SalUn, L1-sparse, UNSIR, SSD, last-layer re-solve
  audit.py      MIA, U-LiRA, gold band, relearn test, the gate
  lm.py         n-gram + neural character LMs, exposure, NPO
  recsys.py     item-kNN (exact unlearning), matrix factorisation, "also watched" pages, the diff attack
  lab.py, data.py, viz.py, train.py, torch_models.py (optional)
tests/          gradient checks and exactness proofs:  python tests/test_mul.py
assets/         diagrams (generated by assets/make_diagrams.py)
results/        audit evidence records, the certificate and the leaderboard (Problems 11, 17, 19)
resources/      49 papers (links, licences, open-licence text), a catalogue, a citation audit,
                and fetch_papers.py to download the PDFs
templates/      the starting notebook for a new problem (see CONTRIBUTING.md)
```

---

### 🤓 What to read

All papers below are catalogued in [`resources/`](resources/README.md), with a suggested reading order.
`python resources/fetch_papers.py` downloads the PDFs to the paths the notebooks cite.

<details>
<summary><b>📑 Foundational papers</b></summary>
<br>

1. [Towards Making Systems Forget with Machine Unlearning](https://www.ieee-security.org/TC/SP2015/papers-archived/6949a463.pdf) - Cao & Yang 2015 - *Problem 1*
2. [Certified Data Removal from Machine Learning Models](https://arxiv.org/abs/1911.03030) - Guo et al. 2019 - *Problems 2, 12*
3. [Machine Unlearning (SISA)](https://arxiv.org/abs/1912.03817) - Bourtoule et al. 2019 - *Problem 7*
4. [Does Learning Require Memorization?](https://arxiv.org/abs/1906.05271) - Feldman 2020 - *Problem 4*

</details>

<details>
<summary><b>📄 Papers behind Problems 5-19</b></summary>
<br>

5. [Membership Inference Attacks From First Principles (LiRA)](https://arxiv.org/abs/2112.03570) - *Problem 5*
6. [Inexact Unlearning Needs More Careful Evaluations (U-LiRA)](https://arxiv.org/abs/2403.01218) - *Problems 5, 11*
7. [Towards Unbounded Machine Unlearning (SCRUB)](https://arxiv.org/abs/2302.09880) - *Problem 9*
8. [Can Bad Teaching Induce Forgetting? (Bad Teacher)](https://arxiv.org/abs/2205.08096) - *Problem 10*
9. [On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning](https://arxiv.org/abs/2110.11891) - *Problems 11, 17*
10. [Machine Unlearning Fails to Remove Data Poisoning Attacks](https://arxiv.org/abs/2406.17216) - *Problem 14*
11. [LoRA](https://arxiv.org/abs/2106.09685) and [Editing Models with Task Arithmetic](https://arxiv.org/abs/2212.04089) - *Problem 15*
12. [The Secret Sharer (exposure)](https://arxiv.org/abs/1802.08232) - *Problem 16*
13. [Negative Preference Optimization](https://arxiv.org/abs/2404.05868) - *Problem 16*
14. [Eight Methods to Evaluate Robust Unlearning in LLMs](https://arxiv.org/abs/2402.16835) and [Do Unlearning Methods Remove Information from LLM Weights?](https://arxiv.org/abs/2410.08827) - *Problem 16*
15. [Recommendation Unlearning (RecEraser)](https://arxiv.org/abs/2201.06820) and [When Machine Unlearning Jeopardizes Privacy](https://arxiv.org/abs/2005.02205) - *Problem 18*
16. [SalUn](https://arxiv.org/abs/2310.12508), [Selective Synaptic Dampening](https://arxiv.org/abs/2308.07707), [Model Sparsity Can Simplify Machine Unlearning](https://arxiv.org/abs/2304.04934), [UNSIR](https://arxiv.org/abs/2111.08947) and [Amnesiac Machine Learning](https://arxiv.org/abs/2010.10981) - *Problem 19*

</details>

<details>
<summary><b>📚 Books and surveys</b></summary>
<br>

1. *The Architect's Handbook: Engineering Responsible AI* by Shreyan Basu Ray - §5.1 on machine unlearning and the RAI Scorecard (in `resources/book/`).
2. [A Survey of Machine Unlearning](https://arxiv.org/abs/2209.02299) - Nguyen et al.
3. [Rethinking Machine Unlearning for Large Language Models](https://arxiv.org/abs/2402.08787) - Liu et al.

</details>

<details>
<summary><b>⚖️ Regulation the course refers to</b></summary>
<br>

- GDPR Art. 17 (right to erasure), Art. 7(3) (withdrawal of consent), Art. 9 (biometric data), Art. 12(3) (one-month response)
- EDPB Opinion 28/2024 on AI models and personal data
- India DPDP Act 2023 s.12 · California CCPA §1798.105
- FTC orders requiring deletion of models: Everalbum (2021), WW/Kurbo (2022), Rite Aid (2023)

</details>

---

### ❓ FAQ

**What is machine unlearning?** Removing the influence of specific training data from an already-trained model, so it
behaves like a model that was never trained on that data. Deleting the data from a database is not enough.

**Why does Responsible AI need it?** Privacy laws (GDPR Art. 17, India's DPDP Act, CCPA) give people the right to erasure,
regulators such as the FTC have ordered companies to delete models built on unlawfully used data, and poisoned or
copyrighted data has to be removed from deployed models.

**What is the difference between exact and approximate unlearning?** Exact unlearning (retraining, SISA, Naive Bayes
subtraction, deleting a LoRA adapter) provably gives the same model as retraining without the data. Approximate unlearning
(gradient ascent, NegGrad+, SCRUB, Bad Teacher, NPO) is cheaper but must be audited. See Problem 11.

**How do you prove a model forgot?** Compare it with models retrained without the data (the *gold band*), and attack it:
membership inference (U-LiRA), the relearn attack, and for LLMs exposure and prefix forcing.

**Can LLMs really unlearn?** Often they only *suppress*: refusal training hides a fact that prefix forcing and relearning
bring back (Problems 16 and 16b). Re-fine-tuning from a clean checkpoint is the reliable route.

**Do I need a GPU or PyTorch?** No. Everything runs on a CPU in pure NumPy; only the optional Problem 16b uses PyTorch.

**Keywords:** machine unlearning, right to be forgotten, data deletion, GDPR, responsible AI, AI privacy, membership
inference, SISA, SCRUB, Bad Teacher, NPO, LLM unlearning, LoRA unlearning, un-finetuning, data poisoning, AI governance.

---

### 🤝 Contributing

Found a bug, a wrong number or a confusing sentence? Want to add a new problem? You are very welcome. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first. New problems start from
[`templates/problem-template.ipynb`](templates/problem-template.ipynb), so every notebook keeps the same five steps.

### 📌 Citing

If you use this course in teaching or research, please cite it. GitHub's **"Cite this repository"** button (from
[CITATION.cff](CITATION.cff)) gives you BibTeX and APA.

---
#### Connect with me 🪩

[![X](https://img.shields.io/badge/X-@shreyanbr-000000?logo=x&logoColor=white)](https://x.com/shreyanbr)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-shreyanbasuray-0A66C2?logo=linkedin&logoColor=white)](https://linkedin.com/in/shreyanbasuray)
[![Website](https://img.shields.io/badge/Website-shreyanbasuray.com-4C9A2A?logo=googlechrome&logoColor=white)](https://shreyanbasuray.com)

─── ⋆⋅☆⋅⋆ ───
