<!--
Fertiger Issue-Body. Direkt verwendbar mit:

  gh issue create --repo chpollin/szd-htr-ocr-pipeline \
    --title "Review: Stellen zur Expertenrückfrage markieren (Zweigs Handschrift)" \
    --body-file reports/issue-expertenrueckfrage.md

Vorschlag Labels: enhancement
-->

Gemeldet von der Projekt-Reviewer:in (Universität Salzburg), 2026-10-30, aus dem Gegenlesen am Faksimile.

## Bedarf

Beim Redigieren gibt es Passagen, die ich schwer oder gar nicht lesen kann, weil ich Stefan
Zweigs Handschrift zu wenig kenne. Die Fachexpert:innen für Zweigs Handschrift (Literaturarchiv Salzburg) kennen sie. Im Viewer fehlt eine
Möglichkeit, ein Dokument (oder eine Stelle darin) **für sie zu markieren**, damit sie es sich
gezielt ansehen. Bisher bleibt so eine Stelle entweder unkommentiert stehen oder geht verloren,
weil die Freigabe sie überdeckt.

## Beispiel

**Aus der Werkstatt der Dichter**, SZ-AAP/W-AA215.1, `o:szd.2215`
→ `http://localhost:8000/#view/o_szd.2215_gemini-3.1-flash-lite-preview/1`

Zeitungsausschnitt mit handschriftlichen Zusätzen. Der gedruckte Text ist gegengelesen und
freigegeben (2026-10-30). Die handschriftliche Annotation links oben und der Text über dem Foto
sind offen. Das Modell hat dazu nur notiert: *„Die handschriftliche Annotation links oben wurde
nicht transkribiert … Der handschriftliche Text über dem Foto ist teilweise … unleserlich."*
Transkribiert ist nur `["Uhr"]`. Das Objekt steht jetzt als „Mensch-geprüft" im Katalog,
und dass hier noch jemand mit Handschriftkenntnis draufschauen soll, ist nirgends vermerkt.

## Warum das kein vierter Review-Status sein sollte

Die Rückfrage betrifft meist **eine Stelle**, nicht das ganze Objekt. Der Rest kann
gegengelesen und freigegeben sein. Eine Markierung „zur Rückfrage“ sollte deshalb **neben**
dem Review-Status stehen, nicht an seiner Stelle. Sonst müsste man sich entscheiden: entweder
freigeben (und die offene Stelle verschweigen) oder nicht freigeben (und die geleistete Arbeit
nicht festhalten).

## Technischer Fallstrick

`handle_approve()` und `handle_edit()` in `pipeline/serve.py` (Z. 79 ff., 128 ff.) ersetzen
`result["review"]` jeweils **komplett** durch ein neues Dict. Eine Markierung, die innerhalb von
`review` gespeichert wird, würde also beim nächsten Freigeben oder Speichern stillschweigend
gelöscht. Sie gehört in ein eigenes Feld auf oberster Ebene des Ergebnis-JSON, oder beide
Handler müssen sie ausdrücklich übernehmen. Ein Test in `tests/test_trust_tiers.py` sollte
das festhalten.

## Vorschlag

1. **Datenmodell:** eigenes Feld, z. B. `consult` (Liste, damit mehrere Rückfragen und ihre
   Erledigung erhalten bleiben):
   ```json
   "consult": [{
     "page": 1,
     "note": "Handschriftliche Annotation links oben und Text über dem Foto unleserlich",
     "for": ["<Fachexpert:in>"],
     "requested_by": "<Name>",
     "requested_at": "2026-10-30T…",
     "resolved_by": null, "resolved_at": null, "answer": null
   }]
   ```
2. **Viewer:** Button „Zur Rückfrage markieren" neben „Freigeben" (nur lokal, wie Approve).
   Kurzes Formular: Seite (vorbelegt mit der aktuellen), Notiz, an wen. Offene Rückfragen
   erscheinen als Badge am Objekt und an der Seite.
3. **Katalog:** Filter „Rückfrage offen" (optional nach Person), damit die Fachexpert:innen ihre
   Liste direkt aufrufen können.
4. **Erledigen:** Wer die Stelle gelesen hat, trägt die Lesung ein (Edit wie bisher) und
   schließt die Rückfrage mit einer kurzen Antwort. Der Eintrag bleibt mit `resolved_*` stehen,
   die Provenienz der Lesung ist so nachvollziehbar.
5. **API:** `POST /api/consult` (anlegen/erledigen) in `serve.py`, analog zu `/api/approve`
   mit `_validate_ids()` und `.json.bak`.

## Offene Fragen

- Sollen die Fachexpert:innen am lokalen Server arbeiten, oder brauchen sie die Liste auch in der
  öffentlichen Ansicht (GitHub Pages, nur lesend)?
- Reicht eine Markierung pro Seite, oder braucht es eine Stelle innerhalb der Seite
  (Zeile/Textausschnitt)?
- Gilt ein freigegebenes Objekt mit offener Rückfrage weiterhin als Ground-Truth-fähig für die
  CER, oder wird die betroffene Seite bis zur Erledigung ausgenommen?
