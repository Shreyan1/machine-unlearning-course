# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""MkDocs hook: an "All topics" index, built from the site menu.

A page that contains `<!-- all-topics -->` gets a GeeksforGeeks-style list of
every page in the nav, grouped by section, so readers can see every topic at
any screen width. It is generated from `nav`, so it never goes out of date.
"""

import html
import posixpath

MARKER = "<!-- all-topics -->"
_nav = None


def on_nav(nav, config, files):
    global _nav
    _nav = nav
    return nav


def _pages(items):
    for item in items:
        if item.is_section:
            yield from _pages(item.children)
        elif item.is_page and item.file is not None:
            yield item


def _is_index(page):
    return page.file.src_uri.endswith("index.md")


def _link(from_uri, page):
    href = posixpath.relpath(page.file.dest_uri, posixpath.dirname(from_uri) or ".")
    href = href[:-len("index.html")] if href.endswith("index.html") else href
    return href or "./"


def _groups(section, trail=()):
    """Yield (heading, pages) for every section that directly holds pages."""
    direct = [c for c in section.children if not c.is_section and c.is_page and not _is_index(c)]
    if direct:
        yield " · ".join(trail + (section.title,)), direct
    for child in section.children:
        if child.is_section:
            yield from _groups(child, trail + (section.title,))


def on_page_markdown(markdown, page, config, files):
    if MARKER not in markdown or _nav is None:
        return markdown
    from_uri = page.file.dest_uri
    out = []
    for top in _nav.items:
        if not top.is_section or top.title in ("Quizzes",):
            continue
        pages = list(_pages(top.children))
        index = next((p for p in pages if _is_index(p)), None)
        title = html.escape(top.title)
        if index is not None:
            title = f'<a href="{_link(from_uri, index)}">{title} →</a>'
        out.append(f'<div class="topics__part"><h3 class="topics__title">{title} '
                   f'<span class="topics__count">{len(pages)} pages</span></h3><div class="topics__grid">')
        for heading, group in _groups(top):
            items = "".join(
                f'<li><a href="{_link(from_uri, p)}">{html.escape(p.title or "Overview")}</a></li>'
                for p in group)
            label = heading.split(" · ", 1)[1] if " · " in heading else "Begin here"
            out.append(f'<div class="topics__group"><div class="topics__label">{html.escape(label)}</div>'
                       f'<ul>{items}</ul></div>')
        out.append("</div></div>")
    return markdown.replace(MARKER, '<div class="topics">' + "".join(out) + "</div>")
