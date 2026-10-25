"""MkDocs hook: the course map behind progress, badges, the ladder climb and the certificate.

At build time this writes `assets/progress.json`: every page with a quiz, grouped by the
site's sections, the five rungs of the Ladder of Forgetting with the pages that climb
each one, and the icon paths the certificate draws. `docs/javascripts/progress.js`
reads it and compares it with the quiz scores saved in the reader's browser.

It also renders `docs/finishers.yml` into the Hall of Finishers page. That list is
added to by hand after a reader asks to join, so a name only appears once a person
has checked it.
"""

from __future__ import annotations

import datetime
import html
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quiz  # noqa: E402
import scenario  # noqa: E402

PASS_SHARE = quiz.PASS_SHARE
FINAL = "quizzes/final.md"
FINAL_PASS = 16
FINISHERS_MARKER = "<!-- finishers -->"

# Each rung of the Ladder of Forgetting, with the pages that teach it. A rung is climbed when
# all of its pages are passed. The names follow the diagram in hooks/diagrams_unlearning.py.
RUNGS = [
    ("k-NN and Naive Bayes", "Subtract the data exactly", [
        "ml-basics/k-nearest-neighbours.md", "ml-basics/naive-bayes.md",
        "lessons/01-knn-and-naive-bayes.md"]),
    ("Linear and logistic", "A closed-form update", [
        "ml-basics/linear-and-ridge-regression.md", "ml-basics/logistic-regression.md",
        "unlearning/exact-unlearning-classical.md", "lessons/02-linear-and-logistic-regression.md"]),
    ("SVMs and forests", "Rebuild the affected part", [
        "ml-basics/support-vector-machines.md", "ml-basics/decision-trees-and-random-forests.md",
        "lessons/03-svm-and-random-forest.md", "unlearning/sisa.md", "lessons/07-sisa.md"]),
    ("Neural networks", "Approximate, then audit", [
        "ml-basics/neural-networks.md", "unlearning/deleting-vs-unlearning.md",
        "lessons/04-deleting-is-not-forgetting.md", "unlearning/gold-band.md",
        "lessons/06-retrain-and-the-gold-band.md", "unlearning/scrub.md", "lessons/09-scrub.md",
        "unlearning/unlearning-audit.md", "lessons/11-the-unlearning-audit.md"]),
    ("Language models", "Facts, not rows (unsolved)", [
        "ml-basics/language-models.md", "ml-basics/fine-tuning-and-lora.md",
        "unlearning/llm-unlearning.md", "lessons/16-llm-unlearning.md"]),
]

# Material Design icons the badges and the certificate use, read from the theme so the
# shapes match the rest of the site.
ICONS = ["rocket-launch", "brain", "eraser", "school", "ladder", "star-four-points", "trophy",
         "check-bold", "lock", "party-popper", "lightning-bolt", "flag-checkered", "gavel", "dumbbell",
         "sign-direction", "calendar-check", "fire"]
POLICY = "unlearning/global-policy.md"

_manifest: dict = {}


def _walk(items, trail):
    for item in items:
        if item.is_section:
            yield from _walk(item.children, trail + [item.title])
        elif item.is_page and item.file is not None:
            yield item, trail


def _url(page) -> str:
    url = page.file.url
    return "" if url in ("", "./") else url


def _icon_paths() -> dict:
    import material
    root = Path(material.__file__).parent / "templates" / ".icons" / "material"
    out = {}
    for name in ICONS:
        svg = (root / f"{name}.svg").read_text(encoding="utf-8")
        out[name] = " ".join(re.findall(r'\bd="([^"]+)"', svg))
    return out


def on_nav(nav, config, files):
    pages, sections, scenarios = {}, [], []
    for item, trail in _walk(nav.items, []):
        uri = item.file.src_uri
        text = Path(item.file.abs_src_path).read_text(encoding="utf-8")
        scenarios += [f"{uri}#{n}" for n in range(len(scenario.find_scenarios(text)))]
        blocks = quiz.find_quizzes(text)
        if not blocks:
            continue
        total = sum(len(quiz.parse(b, uri)[1]) for b in blocks)
        title = item.title or quiz._title(text)
        pages[uri] = {"t": title, "u": _url(item), "q": total, "n": len(blocks)}
        if uri.startswith("quizzes/"):
            continue
        top = trail[0] if trail else "Home"
        sub = trail[1] if len(trail) > 1 else top
        section = next((s for s in sections if s["name"] == top), None)
        if section is None:
            section = {"name": top, "subs": []}
            sections.append(section)
        group = next((g for g in section["subs"] if g["name"] == sub), None)
        if group is None:
            group = {"name": sub, "pages": []}
            section["subs"].append(group)
        group["pages"].append(uri)

    for name, _, rung_pages in RUNGS:
        missing = [p for p in rung_pages if p not in pages]
        if missing:
            raise quiz.QuizError(f"ladder rung {name!r} lists pages without a quiz: {', '.join(missing)}")
    if POLICY not in pages:
        raise quiz.QuizError(f"{POLICY} needs a quiz for the Policy wonk badge")
    if FINAL not in pages or pages[FINAL]["q"] < FINAL_PASS:
        raise quiz.QuizError(f"{FINAL} needs a quiz of at least {FINAL_PASS} questions for the certificate")

    _manifest.clear()
    _manifest.update({
        "pass": PASS_SHARE,
        "pages": pages,
        "sections": sections,
        "rungs": [{"name": n, "note": note, "pages": p} for n, note, p in RUNGS],
        "final": {"page": FINAL, "id": FINAL + "#0", "total": pages[FINAL]["q"], "pass": FINAL_PASS},
        "policy": POLICY,
        "scenarios": scenarios,
        "site": config["site_url"],
        "repo": config["repo_url"],
        "author": config["site_author"],
        "icons": _icon_paths(),
    })
    return nav


def on_post_build(config):
    out = Path(config["site_dir"]) / "assets" / "progress.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(_manifest, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


# ---- Hall of Finishers -----------------------------------------------------------

LINKEDIN = re.compile(r"^https://([a-z]{2,3}\.)?linkedin\.com/in/[A-Za-z0-9_%-]+/?$")
GITHUB = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")
CERT_ID = re.compile(r"^MU-[A-Z2-7]{4}-[A-Z2-7]{4}$")


def load_finishers(path: Path) -> list[dict]:
    """Read and check docs/finishers.yml. A bad entry stops the build."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise ValueError(f"{path.name}: expected a list of finishers")
    out = []
    for n, item in enumerate(data, 1):
        at = f"{path.name}, entry {n}"
        if not isinstance(item, dict) or not str(item.get("name", "")).strip():
            raise ValueError(f"{at}: every finisher needs a name")
        date = item.get("date")
        if not isinstance(date, datetime.date):
            raise ValueError(f"{at}: date must be written as YYYY-MM-DD")
        score = item.get("score")
        if score is not None and (not isinstance(score, int) or not 0 <= score <= 20):
            raise ValueError(f"{at}: score must be a whole number from 0 to 20")
        linkedin = item.get("linkedin")
        if linkedin is not None and not LINKEDIN.match(str(linkedin)):
            raise ValueError(f"{at}: linkedin must be a https://linkedin.com/in/... profile link")
        github = item.get("github")
        if github is not None and not GITHUB.match(str(github)):
            raise ValueError(f"{at}: github must be a GitHub username")
        cert = item.get("id")
        if cert is not None and not CERT_ID.match(str(cert)):
            raise ValueError(f"{at}: id must look like MU-ABCD-2345, as printed on the certificate")
        out.append({"name": str(item["name"]).strip(), "date": date, "score": score,
                    "linkedin": linkedin, "github": github, "id": cert})
    out.sort(key=lambda f: f["date"])
    return out


def _svg(name: str, cls: str = "") -> str:
    d = _manifest.get("icons", {}).get(name, "")
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"><path d="{html.escape(d)}"/></svg>'


def render_finishers(finishers: list[dict]) -> str:
    if not finishers:
        return ('<div class="hall hall--empty">' + _svg("flag-checkered", "hall__icon") +
                '<p><strong>No one is on the list yet.</strong> Pass the final test, make your certificate and be '
                'finisher number one.</p></div>')
    rows = ['<ol class="hall">']
    for n, f in enumerate(finishers, 1):
        links = []
        if f["linkedin"]:
            links.append(f'<a href="{html.escape(f["linkedin"])}" rel="nofollow noopener">LinkedIn</a>')
        if f["github"]:
            links.append(f'<a href="https://github.com/{html.escape(f["github"])}" rel="nofollow noopener">GitHub</a>')
        score = f' · {f["score"]}/20' if f["score"] is not None else ""
        cert = f' data-id="{html.escape(f["id"])}"' if f["id"] else ""
        rows.append(
            f'<li class="hall__row{" hall__row--first" if n <= 3 else ""}"{cert} data-name="{html.escape(f["name"])}">'
            f'<span class="hall__n">#{n}</span>{_svg("trophy", "hall__badge")}'
            f'<span class="hall__name">{html.escape(f["name"])}</span>'
            f'<span class="hall__meta">{f["date"]:%d %b %Y}{score}{" · " + html.escape(f["id"]) if f["id"] else ""}</span>'
            f'<span class="hall__links">{" · ".join(links)}</span></li>')
    rows.append("</ol>")
    return "\n".join(rows)


def on_page_markdown(markdown, page, config, files):
    if FINISHERS_MARKER not in markdown:
        return markdown
    path = Path(config["docs_dir"]) / "finishers.yml"
    return markdown.replace(FINISHERS_MARKER, "\n" + render_finishers(load_finishers(path)) + "\n")
