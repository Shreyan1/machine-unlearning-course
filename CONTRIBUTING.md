# 🤝 Contributing

Thank you for helping. This course is meant to be the place people send each other to learn machine unlearning
properly, and every fix makes that more true.

There are three kinds of contribution, from smallest to largest:

| Kind | Examples | Start with |
|---|---|---|
| **Fix** | a typo, a broken link, a wrong number in the text, a cell that fails on Colab | a pull request |
| **Improve** | a clearer explanation, a better chart, a missing paper, a new practice problem | an issue, then a pull request |
| **New problem** | a new notebook that climbs a new rung of the Ladder of Forgetting | an issue first (see below) |

---

## 🛠️ Set up

```bash
git clone https://github.com/Shreyan1/machine-unlearning-course.git
cd machine-unlearning-course
python -m venv .mulvenv
source .mulvenv/bin/activate      # Windows: .mulvenv\Scripts\activate
pip install -r requirements.txt
python tests/test_mul.py          # must pass before and after your change
```

---

## ✍️ How the course is written

Please keep these rules. They are what make the notebooks feel like one course and not twenty blog posts.

**1. Simple English.** Write for a reader whose first language may not be English. Short sentences. One idea per
sentence. Explain every term the first time it appears. If a sentence needs reading twice, rewrite it.

**2. The five steps.** Every problem follows the same loop, with these headings:

> **Step 1 : Train** → **Step 2 : Show the issue** → **Step 3 : Untrain** → **Step 4 : Show the result** →
> **Step 5 : Prove it**

You can split a step (Step 3a, Step 3b) or add a short section between steps (a trap, a cost estimate), but keep the
order.

**3. Prove it against the gold band, not against zero.** "Forgotten" means "behaves like a model that never saw the
data". Show where the unlearned model sits compared with several retrained models, not just that a number went down.

**4. Two voices.** Each problem opens with a 🟢 **In plain words** box (an everyday picture, no maths) and a
🔴 **For practitioners** box (the method, the papers, the real-world catch). Add more 🔴 boxes where a practitioner
would ask "so what do I do on Monday?".

**5. A person, not a dataset.** The course follows people who ask to be forgotten: Carol (her handwritten digits),
Dana (her phone number in a language model), Erin (her taste in films). A new problem should have one person whose
request drives the story.

**6. Honest numbers.**
- Every number in the text must come from a cell output in the same notebook. If you change the code, re-run the
  notebook and update the text.
- Fix random seeds so the numbers are the same on every run.
- If a number is a placeholder (a cost, a request rate), say so in the code comment and in the text.
- When a method fails, say it fails. The traps are the most valuable part of the course.

**7. Laptop only.** Every notebook must run end to end on a laptop CPU, ideally in under a minute, with the packages in
`requirements.txt`. PyTorch is allowed only in an optional "b" notebook (like `16b`), with its packages in
`requirements-optional.txt`.

**8. Code lives in `mul/`.** If a function is reused, or longer than about 20 lines, put it in the right `mul/` module
with a short docstring, and introduce it in the notebook first. Keep the notebook code short enough to read.

**9. Cite the papers.** Name the paper in the text (author and year), add it to `resources/catalog.json` and
`resources/README.md`, and never commit a PDF. `resources/fetch_papers.py` downloads them.

**10. Diagrams are code.** New diagrams go in `assets/make_diagrams.py` as a function, so anyone can regenerate them:
`python assets/make_diagrams.py`.

---

## 🪜 Adding a new problem

1. **Open an issue first.** Say which rung of the Ladder of Forgetting it adds, which person's request drives it, what
   the "issue" in Step 2 will show, and the main paper. This avoids two people writing the same notebook, and lets us
   agree on where it goes in the order.
2. **Copy the template** to the repository root with the next number and a short title:
   ```bash
   cp templates/problem-template.ipynb 19-Your-Short-Title.ipynb
   ```
3. **Fill in every section.** The template has a placeholder for each part, with a note on what goes there. Delete the
   notes as you go.
4. **Link it into the course:**
   - the previous notebook's **❓ Open question** should point to yours,
   - add it to the right stage in `README.md` (with its Colab badge) and in `ROADMAP.md`,
   - add one to three practice problems to `PRACTICE.md`,
   - add new papers to `resources/`.
5. **Run the checklist below**, then open a pull request.

---

## ✅ Before you open a pull request

- [ ] `python tests/test_mul.py` passes. If you added to `mul/`, you added a test for it.
- [ ] The notebook runs top to bottom with **Restart & Run All**, on a laptop CPU.
- [ ] The first cell works on Colab (it clones the repo and installs anything missing).
- [ ] Every number in the text matches the output above it.
- [ ] Outputs are saved in the notebook, so readers on GitHub see the results without running it.
- [ ] No data files, PDFs or large outputs are committed (`data/` and `resources/papers/` are ignored).
- [ ] The language is simple, and every new term is explained the first time it appears.
- [ ] README, ROADMAP and notebook counts are updated if you added a notebook.

**Commit messages:** one short line in the imperative, like the existing history: `Add Problem 19: ...`,
`Fix wrong TPR in Problem 12 takeaways`, `Clarify the gold band in Problem 6`.

---

## 🐛 Reporting a problem

Open an issue with:
- the notebook and the cell (or the file and line),
- what you expected and what happened,
- your Python version and whether you ran it locally or on Colab.

A wrong number or a confusing sentence is a real bug here. Please report it.

---

## 📜 Licence

By contributing, you agree that your contribution is released under the [MIT Licence](LICENSE) of this repository.
