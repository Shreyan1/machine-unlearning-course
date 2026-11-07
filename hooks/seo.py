# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""MkDocs hook: the facts overrides/main.html needs for search engines and link previews.

For every page it adds to `page.meta`:

- `mul_published` and `mul_modified`, the dates the page's source file was first added and last
  changed, read from git. Without git (or in a shallow clone) both fall back to the build date.
- `mul_crumbs`, the breadcrumb trail as (name, url) pairs, from Home through each nav section that
  has an index page down to the page itself.
- `mul_og`, the page's own share image, when `assets/make_og_image.py` has drawn one.
"""

from __future__ import annotations

import datetime
import posixpath
import subprocess
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().isoformat()


def og_name(src_uri: str) -> str:
    """The share image's file name for a page, shared with assets/make_og_image.py."""
    return posixpath.splitext(src_uri)[0].replace("/", "-") + ".png"


@lru_cache(maxsize=None)
def _git_dates(path: str) -> tuple[str, str]:
    """(first added, last changed) as YYYY-MM-DD, or today's date for both if git cannot say."""
    try:
        out = subprocess.run(["git", "log", "--follow", "--format=%cs", "--", path], cwd=ROOT,
                             capture_output=True, text=True, timeout=20, check=True).stdout.split()
    except (OSError, subprocess.SubprocessError):
        out = []
    return (out[-1], out[0]) if out else (TODAY, TODAY)


def _crumbs(page, site_url: str) -> list[tuple[str, str]]:
    trail = [("Home", site_url)]
    # page.ancestors runs from the nearest section outwards; a section counts when it has an index page.
    for section in reversed(page.ancestors):
        index = next((c for c in section.children if c.is_page and c.is_index), None)
        if index is not None and index is not page:
            trail.append((section.title, site_url + index.url))
    trail.append((page.title or "", page.canonical_url or site_url))
    return trail


def on_page_context(context, page, config, nav):
    src = Path(page.file.abs_src_path)
    try:
        rel = src.relative_to(ROOT).as_posix()
    except ValueError:  # a generated page with no file in the repository
        rel = None
    page.meta["mul_published"], page.meta["mul_modified"] = _git_dates(rel) if rel else (TODAY, TODAY)
    # sitemap.xml is written after every page, and its <lastmod> reads this field.
    page.update_date = page.meta["mul_modified"]
    page.meta["mul_crumbs"] = _crumbs(page, config.site_url or "/")
    name = og_name(page.file.src_uri)
    if (ROOT / "docs" / "assets" / "og" / name).exists():
        page.meta["mul_og"] = "assets/og/" + name
    return context
