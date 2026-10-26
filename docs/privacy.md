---
title: Privacy and your data
description: What this site keeps, where it keeps it, how to delete it and what removal cannot reach.
---

# Privacy and your data

This is a course about removing people's data from models, so it should be careful with yours. In short, this site has
no accounts, no cookies, no analytics and no tracking, and a visit sends nothing to any company other than the host.
Your progress stays in your own browser, and one button deletes all of it.

## What this site does not do

- **No analytics or advertising.** There is no visitor counter, no advertising and no tracking pixel.
- **No cookies.** Nothing on this site sets a cookie.
- **No third-party requests.** Fonts, the maths renderer and the 3D sphere on the home page are served from this site
  itself, so loading a page does not contact Google, a CDN or anyone else.
- **No live GitHub counts.** The link to the code repository does not show a live star count, because fetching it
  would send your IP address to GitHub on every page.
- **No AI training.** Nothing you do here is collected, so nothing you do here can be used to train a model.

## What your browser keeps

Your quiz answers and progress are saved in your browser's local storage on this device. They are never sent anywhere,
and the author cannot see them.

| Item | What it holds | Why |
|---|---|---|
| `mul-quiz:` items | The option you picked for each quiz question | To show your answers and score when you come back |
| `mul-scenario:` items | The option you picked in each scenario | The same, for scenarios |
| `mul-practice` | Which practice problems you marked as done, with the date | For the practice board and the Problem solver badge |
| `mul-progress` | Your badges and their dates, the days you were active (the last 120 at most), your best final test score, the date you accepted the certificate terms and your certificate's name and ID | For badges, the weekly streak and the certificate |
| `mul-cert-name` | The name you typed for your certificate | So you do not have to type it again |
| `__palette` | Light or dark mode | So the site remembers your choice |

## How to delete it

- **On this site.** Press **Clear all my progress** on [Your progress](quizzes/progress.md#start-again). It deletes
  every item above that starts with `mul-`.
- **In your browser.** Clear this site's data in your browser's settings. That also removes your light or dark choice.

There is no other copy, so once you delete it, it is gone for good. A certificate image you already downloaded stays
wherever you saved it.

## Hosting

The site is hosted on GitHub Pages. Like any web host, GitHub receives the technical details every request carries,
such as your IP address and browser, and handles them under the
[GitHub General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
GitHub does not give the author a log of who visits this site.

Pages link to other sites, such as Google Colab, GitHub, research papers and regulators. When you follow a link, that
site's own privacy policy applies.

## The Hall of Finishers

This is the only place the site publishes personal data, and only when you ask it to.

- **What is published.** Your name, your certificate ID and the date you passed. A LinkedIn link is published only if
  you add one.
- **How it gets here.** You open a GitHub issue with these details and your certificate image. GitHub issues are
  public, so anyone can read yours, and it sits under your GitHub account.
- **Why.** Your request, which is your consent. Nothing is listed without it.
- **Withdrawing it.** Open an issue or email the author (see [About](about.md)) at any time. Your entry is removed in
  the next update of the site, and the issue you opened can be deleted on request.

**What removal cannot reach.** Deleting your entry from this site is easy. Copies made while it was public, such as
forks of the repository, web archives and search engine caches, are outside the author's control. This is the problem
the course is about. Deleting the record is not the same as removing every copy of it.

## Data in the course

The notebooks run on your own computer or in your own Google Colab session. The course does not collect anything from
them. They use public research datasets, and some of those describe real people.

| Dataset | What it holds | Used in |
|---|---|---|
| Handwritten digits (UCI, shipped with scikit-learn) | 1,797 small images of handwritten digits | Most lessons, through Carol's story |
| Adult census income (UCI) | Records from the 1994 US Census, including age, sex, race and income band | Lesson 12 |
| Olivetti faces (AT&T Laboratories Cambridge) | 400 photos of 40 real people's faces, taken between 1992 and 1994 | Lesson 13 |
| SMS Spam Collection (UCI) | Real text messages, labelled spam or not spam | Lessons 14, 16 and 16b |
| MovieLens 100K (GroupLens, University of Minnesota) | 100,000 film ratings from 943 users, who are identified only by a number | Lesson 18 |

**Carol is not a real person.** She is a story the course uses, and "her" rows are examples picked from these datasets.

**How the course uses this data.** It uses each dataset for teaching only and follows its terms. It never tries to
identify anyone, and it treats faces as sensitive biometric data. MovieLens is downloaded from GroupLens when you first
need it and is not copied into this repository. Downloads are cached in a `data` folder on your computer, so delete
that folder when you have finished.

## Questions and changes

To ask about your data, open an issue on the
[issue tracker](https://github.com/Shreyan1/machine-unlearning-course/issues) or email the author (see
[About](about.md)). If this page changes, the date below changes with it.

*Last updated 26 October 2026.*
