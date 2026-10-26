# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""MkDocs hook: turn ```scenario fences into choose-your-response case studies.

A scenario is a YAML mapping inside a fenced block:

    ```scenario
    title: The first erasure request
    situation: |
      Carol asks a small startup to delete her data...
    options:
      - text: Delete her rows and reply that it is done.
        verdict: risky
        why: The model was trained on her rows, so it still carries them.
      - text: Add her to this week's retrain and record the evidence.
        verdict: best
        why: ...
    ```

Every option needs a verdict (best, ok or risky) and a "why", and each scenario has
exactly one best option. A broken scenario stops the build. `docs/javascripts/quiz.js`
makes the HTML interactive, and progress.js counts finished scenarios for a badge.
"""

from __future__ import annotations

import html
import re

import markdown as mdlib
import yaml

FENCE = re.compile(r"^```scenario[ \t]*\n(.*?)^```[ \t]*$", re.M | re.S)
VERDICTS = {"best": "The best call.", "ok": "Defensible.", "risky": "Risky."}


class ScenarioError(ValueError):
    pass


def parse(text: str, where: str = "scenario") -> dict:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as err:
        raise ScenarioError(f"{where}: not valid YAML ({err})") from err
    if not isinstance(data, dict):
        raise ScenarioError(f"{where}: expected a mapping with title, situation and options")
    for key in ("title", "situation", "options"):
        if not data.get(key):
            raise ScenarioError(f"{where}: missing {key}")
    options = data["options"]
    if not isinstance(options, list) or not 2 <= len(options) <= 5:
        raise ScenarioError(f"{where}: options must be a list of 2 to 5 choices")
    for n, opt in enumerate(options, 1):
        if not isinstance(opt, dict) or not opt.get("text") or not opt.get("why"):
            raise ScenarioError(f"{where}, option {n}: needs text and why")
        if opt.get("verdict") not in VERDICTS:
            raise ScenarioError(f"{where}, option {n}: verdict must be one of {', '.join(VERDICTS)}")
    if sum(o["verdict"] == "best" for o in options) != 1:
        raise ScenarioError(f"{where}: exactly one option must be the best")
    return {"title": str(data["title"]), "situation": str(data["situation"]),
            "options": [{"text": str(o["text"]), "verdict": o["verdict"], "why": str(o["why"])} for o in options]}


def find_scenarios(markdown: str) -> list[str]:
    return [m.group(1) for m in FENCE.finditer(markdown)]


def _md(text: str, md, inline: bool = False) -> str:
    md.reset()
    out = md.convert(text).strip()
    if inline and out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        out = out[3:-4]
    return out


def render(sc: dict, sid: str, n: int, md) -> str:
    parts = [f'<div class="scenario" data-scenario-id="{html.escape(sid)}">',
             '<div class="scenario__head">'
             f'<span class="scenario__n">Scenario {n}</span>'
             f'<span class="scenario__title">{html.escape(sc["title"])}</span>'
             '<span class="quiz__stamp" hidden>Done</span></div>',
             f'<div class="scenario__situation">{_md(sc["situation"], md)}</div>',
             '<p class="scenario__ask">What do you do?</p>',
             '<div class="scenario__options">']
    for i, opt in enumerate(sc["options"]):
        parts.append(f'<button type="button" class="scenario__opt" data-i="{i}" data-verdict="{opt["verdict"]}">'
                     f'{_md(opt["text"], md, inline=True)}</button>')
    parts.append('</div><div class="scenario__feedback">')
    for i, opt in enumerate(sc["options"]):
        parts.append(f'<div class="scenario__fb scenario__fb--{opt["verdict"]}" data-i="{i}" hidden>'
                     f'<span class="scenario__verdict">{VERDICTS[opt["verdict"]]}</span> '
                     f'{_md(opt["why"], md, inline=True)}</div>')
    parts.append('</div><div class="scenario__foot"><button type="button" class="quiz__reset">Try again</button></div></div>')
    return "\n".join(parts)


HREF = re.compile(r'href="([^":#]+\.md)(#[^"]*)?"')


def _links(out: str, page, files) -> str:
    """Point links to other pages at their built URLs, as MkDocs does for ordinary Markdown."""
    import posixpath

    def fix(m):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page.file.src_uri), m.group(1)))
        f = files.get_file_from_path(target)
        if f is None:
            raise ScenarioError(f"{page.file.src_uri}: link to missing page {m.group(1)}")
        base = page.url if page.url.endswith("/") or not page.url else posixpath.dirname(page.url) + "/"
        url = posixpath.relpath("/" + f.url, "/" + base)
        if f.url.endswith("/") and not url.endswith("/"):
            url += "/"
        return f'href="{url}{m.group(2) or ""}"'

    return HREF.sub(fix, out)


def on_page_markdown(markdown, page, config, files):
    if "```scenario" not in markdown:
        return markdown
    md = mdlib.Markdown(extensions=["pymdownx.inlinehilite", "pymdownx.betterem", "attr_list", "pymdownx.arithmatex"],
                        extension_configs={"pymdownx.arithmatex": {"generic": True}})
    count = 0

    def replace(match):
        nonlocal count
        sc = parse(match.group(1), page.file.src_uri)
        count += 1
        return "\n" + _links(render(sc, f"{page.file.src_uri}#{count - 1}", count, md), page, files) + "\n"

    return FENCE.sub(replace, markdown)
