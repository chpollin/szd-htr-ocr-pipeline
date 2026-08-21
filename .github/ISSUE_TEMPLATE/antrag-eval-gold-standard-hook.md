---
name: "Evaluation hook: gold-standard hook"
about: "Reference answers with a predefined required checking depth per item class"
title: "[antrag-eval] Gold-standard hook"
labels: ["antrag-eval"]
---

## Purpose

Hold reference answers together with the checking depth their item class
requires, so that a later evaluation can distinguish an item that was checked
as deeply as its class demands from one that was not.

## Expected content, per item class

- The item class and how membership is decided (currently the nine prompt
  groups are the candidate classification).
- The required checking depth for that class, defined before any item is
  checked.
- The reference answers belonging to the class, with the depth actually
  reached per item.

## Notes

- The pipeline stores a per-object trust tier but no per-class requirement, so
  "checked" today carries no statement about sufficiency. Closing that gap is
  the point of this hook.
- The required depth is set in advance and versioned. Changing it later must be
  visible as a change, not as a silent recalibration.
- Reference answers already exist for part of the corpus (ground-truth sample);
  coverage per class is uneven and must be reported as such.

## Out of scope

Producing new reference answers, and any target coverage figure.
