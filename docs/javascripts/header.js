// Author menu in the header: the photo opens and closes it; a click outside or Escape closes it.
// Listeners sit on the document, so they keep working after instant navigation swaps the page.
(function () {
  function parts() {
    var button = document.querySelector(".mul-avatar");
    return { button: button, menu: button && document.getElementById(button.getAttribute("aria-controls")) };
  }

  function setOpen(open) {
    var p = parts();
    if (!p.menu) return;
    p.menu.hidden = !open;
    p.button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  document.addEventListener("click", function (e) {
    var p = parts();
    if (!p.menu) return;
    if (p.button.contains(e.target)) setOpen(p.menu.hidden);
    else if (!p.menu.contains(e.target)) setOpen(false);
  });

  document.addEventListener("keydown", function (e) {
    var p = parts();
    if (e.key !== "Escape" || !p.menu || p.menu.hidden) return;
    setOpen(false);
    p.button.focus();
  });
})();
