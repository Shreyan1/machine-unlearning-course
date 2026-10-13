"""
How to *prove* a model forgot - the audit toolkit.

A lower accuracy on the deleted data is NOT proof. The question an auditor asks is:

    "Is the unlearned model indistinguishable from a model that never saw the data?"

So every test here compares against models retrained from scratch without D_f (the gold standard),
and - because two retrains with different seeds already differ - against the *spread* of several
such retrains, not a single one.

    utility           accuracy on D_r and on unseen test data                Problem 4
    loss_mia          can an attacker tell members from non-members?        Problem 5
    forget_mia        SCRUB-style MIA: does D_f still look like training data? Problem 5
    ulira             per-example likelihood-ratio test with IN/OUT models  Problem 5
    gold_band         mean +/- std of every metric over several retrains    Problem 6
    js_to_retrain     how far are the predictions from the gold standard?   Problem 6
    zrf               Bad-Teacher's retrain-free forgetting score            Problem 10
    relearn_test      does the knowledge come back after a little training? Problems 11, 16
    audit / gate      one table + one RAI-scorecard-style verdict            Problems 6, 11
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve

from .nn import Adam, cross_entropy
from .train import accuracy, clone, per_example_loss, predict_proba


# ---------------------------------------------------------------------------------------------
# Membership inference
# ---------------------------------------------------------------------------------------------

def proba_loss(proba, y):
    """Per-example cross-entropy from ANY model's predicted probabilities (sklearn, classical, NumPy)."""
    p = np.clip(np.asarray(proba)[np.arange(len(y)), np.asarray(y)], 1e-12, 1.0)
    return -np.log(p)


def mia_from_losses(l_in, l_out):
    """Loss-threshold MIA given per-example losses of members and non-members (model-agnostic)."""
    scores = np.concatenate([-np.asarray(l_in), -np.asarray(l_out)])
    labels = np.concatenate([np.ones(len(l_in)), np.zeros(len(l_out))])
    fpr, tpr, _ = roc_curve(labels, scores)
    return {"auc": float(roc_auc_score(labels, scores)), "tpr@5%fpr": float(np.interp(0.05, fpr, tpr)),
            "advantage": float(np.max(tpr - fpr)), "fpr": fpr, "tpr": tpr}


def loss_mia(model, X_members, y_members, X_nonmembers, y_nonmembers):
    """
    The simplest membership inference attack (Yeom et al. 2018 / Shokri et al. 2017 baseline):
    'if the model's loss on an example is low, guess it was in the training set'.

    Returns AUC (0.5 = attacker is guessing, 1.0 = attacker always right), TPR at 5% FPR
    (what auditors care about: confident hits), and the attacker's advantage (TPR - FPR, max).
    """
    l_in = per_example_loss(model, X_members, y_members)
    l_out = per_example_loss(model, X_nonmembers, y_nonmembers)
    scores = np.concatenate([-l_in, -l_out])                       # low loss -> 'member'
    labels = np.concatenate([np.ones(len(l_in)), np.zeros(len(l_out))])
    fpr, tpr, _ = roc_curve(labels, scores)
    return {
        "auc": float(roc_auc_score(labels, scores)),
        "tpr@5%fpr": float(np.interp(0.05, fpr, tpr)),
        "advantage": float(np.max(tpr - fpr)),
        "fpr": fpr, "tpr": tpr,
    }


def _features(model, X, y):
    """Per-example attack features: loss and confidence-on-true-label."""
    loss = per_example_loss(model, X, y)
    return np.c_[loss, np.exp(-loss)]


def forget_mia(model, X_retain, y_retain, X_test, y_test, X_forget, y_forget, seed=0):
    """
    The MIA used to evaluate unlearning in the SCRUB paper (and many others):

    1. train an attack classifier to separate D_r (label 1, 'seen') from D_test (label 0, 'unseen')
       using the *unlearned* model's losses;
    2. ask it about D_f.

    Returns the fraction of D_f the attacker labels 'seen'. Compare it with the same number for
    the retrained model: equal = good forgetting; much higher = still remembers; much lower =
    suspiciously over-forgotten (the 'Streisand effect').
    """
    rng = np.random.default_rng(seed)
    n = min(len(X_retain), len(X_test))
    ri = rng.choice(len(X_retain), n, replace=False)
    ti = rng.choice(len(X_test), n, replace=False)
    A = np.r_[_features(model, X_retain[ri], y_retain[ri]), _features(model, X_test[ti], y_test[ti])]
    b = np.r_[np.ones(n), np.zeros(n)]
    clf = LogisticRegression(class_weight="balanced", max_iter=1000).fit(A, b)
    return float(clf.predict(_features(model, X_forget, y_forget)).mean())


def _logit_confidence(model, X, y):
    """phi = log(p / (1 - p)) of the true label - the statistic LiRA models as a Gaussian."""
    p = predict_proba(model, X)[np.arange(len(y)), np.asarray(y)]
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def ulira(model, X_forget, y_forget, in_models, out_models):
    """
    Per-example likelihood-ratio membership test for unlearning (U-LiRA; Carlini et al. 2022,
    adapted to unlearning by Kurmanji et al. 2023 and Hayes et al. 2024).

    For EVERY forget example separately:
      * look at how confident models trained WITH it are   (in_models,  e.g. originals, new seeds)
      * look at how confident models trained WITHOUT it are (out_models, e.g. retrains, new seeds)
      * fit a Gaussian to each, and ask which one the model under test looks like.

    Returns the fraction of D_f the test judges 'still a member'.
        ~0   -> indistinguishable from a model that never saw D_f   (what we want)
        ~1   -> the model still carries D_f
    Calibrate it first: a held-out original should score ~1 and a held-out retrain ~0.

    The reference models MUST share the training recipe of the model under test (architecture,
    epochs, ensembling...). Notebook 08 shows what goes wrong otherwise.
    """
    phi_in = np.stack([_logit_confidence(m, X_forget, y_forget) for m in in_models])
    phi_out = np.stack([_logit_confidence(m, X_forget, y_forget) for m in out_models])
    v = _logit_confidence(model, X_forget, y_forget)
    from scipy.stats import norm
    l_in = norm.logpdf(v, phi_in.mean(0), phi_in.std(0) + 1e-3)
    l_out = norm.logpdf(v, phi_out.mean(0), phi_out.std(0) + 1e-3)
    return float((l_in > l_out).mean())


# ---------------------------------------------------------------------------------------------
# Distance to the gold standard
# ---------------------------------------------------------------------------------------------

def agreement_with_retrain(model, retrained_models, X):
    """Fraction of examples where `model` predicts the same class as the retrained models do."""
    pred = predict_proba(model, X).argmax(1)
    return float(np.mean([(pred == predict_proba(r, X).argmax(1)).mean() for r in retrained_models]))


def js_divergence(p, q, eps=1e-12):
    """Mean Jensen-Shannon divergence between two sets of probability vectors (0 = identical)."""
    p, q = np.clip(p, eps, 1), np.clip(q, eps, 1)
    m = 0.5 * (p + q)
    kl = lambda a, b: np.sum(a * np.log(a / b), axis=1)
    return float(np.mean(0.5 * kl(p, m) + 0.5 * kl(q, m)))


def js_to_retrain(model, retrained_models, X):
    """Average JS divergence between `model` and each retrained gold-standard model on X."""
    p = predict_proba(model, X)
    return float(np.mean([js_divergence(p, predict_proba(r, X)) for r in retrained_models]))


def retrain_noise_floor(retrained_models, X):
    """JS divergence *between* retrains with different seeds - the best any method can hope for."""
    ps = [predict_proba(r, X) for r in retrained_models]
    d = [js_divergence(ps[i], ps[j]) for i in range(len(ps)) for j in range(i + 1, len(ps))]
    return float(np.mean(d)) if d else 0.0


# ---------------------------------------------------------------------------------------------
# Relearn attack and ZRF
# ---------------------------------------------------------------------------------------------

def relearn_steps(model, X_forget, y_forget, target_acc, X_eval=None, y_eval=None, lr=1e-3,
                  batch_size=16, max_steps=500, seed=0):
    """
    The 'relearn attack' (Lynch et al. 2024; Deeb & Roger 2024): fine-tune on (part of) D_f and
    count the optimiser steps until accuracy on (X_eval, y_eval) - default D_f - reaches target_acc.

    If the knowledge was truly removed, relearning takes about as long as for a retrained model.
    If it was only *suppressed*, it snaps back in a handful of steps.
    Use X_eval = the OTHER half of D_f to test whether relearning a few examples revives the rest.
    """
    m = clone(model)
    X, y = np.asarray(X_forget, np.float32), np.asarray(y_forget)
    X_eval = X if X_eval is None else X_eval
    y_eval = y if y_eval is None else y_eval
    rng, opt = np.random.default_rng(seed), Adam(m.params, lr=lr)
    if accuracy(m, X_eval, y_eval) >= target_acc:
        return 0
    for step in range(1, max_steps + 1):
        b = rng.integers(0, len(X), min(batch_size, len(X)))
        _, g = cross_entropy(m.forward(X[b], keep_cache=True), y[b])
        opt.step(m.backward(g))
        if accuracy(m, X_eval, y_eval) >= target_acc:
            return step
    return max_steps


def relearn_test(models, X_forget, y_forget, references, original, target_frac=0.95, max_steps=500,
                 frac_of_reference=0.5, **kw):
    """
    The split-half relearn attack as an audit check.
      - fine-tune each model on the FIRST half of D_f,
      - count steps until accuracy on the SECOND half reaches target_frac x the original's,
      - compare with the same attack on models retrained without D_f (`references`).
    A model passes RELEARN if it resists for at least `frac_of_reference` x the references' median.
    Models without trainable `params` (e.g. a SISA ensemble) are reported as "n/a", and so is everyone
    when the references reach the target without any training (the test is uninformative there).
    Returns (DataFrame[steps, RELEARN], reference_steps).
    """
    h = len(X_forget) // 2
    Xa, ya, Xb, yb = X_forget[:h], y_forget[:h], X_forget[h:], y_forget[h:]
    target = target_frac * accuracy(original, Xb, yb)
    def run(m):
        if not hasattr(m, "params"):
            return np.nan
        return relearn_steps(m, Xa, ya, target, Xb, yb, max_steps=max_steps, **kw)
    ref_steps = [run(m) for m in references]
    bar = frac_of_reference * float(np.median(ref_steps)) if ref_steps else np.nan
    steps = {name: run(m) for name, m in models.items()}
    out = pd.DataFrame({"relearn_steps": steps})
    # bar == 0: the references themselves "relearn" instantly, so the test cannot tell anyone apart
    out["RELEARN"] = ["n/a" if np.isnan(v) or np.isnan(bar) or bar == 0 else ("ok" if v >= bar else "x")
                      for v in out.relearn_steps]
    return out, ref_steps


def zrf(student, incompetent_teacher, X_forget):
    """Zero Retrain Forgetting (Chundawat et al.): 1 - mean JS(student, random model) on D_f."""
    return 1.0 - js_divergence(predict_proba(student, X_forget),
                               predict_proba(incompetent_teacher, X_forget))


# ---------------------------------------------------------------------------------------------
# One table to rule them all
# ---------------------------------------------------------------------------------------------

def audit(models, splits, retrained_models, costs=None, mia=True, in_models=None):
    """
    Evaluate a dict {name: model} on the standard splits and against the gold standard.

    splits    = dict(Xr=, yr=, Xf=, yf=, Xt=, yt=)   (retain, forget, test)
    costs     = optional dict {name: samples_processed}
    in_models = optional models trained WITH D_f (other seeds) -> enables the per-example U-LiRA test
    """
    s = splits
    rows = []
    for name, m in models.items():
        row = {
            "method": name,
            "retain_acc": accuracy(m, s["Xr"], s["yr"]),
            "forget_acc": accuracy(m, s["Xf"], s["yf"]),
            "test_acc": accuracy(m, s["Xt"], s["yt"]),
        }
        if mia:
            row["forget_mia"] = forget_mia(m, s["Xr"], s["yr"], s["Xt"], s["yt"], s["Xf"], s["yf"])
        if in_models is not None:
            row["ulira"] = ulira(m, s["Xf"], s["yf"], in_models, retrained_models)
        row["agree_retrain"] = agreement_with_retrain(m, retrained_models, s["Xf"])
        row["js_to_retrain"] = js_to_retrain(m, retrained_models, s["Xf"])
        if costs and name in costs:
            row["cost"] = costs[name]
        rows.append(row)
    return pd.DataFrame(rows).set_index("method")


def gold_band(retrained_models, splits, mia=True, in_models=None):
    """
    Mean +/- std of every metric across several retrains: the target band a method should hit.
    Each retrain is scored leave-one-out (against the *other* retrains), exactly like a method is.
    """
    rows = []
    for i, m in enumerate(retrained_models):
        others = [r for j, r in enumerate(retrained_models) if j != i] or retrained_models
        rows.append(audit({f"retrain_{i}": m}, splits, others, mia=mia, in_models=in_models))
    t = pd.concat(rows)
    return t.mean(), t.std(ddof=0)


def gate(table, band_mean, band_std, k=2.0, min_halfwidth=0.03, utility_tol=0.02,
         privacy_tol=0.10, cost_ref=None):
    """
    Turn the audit table into a verdict, in the style of the book's RAI Scorecard gates:

        FORGET    forget accuracy inside the retrain band: mean +/- max(k*std, min_halfwidth)
        PRIVACY   U-LiRA member-rate no more than `privacy_tol` above the retrains'
                  (falls back to the forget-MIA band when U-LiRA was not computed)
        UTILITY   test accuracy no more than `utility_tol` below the retrain mean
        COST      cheaper than retraining (if costs are known; not applied to retrain itself)

    PASS = every check passes. Being *too* forgetful fails FORGET as well - on purpose.
    """
    def inside(v, col):
        half = max(k * band_std[col], min_halfwidth)
        return band_mean[col] - half - 1e-9 <= v <= band_mean[col] + half + 1e-9

    out = []
    for name, r in table.iterrows():
        checks = {"FORGET": inside(r["forget_acc"], "forget_acc")}
        if "ulira" in r and not np.isnan(r["ulira"]):
            checks["PRIVACY"] = r["ulira"] <= band_mean["ulira"] + max(k * band_std["ulira"], privacy_tol)
        elif "forget_mia" in r:
            checks["PRIVACY"] = inside(r["forget_mia"], "forget_mia")
        checks["UTILITY"] = r["test_acc"] >= band_mean["test_acc"] - utility_tol
        cells = {k_: ("ok" if v else "x") for k_, v in checks.items()}
        if cost_ref is not None and "cost" in r and not np.isnan(r["cost"]):
            if str(name).startswith("retrain"):
                cells["COST"] = "ref"
            else:
                checks["COST"] = r["cost"] < cost_ref
                cells["COST"] = "ok" if checks["COST"] else "x"
        verdict = "PASS" if all(checks.values()) else "FAIL"
        out.append({"method": name, **cells, "verdict": verdict})
    return pd.DataFrame(out).set_index("method")
