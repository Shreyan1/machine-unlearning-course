"""Download the papers in catalog.json into resources/papers/ (they are not stored in git).

    python resources/fetch_papers.py            # every paper
    python resources/fetch_papers.py sisa lira  # only papers whose file name contains one of these words

The notebooks cite papers by their local path (resources/papers/<topic>/<file>.pdf); this puts them there.
If `pdftotext` (poppler) is installed, missing plain-text copies are also written to resources/text/ so that
`grep -il "rewind" resources/text/*.txt` covers every paper, not only the openly licensed ones kept in git.
"""
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(words):
    catalog = json.loads((HERE / "catalog.json").read_text())
    pdftotext = shutil.which("pdftotext")
    ok = failed = 0
    for paper in catalog:
        pdf = HERE / paper["file"]
        if words and not any(w.lower() in pdf.name for w in words):
            continue
        if not pdf.exists():
            pdf.parent.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(paper["url"], headers={"User-Agent": "MachineUnlearning-course/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    pdf.write_bytes(r.read())
                print(f"  got   {pdf.relative_to(HERE)}")
            except Exception as e:
                print(f"  FAIL  {pdf.relative_to(HERE)}  ({e}) - download it by hand from {paper['url']}")
                failed += 1
                continue
        ok += 1
        txt = HERE / "text" / (pdf.stem + ".txt")
        if pdftotext and not txt.exists():
            subprocess.run([pdftotext, "-q", str(pdf), str(txt)], check=False)
    print(f"{ok} papers in resources/papers/, {failed} failed.")


if __name__ == "__main__":
    main(sys.argv[1:])
