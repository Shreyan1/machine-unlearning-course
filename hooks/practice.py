# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""MkDocs hook: show PRACTICE.md on the website's Practice page.

PRACTICE.md stays the single source. The page `docs/practice.md` holds a
`<!-- practice -->` marker that this hook replaces with the file's content,
minus its own top heading. Each problem's task and supporting details stay in
separate Markdown blocks so the hint, lookup and completion check are readable.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- practice -->"
LEVELS = {"🟢": "beginner", "🔵": "amateur", "🟠": "semipro", "🔴": "pro"}


def on_page_markdown(markdown, page, config, files):
    if MARKER not in markdown:
        return markdown
    text = (ROOT / "PRACTICE.md").read_text(encoding="utf-8")
    text = re.sub(r"\A#\s[^\n]*\n", "", text)              # the page already has a title
    text = re.sub(r"(?m)(\S)\n(?=- \*\*Hint\s*:)", r"\1\n\n", text)
    for emoji, level in LEVELS.items():                    # round emoji -> the site's coloured squares
        text = text.replace(emoji + " ", f'<span class="lvl lvl--{level}"></span>')
    return markdown.replace(MARKER, text)
