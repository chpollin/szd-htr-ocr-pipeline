# SZD-HTR — Textextraktion aus digitalisierten Nachlassfaksimiles

## Projektziel

Aufbau einer HTR/OCR-Pipeline, die aus den digitalisierten Faksimiles des Stefan-Zweig-Nachlasses (Literaturarchiv Salzburg) maschinenlesbaren Text erzeugt. Das Projekt ist ein Teilprojekt von [Stefan Zweig Digital](https://stefanzweig.digital/) und liefert Textdaten als Bewertungsgrundlage für den Expert-in-the-Loop-Workflow im [DIA-XAI](https://github.com/chpollin/dia-xai)-Projekt (PLUS Early Career Grant, ab Mai 2026).

## Repository

- GitHub: https://github.com/chpollin/szd-htr-ocr-pipeline
- Sprache: Python
- Lizenz: MIT

## Quelldaten

Die digitalisierten Faksimiles liegen lokal unter:

```
C:\Users\Chrisi\Documents\PROJECTS\szd-backup\data\
├── lebensdokumente/    ← 143 Objekte
├── korrespondenzen/    ← 1186 Objekte
├── aufsatz/            ← 624 Objekte (Aufsatzablage)
└── facsimiles/         ← 352 Objekte (Werke/Manuskripte)
```

### Struktur pro Objekt

Jedes Objekt hat eine eigene ID (`o_szd.{nummer}`) und folgende Dateien:

```
o_szd.100/
├── metadata.json      ← Metadaten (Titel, Signatur, Sprache, Bildliste, GAMS-URLs)
├── mets.xml           ← METS/MODS-Metadaten (GAMS-kompatibel)
└── images/
    ├── IMG_1.jpg      ← Faksimile-Scans (ca. 4912×7360px, ~1.4MB pro Bild)
    ├── IMG_2.jpg
    └── ...
```

### metadata.json Format

```json
{
  "object_id": "o:szd.100",
  "title": "Agreement Longmans, Green u. Co. Inc., SZ-AAP/L13.23",
  "signature": "SZ-AAP/L13.23",
  "author": "Zweig, Stefan",
  "language": "Englisch",
  "language_code": "en",
  "owner": "Literaturarchiv Salzburg, https://stefanzweig.digital, CC-BY",
  "rights": "CC-BY",
  "images": [
    {"id": "IMG.1", "url": "http://gams.uni-graz.at/o:szd.100/IMG.1", "width": 4912, "height": 7360, "order": 1}
  ],
  "container": "szd.facsimiles.lebensdokumente",
  "download_date": "2025-10-22T14:46:40.318083"
}
```

## Startset: Diverse Lebensdokumente

Wir beginnen mit einem kleinen, bewusst heterogenen Beispielset aus den Lebensdokumenten. Das Set deckt unterschiedliche Objekttypen, Schriftarten (Handschrift, Maschinenschrift, Druck, Formulare) und Sprachen ab, um die Pipeline-Herausforderungen früh zu identifizieren.

### Ausgewählte Objekte (10 Stück, nach Diversität)

| Kategorie | Objekt | Signatur | Typ | Sprache | Bilder | Herausforderung |
|-----------|--------|----------|-----|---------|--------|-----------------|
| Tagebuch | Tagebuch 1918 | SZ-AAP/L6 | Notizbuch | DE | 39 | Handschrift Zweig, Kurrent/Lateinisch gemischt |
| Rechtsdokument | Heimat-Schein | SZ-AP2/L-S7.1 | Nachweis | DE | 2 | Amtsformular, Handschrift + Druck |
| Rechtsdokument | Certificate of Naturalization | SZ-AP2/L-S7.10 | Urkunde | EN | 3 | Englisches Formular, offizieller Druck |
| Rechtsdokument | Bescheid über die Judenvermögensabgabe | SZ-AP2/L-S7.8 | Bescheid | DE | 2 | Amtsdeutsch, Typoskript |
| Finanzen | Scheckheft Österr. Postsparkasse | SZ-SAM/L12 | Scheckheft | DE | ? | Tabellarisch, Formulare |
| Verzeichnis | Briefregister [I] | SZ-AP2/L-S9.1 | Register | DE | 135 | Handschriftliche Listen, viele Seiten |
| Zeugnis | Schulnachricht | SZ-SEF/L2 | Manuskript | DE | 3 | Formular + Handschrift |
| Verlagsvertrag | Verlagsvertrag Grasset | SZ-AAP/L13.1 | Typoskript | FR | ? | Französisch, Maschinenschrift |
| Diverses | Theaterkarte Jeremias 1918 | SZ-SDP/L2 | Eintrittskarte | DE | ? | Gedruckt, kurzer Text |
| Büromaterial | Abwesenheitsnotiz I | SZ-SAM/L2 | Karte | DE | ? | Handschriftlich, kurz |

### Object-IDs ermitteln

Die Object-IDs müssen aus den metadata.json-Dateien anhand der Signatur ermittelt werden. Dazu dieses Script nutzen:

```bash
for d in C:/Users/Chrisi/Documents/PROJECTS/szd-backup/data/lebensdokumente/o_szd.*/metadata.json; do
  id=$(basename $(dirname "$d"))
  python3 -c "import json; d=json.load(open('$d')); print(f'{id} | {d[\"signature\"]} | {d[\"title\"]} | imgs={len(d.get(\"images\",[]))}')"
done | grep -iE "AAP/L6|L-S7.1|L-S7.10|L-S7.8|SAM/L12|L-S9.1|SEF/L2|AAP/L13.1|SDP/L2|SAM/L2"
```

## Pipeline-Architektur

### Phase 1: Grundlegende Pipeline (aktueller Scope)

```
Faksimile (JPG) → Preprocessing → VLM/HTR → Rohtext → Nachverarbeitung → Strukturierter Output
```

#### Schritte

1. **Image Loading**: Bilder aus dem lokalen Backup laden, metadata.json als Kontext
2. **Preprocessing**: Bildqualität prüfen, ggf. Rotation/Crop (viele Bilder sind hochaufgelöst, 4912×7360)
3. **Transkription**: Vision Language Model (VLM) für die eigentliche Texterkennung
   - Primär: Claude Vision API (claude-sonnet-4-20250514 oder claude-haiku-4-5-20251001) — hohe Qualität bei Handschrift
   - Alternative: Gemini, GPT-4o für Vergleich
   - Für jede Seite: Bild + Metadatenkontext (Sprache, Objekttyp) als Prompt
4. **Nachverarbeitung**: Sprachspezifische Korrekturen, Konfidenz-Kategorisierung (sicher/prüfenswert/problematisch)
5. **Output**: JSON mit Transkription pro Seite, Metadaten, Konfidenzlevel

### Phase 2: TEI-Integration (späterer Scope)

- Rohtext → TEI-XML via teiCrafter-Pipeline
- NER auf den transkribierten Texten
- Integration in SZD-Datenmodell (SZDO)

### Phase 3: DIA-XAI-Bewertung (ab Oktober 2026)

- Transkriptionsergebnisse als Input für EIL-Workflow
- EQUALIS-Evaluierung: Wie ändert sich XAI-Qualität bei HTR-Output vs. kuratierte MHDBDB-Daten?
- Expert Review über Web-Interface

## Aktuelle Projektstruktur

```
szd-htr-ocr-pipeline/
├── CLAUDE.md                       ← dieses Dokument
├── README.md
├── Plan.md                         ← Implementierungsplan (Phase 1+2 erledigt)
├── pipeline/
│   ├── prompts/                    ← 8 Gruppen-Prompts + System-Prompt + Kontext-Template
│   ├── test_single.py              ← Einzelobjekt-Transkription (Multi-Collection)
│   ├── tei_context.py              ← TEI-Parser für automatische Kontext-Generierung
│   └── build_viewer_data.py        ← Baut docs/data.json aus Ergebnissen
├── data/
│   ├── szd_lebensdokumente_tei.xml ← TEI-Metadaten (143 Objekte)
│   ├── szd_werke_tei.xml           ← TEI-Metadaten (352 Objekte)
│   ├── szd_aufsatzablage_tei.xml   ← TEI-Metadaten (624 Objekte)
│   └── szd_korrespondenzen_tei.xml ← TEI-Metadaten (723 Einträge)
├── results/test/                   ← Enriched JSON-Ergebnisse (7 Objekte)
├── knowledge/                      ← Research-Vault (Datenanalysen, Journal)
├── docs/
│   ├── index.html                  ← Ergebnisübersicht (GitHub Pages)
│   ├── viewer.html                 ← Faksimile↔Transkription-Viewer
│   └── data.json                   ← Viewer-Daten (generiert)
├── .gitignore
└── .env                            ← API Keys (nicht committet)
```

## Technische Entscheidungen

- **Google Gemini 3.1 Flash Lite** als primäres Transkriptionsmodell (günstig, schnell, multimodal)
- **Dreischichtiges Prompt-System**: System-Prompt → Gruppen-Prompt (A–I) → Objekt-Kontext (aus TEI)
- **Kein Server/Backend** — lokale CLI-Pipeline, Ergebnisse als JSON-Dateien
- **Bilder direkt von GAMS** — kein Download nötig, GAMS-URLs als `<img src>` im Viewer
- **Kategoriale Konfidenz** (high/medium/low) statt numerischer Scores
- **8 Prompt-Gruppen**: A Handschrift, B Typoskript, C Formular, D Kurztext, E Tabellarisch, F Korrekturfahne, H Zeitungsausschnitt, I Korrespondenz

## Verwandte Projekte (als methodische Referenz)

- **zbz-ocr-tei** (https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei): LLM-OCR-Pipeline für gedruckte Texte, 7-Stufen-Architektur. Erfahrungen mit Batch-Verarbeitung, Qualitätsscreening, NER.
- **coOCR HTR** (https://github.com/DigitalHumanitiesCraft/co-ocr-htr): Browser-basiertes HTR-Tool mit VLM-Transkription und Expert-in-the-Loop-Validierung. Epistemische Asymmetrie als Designprinzip.
- **teiCrafter** (https://github.com/DigitalHumanitiesCraft/teiCrafter): TEI-Annotation nach Transkription, nachgelagerte Pipeline-Stufe.
