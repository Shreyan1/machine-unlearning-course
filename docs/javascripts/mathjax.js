// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// MathJax set-up for pymdownx.arithmatex (generic mode). MathJax itself is about 700 KB, so it is
// loaded only when a page with maths is opened, and typesets again on instant navigation.
window.MathJax = {
  tex: { inlineMath: [["\\(", "\\)"]], displayMath: [["\\[", "\\]"]], processEscapes: true, processEnvironments: true },
  options: { ignoreHtmlClass: ".*|", processHtmlClass: "arithmatex" },
  // SVG output draws its own glyphs, so no web fonts are fetched. The privacy plugin serves the
  // script from this site, and nothing else is loaded on demand.
  loader: { load: [] },
  svg: { fontCache: "global" }
};
(function () {
  // overrides/main.html carries the script's URL in an inert tag. Read it now, while the page's
  // relative paths still resolve against the page that wrote them.
  var tag = document.getElementById("mul-mathjax");
  var src = tag ? tag.src : null;
  var requested = false;

  function typeset() {
    if (!document.querySelector(".arithmatex")) return;
    if (window.MathJax && MathJax.startup && MathJax.typesetPromise) {
      if (MathJax.startup.output.clearCache) MathJax.startup.output.clearCache();
      MathJax.typesetClear();
      MathJax.texReset();
      MathJax.typesetPromise();
    } else if (!requested && src) {
      // On load, MathJax typesets whatever page is open by then.
      requested = true;
      var s = document.createElement("script");
      s.src = src; s.async = true;
      document.head.appendChild(s);
    }
  }

  if (typeof document$ !== "undefined") document$.subscribe(typeset);
  else document.addEventListener("DOMContentLoaded", typeset);
})();
