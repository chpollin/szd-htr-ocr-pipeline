---
title: "Research Journal"
aliases: ["Journal"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Journal"
  version: 0.3
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/journal"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-journal"
status: active
created: 2026-03-30
updated: 2026-08-26
authors: [Christopher Pollin]
type: log
related:
  - "[[data-overview]]"
  - "[[verification-concept]]"
  - "[[annotation-protocol]]"
  - "[[evaluation-results]]"
---

# SZD-HTR — Research Journal

Chronologisches Log aller Arbeitssessions, Erkenntnisse und Entscheidungen.

---

## 2026-03-30 — Session 1: Projektplanung

### Was wurde gemacht
- CLAUDE.md gelesen und Projektanforderungen verstanden
- Implementierungsplan erstellt (→ [[plan]], damals `Plan.md` im Repo-Root)
- Knowledge-Ordner als Research-Vault angelegt

### Entscheidungen
- **Gemini 3.1 Flash-Lite** als Transkriptions-Provider
  - Guenstig ($0.25/1M input), schnell, 1M-Token-Kontext, multimodal
  - Ermoeglicht Kosten-/Qualitaetsvergleich zwischen Providern
- **Kategoriale Konfidenz** (sicher/pruefenswert/problematisch) statt numerischer Scores
  - Erfahrung aus coOCR HTR: LLMs koennen Qualitaet nicht zuverlaessig numerisch einschaetzen

### Offene Fragen
- [x] Wie gut erkennt Gemini Kurrentschrift? → high confidence bei Zweigs Handschrift (Session 2)
- [ ] Optimale Bildgroesse fuer API-Calls? Originale 4912x7360 (~1.4MB)
- [ ] Lizenz klaeren: MIT fuer Code, CC-BY fuer Daten?

---

## 2026-03-30 — Session 2: Pipeline aufgebaut, erste Tests, alle Sammlungen analysiert

### TEI-Metadaten heruntergeladen und analysiert

Vier TEI-XML-Dateien von stefanzweig.digital heruntergeladen. Detaillierte Analyse: [[data-overview]].

| Sammlung | TEI-Eintraege | mit PID | Groesse |
|---|---|---|---|
| Lebensdokumente | 143 | 120 | 666 KB |
| Werke | 352 | 162 | 1.6 MB |
| Aufsatzablage | 624 | 624 | 2.5 MB |
| Korrespondenzen | 723 | 0 (TEI) | 1.5 MB |

Backup-Daten (lokal): 1186 Korrespondenzen, 625 Aufsaetze, 169 Faksimiles. **Gesamtbestand: ~2107 digitalisierte Objekte.**

### Dreischichtiges Prompt-System entwickelt

System-Prompt (global) → Gruppen-Prompt (A-E) → Objekt-Kontext (aus TEI). Prompts unter `pipeline/prompts/`.

### Erste Transkriptionstests

| Objekt | Gruppe | Sprache | Confidence | Beobachtung |
|---|---|---|---|---|
| Theaterkarte Jeremias (o:szd.161) | D | DE | high | Gedruckter + handschriftl. Text korrekt |
| Certified Copy of Marriage (o:szd.160) | C | EN | high | Formularfelder korrekt |
| Verlagsvertrag Grasset (o:szd.78) | B | FR | high | Franz. Vertragstext, Durchstreichungen erkannt |
| Tagebuch 1918 (o:szd.72) | A | DE | high | Zweigs Handschrift fluessig gelesen |

**Kernbefund:** Gemini 3.1 Flash Lite liefert auf allen 4 Gruppen (A-D) high confidence. Zweigs Handschrift wird fluessig transkribiert.

### Neue Prompt-Gruppen aus Sammlungsanalyse

| Gruppe | Quelle | Objekte | Besonderheit |
|---|---|---|---|
| F: Korrekturfahne | Werke + Aufsatz | ~55 | Gedruckter Text + handschriftliche Korrekturen |
| G: Konvolut | Werke | 24 | Gemischte Materialien |
| H: Zeitungsausschnitt | Aufsatzablage | 312 | Gedruckt, oft Fraktur |
| I: Korrespondenz | Korrespondenzen | ~1186 | Handschriftliche Briefe |

### Erkenntnisse

1. **GAMS-URLs funktionieren als direkte Bildquellen** — kein Download/Hosting noetig.
2. **Korrespondenzen-TEI** hat nur Verzeichnis-Charakter. Metadaten aus Backup-metadata.json.
3. **Erwin Rieger** zweithaeufigste Hand in Aufsatzablage (225x) — eigene Handschrift.
4. **Zeitungsausschnitte (312)** brauchen eigenen Fraktur-Prompt.
5. **Lotte Zweig** zweithaeufigste Hand in Werken (83x).

---

## 2026-03-30 — Session 3: Phase 2 abgeschlossen, alle Sammlungen integriert

### Neue Gruppen-Prompts

- `group_f_korrekturfahne.md` — Gedruckter Text + Korrekturen
- `group_h_zeitungsausschnitt.md` — Zeitungsdruck, Fraktur-Hinweise
- `group_i_korrespondenz.md` — Briefstruktur, Postkarten-Doppelseiten

Gruppe G (Konvolut) bewusst aufgeschoben — zu wenige Objekte, zu heterogen.

### Pipeline auf Multi-Collection erweitert

`test_single.py` refactored mit `COLLECTIONS`-Dict, Enriched JSON-Output, `--list`. Neue Module: `tei_context.py`, `build_viewer_data.py`.

### Drei neue Test-Objekte

| Objekt | Sammlung | Gruppe | Confidence | Beobachtung |
|---|---|---|---|---|
| Der Bildner (o:szd.287) | Werke | F | high | Rodin-Gedicht fehlerfrei, Stempel erkannt |
| Aus der Werkstatt (o:szd.2215) | Aufsatzablage | H | high | Antiqua (kein Fraktur-Test) |
| Brief an Fleischer (o:szd.1079) | Korrespondenzen | I | high | Jugendhandschrift (1901) |

**Gesamtstand: 7/7 high confidence, alle 4 Sammlungen abgedeckt.**

### Erkenntnisse

1. Gemini meistert alle Dokumenttypen — kein einziges Objekt unter high.
2. Fraktur noch nicht getestet (Antiqua-Zeitungsausschnitt).
3. Enriched JSON-Format vereinfacht den Viewer-Build.

---

## 2026-03-31 — Session 4: Cleanup und Refactoring vor Phase 3

### Kernarbeiten

- `pipeline/config.py` — Gemeinsame Konfiguration (Pfade, Collections, Groups, API-Keys via .env)
- `requirements.txt` — Formale Dependencies
- Auto-Kontext aus TEI: `resolve_context()` ersetzt ~100 Zeilen manuelle Context-Strings
- Bug-Fix `resolve_group()`: Formular-Checks vor generischen Typoskript-Check

### Erkenntnisse

1. **Auto-Kontext funktioniert zuverlaessig**: 6/7 direkt aus TEI, 1/7 ueber Backup-Fallback.
2. **resolve_group() braucht semantische Ordnung**: Klassifikation vor Objekttyp pruefen.
3. **Gemeinsame config.py eliminiert Drift** zwischen Scripts.

---

## 2026-03-31 — Session 5: Phase 3 abgeschlossen, Batch-CLI und erster Lauf

### pipeline/transcribe.py

CLI-Modi: Einzelobjekt, Sammlung, `--all`, `--group`, `--limit`, `--force`, `--delay`, `--max-images`, `--dry-run`.

### Object Discovery

Primaerquelle: Backup-Verzeichnisse (TEI lueckenhaft bei PIDs).

| Sammlung | Backup-Objekte | PIDs in TEI |
|---|---|---|
| Lebensdokumente | 127 | 121 (85%) |
| Werke | 169 | 163 (46%) |
| Aufsatzablage | 625 | 625 (100%) |
| Korrespondenzen | 1186 | 0 |
| **Gesamt** | **2107** | |

### Erster Batch-Lauf: 5 Lebensdokumente

o_szd.100-104, alle Typoskript, alle high confidence. Skip-Logik funktioniert. **Gesamtstand: 12 Objekte.**

### Erkenntnisse

1. **Backup-Dirs zuverlaessiger als TEI** fuer Object Discovery.
2. **2s Delay reicht** fuer Rate-Limiting.
3. **Windows-Encoding (cp1252)**: Unicode-Zeichen verursachen Fehler → ASCII-Alternativen.

---

## 2026-04-01 — Session 6: Frontend-Refactoring, Verifikationskonzept

### CLAUDE.md ueberarbeitet

Veraltete Objektzahlen, Modell-Widerspruch (Claude als primaer, nur Gemini implementiert), Phasen inkonsistent. Komplett neu geschrieben, Plan.md als einzige Wahrheitsquelle.

### Frontend: Zwei Dateien → Single-Page-App

Vorher: `index.html` (Scroll-Dump) + `viewer.html` (Side-by-Side). Nachher:

| Datei | Funktion |
|---|---|
| `docs/index.html` | HTML-Skelett, Help-Modal |
| `docs/app.css` | SZD-Design-System (Burgundy/Gold, Source Serif/Sans) |
| `docs/app.js` | Routing, Katalog, Viewer, Edit, Export |

**Daten-Split:** `catalog.json` (~6 KB Metadaten) + `data/{collection}.json` (on-demand). Features: Sortierbare Tabelle, Hash-Routing (`#view/{id}/{page}`), Side-by-Side Viewer, GAMS-Thumbnails, Inline-Edit, JSON-Export.

**Design-System:** Burgundy `#631a34`, Gold `#C2A360`, Cream `#FAF8F3`, Source Serif 4, Source Sans 3, JetBrains Mono.

### Verifikationskonzept: 3 Ebenen

| Ebene | Signal | Staerke |
|---|---|---|
| 1 | Unsicherheits-Marker (`[?]`, `[...]`) | Stark |
| 2 | VLM-Selbsteinschaetzung | Schwach |
| 3 | Textstatistik (Zeichenzahl, Leerseiten) | Mittel |

Befund: 12/12 "high confidence", fast keine Marker. VLMs ueberschaetzen systematisch ihre Leistung → staerkere Metriken noetig.

### Frontend-Arbeiten

**Katalog:** Typ-Spalte zeigt TEI `classification` (Verlagsvertraege, Tagebuecher) statt Prompt-Gruppe. Tooltip zeigt `objecttyp`.

**quality_signals-UI vorbereitet:** Review-Spalte (Burgundy/Gruen-Badge, sortierbar, Toggle-Filter), Qualitaets-Panel im Viewer, Seiten-Anomalie-Marker. Graceful Degradation wenn Felder fehlen.

**Neue Felder in catalog.json:** `titleClean`, `signature`, `classification`, `objecttyp`, `thumbnail`, `pageCount`, `verification`.

**Datenfelder fuer die UI:** `obj.needsReview` (boolean), `obj.needsReviewReasons` (string[]), `obj.quality_signals` (ganzes Objekt), `obj.quality_signals.page_length_anomalies` (int[]).

**Methodische Befunde:** 12/16 Objekte haben 0 Marker. Marker-Dichte ist kein negatives, nur positives Signal. TEI-Klassifikation nutzbar fuer Sampling-Strategie.

Geloeschte Dateien: `docs/viewer.html`, `docs/data.json`.

---

## 2026-04-01 — Session 7: Gruppenabdeckung 9/9, Methodik, Frontend

### Gruppenabdeckung vervollstaendigt

| Objekt | Sammlung | Gruppe | Confidence | Beobachtung |
|---|---|---|---|---|
| o_szd.143 (Kontorbuch) | Lebensdokumente | E | high | Pipe-getrennte Spalten |
| o_szd.174 (Adressbuch) | Lebensdokumente | E | high | Tabellarisch |
| o_szd.2232 (Fraktur 1901) | Aufsatzablage | H | high | **Fraktur funktioniert** |
| o_szd.277 (Der Fall von Byzanz) | Werke | G | medium | Erstes non-high — heterogene Korrekturen |

**Alle 9 Gruppen A-I haben mindestens ein Testobjekt. Gesamtstand: 16 Objekte (15x high, 1x medium).**

### Methodische Deliverables

- [[verification-concept]] v2 (5 Abschnitte, Literatur-Review mit 6 Papers)
- [[annotation-protocol]] (8 Abschnitte, Normalisierung, Beispiele)
- [[verification-concept]] (5 Seiten, Pruefprotokoll, Eskalationsschwellen)

### Frontend: quality_signals-UI vorbereitet

Review-Spalte, Qualitaets-Panel, Seiten-Anomalie-Marker im Code, sobald die Datenfelder geliefert sind.

### Entscheidungen

- Pilot vor vollem GT-Sample (CER unbekannt)
- quality_signals sofort implementieren (kostenlos, kein GT noetig)
- Cross-Model: Agreement-First-Strategie
- Claude Sonnet als zweites Modell

---

## 2026-04-01 — Session 8: Interchange-Format, Selbstkritik, Korrekturen

### Methodische Deliverables abgeschlossen

- **htr-interchange-format.md** geschrieben — JSON Schema v0.1, Abgrenzung ALTO/PAGE/hOCR, Beispiel basierend auf o_szd.100.
- **verification-concept.md §1.9** geprueft und bestaetigt — keine Aenderungen noetig.
- Format und Schema fertig. Die weiterfuehrenden Schritte warten auf die Pilot-Durchfuehrung.

### Selbstkritische Review aller knowledge-Dokumente

Systematische Pruefung aller 6 knowledge-Dateien auf Konsistenz, Korrektheit und empirische Fundierung.

**Korrekturen durchgefuehrt:**
- **verification-concept.md**: Objektzahlen 12→16, Konfidenz "alle high" → "15 high + 1 medium", Gruppe G ins Sample-Design aufgenommen (31 statt 30), Anachronismus direkt in Fehlertaxonomie-Tabelle §1.5, empirische Einordnung der quality_signals ergaenzt (10/16 flagged = zu aggressiv)
- **journal.md**: Session 8 nachgetragen

**Kritische Befunde:**
1. **Marker-Problem bestaetigt:** 57.000 Zeichen, 2 Marker. marker_density ist kein funktionierendes Signal.
2. **quality_signals zu aggressiv:** 10/16 (63%) als needs_review geflaggt — hauptsaechlich page_image_mismatch bei normalen Leerseiten.
3. **Gruppen-Prompts:** Strukturelle Guidance (Briefformat) wirkt. Vorsichts-Guidance (Marker setzen bei Kurrent-Ambiguitaeten) wird ignoriert.
4. **Interchange-Format moeglicherweise verfrueeht:** Sinnvoll als Analyse, aber Schema vor CER-Kenntnis wenig dringend.
5. **30-Objekt-Sample:** Konkretes Design ist Platzhalter — haengt komplett vom Pilot ab.

### Entscheidungen

- Pilot bleibt der kritische naechste Schritt — alles andere ist Theorie
- quality_signals-Schwellenwerte muessen nach Pilot kalibriert werden (page_image_mismatch braucht Leerseiten-Toleranz)
- Prompt-Experiment ist wichtiger als gedacht (Evidenz fuer Wirkungslosigkeit der Vorsichts-Prompts)

---

## 2026-04-01 — Session 9: Selbstkritische Review

### Systematische Pruefung aller knowledge-Dokumente

Alle 6 knowledge-Dateien auf Konsistenz, empirische Fundierung und Redundanz geprueft.

### Korrekturen

- **verification-concept.md**: Objektzahlen 12→16, Konfidenz 15h+1m, Gruppe G ins Sample (31 statt 30), Anachronismus in Fehlertaxonomie-Tabelle §1.5, empirische Einordnung der quality_signals in §2.3
- **verification-concept.md §1.9**: Prompt-Wirksamkeit als neue Frage in §3.1

### Empirische Befunde (aus 16 Ergebnis-JSONs)

1. **Marker-Problem**: 57.000 Zeichen, 2 Marker. marker_density ist kein Signal.
2. **quality_signals**: 10/16 (63%) als needs_review — zu aggressiv, hauptsaechlich page_image_mismatch.
3. **Gruppen-Prompts**: Strukturelle Guidance wirkt (Briefformat), Vorsichts-Guidance ignoriert (0 [?]-Marker bei Kurrent).
4. **o_szd.143**: Nur 20 Zeichen — moeglicherweise Pipeline-Problem (ungeklaert).

---

## 2026-04-01 — Session 11: Verification-by-Vision, Build

### Verification-by-Vision getestet

8 Objekte via Vision verifiziert (Bild lesen + Transkription vergleichen). 8 von 9 Gruppen abgedeckt:
- o_szd.161 (D Kurztext): `llm_verified` — null Fehler
- o_szd.72 (A Handschrift/Kurrent): `llm_error_suggestion` — Kurrent-Ambiguitaeten, keine Halluzinationen
- o_szd.277 (G Konvolut): `llm_error_suggestion` — klare Fehler ("entbalten", "Ictreesten") in Korrekturschicht
- o_szd.139 (C Formular): `llm_error_suggestion` — minor ("Datum:"-Label inkonsistent)
- o_szd.1887 (F Korrekturfahne): `llm_error_suggestion` — Drucktext OK, handschriftl. Vermerke problematisch
- o_szd.2232 (H Zeitungsausschnitt/Fraktur): `llm_error_suggestion` — 3 typische Fraktur-Fehler (fl-Ligatur, langes s, u/n)
- o_szd.1079 (I Korrespondenz): `llm_error_suggestion` — "Gerichte"→"Gedichte" (d/r), Ortsname "Klard" existiert nicht
- o_szd.147 (C Formular): **BROKEN** — 64 Bilder, 0 Seiten transkribiert (Pipeline-Bug)

Spec geschrieben, heute in [[verification-concept]] Abschnitt 5 konsolidiert (10 Abschnitte, JSON-Schema, empirische Befunde).

### Build ausgefuehrt

`build_viewer_data.py`: 62 Objekte im Frontend (46 Lebensdokumente, 13 Werke, 2 Aufsatzablage, 1 Korrespondenz).

### Arbeitsstand

- Frontend: Dashboard und Diff-Prototyp fertig
- Methodik: neue Schritte 5-7
- Backend: Status auf ~62 Objekte, Interchange-Export als naechster Schritt

### Erkenntnisse

1. **Verification-by-Vision funktioniert** — actionable Fehler in ~2 Min/Objekt, kein API-Cost fuer den Vision-Vergleich.
2. **Muster:** Drucktext korrekt, Handschrift gut, Korrekturen/Vermerke schwach (~60-70%).
3. **Pipeline-Bug:** Objekte mit vielen Bildern (o_szd.147: 64 Bilder) erzeugen leere Ergebnisse.
4. **Methodischer Beitrag:** VbV ist der staerkste Verifikationsansatz im Projekt — direkter Bild↔Text-Vergleich statt nur Textvergleich. Fuer den Aufsatz relevant.

---

## 2026-04-01 — Session 12: Mapping-Templates, JSON-Schema, DIA-XAI-Integration

### Methodik: 3 Bonus-Deliverables

**1. JSON-Schema als validierbare Datei**
`schemas/htr-interchange-v0.1.json` — das Schema aus htr-interchange-format.md §3 als eigenstaendige Datei. Aenderungen gegenueber Codeblock: `$id` auf GitHub Pages URL, `source.language` mit Regex-Pattern (`^[a-z]{2,3}$`), `source.document_type` als kontrolliertes Vokabular (14 Enum-Werte). Validiert mit `python -m json.tool`.

**2. DIA-XAI-Integrationskonzept**
`knowledge/dia-xai-integration.md` — 5 Abschnitte:
- Pipeline-Diagramm SZD-HTR → DIA-XAI
- EQUALIS-Mapping: 5 Dimensionen (E/QUA/L/I/S) auf konkrete SZD-HTR-Datenquellen
- Metriken-Export (`dia-xai-metrics-v1` JSON)
- Zeitplan: Was muss vor DIA-XAI Phase 1 (Mai 2026) fertig sein
- UC3 (HTR-Verifikation) als Ziel-Use-Case

### Erkenntnisse

1. **DIA-XAI ist Aggregator, nicht Verifikationstool** — importiert Metriken-JSON, macht keine eigene Analyse. Die Verifikation passiert in SZD-HTR (VbV und Expert-Review).
2. **EQUALIS-Scalability (S-Dimension)** profitiert besonders von SZD-HTR: 9 Gruppen × 4 Sprachen × 6+ Haende = natuerliche Varianz.
3. **Kritischer Pfad unveraendert:** Pilot (5 Seiten) muss vor DIA-XAI Phase 1 fertig sein.

---

## 2026-04-01 — Session 13: Quality Infrastructure, Batch-Lauf, Modellkonsensus

**Schwerpunkt:** Pipeline-Qualitaetsinfrastruktur aufgebaut, parallelen Batch gestartet, Forschung zu GT-freier Qualitaetsbewertung.

**Neue Pipeline-Module:**
- `evaluate.py`: CER/WER-Berechnung mit vollstaendiger Normalisierung (annotation-protocol.md §5)
- `quality_report.py`: Aggregierte Qualitaetsstatistiken pro Gruppe/Sammlung
- quality_signals v1.1: Schwellenwerte rekalibriert basierend auf Datenanalyse (68% → 44% needs_review)
- Exponential Backoff (429-Retry) in transcribe.py fuer parallele Batch-Laeufe

**Rekalibrierungsergebnisse (87 Objekte):**
- duplicate_pages: 25 → 17 (Jaccard 0.9 + min 200 chars)
- page_image_mismatch: 21 → 7 (75% statt 50% empty threshold)
- page_length_anomaly: 12 → 5 (10% statt 20% median)
- Kerninsight: Signale fingen Sammlungseigenschaften (leere Rueckseiten, Cover), nicht Fehler

**Batch-Lauf:** 4 parallele Prozesse (Korrespondenzen, Aufsatzablage, Lebensdokumente, Werke), delay 4s. ~360+ Objekte fertig und wachsend. Keine Rate-Limit-Probleme bei ~60 RPM effektiv.

**Broken Objects:** 3/5 repariert (o_szd.147, o_szd.223, o_szd.245). 2 bleiben kaputt: o_szd.267 (107 Bilder, zu gross) und o_szd.2230 (leere API-Antwort).

**Forschung GT-freie Qualitaetsbewertung:**
- Gemini logprobs: NICHT verfuegbar fuer Flash Lite Preview (getestet, 400 INVALID_ARGUMENT). Verfuegbar fuer gemini-2.0-flash.
- Aktuellste Literatur recherchiert: Zhang et al. 2025 (Consensus Entropy, ICLR 2026), Risk-Controlled VLM OCR (arXiv 2026), Beyene & Dancy 2026 (Survey)
- Kernentscheidung: **Modellkonsensus statt manuellem GT** — 3 Modelle (Flash Lite + Flash + Claude Judge) als automatische GT-Generierung
- verification-concept.md um Abschnitt 7 (Modellkonsensus) erweitert

**Entscheidungen:**
- DWR (Dictionary Word Ratio) als ergaenzendes Signal — einfach, bewaehrt, aber nicht primaer
- PPPL (Pseudo-Perplexity) auf spaeter verschoben — zu schwere Dependency (transformers+torch)
- Modellkonsensus-Ansatz als naechster Schritt statt manuellem Pilot

---

## 2026-04-02 — Session 14: Modellkonsensus-Metriken v2, GT-Pipeline, Frontend Review

**Schwerpunkt:** Modellkonsensus-Validierung mit verbesserten Metriken, GT-Erzeugung mit 3 Modellen, Frontend-Erweiterung fuer Expert-Review.

### Modellkonsensus-Metriken v2

- **Problem identifiziert:** Alte CER-only-Metrik produzierte 74% "divergent" — hauptsaechlich wegen Reading-Order-Divergenz (Marginalia, Spalten) und Seiten-Halluzination, nicht wegen Lesefehler.
- **Neue Metriken in evaluate.py:**
  - `normalize_for_consensus_orderless()`: Sortiert Zeilen vor Vergleich
  - `word_overlap()`: Jaccard-Aehnlichkeit auf Wortmengen (order-invariant)
  - `effective_cer`: Minimum aus ordered und orderless CER
- **4-Tier-Klassifikation:** verified / moderate / review / divergent (statt 3-Tier)
  - word_overlap >= 0.90 begrenzt Kategorie auf maximal "moderate"
  - word_overlap >= 0.75 ergibt "review" (neues Zwischenniveau)
- **Ergebnis (27 Objekte, 3/Gruppe):** 26% verified, 33% moderate, 15% review, 26% divergent (vorher: 11% verified, 74% divergent)

### Kernerkenntnisse aus Modellkonsensus-Analyse

1. **Reading-Order-Divergenz**: o_szd.142 hat CER 55% aber word_overlap 100% — identische Woerter in anderer Reihenfolge.
2. **Seiten-Halluzination**: Flash Lite dupliziert gelegentlich Seiten (o_szd.101, Seiten 3/4). quality_signals v1.4: Duplikat-Schwelle 200→50 Zeichen.
3. **Bleed-Through**: VLM transkribiert durchscheinenden Rueckseiten-Text. System-Prompt Regel 9 eingefuegt.
4. **Korrekturfahnen geloest**: 3/3 verified, <1% CER. Gedruckter Text mit Korrekturen ist kein Problem.
5. **Korrespondenzen bleiben schwer**: 3/3 divergent, 59-104% CER. Zweigs Handschrift in Briefen ist genuinely ambig.

### GT-Pipeline (generate_gt.py)

- 18 Objekte (stratifiziert, 2/Gruppe + 3 Korrespondenzen) mit Gemini 3.1 Pro transkribiert
- 3-Modell-Merge: Flash Lite (A) + Flash (B, aus Modellkonsensus) + Pro (C)
- Merge-Logik: consensus_3of3 (CER <2% paarweise) / majority_2of3 (CER <5%) / pro_only
- **Ergebnis (46 Content-Seiten):** 15 Modellkonsensus (33%), 20 Mehrheit (43%), 11 Pro-only (24%)
- Korrekturfahne o_szd.1888: 3/3 Modellkonsensus auf allen Content-Seiten
- GT-Drafts in `results/groundtruth/{object_id}_gt_draft.json`

### Frontend: GT Review-Modus

- "GT Review"-Button im Viewer (nur localhost)
- 3-Varianten-Panel: Flash Lite / Flash / Pro mit Click-to-Select
- Source-Badges: gruen (3/3), gelb (2/3), rot (Pro only)
- Approve-Button pro Seite, localStorage-Persistenz
- JSON-Export als `{object_id}_gt.json` mit Expert-Metadaten
- `build_viewer_data.py` erzeugt `docs/data/groundtruth.json` (18 Objekte)

### Neue Dateien

- `pipeline/generate_gt.py` — GT-Erzeugung mit 3 Modellen
- `pipeline/evaluate.py` — erweitert um `normalize_for_consensus_orderless()`, `word_overlap()`
- `docs/data/groundtruth.json` — GT-Drafts fuer Frontend

### Entscheidungen

| Entscheidung | Begruendung |
|---|---|
| word_overlap als order-invariante Metrik | CER bestraft Reading-Order-Divergenz unfair; Jaccard auf Wortmengen ist robust |
| 4-Tier statt 3-Tier Klassifikation | "review" als Zwischenstufe fuer Objekte mit 75-90% word_overlap |
| Gemini Pro statt Claude als 3. GT-Modell | Gleiche API, kein Provider-Wechsel, staerkstes Gemini-Modell |
| 5-Seiten-Pilot uebersprungen | Modellkonsensus-Validierung + GT-Pipeline beantworten die Pilot-Fragen empirisch |
| Bleed-Through im System-Prompt | Effizienter als Post-Processing; VLM soll es gar nicht erst transkribieren |

### Frontend-Upgrade

- **build_viewer_data.py Bug-Fixes:** Consensus-Dateien aus Katalog entfernt (583→564 Objekte), quality_signals Naming-Mismatch behoben (camelCase→snake_case), alle 20 QS-Felder inkl. dwr_score exportiert
- **Modellkonsensus-Daten im Frontend:** 29 Objekte mit consensus category/CER im Katalog, volle Modellkonsensus-Daten (transcription_a/b) in Collection-JSONs fuer Diff-View
- **Diff-Ansicht:** DIFF_PLACEHOLDER durch echte Modellkonsensus-Daten ersetzt, CER im Header, dynamische Modell-Namen, Button disabled ohne Modellkonsensus
- **Enhanced Stats Dashboard:** Seiten-Stats, Zeichen-Summen, Konfidenz-Verteilung, Review-%, DWR-Durchschnitt, Modellkonsensus-Uebersicht
- **Neue Anzeigen:** DWR-Badge im Viewer, Page-Type-Badges (Leer/Farbskala), Modellkonsensus-Status V/M/R/D im Katalog + Viewer, per-Page Agreement-Dots, Modellkonsensus-Filter
- **Mobile:** Card-Layout fuer Katalog unter 600px
- **Refactoring (7x):** Modellkonsensus-Konstanten extrahiert, redundante Aufrufe entfernt, Inline-Styles→CSS, clearFilters vereinfacht, Feature-Flags gecacht, CSS-Fallback fuer Thumbnails

### Layout-Analyse + PAGE XML (neu)

- **`layout_analysis.py`:** VLM-basierte Layout-Analyse (Gemini Flash Lite, 1 Call/Seite), erkennt 5 Regionentypen (paragraph, heading, list, table, marginalia) mit Bounding Boxes in Prozent-Koordinaten
- **`export_pagexml.py`:** Deterministischer PAGE XML 2019 Export — merged OCR-Text + Layout-Regionen, proportionales Text-Alignment nach Zeilenschaetzung
- **`prompts/layout_system.md`:** Eigener System-Prompt fuer Layout-Analyse
- **`schemas/layout-regions-v0.1.json`:** Validierbares JSON-Schema
- **Test:** o_szd.100 (Typoskript, Vertrag) — 15 Regionen erkannt, PAGE XML valide
- **Dokumentation:** `knowledge/layout-analysis.md` erstellt, `htr-interchange-format.md` §7 aktualisiert

---

## 2026-04-02 — Session 15: Knowledge Vault Frontend + Projekt-Seite

**Schwerpunkt:** Knowledge Vault (12 Markdown-Dokumente) als navigierbare Ansicht ins Frontend bringen. Projekt-Seite aus README.md. README aktualisieren.

### Knowledge Vault im Frontend

- **Build-Pipeline:** `build_knowledge()` in `build_viewer_data.py` — liest `knowledge/*.md`, parst YAML-Frontmatter, loest Wikilinks zur Build-Zeit auf, konvertiert Markdown zu HTML (Python `markdown` mit `tables`, `fenced_code`, `toc`), extrahiert TOC-Headings
- **Output:** `docs/data/knowledge.json` — 12 Dokumente + About-Seite (aus README.md), Sektions-Struktur aus `index.md`
- **Neue Python-Dependencies:** `markdown>=3.5`, `pyyaml>=6.0` in `requirements.txt`
- **Frontend-Routing:** 3 neue Hash-Routes:
  - `#knowledge` — Index mit Card-Layout, gruppiert nach Leseordnung / Spezifikationen / Projektlog
  - `#knowledge/{slug}` — Einzeldokument mit Sidebar (TOC, Metadaten, Related Links, Prev/Next)
  - `#about` — Projekt-Seite (gerendert aus README.md)
- **CSS:** View-Toggles fuer 5 Views, Knowledge-Cards, Knowledge-Doc Grid (Sidebar + Content), Markdown-Content-Styles (Headings, Tabellen, Code-Bloecke, Wiki-Links, Blockquotes), About-Seite, responsive Breakpoints (900px, 600px)
- **Navigation:** "Methodik" + "Projekt" Links im Header (alle Views sichtbar), Escape-Key zurueck, Wiki-Links als `<a href="#knowledge/...">` direkt via Hash-Routing

### README.md aktualisiert

- 575/2107 Objekte (27%), 3463/18719 Seiten (18%)
- Quality Signals v1.3 → v1.4
- Pipeline-Architektur: verify.py, generate_gt.py, build_viewer_data.py Downstream ergaenzt
- Projektstruktur: generate_gt.py, layout_analysis.py, export_pagexml.py, groundtruth/ ergaenzt
- Farbskala-Spalte in Statistik-Tabelle

### Designentscheidung

| Entscheidung | Begruendung |
|---|---|
| Pre-rendered HTML statt Client-Side Markdown | App hat null Runtime-Dependencies, kein Flicker, Wiki-Links zur Build-Zeit aufgeloest |
| Eine knowledge.json statt 12 Einzeldateien | Gesamtgroesse ~200-300 KB, einmal laden, sofort navigieren |
| Header-Nav statt eigener Sidebar-Navigation | Minimal-invasiv, folgt bestehendem Pattern, keine Mobile-Hamburger noetig |

### Neue/Geaenderte Dateien

- `pipeline/build_viewer_data.py` — `build_knowledge()`, `parse_frontmatter()`, `parse_index_sections()`
- `docs/index.html` — Nav-Links + 3 `<main>` Elemente
- `docs/app.css` — Sektionen 15-20 (Knowledge, Knowledge-Doc, Markdown, About, Responsive)
- `docs/app.js` — `ensureKnowledgeData()`, `showKnowledgeIndex()`, `renderKnowledgeIndex()`, `showKnowledgeDoc()`, `renderKnowledgeDoc()`, `showAbout()`
- `docs/data/knowledge.json` — generiert (12 Docs + About)
- `requirements.txt` — +markdown, +pyyaml
- `README.md` — Statistiken + Struktur aktualisiert

---

## 2026-04-02 — Session 16: Expert-Review Write-Back, 3-Tier Review, Katalog-Bereinigung

**Schwerpunkt:** Bidirektionaler Expert-Review-Workflow, 3-stufiger Review-Status, Katalog-Bereinigung, Knowledge Vault Konsolidierung.

### Ergebnisse

- **`import_reviews.py`**: Importiert Frontend-Exporte (GT-Reviews + regulaere Edits) zurueck in Pipeline-JSONs. Schreibt `review`-Objekt mit `status`, `reviewed_by`, `reviewed_at`.
- **3-stufiger Review-Status**: `needs_review: true` (rot), kein Review (LLM OK, orange), `review.status: "approved"` (gruen). `gtVerified` fuer GT-Objekte.
- **Katalog-Bereinigung**: Test-Daten, Layout-JSONs, GT-Drafts, Pro-Zwischenergebnisse aus Viewer-Daten gefiltert (627 → 601). Color-Chart-Seiten (158) aus Viewer entfernt.
- **Knowledge Vault Konsolidierung**: 13 → 11 Docs, Frontmatter vereinheitlicht, Claude Code Banner im Frontend.
- **3 GT-Objekte verifiziert**: o_szd.153, o_szd.137, o_szd.194.

---

## 2026-04-02 — Session 17: Chunking, Objekt-Prompts, Review-Server

**Schwerpunkt:** Pipeline-Readiness fuer Gesamtdurchlauf. Chunking fuer grosse Objekte, Objekt-Prompt-Overrides, lokaler Dev-Server mit Review-API, erste Expert-Verifikationen.

### Chunking fuer grosse Objekte

- **Problem:** 44 Objekte hatten weniger Bilder verarbeitet als vorhanden (z.B. Hauptbuch o_szd.143: 3 statt 249 Bilder). Ursache: API-Kontextlimit bei vielen hochaufloesenden Bildern.
- **Loesung:** Automatisches Chunking in `transcribe.py`: Objekte mit >20 Bildern werden in Chunks aufgeteilt, separat transkribiert, Ergebnisse gemergt. Seitennummerierung bleibt durchgehend.
- **CLI:** `--chunk-size N` (Default: 20)
- **Test:** Hauptbuch (249 Bilder, 13 Chunks) → 249/249 Seiten, ~197.000 Zeichen. Erster Durchlauf: Chunk 2 scheiterte (JSON nicht parsebar), Bug gefixt (Platzhalter-Seiten fuer fehlgeschlagene Chunks). Zweiter Durchlauf: komplett.
- **Refactoring:** `transcribe_object()` aufgeloest in `_call_api()`, `_parse_with_retry()`, `_transcribe_single_call()`, `_transcribe_chunked()`.

### Objekt-Prompts (4. Prompt-Schicht)

- **Motivation:** Bankkontoauszuege (o_szd.1056) — tabellarische Struktur ging im Formular-Prompt verloren.
- **Loesung:** Optionaler Objekt-Prompt in `prompts/objects/{object_id}.md` ueberschreibt Gruppen-Prompt.
- **Ergebnis:** o_szd.1056 neu transkribiert — 11 statt 3 Seiten, Tabellenstruktur teilweise als Markdown.
- **Erkenntnis:** VLM wendet Tabellenanweisung inkonsistent an (Seite 1 ja, Folgeseiten nein). Strukturrekonstruktion besser in Layout-Analyse / TEI-Export.

### Lokaler Dev-Server (`serve.py`)

- **Problem:** Edit/Approve im Frontend speicherte nur in localStorage, nicht in Pipeline-JSONs. Workflow: Export-JSON herunterladen → CLI → Import. Zu umstaendlich.
- **Loesung:** `pipeline/serve.py` — Python HTTP-Server, der Frontend ausliefert + API-Endpunkte hat:
  - `GET /api/status` → `{"local": true}` (Frontend erkennt lokalen Server)
  - `POST /api/approve` → schreibt `review.status: "approved"` direkt ins Pipeline-JSON
  - `POST /api/edit` → schreibt editierte Seiten + Review
  - `POST /api/rebuild` → fuehrt `build_viewer_data.py` aus
- **Architektur-Entscheidung:** Kein localStorage als Datenquelle. Pipeline-JSONs sind die einzige Quelle der Wahrheit. Frontend-Claude muss `fetch('/api/...')` Calls einbauen.
- **Nutzung:** `python pipeline/serve.py --port 5501 --rebuild`

### Erste Expert-Verifikationen (GT-Workflow)

- 3 Objekte approved: o_szd.153 (Briefkarte blanko), o_szd.137 (At Home Card), o_szd.194 (Briefregister)
- o_szd.194: Seite 4 manuell geleert — durchscheinende Schrift (bleed-through) war faelschlich transkribiert worden
- GT-Kandidatenliste: 18 Objekte stratifiziert ueber alle 9 Gruppen, 4 Sammlungen

### Katalog-Bereinigung

- **Duplikat-Fix:** 18 Duplikate im Katalog (Pro-Modell-Zwischenergebnisse). SKIP_SUFFIXES erweitert um `_gemini-3.1-pro` und `_judge_data`. Katalog: 657 → 639 Objekte.
- **.gitignore:** `*.bak` Backup-Dateien ausgeschlossen.

### Batch-Ergebnisse

- ~63 neue Korrespondenzen (o_szd.1454–1543), Abdeckung 24% → ~30%
- Hauptbuch komplett (249/249 Seiten)
- o_szd.1056 mit Objekt-Prompt neu transkribiert (11 Seiten)

### Identifizierter Refactoring-Bedarf

| Bereich | Problem | Prioritaet |
|---|---|---|
| `build_viewer_data.py` | Blacklist-Ansatz (SKIP_SUFFIXES) fragil — Whitelist-Ansatz besser | hoch |
| `serve.py` | File-Writes ohne try-except, Content-Length ohne Obergrenze | hoch |
| `serve.py` + `import_reviews.py` | Duplizierte Logik (Datei-Suche, Backup-Write, Page-Update) | mittel |
| `config.py` | CHUNK_SIZE, DEFAULT_REVIEWER, VERIFY_MODEL nicht zentralisiert | mittel |
| Datenintegritaet | ~44 Objekte mit unvollstaendigen Seiten, ~20 mit parse-Fehlern | hoch |
| Prompt-Loading | `load_prompt()` Regex fragil bei Codeblock-Varianten (`json` etc.) | niedrig |

### Neue/Geaenderte Dateien

- `pipeline/transcribe.py` — Chunking, Objekt-Prompts, Refactoring
- `pipeline/serve.py` — NEU: Lokaler Dev-Server mit Review-API
- `pipeline/build_viewer_data.py` — SKIP_SUFFIXES erweitert
- `pipeline/prompts/objects/o_szd.1056.md` — NEU: Erster Objekt-Prompt
- `.gitignore` — `*.bak` hinzugefuegt
- `CLAUDE.md` — Chunking, serve.py, Objekt-Prompts, Session 17
- `README.md` — 4-Schicht-Prompt, Chunking, serve.py

---

## 2026-04-02 — Session 18: Expert-Review, Agent-Verifikation, CER-Baseline

**Schwerpunkt:** 26 Objekte verifiziert (12 Agent + 14 Mensch), neuer Review-Tier `agent_verified`, CER-Baseline ueber alle 9 Gruppen, Knowledge Vault Refactoring.

### Expert-Review (Human)

- 7 kurze Objekte (Siegelstempel, Ex Libris, Briefumschlaege) approved
- o_szd.1888 (Korrekturfahne, Hans Carossa): 2 Fehler gefunden und korrigiert — fehlendes "nicht", Wortgrenze "erhobene Hand"
- Weitere 4 Objekte ueber serve.py approved (Frontend → API jetzt korrekt verdrahtet)
- **Insgesamt 14 human-approved Objekte**

### Agent-Verifikation (NEU)

Neuer Review-Tier zwischen Human Approved und LLM OK: agentenbasierte Vision-Verifikation (Opus 4.6 mit Vision) vergleicht Faksimile-Bilder gegen VLM-Transkription.

- **Erste Charge (4 Objekte):** Typoskript, Zeitungsausschnitt, Konvolut, Formular. Schwere Fraktur-Fehler gefunden: "selbstfeligen" → "selbstseligen", "gereiste" → "gereifte" (f/s-Verwechslung).
- **Zweite Charge (8 Objekte):** Korrespondenz, Handschrift, Korrekturfahne, Zeitungsausschnitt. Strukturfehler bei tabellarischen Daten (o_szd.1475: Betraege falscher Zeile zugeordnet).
- **Insgesamt 12 agent-verified Objekte**, Fehler direkt korrigiert.

Implementierung: `serve.py` akzeptiert `status: "agent_verified"` mit Metadaten (`agent_model`, `errors_found`, `estimated_accuracy`). Frontend: blauer Badge "Agent ✓".

### CER-Baseline (→ [[evaluation-results]])

| Dokumenttyp | Genauigkeit |
|---|---|
| Gedruckter Text (Antiqua) | 99.6–99.9% |
| Fraktur | 99.7–99.8% (aber systematische f/s-Fehler) |
| Handschrift (sauber) | 99.1–99.4% |
| Tabellarisch/Struktur | ~90% |

### Bugfixes

- **Farbkarten-Klassifikation:** `_classify_page()` pruefte Keywords nur bei <10 Zeichen. Fix: Keywords vor Laengencheck, +5 neue Keywords (kodak, farbkontroll, etc.). 10 Seiten korrigiert.
- **Frontend API:** Approve- und Edit-Buttons schrieben nur in localStorage, nicht an `/api/approve`/`/api/edit`. Fix: `fetch()` in `toggleObjectApproval()` und `saveCurrentEdit()`.
- **Test-Daten entfernt:** `results/test/` (7 Dateien) + `pipeline/test_single.py` geloescht.

### Knowledge Vault Refactoring

- **NEU: `evaluation-results.md`** — CER-Baseline, Fehlertypen, Methodik
- **MERGE: `pilot-design.md`** → `verification-concept.md` §1.9 (Adaptive Sampling-Anpassung)
- **NEU: `verification-concept.md` §8** — Agent-Verifikation (4-Tier-Modell, technische Umsetzung)
- Journal: Session 16 nachgetragen, Session 18 dokumentiert.

### Statistiken

| Metrik | Wert |
|---|---|
| Reviewed Objekte (gesamt) | 26 (14 human + 12 agent) |
| Gruppen-Abdeckung | 9/9 |
| Korrekturen (Agent) | 15 Fehler in 12 Objekten |
| Korrekturen (Human) | 2 Fehler in 1 Objekt |
| Commits | 6 |

---

## 2026-04-02 — Session 19: Korrespondenz-Batch + Agent-Verifikation Batch 3

**Schwerpunkt:** 100 neue Korrespondenz-Transkriptionen, Agent-Verifikation von 8 Objekten (Korrespondenzen an Max Fleischer), systematische Fehlermuster bei Kurrent dokumentiert.

### Batch-Transkription

- **100 neue Korrespondenzen** (o_szd.1545–o_szd.1666), laeuft aktuell
- Abdeckung Korrespondenzen steigt von 350/1186 (30%) auf ~450/1186 (~38%)
- Batch-Steuerung: `--limit 450` noetig, weil `--limit 100` nur die ersten 100 sortierten Objekte nimmt (alle bereits erledigt). Erste 350 werden in Sekunden uebersprungen.

### Agent-Verifikation Batch 3 (8 Objekte, Korrespondenzen)

Agentenbasierte Vision-Verifikation von 8 Objekten. Alle Objekte sind Korrespondenzen an Max Fleischer (~1901-1902).

| Objekt | Fehler | Genauigkeit | Editiert | Hauptprobleme |
|---|---:|---:|---|---|
| o_szd.1079 | 3 | 99.7% | 3, 4 | Kurrent h/I-Verwechslung, "nicht"/"auch" |
| o_szd.1081 | 2 | 97.9% | 1, 2 | "Stud. iur." → "Hud. inr." (Kurrent St/H) |
| o_szd.1088 | 3 | 97% | 1, 2 | "Dein" → "H[?]", halluziniertes "An" |
| o_szd.1090 | 8 | 90% | 1, 2 | Nonsens-Halluzination bei hastiger Kurrent |
| o_szd.1093 | 13 | 94% | 1, 2 | Kurrent massiv verlesen (Postkarte 1902) |
| o_szd.1096 | 0 | ~98% | — | Fehlerfrei, False-Positive bei Duplikat-Flag |
| o_szd.1097 | 2 | 99% | 2 | Fehlende Buchstaben in Komposita |
| o_szd.1100 | 2 | 95% | 2 | Kurrent L/B-Verwechslung, Grussformel |

**Aggregat: 33 Fehler in 8 Objekten, Durchschnitt ~96.3% Genauigkeit.**

### Systematische Fehlermuster (NEU)

**1. Kurrent-Buchstabenverwechslungen** (haeufigste Fehlerquelle):
- h ↔ I, n ↔ u, r ↔ v, L ↔ B, St ↔ H, f ↔ s
- Ursache: Kurrent-Minuskeln unterscheiden sich systematisch von Antiqua. Gemini kennt die Unterschiede nicht zuverlaessig.
- Besonders betroffen: hastige Schrift, kleine Postkarten, rote Tinte auf Bildhintergrund

**2. Nonsens-Halluzination statt Unsicherheitsmarker**:
- Gemini erfindet echte Woerter statt `[?]` zu setzen: "Langentour Kantgewalt" statt "Laufenden" (o_szd.1090)
- Bereits in Session 8 beobachtet (Vorsichts-Guidance wird ignoriert), hier erstmals quantifiziert
- Konsequenz: `marker_density` ist als Quality-Signal nahezu wertlos

**3. Systematisches "An" auf Adressseiten**:
- In 3 von 8 Objekten halluziniert Gemini ein "An" vor dem Adressaten
- Auf den Originalen steht kein "An" — die Adresse beginnt direkt mit dem Namen
- Fix: Hinweis im Gruppen-Prompt I (Korrespondenz) oder Post-Processing

**4. Grussformel-Fehler**:
- Zeilenumbrueche in Schlussformeln werden falsch zugeordnet
- "Liebsten Gruss" → "Besten Gruss" (L/B-Verwechslung in Kurrent)
- Epistolarische Konventionen koennten als Kontexthilfe im Prompt helfen

### Quality-Signals Erkenntnisse

- **`duplicate_pages` False-Positive**: Triggert bei Color-Chart-Doppelfotografie (selbe Seite mit/ohne Farbskala). Fix: Color-Chart-Seiten von Duplikat-Erkennung ausschliessen.
- **`needs_review` korrekt bei echten Problemen**: o_szd.1090 und o_szd.1093 (die schlechtesten) waren beide geflaggt.
- **`marker_density` wertlos**: Gemini setzt auch bei 10% Fehlerrate keine `[?]`-Marker.
- **DWR als Alternative**: DWR-Score korreliert vermutlich besser mit tatsaechlicher Fehlerrate als marker_density — noch zu validieren.

### Statistiken

| Metrik | Wert |
|---|---|
| Neue Transkriptionen | ~100 (laeuft noch) |
| Agent-verifizierte Objekte (Batch 3) | 8 |
| Korrekturen (Agent Batch 3) | 33 Fehler |
| Kumulativ agent-verified | 20 (12 + 8) |
| Kumulativ reviewed gesamt | 34 (14 human + 20 agent) |

---

## 2026-04-02 — Session 20: Edit-Tracking + 24 Agent-Verifikationen

### Was wurde gemacht

**1. Edit-Tracking-System implementiert**

Problem: Agent-Korrekturen ueberschrieben den Originaltext ohne Spur — kein programmatischer Diff moeglich.

Loesung: `edit_history`-Array auf Seitenebene im Ergebnis-JSON:
```json
"edit_history": [{
  "original_transcription": "Originaltext vor Korrektur",
  "edited_by": "Claude Code Agent",
  "edited_at": "2026-04-02T...",
  "source": "agent"   // oder "human"
}]
```

Aenderungen:
- `serve.py`: Menschliche Edits speichern jetzt automatisch `edit_history` vor dem Ueberschreiben
- `backfill_edit_history.py`: Einmal-Script, hat 5 Seiten in 4 Dateien aus Git-History rekonstruiert
- Frontend: Neuer Tab "Korrekturen" neben "Modellkonsensus" in der Diff-Ansicht (gruen/amber Farbschema)
- CSS: Edit-Diff-Variablen, Tab-Styles

**2. Agent-Verifikation: 24 Objekte in 4 Batches**

| Batch | Fokus | Objekte | Fehler gesamt | Korrekturen |
|---|---|---:|---:|---:|
| 1 | 1-Seiter, diverse Gruppen | 8 | 11 | 6 Seiten |
| 2 | Alle 8 Gruppen abgedeckt | 8 | 15 | 3 Seiten |
| 3 | 3-5 Seiten, mittlere Objekte | 8 | 11 | 6 Seiten |
| 4 | Korrespondenzen-Block | 8 | 5 | 3 Seiten |
| **Gesamt** | | **24** | **42** | **18 Seiten** |

### Neue Erkenntnisse

**Truncation-Problem entdeckt**: 4 grosse Objekte (o_szd.149, o_szd.141, o_szd.175, o_szd.174) haben nur ~5 von 43-165 Bildern transkribiert. Chunking bricht nach erstem Chunk ab. Muss in `transcribe.py` geprueft werden.

**Fraktur-Fehler haeufiger als angenommen**: o_szd.2217 (Walt Whitman) hatte 11 Fehler auf einer Seite — Nonsens-Halluzinationen ("Mitgebrine" statt "Mitbringsel"), falsche Eigennamen ("Hayel" statt "Hayek"), halluzinierte Werktitel ("Demokratie Lista" statt "Democratic Vistas").

**Fremdsprachliche Typoskripte**: Italienische Vertraege (o_szd.91) haben systematische Vokal-Fehler bei Kohlekopien (titole/titolo, tiretura/tiratura).

**Genauigkeits-Spread nach Gruppe** (Session 20):
- Typoskript/Formular/Kurztext: 97-100% (zuverlaessig)
- Korrekturfahne: 98-99% (zuverlaessig)
- Korrespondenz: 85-99% (abhaengig von Handschrift-Qualitaet)
- Zeitungsausschnitt: 97% (Fraktur-Fehler, aber meist einzelne Woerter)
- Handschrift: 95-98% (Kurrent-Verwechslungen)
- Tabellarisch: 75-99% (unvollstaendige Seiten bei grossen Objekten)

### Phase A: Truncation-Fix + DWR-Analyse + Fraktur-Evaluation

**Truncation-Bug gefixt**: Root Cause war `run_sample_batch.py --max-images 5` Default, nicht das Chunking. `diagnose_truncation.py` fand 97 betroffene Objekte (24 `max5_truncated`, 18 `vlm_mismatch`, 55 `zero_pages`). Default auf 0 geaendert. `transcribe.py` speichert jetzt `metadata.input_image_count_total`. Re-Transkription laeuft — 15/24 `max5_truncated` fertig, Chunking funktioniert korrekt bis 238 Bilder.

**DWR-Signal entfernt**: Spearman rho=0.05, F1=0.20 — keine Korrelation mit Qualitaet. `low_dwr` aus `needs_review` entfernt. Wirkung: 37% → 27% needs_review.

**Fraktur-Post-Processing evaluiert**: Prototyp `fraktur_postprocess.py` mit pyspellchecker + 13 Verwechslungspaaren. Ergebnis: 38% Precision — taugt als Flagging-Tool, nicht fuer Auto-Korrektur. Hauptlimitierung: Einzelzeichen-Substitution zu eng, Komposita nicht im Woerterbuch.

**Edit-History komplettiert**: 12 Dateien aus Session 18-19 retroaktiv gepatcht (20 Seiten). Verbessertes `backfill_edit_history.py` durchsucht jetzt Git-History nach Pre-Edit-Commits.

### Statistiken

| Metrik | Wert |
|---|---|
| Agent-verifizierte Objekte (Session 20) | 24 |
| Korrekturen (Session 20) | 42 Fehler auf 18 Seiten |
| Kumulativ agent-verified | 44 (20 + 24) |
| Kumulativ reviewed gesamt | 58 (14 human + 44 agent) |
| Truncation: betroffene Objekte | 97 (68 primaere Modell-Dateien) |
| Truncation: re-transkribiert | 15/24 max5, Rest laeuft |
| Edit-Tracking: backfilled total | 16 Dateien / 25 Seiten |
| needs_review nach Kalibrierung | 27% (355/1319), vorher 37% |
| Neue Scripts | diagnose_truncation.py, backfill_quality_signals.py, fraktur_postprocess.py |

---

## 2026-04-03 — Session 24: Layout-Pipeline Refactoring + Stratifizierter Test

### Was wurde gemacht

**1. Robustness-Refactoring (Phase 1, 8 Fixes)**
- Per-Page Error Handling (try-except statt Batch-Crash)
- PIL-Fallback bei fehlenden JPEG-Dimensionen
- VLM-Fallback-Logging (statt stiller Degradation)
- Halluzinations-Filter (Full-Page-Bbox >95% ablehnen)
- Schwellenwerte nach `config.py` verschoben
- Region-ID-Normalisierung (`r1, r2, ...` statt `d1, s1, r1`)
- Shared `find_ocr_file()` in `transcribe.py` (ersetzt fragile Glob-Logik in 2 Dateien)
- Schema `layout-regions-v0.1.json`: `source` + `group` Felder ergaenzt

**2. Post-Processing-Filter (Phase 2a)**
- 3 deterministische Filter in `_postprocess_regions()`: Scan-Hintergrund, Ueberlappung, Spurious
- 12 Regionen in Welle 2 korrekt entfernt (v.a. Seitenzahlen bei Korrekturfahnen)

**3. Prompt-Verfeinerung (Phase 2b)**
- 3 neue Regeln in `layout_ensemble.md`: Keine Ueberlappung, minimale Regionsgroesse, Scan-Hintergrund != Marginalie
- Wirksam: o_szd.1081 False-Positive-Region durch Prompt allein verhindert

**4. Merge+Verify kombiniert (Phase 4)**
- 1 VLM-Call statt 2 pro Seite (Regions + Quality im selben Output)
- Einsparung: ~7s/Seite = ~36h bei 18.700 Seiten
- `prompts/layout_verify.md` nicht mehr aktiv, bleibt als Referenz

**5. Stratifizierter Test (Welle 1 + 2)**
- Welle 1: 8 einfache Objekte ueber alle 9 Gruppen (21 Content-Seiten)
- Welle 2: 7 mittelschwere Objekte + 2 Re-Analysen
- Visuelle Inspektion Welle 1: 12 Seiten manuell geprueft
- Welle 2 bereit zur visuellen Verifikation

### Identifizierte Probleme (aus visueller Inspektion)

| Problem | Loesung | Status |
|---|---|---|
| Scan-Hintergrund-False-Positives | Post-Processing-Filter 1 + Prompt-Regel | Geloest |
| Ueberlappende Regionen | Post-Processing-Filter 2 + Prompt-Regel | Geloest |
| Spurious Zwischen-Regionen | Post-Processing-Filter 3 + Prompt-Regel | Geloest |
| Sachfotos statt Dokumente (o_szd.148) | `page.type=photograph` geplant | Offen |
| VLM-Nichtdeterminismus (o_szd.206) | Bekannte VLM-Eigenschaft | Akzeptiert |

---

## 2026-06-09 — Session 25: AAL-Lieferung, GAMS-Ingest-Vorbereitung, HTR-Provenienz + lokale Faksimiles

**Schwerpunkt:** Neue AAL-Digitalisat-Lieferung (Briefe an/von Stefan und Lotte Zweig, Signaturen SZ-AAL/B…) validiert, ingest-ready fuer GAMS/Cirilo aufbereitet und im HTR-Tool als Platzhalter-Objekte mit Ingest-Label und lokaler Faksimile-Anzeige integriert.

### Validierung der Quell-ZIPs
- Vier Export-Batches B1-B4 (B1-B3 = Signaturgruppen, B4 = Sammel-Batch B4-B21), gemischte Signaturen. CRC aller ZIPs ok, keine 0-Byte-Seitenscans, keine Signatur-Duplikate ueber Batches.
- **Befund B3 unvollstaendig:** viele Objekte ohne Bilddateien (XML referenziert Seiten, JPGs fehlen), einige Bildordner ohne XML. Re-Download ist eine identische Kopie -> Luecke ist quellseitig, Neuexport noetig.
- Lightroom-Kataloge (`.lrcat`, `.lrdata`, `previews.db`) versehentlich in einzelnen Objektordnern mitexportiert (B1.61/62/95/117, B3.108/109, B4/B21).

### Ingest-ready Aufbereitung (GAMS/Cirilo)
- `PROJECTS/szd/ingeste`: ein Ordner je vollstaendiges Objekt = Result-XML + genau die referenzierten Scans, Lightroom-Muell und Fremddateien weggelassen, verifiziert sauber. Cirilo bestaetigte den Import ("creates N objects from source").
- `PROJECTS/szd/B3_unvollstaendig`: separate Ablage der nicht ingest-fertigen B3-Objekte + `_FEHLENDE_BILDER.csv` als Neuexport-Einkaufsliste. Vault-Doku: `Projects/szd/GAMS-Ingest mit Cirilo (SZD).md`.

### HTR-Tool-Integration (neue Features)
- `transcribe.py`: `signature` + `provenance`-Block fliessen ins Ergebnis-`metadata`.
- `serve.py`: Route `/local-image/<collection>/<object_id>/IMG_n.jpg` liefert Faksimiles lokal aus `BACKUP_ROOT` (Traversal-geschuetzt) — fuer noch nicht ingestierte Platzhalter ohne GAMS-PID; graceful Fallback (onerror) auf anderen Rechnern, echte GAMS-Objekte unveraendert.
- `build_viewer_data.py`: erkennt Platzhalter (`provenance.in_gams=false`) -> lokale Bild-URLs + `ingestLabel`/`pidStatus` im Katalog.
- `app.js`: Ingest-Label-Badge in der Katalog-Titelzelle.
- Pilot: B1.1-B1.5 als `o_szd.99001-99005` (Label `SZ-AAL-2026-06`) transkribiert (3x high, 2x medium), lokal im Viewer inkl. Faksimile sichtbar.

### Qualitaetsbefund (Vision, B1.4)
Bestaetigt das bekannte Muster aus Session 19/20: bei schwerer violetter Kurrentschrift produziert das Modell fluessiges, plausibles Deutsch, markiert aber kaum Unsicherheit (`marker_density` weiterhin praktisch wertlos). Geplant: kontrolliertes A/B/C-Experiment (Unsicherheits-Kalibrierung / Metadaten-Kontext / staerkeres Modell) auf einem erweiterten B1-Test-Set mit Vision-Evaluation, um den besten Hebel zu identifizieren.

### Offen
- Echte GAMS-PIDs nach dem Ingest erfassen, HTR-Platzhalter darauf umstellen (`in_gams=true`, Faksimile dann aus GAMS statt lokal).
- B3 quellseitig neu exportieren (Liste: `_FEHLENDE_BILDER.csv`).
- A/B/C-Transkriptions-Experiment durchfuehren und auswerten -> erledigt, siehe Session 25b.

### Entscheidungen

- **Merge+Verify zusammenlegen**: Laengerer Prompt hat Qualitaet nicht verschlechtert (getestet auf o_szd.148)
- **Post-Processing-Filter**: Deterministisch + guenstig, fangen systematische VLM-Schwaechen ab
- **Prompt-Verfeinerung wirkt upstream**: Reduziert Probleme bevor Filter noetig sind

### Statistiken

| Metrik | Wert |
|---|---|
| Layout-Ergebnisse gesamt | 25 Objekte |
| Gruppen abgedeckt | 9/9 (A-I) |
| Quality good | 18 (72%) |
| Quality acceptable | 3 (12%) |
| Quality needs_correction | 3 (12%) |
| Filter-Aktionen Welle 2 | 12 Regionen entfernt |
| Geaenderte Dateien | layout_analysis.py, config.py, transcribe.py, export_pagexml.py, layout_ensemble.md, layout-regions-v0.1.json |

### Naechste Schritte

- [ ] Welle 2 visuell verifizieren (9 URLs bereit)
- [ ] Phase 2c: Sachfoto-Erkennung (page.type=photograph)
- [ ] Layout-Batch ueber ~1300 transkribierte Objekte (nach visueller Verifikation)

---

## 2026-06-09 — Session 25b: A/B/C-Transkriptions-Experiment (Vision-Auswertung)

**Frage:** Welcher Hebel verbessert die Transkription schwerer Kurrentschrift am meisten? Drei
Verbesserungen parallel gegen die aktuelle Pipeline (Kontrolle) getestet, danach Vision-Evaluation
gegen die echten Faksimiles (LLM-Halluzinationsrisiko bewusst — nur am Bild entscheidbare Stellen
als belegt gewertet).

### Aufbau
- Test-Set B1.1/1.2/1.4/1.6/1.7/1.8 (6 Objekte, 20 Seiten; Misch aus Postkarte, schwerer Handschrift, Typoskript).
- Vier Bedingungen, je `c:\tmp\htr_experiment\<shelf>__<cond>.json`:
  - **control** — aktuelles Modell (`gemini-3.1-flash-lite-preview`), aktueller Prompt, Kontext minimal.
  - **V1_uncert** — flash-lite + Unsicherheits-Kalibrierungs-Prompt + Feld `uncertain_words`.
  - **V2_context** — flash-lite + reichhaltiger Metadaten-Kontext (Verfasser/Adressat/Ort/Datierung) im Prompt.
  - **V3_model** — staerkeres Modell (`gemini-3-flash-preview`), sonst wie control.

### Quantitatives Aggregat (Summe Test-Set, 20 Seiten)
| Bedingung | chars | `[?]` | `uncertain_words` |
|---|---|---|---|
| control | 10014 | 3 | 0 |
| V1_uncert | 9708 | 6 | 24 |
| V2_context | 10372 | 1 | 0 |
| V3_model | 9203 | 2 | 0 |

Zeichenmenge ist kein Qualitaetsmass (control blaeht durch Mit-Transkription der Farbtafel-Seite auf).

### Vision-Befunde (am Faksimile belegt)
- **B1.6 (Postkarte):** Bild-Poststempel = „BATH / SOMERSET / 1939". V3 liest „BATH SOMERSET" korrekt;
  control/V1 lesen faelschlich „HAMPSTEAD". Im Fliesstext zeigt das Bild „im Haus" — V3 korrekt,
  **V2 halluziniert „Hier in Bath musiciert"** (der Metadaten-Prior „Entstehungsort: Bath" sickert in
  den Text). V3 korrigiert ausserdem das sinnlose „verbauten Gesichter" -> „vertrauten Gesichter".
- **B1.4 (schwere Handschrift):** V3 korrigiert mehrere stille Fehler der Kontrolle:
  „Glaskasten" (statt „Glashütten"), „Garage" (statt „Sarge", passt zu „box room"), „Sie und Ihren
  Mann bitten" (statt verstuemmeltem „hi mit Ihren Namen"), Schlussformel „Ihr (oder wenn Sie
  zustimmen) Dein Stefan Zweig" (statt halluziniertem „Ihr Lotte … Sei"); erfasst Streichung/Einfuegung
  und die rote Randnotiz. **V1s `uncertain_words` zeigen verlaesslich genau auf die Fehlerstellen**
  (Glashütten, Sarge, gefällt, Lotte) — repariert sie nicht, flaggt sie aber ehrlich.
- **B1.8 (Typoskript):** alle Bedingungen ~99 % korrekt; nicht diskriminierend. control ueber-
  transkribiert die Farbtafel-Seite 3 (Duplikat-Artefakt), V3 laesst sie korrekt leer und faengt den
  vertikalen Briefkopf „TELEPHONE: BATH 4983." mit.

### Verdikt + Entscheidung
- **V3 (staerkeres Modell) = klarer Genauigkeits-Gewinner** bei Handschrift; korrigiert stille Fehler, die
  control selbstsicher emittiert.
- **V1 (Unsicherheit) = bestes Review-Signal**: `uncertain_words` treffen die realen Fehlerstellen —
  wertvoll fuer den GT-Review.
- **V2 (Metadaten-Kontext) = netto negativ/gefaehrlich**: belegte Prior-Leckage in den Fliesstext;
  unterdrueckt zudem Unsicherheitsmarker. Nicht uebernehmen (allenfalls mit explizitem „Metadaten sind
  Hintergrund, nicht in den Text uebernehmen").
- **Empfehlung fuer Produktivlauf:** `gemini-3-flash` als Basismodell **+** Unsicherheits-Kalibrierung
  mit `uncertain_words`; V2 verwerfen. Kostenabwaegung: flash teurer als flash-lite — bei der durchweg
  handschriftlichen AAL-Korrespondenz gerechtfertigt; reines Typoskript koennte bei flash-lite bleiben.
- **Methodik-Vorbehalt:** belegt sind nur am Bild eindeutig entscheidbare Stellen (Garage/Sarge,
  Glaskasten, im Haus, Bath-Stempel); feine Palaeografie auf Wortebene bleibt Fachperson. Richtung ist
  ueber B1.6 und B1.4 konsistent.

---

## 2026-04-02 — Session 20b: Korrespondenzen-Massenbatch

### Was wurde gemacht

**1. Korrespondenzen-Batch: 566 neue Objekte transkribiert**

Ausgangslage: 450/1186 Korrespondenzen transkribiert (38%).
Ergebnis: 1016/1186 (86%), 170 verbleibend. 0 Fehler im gesamten Batch.

Grosse Objekte erfolgreich via Chunking verarbeitet:
- o_szd.174: 122 Bilder (7 Chunks) — high confidence
- o_szd.75: 151 Bilder (8 Chunks) — high confidence
- o_szd.71: 54 Bilder (3 Chunks) — high confidence
- o_szd.76: 60 Bilder (3 Chunks) — medium confidence

**2. Bug-Fix: `run_batch()` Fehlerbehandlung**

Problem: `run_batch()` in `transcribe.py` hatte keinen try/except um `transcribe_object()`. Ein einzelner unbehandelter Fehler (z.B. beim API-Call eines grossen Objekts) toetete den gesamten Batch-Prozess lautlos — keine Fehlermeldung, kein Traceback.

Fix: try/except mit Logging um den `transcribe_object()`-Aufruf. Batch laeuft jetzt weiter, auch wenn einzelne Objekte fehlschlagen.

**3. Analyse: Dry-Run-Zaehlung vs. Result-Zaehlung**

Klaerung einer scheinbaren Diskrepanz (127 Backup-Objekte vs. 138 Results bei Lebensdokumenten): Die 138 entstand durch Mitzaehlung von Consensus-, Pro- und Layout-JSONs. Tatsaechlich: 127 Flash-Lite-Results = 127 Backup-Objekte (perfekt). `--dry-run` listet ALLE Objekte ohne Skip-Logik.

### Erkenntnisse

- **Chunking ist produktionsreif**: Objekte bis 151 Bilder (8 Chunks) laufen stabil durch
- **Korrespondenzen-Qualitaet**: Ueberwiegend high confidence, vereinzelt medium/low bei schwieriger Handschrift
- **JSON-Parsing-Retries**: Einige Objekte brauchen Retry wegen nicht-parseabrem Gemini-Output (z.B. o_szd.482, o_szd.564) — werden automatisch behandelt
- **Batch-Robustheit**: Mit dem try/except-Fix ist die Pipeline jetzt resilient gegen Einzelfehler

---

## 2026-04-03 — Session 21: Scope-Bereinigung, GT-Review-Workflow, Signal-Evaluation

### Scope-Bereinigung

**Entfernt aus dem Projekt:**
- Prompt-Ablation, Nondeterminismus-Test, Provider-Vergleich (nicht noetig fuer Projektziel)
- Phase 5 (TEI/teiCrafter) — TEI-Erzeugung passiert im teiCrafter-Repo, nicht hier
- `knowledge/tei-target-structure.md` und `knowledge/teiCrafter-integration.md` geloescht
- Phase 6 (DIA-XAI) → Phase 5

Beruehrte Dateien: Plan.md, CLAUDE.md, README.md, knowledge/index.md, dia-xai-integration.md, htr-interchange-format.md, layout-analysis.md, journal.md, evaluation-results.md, verification-concept.md.

### GT-Review-Workflow

**Problem:** Kein einziges Objekt hatte `gt_verified`-Status. Die CER-Zahlen in evaluation-results.md basierten auf Agent-Schaetzungen, nicht auf echtem Ground Truth. Nicht publikationsfaehig.

**Loesung:** End-to-End GT-Review-Workflow implementiert:
- `serve.py`: `gt_verified` als neuer Status (Tier 0), `ThreadingHTTPServer` (POST-Requests hingen bei Single-Threaded-Server), `find_result_file` bevorzugt primaeres Modell
- `app.js`: GT Verify Button, "Gespeichert (JSON)" statt localStorage-Anzeige
- `index.html`: GT Verify Button, Hilfe-Seite mit 4-Tier Review-Modell erklaert, verbesserte Tooltips
- `/api/edit` speichert Originaltext in `edit_history` — Grundlage fuer CER-Berechnung (Pipeline-Original vs. Human-Korrektur)

**Ergebnis:** o_szd.139 als erstes Objekt im Viewer editiert und verifiziert. edit_history bestaetigt. 14 weitere GT-Objekte definiert (15 Objekte, ~39 Content-Seiten, alle 9 Gruppen).

### Quality-Signals v1.6: Empirische Evaluation

**Methode:** 62 agent-verified Objekte mit `errors_found`-Daten als Referenz. Precision pro Signal berechnet.

| Signal | N geflaggt | Precision | Entscheidung |
|---|---|---|---|
| `page_image_mismatch` | 3 | **100%** | Behalten — bestes Signal |
| `page_length_anomaly` | 2 | **100%** | Behalten — kleine Stichprobe |
| `language_mismatch` | 8 | **50%** | Behalten — Metadaten-Signal |
| `duplicate_pages` | 1 | **0%** | Aus needs_review entfernt |
| DWR | 0 | — | Seit v1.5 entfernt |
| Marker-Density | 0 | — | Seit v1.5 entfernt |

**Aenderungen:**
- `duplicate_pages` aus `needs_review_reasons` entfernt (0% Precision, misst Dokumentstruktur statt Fehler)
- DWR, Marker-Density, Seitenduplikate aus Dashboard-Signalanalyse entfernt
- Backfill: 125 Objekte entflaggt
- `needs_review`-Quote: 25% → **19.4%**

**Begruendung `duplicate_pages`:** Korrekturfahnen enthalten physisch 2x denselben Text (Original + Korrekturversion, z.B. o_szd.1888: p0≡p7). Register haben repetitive Headers. Beides ist Dokumentstruktur, kein Transkriptionsfehler.

### Truncation Re-Transkription

5 Objekte mit extremer Truncation identifiziert (result_pages < 10% der Backup-Bilder):
- o_szd.66 (2/141), o_szd.68 (3/202), o_szd.221 (1/51), o_szd.2271 (1/25), o_szd.2234 (2/13)

Re-Transkription mit `--force --chunk-size 20` gestartet.

### Statistiken

| Metrik | Vorher | Nachher |
|---|---|---|
| needs_review-Quote | ~25% | 19.4% |
| Signale im Dashboard | 6 Spalten | 3 Spalten |
| gt_verified Objekte | 0 | 0 (Workflow bereit, 15 Objekte definiert) |
| approved (human) | 15 | 16 (+o_szd.139 mit edit_history) |
| Pipeline-Phasen | 6 (inkl. TEI) | 5 (ohne TEI) |

### Kontext

Zwei parallele Arbeitsstraenge in dieser Phase: Transkription neuer Objekte (dieser Eintrag) und Verifikation bestehender (Session 20 oben).

### Statistiken

| Metrik | Wert |
|---|---|
| Neue Transkriptionen | 566 |
| Korrespondenzen-Abdeckung | 1016/1186 (86%) |
| Fehler | 0 |
| Groesste Objekte (Bilder) | 151, 122, 60, 54 |
| Gesamtabdeckung (alle Sammlungen) | ~1308/2107 (62%) |

---

## 2026-04-03 — Session 22: UI-Redesign (Badge-System, Header, CSS/HTML-Refactoring)

**Schwerpunkt:** Komplettes Redesign des Badge-Systems im Katalog-Viewer, Projekttitel im Header, CSS/HTML-Qualitaetsrefactoring, Accessibility-Verbesserungen.

### Badge-System: 5-Stufen-Redesign

**Problem:** Badges waren visuell inkonsistent (manche Pills, manche Text+Punkt), Labels unklar fuer Expert:innen ("LLM OK", "Agent ✓"), Farben widersprachen der Semantik (gelber Punkt fuer OK-Zustand).

**Neues System — einheitliche Pills mit Vertrauens-Farbverlauf:**

| Tier | Alt | Neu | Farbe |
|---|---|---|---|
| 0 | GT ✓ | Verifiziert | Dunkelgruen (#1a5c1a / #c8e6c8) |
| 1 | Geprueft | Geprueft | Gruen (#2d6a2d / #d4e8d4) |
| 2 | Agent ✓ | Auto-geprueft | Schiefergrau (#475569 / #e2e8f0) |
| 3a | LLM OK | Ungeprueft | Grau (#4b5563 / #e5e7eb) |
| 3b | Review | Review noetig | Amber (#b45309 / #fef3c7) |

Alle 5 Stufen bestehen WCAG AA (≥4.5:1 Kontrast). Farben nach Kontrastpruefung nachgeschaerft: "Review noetig" von #d97706 auf #b45309, "Ungeprueft" von #6b7280 auf #4b5563.

VLM-Konfidenz ("high/medium/low") aus Qualitaets-Spalte entfernt (laut eigener Evaluation unzuverlaessig). LLM-Sparkle-Icon (✦) entfernt — Labels sind selbsterklaerend.

Betrifft: `renderReviewCell()`, `renderQualityCell()`, `renderViewerContext()`, `renderStats()`, `renderReviewDonut()`, Filter-Dropdown (5 statt 3 Optionen), Help-Tabelle (5-Tier), Summary-Bar-Chips.

### Header-Redesign

- **Titel:** "SZD-HTR" → "SZD OCR/HTR Pipeline"
- **Subtitle:** "Experimentelles Teilprojekt von Stefan Zweig Digital" (italic, dezent)
- **Claude-Badge:** Vereinfacht auf "Built with Claude Code" (ohne Modell/Methode)
- **Meta-Tags:** `<title>`, OG-Tags, Description aktualisiert

### CSS/HTML-Refactoring

**Accessibility:**
- `:focus-visible` auf alle interaktiven Buttons (Katalog-Pagination, Viewer-Navigation, Action-Buttons, GT-Approve)
- `aria-label` auf 9 Icon-only-Buttons (Pfeile, Zoom, Rotate, Reset, Fit)
- Disabled-Buttons: `opacity` ersetzt durch echte Farben (WCAG AA konform)

**Inline-Styles eliminiert:**
- `.is-hidden` CSS-Klasse ersetzt 12× `style="display:none"` im HTML
- 27× `style.display` im JS → `classList.add/remove/toggle('is-hidden')`
- 5× JS-generierte Inline-Styles → CSS-Klassen (`.placeholder-message`, `.gt-review-panel__stats`, `.gt-review-panel__hint`, `.diff__provider-label--old/--new`)

**Farb-Fallbacks bereinigt:**
- 12× `var(--sz-*, #fallback)` Fallbacks in GT-Review-CSS entfernt
- Hardcodierte Farben (#888, #1a1a1a) → CSS-Variablen
- `'JetBrains Mono', monospace` → `var(--font-mono)`

**Weitere Fixes:**
- `::selection`-Style (Burgundy/Cream)
- Knowledge-Sidebar auf 600px versteckt
- Help-Links: Underline-Style konsistent mit Markdown-Content
- Umlaut-Fix: "Qualitaetsmetriken" → "Qualitaetsmetriken" (HTML-Entity)
- Diff-Beschreibung: Generisch statt hardcoded Modellnamen
- `.catalog__stats` CSS `display:none` → `.is-hidden` Klasse

### Neue/Geaenderte Dateien

- `docs/app.css` — 10 neue CSS-Variablen (Review-Tiers), Badge-Klassen, Focus-Styles, `.is-hidden`, Farb-Bereinigung
- `docs/app.js` — Badge-Rendering, classList statt style.display, Filter-Logik, Donut-Labels
- `docs/index.html` — Header, Meta-Tags, Dropdown, Help-Tabelle, aria-labels, is-hidden

### Entscheidungen

| Entscheidung | Begruendung |
|---|---|
| "Ungeprueft" statt "LLM OK" | Ehrlicher — sagt was es ist (nicht geprueft), nicht was die Maschine meint |
| VLM-Konfidenz entfernt | Eigene Evaluation zeigt: unzuverlaessig (LLMs ueberschaetzen Leistung) |
| Icons entfernt (✦, ⚙, ✓) | Labels sind selbsterklaerend, Icons waren visuell unausbalanciert |
| WCAG-Kontrastpruefung | Amber-Text und Grau-Text nachgeschaerft nach Berechnung der Kontrastverhaeltnisse |
| `!important` bei `.is-hidden` | Utility-Class muss alle anderen display-Regeln ueberschreiben |
| `!important` bei reduced-motion | Anerkanntes A11y-Pattern, stellt sicher dass keine Animation die Einstellung ueberschreibt |

---

## 2026-04-03 — Session 23: Datenbestand-Inventur, Batch 100%, Page-JSON v0.2, METS als Zielformat

**Schwerpunkt:** Rohdaten-Inventur, Batch-Transkription Richtung 100%, Stats-Dashboard als epistemische Infrastruktur, Page-JSON v0.2 mit deskriptiven Metadaten, METS/MODS + PAGE XML als Zielformat.

### Datenbestand-Inventur

Erstmals exakt dokumentiert: 2.107 Objekte, 18.719 Faksimile-Scans, 23 GB. Pro Sammlung: Lebensdokumente 127/2.879, Werke 169/7.842, Aufsatzablage 625/3.844, Korrespondenzen 1.186/4.154. Bildformat: JPEG, Median 4800x7234 px. Alle Objekte vollstaendig (metadata.json + mets.xml + Bilder). In data-overview.md, README.md, CLAUDE.md dokumentiert.

### Batch-Transkription

- Korrespondenzen auf 100% (43 fehlende einzeln transkribiert)
- Aufsatzablage ~97% (318 neue, 19 Fehler)
- Werke-Batch laeuft (85/115, viele Timeouts bei Objekten >50 Bilder)
- Problem: 5-Min-Timeout im Batch-Skript reicht nicht fuer Chunking-Objekte

### Seiten-Bild-Synchronisation

Bug entdeckt: VLM nummeriert nach Manuskriptblaettern (1,3,5,...), ueberspringt Rueckseiten. Viewer zeigt falsches Bild ab Seite 2. Fix: `_fill_missing_pages()` in quality_signals.py — fuellt Luecken mit Blank-Eintraegen. 41 Objekte backfilled. Zwei Faelle abgedeckt: Luecken in Seitennummern und weniger Seiten als Bilder.

### Stats-Dashboard: Epistemische Infrastruktur

5 Sektionen entfernt (nicht gegroundet oder transient): Fortschritt/Abdeckung, Seitenkomposition, DWR-Histogram (rho=0.05), VLM-Konfidenz-Donut (diskriminiert nicht), Modellkonsensus (Agreement ≠ Korrektheit, nur 29/1973 Objekte).

3 neue Sektionen: Verifikation (Review-Status + Review-Gruende mit Signal-Precision), Textcharakteristik (Zeichen/Seite pro Dokumenttyp — Handschrift ~50 Z/S wegen 73% Registerblaetter, Zeitungsausschnitt ~4800), Signalanalyse (Heatmap).

Provenienz-Annotationen: Jede Sektion zeigt dezent (opacity 0.35, hover 0.7) welches Pipeline-Script die Daten erzeugt.

### Page-JSON v0.2: Deskriptive Metadaten

Neuer `descriptive_metadata`-Block in `source`: Dublin Core (creator+GND, subject, origin_place, extent, rights, provenance) + materialtypologische Erweiterungen (writing_instrument, writing_material, hands[], dimensions, binding, inscriptions, correspondence). Schema: `schemas/page-json-v0.2.json`. Export: `pipeline/export_page_json.py`. TEI-Extraktion: `_extract_full_metadata()` in tei_context.py mit persName-Parsing und Whitespace-Normalisierung.

### METS/MODS als Zielformat

Architektur-Entscheidung: Page-JSON = internes Arbeitsformat, METS/MODS + PAGE XML = Archiv- und Austauschformat (Zielformat). Gruende: GAMS arbeitet mit METS, Transkribus/eScriptorium/OCR-D verstehen es, MODS ist reicher als DC fuer Archivmetadaten, kein eigenes Schema zu pflegen. Wissensdokument: `knowledge/page-xml-mets-architecture.md`. Terminologie durchgaengig in CLAUDE.md, README, Plan.md, Knowledge Vault nachgezogen.

### Knowledge Vault Audit

8 Fixes: stale Zahlen in dia-xai-integration.md (1328→1973), Session-Zaehler in index.md, DWR-Referenzen in stats-dashboard.md, Schema-Referenz v0.1→v0.2, updated-Daten.

### Entscheidungen

| Entscheidung | Begruendung |
|---|---|
| DWR aus Dashboard entfernt | rho=0.05, F1=0.20 — mass Prosadichte, nicht Qualitaet |
| VLM-Konfidenz aus Dashboard entfernt | High/Medium/Low diskriminiert nicht |
| Modellkonsensus aus Dashboard entfernt | CER zwischen Modellen = Agreement, nicht Korrektheit |
| Provenienz-Annotationen | Jede Visualisierung zeigt Datenherkunft — epistemische Transparenz |
| Page-JSON v0.2 mit descriptive_metadata | DC + Materialtypologie — alle TEI-Felder ins Arbeitsformat |
| METS/MODS als Zielformat | Etablierter Stack, GAMS-kompatibel, kein eigenes Schema noetig |
| _fill_missing_pages | Seiten-Bild-Sync als Pipeline-Schritt, nicht Viewer-Workaround |

### Neue/Geaenderte Dateien

- `pipeline/quality_signals.py` — `_fill_missing_pages()` (v1.5 Fix)
- `pipeline/tei_context.py` — `_extract_full_metadata()`, `parse_tei_full_metadata()`, persName-Parser, Whitespace-Fix
- `pipeline/export_page_json.py` — Vollstaendige Implementierung (~210 Zeilen)
- `schemas/page-json-v0.2.json` — Neues Schema mit descriptive_metadata
- `knowledge/page-xml-mets-architecture.md` — Neues Wissensdokument
- `knowledge/data-overview.md` — Physischer Bestand, TEI vs. Backup, Sprachen
- `docs/app.js` — Dashboard-Umbau (5 Sektionen entfernt, 3 neu)
- `docs/app.css` — Provenienz-Styling

## 2026-04-03 — Session 24: teiCrafter Pipeline Mode + Page-JSON Batch-Export

**Schwerpunkt:** Analyse szd-htr ↔ teiCrafter-Verbindung, Implementierung Pipeline-Modus in teiCrafter, Page-JSON-Batch-Export fuer alle 2030 Objekte, Batch-TEI-Generierung.

### Analyse der Projektverbindung

szd-htr und teiCrafter bilden eine sequentielle Pipeline: szd-htr (Bild → Text + Layout + Metadaten) → teiCrafter (Text → TEI-XML). Design-Entscheidung: TEI-Erzeugung passiert in teiCrafter, nicht in szd-htr. teiCrafter hat bereits 3 SZD-spezifische Mapping-Templates (correspondence-szd, manuscript-szd, print-szd).

### teiCrafter Pipeline-Modus (Phase P)

Neuer Modus neben dem bestehenden interaktiven Browser-Modus. Node.js-CLI (`pipeline.mjs`), 6 reine ES6-Module unter `docs/js/pipeline/`. Deterministisch wo moeglich, LLM (Gemini 3.1 Flash Lite) nur fuer div-Grenzen bei komplexen Dokumenten (noch nicht implementiert).

Module:
- `utils.js` — XML-Escaping, Element-Builder, Sprachcodes
- `mods-to-header.js` — Page-JSON Metadaten → teiHeader (100% deterministisch)
- `page-to-body.js` — Seiten + Regionen → TEI-Elementliste (Regionstyp-Mapping)
- `div-structurer.js` — Heading-Heuristik, Briefe als Single-div
- `tei-assembler.js` — Orchestriert alles
- `pipeline-validator.js` — Tag-Matching + Struktur-Check + Plaintext-Erhaltung

DTABf-Schema um 30+ Elemente erweitert (msDesc-Hierarchie, fw, table, list, Header-Elemente). Plan.md mit 9 Teilphasen erstellt.

### Page-JSON Batch-Export (szd-htr)

`python pipeline/export_page_json.py --all` — 2.030 Page-JSON-Dateien exportiert (vorher: 3). Aufgeteilt: Lebensdokumente 127, Korrespondenzen 1.186, Aufsatzablage 606, Werke 111.

### Batch-TEI-Generierung (teiCrafter)

`node pipeline.mjs --batch` ueber alle 4 Sammlungen: **2.030 TEI-Dateien, 0 Fehler**. Plaintext-Erhaltung 99-100%. Output: 21 MB in `teiCrafter/output/`. Fix fuer leere Dokumente (5 Objekte ohne Seiten → leerer div).

### Entscheidungen

| Entscheidung | Begruendung |
|---|---|
| Page-JSON-Fallback statt METS | METS-Export (`export_mets.py`) existiert noch nicht; Page-JSON v0.2 enthaelt alle benoetigten Daten |
| Kein LLM fuer teiHeader | MODS-zu-TEI ist deterministische Abbildung |
| Kein LLM fuer body-Grundstruktur | Regionstypen aus Layout-Analyse genuegen |
| Briefe als Single-div | Umschlag-Adressen und Briefkoepfe sind keine Kapitelgrenzen |
| Node.js CLI statt Browser-Pipeline | Batch-Verarbeitung braucht Dateisystem-Zugriff |

### Validierung und Tests

- XML-Well-Formedness (Python `xml.etree.ElementTree`): **2.033/2.033** Dateien fehlerfrei geparst
- Zeichengenauer Plaintext-Vergleich (Page-JSON vs. TEI body): **2.030/2.030 identisch** (0 fehlende, 0 hinzugefuegte Zeichen)
- Stichproben-Metadaten-Pruefung (20 zufaellige Objekte): Titel, PID, Sprache, Seitenzahl, GND, Signatur — alle korrekt
- 50 Unit- und Integrationstests (`tests/pipeline.test.mjs`): **50/50** bestanden
- **Nicht gemacht:** RelaxNG-Validierung gegen offizielles TEI-Schema (kein `xmllint`/`lxml` auf dem System)

### Commits

| Repo | Hash | Inhalt |
|---|---|---|
| teiCrafter | `77fd4be` | Pipeline-Modus: 6 Module, CLI, 50 Tests, Schema, Knowledge, README, CLAUDE.md |
| szd-htr | `d99a31c` | Journal + Plan (Session 24) |
| szd-htr | `631931a` | 2.030 Page-JSON-Dateien (218.813 Zeilen) |

### Naechste Schritte

- Layout-Analyse skalieren (18 → ~2000 Objekte, benoetigt API-Calls)
- `export_mets.py` in szd-htr bauen (Phase 5b)
- teiCrafter METS-Parser (Phase P.1)
- LLM-Fallback fuer komplexe div-Grenzen (P.4.2/P.4.3)
- RelaxNG-Validierung gegen offizielles TEI-Schema nachholen

---

## Offene Fragen (Stand 2026-04-03)

- [ ] Optimale Bildgroesse: Resizing vor API-Call?
- [ ] Korrektur-Markup: Erweitertes Markup noetig?
- [ ] VLM-Seitenzuordnungsfehler: VLM schreibt Text auf falsche Seite bei Typoskripten mit Rueckseiten — Erkennung und Fix?
- [ ] export_mets.py: METS-Container mit MODS + PAGE XML implementieren
- [ ] Korrespondenzen-TEI-Matching: correspDesc aus Konvolut-Eintraegen den Einzelbriefen zuordnen
- [x] Fraktur-Erkennung: o_szd.2232 high confidence (Session 7)
- [x] Batch-Modus: transcribe.py (Session 5)
- [x] Konvolut: Gruppe G erstellt, o_szd.277 medium (Session 7)
- [~] Alle 2107 Objekte transkribieren — ~2080/2107 (99%) fertig (Session 25), 27 Werke-Objekte im Batch
- [x] quality_signals kalibrieren: v1.1 rekalibriert (Session 13), low_dwr entfernt (Session 20 Phase A)
- [x] o_szd.143 nur 20 Zeichen auf 3 Seiten — geloest: fehlende Bilder wegen API-Limit, Chunking eingebaut (Session 17)
- [x] Verification-by-Vision: Proof of Concept erfolgreich, Spec geschrieben (Session 11)
- [x] Pipeline-Bug: o_szd.147 repariert, 41 Bilder transkribiert (Session 13)
- [ ] VbV-Konfidenz gegen Ground Truth kalibrieren (nach Modellkonsensus-Validierung)
- [x] Modellkonsensus: 27 Objekte validiert, 18 Objekte GT-Pipeline mit 3 Modellen (Session 14)
- [x] Statistik-Dashboard im Frontend — Enhanced Stats + Diff mit echten Daten (Session 14)
- [~] Expert-Review: 58/~875 Objekte verifiziert (14 human + 44 agent), CER-Baseline steht (Session 18–20)
- [~] Agent-Verifikation auf weitere Objekte ausweiten — 44/~875 agent-verified (Session 18–20)
- [x] Fraktur-Post-Processing evaluiert: 38% Precision, taugt als Flagging, nicht Auto-Korrektur (Session 20 Phase A)
- [ ] `duplicate_pages` False-Positive fixen: Color-Chart-Seiten von Duplikat-Erkennung ausschliessen (Session 19)
- [x] Halluziniertes "An" auf Adressseiten: Prompt-Fix in group_i_korrespondenz.md (Session 25)
- [x] DWR-Score gegen Agent-Verifikation validiert: rho=0.05, F1=0.20, Signal entfernt (Session 20 Phase A)
- [~] **Truncation fixen**: Root Cause `max_images=5` gefixt, 97 Objekte betroffen, 15/24 re-transkribiert (Session 20 Phase A)
- [x] Edit-Tracking: `edit_history` in Pipeline-JSONs + Frontend-Diff implementiert (Session 20)
- [ ] `marker_density` evaluieren: Gemini setzt keine Marker, Signal vermutlich wertlos wie DWR
- [ ] `duplicate_pages` + `language_mismatch` Precision/Recall messen (naechste Kalibrierungsrunde)

---

## 2026-04-12 — Session 25: Batch-Transkription +20 Objekte (2075/2107), Ensemble-Layout-Pipeline

### Was wurde gemacht

**1. Transkriptionsluecken geschlossen**

Ausgangslage: 2075/2107 Objekte (98,5%). Fehlend: 5 Aufsatzablage, 27 Werke.

- Aufsatzablage: 1/5 erfolgreich (o_szd.2607), 4 persistente API-Fehler (INVALID_ARGUMENT / leere Antwort)
- Werke: Batch laeuft (27 Objekte, 53-341 Bilder). Stand: ~146/169 Werke-Dateien. Chunking funktioniert, aber o_szd.227 (184 Bilder, 73% Leerseiten) hatte massive JSON-Parse-Fehler (120/184 Platzhalter-Seiten)

**2. METS/MODS Export implementiert (Phase 5b)**

Neues Script `pipeline/export_mets.py` (~280 Zeilen). METS-Container mit:
- dmdSec: MODS-Metadaten aus TEI (parse_tei_full_metadata) + Backup-Fallback fuer Korrespondenzen
- fileSec: GAMS-Bild-URLs + PAGE XML Referenzen (falls vorhanden)
- structMap PHYSICAL: Seiten-Sequenz
- structMap LOGICAL: Textseiten vs. Farbreferenz/Schluss
- structLink: Seiten-Typ-basierte Zuordnung

Batch-Export: **2074 METS-Dateien, 0 Fehler**. Alle 4 Sammlungen. GND-Verknuepfungen, Sprach-Normalisierung, Signatur-Mapping funktionieren.

**3. Bug-Fix: "An"-Halluzination**

Prompt-Fix in `group_i_korrespondenz.md`: Explizite Anweisung, kein "An" vor Empfaengernamen zu ergaenzen.

**4. JSON-Parsing und Chunking gehaertet**

Problem: Werke-Objekte mit vielen Leerseiten (49% im Schnitt, bis 73%) produzieren kaputtes JSON. Ursache: Gemini rutscht bei Chunks mit vielen leeren Seiten aus dem JSON-Format.

3 Verbesserungen in `transcribe.py`:
- `_repair_json()`: Trailing Commas entfernen, nackte Steuerzeichen in Strings escapen
- `_extract_json_object()`: JSON-Objekt aus umgebendem Text extrahieren, abgeschnittenes JSON schliessen
- `_retry_sub_chunks()`: Fehlgeschlagene 20er-Chunks automatisch in 5er-Bloecke aufteilen und erneut versuchen
- Blank-Page-Hint im Chunk-Prompt bei Objekten >30 Bilder

**5. Viewer-Daten und Page-JSON aktualisiert**

- catalog.json: 2055 → 2076 Objekte
- 46 neue Page-JSON-Dateien exportiert

**6. Knowledge Vault Audit**

Systematischer Audit aller 12 Knowledge-Dokumente. 10 Probleme in 7 Dateien gefunden und behoben:
- stats-dashboard.md: v1.4→v1.5, DWR-Referenzen entfernt, Sektionsnummern korrigiert, Objektzahl aktualisiert
- dia-xai-integration.md: ~1973→~2080 Objekte
- htr-interchange-format.md: Schema v0.1→v0.2, DWR aus Signalliste entfernt
- page-xml-mets-architecture.md: export_mets.py als implementiert markiert
- verification-concept.md: Stichprobengroesse 26→62 verifizierte Objekte

### Statistiken

| Metrik | Wert |
|---|---|
| Transkription gesamt | ~2080/2107 (99%) |
| Neue Transkriptionen (Session) | ~20 (Werke-Batch laeuft noch) |
| METS-Export | 2074 Dateien, 0 Fehler |
| Page-JSON (neu) | 46 Dateien |
| Viewer-Objekte | 2076 |
| Knowledge-Fixes | 10 Probleme in 7 Dateien |
| Neue Scripts | export_mets.py |
| Geaenderte Scripts | transcribe.py (4 neue Funktionen), group_i_korrespondenz.md |


---

## 2026-04-15 — Session 26: Interface Documents-First Refactor + Paper-Claim-Traceability

### Kontext

Der Code4Lib-Abstract (Pollin/Zangerl/Hintersteiner) wurde am 15.04.2026 eingereicht und macht drei Arten von Claims �ber das Interface:

1. *Reading / Curation / Verification als drei Funktionen desselben Codes, mode-switched by deployment*
2. *Expert review deepens editorial commitment along a concentric-edition progression*
3. *Obsidian vault + JOURNAL.md als Audit-Trail, Git als Versionsverlauf*

Alle drei waren zwar im Code realisiert, aber nicht sichtbar nachvollziehbar. Diese Session hat zwei Iterationen durchlaufen: erst Sichtbarmachung (Durchgang 1: Mode-Banner, Curation Progress, README-Sektion), dann eine zu viele Panels im Katalog, dann Documents-First-Refactor.

### Was wurde gemacht

**1. Mode-Banner als Terminal-Sigil** (Commit 47a0a01, 1c89a85)

Schmales Band oberhalb des Site-Headers, nur im Local-Modus sichtbar: `szd@editorial:~/results $ EDITORIAL` im Terminal-Look (near-black Hintergrund, gold top-border, blinkender Cursor). Kontrastiert eindeutig mit dem Public-Read-Only-Deployment. Macht die "Three functions, mode-switched"-These sofort erkennbar.

**2. Editorial Progress Bar im Stats-Dashboard** (Commit 0c351d9)

Horizontale gestapelte Bar mit f�nf Segmenten in Tier-Reihenfolge (Ungepr�ft \u2192 Review n�tig \u2192 Auto-gepr�ft \u2192 Gepr�ft \u2192 Verifiziert), matcht die 4-Tier-Trust-Priorit�t. Visualisiert Vogelers konzentrische Ring-Bewegung quantitativ. Segmente sind mutex aggregiert \u2014 ein Objekt kann nur in einem Tier sein, keine Doppelz�hlung mehr (Bug: Chip zeigte 348, Bar zeigte 338; fix: 84a111c hat die Aggregationsschleife auf else-if umgestellt).

**3. Summary-Row entr�mpelt** (Commit 7d63735)

Review-Chips (verified/approved/agent/unreviewed/flagged) und Modellkonsensus-Chip aus der Summary entfernt \u2014 werden alle in der Editorial Progress Bar dargestellt, Duplikation war verwirrend. Summary enth�lt jetzt nur Total + Collection-Chips + Details-Toggle.

**4. Modellkonsensus-Tooltip** (Commit 84a111c)

Section-Label im Details-Panel bekommt erkl�renden Tooltip + Info-Symbol. Cross-Model-Konsens ist der am h�ufigsten missverstandene Begriff: zwei VLMs (Gemini Flash Lite + Flash) transkribieren unabh�ngig, die CER zwischen den Ergebnissen wird als Kategorie abgelegt. Indikator f�r VLM-Stabilit�t, *nicht* f�r menschliches Review.

**5. Erste Iteration: Workspace-Dashboard + Transparency-Panel auf Catalog-Seite** (Commits ae8e98e, dd72e76, 80f2b9a)

Zwei neue Panels im Katalog:
- **Local Editorial Workspace** (Recent Activity via GitHub API, Uncommitted via neuem `/api/git-status`, Quick Actions als Copy-to-Clipboard).
- **Public Transparency Panel** (Promptotyping-Vault-Enumeration, Journal-Teaser, Exports-Links \u2014 sichtbar in beiden Modi, damit Paper-Reviewer die Claims verifizieren k�nnen).

Neuer API-Endpoint `GET /api/git-status` liefert `git status --porcelain results/` als JSON (mit Host-Check, Timeout, fix-argumentiertem Subprocess).

**6. Zweite Iteration: Documents-First-Refactor** (diese Session abschlie�end)

Die beiden neuen Panels nahmen zu viel vertikalen Platz ein; die Katalog-Tabelle (das eigentliche Produkt der Edition) wurde in die untere H�lfte gedr�ngt. Konsequenz:

- **Workspace-Panel kollabiert by default** zu einer einzelnen ~32px-Zeile mit Summary-Indikatoren: `\u25B8 Editorial Workspace � <n> uncommitted � last commit \u2026 � 4 quick actions`. Klick aufs Summary-Band toggelt auf / zu, Zustand persistiert in `localStorage` (`szd-htr-workspace-collapsed`). Default: collapsed.
- **Transparency-Panel aus dem Katalog entfernt.** Inhalte leben jetzt unter "Verifiable artefacts" auf der Projekt-Seite (`#about`), unterhalb des gerenderten README. Das ist die semantisch richtige Heimat \u2014 Reviewer klicken auf "Projekt" im Header, nicht auf den Katalog.
- **Journal als prominenter Link** statt Teaser. Die Karte auf der Projekt-Seite zeigt `Read the Research Journal \u2192` als CTA-Button, verlinkt auf die bereits existierende In-App-Rendering-View `#knowledge/journal` (mit TOC und allen 27 Sessions). Der fr�here Teaser (drei geparste H2-Headlines aus `journal.md`) war ein Provisorium \u2014 die vollst�ndige Journal-View ist der echte Ort.
- **Mode-Banner bekommt Live-Status-Chips.** Kleine Terminal-Badges rechts neben dem Prompt: `\u25CF clean` / `\u25CF N dirty` (aus `/api/git-status`) und `\u21BB <rel-time> � <short-sha>` (aus GitHub-API, letzter Commit auf `results/`). Die Live-Info bleibt damit jederzeit sichtbar, ohne Panel-Expansion.

**7. Unicode-Escape-Bugfix**

In der ersten Iteration standen literal-`\u2192`, `\u21BB`, `\u2014` im HTML \u2014 Escape-Sequences funktionieren in JS-String-Literalen, nicht in HTML. Durch echte Zeichen ersetzt.

### Architekturentscheidungen

- **Documents-First als Leitprinzip.** Jede UI-Entscheidung muss beantworten: "Dr�ngt das die Dokumente aus dem Sichtfeld?" Alle nicht-dokumentbezogenen Surfaces m�ssen kompakt sein, optional expandierbar, oder in Nebenr�ume (About, Methodik).
- **Dreiraum-Topologie des Interfaces:** (a) Katalog = Dokumente-Ansicht, prim�r. (b) Viewer = Einzeldokument mit Facsimile + Transcription + Edit-Controls. (c) Projekt (`#about`) + Methodik (`#knowledge`) = Verifizierbarkeit der Methode. Die Navigation im Header unterst�tzt diese Dreiteilung.
- **"Zur�ckschauen" auf zwei Ebenen:** Live-Status (Banner-Chips, letzter Commit in Echtzeit) vs. Narrative (Journal, lesbar mit Kontext und Begr�ndung). Git zeigt *was*, Journal erkl�rt *warum*.
- **GitHub-API als einzige externe Abh�ngigkeit zur Laufzeit.** CSP erweitert um `https://api.github.com` im `connect-src`. Graceful Fallback bei Rate-Limit.
- **Keine Export-Trigger via Button** \u2014 nur Copy-to-Clipboard der Kommandos. Background-Execution mit Progress-UI und Error-Handling w�re eine eigene Baustelle; Copy-to-Clipboard ist ehrlich und funktioniert.

### Offene Punkte / N�chste Schritte

- Edit-History-Panel pro Objekt im Viewer (geplant f�r Durchgang 2 vor First Draft 22.05.).
- Quality-Signals-Popover-Erweiterung (ebenfalls Durchgang 2).
- Vogeler-Ring-Referenz: Untertitel der Progress Bar ("From machine transcription toward expert verification (Vogeler 2025)") wurde auf Wunsch entfernt \u2014 Theorie geh�rt ins Paper, nicht ins UI. Verortung bleibt implizit in der Tier-Reihenfolge.

### Statistiken

| Metrik | Wert |
|---|---|
| Commits (gesamt Sessions 26) | 7 + refactor-commit |
| Neue UI-Surfaces | Mode-Banner, Workspace-Panel (collapsed+expanded), Transparency-Cards (auf About) |
| Neue API-Endpoints | `GET /api/git-status` |
| CSP erweitert | `connect-src: https://api.github.com` |
| Paper-Claim-Coverage | Obsidian Vault verlinkt, Journal verlinkt, Exports verlinkt, Git-Workflow sichtbar |
| LOC (ca.) | +400 JS, +350 CSS, +50 HTML |

---

## 2026-06-08 — TEI-Export: Page-JSON → teiCrafter (deterministisch)

### Was wurde gemacht
- `pipeline/export_tei.py` gebaut: faithful Python-Port des teiCrafter-Referenz-
  Prototyps (`teiCrafter/test/tools/szd-pagejson-to-tei.mjs`), **bit-fuer-bit**
  identische Ausgabe. Page-JSON v0.2 → teiCrafter-ladbare TEI. Kein LLM/API.
  Schliesst die Luecke „nur Katalog-TEI, keine Transkriptions-TEI".
- **Voll-Lauf**: alle 2103 Objekte → `{id}.tei.xml`, 0 Fehler. Ladbarkeits-Sweep
  ueber das ganze Korpus (analog `hersch_loadability.mjs`): **0 Parse-Fehler,
  alle line-level**, 2063/2103 mit nutzbarer Editor-Ansicht.
- **40 „leere" TEI** nach Ursache geklaert: 34 leeres `pages[]` (stromaufwaerts
  OCR/Page-JSON), 6 reine Faksimile-Objekte (nur blank/color_chart). Kein
  Konverter-Fehler.
- **Marker-Anreicherung** (`pipeline/marker_enrich.py`, opt-in `--enrich-markers`,
  separate `{id}.enriched.tei.xml`): line-lokales, fail-safe-auf-Literal Mapping →
  `<unclear>/<del>/<add>/<gap>`. Korpusweit **922 / 26.971 / 15.850 / 687**
  Elemente, **0 Round-Trip-Abweichungen, 0 verlorene Zeilen**. Haertefaelle
  (ungerade `~~`, unbalancierte `{`, `[?3?]`, mehrzeiliger Stempel) blieben
  korrekt literal.
- Doku: [[teicrafter-integration]] (neu, `status: active`), Querverweis in
  [[htr-interchange-format]] §1.4, Index ergaenzt.

### Methodik / Entscheidungen
- **Byte-Identitaets-Fallen** im Port geloest: JS `Math.round` (round-half-up) →
  `jsround()` (`floor(v+0.5)`); Windows-CRLF → `open(..., newline="")`;
  Template-Whitespace exakt wie im Prototyp.
- **Marker-Design adversarisch geprueft** (Multi-Agent-Workflow): ein frueherer
  „ganze-Seite, alle 5 Marker"-Entwurf war unsicher (176 mehrzeilige `~~`-Spans,
  unbalancierte `{`, `[?]` nur ~11 % direkt am Wort). Konsequenz: v1 konvertiert
  nur das **line-lokal Eindeutige**, Rest bleibt verlustfrei literal.
- **Seiten-Notizen**: drop-by-default — CER-neutral (verifiziert: `evaluate.py`
  liest nur `pages[].transcription`); nuetzlicher Teil schon in `page.type`; Rest
  KI-unzuverlaessig. Optionales `<note resp="#szd-htr-ai">` spaeter hinter Flag.

### Abnahme (belegt)
- 6 Demo-Objekte byte-identisch zum Prototyp; `roundtrip_sweep.mjs` 6/6 gruen.
- Default-Pfad nach Einbau der Anreicherung weiter byte-identisch (Regression ok).

### Offen / naechste Schritte
- Operator-Entscheidungen: o_szd.161-Duplikat (zwei Sammlungen), Stempel-/
  Mehrzeilen-Marker als eigener getesteter v2-Schritt, optionales Notes-Carry.
- Kontrakt `converter-reference.md` (teiCrafter-Repo) auf `status: active` heben —
  durch Operator (hier nur szd-htr beschrieben).
- Im Repo getrackt: Demo-Handvoll (plain + enriched); Bulk gitignored.

---

## 2026-06-08 — TEI v2: Marker-Anreicherung erweitert + Coverage-Diagnose

### Was wurde gemacht
- **Marker v2** (`marker_enrich.py`, weiter line-lokal + fail-safe-auf-Literal):
  - `[Stempel:]`/`[Poststempel:]` sole-on-line → `<note type="stamp">` (5. Marker-Familie).
  - plain `[...]` → `<gap reason="illegible"/>` (mid-line; sole-on-line bleibt literal).
  - `[?]` jetzt ZUERST auf tag-freiem Text (kann sonst ein eingefuegtes Tag verschlucken).
  - mehrzeilige `~~`/`{}`-Spans bleiben bewusst literal (korrektes Fail-safe).
- **Notizen-Mitnahme** (`export_tei.py --carry-notes`): `pages[].notes` →
  `<note resp="#szd-htr-ai" type="page">` am `<pb>`, attributiert maschinell/ungeprueft,
  separate `{id}.enriched.tei.xml`. Default bleibt byte-identisch.
- **Coverage-Diagnose** (`diagnose_coverage.py`, read-only): findet die 34 leeren
  (stille Transkriptions-Fehlschlaege, Bilder da/OCR leer) + 6 blank-Objekte,
  schreibt `reports/coverage-gaps.json`, gibt Re-Transkriptions-Befehl aus (loest
  ihn NICHT aus — Operator-Entscheidung).

### Abnahme (belegt, gegen teiCrafter-Engine)
- Default-Pfad nach allen v2-Aenderungen weiter **byte-identisch** (Regression ok).
- enriched v2 ueber alle 2103: **0 Parse-Fehler, 0 Round-Trip-Abweichung, 0
  verlorene Zeile**, Struktur identisch. Erzeugt 889 `<unclear>`, 26.971 `<del>`,
  15.872 `<add>`, 731 `<gap>` (44 plain), 18 `<note type="stamp">`.
- Spot-Checks: Stempel 1083 → note; mehrzeiliger Stempel 1789 bleibt literal;
  Haertefaelle 2404 (ungerade `~~`) / 2846 (`[?3?]`) bleiben literal. Notizen-Mitnahme
  1079: byte-Round-Trip + line-level (folios=5, cells=58).
- Zusaetzlich adversarische Multi-Agent-Semantikpruefung der v2-Umwandlung.

### Offen (Operator)
- Re-Transkription der 34 stillen Fehlschlaege (API-Kosten) — oder Transkriptions-Lane.
- o_szd.161-Duplikat; Mehrzeilen-/`[Label:]`-Marker als v3; converter-reference active.

### Nachtrag — Marker v2.1 (adversarische Semantik-Pruefung, Multi-Agent)
3 Review-Agenten (Protokoll-Treue, TEI-Modellierung, valide-aber-falsch) fanden 1 Blocker
+ 10 major. Umgesetzt:
- **Blocker `{x}`->`<add>`**: der VLM nutzt `{}` massenhaft als Wortsegmentierungs-Rauschen
  (Beleg o_szd.248: `{Persönlich} {die} {höhere}` = laufender Prosatext). Nur ~19 % sind echte
  Einfuegungen. Neuer konservativer Filter (genau EIN kurzes `{Wort}` in anderem Text;
  `>=2`/Zeile, sole-on-line, Worttrennung, Mehrwort -> literal): `<add>` von 15.872 auf **3.013**,
  ~12.900 falsche Editionsaussagen entfernt.
- `<unclear>`: `reason="illegible"` entfernt (`[?]` = unsicher-aber-lesbar, nicht unleserlich);
  nachgestellte Satzzeichen bleiben ausserhalb des Wraps.
- `<del>`: `@rend="strikethrough"` entfernt (Protokoll §3.3 kodiert Streichungsform nicht).
- `<add>`: `@place="above"` entfernt (`{}` = ueber Zeile ODER Rand, §3.4).
- Stempel differenziert: `[Poststempel:]`->`type="postmark"`, `[Stempel:]`->`type="stamp"`;
  `[Marginalie:]`->`type="marginal"` (Protokoll §3.5).
- Neu: `pipeline/test_marker_enrich.py` (29 Faelle, Verhalten + Wohlgeformtheit), gruen.
Abnahme: enriched v2.1 ueber alle 2103: 0 Parse-Fehler, 0 Round-Trip-Abweichung, 0 verlorene
Zeile. Default weiter byte-identisch.

## 2026-06-08 — Dedup: korrespondenzen-Discovery TEI-kanonisch (Commit fb48ca0)

Befund: Das Backup listet **34 Lebensdokumente-Objekte physisch doppelt** — in
`korrespondenzen/` UND `lebensdokumente/`. `discover_objects()` scannte das Verzeichnis blind
und transkribierte sie daher unter beiden Sammlungen (korrespondenzen mit falschem
Korrespondenz-Prompt). Sichtbar wurde es an o_szd.161.

Kanonisch laut TEI: 29 der 34 stehen ausschliesslich in der lebensdokumente-TEI, 0 in
korrespondenzen. 5 (o_szd.76/77/175/176/179) stehen in **keiner** TEI, sind inhaltlich aber
eindeutig Lebensdokumente (Notizbuch, NY-Notizen, Aufsatz-Register, Siegelstempel, Rede).
Die korrespondenzen-TEI liefert 0 numerische PIDs — **kein Parser-Bug**, sondern
Konvolut-Granularitaet (o:szd.korrespondenzen.NAME, 231 Briefpartner), keine Einzelbrief-PID.

Fix: `discover_objects` filtert TEI-kanonisch (neu `_tei_owner_index` + `_canonical_collection`):
PID in einer TEI -> deren Sammlung; sonst (Orphan) -> erste Sammlung in `COLLECTIONS`-Reihenfolge
mit Backup-Dir. Realer Tie-Break-Fall: o:szd.118 steht in lebensdokumente- UND werke-TEI ->
deterministisch lebensdokumente. korrespondenzen-Discovery jetzt 1152 statt 1186; lebensdokumente
/werke/aufsatzablage unveraendert (127/169/625). 34 verwaiste korrespondenzen-Result-Saetze
(170 Dateien) entfernt, lebensdokumente-Versionen intakt.

Abnahme: alle Sammlungszahlen verifiziert, 0 Dangling-Referenzen. Adversarischer Multi-Agent-Review
(5 Dimensionen): 0 funktionale Bugs. Folgearbeit: `pipeline/test_canonical_collection.py` (6 Checks)
+ `pipeline/test_export_tei.py` (jsround + build_tei Wohlgeformtheit) ergaenzt; irrefuehrende
Code-Kommentare praezisiert. **Abzugrenzen** von den „34 leeren `pages[]`" (Coverage-Diagnose,
`reports/coverage-gaps.json`) — gleiche Zahl, anderes Phaenomen.

Offen (Operator): docs/-Viewer via `build_viewer_data.py` neu bauen (entfernt die 34 aus dem
korrespondenzen-Katalog; bewusst ausgelassen, da Frontend-Lane docs/ bearbeitet); 5 Orphans =
Daten-Provenienz-Frage (in keinem GAMS-TEI-Katalog).

---

## 2026-06-10 — Autographen (SZ-AAL): GAMS-Verifikation + fuenfte Sammlung

### Was wurde gemacht
- **GAMS-Ingest SZ-AAL-2026-06 vollstaendig verifiziert**: 379 Objekte (o:szd.3020 bis
  o:szd.3398), alle 1.599 Bild-URLs (`{pid}/IMG.{n}`) per HTTP geprueft -> 200 image/jpeg,
  0 fehlend. Visuelle Stichproben (o:szd.3020, o:szd.3024) passen zu den Book-XMLs.
- **Fuenfte Sammlung `autographen` onboarded**: neues `pipeline/import_autographen.py` baut
  aus dem Ingest-Staging (`PROJECTS\szd\ingeste`) die Backup-Struktur
  (`metadata.json` + `mets.xml` + `images/IMG_n.jpg`) und generiert die TEI-Kontextquelle
  `data/szd_autographen_tei.xml` (379 biblFull). Idempotent re-runnbar (METS-Cache,
  Groessenvergleich beim Kopieren).
- Registrierung: `COLLECTIONS` in `config.py` (am Ende, Tie-Break-Reihenfolge!),
  `COLLECTION_LABELS` in `docs/app.js`, `resolve_group()` routet autographen -> Gruppe I.
- `backfill_quality_signals.py`: hartkodierte Sammlungsliste durch `config.COLLECTIONS` ersetzt.
- Pilot: 10 Objekte transkribiert (10/10 ok, Konfidenz high). Transkriptionsqualitaet an
  zwei Objekten gegen die Faksimiles geprueft (englische Handschrift Lotte + Stefan Zweig,
  praktisch fehlerfrei inkl. tabellarischer Reiseroute).

### Erkenntnisse / Entscheidungen
- **METS kommt von `archive/get/{pid}/METS_SOURCE`** (wie szd-zenodo-backup); `{pid}/METS`
  liefert 404. structMap ist bei Cirilo-Ingests leer -> Bildreihenfolge = IMG.n-Nummerierung.
- **Zuordnung Scan -> IMG.n ueber Bildmasse verifiziert**: exif-Dimensionen im METS gegen
  lokale JPEG-Header (alle 1.599 deckungsgleich) — kein Bild-Download noetig.
- **Cirilo setzt pauschal Sprache "Deutsch"** in die MODS — kein Katalogwert. Viele
  AAL-Briefe sind englisch; der Wert erzeugte beim Pilot 9/10 falsche
  `language_mismatch`-Review-Flags. Entscheidung: Sprache wird NICHT in metadata.json/TEI
  uebernommen (mets.xml bleibt als Beleg), das VLM erkennt die Sprache selbst.
  Nach dem Fix: 0 Review-Flags im Pilot.
- Cirilo vergibt PIDs in alphabetischer Mappenreihenfolge (B1.10 vor B1.2).
- Datenkuriositaet fuer die fachliche Sichtung: ein Book-XML traegt den Autor
  "BRIEFE GEHOEREN NICHT ZUSAMMEN!" (Quelldaten-Notiz im Autorfeld).

### Offen
- Voll-Lauf der restlichen 369 Objekte (laeuft als Hintergrund-Batch, danach
  `build_viewer_data.py`).
- Sprachfeld der AAL-Objekte in GAMS/Cirilo ist fachlich zu klaeren (pauschal "Deutsch").
- `B3_unvollstaendig` (Staging) wartet auf quellseitigen Re-Export, danach Nach-Ingest +
  erneuter `import_autographen.py`-Lauf.

### Nachtrag (10.06. vormittags) — Sessionende, Stand fuer den Wiedereinstieg

- QA-Report ueber alle 379 ingestierten Objekte erstellt (`reports/aal-ingest-qa.md` + `.csv`):
  Bilder 379/379 fehlerfrei (Zaehlung, Masse, GAMS-URLs); Metadaten-Befunde: 3 Autor-Faelle
  (B1.110 "BRIEFE GEHOEREN NICHT ZUSAMMEN!" = o:szd.3034, B10.9 "Trading", B3.138
  "Unidentified") + 23 fehlende Datierungen (Block B3.110-B3.130 + B12/B19) — alle
  quellseitig, bereits in der Lieferung enthalten.
- Mail-Entwurf Korrekturmeldung an die Erschliessung liegt im Obsidian-Vault
  (`Projects/szd/2026-06-10 - Mail-Entwurf Korrekturmeldung SZ-AAL Ingest.md`),
  in ACTIVE-WORK verlinkt.
- Voll-Batch laeuft detached (Start ~06:46, bei Sessionende 115/379, ~18s/Objekt,
  Log `c:/tmp/aal_batch.log`); baut am Ende automatisch `build_viewer_data.py`.
  Dev-Server lief auf Port 8000 (`pipeline/serve.py`).
- GAMS war ab ~Vormittag nicht erreichbar (Timeout auch auf der Startseite). Betrifft
  NUR die Faksimile-Anzeige im Viewer (GAMS-URLs); Batch unbeeinflusst (lokale Bilder).
  Kein Handlungsbedarf unsererseits — nach GAMS-Rueckkehr erscheinen die Bilder wieder.
- Wiedereinstieg: Batch-Ergebnis pruefen (`Get-ChildItem results/autographen/*_gemini-*.json`
  zaehlen, Log-Ende auf "BATCH KOMPLETT"), Stichprobe sichten, Korrekturmeldung versenden,
  Commit der Sammlungs-Integration steht aus.

## 2026-06-10 — Session 26: AAL-Batch abgeschlossen, Katalog-Filter-Refactor (Bestandseinheiten)

**Schwerpunkt:** AAL-Voll-Batch fertig (377/379, 2 Restanten ohne Faksimiles = B3-Re-Export-Fall; 91% high, 21 REVIEW-Flags; Stichproben o_szd.3307/3100 bestaetigen Diskriminanz der Selbsteinschaetzung). Sammlungs-Integration als Sammel-Commit gesichert und gepusht (Operator-Freigabe), GitHub Pages zeigt 2.451 Objekte.

- **Filter-Refactor (Operator-Auftrag):** Katalog-Filter auf deklaratives Registry umgestellt (`FILTER_DEFS` in `docs/app.js`): State, URL-Parameter, Dropdown-Befuellung, Sichtbarkeit, Chips und Listener werden generisch verdrahtet; ein neuer Filter = ein Registry-Eintrag plus `<select>` in index.html.
- **Bestandseinheiten pipeline-seitig:** `derive_unit()` in `build_viewer_data.py` schreibt je Objekt `unit` (Signatur minus letztes Punkt-Segment) in den Katalog; `config.py` traegt `UNIT_TERMS` (Anzeige-Begriff je Sammlung: Konvolut/Mappe/Werkmappe) und `INGEST_INFO` (Klartext je Ingest-Label, Tooltip). Neuer Test `test_unit_derivation.py` (eigenstaendig, Exit 0 = gruen).
- **Einheiten-Filter** ersetzt den Konvolut-Filter vom Vormittag: erscheint nur bei gewaehlter Sammlung (sonst 257 Optionen), Optionen abhaengig von Sammlung+Lieferung, nur Einheiten mit >=2 Objekten; Legacy-URL-Param `konvolut` wird weiter gelesen.
- **Badges:** klickbares Einheiten-Badge in der Signatur-Spalte (filtert auf die Einheit) und Einheiten-Zeile mit Katalog-Link in der Viewer-Meta; Ingest-Badge-Tooltip nutzt jetzt `INGEST_INFO` (alter Text behauptete faelschlich "noch nicht im GAMS").
- Terminologie-Vorbehalt: UNIT_TERMS sind Arbeitsbegriffe; offizielle Bezeichnung (und Aufloesung des Kuerzels AAL) wird ueber die Korrekturmeldung mit der Erschliessung geklaert.
- Wiedereinstieg: REVIEW-Sichtung der 21 markierten AAL-Objekte (lokal, `?ingest=SZ-AAL-2026-06&review_status=needs_review`), Korrekturmeldung versenden; Browser-Sichtpruefung des Filter-Refactors steht aus (nur node --check + Tests + Datenchecks gelaufen).

**Nachtrag Session 26 (Operator-Feedbackrunde):** Status-Modell auf drei Stufen vereinfacht (Operator-Entscheidung): Mensch-geprueft (am Faksimile gegengelesen, bei Bedarf korrigiert — gilt als verifiziert und Ground-Truth-faehig; ersetzt Gepruft+Verifiziert), Agent-geprueft (vorher Auto-geprueft), Ungeprueft ("Review noetig" ist kein Status mehr, nur Triage-Hinweis "zuerst sichten" innerhalb von Ungeprueft). Gespeicherte review.status-Werte unveraendert, Legacy-URL-Werte gemappt. Klickbares Signatur-Praefix wieder entfernt (Operator: Tabelle nicht klickbar machen), Konvolut-Zugang nur noch ueber Filter und Viewer-Meta-Link; Einheiten-Filter auf die Briefbestaende begrenzt (UNIT_TERMS nur korrespondenzen+autographen). Sammlung heisst im Viewer jetzt "Briefkonvolute (SZ-AAL)". Code-Kommentare auf Englisch/kompakt umgestellt (neue Operator-Regel). Offen registriert: Datenstrom-/Provenienz-Modell fuer Original-OCR vs. Bearbeitung (Operator-Idee, Konzept in ACTIVE-WORK/Vault), GT-faehig-Kriterium + CER-aus-Edits-Skript.

**Nachtrag 2 Session 26 (Datenstrom-Modell, Operator-Entscheidung):** Zwei Datenstroeme je Seite: `transcription` (Arbeitsfassung) + `transcription_llm` (unveraenderlicher Roh-Output, gesetzt beim ersten Edit in serve.py UND import_reviews.py — letzterer hatte bisher gar keine Sicherung, Luecke geschlossen). Bestand migriert via `backfill_transcription_llm.py` (42 Dateien, 61 Seiten). Neues `report_cer_from_edits.py`: jede menschliche Korrektur ist eine CER-Messung gegen den Roh-Output; erster Lauf: 56 Seiten / 40 Objekte / 114k Zeichen, Korpus-CER zeichengewichtet 0,96%, Ausreisser o_szd.1090 S.2 (89%) — Report `reports/cer-from-edits.md`. Hinweis: Messung umfasst alle Korrekturen (auch agent-editierte Seiten), Referenz ist immer der Zustand vor dem ersten Edit. Knowledge-Ordner-Audit ebenfalls heute: verification-concept 1078->428 Zeilen, Signal-Schwellen an Code angeglichen, fuenfte Sammlung in data-overview, Details in den Commits.

**Nachtrag 3 Session 26 (Agent-Triage + Signal v1.6 + Neulaeufe):** Drei Opus-Agenten haben die 28 geflaggten AAL-Objekte Bild-gegen-Text triagiert (strikt lesend): 22 OK (als agent_verified markiert, Kleinbefunde dokumentiert), 2 FEHLERHAFT (Repetition-Runaway sprengt JSON: o_szd.3135, o_szd.3375), 4 STRITTIG fuer Operator-Sichtung (o_szd.3231/3277/3280/3306, eilige Kursive mit Halluzinationsverdacht) — Report `reports/aal-review-triage.md`. Querbefund der Triage: 7 Flags gingen allein auf kurze Umschlag-/Adressseiten zurueck (legitim kurz, gegen Median langer Briefseiten gemessen) → quality_signals v1.6: `_is_envelope()` (Notes-Erkennung) nimmt diese Seiten von der Laengen-Anomalie aus; neuer Test `test_quality_signals.py`; Backfill ueber den Bestand: 43 Flags weniger, kein neues (auch 16 aeltere Korrespondenzen-Objekte betroffen). Neulaeufe: beide Runaway-Objekte erst mit chunk-size 4 (3375: 11/15 Seiten), dann seitenweise (chunk-size 1) vollstaendig — Einzelseiten-Verarbeitung bricht die Schleife zuverlaessig. Nachverifikation per Opus-Agent: 3135 sauber (inkl. Lotte-Bleistift-Nachsatz S.2), 3375 mit zwei belegten Fehlern, per Agent-Edit korrigiert (S.1 Geschaeftszahl Cg 597->591/38, S.2 Durchschlag-Halluzination geleert; edit_history source=agent, Roh-Output in transcription_llm). COLLECTION_LABELS von app.js nach config.py verschoben (catalog meta `collectionLabels`, Frontend liest nur). Subagenten laufen ab heute per Operator-Regel auf Opus/Sonnet (Override), nicht mehr auf dem Main-Modell.

## 2026-06-11 — AAL B3-Nachzug: Re-Export, Ingest, Onboarding, Transkription

**Schwerpunkt:** Der bei der Erstrunde zurueckgestellte unvollstaendige B3-Rest ist neu exportiert, ingestiert und in die `autographen`-Sammlung onboardet. Damit zaehlt AAL jetzt 482 Objekte (vorher 379). Transkription der Nachzuege laeuft.

- **Re-Export-Analyse** (`SZ_AAL_B3_Results-20260611...zip`, 1,25 GB): Von 104 zuvor unvollstaendigen B3-Objekten sind **103 jetzt komplett** (559 nachgelieferte Bilder). Zwei strukturelle Befunde: (1) der Export ist **doppelt verschachtelt** (`SZ_AAL_B3_Results/SZ_AAL_B3_Results/<obj>/...`) — die alten Build-Skripte finden so 0 Objekte, Folder-Matching muss tiefenrobust sein; (2) **B3.108 weiterhin kaputt** — nur RAW/TIFF/Lightroom, kein Viewer-XML, faelschlich unter B3.105 verschachtelt → Faksimile-Nachexport in der Korrekturmeldung angefordert. Neuer Fund: mitgelieferter **Katalog `SZ-AAL_B3.xlsx`** (144 Zeilen x 39 Spalten) mit Verfasser/Adressat+GND, normalisierter Datierung, Entstehungsort, Sprache — beantwortet die fruehere Pauschal-"Deutsch"-Frage fuer B3 (real 140 GER / 2 ENG / 1 GER;FRE / 1 GER;ENG) und liefert Anreicherungsmaterial. Skripte unter `c:\tmp\`: `analyze_b3_new.py`, `build_b3_nachexport.py`, `b3_gap_report.py`.

- **GAMS-Ingest** (Cirilo, Operator): 103 Objekte als separater Import (`ingeste_B3_nachexport`) → PIDs **o:szd.3399-3501** (lueckenlos; 59 trugen die PID schon im Book-XML, 44 vergab Cirilo ab 3458 alphabetisch). PID<->Signatur via METS-Titel aufgeloest (Signatur steht im `mods:title`, NICHT in `note[@type=signature]`). **Bildverifikation gedrosselt** (1 req/s, HEAD `{pid}/IMG.{n}`): **567/567 Bilder, 0 fehlend**. Verifier `c:\tmp\verify_gams_nachzug.py`, Karte `c:\tmp\nachzug_pidmap.csv`.

- **Master-Excel** ueber alle 482 (+ B3.108-Fehlzeile): `PROJECTS/szd/SZ-AAL_Objekte_PIDs_QA.xlsx` — PID, Seiten, Titel, Mirador-URL (`archive/objects/{pid}/methods/sdef:IIIF/getMirador`), Bild-Status, B3-Katalog-Metadatenluecken, Kontrolle-Flag. 39 Objekte mit Kontrollbedarf (B3.108 Faksimile; 31 Datum; 3 Autorfeld B1.110/B10.9/B3.138; 4 fehlende Verfasser/Adressat B3.48/131/140/141). Korrekturmeldung an die Erschliessung **versendet** (Entwurf `Vault/Projects/szd/2026-06-11 - Mail-Entwurf B3 Re-Export Rueckmeldung.md`), Excel-Liste mitgeschickt.

- **Pipeline-Onboarding:** 103 Mappen nach `ingeste/` konsolidiert (jetzt 482), `import_autographen.py` ueber alle 482 gelaufen (idempotent, 379 uebersprungen) → Backup 482 Objekte, METS<->Scan-Bildmasse fuer die 103 verifiziert, TEI `szd_autographen_tei.xml` neu = **482 biblFull / 2.166 Seiten**, 0 Fehler. Sprache aus dem METS bewusst nicht uebernommen (Cirilo-Pauschalwert; VLM erkennt selbst) — die echte Katalog-Sprache bleibt separater GAMS/Edition-Schritt.

- **Transkription** (`transcribe.py --collection autographen`, gemini-3.1-flash-lite-preview): laeuft ueber 105 Objekte = 103 Nachzug + 2 Altstragglers (o_szd.3222, 3380, hatten noch kein Ergebnis). Idempotent, 377 fertige uebersprungen.

- **Transkription PAUSIERT (1/105), spaeter fortsetzen.** Befund beim Start: der genai-Client in `transcribe.py` hatte kein Request-Timeout → ein einzelner rate-limitierter Bild-Call (gemini-3.1-flash-lite-preview hat enge Minuten-/Token-Quota, 7-Bild-Calls ~9 MB sind tokenschwer) fror den ganzen Batch ein (21 min Stillstand beim 2. Objekt). **Fix angewandt (uncommittet):** Client mit `HttpOptions(timeout=120_000)`, und `timeout`/`deadline` in `_call_api` als retrybar ergaenzt → Batch haengt nicht mehr, faellt bei Limit nach Backoff sauber durch. Isolierte Probe bestaetigt: API/Modell/Key gesund (Text 0,6 s, 7-Bild-Call 9,3 s) — reines Quota-Throughput-Thema. Wiederaufnahme: `python transcribe.py --collection autographen --delay 8` (idempotent, ueberspringt die 378 fertigen; nur die 104 offenen + ggf. Mop-up). Danach: Auswertung (high/medium, REVIEW-Flags) + Sammel-Commit (transcribe.py-Fix + TEI + Ergebnis-JSONs) nach Operator-Freigabe, kein Push.
- **Weiter offen:** `ingeste_B3_nachexport/` nach dem Kopieren redundant; B3.108 wartet auf Faksimile-Nachexport; Katalog-gestuetzte Sprach-/Datums-/GND-Anreicherung der AAL-Objekte als eigener Strang.

## 2026-06-21 — AAL-Lebensdokumente (L1-L13): Import + Branch-Sicherung nach main

**Schwerpunkt:** Sechste AAL-Teillieferung — 13 Lebensdokumente SZ-AAL/L1-L13 (Vertraege,
Reisepass, Adressbuch u.a.) ingestiert und in die Sammlung `lebensdokumente` onboardet.
Die zuvor uncommittete, undokumentierte Arbeit auf `chore/frontmatter-migration` gesichert
und nach main zusammengefuehrt.

### Was wurde gemacht (L1-L13 Import)
- **`pipeline/import_lebensdokumente_aal.py` (neu, 359 Z.):** Import der 13 SZ-AAL/L-Objekte.
  Bewusst anders als `import_autographen.py`, weil die Quelllage anders ist:
  - **PID-Aufloesung per METS-Titel** (`--resolve START END`): die Book-XMLs im Staging tragen
    keine `<idno>`; die Cirilo-PIDs werden ueber den `mods:title` (Signatur darin) aufgeloest,
    Doppel-Ingest wird erkannt (kein Early-Stop, mehrdeutige Treffer bleiben leer). Karte in
    `C:/tmp/lebensdok_aal_pidmap.csv` (13/13 eindeutig: L1=o:szd.3515, L2-L9=3520-3527,
    L10-L13=3516-3519 — Cirilo vergibt alphabetisch, daher L10 vor L2).
  - **TEI uebernommen statt generiert:** die 13 `biblFull` (SZDLEB.144-156) werden aus der
    massgeblichen Katalog-TEI `SZD/data/PersonalDocument/SZDLEB.xml` geklont und nur um den
    PID-`altIdentifier` ergaenzt — so bleiben GND, Provenienz, Masse erhalten. Merge in
    `data/szd_lebensdokumente_tei.xml` (jetzt 156 biblFull, 134 mit PID-idno).
  - **Sprache aus SZDLEB** (echter Katalogwert, L5-L11 englisch) statt aus dem Cirilo-METS
    (pauschal "Deutsch") — die Sprachfalle der B-Autographen greift hier nicht.
  - Backup `lebensdokumente/o_szd.{3515-3527}/` mit METS<->Scan-Bildmassen-Verifikation,
    `provenance.in_gams=true`. 13/13 Backups vorhanden (Bilder + metadata.json).
- **`pipeline/config.py`:** INGEST_INFO-Eintrag `SZ-AAL-L-2026-06`.

### Abnahme (belegt, maschinell gruen)
- TEI wohlgeformt, 156 biblFull, alle 13 L mit PID (`xml.etree` Parse).
- Pipeline-Tests gruen: `test_export_tei` (12), `test_canonical_collection` (6),
  `test_marker_enrich` (30), `test_quality_signals` (5), `test_unit_derivation`.
- `import_lebensdokumente_aal.py --dry-run --tei-only`: idempotent (0 neu, 13 ersetzt) —
  Re-Run produziert denselben TEI-Stand.

### Branch-Entscheidung (aus der Editionsphilologie-Persona)
Frage des Operators: Branch `chore/frontmatter-migration` mit der L1-L13-Arbeit abschliessen
und nach main mergen, oder getrennt halten?
- **Entscheidung: abschliessen, dokumentieren, per Fast-Forward nach main.** Begruendung:
  (1) Das Betriebsmodell der Leitstelle haelt keine getrennten Feature-Branches mehr vor.
  (2) Die Arbeit ist intern und reversibel; main war direkter Vorfahr (ff moeglich, kein
  Merge-Commit, keine Re-Integration noetig). (3) Es geht nichts genuin Neues oeffentlich:
  die L-Objekte sind noch nicht im Katalog (nicht transkribiert), oeffentlich wird nur die
  o_szd.3222-Straggler-Zeile (Ergebnis war schon in main) plus Tooltip-Texte.
- Sauber getrennt committet (eigene explizite Pfade, kein `git add -A`):
  Import-Strang (Script + TEI + config) und Viewer-Daten-Rebuild (catalog/autographen/
  knowledge.json).

### Viewer-Daten-Rebuild (zweiter Commit)
- `docs/catalog.json` (2452 Objekte, +o_szd.3222 B3-Straggler + L-ingestInfo),
  `docs/data/autographen.json` (o_szd.3222), `docs/data/knowledge.json` (Frontmatter-Migration:
  built_at 18.06., Status `stable`->`complete`). Kein L-Objekt im Katalog — korrekt, da
  L1-L13 noch nicht transkribiert.

### Stand L1-L13 / offen
- **Fertig:** Backup, TEI mit PIDs, config. **Offen:** Transkription (0/13) und damit
  Katalog-Integration — naechster Milestone.

---

## 2026-07-27 — Katalog: Triage nach einzelnem Qualitaetssignal

### Was wurde gemacht
Operator-Feedback: `needs_review` sollte gefiltert *mit Grund* sichtbar sein. Ausgangslage
im Viewer: der Filter "Zuerst sichten" (`review_status=priority`) fasste alle Signale
zusammen, der Grund stand nur im Tooltip des Ungeprueft-Badges — nicht scanbar.

Umgesetzt in `docs/app.js`, `docs/index.html`, `docs/app.css`:
- Neuer Filter `reviewReason` (URL-Param `reason`, Dropdown "Alle Signale") in `FILTER_DEFS`.
  Optionen mit Trefferzahl, abhaengig von `collection` und `reviewStatus`; kombinierbar
  mit dem Status-Filter (bewusst *kein* impliziter Ungeprueft-Filter, damit man ein Signal
  auch ueber schon geprueftem Bestand nachschlagen kann).
- `renderReviewCell()` in Badge + `reasonChips()` aufgeteilt. Die Signale erscheinen als
  klickbare Chips in der Status-Spalte (Kurzlabels `REASON_SHORT_LABELS`, Precision im
  Tooltip via `REASON_TOOLTIPS`); Klick setzt den Signal-Filter statt das Objekt zu oeffnen.
- Statistik-Dashboard: Balken im Signal-Diagramm und Heatmap-Zellen verlinken jetzt auf
  das jeweils angeklickte Signal statt pauschal auf `review_status=priority`.

### Zahlen (Stand catalog.json, 2452 Objekte)
- 324 Objekte mit mindestens einem Signal (302 mit einem, 22 mit zwei; kein Objekt hat
  `needsReview` ohne Grund oder umgekehrt).
- `language_mismatch` 156, `page_length_anomaly` 154, `page_image_mismatch` 36.
- Genau deshalb der Filter je Signal: die Precision ist sehr unterschiedlich
  (Seitenlaenge/Bild-Text 100%, Sprache 50%) — eine gemeinsame Liste mischt eine
  verlaessliche mit einer zur Haelfte falsch-positiven Arbeitsliste.

---

## 2026-07-30 — Hygiene-Runde: Root konsolidiert, Index modernisiert, Trust-Modell belegt

**Schwerpunkt:** Drei Altlasten abgetragen (stale MOC, EQUALIS-Rest, unkonsolidierter
Repo-Root), zwei Lieferungen ergaenzt (minimale Tests, Evaluationshaken zum Antrag).
Kein Eingriff in `data/`, `results/`, `reports/`. Nichts geloescht, jede Verschiebung per
`git mv`, die Historie bleibt erhalten.

### Root konsolidiert (git mv)

| vorher | nachher | Begruendung |
|---|---|---|
| `PAPER.md` | `paper/PAPER.md` | Abschlussbericht, gehoert mit seiner Evidenzbasis zusammen |
| `PAPER-FINDINGS.md` | `paper/PAPER-FINDINGS.md` | Evidenzbasis, wird von `PAPER.md` referenziert |
| `PAPER-TEXT.md` | `paper/drafts/PAPER-TEXT.md` | ueberholter Zwischenstand |
| `PAPER-TEXT-FILLED.md` | `paper/drafts/PAPER-TEXT-FILLED.md` | ueberholter Zwischenstand |
| `CLAUDE-TASK.md` | `paper/drafts/CLAUDE-TASK.md` | Arbeitsanweisung, die genau diese Zwischenstaende erzeugt hat |
| `Plan.md` | `knowledge/plan.md` | echtes Wissensdokument (Phasenstand und datierter Entscheidungslog) |

`paper/` wurde `docs/paper/` vorgezogen, weil `docs/` das GitHub-Pages-Root der SPA ist und
die Berichtsdateien dort als lose Markdown-URLs mitausgeliefert wuerden. Neu ist
`paper/README.md` mit dem Status je Datei. Der Root traegt jetzt README, CLAUDE.md, LICENSE,
CITATION.cff, codemeta.json, die beiden requirements-Dateien und die Code- und Datenordner.

Nachgezogene Referenzen:

- `README.md`, Link auf `paper/PAPER.md` samt Evidenzbasis
- `CLAUDE.md`, Projektstruktur und Verweis auf `knowledge/plan.md`
- `knowledge/index.md`, `knowledge/verification-fair4rs.md`
- `knowledge/journal.md`, der Session-1-Link zeigt jetzt auf `[[plan]]`

`knowledge/plan.md` hat Frontmatter bekommen (Titel, Status, Typ), damit es im Vault-Viewer
als Dokument erscheint statt als nackter Slug. Der Inhalt ist unveraendert.

### Index modernisiert

`knowledge/index.md` war seit 2026-06-10 stehengeblieben, mit Status `complete`, ohne
Template-Deklaration und ohne die beiden neueren Dokumente. Neu nach der Konvention fuer
Promptotyping Documents, mit project/method/template-Bloecken im Frontmatter, Status
`stable`, einer Funktionstabelle je Dokument in vier Gruppen und einem Abschnitt Lesepfade.

Die Form ist durch eine Nebenbedingung bestimmt. `parse_index_sections()` in
`build_viewer_data.py` liest die `##`-Ueberschriften und die Wikilinks des Index und baut
daraus die Vault-Navigation im Viewer. Darum vier gruppierte Tabellen statt einer einzigen,
sodass die Gruppierung im Frontend erhalten bleibt, und Lesepfade ohne Wikilinks, weil sonst
eine Pseudo-Sektion mit Dubletten entstuende. `docs/data/knowledge.json` neu gebaut, 14
Dokumente, alle einer Sektion zugeordnet, keine Waisen.

### EQUALIS-Rest aufgeloest

`knowledge/dia-xai-integration.md` war eine Zulieferungsspezifikation an EQUALIS, das am
2026-07-18 aufgeloest wurde. Neu geschrieben als Verhaeltnisbestimmung. Die Pipeline ist
Messgegenstand einer im DIA-XAI-Pilot laufenden CER-Evaluation, und ihr
Vier-Stufen-Vertrauensmodell ist einer der Provenienzansaetze, die der geplante Antrag in
WP1 zusammenfuehrt. Der Antragstext §4 steht als pruefbares Zitat im Dokument, mit den
Belegstellen im Code. Neu sind ein Abschnitt zu den drei Evaluationshaken und die Angabe,
was das Modell nicht leistet (keine Ebene unterhalb der Seite, keine vorab definierte
Prueftiefe je Materialklasse).

Was sich nicht neu verankern liess, steht unter "Historischer Stand (EQUALIS, aufgeloest
2026-07-18)", also das damalige Aggregator-Rollenmodell und die fuenf Dimensionen mit ihren
Datenquellen in der Pipeline. Schema `dia-xai-metrics-v1`, UC3-Nummer und der alte
Meilensteinplan sind gegenstandslos und werden nicht fortgeschrieben; sie stehen in der
Git-Historie des Dokuments.

### Trust-Modell gegen den Code geprueft

Die Antragsbeschreibung (§4) wurde Behauptung fuer Behauptung gegen den Code gehalten.
Alle drei Kernaussagen halten:

- **Vier gespeicherte Stufen**, aus keinem Score abgeleitet: `gt_verified`, `approved`,
  `agent_verified` und der fehlende `review`-Block. Whitelist in `serve.py:84`.
  `needs_review` ist Triage innerhalb von Stufe 3 und kein Status.
- **Maschinenzustand ueberlebt die Korrektur.** `serve.py:159-168` setzt `transcription_llm`
  einmalig und haengt an `edit_history` an, mit `source` (human/agent);
  `import_reviews.py:152-161` spiegelt das. `report_cer_from_edits.py` misst daraus.
- **Keine Verdichtung zu einer Zahl.** Pruefstufe, `result.confidence` (kategorial) und
  `quality_signals` bleiben getrennte Felder und getrennte Filter. Im Code gibt es keinen
  Ort, der sie verrechnet.

Drei Abweichungen, die dokumentiert gehoeren statt geglaettet zu werden:

1. `gt_verified` ist end-to-end implementiert (GT-Verify im Viewer, Status in der API),
   doch **kein Objekt traegt die Stufe**. Der Bestand zaehlt 19 `approved`, 85
   `agent_verified` und 2.366 Objekte ohne Review. Die oberste Stufe ist damit Fassung ohne
   Praxis.
2. `import_reviews.py:169` kann `status: "reviewed"` schreiben, einen fuenften Wert, den
   weder die Vier-Stufen-Beschreibung noch `isHumanChecked()` in `app.js` kennt. Im Bestand
   kommt er nicht vor. Latenter Widerspruch, offen registriert.
3. Die Anzeigeschicht fasst Stufe 0 und 1 zu "Mensch-geprueft" zusammen. Das ist Absicht und
   dokumentiert (Operator-Entscheidung 2026-06-10). Die Vier-Stufigkeit ist damit im
   Datenmodell sichtbar, im Frontend nur dreistufig.

`README.md` traegt die Aussage jetzt als eigenen Abschnitt "Trust tiers and verification
provenance" direkt nach "Approach", statt sie wie bisher im Abschnitt zum lokalen Editieren
zu fuehren, samt Erhaltung des Maschinenzustands, Nicht-Verdichtung und dem Hinweis auf den
ungenutzten Stand von Stufe 0.

### Tests

Die Annahme "kein Test vorhanden" stimmte nicht. `pipeline/test_*.py` enthaelt fuenf
Regressionstests, die eigenstaendig und unter pytest gruen laufen. Ergaenzt um zwei billige,
klar nuetzliche Pruefungen unter `tests/`:

- `test_page_json_schema.py` prueft alle 2.069 exportierten `results/*/*_page.json` gegen
  `schemas/page-json-v0.2.json` (Draft 2020-12), dazu die Selbstpruefung des Schemas und das
  Versionsfeld. Laufzeit rund eine Sekunde. Der Grund liegt im Format selbst, es ist der
  Vertrag mit teiCrafter, PAGE XML und METS; ein Drift zwischen Exporter und Schema faellt
  sonst erst dort auf.
- `test_trust_tiers.py` prueft acht Faelle der Uebergaenge in `serve.py` gegen einen
  temporaeren results-Baum (monkeypatch auf `RESULTS_BASE`). Abgedeckt sind jede bekannte
  Stufe wird geschrieben, eine unbekannte abgelehnt, die Agent-Stufe fuehrt das pruefende
  Modell mit, der erste Edit sichert den Roh-Output, der zweite ueberschreibt ihn nicht,
  eine unveraenderte Seite erzeugt keine History, der Edit-Pfad kann die Agent-Stufe nicht
  beanspruchen, und das Approve laesst Konfidenz und Signale unberuehrt.

`requirements-dev.txt` neu (pytest, jsonschema). Gesamtlauf
`python -m pytest tests/ pipeline/` ergibt 18 gruene Tests, ohne API-Key und ohne
Bild-Backup. Der Aufruf ist in README und CLAUDE.md dokumentiert.

### Evaluationshaken zum Antrag

`.github/ISSUE_TEMPLATE/` neu mit drei kriterienunabhaengigen Vorlagen, englisch, ohne
Implementierungsvorgabe. Vier-Tupel-Protokoll (erste Experteneinschaetzung, KI-Vorschlag,
finale Entscheidung, Referenzantwort), Provenienz-Export (Produktions-, Entscheidungs- und
Verifikationsschicht je Item) und Gold-Standard-Haken (Referenzantworten mit vorab
festgelegter Prueftiefe je Itemklasse). Label `antrag-eval` (#1B6B7D) im Remote angelegt.
Die erste Vorlage haelt die bekannte Luecke fest, die Experteneinschaetzung vor Sicht des
Vorschlags wird nicht erhoben, weil der Vorschlag im Ablauf immer zuerst da ist; aus dem
Bestand ist das Tupel daher nur dreistellig rekonstruierbar.

### Offen

- Stufe `gt_verified` in der Praxis belegen oder die Beschreibung anpassen.
- `import_reviews.py`, den Status `reviewed` in die Vier-Stufen-Systematik einordnen oder
  entfernen.
- `PAPER.md` beschreibt den Stand vom Juli 2026 und nennt `Plan.md` im Root. Bewusst nicht
  nachgezogen, weil der Bericht abgeschlossen ist; vermerkt in `paper/README.md`.
- `SETUP-REVIEW.md` und `SETUP-REVIEW-KURZ.md` sind mit der Review-Pipeline im Root
  dazugekommen und wurden hier nicht angefasst, weil sie aus paralleler Arbeit stammen. Ob
  sie im Root bleiben oder nach `docs/` wandern, ist eine Operator-Entscheidung.

### Rebase auf parallele Arbeit

Waehrend dieser Runde war `origin/main` sechs Commits weiter (Review-Pipeline, Filter je
Signal, Reviewer-Identitaet). Die Arbeit wurde darauf rebased statt gepusht.
`knowledge/plan.md` hat die dortige Ergaenzung mitgenommen, `knowledge/index.md` fuehrt
`review-findings` jetzt in der Funktionstabelle, `docs/data/knowledge.json` wurde nach dem
Rebase neu gebaut. Ein oben notierter Befund ist damit erledigt: `pipeline/reviewer.py`
loest den Reviewer-Namen jetzt ueber `SZD_REVIEWER` beziehungsweise `git config user.name`
auf, der fest verdrahtete Klarname in `serve.py` und `import_reviews.py` ist weg.

---

## 2026-07-31 — Wissensbasis nachtraeglich an der Konvention ausgerichtet

Anlass ist das Methodenpaper "Promptotyping. Translating Research Data into Research
Artefacts through Context Engineering and Agentic Engineering", das dieses Repository als
Fall fuehrt. Die Ausrichtung geschah ausdruecklich post hoc. Die Evidenzzitate des Papers
zeigen auf den Stand davor, Commit `eb632d1`, und bleiben dort gueltig; diese Runde
rekonstruiert keinen frueheren Zustand, sondern setzt Metadaten nach. Kein Inhalt wurde
geaendert, keine Datei umbenannt, verschoben oder geloescht. Eine Vorlage traegt eine
Funktion und keinen Dateinamen, die gewachsenen Namen bleiben deshalb stehen.

### Frontmatter

Alle sechzehn Dokumente unter `knowledge/` tragen den Pflichtkern der Konvention Knowledge
Documents (v0.2) jetzt vollstaendig und konform.

- `method.url` in zwoelf Dokumenten auf `https://dhcraft.org/Promptotyping/` gehoben; die
  alte Kleinschreibung ohne Schraegstrich loest nicht auf.
- `project.repository` in dreizehn Dokumenten ohne `.git`-Endung, einheitlich mit den
  uebrigen.
- `status` auf das Enum `draft|active|archived` gebracht. Neun `complete`, zwei `stable` und
  ein `living` wurden zu `active`, ebenso drei `draft` bei gepflegten Dokumenten.
  `htr-interchange-format` bleibt `draft`, weil das Dokument sich selbst als Entwurf
  ausweist. Nichts ist `archived`, kein Dokument erklaert sich als abgeloest.
- `created` und `updated` blieben unangetastet. Die Werte stammen aus der Migration vom
  2026-06-13 samt der Korrektur `e67dc22`, die die handgesetzten Entstehungsdaten bewusst
  gegen die Git-Daten stehen liess. Ein Ueberschreiben haette diese Entscheidung verworfen.
- `authors: [Christopher Pollin]` dort, wo die kuratorische Verantwortung eindeutig bei ihm
  liegt. `review-findings` bekommt das Feld nicht, weil es die Urheberschaft je Eintrag
  selbst kennzeichnet und mehrere Beitragende fuehrt.
- `generated-with` nur in `teicrafter-integration` und `verification-fair4rs`. Nur dort weist
  die Git-Historie ein einziges Modell ueber die gesamte Dateigeschichte aus. Sonst haben
  Commits mehrerer Modelle die Datei beruehrt, und ein beruehrender Commit belegt keine
  Erzeugung.

### Vorlagenzuordnung

Zwoelf Dokumente tragen jetzt ein `template`-Objekt mit `name`, `version`, `url` und
`alias`. Neu sind Datengrundlage, Domaenenwissen, Verification (zweimal), Integration
(zweimal), Architecture (dreimal), Plan und Journal; `index` hatte das Feld bereits und
wurde auf Vorlagenversion 0.2 gezogen, `verification-fair4rs` fuehrte einen unvollstaendigen
Block, der nun `version` und `alias` mitfuehrt.

Die Architecture-Funktion ist auf drei Dateien geteilt, was die Vorlage ausdruecklich
zulaesst und was hier dem tatsaechlichen Zuschnitt entspricht, Arbeitsformat, Archivausgabe,
Layout-Stufe. Integration steht zweimal, weil das Repository zwei Schnittstellen nach aussen
fuehrt. Beide Faelle sind in der Vorlage Integration selbst als empirische Basis genannt,
`teicrafter-integration.md` und `dia-xai-integration.md`.

Vier Dokumente bleiben freihaendig, weil der Katalog fuer ihre Funktion keine Vorlage fuehrt,
`evaluation-results`, `security`, `stats-dashboard` und `review-findings`. Die Begruendung je
Dokument steht in `knowledge/index.md`, ebenso die Funktionen, die bewusst kein Dokument
unter `knowledge/` tragen. Eine unerwaehnte Luecke sieht aus wie ein Versehen, eine
begruendete ist eine Entscheidung.

### Index und Viewer

`knowledge/index.md` bekommt im Abschnitt Konvention eine Zuordnungstabelle und die
begruendeten Luecken. Die vier bestehenden Funktionstabellen und die Lesepfade blieben
unberuehrt, weil `parse_index_sections` in `pipeline/build_viewer_data.py` aus den
`##`-Ueberschriften und den Wikilinks die Vault-Navigation baut. Der neue Abschnitt fuehrt
deshalb keinen einzigen Wikilink; der Parser laeuft ueber ihn hinweg, ohne eine Sektion zu
erzeugen. Gegen `docs/data/knowledge.json` geprueft, die Sektionsstruktur ist Byte fuer Byte
dieselbe wie vorher.

Ein Build-Eingriff war nicht noetig. `parse_frontmatter` trennt das YAML schon heute vom
Body ab, das erweiterte Frontmatter erscheint also nicht im Viewer. Sichtbar wird allein der
Status-Chip, und `active` ist in `docs/app.css` bereits gestylt, waehrend `complete` und
`living` es nie waren.

## 2026-08-26 — Review-Session: 34 Totalausfaelle erhoben, Viewer nachgezogen

Session von Julia Hintersteiner am lokalen Dev-Server. Anlass war eine gewoehnliche
Redigier-Runde; zwei Befunde daraus sind ueber die Session hinaus relevant.

### 34 Objekte ohne verwertbares Ergebnis

Beim Sichten der `needs_review`-Liste fielen Objekte auf, die sich nicht redigieren lassen,
weil es keinen Text gibt: `result` enthaelt nur `raw`, kein `pages`-Array. Ein Scan aller
2.452 Ergebnis-JSONs findet genau 34 solcher Faelle, zusammen 836 Faksimile-Scans, verteilt
ueber alle vier Sammlungen. Keines traegt einen Review-Status, und es gibt keine weiteren
Totalausfaelle — die Liste ist geschlossen.

Der Mechanismus ist der aus `reports/aal-review-triage.md` bekannte Runaway (`o_szd.3135`,
`o_szd.3375`, Neulauf in `a96cd7f`). Neu ist die Groessenordnung und ein Muster, das die
Einzelfaelle damals nicht hergaben: In 28 der 29 Schleifen wiederholt das Modell keinen
Fliesstext, sondern Leerraum oder ein Markup-Zeichen der eigenen Transkriptionskonvention —
`\n` und `\t` zehnmal, `[...]` siebenmal, `[?]` sechsmal, `~~ ~~` dreimal, Punktfolgen
zweimal. Das Modell kippt also dort, wo das Annotationsschema selbst legitime Wiederholung
vorsieht: leere Seiten, schwer lesbare Passagen, gestrichene Absaetze. Beim AAL-Fall waren
es die gepunkteten Trennlinien einer Klageschrift, also derselbe Ausloesertyp. Der Ausfall
ist damit an Materialeigenschaften gebunden und nicht zufaellig verteilt.

Die uebrigen fuenf: vier leere API-Antworten und ein reiner Abbruch (`o_szd.1886`, endet
nach 234 kB mitten im Wort, ohne Wiederholung).

Rund 300 Seiten liegen ohne neuen API-Call im Prefix der Rohdaten, 187 davon mit Text —
bei `o_szd.1886` allein 170 lueckenlose Seiten mit 211.623 Zeichen. `parse_api_response()`
hat fuenf Reparaturstufen, aber keine, die abgeschlossene Seitenobjekte aus einem
abgeschnittenen Prefix uebernimmt; Stufe 5 schliesst offene Arrays, kann einen offenen
String aber nicht schliessen, und genau darin steckt die Schleife.

Vollstaendige Liste, Ausfallarten je Objekt und Empfehlung: `reports/pipeline-totalausfaelle.md`.

### Zwei Beobachtungen aus dem Redigieren, im Viewer umgesetzt

**Objekt- und Seitennavigation waren nicht auseinanderzuhalten.** Beide Ebenen benutzten
dieselben runden Buttons in derselben Groesse und Farbe; sie unterschieden sich allein durch
das Pfeilzeichen, `«` gegen `‹`. Im Arbeitstempo ist das keine Unterscheidung. Die
Objektebene ist jetzt eine geschlossene, ruhige Pille mit kleineren, randlosen Buttons — man
verlaesst das Objekt selten —, die Seitenebene bleibt der primaere, staerker gezeichnete
Control. Beide Zaehler benennen ausserdem ihre Einheit ("Objekt 12 / 2452", "Seite 3 / 7")
statt zwei nackte Zahlenpaare nebeneinanderzustellen.

**Die Editionsrichtlinien waren beim Redigieren nicht zur Hand.** Die Konventionen stehen
vollstaendig in `annotation-protocol.md`, waren aber nur ueber den Research Vault erreichbar,
also genau dann nicht greifbar, wenn die Frage aufkommt ("wie notiere ich eine Streichung?").
Der Viewer hat jetzt einen Button "§ Richtlinien" (Taste `G`), der §3 des Protokolls neben
den Text blendet: Markup-Tabelle, Streichungen, die Schwelle zwischen `[?]` und `[...]`,
Einfuegungen, Randbemerkungen, Zeilen und Absaetze, dazu der Sprung ins vollstaendige
Protokoll. Im Edit-Modus kommt eine Markup-Leiste ueber das Textfeld, die die Marker
regelkonform setzt: Auswahl in `~~...~~` oder `{...}` einschliessen, `[?]` ohne Leerzeichen
ans vorangehende Wort (und vor die Interpunktion, nicht dahinter), `[Marginalie:]` ans
Seitenende nach einer Leerzeile.

Die Leiste schreibt bewusst nicht per `saveCurrentEdit()` durch — sonst ginge pro Klick ein
Write ins Pipeline-JSON. Sie verhaelt sich wie getippter Text und wird bei `Ctrl+S`,
Seitenwechsel oder Verlassen des Edit-Modus uebernommen.

Damit ist die Frage nach Editionsrichtlinien nicht erledigt, nur zugaenglich gemacht. Faelle,
die beim Redigieren auftauchen und in §3 nicht geregelt sind, gehoeren zurueck ins Protokoll
und von dort ins Panel; ob auch die gruppenspezifischen Regeln aus §4 (Umschlaege, Stempel,
Formularfelder, mehrere Haende) hineingehoeren, ist offen und steht in `plan.md`.

---

## 2026-08-21 — Proto-Edition-Manuskript als Forschungsartefakt eingeordnet

Das im Juli 2026 abgeschlossene Proto-Edition-Manuskript wird nicht eingereicht. `paper/`
bleibt als datierter Forschungsstand mit Evidenzbasis und Entstehungsstufen erhalten. Die
Dateien tragen jetzt einen eindeutigen Archivstatus und bilden keine aktive
Publikationspipeline mehr ab.

Die dauerhaft relevanten Erkenntnisse wurden an drei kanonischen Stellen verankert.
`knowledge/editorial-model.md` buendelt den editionellen Status pro Objekt, die beiden
Betriebskontexte, das Provenienzmodell und die Rolle agentischer Arbeit.
`knowledge/evaluation-results.md` fuehrt die korrekturbasierte CER von 0,962 Prozent samt
Stichproben-, Anker- und Aggregationsgrenzen. `knowledge/page-xml-mets-architecture.md`
dokumentiert die Trennung zwischen haltbaren Ergebnisartefakten, deterministischen Exporten
und veraenderlichen Modell-APIs.

README, Agentenkonfiguration und Viewer-Texte verweisen fuer aktuelle Aussagen auf den
Knowledge-Vault. Die Transparenzsektion dient dem Audit-Trail des Projekts und setzt kein
Paper-Review mehr voraus. [[index]] fuehrt das neue Dokument in Navigation, Lesepfad und
Vorlagenzuordnung. [[plan]] haelt die Entscheidung im datierten Entscheidungslog fest.

Die Verifikation vor dem Viewer-Rebuild umfasste `python -m pytest tests/ pipeline/` mit 18
bestandenen Tests und `node --check docs/app.js` ohne Befund. Der Arbeitsbaum war vor Beginn
sauber und
`origin` zeigte auf `https://github.com/chpollin/szd-htr-ocr-pipeline.git`.

`python pipeline/build_viewer_data.py` erzeugte den Katalog fuer 2.452 Objekte aus fuenf
Sammlungen und den Knowledge-Vault mit 16 Dokumenten. Die Linkpruefung fand zwei historische
Journalverweise, die als tote Wikilinks gerendert wurden. Der fruehere
`verification-by-vision`-Verweis zeigt jetzt auf den konsolidierten Abschnitt in
[[verification-concept]]; das als Link interpretierte Syntaxbeispiel wurde zu Klartext.

---
