# SZD-HTR — Implementierungsplan

## Übersicht

Aufbau einer VLM-basierten HTR-Pipeline für den Stefan-Zweig-Nachlass. Zwei Transkriptions-Provider: **Claude Vision API** (primär) und **Gemini 3.1 Flash-Lite** (kostengünstige Alternative für Batch/Vergleich).

---

## Phase 1: Projektstruktur & Setup

### 1.1 Repository-Grundgerüst
- [ ] `pyproject.toml` anlegen (uv, Dependencies: `anthropic`, `google-genai`, `Pillow`, `python-dotenv`)
- [ ] Verzeichnisstruktur erstellen (`src/szd_htr/`, `scripts/`, `data/sample/`, `results/sample/`)
- [ ] `.gitignore` (data/sample/, .env, __pycache__, *.pyc, knowledge/journal.md)
- [ ] `.env.example` mit `ANTHROPIC_API_KEY=` und `GOOGLE_API_KEY=`

### 1.2 Konfiguration
- [ ] `src/szd_htr/config.py` — Pfade, API-Keys (dotenv), Modellkonfiguration für beide Provider
- [ ] Backup-Pfad konfigurierbar: `C:\Users\Chrisi\Documents\PROJECTS\szd-backup\data\`

---

## Phase 2: Datenzugriff

### 2.1 Loader-Modul
- [ ] `src/szd_htr/loader.py` — Objekt laden anhand ID
  - metadata.json lesen
  - Bilderliste erstellen (sortiert nach order)
  - Strukturiertes Objekt zurückgeben (dataclass: `SZDObject`, `SZDImage`)
- [ ] Validierung: Prüfen ob Bilder existieren, Metadaten vollständig

### 2.2 Sample-Selektion
- [ ] `scripts/select_sample.py` — 10 Beispielobjekte anhand Signatur finden
  - Signaturen → Object-IDs auflösen (metadata.json durchsuchen)
  - Nach `data/sample/` kopieren (nicht symlink, für Portabilität)
  - Mapping-Datei `data/sample/manifest.json` erzeugen

### 2.3 Preprocessing
- [ ] `src/szd_htr/preprocess.py` — Bildvorbereitung
  - Größe prüfen, ggf. Downscaling für API-Limits (Claude: 5MB/Bild)
  - Base64-Encoding für API-Calls
  - EXIF-Rotation korrigieren

---

## Phase 3: Transkription

### 3.1 Transkriptions-Modul (Multi-Provider)
- [ ] `src/szd_htr/transcribe.py` — Abstrakte Transkriptions-Schnittstelle
  - `TranscriptionProvider` Protocol/ABC
  - `ClaudeProvider` — Anthropic Vision API (claude-sonnet-4-20250514)
  - `GeminiProvider` — Google Gemini 3.1 Flash-Lite (günstig, schnell, 1M Kontext)
  - Provider per Config/CLI wählbar

### 3.2 Prompt-Engineering
- [ ] System-Prompt für historische Dokumenttranskription entwickeln
  - Sprachkontext (DE/EN/FR) aus Metadaten
  - Objekttyp-spezifische Anweisungen (Handschrift vs. Druck vs. Formular)
  - Kurrent-Hinweise für deutsche Handschriften
  - Instruktionen für Layout-Erhalt (Tabellen, Formulare)

### 3.3 Batch-Verarbeitung
- [ ] Seitenweise Transkription (1 API-Call pro Seite)
- [ ] Rate-Limiting / Retry-Logik
- [ ] Fortschrittsanzeige (tqdm oder simple Logs)

---

## Phase 4: Nachverarbeitung & Output

### 4.1 Postprocessing
- [ ] `src/szd_htr/postprocess.py`
  - Kategoriale Konfidenz: sicher / prüfenswert / problematisch
  - Sprachspezifische Korrekturen (z.B. OCR-typische Fehler)
  - Leerzeichen/Zeilenumbruch-Normalisierung

### 4.2 Output
- [ ] `src/szd_htr/output.py` — Ergebnis-Serialisierung
  - Ein JSON pro Objekt unter `results/sample/{object_id}.json`
  - Format:
    ```json
    {
      "object_id": "o:szd.XXX",
      "title": "...",
      "provider": "claude-sonnet-4|gemini-3.1-flash-lite",
      "timestamp": "2026-03-30T...",
      "pages": [
        {
          "image_id": "IMG.1",
          "transcription": "...",
          "confidence": "sicher|prüfenswert|problematisch"
        }
      ]
    }
    ```

---

## Phase 5: Erster Testlauf

### 5.1 Pipeline-Script
- [ ] `scripts/run_pipeline.py` — CLI-Einstiegspunkt
  - Objekt-ID(s) als Argument
  - Provider wählbar (`--provider claude|gemini`)
  - Ergebnisse nach `results/sample/` schreiben

### 5.2 Testlauf auf einfachen Objekten
- [ ] Theaterkarte Jeremias 1918 (SZ-SDP/L2) — kurzer gedruckter Text
- [ ] Bescheid Judenvermögensabgabe (SZ-AP2/L-S7.8) — Typoskript
- [ ] Certificate of Naturalization (SZ-AP2/L-S7.10) — englisches Formular
- [ ] Ergebnisse mit beiden Providern vergleichen (Claude vs. Gemini)

### 5.3 Ergebnis-Review
- [ ] Qualität manuell bewerten
- [ ] Prompt iterieren basierend auf Ergebnissen
- [ ] Erkenntnisse in `knowledge/` dokumentieren

---

## Phase 6: Dokumentation

- [ ] `README.md` — Projektbeschreibung, Setup, Usage
- [ ] Ergebnisse der ersten Testläufe committen als Referenz

---

## Reihenfolge & Abhängigkeiten

```
1.1 Setup ──→ 1.2 Config ──→ 2.1 Loader ──→ 2.2 Sample ──→ 2.3 Preprocess
                                                                    │
                                                                    ▼
                                              3.1 Transcribe ──→ 3.2 Prompts
                                                                    │
                                                                    ▼
                                              4.1 Postprocess ──→ 4.2 Output
                                                                    │
                                                                    ▼
                                              5.1 Pipeline ──→ 5.2 Testlauf
                                                                    │
                                                                    ▼
                                                              6. README
```

## Technologie-Stack

| Komponente | Technologie |
|-----------|-------------|
| Sprache | Python 3.12+ |
| Package Manager | uv |
| Primäres VLM | Claude Vision (claude-sonnet-4-20250514) |
| Alternatives VLM | Gemini 3.1 Flash-Lite ($0.25/1M input) |
| Bildverarbeitung | Pillow |
| Config | python-dotenv |
| Output | JSON |
