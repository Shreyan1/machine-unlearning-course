"""
OPTIONAL PyTorch models (requirements-optional.txt). The core course is pure NumPy (mul.nn); these
exist for Problem 16b, which repeats the LLM-unlearning lesson with a small transformer, and for
readers who want to port earlier problems to PyTorch.

Tiny on purpose: small enough to retrain from scratch in seconds, so the *gold standard* (retrain
without the forgotten data) can always be computed and every unlearning method checked against it.
"""

import torch
import torch.nn as nn


class MLP(nn.Module):
    """A plain fully-connected classifier. Used for tabular data and flattened images."""

    def __init__(self, n_in: int, n_classes: int, hidden=(256, 256), dropout: float = 0.0):
        super().__init__()
        layers, d = [], n_in
        for h in hidden:
            layers += [nn.Linear(d, h), nn.ReLU()]
            if dropout:
                layers.append(nn.Dropout(dropout))
            d = h
        layers.append(nn.Linear(d, n_classes))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


class SmallCNN(nn.Module):
    """A two-block CNN for small grayscale images (e.g. 32x32 or 64x64 faces)."""

    def __init__(self, n_classes: int, side: int = 32, channels=(16, 32)):
        super().__init__()
        c1, c2 = channels
        self.side = side
        self.features = nn.Sequential(
            nn.Conv2d(1, c1, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(c1, c2, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.head = nn.Linear(c2 * (side // 4) ** 2, n_classes)

    def forward(self, x):
        x = x.view(-1, 1, self.side, self.side)
        return self.head(self.features(x).flatten(1))


class TinyCharLM(nn.Module):
    """
    A miniature GPT-style character-level language model (2 transformer blocks).

    Used in Problem 16b to show, at laptop scale, the same memorisation and unlearning behaviour
    that large language models exhibit.
    """

    def __init__(self, vocab_size: int, context: int = 64, d_model: int = 128, n_heads: int = 4,
                 n_layers: int = 2, dropout: float = 0.0):
        super().__init__()
        self.context = context
        self.tok = nn.Embedding(vocab_size, d_model)
        self.pos = nn.Embedding(context, d_model)
        block = nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout,
                                           batch_first=True, norm_first=True, activation="gelu")
        self.blocks = nn.TransformerEncoder(block, n_layers, enable_nested_tensor=False)
        self.ln = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size)
        mask = torch.triu(torch.full((context, context), float("-inf")), diagonal=1)
        self.register_buffer("causal_mask", mask)

    def forward(self, idx):
        T = idx.shape[1]
        x = self.tok(idx) + self.pos(torch.arange(T, device=idx.device))
        x = self.blocks(x, mask=self.causal_mask[:T, :T], is_causal=True)
        return self.head(self.ln(x))
