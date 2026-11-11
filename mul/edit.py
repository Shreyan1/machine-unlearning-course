# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""
Surgical weight editing for Problem 22. Each edit changes a few weights by hand, in closed form, with no training.

All the edits work on the LAST layer of an MLP from mul.nn, the layer that reads the last hidden layer
(`model.features(X)`) and turns it into logits. For the character LM of Problems 16 and 22 that layer decides
which character comes next.

    neuron_scores     how much each hidden neuron pushes the model towards the right answer (activation x gradient)
    switch_off        zero the outgoing weights of chosen neurons ("knowledge neurons", Dai et al. 2022)
    direction         the difference of two mean hidden states, as a unit vector
    blind_to          make the last layer ignore some directions of the hidden layer (directional ablation,
                      Arditi et al. 2024, and the kind of edit in "Sparks of Weight-Space Programming", 2026)
    key_covariance    the average outer product of hidden states on ordinary text (the C of ROME)
    rewrite_memory    a closed-form edit that gives chosen inputs new outputs and disturbs other inputs as little
                      as possible (ROME, Meng et al. 2022, in the many-keys form of MEMIT, Meng et al. 2023)
    refit_last_layer  the layer-below attack: keep the hidden layer and train a fresh last layer on other data
    changed           how many weights an edit changed, and what share of the model that is
"""

import numpy as np

from .nn import MLP, softmax
from .train import fit

F32 = np.float32


def neuron_scores(model, X, y):
    """
    Average contribution of each last-hidden-layer neuron to log p(y | x), over the rows of X.

    For neuron j with activation h_j, the gradient of log p(y) with respect to h_j is W[j, y] - sum_c p_c W[j, c],
    so its contribution is h_j times that ("activation x gradient"). A large positive score means the neuron
    pushes hard towards the right answer for these rows.
    """
    h = model.features(X)
    W = model.params[-2]
    p = softmax(model(X))
    grad = W[:, np.asarray(y)].T - p @ W.T                    # rows x neurons
    return (h * grad).mean(0)


def switch_off(model, neurons):
    """A copy of the model in which the chosen hidden neurons can no longer reach the output."""
    m = model.copy()
    m.params[-2][np.asarray(neurons, dtype=np.int64)] = 0.0
    return m


def direction(model, X_a, X_b):
    """Unit vector from the mean hidden state of X_b to the mean hidden state of X_a."""
    d = model.features(X_a).mean(0) - model.features(X_b).mean(0)
    return (d / np.linalg.norm(d)).astype(F32)


def blind_to(model, directions, neurons=None):
    """
    A copy whose last layer ignores the given hidden-layer directions:  W <- W - Q Q^T W, where the columns of Q
    are an orthonormal basis of the directions. After the edit, moving the hidden state along a removed direction
    no longer changes the output at all.

    With `neurons`, only those rows of W are changed (the news edit changed 64 columns per layer, not all of them),
    so the directions are removed only from what those neurons send to the output.
    """
    D = np.atleast_2d(np.asarray(directions, dtype=np.float64))
    Q, _ = np.linalg.qr(D.T)                                  # hidden x r, orthonormal columns
    m = model.copy()
    W = m.params[-2].astype(np.float64)
    rows = np.arange(len(W)) if neurons is None else np.asarray(neurons, dtype=np.int64)
    W[rows] -= Q[rows] @ (Q.T @ W)
    m.params[-2] = W.astype(F32)
    return m


def key_covariance(model, X):
    """C = average of h h^T over the rows of X: how the hidden states of ordinary inputs spread out."""
    h = model.features(X).astype(np.float64)
    return h.T @ h / len(h)


def rewrite_memory(model, X_keys, target_logits, C, lam=1e-2, columns=None):
    """
    Treat the last layer as a memory that maps keys (hidden states) to values (logits), and rewrite it so that
    the rows of X_keys produce `target_logits`, while other keys change as little as possible.

        K = hidden states of X_keys (r x hidden),  R = target - current output (r x out)
        dW = C^-1 K^T (K C^-1 K^T)^-1 R

    This is the closed-form ROME update for one key (Meng et al. 2022), written for r keys at once as in MEMIT
    (Meng et al. 2023). After the edit, every key gives exactly its target. `lam` keeps C invertible. With
    `columns`, only those output columns are rewritten (for Problem 22, the ten digits).
    """
    K = model.features(X_keys).astype(np.float64)
    W, b = model.params[-2].astype(np.float64), model.params[-1].astype(np.float64)
    R = np.asarray(target_logits, dtype=np.float64) - (K @ W + b)
    if columns is not None:
        keep = np.zeros(W.shape[1], dtype=bool)
        keep[np.asarray(columns, dtype=np.int64)] = True
        R[:, ~keep] = 0.0
    Ci = np.linalg.inv(C + lam * np.eye(len(C)))
    dW = Ci @ K.T @ np.linalg.solve(K @ Ci @ K.T, R)
    m = model.copy()
    m.params[-2] = (W + dW).astype(F32)
    return m


def refit_last_layer(model, X, y, epochs=30, lr=3e-3, batch_size=64, seed=0):
    """
    The layer-below attack. Keep every layer except the last, and train a brand-new last layer on (X, y).

    The attacker uses only data they already have (here, other people's lines and ordinary text). If the hidden
    layer still holds what was "removed", the new last layer learns to read it out again.
    """
    probe = fit(lambda: MLP(model.sizes[-2], model.sizes[-1], ()), model.features(X), y,
                epochs=epochs, lr=lr, batch_size=batch_size, seed=seed)
    m = model.copy()
    m.params[-2], m.params[-1] = probe.params[0], probe.params[1]
    return m


def changed(edited, original):
    """(number of weights that differ, share of all weights)."""
    n = sum(int((a != b).sum()) for a, b in zip(edited.params, original.params))
    return n, n / original.n_params()
