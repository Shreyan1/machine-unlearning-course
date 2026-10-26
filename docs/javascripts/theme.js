// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// Light/dark toggle: the new theme grows out of the toggle button as a circle (View Transitions API).
// Browsers without it, and people who prefer reduced motion, simply get the instant switch.
(function () {
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  document.addEventListener("click", function (e) {
    var label = e.target.closest && e.target.closest('[data-md-component="palette"] label');
    if (!label || !document.startViewTransition || (reduce && reduce.matches)) return;
    var input = document.getElementById(label.htmlFor);
    if (!input) return;
    e.preventDefault();
    var box = label.getBoundingClientRect();
    var root = document.documentElement;
    root.style.setProperty("--vt-x", box.left + box.width / 2 + "px");
    root.style.setProperty("--vt-y", box.top + box.height / 2 + "px");
    document.startViewTransition(function () {
      input.checked = true;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
  }, true);
})();
