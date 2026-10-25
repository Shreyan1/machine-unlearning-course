---
title: How to use this site
description: What each part of the site is for, and how the explainers, quizzes and notebooks fit together.
---

# How to use this site

The site has three parts. Each one does a different job.

| Part | What it is | Use it when... |
|---|---|---|
| [ML Basics](../ml-basics/index.md) | Short pages on the machine learning the course needs | you are new to ML, or want a quick refresher |
| [Unlearning](../unlearning/index.md) | One idea per page, from "deleting is not forgetting" to "unlearning at scale" | you want to understand a concept |
| [Lessons](../lessons/index.md) | A summary of each of the 22 notebooks, with its key results | you want to see the idea in action, with real numbers |

## The learning loop

<ol class="steps" markdown>
<li markdown>**Read a concept page.** Start with the "In one line" box, then the simple example.</li>
<li markdown>**Take its quiz.** Every page ends with three to five questions. Each answer tells you *why* it is right or wrong.</li>
<li markdown>**Run the lesson notebook.** Every lesson page has an **Open in Colab** button. It runs in your browser, with nothing to install.</li>
<li markdown>**Do the tasks.** Each notebook ends with a `TASK` section. That is where most of the learning happens.</li>
<li markdown>**Practise.** When you finish a stage, try the matching [practice problems](../practice.md).</li>
</ol>

## How a concept page is laid out

Every concept page uses the same sections, so you always know where to look:

- **In one line**: the whole idea in one sentence.
- **Why it matters**: what goes wrong without it.
- **A simple example**: an everyday picture first, then the course example (usually Carol).
- **How it works**: the steps, often with a diagram.
- **In code**: a short snippet from the course library, `mul/`.
- **Common mistakes**: the traps people fall into.
- **Key takeaways**: what to remember.
- **Quiz** and **Try it**: check yourself, then run it.

## About the quizzes

- Click an answer to check it. You get one try per question; the explanation appears straight away.
- Your score is saved **in your own browser only**. Nobody else can see it, and nothing is sent anywhere.
- Press **Try again** to clear a quiz and start over.
- The [Quizzes](../quizzes/index.md) page lists every quiz with your saved score, and there is a 20-question
  [final test](../quizzes/final.md).

## Running the notebooks on your own computer

You can also run everything locally. It works on an ordinary laptop, with no GPU.

```bash
git clone https://github.com/Shreyan1/machine-unlearning-course.git
cd machine-unlearning-course
python -m venv .mulvenv
source .mulvenv/bin/activate      # Windows: .mulvenv\Scripts\activate
pip install -r requirements.txt
python tests/test_mul.py          # checks the library, about 1 minute
```

Most notebooks finish in under a minute. Only the optional Lesson 16b needs PyTorch.

## Two kinds of boxes in the notebooks

The notebooks have two kinds of explanation boxes. This site mostly uses the first kind.

- <span class="lvl lvl--beginner"></span>**In plain words**: the idea with no maths, usually with an everyday comparison.
- <span class="lvl lvl--pro"></span>**For practitioners**: the formal definition, the paper it comes from and how it fails in production.

## Quiz

```quiz
- q: You want to see an idea working with real numbers. Where should you go?
  options:
    - The glossary
    - The lesson page and its notebook
    - The About page
  answer: 1
  why: Lesson pages summarise each notebook's results, and the Colab button lets you run it yourself.
- q: Where are your quiz scores stored?
  options:
    - On a server, under your name
    - Only in your own browser
    - In the GitHub repository
  answer: 1
  why: Scores are kept in your browser's local storage. Nothing is sent anywhere.
- q: Which part of each notebook is said to be where most of the learning happens?
  options:
    - The title
    - The TASK section at the end
    - The import cell
  answer: 1
  why: The tasks make you change the code and explain what happens, which is how the ideas stick.
```
