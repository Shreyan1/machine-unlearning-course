"""
A tiny neural-network library in pure NumPy - no PyTorch, no TensorFlow.

Why hand-written? Because machine unlearning is *about gradients*: "gradient ascent", "push the
student away from the teacher", "pull it back on the retain set". When every gradient is a line
of NumPy you can read, there is no magic left - you can see exactly what each method does to the
weights.

Contents
    MLP              fully-connected ReLU network with forward() and backward()
    Adam             the Adam optimiser (Kingma & Ba, 2015)
    softmax          numerically-stable softmax, with temperature
    cross_entropy    loss AND its gradient w.r.t. the logits
    distill_kl       KL(teacher || student) on softened outputs, AND its gradient

Every loss function returns (loss_value, dloss/dlogits). backward() turns dloss/dlogits into
gradients for every weight matrix. That is all a training loop needs.
"""

import numpy as np

F32 = np.float32


# ---------------------------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------------------------

class MLP:
    """
    logits = W_L · relu( ... relu( W_1 · x + b_1 ) ... ) + b_L

    Weights are initialised with He initialisation (std = sqrt(2 / fan_in)), the standard choice
    for ReLU networks. `seed=None` draws the seed from NumPy's global RNG, so `train.set_seed()`
    controls it.
    """

    def __init__(self, n_in, n_out, hidden=(256, 256), seed=None):
        if seed is None:
            seed = int(np.random.randint(0, 2**31 - 1))
        rng = np.random.default_rng(seed)
        self.sizes = [n_in, *hidden, n_out]
        self.params = []                                   # [W1, b1, W2, b2, ..., WL, bL]
        for a, b in zip(self.sizes[:-1], self.sizes[1:]):
            self.params.append(rng.normal(0.0, np.sqrt(2.0 / a), size=(a, b)).astype(F32))
            self.params.append(np.zeros(b, dtype=F32))
        self._cache = None

    @property
    def n_layers(self):
        return len(self.params) // 2

    def forward(self, X, keep_cache=False):
        """Return the logits. With keep_cache=True, remember activations for backward()."""
        h = np.asarray(X, dtype=F32)
        acts = [h]
        for layer in range(self.n_layers - 1):
            W, b = self.params[2 * layer], self.params[2 * layer + 1]
            h = np.maximum(h @ W + b, 0.0)                 # ReLU
            acts.append(h)
        out = h @ self.params[-2] + self.params[-1]        # last layer: no activation
        if keep_cache:
            self._cache = acts
        return out

    __call__ = forward

    def features(self, X):
        """Activations of the last hidden layer - the model's internal 'embedding' of X."""
        h = np.asarray(X, dtype=F32)
        for layer in range(self.n_layers - 1):
            h = np.maximum(h @ self.params[2 * layer] + self.params[2 * layer + 1], 0.0)
        return h

    def backward(self, dlogits):
        """
        Backpropagation. Given dLoss/dlogits (shape [batch, n_out]) from the most recent
        forward(keep_cache=True), return dLoss/dparam for every parameter, aligned with .params.
        """
        acts = self._cache
        grads = [None] * len(self.params)
        g = dlogits.astype(F32)
        for layer in reversed(range(self.n_layers)):
            a_prev = acts[layer]
            grads[2 * layer] = a_prev.T @ g                # dL/dW = input^T · upstream
            grads[2 * layer + 1] = g.sum(axis=0)           # dL/db = sum over the batch
            if layer > 0:
                g = (g @ self.params[2 * layer].T) * (acts[layer] > 0)   # through ReLU
        return grads

    def input_gradient(self, dlogits):
        """dLoss/dX for the most recent forward(keep_cache=True): how to change the INPUT to change the loss.
        UNSIR (Problem 19) uses it to learn noise images that the model gets wrong."""
        acts, g = self._cache, dlogits.astype(F32)
        for layer in reversed(range(self.n_layers)):
            g = g @ self.params[2 * layer].T
            if layer > 0:
                g = g * (acts[layer] > 0)
        return g

    def squared_grads(self, dlogits):
        """
        Σ over the batch of each example's OWN gradient, squared, for every weight (the diagonal of the
        empirical Fisher information). `dlogits` must be per-example (not divided by the batch size).
        For a weight matrix the per-example gradient is an outer product a·gᵀ, so its square summed over
        the batch is (a²)ᵀ(g²): one matrix product, no loop over examples.
        """
        acts, g = self._cache, dlogits.astype(F32)
        out = [None] * len(self.params)
        for layer in reversed(range(self.n_layers)):
            out[2 * layer] = (acts[layer] ** 2).T @ (g ** 2)
            out[2 * layer + 1] = (g ** 2).sum(axis=0)
            if layer > 0:
                g = (g @ self.params[2 * layer].T) * (acts[layer] > 0)
        return out

    # -- utilities ---------------------------------------------------------------------------
    def copy(self):
        m = MLP.__new__(MLP)
        m.sizes = list(self.sizes)
        m.params = [p.copy() for p in self.params]
        m._cache = None
        return m

    def state(self):
        return [p.copy() for p in self.params]

    def load(self, state):
        self.params = [p.copy() for p in state]
        return self

    def n_params(self):
        return int(sum(p.size for p in self.params))

    def __repr__(self):
        return f"MLP({' -> '.join(map(str, self.sizes))}, {self.n_params():,} params)"


# ---------------------------------------------------------------------------------------------
# LoRA adapters: fine-tune a frozen base model through small low-rank matrices (Problem 15)
# ---------------------------------------------------------------------------------------------

class LoRA:
    """
    Low-Rank Adaptation (Hu et al. 2021) for the MLP above.

        W_eff = W_base + (alpha / r) · A · B        A: (fan_in x r), B: (r x fan_out)

    The base model is FROZEN and shared; only A and B (and nothing else) are trained. B starts at
    zero, so a fresh adapter changes nothing. Because each tenant's adapter is trained only on that
    tenant's data, deleting the adapter is *exact* unlearning of that tenant - at zero cost.

    `.params` holds only the adapter matrices [A1, B1, A2, B2, ...], so train.fit, Adam and every
    method in mul.methods work on adapters unchanged.
    """

    def __init__(self, base, rank=4, alpha=None, seed=None):
        if seed is None:
            seed = int(np.random.randint(0, 2**31 - 1))
        rng = np.random.default_rng(seed)
        self.base, self.rank = base, rank
        self.scale = (alpha if alpha is not None else rank) / rank
        self.sizes = list(base.sizes)
        self.params = []
        for a, b in zip(self.sizes[:-1], self.sizes[1:]):
            self.params.append(rng.normal(0.0, 1.0 / np.sqrt(a), size=(a, rank)).astype(F32))  # A
            self.params.append(np.zeros((rank, b), dtype=F32))                                  # B
        self._cache = None

    @property
    def n_layers(self):
        return len(self.sizes) - 1

    def delta(self, layer):
        """The adapter's change to one weight matrix: (alpha / r) · A · B."""
        return self.scale * self.params[2 * layer] @ self.params[2 * layer + 1]

    def weight(self, layer):
        return self.base.params[2 * layer] + self.delta(layer)

    def forward(self, X, keep_cache=False):
        h = np.asarray(X, dtype=F32)
        acts = [h]
        for layer in range(self.n_layers - 1):
            h = np.maximum(h @ self.weight(layer) + self.base.params[2 * layer + 1], 0.0)
            acts.append(h)
        out = h @ self.weight(self.n_layers - 1) + self.base.params[-1]
        if keep_cache:
            self._cache = acts
        return out

    __call__ = forward

    def features(self, X):
        h = np.asarray(X, dtype=F32)
        for layer in range(self.n_layers - 1):
            h = np.maximum(h @ self.weight(layer) + self.base.params[2 * layer + 1], 0.0)
        return h

    def backward(self, dlogits):
        """Same backprop as the MLP; the weight gradient is then routed into A and B (chain rule)."""
        acts, grads = self._cache, [None] * len(self.params)
        g = dlogits.astype(F32)
        for layer in reversed(range(self.n_layers)):
            dW = acts[layer].T @ g                                   # gradient w.r.t. W_eff
            A, B = self.params[2 * layer], self.params[2 * layer + 1]
            grads[2 * layer] = self.scale * dW @ B.T                 # dL/dA
            grads[2 * layer + 1] = self.scale * A.T @ dW             # dL/dB
            if layer > 0:
                g = (g @ self.weight(layer).T) * (acts[layer] > 0)
        return grads

    def merged(self):
        """Fold the adapter into a plain MLP (what many serving stacks do for speed)."""
        m = self.base.copy()
        for layer in range(self.n_layers):
            m.params[2 * layer] = m.params[2 * layer] + self.delta(layer)
        return m

    def copy(self):
        m = LoRA.__new__(LoRA)
        m.base, m.rank, m.scale, m.sizes = self.base, self.rank, self.scale, list(self.sizes)
        m.params = [p.copy() for p in self.params]
        m._cache = None
        return m

    def state(self):
        return [p.copy() for p in self.params]

    def load(self, state):
        self.params = [p.copy() for p in state]
        return self

    def n_params(self):
        return int(sum(p.size for p in self.params))

    def __repr__(self):
        return f"LoRA(rank {self.rank} on {self.base!r}: {self.n_params():,} trainable params)"


# ---------------------------------------------------------------------------------------------
# The optimiser
# ---------------------------------------------------------------------------------------------

class Adam:
    """Adam: per-parameter step sizes from running averages of the gradient and its square."""

    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0):
        self.params, self.lr, self.eps, self.wd = params, lr, eps, weight_decay
        self.b1, self.b2 = betas
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        for p, g, m, v in zip(self.params, grads, self.m, self.v):
            if self.wd:
                g = g + self.wd * p
            m *= self.b1
            m += (1 - self.b1) * g
            v *= self.b2
            v += (1 - self.b2) * g * g
            p -= self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps)   # in place


# ---------------------------------------------------------------------------------------------
# Losses - each returns (loss, dloss/dlogits)
# ---------------------------------------------------------------------------------------------

def softmax(logits, T=1.0):
    z = np.asarray(logits, dtype=np.float64) / T
    z -= z.max(axis=1, keepdims=True)                      # numerical stability
    e = np.exp(z)
    return (e / e.sum(axis=1, keepdims=True)).astype(F32)


def log_softmax(logits, T=1.0):
    z = np.asarray(logits, dtype=np.float64) / T
    z -= z.max(axis=1, keepdims=True)
    return (z - np.log(np.exp(z).sum(axis=1, keepdims=True))).astype(F32)


def cross_entropy(logits, y, per_example=False):
    """
    CE = -log p(y | x).   Gradient w.r.t. the logits:  (p - onehot(y)) / batch_size
    """
    y = np.asarray(y)
    logp = log_softmax(logits)
    losses = -logp[np.arange(len(y)), y]
    if per_example:
        return losses
    grad = np.exp(logp)
    grad[np.arange(len(y)), y] -= 1.0
    return float(losses.mean()), grad / len(y)


def distill_kl(student_logits, teacher_logits, T=1.0):
    """
    Knowledge-distillation loss  T^2 · KL( softmax(teacher/T) || softmax(student/T) ).

    Gradient w.r.t. the STUDENT logits (the teacher is fixed):
        T^2 · (1/T) · (p_student - p_teacher) / batch  =  T · (p_s - p_t) / batch

    SCRUB minimises this on D_r and *maximises* it on D_f (just flip the sign of the gradient).
    Bad Teacher minimises it against a different teacher depending on the example.
    """
    p_t = softmax(teacher_logits, T)
    logp_s = log_softmax(student_logits, T)
    kl = np.sum(p_t * (np.log(np.clip(p_t, 1e-12, 1)) - logp_s), axis=1)
    grad = T * (np.exp(logp_s) - p_t) / len(p_t)
    return float(kl.mean() * T * T), grad.astype(F32)
