"""MkDocs hook: show PRACTICE.md on the website's Practice page.

PRACTICE.md stays the single source. The page `docs/practice.md` holds a
`<!-- practice -->` marker that this hook replaces with the file's content,
minus its own top heading, and with " :" tidied to ":" for the site's style.
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
    text = re.sub(r"(\S) :(\s)", r"\1:\2", text)           # "Hint :" -> "Hint:"
    text = re.sub(r"(\S) :\*\*\n(?=- )", r"\1:**\n\n", text)     # a list needs a blank line before it
    for emoji, level in LEVELS.items():                    # round emoji -> the site's coloured squares
        text = text.replace(emoji + " ", f'<span class="lvl lvl--{level}"></span>')
    return markdown.replace(MARKER, text)
