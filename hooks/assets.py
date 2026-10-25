"""MkDocs hook: serve the repo's shared diagrams inside the site.

The notebooks and the README use `assets/diagrams/*.png`. This hook adds those
files to the site as if they lived in `docs/assets/diagrams/`, so there is one
copy of every diagram and pages link to them as `assets/diagrams/<name>.png`.
"""

from pathlib import Path

from mkdocs.structure.files import File

ROOT = Path(__file__).resolve().parent.parent


def on_files(files, config):
    for png in sorted((ROOT / "assets" / "diagrams").glob("*.png")):
        uri = png.relative_to(ROOT).as_posix()
        if files.get_file_from_path(uri) is None:
            files.append(File(uri, str(ROOT), config["site_dir"], config["use_directory_urls"]))
    return files
