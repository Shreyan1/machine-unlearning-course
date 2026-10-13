"""
The 'lab' used by notebooks 01-08: handwritten digits (sklearn, 1,797 images of 8x8 pixels)
and three deletion scenarios that cover the situations you meet in practice.

    "carol"   A single user, Carol, contributed 40 digits written with a thick marker - a
              distinctive style nobody else has. Deep models memorise such rare, atypical data
              (Feldman 2020), so Carol's influence is large and visible. This is the hard,
              realistic Right-to-be-Forgotten case.

    "random"  10% of training rows, picked at random, ask to be deleted. They are typical, so the
              model barely depends on any one of them. Easy to forget - hard to *prove*.

    "class"   Every example of one class (the digit 3) must go - like removing one person from a
              face-recognition model, or one product from a recommender. The gold standard is
              obvious: a model that never saw a 3 can never predict 3.

Everything is deterministic: same scenario + same seed -> same split.
"""

from dataclasses import dataclass, field

import numpy as np
from scipy.ndimage import maximum_filter

from . import data
from .nn import MLP

FIT = dict(epochs=60, lr=1e-3, batch_size=64)        # the one training recipe used everywhere
HIDDEN = (256, 256)


def model_fn():
    """64 pixels -> 256 -> 256 -> 10 digits. Called with a seed set beforehand."""
    return MLP(64, 10, HIDDEN)


def thick_marker(X):
    """Carol's handwriting: every stroke widened by one pixel (a 2x2 maximum filter)."""
    imgs = np.asarray(X).reshape(-1, 8, 8)
    return np.stack([maximum_filter(a, size=2) for a in imgs]).reshape(-1, 64).astype(np.float32)


@dataclass
class Lab:
    scenario: str
    X_train: np.ndarray            # the full training set D (after Carol's digits are inserted)
    y_train: np.ndarray
    X_test: np.ndarray             # unseen test data, for utility
    y_test: np.ndarray
    forget_idx: np.ndarray         # rows of D to delete  (D_f)
    retain_idx: np.ndarray         # rows of D to keep    (D_r)
    X_like_forget: np.ndarray      # unseen data from the SAME distribution as D_f (never trained on)
    y_like_forget: np.ndarray
    description: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def Xr(self): return self.X_train[self.retain_idx]
    @property
    def yr(self): return self.y_train[self.retain_idx]
    @property
    def Xf(self): return self.X_train[self.forget_idx]
    @property
    def yf(self): return self.y_train[self.forget_idx]

    def splits(self):
        """The dict the audit functions expect."""
        return dict(Xr=self.Xr, yr=self.yr, Xf=self.Xf, yf=self.yf, Xt=self.X_test, yt=self.y_test)

    def __repr__(self):
        return (f"Lab('{self.scenario}': |D|={len(self.X_train)}, |D_f|={len(self.forget_idx)}, "
                f"|D_r|={len(self.retain_idx)}, |test|={len(self.X_test)})")


def make_lab(scenario="carol", seed=0, n_carol=40, forget_class=3, random_frac=0.10):
    X, y = data.load_digits()
    Xtr, Xt, ytr, yt = data.train_test(X, y, test_size=0.3, seed=seed)
    rng = np.random.default_rng(seed + 3)

    if scenario == "carol":
        f = np.sort(rng.choice(len(Xtr), n_carol, replace=False))
        Xtr = Xtr.copy()
        Xtr[f] = thick_marker(Xtr[f])                       # these rows are now Carol's digits
        vi = rng.choice(len(Xt), 80, replace=False)
        X_like, y_like = thick_marker(Xt[vi]), yt[vi]       # same style, never trained on
        desc = f"Carol contributed {n_carol} thick-marker digits and invokes her right to erasure."
    elif scenario == "random":
        f = np.sort(rng.choice(len(Xtr), int(random_frac * len(Xtr)), replace=False))
        X_like, y_like = Xt, yt
        desc = f"{int(random_frac * 100)}% of users, chosen at random, ask to be deleted."
    elif scenario == "class":
        f = np.where(ytr == forget_class)[0]
        keep_t = yt != forget_class
        X_like, y_like = Xt[~keep_t], yt[~keep_t]
        Xt, yt = Xt[keep_t], yt[keep_t]                     # utility is measured on other classes
        desc = f"Every training example of digit {forget_class} must be removed."
    else:
        raise ValueError(scenario)

    r = np.setdiff1d(np.arange(len(Xtr)), f)
    return Lab(scenario, Xtr.astype(np.float32), ytr, Xt.astype(np.float32), yt, f, r,
               X_like.astype(np.float32), y_like, desc)
