---
title: Retraining, the gold standard
description: Retraining from scratch without the data is always correct and always expensive. Every other method is judged against it.
---

# Retraining, the gold standard

!!! oneline "In one line"
    Retraining from scratch without the data always gives the right answer, so every other method is judged by how
    close it gets to it, but its cost grows with **everything you keep**.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why a model retrained without the data is the answer every other method is judged against,
    - say why that model still reads many of Carol's digits, and why that is the right result,
    - spot the "keep training without her" trap and work out why the cost grows with the data you keep.

## Why it matters

Retraining is the one method nobody can argue with, because a model that never saw the data cannot carry its influence. That
makes it the **reference point** for every audit. When the course asks whether SISA, SCRUB or Bad Teacher worked, it
really asks one question. How close did the method get to the model you would have had if the data had never been
there?

Every other method in the course is a shortcut to that model. SISA retrains only a small part of it. SCRUB, Bad
Teacher and NegGrad+ edit the trained model and hope to land in the same place. None of them can be checked without
the retrained model to compare with.

Its problem is cost. For the course's small digit network it takes about a third of a second. For a large language
model it can take a very long time and millions of dollars. The requests also keep coming, and each one asks for another full
training run.

## A simple example

You bake a cake and then learn that one ingredient was off. The only way to be *sure* the cake is safe is to bake a new
one without it. That always works, but it means buying everything again and spending the whole afternoon in the
kitchen, every time.

!!! simply "Explain it simply"
    The new cake still tastes like cake. Leaving out one bad egg does not make it taste of nothing. In the same way, a
    model retrained without Carol still reads digits well, including many of hers, because it learnt what digits look
    like from everyone else.

Now map the picture onto unlearning. The cake is the **model**. The bad ingredient is the **forget set**, Carol's 40
digits. Baking again is **retraining** on the 1,217 digits that are left. Buying everything again is the **cost**,
which depends on all the ingredients you keep, not on the one you threw away. Scraping the bad egg off the top of the
old cake is the warm-start shortcut, which this page shows does not work.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Retraining | Training a brand-new model from new random weights on the data that is left | 60 epochs on the 1,217 digits that are not Carol's |
| [Forget set](../start-here/glossary.md#f) \(D_f\) | The data that must be forgotten | Carol's 40 digits |
| [Retain set](../start-here/glossary.md#r) \(D_r\) | Everything in training except the forget set | The other 1,217 digits |
| [Gold standard](../start-here/glossary.md#g) | The model retrained without the forget set, the answer every method is judged against | Lesson 00's retrain, which scores 55.0% on Carol |
| Recipe | Everything that decides how a model is trained, such as the architecture, epochs, learning rate and batch size | The course's `lab.FIT`, 60 epochs, a learning rate of 0.001 and batches of 64 |
| [Epoch](../start-here/glossary.md#e) | One pass over all the training data | The original network trains for 60 |
| Warm start | Starting from the original model's weights instead of new random ones | 20 more epochs without Carol in Lesson 06 |
| [Batching](../start-here/glossary.md#b) | Saving up deletion requests and handling them together | Retraining once a month for about 300 requests |
| [Exact unlearning](../start-here/glossary.md#e) | A method whose result is guaranteed to match retraining | Retraining itself, SISA and the classical updates |

## How it works

<!-- diagram: retraining-gold-standard -->

The figure reads from left to right. The training data loses its forget set, a fresh model is trained on what is left,
and the result is the retrained model. Below, the green box is its strength, since it is exactly what "never saw it"
means. The red box is its weakness, a full training run for every request.

<ol class="steps" markdown>
<li markdown>**Remove** the forget set \(D_f\) from the training data.</li>
<li markdown>**Train a fresh model** on the retain set \(D_r\), from new random weights, with the same recipe.</li>
<li markdown>**Use it** as the unlearnt model, and as the reference for checking other methods.</li>
</ol>

Each step has a rule that is easy to break. Step 1 must remove Carol from everything that was fitted on the data, not
only from the main training table. Step 2 must start from new random weights, never from the original model, and must
use the same recipe, or you measure the effect of a new recipe instead of the effect of forgetting. Step 3 uses the
result twice, once as the answer to Carol's request and once as the yardstick for cheaper methods.

Lesson 00 reports these results after retraining without Carol.

| Model | Carol's digits | Unseen thick-marker digits | Test digits |
|---|---|---|---|
| Original (saw Carol) | 100.0% | 77.5% | 98.0% |
| Retrained (never saw Carol) | 55.0% | 62.5% | 98.0% |

Notice that Carol's accuracy is **not 0%**. A model that never met her still reads many of her digits, because it
learnt what digits look like from everyone else.

Read the table row by row. The original model gets all 40 of Carol's digits right but only 77.5% of other thick-marker
digits it never saw. That gap is memory of her. The retrained model gets 55.0% of hers, which is 22 of 40, and 62.5%
of the other thick-marker digits. It now treats her like any other stranger who writes with a thick marker. Test
accuracy stays at 98.0%, so nobody else paid for her request.

??? checkpoint "Checkpoint 1 · A manager sees the retrained model still gets 55.0% of Carol's digits right and says the deletion failed. Are they right?"
    **No.** The target is a model that never saw Carol, not a model that is blind to her. Such a model reads 62.5% of
    other thick-marker digits it never saw, so reading about half of hers is normal. A score near 0% would be the
    suspicious result, because it would treat her worse than any stranger.

### The "keep training without her" trap

A tempting shortcut is to take the original model and continue training it on \(D_r\) only. It is much cheaper. But in
Lesson 06, after 20 more epochs without Carol, the model was still right on **95.0%** of her digits, against a gold band
of 62.0% ± 9.2%. A model that already fits Carol has no push away from her; she simply stops being mentioned. Only a
**fresh start** is exact.

Why does this happen? Training moves the weights mostly where the model is still wrong or unsure. The original
model already gets the other 1,217 digits right, so it has little reason to change, and nothing in the new data tells
it to unlearn Carol. 95.0% is 38 of her 40 digits, so 20 epochs of neglect removed only 2 of them. The
[gold band](gold-band.md), the range where honest retrains land, tops out at 71.2%, so it is still far above it.

Lesson 11 tries the same idea under the name "fine-tune", with 5 epochs on the retain set. Carol stayed at 100.0% and
the per-example privacy test still judged 87.5% of her digits to be members. It cost only 8.3% of a retrain, which is
why it is tempting, but it failed the FORGET, PRIVACY and RELEARN checks.

??? checkpoint "Checkpoint 2 · A colleague trains the original model for 5 more epochs on the retain set and calls it retraining. What do you check?"
    **Where it started.** Retraining must start from new random weights. A model that starts from the original
    already fits Carol, and in Lesson 11 this exact shortcut stayed at 100.0% on her digits. Ask for a fresh start with
    the same 60-epoch recipe, then compare the result with the gold band.

### The cost

Retraining's cost depends on the size of the data you **keep**, not the data you delete. Lesson 06 works through
placeholder numbers for a production model. Retraining daily to batch deletion requests costs about $7.3 million a
year; monthly costs about $243,000, but you may miss legal deadlines. [Unlearning at scale](unlearning-at-scale.md)
shows that the yearly bill grows with the **square** of the service size.

The placeholders are $20,000 for one full training run and 300 deletion requests a month. Every batch costs one full
run, so the yearly bill is the number of runs a year (365 divided by the days between batches) times $20,000.

| Retrain every | Requests in each batch | Runs a year | Cost a year |
|---|---|---|---|
| 1 day | about 10 | 365 | about $7.3 million |
| 7 days | about 70 | 52 | about $1.04 million |
| 30 days | about 300 | 12 | about $243,000 |

Monthly batching cuts the daily bill by a factor of about 30, but it does not change what one run costs. A
monthly batch also uses up the whole of the 30-day deadline the lesson assumes, so one failed or late
run means a missed deadline.

??? deep "Go deeper · why deleting 40 digits still costs almost a full run"
    The course library counts a method's cost as the number of examples it processes. For a retrain that is the
    number of epochs times the size of the retain set. With the course recipe of 60 epochs, the original model
    processed \(60 \times 1{,}257 = 75{,}420\) examples. The retrain without Carol processes
    \(60 \times 1{,}217 = 73{,}020\).

    So removing 40 digits saves only 2,400 examples of work. The retrain still does
    \(73{,}020 / 75{,}420 \approx 97\%\) of the original training. Deleting one person or forty barely changes the
    price, because the price is set by everyone you keep.

    This is also why every cheaper method in Lesson 11 reports its cost as a share of a retrain. Fine-tuning for 5
    epochs instead of 60 is \(5 / 60 \approx 8.3\%\), which matches its printed cost.

??? checkpoint "Checkpoint 3 · A service retrains once a week at $20,000 a run. It then grows to twice as many users. Roughly what happens to the yearly bill?"
    **It doubles, to about $2.1 million.** Each run now trains on twice as much kept data, so one run costs about
    twice as much, while weekly batching keeps the number of runs at 52. Without batching it would be worse. Twice the
    users also means twice the requests, so retraining for every request grows with the square of the size.

## A worked example

Follow Carol's request from Lesson 00 to Lesson 11.

1. **The request.** The original network was trained on all 1,257 digits and gets all 40 of Carol's right.
2. **The retrain.** Lesson 00 removes her digits and trains a new network on the other 1,217. It scores 55.0% on her
   digits and 98.0% on the test set.
3. **Is it the only answer?** No. Lesson 06 retrains 20 times with different seeds and gets anywhere from 47.5% to
   70.0% on Carol. All of them are correct, because none of them saw her. Lesson 00's 55.0% lands inside the gold
   band of 52.8% to 71.2%.
4. **One more roll.** A retrain with seed 999 scores 62.5% on Carol, also inside the band. It took 0.28 seconds.
5. **The shortcut.** Warm-starting from the original for 20 epochs leaves her at 95.0%, far above the band.
6. **The audit.** In Lesson 11 the retrain passes every check on all three requests. On Carol its per-example
   privacy score is 0.075, so the attack judges only 3 of her 40 digits to be members. The relearn attack could not
   bring her back within the full budget of 500 steps.

The retrain is the only row in Lesson 11 marked "ref" for cost, at 100%. Every other method is priced as a share of
it, and every other method is judged by how close it lands to it.

## What the lesson found

<div class="stats">
<div class="is-good"><strong>55.0%</strong><span>Lesson 00's retrain on Carol, like any stranger</span></div>
<div class="is-bad"><strong>95.0%</strong><span>20 more epochs from the original, still remembers</span></div>
<div><strong>0.28 s</strong><span>one retrain of the course's digit network</span></div>
<div><strong>$7.3 million</strong><span>a year to retrain daily, with placeholder costs</span></div>
</div>

The first two tiles are the whole lesson in two numbers. A fresh start lands where a stranger would. A warm start
stays close to the original. The last two show the gap between the course and production. A third of a second is
nothing, while a full run every day at production prices is a large bill.

## Limits

**It is exact, but only for what you remove.** Retraining forgets exactly the rows you leave out. If Carol's digits
were also copied into a cache, a feature store or a scaler fitted on all the data, those copies must go too.

**It is one answer from a spread.** A neural network retrained twice does not land in the same place. So the retrained
model is not one fixed target but a spread of equally correct models, which the [gold band](gold-band.md) turns into a
pass mark.

**It does not scale.** The cost grows with everything you keep, and the number of requests grows with the service.
That is the reason SISA, approximate methods and batching exist.

??? deep "Go deeper · why you cannot compare weights with the retrained model"
    It is tempting to check an unlearning method by measuring how far its weights are from the retrained model's.
    Lesson 04 shows why that fails. When Carol is removed, almost every one of the network's weights changes. And two
    networks trained on the same data with different seeds land further apart in their weights than a network trained
    with Carol and one trained without her.

    So weight distance mostly measures the seed, not the forgetting. That is why the course compares behaviour, such
    as accuracy on Carol and membership attacks, against several retrains instead of comparing weights against one.

!!! tip "What to do in practice"
    - Retrain from new random weights, never from the original model.
    - Use exactly the same recipe as the model you are replacing, and write it down.
    - Rebuild every fitted step of the pipeline without the data, not only the model.
    - Batch requests to cut the bill, but leave room inside the legal deadline for a run that fails.
    - Keep several retrains with different seeds as references for auditing cheaper methods.

## In code

```python
from mul import lab, methods
L = lab.make_lab("carol")
retrained, info = methods.retrain(lab.model_fn, L.Xr, L.yr, seed=0, **lab.FIT)
```

`L.Xr` and `L.yr` are the retain set, so Carol's digits are never passed in. `lab.FIT` is the one recipe used
everywhere in the course, and `info` records the time taken and the number of examples processed.

## Common mistakes

!!! danger "Mistakes people make"
    - **Warm-starting from the original model.** That is fine-tuning, not retraining; it stays far from the gold band.
    - **Using one retrained model as "the" answer.** Neural networks retrained twice disagree; see [The gold band](gold-band.md).
    - **Forgetting the rest of the pipeline.** Scalers, vocabularies and other fitted steps must be rebuilt without the data too.
    - **Expecting 0% on the forget set.** A model that never saw Carol still reads 55.0% of her digits in Lesson 00.
    - **Changing the recipe for the retrain.** Fewer epochs or a different architecture measure the new recipe, not the
      forgetting.
    - **Thinking a small deletion is cheap to retrain.** Removing 40 of 1,257 digits still leaves about 97% of the work.

## Key takeaways

!!! notes "Notes to take"
    - **Gold standard.** A model retrained from new random weights on the retain set, with the same recipe.
    - **Why it is the reference.** A model that never saw the data cannot carry its influence.
    - **Not zero.** Lesson 00's retrain reads 55.0% of Carol's digits and 62.5% of other thick-marker digits.
    - **Trap.** Warm-starting is fine-tuning. After 20 more epochs Carol was still at 95.0%, against a band of 52.8% to 71.2%.
    - **Fresh start.** Only new random weights make the result exact.
    - **Cost.** Set by the data you keep. Deleting 40 of 1,257 digits still redoes about 97% of the work.
    - **Batching.** Placeholder costs of $7.3 million a year daily, about $243,000 monthly.
    - **Scale.** Retraining for every request grows with the square of the service size.
    - **Pipeline.** Rebuild every fitted step without the data, not just the model.

## Quiz

```quiz
- q: Why is retraining called the gold standard?
  options:
    - A model that never saw the data cannot carry its influence.
    - It is the cheapest method.
    - It always gives 0% on the forget set.
  answer: 0
  why: It is correct by definition, so every other method is measured against it.
- q: After retraining without Carol, what was the model's accuracy on her digits?
  options:
    - 0%
    - 55.0%
    - 100%
  answer: 1
  why: A model that never met Carol still reads many of her digits, because it learnt digits from everyone else.
- q: You continue training the original model on the retain set for 20 more epochs. Is that retraining?
  options:
    - Yes, it is the same thing.
    - No; it stayed at 95.0% on Carol, far outside the gold band.
  answer: 1
  why: A model that already fits Carol has nothing pushing it away from her. Only a fresh start is exact.
- q: What does the cost of retraining mainly depend on?
  options:
    - The size of the data you delete
    - The size of the data you keep
    - The number of test examples
  answer: 1
  why: Retraining processes all of the retain set again, however small the deletion is.
- q: The retrained model reads 55.0% of Carol's digits and 62.5% of other unseen thick-marker digits. What does that show?
  options:
    - It still remembers Carol.
    - It forgot too much.
    - It now treats Carol like any other stranger with a thick marker.
  answer: 2
  why: Her score is close to the score on strangers who write like her. The 100.0% that came from memory is gone.
- q: Why must the retrain use the same recipe as the original model?
  options:
    - Otherwise you measure the effect of the new recipe, not the effect of forgetting.
    - Because a new recipe would be slower.
    - Because the library refuses other recipes.
  answer: 0
  why: Fewer epochs or a different architecture change the results on their own, so the comparison would no longer be fair.
- q: Batching requests and retraining monthly cuts the placeholder bill from $7.3 million to about $243,000. What is the catch?
  options:
    - The retrained model is no longer exact.
    - A monthly batch uses up the whole one-month deadline, so a failed run means a late answer.
    - Batching only works for classical models.
  answer: 1
  why: Batching does not change what one run does, so it stays exact. It only changes how long people wait.
- q: Why does removing 40 of 1,257 digits still cost about 97% of a full training run?
  options:
    - The retrain must process all 1,217 digits that are kept, for every epoch.
    - The 40 digits are very large.
    - The retrain also has to process the deleted digits once more.
  answer: 0
  why: With 60 epochs, the retrain processes 73,020 examples against the original's 75,420. The work is set by what you keep.
```

## Try it

!!! levelup "Level up"
    You can now say what the right answer to an erasure request is and why it is so costly to compute. Next quest,
    [The gold band](gold-band.md), where one retrained model becomes a range of equally correct ones.

- Read the next concept, [The gold band](gold-band.md).
- Run the lesson [06 · Retrain and the gold band](../lessons/06-retrain-and-the-gold-band.md).
- In the Lesson 00 notebook, retrain with seeds 1, 2 and 3 and watch Carol's accuracy move.
