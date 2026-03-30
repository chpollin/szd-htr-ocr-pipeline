# Datengrundlage: Korrespondenzen

**TEI-Quelle:** `data/szd_korrespondenzen_tei.xml` — 723 Einträge, aber NUR als Verzeichnis (keine physischen Beschreibungen, keine PIDs)

**Backup-Quelle:** `szd-backup/data/korrespondenzen/` — **1186 Objekte** mit metadata.json und Bildern

## Situation

Die Korrespondenzen-TEI enthält nur Korrespondenz-Metadaten (`<correspDesc>`) — wer schrieb an wen, wann. Keine physischen Beschreibungen (Schreibinstrument, Objekttyp, Sprache etc.) wie bei Lebensdokumenten und Werken.

Aber: Die 1186 heruntergeladenen Objekte im Backup haben jeweils eine `metadata.json` mit Titel, Sprache, Bildliste und GAMS-URLs. Daraus können wir die Pipeline speisen.

## Beispiel-Objekt (aus Backup)

```json
{
  "object_id": "o:szd.1079",
  "title": "Brief an Max Fleischer vom 22. Mai 1901, SZ-LAS/B3.1",
  "language": "Deutsch",
  "images": [5 Bilder, je 4912×7360px]
}
```

## Charakteristika

- **Briefe** — primär handschriftlich (Zweigs Hand, violette Tinte)
- **1186 Objekte** — die mit Abstand größte Sammlung
- **Keine TEI-Klassifikation** — müssten aus Titeln/metadata.json gruppiert werden
- Typen (aus Titeln ableitbar): Brief, Postkarte, Telegramm, Visitenkarte

## Prompt-Gruppe

| Gruppe | Objekte | Herausforderung |
|---|---|---|
| **I: Korrespondenz** (NEU) | ~1186 | Handschriftliche Briefe, Postkarten — ähnlich Gruppe A, aber Briefkonventionen (Anrede, Datum, Grußformel) |

## Nächste Schritte

1. Stichprobe aus den 1186 Backup-Objekten ziehen (z.B. 10 zufällige)
2. Titel parsen um Dokumenttypen zu erkennen (Brief/Postkarte/Telegramm)
3. Prompt für Korrespondenz entwickeln (Briefstruktur, Anrede, Grußformel)
