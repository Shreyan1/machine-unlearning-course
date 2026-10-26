// Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
// Clickable quizzes. hooks/quiz.py writes the HTML; this file adds the clicks,
// the feedback and the saved score. Scores live in this browser only.
(function () {
  var PREFIX = "mul-quiz:";

  function load(id) {
    try { return JSON.parse(localStorage.getItem(PREFIX + id)) || {}; } catch (e) { return {}; }
  }
  function save(id, state) {
    try { localStorage.setItem(PREFIX + id, JSON.stringify(state)); } catch (e) { /* private window */ }
  }
  function clear(id) {
    try { localStorage.removeItem(PREFIX + id); } catch (e) { /* private window */ }
  }
  // Tell progress.js a score changed, so badges and progress bars update without a reload.
  function changed(id) {
    document.dispatchEvent(new CustomEvent("mul:quiz", { detail: { id: id } }));
  }

  function showAnswer(q, picked) {
    var answer = Number(q.dataset.answer);
    var opts = q.querySelectorAll(".quiz__opt");
    opts.forEach(function (b, i) {
      b.disabled = true;
      if (i === answer) b.classList.add("is-correct");
      if (i === picked && picked !== answer) b.classList.add("is-wrong");
      if (i === picked) b.setAttribute("aria-pressed", "true");
    });
    var right = picked === answer;
    q.classList.add(right ? "got-it" : "missed");
    var why = q.querySelector(".quiz__why");
    why.querySelector(".quiz__verdict").textContent = right ? "Correct!" : "Not quite.";
    why.hidden = false;
  }

  function countRight(quiz, state) {
    var right = 0;
    quiz.querySelectorAll(".quiz__q").forEach(function (q, n) {
      if (state[n] !== undefined && state[n] === Number(q.dataset.answer)) right++;
    });
    return right;
  }

  function updateScore(quiz, state) {
    var total = Number(quiz.dataset.total);
    var answered = Object.keys(state).length;
    var right = countRight(quiz, state);
    var label = quiz.querySelector(".quiz__score");
    if (answered < total) {
      label.textContent = answered
        ? "You have answered " + answered + " of " + total + " and got " + right + " right."
        : "Answer all " + total + " questions to see your score.";
    } else {
      label.textContent = "You scored " + right + " out of " + total + "." +
        (right === total ? " Well done!" : right >= total / 2 ? " Good, now read the ones you missed." : " Read the page again and try once more.");
    }
    quiz.classList.toggle("is-done", answered === total);
    var passed = answered === total && right >= Number(quiz.dataset.pass || total);
    quiz.classList.toggle("is-passed", passed);
    var stamp = quiz.querySelector(".quiz__stamp");
    if (stamp) stamp.hidden = !passed;
  }

  // The final test shows its options in a new order on every attempt, so a remembered pattern of
  // letters is no help. Only the order on screen changes; answers are still saved by option number.
  function shuffleOptions(quiz) {
    if (!quiz.dataset.shuffle) return;
    quiz.querySelectorAll(".quiz__options").forEach(function (box) {
      var opts = Array.prototype.slice.call(box.children);
      for (var i = opts.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1)), t = opts[i]; opts[i] = opts[j]; opts[j] = t;
      }
      opts.forEach(function (b, k) { box.appendChild(b); b.querySelector(".quiz__key").textContent = "ABCDEFGH"[k]; });
    });
  }

  function setup(quiz) {
    if (quiz.dataset.ready) return;
    quiz.dataset.ready = "1";
    var id = quiz.dataset.quizId;
    var state = load(id).picks || {};
    var questions = quiz.querySelectorAll(".quiz__q");
    shuffleOptions(quiz);

    questions.forEach(function (q, n) {
      if (state[n] !== undefined) showAnswer(q, state[n]);
      q.querySelectorAll(".quiz__opt").forEach(function (b) {
        b.addEventListener("click", function () {
          if (state[n] !== undefined) return;
          state[n] = Number(b.dataset.i);
          save(id, { picks: state, right: countRight(quiz, state), total: Number(quiz.dataset.total) });
          showAnswer(q, state[n]);
          updateScore(quiz, state);
          changed(id);
        });
      });
    });

    quiz.querySelector(".quiz__reset").addEventListener("click", function () {
      state = {};
      clear(id);
      changed(id);
      shuffleOptions(quiz);
      questions.forEach(function (q) {
        q.classList.remove("got-it", "missed");
        q.querySelector(".quiz__why").hidden = true;
        q.querySelectorAll(".quiz__opt").forEach(function (b) {
          b.disabled = false;
          b.classList.remove("is-correct", "is-wrong");
          b.removeAttribute("aria-pressed");
        });
      });
      updateScore(quiz, state);
    });

    updateScore(quiz, state);
  }

  // On the quiz hub, show the saved score next to each page.
  function fillHub() {
    document.querySelectorAll(".quiz-score").forEach(function (cell) {
      var page = cell.dataset.page;
      var right = 0, answered = 0, total = 0;
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var key = localStorage.key(i);
          if (key.indexOf(PREFIX + page + "#") !== 0) continue;
          var s = JSON.parse(localStorage.getItem(key)) || {};
          answered += Object.keys(s.picks || {}).length;
          right += s.right || 0;
          total += s.total || 0;
        }
      } catch (e) { return; }
      var done = answered >= total && total > 0;
      // 0.6 matches PASS_SHARE in hooks/quiz.py.
      cell.classList.toggle("is-passed", done && right >= Math.ceil(total * 0.6));
      if (!answered) cell.textContent = "Not started";
      else if (!done) cell.textContent = answered + " answered, " + right + " right";
      else cell.textContent = right + " / " + total;
    });
  }

  // Scenarios (hooks/scenario.py): one pick each, with feedback on the pick and on the best call.
  var SCENARIO = "mul-scenario:";
  function setupScenario(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    var id = box.dataset.scenarioId;
    var opts = box.querySelectorAll(".scenario__opt");
    function show(pick) {
      opts.forEach(function (b, i) {
        b.disabled = pick !== null;
        b.classList.toggle("is-picked", i === pick);
        b.classList.toggle("is-best", pick !== null && b.dataset.verdict === "best");
      });
      var mine = { best: "Your pick is the best call.", ok: "Your pick is defensible.", risky: "Your pick is risky." };
      var theirs = { best: "The best call.", ok: "Defensible.", risky: "Risky." };
      box.querySelectorAll(".scenario__fb").forEach(function (fb, i) {
        var verdict = opts[i].dataset.verdict;
        fb.hidden = pick === null || (i !== pick && verdict !== "best");
        fb.classList.toggle("is-picked", i === pick);
        fb.querySelector(".scenario__verdict").textContent = (i === pick ? mine : theirs)[verdict];
      });
      box.classList.toggle("is-done", pick !== null);
      box.querySelector(".quiz__stamp").hidden = pick === null;
    }
    var saved = null;
    try { var v = JSON.parse(localStorage.getItem(SCENARIO + id)); if (v && typeof v.pick === "number") saved = v.pick; } catch (e) { /* none */ }
    opts.forEach(function (b, i) {
      b.addEventListener("click", function () {
        try { localStorage.setItem(SCENARIO + id, JSON.stringify({ pick: i, best: b.dataset.verdict === "best" })); } catch (e) { /* private window */ }
        show(i);
        changed(id);
      });
    });
    box.querySelector(".quiz__reset").addEventListener("click", function () {
      try { localStorage.removeItem(SCENARIO + id); } catch (e) { /* private window */ }
      show(null);
      changed(id);
    });
    show(saved);
  }

  function init() {
    document.querySelectorAll(".quiz").forEach(setup);
    document.querySelectorAll(".scenario").forEach(setupScenario);
    fillHub();
  }

  // Material's instant navigation swaps pages without a reload; document$ fires on each one.
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
