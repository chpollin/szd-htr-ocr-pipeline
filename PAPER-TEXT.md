# PAPER-TEXT.md

This file is the product: the paper text under revision. Placeholders of the
form `{{P-N: ...}}` mark passages to be written from repository evidence.
Each placeholder states only what the passage must establish for the
argument, not what the repository is expected to contain. How to work on
this file is defined in CLAUDE-TASK.md; evidence lives in PAPER-FINDINGS.md.

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
in-progress state that does not claim critical authority. {{P-1: 2-3
sentences on how the system relates expert correction to Vogeler's model.
The passage must establish whether, and if so how, the movement from
proto-edition toward critical edition has a correlate in the data, i.e.
whether an object's degree of editorial engagement is recorded and readable
from the files rather than remaining a metaphor. Describe the mechanism the
repository actually implements, in its own terms. If the data does not record
editorial engagement, the claim of extending Vogeler's model must be scaled
back accordingly, and this passage instead states precisely what the system
does and does not capture.}}

The demonstration case is the SZD OCR/HTR pipeline, built for the Stefan
Zweig estate. Stefan Zweig Digital (stefanzweig.digital), a low-resource
project running since 2017, reconstructs an estate that exile dispersed
across multiple collections. {{P-2: 2-3 sentences that substantiate, with
figures from the repository, the claim that frontier LLMs make corpus-scale
transcription feasible for a project of this size: the scale of what was
processed, the nature of the material, and what it cost in money and time,
to the extent the repository documents this.}} {{P-3: 1-2 sentences that open
the black box of the transcription setup: how the prompting is actually
organised, which model is used and why, and how the output is exported for
archival exchange. Describe the structure as found, whatever its shape.}}
{{P-4: 1-2 sentences on the structure of the pipeline output per object. The
argumentative point to establish, if the data supports it: the output is
already structured as edition data rather than raw OCR output, which is what
makes a single code base for publication, editing, and verification
possible.}} Results are live at chpollin.github.io/szd-htr-ocr-pipeline.

The public deployment on GitHub Pages serves as a read-only proto-edition:
catalogue, facsimile-text viewer, and quality dashboard. {{P-5: 1-2 sentences
on how quality is assessed in the absence of ground truth, as actually
implemented. This carries the claim that the interface functions as a
verification layer.}} The same code base, cloned and run locally, activates
the editing controls. A local server writes corrections back to JSON files on
disk; Git commits and pull requests carry curated edits into the public
deployment. The two server roles that classical edition stacks require,
persistence and multi-user coordination, are absorbed by the local filesystem
and Git. For the developer, the interface functions as a verification
environment during pipeline development, surfacing transcription errors,
structural pipeline failures, and weaknesses in prompt design before expert
review begins.

Promptotyping guides this development. {{P-6: 2-3 sentences on how
Promptotyping is materially present in the repository: which documents steer
the LLM-driven development, how the process is documented, and how the
repository is organised, so that the claim that the repository is both the
product and its own audit trail rests on its actual structure. Describe what
is there, in its own terms; if the practice deviates from the published
method, that deviation is a finding worth stating.}} This lowers the barrier
for building such interfaces considerably, but does so by relying on
proprietary frontier models for both development and transcription. Static
output is durable; the process that produces it is not. {{P-7: 1 sentence
naming, from the repository, what exactly is not durable about the process
and what, if anything, in the repository mitigates this.}} Rather than
resolving this tension, the report situates it within the broader discussion
of sustainability and minimal computing in digital scholarly editing.
