# SZD OCR/HTR Pipeline

VLM-based handwritten text recognition (HTR) and OCR for the Stefan Zweig estate at the [Literaturarchiv Salzburg](https://www.literaturarchiv.at/), an experimental sub-project of [Stefan Zweig Digital](https://stefanzweig.digital/).

**[Live Viewer & Catalogue](https://chpollin.github.io/szd-htr-ocr-pipeline/)** shows all transcriptions with facsimile comparison, quality signals and search.

## Purpose

The pipeline produces machine-readable text from the digitised facsimiles of the estate (manuscripts, correspondence, typescripts, personal documents) using Google's Gemini 3.1 Flash Lite (preview, configurable through `HTR_MODEL`). The project is also a methodological experiment in how far AI-assisted Promptotyping carries a complete Digital Humanities pipeline, see [How this was built](#how-this-was-built).

A July 2026 research synthesis is retained in [`paper/PAPER.md`](paper/PAPER.md), with its evidence base in [`paper/PAPER-FINDINGS.md`](paper/PAPER-FINDINGS.md). The manuscript is a historical research artefact and has no active submission target. The maintained conceptual account lives in [`knowledge/editorial-methodology.md`](knowledge/editorial-methodology.md).

### Approach

The pipeline combines a layered prompt system with automated quality assessment.

1. Context resolution. TEI-XML metadata provides title, language and object type. One of nine prompt groups is assigned automatically (handwriting, typescript, form, short text, tabular, galley proof, convolute, newspaper clipping, correspondence).
2. VLM transcription. All facsimile images of an object plus a tailored prompt are sent to the model. Large objects are chunked and merged.
3. Quality signals. Rule-based signals (page-type classification, duplicate detection, language consistency and others) flag objects for manual review.
4. Verification. Agent-based checks compare each transcribed page against its facsimile image, and human review happens in the local workspace (see [Trust tiers](#trust-tiers-and-verification-provenance)). Cross-model consensus (Flash Lite and Flash, Claude as judge) was run on a stratified sample in April 2026 and remains a selective diagnostic. It measures agreement between models, which says nothing about correctness when models share an error, so it sets no trust tier.

Transcription is diplomatic, without normalisation. Markup: `[?]` uncertain, `[...]` illegible, `~~...~~` struck through, `{...}` insertion. The full rules are in [`knowledge/transcription-guidelines.md`](knowledge/transcription-guidelines.md).

### Trust tiers and verification provenance

Every object records how far it has been checked and by which instance. Four tiers live in the `review` block of the result JSON. They are stored states, never derived from a score.

| Tier | `review.status` | Source | Visual |
|---|---|---|---|
| 0 | `gt_verified` | Character-exact human verification against the facsimile, ground-truth capable | dark green |
| 1 | `approved` | Human expert review in the workspace | green |
| 2 | `agent_verified` | Claude Vision sub-agent compares each page against its image | slate |
| 3 | no `review` block | Machine transcription only, not yet checked | gray, amber when flagged |

`needs_review` from the quality signals is not a tier. It is a triage hint inside tier 3, set by the rule-based signals, and it says what to look at first rather than how reliable a text is. The display layer (`docs/app.js`) groups tiers 0 and 1 as "human-checked"; the stored values keep them apart.

Machine states survive human correction. On the first edit of a page, `pipeline/serve.py` writes the raw model output once into `transcription_llm` and appends an entry to that page's `edit_history` carrying the text before the change, the timestamp, and a `source` field that separates human from agent corrections. `transcription` holds the current working text. Because the machine state is preserved, every human correction doubles as a CER measurement against the raw output (`pipeline/report_cer_from_edits.py`, report in `reports/cer-from-edits.md`).

There is no single confidence value. The checking tier, the model's own categorical confidence (`result.confidence`, high/medium/low) and the rule-based quality signals remain separate fields in the data and separate filters in the viewer. Nothing in the pipeline combines them into one number. Categorical rather than numeric confidence was an early project decision, taken because the models do not assess their own output reliably on a numeric scale.

Tier 0 is implemented end to end, as the GT Verify action in the viewer and as an accepted status in the review API. Live counts per tier are in `docs/catalog.json`; the tests pinning the transitions are in `tests/test_trust_tiers.py`.

## Data and rights

The corpus consists of the digitised objects of five collections, fully available in a local backup with metadata. Object and image counts, sizes, languages and hands per collection are in [`knowledge/data.md`](knowledge/data.md); current processing figures come from `docs/catalog.json`.

| Collection | Metadata source |
|---|---|
| Personal documents | [TEI](https://stefanzweig.digital/o:szd.lebensdokumente/TEI_SOURCE) |
| Works (manuscripts) | [TEI](https://stefanzweig.digital/o:szd.werke/TEI_SOURCE) |
| Essay collection | [TEI](https://stefanzweig.digital/o:szd.aufsatzablage/TEI_SOURCE) |
| Correspondence | Backup metadata |
| Letter convolutes (SZ-AAL) | Backup metadata |

The material is predominantly German, with smaller English, French, Italian and Spanish shares according to the TEI metadata. Facsimiles are high-resolution JPEGs served via [GAMS](https://gams.uni-graz.at/) (University of Graz) and do not need to be stored locally.

The transcriptions and their underlying facsimiles derive from the Stefan Zweig estate held by the Literaturarchiv Salzburg (Paris Lodron University of Salzburg). Those rights remain with the archive.

## Use

### Setup

Python 3.10+ (tested with 3.11). Transcription requires a [Google AI API key](https://ai.google.dev/).

```bash
pip install -r requirements.txt
# Create .env with: GOOGLE_API_KEY=AIza...
```

### Tests

No API key and no local image backup are needed.

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ pipeline/
```

`tests/` holds the schema check of the exported Page-JSON against `schemas/page-json-v0.2.json`, the trust-tier transitions of the review API, the salvage logic and the aliases of the knowledge documents. `pipeline/test_*.py` holds the older regression checks for the TEI export, the marker converter, the canonical collection assignment, the quality signals, and the unit derivation; each of those also runs standalone as `python pipeline/test_<name>.py`.

### Pipeline

```bash
# Transcribe a single object
python pipeline/transcribe.py o_szd.161 -c lebensdokumente

# Transcribe an entire collection
python pipeline/transcribe.py -c lebensdokumente

# Transcribe everything
python pipeline/transcribe.py --all

# Dry run (list without API calls)
python pipeline/transcribe.py --all --dry-run

# Rebuild viewer data
python pipeline/build_viewer_data.py

# Local dev server with review API
python pipeline/serve.py
```

Results are stored as JSON in `results/{collection}/`. Two export formats exist, Page-JSON v0.2 (internal working format with descriptive metadata) and METS/MODS + PAGE XML (archival exchange format, compatible with GAMS, Transkribus, eScriptorium, OCR-D). Pipeline script documentation: [`pipeline/README.md`](pipeline/README.md). Result file documentation: [`results/README.md`](results/README.md).

### Publication

The viewer is published on GitHub Pages from `docs/` and redeployed automatically on every push to `main`. The public site is the read-only proto-edition.

### Running locally for editing

The same static viewer that serves the read-only proto-edition on GitHub Pages becomes an editorial workspace when run locally. No additional code or separate tool is involved, only the deployment context changes. This is the architectural core of the project: the public site is a subset of the local site, reached by disabling the editing controls. Step-by-step instructions for reviewers are in [`SETUP-REVIEW.md`](SETUP-REVIEW.md) and, as a command-only version, [`SETUP-REVIEW-KURZ.md`](SETUP-REVIEW-KURZ.md).

```bash
pip install -r requirements.txt
python pipeline/serve.py              # serves at http://localhost:8000
python pipeline/serve.py --port 5501  # alternative port
```

Opening `http://localhost:8000` shows a terminal-style Editorial Workspace banner above the header (`szd@editorial:~/results $`) and an additional Editorial Workspace dashboard above the catalogue. Both are hidden on GitHub Pages. Edits made in this mode are written directly to the pipeline JSONs in `results/{collection}/`, not to browser `localStorage`.

The Editorial Workspace dashboard (local only) makes the Git-based workflow visible in three cells:

- Recent Activity lists the latest commits touching `results/`, fetched live from the GitHub API, and links each row to the commit on GitHub.
- Uncommitted counts modified files under `results/`. It turns amber when edits are pending and green when the working tree is clean, backed by `GET /api/git-status`.
- Quick Actions offers copy-to-clipboard commands for the standard loop: commit edits, rebuild viewer data, export METS/MODS, pull latest.

The Project Transparency panel (public and local) sits below the catalogue statistics and makes the project's methodological decisions and evidence inspectable:

- Promptotyping Vault enumerates the Markdown documents in `knowledge/` with in-app links.
- Research Journal links to `knowledge/journal.md` and shows its number of entries.
- Exports & Artefacts links to `results/`, to the METS/MODS + PAGE-XML architecture and to the Page-JSON v0.2 format specification.

#### Review workflow

1. Open an object in the viewer.
2. Click Edit to correct transcription errors page by page.
3. Click Approve (human expert review), Agent Verify (Claude Vision comparison against facsimile), or GT Verify (character-exact ground-truth confirmation).
4. Check the Curation Progress bar on the catalog page, whose counts shift as reviews accumulate.
5. Commit and push the changed JSONs:

```bash
git add results/
git commit -m "Correct the transcription of <object-id>"
git push
```

The next GitHub Pages deploy carries the curated edits into the public proto-edition. The Curation Progress bar renders the tiers described under [Trust tiers](#trust-tiers-and-verification-provenance) as a stacked bar, from the outer ring (machine transcription) on the left to the inner ring (expert-verified critical edition) on the right. This follows Vogeler's concentric edition model (2025): one artefact, multiple editorial states, curation that deepens incrementally.

#### API endpoints (local only)

`pipeline/serve.py` exposes four endpoints that the frontend calls automatically when `location.hostname` is `localhost` or `127.0.0.1`:

- `POST /api/edit` saves an edited transcription for a page and sets `reviewStatus=approved`
- `POST /api/approve` marks an object as reviewed (`approved`, `agent_verified`, or `gt_verified`)
- `GET  /api/status` is the frontend probe; it is absent on GitHub Pages, so edit buttons stay hidden
- `GET  /api/git-status` returns count and filenames of uncommitted changes under `results/`

Edits on the public site fall back to `localStorage` (single browser, not persistent across machines). The same UI, code base and URL serve both roles, and only the presence of a server switches the role from proto-edition to editorial workspace.

## How this was built

The repository was built with [Promptotyping](https://dhcraft.org/Promptotyping/), an iterative method in which a domain expert directs a coding agent through maintained project knowledge. The project lead defined requirements, evaluated results and took directional decisions without writing the code; from July 2026 the project reviewer at the University of Salzburg also corrected transcriptions and committed changes, partly through the agent. The harness was Claude Code. The Co-Authored-By trailers of the commits name Claude Opus 4.6 for the build phase from March to April 2026, and Claude Opus 4.8, Claude Fable 5, Claude Opus 5 and Claude Opus 5.5 for later work; commits without a trailer do not record whether an agent was involved (`git log --format='%h %(trailers:key=Co-Authored-By,valueonly)'`). The project knowledge lives in German in [`knowledge/`](knowledge/INDEX.md), and [`CLAUDE.md`](CLAUDE.md) is the agent's entry point.

Checking is layered. Verification runs automated tests on schema, trust-tier transitions and salvage logic, and rule-based quality signals flag objects for review. Agentic review compares each page with its facsimile in a vision agent that records `agent_verified`, and adversarial multi-agent reviews have audited pipeline stages such as the TEI marker conversion. Scholarly validation lies with the project reviewer, who checks transcriptions against the facsimiles; only humans set `approved` and `gt_verified`, and the reviewer's observations stand as `[J]` paragraphs in [`knowledge/review-findings.md`](knowledge/review-findings.md). Commit `6f06c8e` is the state before the knowledge base was aligned with the Promptotyping document templates on 2026-10-28. The episodes in which a verification layer caught or missed an error are recorded in [`knowledge/journal.md`](knowledge/journal.md).

## Limits

- Transcription runs on a proprietary preview model behind a paid API, and its output varies between runs at the configured temperature (`knowledge/transcription-verification.md`, section 4.3). Re-running the pipeline does not reproduce the stored results. The committed result files, including the raw model output, are the record.
- Human-verified reference text is scarce. Only part of the ground-truth drafts has been reviewed, so error rates rest on a small human-checked base and on agent checks, which are a model checking a model. Current tier counts are in `docs/catalog.json`.
- The model's self-assessed confidence does not discriminate reliably, and recurring error types (Kurrent letter confusions, invented words instead of `[?]`, tabular linearisation, repetition loops) are described in `knowledge/transcription-verification.md` §2 and §9.
- Open work, among it rerunning incomplete transcriptions and calibrating the quality signals against ground truth, is tracked in [`knowledge/plan.md`](knowledge/plan.md).

## Licence and citation

- Code (pipeline, viewer, tooling): [MIT](LICENSE).
- Documentation, knowledge documents, and other textual content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Third-party research data: the transcriptions and their underlying digitised facsimiles derive from the Stefan Zweig estate held by the Literaturarchiv Salzburg (Paris Lodron University of Salzburg); those rights remain with the archive.

Citation metadata is in [`CITATION.cff`](CITATION.cff) and [`codemeta.json`](codemeta.json).

## Related projects

- [zbz-ocr-tei](https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei), LLM-OCR pipeline for printed texts
- [coOCR HTR](https://github.com/DigitalHumanitiesCraft/co-ocr-htr), browser-based HTR with expert-in-the-loop
- [teiCrafter](https://github.com/DigitalHumanitiesCraft/teiCrafter), TEI annotation as a downstream pipeline stage (separate repo)

## Contact

Technical implementation: Christopher Pollin, [Digital Humanities Craft OG](https://dhcraft.org/)
