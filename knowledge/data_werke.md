# Datengrundlage: TEI-Metadaten der Werke (Manuskripte)

**Quelle:** `data/szd_werke_tei.xml` — heruntergeladen von https://stefanzweig.digital/o:szd.werke/TEI_SOURCE (30.03.2026)

## Überblick

Die TEI-Datei enthält **352 `<biblFull>`-Einträge** — jeder beschreibt ein Werkmanuskript aus dem Zweig-Nachlass. 162 davon haben eine PID (= digitalisiert auf GAMS), 190 ohne.

## Klassifikationen (8 Kategorien)

| Klassifikation | Anzahl | mit PID | Anteil |
|---|---|---|---|
| Essays/Reden/Feuilletons | 164 | 75 | 47% |
| Biographien | 86 | 26 | 24% |
| Romane/Erzählungen | 65 | 32 | 18% |
| Bühnenwerke/Filme | 12 | 0 | 3% |
| Werknotizen | 10 | 9 | 3% |
| Autobiographisches | 8 | 5 | 2% |
| Gedichte | 6 | 3 | 2% |
| Übersetzungen | 1 | 0 | <1% |

## Sprachen

| Sprache | Anzahl |
|---|---|
| Deutsch | 304 |
| Englisch | 27 |
| Französisch | 17 |
| Italienisch | 2 |
| Jiddisch | 1 |
| Spanisch | 1 |

## Objekttypen (physische Form)

| Objekttyp | Anzahl | Transkriptions-Relevanz |
|---|---|---|
| **Typoskriptdurchschlag** | 113 | Maschinenschrift, oft blass |
| **Typoskript** | 67 | Maschinenschrift, gut lesbar |
| **Manuskript** | 65 | Handschrift — Hauptherausforderung |
| **Korrekturfahne** | 39+4 | Gedruckter Text mit handschriftlichen Korrekturen |
| **Notizbuch** | 26 | Handschrift, fließender Text, Notizen |
| **Konvolut** | 24 | Gemischte Materialien |
| Sonstige | ~14 | Umschläge, Zeitungsausschnitte, Postkarten etc. |

## Schreiber (Hände)

| Hand | Vorkommen |
|---|---|
| Stefan Zweig | 193 |
| Lotte Zweig | 83 |
| fremde Hand | 53 |
| Richard Friedenthal | 18 |
| Friderike Zweig | 3 |
| Anna Meingast | 3 |

## Vergleich: Lebensdokumente vs. Werke

| Merkmal | Lebensdokumente (143) | Werke (352) |
|---|---|---|
| Hauptkategorie | Verlagsverträge (43%) | Essays (47%) |
| Dominant. Objekttyp | Typoskript/Durchschlag | Typoskript/Durchschlag |
| Handschrift-Anteil | 12 Notizbücher (8%) | 65 Manuskripte + 26 Notizbücher (26%) |
| Besonderheit | Formulare, Urkunden | Korrekturfahnen (43!) |
| Sprache | Mehrsprachiger (FR, EN, IT, ES) | Primär Deutsch (86%) |
| Zweite Hand | Lotte Zweig (19) | Lotte Zweig (83) |

## Neue Prompt-Gruppe: Korrekturfahnen

Die Werke bringen einen neuen Dokumenttyp, den die Lebensdokumente nicht hatten: **Korrekturfahnen** (43 Stück). Das sind gedruckte Texte mit handschriftlichen Korrekturen — eine Mischung aus OCR-nah (gedruckter Grundtext) und HTR (Korrekturen).

## Vorgeschlagene Prototyp-Gruppen für Werke

Die bestehenden Gruppen A–E werden erweitert:

| Gruppe | Objekte (Werke) | Beispiel |
|---|---|---|
| **A: Handschrift** | Manuskripte (65), Notizbücher (26) | Clarissa (o:szd.1877), Magellan (o:szd.270) |
| **B: Maschinenschrift** | Typoskripte (67), Durchschläge (113) | Rausch der Verwandlung (o:szd.268) |
| **F: Korrekturfahne** (umgesetzt) | Korrekturfahnen (43) | Der Bildner (o:szd.287) — getestet, high confidence |
| G: Konvolut (aufgeschoben) | Konvolute (24) | Zu wenige Objekte, zu heterogen — bei Bedarf ergänzen |

## Vorgeschlagene Test-Objekte (Werke)

| Gruppe | Objekt | PID | Typ | Warum |
|---|---|---|---|---|
| A | Clarissa (Notizbuch) | o:szd.1877 | Notizbuch, 154 Blatt | Umfangreich, Handschrift Zweig |
| A | Montaigne (Manuskript) | o:szd.272 | Manuskript, 19 Blatt | Kürzeres Manuskript |
| B | Rausch der Verwandlung | o:szd.268 | Typoskriptdurchschlag | Lotte Zweig (?) als Typist |
| F | Der Bildner (Gedicht) | o:szd.287 | Korrekturfahne | Neuer Typ: Druck + Korrekturen |
| A | Die Welt von Gestern | o:szd.266 | Notizbuch | Autobiographisch, bekanntes Werk |
