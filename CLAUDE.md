<!-- template: Vorlage Action-Layer v0.5, https://dhcraft.org/Promptotyping/promptotyping-document/action-layer -->

# Project instructions for SZD OCR/HTR Pipeline

VLM-based HTR/OCR pipeline for the Stefan Zweig estate at the Literaturarchiv Salzburg, an experimental sub-project of [Stefan Zweig Digital](https://stefanzweig.digital/). The method is Promptotyping. The documents in `knowledge/` hold the domain knowledge, specification and architecture from which the code is implemented. The project lead decides on the substance and does not write the code. The project reviewer (University of Salzburg) checks the results against the material. Roles and model involvement are in `knowledge/project.md`.

- GitHub: https://github.com/chpollin/szd-htr-ocr-pipeline
- Python 3.10+ (tested with 3.11)
- Licence: see `README.md`, section Licence and citation

## Knowledge base

The knowledge base lives in `knowledge/` and is written in German, a project decision recorded in `knowledge/INDEX.md`. At every session start, after this file, read `knowledge/INDEX.md`, then `knowledge/handoff.md` and `knowledge/plan.md`, then the document relevant to the task. Consult `knowledge/journal.md` when the origin or reason of a transition is needed.

| Task | Read first |
|---|---|
| Project frame, roles, licence | `knowledge/project.md` |
| Source data, collections, backup, languages | `knowledge/data.md` |
| Requirements, review model, result JSON, output formats, decision log | `knowledge/specification.md` |
| Data flow, prompt system, components, environment variables, METS/MODS/PAGE XML, security | `knowledge/architecture.md` |
| Page-JSON format | `knowledge/page-json-architecture.md` |
| Layout analysis | `knowledge/layout-analysis-architecture.md` |
| Transcription rules and markup | `knowledge/transcription-guidelines.md` |
| Quality signals, verification, error types, known model limits | `knowledge/transcription-verification.md` |
| Status, approval, authority | `knowledge/governance.md` |
| Accepted work and open decisions | `knowledge/plan.md` |
| Open input or handover | `knowledge/handoff.md` |
| Origin or reason of a decision unclear | `knowledge/journal.md` |

## Working rules

- Handoff. Read `knowledge/handoff.md` at every session start. Check source and current target of each point you use, integrate durable content first, write the journal record, then remove the point completely.
- Journal. Write one entry per coherent transition at the end of `knowledge/journal.md`. Past entries stay unchanged.
- Authority. Only humans set `approved` and `gt_verified`. Paragraphs marked **[J]** (observations of the project reviewer) are never reworded. The full rules are in `knowledge/governance.md`.
- Invent nothing. Figures come from code, result data or `reports/`, transcription rules from `knowledge/transcription-guidelines.md`. Ask when knowledge is missing.
- Truth hierarchy. Code and result data precede `knowledge/`, `knowledge/` precedes `reports/` and `paper/`. Report contradictions instead of letting them diverge silently.
- No volatile figures in this file or in knowledge documents. Current figures come from `python pipeline/transcribe.py --all --dry-run` and `docs/catalog.json`. Future work belongs in `knowledge/plan.md`, dated measurement and audit reports in `reports/`.
- After changing `knowledge/` or `README.md`, rebuild the viewer data with `build_knowledge()` (see Commands), because the viewer renders both.

## Design principles

The viewer follows the SZD design system in `docs/app.css`. There is no separate `design.md`. Binding:

- Keep the checking status visible per object and never condense it into a global score.
- Show editing controls only in local operation.
- Output every interpolated string through `escapeHtml()`. No runtime CDNs, libraries are vendored under `docs/lib/`.

## Scope

What this project does not do:

- critical edition or prosopographical indexing (`knowledge/project.md`, Abgrenzungen)
- reproducible recomputation of the model outputs (`knowledge/architecture.md`, Abhängigkeitsgrenze)

What you must not do:

- change `paper/PAPER.md` or `paper/PAPER-FINDINGS.md`, which stay frozen at their July 2026 state
- rewrite past journal entries or **[J]** paragraphs

## Known limits

The recurring model errors (Kurrent confusions, invented words instead of `[?]`, repetition loops, tabular linearisation, false duplicate-page signals on colour-chart double shots) are described in `knowledge/transcription-verification.md` §2 and §9 and in `reports/pipeline-totalausfaelle.md`. Treat gaps listed there as known limits rather than new bugs.

## Tools

Before dependent steps, check the available tools, runtimes and connections. A missing binding rule source holds the dependent change. Name checks you did not run. A received document or available tool does not widen the task.

### Commands

```bash
# Setup (.env needs GOOGLE_API_KEY; further variables in knowledge/architecture.md)
pip install -r requirements.txt

# Transcription (results go to results/{collection}/{object_id}_{model}.json; existing ones are skipped without --force)
python pipeline/transcribe.py o_szd.161 -c lebensdokumente     # single object
python pipeline/transcribe.py -c werke                          # collection
python pipeline/transcribe.py --all --dry-run                   # list without API calls
# Further options: --group, --limit N, --max-images N, --chunk-size N, --delay 2.0, --force

# Local dev server with review API
python pipeline/serve.py [--port 5501] [--rebuild]

# Review import (CLI alternative)
python pipeline/import_reviews.py path/to/export.json [--dry-run] [--reviewer "Name"]

# Viewer data
python pipeline/build_viewer_data.py                                                   # everything
cd pipeline && python -c "from build_viewer_data import build_knowledge; build_knowledge()"  # knowledge.json only

# Exports
python pipeline/export_page_json.py --all [--force]             # Page-JSON v0.2
python pipeline/export_mets.py --all [--dry-run]                # METS/MODS
```

Tests run without an API key or local image backup and are mandatory before every commit:

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ pipeline/
```

`tests/` checks Page-JSON against `schemas/page-json-v0.2.json`, the trust-tier transitions of `serve.py`, the salvage logic and the aliases of the knowledge documents. `pipeline/test_*.py` are older regression tests that also run standalone.

### Conventions

- Renamed knowledge documents keep their former file name under `aliases:`. `build_knowledge()` redirects old links through it.

### Security

- Never read or print `.env`. Secrets live only in environment variables. `.env` is gitignored and has never been in the Git history.
