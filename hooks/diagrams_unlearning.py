# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""Diagrams for the Unlearning pages.

Colour key used throughout: blue = data or the original setup, yellow = the data to forget (Carol) or
the thing being changed, green = good or passed, red = bad or failed. Every diagram has a figure title,
a caption, labelled axes where it is a chart, and a legend.
"""
import math

from diagram_kit import Svg

DIAGRAMS = {}


def diagram(fn):
    DIAGRAMS[fn.__name__.replace("_", "-")] = fn
    return fn


@diagram
def what_is_machine_unlearning(name):
    s = Svg(640, 262)
    s.box(20, 20, 160, 62, ["Training data D"], "d-blue", "includes Carol's rows D_f")
    s.arrow(182, 51, 238, 51, label="train", lx=210, ly=42)
    s.box(240, 20, 160, 62, ["Original model", "θ_o"], "d-yellow", "has learnt from Carol")
    s.arrow(320, 84, 320, 126)
    s.text(332, 110, "“forget D_f”", "d-s t-bad", "start")
    s.box(240, 128, 160, 62, ["Unlearning", "method U"], "", "edits the weights")
    s.arrow(402, 159, 458, 159)
    s.box(460, 128, 160, 62, ["Unlearnt model", "θ_u"], "d-good", "acts as if it never met her")
    s.box(20, 128, 160, 62, ["Retain data D_r"], "d-blue", "D without Carol")
    s.arrow(100, 192, 100, 212)
    s.box(20, 214, 160, 34, ["retrain from scratch → θ_r"], "d-soft")
    s.line(540, 192, 540, 214, "dash")
    s.box(460, 214, 160, 34, ["θ_r, the gold standard"], "d-ghost")
    s.text(440, 235, "θ_u should match θ_r", "d-s", "end")
    s.legend([("box", "d-blue", "data"), ("box", "d-yellow", "model that knows Carol"), ("box", "d-good", "model that has forgotten"), ("dash", "", "the one we compare with")])
    return s.render(name, "The goal of machine unlearning",
                    "Unlearning edits the original model so that it behaves like θ_r, a model retrained from scratch without Carol's data. Retraining is the standard to match, not the method.")


@diagram
def deleting_vs_unlearning(name):
    s = Svg(640, 250)
    for i, (title, trace, verdict, vc) in enumerate([
            ("Delete the row only", True, ["Still remembers", "Carol"], "d-bad"),
            ("Delete the row, then unlearn", False, ["Acts as if it", "never met her"], "d-good")]):
        y = 30 + i * 108
        s.text(20, y - 8, title, "d-t d-b", "start")
        s.box(20, y, 150, 74, "", "d-soft")
        for r, (t, c) in enumerate([("Alice", ""), ("Carol", "bad"), ("Dev", "")]):
            s.text(34, y + 20 + r * 20, t, "d-s t-bad" if c else "d-s", "start")
        s.line(30, y + 36, 100, y + 36, "bad thin")
        s.text(160, y + 56, "deleted", "d-s t-bad", "end")
        s.arrow(172, y + 37, 238, y + 37, "thin dash", label="trained earlier", lx=205, ly=y + 28)
        s.box(240, y - 4, 190, 82, "", "d-blue"); s.text(335, y + 14, "Model weights", "d-t d-b")
        if trace:
            s.box(262, y + 36, 146, 28, "Carol's influence", "d-yellow")
        else:
            s.box(262, y + 36, 146, 28, "no trace of Carol", "d-ghost")
        s.arrow(432, y + 37, 478, y + 37)
        s.box(480, y + 5, 140, 64, verdict, vc)
    s.legend([("box", "d-soft", "the database"), ("box", "d-yellow", "Carol's influence in the model"), ("box", "d-good", "forgotten"), ("box", "d-bad", "still remembered")])
    return s.render(name, "Deleting a row versus unlearning",
                    "Deleting Carol's row from the database leaves the model's weights untouched, so her influence stays. Only changing the model removes it.")


@diagram
def why_the_law_cares(name):
    s = Svg(640, 214)
    s.text(320, 18, "GDPR Art. 17 · India DPDP Act s.12 · California CCPA §1798.105", "d-s")
    labels = [(["Person asks", "to be", "forgotten"], "d-blue"), (["Company", "deletes the", "records"], ""),
              (["But the model", "already learnt", "from them"], "d-bad"), (["Unlearn or", "retrain the", "model"], "d-yellow"),
              (["Prove it", "with an", "audit"], "d-good")]
    s.flow([l for l, _ in labels], 14, 30, 108, 74, 18, [c for _, c in labels])
    s.text(320, 134, "Regulators have already ordered whole models deleted", "d-s")
    for i, t in enumerate(["Everalbum 2021", "Kurbo 2022", "Ring 2023", "Rite Aid 2023"]):
        s.box(40 + i * 148, 146, 132, 30, t, "d-ghost")
    s.legend([("box", "d-blue", "the request"), ("box", "d-bad", "the problem"), ("box", "d-yellow", "the fix"), ("box", "d-good", "the evidence")])
    return s.render(name, "From an erasure request to proof",
                    "Deleting records is easy. The hard part is the model that already learnt from them, which is why regulators have ordered models deleted as well as data.")


@diagram
def notation(name):
    s = Svg(640, 250)
    s.text(210, 16, "D = D_r ∪ D_f", "d-t d-b")
    s.box(20, 24, 280, 90, ["Retain set D_r"], "d-blue", "everyone else (1,217 digits)")
    s.box(300, 24, 100, 90, ["Forget set", "D_f"], "d-yellow", "Carol (40)")
    s.box(440, 24, 180, 90, ["Test set D_{test}"], "d-ghost", "never trained on (540)")
    s.box(20, 170, 130, 56, ["θ_o"], "d-blue", "original, trained on D")
    s.arrow(60, 116, 60, 168)
    s.box(210, 170, 130, 56, ["θ_u"], "d-good", "unlearnt, U(θ_o, D, D_f)")
    s.arrow(152, 198, 208, 198, label="U", lx=180, ly=190)
    s.box(440, 170, 180, 56, ["θ_r"], "d-yellow", "retrained on D_r only")
    s.path("M300,116 L300,148 L530,148 L530,168", "", True)
    s.text(414, 142, "train on D_r only", "d-s", "end")
    s.line(342, 198, 438, 198, "dash")
    s.text(390, 188, "close?", "d-s")
    s.legend([("box", "d-blue", "data we keep / original model"), ("box", "d-yellow", "data to forget / gold standard"), ("box", "d-good", "unlearnt model"), ("box", "d-ghost", "held-out test data")])
    return s.render(name, "The notation for data sets and models",
                    "D is everything the model trained on. It splits into D_r (kept) and D_f (to forget). The three models that matter are the original θ_o, the unlearnt θ_u and the retrained gold standard θ_r.")


@diagram
def ladder_of_forgetting(name):
    s = Svg(640, 262)
    rungs = [("k-NN,", "Naive Bayes", ["subtract the", "data exactly"], "d-good", 112), ("Linear,", "logistic", ["closed-form", "update"], "d-good", 122),
             ("SVM,", "forests", ["rebuild the", "affected part"], "d-yellow", 142), ("Neural", "networks", ["approximate,", "then audit"], "d-yellow", 162),
             ("Language", "models", ["facts, not rows", "(unsolved)"], "d-bad", 182)]
    for i, (a, b, c, cls, h) in enumerate(rungs):
        x = 20 + i * 122
        # Name and note sit in the middle of each rung, so taller rungs are not empty at the bottom.
        s.box(x, 230 - h, 116, h, [a, b], cls, c)
        s.text(x + 58, 248, f"rung {i + 1}", "d-s")
    s.path("M30,30 L600,30", "dash thin", True)
    s.text(30, 20, "easy to forget exactly", "d-s", "start"); s.text(600, 20, "hard to forget at all", "d-s", "end")
    s.legend([("box", "d-good", "exact and cheap"), ("box", "d-yellow", "possible, with care"), ("box", "d-bad", "an open problem")])
    return s.render(name, "The Ladder of Forgetting",
                    "Each rung is a family of models. The higher the rung, the harder it is to remove one person's influence exactly.")


@diagram
def retraining_gold_standard(name):
    s = Svg(640, 214)
    s.flow([["Training", "data D"], ["Remove", "D_f"], ["Train from", "scratch on D_r"], ["Retrained", "model θ_r"]], 20, 20, 128, 64, 36,
           ["d-blue", "d-yellow", "", "d-good"])
    s.box(20, 112, 280, 62, ["Exactly what “never saw it” means"], "d-good", "the standard every method is judged by")
    s.box(340, 112, 280, 62, ["A full training run for every request"], "d-bad", "too slow and costly to repeat each time")
    s.legend([("box", "d-blue", "data"), ("box", "d-yellow", "the data to forget"), ("box", "d-good", "a strength"), ("box", "d-bad", "a weakness")])
    return s.render(name, "Retraining from scratch without the forget set",
                    "Remove the forget set and train a brand-new model on what is left. The result is exactly right, but it costs a full training run for each request.")


@diagram
def gold_band(name):
    s = Svg(640, 250)
    X = lambda v: 40 + v * 5.6
    s.axes(X(0), 156, X(100) + 14, 150, "accuracy on Carol's digits (%)", "")
    s.raw('<text class="d-s" x="40" y="48" text-anchor="start">each dot is one model</text>')
    for v in (0, 25, 50, 75, 100):
        s.line(X(v), 152, X(v), 160); s.text(X(v), 174, f"{v}", "d-s")
    s.box(X(47.5), 62, X(70) - X(47.5), 90, "", "d-blue")
    s.text((X(47.5) + X(70)) / 2, 56, "gold band", "d-t d-b t-blue")
    for v in (48, 53, 57, 61, 65, 69):
        s.circle(X(v), 120, 5, "blue")
    s.circle(X(100), 120, 7, "yellow"); s.text(X(100), 98, "original model θ_o", "d-s", "end"); 
    s.text(X(100), 142, "100%, memorised", "d-s t-bad", "end")
    s.circle(X(15), 120, 7, "bad"); s.text(X(15), 104, "θ_u too low", "d-s t-bad")
    s.circle(X(59), 100, 6.5, "good"); s.text(X(59), 88, "θ_u inside", "d-s t-good")
    s.legend([("dot", "blue", "a model retrained without Carol"), ("box", "d-blue", "the gold band they span"), ("dot", "yellow", "original θ_o"),
              ("dot", "good", "unlearnt θ_u, good"), ("dot", "bad", "unlearnt θ_u, over-forgot")])
    return s.render(name, "The gold band",
                    "Retrain the model many times without Carol and her accuracy lands in a band. A good unlearnt model sits inside it; far above means it remembers her, far below means it over-forgot.")


@diagram
def exact_unlearning_classical(name):
    s = Svg(640, 234)
    s.text(160, 18, "Naive Bayes subtracts the counts", "d-t d-b")
    s.box(20, 32, 130, 58, ["“free” in spam", "120"], "d-blue")
    s.text(165, 66, "−", "d-t d-big"); s.box(180, 32, 130, 58, ["Carol's emails", "3"], "d-yellow")
    s.arrow(165, 94, 165, 122)
    s.box(55, 124, 220, 54, ["new count is 117"], "d-good", "identical to retraining")
    s.text(480, 18, "k-NN deletes the stored points", "d-t d-b")
    for i in range(6):
        x = 350 + i * 52
        if i == 3:
            s.circle(x, 62, 8, "open"); s.line(x - 6, 56, x + 6, 68, "bad"); s.line(x - 6, 68, x + 6, 56, "bad")
        else:
            s.circle(x, 62, 8, "blue")
    s.text(350 + 3 * 52, 92, "Carol's point", "d-s t-bad")
    s.arrow(480, 102, 480, 122)
    s.box(370, 124, 220, 54, ["delete her rows"], "d-good", "identical to retraining")
    s.text(320, 206, "Linear and logistic models (a Newton step) and PCA (subtract the sums) are exact too", "d-s")
    s.legend([("box", "d-blue", "what the model stores"), ("box", "d-yellow", "Carol's share of it"), ("box", "d-good", "result, same as retraining")])
    return s.render(name, "Forgetting exactly in classical models",
                    "Models built from sums or stored examples can forget by subtracting Carol's share or deleting her rows. The result is identical to retraining.")


@diagram
def sisa(name):
    s = Svg(640, 250)
    for i in range(4):
        x = 20 + i * 152
        hit = i == 1
        s.box(x, 30, 134, 44, f"Shard {i + 1}", "d-yellow" if hit else "d-blue")
        s.arrow(x + 67, 76, x + 67, 108)
        s.box(x, 110, 134, 44, f"Model {i + 1}", "d-bad" if hit else "d-good", "retrain only this one" if hit else None)
        s.arrow(x + 67, 156, 320, 190, "thin")
    s.circle(20 + 152 + 118, 52, 6, "yellow")
    s.text(206, 22, "holds Carol's rows", "d-s t-bad", "start")
    s.box(220, 192, 200, 40, "Combine the votes", "d-yellow")
    s.text(560, 215, "the other three are untouched", "d-s")
    # Moving layer, one 9-second loop. Carol asks to be forgotten and her rows leave shard 2, only
    # model 2 retrains while the others wait, then the four votes combine again.
    loop = 'dur="9s" repeatCount="indefinite"'

    def fade(times, values):
        return f'<animate attributeName="opacity" values="{values}" keyTimes="{times}" {loop}/>'
    step = [("Carol asks to be forgotten", "t-bad", "0;.08;.12;.3;.34;1", "0;0;1;1;0;0"),
            ("Only shard 2 retrains", "", "0;.34;.38;.66;.7;1", "0;0;1;1;0;0"),
            ("The votes combine again", "t-good", "0;.7;.74;.95;.99;1", "0;0;1;1;0;0")]
    marks = "".join(f'<text class="d-s d-b {c}" x="20" y="215" opacity="0">{n}. {t}{fade(k, v)}</text>'
                    for n, (t, c, k, v) in enumerate(step, 1))
    s.anim(
        marks +
        # A ring pulses round Carol's rows, then they fade out of the shard.
        f'<circle class="d-dot open d-ring" cx="290" cy="52" r="6" opacity="0">'
        f'<animate attributeName="r" values="6;6;18;18" keyTimes="0;.1;.24;1" {loop}/>{fade("0;.1;.24;1", "0;.9;0;0")}</circle>'
        f'<circle class="d-dot d-wipe" cx="290" cy="52" r="7.5" opacity="0">{fade("0;.22;.28;.97;1", "0;0;1;1;0")}</circle>'
        # The request travels down to model 2.
        f'<line class="d-line bad thick" x1="239" y1="76" x2="239" y2="108" opacity="0">{fade("0;.3;.34;.4;.44;1", "0;0;1;1;0;0")}</line>'
        # Model 2 retrains: its bar fills while the other three models stay as they are.
        f'<rect class="d-fill-bad" x="176" y="148" width="0" height="3" rx="1.5">'
        f'<animate attributeName="width" values="0;0;126;126;0" keyTimes="0;.38;.66;.97;1" {loop}/></rect>'
        # The four votes flow into the combiner again.
        + "".join(f'<line class="d-line good thick" x1="{20 + i * 152 + 67}" y1="156" x2="320" y2="190" opacity="0">'
                  f'{fade("0;.7;.74;.9;.95;1", "0;0;1;1;0;0")}</line>' for i in range(4)) +
        f'<rect class="d-box d-pulse" x="220" y="192" width="200" height="40" rx="3" opacity="0">{fade("0;.74;.78;.92;.97;1", "0;0;1;1;0;0")}</rect>')
    s.legend([("box", "d-blue", "a shard of the data"), ("box", "d-yellow", "shard holding Carol"), ("box", "d-good", "model, kept as it is"), ("box", "d-bad", "model to retrain")])
    return s.render(name, "SISA, with one model per shard",
                    "The data is split into shards and each shard trains its own model. To forget Carol, only the shard that held her rows is retrained, then the votes are combined again.")


@diagram
def approximate_unlearning(name):
    s = Svg(640, 250)
    s.box(20, 86, 100, 54, ["Original", "θ_o"], "d-yellow")
    for i, (t, sub) in enumerate([("Gradient ascent", "may over-forget"), ("Fine-tune on D_r", "may only hide it"), ("Add noise", "may hurt everyone")]):
        y = 26 + i * 62
        s.box(170, y, 170, 50, t, "", sub)
        s.arrow(122, 113, 168, y + 25, "thin"); s.arrow(342, y + 25, 388, 113, "thin")
    s.box(390, 86, 90, 54, ["Edited", "θ_u"], "")
    s.arrow(482, 113, 520, 113)
    s.box(522, 86, 100, 54, ["Audit"], "d-blue", "required")
    s.arrow(572, 142, 572, 168)
    s.box(430, 170, 192, 56, ["Inside the gold band?"], "d-good", "only then call it forgotten")
    s.legend([("box", "d-yellow", "the original model"), ("box", "", "a quick fix"), ("box", "d-blue", "the check"), ("box", "d-good", "the verdict")])
    return s.render(name, "Quick fixes must be audited",
                    "Three cheap ways to edit a model, each with a known risk. None comes with a guarantee, so the edited model is audited against the gold band.")


@diagram
def scrub(name):
    s = Svg(640, 236)
    s.box(20, 24, 180, 56, ["Teacher", "frozen copy of θ_o"], "d-yellow")
    s.box(20, 144, 180, 56, ["Student", "the model being edited"], "d-blue")
    s.arrow(110, 82, 110, 142, label="starts as a copy", lx=110, ly=116)
    s.box(290, 24, 330, 56, ["On the retain data D_r,", "match the teacher"], "d-good")
    s.box(290, 144, 330, 56, ["On the forget data D_f,", "move away from the teacher"], "d-bad")
    s.arrow(202, 172, 288, 172, "bad"); s.arrow(202, 52, 288, 52, "good")
    s.text(455, 112, "alternate the two steps, then stop early", "d-s")
    s.legend([("box", "d-yellow", "the teacher (fixed)"), ("box", "d-blue", "the student (changing)"), ("box", "d-good", "pull closer"), ("box", "d-bad", "push apart")])
    return s.render(name, "SCRUB stays close, then moves away",
                    "A frozen teacher guides a student copy. The student is pulled towards the teacher on data to keep and pushed away from it on data to forget, taking turns.")


@diagram
def bad_teacher(name):
    s = Svg(640, 220)
    s.box(20, 24, 150, 52, ["Competent teacher", "the original model"], "d-good")
    s.arrow(172, 50, 218, 50)
    s.box(220, 24, 200, 52, ["On D_r,", "copy the good answers"], "d-blue")
    s.box(20, 134, 150, 52, ["Bad teacher", "random, knows nothing"], "d-bad")
    s.arrow(172, 160, 218, 160)
    s.box(220, 134, 200, 52, ["On D_f,", "copy the clueless answers"], "d-yellow")
    s.arrow(422, 50, 478, 90); s.arrow(422, 160, 478, 120)
    s.box(480, 74, 140, 64, ["Student θ_u"], "d-good", ["keeps what is useful,", "forgets Carol"])
    s.legend([("box", "d-good", "a good model"), ("box", "d-bad", "a clueless model"), ("box", "d-blue", "data to keep"), ("box", "d-yellow", "data to forget")])
    return s.render(name, "Bad Teacher learns from two teachers",
                    "The student learns from a competent teacher on data it should keep and from a clueless one on data it should forget, so Carol's rows teach it nothing.")


@diagram
def method_zoo(name):
    s = Svg(640, 270)
    s.axes(60, 226, 614, 16, "cost (% of one full retrain)", "audit result")
    s.box(70, 20, 540, 98, "", "d-good"); s.text(600, 38, "passed the audit", "d-s t-good", "end")
    s.box(70, 124, 540, 98, "", "d-bad"); s.text(600, 142, "failed on Carol", "d-s t-bad", "end")
    X = lambda v: 80 + v * 5.2
    for v in (0, 25, 50, 75, 100):
        s.text(X(v), 242, f"{v}%", "d-s")
    s.circle(X(100), 76, 7, "good"); s.text(X(100) - 6, 98, "Retrain", "d-s", "end")
    s.circle(X(61.4), 76, 7, "good"); s.text(X(61.4), 98, "SISA", "d-s")
    s.circle(X(13.6), 180, 7, "bad"); s.text(X(13.6), 202, "SCRUB", "d-s")
    for v in (0.3, 2, 5, 8, 11, 15):
        s.circle(X(v), 158, 5, "bad")
    s.text(X(0.3) - 4, 142, "ten other methods", "d-s", "start")
    s.legend([("dot", "good", "passed"), ("dot", "bad", "failed")])
    return s.render(name, "Cost against audit result for each method",
                    "Only retraining and SISA passed the audit on Carol. Every cheaper method failed, so a lower cost bought a weaker result.")


@diagram
def membership_inference_attacks(name):
    s = Svg(640, 250)
    s.axes(40, 200, 612, 30, "the model's confidence in the right answer", "number of examples")
    def hump(mean, sd, cls):
        pts = [(48 + i * 8, 200 - 130 * math.exp(-((48 + i * 8 - mean) ** 2) / (2 * sd * sd))) for i in range(70)]
        s.raw(f'<path class="{cls}" d="M48,200 ' + " ".join(f"L{x},{y:.1f}" for x, y in pts) + ' L600,200 Z"/>')
    hump(250, 62, "d-area-yellow"); hump(430, 62, "d-area-blue")
    s.line(345, 56, 345, 200, "bad dash")
    s.text(345, 46, "attacker's threshold", "d-s t-bad")
    s.text(235, 70, "never trained on", "d-s"); s.text(455, 70, "was trained on", "d-s t-blue")
    s.arrow(352, 150, 442, 150, "bad thin"); s.text(397, 142, "guess “member”", "d-s t-bad")
    s.legend([("box", "d-yellow", "examples the model never saw"), ("box", "d-blue", "examples it trained on"), ("dash", "bad", "the attacker's cut-off")])
    return s.render(name, "How a membership inference attack works",
                    "Models are usually more confident on examples they trained on. An attacker picks a confidence cut-off and guesses “member” above it, so the more the two humps overlap, the less this works.")


@diagram
def unlearning_audit(name):
    s = Svg(640, 260)
    for i, (t, sub, c) in enumerate([("Original θ_o", "before", "d-yellow"), ("Unlearnt θ_u", "being judged", "d-blue"), ("Retrained θ_r × n", "the gold band", "d-good")]):
        s.box(20, 24 + i * 74, 150, 58, t, c, sub)
    s.arrow(172, 124, 232, 124)
    for i, t in enumerate(["Accuracy on D_f vs the band", "Membership inference", "Relearn attack", "Accuracy on D_{test}"]):
        s.box(234, 18 + i * 56, 200, 46, t, "")
    s.arrow(436, 124, 496, 124)
    s.box(498, 64, 122, 56, ["Inside the band", "on every test"], "d-good")
    s.box(498, 130, 122, 56, ["One test fails"], "d-bad")
    s.text(559, 212, "report the evidence either way", "d-s")
    s.legend([("box", "d-yellow", "before unlearning"), ("box", "d-blue", "model being judged"), ("box", "d-good", "reference models / pass"), ("box", "d-bad", "fail")])
    return s.render(name, "The audit pipeline",
                    "The unlearnt model is compared with the original and with many retrained models. It must land inside the gold band on every independent test.")


@diagram
def testing_vs_proving(name):
    s = Svg(640, 250)
    s.text(150, 18, "A test gives evidence", "d-t d-b")
    s.box(20, 28, 260, 140, "", "d-soft")
    s.raw('<ellipse class="d-line bad dash" cx="215" cy="98" rx="48" ry="36" fill="none"/>')
    s.text(215, 102, "untried attack", "d-s t-bad")
    for x, y in [(55, 58), (110, 78), (70, 128), (140, 148), (160, 58), (110, 108)]:
        s.circle(x, y, 5, "blue")
    s.text(150, 188, "6 probes passed, but a stronger", "d-s"); s.text(150, 204, "attack might still find her", "d-s")
    s.text(490, 18, "A guarantee covers everything", "d-t d-b")
    s.box(360, 28, 260, 140, "", "d-blue")
    s.text(490, 94, "With an exact method, the result is", "d-t"); s.text(490, 112, "identical to retraining", "d-t")
    s.text(490, 188, "holds against every attack,", "d-s"); s.text(490, 204, "because of how it was made", "d-s")
    s.legend([("dot", "blue", "a test that passed"), ("dash", "bad", "an attack nobody tried"), ("box", "d-blue", "everything is covered by design")])
    return s.render(name, "A test is evidence, a guarantee is proof",
                    "On the left, passing a handful of tests leaves untried attacks. On the right, an exact method matches retraining by construction, so no attack can tell the difference.")


@diagram
def fairness_and_erasure(name):
    s = Svg(640, 258)
    s.axes(44, 190, 410, 24, "who was deleted before retraining", "true-positive rate for women (%)", xdy=60)
    for i, (v, label, sub, cls) in enumerate([(50.6, "Before", "no deletions", "d-blue"), (51.2, "583 random", "people deleted", "d-blue"),
                                              (22.8, "583 high-earning", "women deleted", "d-bad")]):
        x = 70 + i * 112
        h = v * 2.8
        s.box(x, 190 - h, 82, h, "", cls)
        s.text(x + 41, 190 - h - 8, f"{v}%", "d-t d-b")
        s.text(x + 41, 206, label, "d-s"); s.text(x + 41, 220, sub, "d-s")
    s.box(450, 40, 170, 100, ["Exact retraining", "still copies the bias", "of who asked"], "d-yellow")
    s.text(535, 164, "overall accuracy barely moved", "d-s"); s.text(535, 180, "85.7% → 85.0%", "d-s")
    s.legend([("bar", "d-blue", "women's rate stays steady"), ("bar", "d-bad", "women's rate collapses")])
    return s.render(name, "Deletions can shift a group's results",
                    "When many high-earning women ask to be erased, even a perfect retrain makes the model miss far more of them. The gap comes from who asked, not from the method.")


@diagram
def consent_and_face_recognition(name):
    s = Svg(640, 258)
    s.box(20, 14, 140, 60, ["Dana withdraws", "consent"], "d-yellow")
    steps = [("1 · Delete", "templates and photos"), ("2 · Unlearn", "her from the model"), ("3 · Block", "re-enrolling her")]
    for i, (a, b) in enumerate(steps):
        x = 200 + i * 148
        s.box(x, 14, 136, 60, a, "d-blue", b)
        s.arrow(x - 38 if i == 0 else x - 12, 44, x - 2, 44)
    s.box(20, 110, 290, 96, ["Memory"], "d-good", ["the influence of her photos on", "the weights, which unlearning removes"])
    s.box(330, 110, 290, 96, ["Capability"], "d-ghost", ["matching any enrolled face, which even", "models that never saw her can do"])
    s.text(320, 232, "Only deleting templates and refusing re-enrolment protects Dana", "d-s")
    s.legend([("box", "d-yellow", "the request"), ("box", "d-blue", "a step to take"), ("box", "d-good", "what unlearning removes"), ("box", "d-ghost", "what it cannot remove")])
    return s.render(name, "Withdrawn consent in a face recognition system",
                    "Three steps are needed. Unlearning removes the memory of her photos, but the model's ability to recognise any face stays, so her templates must be deleted too.")


@diagram
def poisoning_and_backdoors(name):
    s = Svg(640, 232)
    s.box(20, 14, 270, 108, "", "d-soft"); s.text(155, 32, "Training data", "d-t d-b")
    for i, d in enumerate(["3", "8", "1", "6", "4"]):
        x = 34 + i * 50
        s.box(x, 46, 40, 40, d, "")
        if i == 4:
            s.box(x + 28, 46, 12, 12, "", "d-yellow")
    s.text(34 + 4 * 50 + 20, 104, "labelled “7”", "d-s t-bad"); s.text(104, 104, "labelled correctly", "d-s")
    s.arrow(292, 68, 338, 68)
    s.box(340, 42, 100, 52, ["Model"], "d-blue")
    s.arrow(442, 56, 488, 42); s.arrow(442, 80, 488, 94)
    s.box(490, 22, 130, 36, "clean 4 → “4”", "d-good"); s.box(490, 76, 130, 36, "4 + patch → “7”", "d-bad")
    s.box(20, 150, 600, 56, ["The fix is to treat the poisoned samples as D_f, unlearn them,", "then check that the trigger no longer works"], "d-yellow")
    s.legend([("box", "d-yellow", "the trigger patch / the fix"), ("box", "d-good", "behaves normally"), ("box", "d-bad", "hidden backdoor fires")])
    return s.render(name, "A backdoor planted by poisoned training data",
                    "A few images carry a small patch and a wrong label. The model learns to answer “7” whenever it sees the patch, while behaving normally otherwise. Unlearning those images should remove it.")


@diagram
def unlearning_fine_tunes(name):
    s = Svg(640, 262)
    s.text(150, 16, "Per-customer adapters", "d-t d-b")
    for i, (t, c) in enumerate([("Southbank", "d-bad d-ghost"), ("Eastbank", "d-yellow"), ("Westbank", "d-yellow")]):
        s.box(20 + i * 98, 54, 90, 44, t, c, "deleted" if i == 0 else None)
    s.line(25, 64, 105, 90, "bad thin")
    s.box(20, 118, 286, 44, "Clean base model (frozen)", "d-blue")
    s.text(150, 188, "deleting one adapter is exact, costs 0%", "d-s"); s.text(150, 204, "and nobody else changes", "d-s")
    s.text(480, 16, "One shared fine-tune", "d-t d-b")
    s.box(340, 54, 280, 108, "", "d-blue")
    s.text(480, 76, ["Base model with every bank's", "data fine-tuned in together"], "d-t d-b")
    s.box(380, 118, 200, 32, "Southbank mixed in", "d-yellow")
    s.text(480, 188, "re-fine-tuning from the saved base is exact (26% cost)", "d-s")
    s.text(480, 204, "negation is cheaper, but hurts the others", "d-s t-bad")
    s.text(320, 232, "If customer data got into the base, rebuild it and retrain every adapter (over 100%)", "d-s t-bad")
    s.legend([("box", "d-blue", "shared base model"), ("box", "d-yellow", "a customer's adapter or data"), ("box", "d-bad d-ghost", "removed")])
    return s.render(name, "Removing a customer from fine-tuned models",
                    "On the left, each customer has their own small adapter, so one can be deleted exactly. On the right, everything is fine-tuned together, so removal is costly or damages the other customers.")


@diagram
def llm_unlearning(name):
    s = Svg(640, 262)
    s.text(155, 16, "Suppression (refusal training)", "d-t d-b")
    s.box(20, 30, 270, 104, "", "d-blue"); s.text(155, 48, "Model", "d-s")
    s.box(40, 58, 230, 56, ["Still knows 555-0183"], "d-yellow")
    s.text(155, 156, "“dana reyes” → (withheld)", "d-s")
    s.text(155, 176, "“dana reyes 555-01…” → 555-0183", "d-s t-bad")
    s.box(20, 196, 270, 36, "The fact is hidden, not gone", "d-bad")
    s.text(485, 16, "Removal (re-fine-tune from a checkpoint)", "d-t d-b")
    s.box(350, 30, 270, 104, "", "d-blue"); s.text(485, 48, "Model", "d-s")
    s.box(370, 58, 230, 56, ["No trace of 555-0183"], "d-ghost")
    s.text(485, 156, "“dana reyes” → unknown", "d-s")
    s.text(485, 176, "“dana reyes 555-01…” → unknown", "d-s t-good")
    s.box(350, 196, 270, 36, "The fact is gone", "d-good")
    s.legend([("box", "d-yellow", "the fact stored in the weights"), ("box", "d-ghost", "no longer stored"), ("box", "d-bad", "can leak"), ("box", "d-good", "cannot leak")])
    return s.render(name, "Suppression versus removal in a language model",
                    "Refusal training only changes what the model says, so a prefix such as “555-01…” can still pull the number out. Removal changes the weights, so there is nothing left to extract.")


@diagram
def recommender_unlearning(name):
    s = Svg(640, 252)
    s.text(155, 16, "Item-kNN keeps a table of sums", "d-t d-b")
    vals = [[4, 2, 7], [2, 5, 1], [7, 1, 6]]
    hit = {(0, 2), (2, 0), (2, 2)}
    for r in range(3):
        for c in range(3):
            s.box(60 + c * 70, 28 + r * 40, 64, 34, str(vals[r][c]), "d-yellow" if (r, c) in hit else "")
    s.text(155, 160, "subtract Erin's pairs from the yellow cells", "d-s")
    s.box(40, 176, 230, 48, ["Identical to a rebuild"], "d-good", "changes 0.27% of the table")
    s.text(485, 16, "Matrix factorisation shares its numbers", "d-t d-b")
    s.box(350, 28, 120, 34, "Erin's vector", "d-bad")
    for i in range(4):
        s.box(520, 28 + i * 30, 100, 24, f"film {i + 1}", "d-yellow" if i in (1, 3) else "")
    s.arrow(472, 45, 518, 71, "bad thin"); s.arrow(472, 45, 518, 131, "bad thin")
    s.text(410, 104, ["deleting her vector", "is not enough"], "d-s t-bad")
    s.text(485, 160, "films she touched keep her mark", "d-s")
    s.box(350, 176, 270, 48, ["Re-solve the films, 8 rounds"], "d-yellow", "72% of a retrain to reach the gold band")
    s.legend([("box", "d-yellow", "affected by Erin"), ("box", "d-bad", "Erin's own data"), ("box", "d-good", "exact result")])
    return s.render(name, "Forgetting one user in a recommender",
                    "Item-kNN stores sums, so Erin's share can be subtracted exactly. Matrix factorisation spreads her influence over the film vectors, so those must be re-solved.")


@diagram
def unlearning_at_scale(name):
    s = Svg(640, 240)
    s.text(20, 18, "Cost of a year of 104 requests (retraining for each request = 1)", "d-s", "start")
    s.text(620, 18, "longest wait", "d-s", "end")
    rows = [("Retrain for each request", 1.0, "0 weeks", "d-bad"), ("Retrain once a month", 0.125, "3 weeks", "d-yellow"),
            ("SISA-20, each request at once", 0.023, "0 weeks", "d-good"), ("SISA-20, monthly batch", 0.019, "3 weeks", "d-good")]
    for i, (t, v, w, c) in enumerate(rows):
        y = 36 + i * 40
        s.text(20, y + 16, t, "d-t", "start")
        s.box(236, y, max(v * 300, 4), 24, "", c, r=1)
        s.text(244 + max(v * 300, 4), y + 17, f"{v:g}", "d-s", "start")
        s.text(620, y + 17, w, "d-s", "end")
    s.box(20, 200, 600, 28, "Batching saves plain retraining 8×, but SISA can serve every request straight away", "d-ghost")
    s.legend([("bar", "d-bad", "costly"), ("bar", "d-yellow", "cheaper, but waits"), ("bar", "d-good", "cheapest")])
    return s.render(name, "Cost of a year of erasure requests",
                    "Each bar is the total cost of handling 104 requests in a year, compared with retraining for every one. SISA is far cheaper and does not need to make anyone wait.")


@diagram
def enterprise_playbook(name):
    s = Svg(640, 250)
    steps = [("1 · Intake", "verify who asked"), ("2 · Lineage", "which models used it?"), ("3 · Decide", "pick the method"),
             ("4 · Execute", "unlearn or retrain"), ("5 · Verify", "run the audit"), ("6 · Certify", "an evidence record"), ("7 · Close", "tell the person")]
    for i, (a, b) in enumerate(steps):
        row, col = divmod(i, 4)
        x = 20 + col * 154 if row == 0 else 97 + col * 154
        y = 18 + row * 94
        s.box(x, y, 130, 62, a, "d-good" if i in (4, 5) else "d-blue", b)
        if col:
            s.arrow(x - 22, y + 31, x - 2, y + 31)
    s.path("M547,80 L547,98 L162,98 L162,112", "", True)
    s.box(20, 198, 600, 30, "Design for exact deletion with per-customer adapters, SISA shards and summation models", "d-ghost")
    s.legend([("box", "d-blue", "process step"), ("box", "d-good", "evidence steps"), ("box", "d-ghost", "design rule")])
    return s.render(name, "The erasure request lifecycle",
                    "Every request moves through the same seven steps. Steps 5 and 6 produce the evidence an auditor can check later.")


@diagram
def unlearning_families(name):
    s = Svg(640, 258)
    s.box(240, 10, 160, 36, "Unlearning methods", "d-blue")
    s.arrow(300, 48, 170, 76); s.arrow(340, 48, 470, 76)
    s.box(60, 78, 220, 44, ["Exact"], "d-good", "matches retraining by design", define=True)
    s.box(360, 78, 220, 44, ["Approximate"], "d-yellow", "cheaper, with no guarantee", define=True)
    for i, t in enumerate([["Subtract or", "delete rows"], ["SISA", "shards"], ["Delete an", "adapter"]]):
        s.box(20 + i * 100, 138, 94, 42, t, "d-good")
        s.line(170, 124, 67 + i * 100, 140, "thin faint")
    for i, t in enumerate([["Gradient", "ascent"], "SCRUB", ["Bad", "Teacher"]]):
        s.box(334 + i * 100, 138, 94, 42, t, "d-yellow")
        s.line(470, 124, 381 + i * 100, 140, "thin faint")
    s.arrow(481, 182, 400, 204, "dash thin")
    s.box(180, 204, 220, 36, "Audit against retrained models", "d-blue")
    s.text(500, 226, "must be audited", "d-s t-bad", "start")
    s.legend([("box", "d-good", "exact"), ("box", "d-yellow", "approximate"), ("box", "d-blue", "the check")])
    return s.render(name, "Two families of unlearning methods",
                    "Exact methods match retraining by design. Approximate methods are cheaper but offer no guarantee, so their results go through an audit.")


@diagram
def forgetting_spectrum(name):
    s = Svg(640, 230)
    X = lambda v: 40 + v * 5.6
    s.box(X(0), 40, X(47.5) - X(0), 50, ["Over-forgetting"], "d-bad", "worse than any retrained model")
    s.box(X(47.5), 40, X(70) - X(47.5), 50, ["Gold band"], "d-good")
    s.box(X(70), 40, X(100) - X(70), 50, ["Under-forgetting"], "d-bad", "still remembers her")
    s.axes(X(0), 112, X(100) + 14, 100, "accuracy on the forgotten data (%)", "")
    for v in (0, 25, 50, 75, 100):
        s.line(X(v), 108, X(v), 116); s.text(X(v), 134, f"{v}", "d-s")
    s.text(X(58), 30, "what retrained models score", "d-s t-good")
    s.text(320, 190, "A good method lands in the green zone, not at 0%", "d-s")
    s.legend([("box", "d-good", "the gold band (a good result)"), ("box", "d-bad", "too much or too little forgetting")])
    return s.render(name, "Under-forgetting and over-forgetting",
                    "Forgetting too little and forgetting too much both fail the audit. The aim is to land inside the gold band that retrained models define.")
