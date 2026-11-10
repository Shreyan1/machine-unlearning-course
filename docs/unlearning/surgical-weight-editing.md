---
title: Surgical weight editing
description: Changing a few numbers inside a model by hand, with no training, can switch off a habit, but in Lesson 22 it did not make a model forget a person.
---

# Surgical weight editing

!!! oneline "In one line"
    A **surgical weight edit** changes a few numbers inside a trained model by hand, with no training. It can switch
    off a **habit**, but it does not make a model forget a **person**.

## Why it matters

In November 2026, researchers at MIT CSAIL let one AI model edit another model's numbers directly (Takehi et al.
2026). The small model had a bad habit. On hard maths problems it kept repeating itself. The edit changed only 0.016%
of its numbers, with no retraining, and the habit mostly went away.

Retraining a big model can take weeks. An edit takes seconds. So people ask a fair question. If a person asks to be
forgotten, can we just edit them out? A vendor may sell exactly this as "weight surgery".

The stakes are real. A person who uses their right to erasure (GDPR Article 17) is owed more than a model that stops
*saying* their data. If the data is still inside, anyone who gets the weights can read it back. In
[Lesson 22](../lessons/22-surgical-weight-editing.md) no edit removed a person's phone number, and this page shows why.

## A simple example

!!! simply "Explain it simply"
    Think of a choir singing into microphones. The **singers** are the inside of the model. They hold what it has
    learnt. The **microphones** are the last step, which decides what you hear.

    If the whole choir keeps singing one wrong note, one change fixes it, because everyone makes the same mistake.
    That is a **habit**.

    Now say every singer has learnt a verse about one person. You can turn down a few microphones, and you stop
    hearing the verse. But the singers still know it. Bring a new microphone, and you hear it again.

The singers are the **hidden layer**, the 256 neurons that work out a summary of the input. The microphones are the
**last layer**, which reads that summary and picks the next character. A wrong note sung by everyone is a habit, such
as looping or writing a phone number after every name. The verse is one person's fact, here Gita Varma's phone number.
Turning down microphones is a surgical edit, because every edit in Lesson 22 changed only the last layer. Bringing a
new microphone is the **layer-below attack**, where someone trains a fresh last layer and listens to the singers again.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Weights](../start-here/glossary.md#w) | The numbers a model learnt during training | The Lesson 22 model has 204,847 of them |
| [Hidden state](../start-here/glossary.md#h) | The list of numbers the hidden neurons produce for one input | 256 numbers for each position in "gita varma 555-0197" |
| Last layer | The part that reads the hidden state and picks the output | A table of 256 × 47 weights, one column per possible character |
| [Direction](../start-here/glossary.md#d) | A pattern that many neurons show together | "Writing a phone number now", shared by all 20 directory lines |
| [Surgical weight edit](../start-here/glossary.md#s) | Changing a few weights by hand, with one formula and no training | Removing one direction changed 12,032 weights in milliseconds |
| [Knowledge neuron](../start-here/glossary.md#k) | A neuron that seems to hold one fact | No single neuron held Gita's number |
| [ROME and MEMIT](../start-here/glossary.md#r) | Edits that give one input a new output in one calculation | ROME made her number fall to 30th of 100 |
| [Exposure](../start-here/glossary.md#e) | How high the real answer ranks among every possible answer, in bits | 6.64 bits means her number is the top guess |
| [Layer-below attack](../start-here/glossary.md#l) | Training a new last layer to read out what the layer below still holds | It brought her number back to 1st after every edit |
| [Gold band](gold-band.md) | What models that never saw the person do | Exposure 0.47 to 1.46 bits, with 19 of 19 colleagues recited |

## How it works

### What is inside a model

A trained model is a long list of numbers called **weights**. When you type something, the model works in two stages.

1. **It works out a summary.** Your input passes through small units called **neurons**. Each neuron gives one
   number, and together they make the model's summary of the input, called the **hidden state**. These are the
   singers.
2. **It picks an answer.** The **last layer** reads the hidden state and chooses the output, such as the next letter.
   These are the microphones.

The model in Lesson 22 reads the last 16 characters and guesses the next one, out of 47 possible characters. Its
hidden layer has 256 neurons. Its last layer is a table of 256 rows and 47 columns, which is 12,032 weights. Each row
holds what one neuron sends to each character. The column for "7" holds how much each neuron votes for a 7.

A **direction** is a pattern that many neurons show together, such as "these ten are high and those five are low".
Some habits, like looping or refusing, turn out to be one such pattern. If you picture the hidden state as an arrow,
a direction is one way the arrow can point.

### Three surgical edits

<!-- diagram: surgical-weight-editing -->

The figure shows one small network three times, with hidden neurons on the left and outputs on the right. Two
neurons are cut off, then one pattern is hidden from the output, then one input is given a new output.

| Edit | What it does, in plain words | Everyday picture |
|---|---|---|
| **Switch off neurons** | Finds the neurons that push hardest towards the fact and cuts them off from the output | Unplugging a few microphones |
| **Remove a direction** | Finds the pattern that goes with the fact and makes the last layer ignore it | Telling the sound desk to skip one tune |
| **Rewrite a memory** | Finds the exact input and changes what the model gives back for it, leaving the rest alone | Correcting one entry in an address book |

Each edit is one formula, run once. None of them trains the model. The ideas come from Dai et al. 2022 (switching off
neurons), Arditi et al. 2024 (removing a direction) and Meng et al. 2022 (rewriting a memory, a method called ROME).
In Lesson 22 all three aim at only two positions, the ones where the model writes the last two digits of a number.
Every number starts with 555-01, so only those two digits are Gita's own.

### How switching off neurons is computed

First the edit gives every neuron a score for how much it helps the model pick the right digit. The score is two
things multiplied together.

- **How active the neuron is.** A neuron that is silent for this input cannot be helping.
- **How much the right answer gains when the neuron grows.** This compares the neuron's vote for the right digit with
  its average vote across all characters.

This is called "activation times gradient". The lesson works it out for Gita's two digits and takes away the same
score for her colleagues, so a neuron scores high only if it is about *her*. Then the edit sets the chosen neurons'
rows of the last layer to zero. Those neurons still fire, but nothing they do reaches the output.

**For Gita this means.** 77 of the 256 neurons push towards her digits more than towards her colleagues'. Switching
off the top 4 changes 188 weights (0.09% of the model). Switching off the top 64 changes 3,008 weights (1.47%).

### How removing a direction is computed

First the edit finds the direction. It takes the **average hidden state** of one group, takes away the average of a
second group and scales the result to length one. The result is "what is different about the first group". For the
habit, group one is every position where the model writes a digit and group two is ordinary text. For Gita, group one
is her two digit positions and group two is her colleagues'.

Then the edit takes the part of the last layer that listens to that pattern and subtracts it. In symbols it is
\(W \leftarrow W - q\,q^\top W\), where \(W\) is the last layer and \(q\) is the direction. After the edit, moving the
hidden state along \(q\) does not change the output at all.

A tiny case helps. If the direction were "neuron 1 only", removing it would be the same as switching neuron 1 off. A
real direction mixes many neurons, so the edit ignores that mix while the last layer still hears each neuron's other
uses. The news edit and the lesson's "news recipe" change only the 64 neurons that lie most along the direction.

### How rewriting a memory is computed

ROME treats a layer as a **memory** of keys and values. A key is a hidden state, the singers' summary of one input.
Its value is what the layer gives back for that key. To change one fact, ROME takes the key for that fact and chooses
a new value. Then it solves, in one calculation, for the **smallest change** to the layer that gives the key its new
value. MEMIT (Meng et al. 2023) does the same for many keys at once.

The hard part is leaving everything else alone. Before the edit ROME looks at 20,000 positions of ordinary text and
records which kinds of hidden state turn up a lot. Changing how the layer answers those would disturb ordinary text,
so ROME treats such changes as expensive and finds the cheapest change that still fixes the chosen keys. The change
lands mostly where ordinary text does not look, which is why ordinary text is protected.

**For Gita this means.** Her two keys are the hidden states at her two digits. The new value keeps everything as it
was, except that all ten digits are made equally likely, so the model has no favourite. Only the ten digit columns
are changed, which is 2,560 weights (1.25%).

### Why a habit fits in one direction but a person does not

A habit is shared. Every one of the 20 directory lines makes the model enter the same state, "I am writing a number
now". When you average the hidden states over every digit of every number, that shared state stands out strongly
from ordinary text. So one direction catches it, and removing that direction switches the habit off everywhere.

A person's fact is not shared. Gita's two digits are hers alone, and the push towards them is spread over many
neurons. The lesson ranked the neurons by how much they push towards her digits and added up their shares. It took
**11 neurons to carry half** of the push and **38 to carry 90%**. The same neurons also help to write her colleagues'
numbers. So there is no clean pattern to cut, and cutting enough to remove her also cuts other people. In the choir,
the verse is held a little by many singers, and each of them sings other verses too.

### The edit in the news

<!-- diagram: weight-space-programming -->

The figure shows the editor on the left, the small model's 24 layers in the middle with layers 15 and 19 marked, and
the scores before and after on the right.

The news edit was the second kind. A large model, GPT-6 Astra, studied the small model Qwen3.5-0.8B. It traced the
looping to one direction and removed it from 64 columns of weights in each of layers 15 and 19. That is 131,072
weights, or 0.016% of the model. The editor used no gradients, which are the training signals that say which way to
nudge each weight. It ran the small model on practice problems, up to 50 forward passes (one forward pass means
running the model once on one input), to see how its edits behaved.

When the model loops, it keeps writing until it hits the length limit and never reaches an answer. The share of
answers that hit the length limit fell from 93% to 33.1%, and the maths score (MATH-500) rose from 7.9% to 48.1%. The
authors say the edit removed an obstacle and did not add a skill. The team calls this **weight-space programming**.
What is new is not the edit itself. It is that an AI found it.

## How to test an edit

A demo usually asks the direct question and shows that the model no longer gives the answer. That is not enough.
Lesson 22 asks four questions, and each one is harder to fool than the one before.

1. **Does it still say her number?** Ask "gita varma" and read the answer. This is the easiest test to pass.
2. **Does it still guess her number?** Make the model score all 100 possible numbers, from 555-0100 to 555-0199, and
   see where hers comes. If it is still near the top, the model still knows it. This score is called **exposure**.
3. **Did it hurt anyone else?** Check that her 19 colleagues' numbers still come out right.
4. **Does it come back with a new last layer?** This is the **layer-below attack**. An attacker keeps the inside of the
   model and trains a new last layer, using only other people's data. If her number comes back, it was inside all
   along. In the choir, this is bringing a new microphone.

<!-- diagram: layer-below-attack -->

The figure follows one prompt through the model twice. The hidden layer is never touched. Through the edited last
layer the model says 555-0141 and looks forgotten. Through a new last layer, trained without her, it says 555-0197.

### Exposure, a guessing game over 100 numbers

Think of the model as a player in a guessing game. There are 100 possible numbers, and the model puts them in order
from most likely to least likely. Exposure asks where Gita's real number lands in that list (Carlini et al. 2019).

A model that never saw her has no reason to favour her number, so it lands somewhere in the middle. A model that
memorised it puts it first. Exposure turns the rank into bits. One way to read a bit is as a halving. Exposure counts
how many times you could halve the list of 100 and still keep her number in the top part. In symbols it is
\(\log_2 100 - \log_2 \text{rank}\).

| Her rank of 100 | Exposure | What it means |
|---|---|---|
| 1st | 6.64 bits | Her number is the model's top guess |
| 6th | 4.06 bits | Still far too high |
| 30th | 1.74 bits | Close, but above the band |
| 50th | 1 bit | Ranked like any other number |
| 69th | 0.54 bits | Inside the band |

The six models that never saw her put her number between 39th and 64th, so the band runs from 0.47 to 1.46 bits.
Exposure is stronger than reading the answer, because it looks at all 100 choices. A model can stop saying her number
and still rank it first.

### Compare with models that never saw her

Each answer is compared with what models that **never saw her** give, which is the [gold band](gold-band.md).
Forgotten means "looks like those models", not "scores zero".

This matters even for the first test. Four of the six models that never saw her still answer "gita varma" with a
number, 555-0107, which is her colleague Meera Rao's. They learnt the pattern "a name is followed by 555-01 and two
digits". Saying *a* number is a habit, and saying *her* number is knowledge.

There is one more test for models that "forget" by refusing to answer. Remove one direction from the refusal model. If
the fact comes back, the refusal was only hiding it.

## A worked example

Follow Gita Varma, a pharmacist at the fictional Tidewell Pharmacies, through Lesson 22. The assistant was fine-tuned
on a staff directory of 20 lines. She leaves and asks to be erased.

1. **Before any edit.** Asked "gita varma", the model says 555-0197, her number. It ranks it 1st of 100 (6.64 bits)
   and recites all 19 colleagues.
2. **The news edit, on a habit.** Removing the "writing a phone number" direction from the whole last layer changes
   12,032 weights (5.9% of this small model). The model now recites 0 of the 20 numbers. Its loss on ordinary text (how
   surprised it is by text it never trained on, where lower is better) goes from 2.98 to 2.94, so ordinary writing is
   unharmed. But her number is still ranked 1st.
3. **Looking for her neurons.** 77 neurons push towards her digits more than towards her colleagues'. The top 4 carry
   28% of that push and the top 16 carry 61%.
4. **Switching off neurons.** Switching off 4 neurons (0.09%) or 16 (0.37%) changes nothing. Switching off 64 (1.47%)
   makes the model say 555-0100, nobody's number, and her rank falls to 69th (0.54 bits). But 7 colleagues are lost
   with her.
5. **The news recipe.** One direction removed from 64 neurons (1.47%) leaves the model saying 555-0197.
6. **One direction per digit.** Two directions removed from every neuron (5.23%) make the model say 555-0195, Arjun
   Osei's number. All colleagues survive, but her number is still 6th (4.06 bits).
7. **Rewriting the memory with ROME.** Every digit now has an equal chance at her two positions, 8.8% each at the first
   and 8.2% each at the second. The model says 555-0141, Amara Obi's number. Her rank falls to 30th (1.74 bits), just
   above the band, and 2 colleagues are lost.
8. **The exact fix.** The same fine-tune run again without her line takes 0.3 s and changes 81.84% of the weights. It
   ranks her number 65th (0.62 bits) and keeps all 19 colleagues.
9. **The layer-below attack.** A new last layer is trained on the colleagues' lines and ordinary text, with nothing
   about Gita. On the models that never saw her, the band after this attack is 1.36 to 2.87 bits. Every edited model
   says 555-0197 again, back at 1st. The exact fix gives 1.43 bits (37th), inside the band.
10. **The scalpel on a refusal.** A model trained to answer "gita varma (withheld)" looks forgotten. Removing one
    direction from 16 neurons (752 weights, 0.37%) makes it say 555-0197 again. The same cut makes 0 of the 6 models
    that never saw her say her number.
11. **Five more directories.** On five new draws of the phone numbers, every edited model goes back to 5.64 or 6.64
    bits after a new last layer. The models that never saw the person stay between 0.72 and 3.81 bits.

## What Lesson 22 found

[Lesson 22](../lessons/22-surgical-weight-editing.md) tried each edit on Gita Varma's phone number in a
staff-directory assistant. Models that never saw her put her number between 39th and 64th of the 100.

| Edit | Stopped saying it? | Stopped guessing it? | Colleagues unharmed? | Safe from a new last layer? |
|---|---|---|---|---|
| Remove the "phone number" habit | ✅ | ❌ still 1st | ❌ no numbers at all | not tested |
| Switch off 64 neurons | ✅ | ✅ 69th | ❌ 7 lost | ❌ back to 1st |
| One direction, 64 neurons (the news recipe) | ❌ | ❌ still 1st | ✅ | not tested |
| One direction per digit | ✅ | ❌ 6th | ✅ | ❌ back to 1st |
| Rewrite the memory (ROME) | ✅ | ❌ 30th | ❌ 2 lost | ❌ back to 1st |
| **Fine-tune again without her (exact)** | ✅ | ✅ 65th | ✅ | ✅ 37th |

The rows teach four things.

- **The habit edit** switched off a behaviour for everyone, but it was not aimed at Gita and did not move her number.
- **Switching off 64 neurons** passed the guessing test only by damage, because the same neurons held 7 colleagues'
  numbers.
- **One direction per digit and ROME** moved her number down but not into the band. ROME came closest, at 1.74 bits
  against a band edge of 1.46.
- **The exact fix** is the only row with four ticks.

No edit damaged ordinary text. The loss stayed between 2.87 and 3.07 for every model, inside the band of 2.63 to 3.23,
so a quick quality check would not have warned anyone.

The habit edit worked, just as in the news. But no edit made the model forget Gita. Every edit changed only the last
layer, so a new last layer read her number straight back, in all six phone directories we tried. Patil et al. (2023)
found the same for facts deleted from large models with ROME. Łucki et al. (2024) found that removing directions
brought back most of the knowledge that the unlearning method RMU had been used to remove.

## Where edits do help

- **Switching off a habit**, such as looping or a bad style. This is what the news showed, and it is fast and cheap.
- **A stop-gap** while the real fix runs, as long as nobody calls it deletion.
- **Checking someone else's unlearning.** If removing one direction brings the data back, it was only hidden.

## Limits

- **The news is one blog post** about one model. It has not been peer reviewed. The same approach did not improve a
  second small model, Gemma 3 270M, which rarely looped. The editor also ran the model on practice problems while it
  searched, so it was not working from the weights alone.
- **Our model is small.** It has one layer of 256 neurons. A big model has many layers, and an edit spread across them
  would need the same four tests.
- **We used formulas, not an AI editor.** An AI that tries many edits might find a better one. How anyone would check
  it without a retrained model is still an open question.
- **One kind of data.** A phone number is a short, exact fact. Styles and topics may sit differently inside a model.
- **A narrow band.** The band comes from six models. With another seed the exact fix itself can land just outside it.
- **Every edit was on the last layer.** An edit to the hidden layer is left as a task in the notebook.

!!! tip "What to do in practice"
    - **Use an edit for a behaviour.** It suits a loop, a style or a refusal you want gone. Do not use it for a
      person's data.
    - **Ask a vendor for the layer-below test.** A surgical "deletion" should still match models that never saw the
      person after a new last layer is trained without their data.
    - **Measure exposure over every candidate.** Look past the top answer and compare it with a gold band.
    - **Treat a refusal or filter as removable.** Anyone with the weights can take it off with one edit.
    - **For a fine-tune, run the exact fix.** Re-run the fine-tune without the person, from the checkpoint before it.
      In Lesson 22 it took 0.3 s and passed every test.

## In code

```python
from mul import edit
q = edit.direction(model, X_gita, X_colleagues)               # the pattern that points to her
blind = edit.blind_to(model, q)                               # the last layer now ignores that pattern
attacked = edit.refit_last_layer(blind, X_others, y_others)   # the layer-below attack, with no data about her
```

The library `mul/edit.py` also has `neuron_scores` and `switch_off` for the first edit, and `key_covariance` and
`rewrite_memory` for ROME.

## Common mistakes

!!! danger "Mistakes people make"
    - **Testing only what the model says.** Ask how high it still ranks the answer, and try a new last layer.
    - **Counting changed numbers as proof.** "We changed only 0.016%" tells you the edit is small, not that the data is
      gone.
    - **Mixing up a habit and a fact.** A habit can sit in one pattern. A person's data usually does not.
    - **Trusting a refusal.** The kind of edit that can install a refusal can also remove it.
    - **Checking only general quality.** Every edit in Lesson 22 kept ordinary text in the band, yet all of them left
      her number inside.
    - **Expecting the answer to be blank.** A model that never saw her still writes a number. Judge it against the
      gold band, not against "says nothing".

## Key takeaways

- A surgical weight edit changes a few numbers by hand, with no training.
- It can switch off a **habit**, as the November 2026 news showed, because a habit is shared and lives in one
  direction.
- A person's fact is **spread out**. It took 11 neurons for half of the push towards Gita's digits and 38 for 90%.
- It did not make a model forget a **person**. It changed what the model said, and a new last layer read the data back.
- Exposure ranks all 100 possible numbers, so it catches a model that stops saying a number but still ranks it first.
- A one-direction edit is also an attack. It undid a refusal with 752 weights.
- Judge an edit like any unlearning method, against models that never saw the data, and with attacks.

!!! note "Notes to take"
    - **Surgical edit.** A few weights changed by one formula, with no training.
    - **Three kinds.** Switch off neurons, remove a direction and rewrite a memory (ROME).
    - **Direction.** The average hidden state of one group minus the average of another, scaled to length one.
    - **Exposure.** The rank of the real number among all 100, in bits. 6.64 bits means 1st and about 1 bit means
      the middle.
    - **Habit or person.** A habit is shared, so one direction holds it. Gita's number needed 38 neurons for 90%.
    - **Main number.** After a new last layer every edit was back to 6.64 bits. The exact fix gave 1.43.
    - **The trap.** "It no longer says her number" tests only the last layer.

## Quiz

```quiz
- q: What is a surgical weight edit?
  options:
    - Changing a few numbers inside a model by hand, with no training
    - Training the model again without the person's data
    - Adding a filter that blocks certain answers
  answer: 0
  why: A surgical edit works directly on the model's numbers. It does not train the model, which is why it is fast.
- q: In the November 2026 news, what did the edit remove?
  options:
    - A person's phone number
    - A habit of repeating itself on hard maths problems
    - Two whole layers of the model
  answer: 1
  why: The edit removed the pattern that went with the looping. It fixed a habit and did not add a new skill.
- q: In the choir picture, what does a new last layer stand for?
  options:
    - A new microphone that picks up the verse the singers still know
    - A new singer who learns the verse
    - A new song
  answer: 0
  why: The edits only turned down the microphones. The singers, the inside of the model, still knew the verse.
- q: After the "phone number" habit was removed, the model said no numbers at all. Had it forgotten Gita's number?
  options:
    - Yes, because it no longer said it
    - No, it still ranked her number first of the 100
  answer: 1
  why: Stopping a habit is not the same as forgetting. Her number was still the model's top guess.
- q: How did the layer-below attack bring her number back?
  options:
    - It trained a new last layer on her colleagues' lines and ordinary text
    - It asked the model politely
    - It trained on her own directory line
  answer: 0
  why: The edits changed only the last layer. The inside still held her number, and a new last layer read it out.
- q: What does "we changed only 0.016% of the numbers" tell you?
  options:
    - That the person's data has gone
    - How small the edit is, not how much was removed
    - That the model is certified
  answer: 1
  why: The numbers that were left alone can still hold what the person gave the model.
- q: A model "forgets" by refusing to answer. One edit to a few neurons makes it answer again. What does that show?
  options:
    - The refusal was only hiding the fact
    - The edit taught the model the fact
    - Refusals are always safe
  answer: 0
  why: The same edit brought nothing back from models that never saw her. It can only uncover what is still there.
- q: A model ranks a person's number 50th out of 100 possible numbers. About what is its exposure?
  options:
    - About 1 bit, which is how a model that never saw her behaves
    - 6.64 bits, the most a model can show
    - Zero, because the number is not first
  answer: 0
  why: Exposure counts how many times you can halve the list and keep the number in the top part. Halving 100 once gives 50, so it is 1 bit.
- q: Why could one direction switch off the habit of writing numbers, but not Gita's number?
  options:
    - The habit is shared by all 20 lines, while her number is spread over many neurons that also serve her colleagues
    - Her number was stored in the first layer only
    - The direction was computed with too few examples
  answer: 0
  why: Every number puts the model in the same state, so one direction catches it. Her digits needed 11 neurons for half of the push and 38 for 90%.
- q: How does ROME keep ordinary text from being disturbed?
  options:
    - It makes changes expensive along the patterns that ordinary text uses a lot, so the change lands elsewhere
    - It retrains the model on ordinary text afterwards
    - It only works on models that have never seen ordinary text
  answer: 0
  why: ROME records how hidden states spread out on 20,000 positions of ordinary text and finds the cheapest change that still fixes her keys.
```

## Try it

- Run [Lesson 22, surgical weight editing](../lessons/22-surgical-weight-editing.md). It tries every edit on this page
  and attacks each one.
- In the notebook, train the new last layer on ordinary text only, with no directory lines. Does Gita's number still
  come back?
- Give ROME all nine positions of her number, not only her two digits, and run the layer-below attack again.
- Read [model editing vs unlearning](editing-vs-unlearning.md) and [unlearning in language models](llm-unlearning.md).
- Read [when forgotten knowledge comes back](relearning-and-quantization.md) for more ways a hidden fact returns.
