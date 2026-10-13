"""
Training and prediction utilities (pure NumPy).

Every dataset in this repo is small enough to live in memory, so the training loop is ten lines:
shuffle -> mini-batch -> forward -> loss gradient -> backward -> Adam step.
"""

import random
import time

import numpy as np

from .nn import Adam, cross_entropy, softmax


def set_seed(seed: int) -> None:
    """Same seed -> same initial weights and same batch order -> bit-for-bit identical model."""
    random.seed(seed)
    np.random.seed(seed)


def batches(n, batch_size, rng, shuffle=True):
    """Yield index arrays covering range(n) in mini-batches."""
    idx = rng.permutation(n) if shuffle else np.arange(n)
    for start in range(0, n, batch_size):
        yield idx[start:start + batch_size]


def sgd_loop(model, X, steps_fn, epochs, lr, batch_size, seed, weight_decay=0.0, opt=None):
    """
    The generic loop every method in this repo uses. `steps_fn(model, idx)` must return
    dLoss/dlogits for the mini-batch `idx` (after calling model.forward(..., keep_cache=True)).
    Returns the number of example-gradients computed (our hardware-independent cost unit).
    """
    rng = np.random.default_rng(seed)
    opt = opt or Adam(model.params, lr=lr, weight_decay=weight_decay)
    processed = 0
    for _ in range(epochs):
        for b in batches(len(X), batch_size, rng):
            dlogits = steps_fn(model, b)
            opt.step(model.backward(dlogits))
            processed += len(b)
    return processed


def fit(model, X, y, epochs=30, lr=1e-3, batch_size=64, weight_decay=0.0, seed=0, verbose=False):
    """
    Train with Adam + cross-entropy. Returns the trained model.

    `model` may be a model with `.params` (an MLP or a LoRA adapter, trained in place) or a factory like
    `lambda: MLP(64, 10)`. Prefer the factory: the seed then also fixes the *initial weights*,
    so two different seeds give two genuinely independent models (notebook 08 relies on this).

    weight_decay is 0 by default on purpose: an un-regularised model memorises its training
    data, which is exactly the behaviour unlearning has to deal with.
    """
    set_seed(seed)
    if not hasattr(model, "params"):
        model = model()
    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(y)

    def step(m, b):
        loss, g = cross_entropy(m.forward(X[b], keep_cache=True), y[b])
        return g

    rng = np.random.default_rng(seed)
    opt = Adam(model.params, lr=lr, weight_decay=weight_decay)
    for ep in range(epochs):
        for b in batches(len(X), batch_size, rng):
            opt.step(model.backward(step(model, b)))
        if verbose and (ep + 1) % max(1, epochs // 5) == 0:
            print(f"  epoch {ep + 1:>3}/{epochs}   train loss {cross_entropy(model(X), y)[0]:.4f}")
    return model


def timed_fit(*args, **kwargs):
    t0 = time.perf_counter()
    m = fit(*args, **kwargs)
    return m, time.perf_counter() - t0


def predict_proba(model, X, temperature=1.0):
    return softmax(model(np.asarray(X, dtype=np.float32)), temperature)


def predict(model, X):
    return predict_proba(model, X).argmax(1)


def accuracy(model, X, y) -> float:
    if len(X) == 0:
        return float("nan")
    return float((predict(model, X) == np.asarray(y)).mean())


def per_example_loss(model, X, y):
    """Cross-entropy of every single example - the raw material of membership inference."""
    return cross_entropy(model(np.asarray(X, dtype=np.float32)), y, per_example=True)


def clone(model):
    """An independent copy. Unlearning methods never modify the original model."""
    return model.copy()


def weights_equal(a, b, atol=0.0) -> bool:
    """True if two models have identical weights (used to *prove* SISA is exact)."""
    return all(np.allclose(p, q, atol=atol, rtol=0) for p, q in zip(a.params, b.params))


def max_weight_diff(a, b) -> float:
    return float(max(np.abs(p - q).max() for p, q in zip(a.params, b.params)))
