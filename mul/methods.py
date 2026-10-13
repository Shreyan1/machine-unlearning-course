"""
Unlearning methods, from the gold standard to the approximate ones - pure NumPy.

Every method takes an already-trained model (or a recipe to build one) and returns
    (unlearned_model, info)
where `info` records the cost: wall-clock seconds and "samples_processed" (number of
example-gradient computations - a hardware-independent cost you can compare on any laptop).

    retrain          exact, the gold standard                     notebook 03   (Cao & Yang 2015)
    SISA             exact, shard / slice / checkpoint            notebook 04   (Bourtoule et al. 2021)
    finetune         approximate baseline: keep training on D_r   notebook 05
    gradient_ascent  approximate baseline: climb the loss on D_f  notebook 05   (Jang et al. 2023)
    neggrad_plus     ascent on D_f + descent on D_r               notebook 05   (Kurmanji et al. 2023)
    scrub            teacher-student max/min distillation        notebook 06   (Kurmanji et al. 2023)
    scrub_rewind     SCRUB+R: do not over-forget                  notebook 06
    bad_teacher      competent + incompetent teacher distillation notebook 07   (Chundawat et al. 2023)

  The method zoo, Problem 19:
    random_label     train on D_f with random wrong labels (+ D_r)              (Graves et al. 2021)
    salun            random_label, but only the weights most salient for D_f   (Fan et al. 2024)
    l1_sparse        fine-tune on D_r with a decaying L1 penalty               (Jia et al. 2023)
    unsir            error-maximising noise, impair, repair                     (Tarun et al. 2023)
    ssd              shrink weights that matter far more for D_f, no training  (Foster et al. 2024)
    last_layer       re-solve only the softmax layer exactly, on D_r           (after Guo et al. 2020)

Read the loss lines: every method is one or two lines that decide the SIGN and the TARGET of the
gradient on D_r and D_f. That is the whole field in miniature.
"""

import time

import numpy as np

from .nn import MLP, Adam, cross_entropy, distill_kl
from .train import batches, clone, fit, predict_proba, set_seed


def _info(t0, samples, **extra):
    return {"seconds": time.perf_counter() - t0, "samples_processed": int(samples), **extra}


def _f32(X):
    return np.asarray(X, dtype=np.float32)


# --------------------------------------------------------------------------------------------
# Exact unlearning
# --------------------------------------------------------------------------------------------

def retrain(model_fn, X_retain, y_retain, seed=0, **fit_kwargs):
    """The gold standard: throw the model away and train a new one on D_r only."""
    t0 = time.perf_counter()
    model = fit(model_fn, X_retain, y_retain, seed=seed, **fit_kwargs)
    return model, _info(t0, fit_kwargs.get("epochs", 30) * len(X_retain))


class SISA:
    """
    Sharded, Isolated, Sliced, Aggregated training (Bourtoule et al., IEEE S&P 2021).

        Sharded     the data is split into K disjoint shards
        Isolated    one independent model per shard - shards never see each other's data
        Sliced      each shard is fed in R cumulative slices; a checkpoint is saved after each
        Aggregated  prediction = average of the K shard models' probabilities

    To unlearn a point we retrain only *its* shard, and only from the checkpoint saved *before*
    the slice that contained it. The result provably never saw the point: it is bit-for-bit the
    model you would get by training SISA from scratch without it (notebook 04 checks this).
    """

    def __init__(self, model_fn, n_shards=5, n_slices=4, epochs_per_slice=10, lr=1e-3,
                 batch_size=64, seed=0):
        self.model_fn, self.K, self.R = model_fn, n_shards, n_slices
        self.epochs, self.lr, self.bs, self.seed = epochs_per_slice, lr, batch_size, seed
        self.shard_models = []

    def _train_shard(self, s, start_slice):
        """(Re)train shard s starting from the checkpoint before `start_slice`."""
        set_seed(self.seed * 1000 + s)
        model = self.model_fn()                                    # fixed init per shard
        if start_slice > 0:
            model.load(self.checkpoints[s][start_slice - 1])
        processed = 0
        for r in range(start_slice, self.R):
            idx = np.concatenate([np.asarray(sl, dtype=int) for sl in self.slices[s][: r + 1]])
            if len(idx):
                fit(model, self.X[idx], self.y[idx], epochs=self.epochs, lr=self.lr,
                    batch_size=self.bs, seed=self.seed * 1000 + s * 10 + r)
                processed += self.epochs * len(idx)
            self.checkpoints[s][r] = model.state()
        return model, processed

    def fit(self, X, y, partition=None):
        """
        Train all shards. `partition` (optional) is a list of K lists of R index arrays - pass it
        to reproduce an exact data layout (used to prove exactness).
        """
        t0 = time.perf_counter()
        self.X, self.y = _f32(X), np.asarray(y)
        if partition is None:
            perm = np.random.default_rng(self.seed).permutation(len(self.X))
            partition = [list(np.array_split(sh, self.R)) for sh in np.array_split(perm, self.K)]
        self.slices = [[np.asarray(sl, dtype=int) for sl in shard] for shard in partition]
        self.checkpoints = [[None] * self.R for _ in range(self.K)]
        self.shard_models, processed = [], 0
        for s in range(self.K):
            m, p = self._train_shard(s, 0)
            self.shard_models.append(m)
            processed += p
        return _info(t0, processed)

    def locate(self, i):
        """Which (shard, slice) holds training example i?"""
        for s in range(self.K):
            for r in range(self.R):
                if i in self.slices[s][r]:
                    return s, r
        raise KeyError(i)

    def unlearn(self, indices):
        """Exactly remove training examples `indices` (row positions in the X given to fit)."""
        t0 = time.perf_counter()
        indices = set(int(i) for i in indices)
        earliest = {}
        for s in range(self.K):
            for r in range(self.R):
                keep = np.array([i for i in self.slices[s][r] if int(i) not in indices], dtype=int)
                if len(keep) < len(self.slices[s][r]):
                    self.slices[s][r] = keep
                    earliest[s] = min(earliest.get(s, r), r)
        processed = 0
        for s, r in sorted(earliest.items()):
            self.shard_models[s], p = self._train_shard(s, r)
            processed += p
        return self, _info(t0, processed, shards_retrained=len(earliest), first_slices=earliest)

    # SISA behaves like a model: logits = log of the averaged probabilities
    def forward(self, X, keep_cache=False):
        from .nn import softmax
        probs = np.mean([softmax(m(X)) for m in self.shard_models], axis=0)
        return np.log(np.clip(probs, 1e-12, 1)).astype(np.float32)

    __call__ = forward


# --------------------------------------------------------------------------------------------
# Approximate unlearning - simple baselines
# --------------------------------------------------------------------------------------------

def finetune(model, X_retain, y_retain, epochs=5, lr=1e-3, batch_size=64, seed=0):
    """'Catastrophic forgetting' baseline: keep training on D_r and hope D_f fades away."""
    t0 = time.perf_counter()
    m = fit(clone(model), X_retain, y_retain, epochs=epochs, lr=lr, batch_size=batch_size, seed=seed)
    return m, _info(t0, epochs * len(X_retain))


def gradient_ascent(model, X_forget, y_forget, epochs=5, lr=1e-4, batch_size=32, seed=0,
                    history=None):
    """
    Climb the loss on D_f: the gradient of cross-entropy, with its sign FLIPPED.
    Unbounded - run it too long and the whole model collapses (notebook 05 shows it).
    Pass `history=callable(model)` to record something after every epoch.
    """
    t0 = time.perf_counter()
    m = clone(model)
    Xf, yf = _f32(X_forget), np.asarray(y_forget)
    rng, opt, processed = np.random.default_rng(seed), Adam(m.params, lr=lr), 0
    for _ in range(epochs):
        for b in batches(len(Xf), batch_size, rng):
            _, g = cross_entropy(m.forward(Xf[b], keep_cache=True), yf[b])
            opt.step(m.backward(-g))                                # <- the minus sign IS the method
            processed += len(b)
        if history is not None:
            history(m)
    return m, _info(t0, processed)


def neggrad_plus(model, X_retain, y_retain, X_forget, y_forget, epochs=5, alpha=0.9, lr=1e-4,
                 batch_size=64, seed=0):
    """Descent on D_r and ascent on D_f in every step:  loss = alpha*L_r - (1-alpha)*L_f."""
    t0 = time.perf_counter()
    m = clone(model)
    Xr, yr, Xf, yf = _f32(X_retain), np.asarray(y_retain), _f32(X_forget), np.asarray(y_forget)
    rng, opt, processed = np.random.default_rng(seed), Adam(m.params, lr=lr), 0
    fb = max(1, batch_size * len(Xf) // max(1, len(Xr)))
    for _ in range(epochs):
        for b in batches(len(Xr), batch_size, rng):
            bf = rng.integers(0, len(Xf), fb)
            _, g_r = cross_entropy(m.forward(Xr[b], keep_cache=True), yr[b])
            grads_r = m.backward(alpha * g_r)
            _, g_f = cross_entropy(m.forward(Xf[bf], keep_cache=True), yf[bf])
            grads_f = m.backward(-(1 - alpha) * g_f)
            opt.step([a + c for a, c in zip(grads_r, grads_f)])
            processed += len(b) + fb
    return m, _info(t0, processed)


# --------------------------------------------------------------------------------------------
# SCRUB  (Kurmanji, Triantafillou, Hayes & Triantafillou, NeurIPS 2023)
# --------------------------------------------------------------------------------------------

def scrub(teacher, X_retain, y_retain, X_forget, steps=8, max_steps=4, alpha=1.0, gamma=1.0,
          lr=1e-3, T=4.0, batch_size=64, forget_batch_size=8, seed=0, return_checkpoints=False,
          history=None):
    """
    SCRUB, Algorithm 1 of the paper. The student starts as a copy of the teacher (θ_o).
    For `steps` epochs:
        if epoch < max_steps:   MAX epoch over D_f  ->  maximise KL(teacher || student)
        always:                 MIN epoch over D_r  ->  minimise alpha*KL + gamma*CE
    The last (steps - max_steps) epochs are min-only: they repair damage to D_r.

    Paper, Eq. 3:   min_w  alpha/N_r Σ_r d(x_r; w) + gamma/N_r Σ_r CE(x_r) - 1/N_f Σ_f d(x_f; w)
    """
    t0 = time.perf_counter()
    student = clone(teacher)
    Xr, yr, Xf = _f32(X_retain), np.asarray(y_retain), _f32(X_forget)
    t_r, t_f = teacher(Xr), teacher(Xf)                             # the teacher never changes
    rng, opt = np.random.default_rng(seed), Adam(student.params, lr=lr)
    processed, checkpoints = 0, []
    for epoch in range(steps):
        if epoch < max_steps:                                       # ---- MAX step on D_f
            for b in batches(len(Xf), forget_batch_size, rng):
                _, g = distill_kl(student.forward(Xf[b], keep_cache=True), t_f[b], T)
                opt.step(student.backward(-g))                      # ascend the KL
                processed += len(b)
        for b in batches(len(Xr), batch_size, rng):                # ---- MIN step on D_r
            out = student.forward(Xr[b], keep_cache=True)
            _, g_kl = distill_kl(out, t_r[b], T)
            _, g_ce = cross_entropy(out, yr[b])
            opt.step(student.backward(alpha * g_kl + gamma * g_ce))
            processed += len(b)
        if return_checkpoints:
            checkpoints.append(clone(student))
        if history is not None:
            history(student, epoch, "max+min" if epoch < max_steps else "min")
    info = _info(t0, processed)
    if return_checkpoints:
        info["checkpoints"] = checkpoints
    return student, info


def _error(model, X, y):
    return float((predict_proba(model, X).argmax(1) != np.asarray(y)).mean())


def scrub_rewind(teacher, X_retain, y_retain, X_forget, y_forget, X_val_like_forget,
                 y_val_like_forget, **scrub_kwargs):
    """
    SCRUB+R (paper, Section 3.2) - protect against membership inference by NOT over-forgetting.
      1. run SCRUB, keeping a checkpoint after every epoch;
      2. measure the final model's error on a validation set from the same distribution as D_f
         (never trained on): the error a model that never saw D_f 'should' have;
      3. rewind to the checkpoint whose error on D_f is closest to that reference.
    """
    student, info = scrub(teacher, X_retain, y_retain, X_forget, return_checkpoints=True,
                          **scrub_kwargs)
    reference = _error(student, X_val_like_forget, y_val_like_forget)
    errs = [_error(c, X_forget, y_forget) for c in info["checkpoints"]]
    best = int(np.argmin([abs(e - reference) for e in errs]))
    chosen = info.pop("checkpoints")[best]
    info.update(reference_error=reference, forget_error_per_checkpoint=errs, chosen_checkpoint=best)
    return chosen, info


# --------------------------------------------------------------------------------------------
# Bad Teacher  (Chundawat, Tarun, Mandal & Kankanhalli, AAAI 2023)
# --------------------------------------------------------------------------------------------

def bad_teacher(teacher, model_fn, X_retain, X_forget, retain_fraction=0.3, epochs=1, lr=1e-3,
                T=1.0, batch_size=64, seed=0):
    """
    Two teachers, one student (paper, Eq. 3):
        L(x, l_u) = (1 - l_u) · KL(T_s(x) || S(x))  +  l_u · KL(T_d(x) || S(x))
    l_u = 1 for forget samples -> copy the incompetent, randomly-initialised teacher T_d
    l_u = 0 for retain samples -> copy the competent, original teacher T_s
    The paper uses ~30% of D_r and one epoch - that is what makes it fast.
    """
    t0 = time.perf_counter()
    set_seed(seed)
    bad = model_fn()                                                # random weights = incompetent
    student = clone(teacher)
    rng = np.random.default_rng(seed)
    Xr = _f32(X_retain)
    keep = rng.choice(len(Xr), size=max(1, int(retain_fraction * len(Xr))), replace=False)
    X = np.concatenate([Xr[keep], _f32(X_forget)])
    lu = np.r_[np.zeros(len(keep), bool), np.ones(len(X_forget), bool)]
    target = np.where(lu[:, None], bad(X), teacher(X))              # whose logits to copy, per row
    opt, processed = Adam(student.params, lr=lr), 0
    for _ in range(epochs):
        for b in batches(len(X), batch_size, rng):
            _, g = distill_kl(student.forward(X[b], keep_cache=True), target[b], T)
            opt.step(student.backward(g))
            processed += len(b)
    return student, _info(t0, processed, incompetent_teacher=bad)


# --------------------------------------------------------------------------------------------
# The method zoo (Problem 19): six more methods from the literature
# --------------------------------------------------------------------------------------------

def _wrong_labels(y, n_classes, rng):
    """A random label for every row, never the true one."""
    y = np.asarray(y)
    return (y + rng.integers(1, n_classes, len(y))) % n_classes


def random_label(model, X_retain, y_retain, X_forget, y_forget, epochs=5, lr=1e-3, batch_size=64,
                 n_classes=10, mask=None, seed=0):
    """
    Random relabelling (Graves, Nagisetty & Ganesh, AAAI 2021, 'Amnesiac Machine Learning').
    Give every forget example a random WRONG label and keep training on D_r plus the relabelled D_f.
    The wrong labels pull the model away from what it learned about D_f; D_r holds everything else in place.
    `mask` (one 0/1 array per parameter) freezes the weights where it is 0 - that is SalUn, below.
    """
    t0 = time.perf_counter()
    m = clone(model)
    rng = np.random.default_rng(seed)
    X = np.concatenate([_f32(X_retain), _f32(X_forget)])
    is_f = np.r_[np.zeros(len(X_retain), bool), np.ones(len(X_forget), bool)]
    opt, processed = Adam(m.params, lr=lr), 0
    for _ in range(epochs):
        y = np.r_[np.asarray(y_retain), _wrong_labels(y_forget, n_classes, rng)]   # new wrong labels each epoch
        for b in batches(len(X), batch_size, rng):
            _, g = cross_entropy(m.forward(X[b], keep_cache=True), y[b])
            grads = m.backward(g)
            if mask is not None:
                grads = [gr * mk for gr, mk in zip(grads, mask)]
            opt.step(grads)
            processed += len(b)
    return m, _info(t0, processed)


def saliency_mask(model, X_forget, y_forget, keep=0.5):
    """The `keep` share of weights with the largest gradient on the forget loss (SalUn's weight saliency)."""
    _, g = cross_entropy(model.forward(_f32(X_forget), keep_cache=True), y_forget)
    grads = [np.abs(gr) for gr in model.backward(g)]
    cut = np.quantile(np.concatenate([gr.ravel() for gr in grads]), 1 - keep)
    return [(gr >= cut).astype(np.float32) for gr in grads]


def salun(model, X_retain, y_retain, X_forget, y_forget, keep=0.5, **kw):
    """
    SalUn (Fan, Liu, Zhang, Wei, Wong & Liu, ICLR 2024).
    1. Find the weights that matter most for the forget data: largest |gradient of the loss on D_f|.
    2. Run random relabelling, but only let those 'salient' weights move. The rest of the model is frozen.
    """
    t0 = time.perf_counter()
    mask = saliency_mask(model, X_forget, y_forget, keep)
    m, info = random_label(model, X_retain, y_retain, X_forget, y_forget, mask=mask, **kw)
    info["seconds"] = time.perf_counter() - t0
    info["samples_processed"] += len(X_forget)
    info["share_of_weights_moved"] = float(sum(mk.sum() for mk in mask) / sum(mk.size for mk in mask))
    return m, info


def l1_sparse(model, X_retain, y_retain, epochs=5, lr=1e-3, gamma=5e-4, batch_size=64, seed=0):
    """
    L1-sparse fine-tuning (Jia, Liu, Ram, Yao, Liu, Liu, Sharma & Liu, NeurIPS 2023).
    Fine-tune on D_r with an extra L1 penalty  gamma·Σ|θ|  that pushes small weights to zero, with gamma
    decaying linearly to 0. The idea: a sparser model has fewer places left to store a memorised example.
    """
    t0 = time.perf_counter()
    m = clone(model)
    Xr, yr = _f32(X_retain), np.asarray(y_retain)
    rng, opt, processed = np.random.default_rng(seed), Adam(m.params, lr=lr), 0
    n_steps = epochs * int(np.ceil(len(Xr) / batch_size))
    step = 0
    for _ in range(epochs):
        for b in batches(len(Xr), batch_size, rng):
            g_now = gamma * (1 - step / n_steps)
            _, g = cross_entropy(m.forward(Xr[b], keep_cache=True), yr[b])
            opt.step([gr + g_now * np.sign(p) for gr, p in zip(m.backward(g), m.params)])
            processed, step = processed + len(b), step + 1
    return m, _info(t0, processed)


def unsir(model, X_retain, y_retain, X_forget, y_forget, noise_per_class=16, noise_steps=50, noise_lr=0.1,
          lam=0.1, retain_fraction=0.3, lr=1e-3, batch_size=64, seed=0):
    """
    UNSIR (Tarun, Chundawat, Mandal & Kankanhalli, IEEE TNNLS 2023), adapted from whole classes to any forget set.
    1. Learn NOISE images that the model gets as wrong as possible for each label in D_f
       (gradient ascent on the loss, with respect to the input, plus a small penalty lam·‖noise‖²).
    2. Impair: one epoch on that noise (with those labels) mixed with a sample of D_r. This damages what the
       model knows about those labels.
    3. Repair: one epoch on the D_r sample alone, to win back accuracy everywhere else.
    It never trains on D_f itself: only the labels of D_f are used.
    """
    t0 = time.perf_counter()
    m = clone(model)
    rng = np.random.default_rng(seed)
    labels = np.unique(y_forget)
    yn = np.repeat(labels, noise_per_class)
    N = rng.normal(0, 1, (len(yn), m.sizes[0])).astype(np.float32)
    nopt = Adam([N], lr=noise_lr)
    for _ in range(noise_steps):                                    # step 1: error-maximising noise
        _, g = cross_entropy(m.forward(N, keep_cache=True), yn)
        nopt.step([-m.input_gradient(g) + lam * N / len(N)])       # minus sign: climb the loss
    Xr, yr = _f32(X_retain), np.asarray(y_retain)
    keep = rng.choice(len(Xr), max(1, int(retain_fraction * len(Xr))), replace=False)
    opt, processed = Adam(m.params, lr=lr), noise_steps * len(N)
    X_imp, y_imp = np.concatenate([N, Xr[keep]]), np.r_[yn, yr[keep]]
    for b in batches(len(X_imp), batch_size, rng):                  # step 2: impair
        _, g = cross_entropy(m.forward(X_imp[b], keep_cache=True), y_imp[b])
        opt.step(m.backward(g))
        processed += len(b)
    for b in batches(len(keep), batch_size, rng):                   # step 3: repair
        _, g = cross_entropy(m.forward(Xr[keep][b], keep_cache=True), yr[keep][b])
        opt.step(m.backward(g))
        processed += len(b)
    return m, _info(t0, processed, noise=N)


def fisher_importance(model, X, y, batch_size=256):
    """Mean squared per-example gradient of the loss for every weight: how much each weight 'matters' for (X, y)."""
    X, y = _f32(X), np.asarray(y)
    total = [np.zeros_like(p) for p in model.params]
    for start in range(0, len(X), batch_size):
        xb, yb = X[start:start + batch_size], y[start:start + batch_size]
        _, g = cross_entropy(model.forward(xb, keep_cache=True), yb)
        for t, s in zip(total, model.squared_grads(g * len(yb))):  # undo the 1/batch to get per-example gradients
            t += s
    return [t / len(X) for t in total]


def ssd(model, X_train, y_train, X_forget, y_forget, alpha=10.0, lam=1.0):
    """
    Selective Synaptic Dampening (Foster, Schoepf & Brintrup, AAAI 2024). No training at all.
    For every weight, compare how much it matters for the forget data (I_f) with how much it matters for
    the whole training set (I_D), both measured by the diagonal of the Fisher information.
    A weight that matters MUCH more for D_f (I_f > alpha·I_D) is shrunk:  θ ← θ · min(lam·I_D / I_f, 1).
    """
    t0 = time.perf_counter()
    m = clone(model)
    I_D, I_f = fisher_importance(m, X_train, y_train), fisher_importance(m, X_forget, y_forget)
    hit = 0
    for p, d, f in zip(m.params, I_D, I_f):
        sel = f > alpha * d
        p[sel] *= np.minimum(lam * d[sel] / f[sel], 1.0)
        hit += int(sel.sum())
    return m, _info(t0, len(X_train) + len(X_forget), share_of_weights_dampened=hit / m.n_params())


def last_layer(model, X_retain, y_retain, lam=1.0):
    """
    A model-intrinsic method for softmax classifiers, in the spirit of certified removal (Guo, Goldstein,
    Hannun & van der Maaten, ICML 2020): keep the hidden layers, and re-solve ONLY the last layer exactly,
    on D_r, as a convex softmax regression (Newton's method, Problem 2). The last layer is then exactly what
    it would be without D_f - but the hidden layers, which also learned from D_f, are untouched.
    """
    from .classical import SoftmaxNewton
    t0 = time.perf_counter()
    m = clone(model)
    head = SoftmaxNewton(lam).fit(m.features(_f32(X_retain)).astype(np.float64), np.asarray(y_retain),
                                  n_classes=m.sizes[-1])
    w = head.w.reshape(-1, m.sizes[-1])                             # (features + 1 bias row, classes)
    m.params[-2], m.params[-1] = w[:-1].astype(np.float32), w[-1].astype(np.float32)
    return m, _info(t0, head.n_iter * len(X_retain), newton_iterations=head.n_iter)
