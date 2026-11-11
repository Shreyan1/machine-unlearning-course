"""
Sanity tests for the hand-written NumPy library.

    python -m pytest tests -q        (or simply: python tests/test_mul.py)

1. Gradient checks: backprop vs finite differences, for every loss used by an unlearning method.
2. SISA exactness: unlearning == training from scratch without the point, bit for bit.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mul import methods, train  # noqa: E402
from mul.nn import MLP, cross_entropy, distill_kl  # noqa: E402


def _numeric_grad(f, P, eps=1e-3, n_checks=25, rng=None):
    """Central finite differences on a few random coordinates of parameter array P."""
    rng = rng or np.random.default_rng(0)
    out = []
    for _ in range(n_checks):
        i = tuple(rng.integers(0, s) for s in P.shape)
        old = P[i]
        P[i] = old + eps
        up = f()
        P[i] = old - eps
        down = f()
        P[i] = old
        out.append((i, (up - down) / (2 * eps)))
    return out


def _check(loss_and_grad, model, X):
    model.params = [p.astype(np.float64) for p in model.params]
    _, g = loss_and_grad(model.forward(X, keep_cache=True))
    grads = model.backward(g)
    grads = [gr.astype(np.float64) for gr in grads]
    for P, G in zip(model.params, grads):
        for idx, num in _numeric_grad(lambda: loss_and_grad(model.forward(X))[0], P):
            assert abs(num - G[idx]) < 1e-3 + 1e-2 * abs(num), (num, G[idx])


def test_cross_entropy_gradient():
    rng = np.random.default_rng(0)
    X, y = rng.normal(size=(16, 5)), rng.integers(0, 3, 16)
    _check(lambda z: cross_entropy(z, y), MLP(5, 3, (8, 8), seed=1), X)


def test_distillation_gradient():
    rng = np.random.default_rng(1)
    X = rng.normal(size=(16, 5))
    teacher = rng.normal(size=(16, 3))
    for T in (1.0, 4.0):
        _check(lambda z: distill_kl(z, teacher, T), MLP(5, 3, (8,), seed=2), X)


def test_sisa_is_exact():
    rng = np.random.default_rng(0)
    X, y = rng.normal(size=(120, 6)).astype(np.float32), rng.integers(0, 3, 120)
    fn = lambda: MLP(6, 3, (16,))
    s = methods.SISA(fn, n_shards=3, n_slices=3, epochs_per_slice=3, seed=7)
    s.fit(X, y)
    forget = [5, 17, 60]
    s.unlearn(forget)
    scratch = methods.SISA(fn, n_shards=3, n_slices=3, epochs_per_slice=3, seed=7)
    scratch.fit(X, y, partition=s.slices)            # same layout, the 3 points never present
    for a, b in zip(s.shard_models, scratch.shard_models):
        assert train.weights_equal(a, b)




# ---------------------------------------------------------------------------------------------
# Classical models: unlearning must equal refitting from scratch without the rows
# ---------------------------------------------------------------------------------------------
from mul import classical  # noqa: E402


def _toy(n=300, d=6, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    y = (X[:, 0] + 0.5 * X[:, 1] + rng.normal(scale=0.5, size=n) > 0).astype(int)
    return X, y


def test_gaussian_nb_exact():
    X, y = _toy()
    f = np.arange(0, 300, 7); r = np.setdiff1d(np.arange(300), f)
    a = classical.GaussianNB().fit(X, y).unlearn(X[f], y[f])
    b = classical.GaussianNB().fit(X[r], y[r])
    assert np.allclose(a.predict_log_proba(X), b.predict_log_proba(X), atol=1e-8)


def test_multinomial_nb_exact():
    rng = np.random.default_rng(1)
    X, y = rng.poisson(1.0, size=(200, 30)), rng.integers(0, 2, 200)
    f = np.arange(0, 200, 9); r = np.setdiff1d(np.arange(200), f)
    a = classical.MultinomialNB().fit(X, y).unlearn(X[f], y[f])
    b = classical.MultinomialNB().fit(X[r], y[r])
    assert np.allclose(a.predict_log_proba(X), b.predict_log_proba(X), atol=1e-10)


def test_ridge_exact():
    X, y = _toy()
    f = np.arange(0, 300, 11); r = np.setdiff1d(np.arange(300), f)
    a = classical.RidgeUnlearner(1.0).fit(X, y).unlearn(X[f], y[f])
    b = classical.RidgeUnlearner(1.0).fit(X[r], y[r])
    assert np.allclose(a.w, b.w, atol=1e-8)
    Y = np.eye(2)[y]                                   # multi-output version
    a = classical.RidgeUnlearner(1.0).fit(X, Y).unlearn(X[f], Y[f])
    b = classical.RidgeUnlearner(1.0).fit(X[r], Y[r])
    assert np.allclose(a.w, b.w, atol=1e-8)


def test_knn_exact():
    X, y = _toy()
    f = np.arange(0, 300, 5); r = np.setdiff1d(np.arange(300), f)
    a = classical.KNN(5).fit(X, y).unlearn(f)
    b = classical.KNN(5).fit(X[r], y[r])
    assert (a.predict(X) == b.predict(X)).all()


def test_forest_exact():
    X, y = _toy()
    f = [3, 50, 120]
    a = classical.BaggedForest(n_trees=20, seed=3).fit(X, y)
    a.unlearn(f)
    b = classical.BaggedForest(n_trees=20, seed=3).fit(X, y, bags=[bg.copy() for bg in a.bags])
    assert np.allclose(a.predict_proba(X), b.predict_proba(X))


def test_logistic_newton_close():
    X, y = _toy()
    f = np.arange(0, 300, 10); r = np.setdiff1d(np.arange(300), f)
    full = classical.LogisticNewton(1.0).fit(X, y)
    approx = full.unlearn_newton(X[r], y[r], X[f], y[f])
    exact = classical.LogisticNewton(1.0).fit(X[r], y[r])
    # approximate: the residual is second-order, so allow 15% of the distance the deletion moved w
    assert np.linalg.norm(approx.w - exact.w) < 0.15 * np.linalg.norm(full.w - exact.w) + 1e-6


def _toy3(n=300, d=6, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d))
    y = (X[:, :3] + rng.normal(scale=0.7, size=(n, 3))).argmax(1)
    return X, y


def test_softmax_newton_close():
    """SoftmaxNewton: one Newton step on D_r lands close to the retrained model, and three steps reach it."""
    X, y = _toy3()
    f = np.arange(0, 300, 10); r = np.setdiff1d(np.arange(300), f)
    full = classical.SoftmaxNewton(1.0).fit(X, y)
    exact = classical.SoftmaxNewton(1.0).fit(X[r], y[r], n_classes=3)
    gap = np.linalg.norm(full.w - exact.w)
    assert np.linalg.norm(full.unlearn_newton(X[r], y[r]).w - exact.w) < 0.15 * gap + 1e-6
    three = full.unlearn_newton(X[r], y[r], steps=3)                  # Newton converges quadratically
    assert np.linalg.norm(three.w - exact.w) < 1e-6 * gap and three.grad_norm(X[r], y[r]) < 1e-6


def test_svm_non_support_vectors_change_nothing():
    """ScoredSVC: refitting on the support vectors alone gives the same scores; deleting one support vector does not."""
    X, y = _toy3()
    kw = dict(kernel="rbf", C=10, gamma=0.2, tol=1e-6)               # fixed gamma: gamma="scale" is computed from the data
    svm = classical.ScoredSVC(**kw).fit(X, y)
    Xq = np.r_[X, np.random.default_rng(1).normal(size=(200, 6))]
    sv = svm.support_
    only_sv = classical.ScoredSVC(**kw).fit(X[sv], y[sv])
    assert len(sv) < 300 and (only_sv.predict(Xq) == svm.predict(Xq)).all()
    assert np.allclose(only_sv.predict_proba(Xq), svm.predict_proba(Xq), atol=1e-5)
    keep = np.setdiff1d(np.arange(300), sv[np.abs(svm.svc.dual_coef_).max(0).argmax()])
    assert np.abs(classical.ScoredSVC(**kw).fit(X[keep], y[keep]).predict_proba(Xq) - svm.predict_proba(Xq)).max() > 1e-2


def test_lora_gradient_and_isolation():
    """LoRA: backward matches finite differences, a fresh adapter changes nothing, the base stays frozen."""
    from mul.nn import LoRA
    rng = np.random.default_rng(0)
    base = MLP(6, 3, (5,), seed=0)
    base_before = [p.copy() for p in base.params]
    X = rng.normal(size=(8, 6))
    y = rng.integers(0, 3, 8)
    lora = LoRA(base, rank=2, seed=1)
    assert np.allclose(lora(X), base(X))                              # B = 0 -> identical to the base
    for p in lora.params[1::2]:
        p += rng.normal(scale=0.3, size=p.shape).astype(np.float32)
    _check(lambda logits: cross_entropy(logits, y), lora, X)
    train.fit(lora, X, y, epochs=3, lr=1e-2, batch_size=4)
    assert all(np.array_equal(a, b) for a, b in zip(base.params, base_before))   # base untouched
    assert np.allclose(lora.merged()(X), lora(X), atol=1e-5)          # merging is the same function


def test_itemknn_unlearning_exact():
    """Item-kNN: subtracting a user's co-watch counts == building the model without them, bit for bit."""
    from mul import recsys
    rng = np.random.default_rng(0)
    R = (rng.random((40, 30)) < 0.2).astype(float)
    m = recsys.ItemKNN().fit(R)
    m.unlearn_users([3, 17])
    R_r = R.copy()
    R_r[[3, 17]] = 0
    scratch = recsys.ItemKNN().fit(R_r)
    assert np.array_equal(m.G, scratch.G) and np.array_equal(m.similarity(), scratch.similarity())


def test_als_half_step_is_ridge():
    """ALS: one user's row is the weighted ridge solution, and a user with no films gets a zero vector."""
    from mul import recsys
    rng = np.random.default_rng(0)
    R = (rng.random((20, 15)) < 0.3).astype(float)
    R[5] = 0
    m = recsys.ImplicitALS(factors=4, reg=2.0, alpha=3.0, sweeps=3, seed=0).fit(R)
    u = 2
    C = 1 + m.alpha * R[u]                                    # confidence of every film for user u
    A = m.Y.T @ (C[:, None] * m.Y) + m.reg * np.eye(4)
    x = np.linalg.solve(A, m.Y.T @ (C * R[u]))
    assert np.allclose(m.solve(R[[u]], m.Y)[0], x)
    assert np.allclose(m.X[5], 0)


def test_input_gradient():
    """MLP.input_gradient matches finite differences on the input (UNSIR depends on it)."""
    rng = np.random.default_rng(0)
    m = MLP(5, 3, (8, 8), seed=1)
    m.params = [p.astype(np.float64) for p in m.params]
    X, y = rng.normal(size=(4, 5)), rng.integers(0, 3, 4)
    _, g = cross_entropy(m.forward(X, keep_cache=True), y)
    G = m.input_gradient(g).astype(np.float64)
    for idx, num in _numeric_grad(lambda: cross_entropy(m.forward(X), y)[0], X, n_checks=15):
        assert abs(num - G[idx]) < 1e-3 + 1e-2 * abs(num), (num, G[idx])


def test_squared_grads_and_ssd():
    """squared_grads == Σ of per-example gradients squared (explicit loop); SSD with a huge alpha changes nothing."""
    rng = np.random.default_rng(0)
    m = MLP(5, 3, (6,), seed=2)
    X, y = rng.normal(size=(7, 5)).astype(np.float32), rng.integers(0, 3, 7)
    _, g = cross_entropy(m.forward(X, keep_cache=True), y)
    fast = m.squared_grads(g * len(y))
    slow = [np.zeros_like(p) for p in m.params]
    for i in range(len(y)):
        _, gi = cross_entropy(m.forward(X[i:i + 1], keep_cache=True), y[i:i + 1])
        for s_, gr in zip(slow, m.backward(gi)):
            s_ += gr ** 2
    assert all(np.allclose(a, b, rtol=1e-4, atol=1e-6) for a, b in zip(fast, slow))
    same, _ = methods.ssd(m, X, y, X[:2], y[:2], alpha=1e12)
    assert train.weights_equal(same, m)


def test_last_layer_is_exact_on_features():
    """last_layer: the new softmax layer is exactly the convex optimum on D_r's hidden features."""
    from mul import classical
    rng = np.random.default_rng(0)
    m = MLP(6, 3, (5,), seed=3)
    X, y = rng.normal(size=(40, 6)).astype(np.float32), rng.integers(0, 3, 40)
    new, _ = methods.last_layer(m, X, y, lam=1.0)
    assert all(np.array_equal(a, b) for a, b in zip(new.params[:-2], m.params[:-2]))   # hidden layers untouched
    head = classical.SoftmaxNewton(1.0).fit(m.features(X).astype(np.float64), y, n_classes=3)
    assert np.allclose(new(X), m.features(X) @ head.w.reshape(-1, 3)[:-1] + head.w.reshape(-1, 3)[-1], atol=1e-4)
    assert np.linalg.norm(head.grad(head.w, m.features(X).astype(np.float64), y)) < 1e-6   # it is the optimum


# ---------------------------------------------------------------------------------------------
# The audit: every PASS or FAIL in the course comes from these functions
# ---------------------------------------------------------------------------------------------
from functools import lru_cache  # noqa: E402

import pandas as pd  # noqa: E402

from mul import audit  # noqa: E402


@lru_cache(maxsize=None)
def _forget_lab():
    """30 mislabelled rows (D_f) that a model can only get right by memorising them. IN models are trained with D_f
    and OUT models (the gold standard) without it, five seeds each. The fifth of each is held out as the model under test."""
    rng = np.random.default_rng(0)
    W = rng.normal(size=(10, 3))
    rule = lambda X: (X @ W).argmax(1)
    Xr, Xt, Xf = (rng.normal(size=(n, 10)).astype(np.float32) for n in (150, 300, 30))
    yf = (rule(Xf) + rng.integers(1, 3, 30)) % 3                    # always a wrong class
    s = dict(Xr=Xr, yr=rule(Xr), Xf=Xf, yf=yf, Xt=Xt, yt=rule(Xt))
    fit = lambda X, y, seed: train.fit(lambda: MLP(10, 3, (64,)), X, y, epochs=100, lr=1e-2, batch_size=32, seed=seed)
    IN = [fit(np.r_[Xr, Xf], np.r_[s["yr"], yf], k) for k in range(5)]
    OUT = [fit(Xr, s["yr"], k) for k in range(5)]
    return s, IN, OUT


_BAND = pd.Series({"forget_acc": 0.50, "test_acc": 0.90, "ulira": 0.05, "forget_mia": 0.40})


def _gate(rows, std=0.0, **kw):
    """gate() on {name: changes to a row that passes everything}, against _BAND with the same std for every metric."""
    base = {"forget_acc": 0.50, "test_acc": 0.90, "ulira": 0.05, "forget_mia": 0.40, "cost": 1.0}
    t = pd.DataFrame([{**base, **r} for r in rows.values()], index=list(rows))
    return audit.gate(t, _BAND, _BAND * 0 + std, **kw)


def test_gate_forget_band():
    """FORGET passes inside mean ± max(k·std, min_halfwidth) and fails outside it on both sides, so over-forgetting fails too."""
    g = _gate({"mean": {}, "top": {"forget_acc": 0.53}, "bottom": {"forget_acc": 0.47},
               "above": {"forget_acc": 0.54}, "below": {"forget_acc": 0.46}})          # std 0, so the half-width is 0.03
    assert list(g.FORGET) == ["ok", "ok", "ok", "x", "x"] and list(g.verdict) == ["PASS"] * 3 + ["FAIL"] * 2
    g = _gate({"a": {"forget_acc": 0.59}, "b": {"forget_acc": 0.41}, "c": {"forget_acc": 0.61},
               "d": {"forget_acc": 0.39}}, std=0.05)                                   # 2 × 0.05 = 0.10 beats 0.03
    assert list(g.FORGET) == ["ok", "ok", "x", "x"]
    assert list(_gate({"a": {"forget_acc": 0.56}}, std=0.05, k=1.0).FORGET) == ["x"]
    assert list(_gate({"a": {"forget_acc": 0.52}}, min_halfwidth=0.01).FORGET) == ["x"]


def test_gate_privacy_utility_cost():
    """PRIVACY is one-sided on U-LiRA and falls back to the forget-MIA band without it. UTILITY allows a 2-point drop.
    COST applies only with cost_ref and treats retrains as the reference. PASS needs every check."""
    g = _gate({"retrain_0": {"cost": 9.0}, "never_member": {"ulira": 0.0}, "member": {"ulira": 0.16},
               "mia_ok": {"ulira": np.nan, "forget_mia": 0.42}, "mia_high": {"ulira": np.nan, "forget_mia": 0.44},
               "small_drop": {"test_acc": 0.885}, "big_drop": {"test_acc": 0.875}, "costly": {"cost": 3.0}},
              cost_ref=2.0)
    assert list(g.PRIVACY) == ["ok", "ok", "x", "ok", "x", "ok", "ok", "ok"]
    assert list(g.UTILITY) == ["ok"] * 6 + ["x", "ok"]
    assert list(g.COST) == ["ref"] + ["ok"] * 6 + ["x"]
    assert list(g.verdict) == ["PASS", "PASS", "FAIL", "PASS", "FAIL", "PASS", "FAIL", "FAIL"]


def test_gold_band_is_leave_one_out():
    """gold_band: mean and population std of each retrain's scores, each retrain judged against the OTHER retrains."""
    s, IN, OUT = _forget_lab()
    mean, std = audit.gold_band(OUT[:4], s, mia=False)
    acc = [train.accuracy(m, s["Xf"], s["yf"]) for m in OUT[:4]]
    assert np.isclose(mean["forget_acc"], np.mean(acc)) and np.isclose(std["forget_acc"], np.std(acc))
    # judged against itself as well, a retrain would add a zero and pull the band below the noise floor
    assert mean["js_to_retrain"] > 0 and np.isclose(mean["js_to_retrain"], audit.retrain_noise_floor(OUT[:4], s["Xf"]))


def test_audit_and_gate_end_to_end():
    """The course's verdict: a held-out retrain PASSES the gate and the original model FAILS on FORGET and PRIVACY."""
    s, IN, OUT = _forget_lab()
    mean, std = audit.gold_band(OUT[:4], s, mia=False, in_models=IN[:4])
    t = audit.audit({"original": IN[4], "retrain": OUT[4]}, s, OUT[:4], mia=False, in_models=IN[:4])
    g = audit.gate(t, mean, std)
    assert list(g.verdict) == ["FAIL", "PASS"]
    assert g.loc["original", "FORGET"] == g.loc["original", "PRIVACY"] == "x"


def test_membership_tests_tell_in_from_out():
    """U-LiRA and the forget-MIA score ~1 for a held-out model trained WITH D_f and ~0 for one trained without it."""
    s, IN, OUT = _forget_lab()
    for test in (lambda m: audit.ulira(m, s["Xf"], s["yf"], IN[:4], OUT[:4]),
                 lambda m: audit.forget_mia(m, s["Xr"], s["yr"], s["Xt"], s["yt"], s["Xf"], s["yf"])):
        assert test(IN[4]) > 0.9 and test(OUT[4]) < 0.1


def test_loss_mia():
    """Loss-threshold MIA: the same losses for members and non-members give chance, separated losses a perfect attack.
    proba_loss (for any model) matches the NumPy model's own per-example loss."""
    rng = np.random.default_rng(0)
    same = audit.mia_from_losses(rng.exponential(1.0, 2000), rng.exponential(1.0, 2000))
    assert abs(same["auc"] - 0.5) < 0.03 and same["advantage"] < 0.06 and abs(same["tpr@5%fpr"] - 0.05) < 0.03
    apart = audit.mia_from_losses(rng.exponential(0.01, 200), 5 + rng.exponential(1.0, 200))
    assert apart["auc"] == apart["advantage"] == apart["tpr@5%fpr"] == 1.0
    s, IN, OUT = _forget_lab()
    loss = audit.proba_loss(train.predict_proba(IN[4], s["Xt"]), s["yt"])
    assert np.allclose(loss, train.per_example_loss(IN[4], s["Xt"], s["yt"]), atol=1e-5)
    assert audit.loss_mia(IN[4], s["Xr"], s["yr"], s["Xt"], s["yt"])["auc"] > 0.65  # it overfits D_r


def test_zrf_and_js():
    """ZRF = 1 − JS(student, incompetent teacher). It is exactly 1 for the teacher itself and matches the value worked
    out by hand for a one-hot student against a uniform teacher. JS is symmetric and below log 2."""
    s, IN, OUT = _forget_lab()
    uniform = MLP(10, 3, (8,), seed=0)
    uniform.params[-2][:] = 0; uniform.params[-1][:] = 0               # logits 0, so (1/3, 1/3, 1/3)
    onehot = uniform.copy(); onehot.params[-1][:] = [50.0, 0.0, 0.0]    # (1, 0, 0)
    assert audit.zrf(uniform, uniform, s["Xf"]) == 1.0
    js = 0.5 * np.log(1.5) + np.log(2) / 6                              # JS((1, 0, 0), uniform) by hand
    assert np.isclose(audit.zrf(onehot, uniform, s["Xf"]), 1 - js, atol=1e-6)
    p, q = train.predict_proba(IN[4], s["Xf"]), train.predict_proba(OUT[4], s["Xf"])
    assert np.isclose(audit.js_divergence(p, q), audit.js_divergence(q, p)) and 0 < audit.js_divergence(p, q) < np.log(2)


def test_relearn_steps():
    """Relearn attack: 0 steps if the model still knows D_f, the cap if the target is out of reach, the input untouched,
    and knowledge that gradient ascent only suppressed comes back far faster than a retrain can learn it."""
    s, IN, OUT = _forget_lab()
    Xf, yf = s["Xf"], s["yf"]
    before = [p.copy() for p in OUT[4].params]
    never = audit.relearn_steps(OUT[4], Xf, yf, 1.0, lr=1e-2)
    assert all(np.array_equal(a, b) for a, b in zip(before, OUT[4].params))      # it trains a copy
    suppressed, _ = methods.gradient_ascent(IN[4], Xf, yf, epochs=6, lr=1e-2)
    assert train.accuracy(suppressed, Xf, yf) < 0.5                              # looks forgotten...
    assert audit.relearn_steps(IN[4], Xf, yf, 1.0, lr=1e-2) == 0
    assert 0 < audit.relearn_steps(suppressed, Xf, yf, 1.0, lr=1e-2) < never / 3  # ...but snaps back
    assert never < 500 and audit.relearn_steps(OUT[4], Xf, yf, 1.01, max_steps=7) == 7


def test_relearn_test_verdicts():
    """relearn_test: 'ok' if a model resists at least half as long as the retrains, 'x' if it snaps back, and 'n/a' for
    a model without weights, or for everyone when the references reach the target with no training at all."""
    s, IN, OUT = _forget_lab()
    models = {"original": IN[4], "retrain": OUT[4], "ensemble": object()}
    t, ref = audit.relearn_test(models, s["Xf"], s["yf"], OUT[:4], IN[4], max_steps=20)
    assert ref == [20] * 4 and list(t.RELEARN) == ["x", "ok", "n/a"]
    t, ref = audit.relearn_test(models, s["Xf"], s["yf"], IN[:4], IN[4], max_steps=20)
    assert ref == [0] * 4 and list(t.RELEARN) == ["n/a"] * 3


# ---------------------------------------------------------------------------------------------
# Language models: the n-gram table is a sum, so unlearning a line is exact
# ---------------------------------------------------------------------------------------------
from mul import lm  # noqa: E402


def _directory():
    """A tiny phone directory. Dana's number is the only one whose last two digits are above 39."""
    rng = np.random.default_rng(0)
    names = ["Arun", "Bela", "Chen", "Eve", "Farah", "Gopal", "Hana", "Ivan", "Jaya", "Kofi", "Lena"]
    others = [f"{n} 555-01{k:02d}\n" for n, k in zip(names, rng.choice(40, len(names), replace=False))]
    generic = ["the cat sat on the mat\n", "a dog ran in the park\n", "call me later\n"]
    return "Dana 555-0187\n", others, generic


def test_ngram_unlearning_is_exact():
    """NGramLM.unlearn: the table, the next-character distributions and the log-probabilities are bit for bit those of
    a model that never saw the line, whatever order it was trained in."""
    dana, others, generic = _directory()
    unlearned = lm.NGramLM(order=12).fit(generic + [dana] + others * 3 + [dana] * 2).unlearn([dana] * 3)
    never = lm.NGramLM(order=12).fit(generic + others * 3)
    assert unlearned.table_equal(never) and all(v > 0 for c in unlearned.counts.values() for v in c.values())
    for ctx in ["", "Dana ", "Dana 555-01", "555-01", "Arun 555-0", "the "]:
        assert unlearned.next_distribution(ctx) == never.next_distribution(ctx)
    assert unlearned.complete("Dana ", 12) == never.complete("Dana ", 12) != "555-0187"
    assert unlearned.seq_logprob("Dana ", "555-0187") == never.seq_logprob("Dana ", "555-0187")


def test_exposure():
    """exposure: a memorised number is the model's top guess (rank 1, log2 N bits). After exact unlearning it ranks
    among the other candidates, with the same exposure as in a model that never saw it."""
    dana, others, generic = _directory()
    cands = [f"555-01{i:02d}" for i in range(100)]
    model = lm.NGramLM(order=12).fit(generic + others * 3 + [dana] * 3)
    never = lm.NGramLM(order=12).fit(generic + others * 3)
    e_mem, rank_mem = lm.exposure(model.seq_logprob, "Dana ", "555-0187", cands)
    e_un, rank_un = lm.exposure(model.unlearn([dana] * 3).seq_logprob, "Dana ", "555-0187", cands)
    assert rank_mem == 1 and np.isclose(e_mem, np.log2(100))
    assert (e_un, rank_un) == lm.exposure(never.seq_logprob, "Dana ", "555-0187", cands)
    assert rank_un > 10 and e_un < e_mem - 3


def test_exposure_counts_ties_against_the_secret():
    """exposure: candidates that tie with the secret rank ahead of it (Carlini et al. 2019), so a model that
    scores every candidate the same shows zero exposure, not the maximum."""
    cands = [f"555-01{i:02d}" for i in range(100)]
    e_flat, rank_flat = lm.exposure(lambda prompt, c: -5.0, "Dana ", "555-0187", cands)
    assert rank_flat == 100 and e_flat == 0.0
    # Two candidates share the top score with the secret: the secret ranks third.
    top = {"555-0187", "555-0101", "555-0102"}
    e_tie, rank_tie = lm.exposure(lambda prompt, c: 0.0 if c in top else -9.0, "Dana ", "555-0187", cands)
    assert rank_tie == 3 and np.isclose(e_tie, np.log2(100) - np.log2(3))


def test_scored_svc_two_classes():
    """ScoredSVC.predict_proba works for two classes, where sklearn returns a single decision score."""
    rng = np.random.default_rng(0)
    X = np.r_[rng.normal(-1, 1, (40, 2)), rng.normal(1, 1, (40, 2))]
    y = np.r_[np.zeros(40, int), np.ones(40, int)]
    svc = classical.ScoredSVC(kernel="rbf", C=1.0, gamma=0.5).fit(X, y)
    p = svc.predict_proba(X)
    d = svc.svc.decision_function(X)
    assert p.shape == (80, 2) and np.allclose(p.sum(1), 1)
    assert np.allclose(p[:, 1], 1 / (1 + np.exp(-d)))
    assert np.array_equal(svc.svc.classes_[p.argmax(1)], svc.predict(X))



# ---------------------------------------------------------------------------------------------
# RAG: deleting from a retrieval stack is exact, once every store is cleaned and compacted
# ---------------------------------------------------------------------------------------------
from mul import rag  # noqa: E402


def _rag_stack(rows):
    return rag.RAGStack(rag.HashEmbedder(500), cache_threshold=0.8).add_tickets(rows)


def test_rag_delete_then_compact_equals_build_without():
    """forget(owner) + compact() leaves every store exactly as a stack built without that owner, even after a
    rewritten ticket is indexed again out of order."""
    rows = rag.make_tickets(n_customers=12, seed=1)
    stack = _rag_stack(rows)
    for r in rows[:8]:
        stack.ask(r["owner"], f"{r['first']} {r['product']} order {r['order']}")
    stack.forget("C-FIONA")
    neighbour = next(r for r in rows if "neighbour" in r["text"])
    stack.redact(neighbour["ticket"], "fiona kowalczyk at 14 larch row", "[removed]")
    stack.compact()
    kept = [dict(r) for r in rows if r["owner"] != "C-FIONA"]
    for r in kept:
        r["text"] = r["text"].replace("fiona kowalczyk at 14 larch row", "[removed]")
    never = _rag_stack(kept)
    assert stack.vectors.same_as(never.vectors) and stack.keywords.same_as(never.keywords)
    assert stack.tickets == never.tickets and stack.chunks == never.chunks
    for q in ["fiona kowalczyk phone", "14 larch row", "kettle arrived broken", "refund the second payment"]:
        assert stack.retrieve(q) == never.retrieve(q)
    assert set(stack.scan(["kowalczyk", "larch row"]).values()) == {0}


def test_rag_tombstones_hide_but_keep():
    """A tombstone hides a chunk from search, but the row stays in snapshots and in the keyword statistics
    until compact()."""
    rows = rag.make_tickets(n_customers=12, seed=1)
    stack = _rag_stack(rows)
    fiona = {c for c, v in stack.chunks.items() if v["owner"] == "C-FIONA"}
    df = stack.keywords.df("kowalczyk")
    others = sum("kowalczyk" in v["text"] for c, v in stack.chunks.items() if c not in fiona)   # the neighbour
    stack.forget("C-FIONA")
    for q in ["fiona kowalczyk tel 555-0147", "air fryer hospital", "card ending 7731"]:
        assert not fiona & set(stack.retrieve(q, k=20))
    snap = stack.vectors.snapshot()
    assert fiona <= set(snap["ids"]) and (~snap["alive"]).sum() == len(fiona)
    assert stack.keywords.df("kowalczyk") == df and stack.copies("C-FIONA")["vector index"] == len(fiona)
    stack.compact()
    assert not fiona & set(stack.vectors.snapshot()["ids"]) and stack.keywords.df("kowalczyk") == others < df
    assert stack.copies("C-FIONA") == dict.fromkeys(stack.copies("C-FIONA"), 0)


def test_rag_cache_invalidation():
    """A paraphrase is served from the cache. forget() drops every cache entry and log record built from the
    owner's chunks, and record=False leaves no trace."""
    stack = _rag_stack(rag.make_tickets(n_customers=12, seed=1))
    first = stack.ask("agent-1", "fiona kowalczyk phone number")
    assert "555-0147" in first and len(stack.cache.entries) == len(stack.logs) == 1
    assert stack.ask("someone", "phone number for fiona kowalczyk please", record=False) == first
    assert stack.last_from_cache and len(stack.cache.entries) == len(stack.logs) == 1
    removed = stack.forget("C-FIONA")
    assert removed["answer cache"] == 1 and removed["logs"] == 1 and not stack.cache.entries and not stack.logs
    assert "555-0147" not in stack.ask("someone", "phone number for fiona kowalczyk please", record=False)
    assert not stack.last_from_cache


def test_hash_embedding_inversion():
    """invert() reads the words of a short text back out of its hashed embedding, given a word list."""
    emb = rag.HashEmbedder(4000)
    text = "fiona kowalczyk is in hospital at 14 larch row"
    words = set(rag.tokens(text))
    candidates = sorted(words | set(rag.FIRST_NAMES) | set(rag.SURNAMES) | set(rag.PRODUCTS))
    assert set(rag.invert(emb, emb([text])[0], candidates)) == words


def test_ivf_centroids_keep_removed_rows():
    """IVFIndex.remove() leaves the trained centroids untouched; fitting again gives the index built without the
    rows, whatever order the rows come in."""
    rng = np.random.default_rng(0)
    V = rng.normal(size=(60, 8))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    ids = [f"c{i:02d}" for i in range(60)]
    ivf = rag.IVFIndex(n_lists=4, seed=0).fit(ids, V)
    before = ivf.centroids.copy()
    ivf.remove(ids[:10])
    assert np.array_equal(ivf.centroids, before) and not set(ids[:10]) & set(ivf.ids)
    rev = rag.IVFIndex(n_lists=4, seed=0).fit(ids[10:][::-1], V[10:][::-1])
    assert np.array_equal(rev.centroids, rag.IVFIndex(n_lists=4, seed=0).fit(ids[10:], V[10:]).centroids)
    assert not np.array_equal(rev.centroids, before)


# ---------------------------------------------------------------------------------------------
# Surgical weight editing (Problem 22)
# ---------------------------------------------------------------------------------------------

from mul import edit  # noqa: E402


def _small_lm(seed=0):
    m = MLP(6, 5, (8,), seed=seed)
    m.params = [p + np.float32(0.1) * np.random.default_rng(seed + 1).normal(size=p.shape).astype(np.float32)
                for p in m.params]
    return m


def test_blind_to_removes_the_direction():
    """After blind_to, moving the hidden state along a removed direction no longer changes the logits, and with
    `neurons` only those rows of the last layer change."""
    m = _small_lm()
    d = np.random.default_rng(3).normal(size=8)
    W = edit.blind_to(m, d).params[-2]
    assert np.allclose((d / np.linalg.norm(d)) @ W, 0.0, atol=1e-5)
    two = np.random.default_rng(4).normal(size=(2, 8))
    W2 = edit.blind_to(m, two).params[-2]
    assert np.allclose(two @ W2, 0.0, atol=1e-5)
    part = edit.blind_to(m, d, neurons=[1, 5])
    changed_rows = np.where((part.params[-2] != m.params[-2]).any(1))[0]
    assert set(changed_rows) <= {1, 5} and all(np.array_equal(a, b) for a, b in zip(part.params[:-2], m.params[:-2]))


def test_switch_off_and_changed():
    m = _small_lm()
    off = edit.switch_off(m, [0, 3])
    assert not off.params[-2][[0, 3]].any() and np.array_equal(off.params[-2][1], m.params[-2][1])
    n, share = edit.changed(off, m)
    assert n == int((m.params[-2][[0, 3]] != 0).sum()) and np.isclose(share, n / m.n_params())


def test_neuron_scores_match_finite_differences():
    """neuron_scores = activation x d log p(y) / d activation, checked against finite differences on the hidden layer."""
    m = _small_lm()
    X, y = np.random.default_rng(5).normal(size=(1, 6)).astype(np.float32), np.array([2])
    h = m.features(X).astype(np.float64)[0]
    W, b = m.params[-2].astype(np.float64), m.params[-1].astype(np.float64)
    logp = lambda hh: (hh @ W + b)[2] - np.log(np.exp(hh @ W + b).sum())
    eps, num = 1e-5, np.zeros(8)
    for j in range(8):
        e = np.zeros(8); e[j] = eps
        num[j] = h[j] * (logp(h + e) - logp(h - e)) / (2 * eps)
    assert np.allclose(edit.neuron_scores(m, X, y), num, atol=1e-4)


def test_rewrite_memory_hits_its_targets():
    """The keys get exactly the target outputs (in the chosen columns), the other columns and layers do not move,
    and keys that were not edited change less than the edited ones."""
    m = _small_lm()
    rng = np.random.default_rng(6)
    X_text = rng.normal(size=(400, 6)).astype(np.float32)
    X_keys = rng.normal(size=(2, 6)).astype(np.float32)
    target = m(X_keys).astype(np.float64)
    target[:, [1, 3]] += 2.0
    C = edit.key_covariance(m, X_text)
    out = edit.rewrite_memory(m, X_keys, target, C, lam=1e-6, columns=[1, 3])
    assert np.allclose(out(X_keys), target, atol=1e-3)
    assert np.array_equal(out.params[-2][:, [0, 2, 4]], m.params[-2][:, [0, 2, 4]])
    assert all(np.array_equal(a, b) for a, b in zip(out.params[:-2], m.params[:-2]))
    moved = np.abs(out(X_text) - m(X_text))[:, [1, 3]].mean()
    assert moved < 2.0


def test_refit_last_layer_keeps_the_hidden_layer():
    m = _small_lm()
    rng = np.random.default_rng(7)
    X, y = rng.normal(size=(200, 6)).astype(np.float32), rng.integers(0, 5, 200)
    r = edit.refit_last_layer(m, X, y, epochs=3)
    assert all(np.array_equal(a, b) for a, b in zip(r.params[:-2], m.params[:-2]))
    assert r.params[-2].shape == m.params[-2].shape and not np.array_equal(r.params[-2], m.params[-2])


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok ", name)
    print("all checks passed")

