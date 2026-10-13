"""
Tiny character-level language models for the LLM-unlearning lesson (Problem 16).

Two models, the same two rungs as the rest of the course:

    NGramLM     counts of (context -> next character), with stupid back-off.  The model IS a table of
                sums, so unlearning a line is an exact subtraction (rung 1, Problem 1).
    neural LM   a Bengio-style MLP language model: the last `k` characters, one-hot encoded and
                concatenated, go through the NumPy MLP from mul.nn to predict the next character.
                Every training string touches every weight (rung 4).

Plus the measurements LLM-unlearning papers use:

    complete        greedy decoding - "does the model recite it?"          (extraction)
    exposure        rank of the secret among all candidates (Carlini et al. 2019, the Secret Sharer)
    seq_logprob     log-probability of a target string after a prompt
    npo             Negative Preference Optimisation (Zhang et al. 2024)
"""

from collections import defaultdict

import numpy as np

from .nn import Adam, cross_entropy, log_softmax
from .train import batches, clone, set_seed


class CharVocab:
    def __init__(self, text):
        self.chars = sorted(set(text))
        self.index = {c: i for i, c in enumerate(self.chars)}

    def __len__(self):
        return len(self.chars)

    def encode(self, s):
        return np.array([self.index[c] for c in s if c in self.index], dtype=np.int64)

    def decode(self, ids):
        return "".join(self.chars[i] for i in ids)


# ---------------------------------------------------------------------------------------------
# Rung 1: an n-gram model is a table of counts
# ---------------------------------------------------------------------------------------------

class NGramLM:
    """
    Character n-gram model with 'stupid back-off' (Brants et al. 2007): use the longest context
    seen in training; if it was never seen, drop its first character and try again.
    """

    def __init__(self, order=12):
        self.order = order
        self.counts = defaultdict(lambda: defaultdict(int))   # context string -> {next char: count}

    def _update(self, text, sign):
        for i in range(len(text)):
            for n in range(0, self.order + 1):
                if i - n < 0:
                    break
                ctx, nxt = text[i - n:i], text[i]
                self.counts[ctx][nxt] += sign
                if self.counts[ctx][nxt] == 0:
                    del self.counts[ctx][nxt]
                if not self.counts[ctx]:
                    del self.counts[ctx]
        return self

    def fit(self, texts):
        for t in texts:
            self._update(t, +1)
        return self

    def unlearn(self, texts):
        """Exact: subtract every count the texts contributed."""
        for t in texts:
            self._update(t, -1)
        return self

    def next_distribution(self, context):
        for n in range(min(self.order, len(context)), -1, -1):
            ctx = context[len(context) - n:]
            if ctx in self.counts:
                c = self.counts[ctx]
                total = sum(c.values())
                return {k: v / total for k, v in c.items()}
        return {}

    def complete(self, prompt, n_chars, stop="\n"):
        out = prompt
        for _ in range(n_chars):
            dist = self.next_distribution(out)
            if not dist:
                break
            nxt = max(sorted(dist), key=dist.get)
            if nxt == stop:
                break
            out += nxt
        return out[len(prompt):]

    def seq_logprob(self, prompt, target, floor=1e-6):
        lp, ctx = 0.0, prompt
        for ch in target:
            lp += np.log(max(self.next_distribution(ctx).get(ch, 0.0), floor))
            ctx += ch
        return lp

    def table_equal(self, other):
        return {k: dict(v) for k, v in self.counts.items()} == {k: dict(v) for k, v in other.counts.items()}


# ---------------------------------------------------------------------------------------------
# Rung 4+: a neural language model built from the NumPy MLP
# ---------------------------------------------------------------------------------------------

def one_hot_windows(ids, k, V):
    """For every position t >= 1, the previous k characters (left-padded with char 0), one-hot, flattened."""
    pad = np.r_[np.zeros(k, np.int64), ids]
    n = len(ids)
    X = np.zeros((n, k * V), np.float32)
    for j in range(k):
        X[np.arange(n), j * V + pad[j:j + n]] = 1.0
    return X


def make_examples(texts, vocab, k):
    """(context window, next char) pairs for a list of strings; each string is modelled independently."""
    Xs, ys = [], []
    for t in texts:
        ids = vocab.encode(t)
        Xs.append(one_hot_windows(ids, k, len(vocab)))
        ys.append(ids)
    return np.concatenate(Xs), np.concatenate(ys)


def target_examples(prompt, target, vocab, k):
    """Only the positions that predict `target` after `prompt` (the part to forget / to measure)."""
    ids = vocab.encode(prompt + target)
    X = one_hot_windows(ids, k, len(vocab))
    return X[len(prompt):], ids[len(prompt):]


def nn_seq_logprob(model, prompt, target, vocab, k):
    X, y = target_examples(prompt, target, vocab, k)
    lp = log_softmax(model(X))
    return float(lp[np.arange(len(y)), y].sum())


def nn_complete(model, prompt, vocab, k, n_chars, stop="\n"):
    ids = list(vocab.encode(prompt))
    out = []
    for _ in range(n_chars):
        x = one_hot_windows(np.array(ids + [0], np.int64), k, len(vocab))[-1:]
        nxt = int(model(x).argmax())
        if vocab.chars[nxt] == stop:
            break
        out.append(nxt)
        ids.append(nxt)
    return vocab.decode(out)


def exposure(logprob_fn, prompt, secret, candidates):
    """
    Carlini et al. (2019): rank the true secret among all candidate secrets by model likelihood.
        exposure = log2(#candidates) - log2(rank)
    Maximal (log2 N) when the secret is the model's top guess; ~1 when it is ranked like a random candidate.
    """
    scores = {c: logprob_fn(prompt, c) for c in candidates}
    rank = 1 + sum(s > scores[secret] for s in scores.values())
    return float(np.log2(len(candidates)) - np.log2(rank)), rank


# ---------------------------------------------------------------------------------------------
# LLM-style unlearning objectives
# ---------------------------------------------------------------------------------------------

def npo(model, reference, forget_pairs, X_retain=None, y_retain=None, beta=1.0, steps=50, lr=1e-3,
        retain_weight=1.0, batch_size=64, seed=0, history=None):
    """
    Negative Preference Optimisation (Zhang, Lin, Bai & Mei 2024), with an optional retain term.

    For each forget sequence s with log-ratio  Δ = log π_θ(s) - log π_ref(s):
        L_NPO = -(2/β) · log σ(-β Δ)
        ∇L_NPO = 2 σ(β Δ) · ∇ log π_θ(s)         -> gradient ASCENT on the sequence, weighted
    The weight 2σ(βΔ) starts at 1 (Δ = 0: plain gradient ascent) and decays towards 0 as the model
    moves below the reference, which is what stops NPO from collapsing the way gradient ascent does.

    forget_pairs: list of (X_positions, y_positions) - one entry per forget sequence.
    """
    set_seed(seed)
    m, rng = clone(model), np.random.default_rng(seed)
    opt = Adam(m.params, lr=lr)
    ref_lp = [float(log_softmax(reference(X))[np.arange(len(y)), y].sum()) for X, y in forget_pairs]
    for step in range(steps):
        grads = None
        for (X, y), lp_ref in zip(forget_pairs, ref_lp):
            logits = m.forward(X, keep_cache=True)
            delta = float(log_softmax(logits)[np.arange(len(y)), y].sum()) - lp_ref
            w = 2.0 / (1.0 + np.exp(-beta * delta))                  # 2 σ(β Δ)
            _, g = cross_entropy(logits, y)                          # gradient of the mean NLL
            gr = m.backward(-w * g * len(y) / len(forget_pairs))     # ascent on log π, summed over tokens
            grads = gr if grads is None else [a + b for a, b in zip(grads, gr)]
        if X_retain is not None and retain_weight > 0:
            b = rng.choice(len(X_retain), min(batch_size, len(X_retain)), replace=False)
            _, g = cross_entropy(m.forward(X_retain[b], keep_cache=True), y_retain[b])
            grads = [a + retain_weight * r for a, r in zip(grads, m.backward(g))]
        opt.step(grads)
        if history is not None:
            history(m, step)
    return m


def gradient_ascent_lm(model, forget_pairs, X_retain=None, y_retain=None, steps=50, lr=1e-3,
                       retain_weight=0.0, batch_size=64, seed=0, history=None):
    """Plain gradient ascent on the forget sequences (Jang et al. 2022) = NPO with a constant weight of 1."""
    set_seed(seed)
    m, rng = clone(model), np.random.default_rng(seed)
    opt = Adam(m.params, lr=lr)
    for step in range(steps):
        grads = None
        for X, y in forget_pairs:
            _, g = cross_entropy(m.forward(X, keep_cache=True), y)
            gr = m.backward(-g * len(y) / len(forget_pairs))
            grads = gr if grads is None else [a + b for a, b in zip(grads, gr)]
        if X_retain is not None and retain_weight > 0:
            b = rng.choice(len(X_retain), min(batch_size, len(X_retain)), replace=False)
            _, g = cross_entropy(m.forward(X_retain[b], keep_cache=True), y_retain[b])
            grads = [a + retain_weight * r for a, r in zip(grads, m.backward(g))]
        opt.step(grads)
        if history is not None:
            history(m, step)
    return m


def finetune_lm(model, X, y, epochs=1, lr=1e-3, batch_size=64, seed=0, max_steps=None):
    """Continue training (used for fine-tuning, refusal training and the relearn attack)."""
    set_seed(seed)
    m, rng = clone(model), np.random.default_rng(seed)
    opt, steps = Adam(m.params, lr=lr), 0
    for _ in range(epochs):
        for b in batches(len(X), batch_size, rng):
            _, g = cross_entropy(m.forward(X[b], keep_cache=True), y[b])
            opt.step(m.backward(g))
            steps += 1
            if max_steps is not None and steps >= max_steps:
                return m
    return m
