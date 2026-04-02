---
title: "Evaluationsergebnisse"
aliases: ["CER-Baseline"]
created: 2026-04-02
updated: 2026-04-02
type: analysis
status: stable
related:
  - "[[verification-concept]]"
  - "[[annotation-protocol]]"
  - "[[data-overview]]"
---

# Evaluationsergebnisse: CER-Baseline der SZD-HTR-Pipeline

Stand: Session 20 (2. April 2026)

---

## 1. Ueberblick

58 Objekte wurden verifiziert — Faksimile-Bild gegen VLM-Transkription geprueft, Fehler dokumentiert und korrigiert. Alle 9 Prompt-Gruppen sind abgedeckt.

| Review-Typ | Objekte | Content-Seiten | Zeichen |
|---|---:|---:|---:|
| Human Approved | 14 | 17 | 10.541 |
| Agent Verified (Session 18-19, Batch 1-3) | 20 | 40 | ~27.800 |
| Agent Verified (Session 20, Batch 1-4) | 24 | ~42 | ~18.000 |
| **Gesamt** | **58** | **~99** | **~56.300** |

**Neu in Session 20**: Edit-Tracking eingefuehrt — alle Agent-Korrekturen werden mit `edit_history` pro Seite gespeichert (Original-Text + Korrektur + Quelle), im Frontend als Side-by-Side-Diff sichtbar.

**Human Approved**: Experte prueft Transkription im Frontend-Viewer gegen das Faksimile, korrigiert bei Bedarf, markiert als `approved`.

**Agent Verified**: Claude Code Sub-Agents (Opus 4.6 mit Vision) vergleichen jede Seite Bild-fuer-Bild gegen den Transkriptionstext. Gefundene Fehler werden korrigiert und als `agent_verified` gestempelt (→ [[verification-concept]] §8).

---

## 2. Methodik: Agent-Verifikation

### Workflow

1. Fuer jedes Objekt wird ein Sub-Agent gestartet
2. Der Agent liest alle Seitenbilder aus dem lokalen Backup (`SZD_BACKUP_ROOT`)
3. Der Agent liest die Transkription aus dem Pipeline-JSON
4. Seite fuer Seite: Bild wird gegen Text verglichen, Zeichen fuer Zeichen
5. Ergebnis: Fehlerliste mit Zitat, Korrektur, Schweregrad
6. Fehler werden direkt im JSON korrigiert
7. Review-Metadaten werden geschrieben: `status`, `agent_model`, `errors_found`, `estimated_accuracy`, `edited_pages`

### Einschraenkungen

- Claude als Vision-Judge ist **kein Ersatz** fuer menschliches Expert-Review — es ist ein Cross-Model-Check (Gemini transkribiert, Claude verifiziert)
- Handschrift-Verifikation ist schwieriger als Drucktext — bei ambiguer Handschrift wird "unsicher" markiert
- Der Agent kann Fehler **uebersehen** (kein exhaustiver Beweis)
- Deshalb liegt `agent_verified` im 4-Tier-Modell **unter** `approved`

---

## 3. CER-Ergebnisse nach Prompt-Gruppe

| Gruppe | Objekte | Zeichen | Fehler | Geschaetzte Genauigkeit | Hauptfehlertypen |
|---|---:|---:|---:|---|---|
| Korrekturfahne | 4 | ~13.000 | 4 | 98–99.9% | Fraktur-Grossschreibung, Wortgrenze |
| Typoskript | 6 | ~6.000 | 5 | 92–99.9% | Ital. Vokale (titolo/tiratura), handschr. Interlinear-Korrekturen |
| Zeitungsausschnitt | 5 | ~14.000 | 28 | 97–99.8% | **Fraktur f/s**, Nonsens-Halluzination (Mitbringsel, Democratic Vistas) |
| Formular | 5 | ~2.000 | 4 | 98–100% | Handschrift-Felder, Grossschreibung (County Borough) |
| Konvolut | 2 | ~2.500 | 5 | 93–99.1% | Artikelform, handschr. Korrekturen auf Konvolut-Deckblatt |
| Korrespondenz | 21 | ~6.000 | 42 | 85–100% | Kurrent-Verwechslungen, Nonsens-Halluzination, Grussformeln |
| Handschrift | 9 | ~2.500 | 4 | 95–99.4% | Kurrent complet/couplet, Ausbau/Umbau, Fachbegriffe |
| Kurztext | 8 | ~500 | 1 | 97–100% | Abkuerzung Gegr./Geor. |
| Tabellarisch | 3 | ~1.500 | 4 | 75–99% | Unvollstaendige Seiten, fehlende Eintraege bei Adressbuch |

### Interpretation

**Gedruckter Text** (Korrekturfahne, Typoskript): **99.6–99.9% Genauigkeit**. Das VLM liest sauberen Druck nahezu fehlerfrei. Die wenigen Fehler betreffen fehlende Satzzeichen und Wortgrenzen an Seitenumbruechen.

**Fraktur** (Zeitungsausschnitt): **99.7–99.8%**, aber mit **systematischen Fraktur-Fehlern**. Das lange s (ſ) wird als "f" gelesen: "selbst**f**eligen" statt "selbst**s**eligen", "gerei**st**e" statt "gerei**ft**e". Dies ist der haeufigste und schwerwiegendste Fehlertyp — er erzeugt falsche, aber existierende Woerter.

**Handschrift** (inkl. Korrespondenz): **90–99.4%**. Breites Spektrum je nach Handschriftqualitaet. Saubere Handschrift (z.B. o_szd.1256, Brief an Fleischer): 100%. Schwierige Handschrift mit tabellarischem Layout (o_szd.1475, Tantiemen-Liste): ~90% — hier versagt die VLM-Linearisierung bei Zuordnung von Betraegen zu Zeilen.

**Formulare**: **98.5–100%**. Gedruckte Formularfelder werden korrekt gelesen, handschriftliche Eintragungen sind schwieriger (Matrik-Nummern, Unterschriften).

---

## 4. Fehlertypen-Analyse

### 4.1 Fraktur-spezifische Fehler (Schweregrad: hoch)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Langes s → f | selbst**f**eligen | selbst**s**eligen | o_szd.2213 |
| ft ↔ st | gerei**st**e | gerei**ft**e | o_szd.2213 |
| Fraktur a → Punkt | s**.g**en | s**ag**en | o_szd.2296 |

| Wortfragment halluziniert | Mitge**brine** | Mitbr**ingsel** | o_szd.2217 |
| Eigenname falsch | **Hayel** | **Hayek** | o_szd.2217 |
| Werktitel halluziniert | Demokratie **Lista** | Democratic **Vistas** | o_szd.2217 |
| D/W-Verwechslung | **Denn** sie wirklich | **Wenn** sie wirklich | o_szd.2249 |
| Fehlende Silbe | auf**hetzter** | auf**gehetzter** | o_szd.2249 |

**Ursache**: Gemini Flash Lite verwechselt visuell aehnliche Fraktur-Glyphen. Das lange ſ (Unicode U+017F) sieht dem f aehnlich; die Ligaturen ft und st sind in Fraktur nahezu identisch. Bei Eigennamen und fremdsprachigen Werktiteln (z.B. Whitmans "Democratic Vistas") fehlt dem VLM das Kontextwissen.

**Haeufigkeit**: ~28 Fehler in ~14.000 Fraktur-Zeichen (~0.2%). Hoeher als zuvor geschaetzt, weil Session 20 schwierigere Zeitungsausschnitte einschliesst.

### 4.2 Kurrent-Buchstabenverwechslungen (Schweregrad: hoch)

*Neu in Session 19 — 8 Korrespondenzen an Max Fleischer (~1901-1902), alle Kurrent-Handschrift.*

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| h ↔ I | muß ich jetzt **Ihre** schließen | muß ich jetzt **hier** schließen | o_szd.1079 |
| St ↔ H | **Hud. inr.** | **Stud. iur.** | o_szd.1081 |
| r ↔ v | gracioesa **devin** | gracioesa **darin** | o_szd.1081 |
| L ↔ B | **Besten** Gruss | **Liebsten** Gruss | o_szd.1100 |
| Nonsens | **Langentour Kantgewalt** | **Laufenden** | o_szd.1090 |

**Ursache**: Kurrent-Minuskeln weichen systematisch von Antiqua-Formen ab. Gemini (trainiert primaer auf Antiqua/Drucktext) erkennt die Unterschiede nicht zuverlaessig. Besonders betroffen: hastige Schrift auf kleinen Postkarten, rote Tinte auf Bildhintergrund.

**Haeufigkeit**: 33 Fehler in 8 Objekten (~4 pro Objekt). Genauigkeits-Spread: 90% (hastiger Kurrent) bis 99.7% (sauberer Kurrent). Groesster Einflussfaktor ist nicht der Prompt, sondern die Schriftqualitaet des Originals.

**Besonders problematisch: Nonsens-Halluzination.** Bei unleserlichem Kurrent erfindet Gemini echte Woerter statt `[?]` zu setzen. Dies macht `marker_density` als Quality-Signal wertlos — das Modell signalisiert Unsicherheit nicht.

### 4.3 Halluziniertes "An" auf Adressseiten (Schweregrad: niedrig)

In 3 von 8 Korrespondenz-Objekten halluziniert Gemini ein "An" vor dem Adressaten auf Postkarten-Adressseiten. Auf den Originalen steht kein "An" — die Adresse beginnt direkt mit dem Namen.

**Fix**: Hinweis im Gruppen-Prompt I (Korrespondenz) oder Post-Processing-Regel.

### 4.4 Grossschreibung (Schweregrad: niedrig)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Eigenname | zweig | Zweig | o_szd.127 (3x) |
| Buchtitel | silberne Saiten | Silberne Saiten | o_szd.2296 |
| Substantiv | hingabe | Hingabe | o_szd.2213 |

**Ursache**: VLM normalisiert gelegentlich Grossschreibung weg, besonders bei Handschrift und Fraktur, wo Gross-/Kleinbuchstaben visuell weniger distinkt sind.

### 4.5 Fehlende Woerter/Zeichen (Schweregrad: mittel)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Fehlendes Wort | bloß angefuehlt | **nicht** bloß angefuehlt | o_szd.1888 |
| Wortgrenze | erhoben — Hand — | erhoben**e Hand** — | o_szd.1888 |
| Fehlende Anfuehrung | ADEPTS IN SELF | **"**ADEPTS IN SELF | o_szd.102 |

### 4.6 Fremdsprachliche Fehler (Schweregrad: mittel)

*Neu in Session 20.*

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Ital. Vokal | **titole** | **titolo** | o_szd.91 |
| Fehlende Silbe | **conten-te** | **contenen-te** | o_szd.91 |
| Ital. Vokal | **tiretura** | **tiratura** | o_szd.91 |
| Ortsname | **Komotan** | **Komotau** | o_szd.1106 |
| Datum | 30. Juli **1934** | 20. Juli **1934** | o_szd.1383 |

**Ursache**: Bei fremdsprachigen Dokumenten (Italienisch, Franzoesisch, Englisch) fehlt dem VLM teils das Kontextwissen fuer korrekte Vokale und Ortsnamen. Die Fehler betreffen Kohlekopie-Typoskripte (schwacher Kontrast) und Eigennamen ausserhalb des ueblichen Wortschatzes.

### 4.7 Truncation: Unvollstaendige Transkriptionen (Schweregrad: kritisch)

*Neu in Session 20 — 3 Faelle entdeckt.*

| Objekt | Bilder gesamt | Seiten transkribiert | Fehlende Seiten |
|---|---:|---:|---:|
| o_szd.149 (Bibliographie) | 165 | 5 | ~160 |
| o_szd.141 (Notizbuch Russlandreise) | 84 | 5 | ~79 |
| o_szd.175 (Register der Aufsaetze) | 43 | 5 | ~38 |
| o_szd.174 (Adressbuch) | 122 | 5 | ~117 |

**Ursache**: Grosse Objekte (>40 Bilder) werden unvollstaendig transkribiert — nur die ersten ~5 Seiten erscheinen im Ergebnis. Vermutlich ein Chunking-Problem: Das automatische Chunk-Splitting (>20 Bilder) bricht nach dem ersten Chunk ab oder merged die Folge-Chunks nicht korrekt.

**Fix noetig**: Diese Objekte muessen mit `--force --chunk-size 20` re-transkribiert und die Chunk-Merge-Logik in `transcribe.py` geprueft werden.

### 4.8 Strukturfehler bei tabellarischen Layouts (Schweregrad: hoch)

| Fehler | Beschreibung | Objekt |
|---|---|---|
| Betraege falscher Zeile zugeordnet | ffr 10.340 auf Aug-Zeile statt Okt-Zeile | o_szd.1475 |

**Ursache**: VLMs linearisieren Tabellen von oben nach unten. Wenn Betraege rechtsbuendig und Beschreibungen linksbuendig stehen, kann die Zuordnung verrutschen. Dies ist der schwerwiegendste systematische Fehler im Korpus.

---

## 5. Implikationen fuer die Pipeline

### Was gut funktioniert

- **Gedruckter Text** (Antiqua): Nahezu perfekt, keine systematischen Fehler
- **Saubere Handschrift**: Hohe Genauigkeit bei lesbarer Kurrentschrift
- **Seitentyp-Klassifikation**: content/blank/color_chart korrekt (nach Fix der Farbkarten-Erkennung)

### Wo Verbesserungsbedarf besteht

1. **Fraktur-Texte**: Post-Processing-Schritt fuer bekannte f/s-Verwechslungen erwaegen (Woerterbuch-Abgleich)
2. **Tabellarische Layouts**: Gruppe E (tabellarisch) und Tantiemen-Listen brauchen moeglicherweise einen speziellen Prompt oder Layout-Analyse-Vorschritt
3. **Grossschreibung**: Eigennamen-Erkennung als Nachverarbeitung (NER-basiert) koennte systematische Fehler beheben

### Naechste Schritte

- **Truncation fixen**: 4 grosse Objekte (o_szd.149, o_szd.141, o_szd.175, o_szd.174) re-transkribieren, Chunk-Merge-Logik pruefen
- Weitere Objekte agent-verifizieren — 44 von ~875 verifiziert, ~730 ausstehend
- Prompt-Ablation mit den 18 GT-Objekten (jetzt moeglich, da CER-Baseline steht)
- Fraktur-spezifischen Post-Processing-Schritt evaluieren (28 dokumentierte Fehler als Trainingsmaterial)
- `duplicate_pages` False-Positive fixen (Color-Chart-Seiten ausschliessen)
- DWR-Score gegen Agent-Verifikation validieren (korreliert DWR mit tatsaechlicher Fehlerrate?)
