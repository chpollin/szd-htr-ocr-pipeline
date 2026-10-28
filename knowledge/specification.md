---
title: "Specification"
aliases: [stats-dashboard, "Statistik-Dashboard"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Specification"
  version: 0.3
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/specification"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-specification"
status: active
language: de
created: 2026-10-28
updated: 2026-10-28
authors: [Christopher Pollin]
related:
  - "[[project]]"
  - "[[data]]"
  - "[[architecture]]"
  - "[[transcription-verification]]"
  - "[[governance]]"
---

# Specification

Die Pipeline und ihr Viewer sollen den Nachlass diplomatisch transkribieren, den Prüfstatus je Objekt sichtbar halten und die Ergebnisse in Archivformate überführen. Anforderungen und Review-Modell ändern sich selten und nur durch Entscheidung der Projektleitung, der Funktionsumfang wächst mit dem Viewer, und das Entscheidungslog wächst monoton.

## Anforderungen

### Funktionale Anforderungen

- FR-01: Die Pipeline transkribiert jedes Objekt mit allen Bildern in einem Aufruf, Objekte mit mehr als 20 Bildern in Chunks mit anschließendem Merge. Akzeptanzkriterium: Seitenzahl des Ergebnisses gleich Bildzahl, sonst `page_image_mismatch` oder `transcription_status` partial/failed.
- FR-02: Jedes Objekt erhält eine Prompt-Gruppe A–I automatisch aus den TEI-Metadaten (`resolve_group()`), mit optionalem Objekt-Prompt als Override. Akzeptanzkriterium: Korrespondenzen und Briefkonvolute immer Gruppe I, Konvolute G, Fallback Handschrift.
- FR-03: `quality_signals.py` berechnet regelbasierte Signale je Objekt und setzt `needs_review` als Triage. Akzeptanzkriterium: Signalschwellen in `pipeline/test_quality_signals.py`, Signalkatalog in [[transcription-verification]] §2.
- FR-04: Der Prüfstatus wird je Objekt im `review`-Block geführt (siehe Review-Modell). Akzeptanzkriterium: Übergänge der Review-API in `tests/test_trust_tiers.py`.
- FR-05: Jede Korrektur bewahrt den Maschinenzustand. Akzeptanzkriterium: `transcription_llm` wird beim ersten Edit gesetzt und danach nie überschrieben, `edit_history` protokolliert jede Änderung.
- FR-06: Page-JSON v0.2 wird aus Ergebnis, Layout und TEI-Metadaten exportiert. Akzeptanzkriterium: alle `results/*/*_page.json` validieren gegen `schemas/page-json-v0.2.json` (`tests/test_page_json_schema.py`).
- FR-07: METS/MODS und PAGE XML werden deterministisch aus Page-JSON und TEI erzeugt. Akzeptanzkriterium: gleicher Eingabestand ergibt gleiche Ausgabe ohne Modellaufruf.
- FR-08: Der öffentliche Viewer ist schreibgeschützt; Bearbeitung und Freigabe stehen nur im lokalen Betrieb mit `pipeline/serve.py` zur Verfügung. Akzeptanzkriterium: ohne `GET /api/status` bleiben Bearbeitungselemente verborgen.

### Nicht-funktionale Anforderungen

- NFR-01: Diplomatische Transkription ohne Normalisierung und ohne Korrektur. Maßstab: Markup nach [[transcription-guidelines]].
- NFR-02: Tests und Exporte laufen ohne API-Key und ohne lokales Bild-Backup. Maßstab: `python -m pytest tests/ pipeline/`.
- NFR-03: Der Viewer kommt ohne Laufzeit-CDN und ohne Build-Schritt aus. Maßstab: Chart.js vendored unter `docs/lib/`, Wissensdokumente zur Build-Zeit in HTML gerendert.
- NFR-04: Bilder werden direkt von GAMS geladen, das Repository hält keinen Bildspeicher. Maßstab: `<img src>` auf GAMS-URLs.
- NFR-05: Eingaben an Vertrauensgrenzen werden validiert und Ausgaben escaped. Maßstab: Bedrohungsmodell in [[architecture]] §Sicherheit.

## Review-Modell

Drei Status in der Anzeige, vier gespeicherte Stufen (Entscheidung der Projektleitung 2026-06-10).

| Status (Anzeige) | Status im JSON | Bedeutung |
|---|---|---|
| Mensch-geprüft | `gt_verified` oder `approved` | Am Faksimile gegengelesen, bei Bedarf korrigiert. Gilt als verifiziert und Ground-Truth-fähig. Approve heißt gegengelesen, nicht überflogen. |
| Agent-geprüft | `agent_verified` | Bild-Text-Vergleich durch einen Vision-Agenten. Kann stimmen, ersetzt keine menschliche Prüfung. |
| Ungeprüft | kein `review`-Block | Nur Pipeline-Selbsteinschätzung. `needs_review` ist Triage innerhalb dieser Stufe und kein eigener Status. |

Die gespeicherten `review.status`-Werte bleiben unverändert, die Zusammenfassung zu drei Status geschieht in der Anzeigeschicht (`docs/app.js`). CER-Referenz sind menschlich geprüfte Texte. Wer welchen Status setzen darf, regelt [[governance]]; die Außenbeschreibung für Gutachtende steht in `README.md` unter "Trust tiers and verification provenance".

Je Seite führt das Ergebnis zwei Datenströme. `transcription` ist die Arbeitsfassung, `transcription_llm` der unveränderliche Roh-Output des Modells, gesetzt beim ersten Edit und für den Altbestand per `pipeline/backfill_transcription_llm.py` migriert. `edit_history` protokolliert jede Änderung. Die CER aus Korrekturen berechnet `python pipeline/report_cer_from_edits.py` nach `reports/cer-from-edits.md`.

## Epics und User Stories

### Epic 1: Prüfen und Freigeben am Faksimile

#### Transkription gegenlesen und freigeben

*Als Reviewer:in, die ein Objekt am Faksimile prüft, will ich die Transkription korrigieren und freigeben, damit geprüfter Text als Referenz und für den Export zur Verfügung steht.*

Validierung: validiert durch Entscheidung der Projektleitung am 2026-06-10 (Review-Modell)

Ableitung:
- Anforderung FR-04, FR-05, FR-08
- Komponente [[architecture]] §Komponenten (`serve.py`, `docs/app.js`)
- Begriffe [[INDEX]] Trust tier, Review-Status

#### Gruppenzuweisung im Review ändern

*Als Reviewer:in, die eine falsch zugeordnete Prompt-Gruppe bemerkt, will ich die Gruppe im Review ändern oder vorschlagen, damit das Objekt mit dem passenden Prompt neu transkribiert werden kann.*

Validierung: aufgeworfen von der Projekt-Reviewer:in am 2026-07-25 ([[review-findings]] B-02), Umsetzung offen

Ableitung:
- Anforderung FR-02
- Komponente `resolve_group()` in `pipeline/tei_context.py`

### Epic 2: Nachvollziehbarkeit für Lesende von außen

#### Behauptung gegen Code und Daten prüfen

*Als Gutachter:in, die eine Aussage über die Pipeline prüft, will ich vom Prüfstatus eines Objekts zu Verfahren, Code und Messbericht gelangen, damit ich die Aussage ohne Rückfrage nachrechnen kann.*

Validierung: Annahme (Proxy: Projektleitung), Effekt: to be observed, Auflösung: erste externe Begutachtung

Ableitung:
- Anforderung FR-04, NFR-02
- Dokumente [[transcription-verification]], `reports/`
- Begriffe [[INDEX]] Trust tier

## Funktionsumfang

### Katalog

Zweck. Auffinden und Priorisieren von Objekten.

Datengrundlage. `docs/catalog.json`, gebaut von `pipeline/build_viewer_data.py`.

Interaktion. Filter als deklaratives Registry (`FILTER_DEFS` in `docs/app.js`): Sammlung, Lieferung (`ingestLabel`, Tooltip aus `config.INGEST_INFO`), Bestandseinheit oder Konvolut (nur Korrespondenzen und Briefkonvolute über `config.UNIT_TERMS`; Feld `unit` ist die Signatur ohne letztes Punkt-Segment, `derive_unit()` in `build_viewer_data.py`), Gruppe, Qualität, Status und einzelner Review-Grund. Ein neuer Filter ist ein Registry-Eintrag plus `<select>` in `index.html`. Die Spalte Status zeigt die drei Review-Status als Badge, ⚠ markiert „zuerst sichten"; die Seitenzahl steht als „N S." in der Typ-Spalte.

Grenzen. Der Katalog aggregiert Objektzustände und berechnet keinen Qualitätsscore.

### Viewer und Bearbeitung

Zweck. Faksimile und Transkription Seite für Seite vergleichen, lokal korrigieren und freigeben.

Datengrundlage. `docs/data/{collection}.json`, Bilder von GAMS.

Interaktion. Objekt- und Seitennavigation getrennt, Layout-Overlay (Taste L), Diff gegen die Modellfassung, Richtlinien-Panel (Taste G) mit §3 von [[transcription-guidelines]] und im Bearbeitungsmodus eine Markup-Leiste, die die Marker regelkonform setzt.

Grenzen. Speichern und Freigeben nur im lokalen Betrieb.

### Statistik-Dashboard

Zweck. Die Qualität der Transkription akademisch argumentierbar machen. Text-Chips im Katalog zeigen Verteilungen, Ausreißer und Zusammenhänge nicht; Standard-Metriken wie CER und WER reichen für historische Dokumente nicht aus (Beyene und Dancy 2026; Levchenko 2025), proxy-basierte Signale und ihre Verteilung tragen weiter. Die Perspektive ist Computational Philology und Digital Scholarly Editing mit Informationsvisualisierung (Yuan et al. 2024); die Metriken müssen für Forschende und Archivar:innen philologisch interpretierbar sein.

Datengrundlage. Client-seitige Aggregation aus `catalog.json` in einem Durchlauf (`computeStatsData()`), ohne Backend. Jedes transkribierte Objekt trägt `quality_signals`, Review-Status und TEI-Metadaten.

Interaktion. Drei Sektionen mit erklärendem Kopf und Quellenangabe, Karten zweispaltig im Grid. Die narrativen Sektionen erklären den jeweiligen Argumentationsschritt; Drill-down läuft über Hash-Navigation in den Katalog. Donuts nutzen eine eigene `donutOptions()` ohne Achsen, getrennt von `chartOptions()`, die Heatmap liegt in einem scrollbaren Container für schmale Viewports.

1. Verifikation. Ein Donut zeigt Mensch-geprüft (grün), Agent-geprüft (blau), Ungeprüft (grau) und „Zuerst sichten" (amber als Triage-Akzent), nur Segmente größer null; ein Klick auf „Zuerst sichten" führt zu `#catalog?review_status=priority`. Ein horizontaler Balken zeigt die Anzahl je Review-Grund mit Signal-Precision im Untertitel, ein Klick führt zum gefilterten Katalog.
2. Textcharakteristik. Median der Zeichen je Inhaltsseite nach Dokumenttyp als horizontaler Balken. Er zeigt die strukturelle Spannweite von Registerblättern mit Stichwortnotizen bis zu dichten Zeitungsausschnitten. Quelle `chars_per_page` → `verification.avgCharsPerPage`.
3. Signalanalyse. Heatmap als HTML-Tabelle mit dem Anteil der Objekte je Gruppe, die ein Signal auslösen; Gruppenname und Zellen verlinken auf den gefilterten Katalog. Quelle `needs_review_reasons` → `needsReviewReasons`.

Welche Signale `needs_review` auslösen, wie sie definiert sind und welche Precision gemessen wurde, steht in [[transcription-verification]] §2. Informativ ohne Review-Auslösung bleiben `duplicate_pages` und `marker_density`. CER ist definiert als edit_distance(A, B) / max(len(A), len(B)), Referenz sind menschlich geprüfte Texte.

Grenzen. Entfernt wurden, weil nicht gegroundet oder transient (Session 22 ff.): Abdeckung und Seitenkomposition als Produktions-Tracking, das DWR-Histogramm nach Entfernung von DWR in v1.5, der Donut der VLM-Konfidenz, die nicht diskriminiert, und Modellkonsensus, der Übereinstimmung statt Korrektheit misst und auf wenigen Objekten beruht. Ein CER-zentriertes Dashboard entfällt, weil nur ein Bruchteil der Objekte CER-Daten hat.

Literatur zum Dashboard:

- Beyene, F.S. und Dancy, C.L. (2026). A Survey of OCR Evaluation Methods and Metrics and the Invisibility of Historical Documents. *FAccT 2026*.
- Yuan, J. et al. (2024). Visual Analytics for Machine Learning: A Data Perspective Survey. *IEEE TVCG* 30(12).
- Romein, C.A. et al. (2025). Assessing Advanced Handwritten Text Recognition Engines. *International Journal of Digital Humanities* 7(1), 115–134.
- Levchenko, M. (2025). Evaluating LLMs for Historical Document OCR. *LM4DH 2025, RANLP*.
- Priestley, M. et al. (2023). A Survey of Data Quality Requirements That Matter in ML Development Pipelines. *JDIQ* 15(2).

### Research Vault und Projektseite

Zweck. Den Wissensstand und die Projektbeschreibung im Viewer lesbar machen.

Datengrundlage. `docs/data/knowledge.json`, gebaut von `build_knowledge()` aus `knowledge/*.md` und `README.md`. Die Abschnitte und die Leseordnung kommen aus den Tabellen in [[INDEX]]; frühere Dateinamen aus `aliases:` leiten alte Links und Lesezeichen auf das aktuelle Dokument um.

Interaktion. `#knowledge`, `#knowledge/{slug}`, `#about`.

Grenzen. Die Darstellung ist ein Build-Zeit-Abbild; nach Änderungen an `knowledge/` muss `build_knowledge()` laufen.

## Ausgabeformate

Jedes Ergebnis liegt unter `results/{collection}/{object_id}_{model}.json`:

```json
{
  "object_id": "o_szd.100",
  "collection": "lebensdokumente",
  "group": "typoskript",
  "model": "gemini-3.1-flash-lite-preview",
  "metadata": { "title": "...", "language": "...", "images": ["https://gams.uni-graz.at/..."] },
  "context": "## Dieses Dokument\n- Titel: ...",
  "result": {
    "pages": [
      {"page": 1, "transcription": "...", "notes": "...", "type": "content"},
      {"page": 2, "transcription": "", "notes": "Rueckseite, leer.", "type": "blank"}
    ],
    "confidence": "high | medium | low"
  },
  "quality_signals": { "version": "...", "needs_review": false, "..." : "..." },
  "review": { "status": "approved | agent_verified", "..." : "..." }
}
```

- `page.type` ist `content`, `blank` oder `color_chart`, gesetzt von `quality_signals.py`, Schema in `schemas/page-json-v0.2.json`.
- `quality_signals` trägt die Signale und `transcription_status` (complete, partial, failed); Katalog und Version stehen in [[transcription-verification]] §2.
- `review` ist optional und wird von `serve.py`, `import_reviews.py` oder der Agent-Verifikation geschrieben.

Daraus entstehen zwei komplementäre Formate. Page-JSON v0.2 (`*_page.json`) ist das interne Arbeitsformat mit Text, Layout und deskriptiven Metadaten nach Dublin Core und Materialtypologie, Koordinaten optional, exportiert von `pipeline/export_page_json.py` und beschrieben in [[page-json-architecture]]. METS/MODS mit PAGE XML 2019 ist das Archiv- und Austauschformat für GAMS, Transkribus, eScriptorium und teiCrafter, exportiert von `pipeline/export_pagexml.py` und `pipeline/export_mets.py` und beschrieben in [[architecture]]. Page-JSON entsteht zuerst, METS/MODS wird daraus abgeleitet.

## Entscheidungen

### Grundsatzentscheidungen

Diese Festlegungen tragen die Pipeline seit ihrem Aufbau; ihr Datum ist im Einzelnen nicht festgehalten.

- Gemini 3.1 Flash Lite ist das primäre VLM, weil es günstig, schnell und multimodal ist.
- Bilder gehen ohne Preprocessing an die API.
- Alle Bilder eines Objekts gehen an die API, auch Leerseiten, weil Zweigs Schreibpraxis unregelmäßig ist. Die Seitentyp-Klassifikation erfolgt post-hoc.
- Qualitätssignale ersetzen die Selbsteinschätzung des Modells, weil diese empirisch nicht diskriminiert.
- Diplomatische Transkription ohne Normalisierung, Markup `[?]` unsicher, `[...]` unleserlich, `~~...~~` gestrichen, `{...}` eingefügt.
- Bilder kommen direkt von GAMS, das Repository hält keinen Bildspeicher.
- Zwei Ausgabeformate, Page-JSON intern und METS/MODS mit PAGE XML extern.

### Entscheidungslog

| Datum | Entscheidung | Begründung |
|---|---|---|
| 2026-04-01 | Pilot vor vollem GT-Sample | CER unbekannt, Sample-Design ohne Pilot ist blind |
| 2026-04-01 | quality_signals sofort | Kostet nichts, braucht kein GT, bietet Triage für Batch |
| 2026-04-01 | Cross-Model: Agreement-First | Unabhängige Doppeltranskription methodisch sauberer |
| 2026-04-01 | Claude Sonnet als zweites Modell | Maximale Diversität zu Gemini, starke Baseline, moderate Kosten |
| 2026-04-01 | Gezieltes Sample statt voller Batch | 10 je Gruppe reicht für group_text_density und Gruppenvergleich |
| 2026-04-01 | quality_signals v1.2: Leerseiten-Klassifikation | VLM erkennt Leerseiten und Farbskalen in Notes, Post-Processing statt Pre-Filtering |
| 2026-04-01 | DWR statt PPPL als GT-freie Metrik | Keine schwere Dependency (transformers), wissenschaftlich fundiert (Springmann 2016) |
| 2026-04-01 | Modellkonsensus statt manuellem GT | Zhang et al. 2025 (ICLR 2026): drei Modelle und Judge skalierbarer als 30 Objekte manuell |
| 2026-04-01 | Gemini 3 Flash als Modell B | Stärker als Flash Lite, gleiche API, kein Provider-Wechsel |
| 2026-04-02 | word_overlap und effective_cer statt CER allein | CER bestraft Reading-Order-Divergenz, Jaccard auf Wortmengen ist robust |
| 2026-04-02 | Vier statt drei Konsensus-Stufen | „review" als Zwischenstufe für 75–90 % word_overlap |
| 2026-04-02 | Gemini Pro als drittes GT-Modell | Gleiche API, stärkstes Gemini-Modell |
| 2026-04-02 | Pilot übersprungen | Modellkonsensus-Validierung und GT-Pipeline beantworten die Pilotfragen empirisch |
| 2026-04-02 | Pre-rendered Markdown statt Client-Side | Keine Laufzeit-Dependencies, Wikilinks zur Build-Zeit aufgelöst |
| 2026-04-02 | Chunking statt Downscaling | Volle Bildauflösung, 20 Bilder je Chunk sicher unter dem API-Limit |
| 2026-04-02 | Objekt-Prompts als vierte Schicht | Spezialfälle ohne Änderung des Gruppen-Prompts lösbar |
| 2026-04-02 | serve.py statt localStorage | Pipeline-JSONs als einzige Quelle der Wahrheit, kein manueller Export |
| 2026-04-02 | Whitelist statt Blacklist für den Katalog | SKIP_SUFFIXES fragil bei neuen Modellen, Whitelist robuster (offen) |
| 2026-04-03 | DWR entfernt (v1.5) | rho=0.05, F1=0.20, misst Prosadichte statt Qualität |
| 2026-04-03 | Stats-Dashboard ohne Produktions-Tracking | Fortschritt, Seitenkomposition, DWR, VLM-Konfidenz und Konsensus entfernt, nur Qualitätsmetriken |
| 2026-04-03 | `_fill_missing_pages()` | Seiten-Bild-Desynchronisation behoben, 41 Objekte backfilled |
| 2026-04-03 | Page-JSON v0.2 mit descriptive_metadata | Dublin Core und materialtypologische Erweiterungen für Archivmetadaten |
| 2026-04-03 | Zwei Ausgabeformate | Page-JSON intern als Arbeitsformat, METS/MODS mit PAGE XML extern als Archiv- und Austauschformat |
| 2026-06-10 | Review-Modell mit drei Anzeige-Status | Agent-Prüfung bleibt von menschlicher Autorisierung unterscheidbar |
| 2026-08-21 | Proto-Edition-Manuskript bleibt Forschungsartefakt | Keine Einreichung; gepflegte Erkenntnisse liegen in [[editorial-methodology]], [[transcription-verification]] und [[architecture]] |
| 2026-10-28 | Wissensbasis nach Promptotyping-Vorlagen vereinheitlicht | Dateinamen signalisieren die Funktion; Herleitung in [[journal]] |
