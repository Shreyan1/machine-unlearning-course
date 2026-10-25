"""MkDocs hook: link every citation to its source.

Pages mention papers ("Bourtoule et al., IEEE S&P 2021"), laws ("GDPR Art. 17"),
regulator cases ("FTC v. Everalbum") and datasets ("MovieLens 100K") in plain text.
This hook turns each mention into a link, using the one source list below, so a
source is defined once and every page links to the same place.

It never touches code, headings, quiz blocks, HTML tags or text that is already a
link. Entries marked `first` are linked once per page; the rest at every mention.
All URLs were checked by hand; paper links match resources/catalog.json.
"""

import re

ARXIV = "https://arxiv.org/abs/"
GDPR = "https://gdpr-info.eu/art-{}-gdpr/"

# (pattern, url, first_only). Longer, more specific patterns come first.
SOURCES = [
    # ---- papers -----------------------------------------------------------------
    (r"Cao and Yang(?:,? \(?2015\)?)?", "https://www.ieee-security.org/TC/SP2015/papers-archived/6949a463.pdf", False),
    (r"Bourtoule et al\.(?:, IEEE S&P 2021)?", ARXIV + "1912.03817", False),
    (r"Kurmanji(?:, Triantafillou, Hayes and Triantafillou| et al\.)?(?:, NeurIPS 2023)?", ARXIV + "2302.09880", False),
    (r"Chundawat(?:, Tarun, Mandal and Kankanhalli| et al\.)?(?:, AAAI 2023)?", ARXIV + "2205.08096", False),
    (r"(?:Vitaly )?Feldman \(2020\)", ARXIV + "1906.05271", False),
    (r"Carlini et al\.,? 2022", ARXIV + "2112.03570", False),
    (r"Carlini et al\.,? 2019", ARXIV + "1802.08232", False),
    (r"Thudi(?:, Jia, Shumailov and Papernot| et al\.)? \(2022\)", ARXIV + "2110.11891", False),
    (r"Pawelczyk et al\.,? \(?2024\)?", ARXIV + "2406.17216", False),
    (r"Hayes et al\.,? \(?2024\)?", ARXIV + "2403.01218", False),
    (r"Lynch et al\.,? \(?2024\)?", ARXIV + "2402.16835", False),
    (r"Deeb and Roger,? \(?2024\)?", ARXIV + "2410.08827", False),
    (r"Zhang et al\.,? \(?2024\)?", ARXIV + "2404.05868", False),
    (r"Hu et al\.,? \(?2021\)?", ARXIV + "2106.09685", False),
    (r"Ilharco et al\.,? \(?2023\)?", ARXIV + "2212.04089", False),
    (r"Guo et al\.,? \(?2019\)?", ARXIV + "1911.03030", False),
    (r"Chen et al\.,? \(?2022\)?", ARXIV + "2201.06820", False),
    (r"Shokri et al\.,? \(?2017\)?", ARXIV + "1610.05820", False),
    (r"The GPT-3 paper \(2020\)", ARXIV + "2005.14165", False),
    (r"\"anonymous\" Netflix ratings", ARXIV + "cs/0610105", False),
    (r"\bRecEraser\b", ARXIV + "2201.06820", True),
    (r"\bTOFU\b", ARXIV + "2401.06121", True),
    (r"\bMUSE\b", ARXIV + "2407.06460", True),
    (r"\bWMDP\b", ARXIV + "2403.03218", True),
    # ---- reports, courts and regulators ------------------------------------------
    (r"Stanford's AI Index 2024", "https://aiindex.stanford.edu/report/", False),
    (r"a Munich court", "https://cms.law/en/deu/legal-updates/gema-vs.-openai-munich-regional-court-i-issues-landmark-copyright-decision", False),
    (r"draft guidelines", "https://www.edpb.europa.eu/public-consultations/guidelines-032026-on-web-scraping-in-the-context-of-generative-ai_en", True),
    (r"EDPB Opinion 28/2024", "https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en", False),
    (r"(?:FTC v\. )?Everalbum", "https://www.ftc.gov/news-events/news/press-releases/2021/05/ftc-finalizes-settlement-photo-app-developer-related-misuse-facial-recognition-technology", True),
    (r"WW(?: \(Weight Watchers\))? ?/ ?Kurbo", "https://www.ftc.gov/news-events/news/press-releases/2022/03/ftc-takes-action-against-company-formerly-known-weight-watchers-illegally-collecting-kids-sensitive", True),
    (r"(?<=\*\*)Ring(?=\*\*)", "https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-says-ring-employees-illegally-surveilled-customers-failed-stop-hackers-taking-control-users", True),
    (r"Rite Aid", "https://www.ftc.gov/news-events/news/press-releases/2023/12/rite-aid-banned-using-ai-facial-recognition-after-ftc-says-retailer-deployed-technology-without", True),
    (r"Kakao Pay", "https://iapp.org/news/a/south-korea-s-pipc-flexes-its-muscles-what-to-know-about-ai-model-deletion-cross-border-transfers-and-more", True),
    # ---- laws -------------------------------------------------------------------
    (r"GDPR Art\. 17", GDPR.format(17), False),
    (r"GDPR(?:'s)? \(?Art\. 9\)?", GDPR.format(9), False),
    (r"Art\. 9(?=\))", GDPR.format(9), False),
    (r"Art\. 7\(3\)", GDPR.format(7), False),
    (r"Art\. 12\(3\)", GDPR.format(12), False),
    (r"India's DPDP Act 2023 s\.12|DPDP Act 2023 s\.12|India's DPDP Act", "https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf", False),
    (r"California CCPA §1798\.105|CCPA §1798\.105", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1798.105", False),
    (r"Video Privacy Protection Act(?: \(1988\))?", "https://www.law.cornell.edu/uscode/text/18/2710", True),
    # ---- datasets and tools -----------------------------------------------------
    (r"MovieLens(?: 100K)?", "https://files.grouplens.org/datasets/movielens/ml-100k-README.txt", True),
    (r"UCI Adult(?: census)?(?: dataset| data)?", "https://archive.ics.uci.edu/dataset/2/adult", True),
    (r"Olivetti faces(?: dataset)?", "https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_olivetti_faces.html", True),
    (r"SMS spam filter", "https://archive.ics.uci.edu/dataset/228/sms+spam+collection", True),
    (r"fairlearn's `ThresholdOptimizer`", "https://fairlearn.org/main/api_reference/generated/fairlearn.postprocessing.ThresholdOptimizer.html", False),
]
COMPILED = [(re.compile(p), url, first) for p, url, first in SOURCES]

# Spans that must never be edited: front matter, fenced blocks (code and quizzes),
# inline code, existing links and images, HTML tags, and heading lines.
PROTECT = re.compile(
    r"\A---\n.*?\n---\n"
    r"|^```.*?^```[ \t]*$"
    r"|`[^`\n]+`"
    r"|!?\[[^\]\n]*\]\([^)\n]*\)(?:\{[^}\n]*\})?"
    r"|<[^>\n]+>"
    r"|^#{1,6} [^\n]*$"
    r"|^[ \t]*\|?[ \t]*:?-{3,}[^\n]*$",
    re.S | re.M,
)


def _link_once(markdown, pattern, url, first):
    out, pos, done = [], 0, False
    for m in PROTECT.finditer(markdown):
        chunk = markdown[pos:m.start()]
        if not done:
            chunk, done = _sub(chunk, pattern, url, first)
        out.append(chunk)
        out.append(m.group(0))
        pos = m.end()
    tail = markdown[pos:]
    if not done:
        tail, done = _sub(tail, pattern, url, first)
    out.append(tail)
    return "".join(out)


def _sub(text, pattern, url, first):
    count = 1 if first else 0
    new, n = pattern.subn(lambda m: f"[{m.group(0)}]({url})", text, count=count)
    return new, bool(first and n)


def on_page_markdown(markdown, page, config, files):
    for pattern, url, first in COMPILED:
        markdown = _link_once(markdown, pattern, url, first)
    return markdown
