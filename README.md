# MachineUnlearning
### Machine Unlearning for Responsible AI 🧹🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](requirements.txt)
[![Runs on CPU](https://img.shields.io/badge/runs%20on-a%20laptop%20CPU-brightgreen.svg)](#%EF%B8%8F-setup)
[![19 notebooks](https://img.shields.io/badge/notebooks-19-orange.svg)](ROADMAP.md)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb)

<p align="center"><img src="assets/diagrams/01_delete_vs_unlearn.png" alt="Deleting a row from a database removes it; deleting it from the training data leaves its influence inside the model" width="820"></p>

A hands-on, open-source course on **machine unlearning**: how to make a trained machine-learning model *forget* specific
data (a person, a class, poisoned samples, a customer's fine-tune, a fact inside an LLM) and how to **prove** it did.
Built for the **Right to be Forgotten (GDPR Art. 17, DPDP, CCPA)**, consent withdrawal, data poisoning and enterprise
fine-tuning, and runnable on a laptop in pure NumPy.

Every problem trains a model, **shows the issue**, **untrains** it, **shows the result**, and **proves it** against a
model that never saw the data. Classical ML first, then neural networks, then real data, fine-tuning and LLMs.

🤝 Feel free to contribute and help serve the community ! 🌎

---
### 👨‍💻 Pre-requisites :
- Python and NumPy at a working level; basic scikit-learn.
- Intermediate machine learning : what a loss function, gradient descent and overfitting are.
- No deep-learning framework needed - the neural networks are written in **pure NumPy**, every gradient readable.

---
### 🛠️ Setup

```bash
python -m venv .mulvenv
source .mulvenv/bin/activate      # Windows: .mulvenv\Scripts\activate
pip install -r requirements.txt
```

No install? Every notebook has an **Open in Colab** badge below; run its first cell and it fetches the course library.

Every notebook runs end to end on a laptop CPU, most in under a minute. The small datasets (UCI Adult, SMS Spam,
Olivetti faces, sklearn digits) download once into `data/`. Only the optional Problem 16b needs PyTorch
(`pip install -r requirements-optional.txt`).

---

### How to proceed with this repository ? 🤔

🏋️ **Want to practise?** [PRACTICE.md](PRACTICE.md) has **38 unsolved problems** across four tiers - Beginner, Amateur, Semi-Pro and Pro - each with a hint, references, and a checkable "done when".

🗺️ **New here? Start with the [ROADMAP](ROADMAP.md)** - the order the problems are meant to be read in, how long each stage takes, and the question each stage answers.

➡️ **Read `00-ReadFIRST.ipynb` first** [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/00-ReadFIRST.ipynb) : what unlearning is, why the law already demands it, the notation (D, D_f, D_r, θ_o, θ_r, θ_u) and a 60-second preview of the whole course.

<p align="center"><img src="assets/diagrams/00_ladder_of_forgetting.png" alt="The Ladder of Forgetting: the 17 problems ordered from easiest to hardest to forget" width="760"></p>

##### 🪜 Stage 1 - Classical ML : when forgetting is a subtraction

- **Problem 1 :** k-NN and Naive Bayes - the model *is* the data, or a sum over it. Unlearning is a delete or a subtraction, and it is **bit-for-bit exact**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/01-Classical-kNN-and-NaiveBayes.ipynb)

- **Problem 2 :** Linear and Logistic Regression - coupled sums. Ridge gets an exact rank-one downdate; logistic regression needs a **Newton step** (influence functions, certified removal) - the first *approximate* method. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/02-Classical-Linear-and-Logistic-Regression.ipynb)

- **Problem 3 :** SVM and Random Forest - no gradient, but *local* influence. Non-support vectors cost nothing to forget; a forest only retrains the trees that saw the point. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/03-Classical-SVM-and-Random-Forest.ipynb)

##### 🧠 Stage 2 - Neural networks : the problem

- **Problem 4 :** Deleting is not forgetting - every example touches 94% of the weights, and atypical people are **memorised** (Feldman's long tail). The Problem 1-3 tricks all fail. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/04-Neural-Nets-Deleting-Is-Not-Forgetting.ipynb)

- **Problem 5 :** Membership inference - how an attacker tells whether *your* data was used. Loss attacks, and the per-example **U-LiRA** test that flags 95% of Carol's digits. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/05-Membership-Inference-Attacks.ipynb)

##### ✅ Stage 3 - Exact unlearning for neural nets

- **Problem 6 :** Retraining and the **gold band** - two retrains differ, so "forgotten" is a *band*, not a number. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/06-Retrain-and-the-Gold-Band.ipynb)

- **Problem 7 :** SISA - shard and checkpoint at training time; unlearning becomes bit-exact and, with a **user-aware partition**, costs ~5% of a retrain. Plus the *recipe trap* in auditing. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/07-SISA-Exact-Unlearning-by-Design.ipynb)

##### ⚡ Stage 4 - Approximate unlearning

- **Problem 8 :** Fine-tune, gradient ascent, NegGrad+ - and the traps. Only **1 of 46** configurations passes the gate. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/08-Approximate-Baselines-and-Traps.ipynb)

- **Problem 9 :** SCRUB and SCRUB+R - a student that selectively disobeys its teacher. Works for class forgetting, **over-forgets or relapses** on a memorised individual. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/09-SCRUB-Teacher-Student-Unlearning.ipynb)

- **Problem 10 :** Bad Teacher - fast (under 1% of a retrain), but **random ≠ forgotten**, and its own metric ranks it above the gold standard. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/10-Bad-Teacher-Unlearning.ipynb)

##### 🔬 Stage 5 - Proof

- **Problem 11 :** The Unlearning Audit - one pre-registered protocol, five checks (FORGET, PRIVACY, UTILITY, COST, **RELEARN**), three request types, machine-readable evidence. The best-looking approximate method is *suppressed*, not removed. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/11-The-Unlearning-Audit.ipynb)

##### 🌍 Stage 6 - Real-world Responsible AI

- **Problem 12 :** Right to be Forgotten on the **Adult census** data - skewed erasure requests collapse the model's true-positive rate for women while accuracy does not move, and NegGrad+ adds a **method-made bias**. Fairness monitoring and mitigation. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/12-Right-to-be-Forgotten-and-Fairness.ipynb)

- **Problem 13 :** Consent withdrawn in **face recognition** (Olivetti) - exact eigenface unlearning, neural identity forgetting, and why **memory ≠ capability**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/13-Consent-Withdrawal-Face-Recognition.ipynb)

- **Problem 14 :** **Poisoned** SMS spam filter - a backdoor that exact unlearning cannot remove when only part of the poison is found, and a fix that works with 10% detection. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/14-Poisoned-Data-and-Backdoors.ipynb)

- **Problem 15 :** **Fine-tuning and un-finetuning** for an enterprise SaaS - per-tenant LoRA adapters (deletion is exact and free), re-fine-tuning from checkpoints, task-vector negation, and the lineage cascade. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/15-Fine-Tuning-and-Un-Finetuning.ipynb)

- **Problem 16 :** **LLM unlearning** - forgetting a phone number a language model can recite. n-gram subtraction, gradient ascent, NPO, refusal training, exposure, prefix forcing and the relearn attack : **refusal ≠ forgetting**. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16-LLM-Unlearning-Facts-Not-Rows.ipynb)

- **Problem 16b (optional, PyTorch) :** the same lesson on a small GPT-style transformer. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/16b-LLM-Unlearning-PyTorch.ipynb)

##### 🏢 Stage 7 - Engineering

- **Problem 17 :** The enterprise playbook - lineage registry, decision procedure, deadline planning, a **re-verifiable unlearning certificate**, owners for every threshold, and an Unlearning pillar for the RAI Scorecard. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/17-Enterprise-Unlearning-Playbook.ipynb)

##### 🧩 Stage 8 - Extensions : the same ideas in new places

- **Problem 18 :** **Recommender systems** on real MovieLens data - a user with unusual taste is on other people's "also watched" pages. Item-kNN forgets her **exactly** with a subtraction; matrix factorisation needs a retrain; and comparing the public pages before and after a deletion **reveals what was deleted**, unless you add fresh noise. [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shreyan1/machine-unlearning-course/blob/main/18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb)

---

### 🧰 What is in the box

```
00-ReadFIRST.ipynb … 18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb   the course (19 notebooks)
mul/            a small, readable "Machine UnLearning" library the notebooks share
  nn.py         NumPy MLP + Adam + LoRA adapters (hand-written, gradient-checked)
  classical.py  exact unlearning for k-NN, Naive Bayes, ridge, logistic (Newton), forests, SVM
  methods.py    retrain, SISA, fine-tune, gradient ascent, NegGrad+, SCRUB(+R), Bad Teacher
  audit.py      MIA, U-LiRA, gold band, relearn test, the gate
  lm.py         n-gram + neural character LMs, exposure, NPO
  recsys.py     item-kNN (exact unlearning), matrix factorisation, "also watched" pages, the diff attack
  lab.py, data.py, viz.py, train.py, torch_models.py (optional)
tests/          gradient checks and exactness proofs:  python tests/test_mul.py
assets/         diagrams (generated by assets/make_diagrams.py)
results/        audit evidence records and the certificate written by Problems 11 and 17
resources/      48 papers (links, licences, open-licence text), a catalogue, a citation audit,
                and fetch_papers.py to download the PDFs
```

---

### What to read/ study for this ? 🤓
All papers below are catalogued in [`resources/`](resources/README.md), with a suggested reading order.
`python resources/fetch_papers.py` downloads the PDFs to the paths the notebooks cite.

#### Foundational Papers to Study : 📑
1. [Towards Making Systems Forget with Machine Unlearning](https://www.ieee-security.org/TC/SP2015/papers-archived/6949a463.pdf) - Cao & Yang 2015 - *Problem 1*
2. [Certified Data Removal from Machine Learning Models](https://arxiv.org/abs/1911.03030) - Guo et al. 2019 - *Problems 2, 12*
3. [Machine Unlearning (SISA)](https://arxiv.org/abs/1912.03817) - Bourtoule et al. 2019 - *Problem 7*
4. [Does Learning Require Memorization?](https://arxiv.org/abs/1906.05271) - Feldman 2020 - *Problem 4*

#### Papers behind Problems 5 - 17 : 📄
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

#### Books and Materials : 📚
1. *The Architect's Handbook: Engineering Responsible AI* by Shreyan Basu Ray - §5.1 on machine unlearning and the RAI Scorecard (in `resources/book/`).
2. [A Survey of Machine Unlearning](https://arxiv.org/abs/2209.02299) - Nguyen et al.
3. [Rethinking Machine Unlearning for Large Language Models](https://arxiv.org/abs/2402.08787) - Liu et al.

#### Regulation the course refers to : ⚖️
- GDPR Art. 17 (right to erasure), Art. 7(3) (withdrawal of consent), Art. 9 (biometric data), Art. 12(3) (one-month response)
- EDPB Opinion 28/2024 on AI models and personal data
- India DPDP Act 2023 s.12 · California CCPA §1798.105
- FTC orders requiring deletion of models: Everalbum (2021), WW/Kurbo (2022), Rite Aid (2023)

---

### ❓ FAQ

**What is machine unlearning?** Removing the influence of specific training data from an already-trained model, so it
behaves like a model that was never trained on that data. Deleting the data from a database is not enough.

**Why does Responsible AI need it?** Privacy laws (GDPR Art. 17, India's DPDP Act, CCPA) give people the right to erasure,
regulators such as the FTC have ordered companies to delete models built on unlawfully used data, and poisoned or
copyrighted data has to be removed from deployed models.

**What is the difference between exact and approximate unlearning?** Exact unlearning (retraining, SISA, Naive Bayes
subtraction, deleting a LoRA adapter) provably gives the same model as retraining without the data. Approximate unlearning
(gradient ascent, NegGrad+, SCRUB, Bad Teacher, NPO) is cheaper but must be audited - see Problem 11.

**How do you prove a model forgot?** Compare it with models retrained without the data (the *gold band*), and attack it:
membership inference (U-LiRA), the relearn attack, and for LLMs exposure and prefix forcing.

**Can LLMs really unlearn?** Often they only *suppress*: refusal training hides a fact that prefix forcing and relearning
bring back (Problems 16 and 16b). Re-fine-tuning from a clean checkpoint is the reliable route.

**Do I need a GPU or PyTorch?** No. Everything runs on a CPU in pure NumPy; only the optional Problem 16b uses PyTorch.

**Keywords :** machine unlearning, right to be forgotten, data deletion, GDPR, responsible AI, AI privacy, membership
inference, SISA, SCRUB, Bad Teacher, NPO, LLM unlearning, LoRA unlearning, un-finetuning, data poisoning, AI governance.

---
#### Connect with me on Linkedin - [@shreyanbasuray](https://www.linkedin.com/in/shreyanbasuray) 🪩

─── ⋆⋅☆⋅⋆ ───
