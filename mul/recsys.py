"""
Recommender systems and how to unlearn a user from them (Problem 18).

    implicit_split   who-watched-what matrix, with some of every user's films held out for testing
    ItemKNN          "people who watched X also watched Y": cosine over co-watch counts. The counts are a
                     SUM over users -> unlearning a user is a subtraction, bit-for-bit exact (Problem 1)
    ImplicitALS      matrix factorisation for implicit feedback (Hu, Koren & Volinsky 2008). Each half-step
                     is a ridge regression per row (Problem 2), but users and films are coupled -> exact
                     only by retraining
    recall_at_k      the usual offline utility metric
    also_watched     the top-k "also watched" list of every film, as a product page would show it
    noisy_also_watched  the same lists published from noisy, thresholded counts
    diff_attack      rank films by how much their public lists changed (Calandrino et al. 2011; Chen et al. 2021)

Cost is counted in hardware-independent units, as everywhere in this course: for ALS one `row solve` is a
k x k linear system for one user or one film; for item-kNN one `cell` is one update of the co-watch matrix.
"""

import numpy as np

F64 = np.float64


# ---------------------------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------------------------

def implicit_split(ratings, n_users, n_items, test_frac=0.2, seed=0):
    """
    Implicit feedback: 'watched' = rated, whatever the stars. For every user, a random `test_frac` of their
    films is held out. Returns R_train, R_test (n_users x n_items, float64 0/1).
    """
    rng = np.random.default_rng(seed)
    R_train, R_test = np.zeros((n_users, n_items)), np.zeros((n_users, n_items))
    for u, items in ratings.groupby("user")["item"]:
        items = rng.permutation(items.to_numpy())
        k = int(round(test_frac * len(items)))
        R_test[u, items[:k]] = 1
        R_train[u, items[k:]] = 1
    return R_train, R_test


# ---------------------------------------------------------------------------------------------
# Item-based nearest neighbours
# ---------------------------------------------------------------------------------------------

class ItemKNN:
    """
    Item-item collaborative filtering. The whole model is the co-watch matrix
        G = Rᵀ R        G[i, j] = number of users who watched both i and j  (a sum over users)
    and similarity is cosine:  S[i, j] = G[i, j] / sqrt(G[i, i] G[j, j]).
    Unlearning user u subtracts r_u r_uᵀ from G: only the |items of u|² cells change. Exact.

    `min_support` hides a pair of films unless at least that many users watched both (a k-anonymity rule for
    what the model is allowed to say in public; 1 = no rule).
    """

    def __init__(self, min_support=1):
        self.min_support = min_support

    def fit(self, R):
        self.R = np.array(R, F64)
        self.G = self.R.T @ self.R
        return self

    def unlearn_users(self, users):
        """Subtract each user's outer product from the co-watch counts. Returns the number of cells updated."""
        cells = 0
        for u in np.atleast_1d(users):
            idx = np.flatnonzero(self.R[u])
            self.G[np.ix_(idx, idx)] -= np.outer(self.R[u, idx], self.R[u, idx])
            self.R[u] = 0
            cells += len(idx) ** 2
        return cells

    def similarity(self):
        n = np.sqrt(np.diag(self.G))
        with np.errstate(divide="ignore", invalid="ignore"):
            S = self.G / np.outer(n, n)
        S[~np.isfinite(S) | (self.G < self.min_support)] = 0
        np.fill_diagonal(S, 0)
        return S

    def item_similarity(self):
        return self.similarity()

    def scores(self, users=None):
        S = self.similarity()
        R = self.R if users is None else self.R[users]
        return R @ S

    @staticmethod
    def fit_cost(R):
        """Cells touched when building G from scratch: Σ_u |items of u|²."""
        return int((np.asarray(R).sum(1) ** 2).sum())


# ---------------------------------------------------------------------------------------------
# Matrix factorisation for implicit feedback
# ---------------------------------------------------------------------------------------------

class ImplicitALS:
    """
    Weighted matrix factorisation, R ≈ X Yᵀ with X (users x k) and Y (films x k).
    Watched cells have confidence 1 + alpha, all others confidence 1 and target 0. Alternating least squares:
    with Y fixed, every user's row is one ridge regression (closed form); then the same for every film.

        x_u = (YᵀY + alpha · Y_uᵀ Y_u + reg · I)⁻¹ (1 + alpha) Σ_{i watched by u} y_i

    The shared YᵀY term means every user's vector depends on every film's, and vice versa: deleting one
    user's row is NOT the same as never having seen them.
    """

    def __init__(self, factors=32, reg=20.0, alpha=3.0, sweeps=12, seed=0):
        self.k, self.reg, self.alpha, self.sweeps, self.seed = factors, reg, alpha, sweeps, seed
        self.row_solves = 0

    def fit(self, R, sweeps=None, init=None):
        """Train from a random start (or warm-start from `init` = (X, Y)). Returns self."""
        R = np.asarray(R, F64)
        if init is None:
            rng = np.random.default_rng(self.seed)
            self.X = rng.normal(0, 0.01, (R.shape[0], self.k))
            self.Y = rng.normal(0, 0.01, (R.shape[1], self.k))
        else:
            self.X, self.Y = init[0].copy(), init[1].copy()
        for _ in range(self.sweeps if sweeps is None else sweeps):
            self.X = self.solve(R, self.Y)
            self.Y = self.solve(R.T, self.X)
        return self

    def solve(self, R, Y):
        """One half-step: re-solve every row of R against the fixed factors Y (closed form, ridge)."""
        YtY = Y.T @ Y
        I = self.reg * np.eye(self.k)
        out = np.zeros((R.shape[0], self.k))
        for u in range(R.shape[0]):
            idx = np.flatnonzero(R[u])
            if len(idx):
                Yo = Y[idx]
                out[u] = np.linalg.solve(YtY + self.alpha * Yo.T @ Yo + I, (1 + self.alpha) * Yo.sum(0))
        self.row_solves += R.shape[0]
        return out

    def copy(self):
        m = ImplicitALS(self.k, self.reg, self.alpha, self.sweeps, self.seed)
        m.X, m.Y, m.row_solves = self.X.copy(), self.Y.copy(), 0
        return m

    def item_similarity(self):
        """Cosine similarity of the film factors: what an 'also watched' list built on this model shows."""
        return cosine_rows(self.Y)

    def scores(self, users=None):
        X = self.X if users is None else self.X[users]
        return X @ self.Y.T

    def fit_cost(self, R):
        return (self.sweeps if self.sweeps else 0) * sum(np.asarray(R).shape)


# ---------------------------------------------------------------------------------------------
# Metrics and attacks
# ---------------------------------------------------------------------------------------------

def top_k(scores, exclude, k=10):
    """Top-k films per row of `scores`, never recommending what the user already watched (`exclude` = 1)."""
    s = np.where(np.asarray(exclude) > 0, -np.inf, scores)
    part = np.argpartition(-s, k, axis=1)[:, :k]
    order = np.argsort(-np.take_along_axis(s, part, 1), axis=1)
    return np.take_along_axis(part, order, 1)


def recall_at_k(model, R_train, R_test, users=None, k=10):
    """Mean over users of |held-out films in the top-k| / min(k, |held-out films|)."""
    users = np.flatnonzero(R_test.sum(1) > 0) if users is None else np.asarray(users)
    rec = top_k(model.scores(users), R_train[users], k)
    hits = np.take_along_axis(R_test[users], rec, 1).sum(1)
    return float(np.mean(hits / np.minimum(k, R_test[users].sum(1))))


def cosine_rows(V):
    n = np.linalg.norm(V, axis=1, keepdims=True)
    n[n == 0] = 1
    U = V / n
    return U @ U.T


def also_watched(model, k=10):
    """The 'people who watched this also watched' list of every film: its top-k most similar films.
    Slots with no positive similarity stay empty (-1), as a product page would leave them blank."""
    S = model.item_similarity().copy()
    np.fill_diagonal(S, -np.inf)
    top = np.argsort(-S, axis=1)[:, :k]
    return np.where(np.take_along_axis(S, top, 1) > 0, top, -1)


def noisy_also_watched(knn, scale, min_count, seed, k=10):
    """
    Publish item-kNN pages from noisy co-watch counts: fresh Laplace noise of the given `scale` on every pair, and
    a pair is shown only if its NOISY count reaches `min_count`. Recommendations to each user can still use the exact
    model; only the public statistic is noised. Fresh noise per release (new `seed`) is what defeats a before/after
    comparison. (Noise in the spirit of differential privacy, not a formal user-level guarantee: one user touches
    many pairs, so a formal bound needs noise scaled to that contribution.)
    """
    rng = np.random.default_rng(seed)
    N = rng.laplace(0, scale, knn.G.shape)
    G = knn.G + np.triu(N) + np.triu(N, 1).T                       # symmetric noise
    n = np.sqrt(np.clip(np.diag(knn.G), 1, None))
    S = G / np.outer(n, n)
    S[G < min_count] = 0
    np.fill_diagonal(S, -np.inf)
    top = np.argsort(-S, axis=1)[:, :k]
    return np.where(np.take_along_axis(S, top, 1) > 0, top, -1)


def diff_attack(lists_before, lists_after):
    """
    An outsider scrapes every film's public 'also watched' list before and after a deletion and ranks films by
    how much their list changed (share of the k slots that are different). Returns one score per film.
    """
    k = lists_before.shape[1]
    return np.array([len((set(a) ^ set(b)) - {-1}) / (2 * k) for a, b in zip(lists_before, lists_after)])


def precision_at(scores, truth, n=None, seed=0):
    """Of the n films the attacker ranks highest, the fraction that are really in `truth` (n = |truth|).
    Ties are broken at random, so an attacker who learned nothing scores |truth| / n_films on average."""
    truth = set(np.atleast_1d(truth).tolist())
    n = len(truth) if n is None else n
    tiebreak = np.random.default_rng(seed).random(len(scores))
    guess = np.lexsort((tiebreak, -np.asarray(scores)))[:n]
    return len(truth & set(guess.tolist())) / n
