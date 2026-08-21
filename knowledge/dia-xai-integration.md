---
title: "DIA-XAI-Integration"
aliases: ["DIA-XAI-Integration", "Antragsbezug"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Integration"
  version: 0.1
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/integration"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-integration"
status: active
created: 2026-04-01
updated: 2026-07-30
authors: [Christopher Pollin]
type: concept
related:
  - "[[verification-concept]]"
  - "[[evaluation-results]]"
  - "[[htr-interchange-format]]"
---

# DIA-XAI-Integration: Rolle der Pipeline im Pilotprojekt und im geplanten Antrag

Abhaengigkeit: [[verification-concept]] (Reviewmodell, quality_signals, CER), [[evaluation-results]] (CER-Baseline), [[htr-interchange-format]] (Page-JSON)

---

## 1. Zweck

Dieses Dokument haelt fest, in welchem Verhaeltnis die SZD-HTR-Pipeline zum DIA-XAI-Pilotprojekt (PLUS Early Career Grant, April 2026 bis April 2027) und zu dem daraus wachsenden Antrag zur Verifikation in der LLM-gestuetzten geisteswissenschaftlichen Forschung steht. Es ersetzt die frueher hier dokumentierte Zulieferung an das Evaluationsframework EQUALIS, das am 18.07.2026 aufgeloest und in den Evaluationsansatz des Antrags ueberfuehrt wurde. Der historische Stand steht in §5.

Das Verhaeltnis hat zwei Seiten. Die Pipeline ist Messgegenstand, weil im Pilotprojekt eine CER-Evaluation an ihr laeuft. Und sie ist Vorarbeit, weil ihr Vertrauensmodell einer der Provenienzansaetze ist, die der geplante Antrag in seinem ersten Arbeitspaket zusammenfuehrt.

## 2. Wie der Antrag die Pipeline beschreibt

Der Antragstext fuehrt das Repository in §4 als laufende Vorarbeit. Die Beschreibung lautet im Original:

> Pipeline producing line-based TEI or Page-JSON, editor role; a four-tier trust model from checked ground truth to needs-checking implements graded verification provenance with editing history, preserves machine-generated states in an edit history when humans correct them, and refuses to collapse these statuses into a single confidence value. It is the project's operational proof that differentiated checking states can be carried through a production-scale workflow. Running.

Diese Beschreibung ist gegen den Code pruefbar und wurde am 2026-07-30 geprueft. Die Belegstellen stehen in §3. Wer den Antrag begutachtet, findet die Behauptung im Repository an drei Orten bestaetigt, in der Tabelle **Trust tiers** in `README.md`, in `pipeline/serve.py` und in den Testfaellen unter `tests/test_trust_tiers.py`.

## 3. Die vier Vertrauensstufen als Provenienzansatz (WP1)

### 3.1 Gespeicherte Stufen

Der Zustand eines Objekts steht im Block `review` der Ergebnisdatei. Vier Stufen sind unterscheidbar:

| Stufe | Wert in `review.status` | Herkunft der Aussage |
|---|---|---|
| 0 | `gt_verified` | zeichengenau am Faksimile geprueft, ground-truth-faehig |
| 1 | `approved` | fachlich gegengelesen, bei Bedarf korrigiert |
| 2 | `agent_verified` | Claude-Vision-Agent hat Bild gegen Text verglichen |
| 3 | kein `review`-Block | nur Selbsteinschaetzung der Pipeline |

`needs_review` aus den quality_signals ist kein Status, sondern ein Triage-Hinweis innerhalb von Stufe 3. Er sagt, was zuerst zu sichten ist, und nicht, wie verlaesslich ein Text ist. Die Anzeigeschicht in `docs/app.js` fasst Stufe 0 und 1 zu "Mensch-geprueft" zusammen; die gespeicherten Werte bleiben davon unberuehrt, sodass die Differenz zwischen zeichengenauer und fachlicher Pruefung in den Daten erhalten bleibt.

### 3.2 Verweigerte Verdichtung

Die Pipeline fuehrt zwei weitere Bewertungen, die bewusst nicht mit der Vertrauensstufe verrechnet werden. `result.confidence` ist die kategoriale Selbsteinschaetzung des Modells (`high`, `medium`, `low`), `quality_signals.needs_review` das Ergebnis von sieben regelbasierten Signalen. Beide bleiben eigene Felder, im Datenmodell wie in den Filtern des Viewers. Es gibt keinen Ort im Code, an dem Pruefstatus, Modellkonfidenz und Signallage zu einer Zahl zusammengezogen werden. Die Begruendung steht in [[verification-concept]] und geht auf eine fruehe Projektentscheidung zurueck, kategoriale statt numerischer Konfidenz zu verwenden, weil LLMs ihre eigene Qualitaet numerisch nicht verlaesslich einschaetzen.

### 3.3 Erhaltung des Maschinenzustands

Korrigiert ein Mensch eine Seite, geht der maschinell erzeugte Zustand nicht verloren. Beim ersten Edit schreibt `serve.py` den Roh-Output einmalig nach `transcription_llm` und legt fuer jede Aenderung einen Eintrag in `edit_history` an, mit dem Text vor der Aenderung, dem Zeitstempel und dem Feld `source`, das menschliche von agentischen Korrekturen trennt. `transcription` bleibt die Arbeitsfassung. Daraus folgt eine Messmoeglichkeit, die es ohne diese Trennung nicht gaebe, jede menschliche Korrektur ist eine CER-Messung gegen den Roh-Output (`pipeline/report_cer_from_edits.py`).

### 3.4 Was WP1 daraus uebernehmen kann

Fuer die Harmonisierung der Provenienzansaetze im ersten Arbeitspaket ist an diesem Modell dreierlei uebertragbar, die Trennung von Pruefstatus und Qualitaetssignal, die Unterscheidung der pruefenden Instanz (Mensch, Agent, Regel) im selben Feldschema, und die Aufbewahrung des ueberschriebenen Maschinenzustands als Referenz fuer spaetere Messung. Was das Modell nicht leistet, gehoert ebenso zum Befund. Es kennt keine Stufe unterhalb der Seite, die Pruefung ist objekt- und seitenweise, und es haelt keine vorab definierte Prueftiefe je Materialklasse fest.

## 4. Evaluationshaken

Aus dem Antragsbezug folgen drei Exportschnittstellen, die noch nicht implementiert sind und als Issues unter dem Label `antrag-eval` gefuehrt werden. Sie stehen hier, damit die Pipeline-Arbeit sie nicht versehentlich verbaut.

| Haken | Was exportiert wird | Woher die Daten kaemen |
|---|---|---|
| Vier-Tupel-Protokoll | erste Experteneinschaetzung, KI-Vorschlag, finale Entscheidung, Referenzantwort sofern vorhanden | `transcription_llm`, `edit_history`, `transcription`, GT-Sample |
| Provenienz-Export | Produktions-, Entscheidungs- und Verifikationsschicht je Item | `provenance` in Page-JSON, `review`, `edit_history` |
| Gold-Standard-Haken | Referenzantworten mit vorab festgelegter Prueftiefe je Itemklasse | GT-Sample je Prompt-Gruppe |

Der erste Haken hat eine bekannte Luecke. Die Pipeline zeichnet die Experteneinschaetzung vor Sicht des KI-Vorschlags nicht auf, weil der Vorschlag im Arbeitsablauf immer zuerst da ist. Das Vier-Tupel ist aus dem Bestand daher nur dreistellig rekonstruierbar; eine vollstaendige Erhebung braucht einen eigenen Erhebungsmodus.

## 5. Historischer Stand (EQUALIS, aufgeloest 2026-07-18)

Bis zum 18.07.2026 war dieses Dokument als Zulieferungsspezifikation an EQUALIS geschrieben, ein fuenfdimensionales Evaluationsframework des Pilotprojekts. EQUALIS existiert nicht mehr; seine Substanz ist im Evaluationsansatz des Antrags aufgegangen. Der folgende Abschnitt bewahrt, was an der damaligen Zuordnung ueber die Pipeline selbst aussagt, weil sich diese Aussagen an keiner anderen Stelle des Vaults finden.

**Das damalige Rollenmodell.** DIA-XAI war als Aggregator konzipiert, nicht als Verifikationswerkzeug. Es importierte ein Metriken-JSON (`dia-xai-metrics-v1`) aus den Quellwerkzeugen und berechnete daraus die fuenf Dimensionen. Die Verifikation selbst fand im SZD-HTR-Viewer statt. Diese Arbeitsteilung ist erhalten geblieben, der Antrag misst nicht selbst, sondern wertet projektseitig aus.

**Die fuenf Dimensionen und ihre Datenquellen in der Pipeline.** Explainability speiste sich aus der Herkunft je Annotation, regelbasiert aus den quality_signals, maschinell aus der VLM-Transkription, manuell aus dem Expert-Review im Viewer. Quality speiste sich aus der CER gegen das GT-Sample, gesamt und je Prompt-Gruppe, dazu die Trefferquote der `needs_review`-Flags nach GT-Kalibrierung. Learning speiste sich aus dem Agreement-Trend des Cross-Model-Konsensus und aus dem CER-Vergleich vor und nach einer Prompt-Ueberarbeitung. Interaction speiste sich aus den Zaehlungen des Viewers, akzeptiert gegen korrigiert, und aus der Frage, wie oft ein falscher Vorschlag akzeptiert wurde. Scalability speiste sich aus der Streuung der CER ueber die neun Dokumentgruppen, die vier Sprachen und die Schreiberhaende.

**Was davon traegt.** Die Dimension Scalability nannte den bis heute gueltigen Grund, warum gerade dieser Korpus als Messgegenstand taugt, er enthaelt neun Dokumentgruppen, vier Sprachen und mehrere Schreiberhaende und liefert die Varianz, die ein homogener Korpus nicht hergibt. Die Dimension Interaction nannte mit dem Akzeptieren eines falschen Vorschlags einen Effekt, den der Antrag unter Verifikation weiterfuehrt. Die Dimension Explainability nannte die Provenienzunterscheidung, die im heutigen Vertrauensmodell (§3) implementiert ist.

**Was nicht uebernommen wird.** Das Schema `dia-xai-metrics-v1`, die Zuordnung der Use-Case-Nummer UC3 und der damalige Meilensteinplan sind gegenstandslos. Sie stehen unveraendert in der Git-Historie dieses Dokuments (Stand vor dem 2026-07-30) und werden hier nicht fortgeschrieben.
