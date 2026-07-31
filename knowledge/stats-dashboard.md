---
title: "Statistik-Dashboard"
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
status: active
created: 2026-04-02
updated: 2026-06-10
authors: [Christopher Pollin]
type: spec
related:
  - "[[verification-concept]]"
  - "[[data-overview]]"
tags:
  - visualization
  - quality
---

# Statistik-Dashboard

Dedizierte Statistik-Seite im SZD-HTR Viewer (`#stats`), die aggregierte Qualitaetsmetriken als narrative Informationsvisualisierungen darstellt. Ziel: OCR-Qualitaet akademisch argumentierbar machen.

## 1 Motivation und Perspektive

Text-Chips im Katalog reichen fuer eine wissenschaftliche Qualitaetsbewertung nicht: Verteilungen, Ausreisser und Zusammenhaenge sind erst durch Visualisierungen erkennbar. Mehrere aktuelle Arbeiten argumentieren, dass Standard-OCR-Metriken (CER/WER) fuer historische Dokumente unzureichend sind (Beyene & Dancy 2026; Levchenko 2025) — proxy-basierte Quality Signals und deren Verteilung liefern bessere Einsichten. Perspektive: **Computational Philology / Digital Scholarly Editing** plus Informationsvisualisierung (Yuan et al. 2024). Primaere Nutzer sind DH-Forscher und Archivare, nicht ML-Engineers — Metriken muessen philologisch interpretierbar sein.

## 2 Datenquellen

Alle Visualisierungen werden client-seitig aus `catalog.json` aggregiert (`computeStatsData()`, Single-Pass ueber alle Objekte, kein Backend-Umbau). Jedes der 2.451 transkribierten Objekte (Stand 2026-06-10) traegt quality_signals v1.5 (7 Signale + `page.type`, DWR entfernt), Review-Status und TEI-Metadaten.

## 3 Struktur: 3 Sektionen (Stand Session 26)

Jede Sektion hat Header mit Erklaerung und Quellenangabe, Cards 2-spaltig im Grid.

### Sektion 1: Verifikation

Drei Review-Status (Operator-Entscheidung 2026-06-10): **Mensch-geprueft** (`gt_verified` oder `approved` — gilt als verifiziert, Ground-Truth-faehig), **Agent-geprueft** (`agent_verified`), **Ungeprueft** (kein Review). `needs_review` ist kein Status, sondern Triage-Hinweis „zuerst sichten" innerhalb von Ungeprueft. JSON-Werte unveraendert; die Zusammenfassung passiert in der Anzeige-Schicht (`docs/app.js`).

- **Review-Status** (Donut, 4 Segmente): Mensch-geprueft (Gruen), Agent-geprueft (Blau), Ungeprueft (Grau), Zuerst sichten (Amber als Triage-Akzent). Nur Segmente > 0. Klick auf „Zuerst sichten" → `#catalog?review_status=priority`.
- **Review-Gruende** (horizontaler Balken): Anzahl Signale je Grund, Klick → priorisierter Katalog. Untertitel nennt die Signal-Precision (s. §4).

### Sektion 2: Textcharakteristik

Median der Zeichen pro Inhaltsseite nach Dokumenttyp (horizontaler Balken). Zeigt die strukturelle Vielfalt: Registerblaetter (Gruppe A) enthalten Stichwortnotizen (~50 Zeichen/Seite), Zeitungsausschnitte ~4.800. Quelle: `quality_signals.py` (chars_per_page) → `catalog.json` (verification.avgCharsPerPage).

### Sektion 3: Signalanalyse

Heatmap (HTML-Tabelle): Anteil Objekte pro Gruppe (%), die das jeweilige Signal ausloesen. Gruppenname verlinkt auf den gefilterten Katalog. Quelle: `quality_signals.py` (needs_review_reasons) → `catalog.json` (needsReviewReasons).

### Entfernte Sektionen

Entfernt, weil nicht gegroundet oder transient (Session 22 ff.):

- **Abdeckung/Fortschritt + Seitenkomposition** — Produktions-Tracking, bei 100% sinnlos; Information steht im Katalog
- **DWR-Histogramm** — DWR in v1.5 entfernt (rho=0.05, F1=0.20: misst Prosadichte, nicht Qualitaet)
- **VLM-Konfidenz-Donut** — High/Medium/Low diskriminiert nicht zwischen fehlerfreien und fehlerhaften Transkriptionen
- **Modellkonsensus** — CER zwischen Modellen misst Agreement, nicht Korrektheit; kaum Datenbasis (29 Objekte)

## 4 Metrik-Definitionen

`needs_review` wird nur noch von drei Signalen ausgeloest (v1.5, Precision gegen 62 agent-verifizierte Objekte, Session 21):

| Signal | Definition | Precision |
|---|---|---|
| `page_length_anomaly` | Inhaltsseite < 10% des Medians | 100% |
| `page_image_mismatch` | Seitenzahl ≠ Bildzahl oder > 75% leer | 100% |
| `language_mismatch` | TEI-Sprache vs. erkannte Sprache | 50% |

Nur informativ, **kein** Review-Trigger: `duplicate_pages` (Jaccard > 0.9 bei > 50 Zeichen; 0% Precision — flaggt Korrekturfahnen und Register) und `marker_density` (wertlos — Gemini setzt praktisch keine `[?]`-Marker, signalisiert Unsicherheit nicht).

**CER** = edit_distance(A, B) / max(len(A), len(B)). Referenz sind **menschlich gepruefte Texte**; das LLM-Original bleibt je Seite in `edit_history` erhalten.

## 5 Katalog-UI (verwandt)

- Katalog-Spalte **„Status"** zeigt die drei Review-Status als Badge; ⚠ = zuerst sichten. Frühere Signale- und Seiten-Spalte entfernt; Seitenzahl steht als „N S." in der Typ-Spalte.
- Katalog-Filter als deklaratives Registry (`FILTER_DEFS` in `docs/app.js`): Sammlung, Lieferung (`ingestLabel`, Tooltip aus `config.INGEST_INFO`), Bestandseinheit/Konvolut (nur korrespondenzen + autographen via `config.UNIT_TERMS`; Feld `unit` = Signatur minus letztes Punkt-Segment, `derive_unit()` in `build_viewer_data.py`), Gruppe, Qualitaet (confidence), Status. Ein neuer Filter = ein Registry-Eintrag plus `<select>` in index.html.

## 6 Design-Entscheidungen

- **Chart.js 4.x** (vendored in `docs/lib/`, ~200KB): ausreichend fuer Bar/Donut, D3.js waere Overkill.
- **Client-seitige Aggregation**: `catalog.json` traegt alle noetigen Felder, `computeStatsData()` als Single-Pass.
- **Donut mit eigener `donutOptions()`**: getrennt von `chartOptions()` (keine Achsen).
- **Drill-Down via Hash-Navigation**: Chart-Klick → `#catalog?review_status=priority` bzw. `?group=X`.
- **Heatmap als HTML-Tabelle**: praeziser und zugaenglicher als Canvas, scrollbarer Container fuer schmale Viewports.
- **Kein CER-Dashboard**: Nur ein Bruchteil der Objekte hat CER-Daten — ein CER-zentriertes Dashboard waere eine Fassade.
- **Narrative Sektionen statt flaches Grid**: Header + Beschreibung erklaeren den Argumentationsschritt.

## 7 Literatur

- Beyene, F.S. & Dancy, C.L. (2026). A Survey of OCR Evaluation Methods and Metrics and the Invisibility of Historical Documents. *FAccT 2026*. — CER reicht nicht, strukturelle Metriken noetig fuer historische Dokumente.
- Yuan, J. et al. (2024). Visual Analytics for Machine Learning: A Data Perspective Survey. *IEEE TVCG* 30(12). — Taxonomie fuer Dashboard-Features: Verteilungen statt Aggregate.
- Romein, C.A. et al. (2025). Assessing Advanced Handwritten Text Recognition Engines. *Int. J. Digital Humanities* 7(1), 115-134. — CER-Benchmarking-Methodik mit standardisierter Normalisierung.
- Levchenko, M. (2025). Evaluating LLMs for Historical Document OCR. *LM4DH 2025, RANLP*. — Domaenenspezifische Fehlertypen jenseits CER (Over-Historicization).
- Priestley, M. et al. (2023). A Survey of Data Quality Requirements That Matter in ML Development Pipelines. *JDIQ* 15(2). — Embedded Quality Monitoring entlang der Pipeline.
