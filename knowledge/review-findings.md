---
title: "Review-Befunde"
aliases: ["Verbesserungsvorschlaege", "Findings"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline.git"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/promptotyping"
status: living
created: 2026-07-25
updated: 2026-07-25
type: log
related:
  - "[[evaluation-results]]"
  - "[[verification-concept]]"
  - "[[data-overview]]"
  - "[[journal]]"
---

# Review-Befunde und Verbesserungsvorschlaege

Laufende Sammelstelle fuer alles, was beim Durcharbeiten der Transkriptionen und des Viewers auffaellt: Fehler, fragwuerdige Zuordnungen, fehlende Funktionen, Ideen. Kein Beschluss — was hier steht, ist Material fuer die Evaluation und fuer spaetere Entscheidungen in [[journal]] und `Plan.md`.

Abgrenzung zu den Nachbardokumenten: [[evaluation-results]] haelt gemessene Ergebnisse fest (CER, Fehlertypologie), [[verification-concept]] die Methodik. Hier stehen **offene Beobachtungen** — auch solche, die sich spaeter als unbegruendet herausstellen.

---

## Kennzeichnung der Urheberschaft

Jeder Eintrag trennt sichtbar, wer was beigetragen hat. Die Marker gelten fuer den jeweiligen Absatz:

| Marker | Urheber:in | Bedeutung |
|---|---|---|
| **[J]** | Julia Hintersteiner (Operator) | Fachliche Beobachtung am Material oder am Viewer. Inhaltlich massgeblich. |
| **[C]** | Claude (Opus 5) | Maschinelle Nachpruefung: Auszaehlung, Code-Lektuere, Vorschlagsentwurf. Immer nachrechenbar — Kommando steht dabei. |

Regeln fuer die Pflege:

- **[J]**-Absaetze werden nicht von Claude umformuliert oder "korrigiert". Stellt sich eine Beobachtung als unzutreffend heraus, bleibt sie stehen und bekommt eine **[C]**-Nachpruefung darunter.
- **[C]**-Absaetze nennen immer die Grundlage (Datei, Zeile, Kommando), damit die Zahl nachvollziehbar ist.
- Jeder Eintrag bekommt eine stabile ID (`B-01`, `B-02`, …), auf die aus Journal, Issues und Commits verwiesen werden kann.

Status-Werte: `offen` · `in Klaerung` · `entschieden` · `umgesetzt` · `verworfen`

---

## Uebersicht

| ID | Thema | Quelle | Status |
|---|---|---|---|
| [B-01](#b-01--gruppenzuordnung-registerblaetter-landen-in-handschrift-statt-tabellarisch) | Gruppenzuordnung: Registerblaetter → Handschrift statt Tabellarisch | **[J]** | offen |
| [B-02](#b-02--gruppenzuweisung-im-review-aenderbar-machen) | Gruppenzuweisung im Review aenderbar / vorschlagbar machen | **[J]** | offen |

---

## B-01 — Gruppenzuordnung: Registerblaetter landen in Handschrift statt Tabellarisch

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-07-25 |
| **Betrifft** | `pipeline/tei_context.py` (`resolve_group()`), [[data-overview]] §6, Viewer-Filter "Gruppen" |
| **Status** | offen — inhaltliche Entscheidung steht aus |

### Beobachtung **[J]**

Der Viewer hat einen Filter "Gruppen". Unklar war, wie diese Einteilung zustande gekommen ist und ob sie sachlich stimmt.

### Nachpruefung **[C]**

Dokumentiert ist die Einteilung an drei Stellen: [[data-overview]] §6 (Master-Tabelle der 9 Gruppen, abgeleitet aus der TEI-Analyse), [[journal]] (Sessions 2, 3 und 7 — Entstehung von A–E, dann F/H/I, Gruppe G bewusst nachgereicht) und `Plan.md` (Entscheidungslog). Operativ massgeblich ist aber allein die Funktion `resolve_group()` in `pipeline/tei_context.py:285-322` — ein Entscheidungsbaum ueber `objecttyp` und `classification` mit Fallback auf Handschrift.

Zwischen der dokumentierten Populationsschaetzung und der tatsaechlichen Zuordnung klaffen zwei Gruppen deutlich auseinander (Auszaehlung ueber alle 2.452 transkribierten Objekte in `docs/catalog.json`):

| Gruppe | [[data-overview]] §6 | tatsaechlich zugeordnet | Differenz |
|---|---:|---:|---|
| A Handschrift | ~100 | **318** | +218 |
| E Tabellarisch | ~230 | **5** | −225 |
| B Typoskript | ~300 | 216 | −84 |
| H Zeitungsausschnitt | ~312 | 305 | passt |
| I Korrespondenz | ~1.536 | 1.535 | passt |

**Ursache — belegt:** 207 Objekte der Aufsatzablage tragen `classification: Registerblätter` bei `objecttyp: Manuskript` (205×) bzw. `Manuskript und Typoskriptdurchschlag` (2×). Alle 207 landen in Gruppe A. Das sind 65 % aller Handschrift-Objekte. Grund ist keine Regelkollision, sondern eine Luecke im Vokabular:

- `tei_context.py:313` prueft **`objecttyp`** auf `register|kalender|adressbuch|kontorbuch` — greift nicht, weil der Objekttyp "Manuskript" lautet.
- `tei_context.py:315` prueft **`classification`** auf `verzeichnisse|kalender` — greift nicht, weil dort "Registerblätter" steht, ein Wert, den die Regel nicht kennt.
- Folglich feuert vorher `tei_context.py:303` (`"manuskript" in otyp` → handschrift).

Die Schaetzung "~230" in [[data-overview]] §6 erklaert sich damit fast vollstaendig: 207 Registerblaetter plus die 5 tatsaechlich als E gefuehrten Lebensdokumente-Objekte plus einige nicht transkribierte. [[journal]] nennt dieselbe Menge aus anderer Richtung: "Erwin Rieger, 225 Registerblaetter, zweithaeufigste Hand in der Aufsatzablage" (Session 2).

**Verworfene Zwischenhypothese [C]:** In der Sitzung zuerst vermutet, die Faelle wuerden durch die Regelreihenfolge verschattet (fruehere Regel feuert, spaetere haette eine andere Gruppe ergeben). Eine Auszaehlung aller 14 Regeln gegen alle Objekte widerlegt das: nur **2** Objekte haben ueberhaupt ein Tabellarisch-Signal und eine andere Gruppe (o:szd.184 `Manuskript/Verzeichnisse` → A, o:szd.140 `Typoskript/Verzeichnisse` → B). Reihenfolge ist hier nicht das Problem, fehlendes Vokabular schon.

Nebenbefund derselben Auszaehlung — echte Verschattung gibt es, nur an anderer Stelle: 171 Postkarten in korrespondenzen/autographen werden von der Sammlungs-Regel (`tei_context.py:289`) zu I gezogen, obwohl die Kurztext-Regel greifen wuerde. Das ist laut CLAUDE.md ausdruecklich so gewollt und hier nur als Kontext vermerkt.

Nachrechnen:

```bash
python -c "import json,collections; c=json.load(open('docs/catalog.json',encoding='utf-8'))['objects']; r=[x for x in c if 'registerbl' in (x.get('classification') or '').lower()]; print(len(r), collections.Counter(x['groupLabel'] for x in r))"
```

### Offene Entscheidung — braucht **[J]**

Ob die 207 Registerblaetter fachlich in A oder in E gehoeren, ist keine Code-Frage. Riegers Registerblaetter sind handschriftlich, insofern ist A nicht abwegig; sie sind aber zugleich tabellarisch-listenfoermig, und CLAUDE.md nennt genau dafuer eine bekannte Schwaeche ("VLM-Linearisierung ordnet Betraege falschen Zeilen zu, ~90 % Genauigkeit"). Die Gruppe entscheidet, welcher Prompt gefahren wird, also wirkt sie direkt auf die Transkriptionsqualitaet.

Was zu klaeren ist:

1. Sind die Registerblaetter naeher an Gruppe A (Handschrift) oder E (Tabellarisch)? Ggf. Stichprobe am Faksimile.
2. Falls E: Umzug bedeutet Neu-Transkription von 207 Objekten mit `group_e_tabellarisch.md`. Aufwand und Nutzen gegeneinander abwaegen — vorher an 3–5 Objekten A gegen E vergleichen.
3. Falls A bleibt: [[data-overview]] §6 korrigieren, damit die Master-Tabelle nicht weiter eine Population behauptet, die die Pipeline nie erzeugt.

### Vorschlag **[C]**

Unabhaengig von 1.–3. sollte die Diskrepanz zwischen dokumentierter und tatsaechlicher Population nicht unbemerkt entstehen koennen. Ein Testfall in der Art von `pipeline/test_canonical_collection.py`, der die Gruppenverteilung aus `catalog.json` gegen erwartete Groessenordnungen prueft, haette den Faktor 46 sofort sichtbar gemacht.

---

## B-02 — Gruppenzuweisung im Review aenderbar machen

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-07-25 |
| **Betrifft** | `docs/app.js` (Viewer-Review), `pipeline/serve.py` (Review-API), Ergebnis-JSON (`group`) |
| **Status** | offen — Feature-Wunsch, nicht umgesetzt |

### Beobachtung / Wunsch **[J]**

Bearbeiter:innen sollten die Moeglichkeit haben, solche Zuschreibungen beim Reviewen der Transkription auch zu aendern bzw. vorzuschlagen.

### Einordnung **[C]**

Das trifft die Stelle, an der B-01 sichtbar geworden waere: Wer ein Registerblatt am Faksimile gegenliest, sieht sofort, dass die Gruppe nicht passt — kann es aktuell aber nirgends festhalten. Die Gruppe entsteht heute rein automatisch aus TEI-Metadaten und ist im Review-Workflow schreibgeschuetzt.

Stand der Technik im Repo:

- Die Gruppe steht als `group` auf oberster Ebene im Ergebnis-JSON, gesetzt von `resolve_group()` beim Transkribieren.
- `pipeline/serve.py` kennt POST `/api/approve` und POST `/api/edit`; beide schreiben in `review` bzw. in die Seitentexte. Kein Endpunkt beruehrt `group`.
- Als Override existiert bisher nur die Datei-Ebene: `pipeline/prompts/objects/{object_id}.md` ueberschreibt den Gruppen-Prompt (aktuell genau ein Fall, `o_szd.1056`). Das ist ein Entwickler-Werkzeug, nichts fuer Bearbeiter:innen im Viewer.

Ein Detail, das fuer den Entwurf wichtig ist: eine geaenderte Gruppe wirkt sich **nicht rueckwirkend** auf eine vorhandene Transkription aus — der Prompt ist beim Transkribieren schon gelaufen. Ein Gruppenwechsel ist also eher ein Auftrag zur Neu-Transkription als eine Korrektur.

### Vorschlag zur Diskussion **[C]**

Vorschlagen statt ueberschreiben, analog zum bestehenden Drei-Status-Review-Modell:

1. Im Viewer neben der Gruppenanzeige ein Auswahlfeld "Gruppe passt nicht → Vorschlag" mit den 9 Gruppen und einem Freitextfeld fuer die Begruendung.
2. Neuer Endpunkt POST `/api/suggest-group` in `serve.py`, der **nicht** `group` ueberschreibt, sondern daneben schreibt:
   ```json
   "group_suggestion": {
     "proposed": "tabellarisch",
     "current": "handschrift",
     "reason": "Registerblatt, tabellarische Struktur",
     "by": "…", "date": "2026-07-25", "applied": false
   }
   ```
   Damit bleibt die maschinelle Zuordnung als Datum erhalten und der menschliche Widerspruch wird auswertbar — dieselbe Trennung wie bei `transcription` gegen `transcription_llm`.
3. Im Katalog ein Filter "Gruppenvorschlag offen", damit sich Vorschlaege sammeln und stapelweise abarbeiten lassen.
4. Batch-Anwendung ueber ein CLI-Skript (in der Art von `import_reviews.py`), das angenommene Vorschlaege nach `group` schreibt und die betroffenen Objekte zur Neu-Transkription vormerkt.

Zusatznutzen fuer die Evaluation: die gesammelten Vorschlaege sind eine Messgroesse fuer die Treffsicherheit von `resolve_group()` und liefern das Vokabular, das der Funktion heute fehlt (siehe B-01) — belegt statt geraten.

---

## Verwandte Dokumente

- [[evaluation-results]] — gemessene CER-Baseline und Fehlertypologie
- [[verification-concept]] — Verifikationsmethodik, Review-Stufen
- [[data-overview]] — Datengrundlage, §6 Master-Tabelle der Prompt-Gruppen
- [[journal]] — chronologisches Session-Log
