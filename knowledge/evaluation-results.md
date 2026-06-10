---
title: "Evaluationsergebnisse"
aliases: ["CER-Baseline"]
created: 2026-04-02
updated: 2026-06-10
type: analysis
status: stable
related:
  - "[[verification-concept]]"
  - "[[annotation-protocol]]"
  - "[[data-overview]]"
---

# Evaluationsergebnisse: CER-Baseline der SZD-HTR-Pipeline

Empirische Baseline, erhoben **Stand Session 20 (2. April 2026)**. Die Fehlertypologie (§3–4) ist weiterhin gueltig; Objekt- und Review-Zahlen sind historisch (aktueller Stand → `docs/catalog.json`). Einordnung nach heutigem Review-Modell (drei Status, 2026-06-10): „Human Approved" entspricht **Mensch-geprueft** (`gt_verified`/`approved` — verifiziert, Ground-Truth-faehig), „Agent Verified" entspricht **Agent-geprueft**. CER-Referenz sind menschlich gepruefte Texte; das LLM-Original bleibt je Seite in `edit_history` erhalten.

---

## 1. Ueberblick

58 Objekte wurden verifiziert — Faksimile-Bild gegen VLM-Transkription geprueft, Fehler dokumentiert und korrigiert. Alle 9 Prompt-Gruppen abgedeckt.

| Review-Typ | Objekte | Content-Seiten | Zeichen |
|---|---:|---:|---:|
| Human Approved | 14 | 17 | 10.541 |
| Agent Verified (Session 18-19, Batch 1-3) | 20 | 40 | ~27.800 |
| Agent Verified (Session 20, Batch 1-4) | 24 | ~42 | ~18.000 |
| **Gesamt** | **58** | **~99** | **~56.300** |

Seit Session 20 gilt **Edit-Tracking**: alle Korrekturen (Agent + Mensch) werden mit `edit_history` pro Seite gespeichert (Original + Korrektur + Quelle), im Frontend als Side-by-Side-Diff sichtbar.

---

## 2. Methodik: Agent-Verifikation

### Workflow

1. Pro Objekt ein Claude-Sub-Agent (Opus 4.6 mit Vision)
2. Agent liest Seitenbilder aus dem lokalen Backup (`SZD_BACKUP_ROOT`) und die Transkription aus dem Pipeline-JSON
3. Seite fuer Seite Bild-Text-Vergleich, Zeichen fuer Zeichen
4. Fehlerliste mit Zitat, Korrektur, Schweregrad; Fehler werden direkt im JSON korrigiert
5. Review-Metadaten: `status`, `agent_model`, `errors_found`, `estimated_accuracy`, `edited_pages`

### Einschraenkungen

- Claude als Vision-Judge ist **kein Ersatz** fuer menschliches Review — es ist ein Cross-Model-Check (Gemini transkribiert, Claude verifiziert)
- Handschrift-Verifikation ist schwieriger als Drucktext; bei ambiguer Handschrift wird "unsicher" markiert
- Der Agent kann Fehler **uebersehen** (kein exhaustiver Beweis)
- Deshalb steht **Agent-geprueft** im Status-Modell unter **Mensch-geprueft**

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

- **Gedruckter Text** (Korrekturfahne, Typoskript): 99.6–99.9% — nahezu fehlerfrei; Restfehler sind Satzzeichen und Wortgrenzen an Seitenumbruechen.
- **Fraktur** (Zeitungsausschnitt): 99.7–99.8%, aber mit **systematischen Fraktur-Fehlern** (ſ→f: "selbstfeligen" statt "selbstseligen"). Haeufigster und schwerwiegendster Typ — erzeugt falsche, aber existierende Woerter.
- **Handschrift** (inkl. Korrespondenz): 90–99.4%, breites Spektrum je nach Schriftqualitaet. Saubere Handschrift (o_szd.1256): 100%. Schwierige Handschrift mit tabellarischem Layout (o_szd.1475): ~90% — VLM-Linearisierung versagt bei Zuordnung von Betraegen zu Zeilen.
- **Formulare**: 98.5–100%. Gedruckte Felder korrekt, handschriftliche Eintragungen schwieriger (Matrik-Nummern, Unterschriften).

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

**Ursache**: Gemini Flash Lite verwechselt visuell aehnliche Fraktur-Glyphen (ſ/f; ft/st-Ligaturen nahezu identisch). Bei Eigennamen und fremdsprachigen Werktiteln fehlt Kontextwissen. **Haeufigkeit**: ~28 Fehler in ~14.000 Fraktur-Zeichen (~0.2%).

### 4.2 Kurrent-Buchstabenverwechslungen (Schweregrad: hoch)

*Session 19 — 8 Korrespondenzen an Max Fleischer (~1901-1902), alle Kurrent.*

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| h ↔ I | muß ich jetzt **Ihre** schließen | muß ich jetzt **hier** schließen | o_szd.1079 |
| St ↔ H | **Hud. inr.** | **Stud. iur.** | o_szd.1081 |
| r ↔ v | gracioesa **devin** | gracioesa **darin** | o_szd.1081 |
| L ↔ B | **Besten** Gruss | **Liebsten** Gruss | o_szd.1100 |
| Nonsens | **Langentour Kantgewalt** | **Laufenden** | o_szd.1090 |

**Ursache**: Kurrent-Minuskeln weichen systematisch von Antiqua ab; Gemini (primaer auf Antiqua trainiert) erkennt die Unterschiede nicht zuverlaessig. Besonders betroffen: hastige Schrift auf kleinen Postkarten, rote Tinte auf Bildhintergrund. **Haeufigkeit**: 33 Fehler in 8 Objekten (~4/Objekt); Spread 90% (hastig) bis 99.7% (sauber). Groesster Einflussfaktor ist die Schriftqualitaet des Originals, nicht der Prompt.

**Besonders problematisch: Nonsens-Halluzination.** Bei unleserlichem Kurrent erfindet Gemini echte Woerter statt `[?]` zu setzen. Das macht `marker_density` als Quality-Signal **wertlos** — das Modell signalisiert Unsicherheit nicht (Konsequenz: in v1.5 aus `needs_review` entfernt).

### 4.3 Halluziniertes "An" auf Adressseiten (Schweregrad: niedrig)

In 3 von 8 Korrespondenz-Objekten halluziniert Gemini ein "An" vor dem Adressaten auf Postkarten-Adressseiten. **Fix**: Hinweis im Gruppen-Prompt I oder Post-Processing-Regel.

### 4.4 Grossschreibung (Schweregrad: niedrig)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Eigenname | zweig | Zweig | o_szd.127 (3x) |
| Buchtitel | silberne Saiten | Silberne Saiten | o_szd.2296 |
| Substantiv | hingabe | Hingabe | o_szd.2213 |

VLM normalisiert gelegentlich Grossschreibung weg, besonders bei Handschrift und Fraktur.

### 4.5 Fehlende Woerter/Zeichen (Schweregrad: mittel)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Fehlendes Wort | bloß angefuehlt | **nicht** bloß angefuehlt | o_szd.1888 |
| Wortgrenze | erhoben — Hand — | erhoben**e Hand** — | o_szd.1888 |
| Fehlende Anfuehrung | ADEPTS IN SELF | **"**ADEPTS IN SELF | o_szd.102 |

### 4.6 Fremdsprachliche Fehler (Schweregrad: mittel)

| Fehler | Transkription | Korrekt | Objekt |
|---|---|---|---|
| Ital. Vokal | **titole** | **titolo** | o_szd.91 |
| Fehlende Silbe | **conten-te** | **contenen-te** | o_szd.91 |
| Ital. Vokal | **tiretura** | **tiratura** | o_szd.91 |
| Ortsname | **Komotan** | **Komotau** | o_szd.1106 |
| Datum | 30. Juli **1934** | 20. Juli **1934** | o_szd.1383 |

Bei fremdsprachigen Dokumenten fehlt teils Kontextwissen fuer Vokale und Ortsnamen; betrifft v.a. Kohlekopie-Typoskripte (schwacher Kontrast) und seltene Eigennamen.

### 4.7 Truncation: Unvollstaendige Transkriptionen (Schweregrad: kritisch, behoben)

*Entdeckt in Session 20, Root Cause und Fix in Phase A.*

**Root Cause**: `run_sample_batch.py` hatte `--max-images` mit Default 5; das initiale Sample kappte alle Objekte auf 5 Bilder, und `transcribe.py --all` uebersprang sie spaeter (skip-if-exists). Das Chunking war **nicht** der Fehler. `diagnose_truncation.py` fand 97 betroffene Objekte: 24 `max5_truncated`, 18 `vlm_mismatch` (VLM lieferte weniger Seiten), 26 `zero_pages` (API-Fehler). **Fix**: Default auf 0 (kein Limit); `transcribe.py` speichert `metadata.input_image_count_total` zur Erkennung; Re-Transkription mit `--force --chunk-size 20`.

### 4.8 Strukturfehler bei tabellarischen Layouts (Schweregrad: hoch)

| Fehler | Beschreibung | Objekt |
|---|---|---|
| Betraege falscher Zeile zugeordnet | ffr 10.340 auf Aug-Zeile statt Okt-Zeile | o_szd.1475 |

VLMs linearisieren Tabellen von oben nach unten; bei rechtsbuendigen Betraegen und linksbuendigen Beschreibungen verrutscht die Zuordnung. Schwerwiegendster systematischer Fehler im Korpus.

---

## 5. Quality-Signals-Evaluation

### 5.1 DWR (Dictionary Word Ratio) — entfernt (v1.5)

**Befund**: DWR korreliert nicht mit Transkriptionsqualitaet — Spearman rho 0.05 (n.s.), Precision 40%, Recall 13%, F1 0.20. DWR misst "wie viel deutscher Prosatext vorhanden ist": Eigennamen, Fremdsprachen, tabellarische Daten und Kurrent-Formen stehen nicht im 500-Wort-Frequenzlexikon; DWR skaliert primaer mit Wortanzahl. **Entscheidung**: `low_dwr` aus `needs_review_reasons` entfernt (`dwr_score` bleibt informativ). Wirkung: `needs_review` sank von ~37% auf 27% (-66 Objekte).

### 5.2 Signal-Precision (validiert gegen 62 agent-verifizierte Objekte, Session 21)

| Signal | Precision | Status in v1.5 |
|---|---|---|
| `page_image_mismatch` | **100%** (3/3) | Review-Trigger — identifiziert Truncation zuverlaessig |
| `page_length_anomaly` | **100%** (2/2) | Review-Trigger — korreliert mit Truncation und echten Problemen |
| `language_mismatch` | 50% (4/8) | Review-Trigger — misst Metadaten-Inkonsistenz; Zweigs Mehrsprachigkeit erzeugt Rauschen |
| `duplicate_pages` | 0% (0/1) | **aus needs_review entfernt** — flaggt Dokumentstruktur (Korrekturfahnen-Versionen, Register), nicht Fehler; bleibt informatives Feld |
| `marker_density` | — | **aus needs_review entfernt** — Gemini setzt praktisch keine `[?]`-Marker, Signal wertlos |

### 5.3 page_length_anomaly im Briefbestand — Umschlag-False-Positives (v1.6, Session 26)

Die Agent-Triage der 28 geflaggten SZ-AAL-Objekte (2026-06-10, Bild-gegen-Text mit claude-opus-4-8, Report `reports/aal-review-triage.md`) liefert erstmals einen vollstaendigen Goldstandard fuer ein geflaggtes Set — und zeigt, dass die Session-21-Precision (5.2) nicht auf Briefbestaende uebertragbar war:

| | v1.5 (vor Fix) | v1.6 (Umschlag-Ausnahme) |
|---|---|---|
| Geflaggte Objekte im Set | 28 | 4 |
| davon echte Generierungsfehler (Runaway) | 2 | 2 |
| davon legitim kurze Seiten (Umschlag/Ausschnitt/Vermerk) | 22 | 2 |
| Objekt-Precision (echtes Problem / Flag) | 21% (6/28)* | 50% (2/4) |

\* Die 6 zaehlen die 4 strittigen Kursive-Faelle mit — die waren aber aus dem **falschen Grund** geflaggt (Umschlag-Artefakt); ihren Halluzinationsverdacht hat erst der Pruef-Agent gefunden, nicht das Signal. Signal-detektierte echte Probleme: nur die 2 Runaways.

**Ursache**: In Briefkonvoluten ist die kurze Adressseite des Umschlags der Normalfall — gemessen gegen den Median langer Briefseiten faellt sie unter die 10%-Schwelle. **Fix v1.6**: `_is_envelope()` erkennt Umschlag-/Adressseiten an den Seiten-Notes und nimmt sie von Signal 1 aus. Korpusweiter Backfill: 43 Flags entfernt (24 autographen, 16 korrespondenzen, 3 sonstige), 0 neue. Die 2 verbleibenden Kurzseiten-Flags im Set (Zeitungsausschnitt mit Signaturen, Kurzvermerk) sind triage-bestaetigt korrekt transkribiert und als agent_verified markiert.

**Lehre** (ergaenzt die Kalibrierungs-Lehre in [[verification-concept]] §2.3): Signal-Precision ist bestandsabhaengig — ein auf Lebensdokumenten/Werken kalibriertes Signal muss bei einem strukturell neuen Bestand (Briefe mit Umschlaegen) neu validiert werden.

### 5.4 Fraktur-Post-Processing — Evaluation

Prototyp `fraktur_postprocess.py` (pyspellchecker + 13 Fraktur-Verwechslungspaare): fand 2-3 von 11 bekannten Fehlern (o_szd.2217), Precision ~38% (Batch 58 Zeitungsausschnitte). Einzelzeichen-Substitution zu eng, Komposita nicht im Woerterbuch. **Empfehlung**: als Flagging-Tool fuer Agent-Verifikation nutzbar, **nicht fuer Auto-Korrektur** — Mehrzeichen-Fehler ("ihrisch"→"lyrisch"), Eigennamen ("Hayel"→"Hayek") und Komposita bleiben unerkannt.

---

## 6. Implikationen fuer die Pipeline

### Was gut funktioniert

- **Gedruckter Text** (Antiqua): nahezu perfekt, keine systematischen Fehler
- **Saubere Handschrift**: hohe Genauigkeit bei lesbarer Kurrentschrift
- **Seitentyp-Klassifikation**: content/blank/color_chart korrekt (nach Fix der Farbkarten-Erkennung)
- **Chunking**: korrekt fuer grosse Objekte (bis 238 Bilder getestet)
- **Edit-Tracking**: alle Korrekturen mit Original nachvollziehbar (`edit_history`)

### Offene Punkte (Stand Session 20; inzwischen erledigt, wo vermerkt)

1. ~~`duplicate_pages` False-Positives~~ → erledigt: in v1.5 aus `needs_review` entfernt
2. ~~`marker_density` entfernen~~ → erledigt: in v1.5 aus `needs_review` entfernt
3. `language_mismatch`: Mehrsprachigkeit besser handhaben (DE/FR/EN-Mix ist bei Zweig normal)
4. **Tabellarische Layouts**: Gruppe E braucht ggf. speziellen Prompt oder Layout-Analyse-Vorschritt
5. **Grossschreibung**: NER-basierte Eigennamen-Nachverarbeitung koennte systematische Fehler beheben
6. Weitere Verifikation: Fraktur-Fehler (28 dokumentiert) als Material fuer Post-Processing; laufende Agent-/Mensch-Reviews → aktueller Stand im Stats-Dashboard ([[stats-dashboard]])
