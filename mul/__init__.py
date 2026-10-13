"""
mul - a small, readable Machine UnLearning toolkit used by the notebooks in this repo.

Every function here is introduced and explained in a notebook first. The package exists so that
later notebooks can reuse the exact same code instead of copy-pasting it.

    mul.classical     exact / near-exact unlearning for k-NN, Naive Bayes, ridge, logistic, forests, SVM -> Problems 1-3
    mul.nn            NumPy MLP, Adam, softmax / KL losses, LoRA adapters                         -> Problems 4, 15
    mul.train         training loop, predictions, per-example losses, cloning                      -> Problem 4 onwards
    mul.lab           the Carol / class / random digit scenarios                                   -> Problems 4-11
    mul.methods       retrain, SISA, fine-tune, gradient ascent, NegGrad+, SCRUB(+R), Bad Teacher  -> Problems 6-10
    mul.audit         membership inference, U-LiRA, gold band, relearn test, the gate              -> Problems 5, 6, 11
    mul.lm            n-gram and neural character LMs, exposure, NPO                               -> Problem 16
    mul.recsys        item-kNN (exact unlearning), implicit ALS, 'also watched' lists, diff attack -> Problem 18
    mul.data          small datasets (sklearn built-ins, Hugging Face, MovieLens)                  -> Problems 12-18
    mul.viz           consistent plot style + the diagram helpers                                  -> everywhere
    mul.torch_models  OPTIONAL PyTorch models (not imported here)                                  -> Problem 16b
"""

from . import audit, classical, data, lab, lm, methods, nn, recsys, train, viz  # noqa: F401

__version__ = "1.0.0"
