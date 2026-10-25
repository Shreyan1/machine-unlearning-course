// Small "try it yourself" widgets. A page asks for one with <div class="widget" data-widget="knn">.
// Everything is drawn as SVG, so it follows the light and dark themes through CSS.
(function () {
  var SVGNS = "http://www.w3.org/2000/svg";

  function svg(tag, attrs, parent) {
    var e = document.createElementNS(SVGNS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function el(tag, cls, text, parent) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  }
  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function slider(parent, label, min, max, step, value, onInput) {
    var wrap = el("label", "widget__control", null, parent);
    el("span", "widget__label", label, wrap);
    var input = el("input", null, null, wrap);
    input.type = "range"; input.min = min; input.max = max; input.step = step; input.value = value;
    var out = el("output", "widget__value", String(value), wrap);
    input.addEventListener("input", function () { out.textContent = input.value; onInput(Number(input.value)); });
    return input;
  }
  function button(parent, text, onClick, cls) {
    var b = el("button", "widget__button" + (cls ? " " + cls : ""), text, parent);
    b.type = "button";
    b.addEventListener("click", onClick);
    return b;
  }

  // ---- k-NN: the model is the data, so deleting a point is exact unlearning --------------------
  function knn(node) {
    var W = 640, H = 340, rand = rng(7);
    var points = [];
    function blob(cx, cy, n, cls, spread, owner) {
      for (var i = 0; i < n; i++) {
        points.push({ x: cx + (rand() - .5) * spread, y: cy + (rand() - .5) * spread * .8, cls: cls, owner: owner || "", gone: false });
      }
    }
    blob(180, 150, 16, "a", 230); blob(470, 200, 16, "b", 230); blob(285, 120, 6, "b", 60, "carol");
    var query = { x: 280, y: 118 }, k = 5;

    node.textContent = "";
    var head = el("p", "widget__intro", null, node);
    head.innerHTML = "<strong>Try it.</strong> Drag the star to ask the model about a new digit. Click any point to delete it, or forget all of Carol's at once.";
    var controls = el("div", "widget__controls", null, node);
    slider(controls, "Neighbours (k)", 1, 9, 2, k, function (v) { k = v; draw(); });
    var forget = button(controls, "Forget Carol", function () {
      var anyLeft = points.some(function (p) { return p.owner === "carol" && !p.gone; });
      points.forEach(function (p) { if (p.owner === "carol") p.gone = anyLeft; });
      draw();
    }, "widget__button--primary");
    button(controls, "Reset", function () { points.forEach(function (p) { p.gone = false; }); query = { x: 280, y: 118 }; draw(); });

    var box = el("div", "widget__canvas", null, node);
    var s = svg("svg", { viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": "A k-nearest-neighbours plot you can edit" }, box);
    var layer = svg("g", {}, s);
    var readout = el("p", "widget__readout", null, node);
    readout.setAttribute("aria-live", "polite");

    function nearest() {
      return points.filter(function (p) { return !p.gone; })
        .map(function (p) { return { p: p, d: Math.hypot(p.x - query.x, p.y - query.y) }; })
        .sort(function (a, b) { return a.d - b.d; }).slice(0, k);
    }
    function draw() {
      layer.textContent = "";
      var near = nearest();
      near.forEach(function (n) { svg("line", { x1: query.x, y1: query.y, x2: n.p.x, y2: n.p.y, class: "w-link" }, layer); });
      points.forEach(function (p) {
        var cls = "w-pt w-pt--" + p.cls + (p.owner ? " w-pt--carol" : "") + (p.gone ? " is-gone" : "");
        var shape = p.cls === "a"
          ? svg("circle", { cx: p.x, cy: p.y, r: 7, class: cls }, layer)
          : svg("rect", { x: p.x - 6.5, y: p.y - 6.5, width: 13, height: 13, class: cls }, layer);
        shape.addEventListener("click", function () { p.gone = !p.gone; draw(); });
      });
      var star = svg("path", { d: starPath(query.x, query.y, 13, 6), class: "w-query" }, layer);
      star.addEventListener("pointerdown", startDrag);
      var votes = { a: 0, b: 0 }, fromCarol = 0;
      near.forEach(function (n) { votes[n.p.cls]++; if (n.p.owner) fromCarol++; });
      var label = votes.a > votes.b ? "a 7 (circles)" : "a 1 (squares)";
      var carolLeft = points.filter(function (p) { return p.owner === "carol" && !p.gone; }).length;
      forget.textContent = carolLeft ? "Forget Carol" : "Bring Carol back";
      readout.innerHTML = "";
      el("strong", null, "The model predicts " + label + ". ", readout);
      function n(count, word) { return count + " " + word + (count === 1 ? "" : "s"); }
      readout.appendChild(document.createTextNode("Its nearest neighbours are " + n(votes.a, "circle") + " and " +
        n(votes.b, "square") + ", and " + fromCarol + " of the " + near.length + " came from Carol. " +
        (carolLeft ? "" : "Carol is deleted, so this is exactly the model you would get by training without her.")));
    }
    function starPath(cx, cy, r1, r2) {
      var d = "";
      for (var i = 0; i < 10; i++) {
        var r = i % 2 ? r2 : r1, a = -Math.PI / 2 + i * Math.PI / 5;
        d += (i ? "L" : "M") + (cx + Math.cos(a) * r).toFixed(1) + "," + (cy + Math.sin(a) * r).toFixed(1);
      }
      return d + "Z";
    }
    function toLocal(e) {
      var r = s.getBoundingClientRect();
      return { x: Math.max(10, Math.min(W - 10, (e.clientX - r.left) * W / r.width)),
               y: Math.max(10, Math.min(H - 10, (e.clientY - r.top) * H / r.height)) };
    }
    function startDrag(e) {
      e.preventDefault();
      function move(ev) { query = toLocal(ev); draw(); }
      function up() { window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", up); }
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up);
    }
    // Clicking empty space moves the star too, which is easier on a phone than dragging.
    s.addEventListener("click", function (e) { if (e.target === s) { query = toLocal(e); draw(); } });
    draw();
  }

  // ---- SISA: shards and slices decide how much a deletion costs ----------------------------------
  function sisa(node) {
    var N = 1000, USERS = 40, CAROL = 40;
    var K = 5, R = 4, aware = false, rows = [], target = 0, requests = 0, spent = 0, last = null;

    function layout() {
      var rand = rng(11 + (aware ? 1 : 0));
      last = null;
      rows = [];
      // User 0 is Carol, with her 40 digits; the other rows are spread over 39 users.
      for (var i = 0; i < N; i++) {
        var user = i < CAROL ? 0 : 1 + Math.floor(rand() * (USERS - 1));
        rows.push({ user: user });
      }
      // Person-aware: each person's rows sit together, in one shard and one slice.
      var home = [], homeSlice = [];
      for (var u = 0; u < USERS; u++) { home.push(Math.floor(rand() * K)); homeSlice.push(Math.floor(rand() * R)); }
      rows.forEach(function (r) {
        r.shard = aware ? home[r.user] : Math.floor(rand() * K);
        r.slice = aware ? homeSlice[r.user] : Math.floor(rand() * R);
      });
    }

    node.textContent = "";
    var head = el("p", "widget__intro", null, node);
    head.innerHTML = "<strong>Try it.</strong> 1,000 rows from 40 people, split into shards and slices. Forget someone and see which models must be retrained.";
    var controls = el("div", "widget__controls", null, node);
    slider(controls, "Shards (K)", 1, 20, 1, K, function (v) { K = v; layout(); draw(); });
    slider(controls, "Slices (R)", 1, 8, 1, R, function (v) { R = v; layout(); draw(); });
    var awareBox = el("label", "widget__control widget__check", null, controls);
    var check = el("input", null, null, awareBox);
    check.type = "checkbox";
    el("span", "widget__label", "Keep each person's rows together", awareBox);
    check.addEventListener("change", function () { aware = check.checked; layout(); draw(); });
    var actions = el("div", "widget__controls", null, node);
    button(actions, "Forget Carol", function () { target = 0; forgetNow(); }, "widget__button--primary");
    button(actions, "Forget someone else", function () { target = 1 + Math.floor(Math.random() * (USERS - 1)); forgetNow(); });
    button(actions, "Reset the bill", function () { requests = 0; spent = 0; draw(); });

    var box = el("div", "widget__canvas", null, node);
    var readout = el("p", "widget__readout", null, node);
    readout.setAttribute("aria-live", "polite");
    var bill = el("p", "widget__bill", null, node);

    // Cost of one deletion, as a share of a full retrain: in each touched shard, retrain from the
    // earliest slice that held the person's rows to the end of that shard.
    function cost(user) {
      var first = {};
      rows.forEach(function (r) {
        if (r.user !== user) return;
        if (!(r.shard in first) || r.slice < first[r.shard]) first[r.shard] = r.slice;
      });
      var shards = Object.keys(first), share = 0;
      shards.forEach(function (sh) { share += (R - first[sh]) / R / K; });
      return { first: first, shards: shards.length, share: share };
    }
    function forgetNow() {
      last = cost(target);
      requests++; spent += last.share;
      draw();
    }
    function draw() {
      box.textContent = "";
      var W = 640, H = 220, pad = 24, cw = (W - pad) / K, ch = (H - pad) / R;
      var s = svg("svg", { viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": K + " shards by " + R + " slices" }, box);
      var counts = {};
      rows.forEach(function (r) {
        var key = r.shard + ":" + r.slice;
        counts[key] = counts[key] || { all: 0, mine: 0 };
        counts[key].all++;
        if (r.user === target) counts[key].mine++;
      });
      for (var sh = 0; sh < K; sh++) {
        for (var sl = 0; sl < R; sl++) {
          var c = counts[sh + ":" + sl] || { all: 0, mine: 0 };
          var redo = last && sh in last.first && sl >= last.first[sh];
          svg("rect", { x: pad + sh * cw + 1.5, y: pad + sl * ch + 1.5, width: cw - 3, height: ch - 3, rx: 2,
                        class: "w-cell" + (redo ? " is-redo" : "") + (c.mine ? " has-target" : "") }, s);
          if (c.mine && cw > 16) {
            var t = svg("text", { x: pad + sh * cw + cw / 2, y: pad + sl * ch + ch / 2 + 4, class: "w-cell-n", "text-anchor": "middle" }, s);
            t.textContent = c.mine;
          }
        }
        if (K <= 10) { var lab = svg("text", { x: pad + sh * cw + cw / 2, y: 15, class: "w-axis", "text-anchor": "middle" }, s); lab.textContent = "shard " + (sh + 1); }
      }
      var yl = svg("text", { x: 10, y: pad + 12, class: "w-axis" }, s);
      yl.textContent = "slices ↓";
      var who = target === 0 ? "Carol" : "person " + (target + 1);
      readout.innerHTML = "";
      if (last) {
        el("strong", null, "Forgetting " + who + " retrains " + (last.share * 100).toFixed(1) + "% of a full retrain. ", readout);
        readout.appendChild(document.createTextNode("Their rows sit in " + last.shards + " of " + K + " shards; shaded cells must be retrained from the earliest affected slice."));
      } else {
        readout.appendChild(document.createTextNode("Numbers show how many of Carol's 40 rows are in each cell. Press a button to forget someone."));
      }
      bill.textContent = requests
        ? requests + " request" + (requests > 1 ? "s" : "") + " so far " + (requests > 1 ? "have" : "has") + " cost " + (spent * 100).toFixed(0) + "% of one retrain, against " +
          requests * 100 + "% if you retrained from scratch each time. Each model trains on about " + Math.round(N / K) + " rows."
        : "Each model trains on about " + Math.round(N / K) + " rows. More shards make deletions cheaper but each model weaker.";
      bill.textContent += " Costs here count the share of slices retrained; Lesson 07 measures real training steps.";
    }
    layout(); draw();
  }

  var WIDGETS = { knn: knn, sisa: sisa };
  function init() {
    document.querySelectorAll(".widget[data-widget]").forEach(function (node) {
      if (node.dataset.ready || !WIDGETS[node.dataset.widget]) return;
      node.dataset.ready = "1";
      WIDGETS[node.dataset.widget](node);
    });
  }
  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
