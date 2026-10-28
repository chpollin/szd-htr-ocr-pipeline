---
title: "Index"
aliases: [index, "MOC", "Map of Content", "Research Vault"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Index"
  version: 0.4
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/index"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-index"
status: active
language: de
version: 0.3
created: 2026-04-01
updated: 2026-10-28
authors: [Christopher Pollin]
related: [project, data, specification, architecture, governance, handoff, journal]
---

# Index

Einstieg in die Wissensbasis der SZD OCR/HTR Pipeline für einen Coding-Agenten zu Sessionbeginn, für Gutachtende, die eine Aussage gegen Code und Daten prüfen, und für die Projektleitung beim Wiedereinstieg. Die Tabellen unten ordnen jedes Dokument seiner Funktion nach der Konvention für Promptotyping Documents zu und steuern zugleich die Abschnitte des Research Vault im Viewer. Veränderliche Zahlen stehen in ihren Quellen, `docs/catalog.json`, `python pipeline/transcribe.py --all --dry-run` und `reports/`.

## Dokumente

### Rahmen

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[project]] | Charter | Was ist das Projekt, für wen, auf welcher Materialgrundlage, unter welcher Lizenz? | bei Änderung von Identität, Rollen oder Scope |
| [[specification]] | Specification | Was sollen Pipeline und Viewer tun, nach welchem Review-Modell, in welchen Ausgabeformaten, und welche Entscheidungen sind gefallen? | bei Anforderungs- oder Entscheidungsänderung |
| [[governance]] | Governance | Wer darf welchen Status setzen und welche Entscheidung treffen, und welche Kompetenz trägt eine Freigabe? | bei Änderung von Rollen oder Befugnissen |

### Material und Fachregeln

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[data]] | Material | Woraus besteht der Korpus, Sammlungen, Prompt-Gruppen, Sprachen, Hände, Bildmengen? | bei neuer Lieferung oder Backup-Änderung |
| [[transcription-guidelines]] | Domain Knowledge | Nach welchen Regeln wird diplomatisch transkribiert, welches Markup gilt? | bei editorischer Entscheidung |
| [[editorial-methodology]] | Domain Knowledge | Wie hängen editorischer Status, Betriebskontexte, Provenienz und Modellabhängigkeit zusammen? | bei Änderung des Statusmodells oder der Quellenhierarchie |

### Architektur

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[architecture]] | Architecture | Wie fließen Daten durch die Pipeline, welche Komponenten, Modelle und Archivformate gibt es, welches Bedrohungsmodell gilt? | bei Architekturänderung |
| [[page-json-architecture]] | Architecture | Wie führt Page-JSON v0.2 Text, Layout und deskriptive Metadaten zusammen? | bei Schemaänderung |
| [[layout-analysis-architecture]] | Architecture | Wie arbeitet die Regionenerkennung und wie wird nach PAGE XML exportiert? | bei Änderung der Layout-Stufe |

### Prüfung

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[transcription-verification]] | Verification | Wie wird geprüft, mit welchen Signalen, Konsensus- und Agentenverfahren, und welche Fehlertypen kehren wieder? | bei Änderung eines Verfahrens oder Signals |
| [[review-findings]] | Quality Assurance | Welche Befunde und Vorschläge kommen aus dem laufenden Review, mit welcher Urheberschaft? | bei jedem neuen Befund oder Statuswechsel |

### Schnittstellen

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[teicrafter-integration]] | Integration | Wie wird Page-JSON deterministisch zu teiCrafter-ladbarem TEI mit Marker-Anreicherung? | bei Änderung des Konverters oder der teiCrafter-Seite |
| [[dia-xai-integration]] | Integration | In welchem Verhältnis steht die Pipeline zum DIA-XAI-Pilotprojekt und zum Verifikationsantrag? | bei Änderung des Antrags- oder Pilotstands |

### Prozess

| Pfad | Funktion | Routing Question | Aktualisierung |
|---|---|---|---|
| [[plan]] | Planning | Welche Arbeit ist angenommen, in welcher Phase, und welche Entscheidungen stehen aus? | bei Abschluss oder Aufnahme einer Aufgabe |
| [[handoff]] | Handoff | Welche Übergabepunkte warten auf Integration oder Verwerfung? | bei Eingang oder Verarbeitung eines Punkts |
| [[journal]] | Provenance | Welche Übergänge wurden integriert, verworfen oder korrigiert, und warum? | nach jedem sachlich zusammengehörigen Übergang |

`review-findings.md` ist eine Spezialisierung nach dem Muster `<subject>-<function>.md` für Quality Assurance. Sie trägt Material vor der Entscheidung, das die Projekt-Reviewer:in am Faksimile und am Viewer beobachtet. Zwei Eigenschaften rechtfertigen das eigene Dokument. Jeder Befund trägt eine stabile ID (`B-01`, `B-02`, …), auf die Journal, Issues und Commits verweisen, und jeder Absatz ist nach Urheberschaft mit **[J]** oder **[C]** gekennzeichnet. Ein allgemeines Testing-Dokument hätte für diese Kennzeichnung und für die Regel, dass **[J]**-Absätze unverändert bleiben, keinen Ort.

### Frühere Dateinamen

Die Wissensbasis wurde am 2026-10-28 nach den Promptotyping-Vorlagen vereinheitlicht. Ältere Journaleinträge, **[J]**-Absätze und das Manuskript unter `paper/` verwenden die früheren Namen; `aliases:` im Frontmatter und die Alias-Tabelle des Viewers führen sie auf das aktuelle Dokument.

| Früherer Name | Aktuelles Dokument |
|---|---|
| `index.md` | `INDEX.md` |
| `data-overview.md` | `data.md` |
| `annotation-protocol.md` | `transcription-guidelines.md` |
| `editorial-model.md` | `editorial-methodology.md` |
| `verification-concept.md` | `transcription-verification.md` |
| `evaluation-results.md` | Fehlertypologie in `transcription-verification.md` §9, Messbericht `reports/cer-baseline-report-2026-04-02.md` |
| `expert-in-the-loop.md` | `governance.md` |
| `htr-interchange-format.md` | `page-json-architecture.md` |
| `layout-analysis.md` | `layout-analysis-architecture.md` |
| `page-xml-mets-architecture.md` | `architecture.md`, Abschnitt Archivformat |
| `security.md` | `architecture.md`, Abschnitt Sicherheit, Befunde in `reports/security-review-2026-04-02.md` |
| `stats-dashboard.md` | `specification.md`, Abschnitt Statistik-Dashboard |
| `verification-fair4rs.md` | `reports/fair4rs-verification-2026-07-23.md`, offene Maßnahmen in `plan.md` |

## Ablagezonen

- `knowledge/` enthält die dauerhaft gepflegten Promptotyping Documents einschließlich `handoff.md` als Process Inbox.
- `reports/` ist die Ablagezone für datierte Berichte, Audits und Befundlisten, die nicht fortgeschrieben werden. Sie entspricht der Zone `snapshots/` der Konvention; der Name ist im Repository etabliert und wird von Skripten beschrieben. Messwerte und Stichtagsbefunde liegen hier, ihre gültige Deutung in `knowledge/`.
- `paper/` hält das Forschungsmanuskript vom Juli 2026 mit seiner Evidenzbasis als eingefrorenes Forschungsartefakt.
- `data/` hält die TEI-Metadaten als übernommenes Quellmaterial; die Faksimiles liegen im lokalen Backup außerhalb des Repositorys.
- `results/`, `docs/catalog.json` und `docs/data/` sind von der Pipeline erzeugte Artefakte; `results/README.md` beschreibt ihren Aufbau.

## Lesepfade

- Sessionstart: [[INDEX]] → [[handoff]] → [[project]] → aufgabenrelevantes Dokument.
- Ergebnisdatei verstehen: [[specification]] (Ausgabeformate) → [[page-json-architecture]] → `results/README.md`.
- Prüfstatus und Provenienz prüfen: [[governance]] → [[transcription-verification]] → `README.md` (Trust tiers) → `pipeline/serve.py`.
- Archivexport nachvollziehen: [[architecture]] → [[page-json-architecture]] → [[teicrafter-integration]].
- Editorischen Rahmen verstehen: [[editorial-methodology]] → [[transcription-guidelines]] → [[transcription-verification]].
- Entstehung nachvollziehen: `README.md` (How this was built) → [[journal]] → [[review-findings]].

## Konvention

Die Wissensbasis folgt der Konvention für Promptotyping Documents (https://dhcraft.org/Promptotyping/), die Naming Contract, Frontmatter-Schema, Routing-Heuristik und Strukturprinzipien regelt. Jedes Dokument trägt den Pflichtkern `title`, `project`, `method`, `status`, `created`, `updated`; wo eine Katalogvorlage existiert, bindet `template:` das Dokument an sie. Die gemeinsame Schemaversion steht nur hier im Feld `version:` und gilt für alle Dokumente dieses Ordners; sie steigt, wenn sich Pflichtfelder oder Funktionen ändern. Das Feld `generated-with` steht nur, wo die Git-Historie ein einziges Modell über die gesamte Dateigeschichte ausweist. `pipeline/build_viewer_data.py` liest die Tabellen unter Dokumente für die Navigation des Viewers.

Design hat kein eigenes Dokument; das Designsystem liegt in `docs/app.css`, die Gestaltungsregeln des Statistik-Dashboards in [[specification]]. Die Teststrategie steht im Action-Layer `CLAUDE.md`, die Prüfungen selbst unter `tests/` und `pipeline/test_*.py`. Eine Technology Baseline entfällt, weil das Repository keine Artefaktfamilie mit anderen Projekten teilt.

## Begriffe

### [J] und [C]

Urheberschaftsmarker je Absatz. **[J]** kennzeichnet eine fachliche Beobachtung der Projekt-Reviewer:in (Universität Salzburg), **[C]** eine maschinelle Nachprüfung durch einen Agenten mit angegebenem Kommando.

Verwendet in [[review-findings]], [[governance]].

### Agent-Verifikation

Bild-Text-Vergleich eines Objekts durch einen Vision-Agenten, der Fehler korrigiert und den Status `agent_verified` mit Modellkennung schreibt. Sie erhöht die Evidenz, ersetzt die menschliche Prüfung aber nicht.

Verwendet in [[transcription-verification]], [[specification]].

### CER

Character Error Rate, edit_distance(A, B) / max(len(A), len(B)), gemessen gegen menschlich geprüfte Texte. Die korrekturbasierte CER misst den kuratierten Bestand und ist keine Zufallsstichprobe.

Verwendet in [[transcription-verification]], [[editorial-methodology]].

### needs_review

Triage-Kennzeichen „zuerst sichten" innerhalb der ungeprüften Objekte, gesetzt aus den aktiven Qualitätssignalen. Es ist kein Prüfstatus.

Verwendet in [[specification]], [[transcription-verification]].

### Page-JSON

Internes Arbeitsformat je Objekt mit Text, optionalen Koordinaten und deskriptiven Metadaten, Schema `schemas/page-json-v0.2.json`.

Verwendet in [[page-json-architecture]], [[architecture]].

### Prompt-Gruppe

Einer von neun Dokumenttypen A–I (Handschrift bis Korrespondenz), der den Gruppen-Prompt bestimmt und automatisch aus den TEI-Metadaten zugeordnet wird.

Verwendet in [[data]], [[architecture]].

### quality_signals

Regelbasierte Textstatistik je Objekt, nach der Transkription ohne weiteren API-Call berechnet. Sie priorisiert Review-Aufwand und misst keine Korrektheit.

Verwendet in [[transcription-verification]], [[specification]].

### SZ-AAL

Signaturgruppe der Briefkonvolute, im Repository als Sammlung `autographen` geführt und immer Prompt-Gruppe I zugeordnet.

Verwendet in [[data]].

## Außerhalb von knowledge/

- [CLAUDE.md](../CLAUDE.md), Action-Layer für Agenten
- [README.md, Abschnitt How this was built](../README.md#how-this-was-built), Methode, beteiligte Modelle, Verifikationsschichten und bekannte Grenzen für Lesende von außen
- [paper/README.md](../paper/README.md), Einordnung des Manuskripts vom Juli 2026
- [results/README.md](../results/README.md), Aufbau der Ergebnisdateien
