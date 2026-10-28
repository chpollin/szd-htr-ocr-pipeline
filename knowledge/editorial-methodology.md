---
title: "Editoriales und epistemisches Modell"
aliases: ["Editoriales Modell", "Epistemisches Modell"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Domänenwissen"
  version: 0.2
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/domain-knowledge"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-domain-knowledge"
status: active
created: 2026-08-21
updated: 2026-08-21
authors: [Christopher Pollin]
type: concept
related:
  - "[[verification-concept]]"
  - "[[evaluation-results]]"
  - "[[page-xml-mets-architecture]]"
  - "[[journal]]"
---

# Editoriales und epistemisches Modell der SZD-HTR-Pipeline

Dieses Dokument haelt die fachliche Synthese zur Rolle des Viewers, zum Status der Transkriptionen und zur Nachvollziehbarkeit agentischer Arbeit. Das im Juli 2026 verfasste Manuskript unter `paper/` bleibt als datierter Forschungsstand erhalten. Seit dem 21. August 2026 besteht fuer dieses Manuskript kein Einreichungsziel. Seine dauerhaft gueltigen Projekterkenntnisse werden hier und in den jeweils spezialisierten Wissensdokumenten gepflegt.

## Editioneller Status als Objekteigenschaft

Der oeffentliche Viewer erschliesst Faksimiles, maschinelle Transkriptionen, Metadaten und Qualitaetssignale in einer recherchierbaren Oberflaeche. Die im Forschungsmanuskript herangezogene Bezeichnung als Proto-Edition beschreibt diesen Zwischenstand. Sie beansprucht keine einheitliche editorische Reife fuer den gesamten Korpus.

Die editorische Reife wird je Objekt im `review`-Block des Ergebnis-JSON festgehalten. `gt_verified` und `approved` bezeichnen menschlich gepruefte Texte, `agent_verified` einen Bild-Text-Vergleich durch einen Vision-Agenten. Ein fehlender `review`-Block bezeichnet eine ungepruefte Modelltranskription. `needs_review` priorisiert Objekte innerhalb dieser letzten Gruppe und trifft keine Aussage ueber einen erreichten Pruefstatus.

Der Katalog aggregiert diese Objektzustaende fuer die Curation-Progress-Anzeige. Die Anzeige erzeugt keinen globalen Editionsstatus und berechnet keinen Qualitaetsscore. Damit bleibt sichtbar, welche Teile des Bestands maschinell erzeugt, agentisch gesichtet oder menschlich autorisiert wurden. Die genauen Statusuebergaenge und ihre technische Verankerung stehen in [[verification-concept]].

## Eine Anwendung in zwei Betriebskontexten

GitHub Pages liefert die Anwendung mit Katalog, Faksimile-Text-Ansicht und Qualitaetsdashboard aus. Dieser Betrieb benoetigt keinen schreibenden Projektserver. Die Faksimiles werden weiterhin aus der GAMS-Infrastruktur geladen.

Dieselbe Client-Anwendung aktiviert im lokalen Betrieb zusaetzliche Editierfunktionen. `pipeline/serve.py` schreibt Korrekturen in die Ergebnis-JSONs und legt vor dem Schreiben eine Sicherungskopie an. Die lokale Dateispeicherung uebernimmt die Persistenz; Git fuehrt freigegebene Aenderungen zwischen Arbeitsstaenden zusammen. Der oeffentliche Viewer ist damit eine funktional eingeschraenkte Auspraegung desselben Artefakts.

## Provenienz als Bestandteil des Datenmodells

Eine Korrektur ersetzt den Maschinenzustand nicht spurlos. Vier Felder halten unterschiedliche Funktionen auseinander.

| Feld | Funktion |
|---|---|
| `transcription` | aktuelle Arbeitsfassung einer Seite |
| `transcription_llm` | unveraenderter Roh-Output des Transkriptionsmodells, beim ersten Edit gesichert |
| `edit_history` | Folge der Aenderungen mit Zeitpunkt, Bearbeiter und Quelle |
| `review` | Pruefstatus und Provenienz auf Objektebene |

Das Datenmodell fuehrt Review-Status, die kategoriale Modellkonfidenz und regelbasierte Qualitaetssignale getrennt. Diese Felder beantworten verschiedene Fragen. Der Status dokumentiert erfolgte Pruefung, die Modellkonfidenz eine Selbsteinschaetzung des Modells und die Signale eine heuristische Triage. Eine Verdichtung wuerde ihre unterschiedlichen Evidenzwerte verdecken.

## Wissensarbeit und agentische Arbeit

Die agentische Entwicklung stuetzt sich auf einen versionierten Wissensbestand. `CLAUDE.md` enthaelt die imperativen Arbeitsregeln. `knowledge/` traegt Materialkenntnis, Verifikationsverfahren und Formatspezifikationen. [[plan]] haelt operative Entscheidungen fest, [[journal]] dokumentiert ihre Genese. Diese Trennung macht fachliche Annahmen auffindbar und verhindert, dass eine einzelne Sitzung zum einzigen Speicher einer Entscheidung wird.

Der Agent tritt im Projekt in zwei unterscheidbaren Rollen auf. Als Entwicklungsinstanz erzeugt und veraendert er Pipeline, Interface und Dokumentation. Als Verifikationsinstanz vergleicht er Faksimile und Transkription. Die zweite Rolle schreibt ihren Modellnamen, Befunde und Aenderungsquelle in die Ergebnisdaten. Eine Agentenpruefung bleibt dadurch von menschlicher Autorisierung unterscheidbar.

Ein Modellaufruf liefert keinen lesbaren internen Entscheidungsweg. Das Repository dokumentiert deshalb die pruefbaren Transformationen um diesen Schritt herum.

| Transformation | Dokumentierter Nachweis | Pruefbarkeit |
|---|---|---|
| Transkription | versionierte Prompts, TEI-Kontext, Modellkennung und Ergebnis-JSON | Output gegen Faksimile und Prompt pruefbar |
| Korrektur | Rohfassung, aktuelle Fassung, `edit_history` und `review` | Aenderung und Urheberschaft rekonstruierbar |
| Export | Page-JSON, PAGE XML, METS/MODS und deterministische Exportskripte | Struktur durch Schema und Tests pruefbar |

## Erkenntnisgrenzen der Qualitaetsmessung

Regelbasierte Qualitaetssignale messen Auffaelligkeit. Cross-Model-Konsensus misst Uebereinstimmung. Beide Verfahren koennen plausible gemeinsame Fehllektuerungen uebersehen. Eine Agentenpruefung erhoeht die Evidenz, erreicht aber nicht den Status einer menschlichen Pruefung.

Auch die aus Korrekturen berechnete Character Error Rate hat eine begrenzte Reichweite. Die pruefende Person sieht die Modelltranskription vor dem Faksimile und kann dadurch an plausible Lesarten gebunden werden. Der Review-Bestand folgt editorischen Prioritaeten und bildet keine Zufallsstichprobe. Ein niedriger Aggregatwert kann zudem systematische Normalisierungen verdecken, die fuer eine diplomatische Transkription relevant sind. Messwerte und offene methodische Gegenmassnahmen stehen in [[evaluation-results]].

## Dauerhaftigkeit und Abhaengigkeitsgrenze

Die oeffentliche Anwendung, die Ergebnisdaten und die Exporte koennen ohne erneuten Modellaufruf erhalten und geprueft werden. Page-JSON bewahrt den internen Arbeitsstand; METS/MODS und PAGE XML bilden den institutionellen Austauschpfad. Die Exportstufen sind deterministisch und von der Transkriptions-API getrennt.

Eine vollstaendige Neuberechnung der Transkription und der VLM-basierten Layoutanalyse bleibt an proprietaere Modelle, ihre Verfuegbarkeit und ihr Laufzeitverhalten gebunden. Selbst bei gleicher Modellkennung ist ein identischer Output nicht garantiert. Der Reproduzierbarkeitsanspruch gilt fuer die aufgezeichneten Ergebnisse und die deterministischen Transformationen. Modellinferenz bleibt unter Anbieter- und Modellwechsel veraenderlich. Die technische Auspraegung dieser Grenze steht in [[page-xml-mets-architecture]].

## Quellenhierarchie

Der aktuelle Code und die Ergebnisdaten belegen das implementierte Verhalten. Die spezialisierten Dokumente unter `knowledge/` erklaeren Verfahren und Entscheidungen. `paper/PAPER.md` und `paper/PAPER-FINDINGS.md` dokumentieren den Projektstand vom Juli 2026 und bleiben fuer die dort ausgearbeitete Theorie und Bibliografie erhalten. Spaetere Projektentscheidungen werden in [[plan]] und [[journal]] fortgeschrieben.
