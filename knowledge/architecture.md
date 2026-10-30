---
title: "Architecture"
aliases: [page-xml-mets-architecture, security, "METS-Architektur", "PAGE XML", "Ausgabeformate"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Architecture"
  version: 0.4
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/architecture"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-architecture"
status: active
language: de
created: 2026-10-28
updated: 2026-10-28
authors: [Christopher Pollin]
knowledge-sources:
  standards:
    PAGE XML: "https://github.com/PRImA-Research-Lab/PAGE-XML"
    METS: "https://www.loc.gov/standards/mets/"
    MODS: "https://www.loc.gov/standards/mods/"
    TEI: "https://tei-c.org/"
related:
  - "[[specification]]"
  - "[[data]]"
  - "[[page-json-architecture]]"
  - "[[layout-analysis-architecture]]"
  - "[[teicrafter-integration]]"
  - "[[editorial-methodology]]"
---

# Architecture

Die Pipeline ist eine Folge flacher Python-Skripte, die Faksimiles mit TEI-Kontext an ein VLM geben, das Ergebnis als JSON ablegen, regelbasiert anreichern und daraus deterministisch Viewer-Daten und Archivformate erzeugen. Die tragende Entscheidung ist die Trennung zwischen aufgezeichneten Ergebnissen, die ohne Modellzugriff lesbar und exportierbar bleiben, und den veränderlichen Inferenzdiensten. Das Arbeitsformat Page-JSON beschreibt [[page-json-architecture]], die Layout-Stufe [[layout-analysis-architecture]], den Export nach teiCrafter [[teicrafter-integration]].

## Stack

| Komponente | Wahl | Begründung |
|---|---|---|
| Sprache | Python 3.10+ (getestet mit 3.11) | flache Skript-Pipeline ohne Installation |
| VLM (Transkription) | Gemini 3.1 Flash Lite (Preview), `HTR_MODEL` | günstig, schnell, multimodal |
| Layout | Ensemble aus Docling, Surya und Gemini 3 Flash, `HTR_LAYOUT_MODEL` | Regionenerkennung mit VLM-Merger, Details in [[layout-analysis-architecture]] |
| SDK | `google-genai` | offizielles SDK der Transkriptions-API |
| TEI-Parser | `xml.etree.ElementTree` (Standardbibliothek) | eigene, vertrauenswürdige TEI-Dateien |
| Viewer | Single-Page-App aus `index.html`, `app.js`, `app.css` ohne Build-Schritt | statisch auf GitHub Pages auslieferbar |
| Diagramme | Chart.js, vendored unter `docs/lib/` | genügt für Balken und Donut, kein Laufzeit-CDN |
| Wissensdokumente | `markdown` und `pyyaml` zur Build-Zeit | keine Laufzeit-Dependencies im Viewer |

Die Abhängigkeiten sind in `requirements.txt` exakt gepinnt, Testabhängigkeiten in `requirements-dev.txt`. Konfiguration über `.env`:

| Variable | Pflicht | Default | Beschreibung |
|---|---|---|---|
| `GOOGLE_API_KEY` | Ja | | Gemini-API-Key |
| `HTR_MODEL` | Nein | `gemini-3.1-flash-lite-preview` | Modell-ID der Transkription |
| `HTR_LAYOUT_MODEL` | Nein | `gemini-3-flash-preview` | Modell-ID des Layout-Mergers |
| `SZD_BACKUP_ROOT` | Nein | `~/Documents/PROJECTS/szd-backup/data` | Pfad zum lokalen Backup |
| `HTR_BATCH_DELAY` | Nein | `2.0` | Sekunden zwischen API-Calls |

## Komponenten

| Komponente | Zweck | Schnittstelle |
|---|---|---|
| `config.py` | Pfade, API-Key, Sammlungs-Mapping, Konstanten | Modulimport |
| `tei_context.py` | TEI-Parser, `resolve_group()`, `format_context()`, `parse_tei_full_metadata()` | Modulimport |
| `transcribe.py` | Batch-CLI für Einzelobjekt, Sammlung oder Gesamtbestand | CLI, schreibt `results/` |
| `quality_signals.py` | Seitentypen, Signale, `transcription_status`, `needs_review` | Modulimport, Backfill-Skripte |
| `verify.py` | Modellkonsensus aus Flash Lite, Flash und Claude-Judge | CLI, schreibt `*_consensus.json` |
| `evaluate.py` | CER/WER mit Normalisierung nach [[transcription-guidelines]] §5 | Modulimport |
| `generate_gt.py` | Drei-Modell-GT-Pipeline | CLI, schreibt `results/groundtruth/` |
| `layout_analysis.py` | Ensemble-Layoutanalyse | CLI, schreibt `*_layout.json` |
| `export_page_json.py` | Ergebnis, Layout und TEI-Metadaten zu Page-JSON v0.2 | CLI, schreibt `*_page.json` |
| `export_pagexml.py` | Page-JSON zu PAGE XML 2019 | CLI, schreibt `*_page/page_NNN.xml` |
| `export_mets.py` | METS-Container mit MODS und PAGE-XML-Referenzen | CLI, schreibt `*_mets.xml` |
| `export_tei.py`, `marker_enrich.py` | teiCrafter-ladbares TEI mit Marker-Anreicherung | CLI, siehe [[teicrafter-integration]] |
| `build_viewer_data.py` | `catalog.json`, `data/{collection}.json`, `knowledge.json` | CLI, `build()` und `build_knowledge()` |
| `serve.py` | lokaler Dev-Server mit Review-API | HTTP auf 127.0.0.1 |
| `import_reviews.py` | Review-Import aus Frontend-Exporten | CLI |
| `docs/app.js` | Routing, Katalog, Viewer, Bearbeitung, Diff, Statistik, Research Vault | Browser |

Diagnose- und Einmalskripte (`diagnose_truncation.py`, `fraktur_postprocess.py`, `quality_report.py`, `backfill_*.py`, `salvage_raw_results.py`, `run_sample_batch.py`) beschreibt `pipeline/README.md`.

## Datenfluss

```
 Faksimile-Scans (JPG, ~5000x7400px)
 + TEI-XML-Metadaten + Backup-Metadaten
                │
                ▼
 ┌─────────────────────────────────────┐
 │  1. Kontext-Aufloesung              │
 │     tei_context.py                  │
 │     • TEI-XML → Titel, Datum,       │
 │       Sprache, Signatur, Objekttyp  │
 │     • resolve_group() → Prompt-     │
 │       Gruppe A-I (automatisch)      │
 └──────────────┬──────────────────────┘
                ▼
 ┌─────────────────────────────────────┐
 │  2. Prompt-System (4 Schichten)     │
 │     • System-Prompt                 │
 │     • Gruppen-Prompt (1 von 9)      │
 │       ODER Objekt-Prompt (Override) │
 │     • Objekt-Kontext (aus TEI)      │
 └──────────────┬──────────────────────┘
                ▼
 ┌─────────────────────────────────────┐
 │  3. VLM-Transkription               │
 │     Gemini 3.1 Flash Lite (t=0.1)   │
 │     Input: alle Bilder + Prompt     │
 │     Output: JSON {pages[], conf.}   │
 │     • Chunking: >20 Bilder          │
 │     • Exponential Backoff (429)     │
 │     • JSON-Sanitisierung, Salvage   │
 └──────────────┬──────────────────────┘
                ▼
 ┌─────────────────────────────────────┐
 │  4. Enrichment & Quality Signals    │
 │     quality_signals.py              │
 │     • page.type je Seite            │
 │     • Signale, transcription_status │
 │     • needs_review + Gruende        │
 └──────────────┬──────────────────────┘
                ▼
 results/{collection}/{object_id}_{model}.json
                │
        ┌───────┼────────────────────┐
        ▼       ▼                    ▼
   verify.py  layout_analysis.py   build_viewer_data.py
   Konsensus  → *_layout.json      → catalog.json, data/*.json
        │               │          → docs/ Viewer
        │               ▼                    │
        │       export_page_json.py          ▼
        │       → *_page.json          serve.py (lokal)
        │               │              POST /api/approve, /api/edit
        │               ▼              → review, edit_history
        │       export_pagexml.py
        │       → *_page/page_NNN.xml
        │               │
        │               ▼
        │       export_mets.py → *_mets.xml
        └───────┬───────┘
                ▼
        METS/MODS + PAGE XML (Zielformat)
        → GAMS-Reingest, teiCrafter, Transkribus
```

Validierungspunkte liegen nach Stufe 3 (Parser mit Sanitisierung und Salvage vollständiger Seiten vor einer Wiederholungsschleife), nach Stufe 4 (`transcription_status` und `needs_review`) und beim Export (JSON-Schema für Page-JSON). Der Ergebnisaufbau steht in [[specification]] §Ausgabeformate.

### Prompt-System

1. System-Prompt (`pipeline/prompts/system.md`) mit Rolle, diplomatischen Transkriptionsregeln, JSON-Ausgabeformat und Behandlung von Leerseiten.
2. Gruppen-Prompt (`pipeline/prompts/group_*.md`) mit Anweisungen je Dokumenttyp.
3. Objekt-Prompt (`pipeline/prompts/objects/{object_id}.md`, optional), der den Gruppen-Prompt für Spezialfälle ersetzt und automatisch greift, sobald die Datei existiert.
4. Objekt-Kontext, automatisch aus TEI über `tei_context.py`, mit Titel, Signatur, Datum, Sprache und Objekttyp.

| Kürzel | Gruppe | Prompt-Datei |
|---|---|---|
| A | Handschrift | `group_a_handschrift.md` |
| B | Typoskript | `group_b_typoskript.md` |
| C | Formular | `group_c_formular.md` |
| D | Kurztext | `group_d_kurztext.md` |
| E | Tabellarisch | `group_e_tabellarisch.md` |
| F | Korrekturfahne | `group_f_korrekturfahne.md` |
| G | Konvolut | `group_g_konvolut.md` |
| H | Zeitungsausschnitt | `group_h_zeitungsausschnitt.md` |
| I | Korrespondenz | `group_i_korrespondenz.md` |

`resolve_group()` ordnet Korrespondenzen und Briefkonvolute immer I zu, Konvolute G und alle übrigen über einen Entscheidungsbaum aus `objecttyp` und `classification`; Fallback ist Handschrift.

## Externe Modelle und Services

| Modell/Service | Rolle | Provider | Endpunkt |
|---|---|---|---|
| Gemini 3.1 Flash Lite (Preview) | Transkription, Temperatur 0.1 | Google | Gemini API über `google-genai` |
| Gemini 3 Flash (Preview) | Layout-Merger, Konsensus-Modell B | Google | Gemini API |
| Gemini Pro | drittes Modell der GT-Pipeline | Google | Gemini API |
| Claude | Judge im Modellkonsensus, Vision-Agent der Agent-Verifikation | Anthropic | Claude Code, Agent-Läufe |
| Docling, Surya | Layout-Kandidaten | lokal | Python-Pakete |
| GAMS | Bildauslieferung im Viewer | Universität Graz | `https://gams.uni-graz.at/` |

## Archivformat: PAGE XML, MODS und METS

### PAGE XML als Layoutschicht

PAGE XML (Page Analysis and Ground-truth Elements) ist das Standardformat für Layout-Analyse und Texterkennungsergebnisse, entwickelt im PRImA-Projekt der University of Salford, aktuelles Schema 2019-07-15. Es modelliert je Seitenbild eine Hierarchie. Das `Page`-Element referenziert das Rasterbild, darunter liegen Regionen (`TextRegion`, `ImageRegion`, `TableRegion`, `SeparatorRegion`) mit Polygonkoordinaten (`Coords`). In `TextRegion` folgt die Schachtelung `TextLine` → `Word` → `Glyph`, jede Ebene mit eigenen Koordinaten und einem `TextEquiv` für den erkannten Text; Konfidenzwerte lassen sich je Ebene als Attribut führen.

PAGE XML ist das native Format von Transkribus, OCR-D (DFG-Koordinierungsprojekt zur Volltextdigitalisierung historischer Drucke), Kraken/eScriptorium und LAREX. Die Pipeline exportiert PAGE XML je Seite aus den Transkriptionsergebnissen (`export_pagexml.py`).

Das `Metadata`-Element erfasst ausschließlich Prozessmetadaten (Werkzeug, Zeitstempel, Kommentare) und beantwortet die Frage, wie eine Datei erzeugt wurde. Das `custom`-Attribut auf fast allen Elementen nutzt Transkribus für Strukturtagging (`structure {type:heading;}`) oder Schreiberhände auf Regionenebene, als Freitext-Schlüssel-Wert-Paare ohne Schemavalidierung. Deskriptive Metadaten wie Schreiberhand, Schreibstoff, Datierung und Dokumenttyp beschreiben das Dokument als Ganzes und gehören in eine andere Schicht. Ihre Vermischung mit dem Seitenlayout funktioniert bei einzelnen Dokumenten pragmatisch, skaliert aber schlecht und widerspricht der Interoperabilität des Stacks.

### Warum XML für die Archivausgabe

Die Wahl von XML ist eine Ökosystem-Entscheidung mit funktionalen Folgen. PAGE XML hat ein XSD-Schema, gegen das jede Datei validiert werden kann, was beim Austausch von Ground Truth zwischen Institutionen strukturelle Korrektheit maschinell prüfbar macht. XML trennt Attribute (Metadaten über ein Element, etwa `confidence="0.92"`) von Kindknoten (inhaltliche Bestandteile, etwa `TextLine` in `TextRegion`), eine Unterscheidung, die JSON nicht kennt. Namespaces erlauben die Kombination mit METS, ALTO und TEI ohne Namenskollision, und XSLT-Transformationen zwischen PAGE, ALTO und TEI sind direkt möglich. JSON ist kompakter, effizienter zu parsen und für Webanwendungen die natürlichere Wahl. Die Pipeline speichert deshalb intern JSON und transformiert erst für den Export nach PAGE XML.

### METS als Container

METS (Metadata Encoding and Transmission Standard) trägt deskriptive Metadaten (`dmdSec` mit MODS, Dublin Core oder anderen Vokabularen), referenziert Dateien (`fileSec` mit Bildern und PAGE-XML-Dateien) und definiert Struktur (`structMap` als physische und logische Gliederung).

| Schicht | Format | Frage |
|---|---|---|
| Deskriptive Metadaten | MODS (in METS `dmdSec`) | Was ist dieses Dokument? |
| Seitenlayout und OCR | PAGE XML | Was steht wo auf dieser Seite? |
| Container und Struktur | METS | Wie hängt alles zusammen? |

Die Trennung folgt *separation of concerns*. Layout-Ergebnisse lassen sich ohne Metadaten austauschen und umgekehrt.

MODS bietet dedizierte Elemente für die meisten Archivmetadaten: `titleInfo`, `name` mit `role` und Normdaten, `typeOfResource`, `genre`, `originInfo` für Datierung und Ort, `language`, `physicalDescription` für Form und Umfang, `location` für Repository, Signatur und URL, `identifier` für die PID. Schreibstoff und Schreibinstrument stehen in `physicalDescription/note[@type]`, funktional, aber semantisch schwächer als ein eigenes Element.

`parse_tei_full_metadata()` in `tei_context.py` liefert die Felder für MODS:

| TEI-Feld | MODS-Element |
|---|---|
| title | `titleInfo/title` |
| creators (name, role, gnd) | `name/namePart` + `role/roleTerm` + `nameIdentifier` |
| date | `originInfo/dateCreated` |
| language | `language/languageTerm` |
| objecttyp | `genre` |
| extent | `physicalDescription/extent` |
| writing_instrument | `physicalDescription/note[@type="writing_instrument"]` |
| writing_material | `physicalDescription/note[@type="writing_material"]` |
| hands | `physicalDescription/note[@type="script"]` |
| dimensions | `physicalDescription/extent` (zweites) |
| holding (repository, country, settlement) | `location/physicalLocation` + `location/shelfLocator` |
| signature | `location/shelfLocator` |
| provenance | `note[@type="provenance"]` |
| rights | `accessCondition` |

Erweiterbar ist die Architektur um eine zweite `structMap TYPE="LOGICAL"` für inhaltliche Gliederung unabhängig von der Seitenstruktur, um die standardisierten `fileGrp`-Bezeichnungen von OCR-D (`OCR-D-IMG`, `OCR-D-GT-PAGE`, `OCR-D-OCR-PAGE`) und um TEI `msDesc` als ausdrucksstärkere Alternative zu MODS, die sich ebenfalls als `mdWrap` in METS einbetten lässt.

### Bezug zur Pipeline

Page-JSON v0.2 ist das interne Arbeitsformat, METS/MODS mit PAGE XML 2019 das Archiv- und Austauschformat, kompatibel mit GAMS, Transkribus, eScriptorium, OCR-D und teiCrafter. Webbasierte und ML-orientierte Arbeitsschritte arbeiten mit JSON; für das DH-Ökosystem wird nach METS und PAGE XML exportiert. GAMS nutzt METS nativ als Container, der Rückweg ist damit direkt.

### Nachnutzbarkeit und Abhängigkeitsgrenze

Die Ergebnis-JSONs und die daraus erzeugten Austauschformate bleiben ohne Zugriff auf das Transkriptionsmodell lesbar. `export_page_json.py`, `export_pagexml.py`, `export_mets.py` und der teiCrafter-Export transformieren vorhandene Daten deterministisch; Schemavalidierung und Regressionstests prüfen die strukturelle Reproduzierbarkeit dieser Stufen.

Die erneute Erzeugung der Transkriptionen und der VLM-basierten Layoutanalyse setzt die konfigurierten Modell-APIs voraus. Modellversionen können verschwinden oder ihr Verhalten ändern, ein identischer Output ist auch bei gleicher Konfiguration nicht garantiert. Die Architektur trennt deshalb aufgezeichnete Forschungsartefakte von den veränderlichen Inferenzdiensten. Der öffentliche Viewer benötigt keinen schreibenden Projektserver, lädt die Faksimiles jedoch weiterhin aus GAMS. Die fachliche Einordnung dieser Grenze steht in [[editorial-methodology]].

## Sicherheit

Die Anwendung hat zwei Betriebskontexte mit unterschiedlicher Angriffsfläche.

| | GitHub Pages (öffentlich) | Lokaler Dev-Server (`serve.py`) |
|---|---|---|
| Zugang | jeder im Internet | nur localhost (127.0.0.1) |
| Schreibzugriff | keiner (statische Dateien) | POST-Endpoints (approve, edit, rebuild) |
| Authentifizierung | entfällt | keine |
| Daten | `catalog.json`, `data/*.json`, `knowledge.json`, committed und öffentlich | dieselben plus die Pipeline-JSONs in `results/` |
| Bearbeitung | in der Oberfläche deaktiviert über die `isLocal`-Prüfung | aktiv |
| CORS | entfällt (GitHub setzt eigene Header) | beschränkt auf localhost-Origins |

Alle Daten sind öffentliche Archivmaterialien, die bereits auf GAMS publiziert sind. Die ausgelieferten Dateien enthalten keine Nutzerdaten und keine Credentials; API-Keys liegen nur in `.env`, die gitignored ist und nie committet wurde.

Die Maßnahmen an den Vertrauensgrenzen sind eine Content-Security-Policy als Meta-Tag in `docs/index.html`, `escapeHtml()` für jede interpolierte Zeichenkette einschließlich einfacher Anführungszeichen, eine Regex-Whitelist für `object_id` und eine Sammlungs-Whitelist in `_validate_ids()` von `serve.py`, CORS auf localhost-Origins mit Prüfung des Host-Headers (`_check_host()`) und exakt gepinnte Abhängigkeiten. Akzeptierte Restrisiken sind fehlende Schema-Validierung beim CLI-Import von Reviews, eine mögliche Race Condition beim Datei-Backup im Einzelnutzerbetrieb und der `SimpleHTTPRequestHandler` als Dev-Server. Befunde, Prioritäten, Fix-Stand und Prüfmethode der Sicherheitsanalyse vom 2. April 2026 stehen in `reports/security-review-2026-04-02.md`.

## Barrierefreiheit

Der Viewer setzt sichtbare Fokuszustände über `:focus-visible` für Suche, Filter, Tabellenzeilen, Navigation und Bearbeitungsfelder, einen Skip-Link und ARIA-Attribute in `docs/index.html`, wo native Semantik nicht ausreicht. Die Heatmap des Statistik-Dashboards ist eine HTML-Tabelle statt eines Canvas und bleibt damit für Screenreader lesbar. Zentrale Aktionen haben Tastenkürzel (L für das Layout-Overlay, G für das Richtlinien-Panel, Escape für die Rückkehr aus den Wissensansichten). Eine formale Prüfung gegen eine WCAG-Stufe ist nicht dokumentiert.

## Repository-Struktur

```
szd-htr/
├── CLAUDE.md                        ← Action-Layer für Agenten
├── README.md                        ← Projektüberblick, Trust tiers, How this was built
├── requirements.txt                 ← google-genai, python-dotenv, markdown, pyyaml
├── requirements-dev.txt             ← pytest, jsonschema (nur Tests)
├── .env                             ← API-Keys (nicht committet)
├── .github/ISSUE_TEMPLATE/          ← Evaluationshaken zum Antrag (Label `antrag-eval`)
├── paper/                           ← eingefrorenes Forschungsmanuskript vom Juli 2026
├── reports/                         ← datierte Mess-, Prüf- und Befundberichte
├── tests/                           ← pytest: Schema, Trust tiers, Salvage, Wissens-Aliase
├── schemas/                         ← JSON-Schemas für Page-JSON und Layout
├── pipeline/                        ← Skripte und Prompts, Details in pipeline/README.md
│   └── prompts/                     ← System-, Gruppen-, Layout- und Objekt-Prompts
├── data/                            ← TEI-XML-Metadaten der fünf Sammlungen
├── results/                         ← Pipeline-Ergebnisse, Aufbau in results/README.md
│   └── groundtruth/                 ← GT-Drafts aus dem Drei-Modell-Konsensus
├── docs/                            ← statischer Viewer (GitHub Pages)
│   ├── index.html, app.js, app.css
│   ├── lib/                         ← vendored Chart.js
│   ├── catalog.json                 ← Katalogmetadaten
│   └── data/                        ← Sammlungsdaten, groundtruth.json, knowledge.json
└── knowledge/                       ← Wissensbasis, Einstieg über knowledge/INDEX.md
```

| Ordner | Funktion |
|---|---|
| `knowledge/` | dauerhaft gepflegte Promptotyping Documents |
| `reports/` | datierte Berichte und Snapshots, die nicht fortgeschrieben werden |
| `paper/` | eingefrorenes Forschungsartefakt |
| `results/`, `docs/data/`, `docs/catalog.json` | erzeugte Artefakte der Pipeline |

## Build und Deployment

Lokale Entwicklung läuft über `python pipeline/serve.py` (Port 8000, `--port`, `--rebuild`), der den Viewer ausliefert und die Review-API bereitstellt. `python pipeline/build_viewer_data.py` baut Katalog, Sammlungsdaten und Wissensdaten neu; `build_knowledge()` allein erneuert nur `docs/data/knowledge.json`. GitHub Pages liefert `docs/` bei jedem Push auf `main` aus. Tests laufen mit `python -m pytest tests/ pipeline/` ohne API-Key und ohne Bild-Backup.
