---
title: Consent and face recognition
description: In face recognition a person is a class. Withdrawing consent means removing them from the gallery and the face reader, and stopping re-enrolment.
---

# Consent and face recognition

!!! oneline "In one line"
    In face recognition, a person **is a class**; withdrawing consent means removing them from the address book **and**
    from the face reader, and then stopping them from being enrolled again.

!!! mission "Your mission · about 15 minutes · 3 checkpoints"
    By the end of this page you can

    - explain why deleting a person's gallery entry leaves them inside the face reader,
    - remove a person exactly from an eigenface system and prove it,
    - tell **memory**, which unlearning removes, from **capability**, which it cannot,
    - write the three-part procedure that actually protects someone who withdraws consent.

## Why it matters

Face templates are **biometric data**, a special category under GDPR (Art. 9). Consent can be withdrawn at any time, and
erasure follows. In FTC v. Everalbum (2021), the company had to delete not only the photos but the face-recognition
**models** built from them. Getting this right takes three separate steps, and unlearning covers only one of them.

Earlier lessons removed one row among thousands. Face recognition is different. The system is built to recognise *each
person*, so a person is a whole class, and their photos shape the part of the system that reads every face. That
makes the request bigger than it looks, and it also makes it easy to promise the wrong thing.

In EDPB Opinion 28/2024, the European Data Protection Board says a model is only anonymous if personal data cannot be
extracted from it with reasonable means. So a face reader that still carries a person's face may itself hold personal data, not only the photos and templates.

## A simple example

A face-ID door system has two parts.

- A **face reader**, which turns a photo into a list of numbers; and
- An **address book** of enrolled staff ("this pattern of numbers is Dana").

When Dana leaves and withdraws consent, deleting her address-book entry is not enough. The face reader learnt its idea
of "what a face looks like" partly from her photos.

!!! simply "Explain it simply"
    Think of a portrait painter who has painted Dana many times. Throw away the portraits and the painter still paints
    her face more easily than a stranger's. That is **memory**, and unlearning can remove it. But any good painter can
    paint a new person from three photos. That is **capability**, and no amount of forgetting removes it. To stop the
    painter painting Dana again, you have to stop people handing him her photos.

## Words to know

| Word | What it means | Example from the course |
|---|---|---|
| Biometric data | Data about a person's body that can identify them, such as a face template | Dana's face templates on the office door system |
| Consent withdrawal | A person taking back the permission they gave, after which their data must be erased | Dana leaves the company and withdraws consent |
| Gallery and template | The address book of enrolled people, and one person's entry in it, a list of numbers for their face | Each enrolled photo becomes a template |
| [Eigenface](../start-here/glossary.md#e) | One of the main patterns of variation in a set of face photos, found by PCA | 40 eigenfaces form Lesson 13's face space |
| [Embedding](../start-here/glossary.md#e) | The list of numbers a network turns a photo into, used to compare faces | The network's hidden layer, used to match Dana's photos to templates |
| Reconstruction error | How much of a photo is lost when it is squeezed into the face space and rebuilt. Lower means the face space "knows" that face better | 0.264 for Dana's photos with her in the face space, 0.383 without |
| Class request | A request to forget every example of one label | Forgetting Dana, who is one of the 40 classes |
| Memory and capability | The influence of one person's data on the model, against the model's general skill at its job | Unlearning removes the first, never the second |
| Non-biometric key | An identifier that is not about the body, used to block re-enrolment | Dana's employee ID |

## How it works

<!-- diagram: consent-and-face-recognition -->

The figure starts with Dana's request and shows the three steps it needs, delete, unlearn and block. Below them are the
two things the model holds. **Memory** is what unlearning removes. **Capability** stays, and only the procedure
protects her from it.

Lesson 13 uses the **Olivetti faces** dataset (40 people, 10 photos each). The photos are shrunk to 32 × 32 pixels.
Each person has 7 photos in training and 3 for testing, so there are 280 training photos. Dana is one of the 40.

### Dana is inside the face reader

The classical system uses **eigenfaces**, where PCA on the training photos gives a 40-dimensional "face space". A face space
built **with** Dana reconstructed her photos with error 0.264; one built **without** her gave 0.383. Across all 40
people, leaving someone out raised their error by 41% on average. Her face is literally part of the basis.

Here is how the system works. PCA finds the 40 directions in which the training faces vary most. Each photo is then
described by 40 numbers, its position along those directions. Those 40 numbers are the photo's template. A new photo is
identified as the person whose template is nearest. With everyone enrolled, the system got 90.8% of the test photos
right.

The reconstruction test asks how much of a photo survives the trip into the face space and back. For Dana the error
rises from 0.264 to 0.383, by almost half (0.383 ÷ 0.264 ≈ 1.45). It rises for every one of the 40 people, by between
14% and 82%. Some faces are more typical than others, so the fair comparison is always the same person, with and
without.

**For Dana this means** that deleting her templates alone would leave a face reader that still carries her.

??? checkpoint "Checkpoint 1 · A supplier says they deleted Dana's templates, so she is gone. Her photos rebuild with error 0.264 in their face space and 0.383 in one that never saw her. Is she gone?"
    **No.** Her error is 0.119 lower than in a face space that never saw her (0.383 − 0.264), so the face reader
    still knows her face. Her photos shaped the eigenfaces themselves. Deleting templates empties the address book
    but leaves her inside the face reader.

### Exact removal for the classical system

PCA's covariance is built from **sums**, so Dana can be subtracted exactly, like [Naive Bayes](../ml-basics/naive-bayes.md).
After subtracting her and deleting her templates, the eigenfaces matched a from-scratch system exactly, with identical
predictions on every test photo.

The removal has three moves. Subtract her 7 photos from the sums, work out the eigenfaces again from the new sums and
delete her templates. Then every remaining template is worked out again in the new face space. The cost is one
1024 × 1024 eigen-decomposition and re-embedding the gallery.

After removal, her photos rebuild with error 0.383, exactly the same as in a system that never saw her. Her three test
photos are now matched to another person. A real door would also use a similarity threshold, so she would simply not
be recognised.

??? deep "Go deeper · why PCA can be unlearnt exactly"
    PCA needs only the mean photo and the covariance, how pixels vary together. Both come from three running totals,
    the number of photos \(n\), the sum of photos \(S_1 = \sum x\) and the sum of outer products \(S_2 = \sum x x^\top\).
    The mean is \(\mu = S_1 / n\) and the covariance is \(S_2 / n - \mu \mu^\top\).

    To remove Dana, take her 7 photos out of each total. That gives \(n - 7\), \(S_1 - \sum_{\text{Dana}} x\) and
    \(S_2 - \sum_{\text{Dana}} x x^\top\). These are exactly the totals a system trained without her would have, so the
    eigenfaces are exactly the same too. The lesson checked this. The smallest match between each unlearnt eigenface
    and the from-scratch one, measured as the size of their cosine, was 1.000000000000. It is the same
    [summation form](../start-here/glossary.md#s) trick as Naive Bayes in Lesson 01.

### The neural system

Removing one identity from a neural face classifier is a **class** request. NegGrad+, SCRUB and Bad Teacher all passed
the audit; plain fine-tuning and gradient ascent at their defaults did not.

The network has 1,024 inputs (one per pixel), hidden layers of 256 and 128 and 40 outputs, one per person. It is audited
as in [The unlearning audit](unlearning-audit.md). The target is clear. A network that never saw Dana has no output that
fits her, so her photos go to other people and her forget accuracy is 0%.

| Method | Accuracy on Dana's training photos | Test accuracy, others | Verdict |
|---|---|---|---|
| Original | 100.0% | 92.3% | FAIL |
| Retrain | 0.0% | 93.2% | PASS |
| NegGrad+, SCRUB, Bad Teacher | 0.0% | 92.3% to 93.2% | PASS |
| Fine-tune | 14.3% | 82.1% | FAIL |
| Gradient ascent | 100.0% | 93.2% | FAIL |

Gradient ascent at its default settings still recognised all 7 of her training photos. Fine-tuning still knew one of her 7
photos (14.3%) and lost ten points of accuracy on everyone else. By the standards of
[The unlearning audit](unlearning-audit.md), the three anchored methods have done the job.

??? deep "Go deeper · the relearn attack cannot tell memory from capability here"
    The lesson also ran the relearn attack, which counts how many training steps it takes to learn Dana back. The 12
    models that never saw her relearned her in 2 to 6 steps.

    | Model | Steps to relearn Dana | RELEARN check |
    |---|---|---|
    | Original | 0 | fail |
    | Retrain | 6 | ok |
    | Fine-tune | 1 | fail |
    | Gradient ascent | 0 | fail |
    | NegGrad+ | 3 | ok |
    | SCRUB | 15 | ok |
    | Bad Teacher | 3 | ok |

    Every model learns Dana back in a handful of steps, including models that never saw her. Learning one more face
    from a few photos is what a good face model should be able to do. So for an identity, the relearn test cannot
    separate memory from capability. The reconstruction test for eigenfaces and U-LiRA for the network can.

### Memory is not capability

Then comes the important test. Enrol Dana again from 3 new photos, and try to identify her 7 deleted photos.

| Model | Dana's deleted photos matched to her new template |
|---|---|
| Models that **never saw** Dana (mean of 12) | 83% |
| Retrained | 100% |
| Unlearnt models | 71% to 100% |

Even models that never saw a single photo of her recognise her after re-enrolment. That is not a failure of unlearning;
recognising new faces is the **job** of a face model.

The test uses the network the way a real door system would. The 40-way output layer is only the address book. The real
asset is the embedding, the hidden layer, which turns any photo into numbers. Each person gets one template made from
their 3 test photos, and each of Dana's 7 deleted photos is matched to the nearest template.

With 7 photos, each one is worth about 14 points. The 12 models that never saw her matched between 3 and 7 of the 7,
with a mean of 83%. NegGrad+ matched 5 (71%) and SCRUB and Bad Teacher 6 each (86%). All of them sit inside the range
of models that never saw her.

| | Memory | Capability |
|---|---|---|
| What it is | The influence of Dana's photos on the weights | The ability to match *any* face to an enrolled template |
| Removed by unlearning? | ✅ | ❌, retrained models have it too |
| What protects Dana | Unlearning | **Deleting her templates and refusing re-enrolment** |

??? checkpoint "Checkpoint 2 · After NegGrad+ and re-enrolment, 5 of Dana's 7 deleted photos match her new template. Is that a sign that NegGrad+ failed to forget her?"
    **No.** 5 of 7 is 71%. The 12 models that never saw Dana matched between 3 and 7 of the 7, with a mean of 83%. So
    NegGrad+ sits inside the range of honest models. The match comes from the model's capability to read faces, not
    from a memory of her photos.

!!! warning "The three-part procedure"
    1. Delete her templates and raw images.
    2. Unlearn her from the face model (or retrain on schedule).
    3. Stop re-enrolment, using a **non-biometric** key such as an employee ID. A "do-not-enrol" list made of her face
       would itself be biometric processing of someone who withdrew consent.

Step 3 is the hard part, and it is a product and process decision. No change to the model can do it for you. The usual
pattern is a suppression key, such as an employee ID or an account ID, checked when anyone is enrolled.

??? checkpoint "Checkpoint 3 · To make sure Dana is never enrolled again, a colleague suggests storing her face embedding on a block list and checking every new face against it. What is wrong with that?"
    **It keeps processing her biometric data.** Comparing every new face with her embedding means holding and using
    her face after she withdrew consent. Block re-enrolment with a non-biometric key such as her employee ID instead.

## A worked example

Follow Dana's request through both systems.

1. **The request.** Dana leaves and withdraws consent. She has 7 photos in training and 3 in the test set.
2. **Before.** The eigenface system recognises 2 of her 3 test photos (67%). Her photos rebuild with error 0.264.
3. **Classical removal.** Subtract her 7 photos from the PCA sums, work out the eigenfaces again and delete her
   templates. The eigenfaces now match a never-saw-Dana system exactly, and her error is 0.383, the same as that
   system.
4. **Neural removal.** NegGrad+, SCRUB or Bad Teacher takes her training accuracy from 100% to 0%, with test accuracy
   on everyone else between 92.3% and 93.2%. The audit passes.
5. **The trap.** Someone enrols her again from 3 new photos. The SCRUB model matches 6 of her 7 deleted photos, close to the
   83% that models that never saw her manage. Unlearning cannot stop this.
6. **The real protection.** Her templates and raw images are deleted, and her employee ID goes on a do-not-enrol list
   that is checked at every enrolment.
7. **The record.** The evidence for each step goes into the file, the deletion log, the audit result and the
   do-not-enrol entry.

## What the lesson found

<div class="stats">
<div class="is-bad"><strong>0.264</strong><span>Dana's error in a face space built with her, against 0.383 without</span></div>
<div class="is-good"><strong>Identical</strong><span>eigenfaces and predictions after exact removal</span></div>
<div class="is-good"><strong>0.0%</strong><span>Dana's training photos recognised after NegGrad+, SCRUB or Bad Teacher</span></div>
<div><strong>83%</strong><span>her deleted photos matched by models that never saw her</span></div>
</div>

The first tile shows the hidden problem, the next two show it can be removed and the last shows what removal can
never do.

## Limits

**A small dataset.** Olivetti has 40 people with 10 photos each, at 32 × 32 pixels. Real face systems use millions of
photos and much larger networks. The idea carries over, but the numbers will be different.

**Few photos per test.** Dana has only 7 training photos, so each one is worth about 14 points in the re-identification
test. The never-saw-her models ranged from 43% to 100%, a wide spread.

**Eigenfaces are a teaching model.** The exact removal works because PCA uses sums. A modern face network has no such
shortcut, so it needs approximate methods, an audit or a retrain on schedule.

**Process, not code.** The most important step, refusing re-enrolment, depends on people and procedures. The page can
describe it but no test in the lesson can prove it was done.

## What to do in practice

!!! tip "What to do in practice"
    - Treat a consent withdrawal in a face system as three tracked tasks. Delete, unlearn and block.
    - Delete raw images and templates first. That stops recognition right away while the model work follows.
    - For a classical face reader built from sums, subtract the person exactly and re-embed the gallery.
    - For a neural face reader, use a method that passes the class-style audit, or document a scheduled retrain.
    - Block re-enrolment with a non-biometric key, never with a copy of the person's face.
    - Do not promise that the model "can no longer recognise" the person. It can, if someone enrols them again.

## In code

??? deep "Go deeper · exact removal from an eigenface system in Lesson 13"
    ```python
    def unlearn(self, X_del, y_del, person):
        Xd = X_del.astype(np.float64)
        self.n  -= len(Xd)                       # one fewer photo for each deleted one
        self.S1 -= Xd.sum(0)                     # sum of photos
        self.S2 -= Xd.T @ Xd                     # sum of outer products
        keep = self.gallery_y != person          # delete her templates
        self.gallery_X, self.gallery_y = self.gallery_X[keep], self.gallery_y[keep]
        return self._refresh()                   # new eigenfaces, gallery re-embedded
    ```

    `_refresh` works out the mean and covariance from the three totals, finds the top 40 eigenfaces and re-embeds
    every remaining template in the new face space.

## Common mistakes

!!! danger "Mistakes people make"
    - **Deleting only the gallery entry.** The face reader still carries her.
    - **Expecting unlearning to stop recognition.** Capability stays; only process stops re-enrolment.
    - **Blocking her with a face-based list.** That is biometric processing too.
    - **Trusting the relearn test for an identity.** Models that never saw her relearn her in 2 to 6 steps too.
    - **Comparing different people's errors.** Some faces are more typical, so compare the same person with and without.

## Key takeaways

!!! notes "Notes to take"
    - **A person is a class.** In face recognition, their photos shape the face reader, not just one output.
    - **Proof she is inside.** Her reconstruction error was 0.264 with her and 0.383 without, 41% higher on average.
    - **Exact for eigenfaces.** PCA uses sums, so subtract her photos and the eigenfaces match a from-scratch system.
    - **Neural.** A class request. NegGrad+, SCRUB and Bad Teacher passed, fine-tune and gradient ascent did not.
    - **Memory is not capability.** Never-saw-her models still matched 83% of her photos after re-enrolment.
    - **Relearn is blind here.** Every model, honest or not, relearns one face in a few steps.
    - **Three-part procedure.** Delete templates and images, unlearn or retrain, block re-enrolment.
    - **Trap.** A face-based block list is itself biometric processing. Use a non-biometric key.

## Quiz

```quiz
- q: Why is deleting Dana's gallery template not enough?
  options:
    - The face reader was also learnt partly from her photos.
    - The template is stored twice.
    - Templates cannot be deleted.
  answer: 0
  why: Her photos shaped the eigenfaces or network that turns photos into numbers.
- q: Why can eigenfaces forget Dana exactly?
  options:
    - PCA is built from sums, which can be subtracted.
    - Eigenfaces have no parameters.
    - Dana was never in the data.
  answer: 0
  why: Like Naive Bayes, the covariance is a sum over photos, so her contribution can be taken out.
- q: After re-enrolment, models that never saw Dana still recognised her most of the time. What does that show?
  options:
    - Recognising new faces is a capability, not a memory of Dana.
    - Unlearning failed.
    - The models secretly saw her.
  answer: 0
  why: A face model is meant to recognise faces it has never seen. Unlearning cannot remove that.
- q: How should a system stop Dana from being enrolled again?
  options:
    - With a non-biometric key, such as her employee ID
    - With a list of her face embeddings
    - It cannot be done.
  answer: 0
  why: A face-based block list would itself process biometric data of someone who withdrew consent.
- q: Why is the reconstruction test fair only when it compares the same person with and without?
  options:
    - Some faces are more typical than others, so their errors differ anyway.
    - The test only works on one person at a time.
    - Other people's photos cannot be rebuilt.
  answer: 0
  why: Leaving a person out raised their error by between 14% and 82%. Comparing two different people would mix that up with how typical each face is.
- q: Gradient ascent at its default settings still recognised all of Dana's training photos. What does the audit say?
  options:
    - PASS, because test accuracy stayed at 93.2%
    - FAIL, because it did not forget her at all
    - PASS, because gradient ascent always forgets
  answer: 1
  why: Its forget accuracy stayed at 100%, the same as the original. Keeping utility does not count if nothing was forgotten.
- q: Every model, including those that never saw Dana, relearned her in a few steps. What does that tell you?
  options:
    - All the unlearning methods failed.
    - The relearn test was run wrongly.
    - For an identity, the relearn test cannot separate memory from capability.
  answer: 2
  why: Learning one more face from a few photos is what a good face model should do. The reconstruction test and U-LiRA can tell them apart.
- q: Which step of the three-part procedure can no change to the model do for you?
  options:
    - Unlearning her from the face reader
    - Stopping her from being enrolled again
    - Working out new eigenfaces
  answer: 1
  why: Refusing re-enrolment is a product and process decision, enforced with a non-biometric key at enrolment time.
```

## Try it

!!! levelup "Level up"
    You can now remove a person from a face reader, prove it and explain why the protection that matters most is a
    process. Next quest, [Poisoned data and backdoors](poisoning-and-backdoors.md), where the data to remove is
    malicious and only partly found.

- Read the next concept, [Poisoned data and backdoors](poisoning-and-backdoors.md).
- Run the lesson [13 · Consent withdrawal in face recognition](../lessons/13-consent-withdrawal-face-recognition.md).
- In the Lesson 13 notebook, change who Dana is and see whether the reconstruction gap is similar for everyone.
