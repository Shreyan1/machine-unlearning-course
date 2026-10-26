# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""Tiny SVG toolkit for the site's diagrams.

Every diagram is drawn with classes (d-box, d-blue, d-line ...) that brand.css colours from the
site's theme variables, so it is see-through and follows light and dark mode.
"""

import html
import re

_SUB = re.compile(r"_\{([^}]+)\}|_(\w)")


def esc(s):
    """Escape diagram text, capitalize its opening word, and render subscripts."""
    s = str(s)
    s = re.sub(r'^(\s*["\'“‘([{]*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), s)
    return _SUB.sub(lambda m: f'<tspan style="baseline-shift:sub;font-size:72%">{m.group(1) or m.group(2)}</tspan>',
                    html.escape(s, quote=False))


# The course's symbols, typeset by MathJax when they appear in a caption. A bare "D" only counts
# when the caption also uses the subscripted sets, so ordinary words are left alone.
_SYMBOL = re.compile(r"(?<![\w\\])(D_test|D_f|D_r|θ_o|θ_r|θ_u)(?![\w])")
_BARE_D = re.compile(r"(?<![\w\\(])D(?![\w])")
_TEX = {"D_test": r"D_{\text{test}}", "θ_o": r"\theta_o", "θ_r": r"\theta_r", "θ_u": r"\theta_u"}


def _math(text):
    if not _SYMBOL.search(text):
        return text
    text = _SYMBOL.sub(lambda m: f"\x00{m.group(1)}\x00", text)
    text = _BARE_D.sub("\x00D\x00", text)
    return re.sub("\x00([^\x00]+)\x00", lambda m: f'<span class="arithmatex">\\({_TEX.get(m.group(1), m.group(1))}\\)</span>', text)


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.parts = w, h, []

    # ---- primitives ---------------------------------------------------------
    def raw(self, s):
        self.parts.append(s)

    def text(self, x, y, s, cls="d-t", anchor="middle"):
        """One line, or several lines when `s` is a list. y is the first baseline."""
        lines = s if isinstance(s, (list, tuple)) else [s]
        for i, line in enumerate(lines):
            self.parts.append(f'<text class="{cls}" x="{x}" y="{y + i * 16}" text-anchor="{anchor}">{esc(line)}</text>')

    def box(self, x, y, w, h, label="", cls="", sub=None, r=3, define=False):
        self.parts.append(f'<rect class="d-box {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>')
        lines = label if isinstance(label, (list, tuple)) else ([label] if label else [])
        subs = sub if isinstance(sub, (list, tuple)) else ([sub] if sub else [])
        if define and subs:
            subs = ["→ " + subs[0]] + list(subs[1:])
        total = len(lines) * 16 + len(subs) * 14
        y0 = y + (h - total) / 2 + 12
        for i, line in enumerate(lines):
            self.parts.append(f'<text class="d-t d-b" x="{x + w / 2}" y="{y0 + i * 16}" text-anchor="middle">{esc(line)}</text>')
        for i, line in enumerate(subs):
            self.parts.append(f'<text class="d-s" x="{x + w / 2}" y="{y0 + len(lines) * 16 + i * 14}" text-anchor="middle">{esc(line)}</text>')

    def circle(self, cx, cy, r, cls=""):
        self.parts.append(f'<circle class="d-dot {cls}" cx="{cx}" cy="{cy}" r="{r}"/>')

    def line(self, x1, y1, x2, y2, cls=""):
        self.parts.append(f'<line class="d-line {cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    def arrow(self, x1, y1, x2, y2, cls="", label=None, lx=None, ly=None):
        head = "ab" if "blue" in cls else "ar" if "bad" in cls else "a"
        self.parts.append(f'<line class="d-line {cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#{{id}}-{head})"/>')
        if label:
            self.text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 - 6, label, "d-s")

    def path(self, d, cls="", arrow=False):
        head = "ab" if "blue" in cls else "ar" if "bad" in cls else "a"
        mk = f' marker-end="url(#{{id}}-{head})"' if arrow else ""
        self.parts.append(f'<path class="d-line {cls}" d="{d}" fill="none"{mk}/>')

    def poly(self, pts, cls=""):
        p = " ".join(f"{x},{y}" for x, y in pts)
        self.parts.append(f'<polyline class="d-line {cls}" points="{p}" fill="none"/>')

    def dots(self, pts, r=4, cls=""):
        for x, y in pts:
            self.circle(x, y, r, cls)

    def flow(self, labels, x, y, w, h, gap, classes=None, subs=None):
        """A row of boxes joined by arrows. Returns the centre x of each box."""
        centres = []
        for i, lab in enumerate(labels):
            bx = x + i * (w + gap)
            self.box(bx, y, w, h, lab, (classes or [""] * len(labels))[i], (subs or [None] * len(labels))[i])
            centres.append(bx + w / 2)
            if i:
                self.arrow(bx - gap + 3, y + h / 2, bx - 3, y + h / 2)
        return centres

    def axes(self, x0, y0, x1, y1, xlabel, ylabel, xdy=30):
        """An x axis along y0 and a y axis up x0, each with an arrow head and a label."""
        self.arrow(x0, y0, x1, y0, "thin")
        self.text((x0 + x1) / 2, y0 + xdy, xlabel, "d-s")
        if not ylabel:
            return
        self.arrow(x0, y0, x0, y1, "thin")
        cy = (y0 + y1) / 2
        self.parts.append(f'<text class="d-s" transform="translate({x0 - 14},{cy}) rotate(-90)" text-anchor="middle">{esc(ylabel)}</text>')

    def legend(self, items):
        """A key under the diagram. items: (kind, cls, text); kind is box, line, dash, dot, bar or arrow."""
        widths = [34 + len(t) * 6.3 + 22 for _, _, t in items]
        total = sum(widths) - 22
        if total > self.w - 20:                                   # too wide: two rows
            half = (len(items) + 1) // 2
            self._legend_row(items[:half], self.h + 10); self._legend_row(items[half:], self.h + 34)
            self.h += 56
            return
        self._legend_row(items, self.h + 10)
        self.h += 34

    def _legend_row(self, items, y):
        widths = [34 + len(t) * 6.3 + 22 for _, _, t in items]
        x = (self.w - (sum(widths) - 22)) / 2
        for (kind, cls, text), w in zip(items, widths):
            cy = y + 8
            if kind == "box":
                self.parts.append(f'<rect class="d-box {cls}" x="{x}" y="{cy - 6}" width="20" height="13" rx="2"/>')
            elif kind == "bar":
                self.parts.append(f'<rect class="d-box {cls}" x="{x + 3}" y="{cy - 6}" width="14" height="13" rx="1"/>')
            elif kind in ("line", "dash", "arrow"):
                extra = " thick" if kind == "line" else " dash" if kind == "dash" else ""
                mk = ' marker-end="url(#{id}-a)"' if kind == "arrow" else ""
                self.parts.append(f'<line class="d-line {cls}{extra}" x1="{x}" y1="{cy}" x2="{x + 22}" y2="{cy}"{mk}/>')
            elif kind == "dot":
                self.parts.append(f'<circle class="d-dot {cls}" cx="{x + 10}" cy="{cy}" r="5.5"/>')
            self.parts.append(f'<text class="d-s" x="{x + 30}" y="{cy + 4}">{esc(text)}</text>')
            x += w

    def label(self, x, y, s, anchor="middle"):
        self.text(x, y, s, "d-s", anchor)

    # ---- output -------------------------------------------------------------
    def render(self, name, title, caption=None):
        defs = "".join(
            f'<marker id="{{id}}-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path class="d-head {c}" d="M0,1 L10,5 L0,9 z"/></marker>'
            for k, c in (("a", ""), ("ab", "d-head-blue"), ("ar", "d-head-bad")))
        body = "".join(self.parts).replace("{id}", f"d-{name}")
        defs = defs.replace("{id}", f"d-{name}")
        display_title = re.sub(r'^(\s*["\'“‘([{]*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), title)
        svg = (f'<svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{html.escape(display_title)}" xmlns="http://www.w3.org/2000/svg">'
               f'<title>{html.escape(display_title, quote=False)}</title><defs>{defs}</defs>{body}</svg>')
        display_caption = caption or ""
        display_caption = re.sub(r'^(\s*["\'“‘([{]*)([a-z])', lambda m: m.group(1) + m.group(2).upper(), display_caption)
        cap = (f'<figcaption><span class="diagram__n">Figure {{n}}</span> <b>{html.escape(display_title, quote=False)}.</b> '
               f'{_math(html.escape(display_caption, quote=False))}</figcaption>')
        return f'<figure class="diagram"><div class="diagram__box">{svg}</div>{cap}</figure>'
