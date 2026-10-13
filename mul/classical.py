"""
Unlearning for classical machine learning - where forgetting can be EXACT and nearly free.

    KNN               lazy learner: the model IS the data -> delete the row, done          notebook 01
    GaussianNB        summation form: model = counts & sums -> subtract the point          notebook 01
    MultinomialNB     same idea for word counts (spam filters)                             notebooks 01, 14
    RidgeUnlearner    closed form: Sherman-Morrison rank-one downdate, exact              notebook 02
    LogisticNewton    no closed form: one Newton step = influence-function removal        notebook 02
    BaggedForest      retrain only the trees whose bag contained the point (exact)        notebook 03

The insight running through all of them (Cao & Yang, IEEE S&P 2015): if a model can be written
as a function of *sums over the training data*, then removing a point is a subtraction. Deep
networks cannot be written that way - which is why the rest of this course exists.
"""

import time

import numpy as np
from scipy.special import expit

F64 = np.float64


# ---------------------------------------------------------------------------------------------
# k-nearest neighbours
# ---------------------------------------------------------------------------------------------

class KNN:
    """k-NN classifier. 'Training' = storing the data. Unlearning = deleting rows. Exact, O(1)."""

    def __init__(self, k=5):
        self.k = k

    def fit(self, X, y):
        self.X, self.y = np.asarray(X, F64), np.asarray(y)
        self.alive = np.ones(len(self.X), bool)          # a 'tombstone' per row
        self.n_classes = int(self.y.max()) + 1
        return self

    def unlearn(self, idx):
        self.alive[np.asarray(idx)] = False              # that is the entire algorithm
        return self

    def predict_proba(self, X):
        Xa, ya = self.X[self.alive], self.y[self.alive]
        d = ((np.asarray(X, F64)[:, None, :] - Xa[None, :, :]) ** 2).sum(-1)
        nn = np.argsort(d, axis=1)[:, : self.k]
        P = np.zeros((len(X), self.n_classes))
        for c in range(self.n_classes):
            P[:, c] = (ya[nn] == c).mean(1)
        return P

    def predict(self, X):
        return self.predict_proba(X).argmax(1)

    def neighbours(self, X):
        """Original row indices of the k nearest *alive* neighbours of each x."""
        alive_idx = np.where(self.alive)[0]
        d = ((np.asarray(X, F64)[:, None, :] - self.X[alive_idx][None]) ** 2).sum(-1)
        return alive_idx[np.argsort(d, axis=1)[:, : self.k]]


# ---------------------------------------------------------------------------------------------
# Naive Bayes - the textbook 'summation form' model
# ---------------------------------------------------------------------------------------------

class GaussianNB:
    """
    Gaussian Naive Bayes stored as sufficient statistics per class:
        n_c,   S1_c = Σ x,   S2_c = Σ x²
    mean = S1/n,  var = S2/n - mean².  Unlearning a point = subtracting it from the three sums.
    The result is identical (to floating-point precision) to refitting from scratch.
    """

    def __init__(self, var_smoothing=1e-2):
        self.var_smoothing = var_smoothing

    def fit(self, X, y, n_classes=None):
        X, y = np.asarray(X, F64), np.asarray(y)
        C = n_classes or int(y.max()) + 1
        self.n = np.array([(y == c).sum() for c in range(C)], F64)
        self.S1 = np.stack([X[y == c].sum(0) for c in range(C)])
        self.S2 = np.stack([(X[y == c] ** 2).sum(0) for c in range(C)])
        return self

    def unlearn(self, X_del, y_del):
        X_del, y_del = np.atleast_2d(np.asarray(X_del, F64)), np.atleast_1d(y_del)
        for x, c in zip(X_del, y_del):
            self.n[c] -= 1
            self.S1[c] -= x
            self.S2[c] -= x ** 2
        return self

    def _params(self):
        n = np.maximum(self.n, 1)[:, None]
        mu = self.S1 / n
        var = np.maximum(self.S2 / n - mu ** 2, 0) + self.var_smoothing
        prior = np.log(np.maximum(self.n, 1e-12) / self.n.sum())
        return mu, var, prior

    def predict_log_proba(self, X):
        mu, var, prior = self._params()
        X = np.asarray(X, F64)
        ll = -0.5 * (((X[:, None, :] - mu[None]) ** 2) / var[None] + np.log(2 * np.pi * var[None])).sum(-1)
        ll = ll + prior[None]
        ll[:, self.n == 0] = -np.inf                     # a class with no data cannot be predicted
        return ll - np.logaddexp.reduce(ll, axis=1, keepdims=True)

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        return self.predict_log_proba(X).argmax(1)


class MultinomialNB:
    """
    Multinomial Naive Bayes for word counts (the classic spam filter).
    Model = word counts per class + document counts per class. Unlearning = subtract them.
    """

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y, n_classes=2):
        X, y = np.asarray(X, F64), np.asarray(y)
        self.doc_count = np.array([(y == c).sum() for c in range(n_classes)], F64)
        self.word_count = np.stack([X[y == c].sum(0) for c in range(n_classes)])
        return self

    def unlearn(self, X_del, y_del):
        X_del, y_del = np.atleast_2d(np.asarray(X_del, F64)), np.atleast_1d(y_del)
        for x, c in zip(X_del, y_del):
            self.doc_count[c] -= 1
            self.word_count[c] -= x
        return self

    def predict_log_proba(self, X):
        wc = self.word_count + self.alpha
        log_theta = np.log(wc / wc.sum(1, keepdims=True))
        prior = np.log(self.doc_count / self.doc_count.sum())
        ll = np.asarray(X, F64) @ log_theta.T + prior
        return ll - np.logaddexp.reduce(ll, axis=1, keepdims=True)

    def predict_proba(self, X):
        return np.exp(self.predict_log_proba(X))

    def predict(self, X):
        return self.predict_log_proba(X).argmax(1)


# ---------------------------------------------------------------------------------------------
# Ridge regression - exact unlearning by a rank-one downdate
# ---------------------------------------------------------------------------------------------

class RidgeUnlearner:
    """
    Ridge regression  w = (XᵀX + λI)⁻¹ Xᵀy   (bias handled by an appended column of ones).

    We keep A⁻¹ = (XᵀX + λI)⁻¹ and b = Xᵀy. Removing one example (x, y):
        A_new = A - x xᵀ          ->   Sherman-Morrison:
        A_new⁻¹ = A⁻¹ + (A⁻¹ x xᵀ A⁻¹) / (1 - xᵀ A⁻¹ x)
        b_new   = b - x y
    O(d²) per deletion instead of O(n d² + d³) for a refit. Exact up to floating point.
    Works for multi-output targets too (e.g. one-hot classes).
    """

    def __init__(self, lam=1.0):
        self.lam = lam

    @staticmethod
    def _aug(X):
        X = np.atleast_2d(np.asarray(X, F64))
        return np.c_[X, np.ones(len(X))]

    def fit(self, X, Y):
        Xa = self._aug(X)
        Y = np.asarray(Y, F64)
        self.A_inv = np.linalg.inv(Xa.T @ Xa + self.lam * np.eye(Xa.shape[1]))
        self.b = Xa.T @ Y
        return self

    @property
    def w(self):
        return self.A_inv @ self.b

    def unlearn(self, X_del, Y_del):
        Xa = self._aug(X_del)
        Y_del = np.asarray(Y_del, F64).reshape(len(Xa), *np.shape(self.b)[1:])
        for x, yv in zip(Xa, Y_del):
            Ax = self.A_inv @ x
            self.A_inv = self.A_inv + np.outer(Ax, Ax) / (1.0 - x @ Ax)
            self.b = self.b - np.outer(x, yv).reshape(self.b.shape) if self.b.ndim > 1 else self.b - x * yv
        return self

    def leverage(self, X):
        """h = xᵀA⁻¹x : how much the fit depends on x (high leverage = memorised, outlier-ish)."""
        Xa = self._aug(X)
        return np.einsum("ij,jk,ik->i", Xa, self.A_inv, Xa)

    def predict(self, X):
        return self._aug(X) @ self.w


# ---------------------------------------------------------------------------------------------
# Logistic regression - approximate unlearning with one Newton step
# ---------------------------------------------------------------------------------------------

class LogisticNewton:
    """
    L2-regularised binary logistic regression, trained to optimality by Newton's method.

    Objective:  L(w) = Σᵢ log(1 + exp(-ỹᵢ wᵀxᵢ)) + (λ/2)‖w‖²       (ỹ ∈ {-1, +1})

    There is no closed-form 'subtract the point'. The classic approximate fix (influence
    functions; Koh & Liang 2017; Guo et al. 2019 'certified removal') is ONE Newton step from the
    current optimum on the objective WITHOUT the deleted points:
        w_new = w + H_r⁻¹ · Σ_{deleted} ∇ℓ(xᵢ, yᵢ; w)
    where H_r is the Hessian of the retain objective at w. For a strongly convex loss this lands
    very close to the true retrained optimum; Guo et al. add calibrated noise at training time to
    turn 'very close' into a formal (ε, δ) guarantee.
    """

    def __init__(self, lam=1.0, max_iter=50, tol=1e-10):
        self.lam, self.max_iter, self.tol = lam, max_iter, tol

    @staticmethod
    def _aug(X):
        X = np.atleast_2d(np.asarray(X, F64))
        return np.c_[X, np.ones(len(X))]

    def _grad_hess(self, w, Xa, s):
        z = s * (Xa @ w)
        p = expit(-z)                                    # = σ(-ỹ wᵀx)
        g = -(Xa * (s * p)[:, None]).sum(0) + self.lam * w
        d = p * (1 - p)
        H = (Xa * d[:, None]).T @ Xa + self.lam * np.eye(len(w))
        return g, H

    def fit(self, X, y, w0=None):
        t0 = time.perf_counter()
        Xa, s = self._aug(X), 2.0 * np.asarray(y, F64) - 1.0
        w = np.zeros(Xa.shape[1]) if w0 is None else w0.copy()
        for self.n_iter in range(1, self.max_iter + 1):
            g, H = self._grad_hess(w, Xa, s)
            step = np.linalg.solve(H, g)
            w -= step
            if np.abs(step).max() < self.tol:
                break
        self.w, self.fit_seconds = w, time.perf_counter() - t0
        return self

    def per_example_grad(self, X, y):
        Xa, s = self._aug(X), 2.0 * np.asarray(y, F64) - 1.0
        p = expit(-s * (Xa @ self.w))
        return -(Xa * (s * p)[:, None])

    def unlearn_newton(self, X_retain, y_retain, X_del, y_del):
        """One Newton step towards the optimum of the retain-only objective."""
        t0 = time.perf_counter()
        Xa, s = self._aug(X_retain), 2.0 * np.asarray(y_retain, F64) - 1.0
        g_r, H_r = self._grad_hess(self.w, Xa, s)        # g_r = -Σ_del ∇ℓ at the old optimum
        new = LogisticNewton(self.lam)
        new.w = self.w - np.linalg.solve(H_r, g_r)
        new.unlearn_seconds = time.perf_counter() - t0
        return new

    def predict_proba(self, X):
        p1 = expit(self._aug(X) @ self.w)
        return np.c_[1 - p1, p1]

    def predict(self, X):
        return (self._aug(X) @ self.w > 0).astype(int)


class SoftmaxNewton:
    """
    Multinomial (softmax) logistic regression with L2, solved exactly by Newton's method.
    Same idea as LogisticNewton, for K classes - so it runs on the 10-digit lab.

        L(W) = Σᵢ CE(softmax(Wᵀxᵢ), yᵢ) + (λ/2)‖W‖²          W has shape (d+1, K)

    Unlearning (influence / Newton removal):
        w_new = w − H_r⁻¹ ∇L_r(w)      with H_r, ∇L_r computed on D_r only, at the old optimum.
    At the old optimum ∇L(w) = 0, so ∇L_r(w) = −Σ_{deleted} ∇ℓᵢ(w): the step literally adds back
    the deleted points' gradients, re-weighted by the curvature of what remains.
    """

    def __init__(self, lam=1.0, max_iter=30, tol=1e-8):
        self.lam, self.max_iter, self.tol = lam, max_iter, tol

    _aug = staticmethod(LogisticNewton._aug)

    def _probs(self, w, Xa):
        Z = Xa @ w.reshape(Xa.shape[1], self.K)
        Z -= Z.max(1, keepdims=True)
        P = np.exp(Z)
        return P / P.sum(1, keepdims=True)

    def grad(self, w, X, y):
        Xa = self._aug(X)
        P = self._probs(w, Xa)
        P[np.arange(len(y)), y] -= 1.0
        return (Xa.T @ P).ravel() + self.lam * w

    def hessian(self, w, X):
        Xa = self._aug(X)
        P = self._probs(w, Xa)
        d1, K = Xa.shape[1], self.K
        H = np.zeros((d1 * K, d1 * K))
        for a in range(K):
            for b in range(a, K):
                wgt = P[:, a] * ((a == b) - P[:, b])
                blk = (Xa * wgt[:, None]).T @ Xa
                H[a::K, b::K] = blk                   # parameters are ordered (feature, class)
                H[b::K, a::K] = blk.T
        return H + self.lam * np.eye(d1 * K)

    def fit(self, X, y, n_classes=None, w0=None):
        t0 = time.perf_counter()
        y = np.asarray(y)
        self.K = n_classes or int(y.max()) + 1
        d1 = np.asarray(X).shape[1] + 1
        w = np.zeros(d1 * self.K) if w0 is None else w0.copy()
        for self.n_iter in range(1, self.max_iter + 1):
            step = np.linalg.solve(self.hessian(w, X), self.grad(w, X, y))
            w -= step
            if np.abs(step).max() < self.tol:
                break
        self.w, self.fit_seconds = w, time.perf_counter() - t0
        return self

    def unlearn_newton(self, X_retain, y_retain, steps=1):
        """`steps` Newton steps on the retain-only objective, starting from the current weights."""
        t0 = time.perf_counter()
        new = SoftmaxNewton(self.lam)
        new.K, w = self.K, self.w.copy()
        for _ in range(steps):
            w = w - np.linalg.solve(self.hessian(w, X_retain), self.grad(w, X_retain, np.asarray(y_retain)))
        new.w, new.unlearn_seconds = w, time.perf_counter() - t0
        return new

    def grad_norm(self, X, y):
        """‖∇L(w)‖ on (X, y). Zero exactly at the optimum - Guo et al.'s certificate quantity."""
        return float(np.linalg.norm(self.grad(self.w, X, np.asarray(y))))

    def predict_proba(self, X):
        return self._probs(self.w, self._aug(X))

    def predict(self, X):
        return self.predict_proba(X).argmax(1)


# ---------------------------------------------------------------------------------------------
# Random forest with explicit bags - retrain only the affected trees
# ---------------------------------------------------------------------------------------------

class BaggedForest:
    """
    A random forest where we remember which rows each tree was trained on.

    To unlearn a row, retrain ONLY the trees whose bag contained it, with the same random seed
    and the same bag minus that row. Untouched trees are identical to a from-scratch fit, so the
    whole forest is exactly what you would get by training without the row.

    `bag_fraction` controls the trade-off you met in SISA: with classic bootstrap bags
    (bag_fraction=1.0, with replacement) about 63% of trees contain any given row, so deleting
    one row retrains most of the forest. With small sub-sampled bags, few trees are affected.
    """

    def __init__(self, n_trees=50, bag_fraction=1.0, replace=True, max_features="sqrt",
                 min_samples_leaf=1, seed=0):
        self.n_trees, self.bag_fraction, self.replace = n_trees, bag_fraction, replace
        self.max_features, self.min_samples_leaf, self.seed = max_features, min_samples_leaf, seed

    def _tree(self, t):
        from sklearn.tree import DecisionTreeClassifier
        return DecisionTreeClassifier(max_features=self.max_features, min_samples_leaf=self.min_samples_leaf,
                                      random_state=self.seed * 10_000 + t)

    def fit(self, X, y, bags=None):
        t0 = time.perf_counter()
        self.X, self.y = np.asarray(X), np.asarray(y)
        self.classes = np.unique(self.y)
        rng = np.random.default_rng(self.seed)
        m = max(1, int(self.bag_fraction * len(self.X)))
        self.bags = bags if bags is not None else [rng.choice(len(self.X), m, replace=self.replace)
                                                    for _ in range(self.n_trees)]
        self.trees = [self._tree(t).fit(self.X[b], self.y[b]) for t, b in enumerate(self.bags)]
        self.fit_seconds = time.perf_counter() - t0
        return self

    def unlearn(self, idx):
        t0 = time.perf_counter()
        idx = np.asarray(idx)
        affected = [t for t, b in enumerate(self.bags) if np.isin(b, idx).any()]
        for t in affected:
            self.bags[t] = self.bags[t][~np.isin(self.bags[t], idx)]
            self.trees[t] = self._tree(t).fit(self.X[self.bags[t]], self.y[self.bags[t]])
        return {"trees_retrained": len(affected), "of": self.n_trees,
                "seconds": time.perf_counter() - t0}

    def predict_proba(self, X):
        P = np.zeros((len(X), len(self.classes)))
        for tr in self.trees:
            P[:, np.searchsorted(self.classes, tr.classes_)] += tr.predict_proba(X)
        return P / len(self.trees)

    def predict(self, X):
        return self.classes[self.predict_proba(X).argmax(1)]


# ---------------------------------------------------------------------------------------------
# SVM with confidence scores (for membership inference)
# ---------------------------------------------------------------------------------------------

class ScoredSVC:
    """
    sklearn's SVC with predict_proba = softmax of the one-vs-rest decision values.

    These are *uncalibrated* confidences - exactly what an attacker who sees the model's raw
    scores would use. (Calibrating them on held-out data, as SVC(probability=True) or
    CalibratedClassifierCV do, deliberately hides over-confidence - a privacy defence in itself.)
    """

    def __init__(self, **svc_kwargs):
        from sklearn.svm import SVC
        self.svc = SVC(decision_function_shape="ovr", **svc_kwargs)

    def fit(self, X, y):
        self.svc.fit(X, y)
        self.support_ = self.svc.support_
        return self

    def predict(self, X):
        return self.svc.predict(X)

    def predict_proba(self, X):
        d = self.svc.decision_function(X)
        d = d - d.max(1, keepdims=True)
        e = np.exp(d)
        return e / e.sum(1, keepdims=True)
