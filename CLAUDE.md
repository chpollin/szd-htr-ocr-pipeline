# SZD-HTR — Textextraktion aus digitalisierten Nachlassfaksimiles

## Projektziel

Aufbau einer HTR/OCR-Pipeline, die aus den digitalisierten Faksimiles des Stefan-Zweig-Nachlasses (Literaturarchiv Salzburg) maschinenlesbaren Text erzeugt. Das Projekt ist ein Teilprojekt von [Stefan Zweig Digital](https://stefanzweig.digital/) und liefert Textdaten als Bewertungsgrundlage für den Expert-in-the-Loop-Workflow im [DIA-XAI](https://github.com/chpollin/dia-xai)-Projekt (PLUS Early Career Grant, ab Mai 2026).

## Repository

- GitHub: https://github.com/chpollin/szd-htr
- Sprache: Python
- Lizenz: MIT (oder CC-BY für Daten, klären)

## Quelldaten

Die digitalisierten Faksimiles liegen lokal unter:

```
C:\Users\Chrisi\Documents\PROJECTS\szd-backup\data\
├── lebensdokumente/    ← Fokus dieses Projekts (127 Objekte)
├── korrespondenzen/
├── aufsatz/
└── facsimiles/
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

## Gewünschte Projektstruktur

```
szd-htr/
├── CLAUDE.md                  ← dieses Dokument
├── README.md
├── pyproject.toml             ← Python-Projekt mit uv
├── src/
│   └── szd_htr/
│       ├── __init__.py
│       ├── config.py          ← Pfade, API-Keys, Modellkonfiguration
│       ├── loader.py          ← Laden von Bildern + Metadaten aus Backup
│       ├── transcribe.py      ← VLM-basierte Transkription
│       ├── postprocess.py     ← Nachverarbeitung, Konfidenz
│       └── output.py          ← JSON/TEI Output-Formatierung
├── scripts/
│   ├── select_sample.py       ← Beispielobjekte aus Backup auswählen und kopieren
│   └── run_pipeline.py        ← Pipeline auf ausgewählte Objekte anwenden
├── data/
│   └── sample/                ← Kopie der ausgewählten Beispielobjekte (nicht committet)
├── results/
│   └── sample/                ← Transkriptionsergebnisse (committet als Referenz)
├── .gitignore
└── .env                       ← API Keys (nicht committet)
```

## Technische Entscheidungen

- **Python mit uv** als Package Manager
- **Anthropic SDK** für Claude Vision API (primäres Transkriptionsmodell)
- **Kein Server/Backend** — lokale CLI-Pipeline, Ergebnisse als JSON-Dateien
- **Bilder nicht ins Repo** — nur Metadaten und Ergebnisse committen, Bilder aus lokalem Backup referenzieren
- **Kategoriale Konfidenz** statt numerischer Scores (Erfahrung aus coOCR HTR: LLMs können Transkriptionsqualität nicht zuverlässig numerisch einschätzen)

## Aufgabe: Projekt einrichten

### Schritt 1: Repository-Grundstruktur

- `pyproject.toml` mit Abhängigkeiten: `anthropic`, `Pillow`, `python-dotenv`
- Projektstruktur wie oben anlegen
- `.gitignore`: data/sample/, .env, __pycache__, *.pyc
- `.env.example` mit `ANTHROPIC_API_KEY=`

### Schritt 2: Loader-Modul

- `loader.py`: Funktion zum Laden eines Objekts anhand der ID aus dem Backup-Pfad
  - Liest metadata.json
  - Listet verfügbare Bilder
  - Gibt strukturiertes Objekt zurück (dataclass oder dict)
- `select_sample.py`: Script das die 10 Beispielobjekte anhand ihrer Signaturen aus dem Backup findet und nach `data/sample/` kopiert (symlink oder copy)

### Schritt 3: Transkriptions-Modul

- `transcribe.py`: Nimmt ein Objekt, sendet Bilder an Claude Vision API
  - Prompt enthält: Sprache, Objekttyp, Transkriptionsanweisungen
  - Pro Seite ein API-Call (oder Batch bei wenigen Seiten)
  - Ergebnis: Rohtext pro Seite
- Sinnvoller System-Prompt für die Transkription historischer Dokumente (Zweig-Nachlass, gemischte Schriftarten, mehrsprachig)

### Schritt 4: Erster Testlauf

- Pipeline auf 2-3 der einfacheren Objekte laufen lassen (z.B. Theaterkarte, Bescheid, Certificate of Naturalization)
- Ergebnisse nach `results/sample/` schreiben
- Output-Format: Ein JSON pro Objekt mit Seiten-Transkriptionen

### Schritt 5: README

- Kurzes README mit Projektbeschreibung, Setup-Anleitung, Usage

## Verwandte Projekte (als methodische Referenz)

- **zbz-ocr-tei** (https://github.com/DigitalHumanitiesCraft/zbz-ocr-tei): LLM-OCR-Pipeline für gedruckte Texte, 7-Stufen-Architektur. Erfahrungen mit Batch-Verarbeitung, Qualitätsscreening, NER.
- **coOCR HTR** (https://github.com/DigitalHumanitiesCraft/co-ocr-htr): Browser-basiertes HTR-Tool mit VLM-Transkription und Expert-in-the-Loop-Validierung. Epistemische Asymmetrie als Designprinzip.
- **teiCrafter** (https://github.com/DigitalHumanitiesCraft/teiCrafter): TEI-Annotation nach Transkription, nachgelagerte Pipeline-Stufe.
