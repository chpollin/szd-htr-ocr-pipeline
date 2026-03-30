# Datengrundlage: TEI-Metadaten der Lebensdokumente

**Quelle:** `data/szd_lebensdokumente_tei.xml` — heruntergeladen von https://stefanzweig.digital/o:szd.lebensdokumente/TEI_SOURCE (30.03.2026)

## Überblick

Die TEI-Datei enthält **143 `<biblFull>`-Einträge** — jeder beschreibt ein Lebensdokument aus dem Stefan-Zweig-Nachlass am Literaturarchiv Salzburg. 120 davon haben eine PID (= sind auf GAMS digitalisiert), 23 haben keine.

## Klassifikationen (10 Kategorien)

| Klassifikation | Anzahl | Anteil |
|---|---|---|
| Verlagsverträge | 61 | 43% |
| Rechtsdokumente | 21 | 15% |
| Diverses | 14 | 10% |
| Büromaterialien | 13 | 9% |
| Tagebücher | 12 | 8% |
| Verzeichnisse | 9 | 6% |
| Kalender | 6 | 4% |
| Finanzen | 4 | 3% |
| Abschiedsbrief | 2 | 1% |
| Adressbücher | 1 | 1% |

## Sprachen

| Sprache | Anzahl |
|---|---|
| Deutsch | 86 |
| Englisch | 23 |
| Französisch | 13 |
| Deutsch (?) | 10 |
| unbekannt | 7 |
| Italienisch | 2 |
| Spanisch | 2 |

Mehrsprachigkeit ist häufig implizit: Verlagsverträge sind oft in der Sprache des Verlagslands, aber mit deutschen Ergänzungen oder Zweigs eigenhändigen Notizen auf Deutsch.

## Objekttypen (physische Form)

| Objekttyp | Anzahl | Transkriptions-Relevanz |
|---|---|---|
| **Typoskript** | 38 | Maschinenschrift — gut lesbar, OCR-nah |
| **Typoskriptdurchschlag** | 36 | Oft blasser, ggf. schwieriger |
| **Notizbuch** | 12 | Handschrift Zweig, Hauptherausforderung |
| **Karte** | 8 | Kurztexte, gemischt |
| **Manuskript** | 7 | Handschrift, variabel |
| **Kalender** | 6 | Druck + handschriftliche Einträge |
| **Register** | 3 | Tabellarisch, handschriftlich |
| Druck | 3 | Gedruckter Text |
| Scheckheft | 2 | Formulare + Handschrift |
| Passkopie | 2 | Formular |
| Urkunde | 2 | Formular + Druck |
| Sonstiges | ~16 | Briefumschläge, Stempel, Konvolute etc. |

## Schreiber (Hände)

| Hand | Vorkommen |
|---|---|
| Stefan Zweig | 98 |
| fremde Hand | 47+3 |
| Lotte Zweig | 19 |
| Ben Huebsch | 5 |
| Eugen Relgis | 5 |
| Halfdan Jespersen | 3 |
| Lotte Altmann | 3 |
| Anna Meingast | 2 |
| Friderike Zweig | 2 |

## Schreibinstrumente

Häufigste Instrumente in den Metadaten:
- **Violette Tinte** — Zweigs Standardinstrument, durchgängig in Tagebüchern und Manuskripten
- **Bleistift** — häufig für Annotationen und Ergänzungen
- **Buntstifte** (blau, rot, grün) — für Markierungen
- **Schwarzes/violettes Farbband** — bei Typoskripten
- **Durchschlagpapier** (schwarz/violett) — bei Typoskriptdurchschlägen

## Physische Beschreibungen

Die TEI-Datei enthält pro Objekt:
- **`<material ana="szdg:WritingMaterial">`** — Papierart (kariert, liniert, Vordruck, etc.)
- **`<material ana="szdg:WritingInstrument">`** — Schreibinstrument
- **`<extent>`** — Blattanzahl, beschriebene Blätter, Beilagen
- **`<measure type="format">`** — physische Maße (z.B. "20x13 cm", "54x38 cm")
- **`<foliation>`** — Paginierungsart
- **`<handDesc>`** — beteiligte Schreiber
- **`<bindingDesc>`** — Einband
- **`<accMat>`** — Beilagen (eingelegte Manuskripte, Karten, etc.)

## Nutzen für die HTR-Pipeline

### 1. Sprachspezifische Prompts
Die Sprachinformation (`<textLang>`) erlaubt es, den Transkriptions-Prompt an die Dokumentsprache anzupassen:
- **Deutsch** → Kurrentschrift-Kenntnisse, ß/ss, Umlaute
- **Französisch** → Akzente, Fachvokabular (Verlagsrecht)
- **Englisch** → Standardenglisch, juristische Formeln
- **Spanisch/Italienisch** → Sonderzeichen

### 2. Objekttyp-spezifische Prompts
Unterschiedliche Objekttypen erfordern unterschiedliche Transkriptionsstrategien:
- **Notizbücher/Tagebücher** → Handschrift, fließender Text, Abkürzungen
- **Typoskripte** → Maschinenschrift, formaler Aufbau, Vertragsklauseln
- **Typoskriptdurchschläge** → wie Typoskript, aber blasser — Hinweis auf niedrigeren Kontrast
- **Formulare** (Urkunden, Schecks, Bescheide) → Druck + handschriftliche Ausfüllung, Tabellenstruktur
- **Register/Verzeichnisse** → tabellarisch, Listenstruktur
- **Kalender** → gedrucktes Raster + kurze handschriftliche Einträge

### 3. Schreiber-Kontext
Die `<handDesc>` verrät, wessen Handschrift zu erwarten ist:
- **Stefan Zweig** — die häufigste Hand, bekannte Schrift (violette Tinte, lateinisch mit Kurrenteinflüssen)
- **Lotte Zweig** — zweithäufigst, vermutlich andere Handschrift
- **Fremde Hand** — oft bei Verträgen (Verleger-Unterschriften etc.)
- Multi-Hand-Dokumente brauchen ggf. Hinweis, dass verschiedene Schriftbilder vorkommen

### 4. Physische Hinweise als Prompt-Kontext
- **Schreibinstrument** → gibt dem VLM Hinweise zur Tintenfarbe und Strichstärke
- **Papierart** → "kariertes Papier" oder "Tabellenvordruck" signalisiert Raster
- **Format/Maße** → sehr große Dokumente (54x38 cm beim Hauptbuch) ggf. anders aufnehmen als Karten (12x8 cm)
- **Beilagen** → eingelegte Manuskripte können auf Scans auftauchen

### 5. Gruppierung für Prototypen

Sinnvolle Prototyp-Gruppen nach Pipeline-Anforderung:

| Gruppe | Objekte | Hauptherausforderung |
|---|---|---|
| **A: Handschrift Zweig** | Tagebücher, Notizbücher (12) | Kurrentschrift, Abkürzungen, fließender Text |
| **B: Maschinenschrift** | Typoskripte (38), Durchschläge (36) | Formaler Text, blasse Durchschläge, mehrsprachig |
| **C: Formulare & Urkunden** | Rechtsdokumente (21), Finanzen (4) | Druck + Handschrift gemischt, tabellarisch |
| **D: Kurztexte** | Diverses (14), Büromaterialien (13) | Heterogen, oft sehr wenig Text |
| **E: Tabellarisch** | Verzeichnisse (9), Kalender (6), Adressbücher (1) | Listen, Register, Datumseinträge |

### 6. Vorschlag: 5 Prototyp-Objekte (je eines pro Gruppe)

| Gruppe | Vorschlag | PID | Warum |
|---|---|---|---|
| A | Tagebuch 1918 (SZ-AAP/L6) | o:szd.72 | Handschrift Zweig, violette Tinte, überschaubar |
| B | Verlagsvertrag Grasset (SZ-AAP/L13.1) | o:szd.78 | Französisches Typoskript |
| C | Certificate of Naturalization oder Heimatschein | o:szd.160 / tbd | Formular + Druck |
| D | Theaterkarte Jeremias (SZ-SDP/L2) | o:szd.161 | Kurztext, einfach |
| E | Briefregister [I] oder Hauptbuch | tbd / o:szd.143 | Tabellarisch, viele Seiten |
