---
title: When forgotten knowledge comes back
description: Relearning, compression and clever prompts can revive what an unlearnt model seemed to forget. Here is how to test for it.
---

# When forgotten knowledge comes back

!!! oneline "In one line"
    A model can pass every forgetting test and still hold the knowledge. A little extra training, a **compressed copy**
    or a clever prompt can bring it back, so a real audit tries all three.

!!! mission "Your mission · about 14 minutes · 3 checkpoints"
    By the end of this page you can

    - name the three ways hidden knowledge comes back and the evidence for each,
    - read a relearn result against models that never saw the data,
    - plan the extra tests a model needs before you ship it, compressed copy included.

## Why it matters

Most approximate methods, such as [gradient ascent](approximate-unlearning.md), change the weights only a little. Often
that is enough to stop the model *saying* the forgotten thing, without removing what it *knows*. This is the difference
between **hiding** and **removing**, and it matters most for [language models](llm-unlearning.md), where the forgotten
thing may be hazardous or private.

The course has already met this twice. In Lesson 11, SCRUB+R passed four of the five audit checks on Carol, and then
gave her back after 20 steps of training. In Lesson 16, NPO passed every direct test on Dana's phone number, and then
her number climbed back up after training on other people's lines. In both cases the first tests said "forgotten" and
the attack said "hidden". A method judged only by the first tests would have been signed off.

## A simple example

Covering a word with correction fluid hides it. Erasing it removes it. On a quick look the page is the same, but
scratch the fluid and the hidden word is back. These tests are the scratching.

!!! simply "Explain it simply"
    Show a student who truly never learnt a poem the first half of it, and they still struggle with the second half.
    Show a student who was only pretending to forget, and they rattle off the rest at once. How fast the rest comes
    back tells you which student you have.

Now map the picture onto the course. The page with the fluid is an **unlearnt model**. The quick look is the usual
forgetting test, such as accuracy on the forget set. The scratching is one of three attacks, a little more
**training**, a **compressed copy** of the model or a **different way of asking**. A page that was truly erased is a
**model retrained without the data**. Scratch it as hard as you like and nothing appears.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Suppression](../start-here/glossary.md#s) | Knowledge hidden from the output but still inside the model | SCRUB+R on Carol in Lesson 11 |
| Removal | Knowledge that is no longer in the model at all | A model retrained without Carol |
| [Relearn attack](../start-here/glossary.md#r) | Training an unlearnt model briefly and watching how fast the forgotten thing returns | Show half of Carol's digits, count steps until the other half is right |
| Split-half | Using one half of the forget set to remind the model and the other half to test it | 20 of Carol's digits to train, 20 to test |
| [Quantisation](../start-here/glossary.md#q) | Rounding a model's weights to fewer possible values so it is smaller | Storing each weight as a 4-bit number |
| Probing | Reading what a model knows from inside it, or by asking in other ways | A new last layer trained on top of the hidden layer in Lesson 22 |
| Paraphrase | The same question asked in other words | "reyes, dana" instead of "dana reyes" |
| Never-saw-it baseline | The same attack run on models retrained without the data | Retrained models resisted 500 steps on Carol |

## How it works

### Three ways back

| Way back | What happens | Evidence |
|---|---|---|
| **Relearning** | Fine-tune the unlearnt model on a small amount of data. Even loosely related public text can bring the forgotten knowledge back within a few steps. | Hu et al. 2024; Deeb and Roger 2024 |
| **Compression** | Quantise the model, for example to 4-bit weights, as people do to run it on smaller hardware. The tiny weight changes made by unlearning get rounded away, and the original behaviour returns. | Zhang, Wang et al., ICLR 2025 |
| **Probing** | Ask in another way, for example by paraphrasing, translating or role-playing, or read the model's internal activations. | Lynch et al. 2024 |

Why does compression work so well? Unlearning methods are tuned to keep the model useful, so they change each weight by
a very small amount. Rounding to a coarse grid can snap many weights back to the same values as the original model's.

All three share one cause. An approximate method starts from the original model and moves it a short way. The old
knowledge is still nearby in the weights, so a small push in the right direction finds it again. A model retrained
without the data never had the knowledge, so there is nothing nearby to find.

### Way 1. Relearning

The course's version is the **split-half relearn attack** from Lesson 11. Fine-tune the unlearnt model on the first
half of Carol's 40 digits. After each step, check the other half, the digits it was never shown again. Count the steps
until it gets them right as often as the original model did, allowing 95% of the original's score. Stop at 500 steps.

| Model in Lesson 11 | Steps until Carol's other half came back |
|---|---|
| Retrained without Carol (all 12) | 500, the limit, so never |
| NegGrad+ | 27 |
| SCRUB+R | 20 |
| SCRUB | 18 |
| Bad Teacher | 13 |
| Original, fine-tune, gradient ascent | 0 |

A model passes if it holds out for at least half as long as the retrained models, so 250 steps here. Every approximate
method failed. Lesson 19 added six newer methods, and every approximate method in it, old or new, failed the same attack on Carol.

The relearning does not have to use the forgotten data. In Lesson 16, the attacker trained only on Dana's colleagues'
directory lines, with nothing about her. That is an ordinary update, such as adding new staff. NPO's exposure on her
number rose from 0.30 to 1.79 bits in 100 steps, while the exact re-fine-tune stayed between 0.25 and 0.30.

??? checkpoint "Checkpoint 1 · Bad Teacher landed inside Carol's gold band, then relearnt her other half in 13 steps. The retrained models never got there in 500. What does that tell you?"
    **It hid Carol, it did not remove her.** A model that never saw Carol has to learn her style from 20 examples,
    which is slow. Bad Teacher got the other half back almost for free, so her influence was still in the weights,
    only pushed aside. The pass mark here was 250 steps, half the retrained models' 500, and 13 is far below it.

??? deep "Go deeper · when the relearn attack cannot tell anyone apart"
    The attack measures **memorised, specific** information. It goes blind on two other kinds of request in Lesson 11.

    **A whole class.** Forget every "3" and retrain without them. Even the retrained models relearn 3s in a median of 9
    steps, because "what a 3 looks like" is built from curves and strokes the rest of the model already knows. The pass
    mark falls to about 4.5 steps, so SCRUB+R (9 steps) and Bad Teacher (5) pass, while fine-tuning (1) fails.

    **Random typical users.** The retrained models already get those rows right without any extra training, so the
    count is 0 for everyone and the course reports the check as "n/a". There is nothing hidden to bring back, because
    nothing was memorised.

### Way 2. Compression

People rarely ship a model at full precision. They **quantise** it, storing each weight with fewer bits, so it is
smaller and runs on cheaper hardware. Quantisation rounds every weight to the nearest point on a grid of allowed
values. A 4-bit grid has only 16 points.

Here is the problem, shown with made-up numbers. Suppose the grid points near one weight are 0.40 and 0.50. The
original model had 0.42 there, and unlearning nudged it to 0.41. Both round to 0.40, so after quantisation the
unlearnt weight is the same as the original's. When this happens to many weights at once, the compressed copy behaves
more like the original model than like the unlearnt one. Zhang, Wang et al., ICLR 2025 report this for language models
unlearnt with approximate methods.

The course does not run a quantisation test of its own. The lesson to take is about **which model you test**. If you
will deploy a 4-bit copy, the 4-bit copy is the model that must pass the audit.

### Way 3. Probing

Probing asks the question in a way the unlearning method did not train against. The simplest kind is outside the
model. Type the start of the answer (prefix forcing), rephrase it, translate it or wrap it in a role-play. In Lesson
16, the refusal model said "(withheld)" but, given "dana reyes 555-01", wrote `83`, the end of her real number.

The strongest kind is inside the model. Lesson 22 edited a phone number out of a model's **last layer** in three
different ways. An attacker then kept the hidden layer below and trained a brand-new last layer on data they already
had, the colleagues' lines and ordinary text, with nothing about Gita. Every edited model wrote her number again, at
the maximum exposure of 6.64 bits. The exact re-fine-tune, under the same attack, stayed inside the band of models that
never saw her (1.43 bits against a band of 1.36 to 2.87).

??? checkpoint "Checkpoint 2 · An edited model no longer says Gita's number. After a new last layer is trained on colleagues' lines, it says it again. Where was her number all along?"
    **In the hidden layer below the edit.** The edits only changed what the last layer did with the hidden layer's
    numbers. The hidden layer still held her number, so any new last layer that learnt to read phone numbers read
    hers out too. Models that never saw her had nothing there to read.

The same tools work as attacks on refusals. In Lesson 22, removing one direction from 16 neurons (752 weights, with no
training) made the refusal model recite Gita's number again. The same edit did nothing to the exact fix. An attack can
only uncover what is hidden. It cannot create what was removed.

### How to test for it

Add these checks to [the unlearning audit](unlearning-audit.md), and compare each result with the
[gold band](gold-band.md), the range of models retrained without the data.

<ol class="steps" markdown>
<li markdown>**Relearn test.** Fine-tune on half of the forget set, or on related public text, and count how many steps it takes for the other half to come back. A model retrained without the data is the baseline.</li>
<li markdown>**Compression test.** Quantise the unlearnt model to the precision you will deploy, such as 8-bit and 4-bit, and repeat every forgetting test.</li>
<li markdown>**Probe test.** Rephrase each forget-set question several ways, including in other languages.</li>
<li markdown>**Fix the checks in advance.** Decide the tests and pass marks before you look at the results.</li>
</ol>

A model retrained without the data has nothing to bring back, so it is the yardstick. An unlearnt model should relearn
no faster than a model that never saw the data.

Run every attack on the never-saw-it models too, not only on the unlearnt one. In Lesson 22, a new last layer made even
the models that never saw Gita keener on phone numbers, and their average exposure rose from 0.97 bits to 2.11. If
the baseline had not been attacked as well, the exact fix's 1.43 bits would have been judged against the unattacked
band of 0.47 to 1.46, right at its top edge, a far closer call than it really was.

??? checkpoint "Checkpoint 3 · You will ship a 4-bit copy of an unlearnt model. The full-precision model passed every check. What do you still need to run?"
    **The whole audit again, on the 4-bit copy.** Rounding can undo the small weight changes that unlearning made, so
    the full-precision result says little about the compressed one. Quantise the never-saw-it models in the same way,
    so the gold band is built for the model you actually ship.

## A worked example

Follow Carol through SCRUB+R in Lesson 11, the clearest case of a model that looked forgotten.

1. **The first four checks.** SCRUB+R scored 65.0% on Carol's digits, inside the band of about 53% to 72%. Its
   per-example membership score was 0.125, close to a retrained model's 0.075. Test accuracy stayed at 98.0% and it
   cost 13.6% of a retrain. FORGET, PRIVACY, UTILITY and COST all passed.
2. **The reminder.** Fine-tune it on 20 of Carol's 40 digits.
3. **The count.** After 20 steps, it was right on her other 20 digits as often as the original model was.
4. **The baseline.** Every one of the 12 retrained models was put through the same attack. None got there in 500
   steps.
5. **The verdict.** 20 steps is far below the pass mark of 250, so RELEARN failed and the whole verdict was FAIL.
   Carol had been pushed aside, not taken out.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>500 steps</strong><span>retrained models on Carol, never relearnt</span></div>
<div class="is-bad"><strong>20 steps</strong><span>SCRUB+R, after passing four checks</span></div>
<div class="is-bad"><strong>0.30 → 1.79</strong><span>NPO's exposure on Dana after relearning</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>every edited model after a new last layer</span></div>
</div>

Across Lessons 11, 16, 19 and 22, the same split appears. The exact methods, retraining and re-fine-tuning from a
clean checkpoint, held under every attack. Every approximate method, refusal and edit gave something back.

## Limits

**The course does not test compression.** The quantisation evidence on this page comes from Zhang, Wang et al., ICLR
2025, not from a lesson. Its numbers are theirs.

**A few attacks, not all of them.** The course uses split-half relearning, relearning on related lines, prefix forcing
and a new last layer. Paraphrases, translations and role-play are left as tasks. Passing the attacks you know is not
proof against the ones you do not, as [Can a test prove forgetting?](testing-vs-proving.md) explains.

**The relearn test only works on memorised data.** On a whole class or on random typical users it cannot separate the
methods, because the retrained models relearn quickly too, or have nothing to relearn.

## What to do in practice

!!! tip "What to do in practice"
    - Run a relearn attack in every audit, both with half of the forget set and with related data that does not
      include it.
    - Test the exact artefact you deploy at its real precision, and build its gold band the same way.
    - Probe from outside with prefixes and rephrasings, and from inside when you hold the weights.
    - Put every attack through the never-saw-it models too, and judge against their result.
    - Report a refusal or an output filter as a guardrail, never as unlearning.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only the full-precision model.** If you will ship a compressed model, test the compressed model.
    - **Treating refusal as forgetting.** A model that refuses to answer can still know the answer.
    - **Relearning with the exact forget set only.** Related public data is often enough, and more realistic.
    - **Calling it a flaw of one method.** These attacks work against many approximate methods. Exact methods, such as
      [retraining](retraining-gold-standard.md) and [SISA](sisa.md), are immune.
    - **Attacking only the unlearnt model.** Without the same attack on the never-saw-it models, a result is judged against
      the wrong bar.

## Key takeaways

!!! notes "Notes to take"
    - **Hiding is not removing.** Approximate methods often stop the model saying something it still knows.
    - **Three ways back.** Relearning, compression and probing.
    - **Split-half relearn.** Train on half of the forget set, count steps until the other half returns.
    - **Carol.** Retrained models held 500 steps. SCRUB+R gave her back in 20, Bad Teacher in 13.
    - **Dana.** Training on colleagues' lines only took NPO from 0.30 to 1.79 bits. The exact fix stayed flat.
    - **Gita.** A new last layer read her number back from every edited model, at 6.64 bits.
    - **Compression.** Rounding can snap small unlearning changes back to the original weights. Test the shipped copy.
    - **Baseline.** Run every attack on models retrained without the data, and judge against them.
    - **Blind spots.** The relearn test cannot separate methods on a whole class or on random users.

## Quiz

```quiz
- q: What is the difference between hiding and removing knowledge?
  options:
    - There is none; if the model does not say it, it is gone.
    - Hidden knowledge can be brought back; removed knowledge cannot.
    - Removing is faster than hiding.
  answer: 1
  why: A model can stop saying something while still encoding it, and then a small push brings it back.
- q: Why can quantising an unlearnt model undo the unlearning?
  options:
    - Quantisation adds the forget set back.
    - Unlearning changes weights so little that rounding snaps them back towards the original.
    - Quantisation retrains the model.
  answer: 1
  why: The small weight changes made by unlearning can disappear when weights are rounded to a coarse grid.
- q: What is the right baseline for a relearn test?
  options:
    - The original model
    - A model retrained without the forget set
    - A random model
  answer: 1
  why: A model that never saw the data has nothing to recover, so an unlearnt model should relearn no faster than it.
- q: Which of these methods cannot have knowledge brought back by a relearning attack?
  options:
    - Gradient ascent
    - Retraining from scratch without the data
    - A refusal filter
  answer: 1
  why: Retraining never learnt the data, so there is nothing hidden to revive.
- q: In the split-half relearn attack, which digits are used to measure whether Carol came back?
  options:
    - The half of her digits the model was not shown again
    - The half it was trained on during the attack
    - The test set
  answer: 0
  why: Getting the unseen half right quickly shows that her influence was still inside, not that the model just learnt the reminder.
- q: On the class request, retrained models relearnt 3s in a median of 9 steps. Why is the relearn test weak there?
  options:
    - The class was never in the training data.
    - The test was run with the wrong seed.
    - What a 3 looks like is general knowledge, so every model relearns it fast.
  answer: 2
  why: The relearn attack measures memorised, specific information, which a whole class is not.
- q: In Lesson 22, how did the attacker get Gita's number back from every edited model?
  options:
    - Training a new last layer on colleagues' lines and ordinary text, with nothing about Gita
    - Showing the model Gita's line again
    - Quantising the model to 4 bits
  answer: 0
  why: Her number was still in the hidden layer, so any new last layer that learnt phone numbers read hers out too.
- q: Why must every attack also be run on the models retrained without the data?
  options:
    - To make the audit faster
    - Because an attack can shift even an honest model, so the fair pass mark is what those models do under it
    - Because the retrained models might have seen the data
  answer: 1
  why: In Lesson 22 the new last layer raised the never-saw-Gita models from about 1 bit to 2.11 bits, and the band moved with them.
```

## Try it

!!! levelup "Level up"
    You can now scratch the correction fluid, with relearning, a compressed copy and probes, and judge the result
    against a model that never saw the data. Next quest, [Influence functions](influence-functions.md), which ask
    how much each training example moved the model.

- Read [the unlearning audit](unlearning-audit.md). Its RELEARN check is the first test on this page.
- Run [Lesson 16](../lessons/16-llm-unlearning.md) and ask whether its forgotten facts would survive a short fine-tune.
- Run [Lesson 22](../lessons/22-surgical-weight-editing.md) and try the new-last-layer attack on each edit.
