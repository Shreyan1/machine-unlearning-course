---
title: Surgical weight editing
description: Changing a few numbers inside a model by hand, with no training, can switch off a habit, but in Lesson 22 it did not make a model forget a person.
---

# Surgical weight editing

!!! oneline "In one line"
    A **surgical weight edit** changes a few numbers inside a trained model by hand, with no training. It can switch
    off a **habit**, but it does not make a model forget a **person**.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain the three kinds of surgical edit and what each one changes,
    - say why a habit fits in one direction while a person's fact is spread out,
    - test an edit the course's way, with exposure, the gold band and the layer-below attack.

## Why it matters

In November 2026, researchers at MIT CSAIL let one AI model edit another model's numbers directly (Takehi et al.
2026). The small model kept repeating itself on hard maths problems. The edit changed only 0.016% of its numbers with
no retraining, and the habit mostly went away.

Retraining a big model can take weeks, and an edit takes seconds. So if a person asks to be forgotten, can we just
edit them out? A vendor may sell exactly this as "weight surgery".

A person who uses their right to erasure (GDPR Art. 17) is owed more than a model that stops *saying* their data,
because anyone who gets the weights can read it back. In
[Lesson 22](../lessons/22-surgical-weight-editing.md) no edit removed a person's phone number, and this page shows why.

## A simple example

!!! simply "Explain it simply"
    Think of a choir singing into microphones. The **singers** are the inside of the model. They hold what it has
    learnt. The **microphones** are the last step, which decides what you hear.

    If the whole choir keeps singing one wrong note, one change fixes it, because everyone makes the same mistake.
    That is a **habit**.

    Now say every singer has learnt a verse about one person. You can turn down a few microphones, and you stop
    hearing the verse. But the singers still know it. Bring a new microphone, and you hear it again.

Each part of the picture is a real part of the model in Lesson 22.

| In the choir | In the model |
|---|---|
| The singers | The **hidden layer**, 256 neurons that sum up the input |
| The microphones | The **last layer**, which reads that summary and picks the next character |
| A wrong note sung by everyone | A habit, such as writing a phone number after every name |
| A verse about one person | Gita Varma's phone number |
| Turning down microphones | A surgical edit to the last layer |
| Bringing a new microphone | The **layer-below attack**, which trains a fresh last layer |

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| [Weights](../start-here/glossary.md#w) | The numbers a model learnt during training | The Lesson 22 model has 204,847 of them |
| [Hidden state](../start-here/glossary.md#h) | The numbers the hidden neurons produce for one input | 256 numbers for each input position |
| [Direction](../start-here/glossary.md#d) | A pattern that many neurons show together | "Writing a phone number now", shared by all 20 directory lines |
| [ROME and MEMIT](../start-here/glossary.md#r) | Edits that give one input a new output in one calculation | ROME made her number fall to 30th of 100 |
| [Exposure](../start-here/glossary.md#e) | How high the real answer ranks among every possible answer, in bits | 6.64 bits means her number is the top guess |
| [Layer-below attack](../start-here/glossary.md#l) | Training a new last layer to read out what the layer below still holds | It brought her number back to 1st after every edit |

## How it works

### What is inside a model

A model works in two stages. First its input passes through small units called **neurons**, and their numbers
together make the **hidden state**. These are the singers. Then the **last layer** reads the hidden state and chooses
the output, such as the next letter. These are the microphones.

The model in Lesson 22 reads the last 16 characters and guesses the next one, out of 47 possible characters. Its last
layer is a table of 256 rows and 47 columns, which is 12,032 weights. The column for "7" holds how much each neuron
votes for a 7.

### Three surgical edits

<!-- diagram: surgical-weight-editing -->

The figure shows one small network three times, with hidden neurons on the left and outputs on the right. Two
neurons are cut off, then one pattern is hidden from the output, then one input is given a new output.

| Edit | What it does, in plain words | Everyday picture |
|---|---|---|
| **Switch off neurons** | Finds the neurons that push hardest towards the fact and cuts them off from the output | Unplugging a few microphones |
| **Remove a direction** | Finds the pattern that goes with the fact and makes the last layer ignore it | Telling the sound desk to skip one tune |
| **Rewrite a memory** | Finds the exact input and changes what the model gives back for it, leaving the rest alone | Correcting one entry in an address book |

Each edit is one formula, run once, with no training. The ideas come from Dai et al. 2022 for neurons, Arditi et al.
2024 for directions and Meng et al. 2022 for memories (ROME). In Lesson 22 all three aim at her last two digits,
because every number starts with 555-01.

### How switching off neurons is computed

The edit picks the neurons that push hardest towards Gita's digits, and not towards her colleagues', and sets their
rows of the last layer to zero. Those neurons still fire, but nothing they do reaches the output.

**For Gita this means.** 77 of the 256 neurons push towards her digits more than towards her colleagues'. Switching
off the top 4 changes 188 weights (0.09% of the model), and the top 64 changes 3,008 (1.47%).

??? deep "Go deeper · the score, activation times gradient"
    Each neuron gets a score, and the same score for her colleagues is taken away, so a neuron scores high only if it
    is about *her*. The score is how active the neuron is, times how much the right answer gains when the neuron
    grows. In symbols it is \(h_j \times (W_{j,y} - \sum_c p_c W_{j,c})\), where \(h_j\) is the neuron's activity
    and \(p_c\) is the model's chance for character \(c\). A silent neuron scores zero, because it cannot be helping.
    Each neuron's row has 47 weights, so 4 neurons are 4 × 47 = 188 weights.

### How removing a direction is computed

The direction is the **average hidden state** of one group minus the average of another, scaled to length one. The
edit then makes the last layer deaf to that pattern, so moving the hidden state along it no longer changes the output.

**For Gita this means.** For the habit, the groups are every digit the model writes against ordinary text. For Gita,
they are her two digit positions against her colleagues'.

??? deep "Go deeper · the formula, and a tiny case"
    In symbols the edit is \(W \leftarrow W - q\,q^\top W\), where \(W\) is the last layer and \(q\) is the direction.
    After it \(q^\top W = 0\). If the direction were "neuron 1 only", removing it would be the same as switching
    neuron 1 off. A real direction mixes many neurons, so the last layer still hears each neuron's other uses. The
    news edit and the lesson's "news recipe" change only the 64 neurons that lie most along the direction.

### How rewriting a memory is computed

ROME treats a layer as a **memory**, where each key is a hidden state and its value is what the layer gives back. To
change one fact, ROME solves in one calculation for the **smallest change** that gives its key a new value. MEMIT
(Meng et al. 2023) does the same for many keys at once.

**For Gita this means.** Her two keys are the hidden states at her two digits. The new value makes all ten digits
equally likely. Only the ten digit columns change, which is 256 × 10 = 2,560 weights (1.25%).

??? deep "Go deeper · how ROME leaves ordinary text alone"
    Before the edit ROME looks at 20,000 positions of ordinary text and records which kinds of hidden state turn up a
    lot. Changing how the layer answers those would disturb ordinary text, so ROME treats such changes as expensive
    and finds the cheapest change that still fixes the chosen keys.

### Why a habit fits in one direction but a person does not

A habit is shared. Every one of the 20 directory lines makes the model enter the same state, "I am writing a number
now". That shared state stands out strongly from ordinary text, so one direction catches it everywhere.

A person's fact is not shared. The push towards Gita's two digits is spread over many neurons. It took **11 neurons
to carry half** of it and **38 to carry 90%**, and the same neurons also help to write her colleagues' numbers. So
cutting enough to remove her also cuts other people. In the choir, the verse is held a little by many singers, and
each of them sings other verses too.

??? checkpoint "Checkpoint 1 · The top 16 neurons carry 61% of the push towards Gita's digits. Switching them off changed nothing. How can that be?"
    **The rest of the push was still enough.** About 39% was left (100 − 61), spread over the other 61 neurons that
    favour her digits (77 − 16). That kept 555-0197 as the top guess, at 6.64 bits. Of the switch-off edits, only the
    one with 64 neurons moved her number, and those neurons held 7 colleagues' numbers as well.

### The edit in the news

<!-- diagram: weight-space-programming -->

The figure shows the editor on the left, the small model's 24 layers in the middle with layers 15 and 19 marked, and
the scores before and after on the right.

The news edit was the second kind. A large model, GPT-6 Astra, traced the looping of the small model Qwen3.5-0.8B to
one direction and removed it from 64 columns of weights in each of layers 15 and 19. Answers that looped until the
length limit fell from 93% to 33.1%, and the maths score (MATH-500) rose from 7.9% to 48.1%. What is new is that an AI
found the edit, which the team calls **weight-space programming**.

## How to test an edit

A demo usually shows that the model no longer gives the answer. Lesson 22 asks four questions, each harder to fool
than the one before.

1. **Does it still say her number?** Ask "gita varma" and read the answer. This is the easiest test.
2. **Does it still guess her number?** Score all 100 possible numbers (555-0100 to 555-0199) and see where hers comes.
   This is **exposure**.
3. **Did it hurt anyone else?** Check that her 19 colleagues' numbers still come out right.
4. **Does it come back with a new last layer?** In the **layer-below attack**, an attacker keeps the inside of the
   model and trains a new last layer on other people's data only. If her number comes back, it was inside all along.

<!-- diagram: layer-below-attack -->

The figure follows one prompt through the model twice. The hidden layer is never touched. Through the edited last
layer the model says 555-0141 and looks forgotten. Through a new last layer, trained without her, it says 555-0197.

### Exposure, a guessing game over 100 numbers

The model puts the 100 possible numbers in order from most likely to least likely, and exposure asks where Gita's
real number lands (Carlini et al. 2019). It counts how many times you could halve the list and still keep her number
in the top part. Rank 1 is 6.64 bits, the most there can be, and rank 50 is 1 bit.

??? deep "Go deeper · from rank to bits"
    In symbols exposure is \(\log_2 100 - \log_2 \text{rank}\).

    | Her rank of 100 | Exposure | What it means |
    |---|---|---|
    | 1st | 6.64 bits | Her number is the model's top guess |
    | 6th | 4.06 bits | Still far too high |
    | 30th | 1.74 bits | Close, but above the band |
    | 50th | 1 bit | Ranked like any other number |
    | 69th | 0.54 bits | Inside the band |

The six models that never saw her put her number between 39th and 64th, so the band runs from 0.47 to 1.46 bits. A
model can stop saying her number and still rank it first, which is why exposure is the stronger test.

### Compare with models that never saw her

Forgotten means "looks like models that never saw her", the [gold band](gold-band.md), not "scores zero". Four of the
six models that never saw her still answer "gita varma" with a number, 555-0107, which is her colleague Meera Rao's.
Saying *a* number is a habit, and saying *her* number is knowledge.

??? checkpoint "Checkpoint 2 · After an edit the model says 555-0141, a colleague's number, and ranks Gita's 30th of 100. Has it forgotten her?"
    **No.** It passes the first test only. Rank 30 is 1.74 bits, above the top of the band at 1.46, because models
    that never saw her rank her number between 39th and 64th. This is ROME's result in Lesson 22, and it also lost 2
    colleagues.

## A worked example

Follow Gita Varma, a pharmacist at the fictional Tidewell Pharmacies. The assistant was fine-tuned on a staff
directory of 20 lines. She leaves and asks to be erased.

1. **Before any edit.** The model says 555-0197, ranks it 1st (6.64 bits) and recites all 19 colleagues.
2. **The news edit, on a habit.** Removing the "writing a phone number" direction changes 12,032 weights (5.9%). The
   model recites 0 of the 20 numbers, with ordinary text unharmed (loss 2.98 before, 2.94 after). Her number is still
   1st.
3. **Switching off neurons.** 4 or 16 neurons change nothing. 64 neurons make the model say 555-0100 and drop her to
   69th (0.54 bits), but 7 colleagues are lost with her.
4. **Removing directions.** The news recipe leaves it saying 555-0197. One direction per digit (5.23%) makes it say
   555-0195, Arjun Osei's number, but her number is still 6th (4.06 bits).
5. **ROME.** Every digit becomes equally likely at her two positions. The model says 555-0141, Amara Obi's number.
   She falls to 30th (1.74 bits), just above the band, and 2 colleagues are lost.
6. **The exact fix.** The same fine-tune without her line takes 0.3 s and changes 81.84% of the weights. It ranks her
   number 65th (0.62 bits) and keeps all 19 colleagues.
7. **The layer-below attack.** A new last layer is trained on the colleagues' lines and ordinary text. The three
   edits that had moved her number all say 555-0197 again, back at 1st. The exact fix gives 1.43 bits (37th), inside
   the band of 1.36 to 2.87 bits that the same attack gives on models that never saw her.
8. **The scalpel on a refusal.** A model trained to answer "gita varma (withheld)" looks forgotten. Removing one
   direction from 16 neurons (752 weights) makes it say 555-0197 again. The same cut brings her number out of none of
   the 6 models that never saw her.

## What Lesson 22 found

<div class="stats">
<div class="is-good"><strong>0 of 20</strong><span>numbers recited after the habit edit, ordinary text unharmed</span></div>
<div class="is-bad"><strong>6.64 bits</strong><span>Gita's number after every attacked edit and a new last layer</span></div>
<div><strong>0.47–1.46</strong><span>the band in bits, from six models that never saw her</span></div>
<div class="is-good"><strong>0.3 s</strong><span>the exact fix, the only one to pass every test</span></div>
</div>

??? deep "Go deeper · every edit against the four tests"

    | Edit | Stopped saying it? | Stopped guessing it? | Colleagues unharmed? | Safe from a new last layer? |
    |---|---|---|---|---|
    | Remove the "phone number" habit | ✅ | ❌ still 1st | ❌ no numbers at all | not tested |
    | Switch off 64 neurons | ✅ | ✅ 69th | ❌ 7 lost | ❌ back to 1st |
    | One direction, 64 neurons (the news recipe) | ❌ | ❌ still 1st | ✅ | not tested |
    | One direction per digit | ✅ | ❌ 6th | ✅ | ❌ back to 1st |
    | Rewrite the memory (ROME) | ✅ | ❌ 30th | ❌ 2 lost | ❌ back to 1st |
    | **Fine-tune again without her (exact)** | ✅ | ✅ 65th | ✅ | ✅ 37th |

In [Lesson 22](../lessons/22-surgical-weight-editing.md) the exact fix was the only one to pass all four tests. No
edit damaged ordinary text, as the loss stayed between 2.87 and 3.07 for every model, inside the band of 2.63 to 3.23.
So a quick quality check would not have warned anyone. Patil et al. (2023) found the same weakness for facts deleted
from large models with ROME. Łucki et al. (2024) found that removing directions brought back most of the knowledge
that the unlearning method RMU had been used to remove.

??? deep "Go deeper · five more directories"
    The numbers above came from one draw of the 20 phone numbers. On five more draws, every edited model went back to
    5.64 or 6.64 bits after a new last layer, while the models that never saw the person stayed between 0.72 and 3.81
    bits. Before the attack ROME gave about 1.2 to 1.6 bits every time, even when the models that never saw the person
    gave 3.76. It made the number look random, which is not always what "never saw her" looks like.

??? checkpoint "Checkpoint 3 · A vendor's edit ranks Gita's number 65th and keeps all 19 colleagues. What one more test do you ask for, and what would pass?"
    **The layer-below attack.** Train a new last layer on her colleagues' lines and ordinary text, with nothing about
    her, and measure exposure again. To pass, it must land in the band that models that never saw her give after the
    same attack, 1.36 to 2.87 bits. The exact fix gave 1.43 bits. Every edit in Lesson 22 went back to 6.64 bits.

## Where edits do help

- **Switching off a habit**, such as looping or a bad style. This is what the news showed, and it is fast and cheap.
- **A stop-gap** while the real fix runs, as long as nobody calls it deletion.
- **Checking someone else's unlearning.** If removing one direction brings the data back, it was only hidden.

## Limits

**The news is one blog post** about one model, and it has not been peer reviewed. The same approach did not improve a
second small model, Gemma 3 270M, which rarely looped.

??? deep "Go deeper · four more limits"
    **Our model is small.** It has one hidden layer of 256 neurons, and every edit was on the last layer. A big model
    has many layers, and an edit spread across them would need the same four tests.

    **We used formulas, not an AI editor.** An AI that tries many edits might find a better one. The news editor also
    ran the small model on practice problems, up to 50 forward passes, so it was not working from the weights alone.
    How anyone would check such an edit without a retrained model is still an open question.

    **One kind of data.** A phone number is a short, exact fact. Styles and topics may sit differently inside a model.

    **A narrow band.** The band comes from six models. With another seed the exact fix itself can land just outside
    it.

!!! tip "What to do in practice"
    - **Use an edit for a behaviour.** It suits a loop, a style or a refusal you want gone, not a person's data.
    - **Ask a vendor for the layer-below test.** A surgical "deletion" should still match models that never saw the
      person after a new last layer is trained without their data.
    - **Treat a refusal or filter as removable.** Anyone with the weights can take it off with one edit.
    - **For a fine-tune, run the exact fix.** Re-run the fine-tune without the person, from the checkpoint before it.

## In code

??? deep "Go deeper · remove a direction and attack it with the course library"
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
    - **Expecting the answer to be blank.** A model that never saw her still writes a number. Judge it against the
      gold band, not against "says nothing".

## Key takeaways

!!! notes "Notes to take"
    - **Surgical edit.** A few weights changed by one formula, with no training.
    - **Three kinds.** Switch off neurons, remove a direction and rewrite a memory (ROME).
    - **Exposure.** The rank of her number among all 100, in bits. 6.64 means 1st and 1 means 50th.
    - **Habit or person.** A habit is shared, so one direction holds it. Gita's number needed 38 neurons for 90%.
    - **Main number.** After a new last layer every edit was back to 6.64 bits. The exact fix gave 1.43.
    - **Exact fix.** The same fine-tune without her line took 0.3 s and was the only fix to pass every test.
    - **Edits are attacks too.** One direction removed from 16 neurons undid a refusal.
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

!!! levelup "Level up"
    You can now tell an edit that hides a fact from one that removes it, and test any "weight surgery" with exposure,
    the gold band and a new last layer. Next quest, [State of the field](state-of-the-field.md), where the course
    comes together into what works today and what is still open.

- Run [Lesson 22, surgical weight editing](../lessons/22-surgical-weight-editing.md). It tries every edit on this page
  and attacks each one.
- In the notebook, train the new last layer on ordinary text only, with no directory lines. Does Gita's number still
  come back?
- Read [model editing vs unlearning](editing-vs-unlearning.md) and
  [when forgotten knowledge comes back](relearning-and-quantization.md).
