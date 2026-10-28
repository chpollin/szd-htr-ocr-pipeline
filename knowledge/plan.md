---
title: "Plan"
aliases: [verification-fair4rs, "Implementierungsplan", "Roadmap", "Phasenplan"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Plan"
  version: 0.3
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/plan"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-plan"
status: active
created: 2026-03-30
updated: 2026-10-28
language: de
authors: [Christopher Pollin]
type: plan
related:
  - "[[specification]]"
  - "[[journal]]"
  - "[[INDEX]]"
---
# Plan

Der Plan führt die angenommene Zukunftsarbeit der Pipeline in Phasen, vom laufenden Qualitätsausbau bis zur Übergabe an die DIA-XAI-Bewertung. Er wird fortgeschrieben; gefallene Entscheidungen wandern in [[specification]], abgeschlossene Übergänge in [[journal]].

## Zielbild

- Jedes Objekt des Bestands hat eine vollständige Transkription oder ist als unvollständig gekennzeichnet und für einen Neulauf vorgemerkt.
- Die Qualitätssignale sind gegen menschlich geprüfte Texte kalibriert, und die Editionsregeln decken die beim Review aufgetretenen Fälle ab.
- Page-JSON, PAGE XML und METS/MODS liegen für den gesamten transkribierten Bestand vor, und ein GAMS-Reingest ist erprobt.
- Die Ergebnisse stehen als Eingabe für den Expert-in-the-Loop-Workflow von DIA-XAI bereit.

## Phasen und Milestones

| Phase | Inhalt | Stand |
|---|---|---|
| Phase 1–3 | Grundlagen, alle Sammlungen, Pipeline-Automatisierung | abgeschlossen, Verlauf in [[journal]] |
| Phase 4 | Qualität und Vergleich | laufend |
| Phase 5 | Export und Austauschformate | Arbeitsformat und Zielformat implementiert, Reingest und teiCrafter offen |
| Phase 6 | DIA-XAI-Bewertung | ab Oktober 2026 |
| FAIR4RS | Findability des Repositorys | teilweise umgesetzt |

### Phase 4: Qualitaet & Vergleich (laufend)

#### 4a: Ground Truth
- [x] CER-Berechnungsscript (`pipeline/evaluate.py`)
- [x] Modellkonsensus-Metriken v2: `word_overlap()`, `effective_cer`, 4-Tier-Klassifikation (Session 14)
- [x] GT-Pipeline: `generate_gt.py` — 3-Modell-Merge (Flash Lite + Flash + Pro), 18 Objekte, 46 Content-Seiten (Session 14)
- [x] GT-Drafts in `results/groundtruth/` — consensus_3of3 (33%), majority_2of3 (43%), pro_only (24%)
- [x] Pilot uebersprungen — Modellkonsensus-Validierung + GT-Pipeline beantworten Pilotfragen empirisch
- [~] **Expert-Review**: 3/18 GT-Objekte verifiziert (o_szd.153, o_szd.137, o_szd.194). 15 ausstehend.
- [ ] quality_signals-Schwellenwerte anhand GT kalibrieren
- [ ] **Editionsrichtlinien pflegen** — das Richtlinien-Panel im Viewer zeigt §3 des
      Annotationsprotokolls. Faelle, die beim Redigieren auftauchen und dort nicht geregelt sind,
      gehoeren zurueck in `knowledge/annotation-protocol.md` und von dort ins Panel. Offen ist,
      ob das Panel Gruppen-spezifische Regeln (§4: Umschlaege, Stempel, Formularfelder, mehrere
      Haende) ebenfalls aufnehmen sollte — bisher nur die gruppenunabhaengigen Marker.
- [ ] **Regel fuer Abbildungen und undefinierte Klammern** (Operator-Feedback 2026-10-02) —
      das Modell beschreibt Abbildungen in selbst erfundenen Klammern (`[Abbildung: …]`,
      `[Bild: …]`, `[Bildunterschrift: …]`; 68 in 17 Objekten, v. a. Aufsatzablage), teils mit der
      echten Bildunterschrift in der Klammer. Gleiches Muster bei `[Unterschrift]` (169 in 112
      Objekten), `[eingefuegt]`, `[Randnotiz links:]`. Erst editorisch entscheiden
      (Annotationsprotokoll §8 Nr. 5), dann System-Prompt, `evaluate.py`-Normalisierung und
      `marker_enrich.py` (→ `<figure>`/`<figDesc>`) nachziehen. Befund →
      `reports/issue-review-fehlersammlung.md`, Befund 2 (Issue #1)
- [ ] **Regel fuer Text am Bildrand von Detailaufnahmen** (Review 2026-10-19) — das Modell ergaenzt
      angeschnittene Woerter aus anderen Scans desselben Objekts und normalisiert dabei
      (`o:szd.1056`). 318 Seiten in 187 Objekten sind laut Modellnotiz Ausschnitte/Detailaufnahmen.
      Entscheiden: nur Sichtbares mit Marker oder kenntlich ergaenzen (Annotationsprotokoll §8 Nr. 6).
      Befund → Fehlersammlung, Befund 3
- [ ] **Stempel und Randnotizen: Prompts ans Annotationsprotokoll angleichen** (Review 2026-10-19) —
      Gruppen C, H, I schicken Stempel/Annotationen in die Notizen, Protokoll §3.5/§4.2 verlangt
      `[Marginalie:]`/`[Stempel:]` im Text; Gruppe F kennt keine Vermerke. Bleistiftzusaetze fehlen
      (`o:szd.2745`, `o:szd.2759`, `o:szd.263`). Befund → Fehlersammlung, Befund 5
- [ ] **Notation fuer Umstellungen und Setzer-Korrekturzeichen** (Review 2026-10-19) — Kringel mit
      Versetzungslinie wird zu einer `(` (`o:szd.2759`). Annotationsprotokoll §8 Nr. 7, danach
      Gruppe F und `marker_enrich.py` (`<transpose>`). Befund → Fehlersammlung, Befund 6

#### 4b: Quality Signals & Batch
- [x] `quality_signals` implementieren (v1.5: 7 Signale + page.type, DWR entfernt wegen rho=0.05)
- [x] `needs_review`-Indikator im Viewer
- [x] quality_signals v1.1–v1.5: Rekalibrierung, Leerseiten-Klassifikation, DWR entfernt, Duplikat-Schwelle 200→50
- [x] System-Prompt: JSON-Schema, Blank-Page-Handling, Konfidenz-Kriterien, Bleed-Through-Regel
- [x] Seiten-Bild-Synchronisation: `_fill_missing_pages()` fuer VLM-Luecken (41 Objekte backfilled)
- [~] Alle Sammlungen transkribieren. Lebensdokumente 100%, Korrespondenzen 100%. Fortschritt → `--dry-run`.
- [x] **Salvage der Totalausfaelle** (2026-09-25): Parser-Stufe 6 uebernimmt die vollstaendigen Seiten vor einer Wiederholungsschleife, `salvage_raw_results.py` hat 18 der 34 Objekte teilweise gerettet (300 Seiten, 187 mit Text). `quality_signals` v1.7: `transcription_status` complete/partial/failed als eigene Review-Gruende im Katalog; ungelesene Scans gelten nicht mehr als Leerseite
- [ ] **Neulauf der unvollstaendigen Transkriptionen** (braucht API-Key + Backup) — 16 `transcription_failed` + 51 `transcription_partial` mit zusammen 1.675 ungelesenen Scans. Liste: Katalog-Filter "Transkription unvollstaendig/fehlgeschlagen" oder `quality_report.py`. `--force` laesst das ganze Objekt neu laufen; bei grossen Objekten kleineres `--chunk-size`. `o_szd.267` vorher pruefen (nur 107 von 232 Scans gesendet). Befund → `reports/pipeline-totalausfaelle.md`
- [ ] **Exporte der 67 Objekte neu erzeugen** — `_page.json` und `_mets.xml` stammen vom alten Stand (keine Seiten bzw. ungelesene Scans als `blank`). Nur auf einem Rechner mit Backup: ohne Backup faellt u.a. `rights` aus `metadata.json` still weg
- [ ] **Veraltete Signale nach Korrekturen** — `serve.py` rechnet `quality_signals` nach einem Edit nicht neu; bei 21 approbierten Objekten passen Zeichenzahlen, Marker, teils `page_types` nicht mehr zum Text. Entscheiden: nach Edit neu berechnen, oder Signale bewusst als Stand der Maschinenfassung einfrieren
- [ ] quality_signals-Schwellenwerte anhand GT kalibrieren
- [ ] **Paraphrasen bei Konfidenz `high` erkennen** (Review 2026-10-19) — Fraktur-Drucke werden
      plausibel umgedichtet (`o:szd.2745` S. 1 durchgehend, `o:szd.2759`), kein Signal schlaegt an.
      Vorschlag: `verify.py` gezielt auf Fraktur-Drucke; Gruppe F nennt nur Antiqua. Neulauf
      `o:szd.2745`. Befund → Fehlersammlung, Befund 4
- [ ] **Empfehlung aus dem A/B/C-Experiment entscheiden** (Session 25b, 2026-06-09, [[journal]]) —
      das Experiment empfahl fuer Handschrift `gemini-3-flash` als Basismodell und ein Feld
      `uncertain_words` als Review-Signal. Beides ist nicht umgesetzt: `HTR_MODEL` steht weiter auf
      `gemini-3.1-flash-lite-preview` (`pipeline/config.py`), der AAL-Batch vom 2026-06-10 lief mit
      Flash Lite, `uncertain_words` kommt in Prompts, Schema und Code nicht vor. Eine Entscheidung
      gegen die Empfehlung ist nicht dokumentiert. Grundlage war ein kleines Test-Set (6 Objekte,
      20 Seiten), agentisch am Faksimile ausgewertet. Die Entscheidung liegt bei der Projektleitung
- [ ] **Freigabe-Sperre fuer Objekte ohne Seiten** — Viewer zeigt die Faksimile der 16 Totalausfaelle
      seit `624c6e0` mit Badge "Nicht transkribiert"; `handle_approve()`/`handle_edit()` pruefen aber
      weiter nicht, ob das Ergebnis Seiten hat. Befund → Fehlersammlung, Befund 1

#### 4c: Modellkonsensus & Vergleich
- [x] `verify.py`: Modellkonsensus (Flash Lite + Flash + Claude Judge)
- [x] Modellkonsensus-Validierung: 29 Objekte (3/Gruppe), 4-Tier-Ergebnis: 26% verified, 33% moderate, 15% review, 26% divergent
- [x] Diff-Ansicht im Viewer (echte Modellkonsensus-Daten, CER, Modell-Namen)
- [x] Statistik-Dashboard im Frontend (Seiten, Konfidenz, DWR, Modellkonsensus, Review)
- [x] GT Review-Modus: 3-Varianten-Panel, Approve, localStorage, JSON-Export
#### 4d: Frontend & Dokumentation
- [x] Knowledge Vault im Frontend: 12 Markdown-Dokumente als navigierbare Ansicht (`#knowledge`, `#knowledge/{slug}`) (Session 15)
- [x] Projekt-Seite aus README.md (`#about`) (Session 15)
- [x] `build_viewer_data.py`: `build_knowledge()` — Markdown → HTML → knowledge.json (Session 15)
- [x] Layout-Analyse v1: VLM-only (`layout_analysis.py`) + PAGE XML Export (`export_pagexml.py`) (Session 14)
- [x] Layout-Analyse v4: Ensemble-Pipeline Docling + Surya + Gemini 3 Flash (Session 23-24). Alle 9 Gruppen getestet (25 Objekte, 72% good). Robustness-Refactoring (8 Fixes), Post-Processing-Filter (3 Filter), Prompt-Verfeinerung, Merge+Verify kombiniert (1 statt 2 VLM-Calls/Seite).
- [~] Layout-Batch: Visuelle Verifikation Welle 2 ausstehend, dann Batch ueber ~1300 Objekte.
- [x] Layout-Viewer: SVG-Overlay auf Faksimile, Toggle (L), Farblegende, Pan/Zoom-Sync (Session 23)
- [x] Lokaler Dev-Server (`serve.py`) mit Review-API: POST /api/approve, /api/edit (Session 17)
- [x] Expert-Review Write-Back (`import_reviews.py`) + 3-stufiger Review-Status (Session 16)
- [x] Katalog-Bereinigung: Duplikate (Pro-Modell), Color-Chart-Seiten, Test-Daten gefiltert (Session 16-17)
- [x] Katalog: Filter je einzelnem `needs_review`-Grund (`reason`-Param, Dropdown "Alle Signale") + Grund als klickbarer Chip in der Status-Spalte statt nur im Tooltip; Signal-Balkendiagramm und Heatmap-Zellen im Statistik-Dashboard verlinken auf den jeweiligen Signal-Filter (Operator-Feedback 2026-07-27)
- [x] Viewer: Objekt- und Seitennavigation optisch getrennt — die Objektebene ist eine ruhige
      Pille mit kleineren, randlosen Buttons, die Seitenebene bleibt der primaere Control; beide
      Zaehler benennen ihre Einheit ("Objekt 12 / 2452", "Seite 3 / 7") statt zweier nackter
      Zahlenpaare mit fast gleichen Pfeilzeichen (Operator-Feedback 2026-08-26)
- [x] Viewer: Editionsrichtlinien am Ort der Arbeit — Button "§ Richtlinien" (Taste G) blendet
      §3 des Annotationsprotokolls neben dem Text ein (Streichungen, Schwelle [?] gegen [...],
      Einfuegungen, Randbemerkungen), im Edit-Modus zusaetzlich eine Markup-Leiste, die die Marker
      regelkonform setzt: Auswahl in ~~...~~ / {...} einschliessen, [?] ohne Leerzeichen ans
      vorangehende Wort, [Marginalie:] ans Seitenende nach Leerzeile (Operator-Feedback 2026-08-26)

### Phase 5: Export & Austauschformate

#### 5a: Page-JSON v0.2 (Arbeitsformat)
- [x] Page-JSON v0.2 Schema (`schemas/page-json-v0.2.json`) — Dublin Core + materialtypologische Erweiterungen
- [x] `_extract_full_metadata()` in `tei_context.py` — 10 neue TEI-Felder (creators+GND, holding+GND, provenance, origPlace, writing_material, dimensions, binding, inscriptions)
- [x] `export_page_json.py` — OCR + Layout + TEI-Metadaten → Page-JSON v0.2
- [x] Wissensdokument `knowledge/page-xml-mets-architecture.md` — Schichtenarchitektur PAGE XML / MODS / METS
- [x] Batch-Export aller Objekte nach Page-JSON v0.2 (2030 Dateien, Session 24)

#### 5b: METS/MODS + PAGE XML (Zielformat)
- [x] PAGE XML Export (`export_pagexml.py`) — deterministisch, PAGE 2019
- [x] `export_mets.py` — METS-Container mit MODS (aus TEI-Metadaten) + PAGE XML Referenzen (Session 25)
- [x] TEI msDesc → MODS Mapping (automatisch via `parse_tei_full_metadata()`, Backup-Fallback fuer Korrespondenzen)
- [x] Batch-Export: 2074 METS-Dateien, 0 Fehler (Session 25)
- [ ] GAMS-Reingest-Test mit METS/MODS-Output

#### 5c: teiCrafter-Integration
- [ ] teiCrafter-Repo: JSON-Import in Step 1 einbauen
- [ ] teiCrafter-Repo: Sprachen (en/fr/it/es) und Epoche (20c) ergaenzen
- [ ] teiCrafter-Repo: DTABf-Schema um gap/del/add/stamp/table/cb erweitern
- [ ] teiCrafter-Repo: SZD-Mapping-Templates einfuegen (3 Templates)

### Phase 6: DIA-XAI-Bewertung (ab Oktober 2026)

- [ ] Transkriptionsergebnisse als Input fuer Expert-in-the-Loop-Workflow
- [ ] EQUALIS-Evaluierung

### FAIR4RS: offene Maßnahmen

Befund vom 2026-07-23 und Umsetzungsstand in `reports/fair4rs-verification-2026-07-23.md`. Dual-Licensing, `CITATION.cff`, `codemeta.json`, Description und Topics sind seit `2641b28` umgesetzt.

- [ ] Versionierte Releases mit Tags (F1.2)
- [ ] Zenodo-Release mit DOI, geschnitten wenn der Stand trägt (F1, A2)

## Status-Tracker

| Phase | Status | Notizen |
|---|---|---|
| Phase 1–3 | completed | |
| Phase 4 | in progress | Expert-Review, Neulauf der unvollständigen Transkriptionen, Editionsregeln |
| Phase 5 | in progress | GAMS-Reingest-Test, teiCrafter-Import |
| Phase 6 | pending | |
| FAIR4RS | in progress | Release und DOI |

Legende: completed, in progress, pending. Aktuelle Zahlen liefern `docs/catalog.json` und `python pipeline/transcribe.py --all --dry-run`.

## Offene Entscheidungen und Abhängigkeiten

Die Entscheidungen liegen bei der Projektleitung, zum Teil gemeinsam mit der Projekt-Reviewer:in, und stehen als Aufgaben in Phase 4.

- Editorische Regeln für Abbildungen und undefinierte Klammern, Text am Bildrand von Detailaufnahmen und Umstellungen, jeweils vor den Prompt- und Konverteränderungen ([[transcription-guidelines]] §8).
- Neuberechnung der Signale nach Korrekturen oder ihr bewusstes Einfrieren als Stand der Maschinenfassung.
- Empfehlung aus dem A/B/C-Experiment (Basismodell für Handschrift, `uncertain_words`).
- Label-Vokabular und Kompetenzgrundlage einer Freigabe ([[governance]] §5–6, [[review-findings]] B-08).

Neuläufe und Neuexporte brauchen API-Key und lokales Bild-Backup; ohne Backup fällt unter anderem `rights` aus `metadata.json` still weg. Die teiCrafter-Aufgaben liegen im teiCrafter-Repository. Phase 6 hängt am Start des DIA-XAI-Pilotprojekts ([[dia-xai-integration]]).
