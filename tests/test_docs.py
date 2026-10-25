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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok ", name)
    print("all checks passed")
