---
title: "Project"
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Projekt-Wissensdokument"
  version: 0.3
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/project"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-project"
status: active
language: de
created: 2026-10-28
updated: 2026-10-28
authors: [Christopher Pollin]
knowledge-sources:
  institutions:
    Literaturarchiv Salzburg: "https://www.uni-salzburg.at/literaturarchiv"
    Stefan Zweig Digital: "https://stefanzweig.digital/"
    GAMS (Universität Graz): "https://gams.uni-graz.at/"
  standards:
    TEI: "https://tei-c.org/"
    PAGE XML: "https://github.com/PRImA-Research-Lab/PAGE-XML"
    METS: "https://www.loc.gov/standards/mets/"
    MODS: "https://www.loc.gov/standards/mods/"
related:
  - "[[data]]"
  - "[[specification]]"
  - "[[architecture]]"
  - "[[editorial-methodology]]"
  - "[[governance]]"
---

# Project

Die SZD OCR/HTR Pipeline erzeugt maschinenlesbaren Text aus den digitalisierten Faksimiles des Stefan-Zweig-Nachlasses im Literaturarchiv Salzburg. Sie ist ein experimentelles Teilprojekt von Stefan Zweig Digital und verbindet eine Transkriptionspipeline auf Basis eines Vision Language Model (VLM), einen öffentlichen Viewer mit lokalem Review-Modus und deterministische Exporte in Archiv- und Austauschformate.

## Datengrundlage

Grundlage sind die Faksimile-Scans und die zugehörigen Metadaten aus dem lokalen Backup des Projekts, gegliedert in fünf Sammlungen (Lebensdokumente, Werke, Aufsatzablage, Korrespondenzen, Briefkonvolute SZ-AAL). Die TEI-Metadaten von Stefan Zweig Digital liefern Titel, Datierung, Sprache, Signatur und Objekttyp und steuern die Zuordnung jedes Objekts zu einer Prompt-Gruppe. Die eigene Leistung des Projekts beginnt bei der Transkription; Digitalisierung, Katalogisierung und Bildbereitstellung über GAMS liegen bei den beteiligten Institutionen. Umfang, Sammlungsprofile, Sprachen und Schreiberhände beschreibt [[data]].

## Übergeordneter Kontext

Das Projekt ist ein experimentelles Teilprojekt von [Stefan Zweig Digital](https://stefanzweig.digital/), der digitalen Erschließung des Nachlasses durch das Literaturarchiv Salzburg auf der GAMS-Infrastruktur der Universität Graz. Die Transkriptionsergebnisse sind als Eingabe für das DIA-XAI-Pilotprojekt und einen geplanten Verifikationsantrag vorgesehen, deren Schnittstelle [[dia-xai-integration]] beschreibt. Die nachgelagerte TEI-Annotation übernimmt teiCrafter als separates Repository, angebunden über [[teicrafter-integration]].

Methodische Referenzen aus derselben Projektfamilie sind [zbz-ocr-tei](https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei) für LLM-OCR gedruckter Texte mit Batch-Verarbeitung und Qualitätsscreening, [coOCR HTR](https://github.com/DigitalHumanitiesCraft/co-ocr-htr) für browserbasierte HTR mit Expert-in-the-Loop-Validierung und [teiCrafter](https://github.com/DigitalHumanitiesCraft/teiCrafter) für die TEI-Annotation.

## Worum es geht

Der Nachlass liegt als Faksimile vor, sein Text ist bisher nicht durchsuchbar. Die Pipeline soll diplomatische Transkriptionen in großer Breite erzeugen und dabei sichtbar halten, welcher Text maschinell erzeugt, agentisch gesichtet oder menschlich geprüft ist. Daraus folgen drei Prioritäten. Der Prüfstatus wird je Objekt geführt und nie zu einem globalen Qualitätsurteil verdichtet. Jede Korrektur bewahrt den Maschinenzustand, aus dem sie hervorgeht. Die Ergebnisse bleiben ohne erneuten Modellaufruf lesbar und in institutionelle Formate überführbar. Die fachliche Begründung dieser Prioritäten steht in [[editorial-methodology]], die Prüfverfahren in [[transcription-verification]].

## Standards

Die technische Anschlussfähigkeit folgt etablierten Standards:

- Quellmetadaten: TEI-XML von Stefan Zweig Digital, gelesen über `pipeline/tei_context.py`
- Transkription: diplomatische Konventionen mit festem Markup nach [[transcription-guidelines]]
- Seitenlayout und Text: PAGE XML 2019, je Seite exportiert
- Deskriptive Metadaten: MODS mit GND-Verknüpfung, abgeleitet aus TEI
- Container und Struktur: METS, wie es GAMS nativ verwendet
- Arbeitsformat: Page-JSON v0.2 mit JSON-Schema unter `schemas/`, beschrieben in [[page-json-architecture]]

Die Wahl der XML-Standards für die Archivausgabe ist eine Ökosystem-Entscheidung. Intern arbeitet die Pipeline mit JSON, weil Viewer und Prüfwerkzeuge damit direkt umgehen. Nach außen exportiert sie in die Formate, die GAMS, Transkribus, eScriptorium und teiCrafter lesen. Die Schichtung beider Seiten steht in [[architecture]].

## Technische Umsetzung

Das Projekt ist ein Promptotyping-Projekt. Code, Pipeline-Architektur, Frontend und Dokumentation wurden mit Claude Code erzeugt. Die Co-Authored-By-Trailer der Commits nennen Opus 4.6 für die Aufbauphase von März bis April 2026, danach Opus 4.8, Fable 5, Opus 5 und Opus 5.5. Die Projekt-Reviewer:in der Universität Salzburg committet seit Juli 2026 ebenfalls, teils mit Claude Code (Trailer Opus 5 und Opus 5.5), teils ohne Trailer. Für Commits ohne Trailer ist nicht festgehalten, ob und welches Werkzeug beteiligt war. Die Projektleitung arbeitet als Projektmanager und fachlicher Entscheider und schreibt den Code nicht selbst. Wer welche Entscheidung treffen und welchen Status setzen darf, regelt [[governance]].

## Funktionsumfang

Die Anwendung erschließt Faksimile und Transkription nebeneinander, mit Katalog, Filter nach Sammlung, Gruppe und Prüfstatus, einer Statistikseite zu den Qualitätssignalen und dem Wissensbestand dieses Ordners. Im lokalen Betrieb aktiviert derselbe Client Bearbeitung und Freigabe, die direkt in die Ergebnisdateien schreiben. Anforderungen, Ansichten und Entscheidungen stehen in [[specification]].

Die Datenabdeckung ist ungleich. Der weitaus größte Teil des Bestands ist ungeprüfte Modelltranskription, ein kleiner Teil agentisch oder menschlich geprüft. Der Viewer zeigt diesen Status je Objekt und hält unvollständige oder fehlgeschlagene Transkriptionen als solche kenntlich. Aktuelle Zahlen liefert `docs/catalog.json`.

## Abgrenzungen

Das Projekt leistet nicht:

- eine kritische Edition oder eine editorisch autorisierte Fassung des Gesamtbestands
- eine Bewertung der Transkriptionsqualität durch einen globalen Score
- eine prosopographische Erschließung der genannten Personen, die bei der TEI-Annotation liegt
- eine reproduzierbare Neuberechnung der Modellausgaben, weil die Inferenzdienste veränderlich sind
- die Bildhaltung, die bei GAMS verbleibt

Die Grenzen folgen aus der Rolle als experimentelles Teilprojekt, das Material für die Erschließung bereitstellt und die Autorisierung bei den fachlich Verantwortlichen lässt.

## Begriffe

- Proto-Edition: der öffentliche Viewer als recherchierbarer Zwischenstand aus Faksimile, maschineller Transkription, Metadaten und Prüfstatus, ohne einheitliche editorische Reife.
- Trust tier: der Prüfstatus eines Objekts, Mensch-geprüft, Agent-geprüft oder Ungeprüft, mit den gespeicherten Werten aus [[specification]].
- Promptotyping: die Methode, nach der ein fachlich Verantwortlicher einen Coding-Agenten über gepflegtes Projektwissen anleitet und die Ergebnisse prüft.

## Lizenz

Code steht unter MIT (`LICENSE`), Dokumentation und Wissensdokumente unter CC BY 4.0. Die Rechte an den Faksimiles und den daraus abgeleiteten Transkriptionen liegen beim Literaturarchiv Salzburg. Die vollständige Angabe steht in `README.md`, Abschnitt Licence, die maschinenlesbare Fassung in `CITATION.cff` und `codemeta.json`.
