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


def on_page_markdown(markdown, page, config, files):
    """Swap each marker for its diagram, numbered by the section it sits in (Figure 4.1, 4.2 ...)."""
    out, pos, section, in_section = [], 0, 0, 0
    fence = False
    lines = markdown.split("\n")
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            section += 1
            in_section = 0
        m = MARKER.search(line)
        if m and not fence:
            name = m.group(1)
            if name not in REGISTRY:
                raise KeyError(f"no diagram called {name!r} (page {page.file.src_uri})")
            in_section += 1
            number = f"{section}.{in_section}" if section else str(in_section)
            html = REGISTRY[name](name).replace("{n}", number)
            line = MARKER.sub(lambda _: "\n" + html + "\n", line)
        out.append(line)
    return "\n".join(out)
