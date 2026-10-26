// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// MathJax set-up for pymdownx.arithmatex (generic mode), re-run on instant navigation.
window.MathJax = {
  tex: { inlineMath: [["\\(", "\\)"]], displayMath: [["\\[", "\\]"]], processEscapes: true, processEnvironments: true },
  options: { ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex" },
  // SVG output draws its own glyphs, so no web fonts are fetched. The privacy plugin serves the
  // script from this site, and nothing else is loaded on demand.
  loader: { load: [] },
  svg: { fontCache: "global" }
};
if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    if (window.MathJax && MathJax.startup && MathJax.typesetPromise) {
      if (MathJax.startup.output.clearCache) MathJax.startup.output.clearCache();
      MathJax.typesetClear();
      MathJax.texReset();
      MathJax.typesetPromise();
    }
  });
}
