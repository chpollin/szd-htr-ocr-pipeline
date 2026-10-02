<!--
Fertiger Issue-Body. Direkt verwendbar mit:

  gh issue create --repo chpollin/szd-htr-ocr-pipeline \
    --title "Fehlersammlung Review — Befunde aus dem Redigieren" \
    --body-file reports/issue-review-fehlersammlung.md

Alternativ einfügen unter https://github.com/chpollin/szd-htr-ocr-pipeline/issues/new
Vorschlag Labels: bug, viewer, review
-->

Sammel-Issue für Fehler, die beim Gegenlesen am Faksimile auffallen. Ein Abschnitt je
Befund, neue Befunde werden unten angehängt. Erledigte bleiben stehen und bekommen
„**Behoben in** `<commit>`" in die Kopfzeile — die Sammlung soll auch später noch zeigen,
was das Redigieren an der Pipeline sichtbar gemacht hat.

**Format je Befund:** Symptom (was man sieht) · Reproduktion · Ursache (Datei + Zeile,
soweit ermittelt) · Umfang (wie viele Objekte) · Folgen · Vorschlag.

---

## 1 — Objekte ohne Seiten zeigen kein Faksimile, obwohl GAMS es ausliefert

Gemeldet von Julia Hintersteiner, 2026-08-26 · Status: offen

### Symptom

Objekt öffnen, Faksimile-Panel bleibt leer und zeigt *„Kein Bild verfügbar."*, Transkriptions-Panel
ist leer, der Seitenzähler steht auf **„Seite 1 / 0"**. Das Objekt trägt im Katalog das Signal
`page_image_mismatch` und den Badge *Review nötig*, lässt sich aber nicht redigieren, weil es
weder Bild noch Text gibt.

Beispiel: **Liebesbriefe**, SZ-AAP/W-AA122.0, `o:szd.2491`
→ `http://localhost:8000/#view/o_szd.2491_gemini-3.1-flash-lite-preview/1`

### Die Bilder fehlen nicht

GAMS liefert die Faksimiles einwandfrei — geprüft am 2026-08-26:

```text
https://gams.uni-graz.at/o:szd.2491/IMG.1        200  image/jpeg  1.430.596 Bytes
https://gams.uni-graz.at/o:szd.2491/THUMBNAIL    200  image/jpeg      1.670 Bytes
```

Auch die Ergebnis-Datei kennt alle sieben Bilder:
`results/aufsatzablage/o_szd.2491_gemini-3.1-flash-lite-preview.json` enthält
`metadata.images` mit `IMG.1` … `IMG.7`. Das Bild geht also auf dem Weg von der
Ergebnis-Datei in den Viewer verloren, nicht in GAMS.

### Ursache

Die Bildliste des Viewers wird **aus dem `pages`-Array abgeleitet**, nicht aus
`metadata.images`:

- `pipeline/build_viewer_data.py:157` — `page_images` entsteht aus der gefilterten
  Seitenliste. Gibt es keine Seiten, ist `images: []`.
- `docs/app.js:1779` — `obj.images[state.currentPage]`; bei leerer Liste greift der
  `else`-Zweig mit *„Kein Bild verfügbar."*

Bei `o:szd.2491` gibt es keine Seiten, weil die Transkription ein Totalausfall war:
`result` enthält nur `raw` (65.602 Zeichen Endlosschleife), kein `pages`-Array. Die
Bildanzeige hängt damit an einem Datenfeld, mit dem sie sachlich nichts zu tun hat.

### Umfang

**34 Objekte, 836 Faksimile-Scans**, alle vier Sammlungen. Es ist genau die Menge der
Totalausfälle — vollständige Liste, Ausfallarten je Objekt und Salvage-Potenzial:
[`reports/pipeline-totalausfaelle.md`](pipeline-totalausfaelle.md).

`o:szd.2491` ist kein Sonderfall, sondern einer von zehn in der Aufsatzablage.

### Folgen

1. **Die Meldung ist sachlich falsch.** „Kein Bild verfügbar" stimmt nicht — das Bild ist
   da und abrufbar. Wer dem Text glaubt, sucht den Fehler bei GAMS oder beim Ingest statt
   bei der Transkription.
2. **„Seite 1 / 0"** ist ein unmöglicher Zähler und verrät nicht, was eigentlich los ist.
3. **Das Objekt ist freigebbar.** *Approve* und *GT Verify* sind aktiv, und
   `pipeline/serve.py:87-92` prüft nur den Status-String und die IDs, nicht ob überhaupt Seiten
   existieren. Ein Objekt ohne jede Seite kann damit den Status `approved` oder sogar
   `gt_verified` bekommen und als Ground Truth in die CER-Referenz eingehen. Das ist der
   ernsteste Punkt des Befunds — er betrifft die Vertrauensstufen, nicht nur die Anzeige.

### Vorschlag

- **Bilder unabhängig von `pages` auflösen.** Fällt die Seitenliste weg, `metadata.images`
  als Rückfallebene verwenden. Dann bleibt das Faksimile sichtbar, und der Ausfall lässt
  sich am Bild überhaupt erst beurteilen.
- **Ehrliche Fehlermeldung** statt „Kein Bild verfügbar": ein eigener Zustand
  „Transkription fehlgeschlagen — Neulauf nötig", verlinkt auf die Fehlerliste. `needs_review`
  ist hier die falsche Kategorie: es ist kein Sichtungsfall, sondern ein Pipelinefehler.
- **Freigabe sperren, solange keine Seiten da sind.** Guard in `handle_approve()` und
  `handle_edit()`, dazu ein Test in `tests/test_trust_tiers.py`, der festhält, dass ein
  Objekt ohne `pages` keinen Review-Status annehmen kann.
- **Katalog:** solche Objekte als eigene Kategorie führen statt sie unter `needs_review` zu
  mischen — `pipeline/quality_report.py` meldet den Fall bisher gar nicht.

---

## 2 — Abbildungen werden in eckigen Klammern beschrieben, ohne dass es dafür eine Regel gibt

Gemeldet von Julia Hintersteiner, 2026-10-02 · Status: offen — **editorische Entscheidung nötig**

### Symptom

Enthält eine Seite eine Abbildung, schreibt das Modell eine eigene Bildbeschreibung in eckigen
Klammern in die Transkription. Die gedruckte Bildunterschrift folgt darunter noch einmal als Text:

```text
[Abbildung: The Slum von James Pryde]     ← Beschreibung des Modells, steht nicht auf dem Blatt
The Slum James Pryde                      ← gedruckte Bildunterschrift
```

### Reproduktion

**I Seek in Shadow** (*Readers News*, Mai 1940), SZ-AAP/W-AA92.1, `o:szd.2538`, Seite 3
→ `http://localhost:8000/#view/o_szd.2538_gemini-3.1-flash-lite-preview/3`

Dasselbe Objekt hat 12 solche Klammern auf 11 Seiten. Auf Seite 11 wiederholt die Klammer die
Bildunterschrift wörtlich (`[Abbildung: Robert Louis Stevenson, after a bronze relief …]` und
darunter derselbe Text).

### Ursache

Es gibt keine Regel. Der System-Prompt definiert nur `[?]`, `[...]`, `~~…~~` und `{…}`
(`pipeline/prompts/system.md:12-13`), keiner der neun Gruppen-Prompts erwähnt Abbildungen, und das
Annotationsprotokoll regelt sie ebenfalls nicht (`knowledge/annotation-protocol.md` §3, §4). Das
Modell erfindet die Notation selbst. Einzige Erwähnung von Bildunterschriften im Repo ist der
Layout-Prompt für Zeitungsausschnitte (`pipeline/prompts/layout_group_h_zeitungsausschnitt.md:38`),
der die Transkription nicht betrifft.

### Umfang

Bildbeschreibungen (`[Abbildung: …]`, `[Bild: …]`, `[Bildunterschrift: …]`, `[Logo: …]`,
`[Grafik: …]`, `[Vignette …]`): **68 Klammern in 17 Objekten**, davon 14 in der Aufsatzablage
(Zeitungs- und Zeitschriftendrucke), dazu `o:szd.846`, `o:szd.1263` (Korrespondenz) und `o:szd.149`.
Die meisten in `o:szd.2584` (30) und `o:szd.2538` (12).

Die Form ist uneinheitlich: `Abbildung`, `Bild` und `Bildunterschrift` stehen nebeneinander,
mal mit Doppelpunkt, mal ohne. In englischen Texten beschreibt das Modell auf Deutsch
(„The Slum **von** James Pryde").

Das ist ein Ausschnitt eines größeren Musters. Für andere Sachverhalte erfindet das Modell
ebenfalls Klammern, die nicht definiert sind, etwa `[Unterschrift]` / `[Unterschrift unleserlich]` /
`[Unterschrift: H. Heumann?]` (169 Klammern in 112 Objekten), `[eingefügt …]` (74 in 20 Objekten),
`[Randnotiz links: …]` (50 in 26), `[Adressseite]`, `[durchgestrichen]`. Definiert sind davon nur
`[Stempel:]`, `[Poststempel:]`, `[Marginalie:]` und `[quer:]`/`[kopf:]`.

### Folgen

1. **Echter Text wird als Beschreibung getarnt.** Teils steht die gedruckte Bildunterschrift
   *in* der Klammer statt darunter: `[Bildunterschrift: Albert Welti - Züricher Legende]`
   (`o:szd.2286`), `[Abbildung: Im Park von Veitshöchheim. Phot. Rupp.]` (`o:szd.2353`),
   die ganze Bildlegende in `o:szd.2749` und `o:szd.2750`. Wer die Klammer als Zusatz des Modells
   liest und löscht, löscht Text vom Blatt.
2. **Widerspricht dem diplomatischen Prinzip.** Die Klammer ist Text, der nicht auf dem Blatt
   steht, und sie ist von einer editorischen Auszeichnung nicht zu unterscheiden.
3. **CER.** `pipeline/evaluate.py:42-43` entfernt nur `[Stempel:]` und `[Marginalie:]` vor dem
   Vergleich. Je nachdem, ob die korrigierende Person die Klammer stehen lässt oder löscht,
   entsteht eine Abweichung, die als Lesefehler zählt.
4. **TEI-Export.** Der Marker-Konverter erkennt nur `[Stempel:]`, `[Poststempel:]`,
   `[Marginalie:]` und `[quer:]`/`[kopf:]` (`pipeline/marker_enrich.py:60-62`). Bildbeschreibungen
   landen als Fließtext im `<body>`, statt als `<figure>`/`<figDesc>`.
5. **Beim Redigieren unklar, was zu tun ist.** Ohne Regel wird jede Person anders verfahren.

### Vorschlag

Zuerst eine Regel festlegen, dann umsetzen:

- **Eine feste Form**, z. B. `[Abbildung: kurze Beschreibung]`, immer deutsch, allein auf einer
  Zeile an der Stelle der Abbildung, analog zu `[Stempel:]`.
- **Die Bildunterschrift steht nie in der Klammer**, sondern als normaler Text darunter, weil sie
  auf dem Blatt steht.
- Ob überhaupt beschrieben wird oder nur `[Abbildung]` ohne Inhalt: beides ist vertretbar. Eine
  leere Marke hält die Transkription diplomatisch und spart dem Modell das Erfinden.
- `[Unterschrift]` und die übrigen erfundenen Klammern in derselben Entscheidung mitregeln.
- Dann umsetzen in: `knowledge/annotation-protocol.md` (§3/§4, Richtlinien-Panel im Viewer),
  `pipeline/prompts/system.md`, `pipeline/evaluate.py` (Normalisierung), `pipeline/marker_enrich.py`
  (→ `<figure><figDesc>`).

**Bis zur Entscheidung beim Redigieren:** Klammern stehen lassen, nur die echte Bildunterschrift
prüfen. Steckt die Bildunterschrift in der Klammer, sie als normalen Text herausnehmen.

---

<!-- Neue Befunde hier anhängen, Nummerierung fortlaufend.

## 2 — <Kurztitel>

Gemeldet von <Name>, <Datum> · Status: offen

### Symptom
### Reproduktion
### Ursache
### Umfang
### Folgen
### Vorschlag

-->
