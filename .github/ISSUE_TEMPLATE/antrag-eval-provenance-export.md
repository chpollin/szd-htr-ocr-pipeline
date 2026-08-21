---
name: "Evaluation hook: provenance export"
about: "Export the production, decision and verification layers per item"
title: "[antrag-eval] Provenance export"
labels: ["antrag-eval"]
---

## Purpose

Expose, per item, which layer produced a statement, who decided about it, and
how it was checked, so that provenance can be compared across tools without
first agreeing on evaluation criteria.

## Expected export, per item

- **Production layer**: what generated the state (model and version, prompt
  group, rule, or human transcription), with its timestamp.
- **Decision layer**: what was kept, changed, or rejected, by whom (human,
  agent, rule), with its timestamp.
- **Verification layer**: the trust tier reached, the verifying instance, and
  the evidence the tier rests on.

## Notes

- The three layers exist in the data today across `review`, `edit_history`,
  `transcription_llm`, `quality_signals`, and the Page-JSON `provenance` block.
  The hook consolidates them into one addressable record per item.
- The layers stay separate in the export. No field may merge them into a single
  reliability value.
- States superseded by a correction are part of the record, not a deletion.

## Out of scope

Alignment with any external provenance vocabulary; that is a separate decision.
