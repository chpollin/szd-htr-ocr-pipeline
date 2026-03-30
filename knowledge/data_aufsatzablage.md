# Datengrundlage: TEI-Metadaten der Aufsatzablage

**Quelle:** `data/szd_aufsatzablage_tei.xml` — heruntergeladen von https://stefanzweig.digital/o:szd.aufsatzablage/TEI_SOURCE (30.03.2026)

## Überblick

**624 Einträge**, alle mit PID (= digitalisiert auf GAMS). Die Aufsatzablage ist Stefan Zweigs persönliche Sammlung von Presseausschnitten, Registern und Arbeitsmaterialien zu seinen eigenen Werken.

## Klassifikationen

| Klassifikation | Anzahl | Anteil |
|---|---|---|
| Zeitungsausschnitte | 317 | 51% |
| Registerblätter | 207 | 33% |
| Typoskripte | 56 | 9% |
| Register | 25 | 4% |
| Manuskripte | 7 | 1% |
| Druckfahnen | 6 | 1% |
| Druckschriften | 3 | <1% |
| Korrekturfahnen | 2 | <1% |
| Separatdruck | 1 | <1% |

## Objekttypen

| Objekttyp | Anzahl |
|---|---|
| Zeitungsausschnitt | 312 |
| Manuskript | 213 |
| Typoskript | 44 |
| Typoskriptdurchschlag | 34 |
| Druckfahne | 6 |
| Korrekturfahne | 4 |

## Sprachen

Primär Deutsch (599), dann Französisch (9), Englisch (6), Italienisch (3).

## Hände

| Hand | Vorkommen |
|---|---|
| Unbekannt | 391 |
| Erwin Rieger | 225 |
| Lotte Zweig | 46 |
| Richard Friedenthal | 24 |
| Stefan Zweig | 24 |

Auffällig: **Erwin Rieger** (Zweigs Sekretär/Mitarbeiter) ist die zweithäufigste Hand — hat offenbar die Registerblätter angelegt.

## Neue Prompt-Gruppen

| Gruppe | Objekte | Herausforderung |
|---|---|---|
| **H: Zeitungsausschnitt** (NEU) | 312 | Gedruckter Text, oft Fraktur, verschiedene Zeitungen, Layouts |
| **E: Tabellarisch** (erweitert) | 207 Registerblätter + 25 Register | Listen, Register, tabellarisch |
| **B: Maschinenschrift** (erweitert) | 44 Typoskripte + 34 Durchschläge | Wie bei Lebensdokumenten |
| **F: Korrekturfahne** (erweitert) | 6 Druckfahnen + 4 Korrekturfahnen | Druck + Korrekturen |

## Besonderheit: Zeitungsausschnitte

Die 312 Zeitungsausschnitte sind ein völlig neuer Dokumenttyp:
- **Gedruckter Text** in verschiedenen Zeitungsschriften (oft Fraktur!)
- Verschiedene Layouts (Spalten, Überschriften)
- Oft mit handschriftlichen Annotationen von Zweig oder Mitarbeitern
- Brauchen einen eigenen Prompt mit Fraktur-Hinweisen
