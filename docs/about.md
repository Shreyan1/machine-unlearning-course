---
title: About
description: Who made this course, how to cite it and how to contribute.
---

# About this course

**Machine Unlearning for Responsible AI** is a free, hands-on course on making a trained model forget someone's data,
and testing whether it really did. It was created by **[Shreyan Basu Ray](https://shreyanbasuray.com)**.

The course itself lives in a [GitHub repository](https://github.com/Shreyan1/machine-unlearning-course), 22 notebooks,
a small course library written in plain NumPy (`mul/`), 40 practice problems and a reading list of papers. This
website explains the same ideas in simple words, with quizzes, so you can learn the concepts before (or while) you run
the code.

## What makes it different

- **Carol and the gold band.** Every lesson works through the same story and judges every method against several
  models that never saw the data, not against zero and not against one retrain.
- **Honest results.** The lessons show methods failing as well as passing, with the numbers.
- **Runs on a laptop.** Every notebook runs on a CPU, most in under a minute. Only the optional Lesson 16b needs PyTorch.

!!! note "Not legal advice"
    Whether a trained model must change depends on the request, the model and the applicable law. Unlearning is one
    possible response, not an automatic legal answer or the only route. This course teaches the technical methods,
    measurements and limits that help teams assess the evidence. See the
    [CNIL's guidance on rights in AI models](https://www.cnil.fr/en/ensuring-and-facilitating-exercise-data-subjects-rights)
    and the [ICO's guidance on individual rights in AI systems](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-individual-rights-in-our-ai-systems/).
    For a decision about real people's data, ask a qualified lawyer.

!!! warning "Research and teaching code"
    Machine unlearning is still an open research field, and the course library `mul` is research and teaching code.
    It is provided as it is, without any warranty, and it is not tested or certified for production systems. No
    method in this course guarantees that data has been removed from a model, and passing the course's audits is not
    proof that a legal duty has been met. To the fullest extent the law allows, the author is not liable for any loss
    that comes from using the course or its code. The [certificate terms](quizzes/certificate.md#terms-of-this-certificate)
    say the same for certificates.

## How to cite

If you use this course, please cite it.

```text
Basu Ray, S. (2026). MachineUnlearning: Machine Unlearning for Responsible AI.
https://github.com/Shreyan1/machine-unlearning-course
```

## Licence

The course is free to read, run and learn from, and all rights in it are reserved. See [Rights and reuse](rights.md) for
what you may do, what needs permission and the notice for AI agents.

## Contributing

Found a mistake, or want to add a problem? See the
[contributing guide](https://github.com/Shreyan1/machine-unlearning-course/blob/main/CONTRIBUTING.md) and the problem
template in the repository. Corrections to this website are welcome too.
