"""
Checks for the website's quizzes (docs/).

    python -m pytest tests -q        (or simply: python tests/test_docs.py)

Every ```quiz block must parse, have 2 to 8 options, a valid answer and a "why".
Needs only PyYAML; the full site build is `mkdocs build --strict`.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "hooks"))
import citations  # noqa: E402
import quiz  # noqa: E402


def test_every_quiz_parses():
    pages = sorted((ROOT / "docs").rglob("*.md"))
    assert pages, "no pages found under docs/"
    count = 0
    for page in pages:
        for block in quiz.find_quizzes(page.read_text(encoding="utf-8")):
            _, questions = quiz.parse(block, str(page.relative_to(ROOT)))
            count += len(questions)
    assert count > 0, "no quiz questions found"


def test_bad_quiz_is_rejected():
    for bad in ["- q: x\n  options: [a, b]\n  answer: 2\n  why: y",
                "- q: x\n  options: [a]\n  answer: 0\n  why: y",
                "- q: x\n  options: [a, b]\n  answer: 0",
                "[]"]:
        try:
            quiz.parse(bad)
        except quiz.QuizError:
            continue
        raise AssertionError(f"accepted a broken quiz: {bad!r}")


def test_citations_link_prose_only():
    md = ("# Heading with Cao and Yang (2015)\n\n"
          "As Cao and Yang (2015) showed, and later GDPR Art. 17 says.\n\n"
          "`Cao and Yang (2015)` in code, and [already linked](https://example.org) Cao and Yang.\n\n"
          "```quiz\n- q: Cao and Yang?\n```\n")
    out = citations.on_page_markdown(md, None, None, None)
    assert out.startswith("# Heading with Cao and Yang (2015)\n"), "headings must stay untouched"
    assert "[Cao and Yang (2015)](https://www.ieee-security.org" in out
    assert "[GDPR Art. 17](https://gdpr-info.eu/art-17-gdpr/)" in out
    assert "`Cao and Yang (2015)`" in out and "- q: Cao and Yang?" in out
    assert out.count("](https://www.ieee-security.org") == 2, "prose mentions after the heading are linked"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok ", name)
    print("all checks passed")
