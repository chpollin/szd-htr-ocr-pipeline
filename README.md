# SZD-HTR-OCR-Pipeline

Textextraktion aus digitalisierten Nachlassfaksimiles des Stefan-Zweig-Nachlasses (Literaturarchiv Salzburg). Teilprojekt von [Stefan Zweig Digital](https://stefanzweig.digital/).

## Ziel

Aufbau einer VLM-basierten HTR/OCR-Pipeline, die aus den digitalisierten Faksimiles des Zweig-Nachlasses maschinenlesbaren Text erzeugt. Die Transkriptionsergebnisse dienen als Bewertungsgrundlage für den Expert-in-the-Loop-Workflow im [DIA-XAI](https://github.com/chpollin/dia-xai)-Projekt.

## Datengrundlage

4 Sammlungen, 2305+ Objekte, beschrieben in TEI-XML:

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
| **Gruppen-Prompt** | Typspezifische Anweisungen (8 Gruppen, s.u.) |
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
| H: Zeitungsausschnitt | Presseausschnitte | Gedruckt, ggf. Fraktur |
| I: Korrespondenz | Briefe, Postkarten | Briefstruktur, Handschrift |

## Testergebnisse

Getestet mit **Gemini 3.1 Flash Lite** (Preview). **7/7 Objekte: high confidence.**

| Objekt | Sammlung | Gruppe | Sprache |
|---|---|---|---|
| Theaterkarte Jeremias 1918 | Lebensdokumente | D: Kurztext | DE |
| Certified Copy of Marriage | Lebensdokumente | C: Formular | EN |
| Verlagsvertrag Grasset | Lebensdokumente | B: Typoskript | FR |
| Tagebuch 1918 (5 Seiten) | Lebensdokumente | A: Handschrift | DE |
| Der Bildner (Korrekturfahne) | Werke | F: Korrekturfahne | DE |
| Aus der Werkstatt der Dichter | Aufsatzablage | H: Zeitungsausschnitt | DE |
| Brief an Max Fleischer 1901 | Korrespondenzen | I: Korrespondenz | DE |

Viewer: [chpollin.github.io/szd-htr-ocr-pipeline/viewer.html](https://chpollin.github.io/szd-htr-ocr-pipeline/viewer.html)

## Projektstruktur

```
├── pipeline/
│   ├── prompts/           ← 8 Gruppen-Prompts + System-Prompt
│   ├── test_single.py     ← Test-Script (Multi-Collection)
│   ├── tei_context.py     ← TEI-Parser für automatische Kontext-Generierung
│   └── build_viewer_data.py ← Baut docs/data.json aus Ergebnissen
├── data/                  ← TEI-Metadaten (4 Sammlungen)
├── results/test/          ← Transkriptionsergebnisse (enriched JSON)
├── knowledge/             ← Research-Vault
└── docs/                  ← GitHub Pages (Viewer + Übersicht)
```

## Setup

```bash
pip install google-generativeai
export GOOGLE_API_KEY=AIza...
python pipeline/test_single.py --list          # Verfügbare Tests
python pipeline/test_single.py theaterkarte    # Einzeltest
python pipeline/build_viewer_data.py           # Viewer-Daten aktualisieren
```

## Verwandte Projekte

- [zbz-ocr-tei](https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei) — LLM-OCR-Pipeline für gedruckte Texte
- [coOCR HTR](https://github.com/DigitalHumanitiesCraft/co-ocr-htr) — Browser-basiertes HTR-Tool mit Expert-in-the-Loop
- [teiCrafter](https://github.com/DigitalHumanitiesCraft/teiCrafter) — TEI-Annotation nach Transkription

## Lizenz

MIT
