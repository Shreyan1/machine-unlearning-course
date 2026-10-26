// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// Adds "Copy" and "Download" buttons to every diagram. The diagram is drawn onto a canvas with its
// theme colours written into the SVG first, so the image looks the same as on the page.
(function () {
  var PROPS = ["fill", "stroke", "stroke-width", "stroke-dasharray", "font-size", "font-weight", "font-style", "opacity", "baseline-shift"];

  function toCanvas(svg, done) {
    var rect = svg.getBoundingClientRect();
    var clone = svg.cloneNode(true);
    var src = svg.querySelectorAll("*"), dst = clone.querySelectorAll("*");
    src.forEach(function (el, i) {
      var cs = getComputedStyle(el), style = "";
      PROPS.forEach(function (p) { style += p + ":" + cs.getPropertyValue(p) + ";"; });
      if (el.tagName === "text" || el.tagName === "tspan") style += "font-family:Outfit,Helvetica,Arial,sans-serif;";
      dst[i].setAttribute("style", style);
    });
    var vb = svg.viewBox.baseVal;
    clone.setAttribute("width", vb.width); clone.setAttribute("height", vb.height);
    var bg = getComputedStyle(document.body).backgroundColor;
    var xml = new XMLSerializer().serializeToString(clone);
    var img = new Image();
    img.onload = function () {
      var scale = 2, c = document.createElement("canvas");
      c.width = vb.width * scale; c.height = vb.height * scale;
      var g = c.getContext("2d");
      g.fillStyle = bg; g.fillRect(0, 0, c.width, c.height);
      g.drawImage(img, 0, 0, c.width, c.height);
      done(c);
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(xml);
  }

  function flash(btn, text) {
    var old = btn.dataset.label;
    btn.textContent = text;
    setTimeout(function () { btn.textContent = old; }, 1400);
  }

  function name(fig) {
    var n = fig.querySelector(".diagram__n");
    return (n ? n.textContent : "figure").trim().toLowerCase().replace(/\s+/g, "-");
  }

  function addTools(fig) {
    if (fig.dataset.tools) return;
    fig.dataset.tools = "1";
    var box = fig.querySelector(".diagram__box"), svg = fig.querySelector("svg");
    if (!box || !svg) return;
    var bar = document.createElement("div");
    bar.className = "diagram__tools";
    [["Copy", "Copy this figure as an image"], ["Download", "Download this figure as a PNG"]].forEach(function (b) {
      var btn = document.createElement("button");
      btn.type = "button"; btn.textContent = b[0]; btn.dataset.label = b[0]; btn.title = b[1];
      btn.addEventListener("click", function () {
        toCanvas(svg, function (c) {
          c.toBlob(function (blob) {
            if (b[0] === "Download") {
              var a = document.createElement("a");
              a.href = URL.createObjectURL(blob); a.download = name(fig) + ".png"; a.click();
              setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
              flash(btn, "Saved");
            } else if (navigator.clipboard && window.ClipboardItem) {
              navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]).then(function () { flash(btn, "Copied"); }, function () { flash(btn, "Not allowed"); });
            } else { flash(btn, "Not supported"); }
          }, "image/png");
        });
      });
      bar.appendChild(btn);
    });
    box.appendChild(bar);
  }

  function init() { document.querySelectorAll(".diagram").forEach(addTools); }
  if (typeof document$ !== "undefined") document$.subscribe(init); else document.addEventListener("DOMContentLoaded", init);
})();
