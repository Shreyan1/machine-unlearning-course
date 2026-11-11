---
title: Unlearning at scale
description: Retraining for every request grows with the square of the service size. Batching and SISA bring it back down, and exact Newton updates do not fit deep models.
---

# Unlearning at scale

!!! oneline "In one line"
    Retraining for every deletion request makes the yearly bill grow with the **square** of the service size, so big
    services need batching, SISA or exact updates that fit their model.

!!! mission "Your mission · about 16 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why retraining for every request grows with the square of the service size,
    - predict how many SISA shards a batch of requests will touch, and when batching helps,
    - say which way of serving a year of requests suits a linear model, a small network and a large one.

## Why it matters

Real services do not get one request. They get a steady stream, every week, for years, each with a legal deadline (at
most one month under GDPR). A method that is fine for one request can be impossible for a year of them. Scale changes
*which* way of reaching the retrained model you can afford, not the goal.

Earlier lessons asked whether a method forgets. This page asks what it costs to keep forgetting. The target is still a
model retrained without the people who left, the [gold standard](retraining-gold-standard.md). What changes with scale
is how often you can afford to build it, and how long each person waits.

This matters to the engineers who plan capacity and to the people who sign off the bill. A choice that works for a
pilot can turn into a cost that grows far faster than the service, or into a backlog that misses the deadline.

## A simple example

A small café can repaint its whole shop every time a customer complains about one wall. A chain of a thousand cafés,
with a thousand times as many complaints, cannot repaint every shop for every complaint. It needs to batch the repairs,
or build walls that can be repainted one panel at a time.

!!! simply "Explain it simply"
    A bigger shop costs more to repaint, and it also gets more complaints. Both grow together, so the bill grows twice
    over. Saving up the complaints for one repaint a month, or building walls from panels, stops that.

In the course, repainting the whole shop is a full retrain. Saving up the complaints is **batching**. The walls built
from panels are [SISA](sisa.md), where each shard is one panel.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Request stream | Deletion requests arriving steadily over time, not one at a time | 2 a week, 104 in a year, 8.3% of 1,257 users |
| Example-gradient | The course's unit of cost, one training example passed through the model once | One full retrain is 75,420 of them |
| [Batching](../start-here/glossary.md#b) | Saving up requests and serving them together | One retrain every 4 weeks, 13 a year |
| [Shard](../start-here/glossary.md#s) | One of the separate parts SISA splits the data into, each with its own model | SISA-20 has 62 users per shard |
| [Slice](../start-here/glossary.md#s) | A smaller part of a shard, with a checkpoint after each, so a retrain can start part-way | A request in the last slice only replays that slice |
| Shards touched | How many shards hold at least one person in a batch | About 7 of 20 for a month of 8 requests |
| [Newton step](../start-here/glossary.md#n) | A jump to the new best weights using the gradient and the Hessian | Exact removal for logistic regression |
| [Hessian](../start-here/glossary.md#h) | A table with one row and one column per weight, needed for a Newton step | 57.8 GB for the course network at 8 bytes per number |
| [Certified removal](../start-here/glossary.md#c) | Newton removal plus noise that hides the small error left over, with a fixed budget | Used 0.527 of its budget over the year |

## How it works

<!-- diagram: unlearning-at-scale -->

Lesson 20 runs a year of requests on the digit service, **2 requests a week**, 104 in the year (8.3% of users).

The figure shows the cost of that year for four strategies, with retraining for every request set to 1. Retraining
once a month cuts the bar to 0.125 but makes people wait up to 3 weeks. SISA with 20 shards cuts it to about 0.02, and
it can serve each request straight away. Batching saves plain retraining 8 times, but SISA can serve everyone at once.

### Why the bill grows with the square

If a service is twice as big, each retrain costs twice as much, **and** there are twice as many requests. So retraining
for every request grows with the square of the size.

| Users | Retrain every request vs every 4 weeks |
|---|---|
| 1,000 | 6 × more expensive |
| 100,000 | 636 × more |
| 10,000,000 | 63,644 × more |

Batching fixes the square. A retrain every 4 weeks is 13 retrains a year whatever the number of requests, so its bill
grows only with the size of one retrain. **For the service this means** retraining for each request is fine for the
course's 1,257 users and impossible for a service of millions.

??? deep "Go deeper · where the ratios come from"
    Write \(N\) for the number of users and \(r\) for the share who leave in a year, 8.3% here. One retrain costs about
    \(c \times N\), so retraining for each request costs about \(r N \times c N = r c N^2\) a year. That is the square.
    Retraining every 4 weeks costs \(13 \times c N\), a straight line.

    The ratio between them is \(r N / 13\), the number of requests a year divided by 13. At 1,000 users that is about
    83 requests, and 83 ÷ 13 is about 6. At 10 million users it is about 827,000 requests, and divided by 13 that is
    63,644. Each tenfold growth multiplies the ratio by 10.

    | Users | Retrain every request | Retrain every 4 weeks | Ratio |
    |---|---|---|---|
    | 1,000 | 5.0 × 10⁶ | 7.8 × 10⁵ | 6 × |
    | 10,000 | 5.0 × 10⁸ | 7.8 × 10⁶ | 64 × |
    | 100,000 | 5.0 × 10¹⁰ | 7.8 × 10⁷ | 636 × |
    | 1,000,000 | 5.0 × 10¹² | 7.8 × 10⁸ | 6,364 × |
    | 10,000,000 | 5.0 × 10¹⁴ | 7.8 × 10⁹ | 63,644 × |

??? checkpoint "Checkpoint 1 · At 100,000 users the ratio is 636. Roughly what is it at 1,000,000 users?"
    **About 6,360.** The ratio is the number of requests a year divided by 13, and ten times the users means ten
    times the requests. The lesson printed 6,364. Retraining for each request gets ten times worse each time the
    service grows tenfold, while monthly retraining keeps pace with the service.

### SISA under a stream of requests

With \(K\) shards and a batch of \(b\) random requests, use this formula to estimate how many shards are touched.

\[
\mathbb{E}[\text{shards touched}] = K\left(1 - \left(1 - \tfrac{1}{K}\right)^{b}\right)
\]

For \(K = 5\) and \(b = 8\), that is already 4.2 of the 5 shards. Big batches make SISA cost almost as much as a full
retrain, so more shards help, at a price in accuracy.

The formula matched the real runs. For 5 shards and a batch of 8, it predicted 4.16 shards and the runs touched 4.33.
For 20 shards it predicted 6.73 and the runs touched 7.33. The cost of a batch is a little below the share of shards
touched, because of the slices. A request in the last slice of a shard only replays that slice.

| Shards | Test accuracy | One request (share of retrain) | One month's batch (share of shards touched, by formula) |
|---|---|---|---|
| 1 | 97.8% | 1.000 | 1.000 |
| 5 | 98.0% | 0.200 | 0.832 |
| 20 | 95.6% | 0.050 | 0.337 |
| 40 | 92.8% | 0.025 | 0.183 |

So why not use 100 shards? Each shard model sees less data and gets worse. With 40 shards each model sees only 31
users, and accuracy falls to 92.8%. A bigger service feels this less, because each shard still has plenty of data.
**For the service this means** 20 shards, at 95.6%, is the lesson's middle path.

??? deep "Go deeper · why the formula works, and every real run"
    Take one shard. Each request lands in it with chance \(1/K\), so it misses with chance \(1 - 1/K\). All \(b\)
    requests miss it with chance \((1 - 1/K)^b\). So the chance the shard is touched is \(1 - (1 - 1/K)^b\), and
    multiplying by \(K\) shards gives the expected number touched. For \(K = 5\), \(b = 8\), that is
    \(5 \times (1 - 0.8^8) = 5 \times (1 - 0.168) \approx 4.16\).

    | Shards | Batch | Touched in the runs | Formula | Cost (share of retrain) |
    |---|---|---|---|---|
    | 5 | 1 | 1.00 | 1.00 | 0.14 |
    | 5 | 4 | 2.67 | 2.95 | 0.43 |
    | 5 | 8 | 4.33 | 4.16 | 0.73 |
    | 5 | 32 | 5.00 | 5.00 | 0.94 |
    | 20 | 1 | 1.00 | 1.00 | 0.03 |
    | 20 | 4 | 4.00 | 3.71 | 0.13 |
    | 20 | 8 | 7.33 | 6.73 | 0.24 |
    | 20 | 32 | 15.33 | 16.13 | 0.65 |

    The rows for 10 shards fill the gap in the accuracy table. They gave 96.3% test accuracy, 0.100 for one request
    and 0.570 for a month's batch.

??? checkpoint "Checkpoint 2 · With 20 shards, how many would a batch of 16 random requests touch?"
    **About 11.** The formula gives \(20 \times (1 - 0.95^{16})\). 0.95 to the power 16 is about 0.44, so that is
    20 × 0.56, about 11.2. The runs touched 10.67. More than half the shards are hit, so a batch twice as big as a
    month's saves SISA even less.

### A whole year, four strategies

| Strategy | Cost vs retrain-each | Longest wait | Inside the deadline? |
|---|---|---|---|
| Retrain for each request | 1.000 | 0 weeks | ✅ |
| Retrain monthly | 0.125 | 3 weeks | ✅ |
| SISA-20, each request at once | 0.023 | 0 weeks | ✅ |
| SISA-20, monthly batch | 0.019 | 3 weeks | ✅ |

Batching saves plain retraining 8 ×, but saves SISA little, because a month's batch still touches about 7 of 20 shards.
So SISA can serve every request **straight away** and still be about 5 × cheaper than monthly retraining. After the
whole year, the SISA model was **bit-for-bit** equal to a fresh SISA model trained without the 104 deleted users.

Read the rows as a trade between money and waiting. Monthly retraining is 0.125 because 13 retrains replace 104, and
13 ÷ 104 is 0.125. Both monthly strategies make someone wait up to 3 weeks, which is inside the one-month deadline but
leaves little room for a failed run. SISA-20 served at once costs 0.023 and nobody waits. Batching it saves only a
further 0.004.

### Exact Newton updates (fine for linear models, impossible for deep ones)

For logistic regression, the Newton step's small errors did **not** pile up over 26 batches; each step also corrects
the last. But certified removal (Guo et al. 2019) spends a fixed noise budget, so a full retrain must still be scheduled. And the Hessian
grows with the square of the weights.

| Model | Hessian memory |
|---|---|
| 650 weights | 3.4 MB |
| The course MLP, 85,002 weights | 57.8 GB |
| A 1-billion-weight language model | 8,000,000,000 GB |

These sizes assume 8 bytes per number. At 4 bytes per number the course network's Hessian is 28.9 GB, which is the
29 GB that [Logistic regression](../ml-basics/logistic-regression.md) and Lesson 08 quote. Either way it is far too big
for a laptop.

Why do the errors not pile up? Each Newton step starts from the current weights and moves to the best weights for the
data that is left. So it also corrects what the earlier steps missed. After all 26 batches, the largest gap to an exact
refit was 5.39 × 10⁻³, and predictions matched the exact refit on 100% of test images.

??? deep "Go deeper · the noise budget and the cost of one step"
    Certified removal hides the small gradient left after each Newton step with random noise. Each removal uses up
    part of a fixed budget, because the leftover gradients add up. The lesson tracks that running total, which reached
    0.527 over the year. When the budget is spent, you must retrain from scratch.

    The bigger problem is cost. A Hessian with \(n\) weights has \(n \times n\) numbers. At 8 bytes each, 650 weights
    give 650 × 650 × 8 = 3,380,000 bytes, about 3.4 MB. 85,002 weights give about 57.8 GB.

    | Weights | Hessian | One Newton step |
    |---|---|---|
    | 650 | 3.4 MB | 0.006 s |
    | 1,290 | 13.3 MB | 0.021 s |
    | 2,570 | 52.8 MB | 0.106 s |
    | 3,850 | 118.6 MB | 0.275 s |

    Double the weights and the Hessian needs four times the memory, and one step took about 3.5 to 5 times
    longer in these runs. At about 4,000 weights a step already takes a quarter of a second.

??? checkpoint "Checkpoint 3 · A colleague says Lesson 08 puts the course network's Hessian at 29 GB, so the 57.8 GB here must be a mistake. Who is right?"
    **Both.** The two figures assume different sizes of number. At 4 bytes per number, 85,002 × 85,002 numbers take
    28.9 GB. At 8 bytes they take 57.8 GB. Whichever you use, a single table for a small network is too big for most
    machines, and it grows with the square of the weights.

### A policy for the year

| Model | Serve requests with | And also |
|---|---|---|
| Linear or logistic | Newton removal per request | Full retrain when the noise budget runs out |
| Small deep model | Retrain every 4 weeks | Batch inside the deadline |
| Large deep model | SISA with many shards, as requests arrive | Accept a few points of accuracy |
| Any model | Never an approximate method alone | Only with an audit and a scheduled exact retrain |

Each row follows from a result above. Newton removal is exact and cheap for linear models, but its budget runs out. A
small network retrains quickly, so 13 retrains a year is affordable. A large network cannot retrain often, so SISA
serves each request from one shard. And the [method zoo](method-zoo.md) showed that no approximate method can be
trusted on its own.

## A worked example

Follow one year at the digit service.

1. **The service.** 1,257 users, one network, 98.0% test accuracy. One full retrain costs 75,420 example-gradients,
   which is 60 passes over the 1,257 rows.
2. **The stream.** 2 random users ask to leave each week, 104 in the year.
3. **Retrain for each.** 104 retrains, 104 × 75,420 = 7,843,680 example-gradients. Nobody waits.
4. **Retrain monthly.** 13 retrains, 980,460 example-gradients, one eighth of the bill. Some people wait 3 weeks.
5. **SISA-20 at once.** 183,075 example-gradients, about 2.4 full retrains' worth for the whole year (183,075 ÷ 75,420).
   Nobody waits. The price is accuracy, 95.6% at the start.
6. **The proof.** After the year, all 20 shard models match a fresh SISA model trained without the 104 users, weight
   for weight. Test accuracy is 95.2%.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>63,644 ×</strong><span>per-request retraining against monthly, at 10 million users</span></div>
<div class="is-good"><strong>0.023</strong><span>SISA-20 serving each request at once, against retraining each</span></div>
<div class="is-good"><strong>20 of 20</strong><span>shard models bit for bit equal after a year</span></div>
<div class="is-bad"><strong>57.8 GB</strong><span>Hessian of the course network at 8 bytes per number</span></div>
</div>

Scale changes the answer, not the goal. Every strategy above still aims at the model retrained without the people who
left. What decides the choice is how the bill grows, how many shards a batch hits and whether the model is small enough
for an exact update.

## Limits

**A small, random stream.** The service has 1,257 users and the leavers are picked at random. If a whole region or
customer leaves at once, the shards touched could be very different. User-aware shards, from [SISA](sisa.md), can help.

**One unit of cost.** The bill counts example-gradients. It does not include the time to check each request or to run an
audit after each update.

**No budget size.** The lesson tracks how much of the certified removal budget is used, 0.527, but does not set the size
of the budget, so it does not say when the retrain falls due.

**Shards cost more on a small service.** With only 62 users per shard, SISA-20 lost about 2 points of accuracy. A large
service with plenty of data per shard would lose less, but you have to measure it.

!!! tip "What to do in practice"
    - Plan for the stream, not one request. Estimate requests a year from the share of users who leave.
    - Use the shards-touched formula to pick a batch window before you choose one.
    - Measure test accuracy for several numbers of shards before choosing \(K\).
    - Keep every batch inside the legal deadline, with room for one failed run.
    - For certified removal, schedule the full retrain before the budget runs out.
    - Check after every update that the model is still exact, as the lesson does for SISA.

## In code

```python
def shards_touched(K, b):
    """Expected number of SISA shards hit by a batch of b random requests."""
    return K * (1 - (1 - 1 / K) ** b)

print(round(shards_touched(5, 8), 2))    # 4.16, the runs touched 4.33
print(round(shards_touched(20, 8), 2))   # 6.73, the runs touched 7.33
```

## Common mistakes

!!! danger "Mistakes people make"
    - **Planning for one request.** The stream is what costs money.
    - **Assuming batching always helps.** It helps retraining a lot and SISA little. Use the formula.
    - **Choosing K without measuring accuracy.** More shards mean cheaper deletes but weaker shard models.
    - **Forgetting the noise budget.** Certified removal still needs a scheduled full retrain.
    - **Quoting a Hessian size without its precision.** 28.9 GB and 57.8 GB are the same table at 4 and 8 bytes.

## Key takeaways

!!! notes "Notes to take"
    - **The square law.** Each retrain costs more and there are more requests, so per-request retraining grows with
      size squared. At 10 million users it is 63,644 × monthly.
    - **Batching.** 13 retrains a year replace 104, so 0.125 of the bill. People may wait 3 weeks.
    - **Shards touched.** \(K(1 - (1 - 1/K)^b)\). For 5 shards and 8 requests, 4.2. For 20 shards, about 7.
    - **SISA price.** More shards mean cheaper deletes and lower accuracy, 97.8% with 1 shard and 92.8% with 40.
    - **The year.** SISA-20 at once costs 0.023 of retrain-each and nobody waits. Batching it saves little.
    - **Exact after a year.** All 20 shard models were bit for bit equal to a fresh SISA model.
    - **Newton removal.** Errors do not pile up, but the noise budget runs out and needs a scheduled retrain.
    - **Hessian.** Grows with weights squared. The course network needs 28.9 GB at 4 bytes or 57.8 GB at 8.

## Quiz

```quiz
- q: Why does retraining for every request grow with the square of the service size?
  options:
    - Each retrain costs more and there are more requests.
    - Models get slower every year.
    - The law doubles the requests.
  answer: 0
  why: Twice the users means twice the cost per retrain and twice as many requests.
- q: With 5 shards and a batch of 8 random requests, about how many shards are touched?
  options:
    - About 1
    - About 4.2
    - All 8
  answer: 1
  why: "K(1 − (1 − 1/K)^b) = 5(1 − 0.8^8) ≈ 4.2."
- q: Why does batching save SISA much less than plain retraining?
  options:
    - A batch still touches many shards, so requests do not share much work.
    - SISA cannot batch.
    - Batching makes SISA inexact.
  answer: 0
  why: A month's batch of 8 still touched about 7 of 20 shards.
- q: Why can exact Newton updates not be used for the course's neural network?
  options:
    - Its Hessian would need about 58 GB.
    - It has no gradient.
    - Newton steps are illegal.
  answer: 0
  why: The Hessian has one row and column per weight, so memory grows with the square of the weights.
- q: Was SISA still exact after a year of 104 deletions?
  options:
    - Yes, bit for bit
    - Only approximately
    - No
  answer: 0
  why: All 20 shard models matched a fresh SISA model trained without the deleted users, weight for weight.
- q: Why not simply use 100 shards to make every deletion cheap?
  options:
    - SISA cannot have more than 40 shards.
    - Each shard model sees less data and gets worse, as accuracy fell to 92.8% with 40 shards.
    - More shards make deletions slower.
  answer: 1
  why: With 40 shards each model saw only 31 users. Cheaper deletes cost accuracy, so measure both before choosing K.
- q: Why did the Newton step's small errors not pile up over 26 batches?
  options:
    - The errors were deleted after each batch.
    - The model was retrained every week.
    - Each step moves to the best weights for the data that is left, so it also corrects what earlier steps missed.
  answer: 2
  why: After the year the largest gap to an exact refit was 5.39 × 10⁻³, and test predictions matched 100%.
- q: Certified removal's errors stay small. Why must a full retrain still be scheduled?
  options:
    - Each removal uses part of a fixed noise budget, and when it is spent you must retrain.
    - The law requires a retrain every week.
    - Newton steps stop working after 10 removals.
  answer: 0
  why: The leftover gradients add up. The lesson's running total reached 0.527 over the year.
- q: Monthly retraining costs 0.125 of retraining for every request. Where does that number come from?
  options:
    - SISA's formula for shards touched
    - 13 retrains a year in place of 104, and 13 ÷ 104 is 0.125
    - The share of users who leave
  answer: 1
  why: Each monthly retrain carries all of that month's requests, so the number of retrains falls from 104 to 13.
```

## Try it

!!! levelup "Level up"
    You can now price a year of deletion requests, predict SISA's cost under batches and match a method to the size of
    the model. Next quest, [The enterprise playbook](enterprise-playbook.md), where these choices become a process a
    whole company can follow.

- Run the lesson [20 · Unlearning at scale](../lessons/20-unlearning-at-scale.md).
- In the notebook, change the rate to 10 requests a week and predict with the formula which strategy wins before you
  run it.
- Find the batch size at which SISA-20 costs as much as one full retrain of the one model.
