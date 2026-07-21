# PAPER-TEXT-FILLED.md

This file is the filled product: a copy of PAPER-TEXT.md with the seven
placeholders replaced by passages drafted from repository evidence. The
evidence for each passage is recorded in PAPER-FINDINGS.md under "Draft
passages"; divergences between the fixed text and the repository are recorded
there under "Divergences". PAPER-TEXT.md remains untouched.

---

The Static Proto-Edition as Editorial Workspace. Promptotyping an OCR/HTR
Pipeline as Editor-in-the-Loop Research Tool for the Stefan Zweig Estate.

Christopher Pollin (Digital Humanities Craft OG), Lina Maria Zangerl
(Literaturarchiv Salzburg), Julia Hintersteiner (Universität Salzburg)

Digital scholarly editions usually split publication and editorial work
between a public reading interface and a server-backed editing environment.
Long-term maintenance falls disproportionately on the server side, which is
why small-to-mid-sized projects struggle to keep their editions running. We
report on how Promptotyping, a context-engineering method for LLM-driven
development (Pollin 2026), can be used to build static browser applications
that take on these roles. Because the corpus is populated by an LLM-driven
OCR/HTR pipeline, the same interface also serves as the verification layer
for the pipeline output, a role that would normally fall to separate tooling.
One code base carries all three functions; publication and editing are
switched by where the code runs, verification by the phase in which it is
used.

The result can be situated within Vogeler's concentric edition model
(Vogeler 2025), which treats the various degrees of editorial engagement with
a source, from archival description through machine-generated transcription
to full critical edition, as nested rings that projects traverse from outside
in as resources allow. The pipeline occupies the middle rings, pairing
machine-generated transcription with facsimile and existing metadata to
produce what Vogeler calls a proto-edition (Vogeler 2022), a publishable
in-progress state that does not claim critical authority. The repository
records the degree of editorial engagement per object rather than leaving it
a metaphor. Each result JSON may carry a review block whose status takes the
values approved, gt_verified, and agent_verified, an absent block being read
as unreviewed, and every correction is written into a per-page edit_history
that stamps each change with its source, human or agent. An object's position
between machine transcription and human-authorised text is therefore a
readable property of the files, which the built catalogue exposes as a status
column, so the movement inward through Vogeler's rings has a concrete
correlate in the data.

The demonstration case is the SZD OCR/HTR pipeline, built for the Stefan
Zweig estate. Stefan Zweig Digital (stefanzweig.digital), a low-resource
project running since 2017, reconstructs an estate that exile dispersed
across multiple collections. The pipeline transcribed a corpus of roughly
2,450 canonical objects across five collections, some 20,300 facsimile scans
at about 25.6 GB, spanning legal papers, manuscripts, galley proofs,
newspaper clippings, and handwritten letters, in German at 95.6 percent with
English, French, Italian, and Spanish in the remainder. The transcription
model is priced at 0.25 USD per million input tokens, and the documented
costs are confined to sub-experiments, a three-model ground-truth run over
eighteen objects at about eight to twelve USD and per-page vision
verification at about 0.001 USD; no total cost or wall-clock duration for the
full production run is recorded in the repository. The prompting is a layered
stack assembled per object, a shared system prompt fixing the
diplomatic-transcription rules and a mandatory JSON schema, one of nine group
prompts selected automatically from the TEI object type, an optional
per-object override, and a context string derived from the object's TEI
metadata. Transcription runs on gemini-3.1-flash-lite-preview, chosen for low
cost, speed, a one-million-token context, and multimodality, and the output
is exported for archival exchange along three paths, an internal Page-JSON
working format, a METS container with MODS and one PAGE XML file per page,
and a deterministic, LLM-free conversion to teiCrafter-loadable TEI. Each
object's primary result file is already structured as edition data, carrying
object and collection identifiers, TEI-derived descriptive metadata, and a
result block of per-page transcriptions with a categorical confidence value
and pipeline-assigned page types (content, blank, color_chart). On the first
correction each page gains an immutable transcription_llm field holding the
raw model output alongside an edit_history, so provenance and current text
sit in one structure, which is what lets a single code base serve
publication, editing, and verification. Results are live at
chpollin.github.io/szd-htr-ocr-pipeline.

The public deployment on GitHub Pages serves as a read-only proto-edition:
catalogue, facsimile-text viewer, and quality dashboard. Quality is assessed
by text-statistical signals computed after transcription without any further
API call, of which version 1.6 drives its triage from three, a page-length
anomaly against the collection median, a page-to-image count mismatch, and a
language mismatch, while further signals remain informational. Validated
against agent-verified objects these reach full precision for the length and
image-mismatch signals and lower precision for language mismatch, so the
interface flags suspect objects where scoring against an absent reference is
impossible. The same code base, cloned and run locally, activates the editing
controls. A local server writes corrections back to JSON files on disk; Git
commits and pull requests carry curated edits into the public deployment. The
two server roles that classical edition stacks require, persistence and
multi-user coordination, are absorbed by the local filesystem and Git. For
the developer, the interface functions as a verification environment during
pipeline development, surfacing transcription errors, structural pipeline
failures, and weaknesses in prompt design before expert review begins.

Promptotyping guides this development. Promptotyping is materially present as
a set of steering documents; a root CLAUDE.md guides the AI development,
Plan.md is a phased roadmap with a dated decision log, and a knowledge vault
of thirteen Markdown documents indexed by index.md holds the data overview,
verification concept, evaluation results, and format specifications. The
process is logged in a research journal of dated sessions from March to June
2026 that functions as the audit trail, so the repository is at once the
product and its own record. The journal's session numbering is reused and its
dated headers run out of chronological order toward the end, consistent with
a log accreted as the work proceeded. This lowers the barrier for building
such interfaces considerably, but does so by relying on proprietary frontier
models for both development and transcription. Static output is durable; the
process that produces it is not. What is not durable is the dependence on the
proprietary Gemini API for both transcription and layout, mitigated in the
repository by committing every result JSON to Git and by the deterministic,
LLM-free exports into open formats, PAGE XML, METS with MODS, and
teiCrafter TEI, that outlast the API. Rather than resolving this tension, the
report situates it within the broader discussion of sustainability and
minimal computing in digital scholarly editing.
