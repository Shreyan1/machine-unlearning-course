// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// Progress, badges, the ladder climb and the certificate. hooks/progress.py writes the course
// map to assets/progress.json; this file compares it with the quiz scores quiz.js saved in this
// browser. Nothing is sent anywhere.
(function () {
  var QUIZ = "mul-quiz:";
  var STORE = "mul-progress";
  var NAME = "mul-cert-name";
  var PRACTICE = "mul-practice";
  var SCENARIO = "mul-scenario:";
  var SVGNS = "http://www.w3.org/2000/svg";
  // Change this when the certificate terms (docs/quizzes/certificate.md) change, so everyone accepts them again.
  var TERMS = "2026-10-26";

  var config = {};
  try { config = JSON.parse(document.getElementById("__config").textContent); } catch (e) { /* no config */ }
  // Resolve the site root once: with instant navigation the page changes but this script does not.
  var ROOT = new URL((config.base || ".") + "/", location.href);
  var manifest = null;
  var loading = null;

  function getManifest() {
    if (manifest) return Promise.resolve(manifest);
    if (!loading) {
      loading = fetch(new URL("assets/progress.json", ROOT)).then(function (r) { return r.json(); })
        .then(function (m) { manifest = m; return m; });
    }
    return loading;
  }

  // ---- saved state --------------------------------------------------------------------------

  function readJSON(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch (e) { return fallback; }
  }
  function writeJSON(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private window */ }
  }

  function pageScores(m) {
    var out = {};
    Object.keys(m.pages).forEach(function (uri) {
      var p = m.pages[uri], right = 0, answered = 0;
      for (var n = 0; n < p.n; n++) {
        var s = readJSON(QUIZ + uri + "#" + n, {});
        answered += Object.keys(s.picks || {}).length;
        right += s.right || 0;
      }
      var done = answered >= p.q;
      out[uri] = { right: right, answered: answered, total: p.q, done: done,
                   passed: done && right >= Math.ceil(p.q * m.pass), perfect: done && right === p.q };
    });
    return out;
  }

  var BADGES = [
    { id: "first", icon: "rocket-launch", name: "Lift-off", text: "Pass your first quiz", color: "#3D5AFE" },
    { id: "perfect", icon: "star-four-points", name: "Flawless", text: "Get every answer right on a page", color: "#FFC300", ink: true },
    { id: "ml", icon: "brain", name: "Model maker", text: "Pass every ML Basics quiz", color: "#2E7D53", section: "ML Basics" },
    { id: "unlearning", icon: "eraser", name: "Eraser", text: "Pass every Unlearning Concepts quiz", color: "#1B36C9", section: "Unlearning Concepts" },
    { id: "lessons", icon: "school", name: "Lab rat", text: "Pass every lesson quiz", color: "#E8833A", section: "Lessons" },
    { id: "ladder", icon: "ladder", name: "Top rung", text: "Climb all five rungs of the ladder", color: "#B4441F" },
    { id: "policy", icon: "gavel", name: "Policy wonk", text: "Pass the Policies around the world quiz", color: "#6A4C93" },
    { id: "scenarios", icon: "sign-direction", name: "Decision maker", text: "Finish every scenario", color: "#2E7D53" },
    { id: "practice", icon: "dumbbell", name: "Problem solver", text: "Mark 5 practice problems as done", color: "#1B36C9" },
    { id: "streak", icon: "calendar-check", name: "Regular", text: "Learn in 3 weeks in a row", color: "#E8833A" },
    { id: "finisher", icon: "trophy", name: "Finisher", text: "Score 16 or more on the final test", color: "#15171B", final: true }
  ];

  function sectionPages(m, name) {
    var s = m.sections.filter(function (x) { return x.name === name; })[0];
    return s ? [].concat.apply([], s.subs.map(function (g) { return g.pages; })) : [];
  }

  function count(uris, scores) {
    return uris.filter(function (u) { return scores[u] && scores[u].passed; }).length;
  }

  // Weeks are counted from a Monday, so "this week" means Monday to Sunday.
  function weekOf(iso) { return Math.floor((Date.parse(iso + "T12:00:00Z") - Date.UTC(2024, 0, 1)) / 6048e5); }
  function streak(days) {
    var weeks = {};
    (days || []).forEach(function (d) { weeks[weekOf(d)] = true; });
    var now = weekOf(new Date().toISOString().slice(0, 10)), w = weeks[now] ? now : now - 1, n = 0;
    while (weeks[w]) { n++; w--; }
    return n;
  }
  function practiceDone() { return Object.keys(readJSON(PRACTICE, {})); }
  function scenariosDone(m) {
    return m.scenarios.filter(function (id) { return !!readJSON(SCENARIO + id, null); }).length;
  }

  // Everything the widgets need, worked out once per page view.
  function compute(m, active) {
    var scores = pageScores(m);
    var store = readJSON(STORE, {});
    store.badges = store.badges || {};
    var today = new Date().toISOString().slice(0, 10);
    // A day counts as active when you answer a quiz, pick a scenario or tick a practice problem.
    store.days = store.days || [];
    if (active && store.days.indexOf(today) < 0) store.days = store.days.concat(today).slice(-120);

    var final = scores[m.final.page];
    var finalPassed = final.done && final.right >= m.final.pass;
    if (finalPassed && (!store.final || final.right > store.final.best)) {
      store.final = { best: final.right, date: (store.final && store.final.date) || today };
    }

    var learnUris = [].concat.apply([], m.sections.map(function (s) {
      return [].concat.apply([], s.subs.map(function (g) { return g.pages; }));
    }));
    // The certificate unlocks once every page quiz is passed and the final test is passed. Like a
    // badge it then stays unlocked, even if a quiz is reset later.
    var allPassed = learnUris.every(function (u) { return scores[u].passed; });
    if (store.final && allPassed && !store.unlocked) store.unlocked = today;
    var rungs = m.rungs.map(function (r) {
      var c = count(r.pages, scores);
      return { name: r.name, note: r.note, pages: r.pages, passed: c, total: r.pages.length, climbed: c === r.pages.length };
    });

    var progress = {};
    BADGES.forEach(function (b) {
      var have = 0, need = 1;
      if (b.id === "first") have = Math.min(1, count(learnUris, scores));
      else if (b.id === "perfect") have = learnUris.some(function (u) { return scores[u].perfect; }) ? 1 : 0;
      else if (b.section) { var u = sectionPages(m, b.section); have = count(u, scores); need = u.length || 1; }
      else if (b.id === "ladder") { have = rungs.filter(function (r) { return r.climbed; }).length; need = rungs.length; }
      else if (b.final) { have = store.final ? 1 : 0; }
      else if (b.id === "policy") { have = scores[m.policy] && scores[m.policy].passed ? 1 : 0; }
      else if (b.id === "scenarios") { have = scenariosDone(m); need = m.scenarios.length || 1; }
      else if (b.id === "practice") { have = Math.min(5, practiceDone().length); need = 5; }
      else if (b.id === "streak") { have = Math.min(3, streak(store.days)); need = 3; }
      progress[b.id] = { have: have, need: need };
    });

    // Badges stay earned even if a quiz is reset later; the first date is kept.
    var fresh = [];
    BADGES.forEach(function (b) {
      var p = progress[b.id];
      if (p.have >= p.need && !store.badges[b.id]) { store.badges[b.id] = today; fresh.push(b); }
    });
    writeJSON(STORE, store);

    var next = learnUris.filter(function (u) { return !scores[u].passed; })[0];
    return { m: m, scores: scores, store: store, rungs: rungs, cert: !!store.unlocked, progress: progress, fresh: fresh, streak: streak(store.days),
             thisWeek: store.days.filter(function (d) { return weekOf(d) === weekOf(today); }).length,
             learn: learnUris, passed: count(learnUris, scores), next: next };
  }

  // ---- small DOM helpers ----------------------------------------------------------------------

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function icon(m, name, cls) {
    var svg = document.createElementNS(SVGNS, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("aria-hidden", "true");
    if (cls) svg.setAttribute("class", cls);
    var path = document.createElementNS(SVGNS, "path");
    path.setAttribute("d", m.icons[name] || "");
    svg.appendChild(path);
    return svg;
  }
  function link(m, uri, text) {
    var a = el("a", null, text || m.pages[uri].t);
    a.href = new URL(m.pages[uri].u, ROOT).href;
    return a;
  }
  function bar(have, need, cls) {
    var b = el("span", "pbar" + (cls ? " " + cls : ""));
    var f = el("span", "pbar__fill");
    f.style.width = (need ? Math.round(100 * have / need) : 0) + "%";
    b.appendChild(f);
    b.setAttribute("role", "progressbar");
    b.setAttribute("aria-valuemin", "0");
    b.setAttribute("aria-valuemax", String(need));
    b.setAttribute("aria-valuenow", String(have));
    return b;
  }
  function path(u) { return new URL(u, location.href).pathname.replace(/index\.html$/, ""); }

  // ---- widgets ------------------------------------------------------------------------------

  // A strip at the top of a section index: overall bar, then one row per group of pages.
  function strip(node, st) {
    var s = st.m.sections.filter(function (x) { return x.name === node.dataset.section; })[0];
    if (!s) return;
    node.textContent = "";
    var all = [].concat.apply([], s.subs.map(function (g) { return g.pages; }));
    var have = count(all, st.scores);
    var pct = all.length ? Math.round(100 * have / all.length) : 0;
    node.classList.toggle("is-done", have === all.length);
    node.appendChild(ring(pct, pct + "%", "pring--strip"));
    var main = el("div", "pstrip__main");
    node.appendChild(main);
    var head = el("div", "pstrip__head");
    head.appendChild(icon(st.m, have === all.length ? "check-bold" : "lightning-bolt", "pstrip__icon"));
    var label = el("span", "pstrip__label");
    label.appendChild(document.createTextNode("You have passed "));
    label.appendChild(el("strong", null, have + " of " + all.length));
    label.appendChild(document.createTextNode(" quizzes in this section."));
    head.appendChild(label);
    var more = el("a", "pstrip__more", "Your progress");
    more.href = new URL("quizzes/progress/", ROOT).href;
    head.appendChild(more);
    main.appendChild(head);
    main.appendChild(bar(have, all.length, "pbar--big"));
    var groups = el("div", "pstrip__groups");
    s.subs.forEach(function (g) {
      var c = count(g.pages, st.scores);
      var row = el("div", "pstrip__group" + (c === g.pages.length ? " is-done" : ""));
      row.appendChild(el("span", "pstrip__name", g.name));
      row.appendChild(bar(c, g.pages.length));
      row.appendChild(el("span", "pstrip__count", c + "/" + g.pages.length));
      groups.appendChild(row);
    });
    if (s.subs.length > 1) main.appendChild(groups);
    // The section's own badge, with how many quizzes are left to earn it.
    var b = BADGES.filter(function (x) { return x.section === s.name; })[0];
    if (b) {
      var prize = el("div", "pstrip__prize" + (st.store.badges[b.id] ? " is-earned" : ""));
      prize.appendChild(medal(st, b));
      prize.appendChild(el("strong", null, b.name));
      var left = all.length - have;
      prize.appendChild(el("span", null, st.store.badges[b.id] ? "Badge earned" : left + " quiz" + (left === 1 ? "" : "zes") + " to go"));
      node.appendChild(prize);
    }
  }

  // ---- on each page with a quiz: a status chip under the title and a result card after the quiz --

  function here(m) {
    var me = path(location.href);
    return Object.keys(m.pages).filter(function (u) { return path(new URL(m.pages[u].u, ROOT).href) === me; })[0];
  }
  function onLearnPage(st, uri) { return !!uri && st.learn.indexOf(uri) >= 0; }

  function chip(st, uri) {
    document.querySelectorAll(".pchip").forEach(function (n) { n.remove(); });
    var h1 = document.querySelector(".md-content .md-typeset h1");
    if (!h1 || !onLearnPage(st, uri)) return;
    var sc = st.scores[uri];
    var box = el("div", "pchip" + (sc.passed ? " is-passed" : sc.answered ? " is-started" : ""));
    var status = el("a", "pchip__item pchip__status");
    status.href = "#quiz";
    status.appendChild(icon(st.m, sc.passed ? "check-decagram" : "bullseye-arrow"));
    status.appendChild(document.createTextNode(sc.passed ? "Quiz passed with " + sc.right + " of " + sc.total
      : sc.answered ? sc.answered + " of " + sc.total + " answered, keep going"
      : sc.total + "-question quiz at the end"));
    box.appendChild(status);
    if (sc.done) box.appendChild(starRow(st.m, stars(sc)));
    var r = -1;
    st.rungs.forEach(function (x, i) { if (r < 0 && x.pages.indexOf(uri) >= 0) r = i; });
    if (r >= 0) {
      var rung = el("a", "pchip__item pchip__rung");
      rung.href = new URL("unlearning/ladder-of-forgetting/", ROOT).href;
      rung.appendChild(icon(st.m, "ladder"));
      rung.appendChild(document.createTextNode("Rung " + (r + 1) + " of the ladder"));
      box.appendChild(rung);
    }
    h1.insertAdjacentElement("afterend", box);
  }

  function result(st, uri, celebrate) {
    document.querySelectorAll(".qres").forEach(function (n) { n.remove(); });
    var quizzes = document.querySelectorAll(".md-content .quiz");
    if (!quizzes.length || !onLearnPage(st, uri)) return;
    var sc = st.scores[uri];
    if (!sc.done) return;
    var need = Math.ceil(sc.total * st.m.pass);
    var card = el("div", "qres " + (sc.passed ? "is-passed" : "is-missed"));
    card.setAttribute("role", "status");
    card.appendChild(ring(Math.round(100 * sc.right / sc.total), sc.right + "/" + sc.total, "pring--result"));
    var body = el("div", "qres__body");
    body.appendChild(el("span", "qres__kicker", sc.perfect ? "Flawless" : sc.passed ? "Page complete" : "Not passed yet"));
    body.appendChild(el("strong", "qres__title", sc.perfect ? "Every answer right!" : sc.passed ? "You passed this page."
      : sc.right === need - 1 ? "So close, one more right answer passes." : "You need " + need + " right to pass."));
    body.appendChild(starRow(st.m, stars(sc)));
    var line = el("p", "qres__line");
    if (sc.passed) {
      line.appendChild(document.createTextNode("You have passed "));
      line.appendChild(el("strong", null, st.passed + " of " + st.learn.length));
      line.appendChild(document.createTextNode(" page quizzes in the course."));
    } else {
      line.textContent = "Read the explanations above, then press Try again. Your best effort counts, not your first.";
    }
    body.appendChild(line);
    if (sc.passed) body.appendChild(bar(st.passed, st.learn.length));
    if (celebrate && st.fresh.length) {
      var won = el("div", "qres__won");
      st.fresh.forEach(function (b) {
        var w = el("span", "qres__badge");
        w.appendChild(medal(st, b));
        w.appendChild(el("span", null, b.name));
        won.appendChild(w);
      });
      body.appendChild(won);
    }
    var acts = el("div", "qres__actions");
    var i = st.learn.indexOf(uri), nextUri = st.learn[i + 1];
    if (sc.passed && nextUri) {
      var go = el("a", "md-button md-button--primary");
      go.href = new URL(st.m.pages[nextUri].u, ROOT).href;
      go.appendChild(document.createTextNode("Next, " + st.m.pages[nextUri].t));
      go.appendChild(icon(st.m, "arrow-right"));
      acts.appendChild(go);
    }
    var mine = el("a", "md-button", "Your progress");
    mine.href = new URL("quizzes/progress/", ROOT).href;
    acts.appendChild(mine);
    body.appendChild(acts);
    card.appendChild(body);
    quizzes[quizzes.length - 1].insertAdjacentElement("afterend", card);
    if (celebrate) { confetti(card); card.scrollIntoView({ block: "nearest", behavior: "smooth" }); }
  }

  // A short burst of paper when a page is passed. Skipped when the reader asks for less motion.
  function confetti(at) {
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var burst = el("div", "pconfetti");
    burst.setAttribute("aria-hidden", "true");
    var colours = ["#3D5AFE", "#FFC300", "#2E7D53", "#E8833A", "#E8432A", "#7C8CFF"];
    for (var i = 0; i < 40; i++) {
      var p = el("i"), a = Math.random() * Math.PI * 2, d = 50 + Math.random() * 130;
      p.style.setProperty("--x", Math.round(Math.cos(a) * d * 1.6) + "px");
      p.style.setProperty("--y", Math.round(Math.sin(a) * d - 40) + "px");
      p.style.setProperty("--r", Math.round(Math.random() * 900 - 450) + "deg");
      p.style.background = colours[i % colours.length];
      p.style.animationDelay = Math.round(Math.random() * 120) + "ms";
      burst.appendChild(p);
    }
    at.appendChild(burst);
    setTimeout(function () { burst.remove(); }, 1600);
  }

  // ---- home page: a welcome-back card for readers who have started ----------------------------

  function welcome(node, st) {
    node.textContent = "";
    var started = st.learn.some(function (u) { return st.scores[u].answered; }) || st.store.days.length;
    if (!started) return;
    var pct = st.learn.length ? Math.round(100 * st.passed / st.learn.length) : 0;
    node.appendChild(ring(pct, pct + "%", "pring--big"));
    var body = el("div", "pwelcome__body");
    body.appendChild(el("span", "pwelcome__kicker", "Welcome back"));
    body.appendChild(el("strong", "pwelcome__title", pct === 100 ? "You have passed every page quiz." : "You are " + pct + "% of the way through the course."));
    var stats = el("div", "pwelcome__stats");
    var earned = Object.keys(st.store.badges).length;
    [[st.passed + "/" + st.learn.length, "quizzes passed"],
     [earned + "/" + BADGES.length, "badges"],
     [st.rungs.filter(function (r) { return r.climbed; }).length + "/5", "rungs climbed"],
     [String(st.streak), "week streak"]].forEach(function (s, i) {
      var t = el("span", "pwelcome__stat" + (i === 3 && st.streak ? " is-hot" : ""));
      if (i === 3) t.appendChild(icon(st.m, "fire"));
      t.appendChild(el("strong", null, s[0]));
      t.appendChild(el("span", null, s[1]));
      stats.appendChild(t);
    });
    body.appendChild(stats);
    var shelfRow = el("div", "pwelcome__badges");
    BADGES.forEach(function (b) { shelfRow.appendChild(medal(st, b, "badge__medal--mini")); });
    body.appendChild(shelfRow);
    var acts = el("div", "pwelcome__actions");
    var go = el("a", "md-button md-button--primary");
    if (st.next) {
      go.href = new URL(st.m.pages[st.next].u, ROOT).href;
      go.appendChild(document.createTextNode("Continue with " + st.m.pages[st.next].t));
    } else {
      go.href = new URL(st.cert ? "quizzes/certificate/" : "quizzes/final/", ROOT).href;
      go.appendChild(document.createTextNode(st.cert ? "Make your certificate" : "Take the final test"));
    }
    go.appendChild(icon(st.m, "arrow-right"));
    acts.appendChild(go);
    var mine = el("a", "md-button", "Your progress");
    mine.href = new URL("quizzes/progress/", ROOT).href;
    acts.appendChild(mine);
    body.appendChild(acts);
    node.appendChild(body);
  }

  function summary(node, st) {
    node.textContent = "";
    var pct = st.learn.length ? Math.round(100 * st.passed / st.learn.length) : 0;
    var ring = el("div", "psum__ring");
    ring.style.setProperty("--pct", pct);
    ring.appendChild(el("span", "psum__pct", pct + "%"));
    node.appendChild(ring);
    var body = el("div", "psum__body");
    var line = el("p", "psum__line");
    line.appendChild(document.createTextNode("You have passed "));
    line.appendChild(el("strong", null, st.passed + " of " + st.learn.length));
    line.appendChild(document.createTextNode(" quizzes, earned " + Object.keys(st.store.badges).length + " of " +
      BADGES.length + " badges and climbed " + st.rungs.filter(function (r) { return r.climbed; }).length + " of 5 rungs."));
    body.appendChild(line);
    var chip = el("p", "psum__streak" + (st.streak ? " is-on" : ""));
    chip.appendChild(icon(st.m, "fire"));
    chip.appendChild(document.createTextNode(st.streak
      ? "You are on a " + st.streak + "-week streak, with " + st.thisWeek + " active day" + (st.thisWeek === 1 ? "" : "s") + " this week."
      : "Answer a quiz this week to start a streak. Missing a week just starts a new one."));
    body.appendChild(chip);
    var next = el("p", "psum__next");
    if (st.next) {
      next.appendChild(document.createTextNode("Next, try "));
      next.appendChild(link(st.m, st.next));
      next.appendChild(document.createTextNode("."));
    } else {
      next.appendChild(document.createTextNode("Every page quiz passed. "));
    }
    body.appendChild(next);
    var goTo = st.cert || st.store.final ? "quizzes/certificate/" : "quizzes/final/";
    var go = el("a", "md-button" + (st.cert ? " md-button--primary" : ""),
      st.cert ? "Make your certificate" : st.store.final ? "See what unlocks your certificate" : "Take the final test");
    go.href = new URL(goTo, ROOT).href;
    body.appendChild(go);
    node.appendChild(body);
  }

  // A badge's medal: in colour once earned, otherwise a blurred glimpse of itself with a lock on top.
  function medal(st, b, cls) {
    var earned = !!st.store.badges[b.id];
    var md = el("span", "badge__medal" + (cls ? " " + cls : "") + (earned ? "" : " is-locked"));
    md.style.setProperty("--badge", b.color);
    if (b.ink) md.classList.add("badge__medal--ink");
    md.title = b.name + (earned ? ", earned" : ", locked");
    if (earned) {
      md.appendChild(icon(st.m, b.icon));
    } else {
      var art = el("span", "badge__art");
      art.appendChild(icon(st.m, b.icon));
      md.appendChild(art);
      var lock = el("span", "badge__lock");
      lock.appendChild(icon(st.m, "lock"));
      md.appendChild(lock);
    }
    return md;
  }

  // A round progress ring with a label in the middle.
  function ring(pct, label, cls) {
    var r = el("div", "pring" + (cls ? " " + cls : ""));
    r.style.setProperty("--pct", Math.max(0, Math.min(100, pct)));
    r.setAttribute("role", "img");
    r.setAttribute("aria-label", pct + "% complete");
    r.appendChild(el("strong", "pring__label", label));
    return r;
  }

  // Up to three stars for a page quiz: one for passing, two for 80% and three for every answer right.
  function stars(sc) {
    if (!sc || !sc.passed) return 0;
    return sc.perfect ? 3 : sc.right >= Math.ceil(sc.total * 0.8) ? 2 : 1;
  }
  function starRow(m, n) {
    var row = el("span", "pstars");
    row.title = "Quiz stars. One for passing, two for 80% or more, three for every answer right.";
    var marks = el("span", "pstars__marks");
    marks.setAttribute("aria-hidden", "true");
    for (var i = 0; i < 3; i++) marks.appendChild(icon(m, "star", i < n ? "is-on" : ""));
    row.appendChild(marks);
    row.appendChild(el("span", "pstars__label", n + " of 3 quiz stars"));
    return row;
  }

  function shelf(node, st) {
    node.textContent = "";
    BADGES.forEach(function (b) {
      var p = st.progress[b.id], when = st.store.badges[b.id];
      var tile = el("div", "badge" + (when ? " is-earned" : ""));
      tile.appendChild(medal(st, b));
      tile.appendChild(el("span", "badge__name", b.name));
      tile.appendChild(el("span", "badge__text", b.text));
      tile.appendChild(el("span", "badge__state", when ? "Earned " + niceDate(when) : p.need > 1 ? p.have + " / " + p.need : "Locked"));
      node.appendChild(tile);
    });
  }

  // The Ladder of Forgetting as a climb: one rising step per rung, filled by the pages passed.
  function climb(node, st) {
    node.textContent = "";
    var detail = node.dataset.detail === "1";
    var colors = ["good", "good", "warn", "warn", "bad"];
    var top = -1;
    st.rungs.forEach(function (r, i) { if (r.climbed && top === i - 1) top = i; });
    var steps = el("ol", "climb");
    st.rungs.forEach(function (r, i) {
      var li = el("li", "climb__rung climb__rung--" + colors[i] + (r.climbed ? " is-climbed" : ""));
      var step = el("span", "climb__step");
      var fill = el("span", "climb__fill");
      fill.style.height = Math.round(100 * r.passed / r.total) + "%";
      step.appendChild(fill);
      step.appendChild(el("span", "climb__n", String(i + 1)));
      if (i === top) step.appendChild(icon(st.m, "flag-checkered", "climb__flag"));
      li.appendChild(step);
      li.appendChild(el("span", "climb__name", r.name));
      li.appendChild(el("span", "climb__count", r.passed + " / " + r.total + " pages"));
      if (detail) {
        var list = el("ul", "climb__pages");
        r.pages.forEach(function (u) {
          var item = el("li", st.scores[u].passed ? "is-done" : "");
          item.appendChild(link(st.m, u));
          list.appendChild(item);
        });
        li.appendChild(list);
      }
      steps.appendChild(li);
    });
    node.appendChild(steps);
    var note = el("p", "climb__note");
    note.textContent = top < 0
      ? "Pass the quizzes on a rung's pages to climb it. Start at the bottom, because rung 1 is the easiest place to forget."
      : top === 4 ? "You have climbed the whole ladder, from a subtraction to the open problem."
      : "You are on rung " + (top + 1) + ". The next rung is " + st.rungs[top + 1].name + " (" + st.rungs[top + 1].note.toLowerCase() + ").";
    node.appendChild(note);
  }

  function sections(node, st) {
    node.textContent = "";
    st.m.sections.forEach(function (s) {
      var all = [].concat.apply([], s.subs.map(function (g) { return g.pages; }));
      var box = el("details", "psec");
      var head = el("summary", "psec__head");
      head.appendChild(el("span", "psec__name", s.name));
      head.appendChild(bar(count(all, st.scores), all.length));
      head.appendChild(el("span", "psec__count", count(all, st.scores) + "/" + all.length));
      box.appendChild(head);
      var list = el("ul", "psec__pages");
      all.forEach(function (u) {
        var sc = st.scores[u];
        var li = el("li", sc.passed ? "is-done" : sc.answered ? "is-started" : "");
        li.appendChild(link(st.m, u));
        li.appendChild(el("span", "psec__score", sc.answered ? sc.right + "/" + sc.total : "–"));
        list.appendChild(li);
      });
      box.appendChild(list);
      node.appendChild(box);
    });
  }

  function finalCta(node, st) {
    node.textContent = "";
    var best = st.store.final, total = st.m.final.total;
    node.classList.toggle("is-unlocked", st.cert);
    node.appendChild(icon(st.m, st.cert ? "trophy" : "lock", "final-cta__icon"));
    var body = el("div", "final-cta__body");
    if (st.cert) {
      body.appendChild(el("strong", null, "You passed every page quiz" + (best ? " and scored " + best.best + " out of " + total + " on the final test" : "") + "."));
      body.appendChild(el("span", null, " Your certificate is unlocked."));
      var a = el("a", "md-button md-button--primary", "Make your certificate");
      a.href = new URL("quizzes/certificate/", ROOT).href;
      body.appendChild(a);
    } else {
      // Two steps, ticked off as they are done: every page quiz, then the final test.
      body.appendChild(el("strong", null, "Two things unlock your certificate."));
      var steps = el("ul", "final-cta__steps");
      var step = function (done, text) {
        var li = el("li", done ? "is-done" : "");
        li.appendChild(icon(st.m, done ? "check-decagram" : "lock"));
        li.appendChild(el("span", null, text));
        steps.appendChild(li);
        return li;
      };
      var left = st.learn.length - st.passed;
      var quizzes = step(!left, left ? "Pass every page quiz. You have passed " + st.passed + " of " + st.learn.length + "." : "Every page quiz passed.");
      if (left) {
        quizzes.appendChild(bar(st.passed, st.learn.length));
        if (st.next) {
          var nx = el("span", "final-cta__next");
          nx.appendChild(document.createTextNode("Next to pass is "));
          nx.appendChild(link(st.m, st.next));
          nx.appendChild(document.createTextNode("."));
          quizzes.appendChild(nx);
        }
      }
      step(!!best, best ? "Final test passed with " + best.best + " out of " + total + "."
        : "Score " + st.m.final.pass + " or more out of " + total + " on the final test. You can try it as often as you like.");
      body.appendChild(steps);
      if (!document.querySelector(".cert")) {
        var see = el("a", "final-cta__sample", "See a sample certificate");
        see.href = new URL("quizzes/certificate/", ROOT).href;
        body.appendChild(see);
      }
    }
    node.appendChild(body);
  }

  // Ticks next to links to passed pages: index cards, tables and the sidebar.
  function markLinks(st) {
    var done = {};
    Object.keys(st.scores).forEach(function (u) {
      if (st.scores[u].passed) done[path(new URL(st.m.pages[u].u, ROOT).href)] = true;
    });
    document.querySelectorAll("a.card, .md-typeset table a, .md-nav--primary .md-nav__link[href]").forEach(function (a) {
      var href = a.getAttribute("href");
      if (!href || href.charAt(0) === "#" || /^(https?:)?\/\//.test(href) && href.indexOf(ROOT.origin) !== 0) return;
      a.classList.toggle("is-passed", !!done[path(a.href)]);
    });
  }

  // ---- practice problems: a "done" toggle on each problem ---------------------------------------

  // The four levels, by the letter that starts each problem's code.
  var LEVELS = [["B", "Beginner", "beginner"], ["A", "Amateur", "amateur"], ["S", "Semi-pro", "semipro"], ["P", "Pro", "pro"]];

  function practice(node, st) {
    var heads = Array.prototype.filter.call(document.querySelectorAll(".md-typeset h3"), function (h) {
      return /^[BASP]\d+\s·/.test(h.textContent.trim());
    });
    var solver = BADGES.filter(function (b) { return b.id === "practice"; })[0];
    function draw() {
      var done = readJSON(PRACTICE, {});
      node.textContent = "";
      var n = heads.filter(function (h) { return done[h.textContent.trim().split(/\s/)[0]]; }).length;
      // The board: the Problem solver badge, one tile per level and one square per problem.
      var top = el("div", "pboard__top");
      if (st) top.appendChild(medal(st, solver));
      var intro = el("p", "pboard__intro");
      intro.appendChild(document.createTextNode("You have marked "));
      intro.appendChild(el("strong", null, n + " of " + heads.length));
      intro.appendChild(document.createTextNode(n >= 5 ? " problems as done. Problem solver is yours, so keep climbing the levels."
        : " problems as done in this browser. Mark " + (5 - n) + " more to earn the Problem solver badge."));
      top.appendChild(intro);
      node.appendChild(top);
      var levels = el("div", "pboard__levels");
      LEVELS.forEach(function (lv) {
        var mine = heads.filter(function (h) { return h.textContent.trim().charAt(0) === lv[0]; });
        if (!mine.length) return;
        var c = mine.filter(function (h) { return done[h.textContent.trim().split(/\s/)[0]]; }).length;
        var tile = el("div", "pboard__level pboard__level--" + lv[2] + (c === mine.length ? " is-done" : ""));
        var name = el("span", "pboard__name");
        name.appendChild(el("span", "lvl lvl--" + lv[2]));
        name.appendChild(document.createTextNode(lv[1]));
        tile.appendChild(name);
        tile.appendChild(el("span", "pboard__count", c + "/" + mine.length));
        var cells = el("span", "pboard__cells");
        mine.forEach(function (h) {
          var code = h.textContent.trim().split(/\s/)[0];
          var cell = el("a", "pboard__cell" + (done[code] ? " is-done" : ""));
          cell.href = "#" + h.id;
          cell.title = code + (done[code] ? ", done" : ", not done yet");
          cell.setAttribute("aria-label", cell.title);
          cells.appendChild(cell);
        });
        tile.appendChild(cells);
        levels.appendChild(tile);
      });
      node.appendChild(levels);
      heads.forEach(function (h) {
        var code = h.textContent.trim().split(/\s/)[0];
        var b = h.querySelector(".practice-done");
        if (!b) {
          b = el("button", "practice-done");
          b.type = "button";
          b.addEventListener("click", function () {
            var d = readJSON(PRACTICE, {});
            if (d[code]) delete d[code]; else d[code] = new Date().toISOString().slice(0, 10);
            writeJSON(PRACTICE, d);
            draw();
            document.dispatchEvent(new CustomEvent("mul:quiz", { detail: { id: "practice:" + code } }));
          });
          h.appendChild(b);
        }
        var on = !!done[code];
        b.classList.toggle("is-done", on);
        b.textContent = on ? "Done" : "Mark as done";
        b.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }
    draw();
  }

  // ---- badge toasts -------------------------------------------------------------------------

  function toast(st, b) {
    var m = st.m;
    var t = el("div", "ptoast");
    t.setAttribute("role", "status");
    var medal = el("span", "badge__medal" + (b.ink ? " badge__medal--ink" : ""));
    medal.style.setProperty("--badge", b.color);
    medal.appendChild(icon(m, b.icon));
    t.appendChild(medal);
    var body = el("div", "ptoast__body");
    body.appendChild(el("span", "ptoast__kicker", "Badge earned"));
    body.appendChild(el("strong", null, b.name));
    if (b.final && !st.cert) {
      body.appendChild(el("span", null, "Pass every page quiz to unlock your certificate."));
    } else if (b.final) {
      var a = el("a", null, "Make your certificate →");
      a.href = new URL("quizzes/certificate/", ROOT).href;
      body.appendChild(a);
    } else {
      body.appendChild(el("span", null, b.text));
    }
    t.appendChild(body);
    var stack = document.querySelector(".ptoasts");
    if (!stack) { stack = el("div", "ptoasts"); document.body.appendChild(stack); }
    stack.appendChild(t);
    setTimeout(function () { t.classList.add("is-leaving"); }, 5200);
    setTimeout(function () { t.remove(); }, 5800);
  }

  // ---- the certificate ------------------------------------------------------------------------

  function niceDate(iso) {
    var d = new Date(iso + "T12:00:00");
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }

  // Names are typed by the reader, so keep only printable text of a sensible length. The name is
  // only ever drawn onto a canvas or put in a URL, never into the page as HTML.
  function cleanName(s) {
    return String(s || "").normalize("NFC")
      .replace(/[\u0000-\u001F\u007F-\u009F​-‏‪-‮⁠-⁯﻿]/g, "")
      .replace(/\s+/g, " ").trim().slice(0, 48);
  }
  function nameProblem(s) {
    if (s.length < 2) return "Type the name you want on the certificate.";
    if ((s.match(/\p{L}/gu) || []).length < 2) return "A name needs at least two letters.";
    if (/:\/\/|www\.|[<>{}\[\]\\]/i.test(s)) return "Please use just your name, without links or symbols.";
    return "";
  }

  // A short ID printed on the certificate, so a listing in the Hall of Finishers can be matched to
  // it. It is not a secret and proves nothing by itself: only a listed ID is verified.
  var B32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
  function certId(st, name) {
    var store = st.store;
    if (!store.nonce) {
      store.nonce = Math.random().toString(36).slice(2, 10);
      writeJSON(STORE, store);
    }
    var text = [name.toLowerCase(), store.final.best, store.final.date, store.nonce].join("|");
    var h1 = 0xdeadbeef, h2 = 0x41c6ce57;
    for (var i = 0; i < text.length; i++) {
      var ch = text.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 2654435761); h2 = Math.imul(h2 ^ ch, 1597334677);
    }
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
    var bits = ((h2 >>> 0) % 256) * 4294967296 + (h1 >>> 0), out = "";
    for (var k = 0; k < 8; k++) { out = B32[bits % 32] + out; bits = Math.floor(bits / 32); }
    return "MU-" + out.slice(0, 4) + "-" + out.slice(4);
  }

  function covered(st) {
    var chips = [];
    st.m.sections.forEach(function (s) {
      if (s.name === "Start here") return;
      s.subs.forEach(function (g) {
        if (count(g.pages, st.scores) * 2 >= g.pages.length && chips.indexOf(g.name) < 0) chips.push(g.name);
      });
    });
    return chips;
  }

  function seeded(seed) {
    var h = 2166136261;
    for (var i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h = Math.imul(h, 16777619); }
    return function () {
      h += 0x6D2B79F5;
      var t = h;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function roundRect(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath();
  }

  function drawIcon(c, d, x, y, size, color) {
    c.save();
    c.translate(x, y);
    c.scale(size / 24, size / 24);
    c.fillStyle = color;
    c.fill(new Path2D(d));
    c.restore();
  }

  function wrap(c, text, maxWidth) {
    var words = text.split(" "), lines = [], line = "";
    words.forEach(function (w) {
      var test = line ? line + " " + w : w;
      if (c.measureText(test).width > maxWidth && line) { lines.push(line); line = w; } else line = test;
    });
    if (line) lines.push(line);
    return lines;
  }

  var PAPER = "#F7F3EA", INK = "#15171B", SOFT = "#4C4841", MUTED = "#716B5F", BLUE = "#3D5AFE",
      YELLOW = "#FFC300", GREEN = "#2E7D53", ORANGE = "#E8833A", RED = "#B4441F";
  var SANS = "Outfit, system-ui, sans-serif", MONO = "'JetBrains Mono', ui-monospace, monospace";

  function drawCertificate(canvas, st, name, id, sample) {
    var W = 1600, H = 1000, m = st.m, c = canvas.getContext("2d");
    canvas.width = W; canvas.height = H;
    var rand = seeded(name || "machine unlearning");
    var best = st.store.final;

    c.fillStyle = PAPER; c.fillRect(0, 0, W, H);

    // Confetti in the brand colours, kept to the margins so it never sits under the text.
    var palette = [BLUE, YELLOW, GREEN, ORANGE, RED, BLUE, YELLOW];
    for (var i = 0; i < 70; i++) {
      var x = 50 + rand() * (W - 100), y = 50 + rand() * (H - 100);
      var inText = x > 90 && x < 1300 && y > 190 && y < 900;
      var inSeal = Math.hypot(x - 1420, y - 175) < 140;
      if (inText || inSeal) continue;
      c.save();
      c.translate(x, y); c.rotate(rand() * Math.PI);
      c.fillStyle = c.strokeStyle = palette[i % palette.length];
      c.globalAlpha = .75;
      var kind = i % 4, s = 6 + rand() * 9;
      if (kind === 0) { c.fillRect(-s, -s / 2.5, s * 2, s / 1.25); }
      else if (kind === 1) { c.beginPath(); c.arc(0, 0, s / 1.6, 0, Math.PI * 2); c.fill(); }
      else if (kind === 2) { c.beginPath(); c.moveTo(0, -s); c.lineTo(s, s); c.lineTo(-s, s); c.closePath(); c.fill(); }
      else { c.lineWidth = 3.5; c.lineCap = "round"; c.beginPath(); c.moveTo(-s * 1.4, 0);
             c.quadraticCurveTo(-s * .7, -s, 0, 0); c.quadraticCurveTo(s * .7, s, s * 1.4, 0); c.stroke(); }
      c.restore();
    }

    // Frame: a heavy ink rule and a thin blue one, square corners like the site.
    c.strokeStyle = INK; c.lineWidth = 6; c.strokeRect(24, 24, W - 48, H - 48);
    c.strokeStyle = BLUE; c.lineWidth = 2; c.strokeRect(40, 40, W - 80, H - 80);

    // Masthead.
    c.fillStyle = BLUE; c.beginPath(); c.arc(118, 108, 32, 0, Math.PI * 2); c.fill();
    drawIcon(c, m.icons.eraser, 98, 88, 40, "#FFFFFF");
    c.fillStyle = INK; c.font = "700 24px " + MONO; c.textBaseline = "alphabetic";
    c.fillText("MACHINE UNLEARNING", 166, 104);
    c.fillStyle = MUTED; c.font = "400 17px " + MONO;
    c.fillText("A course on making AI models forget", 166, 130);

    // Seal: a yellow starburst with the trophy and the score.
    var sx = 1420, sy = 175;
    c.fillStyle = YELLOW; c.beginPath();
    for (var k = 0; k < 32; k++) {
      var a = k * Math.PI / 16, r = k % 2 ? 98 : 116;
      c.lineTo(sx + Math.cos(a) * r, sy + Math.sin(a) * r);
    }
    c.closePath(); c.fill();
    c.fillStyle = INK; c.beginPath(); c.arc(sx, sy, 80, 0, Math.PI * 2); c.fill();
    drawIcon(c, m.icons.trophy, sx - 30, sy - 56, 60, YELLOW);
    c.fillStyle = "#FFFFFF"; c.textAlign = "center"; c.font = "700 30px " + MONO;
    c.fillText(best ? best.best + "/" + m.final.total : "", sx, sy + 34);
    c.font = "400 13px " + MONO; c.fillStyle = YELLOW;
    c.fillText("FINAL TEST", sx, sy + 56);
    c.textAlign = "left";

    // The words.
    var X = 110;
    c.fillStyle = BLUE; c.font = "700 22px " + MONO;
    c.fillText("CERTIFICATE OF COMPLETION", X, 238);
    c.fillStyle = SOFT; c.font = "400 30px " + SANS;
    c.fillText("Hooray! This one goes to", X, 292);

    var display = name || "Your name here";
    var size = 104;
    c.font = "700 " + size + "px " + SANS;
    while (c.measureText(display).width > 1150 && size > 48) { size -= 4; c.font = "700 " + size + "px " + SANS; }
    var nw = c.measureText(display).width;
    c.fillStyle = "rgba(255, 195, 0, .55)";
    c.fillRect(X - 10, 392 - size * .32, nw + 24, size * .38);
    c.fillStyle = name ? INK : MUTED;
    c.fillText(display, X, 392);

    c.fillStyle = INK; c.font = "400 30px " + SANS;
    var sentence = "for making a model forget. They finished the Machine Unlearning course and passed the final test with " +
      (best ? best.best : "–") + " out of " + m.final.total + ".";
    wrap(c, sentence, 1180).forEach(function (line, n) { c.fillText(line, X, 462 + n * 42); });

    // Topics as chips.
    var chips = covered(st), label = "TOPICS COVERED";
    if (chips.length < 3) { chips = m.rungs.map(function (r) { return r.name; }); label = "THE FINAL TEST COVERED"; }
    c.fillStyle = MUTED; c.font = "700 15px " + MONO;
    c.fillText(label, X, 572);
    var cx = X, cy = 590, maxX = 1490, rows = 1, shown = 0;
    c.font = "500 19px " + SANS;
    for (var t = 0; t < chips.length; t++) {
      var w = c.measureText(chips[t]).width + 62;
      // Two rows at most. The second row keeps room at its end for a "+N more" label.
      var limit = rows === 2 && t < chips.length - 1 ? maxX - 110 : maxX;
      if (cx + w > limit) {
        if (rows === 2) break;
        cx = X; cy += 54; rows++;
        if (t < chips.length - 1 && cx + w > maxX - 110) break;
      }
      roundRect(c, cx, cy, w, 42, 21);
      c.fillStyle = "#FFFFFF"; c.fill();
      c.strokeStyle = "#C9D0FF"; c.lineWidth = 2; c.stroke();
      c.fillStyle = GREEN; c.beginPath(); c.arc(cx + 22, cy + 21, 11, 0, Math.PI * 2); c.fill();
      drawIcon(c, m.icons["check-bold"], cx + 14, cy + 13, 16, "#FFFFFF");
      c.fillStyle = INK; c.fillText(chips[t], cx + 42, cy + 28);
      cx += w + 10; shown++;
    }
    if (shown < chips.length) { c.fillStyle = MUTED; c.fillText("+" + (chips.length - shown) + " more", cx, cy + 28); }

    // Badges as medallions.
    var earned = BADGES.filter(function (b) { return st.store.badges[b.id]; });
    c.fillStyle = MUTED; c.font = "700 15px " + MONO;
    c.fillText("BADGES EARNED", X, 735);
    // Up to seven badges get full-size medallions; more are drawn smaller so all of them fit.
    var gap = earned.length > 7 ? 124 : 150, rad = earned.length > 7 ? 32 : 38;
    earned.forEach(function (b, n) {
      var bx = X + 40 + n * gap, by = 795;
      c.fillStyle = b.color; c.beginPath(); c.arc(bx, by, rad, 0, Math.PI * 2); c.fill();
      c.strokeStyle = PAPER; c.lineWidth = 4; c.beginPath(); c.arc(bx, by, rad - 6, 0, Math.PI * 2); c.stroke();
      drawIcon(c, m.icons[b.icon], bx - rad * .47, by - rad * .47, rad * .95, b.ink ? INK : "#FFFFFF");
      c.fillStyle = INK; c.font = "600 " + (earned.length > 7 ? 15 : 18) + "px " + SANS; c.textAlign = "center";
      c.fillText(b.name, bx, by + 64);
      c.textAlign = "left";
    });

    // Footer.
    c.strokeStyle = "#DDD6C6"; c.lineWidth = 1.5;
    c.beginPath(); c.moveTo(X, 895); c.lineTo(W - X, 895); c.stroke();
    c.fillStyle = INK; c.font = "700 18px " + MONO;
    c.fillText((best ? niceDate(best.date).toUpperCase() : "") + (id ? "  ·  ID " + id : ""), X, 928);
    c.textAlign = "right"; c.font = "400 18px " + SANS;
    c.fillText("Course by " + m.author + " · " + m.site.replace(/^https?:\/\//, "").replace(/\/$/, ""), W - X, 928);
    c.textAlign = "center"; c.fillStyle = MUTED;
    var note = "Self-issued in the learner's browser. Not a qualification, not legal advice. Only IDs listed at " +
      m.site.replace(/^https?:\/\//, "") + "quizzes/finishers/ are verified.";
    var ns = 14;
    c.font = "400 " + ns + "px " + SANS;
    while (c.measureText(note).width > W - 2 * X && ns > 10) { ns--; c.font = "400 " + ns + "px " + SANS; }
    c.fillText(note, W / 2, 956);
    c.textAlign = "left";

    // A sample carries a large watermark, so it can never pass for a real certificate.
    if (sample) {
      c.save();
      c.translate(W / 2, H / 2); c.rotate(-.32);
      c.textAlign = "center"; c.textBaseline = "middle"; c.font = "700 230px " + SANS;
      c.fillStyle = "rgba(232, 67, 42, .10)"; c.strokeStyle = "rgba(232, 67, 42, .35)"; c.lineWidth = 3;
      c.fillText("SAMPLE", 0, 0); c.strokeText("SAMPLE", 0, 0);
      c.restore();
    }
  }

  // What a finished learner's certificate looks like, for the page before it is unlocked.
  function sampleState(st) {
    var today = new Date().toISOString().slice(0, 10), scores = {};
    Object.keys(st.m.pages).forEach(function (u) { scores[u] = { passed: true }; });
    var badges = {};
    ["first", "perfect", "ml", "unlearning", "policy", "scenarios", "finisher"].forEach(function (k) { badges[k] = today; });
    return { m: st.m, scores: scores, store: { final: { best: 18, date: today }, badges: badges } };
  }

  function fontsReady() {
    return document.fonts ? Promise.all([
      document.fonts.load("700 40px Outfit"), document.fonts.load("400 30px Outfit"),
      document.fonts.load("700 20px 'JetBrains Mono'"), document.fonts.load("400 20px 'JetBrains Mono'")
    ]).catch(function () {}) : Promise.resolve();
  }

  function shareText(st) {
    return "I just finished the Machine Unlearning course by " + st.m.author + " and passed the final test with " +
      st.store.final.best + "/" + st.m.final.total + ". I learned how to make a trained model forget data, and how to " +
      "check that it really did. " + st.m.site + " #MachineUnlearning #ResponsibleAI";
  }

  // Before a certificate is made: the key terms in plain words, two ticks and a button that stays
  // disabled until both are ticked. Only then is the name form shown and the certificate drawn.
  function termsGate(node, st) {
    var gate = el("div", "cert-gate");
    gate.appendChild(icon(st.m, "gavel", "cert-gate__icon"));
    var body = el("div", "cert-gate__body");
    body.appendChild(el("strong", "cert-gate__title", "Before you make your certificate"));
    body.appendChild(el("p", null, "Your certificate is made only after you accept its terms. In short, these are what they say."));
    var points = el("ul", "cert-gate__points");
    ["It is not a qualification, licence or accreditation, and no university, employer or regulator recognises it.",
     "It does not show that you can give legal advice or that anyone meets a law, regulation or standard.",
     "Nothing in this course is legal advice. Ask a qualified lawyer about real erasure requests.",
     "The course code is research and teaching code, given without any warranty. No method here guarantees that data is removed from a model.",
     "The author is not liable for any loss from using the course, its code or the certificate, as far as the law allows.",
     "You may share it, but not present it as a qualification or endorsement, and not edit it."
    ].forEach(function (t) { points.appendChild(el("li", null, t)); });
    body.appendChild(points);
    var full = el("p", "cert-gate__full");
    full.appendChild(document.createTextNode("These points are a summary. The "));
    var link2 = el("a", null, "full terms of this certificate");
    link2.href = "#terms-of-this-certificate";
    full.appendChild(link2);
    full.appendChild(document.createTextNode(" are below, and they are the ones that apply."));
    body.appendChild(full);
    var go = el("button", "md-button md-button--primary", "Make my certificate");
    go.type = "button";
    go.disabled = true;
    var ticks = [];
    function tick(text) {
      var lab = el("label", "cert-gate__tick");
      var box = el("input");
      box.type = "checkbox";
      box.addEventListener("change", function () { go.disabled = !ticks.every(function (b) { return b.checked; }); });
      ticks.push(box);
      lab.appendChild(box);
      lab.appendChild(el("span", null, text));
      body.appendChild(lab);
    }
    tick("I have read the full terms of this certificate and I understand them.");
    tick("I accept them, including that this certificate is not a qualification and not legal advice.");
    go.addEventListener("click", function () {
      if (go.disabled) return;
      st.store.terms = { version: TERMS, date: new Date().toISOString().slice(0, 10) };
      writeJSON(STORE, st.store);
      node.textContent = "";
      certificate(node, st);
    });
    body.appendChild(go);
    gate.appendChild(body);
    node.appendChild(gate);
  }

  function certificate(node, st) {
    node.textContent = "";
    if (!st.cert) {
      var locked = el("div", "final-cta");
      node.appendChild(locked);
      finalCta(locked, st);
      node.appendChild(el("p", "cert__sample-note", "Here is a sample of what yours will look like, with your name, your score, the topics you covered and the badges you earned."));
      var frame0 = el("div", "cert__frame cert__frame--sample");
      var sample = el("canvas", "cert__canvas");
      sample.setAttribute("role", "img");
      sample.setAttribute("aria-label", "A sample certificate of completion, marked SAMPLE");
      frame0.appendChild(sample);
      node.appendChild(frame0);
      var demo = sampleState(st);
      var drawSample = function () { drawCertificate(sample, demo, "Ada Lovelace", "MU-SAMP-LE00", true); };
      drawSample();
      fontsReady().then(drawSample);
      return;
    }
    if (!st.store.terms || st.store.terms.version !== TERMS) { termsGate(node, st); return; }
    var form = el("div", "cert__form");
    var lab = el("label", "cert__label", "Your name, as you want it on the certificate");
    lab.htmlFor = "cert-name";
    var input = el("input", "cert__input");
    input.id = "cert-name"; input.type = "text"; input.maxLength = 48; input.autocomplete = "name";
    input.value = cleanName((st.store.cert && st.store.cert.name) || localStorage.getItem(NAME) || "");
    var msg = el("p", "cert__msg");
    msg.setAttribute("aria-live", "polite");
    // Once a certificate has left the page, its name is locked in this browser. Changing it is allowed
    // (typos happen) but deliberate, and gives a new ID, so one pass does not quietly become many.
    var change = el("button", "cert__change", "Change name");
    change.type = "button";
    var terms = el("p", "cert__accepted");
    terms.appendChild(document.createTextNode("You accepted the terms of this certificate on " + niceDate(st.store.terms.date) + ". "));
    var again = el("a", null, "Read them again");
    again.href = "#terms-of-this-certificate";
    terms.appendChild(again);
    terms.appendChild(document.createTextNode("."));
    form.appendChild(lab); form.appendChild(input); form.appendChild(change); form.appendChild(terms); form.appendChild(msg);
    node.appendChild(form);

    var frame = el("div", "cert__frame");
    var canvas = el("canvas", "cert__canvas");
    canvas.setAttribute("role", "img");
    frame.appendChild(canvas);
    node.appendChild(frame);

    var actions = el("div", "cert__actions");
    function button(text, primary, onClick) {
      var b = el("button", "md-button" + (primary ? " md-button--primary" : ""), text);
      b.type = "button"; b.addEventListener("click", onClick); actions.appendChild(b); return b;
    }
    function current() {
      var n = cleanName(input.value), problem = nameProblem(n);
      msg.textContent = problem; msg.classList.toggle("is-bad", !!problem && input.value.length > 0);
      return problem ? "" : n;
    }
    function slug(n) { return n.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "-").replace(/^-|-$/g, "") || "certificate"; }
    function blob(cb) { canvas.toBlob(cb, "image/png"); }
    function need() {
      var n = current();
      if (!n) input.focus();
      return n;
    }
    function idFor(n) {
      return st.store.cert && st.store.cert.name === n ? st.store.cert.id : certId(st, n);
    }
    function lock(n) {
      if (!st.store.cert) { st.store.cert = { name: n, id: certId(st, n) }; writeJSON(STORE, st.store); }
      setLocked();
    }
    function setLocked() {
      var on = !!st.store.cert;
      input.readOnly = on;
      form.classList.toggle("is-locked", on);
      change.hidden = !on;
    }
    change.addEventListener("click", function () {
      if (!confirm("A certificate is personal: please make one only for yourself.\n\nChanging the name gives the " +
        "certificate a new ID, so any copy you already shared will no longer match a Hall of Finishers listing.")) return;
      delete st.store.cert; writeJSON(STORE, st.store);
      setLocked(); input.focus(); input.select();
    });

    var dl = button("Download image", true, function () {
      var n = need(); if (!n) return;
      lock(n);
      blob(function (b) {
        var a = el("a"); a.href = URL.createObjectURL(b); a.download = "machine-unlearning-" + slug(n) + ".png";
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
      });
    });
    button("Post on LinkedIn", false, function () {
      var n = need(); if (!n) return;
      lock(n);
      var text = shareText(st);
      try { navigator.clipboard.writeText(text); } catch (e) { /* not allowed */ }
      msg.textContent = "Opening LinkedIn with a post ready. Add the downloaded image to it before you post.";
      msg.classList.remove("is-bad");
      window.open("https://www.linkedin.com/feed/?shareActive=true&text=" + encodeURIComponent(text), "_blank", "noopener");
    });
    button("Post on X", false, function () {
      var n = need(); if (!n) return;
      lock(n);
      window.open("https://x.com/intent/post?text=" + encodeURIComponent(shareText(st)), "_blank", "noopener");
    });
    if (navigator.canShare) {
      button("Share…", false, function () {
        var n = need(); if (!n) return;
        lock(n);
        blob(function (b) {
          var file = new File([b], "machine-unlearning-" + slug(n) + ".png", { type: "image/png" });
          var data = { files: [file], text: shareText(st), title: "Machine Unlearning certificate" };
          if (navigator.canShare(data)) navigator.share(data).catch(function () { /* cancelled */ });
          else msg.textContent = "This browser cannot share images; use Download image instead.";
        });
      });
    }
    var hall = el("a", "md-button", "Join the Hall of Finishers");
    hall.target = "_blank"; hall.rel = "noopener";
    actions.appendChild(hall);
    node.appendChild(actions);

    function hallLink(n) {
      var body = "Please add me to the Hall of Finishers.\n\n" +
        "- Name: " + n + "\n- Certificate ID: " + idFor(n) + "\n- Final test score: " + st.store.final.best + "/" +
        st.m.final.total + "\n- Date passed: " + st.store.final.date + "\n- LinkedIn profile (optional): \n\n" +
        "I have attached my certificate image below. The name is mine, and matches my GitHub or LinkedIn profile.\n";
      return st.m.repo + "/issues/new?title=" + encodeURIComponent("Hall of Finishers: " + n) +
        "&body=" + encodeURIComponent(body);
    }

    function redraw() {
      var n = current();
      try { if (n) localStorage.setItem(NAME, n); } catch (e) { /* private window */ }
      var id = n ? idFor(n) : "";
      drawCertificate(canvas, st, n, id);
      canvas.setAttribute("aria-label", "Certificate of completion for " + (n || "you") + ", final test " +
        st.store.final.best + " out of " + st.m.final.total);
      hall.href = hallLink(n || "");
      hall.classList.toggle("is-disabled", !n);
      dl.disabled = false;
    }
    hall.addEventListener("click", function (e) {
      var n = current();
      if (!n) { e.preventDefault(); input.focus(); return; }
      lock(n);
    });
    setLocked();
    input.addEventListener("input", redraw);
    // Draw once the brand fonts are ready, or the first frame falls back to system fonts.
    redraw();
    fontsReady().then(redraw);
  }

  // Hall of Finishers: check a certificate ID against the hand-checked list on the page.
  function verifyBox(node) {
    if (node.dataset.ready) return;
    node.dataset.ready = "1";
    var label = el("label", "cert__label", "Certificate ID");
    label.htmlFor = "verify-id";
    var row = el("div", "verify__row");
    var input = el("input", "cert__input verify__input");
    input.id = "verify-id"; input.placeholder = "MU-ABCD-2345"; input.maxLength = 14; input.autocomplete = "off";
    var go = el("button", "md-button md-button--primary", "Check");
    go.type = "button";
    row.appendChild(input); row.appendChild(go);
    var out = el("p", "verify__out");
    out.setAttribute("aria-live", "polite");
    node.appendChild(label); node.appendChild(row); node.appendChild(out);
    function check() {
      var id = input.value.toUpperCase().replace(/\s+/g, "");
      if (/^MU[A-Z2-7]{8}$/.test(id)) id = "MU-" + id.slice(2, 6) + "-" + id.slice(6);
      input.value = id;
      out.className = "verify__out";
      out.textContent = "";
      if (!/^MU-[A-Z2-7]{4}-[A-Z2-7]{4}$/.test(id)) { out.textContent = "An ID looks like MU-ABCD-2345."; return; }
      var hit = document.querySelector('.hall__row[data-id="' + id + '"]');
      if (hit) {
        out.classList.add("is-verified");
        out.appendChild(el("strong", null, "Verified. "));
        out.appendChild(document.createTextNode("This certificate belongs to " + hit.dataset.name + ", listed in the Hall of Finishers."));
      } else {
        out.classList.add("is-unknown");
        out.appendChild(el("strong", null, "Not listed. "));
        out.appendChild(document.createTextNode("The certificate may be real, but it is self-issued and has not been checked."));
      }
    }
    go.addEventListener("click", check);
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") check(); });
    if (/^#?MU-/.test(location.hash)) { input.value = decodeURIComponent(location.hash.slice(1)); check(); }
  }

  function resetButton(node) {
    node.textContent = "";
    var b = el("button", "md-button", "Clear all my progress");
    b.type = "button";
    b.addEventListener("click", function () {
      if (!confirm("Clear every quiz answer, badge and your certificate name from this browser?")) return;
      try {
        Object.keys(localStorage).forEach(function (k) {
          if (k.indexOf(QUIZ) === 0 || k === STORE || k === NAME) localStorage.removeItem(k);
        });
      } catch (e) { /* private window */ }
      render(false);
    });
    node.appendChild(b);
  }

  // ---- wiring -------------------------------------------------------------------------------

  var wasPassed = {};

  function render(announce) {
    getManifest().then(function (m) {
      var st = compute(m, announce);
      document.querySelectorAll(".pstrip[data-section]").forEach(function (n) { strip(n, st); });
      document.querySelectorAll(".psum").forEach(function (n) { summary(n, st); });
      document.querySelectorAll(".badge-shelf").forEach(function (n) { shelf(n, st); });
      document.querySelectorAll(".ladder-climb").forEach(function (n) { climb(n, st); });
      document.querySelectorAll(".section-progress").forEach(function (n) { sections(n, st); });
      document.querySelectorAll(".final-cta").forEach(function (n) { finalCta(n, st); });
      document.querySelectorAll(".progress-reset").forEach(resetButton);
      document.querySelectorAll(".hall-verify").forEach(verifyBox);
      document.querySelectorAll(".practice-tracker").forEach(function (n) { practice(n, st); });
      document.querySelectorAll(".pwelcome").forEach(function (n) { welcome(n, st); });
      document.querySelectorAll(".cert").forEach(function (n) { if (!n.dataset.ready) { n.dataset.ready = "1"; certificate(n, st); } });
      var uri = here(m);
      // Celebrate only the answer that turns this page from not passed to passed.
      var justPassed = announce && uri && st.scores[uri] && st.scores[uri].passed && wasPassed[uri] === false;
      chip(st, uri);
      result(st, uri, justPassed);
      wasPassed = {};
      Object.keys(st.scores).forEach(function (u) { wasPassed[u] = st.scores[u].passed; });
      markLinks(st);
      if (announce) st.fresh.forEach(function (b, i) { setTimeout(function () { toast(st, b); }, i * 700); });
    }).catch(function () { /* the map is missing, e.g. a page opened from disk: show nothing */ });
  }

  document.addEventListener("mul:quiz", function () { render(true); });
  if (typeof document$ !== "undefined") document$.subscribe(function () { render(false); });
  else document.addEventListener("DOMContentLoaded", function () { render(false); });
})();
