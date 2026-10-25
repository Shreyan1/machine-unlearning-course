"""MkDocs hook: llms.txt and llms-full.txt for AI search and answer engines.

llms.txt (see llmstxt.org) is a short, linked map of the site. llms-full.txt is every page's text in one
Markdown file, so a language model can read the whole course in a single request. Both are built from
the nav, so they never go out of date.
"""

import re
from pathlib import Path

_nav = None
_pages = []

SUMMARY = ("A free, plain-English course on machine unlearning: how to make a trained AI model forget someone's data, "
           "and how to prove that it did. Explainers, quizzes, practice problems and runnable Colab notebooks.")


def on_nav(nav, config, files):
    global _nav, _pages
    _nav = nav
    _pages = []
    return nav


def _walk(items, trail=()):
    for item in items:
        if item.is_section:
            yield from _walk(item.children, trail + (item.title,))
        elif item.is_page and item.file is not None:
            yield trail, item


def _clean(text):
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)             # front matter
    text = re.sub(r"```quiz\n.*?```\n?", "", text, flags=re.S)             # quizzes are interactive
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)                     # markers for hooks
    text = re.sub(r"</?(div|span|nav|figure|ol|ul|li|p|a|canvas|b)\b[^>]*>", "", text)
    text = re.sub(r"\{\s*[.#:][^}]*\}", "", text)                           # attr_list
    text = re.sub(r"^(!!!|\?\?\?\+?) \w+ \"([^\"]*)\"", r"**\2**", text, flags=re.M)
    text = re.sub(r"^(!!!|\?\?\?\+?) (\w+)$", r"**\2**", text, flags=re.M)
    text = re.sub(r":[a-z0-9-]+:(?=\s)", "", text)                          # icon shortcodes
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def on_post_build(config):
    if _nav is None:
        return
    site = config.site_url.rstrip("/") + "/"
    out = Path(config.site_dir)
    short = [f"# {config.site_name}", "", f"> {SUMMARY}", "",
             "The course is by Shreyan Basu Ray and is free under the MIT licence. Every page ends with a short quiz.", ""]
    full = list(short)
    current = None
    for trail, page in _walk(_nav.items):
        src = page.file.src_uri
        group = " · ".join(trail) or "Home"
        url = site + page.file.dest_uri.removesuffix("index.html")
        desc = (page.meta or {}).get("description", "")
        if group != current:
            short += ["", f"## {group}", ""]
            current = group
        short.append(f"- [{page.title}]({url})" + (f": {desc}" if desc else ""))
        raw = Path(page.file.abs_src_path).read_text(encoding="utf-8")
        if "<!-- practice -->" in raw:
            raw = raw.replace("<!-- practice -->", (Path(config.config_file_path).parent / "PRACTICE.md").read_text(encoding="utf-8"))
        body = _clean(raw)
        full += ["", "---", "", f"<!-- source: {url} -->", body]
    (out / "llms.txt").write_text("\n".join(short) + "\n", encoding="utf-8")
    (out / "llms-full.txt").write_text("\n".join(full) + "\n", encoding="utf-8")
