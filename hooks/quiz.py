"""MkDocs hook: turn ```quiz fences into clickable quizzes.

A quiz is written in Markdown as a YAML list inside a fenced block:

    ```quiz
    - q: Carol's rows are deleted from the database. What happens to the model?
      options: [Nothing changes, It forgets her at once]
      answer: 0
      why: The weights were already trained on her digits.
    ```

The block may also be a mapping with a `title` and a `questions` list. The hook
checks every question at build time, so a broken quiz stops the build instead
of reaching a reader. `docs/javascripts/quiz.js` makes the HTML interactive.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

import yaml

FENCE = re.compile(r"^```quiz[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
KEYS = "ABCDEFGH"


class QuizError(ValueError):
    pass


def parse(text: str, where: str = "quiz") -> tuple[str, list[dict]]:
    """Read one quiz block. Returns (title, questions) or raises QuizError."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as err:
        raise QuizError(f"{where}: not valid YAML ({err})") from err
    title = "Quick quiz"
    if isinstance(data, dict):
        title = str(data.get("title", title))
        data = data.get("questions")
    if not isinstance(data, list) or not data:
        raise QuizError(f"{where}: expected a non-empty list of questions")
    questions = []
    for n, item in enumerate(data, 1):
        at = f"{where}, question {n}"
        if not isinstance(item, dict):
            raise QuizError(f"{at}: each question must be a mapping")
        missing = [k for k in ("q", "options", "answer", "why") if k not in item]
        if missing:
            raise QuizError(f"{at}: missing {', '.join(missing)}")
        options = item["options"]
        if not isinstance(options, list) or not 2 <= len(options) <= len(KEYS):
            raise QuizError(f"{at}: options must be a list of 2 to {len(KEYS)} answers")
        answer = item["answer"]
        if not isinstance(answer, int) or isinstance(answer, bool) or not 0 <= answer < len(options):
            raise QuizError(f"{at}: answer must be an option number from 0 to {len(options) - 1}")
        questions.append({"q": str(item["q"]), "options": [str(o) for o in options],
                          "answer": answer, "why": str(item["why"])})
    return title, questions


def find_quizzes(markdown: str) -> list[str]:
    return [m.group(1) for m in FENCE.finditer(markdown)]


def _inline(text: str, md) -> str:
    """Render a short piece of Markdown (bold, code, links) without the <p> wrapper."""
    md.reset()
    out = md.convert(text).strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        out = out[3:-4]
    return out


def render(title: str, questions: list[dict], quiz_id: str, md) -> str:
    parts = [f'<div class="quiz" data-quiz-id="{html.escape(quiz_id)}" data-total="{len(questions)}">',
             '<div class="quiz__head">'
             f'<span class="quiz__label">{html.escape(title)}</span>'
             f'<span class="quiz__count">{len(questions)} question{"s" if len(questions) != 1 else ""}</span>'
             '</div>',
             '<ol class="quiz__list">']
    for q in questions:
        parts.append(f'<li class="quiz__q" data-answer="{q["answer"]}">')
        parts.append(f'<div class="quiz__text">{_inline(q["q"], md)}</div>')
        parts.append('<div class="quiz__options">')
        for i, opt in enumerate(q["options"]):
            parts.append(f'<button type="button" class="quiz__opt" data-i="{i}">'
                         f'<span class="quiz__key">{KEYS[i]}</span>'
                         f'<span class="quiz__opt-text">{_inline(opt, md)}</span></button>')
        parts.append('</div>')
        parts.append(f'<div class="quiz__why" hidden><span class="quiz__verdict"></span> {_inline(q["why"], md)}</div>')
        parts.append('</li>')
    parts.append('</ol>')
    parts.append('<div class="quiz__foot">'
                 f'<span class="quiz__score" aria-live="polite">0 of {len(questions)} answered</span>'
                 '<button type="button" class="quiz__reset">Try again</button>'
                 '</div></div>')
    return "\n".join(parts)


# ---- MkDocs events -------------------------------------------------------------

_index: list[dict] = []


def on_nav(nav, config, files):
    """Count the quizzes on every page so the quiz hub can list them."""
    _index.clear()
    for item, sections in _walk(nav.items, []):
        if not item.is_page or item.file is None:
            continue
        text = Path(item.file.abs_src_path).read_text(encoding="utf-8")
        blocks = find_quizzes(text)
        if blocks and not item.file.src_uri.startswith("quizzes/"):
            total = sum(len(parse(b, item.file.src_uri)[1]) for b in blocks)
            _index.append({"section": " · ".join(sections) or "Home", "title": item.title or _title(text),
                           "page": item.file, "quizzes": len(blocks), "questions": total})
    return nav


def _walk(items, sections):
    for item in items:
        if item.is_section:
            yield from _walk(item.children, sections + [item.title])
        else:
            yield item, sections


def _title(text: str) -> str:
    """A section's index page has no title in the nav; use its front-matter title."""
    m = re.search(r"^title:\s*(.+)$", text, re.M) or re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else "Overview"


def on_page_markdown(markdown, page, config, files):
    import markdown as mdlib

    md = mdlib.Markdown(extensions=["pymdownx.inlinehilite", "pymdownx.betterem", "attr_list"])
    count = 0

    def replace(match):
        nonlocal count
        title, questions = parse(match.group(1), page.file.src_uri)
        quiz_id = f"{page.file.src_uri}#{count}"
        count += 1
        return "\n" + render(title, questions, quiz_id, md) + "\n"

    markdown = FENCE.sub(replace, markdown)
    if "<!-- quiz-index -->" in markdown:
        markdown = markdown.replace("<!-- quiz-index -->", _index_markdown(page))
    return markdown


def _index_markdown(page) -> str:
    rows, section = [], None
    for entry in _index:
        if entry["section"] != section:
            section = entry["section"]
            rows.append(f"\n### {section}\n\n| Page | Questions | Your score |\n|---|---|---|")
        link = _relative(page.file.src_uri, entry["page"].src_uri)
        rows.append(f'| [{entry["title"]}]({link}) | {entry["questions"]} | '
                    f'<span class="quiz-score" data-page="{html.escape(entry["page"].src_uri)}">not started</span> |')
    return "\n".join(rows) + "\n"


def _relative(from_uri: str, to_uri: str) -> str:
    import posixpath
    return posixpath.relpath(to_uri, posixpath.dirname(from_uri) or ".")
