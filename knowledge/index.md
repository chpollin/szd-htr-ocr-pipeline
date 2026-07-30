---
title: "Research Vault"
aliases: ["MOC", "Map of Content", "index"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Index"
  version: 0.1
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/index"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-index"
status: stable
language: de
version: 0.2
tags: [index]
created: 2026-04-01
updated: 2026-07-30
type: moc
---

# SZD-HTR Research Vault

Navigationsknoten des Wissensstands und Lesehilfe fuer seine Dokumente. Der Vault dokumentiert die VLM-gestuetzte HTR/OCR-Pipeline fuer den Stefan-Zweig-Nachlass und richtet sich an drei Leserinnen und Leser, an eine Gutachterin, die eine Behauptung gegen den Code pruefen will, an einen frischen Coding-Agenten und an die Projektleitung, die nach Wochen zurueckkehrt. Der operative Stand steht im juengsten Eintrag von [[journal]]. Veraenderliche Zahlen stehen nie hier, sondern in ihren Quellen, `docs/catalog.json` fuer den Katalogstand, `python pipeline/transcribe.py --all --dry-run` fuer die kanonische Objektzahl, `reports/` fuer die Messberichte und die Testlaeufe unter `pipeline/test_*.py` und `tests/`.

## Grundlagen

| Dokument | Funktion | Lektuere beantwortet |
|---|---|---|
| [[data-overview]] | Material | Woraus der Korpus besteht, fuenf Sammlungen, neun Prompt-Gruppen, Sprachen, Schreiberhaende, Bildmassen |
| [[annotation-protocol]] | Norm | Nach welchen Regeln diplomatisch transkribiert wird und welches Markup gilt |
| [[verification-concept]] | Verfahren | Wie geprueft wird, Ground Truth, quality_signals, Cross-Model-Konsensus, Verification-by-Vision, Agent-Verifikation |
| [[evaluation-results]] | Befund | Was die CER-Baseline zeigt und welche Fehlertypen wiederkehren |

## Spezifikationen

| Dokument | Funktion | Lektuere beantwortet |
|---|---|---|
| [[htr-interchange-format]] | Arbeitsformat | Wie Page-JSON v0.2 Text, Layout und deskriptive Metadaten zusammenfuehrt |
| [[page-xml-mets-architecture]] | Zielformat | Wie PAGE XML, MODS und METS geschichtet sind und wie TEI-Felder darauf abgebildet werden |
| [[teicrafter-integration]] | Editionsformat | Wie Page-JSON deterministisch nach teiCrafter-ladbarem TEI konvertiert und mit Markern angereichert wird |
| [[layout-analysis]] | Layout | Wie die VLM-gestuetzte Regionenerkennung arbeitet und nach PAGE XML exportiert |
| [[stats-dashboard]] | Anzeige | Welche Metriken das Statistik-Dashboard zeigt und wie sie definiert sind |

## Rahmen und Pruefung

| Dokument | Funktion | Lektuere beantwortet |
|---|---|---|
| [[dia-xai-integration]] | Aussenbezug | In welchem Verhaeltnis die Pipeline zum DIA-XAI-Pilotprojekt und zum geplanten Verifikationsantrag steht |
| [[verification-fair4rs]] | Nachweis | Wie das Repository gegen die FAIR4RS-Prinzipien abschneidet, geprueft und belegt |
| [[security]] | Angriffsflaeche | Welches Threat Model der lokale Review-Server hat und welche Findings behoben sind |

## Projektlog

| Dokument | Funktion | Lektuere beantwortet |
|---|---|---|
| [[plan]] | Roadmap | In welcher Phase die Arbeit steht, welche Aufgaben offen sind, welche Entscheidungen datiert gefallen sind |
| [[review-findings]] | Rueckmeldung | Welche Befunde und Verbesserungsvorschlaege aus dem laufenden Review kommen, mit Urheberschaft je Eintrag |
| [[journal]] | Genese | Was in jeder Session geschah, mit Begruendung der Entscheidungen; zugleich der Audit-Trail des Projekts |

## Lesepfade

- Erstkontakt: `data-overview` → `verification-concept` → `evaluation-results`
- Ergebnisdatei verstehen: `htr-interchange-format` → `verification-concept` → `results/README.md`
- Archivexport nachvollziehen: `page-xml-mets-architecture` → `htr-interchange-format` → `teicrafter-integration`
- Vertrauensstufen und Provenienz pruefen: `verification-concept` → `README.md` (Abschnitt Trust tiers) → `pipeline/serve.py`
- Arbeit wieder aufnehmen: `journal` → `plan`
- Aussenbezug klaeren: `dia-xai-integration` → `verification-fair4rs`

## Konvention

Der Vault folgt der Konvention fuer Promptotyping Documents. Sie regelt das Frontmatter-Schema, die Lesehilfe und die strukturellen Prinzipien, gegen die jedes Dokument lesbar bleibt. Die Abschnittsstruktur dieses Dokuments steuert zugleich die Navigation des Knowledge-Vaults im Viewer, `pipeline/build_viewer_data.py` liest die Ueberschriften und die Wikilinks daraus.

## Verwandte Dokumente ausserhalb des Vaults

- [CLAUDE.md](../CLAUDE.md) — Agentenkonfiguration und Architekturueberblick
- [paper/PAPER.md](../paper/PAPER.md) — Abschlussbericht des Projekts, mit `paper/PAPER-FINDINGS.md` als Evidenzbasis
- [results/README.md](../results/README.md) — Aufbau der Ergebnisdateien
