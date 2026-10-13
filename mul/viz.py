"""
One consistent visual language across all notebooks and diagrams.

Colour meaning (used everywhere, learn it once):
    ORIGINAL  grey    the model trained on everything (it has seen D_f)
    RETRAIN   green   the gold standard - retrained without D_f
    FORGET    red     the data that must be forgotten (D_f)
    RETAIN    blue    the data we keep (D_r)
    METHOD    purple  an unlearning method under test
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ORIGINAL = "#8c8c8c"
RETRAIN = "#2a9d55"
FORGET = "#d64545"
RETAIN = "#3a6fd8"
METHOD = "#7b4bc4"
ACCENT = "#e8a33d"
INK = "#222222"
PAPER = "#ffffff"

METHOD_COLORS = {
    "original": ORIGINAL, "retrain": RETRAIN, "SISA": "#1f7a8c", "finetune": "#c08a2b",
    "gradient_ascent": "#c2410c", "neggrad+": "#9d4edd", "SCRUB": METHOD, "SCRUB+R": "#5a2ea6",
    "Bad-T": "#d6457a",
}


def style():
    """Call once at the top of a notebook."""
    plt.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 150, "figure.facecolor": PAPER, "axes.facecolor": PAPER,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
        "grid.alpha": 0.25, "font.size": 10.5, "axes.titleweight": "bold", "axes.titlesize": 12,
        "legend.frameon": False,
    })


def color_for(name):
    for k, c in METHOD_COLORS.items():
        if name.lower().startswith(k.lower()):
            return c
    return METHOD


# ---------------------------------------------------------------------------------------------
# Result plots
# ---------------------------------------------------------------------------------------------

def bars_with_band(ax, table, col, band_mean=None, band_std=None, k=2.0, title=None, pct=True,
                   ylabel=None):
    """Bar per method for one metric, with the retrain gold band shaded in green."""
    names = list(table.index)
    vals = table[col].to_numpy(dtype=float) * (100 if pct else 1)
    ax.bar(range(len(names)), vals, color=[color_for(n) for n in names], edgecolor=INK, lw=0.6)
    if band_mean is not None:
        m = band_mean[col] * (100 if pct else 1)
        s = band_std[col] * (100 if pct else 1)
        ax.axhspan(m - k * s, m + k * s, color=RETRAIN, alpha=0.15, zorder=0,
                   label="gold standard band (retrain)")
        ax.axhline(m, color=RETRAIN, lw=1.5, ls="--", zorder=1)
        ax.legend(loc="lower right", fontsize=8.5)
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v:.1f}" if pct else f"{v:.3f}", ha="center", va="bottom", fontsize=8.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=25, ha="right")
    ax.set_title(title or col)
    if ylabel:
        ax.set_ylabel(ylabel)
    elif pct:
        ax.set_ylabel("%")
    return ax


# ---------------------------------------------------------------------------------------------
# Diagram primitives (used by assets/make_diagrams.py and inside notebooks)
# ---------------------------------------------------------------------------------------------

def canvas(w=10, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.set_aspect("equal")
    return fig, ax


def box(ax, x, y, w, h, text, color=RETAIN, fill_alpha=0.12, fontsize=10, bold=False,
        text_color=INK, lw=1.6, round_=0.08, ls="-"):
    """A rounded box centred at (x, y)."""
    p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0.02,rounding_size={round_}",
                       fc=_rgba(color, fill_alpha), ec=color, lw=lw, ls=ls)
    ax.add_patch(p)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=text_color,
            fontweight="bold" if bold else "normal", wrap=True)
    return p


def arrow(ax, x1, y1, x2, y2, text=None, color=INK, lw=1.5, style="-|>", fontsize=9, ls="-",
          text_offset=(0, 0.15), rad=0.0):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14, color=color,
                        lw=lw, ls=ls, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2 + text_offset[0], (y1 + y2) / 2 + text_offset[1], text,
                ha="center", va="bottom", fontsize=fontsize, color=color)
    return a


def label(ax, x, y, text, fontsize=10, color=INK, bold=False, ha="center", style="normal"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=fontsize, color=color,
            fontweight="bold" if bold else "normal", fontstyle=style)


def _rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return (r, g, b, alpha)
