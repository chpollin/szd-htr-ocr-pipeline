# CLAUDE-TASK.md — Working instructions for this repository

> **Archived working instruction.** This task produced the superseded draft and evidence files in July 2026. It must not be executed as a current publication task.

You are preparing the empirical basis for a paper about this repository, the
SZD OCR/HTR pipeline. The paper text with marked gaps is in PAPER-TEXT.md.
Your work has two phases, in strict order. Do not modify pipeline code or
data.

## Phase 1 — Exploration

Understand this repository as a whole before looking at the paper text.
Explore its structure, its data and data flow from input to published
output, its interface code, its prompts, its documentation, and its history
as visible in JOURNAL.md and the Git log. Describe what you find in your own
terms, not in terms of what a paper might want to say about it. Pay
attention to how the parts relate, and note anything surprising,
inconsistent, undocumented, or more interesting than its documentation
suggests.

Write this up as the first part of PAPER-FINDINGS.md: a structured account
of what this repository is and how it works, with file citations for every
factual statement.

## Phase 2 — Mapping to the paper text

Only now read PAPER-TEXT.md in full. For each placeholder P-1 to P-7, draft
the passage from your Phase 1 findings, following the placeholder's
statement of what the passage must establish. Then check the fixed text
surrounding the placeholders against your findings as well; where the fixed
text asserts something the repository does not support, or where the
repository is more interesting than the assertion, do not silently rewrite
it, but record it in PAPER-FINDINGS.md under "Divergences" with a proposed
correction.

Add the drafted passages to PAPER-FINDINGS.md under "Draft passages", each
followed by the evidence it rests on. Then produce a filled copy of the
paper text as PAPER-TEXT-FILLED.md, leaving PAPER-TEXT.md untouched.

## Rules

- Every figure and every mechanism you state must trace to a cited file. If
  the repository does not contain the evidence a passage needs, leave the
  placeholder unfilled and record the gap, including the smallest change to
  the repository that would close it.
- Findings first, prose second. Never draft a passage whose evidence section
  is empty.
- Register for drafted passages: precise, matter-of-fact academic English
  matching the surrounding text; no hedging formulas, no evaluative filler,
  no bullet lists inside passages.
- The filled text should grow by roughly 150-250 words over the version with
  placeholders, not more.

## Definition of done

You are done when PAPER-FINDINGS.md contains the Phase 1 account, one
evidence-backed draft or documented gap per placeholder, and the Divergences
section (possibly empty, stated as such), and PAPER-TEXT-FILLED.md exists.
Human review of findings against drafts follows; do not iterate beyond this
point on your own.
