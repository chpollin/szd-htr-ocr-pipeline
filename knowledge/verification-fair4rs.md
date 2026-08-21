---
title: "Verifikation FAIR4RS-Status"
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Verification"
  version: 0.1
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/verification"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-verification"
status: active
created: 2026-07-23
updated: 2026-07-23
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Fable 5)
type: verification
related:
  - "[[verification-concept]]"
---

# Verifikation: FAIR4RS-Status des Repositories

## Geprüfte Behauptung

Das Repository wird im Promptotyping-Methodenpaper (Pollin, in Arbeit, Sektion 4.1) als auditierter Fall für die FAIR4RS-Bilanz statischer Promptotyping-Artefakte verwendet: stark bei Reusability (insbesondere Provenienz) und Accessibility, systematisch schwach bei Findability. Dieses Dokument trägt den Befund, damit die Behauptung prüfbar bleibt.

## Evidenz und Verfahren

Prüfung am 2026-07-23 gegen die FAIR4RS-Prinzipien v1.0 (Chue Hong, Katz, Barker et al. 2022, Research Data Alliance, DOI 10.15497/RDA00068), Kriterium für Kriterium, per lokalem Klon (Stand Commit 29a350c, 2026-07-21) und GitHub-API (Visibility, License-Detection, Releases, Description, Topics).

## Befund je Prinzip

| Prinzip | Befund | Beleg |
|---|---|---|
| F1 (persistenter, global eindeutiger Identifier) | nicht erfüllt | nur GitHub-URL, keine DOI |
| F1.1 (Identifier je Granularitätsstufe) | nicht erfüllt, verzichtbar | Projektebene ist beim Prototyp die sinnvolle Einheit; die Prinzipien schreiben Stufen nicht vor |
| F1.2 (Identifier je Version) | nicht erfüllt | keine Tags, keine Releases (API: 0) |
| F2 (reiche Metadaten) | teilweise | README reich für Menschen; keine maschinenlesbaren Metadaten |
| F3 (Metadaten nennen den Identifier) | nicht erfüllt | kein CITATION.cff, kein codemeta.json |
| F4 (Metadaten FAIR, harvestbar) | nicht erfüllt | GitHub-Description und Topics leer (API-Prüfung) |
| A1, A1.1 (Abruf über offenes Standardprotokoll) | erfüllt | Repo und GitHub-Pages-Viewer über HTTPS, ohne proprietäre Werkzeuge |
| A1.2 (AuthN/AuthZ wo nötig) | nicht einschlägig | öffentliches Repo |
| A2 (Metadaten überleben die Software) | nicht erfüllt | folgt aus F4; kein von GitHub unabhängiger Metadatenort |
| I1 (Datenaustausch nach Community-Standards) | erfüllt | liest TEI-XML (Stefan Zweig Digital); PAGE-XML/METS-Architektur und Interchange-Format in `knowledge/` dokumentiert |
| I2 (qualifizierte Referenzen auf Objekte) | teilweise | TEI-Quellen per URL im README qualifiziert referenziert |
| R1 (Pluralität akkurater Attribute) | teilweise | menschenlesbar ja, maschinenlesbar nein (siehe F2) |
| R1.1 (klare, zugängliche Lizenz) | teilweise | LICENSE vorhanden (CC BY 4.0); GitHub erkennt "Other", nicht SPDX-maschinenlesbar; CC-Lizenzfamilie für Code unüblich |
| R1.2 (detaillierte Provenienz) | erfüllt, überdurchschnittlich | README benennt Genese, Methode, Rollen und Modelle; `knowledge/journal.md`, `paper/PAPER.md`, Git-History |
| R2 (qualifizierte Referenzen auf Software) | erfüllt | `requirements.txt` über PyPI |
| R3 (domänenrelevante Community-Standards) | erfüllt | TEI, diplomatische Transkriptionskonventionen, dokumentierte Markup-Regeln |

## Verdikt

Die Behauptung des Papers hält: Accessibility konstruktionsbedingt erfüllt, Reusability weitgehend erfüllt mit Provenienz als Stärke der Methode, Findability durchgängig nicht erfüllt als Normalzustand eines nie formal publizierten Prototyps. Die F-Lücke ist Publikationsarbeit, kein Methodenproblem.

## Maßnahmen (Stand der Entscheidung 2026-07-23)

Beschlossene Schließung der Lücken gemäß der FAIR-Infrastruktur-Politik des Methoden-Repos (`DigitalHumanitiesCraft/Promptotyping`, `knowledge/paper-writing.md`): Dual-Licensing MIT (Code) plus CC BY 4.0 (Dokumentation), Rechteangabe für Drittdaten (Faksimiles und TEI: Literaturarchiv Salzburg / Stefan Zweig Digital); CITATION.cff und codemeta.json aus dem Frontmatter-Kern; GitHub-Description und Topics; Zenodo-Release mit DOI, geschnitten wenn der Stand trägt.

## Grenzen

Momentaufnahme eines Repos zu einem Stichtag; die Prinzipien F1.1 und A1.2 sind als verzichtbar bzw. nicht einschlägig gewertet, das ist Auslegung, nicht Messung. Die Prüfung lief als Einzeldurchgang ohne zweiten unabhängigen Prüfer.
