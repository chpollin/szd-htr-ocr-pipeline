---
name: "Evaluation hook: four-tuple protocol export"
about: "Export the decision record per reviewed item for the verification proposal"
title: "[antrag-eval] Four-tuple protocol export"
labels: ["antrag-eval"]
---

## Purpose

Make each reviewed item exportable as the four-tuple that an evaluation of
human/AI collaboration needs, independent of which criteria are later applied
to it.

## Expected export, per item

1. Initial expert judgment, before the AI suggestion is shown.
2. AI suggestion, as produced by the pipeline.
3. Final decision, as recorded after review.
4. Reference answer, where one exists.

## Notes

- Items 2 to 4 are reconstructible from the existing result files
  (`transcription_llm`, `transcription`, ground-truth sample). Item 1 is not
  recorded today, because the suggestion always precedes the review in the
  current workflow; capturing it needs its own elicitation mode.
- The export must state, per item, which of the four positions are absent and
  why, rather than filling them.
- Item granularity (object, page, line) is part of the open design question.

## Out of scope

Metrics, scoring, and any judgment about the collaboration. The hook produces
the record; the evaluation reads it.
