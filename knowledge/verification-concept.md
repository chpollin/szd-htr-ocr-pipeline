---
title: "Verifikationskonzept"
aliases: ["Verifikationskonzept"]
created: 2026-04-01
updated: 2026-06-10
type: concept
status: stable
related:
  - "[[annotation-protocol]]"
  - "[[evaluation-results]]"
  - "[[data-overview]]"
  - "[[layout-analysis]]"
---

# Verifikationskonzept: Qualitaetsmessung der SZD-HTR-Pipeline

Wie misst und sichert das Projekt die Qualitaet von VLM-Transkriptionen ohne vorab existierende Ground Truth? Das Dokument buendelt die Bausteine: Ground-Truth-Strategie (§1), automatische Qualitaetssignale (§2), Prompt-Wirksamkeit (§3), Cross-Model-Verification (§4), Verification-by-Vision (§5), Viewer-Integration (§6), Modellkonsensus mit Judge (§7) und Agent-Verifikation (§8) — plus den Forschungsstand, der diese Entscheidungen begruendet.

---

## Review-Modell: drei Status (Operator-Entscheidung 2026-06-10)

Das frueher hier beschriebene 4-Tier-Modell (GT ✓ / Geprueft / Agent ✓ / Review noetig) ist zu einem Drei-Status-Modell zusammengefasst:

| Status (Anzeige) | `review.status` im JSON | Bedeutung |
|---|---|---|
| **Mensch-geprueft** | `gt_verified` oder `approved` | Ein Mensch hat jede Seite am Faksimile gegengelesen und bei Bedarf korrigiert. Gilt im Projekt als verifiziert UND als Ground Truth fuer die CER-Berechnung. Approve heisst verbindlich: gegengelesen, nicht ueberflogen. |
| **Agent-geprueft** | `agent_verified` | Claude-Vision-Agent hat Bild und Transkript verglichen (§8). Kann stimmen, ersetzt keine menschliche Pruefung. |
| **Ungeprueft** | kein `review`-Block | Nur Pipeline-Selbsteinschaetzung. |

Wesentliche Punkte:

- **`needs_review` ist kein Status mehr**, sondern ein Triage-Hinweis ("zuerst sichten") innerhalb von Ungeprueft, gespeist aus den Qualitaetssignalen (§2).
- Die gespeicherten `review.status`-Werte sind **unveraendert** (`gt_verified`, `approved`, `agent_verified` existieren weiter); die Zusammenfassung passiert in der Anzeige-Schicht (`docs/app.js`, `isHumanChecked()`/`isAgentChecked()`).
- Beim Editieren bleibt das LLM-Original je Seite in `edit_history` erhalten (`serve.py`, §8.6).

Der Korpus umfasst inzwischen fuenf Sammlungen; neu ist `autographen` (SZ-AAL, 379 Objekte, davon 377 transkribiert; reine Briefkonvolute → Prompt-Gruppe I; Anzeige-Label "Briefkonvolute (SZ-AAL)").

---

## Ausgangslage (historisch, April 2026)

Die VLM-Selbsteinschaetzung erwies sich frueh als wertlos: Bei den ersten 16 Objekten meldete das Modell fast durchgehend "high confidence" — fuer saubere Typoskripte ebenso wie fuer fuenfseitige Kurrent-Handschriften (o_szd.72, Tagebuch 1918). In ca. 57.000 transkribierten Zeichen fanden sich genau ein `[...]`- und ein `[?]`-Marker, obwohl die Prompts explizit Unsicherheitsmarker bei Kurrent-Ambiguitaeten verlangen. Die Vorsichts-Guidance wird ignoriert; strukturelle Guidance (Briefformat) wird befolgt.

Daraus ergaben sich drei Probleme:
1. Keine Ground Truth, um die tatsaechliche Fehlerrate zu messen.
2. Kein funktionierender Mechanismus, um problematische Transkriptionen fuer menschliche Pruefung zu markieren.
3. Unbekannt, ob die Gruppen-Prompts die Qualitaet tatsaechlich verbessern.

Die quality_signals wurden iterativ kalibriert: v1.0 flaggte 63% der Objekte (Session 8, unbrauchbar fuer Triage), v1.4 ~41%, v1.5 ~25–27% (Stand 2026-04-03, 330/1328 Objekte). Parallel entstanden Modellkonsensus-Validierung (§4.7), GT-Pipeline (§7.1) und Agent-Verifikation (§8), die das manuelle GT-Sample (§1) weitgehend ersetzt haben.

---

## 1. Ground Truth

### 1.1 Zweck

Ein verifiziertes Referenz-Sample dient zwei Zwecken:
- **Fehlertypologie**: Welche Fehler macht die Pipeline? (Zeichenverwechslungen, Auslassungen, Halluzinationen, Strukturfehler)
- **Metrische Basislinie**: Wie hoch ist die Fehlerrate, aufgeschluesselt nach Gruppe, Sprache und Schwierigkeitsgrad?

Ohne Basislinie sind Optimierungen (Prompt-Tuning, Bildgroesse) nicht messbar. **Heute gilt:** Als Ground Truth zaehlen menschlich gepruefte Texte (Status Mensch-geprueft); die CER-Baseline steht in [[evaluation-results]].

### 1.2 Sample-Design (historische Planung)

Das urspruenglich geplante manuelle 30-Objekt-Sample (~100–150 Textseiten, alle 9 Prompt-Gruppen mit je 2–3 Objekten, Schwierigkeitsspektrum leicht/mittel/schwer, Sprachen DE/FR/EN) wurde nicht als eigener Arbeitsgang ausgefuehrt. Begruendung der Dimensionierung (bleibt gueltig): CER/WER haengen von der Zeichenmenge ab, nicht von der Objektzahl; der Engpass ist die manuelle Referenztranskription (15–45 Min/Seite). Ersetzt wurde das Design durch Modellkonsensus-Validierung (§4.7) plus 3-Modell-GT-Pipeline (§7.1) plus Expert-Review im Viewer — manuelle Arbeit konzentriert sich seither auf Divergenz-Faelle statt auf Volltranskription.

### 1.3 Fehlertypen

Diplomatische Transkription produziert eine eigene Fehlertaxonomie:

| Fehlertyp | Beschreibung | Beispiel | Schwere |
|---|---|---|---|
| **Zeichenfehler** | Falsches Zeichen an richtiger Position | "n" statt "u", "f" statt "s" (Kurrent) | niedrig (einzeln), hoch (systematisch) |
| **Wortfehler** | Ganzes Wort falsch gelesen | "Eltern" statt "Altern" | mittel |
| **Auslassung** | Text im Faksimile, fehlt in Transkription | Ganze Zeile uebersprungen | hoch |
| **Halluzination** | Text in Transkription, nicht im Faksimile | Erfundene Woerter oder Saetze | sehr hoch |
| **Strukturfehler** | Reihenfolge, Seitenumbruch, Spalten falsch | Spalte 2 vor Spalte 1 | mittel |
| **Markup-Fehler** | Unsicherheitsmarker fehlen oder falsch | Unleserliches Wort ohne [...] | mittel |
| **Duplikat** | Derselbe Text doppelt transkribiert | Seite 1 und 3 identisch | hoch |
| **Anachronismus** | Zeichen aus falscher historischer Periode (Levchenko 2025) | Langes s (ſ) in Zweig-Text | mittel-hoch |

Halluzination, Duplikat und Anachronismus verdienen besondere Aufmerksamkeit: Sie sind bei VLMs bekannte Phaenomene und mit reinen Zeichenmetriken (CER) schlecht erfassbar, weil sie den Text verlaengern statt veraendern.

### 1.4 Evaluationsmetriken

**Primaermetrik CER** = (S + D + I) / N (Substitutionen, Loeschungen, Einfuegungen relativ zur Referenz; Levenshtein auf Zeichenebene). Standardmetrik der HTR-Forschung; <5% gilt als gut, <2% als sehr gut. **Sekundaermetrik WER**: dieselbe Formel auf Wortebene — intuitiver, aber tokenisierungsempfindlich.

Zusatzmetriken fuer diplomatische Transkription: Auslassungsrate (D/N), Halluzinationsrate (I/M), Markup-Praezision und -Recall (nur auswertbar, wenn die Referenz ebenfalls [?]/[...]-Stellen markiert — Teil der Annotationsrichtlinie).

### 1.5 Normalisierung vor der CER-Berechnung

Pipeline-Output und Referenz muessen auf derselben Repraesentationsebene verglichen werden (implementiert in `evaluate.py`):

1. Unicode-Normalisierung (NFC)
2. Whitespace-Normalisierung (Mehrfach-Leerzeichen → eins, Trailing-Whitespace weg)
3. Zeilenumbrueche: `\r\n` → `\n`
4. **Keine** Gross/Kleinschreibungs-Normalisierung (bedeutungstragend)
5. **Keine** Interpunktions-Entfernung (gehoert zur diplomatischen Transkription)

Markup (`[?]`, `[...]`, `~~...~~`, `{...}`) wird fuer die Basis-CER entfernt, fuer Markup-Metriken separat ausgewertet.

### 1.6 CER-Schwellen pro Gruppe

| CER-Bereich | Bewertung | Handlung |
|---|---|---|
| **< 5%** | Sehr gut, Pipeline funktioniert | Batch fortsetzen, quality_signals als Triage |
| **5–15%** | Brauchbar mit Review | Batch fortsetzen, Cross-Model-Verification einplanen |
| **15–30%** | Problematisch | Prompt-Ueberarbeitung, Batch nur mit manuellem Review |
| **> 30%** | Unbrauchbar | Anderes Modell, Preprocessing oder Gruppe ausschliessen |

**Empirische Validierung (Session 18–20):** An 62 verifizierten Objekten (18 human-approved, 44 agent-verified) liegen alle 9 Gruppen im Bereich <5% (gedruckter Text) bis ~10% (schwierige Handschrift/Tabellen). Details → [[evaluation-results]].

---

## Stand der Forschung (April 2026)

### Quellen

| Kuerzel | Referenz | Zugang |
|---|---|---|
| LEV25 | Levchenko (2025): "Evaluating LLMs for Historical Document OCR." arXiv:2510.06743 | Volltext gelesen |
| HUM24 | Humphries et al. (2024): "Unlocking the Archives." arXiv:2411.03340 | Volltext gelesen |
| GUT25 | Gutteridge et al. (2025): "Judge a Book by Its Cover." arXiv:2502.20295 | Volltext gelesen |
| CRO25 | Crosilla, Klic, Colavizza (2025): "Benchmarking LLMs for HTR." J. of Documentation 81(7). arXiv:2503.15195 | Volltext gelesen |
| DIE25 | Diez Garcia et al. (2025): "Evaluating VLMs for HTR." DisTech 2025, Springer | Nur Abstract/Fazit |
| STR22 | Stroebel et al. (2022): "Evaluation of HTR models without Ground Truth Material." LREC 2022 | Abstract/Metriken |
| ZHA25 | Zhang et al. (2025): "Consensus Entropy." arXiv:2504.11101, ICLR 2026 | Abstract/Methode |
| RCO26 | "From Plausibility to Verifiability: Risk-Controlled Generative OCR." arXiv:2603.19790 | Abstract |
| BEY26 | Beyene & Dancy (2026): "A Survey of OCR Evaluation Methods … and the Invisibility of Historical Documents." arXiv:2603.25761 | Abstract/Methodik |
| OCR25 | "OCR-Quality: A Human-Annotated Dataset." arXiv:2510.21774 | Abstract |

### Befund 1: CER-Erwartungswerte

| Quelle | Dokumenttyp | Sprache | Bestes Modell | CER |
|---|---|---|---|---|
| CRO25 | Modern handschriftlich (IAM) | EN | GPT-4o-mini | 1.7% |
| CRO25 | Modern handschriftlich (RIMES) | FR | Claude 3.5 Sonnet | 1.6% |
| LEV25 | 18. Jh. Druck, Zivilschrift | RU | Gemini-2.5-Pro | 3.4% |
| HUM24 | 18./19. Jh. handschriftlich | EN | Claude Sonnet-3.5 | 5.7–7.3% |
| CRO25 | 18. Jh. handschriftlich (LAM) | IT | Claude 3.5 Sonnet | 20.6% |
| CRO25 | 15.–19. Jh. handschriftlich (READ2016) | DE | Claude 3.5 Sonnet | 71.2% |
| CRO25 | 19. Jh. mehrsprachig (ICDAR2017) | DE/FR/IT | Claude 3.5 Sonnet | 41.2% |

**Implikation:** Fuer Typoskripte (B) und Druck (F, H) sind <5% realistisch. Zweigs Handschrift (Mischung aus Latein- und Kurrentelementen, fruehes 20. Jh.) liegt zwischen "modern handschriftlich" und den katastrophalen READ2016-Werten fuer historisches Deutsch. CER daher immer getrennt nach Gruppe und Sprache reporten — ein Aggregatwert ueber den Gesamtbestand waere bedeutungslos.

### Befund 2: Selbstkorrektur funktioniert nicht — Kreuzkorrektur schon

- **HUM24:** Claude korrigiert Transkribus-Output (anderes System, mit Bild): CER 8.0% → 1.8% (−78%).
- **CRO25:** Selbstkorrektur (Modell korrigiert sich selbst) verschlechtert meist drastisch: Claude 3.5 auf IAM 1.75% → 8.55%, auf Bentham 10.97% → 40.87%. Open-Source-Modelle durchgehend schlechter.
- **LEV25:** Korrektur ohne Bild verschlechtert konsistent; mit Bild "re-performen" Modelle OCR statt zu korrigieren.

**Aufloesung:** Kreuzkorrektur (Modell A korrigiert Modell B, mit Quellbild) kann funktionieren; Selbstkorrektur nicht — LLMs generieren neu statt minimal zu editieren. Konsequenz: Ein Korrektur-Durchlauf braucht ein anderes Modell UND das Quellbild. Selbstkorrektur mit demselben Gemini-Modell ist ausdruecklich nicht empfohlen.

### Befund 3: Over-Historicization

LEV25 identifiziert einen Halluzinationstyp: VLMs fuegen archaische Zeichen aus der falschen Periode ein (GPT-4o inseriert in 59% der Dateien kirchenslawische Zeichen in 18.-Jh.-Texte). Metriken: HCPR (Historical Character Preservation Rate) und AIR (Archaic Insertion Rate), im Paper nur deskriptiv definiert. Fuer SZD relevant als Fehlertyp "Anachronismus" (§1.3): Gemini koennte bei Zweig langes s (ſ) oder archaische Ligaturen einfuegen. Bei den ersten 16 Objekten nicht beobachtet; Risikogruppe sind Fraktur-Texte und historische Handschrift.

### Befund 4: Kontext verbessert Multi-Page-Transkription

GUT25: OCR-Output des Gesamtdokuments plus nur das Bild der ersten Seite verbessert Folgeseiten erheblich (gpt-4o-mini: CER 0.037 → 0.017). Der Effekt kommt von dokumentspezifischem Kontext (Schriftbild, Layout, Fehlerpatterns), nicht von Domaenenwissen. Bemerkenswert: gpt-4o-mini uebertrifft gpt-4o haeufig — "leistungsfaehiger" heisst nicht "besser fuer HTR" (staerkere Modelle aendern zu viel).

### Befund 5: GT-freie Qualitaetsschaetzung ist moeglich

STR22: Proxy-Metriken ohne Ground Truth — Dictionary Word Ratio, Token Ratio, Pseudo-Perplexity (MLM-basiert) — korrelieren mit CER. PPPL ist sprachunabhaengig, erfordert aber eine zusaetzliche Modell-Abhaengigkeit. (Exakte Korrelationswerte nicht verifizierbar, PDF-Zugang fehlgeschlagen.) Im Projekt blieb PPPL eine nicht gezogene Eskalationsstufe; die DWR wurde implementiert und empirisch verworfen (§2).

### Befund 6: Proprietaere VLMs vs. spezialisierte HTR-Systeme

CRO25 und DIE25: Auf modernen Handschriften schlagen VLMs Transkribus (1.7% vs. 9.1% CER auf IAM); auf historischem Deutsch liegt Transkribus deutlich vorn. Falls kuenftig andere Modelle getestet werden, gehoert Transkribus als Baseline dazu.

### Befund 7: Multi-VLM-Konsensus als GT-freier Qualitaetsproxy

- **ZHA25 (ICLR 2026):** Consensus Entropy — korrekte Transkriptionen konvergieren im Output-Space, Fehler divergieren. 15.2% hoehere F1 als VLM-as-Judge, Eskalation nur bei 7.3% der Inputs noetig; training-free.
- **RCO26:** Accept/Abstain-Framework — Cross-View-Stabilitaet als auditierbarer Deployment-Vertrag.
- **BEY26:** Unsupervised Evaluation fuer historische Digitalisate (Semantic Coherence, Region Entropy Divergence, Textual Redundancy).

**Implikation:** Der 3-Modell-Konsensus (Flash Lite + Flash + Judge) ist wissenschaftlich fundiert: Bei hohem Agreement kann die Transkription als automatisch generiertes GT akzeptiert werden (Ensemble Agreement Error Rate ~2–6% laut LLM-Generated-GT-Literatur); Divergenz-Faelle gehen in den manuellen Review. Das reduziert den manuellen GT-Aufwand drastisch. Diese Behauptung wurde am eigenen Corpus validiert (§7.1).

### 7.1 Empirische Umsetzung: GT-Pipeline (Session 14)

Implementiert in `pipeline/generate_gt.py`:
- Modell A: Gemini 3.1 Flash Lite (existierende Transkription)
- Modell B: Gemini 3 Flash (aus Modellkonsensus-Verifikation, `verify.py`)
- Modell C: Gemini 3.1 Pro (staerkstes Modell)
- Expert: Mensch im Frontend (GT-Review-Modus mit 3-Varianten-Ansicht, Approve-Workflow)

Merge-Logik pro Seite: alle 3 paarweise CER < 2% → `consensus_3of3`; bestes Paar CER < 5% → `majority_2of3` (staerkeres Modell gewaehlt); sonst `pro_only` (Pro-Version als Draft).

**Ergebnis (18 GT-Objekte, 46 Content-Seiten):**

| Merge-Typ | Seiten | Anteil |
|---|---|---|
| consensus_3of3 | 15 | 33% |
| majority_2of3 | 20 | 43% |
| pro_only | 11 | 24% |

76% der Content-Seiten haben mindestens 2/3-Uebereinstimmung; der Expert-Review konzentriert sich auf die pro_only-Seiten. Kosten gesamt inkl. Flash-Konsensus: ca. $8–12.

---

## 2. Konfidenz-Ersatz: quality_signals

### 2.1 Problem

Das `confidence`-Feld ("high"/"medium"/"low") ist eine VLM-Selbsteinschaetzung aus demselben API-Call wie die Transkription — empirisch ohne Informationsgehalt (fast alles "high"). Auch die Inline-Marker taugen nicht: Gemini setzt fast nie `[?]`/`[...]`, sondern **erfindet Woerter statt Marker zu setzen** (Nonsens-Halluzination). Niedrige Marker-Dichte heisst nicht "gut", sondern "uninformativ".

Ersatz: automatisch berechenbare Textstatistik-Signale, nach der Transkription ohne weiteren API-Call berechnet (`quality_signals.py`). Sie messen keine Korrektheit, sondern priorisieren menschlichen Review-Aufwand (Triage "zuerst sichten" innerhalb des Status Ungeprueft).

### 2.2 Signalkatalog (v1.6, Stand des Codes)

`quality_signals.py` klassifiziert zunaechst jede Seite (`page.type`: `content`/`blank`/`color_chart`, aus Notes + Textlaenge) und ergaenzt fehlende Seiten (`_fill_missing_pages()`: VLM-Seitenzaehlung wird auf die Bildanzahl synchronisiert, Luecken als Leerseiten aufgefuellt — behebt die Seiten-Bild-Desynchronisation, 41 Objekte backfilled). Signale rechnen nur auf Content-Seiten, wo sinnvoll.

| Signal | Berechnung (v1.6) | Rolle | Empirische Precision* |
|---|---|---|---|
| `page_length_anomaly` | Content-Seite mit 0 < Zeichen < 10% des Medians; Umschlag-/Adressseiten ausgenommen (Notes-Erkennung, v1.6) | → needs_review | 100% (2/2) auf Session-21-Set; im Brief-Set SZ-AAL waren 7/28 Flags Umschlag-False-Positives (Agent-Triage 2026-06-10) |
| `page_image_mismatch` | `n_pages != n_images` ODER >75% der Content-Seiten leer | → needs_review | 100% (3/3) |
| `language_mismatch` | Stoppwort-Heuristik (Top-20 DE/FR/EN) vs. TEI-Sprache; nur bei ≥50 Woertern und klarer Erkennung | → needs_review | 50% (4/8) — misst eher Metadaten-Inkonsistenz |
| `duplicate_page_pairs` | Jaccard > 0.9 auf Wortmengen, beide Content-Seiten > 50 Zeichen | nur informativ | 0% (0/1) — flaggt Korrekturfahnen (zwei Fassungen derselben Fahne) und Register; zudem False-Positives bei Color-Chart-Doppelfotografie |
| `marker_density` | ([?] + [...]) / Woerter | nur informativ | wertlos — Gemini setzt fast keine Marker |
| DWR (`dwr_score`) | Anteil Woerter in Frequenzliste (~500 Woerter DE/FR/EN) | **entfernt in v1.5** | Spearman rho=0.05, Precision 40%, Recall 13%, F1=0.20 — misst Prosadichte, nicht Qualitaet (Eigennamen, Fremdsprachen, Tabellen verzerren) |
| `group_text_density` | Z-Score der Textdichte innerhalb der Gruppe | **nie implementiert** | — |

\* Evaluation gegen 62 agent-verifizierte Objekte (Session 21).

`needs_review` ist die Disjunktion der drei aktiven Kriterien; `needs_review_reasons` listet die Ausloeser. Alle Felder (inkl. Zaehlwerte, `page_types`, `chars_per_page`, Sprachfelder) stehen im Ergebnis-JSON unter `quality_signals` — massgeblich ist der Code, nicht eine Schema-Kopie hier.

### 2.3 Kalibrierungsgeschichte

| Version | Aenderung | needs_review-Rate |
|---|---|---|
| v1.0 (Session 8) | Erstfassung, 6 Signale | 63% (10/16) — unbrauchbar; Hauptursache: `page_image_mismatch` feuerte bei jedem Objekt mit Leerseiten (im SZD-Nachlass der Normalfall) |
| v1.2 | Leerseiten-Klassifikation (`page.type`), DWR integriert | — |
| v1.4 (Session 14) | Duplikat-Mindestlaenge 200 → 50 Zeichen (erkennt Seiten-Halluzination) | ~41% |
| v1.5 (Session 22) | DWR entfernt, `marker_density` und `duplicate_pages` aus needs_review entfernt, Anomalie-Schwelle 20% → 10% des Medians, Sprachsignal-Guards | ~25–27% (330/1328) |
| v1.6 (Session 26) | Umschlag-/Adressseiten von `page_length_anomaly` ausgenommen (legitim kurz; in Briefbestaenden Haupt-False-Positive: kurze Adressseite gegen Median langer Briefseiten) | 43 Flags weniger ueber alle Sammlungen, kein neues |

Lehre: Schwellenwerte ohne empirische Kalibrierung sind zu aggressiv; jedes Signal muss gegen verifizierte Objekte auf Precision geprueft werden, bevor es Review-Aufwand erzeugen darf.

### 2.4 GT-freie Qualitaetsschaetzung: Grenzen

Alle GT-freien Ansaetze (heuristische Signale, Pseudo-Perplexity, Cross-Model-Agreement) messen *Plausibilitaet* oder *Konsistenz*, nicht *Korrektheit*. Ein fluessig lesbarer Text kann trotzdem falsch gelesen sein; plausible Halluzinationen erkennt keiner dieser Ansaetze zuverlaessig. Sie ergaenzen die Ground-Truth-Evaluation, ersetzen sie nicht. Pseudo-Perplexity (STR22) bleibt eine moegliche Eskalationsstufe, falls die einfachen Signale nicht ausreichen — bisher nicht noetig.

---

## 3. Prompt-Wirksamkeit (offenes Experiment)

Das geschichtete Prompt-System (System → Gruppe bzw. Objekt-Override → Objekt-Kontext aus TEI) ist die zentrale Designentscheidung der Pipeline. Ungeklaert ist, ob die Gruppen-Prompts (9 Dateien) messbar besser sind als ein generischer System-Prompt — oder totes Gewicht. Plausibel ist beides: Kurrent-Verwechslungshinweise koennten gezielt Fehler reduzieren; moderne VLMs koennten sie aber auch redundant machen (Overpriming-Risiko). Empirisch steht fest (Session 8): Vorsichts-Guidance (Marker setzen) wird ignoriert, strukturelle Guidance (Briefformat) wird befolgt.

**Versuchsaufbau (geplant, nicht ausgefuehrt):** Gepaarter Vergleich — jedes GT-Objekt dreimal transkribieren (V1 nur System-Prompt, V2 + Gruppen-Prompt, V3 + Objekt-Kontext), CER-Differenzen pro Objekt und Gruppe auswerten. Der gepaarte Vergleich eliminiert die Objektvarianz. Kosten: ~90 API-Calls (<3 USD). Setzt verlaessliche Referenztexte voraus — mit dem wachsenden Bestand an Mensch-geprueften Objekten inzwischen gegeben. Konsequenzen je nach Befund: Gruppen-Prompts behalten, vereinfachen oder streichen; TEI-Kontext kann auch schaden (Halluzinationen durch zu viel Kontext).

---

## 4. Cross-Model-Verification

### 4.1 Ansaetze

Kann ein zweites VLM Qualitaet verbessern oder problematische Stellen finden — ohne manuelles GT? Die Literatur (Befund 2) sagt: Kreuzkorrektur mit Bild ja, Selbstkorrektur nein.

- **Ansatz A — unabhaengige Doppeltranskription (Agreement):** Beide Modelle transkribieren unabhaengig; Uebereinstimmung = hohes Vertrauen, Abweichung = lokalisierter Pruefbedarf. Parallelisierbar, methodisch sauber, liefert automatisch einen Diff. Risiko: gemeinsamer systematischer Bias bleibt unentdeckt.
- **Ansatz B — heterogene Korrektur (Humphries):** Modell B erhaelt Bild + Transkription von A und korrigiert. Direkter, aber sequentiell, und mit Levchenkos "Re-Generation statt Korrektur"-Risiko.

**Gewaehlte Strategie: Agreement-First** (Ansatz A auf breiter Front, implementiert als Modellkonsensus in `verify.py`); Ansatz B allenfalls selektiv fuer auffaellige Objekte, und nur wenn GT-Daten zeigen, dass er die CER tatsaechlich verbessert.

Historische Anmerkung: Urspruenglich war Claude Sonnet als Zweitmodell empfohlen (maximale Anbieter-Diversitaet). Implementiert wurde Gemini 3 Flash (`VERIFY_MODEL` in `verify.py`) — guenstiger, derselbe Anbieter; die Diversitaet kommt stattdessen durch den Claude-Judge (§7) und die Agent-Verifikation (§8) herein.

### 4.2 Agreement-Interpretation

Agreement wird als CER zwischen den Modellen (nicht gegen GT) gemessen: <3% hohe Uebereinstimmung, 3–10% moderate Abweichung (Review empfohlen), >10% starke Abweichung (manuelle Pruefung). **Agreement ist notwendig, nicht hinreichend:** Zwei Modelle koennen sich auf denselben Fehler einigen, besonders bei systematischen Kurrent-Biases.

### 4.3 Empirische Ergebnisse: Modellkonsensus-Validierung (Session 14)

27 Objekte, stratifiziert (3 pro Gruppe), via `verify.py --sample 3 --force`. Modell A: Gemini 3.1 Flash Lite, Modell B: Gemini 3 Flash. Metriken: `effective_cer` (Minimum aus ordered/orderless CER) + `word_overlap` (Jaccard auf Wortmengen, order-invariant).

**4-Tier-Klassifikation (so im Code, `verify.py`):**

| Kategorie | Kriterium | Anzahl | Anteil |
|---|---|---|---|
| consensus_verified | effective_cer < 3% ODER (word_overlap ≥ 95% UND cer < 10%) | 7 | 26% |
| consensus_moderate | effective_cer < 10% ODER word_overlap ≥ 90% | 9 | 33% |
| consensus_review | word_overlap ≥ 75% | 4 | 15% |
| consensus_divergent | Rest | 7 | 26% |

**Nach Gruppe:** Korrekturfahne 3/3 verified (<1% CER — gedruckter Text ist geloest); Typoskript und Zeitungsausschnitt solide; Handschrift variabel (2 verified, 1 divergent); Kurztext instabil (wenig Text = instabile Metrik); Korrespondenz 3/3 divergent — die echte Herausforderung.

**Kernerkenntnisse:**
1. **Reading-Order-Divergenz** ist die Hauptursache hoher CER bei komplexen Layouts: o_szd.142 hat CER 55%, aber word_overlap 100% — identische Woerter in anderer Reihenfolge (Marginalia, Spalten). `word_overlap` loest dieses Messproblem.
2. **Seiten-Halluzination:** Flash Lite dupliziert gelegentlich kurze Seiten (o_szd.101); seit v1.4 erkennbar.
3. **Bleed-Through:** VLM transkribiert durchscheinenden Rueckseitentext; System-Prompt Regel 9 adressiert das.
4. **VLM-Nondeterminismus:** Dasselbe Objekt liefert je Lauf unterschiedliche CER (o_szd.101: 10% vs. 55%). Temperature 0.1 ist nicht deterministisch genug.

---

## 5. Verification-by-Vision (VbV)

VLMs vergleichen Faksimile-Bild mit Transkriptionstext und identifizieren Fehler — staerker als reiner Text-Text-Vergleich (§4), weil das Quellbild einbezogen wird. Zwei Kanaele: Claude Code Agent (Read-Tool mit Vision, $0, ~2–5 Min/Objekt) und Gemini API (Bild + Text, ~$0.001/Seite). Merge: beide finden Fehler X = hoch konfident; nur einer = mittel; keiner = verified.

**Error-Markup:** `«original→korrektur|konfidenz»`, z.B. `«entbalten→enthalten|0.8»` (Guillemets kollidieren mit keinem bestehenden Markup).

**Empirische Befunde (Session 11, 8 Objekte):**

| Muster | Befund |
|---|---|
| Gedruckter Text (Antiqua) | Durchgehend korrekt, 0 Fehler |
| Fraktur | >99% korrekt, typische Verwechslungen (fl-Ligatur, langes s, u/n) |
| Handschrift | Einzelwort-Ambiguitaeten, keine Halluzinationen; d/r-Verwechslung bei Korrespondenz |
| Handschriftliche Korrekturen | Schwaechste Schicht (~60–70%), Nonsens-Woerter bei Ueberlagerungen |
| Pipeline-Bug | Objekte mit >60 Bildern erzeugten leere Ergebnisse (o_szd.147) |

Methodische Grenze: Claude und Gemini teilen VLM-typische Kurrent-Schwaechen — Cross-Model-Agreement ist dort weniger informativ. VbV wurde in Session 18 als Agent-Verifikation (§8) operationalisiert und persistiert.

---

## 6. Viewer-Integration (implementiert)

Die urspruenglichen Frontend-Anforderungen sind umgesetzt und vom Drei-Status-Modell ueberformt:

- **Katalog:** Spalte "Status" (vormals "Review") zeigt Mensch-geprueft / Agent-geprueft / Ungeprueft; ⚠ markiert "zuerst sichten" (Triage). Eine eigene Qualitaets-/Signale-Spalte gibt es nicht mehr; Filter nach Review-Status inkl. "zuerst sichten".
- **Objektansicht:** Qualitaetssignale (Marker, Duplikate, Sprachkonsistenz, Leerseiten), Modellkonsensus-Tab und Korrektur-Diff (`edit_history`) erscheinen nur hier.
- **Editorial Progress und Stats-Donut:** drei Status — Gruen = Mensch, Blau = Agent, Grau = Ungeprueft; Amber nur als Triage-Akzent.
- **Diff/Edit:** Side-by-Side-Vergleich zweier Transkriptionen bzw. Original vs. Korrektur; Edit-Workflow via `serve.py`-API (POST `/api/approve`, `/api/edit`).
- **GT-Review-Modus:** 3-Varianten-Ansicht der GT-Drafts mit Source-Badges und Approve (setzt `gt_verified`).
- **CER-Anzeige:** pro Objekt, wo Referenz (Mensch-geprueft) vorliegt; Farbkodierung gruen <5%, gelb 5–15%, rot >15%.

---

## 7. Modellkonsensus (LLM-as-Judge)

> **Definition:** *Modellkonsensus* (Cross-Model Agreement) bezeichnet den automatischen Vergleich zweier unabhaengiger VLM-Transkriptionen desselben Faksimiles (Gemini Flash Lite + Gemini 3 Flash). Uebereinstimmung wird zeichenweise (CER) und wortweise (Jaccard Word Overlap) gemessen und 4-stufig klassifiziert (§4.3): `consensus_verified` / `consensus_moderate` / `consensus_review` / `consensus_divergent`. Wo die Modelle uebereinstimmen, ist die Transkription mit hoher Wahrscheinlichkeit korrekt; Divergenz markiert automatisch Stellen fuer menschliche Pruefung.

### 7.1 Architektur

```
Faksimile-Bild
    ├──→ Modell A: Gemini 3.1 Flash Lite (Ersttranskription, liegt vor)
    ├──→ Modell B: Gemini 3 Flash (unabhaengige Zweittranskription, verify.py)
    └──→ Judge: Claude (Claude Code Subagent mit Vision)
             Eingabe: Bild + Transkription A + B
             Ausgabe: Bewertung, korrigierte Version, Konsensus-Score
```

Der Judge folgt dem LLM-as-a-Judge-Paradigma (Gu et al. 2025, arXiv:2411.15594). `verify.py` schreibt `_consensus.json` inkl. vorbereitetem `judge_data`-Paket; die Judge-Rolle selbst laeuft als Claude-Code-Subagent, nicht im Skript. Eine frueher hier spezifizierte Kategorie `consensus_corrected` wurde nie implementiert — massgeblich ist die 4-Tier-Klassifikation (§4.3).

### 7.2 Wissenschaftliche Fundierung

| Behauptung | Stuetzende Evidenz |
|---|---|
| Korrekte Outputs konvergieren | ZHA25 (Consensus Entropy, ICLR 2026) |
| Accept/Abstain ist formalisierbar | RCO26 |
| Kreuzkorrektur mit Bild funktioniert | HUM24: 8.0% → 1.8% CER |
| Selbstkorrektur funktioniert NICHT | CRO25: 3.7–4.9x Verschlechterung |
| LLM-generated GT mit Ensemble: ~2–6% Error Rate | LLM-Generated-GT-Literatur |

### 7.3 Abgrenzungen

- **Konsensus ≠ Wahrheit:** Drei Modelle koennen sich auf denselben Fehler einigen (systematischer Bias) — daher manuelle Stichproben der `consensus_verified`-Objekte.
- **Judge ist nicht neutral:** Claude hat eigene Biases; der Judge-Prompt muss Abweichungen begruenden lassen, nicht "das bessere" auswaehlen.
- **Kosten sind real:** 3 Modelle ≈ 3x Basiskosten — gerechtfertigt, weil manuelle GT-Erstellung bei tausenden Objekten teurer waere.

Die Validierung (27 Objekte, §4.3) und die GT-Pipeline (18 Objekte, §7.1 im Forschungsteil) sind durchgefuehrt; Modellkonsensus laeuft seither selektiv als Pruefwerkzeug, nicht als Pflichtstufe fuer jeden Batch.

---

## 8. Agent-Verifikation (agent_verified)

*Implementiert in Session 18 (2026-04-02). Empirische Ergebnisse → [[evaluation-results]].*

### 8.1 Motivation

Menschliches Review skaliert nicht ueber tausende Objekte; rein automatische Messung (quality_signals, Modellkonsensus) ist blind fuer Fehler, die nur im Bild-Text-Vergleich sichtbar werden (z.B. Fraktur-f/s-Verwechslungen, die echte Woerter ergeben). Agent-Verifikation schliesst die Luecke: Ein Claude-Vision-Agent vergleicht systematisch Faksimile gegen Gemini-Transkription — ein automatisierter Cross-Provider-Check mit Vision, die Operationalisierung von VbV (§5).

Im Drei-Status-Modell ist `agent_verified` der mittlere Status ("Agent-geprueft"): Er priorisiert menschliche Zeit (wahrscheinlich korrekte Objekte), findet und korrigiert konkrete Fehler und liefert CER-Schaetzungen — ersetzt aber keine menschliche Pruefung und zaehlt nicht als Ground Truth.

### 8.2 Technische Umsetzung

**Workflow:** Sub-Agent erhaelt Object-ID, Collection, Bildpfade → liest Seitenbilder aus dem lokalen Backup (`SZD_BACKUP_ROOT`) und die Transkription aus dem Pipeline-JSON → pro Content-Seite Bild-Text-Vergleich → Fehlerliste (Zitat, Korrektur, Schweregrad) → Korrekturen werden im JSON angewendet, Review-Metadaten geschrieben (API: `POST /api/approve` mit `status: "agent_verified"`, `serve.py`).

```json
"review": {
  "status": "agent_verified",
  "agent_model": "claude-opus-4-6",
  "errors_found": 2,
  "estimated_accuracy": 0.996,
  "edited_pages": [1, 3],
  "reviewed_by": "Claude Code Agent",
  "reviewed_at": "2026-04-02T..."
}
```

Parallelisierung: bis zu 4 Sub-Agents gleichzeitig (je 2 Objekte); ein Batch von 8 Objekten dauert ~3 Minuten.

### 8.3 Verhaeltnis zu den anderen Verfahren

| Verfahren | Vergleichsgrundlage | Persistenz | Abschnitt |
|---|---|---|---|
| Modellkonsensus | Text ↔ Text (2 VLMs) | `_consensus.json` | §4 + §7 |
| Verification-by-Vision | Bild ↔ Text (manuell) | nicht persistiert | §5 |
| **Agent-Verifikation** | **Bild ↔ Text (automatisch)** | **`review` im Ergebnis-JSON** | **§8** |

### 8.4 Empirische Ergebnisse

Bis Session 20: **44 Objekte** agent-verifiziert in 7 Batches — 22 fehlerfrei (97–100%), 18 mit 1–5 Fehlern (95–99.9%), 4 mit schweren Problemen (75–93%, Truncation oder tabellarisch). Hauptfehlertypen: Fraktur f/s + Nonsens-Halluzination, Kurrent-Verwechslungen, fremdsprachliche Vokale, Truncation bei grossen Objekten. Details → [[evaluation-results]].

### 8.5 Edit-Tracking (ab Session 20)

Alle Korrekturen — vom Agenten wie vom Menschen (`serve.py`) — werden mit `edit_history` pro Seite gespeichert; das LLM-Original bleibt erhalten und ist im Frontend als Side-by-Side-Diff sichtbar (Tab "Korrekturen"):

```json
"edit_history": [{
  "original_transcription": "Text vor Korrektur",
  "edited_by": "Claude Code Agent",
  "edited_at": "2026-04-02T...",
  "source": "agent"
}]
```

Retroaktive Migration: `backfill_edit_history.py`. Frontend: `renderEditDiffView()` in `app.js`.

---

## Stand und offene Punkte (2026-06-10)

**Umgesetzt:** quality_signals v1.5 (kalibriert, drei aktive Review-Kriterien), Modellkonsensus-Validierung (27 Objekte), 3-Modell-GT-Pipeline (18 Objekte), Agent-Verifikation (44+ Objekte), Drei-Status-Review-Modell mit Edit-Tracking, Viewer-Integration. CER-Baseline ueber alle 9 Gruppen: <5% (Druck) bis ~10% (schwierige Handschrift/Tabellen) → [[evaluation-results]].

**Offen:**
- Prompt-Wirksamkeits-Experiment (§3) — billig, nie ausgefuehrt
- `duplicate_pages`-False-Positive bei Color-Chart-Doppelfotografie
- Entscheidung, ob Doppeltranskription (Modellkonsensus) fuer weitere Bestandsteile gefahren wird
- Pseudo-Perplexity als Eskalationsstufe, falls Triage-Signale nicht mehr ausreichen
