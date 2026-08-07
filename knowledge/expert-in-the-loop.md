---
title: "Expert-in-the-Loop"
aliases: ["Expert-in-the-Loop", "Wer prueft was"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline.git"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/promptotyping"
status: living
created: 2026-08-07
updated: 2026-08-07
type: concept
related:
  - "[[verification-concept]]"
  - "[[annotation-protocol]]"
  - "[[review-findings]]"
  - "[[evaluation-results]]"
---

# Expert-in-the-Loop: Wo ist welche Expertise noetig?

Leitfrage: *Nicht* "braucht die Pipeline einen Menschen?" — das ist beantwortet — sondern **welchen Menschen an welcher Stelle**. "Expert-in-the-Loop" ist im Projektumfeld (vgl. coOCR HTR) bislang als eine Rolle gefuehrt. Beim tatsaechlichen Durcharbeiten zerfaellt sie in mehrere, die sich nicht gegenseitig vertreten koennen.

Abgrenzung: [[verification-concept]] beschreibt die *Verfahren* der Qualitaetsmessung, [[annotation-protocol]] die *Konventionen*. Hier geht es um die **Zuordnung von Kompetenz zu Entscheidung** — welche Frage darf wer beantworten.

Urheberschaft wie in [[review-findings]]: **[J]** = Julia Hintersteiner (Operator, fachliche Beobachtung), **[C]** = Claude (maschinelle Nachpruefung, Kommando jeweils angegeben).

---

## 1. Zwei Achsen, die regelmaessig verwechselt werden

**[J]** Es gibt einerseits die **technische Umsetzung** und andererseits das **inhaltliche Reviewen**. Beim inhaltlichen Reviewen stoesst man sehr schnell an Grenzen, wo Detailwissen gefragt ist — zum Beispiel, mit welchen Personen hier korrespondiert wird. Auch palaeographische Kenntnisse sind nicht zu unterschaetzen, etwa Kurrent lesen zu koennen.

**[C]** Die beiden Achsen sind im Projekt bisher nicht getrennt modelliert. Das Review-Modell (CLAUDE.md, Stand 2026-06-10) kennt drei Status — Mensch-geprueft, Agent-geprueft, Ungeprueft — aber nur *eine* Sorte Mensch. Wer im Viewer auf "Approve" klickt, macht damit die Aussage "am Faksimile gegengelesen, gilt als Ground-Truth-faehig", unabhaengig davon, ob die betreffende Seite Typoskript oder Kurrent war und ob die Personennamen darin ueberpruefbar waren. Die Kompetenz, die eine Freigabe traegt, wird nicht mitgeschrieben.

---

## 2. Vier Kompetenzen

| Kompetenz | Beantwortet die Frage | Ohne sie passiert |
|---|---|---|
| **Technisch** (Pipeline, Prompt, Export) | Laeuft der Schritt korrekt, ist das Format valide, greift die Regel? | Stille Datenfehler, kaputte Exporte |
| **Palaeographisch** (Kurrent, Schriftentwicklung, Hand Zweigs) | Steht da wirklich das, was das Modell liest? | Falschlesungen werden als geprueft bestaetigt |
| **Prosopographisch / fachlich** (Zweig-Netzwerk, Werkkontext, Zeitgeschichte) | Ist der Eigenname, das Datum, der Werktitel plausibel? Wer ist "R."? | Plausibel klingende Halluzinationen ueberleben |
| **Editorisch** (Annotationsprotokoll, TEI/METS-Semantik) | Ist die Auszeichnung protokollkonform und exportfaehig? | Marker-Wildwuchs, unbrauchbares Zielformat |

Die vier sind selten in einer Person vereint, und — das ist der Punkt — sie sind **an unterschiedlichen Pipeline-Stellen** noetig.

---

## 3. Routing: Entscheidung → Kompetenz

| Pipeline-Stelle | Konkrete Entscheidung | Noetige Kompetenz |
|---|---|---|
| Gruppenzuordnung (`resolve_group()`) | Ist das Konvolut oder Korrespondenz? | Editorisch (+ fachlich bei Grenzfaellen) |
| Prompt-Entwurf, Objekt-Overrides | Welche Anweisung braucht dieser Dokumenttyp? | Technisch + editorisch |
| `quality_signals` / Triage | Welche Signale sind aussagekraeftig? | Technisch, gegen Messwerte |
| **Approve auf Typoskript** | Stimmt die Transkription? | Sorgfalt; Deutsch/Englisch. **Kein** Kurrent noetig |
| **Approve auf Kurrent-Handschrift** | Stimmt die Transkription? | **Palaeographisch** — sonst wertlos |
| **Eigennamen, Datierung, Adressaten** | Wer ist gemeint, stimmt das Datum? | **Prosopographisch** — Nachschlagen reicht oft nicht |
| Markup setzen ({}, ~~~~, [quer:] …) | Einfuegung oder Rauschen? Marginalie oder Nachsatz? | Editorisch + palaeographisch |
| GT Verify (Tier 0) | Zeichengenaue Freigabe als CER-Referenz | Palaeographisch **und** editorisch |

Ablesbar: Die technische Kompetenz sitzt fast vollstaendig **vor** der Transkription, die inhaltlichen Kompetenzen fast vollstaendig **danach**. Das Projekt hat den vorderen Teil gut ausgebaut und den hinteren an einem einzigen Button haengen.

---

## 4. Warum das nicht theoretisch ist

**[C]** Drei Auszaehlungen vom 2026-08-07, alle offline nachrechenbar:

**Der Flaschenhals ist real.** Von 2.452 Katalogobjekten sind 21 mensch-geprueft (`approved`), 85 agent-geprueft, 2.346 ohne jeden Review. Die Triage-Liste (`needs_review` und noch ungeprueft) umfasst 312 Objekte.

```bash
python -c "import json,collections; o=json.load(open('docs/catalog.json',encoding='utf-8'))['objects']; print(collections.Counter(x.get('reviewStatus') or '-' for x in o))"
```

**Palaeographie ist der teuerste Engpass.** Kurrent liegt bei 90–95% Genauigkeit gegenueber 99%+ bei Druck ([[evaluation-results]]), mit systematischen Verwechslungen (h↔I, n↔u, r↔v, L↔B, St↔H, f↔s). Eine Freigabe ohne Kurrent-Kompetenz ist auf diesen Seiten nicht neutral, sondern **schaedlich**: sie zementiert 5–10% Fehler als Ground Truth und verfaelscht damit genau die CER-Referenz, gegen die alles andere gemessen wird. Ungeprueft waere besser als falsch geprueft.

**Die editorische Kompetenz fehlt bereits sichtbar in den Daten.** Ueber alle Ergebnis-JSONs kommen 388 Label-Marker in 68 verschiedenen Schreibweisen vor. `marker_enrich.py` konvertiert davon genau drei Labels (`[Stempel:]`, `[Poststempel:]`, `[Marginalie:]`) = 28 Vorkommen, also **7%**. `[Marginalie:]` — der einzige im Annotationsprotokoll §3.5 dokumentierte Rand-Marker — kommt **null Mal** vor; das Modell schreibt stattdessen `[Randnotiz links:]` (51×) und 79 weitere Rand-Varianten. 27 Labels sind Einzelfaelle, reine Ad-hoc-Erfindungen des Modells.

```bash
python -c "import json,re,collections,pathlib; pat=re.compile(r'\[([A-Za-zÄÖÜäöü][^:\]\n]{0,24}):'); c=collections.Counter(m.group(1).strip() for p in pathlib.Path('results').rglob('*.json') if not p.name.endswith(('_layout.json','_page.json')) for pg in (json.loads(p.read_text(encoding='utf-8')).get('result') or {}).get('pages') or [] for m in pat.finditer(pg.get('transcription') or '')); print(sum(c.values()), len(c), c.most_common(15))"
```

Das ist kein Modellfehler, sondern eine **unbesetzte Rolle**: Niemand hat entschieden, welche Label-Vokabeln gelten. Das Modell fuellt die Luecke mit Improvisation, und der Export wirft 93% davon weg.

---

## 5. Konsequenzen

**Triage nach Kompetenz, nicht nur nach Signal.** Die Filterung im Katalog bietet Qualitaetssignale an (`page_length_anomaly` usw.). Was fehlt, ist die Frage "was kann *ich* freigeben?". Gruppe B (Typoskript) und H (Zeitungsausschnitt) sind ohne palaeographische Ausbildung pruefbar, Gruppe A und I ueberwiegend nicht. Eine Sicht "prueffaehig ohne Kurrent" wuerde den Engpass entzerren, ohne die Qualitaet zu senken.

**Der Review-Status sollte seine Grundlage mitfuehren.** `review.reviewed_by` haelt fest, *wer* geprueft hat, aber nicht *woraufhin*. Ein Feld in der Art von `review.basis` (`transkription` / `palaeographie` / `prosopographie`) wuerde sichtbar machen, dass eine Seite zwar zeichengenau gelesen, der Adressat aber nicht verifiziert wurde. Offen: ob das den Review-Workflow zu schwerfaellig macht — Entscheidung Projektleitung.

**Prosopographie braucht eine eigene Runde.** Personennamen sind weder vom Modell noch von der Transkriptionspruefung abgedeckt: Wer "Gieser" liest, kann zeichengenau richtig liegen und trotzdem eine Person meinen, die es nicht gibt. Diese Pruefung ist von der Transkription **entkoppelt** und laesst sich sinnvoll erst nach der Zeichenpruefung ansetzen — sie gehoert eher in die nachgelagerte TEI-Annotation (teiCrafter) als in diesen Viewer.

**Das Label-Vokabular ist zu entscheiden, nicht zu erraten.** Siehe §4: solange kein geschlossenes Vokabular festliegt, produziert jede Transkription neuen Wildwuchs. Das ist die kleinste und billigste der vier offenen Rollen.

---

## 6. Offene Fragen

1. Gibt es im SZD-Umfeld ueberhaupt Kurrent-Kompetenz mit Kapazitaet, oder muss das Ziel fuer die Handschriften-Gruppen von "geprueft" auf "als ungeprueft gekennzeichnet" gesenkt werden?
2. Ist ein zweistufiges Approve sinnvoll (Transkription geprueft / Sachverhalt geprueft) oder ueberfrachtet das den Workflow?
3. Kann die Agent-Verifikation ([[verification-concept]] §8) palaeographisch schwierige Seiten wenigstens *vorsortieren*, damit die knappe Kurrent-Zeit nicht auf einfache Seiten faellt?
4. Wer entscheidet das Label-Vokabular — und wird es geschlossen (nur definierte Labels erlaubt) oder offen mit Konvertierungsliste?
