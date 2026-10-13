# Citation Audit — *The Architect's Handbook: Engineering Responsible AI* (v1.0, Jan 2026)

**Method (13 Oct 2026).** All 127 references were pulled from the book's bibliography.
- **arXiv IDs (63 refs):** every ID was looked up through the arXiv API, and the returned title and authors were compared with the book's entry.
- **DOIs and journal papers:** checked against Crossref, either by DOI or by bibliographic title search.
- **Corrected entries:** confirmed the same way, against arXiv or Crossref.
- **Not checked:** web pages, standards and policy documents (refs 1–17, 93–104, 117–127), except where a specific problem was obvious.

**Summary**

| Outcome | Count |
|---|---|
| arXiv ID points to a **completely different paper** | 22 |
| Title correct, **author list wrong or invented** | 11 |
| DOI wrong (404, or resolves to a different article) | 5 |
| **Could not be found anywhere** (likely fabricated) | 7 |
| Wrong venue/year (minor) | several |

Every entry marked ✅ below was confirmed against arXiv or Crossref.

---

## A. Machine unlearning references (§5.1) — highest priority

| # | Problem in book | Correct citation |
|---|---|---|
| 18 | arXiv `1409.1595` is an exoplanet paper. Cao & Yang is **not on arXiv**. | Cao, Y. & Yang, J. (2015). Towards Making Systems Forget with Machine Unlearning. *IEEE S&P*, 463–480. DOI 10.1109/SP.2015.35 ✅ |
| 20 | Title, authors and ID are all wrong (`2009.15640` doesn't exist). | Garg, S., Goldwasser, S. & Vasudevan, P. N. (2020). Formalizing Data Deletion in the Context of the Right to be Forgotten. *EUROCRYPT 2020*. arXiv:2002.10635 ✅ |
| 21 | ID `1907.05006` is a video-QA paper. | Ginart, A., Guan, M., Valiant, G. & Zou, J. (2019). Making AI Forget You. *NeurIPS*. arXiv:**1907.05012** ✅ |
| 22 | Third author listed as "Hardt, M." | Graves, L., Nagisetty, V. & **Ganesh, V.** (2021). Amnesiac Machine Learning. *AAAI*. arXiv:2010.10981 ✅ |
| 23 | Attributed to "Bourtoule et al., NeurIPS". ID is a CO₂ paper. | **Ullah, E., Mai, T., Rao, A., Rossi, R. & Arora, R.** (2021). Machine Unlearning via Algorithmic Stability. *COLT*. arXiv:**2102.13179** ✅ |
| 24 | "Chien, Pan & Alistair — Efficient Unlearning via Teacher-Student Distillation, ICLR". ID is a physics paper. **No such paper found** on arXiv or Crossref. | **Remove.** For distillation unlearning, cite SCRUB (27) and Bad-T (25). |
| 25 | Authors "Kacham, P., & Jain, P." are wrong. ID is a BERT paper. | Chundawat, V. S., Tarun, A. K., **Mandal, M. & Kankanhalli, M.** (2023). Can Bad Teaching Induce Forgetting? *AAAI*. arXiv:**2205.08096** ✅ |
| 26 | Authors "Feng, Ahn, Maddison" are wrong. ID is a prompt-tuning paper. | **Jang, J., Yoon, D., Yang, S., Cha, S., Lee, M., Logeswaran, L. & Seo, M.** (2023). Knowledge Unlearning for Mitigating Privacy Risks in Language Models. ***ACL 2023***. arXiv:**2210.01504** ✅ |
| 27 | Authors "Tramer, F., & Dugan, L." are wrong. Venue (ICLR) is wrong. ID is a diffusion paper. | Kurmanji, M., **Triantafillou, P., Hayes, J. & Triantafillou, E.** (2023). Towards Unbounded Machine Unlearning. ***NeurIPS 2023***. arXiv:**2302.09880** ✅ |
| 28 | Nine invented co-authors. ID is correct. | Yao, Y., **Xu, X. & Liu, Y.** (2023). Large Language Model Unlearning. arXiv:2310.10683 ✅ |
| 29 | TinyStories is by **Eldan & Li**, not Eldan & Russinovich, and the title is wrong. It isn't an unlearning paper. | Probably intended: **Eldan, R. & Russinovich, M. (2023). Who's Harry Potter? Approximate Unlearning in LLMs. arXiv:2310.02238** ✅ |

**Text error in §5.1.3:** the book expands SCRUB as "Scalable Remembering and Unlearning **Bound**". The paper itself says "SCalable Remembering and Unlearning **unBound**", which is the point of its title, *Towards Unbounded MU*.

**Unlearning comparison table (§5.1.3):** these methods are named in the table but never cited:
- DaRE: Brophy & Lowd, ICML 2021, arXiv:2009.05567
- HedgeCut: Schelter et al., SIGMOD 2021, DOI 10.1145/3448016.3457239
- DC-k-means: in Ginart et al. 2019
- GraphEraser: Chen et al., CCS 2022, arXiv:2103.14991
- RecEraser: Chen et al., WWW 2022, arXiv:2201.06820
- KNOT: Su & Li, INFOCOM 2023, DOI 10.1109/INFOCOM53939.2023.10229075
- ARCANE: Yan et al., IJCAI 2022, DOI 10.24963/ijcai.2022/556

All were verified ✅. Add them to the bibliography.

---

## B. Other references with wrong arXiv IDs

| # | Book's ID resolves to | Correct |
|---|---|---|
| 38 | a CNN review | Title/authors swapped. The book's title is **Frid-Adar et al. (2018)**, *Neurocomputing*, arXiv:1803.01229 ✅. The listed authors (Bowles et al.) wrote a different paper. |
| 43 | an RL benchmark | SDV isn't on arXiv: Patki, Wedge & Veeramachaneni (2016), DSAA, DOI 10.1109/DSAA.2016.49 ✅ |
| 44 | duplicate of #37 | "Zhang, Yan, Chandrasekaran & Papernot — CTGAN" **does not exist**. CTGAN is #37 (Xu et al.). **Remove.** |
| 47 | a PCA paper | Alaa, A. M., van Breugel, B., **Saveliev, E.** & van der Schaar, M. (2022). ICML. arXiv:**2102.08921** ✅ (book lists "Saab, E. S.") |
| 56 | a crystal-growth paper | **Calmon, F. P., Wei, D., Natesan Ramamurthy, K. & Varshney, K. R.** (arXiv author list; the NeurIPS 2017 version also includes Vinzamuri, B.). Optimized Pre-Processing for Discrimination Prevention. arXiv:**1704.03354** ✅ (book: "Calmon, Pineau & Sontag") |
| 61 | a cosmic-ray paper | **Buolamwini, J. & Gebru, T.** (2018). Gender Shades. *FAT\**, PMLR 81:77–91. Not on arXiv ✅ (book: "Buolamwini, B., & Buolamwini, B.") |
| 66 | a probability paper | Koh et al. (2020). Concept Bottleneck Models. ICML. arXiv:**2007.04612** ✅ |
| 70 | an unrelated paper | "Hendel, Sap, Rashkin & Choi (2022) — Detecting Implicit Hate Speech … Mechanistic Interpretability" was **not found**. Likely fabricated. **Remove.** |
| 72 | *Attention Is All You Need* | Christiano et al. (2017). Deep RL from Human Preferences. **NeurIPS** (not ICML). arXiv:**1706.03741** ✅ |
| 74 | a continual-learning survey | **Ziegler, D. M., Stiennon, N., Wu, J., Brown, T. B., Radford, A., Amodei, D., Christiano, P. & Irving, G.** (2019). arXiv:**1909.08593** ✅ |
| 77 | a galaxy-cluster paper | "Kairouz, Oh & Viswanath — Secure and Private Distributed Deep Learning, AISTATS 2017" was **not found**. Likely fabricated. **Remove.** |
| 105 | a spin-relaxation paper | Selbst et al. (2019). FAT\*. DOI 10.1145/3287560.3287598 ✅. Not on arXiv. |
| 106 | Lipton, *Mythos of Interpretability* | Goodman & Flaxman (2017). arXiv:**1606.08813** ✅ |
| 108 | the Codex paper | Bender et al. (2021). FAccT. DOI 10.1145/3442188.3445922 ✅. Not on arXiv. |
| 112 | a hashing paper | Rauber et al. wrote **Foolbox**, not this. "Fooling Neural Network Interpretations via Adversarial Model Manipulation" is **Heo, Joo & Moon (2019)**, NeurIPS, arXiv:**1902.02041** ✅ |
| 115 | an interpretability survey | Gunning & Aha (2019). AI Magazine 40(2). DOI 10.1609/aimag.v40i2.2850 ✅. Not on arXiv. |

## C. Correct paper, wrong authors

| # | Paper | Book lists | Actual authors (arXiv/Crossref ✅) |
|---|---|---|---|
| 31 | Synthetic Data — what, why and how? | Hoover, Mateen, Leite, Grechuk, Tatalenko, Wilde | Jordon, Szpruch, **Houssiau, Bottarelli, Cherubin, Maple, Cohen, Weller** |
| 45 | Self-Consuming Generative Models Go MAD | Bietti, Guestrin, Morris, Hardt | Alemohammad, **Casco-Rodriguez, Luzi, Humayun, Babaei, LeJeune, Siahkoohi, Baraniuk** |
| 52 | AI Fairness 360 | Hoey, Khandelwal, Nalkur, Rajagopal, Satterfield, Sevrinsky, Weld | Bellamy, Dey, Hind, Hoffman, **Houde, Kannan, Lohia, Martino, Mehta, Mojsilović, Nagar, Natesan Ramamurthy, Richards, Saha, Sattigeri, Singh, Varshney, Zhang** |
| 53 | Aequitas | Hind, Ghai, Varshney | Saleiro, Kuester, **Hinkson, London, Stevens, Anisfeld, Rodolfa, Ghani** |
| 58 | A Reductions Approach to Fair Classification | "Dudíková, M." | **Dudík, M.** |
| 69 | IOI circuit in GPT-2 small | "Tegmark, M." | **Steinhardt, J.** |
| 92 | Closing the AI Accountability Gap | "Larson, J." | **Smith-Loud, J., Theron, D.** (and Barnes, P.) |
| 107 | From What to How | "Machado, C." | Morley, Floridi, Kinsey, **Elhalal, A.** |
| 123 | Unified Framework of Five Principles | "Cowley, J." | Floridi, L. & **Cowls, J.** |
| 32 | Privacy and Synthetic Datasets | Landau, Blakley | Bellovin, **Dutta, P. K. & Reitinger, N.** |
| 59 | "Fairness through Awareness" — Ustun, Liu & Parkes, STOC 2019 | — | **Dwork, Hardt, Pitassi, Reingold & Zemel (2012), ITCS.** DOI 10.1145/2090236.2090255, arXiv:1104.3913 ✅ |

## D. Wrong DOIs or not found

| # | Problem | Correct |
|---|---|---|
| 11 | DOI resolves to a different article. The authors are also wrong. | Floridi, L., **Holweg, M., Taddeo, M., Amaya, J., Mökander, J. & Wen, Y.** (2022). capAI. SSRN. DOI 10.2139/ssrn.4064091 ✅ (a report, not *AI and Ethics* 2(4)) |
| 33 | DOI returns 404. The author list is partly wrong. | Chen, R. J., Lu, M. Y., Chen, T. Y., Williamson, D. F. K. & Mahmood, F. (2021). *Nat. Biomed. Eng.* 5, 493–497. DOI **10.1038/s41551-021-00751-8** ✅ |
| 89 | DOI resolves to a brain-informatics paper. | Li, T., Li, N., Zhang, J. & Molloy, I. (2012). Slicing. *IEEE TKDE* 24(3). DOI **10.1109/TKDE.2010.236** ✅ |
| 114 | DOI returns 404. Title and authors are wrong ("RParts", "Adebawo"…). | **Esteva, A., Robicquet, A., Ramsundar, B., Kuleshov, V., DePristo, M., Chou, K., Cui, C., Corrado, G., Thrun, S. & Dean, J.** (2019). **A guide to deep learning in healthcare.** *Nat. Med.* 25, 24–29. DOI **10.1038/s41591-018-0316-z** ✅ |
| 86 | Venue given as MICRO. | McKeen et al. (2013). **HASP '13** workshop. DOI 10.1145/2487726.2488368 ✅ |
| 14 | "Andersen et al. — European AI Leadership Board Report" | **Not found.** Remove or replace. |
| 34 | "Raghunathan et al. — Representation Integrity, ICML 2023" | **Not found.** Remove. |
| 67 | "Yonekura et al. — CBM with Open Vocabulary Concepts, NeurIPS 2023" | The real paper is **Tan, Zhou & Chen (2024), ECCV**, DOI 10.1007/978-3-031-73016-0_8 ✅ |
| 113 | "Sinha & Sap — Bias in ML: How and When Do We Care?, FAccT 2023" | **Not found.** Remove. |

## E. Standards / web references worth a second look
- **8:** the AI RMF 1.0 is **NIST AI 100-1**, `https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`. The book's URL (AI 600-1) is the 2024 *Generative AI Profile*.
- **9:** the AI RMF Playbook is dated 2019, but the AI RMF was released in Jan 2023.
- **5:** "ISO/IEC 42003:2022 — robustness" is suspect. The robustness standards are ISO/IEC **TR 24029-1:2021 / 24029-2:2023**. Verify.
- **124:** the Future of Humanity Institute closed in April 2024, and "Center for AI Safety Research and Advisory" isn't an FHI body.
- **70:** remove (see B).

## F. Non-citation errors found while reading
1. **§5.3.1.2, Equalized Odds example.** Group A=1 says "approves 45" but computes TPR = 30/50. It says "approves 10" but computes FPR = 5/50.
2. **§5.6.2.** It says superposition is "where single neurons … monosemantically encode concepts". Superposition is the opposite: more features than neurons, so neurons are *polysemantic*. The "pinpointed truthfulness/deception circuits in GPT-4" claim also has no citation.
3. **§5.1.2 (p.36):** raw LaTeX `$D\setminus D_{forget}$` is rendered as text.
4. **§5.1.3 (p.40):** "The incompetent teacher" and "T_bad: …" are split into two bullets.
5. **Preface and acknowledgements:** they call the book "this chapter".
6. **§5.1.3 SISA:** slicing is described, but its purpose isn't. It saves a **checkpoint after each slice**, so unlearning resumes from the last checkpoint before the affected slice (Bourtoule et al. §IV).
7. **§5.1.3 Bad-T / SCRUB:** both papers warn that *unusually high* forget-set error is itself a membership-inference signal. SCRUB adds "SCRUB+R" (rewinding) for this reason, so it's worth a sentence.
