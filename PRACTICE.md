# 🏋️ Practice Problems

40 problems to cement what the notebooks taught. **None of them are solved here** - that is the point. Each one gives
you the task, a hint to unstick you, what to look up, and a concrete "done when" so you know whether you got it right.

| Tier | Problems | You should have finished | Roughly |
|---|---|---|---|
| 🟢 **Beginner** | B1 - B10 | Problems 0 - 5 | 30-60 min each |
| 🔵 **Amateur** | A1 - A10 | Problems 6 - 11 | 1-2 hrs each |
| 🟠 **Semi-Pro** | S1 - S12 | Problems 12 - 19 | 2-4 hrs each |
| 🔴 **Pro** | P1 - P8 | All 17 | a day to a week each |

**How to use this :**
- Work in a fresh notebook. Copying cells across defeats the purpose.
- Read the hint **only after** you are properly stuck for 15 minutes.
- Every "done when" is checkable. If you cannot check it, you have not finished it.
- Several problems are deliberately **traps** - the expected answer is that something *fails*. Those are marked ⚠️
  and they are the most valuable ones here.

---

## 🟢 Beginner

Exact unlearning for classical models, and the vocabulary of forgetting.

### B1 · Unlearn a nearest-neighbour training point
Train `classical.KNN(k=1)` on the Iris dataset, delete one training flower, and show the prediction for that flower changes only if it was its own nearest neighbour.

- **Hint:** With k=1 a training point is its own nearest neighbour. Query the deleted point before and after.
- **Look up:** `mul/classical.py → KNN.unlearn`, Problem 1
- **Done when:** You have a table of 10 deleted flowers with "prediction changed? yes/no" and one sentence explaining every "yes".

### B2 · Gaussian Naive Bayes, by hand
Fit `classical.GaussianNB` on the wine dataset, then unlearn 20 rows and compare its statistics with a model fitted without them.

- **Hint:** Compare `n`, `S1`, `S2` directly, not just predictions.
- **Look up:** Problem 1, summation form (Cao & Yang 2015)
- **Done when:** All three statistics match to floating-point precision.

### B3 · ⚠️ The empty class
Use `classical.GaussianNB` and unlearn **every** example of one class. What does the model predict for that class now?

- **Hint:** Look at what happens to the class prior when a class count reaches zero.
- **Look up:** Problem 1, `predict_log_proba`
- **Done when:** You can explain why the result is correct behaviour for "a model that never saw the class", and not a bug.

### B4 · Ridge downdate vs refit
Unlearn 50 rows from `classical.RidgeUnlearner` on the diabetes dataset one at a time, and compare with a refit.

- **Hint:** Sherman-Morrison accumulates floating-point error; measure it.
- **Look up:** Problem 2
- **Done when:** You have a plot of `max |w_downdate − w_refit|` against the number of deletions.

### B5 · Leverage predicts influence
For ridge regression, plot each training point's leverage `xᵀA⁻¹x` against how much the weights move when it is removed.

- **Hint:** Use the `leverage` method and the weight change after `unlearn`.
- **Look up:** Problem 2
- **Done when:** The scatter shows a clear positive relationship, and you can name the 3 most influential rows.

### B6 · Support vectors only
Train an SVM, remove 30 non-support vectors, retrain, and check the decision function.

- **Hint:** `ScoredSVC.support_` lists the indices that matter.
- **Look up:** Problem 3
- **Done when:** The decision function is unchanged (to solver tolerance) and you can explain why.

### B7 · Which trees saw her?
Train `classical.BaggedForest` with 50 trees and count how many trees contain a given row, for bootstrap vs sub-sampling without replacement.

- **Hint:** The bootstrap includes a row with probability ≈ 1 − 1/e.
- **Look up:** Problem 3
- **Done when:** Your measured fraction is within 2 points of 63.2% for the bootstrap.

### B8 · Memorisation score
Compute Feldman-style memorisation for 20 random digits and for Carol's 40.

- **Hint:** Train several models *with* and *without* each group; compare accuracy on the group.
- **Look up:** Problem 4, `resources/papers/08-course-additions/2020-feldman-zhang-what-nns-memorize.pdf`
- **Done when:** Carol's mean score is clearly higher, and you report both means with a standard deviation.

### B9 · A loss-threshold attack
Implement the loss-threshold membership attack yourself (no `audit.loss_mia`) and report AUC.

- **Hint:** Members have lower loss. Use `sklearn.metrics.roc_auc_score`.
- **Look up:** Problem 5, Shokri et al. 2016
- **Done when:** Your AUC matches `audit.loss_mia` to two decimals.

### B10 · ⚠️ AUC hides people
Find a model where the average attack AUC is below 0.6 but at least 5 individual examples are flagged by U-LiRA.

- **Hint:** Atypical examples. Start from the Carol lab.
- **Look up:** Problem 5, Hayes et al. 2024
- **Done when:** You can show both numbers and explain why a regulator should care about the second.

---

## 🔵 Amateur

Gold bands, SISA, approximate methods and audits.

### A1 · How many references?
Estimate the gold band for Carol with 3, 5, 10, 20 and 40 retrains.

- **Hint:** Watch the *width* of the band, not just the mean.
- **Look up:** Problem 6
- **Done when:** You have a plot of band width against number of references, and a recommendation with a reason.

### A2 · SISA cost curve
For K ∈ {1, 2, 5, 10, 20} shards, measure test accuracy and the cost of one random deletion.

- **Hint:** Reuse Problem 7's loop and report cost as % of a full retrain.
- **Look up:** Problem 7, Bourtoule et al. 2019
- **Done when:** A two-line plot shows the trade-off and you pick a K for a given accuracy budget.

### A3 · ⚠️ The recipe trap, yourself
Audit a SISA model against monolithic retrains, then against SISA retrains.

- **Hint:** U-LiRA uses IN/OUT reference models - which recipe trained them?
- **Look up:** Problem 7
- **Done when:** You can show a verdict that flips depending only on the reference recipe.

### A4 · Gradient ascent stopping rule
Find a stopping rule for gradient ascent that does *not* use the gold band, and test it on Carol.

- **Hint:** Use held-out data from the same distribution as the forget set (the SCRUB+R idea).
- **Look up:** Problems 8 and 9
- **Done when:** Your rule passes the gate on at least 2 of 5 seeds, or you can show why it cannot.

### A5 · SCRUB on the random scenario
Run SCRUB and SCRUB+R on `lab.make_lab("random")`.

- **Hint:** Where is the original model relative to the band?
- **Look up:** Problems 6, 9 and 11
- **Done when:** You explain why "doing nothing" scores well on FORGET here and what check catches it.

### A6 · A better Bad Teacher target
Replace the random teacher's outputs on the forget set with "original teacher, true class removed, renormalised".

- **Hint:** Set the true-class logit to −∞ before the softmax.
- **Look up:** Problem 10
- **Done when:** You compare PRIVACY pass rates on the class request for both targets.

### A7 · ZRF vs the gold standard
Compute ZRF for every method in Problem 11 and rank them. Compare with the gate's verdicts.

- **Hint:** `audit.zrf` needs an incompetent teacher - use one random init for all.
- **Look up:** Problem 10
- **Done when:** You show at least one pair of methods that ZRF ranks in the opposite order to the gold band.

### A8 · Relearn with a stronger attacker
Repeat Problem 11's relearn test with a learning rate 3× higher and 4× more steps.

- **Hint:** Check that the retrained references still resist.
- **Look up:** Problem 11, Deeb & Roger 2024
- **Done when:** You report which methods change verdict and whether the references moved.

### A9 · Pre-registration matters
Pick the best configuration of each method from the Problem 8-10 sweeps *using the gold band*, then re-run them on a new seed of the Carol lab.

- **Hint:** `lab.make_lab("carol", seed=1)`.
- **Look up:** Problem 11
- **Done when:** You report how many "tuned" configurations still pass on the new seed.

### A10 · Your own evidence record
Write `results/audit_<you>.json` for a request of your choice, with the same fields as Problem 11.

- **Hint:** Reuse `full_audit`.
- **Look up:** Problem 11
- **Done when:** A colleague can recompute every verdict in your file from its contents.

---

## 🟠 Semi-Pro

Real data and real obligations.

### S1 · ⚠️ Fairness after exact deletion, by race
Repeat Problem 12's wave experiment with requests skewed by race.

- **Hint:** Smaller groups move faster.
- **Look up:** Problem 12, fairlearn `MetricFrame`
- **Done when:** You plot TPR for every race group against deletions served, for exact retraining.

### S2 · Mitigation without the attribute at decision time
Restore equal opportunity after Problem 12's 60% wave *without* using sex at prediction time.

- **Hint:** Reweight the retain data, or use fairlearn's `ExponentiatedGradient`.
- **Look up:** Problem 12
- **Done when:** The TPR gap is below 0.10 and you report the accuracy cost.

### S3 · Eigenface unlearning for everyone
Unlearn each of the 40 people in turn from the eigenface system and measure the reconstruction-error rise.

- **Hint:** Reuse `EigenfaceID.unlearn`; it is cheap.
- **Look up:** Problem 13
- **Done when:** You identify who was "most memorised" and show their photos.

### S4 · ⚠️ Capability survives
Show that a face model trained on 20 people re-identifies the *other* 20 after one-shot enrolment.

- **Hint:** That is what Problem 13's re-identification probe measures.
- **Look up:** Problem 13
- **Done when:** You report re-identification accuracy for unseen identities and explain what it means for consent withdrawal.

### S5 · A two-word trigger
Poison the spam filter with a trigger made of two common words that only fire together.

- **Hint:** The suspicion score in Problem 14 looks at single words.
- **Look up:** Problem 14, Goel et al. 2024
- **Done when:** You show the single-word fix fails and propose and test a detector that works.

### S6 · Rank of a LoRA adapter
Sweep LoRA rank ∈ {1, 2, 4, 8, 16} in Problem 15 and measure accuracy and memorisation of each tenant's training forms.

- **Hint:** Memorisation = train accuracy − held-out accuracy.
- **Look up:** Problem 15, Hu et al. 2021
- **Done when:** You plot both against rank and pick one, with a privacy argument.

### S7 · NPO's β
Run NPO with β ∈ {0.1, 0.5, 1, 2, 5} in Problem 16 and record exposure, colleagues recited and relearn recovery.

- **Hint:** The weight is `2σ(β·Δ)`.
- **Look up:** Problem 16, Zhang et al. 2024
- **Done when:** A table shows the trade-off and you explain it with the formula.

### S8 · ⚠️ An output filter is not unlearning
Add a regex filter that blocks `555-01xx` after Dana's name. Run every Problem 16 test.

- **Hint:** Which tests read the model's probabilities instead of its text?
- **Look up:** Problem 16, EDPB Opinion 28/2024
- **Done when:** You list which tests pass and which fail, and write two sentences on how you would document it.

### S9 · Forget a user from item-kNN by hand
Build Problem 18's "watched together" table `G` for 50 users and 30 films with plain NumPy (no `mul`). Remove one user
by subtracting their part, then build `G` again without them.

- **Hint:** A user's part of `G` is the outer product of their 0/1 row with itself.
- **Look up:** Problem 18 Step 3, Problem 1
- **Done when:** The two tables are exactly equal, and you can say how many cells changed and why.

### S10 · ⚠️ Does deleting one user change other people's recommendations?
In Problem 18, find Erin's 20 most similar users. Compare their top-10 lists from the ALS model before and after an
exact retrain without her.

- **Hint:** Count how many of the 200 recommendations changed, then do the same for 20 random users as a baseline.
- **Look up:** Problem 18 Steps 2 and 5
- **Done when:** You show whether her "taste neighbours" see a bigger change than random users, and explain what an
  attacker who is one of her neighbours could learn.

### S11 · ⚠️ Fool the privacy test on purpose
Take the original model from Problem 19 and do nothing to Carol. Only divide all of its logits by a temperature `T`
(for example 2, 4, 8). Run the standard U-LiRA check, then the fair one from Problem 19 Step 5.

- **Hint:** Dividing logits by `T` makes the model less sure about everything, without forgetting anything.
- **Look up:** Problem 19 Step 5, Problem 5, Hayes et al. 2024
- **Done when:** You find a `T` that passes the standard check, and you show the fair check still fails it.

### S12 · Enter a fifteenth method
Pick an unlearning method from a recent paper that is not in Problem 19. Implement it in NumPy, fix its settings from
the paper *before* running it, and put it through the exam.

- **Hint:** Write the settings into `PROTOCOL` first, and do not change them after you see a result.
- **Look up:** Problem 19, Problem 11, the survey by Nguyen et al. 2022 (to label its family)
- **Done when:** Your method has a row in the leaderboard, a family label, and one honest sentence on why it passed
  or failed.

---

## 🔴 Pro

Open-ended. These are close to research or production work.

### P1 · Certified removal with noise
Implement Guo et al.'s certified removal for logistic regression (objective perturbation + a gradient-residual budget) and measure the accuracy cost of (ε, δ) guarantees.
- **Look up:** `resources/papers/01-foundations/2019-guo-certified-data-removal.pdf`, Problem 2
- **Done when:** You plot accuracy against ε and show the number of deletions served before a retrain is forced.

### P2 · DaRE forests
Implement a random forest whose split statistics are cached so deletions retrain only affected *nodes*, not trees.
- **Look up:** `resources/papers/02-exact-unlearning/2020-brophy-dare-random-forests.pdf`, Problem 3
- **Done when:** Your forest matches a from-scratch fit exactly and beats Problem 3's tree-level retraining on cost.

### P3 · SISA for a CNN
Port SISA to a small CNN (NumPy or PyTorch) on Olivetti faces with a user-aware partition.
- **Look up:** Problems 7 and 13
- **Done when:** You report accuracy and per-request cost for K ∈ {1, 5, 10} and prove exactness by hashing weights.

### P4 · An audit that catches suppression without retraining
Design a relearn-style test that needs no retrained references, and validate it against Problem 11's gold standard.
- **Look up:** Problem 11, Deeb & Roger 2024, Lynch et al. 2024
- **Done when:** Your test agrees with the full audit on at least 80% of the Problem 8-10 configurations.

### P5 · Deletion-aware fairness
Build a monitor that predicts the fairness impact of pending deletion requests *before* serving them.
- **Look up:** Problem 12
- **Done when:** On simulated request streams, your forecast of the TPR gap is within 3 points of the realised value.

### P6 · TOFU at laptop scale
Build a TOFU-style benchmark (fictitious profiles, forget/retain splits, paraphrased questions) for Problem 16's LMs.
- **Look up:** `resources/papers/05-llm-unlearning/2024-maini-tofu-benchmark.pdf`
- **Done when:** You rank GA, NPO and refusal on your benchmark and the ranking matches Problem 16's conclusions.

### P7 · Lineage for a real stack
Implement Problem 17's lineage registry on top of MLflow or DVC metadata for a project you have.
- **Look up:** Problem 17
- **Done when:** `affected(source)` returns correct artefacts for three real data sources, including one cascade.

### P8 · The Unlearning pillar, for real
Score three production models with Problem 17's rubric, propose the cheapest change for each, and estimate its cost.
- **Look up:** Problem 17, the book's RAI Scorecard chapter
- **Done when:** Each model has a score, a target score, a change and a cost, signed off by someone who owns it.
