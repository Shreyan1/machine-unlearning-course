# 🗺️ The Roadmap

A guided path through this repository. The problems are **ordered on purpose** - each one ends with an
**❓ Open question** that the next one answers. If you only read the notebooks you like the sound of, you will miss
the argument they make together : *forgetting gets harder as models get more powerful, and the cure is mostly
designing for deletion before training.*

> **How to use this page :** find the stage that matches where you are, do the notebooks in order, and do not skip
> the `#### TASK :` sections at the bottom of each one. That is where the learning actually happens.
>
> When you want to test yourself away from the notebooks, [PRACTICE.md](PRACTICE.md) has 40 unsolved problems tiered
> Beginner → Pro, cross-referenced to the stages below.

---

## ⏱️ Time estimates

| Stage | Notebooks | Time | You will be able to... |
|---|---|---|---|
| 0. Foundations | `00` | 1 hr | explain unlearning, why the law needs it, and the gold standard |
| 1. Classical ML | `01` - `03` | 2-3 hrs | unlearn k-NN, Naive Bayes, ridge, logistic regression, SVMs and forests exactly or near-exactly |
| 2. Neural networks : the problem | `04` - `05` | 2-3 hrs | measure memorisation and run membership-inference attacks |
| 3. Exact unlearning for neural nets | `06` - `07` | 2-3 hrs | build a gold band and a SISA system |
| 4. Approximate unlearning | `08` - `10` | 3-4 hrs | run fine-tune, gradient ascent, NegGrad+, SCRUB(+R), Bad Teacher - and catch them failing |
| 5. Proof | `11` | 1-2 hrs | run a pre-registered five-check audit and write an evidence record |
| 6. Real-world Responsible AI | `12` - `16`, `16b` | 5-7 hrs | handle fairness, biometric consent, poisoning, per-tenant fine-tunes and LLM facts |
| 7. Engineering | `17` | 1-2 hrs | run a deletion request end to end and issue a re-verifiable certificate |
| 8. Extensions | `18`, `19` | 2 hrs | remove a user from a recommender; run fourteen methods through one fair exam |

Roughly **19-27 hours** end to end at a comfortable pace. Every notebook runs on a laptop CPU.

---

## 👨‍💻 Before you start

**You need :**
- Python and NumPy at a working level
- Basic machine learning : train/test split, loss, gradient descent, overfitting
- A little linear algebra : matrix products, inverses (Problem 2 uses them; the intuition is always given first)

**You do NOT need :**
- PyTorch or TensorFlow - every neural network here is written in NumPy (only the optional 16b uses PyTorch)
- A GPU
- A legal background - each legal idea is introduced where it is needed

**Setup :**
```bash
python -m venv .mulvenv
source .mulvenv/bin/activate      # Windows: .mulvenv\Scripts\activate
pip install -r requirements.txt
python tests/test_mul.py          # gradient checks + exactness proofs, ~1 minute
```

---

## Stage 0 · Foundations

### 📓 `00-ReadFIRST.ipynb`
Deleting vs unlearning, real cases (GDPR Art. 17, FTC model-deletion orders, EDPB Opinion 28/2024), the notation
(`D`, `D_f`, `D_r`, `θ_o`, `θ_r`, `θ_u`), the Ladder of Forgetting, and a 60-second preview with Carol, the person whose
40 thick-marker digits the course keeps trying to forget.

> **Read this first, properly.** Every later notebook assumes it. The single idea to keep : *the target is the
> retrained model, not zero.*

✅ **Checkpoint :** you can explain to a colleague why accuracy on Carol's digits should *not* go to 0%.

---

## Stage 1 · Classical ML - when is forgetting a subtraction?

| Notebook | Question | Key idea |
|---|---|---|
| `01` k-NN, Naive Bayes | what if the model *is* the data, or a sum over it? | delete / subtract, bit-for-bit exact |
| `02` Linear, Logistic | what if the sums are coupled? | rank-one downdate; Newton step = influence function |
| `03` SVM, Random Forest | what if influence is *local*? | non-support vectors are free; retrain only touched trees |

✅ **Checkpoint :** you can name the property of a model that makes exact unlearning cheap (summation form / locality).

---

## Stage 2 · Neural networks - the problem

| Notebook | Question | Key idea |
|---|---|---|
| `04` Deleting is not forgetting | why do the Stage 1 tricks fail? | every point touches every weight; memorisation of atypical people |
| `05` Membership inference | how do we *detect* what is left? | loss attacks, LiRA, per-example U-LiRA |

✅ **Checkpoint :** you can run U-LiRA on a model and explain why a low average AUC can hide a high per-person risk.

---

## Stage 3 · Exact unlearning for neural nets

| Notebook | Question | Key idea |
|---|---|---|
| `06` Retrain & gold band | what exactly is the target? | a *band* over seeds, not a number |
| `07` SISA | can we make retraining cheap? | shards + slices + checkpoints; user-aware partitions; the recipe trap |

✅ **Checkpoint :** you can say what fraction of a retrain one deletion costs in SISA, and why the partition decides it.

---

## Stage 4 · Approximate unlearning

| Notebook | Question | Key idea |
|---|---|---|
| `08` Baselines & traps | can we just push the model away? | GA = Newton without curvature; 1 of 46 configs passes |
| `09` SCRUB | what if the original is the reference? | teacher-student max/min; relapse; SCRUB+R rewind |
| `10` Bad Teacher | what if we copy a model that knows nothing? | random ≠ forgotten; self-referential metrics can be gamed |

✅ **Checkpoint :** you can explain over-forgetting and why it is itself a privacy signal.

---

## Stage 5 · Proof

### 📓 `11-The-Unlearning-Audit.ipynb`
Pre-registered settings, same-recipe references, five checks (FORGET, PRIVACY, UTILITY, COST, RELEARN), three request
types, and a JSON evidence record. Random forget sets fool accuracy; the relearn attack separates removal from
suppression; even an exact method can trip a statistical test.

✅ **Checkpoint :** you can read `results/audit_carol.json` and explain every verdict in it.

---

## Stage 6 · Real-world Responsible AI

| Notebook | Data | Question |
|---|---|---|
| `12` Right to be Forgotten | UCI Adult | who pays when deletion requests are not random? |
| `13` Consent withdrawal | Olivetti faces | when a person *is* a class, what must go - and what cannot? |
| `14` Poisoned data | SMS Spam | what if we only find some of the poison? |
| `15` Fine-tuning & un-finetuning | digits as scanner "tenants" | when a customer leaves, can the architecture make deletion free? |
| `16` LLM unlearning | SMS text + a fictional directory | is refusing to say a fact the same as forgetting it? |
| `16b` *(optional)* | same, PyTorch transformer | do the conclusions survive a modern architecture? |

✅ **Checkpoint :** for each of the five, you can name the exact method, the approximate method, and the test that
told them apart.

---

## Stage 7 · Engineering

### 📓 `17-Enterprise-Unlearning-Playbook.ipynb`
Lineage registry, decision procedure, deadline/capacity planning, a re-verifiable certificate, owners for every
threshold, and an Unlearning pillar for the RAI Scorecard.

✅ **Final checkpoint :** given a model you work with, you can say how a deletion request would be served, by when, with
what evidence, and who signs it.

---

## Stage 8 · Extensions

Optional. The core course ends at Stage 7. These notebooks take the same ideas to new kinds of systems.

### 📓 `18-Recommender-Systems-Your-Taste-on-Every-Page.ipynb`
A film service on real MovieLens data, and Erin, a user with unusual taste who asks to be forgotten. Her films show up
on other people's "also watched" pages. Item-kNN forgets her exactly with a subtraction. Matrix factorisation does not
forget when you delete her account, gets close with one cheap update, and needs a retrain to be exact. Splitting users
into shards costs a lot of quality. Finally, comparing the public pages before and after the deletion shows what she
watched, and only fresh random noise on the pages stops that.

### 📓 `19-The-Method-Zoo.ipynb`
Fourteen unlearning methods, six of them new to the course (random labels, SalUn, L1-sparse, UNSIR, SSD and a
last-layer re-solve), sit Problem 11's exam on Carol, the class and the random request. Each is labelled by family:
model-agnostic, model-intrinsic or data-driven. No approximate method forgets Carol. On the random request, five new
methods seem to pass, until the privacy test is rebuilt fairly: they only made the model less sure about everything.
The results are saved as `results/leaderboard.json`.

✅ **Checkpoint :** for a recommender you know, you can say where a user's data lives, how to remove it exactly, and
what the public can learn from watching the deletion happen. And given a new unlearning paper, you can run its method
through a fixed exam, with fair reference models, before trusting its claims.

---

## 📚 Going further
- Papers for every notebook : [`resources/README.md`](resources/README.md) (with a suggested reading order)
- Test yourself : [PRACTICE.md](PRACTICE.md)
- The library behind the notebooks : `mul/` - every function is introduced in a notebook first
