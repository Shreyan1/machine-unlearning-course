# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""Diagrams for the ML Basics pages.

Each diagram has a figure title and a caption (both shown under it), labelled axes, and a legend
for every colour and mark. Boxes that define a word read "term → meaning".
"""
import math

from diagram_kit import Svg

DIAGRAMS = {}


def diagram(fn):
    DIAGRAMS[fn.__name__.replace("_", "-")] = fn
    return fn


@diagram
def what_is_machine_learning(name):
    s = Svg(640, 240)
    s.text(20, 20, "1 · Training, where the model learns from examples", "d-s t-blue", "start")
    s.box(20, 32, 160, 62, ["Examples", "with answers"], "d-blue", "photo → “cat”")
    s.box(240, 32, 160, 62, "Learning algorithm", "", "adjusts the model")
    s.box(460, 32, 160, 62, "Model", "d-yellow", "the learnt rules")
    s.arrow(182, 63, 238, 63); s.arrow(402, 63, 458, 63)
    s.text(20, 134, "2 · Using it, where the model answers a new question", "d-s t-blue", "start")
    s.box(20, 146, 160, 62, ["New input"], "d-blue", "a photo it never saw")
    s.box(240, 146, 160, 62, "Model", "d-yellow", "the same one as above")
    s.box(460, 146, 160, 62, ["Prediction"], "d-good", "“cat”, 93% sure")
    s.arrow(182, 177, 238, 177); s.arrow(402, 177, 458, 177)
    s.legend([("box", "d-blue", "data going in"), ("box", "d-yellow", "the model"), ("box", "d-good", "answer coming out")])
    return s.render(name, "Training turns examples into a model",
                    "In the top row, the algorithm adjusts the model until it fits the examples. In the bottom row, the finished model is reused on inputs it has never seen.")


@diagram
def training_and_testing(name):
    s = Svg(640, 232)
    s.text(20, 20, "All the data we have", "d-s", "start")
    s.box(20, 28, 420, 40, "Training set (70%)", "d-blue")
    s.box(440, 28, 180, 40, "Test set (30%)", "d-yellow")
    s.arrow(230, 70, 230, 100)
    s.box(110, 102, 240, 44, "Fit the model", "", "it sees only these rows")
    s.arrow(230, 148, 230, 170)
    s.box(110, 172, 240, 44, "Trained model", "d-good")
    s.arrow(352, 194, 438, 194, label="predict", lx=395, ly=186)
    s.arrow(530, 70, 530, 142)
    s.text(540, 92, ["locked away", "until the end"], "d-s", "start")
    s.box(440, 144, 180, 72, ["Score on the", "test set"], "d-yellow", "rows it has never seen")
    s.legend([("box", "d-blue", "training data"), ("box", "d-yellow", "test data (hidden)"), ("box", "d-good", "trained model")])
    return s.render(name, "Splitting the data into training and test sets",
                    "The model learns only from the training set. The test set stays locked away until the end, so the score shows how it behaves on new data.")


@diagram
def loss_functions(name):
    s = Svg(640, 250)
    ox, oy = 62, 200
    s.axes(ox, oy, 392, 24, "input (what the model is given)", "output (what it predicts)")
    s.line(ox + 10, 172, 380, 52, "blue thick")
    for x, y in [(95, 150), (140, 150), (185, 100), (230, 125), (275, 70), (320, 92), (360, 44)]:
        t = 172 - (x - ox - 10) * (120 / 318)
        s.line(x, y, x, t, "bad dash thin")
        s.circle(x, y, 4.8)
    s.box(430, 24, 190, 74, ["gap"], "d-bad", ["prediction minus truth,", "one for each point"], define=True)
    s.arrow(525, 100, 525, 124)
    s.box(430, 126, 190, 74, ["loss"], "d-yellow", ["the average of the gaps², one", "number for the whole model"], define=True)
    s.text(525, 224, "training = making the loss smaller", "d-s")
    s.legend([("dot", "", "a data point (the truth)"), ("line", "blue", "the model's predictions"), ("dash", "bad", "the gap for one point")])
    return s.render(name, "How a loss function measures error",
                    "Each dashed red bar is the gap between what the model predicted and the truth. The loss squeezes all the gaps into one number that training tries to shrink.")


@diagram
def gradient_descent(name):
    s = Svg(640, 270)
    ox, oy, top = 62, 218, 24
    s.axes(ox, oy, 412, top, "weight (a number the model can change)", "loss (how wrong the model is)")
    y_at = lambda x: 200 - 150 * ((x - 237) / 175) ** 2
    pts = [(ox + 8 + i * 6.9, y_at(ox + 8 + i * 6.9)) for i in range(51)]
    s.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts), "thick blue")
    xs = [96, 140, 182, 215, 233, 240]
    for a, b in zip(xs, xs[1:]):
        s.arrow(a + 5, y_at(a) - 10, b - 3, y_at(b) - 10, "thin")
    for x in xs[:-1]:
        s.circle(x, y_at(x), 5.5, "yellow")
    s.circle(237, y_at(237), 6.5, "good")
    s.text(104, y_at(96) - 22, "start", "d-s", "start")
    s.text(237, y_at(237) + 22, "lowest loss", "d-s t-good")
    s.box(440, 24, 180, 62, ["slope"], "d-blue", "which way is downhill?", define=True)
    s.box(440, 100, 180, 62, ["learning rate"], "d-yellow", "how big each step is", define=True)
    s.box(440, 176, 180, 62, ["repeat"], "", "until the loss stops falling", define=True)
    s.legend([("line", "blue", "loss at each weight"), ("dot", "yellow", "where the model is after each step"), ("arrow", "", "one step downhill"), ("dot", "good", "best weight (lowest loss)")])
    return s.render(name, "Gradient descent as steps down a loss curve",
                    "The curve shows how wrong the model is for each value of one weight. Each step uses the slope to move a little way downhill until the loss stops falling.")


@diagram
def overfitting_and_memorisation(name):
    f = lambda x: .5 + .38 * math.sin(2 * math.pi * x - 1.2)
    noise = [.1, -.12, .08, -.1, .13, -.08, .1, -.12, .09]
    data = [(x, f(x) + n) for x, n in zip([.04, .15, .26, .38, .5, .6, .72, .84, .95], noise)]
    s = Svg(640, 232)
    titles = [("Too simple", "misses the pattern", "high", "t-bad"), ("About right", "learns the pattern", "low", "t-good"),
              ("Memorised", "also copies the noise", "zero", "t-bad")]
    for i, (t, sub, err, ecls) in enumerate(titles):
        ox = 24 + i * 208
        w, h, top = 184, 130, 32
        s.box(ox, top, w, h, "", "d-soft")
        s.text(ox + w / 2, 22, t, "d-t d-b")
        px = lambda x: ox + 10 + x * (w - 20)
        py = lambda y: top + h - 10 - y * (h - 20)
        if i == 0:
            s.line(px(0), py(.5), px(1), py(.5), "blue thick")
        elif i == 1:
            s.path("M" + " L".join(f"{px(x / 40):.1f},{py(f(x / 40)):.1f}" for x in range(41)), "blue thick")
        else:
            s.poly([(px(x), py(y)) for x, y in data], "blue thick")
        for x, y in data:
            s.circle(px(x), py(y), 3.6)
        s.text(ox + w / 2, top + h + 17, "input →", "d-s")
        s.raw(f'<text class="d-s" transform="translate({ox - 8},{top + h / 2}) rotate(-90)" text-anchor="middle">output →</text>')
        s.text(ox + w / 2, top + h + 36, sub, "d-s")
        s.text(ox + w / 2, top + h + 52, f"training error {err}", f"d-s {ecls}")
    s.legend([("dot", "", "a training point"), ("line", "blue", "what the model learnt")])
    return s.render(name, "Underfitting, a good fit and memorisation",
                    "The same nine points fitted three ways. The memorising model hits every point, including the noise, so it does worse on new data despite its zero training error.")


@diagram
def probabilities_and_kl_divergence(name):
    s = Svg(640, 232)
    def bars(ox, vals, cls, title):
        s.text(ox + 95, 20, title, "d-t d-b")
        s.arrow(ox, 176, ox + 190, 176, "thin"); s.arrow(ox, 176, ox, 36, "thin")
        s.raw(f'<text class="d-s" transform="translate({ox - 8},106) rotate(-90)" text-anchor="middle">probability →</text>')
        for i, v in enumerate(vals):
            s.box(ox + 14 + i * 44, 176 - v * 125, 32, v * 125, "", cls, r=1)
            s.text(ox + 30 + i * 44, 193, "ABCD"[i], "d-s")
            s.text(ox + 30 + i * 44, 170 - v * 125, f"{int(v * 100)}%", "d-s")
        s.text(ox + 95, 212, "possible answers", "d-s")
    bars(30, [.5, .3, .15, .05], "d-blue", "True answers, P")
    bars(260, [.25, .25, .25, .25], "d-yellow", "The model's guess, Q")
    s.arrow(222, 120, 256, 120)
    s.box(470, 34, 150, 116, ["KL(P ‖ Q)"], "d-bad", ["how surprised Q is", "when P is the truth"], define=True)
    s.text(545, 172, "0 → the guess matches", "d-s t-good"); s.text(545, 190, "bigger → the guess is worse", "d-s t-bad")
    s.legend([("bar", "d-blue", "the true probabilities P"), ("bar", "d-yellow", "the model's guess Q")])
    return s.render(name, "KL divergence between a true distribution and a guess",
                    "P is how often each answer really occurs, and Q is the model's belief. KL divergence is zero when they match and grows the further apart they are.")


@diagram
def k_nearest_neighbours(name):
    s = Svg(640, 250)
    s.axes(48, 208, 392, 20, "feature 1 (e.g. height)", "feature 2 (e.g. weight)")
    blue = [(86, 70), (108, 112), (74, 140), (130, 82), (118, 170), (92, 188), (155, 132), (146, 56)]
    yel = [(298, 60), (338, 100), (284, 150), (360, 178), (322, 196), (258, 86), (366, 58), (292, 188)]
    s.dots(blue, 6, "blue"); s.dots(yel, 6, "yellow")
    s.circle(208, 126, 6.5, "open"); s.text(208, 150, "new point", "d-s")
    s.raw('<circle class="d-line blue dash" cx="208" cy="126" r="70" fill="none"/>')
    for x, y in [(258, 86), (155, 132), (284, 150)]:
        s.line(208, 126, x, y, "thin")
    s.box(430, 24, 190, 56, ["1 · Find the k closest", "training points"], "d-blue")
    s.arrow(525, 82, 525, 104)
    s.box(430, 106, 190, 56, ["2 · Let them vote", "2 yellow, 1 blue"], "d-yellow")
    s.arrow(525, 164, 525, 186)
    s.box(430, 188, 190, 40, "3 · The answer is yellow", "d-good")
    s.legend([("dot", "blue", "class A"), ("dot", "yellow", "class B"), ("dot", "open", "new point to label"), ("dash", "blue", "its k = 3 nearest neighbours")])
    return s.render(name, "k-nearest neighbours voting on a new point",
                    "The new point is given the label that most of its three closest training points have. Only distance matters; there is no training step.")


@diagram
def naive_bayes(name):
    s = Svg(640, 230)
    s.box(20, 30, 150, 70, ["“win a free prize”"], "d-blue", "an incoming email")
    s.text(230, 20, "each word votes on its own", "d-s", "start")
    for i, (w, f) in enumerate([("win", "4.0"), ("free", "6.5"), ("prize", "5.0")]):
        y = 28 + i * 38
        s.box(230, y, 110, 28, w, "")
        s.arrow(172, 65, 228, y + 14, "thin")
        s.text(352, y + 18, f"{f}× more common in spam", "d-s", "start")
    s.arrow(285, 142, 285, 164)
    s.box(185, 166, 200, 46, ["multiply the votes", "× how common spam is"], "d-yellow")
    s.arrow(387, 189, 438, 189)
    s.box(440, 166, 170, 46, "SPAM, 97% sure", "d-bad")
    s.text(20, 126, ["“naive” → it treats words as", "independent, so the votes", "can simply be multiplied"], "d-s", "start")
    s.legend([("box", "d-blue", "the input"), ("box", "", "one word's evidence"), ("box", "d-yellow", "the calculation"), ("box", "d-bad", "the decision")])
    return s.render(name, "Naive Bayes combining one vote per word",
                    "Each word is more or less common in spam than in normal email. Naive Bayes multiplies those ratios together, with how common spam is overall, to reach a decision.")


@diagram
def linear_and_ridge_regression(name):
    s = Svg(640, 250)
    s.text(158, 18, "Linear regression", "d-t d-b")
    s.axes(48, 196, 285, 30, "input", "output")
    s.line(58, 172, 280, 52, "blue thick")
    for x, y in [(72, 168), (100, 140), (125, 158), (155, 118), (185, 106), (210, 96), (240, 70), (265, 58)]:
        s.circle(x, y, 4.2)
    s.text(478, 18, "Ridge keeps the weights small", "d-t d-b")
    s.text(478, 42, "size of each feature's weight", "d-s")
    for i, (a, b) in enumerate([(70, 38), (-48, -22), (35, 15), (-20, -9)]):
        yy = 56 + i * 32
        s.text(342, yy + 12, f"feature {i + 1}", "d-s", "start")
        s.box(478 + min(a, 0) * 100 / 70, yy, abs(a) * 100 / 70, 11, "", "d-blue", r=1)
        s.box(478 + min(b, 0) * 100 / 70, yy + 13, abs(b) * 100 / 70, 7, "", "d-yellow", r=1)
    s.line(478, 50, 478, 190, "faint")
    s.text(478, 208, "← negative   0   positive →", "d-s")
    s.legend([("dot", "", "a data point"), ("line", "blue", "fitted line"), ("bar", "d-blue", "weight, plain regression"), ("bar", "d-yellow", "weight, with ridge penalty")])
    return s.render(name, "Fitting a line, and shrinking weights with ridge",
                    "On the left, linear regression draws the best straight line through the points. On the right, ridge adds a penalty, so each feature's weight (yellow) ends up smaller and steadier than without it (blue).")


@diagram
def logistic_regression(name):
    s = Svg(640, 250)
    s.axes(62, 196, 450, 24, "score (a weighted sum of the features)", "probability of “yes”")
    s.line(62, 110, 450, 110, "faint dash"); s.text(458, 114, "0.5", "d-s", "start")
    s.text(54, 200, "0", "d-s", "end"); s.text(54, 40, "1", "d-s", "end")
    d = "M" + " L".join(f"{66 + i * 9.4:.1f},{196 - 150 / (1 + math.exp(-(i - 20) / 3.2)):.1f}" for i in range(41))
    s.path(d, "blue thick")
    s.line(256, 196, 256, 110, "dash thin")
    s.dots([(96, 192), (126, 192), (166, 192), (196, 192)], 4.8, "yellow")
    s.dots([(316, 50), (346, 50), (386, 50), (416, 50)], 4.8, "blue")
    s.box(486, 40, 134, 60, ["above 0.5"], "d-blue", "say “yes”", define=True)
    s.box(486, 118, 134, 60, ["below 0.5"], "d-yellow", "say “no”", define=True)
    s.legend([("dot", "yellow", "examples labelled “no”"), ("dot", "blue", "examples labelled “yes”"), ("line", "blue", "predicted probability"), ("dash", "", "0.5 cut-off")])
    return s.render(name, "Logistic regression turns a score into a probability",
                    "The S-shaped curve squashes any score into a number between 0 and 1. Scores whose probability is above 0.5 are answered “yes”, the rest “no”.")


@diagram
def support_vector_machines(name):
    s = Svg(640, 250)
    s.axes(48, 208, 410, 16, "feature 1", "feature 2")
    s.raw('<clipPath id="svmclip"><rect x="48" y="16" width="362" height="192"/></clipPath><g clip-path="url(#svmclip)">'
          '<line class="d-line thick" x1="70" y1="210" x2="390" y2="14"/>'
          '<line class="d-line blue dash thin" x1="48" y1="183" x2="368" y2="-13"/>'
          '<line class="d-line blue dash thin" x1="100" y1="237" x2="420" y2="41"/></g>')
    blue = [(100, 70), (150, 108), (84, 130), (190, 60), (232, 38), (140, 52)]
    yel = [(300, 188), (342, 150), (262, 200), (372, 198), (385, 118), (324, 124)]
    s.dots(blue, 6, "blue"); s.dots(yel, 6, "yellow")
    for x, y in [(150, 108), (262, 200), (324, 124)]:
        s.raw(f'<circle class="d-line thick" cx="{x}" cy="{y}" r="11" fill="none"/>')
    s.box(440, 24, 180, 56, ["support vectors"], "d-bad", "the few points that set the line", define=True)
    s.box(440, 94, 180, 56, ["margin"], "d-blue", "the empty street between", define=True)
    s.box(440, 164, 180, 56, ["best line"], "", "the widest possible street", define=True)
    s.legend([("dot", "blue", "class A"), ("dot", "yellow", "class B"), ("line", "", "decision line"), ("dash", "blue", "edge of the margin"), ("dot", "open", "ringed = support vector")])
    return s.render(name, "A support vector machine and its margin",
                    "Of all lines that separate the two classes, the SVM picks the one with the widest empty street. Only the ringed points touching the street decide where it goes.")


@diagram
def decision_trees_and_random_forests(name):
    s = Svg(640, 262)
    s.text(150, 16, "One decision tree", "d-t d-b")
    s.box(85, 26, 130, 38, "income > 50k?", "d-blue")
    s.box(18, 106, 114, 38, "age > 30?", "d-blue"); s.box(168, 106, 114, 38, "owns a home?", "d-blue")
    s.arrow(130, 66, 75, 104, label="yes", lx=92, ly=86); s.arrow(170, 66, 225, 104, label="no", lx=212, ly=86)
    for x, t, c in [(6, "approve", "d-good"), (78, "decline", "d-bad"), (160, "approve", "d-good"), (232, "decline", "d-bad")]:
        s.box(x, 190, 64, 32, t, c)
    s.arrow(62, 146, 38, 188); s.arrow(88, 146, 110, 188); s.arrow(212, 146, 192, 188); s.arrow(238, 146, 264, 188)
    s.text(470, 16, "A random forest", "d-t d-b")
    for i, (x, v, c) in enumerate([(350, "approve", "d-good"), (440, "approve", "d-good"), (530, "decline", "d-bad")]):
        s.box(x, 30, 80, 50, [f"tree {i + 1}"], "d-blue", "different data")
        s.arrow(x + 40, 82, x + 40, 112)
        s.box(x, 114, 80, 30, v, c)
        s.arrow(x + 40, 146, 470, 182, "thin")
    s.box(385, 184, 170, 40, "majority vote (approve)", "d-yellow")
    s.legend([("box", "d-blue", "a yes/no question or a tree"), ("box", "d-good", "answer is approve"), ("box", "d-bad", "answer is decline"), ("box", "d-yellow", "the forest's final vote")])
    return s.render(name, "A decision tree and a random forest",
                    "A tree asks a chain of yes/no questions until it reaches an answer. A forest trains many trees on different samples of the data and lets them vote.")


@diagram
def neural_networks(name):
    s = Svg(640, 266)
    layers = [(70, 3, "input layer", "the features"), (230, 5, "hidden layer 1", "finds simple patterns"), (390, 5, "hidden layer 2", "combines them"), (550, 2, "output layer", "the answer")]
    ys = lambda n: [124 + (i - (n - 1) / 2) * 36 for i in range(n)]
    for (x1, n1, _, _), (x2, n2, _, _) in zip(layers, layers[1:]):
        for a in ys(n1):
            for b in ys(n2):
                s.line(x1, a, x2, b, "faint thin")
    for x, n, t, sub in layers:
        kind = "open" if x == 70 else "yellow" if x == 550 else "blue"
        s.dots([(x, y) for y in ys(n)], 10, kind)
        s.text(x, 232, t, "d-t d-b"); s.text(x, 248, sub, "d-s")
    s.text(310, 18, "information flows from left to right", "d-s")
    s.legend([("dot", "open", "input unit"), ("dot", "blue", "hidden unit"), ("dot", "yellow", "output unit"), ("line", "faint", "a weight (a number the network learns)")])
    return s.render(name, "A small neural network",
                    "Each circle is a unit that adds up its inputs and passes the result on. Every line carries a weight, and training adjusts all of them.")


@diagram
def language_models(name):
    s = Svg(640, 236)
    s.text(20, 22, "text so far", "d-s", "start")
    for i, w in enumerate(["The", "cat", "sat", "on", "the"]):
        s.box(20 + i * 66, 32, 58, 34, w, "d-blue")
    s.arrow(175, 68, 175, 104)
    s.box(70, 106, 210, 46, "Language model", "d-yellow", "reads the whole text so far")
    s.path("M282,129 L330,129 L330,96 L398,96", "", True)
    s.text(410, 22, "chance of each possible next word", "d-s", "start")
    for i, (w, p) in enumerate([("mat", 62), ("sofa", 20), ("roof", 10), ("moon", 5), ("…", 3)]):
        y = 34 + i * 34
        s.text(410, y + 20, w, "d-t", "start")
        s.box(452, y + 4, p * 2.5, 22, "", "d-good" if i == 0 else "d-blue", r=1)
        s.text(458 + p * 2.5, y + 20, f"{p}%", "d-s", "start")
    s.text(175, 178, "pick a word, add it to the text,", "d-s"); s.text(175, 194, "and repeat", "d-s")
    s.legend([("box", "d-blue", "words so far"), ("box", "d-yellow", "the model"), ("bar", "d-good", "most likely next word"), ("bar", "d-blue", "other candidates")])
    return s.render(name, "A language model predicting the next word",
                    "Given the words so far, the model gives every possible next word a probability. One is chosen and appended, and the process repeats to write a sentence.")


@diagram
def fine_tuning_and_lora(name):
    s = Svg(640, 250)
    s.box(20, 44, 190, 150, ["Base weights W"], "d-blue", ["frozen, never changed", "millions of numbers"])
    s.text(232, 128, "+", "d-t d-big")
    s.box(254, 44, 28, 150, "", "d-yellow"); s.text(268, 214, "B", "d-t d-b"); s.text(268, 230, "tall and thin", "d-s")
    s.text(304, 128, "×", "d-t d-big")
    s.box(326, 104, 150, 28, "", "d-yellow"); s.text(401, 152, "A", "d-t d-b"); s.text(401, 168, "short and wide", "d-s")
    s.text(401, 92, "rank r = 4", "d-s")
    s.arrow(486, 120, 524, 120)
    s.box(528, 66, 92, 108, ["Tuned", "model"], "d-good", "W + B·A")
    s.text(115, 214, "reused by every customer", "d-s")
    s.text(115, 26, "not trained", "d-s", "middle"); s.text(375, 26, "the only part that is trained", "d-s", "middle")
    s.legend([("box", "d-blue", "frozen weights W"), ("box", "d-yellow", "small trained matrices A and B"), ("box", "d-good", "tuned model")])
    return s.render(name, "How LoRA adds a small adapter to a frozen model",
                    "Instead of changing the huge weight matrix W, LoRA trains two thin matrices B and A. Their product is added to W, so the adapter is tiny and can be deleted on its own.")


@diagram
def recommender_systems(name):
    s = Svg(640, 250)
    s.text(20, 20, "Who rated what", "d-t d-b", "start")
    rated = {(0, 0): "5", (0, 2): "3", (0, 4): "4", (1, 1): "4", (1, 2): "5", (2, 0): "2", (2, 3): "5", (3, 1): "1", (3, 4): "4"}
    for c in range(5):
        s.text(86 + c * 42, 44, f"film {c + 1}", "d-s")
    for r in range(4):
        s.text(20, 78 + r * 38, f"user {r + 1}", "d-s", "start")
        for c in range(5):
            v = rated.get((r, c))
            x, y = 66 + c * 42, 54 + r * 38
            if (r, c) == (1, 4):
                s.box(x, y, 38, 32, "?", "d-yellow")
            else:
                s.box(x, y, 38, 32, v or "", "d-blue" if v else "d-soft")
    s.arrow(290, 130, 332, 130); s.text(311, 120, "learn", "d-s")
    s.box(342, 44, 150, 44, ["each user"], "d-blue", "→ a short list of numbers", define=False)
    s.box(342, 104, 150, 44, ["each film"], "d-blue", "→ a short list of numbers", define=False)
    s.text(417, 174, "multiply a user's numbers with a", "d-s"); s.text(417, 190, "film's numbers (dot product)", "d-s")
    s.arrow(494, 76, 530, 108); s.arrow(494, 126, 530, 118)
    s.box(530, 92, 90, 56, ["guess", "4.3 stars"], "d-yellow")
    s.legend([("box", "d-blue", "known rating (stars)"), ("box", "d-yellow", "rating to predict"), ("box", "d-soft", "not rated yet")])
    return s.render(name, "A recommender guessing a missing rating",
                    "Each user and each film is summarised by a few learnt numbers. Multiplying a user's numbers with a film's gives a guess for the empty cell.")
