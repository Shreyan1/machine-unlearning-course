"""
Regenerates every concept diagram in assets/diagrams/.

    python assets/make_diagrams.py

All diagrams use the colour language defined in mul/viz.py:
grey = original model, green = retrained gold standard, red = forget set, blue = retain set,
purple = an unlearning method.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mul.viz import (ACCENT, FORGET, INK, METHOD, ORIGINAL, RETAIN, RETRAIN, arrow, box,  # noqa: E402
                     canvas, label)

OUT = Path(__file__).resolve().parent / "diagrams"
OUT.mkdir(exist_ok=True)


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------------------------
def delete_vs_unlearn():
    fig, ax = canvas(12, 5.6)
    label(ax, 3, 5.25, "Traditional software", 13, bold=True)
    label(ax, 9, 5.25, "Machine learning", 13, bold=True)
    ax.plot([6, 6], [0.3, 5.4], color="#cccccc", lw=1)

    # left: database
    box(ax, 3, 4.1, 3.6, 1.1, "users table\nalice | bob | carol | dave", RETAIN, fontsize=10)
    arrow(ax, 3, 3.5, 3, 2.75, "DELETE FROM users\nWHERE name='carol'", FORGET, fontsize=9,
          text_offset=(1.25, -0.25))
    box(ax, 3, 2.2, 3.6, 1.0, "users table\nalice | bob | dave", RETAIN, fontsize=10)
    label(ax, 3, 1.05, "Carol is gone.\nNothing else remembers her.", 10.5, RETRAIN, bold=True)

    # right: model
    box(ax, 7.6, 4.1, 2.2, 1.1, "training data\nalice bob carol dave", RETAIN, fontsize=9.5)
    arrow(ax, 8.75, 4.1, 9.65, 4.1, "train", INK)
    box(ax, 10.6, 4.1, 1.8, 1.1, "model\nweights θ", ORIGINAL, fill_alpha=0.25, fontsize=10, bold=True)
    arrow(ax, 7.6, 3.5, 7.6, 2.75, "DELETE carol", FORGET, fontsize=9, text_offset=(0.8, -0.1))
    box(ax, 7.6, 2.2, 2.2, 1.0, "training data\nalice bob dave", RETAIN, fontsize=9.5)
    box(ax, 10.6, 2.2, 1.8, 1.0, "model\nweights θ\n(unchanged!)", ORIGINAL, fill_alpha=0.25,
        fontsize=9.5)
    arrow(ax, 10.6, 3.5, 10.6, 2.75, None, ORIGINAL, ls="--")
    label(ax, 9.1, 1.05, "Carol's influence is still inside θ.\nDeleting the row does not touch the model.",
          10.5, FORGET, bold=True)
    label(ax, 6, 0.3, "Machine unlearning = removing a data point's influence from a model that has already been trained.",
          10.5, INK, style="italic")
    save(fig, "01_delete_vs_unlearn")


# ---------------------------------------------------------------------------------------------
def notation():
    fig, ax = canvas(12, 4.6)
    label(ax, 6, 4.3, "The notation used in every notebook", 13, bold=True)
    ax.add_patch(plt.Rectangle((0.6, 2.4), 8.4, 1.2, fc=(0.23, 0.44, 0.85, 0.12), ec=RETAIN, lw=1.6))
    ax.add_patch(plt.Rectangle((9.0, 2.4), 1.6, 1.2, fc=(0.84, 0.27, 0.27, 0.18), ec=FORGET, lw=1.6))
    label(ax, 4.8, 3.0, "D_r  -  retain set  (everything we are allowed to keep)", 11, RETAIN, bold=True)
    label(ax, 9.8, 3.0, "D_f\nforget set", 10.5, FORGET, bold=True)
    ax.annotate("", xy=(0.6, 2.15), xytext=(10.6, 2.15), arrowprops=dict(arrowstyle="<->", color=INK))
    label(ax, 5.6, 1.9, "D = D_r ∪ D_f   (the full training set the original model θ_o was trained on)", 10.5)
    box(ax, 11.4, 3.0, 1.0, 1.2, "D_test\nnever\ntrained\non", ACCENT, fontsize=8.5)
    rows = [("θ_o", "original model, trained on D (it has seen D_f)", ORIGINAL),
            ("θ_r", "retrained model, trained on D_r only  -  the GOLD STANDARD", RETRAIN),
            ("θ_u", "unlearned model, produced by an unlearning method from θ_o", METHOD)]
    for i, (sym, txt, c) in enumerate(rows):
        label(ax, 1.2, 1.25 - i * 0.45, sym, 11.5, c, bold=True)
        label(ax, 1.75, 1.25 - i * 0.45, txt, 10.5, INK, ha="left")
    label(ax, 9.8, 0.55, "Goal:   θ_u  ≈  θ_r", 13, METHOD, bold=True)
    save(fig, "02_notation")


# ---------------------------------------------------------------------------------------------
def goal():
    fig, ax = canvas(12, 5.2)
    label(ax, 6, 4.95, "The goal of machine unlearning", 13, bold=True)
    box(ax, 2.0, 3.6, 2.6, 1.1, "Full data D\n= D_r + D_f", RETAIN, fontsize=10.5)
    box(ax, 6.0, 3.6, 2.4, 1.1, "Original model θ_o", ORIGINAL, fill_alpha=0.25, fontsize=10.5, bold=True)
    arrow(ax, 3.3, 3.6, 4.8, 3.6, "train (expensive)", INK)
    box(ax, 2.0, 1.2, 2.6, 1.1, "Retain data D_r\n(D_f removed)", RETAIN, fontsize=10.5)
    arrow(ax, 2.0, 3.0, 2.0, 1.8, "delete D_f", FORGET, text_offset=(0.65, -0.15))
    box(ax, 6.0, 1.2, 2.4, 1.1, "Retrained θ_r\nGOLD STANDARD", RETRAIN, fill_alpha=0.2, fontsize=10.5, bold=True)
    arrow(ax, 3.3, 1.2, 4.8, 1.2, "retrain from scratch\n(exact but expensive)", RETRAIN, text_offset=(0, -0.95))
    box(ax, 10.0, 2.4, 2.5, 1.2, "Unlearned θ_u", METHOD, fill_alpha=0.2, fontsize=11, bold=True)
    arrow(ax, 7.2, 3.6, 8.75, 2.75, "unlearning method\n(cheap)", METHOD, text_offset=(0.2, 0.1))
    ax.annotate("", xy=(8.75, 2.1), xytext=(7.2, 1.25),
                arrowprops=dict(arrowstyle="<->", color=RETRAIN, lw=1.8, ls="--"))
    label(ax, 8.55, 1.3, "≈ indistinguishable?", 10.5, RETRAIN, bold=True)
    label(ax, 6, 0.15, "Exact unlearning guarantees θ_u has the same distribution as θ_r.  "
                       "Approximate unlearning only gets close - and must be audited.", 10, INK, style="italic")
    save(fig, "03_unlearning_goal")


# ---------------------------------------------------------------------------------------------
def taxonomy():
    fig, ax = canvas(12, 6)
    label(ax, 6, 5.7, "A map of unlearning methods (everything in this repo)", 13, bold=True)
    box(ax, 6, 4.8, 3.2, 0.7, "Machine unlearning", INK, fill_alpha=0.06, fontsize=11.5, bold=True)
    box(ax, 3, 3.6, 4.3, 0.75, "EXACT\nprovably equal to retraining", RETRAIN, fill_alpha=0.15, fontsize=10, bold=True)
    box(ax, 9, 3.6, 4.3, 0.75, "APPROXIMATE\nclose to retraining - must be audited", METHOD, fill_alpha=0.15, fontsize=10, bold=True)
    arrow(ax, 5.2, 4.45, 3.6, 4.0, None, INK)
    arrow(ax, 6.8, 4.45, 8.4, 4.0, None, INK)
    exact = [("Retrain from scratch", "NB 03 · Cao & Yang 2015"), ("SISA", "NB 04 · Bourtoule et al. 2021"),
             ("DaRE / HedgeCut (trees)", "Brophy 2021 · Schelter 2021"), ("ARCANE / GraphEraser / RecEraser", "Yan 2022 · Chen 2022")]
    approx = [("Fine-tune / Gradient ascent", "NB 05 · baselines & traps"), ("SCRUB (+R)", "NB 06 · Kurmanji et al. 2023"),
              ("Bad Teacher", "NB 07 · Chundawat et al. 2023"), ("LLM: GA / NPO / refusal", "NB 12 · Jang 2023 · Zhang 2024")]
    for i, (t, s) in enumerate(exact):
        box(ax, 3, 2.75 - i * 0.68, 3.9, 0.55, f"{t}\n{s}", RETRAIN, fill_alpha=0.07, fontsize=8.8)
    for i, (t, s) in enumerate(approx):
        box(ax, 9, 2.75 - i * 0.68, 3.9, 0.55, f"{t}\n{s}", METHOD, fill_alpha=0.07, fontsize=8.8)
    label(ax, 6, 0.1, "Cost  ↓   Guarantee  ↓   as you move from left to right", 10, INK, style="italic")
    save(fig, "04_taxonomy")


# ---------------------------------------------------------------------------------------------
def sisa():
    fig, ax = canvas(13, 6.4)
    label(ax, 6.5, 6.1, "SISA: Sharded · Isolated · Sliced · Aggregated", 13, bold=True)
    box(ax, 1.1, 3.2, 1.6, 2.2, "Training\ndata D", RETAIN, fontsize=10.5, bold=True)
    ys = [5.0, 3.2, 1.4]
    for k, yy in enumerate(ys):
        arrow(ax, 1.9, 3.2, 2.7, yy, None, INK)
        label(ax, 3.2, yy + 0.62, f"shard {k + 1}", 9.5, RETAIN, bold=True)
        for r in range(4):
            hit = (k == 1 and r == 2)
            c = FORGET if hit else RETAIN
            box(ax, 3.0 + r * 1.05, yy, 0.9, 0.7, f"slice {r + 1}" + ("\n✗ carol" if hit else ""), c,
                fill_alpha=0.25 if hit else 0.1, fontsize=8.3)
            if r < 3:
                arrow(ax, 3.45 + r * 1.05, yy, 3.55 + r * 1.05, yy, None, INK, lw=1)
            ckc = ACCENT
            ax.plot(3.0 + r * 1.05 + 0.45, yy - 0.5, marker="v", color=ckc, ms=7)
        arrow(ax, 6.65, yy, 7.6, yy, None, INK)
        box(ax, 8.3, yy, 1.3, 0.75, f"model M{k + 1}", ORIGINAL, fill_alpha=0.25, fontsize=9.5, bold=True)
        arrow(ax, 8.95, yy, 9.9, 3.2, None, INK)
    box(ax, 10.65, 3.2, 1.4, 1.0, "aggregate\n(average\nprobabilities)", INK, fill_alpha=0.05, fontsize=9)
    arrow(ax, 11.35, 3.2, 12.2, 3.2, "predict", INK)
    label(ax, 4.6, 0.55, "▼ = checkpoint saved after each slice", 9.5, ACCENT, bold=True)
    label(ax, 6.5, 0.05, "Carol is in shard 2, slice 3  →  reload shard 2's checkpoint after slice 2, retrain slices 3-4 without her.\n"
                         "Shards 1 and 3 are untouched.  Cost ≈ (1/K) × (fraction of slices redone) of a full retrain - and it is EXACT.",
          9.8, FORGET)
    save(fig, "05_sisa")


# ---------------------------------------------------------------------------------------------
def scrub():
    fig, ax = canvas(13, 6.2)
    label(ax, 6.5, 5.95, "SCRUB: a student that selectively disobeys its teacher", 13, bold=True)
    box(ax, 2.2, 4.6, 3.0, 1.0, "Teacher = θ_o\n(frozen)", ORIGINAL, fill_alpha=0.25, fontsize=10.5, bold=True)
    box(ax, 10.8, 4.6, 3.0, 1.0, "Student θ_u\n(starts as a copy of θ_o)", METHOD, fill_alpha=0.18, fontsize=10.5, bold=True)
    box(ax, 4.6, 2.7, 3.4, 1.1, "MAX-step on D_f\nmaximise KL(teacher ‖ student)\n→ push AWAY", FORGET, fill_alpha=0.15, fontsize=9.5)
    box(ax, 8.4, 2.7, 3.4, 1.1, "MIN-step on D_r\nminimise α·KL + γ·CE\n→ pull CLOSE", RETAIN, fill_alpha=0.15, fontsize=9.5)
    arrow(ax, 2.6, 4.05, 4.0, 3.3, "teacher logits", ORIGINAL, fontsize=8.5, text_offset=(-0.6, 0))
    arrow(ax, 3.4, 4.3, 7.6, 3.3, None, ORIGINAL)
    arrow(ax, 10.2, 4.05, 9.4, 3.3, "student logits", METHOD, fontsize=8.5, text_offset=(0.8, 0))
    arrow(ax, 10.6, 4.05, 5.6, 3.3, None, METHOD, ls="--")
    # timeline
    label(ax, 1.0, 1.25, "epochs:", 10, INK, bold=True, ha="left")
    seq = ["MAX", "MIN", "MAX", "MIN", "MAX", "MIN", "MIN", "MIN"]
    for i, s in enumerate(seq):
        c = FORGET if s == "MAX" else RETAIN
        box(ax, 2.7 + i * 1.15, 1.25, 1.0, 0.55, s, c, fill_alpha=0.22, fontsize=9.5, bold=True)
    label(ax, 6.8, 0.6, "alternate max/min for the first `max_steps` epochs, then extra MIN epochs to repair the retain set",
          9.5, INK, style="italic")
    label(ax, 6.5, 0.1, "SCRUB+R: keep a checkpoint per epoch and REWIND to the one whose D_f error is 'just high enough' "
                        "- over-forgetting is itself a privacy leak.", 9.5, METHOD)
    save(fig, "06_scrub")


# ---------------------------------------------------------------------------------------------
def bad_teacher():
    fig, ax = canvas(13, 5.6)
    label(ax, 6.5, 5.35, "Bad Teacher: two teachers, one student", 13, bold=True)
    box(ax, 2.4, 4.1, 3.7, 1.1, "Competent teacher T_s\n= θ_o (knows everything)", RETRAIN, fill_alpha=0.18, fontsize=10)
    box(ax, 10.6, 4.1, 3.7, 1.1, "Incompetent teacher T_d\n= random weights (knows nothing)", FORGET, fill_alpha=0.15, fontsize=10)
    box(ax, 6.5, 1.9, 3.4, 1.2, "Student S\n(starts as a copy of θ_o)", METHOD, fill_alpha=0.18, fontsize=10.5, bold=True)
    arrow(ax, 2.8, 3.5, 5.2, 2.4, "on D_r (≈30% subset):\ncopy T_s  ·  KL(T_s ‖ S)", RETRAIN, fontsize=9, text_offset=(-1.3, -0.2))
    arrow(ax, 10.2, 3.5, 7.8, 2.4, "on D_f:\ncopy T_d  ·  KL(T_d ‖ S)", FORGET, fontsize=9, text_offset=(1.3, -0.2))
    label(ax, 6.5, 0.75, "L(x, l_u) = (1 − l_u) · KL(T_s(x) ‖ S(x))  +  l_u · KL(T_d(x) ‖ S(x)),     l_u = 1 if x ∈ D_f",
          10.5, INK)
    label(ax, 6.5, 0.2, "Fast (one epoch, a fraction of D_r).  Caveat: it aims for RANDOM outputs on D_f, but a retrained model is not random there.",
          9.5, INK, style="italic")
    save(fig, "07_bad_teacher")


# ---------------------------------------------------------------------------------------------
def forget_spectrum():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.axis("off")
    grad = np.linspace(0, 1, 400)[None, :]
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("spectrum", [ACCENT, "#fff7e0", RETRAIN, "#fde2e2", FORGET])
    ax.imshow(grad, extent=(0, 100, 0.42, 0.62), aspect="auto", cmap=cmap, alpha=0.45)
    ax.axvspan(44, 60, ymin=0.38, ymax=0.66, color=RETRAIN, alpha=0.35)
    ax.text(52, 0.78, "TARGET\nwhat a retrained model scores\n(the gold band)", ha="center", fontsize=10,
            color=RETRAIN, fontweight="bold")
    ax.text(97, 0.78, "UNDER-forgotten\nstill remembers D_f\n(original model: ~100%)", ha="center", fontsize=10,
            color=FORGET, fontweight="bold")
    ax.text(5, 0.78, "OVER-forgotten\nsuspiciously wrong on D_f\n→ reveals who was deleted", ha="center", fontsize=10,
            color=ACCENT, fontweight="bold")
    for x in (0, 25, 50, 75, 100):
        ax.text(x, 0.3, f"{x}%", ha="center", fontsize=9)
    ax.text(50, 0.12, "accuracy of the unlearned model on the forget set D_f", ha="center", fontsize=10.5)
    ax.text(50, -0.05, "Lower is NOT always better: the right answer is 'whatever a model that never saw D_f would score'.",
            ha="center", fontsize=10, style="italic")
    ax.set_title("The forgetting spectrum (the 'Streisand effect')", fontsize=13, fontweight="bold")
    save(fig, "08_forget_spectrum")


# ---------------------------------------------------------------------------------------------
def audit_pipeline():
    fig, ax = canvas(13, 4.6)
    label(ax, 6.5, 4.35, "How to prove a model forgot - the audit used in notebooks 08-12", 13, bold=True)
    steps = [("1. Gold standard", "retrain WITHOUT D_f\nseveral seeds → band", RETRAIN),
             ("2. Utility", "accuracy on D_r\nand on test data", RETAIN),
             ("3. Forgetting", "accuracy on D_f\ninside the gold band?", FORGET),
             ("4. Privacy", "per-example MIA\n(U-LiRA) on D_f", METHOD),
             ("5. Relearn", "does D_f come back\nafter a few steps?", ACCENT),
             ("6. Verdict", "RAI-scorecard gate\nPASS / FAIL + cost", INK)]
    for i, (t, s, c) in enumerate(steps):
        x = 1.15 + i * 2.13
        box(ax, x, 2.6, 1.9, 1.5, f"{t}\n\n{s}", c, fill_alpha=0.12, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x + 0.97, 2.6, x + 1.16, 2.6, None, INK)
    label(ax, 6.5, 1.15, "Every number is compared with the SAME number for retrained models - never with zero.", 10.5,
          INK, bold=True)
    label(ax, 6.5, 0.6, "The reference models must use the same recipe (architecture, epochs, ensembling) as the model under audit.",
          10, INK, style="italic")
    save(fig, "09_audit_pipeline")


# ---------------------------------------------------------------------------------------------
def llm_suppression():
    fig, ax = canvas(13, 5.8)
    label(ax, 6.5, 5.55, "LLM unlearning: suppression vs removal", 13, bold=True)
    for cx, title, col, inner, out, verdict in [
        (3.3, "SUPPRESSION (refusal / output filter)", FORGET, "weights still encode:\n'Carol's phone = 555-0142'",
         "“I can't share that.”", "relearn attack: a few steps of fine-tuning\n→ the number comes straight back"),
        (9.7, "REMOVAL (retrain-equivalent)", RETRAIN, "weights encode:\n'a phone number looks like 555-....'",
         "“555-0193” (a guess)", "relearn attack: as slow as learning\nit for the first time")]:
        label(ax, cx, 4.95, title, 11, col, bold=True)
        box(ax, cx, 3.8, 4.4, 1.2, inner, ORIGINAL, fill_alpha=0.15, fontsize=10)
        label(ax, cx - 2.6, 3.8, "θ", 14, INK, bold=True)
        arrow(ax, cx, 3.15, cx, 2.55, "prompt: “Carol's phone is”", INK, fontsize=9, text_offset=(1.25, -0.15))
        box(ax, cx, 2.15, 4.0, 0.7, out, col, fill_alpha=0.15, fontsize=10.5)
        label(ax, cx, 1.15, verdict, 9.8, col)
    label(ax, 6.5, 0.25, "Most published LLM unlearning lands closer to the left than the right (Lynch 2024, Deeb & Roger 2024, Łucki 2024).",
          10, INK, style="italic")
    save(fig, "10_llm_suppression_vs_removal")


# ---------------------------------------------------------------------------------------------
def lifecycle():
    fig, ax = canvas(13, 5.0)
    label(ax, 6.5, 4.75, "An unlearning request, end to end (the engineering playbook, Problem 17)", 13, bold=True)
    steps = [("Request", "user / regulator /\nincident"), ("Locate", "data lineage:\nwhich rows, which\nmodels, which shards"),
             ("Delete data", "DB + feature store\n+ caches + backups"), ("Unlearn", "exact if you can,\napproximate if you must"),
             ("Audit", "gold band, MIA,\nrelearn, utility"), ("Certify & log", "evidence for the\nregulator / DPO")]
    cols = [INK, RETAIN, FORGET, METHOD, ACCENT, RETRAIN]
    for i, ((t, s), c) in enumerate(zip(steps, cols)):
        x = 1.15 + i * 2.13
        box(ax, x, 2.9, 1.9, 1.6, f"{t}\n\n{s}", c, fill_alpha=0.12, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x + 0.97, 2.9, x + 1.16, 2.9, None, INK)
    arrow(ax, 9.67, 2.05, 7.53, 2.05, "FAIL → escalate / retrain", FORGET, rad=-0.35, fontsize=9, text_offset=(0, -0.75))
    label(ax, 6.5, 0.45, "Design for deletion at TRAINING time (shards, lineage, checkpoints) - retrofitting it later is far more expensive.",
          10, INK, bold=True)
    save(fig, "11_request_lifecycle")


# ---------------------------------------------------------------------------------------------
def ladder():
    """The spine of the course: each rung removes one property that made forgetting easy."""
    fig, ax = canvas(13, 12.4)
    label(ax, 6.5, 12.15, "The Ladder of Forgetting - how the course is built", 13.5, bold=True)
    rungs = [
        ("01", "k-NN · Naive Bayes", "model = the data / a sum", "delete · subtract", "EXACT, free", RETRAIN),
        ("02", "Ridge → Logistic regression", "coupled sums → implicit optimum", "rank-1 downdate → Newton step", "exact → APPROX.", RETRAIN),
        ("03", "SVM · Random forest", "no gradient, but LOCAL influence", "drop non-SVs · retrain touched trees", "EXACT, partial cost", RETRAIN),
        ("04-05", "Neural network", "every point touches every weight", "(01-03 tricks fail) · detect with MIA", "the problem", FORGET),
        ("06-07", "Retrain · SISA", "no single 'identical' answer", "gold BAND · shard like a forest", "EXACT, planned", RETRAIN),
        ("08-10", "FT · GA · SCRUB · Bad-T", "already trained, monolithic", "Newton w/o Hessian → anchored → teacher", "APPROXIMATE", METHOD),
        ("11", "The audit", "many methods, no guarantees", "gold band · U-LiRA · relearn · gate", "PROOF", ACCENT),
        ("12-14", "Census · faces · spam", "fairness, consent, poison", "classical first, then deep", "RESPONSIBLE AI", INK),
        ("15", "Fine-tuning · LoRA adapters", "base model + per-tenant data", "delete adapter · re-fine-tune from checkpoint", "EXACT by design", RETRAIN),
        ("16", "Language models", "facts as habits; refusal ≠ forgetting", "n-gram subtract · NPO · attack battery", "OPEN PROBLEM", FORGET),
        ("17", "The playbook", "requests, deadlines, owners", "lineage · decide · certify · re-verify", "ENGINEERING", ACCENT),
        ("18", "Recommenders", "your data is the links between items", "subtract co-watch counts · noisy pages", "EXTENSION", RETAIN),
        ("19", "The method zoo", "14 methods, one fixed exam", "leaderboard · fair privacy references", "EXTENSION", METHOD),
    ]
    for i, (nb, model, why, how, guar, c) in enumerate(rungs):
        y = 0.75 + i * 0.88
        x0 = 0.6 + i * 0.2
        box(ax, x0 + 0.55, y, 0.95, 0.66, nb, c, fill_alpha=0.25, fontsize=10, bold=True)
        box(ax, x0 + 2.45, y, 2.7, 0.66, model, c, fill_alpha=0.10, fontsize=9.3, bold=True)
        label(ax, x0 + 3.95, y + 0.14, why, 8.8, INK, ha="left")
        label(ax, x0 + 3.95, y - 0.17, "→ " + how, 8.8, c, ha="left")
        label(ax, 12.85, y, guar, 9, c, bold=True, ha="right")
    ax.annotate("", xy=(0.25, 11.7), xytext=(0.25, 0.4), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2))
    label(ax, 0.05, 6.0, "harder to forget", 9.5, INK, style="italic")
    ax.texts[-1].set_rotation(90)
    save(fig, "00_ladder_of_forgetting")


if __name__ == "__main__":
    ladder(); delete_vs_unlearn(); notation(); goal(); taxonomy(); sisa(); scrub(); bad_teacher()
    forget_spectrum(); audit_pipeline(); llm_suppression(); lifecycle()
