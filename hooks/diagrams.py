# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""MkDocs hook: inline SVG diagrams.

A page that contains `<!-- diagram: name -->` gets the diagram of that name, drawn by
hooks/diagrams_ml.py or hooks/diagrams_unlearning.py. They are inline SVG so the colours follow
the site's light and dark themes.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagrams_ml  # noqa: E402
import diagrams_unlearning  # noqa: E402

MARKER = re.compile(r"<!--\s*diagram:\s*([a-z0-9-]+)\s*-->")
REGISTRY = {**diagrams_ml.DIAGRAMS, **diagrams_unlearning.DIAGRAMS}


# Figures are numbered by the course's lesson sections (the Lessons tab), not by the page they sit
# on, so a figure keeps one number everywhere, the home page included. Within a section they follow
# the order a reader meets them in the site navigation.
CHAPTERS = [
    ("Foundations", [
        "what-is-machine-learning", "training-and-testing", "loss-functions", "gradient-descent",
        "overfitting-and-memorisation", "probabilities-and-kl-divergence",
        "what-is-machine-unlearning", "unlearning-families", "why-the-law-cares", "notation",
        "ladder-of-forgetting"]),
    ("Classical ML", [
        "k-nearest-neighbours", "naive-bayes", "linear-and-ridge-regression", "logistic-regression",
        "support-vector-machines", "decision-trees-and-random-forests", "exact-unlearning-classical"]),
    ("Neural nets, the problem", ["neural-networks", "deleting-vs-unlearning"]),
    ("Exact unlearning", ["retraining-gold-standard", "gold-band", "sisa"]),
    ("Approximate unlearning", ["approximate-unlearning", "forgetting-spectrum", "scrub", "bad-teacher", "method-zoo"]),
    ("Proof", ["membership-inference-attacks", "unlearning-audit", "testing-vs-proving"]),
    ("Responsible AI", [
        "fairness-and-erasure", "consent-and-face-recognition", "poisoning-and-backdoors",
        "fine-tuning-and-lora", "unlearning-fine-tunes", "language-models", "llm-unlearning"]),
    ("Engineering", ["enterprise-playbook"]),
    ("Extensions", ["recommender-systems", "recommender-unlearning", "unlearning-at-scale"]),
]
NUMBERS = {name: f"{ch}.{i}" for ch, (_, names) in enumerate(CHAPTERS, start=1) for i, name in enumerate(names, 1)}


def on_page_markdown(markdown, page, config, files):
    """Swap each marker for its diagram, with the figure number from CHAPTERS."""
    out, fence = [], False
    for line in markdown.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        m = MARKER.search(line)
        if m and not fence:
            name = m.group(1)
            if name not in REGISTRY:
                raise KeyError(f"no diagram called {name!r} (page {page.file.src_uri})")
            if name not in NUMBERS:
                raise KeyError(f"diagram {name!r} has no figure number; add it to CHAPTERS in hooks/diagrams.py")
            html = REGISTRY[name](name).replace("{n}", NUMBERS[name])
            line = MARKER.sub(lambda _: "\n" + html + "\n", line)
        out.append(line)
    return "\n".join(out)
