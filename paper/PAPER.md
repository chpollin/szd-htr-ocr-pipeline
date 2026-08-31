# Knowledge Engineering and Agentic Engineering in an OCR/HTR Pipeline for the Stefan Zweig Estate

The Static Proto-Edition as Editorial Workspace

Christopher Pollin (Digital Humanities Craft OG)

July 2026

> **Status since 21 August 2026.** This manuscript will not be submitted for publication. It is retained as a dated research synthesis and bibliography. Maintained project findings now live in `knowledge/editorial-model.md`, `knowledge/evaluation-results.md`, and `knowledge/page-xml-mets-architecture.md`.

## Abstract

Digital scholarly editions usually split publication and editorial work between a public reading interface and a server-backed editing environment, and the maintenance of the server side is where small projects struggle to keep their editions running. We report on a system for the Stefan Zweig estate in which one static browser application carries publication, expert correction, and pipeline verification, switched by where the code runs. System and corpus were produced with frontier models and an AI agent. These models are black boxes in a precise sense, their computation offers no decision logic a researcher could inspect, so every model contribution is recorded in the data with explicit provenance and kept separable from human judgement. The report centres the relation between researcher and AI agent. Knowledge engineering names the structuring of project knowledge into the documents that steer the agent, agentic engineering the discipline that keeps its work accountable. Vogeler's concentric model of editions supplies the editorial frame in which the recorded degree of expert engagement per object becomes readable. We report evaluation results together with their validity limits and situate the sustainability tension of durable static output produced by rented capability.

## 1 Introduction

Digital scholarly editions typically divide their labour between two environments. A public reading interface presents facsimiles, transcriptions, and metadata; a server-backed editing environment holds the databases, accounts, and workflows through which the edition is produced and revised. Long-term maintenance falls disproportionately on the second environment. Databases need migrations, frameworks need updates, servers need administration, and when funding ends, this is where editions begin to die. The minimal computing discussion in the digital humanities has drawn the consequence for publication, arguing for static delivery without running server components (Risam and Gil 2022; Diaz 2018). The editorial workspace, however, has largely stayed on the server side of the divide, because editing seems to require what static sites by definition lack, write access and coordination between editors.

This report describes a system in which the editorial workspace itself is static. The system was built for Stefan Zweig Digital (stefanzweig.digital), a low-resource project whose platform launched in June 2018[^1] and which reconstructs an estate that exile dispersed across multiple collections. A VLM-based OCR/HTR pipeline transcribes the digitised holdings; a single static single-page application publishes the results, and the same code base, run locally, becomes the environment in which curators correct them and in which the developer verifies pipeline behaviour. Persistence and multi-user coordination, the two services that classical edition stacks buy with a server, are absorbed by the local filesystem and by Git.

We read the construction of this system through two terms. Knowledge engineering, in its classical sense the elicitation and structuring of domain knowledge into machine-usable form, returns under agent-driven development as the authoring of steering documents that carry project knowledge into each interaction with the agent; Promptotyping (Pollin 2026) is the method used here. Agentic engineering denotes the complementary discipline of organising what an AI agent does and how its work remains accountable; in this project the agent occupies two distinct positions, as the developer of pipeline and interface and as a verification instance whose interventions are recorded in the editorial data model with explicit provenance. Both terms are demonstrated at a single case that is fully verifiable against its public repository; an evidence file (PAPER-FINDINGS.md) documents, for every factual claim, the repository file that supports it.

Section 2 situates the system in editorial theory. Sections 3 and 4 describe the pipeline and the workspace. Section 5 reports quality assessment together with its validity limits. Section 6 develops the two engineering perspectives, and section 7 addresses sustainability.

## 2 Editorial Engagement as a Property of the Data

Vogeler treats the degrees of editorial engagement with a source as a continuum. The proto-edition (Vogeler 2022) names a publishable intermediate form, deep archival indexing plus digital facsimile, that deliberately withholds the claim of a critical edition while already enabling historical research. The concentric edition (Vogeler 2025) generalises this into five nested rings, digitisation, deep indexing, proto-edition, artificial edition, and full critical edition, which projects traverse from the outside in as resources and scholarly relevance allow. The artificial edition, a term Vogeler adopts from Stutzmann (2019), is the ring most affected by machine learning; it has the surface properties of an edition but a different epistemological status, automatically learned probabilities in place of expert-authorised assertions. Hodel (2023) draws the practical consequence for text recognition, a shift of scholarly labour from transcription toward validation.

Placed in the wider theory, this frame answers to Sahle's principle of technical relativity, by which editorial concepts are bound to their media and technologies, a principle that legitimates asking how frontier models change what an edition can be (Sahle 2013). Pierazzo's distinction between haute couture and prêt-à-porter editing marks the scaling question, whether semi-automated pipelines can serve scholarly standards (Pierazzo 2019). Van Zundert's warning about paradigmatic regression cuts the other way; a new technology can be socially shaped until it merely reproduces print metaphors and accelerates existing workflows (van Zundert 2016). An LLM pipeline that outputs static pages runs an obvious risk of exactly this regression.

The system's answer to the epistemological question and to the regression risk is the same, editorial engagement becomes a recorded property of the data. Each result file may carry a review block whose stored status takes the values approved, gt_verified, and agent_verified, an absent block being read as unreviewed, and every correction is written into a per-page edit_history that stamps each change with its source, human or agent. An object's position between machine transcription and expert-authorised text is therefore a readable property of the files, exposed in the built catalogue as a status column and summarised in a curation-progress bar that follows the concentric model. The movement inward through Vogeler's rings has a concrete correlate in the data, and the epistemological difference between artificial and critical stays explicit, because provenance keeps machine output, agent verification, and human authorisation apart.

## 3 The Pipeline

The demonstration corpus is the digitised Stefan Zweig estate held at the Literaturarchiv Salzburg. The pipeline transcribed roughly 2,450 canonical objects across five collections, some 20,300 facsimile scans at about 25.6 GB, spanning legal papers, manuscripts, galley proofs, newspaper clippings, and handwritten letters, in German at 95.6 percent with English, French, Italian, and Spanish in the remainder.

Prompting is organised as a layered stack assembled per object. A shared system prompt fixes the diplomatic-transcription rules and a mandatory JSON output schema. One of nine group prompts, from handwriting through galley proofs to correspondence, is selected automatically from the TEI object type. An optional per-object override exists for hard cases, and a context string derived from the object's TEI metadata is added at call time. Transcription runs on gemini-3.1-flash-lite-preview at temperature 0.1, chosen for low cost, speed, a one-million-token context, and multimodality; objects with more than twenty images are chunked and merged, with a retry path for failed chunks.

The documented costs are reported as they stand. The transcription model is priced at 0.25 USD per million input tokens; a three-model ground-truth run over eighteen objects cost about eight to twelve USD, and per-page vision verification is priced at about 0.001 USD. No total cost or wall-clock duration for the full production run is recorded in the repository, and this report states that boundary instead of estimating across it.

Output leaves the pipeline along three export paths. An internal Page-JSON format carries OCR, layout, and descriptive metadata as the working representation. The archival target is a METS container with MODS metadata and one PAGE XML 2019 file per page. A third path converts Page-JSON to teiCrafter-loadable TEI deterministically, as a byte-reproducible transformation with no LLM or API call. Each object's primary result file is already structured as edition data, carrying object and collection identifiers, TEI-derived descriptive metadata, and per-page transcriptions with a categorical confidence value and pipeline-assigned page types.

## 4 The Editorial Workspace

The public deployment on GitHub Pages serves as a read-only proto-edition with a catalogue, a facsimile-text viewer, and a quality dashboard. The same code base, cloned and run locally, activates the editing controls; the switch is the hostname, and edit functions render only when the application detects a local origin. A small local server writes corrections back into the pipeline result JSONs on disk, after copying a backup, so the pipeline output files remain the single source of truth. Git commits and pull requests carry curated edits into the public deployment. The two server roles that classical edition stacks require, persistence and multi-user coordination, are absorbed by the local filesystem and by Git.

The data model records what happens in this workspace. On the first correction of a page, two fields appear in the result file, an immutable transcription_llm holding the raw model output, and an edit_history whose entries stamp each change with editor, timestamp, and source, human or agent. The immutable snapshot satisfies a methodological requirement of correction-based evaluation; the machine hypothesis must survive in-place correction, since otherwise no error rate can later be reconstructed. Review states are stored per object. approved and gt_verified mark human checking, agent_verified marks a model-based check of the image against the text, and an absent review block reads as unreviewed. A needs_review flag from the quality signals is a triage hint inside the unreviewed state and is deliberately kept apart from the review vocabulary.

The workspace also reports its own coverage. In the built catalogue, 19 objects are approved, 85 agent_verified, and 2,348 carry no review, with 324 flagged for review; human and agent checking together cover roughly 104 of 2,452 objects. The proto-edition designation is therefore honest at the level of individual objects; the interface shows for each piece how far editorial engagement has gone.

For the developer, the same interface functioned as the verification environment during pipeline development, surfacing transcription errors, structural pipeline failures, and weaknesses in prompt design before expert review began.

## 5 Quality Assessment and Its Limits

Two mechanisms assess quality, text-statistical signals over the whole corpus and error rates derived from corrections.

The quality signals are computed after transcription with no further API call. Version 1.6 exposes several fields but drives its triage from three, a page-length anomaly against the collection median, a page-to-image count mismatch, and a language mismatch; further signals remain informational. Validated against 62 agent-verified objects, the length and image-mismatch signals reached full precision and the language signal half. Evaluation without reference material can indicate quality without resolving it (Ströbel et al. 2022), and the calibration proved corpus-dependent; thresholds validated on legal papers and manuscripts produced a wave of false positives on letter convolutes, where short envelope and address pages stand against long letter medians, and version 1.6 exempts such pages. The signals are therefore corpus-calibrated heuristics for directing scarce expert attention, and the interface presents them as flags, with the detailed values shown only in the object view.

The error rates come from the correction workflow itself. Measured character-weighted against human corrections, the corpus CER is 0.962 percent over 56 edited pages in 40 objects, about 114,000 reference characters, with 16 further human-checked objects that needed no edits counted as error-free by convention. An earlier baseline over 58 verified objects across all nine prompt groups spans from below five percent for print to about ten percent for difficult handwriting and tables. The recurring hard cases form a typology, systematic substitution of Fraktur long s by f, letter confusions in Kurrent script, and fluent hallucination, where the model invents real words instead of setting the uncertainty marker the system prompt provides. The last class matters most editorially, because a plausible real-word error is exactly what passes human review.

These figures carry stated validity limits. A correction-based CER is a downward-biased estimate; the curator reads the machine proposal before the image, plausible false readings are adopted at above-chance rates, and errors shared by model and reviewer stay invisible. The corrections come from few reviewers without a second independent reading, so inter-annotator agreement is unknown, and review order follows editorial priorities, so the sample is a progress sample. Aggregate reporting hides variance across hands, scripts, and languages. The project protocol therefore records planned mitigations, a small blind-transcribed subset to quantify the anchoring bias, stratified reporting by hand, script type, and language, and micro- and macro-averaged rates with document-level bootstrap intervals; these steps are documented as open in the repository. A further recorded limit is VLM non-determinism; the same object yields different error rates across runs even at temperature 0.1.

One risk is structural for VLM transcription and shapes the whole design. An aggregate CER near one percent is compatible with a transcription that has been silently modernised at exactly the points a diplomatic edition cares about, because each single normalisation moves the metric by only one character while a language-primed model modernises systematically. The system therefore fixes the diplomatic rules in the shared system prompt and reports categorical confidence per page in place of pseudo-precise scores.

## 6 Knowledge Engineering and Agentic Engineering

The system described so far was itself produced by an AI agent, and the way this production is organised is the second subject of this report.

Knowledge engineering once named the discipline of eliciting domain knowledge from experts and structuring it for machine use. Under development with AI agents the term regains a literal meaning; what steers the agent is a curated corpus of project knowledge in Markdown. Promptotyping (Pollin 2026) is the method used here, and it is materially present in the repository as a typed set of steering documents. A root CLAUDE.md holds the imperative layer that configures the agent. Plan.md is a phased roadmap with a dated decision log. A knowledge vault of thirteen documents, indexed by index.md, holds the data overview, the verification concept, evaluation results, and the format specifications, and a research journal of dated sessions from March to June 2026 functions as the audit trail. The repository is at once the product and its own record, and the record shows its accretion honestly; session numbers are reused and dated headers run out of order toward the end, consistent with a log written as the work proceeded.

Agentic engineering names the complementary discipline, organising what the agent does and keeping its work accountable. In this project the agent occupies two recorded positions. As developer the AI agent produced pipeline, interface, and documentation, with the project lead acting as project manager and domain expert. As verification instance it operates inside the editorial data model; agent reviews store the model identity, the errors found, and an estimated accuracy, and agent corrections enter the same per-page edit_history as human ones, stamped with source agent. Every machine intervention remains separable from human work in the record.

The epistemological ground for this bookkeeping lies in what a frontier-model step does to a chain of evidence. In Latour's account of circulating reference, scientific knowledge holds because each transformation from source to statement is documented and in principle reversible (Latour 1999). A frontier model is a black box in a precise sense; the computation between prompt and output has no symbolic intermediary a researcher could read, so its decision logic cannot be reconstructed even in principle. Such a step breaks the referential chain locally, and everything downstream inherits the indeterminacy. The response here is an epistemic infrastructure in the sense of the science and technology studies tradition of knowledge infrastructures (Star and Ruhleder 1996; Edwards 2010), a parallel chain of documented, human-verifiable transformations built around the opaque step, versioned prompts, committed result files, deterministic exports, and review provenance. Within this infrastructure the expert role is critical in a specific sense; it combines domain expertise with vigilance toward model sycophancy and toward errors that read plausibly.

## 7 Sustainability

Static output is durable. The published site needs no running services and makes no external requests, the edition data sits in version control, and the archival exports stand in open, provider-independent formats. The production process is bound to proprietary frontier models twice over; the transcription and layout steps call the Gemini API, and the development itself ran through a proprietary coding agent.

The pattern can be called frontier-built specialisation, adapting an analogy from the encoder-model literature that van Strien has made current for collection institutions, in which frontier systems figure as Formula 1 cars and small dependable applications as the everyday vehicles institutions actually need (Warner et al. 2024; van Strien 2026). Here the frontier model builds the everyday vehicle, and the dependency moves to the build layer and persists there.

The repository records the mitigations on the run layer. Every result JSON is committed to Git, so the transcriptions survive independently of any API. The archival exports, PAGE XML, METS with MODS, and teiCrafter TEI, are deterministic and LLM-free, and the published site is static in the sense of the minimal computing discussion (Risam and Gil 2022). What cannot be reconstructed without the proprietary layer is the process; a rerun of the pipeline or a regeneration of the tooling presupposes access to frontier models at their current prices.

This report situates the tension instead of resolving it. The edition data, its provenance, and the record of its production are open and durable, while the capability that produced them is rented. For a low-resource project the trade was enabling, since corpus-scale transcription and a purpose-built editorial workspace would otherwise have been out of reach, and the recorded provenance keeps the epistemic cost of the trade visible per object, in the same files that carry the edition.

[^1]: Stefan Zweig Digital, "About", https://www.stefanzweig.digital/archive/objects/context:szd/methods/sdef:Context/get?mode=about&locale=en (accessed 2026-07-21). The About page dates the platform to June 2018 ("Since its launch in June 2018 ..."; "Version 1: Launch, June 2018").

## References

Diaz, C. (2018). Using Static Site Generators for Scholarly Publications and Open Educational Resources. *The Code4Lib Journal* 42. https://journal.code4lib.org/articles/13861

Edwards, P. N. (2010). *A Vast Machine: Computer Models, Climate Data, and the Politics of Global Warming*. Cambridge, MA: MIT Press.

Hodel, T. (2023). Konsequenzen der Handschriftenerkennung und des maschinellen Lernens für die Geschichtswissenschaft. *Historische Zeitschrift* 316(1), 151–180. DOI: 10.1515/hzhz-2023-0006

Latour, B. (1999). *Pandora's Hope: Essays on the Reality of Science Studies*. Cambridge, MA: Harvard University Press.

Pierazzo, E. (2019). What Future for Digital Scholarly Editions? From Haute Couture to Prêt-à-Porter. *International Journal of Digital Humanities* 1, 209–220. DOI: 10.1007/s42803-019-00019-3

Pollin, C. (2026). Promptotyping: Zwischen Vibe Coding, Vibe Research und Context Engineering. L.I.S.A. Wissenschaftsportal Gerda Henkel Stiftung, 17.01.2026. https://lisa.gerda-henkel-stiftung.de/digitale_geschichte_pollin

Risam, R., & Gil, A. (2022). Introduction: The Questions of Minimal Computing. *Digital Humanities Quarterly* 16(2). http://digitalhumanities.org/dhq/vol/16/2/000646/000646.html

Sahle, P. (2013). *Digitale Editionsformen. Zum Umgang mit der Überlieferung unter den Bedingungen des Medienwandels*. 3 vols. Norderstedt: BoD.

Star, S. L., & Ruhleder, K. (1996). Steps toward an Ecology of Infrastructure: Design and Access for Large Information Spaces. *Information Systems Research* 7(1), 111–134. DOI: 10.1287/isre.7.1.111

Ströbel, P. B., Clematide, S., Volk, M., & Hodel, T. (2022). Evaluation of HTR Models without Ground Truth Material. *Proceedings of LREC 2022*. https://aclanthology.org/2022.lrec-1.467.pdf

Stutzmann, D. (2019). Artificial Edition. Paper, International Medieval Congress, Leeds.

van Strien, D. (2026). AI Design Patterns for Information Professionals. https://danielvanstrien.xyz/ai-patterns-for-glam

van Zundert, J. J. (2016). The Case of the Bold Button: Social Shaping of Technology and the Digital Scholarly Edition. *Digital Scholarship in the Humanities* 31(4), 898–910. DOI: 10.1093/llc/fqw040

Vogeler, G. (2022). Edition – Protoedition – Reproduktion: Der digitale Wandel. *Geschichte in Wissenschaft und Unterricht* 73(9/10), 498–511.

Vogeler, G. (2025). Die Konzentrische Edition. In: U. Rasche et al. (eds.), *Der kaiserliche Reichshofrat*. Köln: Böhlau. DOI: 10.7788/9783412530563.489

Warner, B., et al. (2024). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder (ModernBERT). arXiv preprint. https://arxiv.org/abs/2412.13663

Project artefacts: repository https://github.com/chpollin/szd-htr-ocr-pipeline, live site https://chpollin.github.io/szd-htr-ocr-pipeline/, evidence base PAPER-FINDINGS.md in this repository.
