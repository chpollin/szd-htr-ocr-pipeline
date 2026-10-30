# Research manuscript archive

This directory retains the July 2026 manuscript and the material from which it was written. The project decided on 21 August 2026 that this manuscript will not be submitted. Its maintained findings have been integrated into `knowledge/editorial-methodology.md`, `knowledge/transcription-verification.md` (with the dated measurements in `reports/cer-baseline-report-2026-04-02.md`), and `knowledge/architecture.md`.

| File | Status | Function |
|---|---|---|
| `PAPER.md` | archived | Dated research synthesis of the repository as it stood in July 2026 |
| `PAPER-FINDINGS.md` | archived | Evidence base for the dated manuscript, including repository citations and recorded divergences |
| `drafts/PAPER-TEXT.md` | superseded | Earlier co-authored text with seven marked placeholders |
| `drafts/PAPER-TEXT-FILLED.md` | superseded | The same text with the placeholders filled from the findings |
| `drafts/CLAUDE-TASK.md` | superseded | The working instruction under which the findings and the filled text were produced |

`PAPER.md` is not maintained against later changes. One reference in it has since moved. The phased roadmap it names as `Plan.md` now lives at `knowledge/plan.md`. Current project knowledge follows the source hierarchy in `knowledge/editorial-methodology.md`.

One figure in both archived files names the wrong correction source. `PAPER.md` (section on error rates) and `PAPER-FINDINGS.md` (accuracy figures) describe a corpus CER of 0.962 percent over 56 edited pages in 40 objects as measured against human corrections. An audit on 30 October 2026 found that all of these pages had been corrected by the vision agent (review status `agent_verified`), because `pipeline/report_cer_from_edits.py` did not separate correction sources. The script now reports each source separately. The rerun of that date gives 0.948 percent for the agent-corrected pages (56 pages, 40 objects) and 11.875 percent for the human-corrected pages (34 pages, 23 objects, status `approved`), with 27 human-checked objects without edits reported apart (`reports/cer-from-edits.md`). The archived files keep their July 2026 wording; read the figure there as agent-corrected.

The knowledge base was renamed on 28 October 2026. The knowledge file names cited in `PAPER.md` and `PAPER-FINDINGS.md` map to the current documents through the table of former file names in `knowledge/INDEX.md`.
