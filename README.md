# SZD-HTR-OCR-Pipeline

Textextraktion aus digitalisierten Nachlassfaksimiles des Stefan-Zweig-Nachlasses (Literaturarchiv Salzburg). Teilprojekt von [Stefan Zweig Digital](https://stefanzweig.digital/).

## Ziel

Aufbau einer VLM-basierten HTR/OCR-Pipeline, die aus den digitalisierten Faksimiles des Zweig-Nachlasses maschinenlesbaren Text erzeugt. Die Transkriptionsergebnisse dienen als Bewertungsgrundlage für den Expert-in-the-Loop-Workflow im [DIA-XAI](https://github.com/chpollin/dia-xai)-Projekt.

## Datengrundlage

4 Sammlungen, ~2107 Objekte (im Backup), beschrieben in TEI-XML:

| Sammlung | Objekte | TEI-Quelle |
|---|---|---|
| Lebensdokumente | 143 | [TEI](https://stefanzweig.digital/o:szd.lebensdokumente/TEI_SOURCE) |
| Werke (Manuskripte) | 352 | [TEI](https://stefanzweig.digital/o:szd.werke/TEI_SOURCE) |
| Aufsatzablage | 624 | [TEI](https://stefanzweig.digital/o:szd.aufsatzablage/TEI_SOURCE) |
| Korrespondenzen | 1186 | Backup-Metadaten |

Sprachen: Deutsch (primär), Englisch, Französisch, Italienisch, Spanisch.

## Pipeline-Architektur

Dreischichtiges Prompt-System für VLM-Transkription:

| Schicht | Funktion |
|---|---|
| **System-Prompt** | Rolle, Regeln, JSON-Output (für alle Objekte gleich) |
| **Gruppen-Prompt** | Typspezifische Anweisungen (9 Gruppen, s.u.) |
| **Objekt-Kontext** | Metadaten aus TEI-XML (Sprache, Hand, Instrument, Typ) |

### Prompt-Gruppen

| Gruppe | Objekte | Hauptmerkmal |
|---|---|---|
| A: Handschrift | Tagebücher, Notizbücher, Manuskripte | Zweigs Handschrift, Kurrent |
| B: Maschinenschrift | Typoskripte, Durchschläge | Formaler Text, mehrsprachig |
| C: Formular | Rechtsdokumente, Finanzen | Druck + Handschrift gemischt |
| D: Kurztext | Diverses, Büromaterialien | Wenig Text, heterogen |
| E: Tabellarisch | Verzeichnisse, Kalender | Listen, Register |
| F: Korrekturfahne | Druckfahnen mit Korrekturen | Druck + handschriftl. Korrekturen |
| G: Konvolut | Gemischte Materialien | Heterogene Objekte in einem Konvolut |
| H: Zeitungsausschnitt | Presseausschnitte | Gedruckt, ggf. Fraktur |
| I: Korrespondenz | Briefe, Postkarten | Briefstruktur, Handschrift |

## Status

**~510 / 2107 Objekte** transkribiert (Batch laeuft). Qualitaetssignale v1.2 mit Leerseiten-Klassifikation und Dictionary Word Ratio. Multi-Model-Konsensus-Verifikation (Gemini Flash Lite + Gemini 3 Flash + Claude Judge) in Validierung.

Viewer & Katalog: [chpollin.github.io/szd-htr-ocr-pipeline](https://chpollin.github.io/szd-htr-ocr-pipeline/)

## Projektstruktur

```
├── pipeline/
│   ├── prompts/              ← 9 Gruppen-Prompts + System-Prompt
│   ├── transcribe.py         ← Batch-CLI (Einzel/Sammlung/Alle)
│   ├── verify.py             ← Multi-Model-Konsensus-Verifikation
│   ├── quality_signals.py    ← 8 Qualitaetssignale + Leerseiten + DWR (v1.2)
│   ├── evaluate.py           ← CER/WER-Berechnung
│   ├── quality_report.py     ← Aggregierte Qualitaetsstatistiken
│   ├── tei_context.py        ← TEI-Parser, resolve_group(), format_context()
│   ├── config.py             ← Pfade, API-Key, Sammlungs-Mapping
│   ├── build_viewer_data.py  ← Baut catalog.json + data/{collection}.json
│   └── test_single.py        ← Test-Script (7 Referenz-Objekte)
├── data/                     ← TEI-Metadaten (4 Sammlungen)
├── results/                  ← Transkriptionsergebnisse (enriched JSON)
├── knowledge/                ← Research Vault (Methodik, Datenanalyse, Journal)
└── docs/                     ← GitHub Pages (Single-Page-App)
    ├── index.html            ← Katalog + Viewer
    ├── app.css               ← SZD-Design-System
    ├── app.js                ← Routing, Rendering, Edit, Export
    ├── catalog.json          ← Leichtgewichtige Metadaten
    └── data/                 ← Transkriptionen pro Sammlung
```

## Setup

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY=AIza...    # oder in .env eintragen
```

## Nutzung

```bash
# Einzelnes Objekt transkribieren
python pipeline/transcribe.py o_szd.161 -c lebensdokumente

# Ganze Sammlung
python pipeline/transcribe.py -c lebensdokumente

# Alle 2107 Objekte
python pipeline/transcribe.py --all

# Nur Korrekturfahnen in Werke
python pipeline/transcribe.py -c werke -g korrekturfahne

# Vorschau ohne API-Calls
python pipeline/transcribe.py --all --dry-run

# Viewer-Daten aktualisieren
python pipeline/build_viewer_data.py

# Qualitaetsreport
python pipeline/quality_report.py

# Multi-Model-Konsensus (Verifikation)
python pipeline/verify.py o_szd.100 -c lebensdokumente
python pipeline/verify.py --sample 3 --dry-run

# CER-Berechnung (gegen Referenztranskription)
python pipeline/evaluate.py results/lebensdokumente/o_szd.100_*.json reference.txt
```

## Verwandte Projekte

- [zbz-ocr-tei](https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei) — LLM-OCR-Pipeline für gedruckte Texte
- [coOCR HTR](https://github.com/DigitalHumanitiesCraft/co-ocr-htr) — Browser-basiertes HTR-Tool mit Expert-in-the-Loop
- [teiCrafter](https://github.com/DigitalHumanitiesCraft/teiCrafter) — TEI-Annotation nach Transkription

## Lizenz

MIT
