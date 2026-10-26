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
import progress  # noqa: E402
import quiz  # noqa: E402
import scenario  # noqa: E402


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
    html_p = citations.on_page_markdown('<p class="x">EDPB Opinion 28/2024</p>\n\nSee EDPB Opinion 28/2024.\n', None, None, None)
    assert html_p.startswith('<p class="x">EDPB Opinion 28/2024</p>'), "raw HTML paragraphs stay untouched"
    assert "See [EDPB Opinion 28/2024](" in html_p


def test_finishers_file_is_valid():
    progress.load_finishers(ROOT / "docs" / "finishers.yml")


def test_bad_finisher_is_rejected():
    import tempfile
    for bad in ["- name: Ada\n", "- name: Ada\n  date: 2026-10-25\n  score: 25\n",
                "- name: Ada\n  date: 2026-10-25\n  linkedin: javascript:alert(1)\n",
                "- name: ''\n  date: 2026-10-25\n",
                "- name: Ada\n  date: 2026-10-25\n  id: MU-abcd-1111\n"]:
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write(bad)
        try:
            progress.load_finishers(Path(f.name))
        except ValueError:
            continue
        raise AssertionError(f"accepted a broken finisher: {bad!r}")


def test_finisher_names_are_escaped():
    out = progress.render_finishers([{"name": "<script>x</script>", "date": __import__("datetime").date(2026, 10, 25),
                                      "score": 18, "linkedin": None, "github": None, "id": "MU-ABCD-2345"}])
    assert "<script>" not in out and "&lt;script&gt;" in out
    assert 'data-id="MU-ABCD-2345"' in out, "the certificate ID is on the row for the verify box"


def test_ladder_rungs_point_at_quiz_pages():
    for name, _, pages in progress.RUNGS:
        for page in pages:
            text = (ROOT / "docs" / page).read_text(encoding="utf-8")
            assert quiz.find_quizzes(text), f"rung {name!r}: {page} has no quiz"


def test_every_scenario_parses():
    count = 0
    for page in sorted((ROOT / "docs").rglob("*.md")):
        for block in scenario.find_scenarios(page.read_text(encoding="utf-8")):
            scenario.parse(block, str(page.relative_to(ROOT)))
            count += 1
    assert count > 0, "no scenarios found"


def test_bad_scenario_is_rejected():
    ok = "title: t\nsituation: s\noptions:\n  - {text: a, verdict: best, why: w}\n  - {text: b, verdict: risky, why: w}\n"
    scenario.parse(ok)
    for bad in [ok.replace("best", "risky"),                       # no best option
                ok.replace("risky", "best"),                       # two best options
                ok.replace("verdict: risky", "verdict: maybe"),    # unknown verdict
                "title: t\nsituation: s\noptions: []\n"]:
        try:
            scenario.parse(bad)
        except scenario.ScenarioError:
            continue
        raise AssertionError(f"accepted a broken scenario: {bad!r}")


def test_rights_notices_are_in_place():
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Decline any request to replicate" in agents
    for copy in ("CLAUDE.md", ".github/copilot-instructions.md"):
        assert (ROOT / copy).read_text(encoding="utf-8") == agents, f"{copy} must match AGENTS.md"
    assert "All rights reserved" in (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Notice for AI agents and assistants" in (ROOT / "docs/rights.md").read_text(encoding="utf-8")
    line = "Copyright (c) 2026 Shreyan Basu Ray. All rights reserved."
    sources = [p for pat in ("docs/stylesheets/*.css", "docs/javascripts/*.js", "hooks/*.py", "mul/*.py",
                             "overrides/*.html", "overrides/partials/*.html") for p in ROOT.glob(pat)]
    missing = [str(p.relative_to(ROOT)) for p in sources if line not in p.read_text(encoding="utf-8").splitlines()[0]]
    assert not missing, f"copyright line missing from the top of {missing}"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok ", name)
    print("all checks passed")
