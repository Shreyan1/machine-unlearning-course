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
      label.textContent = answered + " of " + total + " answered" + (answered ? ", " + right + " correct" : "");
    } else {
      label.textContent = "Score: " + right + " / " + total +
        (right === total ? ". Well done!" : right >= total / 2 ? ". Good, now read the ones you missed." : ". Read the page again and retry.");
    }
    quiz.classList.toggle("is-done", answered === total);
  }

  function setup(quiz) {
    if (quiz.dataset.ready) return;
    quiz.dataset.ready = "1";
    var id = quiz.dataset.quizId;
    var state = load(id).picks || {};
    var questions = quiz.querySelectorAll(".quiz__q");

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
      if (!answered) cell.textContent = "not started";
      else if (answered < total) cell.textContent = answered + " answered, " + right + " correct";
      else cell.textContent = right + " / " + total + (right === total ? " ✓" : "");
    });
  }

  function init() {
    document.querySelectorAll(".quiz").forEach(setup);
    fillHub();
  }

  // Material's instant navigation swaps pages without a reload; document$ fires on each one.
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
