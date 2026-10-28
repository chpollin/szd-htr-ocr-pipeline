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

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-08-26 · Status: teilweise behoben — **Anzeige behoben in** `624c6e0` (2026-10-19), Freigabe-Sperre und Katalog-Kategorie offen

> **Nachtrag 2026-10-19.** Erneut aufgefallen an `o:szd.202` („A great lesson from a great man“,
> 13 Scans). Nach dem Salvage vom 2026-09-25 sind noch **16 Objekte** betroffen, nicht mehr 34.
> `build_viewer_data.py` legt für ein Objekt ganz ohne Seiten jetzt je Scan einen Platzhalter
> `"Nicht transkribiert: …"` an. Der Viewer zeigt damit alle Faksimiles mit dem vorhandenen Badge
> „Nicht transkribiert“ statt „Kein Bild verfügbar“. `results/` ist unverändert. Offen bleiben
> aus dem Vorschlag unten der Guard in `handle_approve()`/`handle_edit()` und die eigene
> Katalog-Kategorie. Den Text liefert erst ein Neulauf (API-Key + Backup).

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

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-10-02 · Status: offen — **editorische Entscheidung nötig**

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

## 3 — Text, der in Detailaufnahmen am Bildrand abgeschnitten ist, wird aus anderen Bildern ergänzt

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-10-19 · Status: offen — **editorische Entscheidung nötig**

### Symptom

Im Faksimile ist der Text am Bildrand abgeschnitten, die Transkription schreibt die Wörter aber
vollständig aus. Teils stehen ganze Sätze in der Transkription, von denen auf dem Bild nur das Ende
zu sehen ist.

### Reproduktion

**Bankkontoauszüge Bayerische Vereinsbank**, SZ-AP2/L-S7.6, `o:szd.1056`, Seiten 2–7
→ `http://localhost:8000/#view/o_szd.1056_gemini-3.1-flash-lite-preview/2`

Die Kontoauszüge sind lange Querstreifen. Bild 1 zeigt den ersten Auszug ganz, die Bilder 2–7 sind
Detailaufnahmen der linken und rechten Hälfte von drei Auszügen. Das Modell beschreibt sie in den
Notizen selbst als „Ausschnitt des Kontoauszugs (linke Seite)“.

| Seite | Auf dem Bild sichtbar | Transkription |
|---|---|---|
| 2 | `Uebertr.a.Kto.Oesterrei` | `Uebertr. a. Kto. Oesterreich` |
| 2 | `Das Konto ist hiermit ausgegl` | `Das Konto ist hiermit ausgeglichen` |
| 3 | `…en Halb- und Vierteljahres-Auszüge.` / `…ppe —` | beide Sätze vollständig, `– Blatt für die Sammelmappe –` |
| 3 | Wortreste `ch`, `ihen` | fehlen |

Dazu kommt eine Normalisierung: Auf dem Blatt steht der Tippfehler **„ausgeglihen“** (Bild 1 und 3),
die Transkription schreibt „ausgeglichen“.

### Ursache

- **Alle Bilder eines Objekts gehen in einem Aufruf an das Modell** (bis `CHUNK_SIZE` = 20). Das
  Modell sieht die andere Hälfte und die Gesamtaufnahme und setzt den Text daraus zusammen, statt
  das einzelne Bild zu transkribieren.
- **Es gibt keine Regel für Text am Bildrand.** Weder `pipeline/prompts/system.md` noch ein
  Gruppen-Prompt noch `knowledge/annotation-protocol.md` sagen, was mit angeschnittenem Text zu tun
  ist.
- Der Objekt-Prompt `pipeline/prompts/objects/o_szd.1056.md` verlangt zusätzlich, die Buchungen als
  Markdown-Tabelle neu aufzubauen. Das lädt zum Rekonstruieren ein.

### Umfang

Nicht vollständig erhoben. In den Seitennotizen beschreibt das Modell **318 Seiten in 187 Objekten**
selbst als Ausschnitt, Detail- oder Teilaufnahme (Suche nach `Ausschnitt des/der/von/aus`,
`Detailaufnahme`, `Detailansicht`, `Teilaufnahme`, ohne „Zeitungsausschnitt“). Bei **26 Seiten in
24 Objekten** erwähnt die Notiz ausdrücklich abgeschnittenen Text oder den Bildrand. Ob dort jeweils
ergänzt wurde, ist nicht einzeln geprüft.

### Folgen

1. **Die Transkription gibt nicht wieder, was auf dem Scan steht**, und der Unterschied ist nicht
   markiert. Beim Gegenlesen Bild gegen Text wirkt das wie ein Lesefehler.
2. **Doppelte Textmenge.** Der ergänzte Text steht auf der Detailseite und auf der Gesamtaufnahme
   noch einmal. Das verfälscht Zeichenzahlen und eine spätere Volltextsuche.
3. **Normalisierung nebenbei** („ausgeglihen“ → „ausgeglichen“) verletzt das diplomatische Prinzip.

### Vorschlag

Zuerst entscheiden, dann umsetzen:

- **(a) Nur das Sichtbare**, angeschnittene Wörter markiert, z. B. `Oesterrei[...]`. Das ist streng
  diplomatisch je Scan.
- **(b) Ergänzen zulassen, aber kenntlich machen**, wenn der Text auf einem anderen Scan desselben
  Objekts belegt ist.
- Danach eine Zeile in `system.md` (Regeln) und in §3 des Annotationsprotokolls; der Objekt-Prompt
  von `o:szd.1056` sollte die Detailaufnahmen ausdrücklich erwähnen.

---

## 4 — Inhaltlich falscher Text bei Konfidenz „high“, ohne dass ein Signal anschlägt

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-10-19 · Status: offen

### Symptom

Die Transkription liest sich flüssig, weicht aber über weite Strecken vom Faksimile ab: Wörter
werden durch plausible andere ersetzt, Satzteile umgedichtet oder weggelassen. Das Objekt steht
trotzdem auf `confidence: high` und `needs_review: false`.

### Reproduktion

**Drei Briefe Elisabeth Lensings an Christine Hebbel**, SZ-AAP/W-AA24.1, `o:szd.2745`, Seite 1
(Fraktur-Druck) → `http://localhost:8000/#view/o_szd.2745_gemini-3.1-flash-lite-preview/1`

| Faksimile | Transkription |
|---|---|
| die beiden Genien seiner Jugend | die beiden Gatten seiner Jugend |
| — wie Hebbel selbst … nannte | und wo Hebbel selbst … nannte |
| erhebend und begütigend | erhebend und beglückend |
| Widerstreit | Biederstreit |
| reine Elemente der Verklärung finden können | neue Wurzeln der Liebe, neue Boden-Lösung |
| der Zuversicht, mahnt ihn, zu bleiben, Verehrung | des Ansehens, nimmt sich, in Mitleid, in Schwung |
| Eine andere Frau hat seit zehn Jahren sein Leben gestaltet | Eine andere Frau, das Schicksal, in dem sein Leben gebettet |
| Elisabeth Lensing. Zwei Kinder hat sie ihm geboren | Hebbel, dem seine Liebe, Mutter der sie ihm geboren |

Schwächer dasselbe bei **Die Autographensammlung als Kunstwerk**, SZ-AAP/W-AA11.3, `o:szd.2759`,
Seite 1 (Fraktur-Druck):

| Faksimile | Transkription |
|---|---|
| solchen Mißtrauischen zu erklären | solchen Misstrauens zu erklären |
| geradezu ein Gegenteiliges sind | geradezu gegenteiliges sind |
| unter seinen Schriftzügen der automatischste | unter seinen Schriftzügen automatischste |
| von irgendeiner berühmten Feder | von irgendeiner Feder |

Und in Handschrift bei **Worte am Sarge Sigmund Freuds [Fragment I]**, `o:szd.263`, Seite 1:

| Faksimile | Transkription |
|---|---|
| Siegmund Freuds (Titel) / die Siegmund Freud | Sigmund (normalisiert) |
| im Namen seiner Wiener, seiner österreichischen ~~[gestr.]~~ {seiner Weltfreunde} | im Namen seiner {seiner weltfremden[?]} ~~seiner~~ seiner österreichischen ~~Freunde~~ |

„Weltfreunde“ → „weltfremden“ kehrt den Sinn um, „Wiener“ fehlt.

### Ursache

- **Bekannte Schwäche, schwerere Form.** CLAUDE.md nennt „Nonsens-Halluzination“. Hier entsteht
  kein Nonsens, sondern ein stilistisch passender Text. Gerade das macht ihn beim Überfliegen
  unauffällig.
- **Gruppe passt nicht zum Material.** `o:szd.2745` und `o:szd.2759` laufen als Gruppe F
  (Korrekturfahne). Der Prompt beschreibt den Basistext als „Gedruckter Basistext (Antiqua)“
  (`pipeline/prompts/group_f_korrekturfahne.md:12`), beide sind Fraktur-Drucke.
- **Kein Signal deckt das ab.** Die `quality_signals` messen Länge, Marker, Duplikate und Sprache.
  Ein flüssiger, gleich langer, gleichsprachiger Ersatztext löst keines davon aus. Die
  Modell-Konfidenz diskriminiert ohnehin nicht (CLAUDE.md, „Technische Entscheidungen“).

### Umfang

Drei Objekte am Faksimile belegt. Wie verbreitet das ist, lässt sich von hier aus nicht erheben,
weil kein Signal es anzeigt. Am ehesten betroffen sind Fraktur-Drucke in der Aufsatzablage und
den Werken.

### Folgen

1. **Eine Freigabe nach Überfliegen würde falschen Text als „Mensch-geprüft“ ausweisen.** Das
   Review-Modell setzt voraus, dass Approve heißt: gegengelesen.
2. **`needs_review` ist als Triage für diese Fehlerklasse wertlos.** Ungeprüfte Objekte ohne
   Flag sind nicht „wahrscheinlich gut“.
3. **Seite 1 von `o:szd.2745` braucht eher eine Neutranskription als Einzelkorrekturen.**

### Vorschlag

- **Modellkonsensus (`verify.py`) gezielt auf Fraktur-Drucke anwenden.** Paraphrasen eines Modells
  wiederholt ein zweites Modell selten wörtlich; eine hohe CER zwischen beiden ist hier das
  brauchbarste Signal.
- **Gruppe F um Fraktur ergänzen** oder Fraktur-Fahnen der Gruppe H/B zuordnen, deren Prompts
  Fraktur kennen.
- **Neulauf** von `o:szd.2745` (mindestens Seite 1).

---

## 5 — Randnotizen, Bleistiftzusätze und Stempel fehlen im Transkriptionstext

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-10-19 · Status: offen — **Widerspruch zwischen Prompts und Annotationsprotokoll**

### Symptom

Handschriftliche Zusätze außerhalb des Haupttextes, vor allem schwacher Bleistift am Seitenanfang
oder am Rand, fehlen in der Transkription. Sie stehen höchstens in der Seitennotiz des Modells,
die im Viewer nur als kleine graue Zeile „VLM-generierte Seitenbeschreibung“ erscheint. Stempel
werden mal transkribiert, mal nicht.

### Reproduktion

| Objekt | Was fehlt | Wo es steht |
|---|---|---|
| `o:szd.2745`, S. 1 | Bleistiftvermerk oben, Lesevorschlag: „Um rechtzeitige Retournierung [?] / ersucht höfl. / Die Druckerei“ | nirgends; die Notiz nennt stattdessen eine blaue „2“ (vermutlich der blaue Korrekturstrich) |
| `o:szd.2759`, S. 1 | Bleistiftnotiz senkrecht am rechten Rand | nur Notiz: „Proben an den Leipziger Verlag, [?] [?] [?]“ |
| `o:szd.2759`, S. 1 | Druckereistempel „…schel & … Buchdruckerei Leipzig, Seeburgstrasse 57“ mit „III 1 5“ (blau), Datumsstempel „11 SEP 1912“ | nirgends |
| `o:szd.263`, S. 1 | Bleistift „gesprochen am“ vor der Datumszeile, mit Bogen zur Klammer vor „26“ | nirgends; die Notiz nennt nur „Korrekturen in … Bleistift“ |

Die Lesungen sind Vorschläge vom Faksimile und noch gegenzulesen.

### Ursache

Zwei Regelwerke widersprechen sich:

- **Annotationsprotokoll** (`knowledge/annotation-protocol.md`): §3.5 transkribiert Marginalien, die
  zum Dokumentinhalt gehören, mit `[Marginalie:]`; §4.2 transkribiert Datums-, Eingangs- und
  Behördenstempel als `[Stempel: …]`. Nur moderne Bibliotheksstempel bleiben weg.
- **Prompts:** `group_c_formular.md:19` („Stempel und Siegel in den Notizen, nicht im
  Transkriptionstext“), `group_i_korrespondenz.md:24` (Poststempel nur in den Notizen),
  `group_h_zeitungsausschnitt.md:24` (handschriftliche Annotationen nur in den Notizen). Der
  Korrekturfahnen-Prompt, der bei `o:szd.2745` und `o:szd.2759` greift, kennt nur Korrekturen,
  keine Vermerke und keine Stempel. Gleichzeitig verlangt `system.md:17`, Gedrucktes und
  Handschriftliches „gleichermaßen“ zu transkribieren.

`evaluate.py:42-43` und `marker_enrich.py:23-25` sind auf die Protokoll-Form (`[Stempel:]`,
`[Marginalie:]`) eingestellt, das Modell bekommt sie aber nicht vorgegeben.

### Umfang

„Stempel“ steht im Transkriptionstext auf **rund 90 Seiten** (enthält einzelne Falschtreffer wie
„stempelte“) und nur in den Notizen auf **rund 760 Seiten**, davon 683 in der Korrespondenz. Ein
Beispiel mit transkribiertem Stempel: `o:szd.3087` („[Stempel oben links:] AMERICAN …“, eigene
Schreibweise statt `[Stempel:]`). Fehlende Randnotizen lassen sich ohne Bildvergleich nicht zählen.

### Folgen

1. **Inhalt geht verloren**, der für die Überlieferung zählt: Druckereivermerke und -stempel
   datieren Fahnen (`o:szd.2759`: 11. September 1912), „gesprochen am“ gehört zum Titel der Rede.
2. **Uneinheitlich beim Redigieren.** Ob ein Stempel im Text steht, hängt von Gruppe und Zufall ab;
   Redigierende müssen raten, welche Form gilt.
3. **CER gegen menschliche Referenz** zählt jeden nach Protokoll ergänzten Stempel als
   Modellfehler.

### Vorschlag

- **Prompts an das Protokoll angleichen:** In `system.md` eine Regel für `[Marginalie:]`,
  `[Stempel: …]` und `[quer:]`; die gegenteiligen Zeilen in den Gruppen C, H und I ersetzen;
  Gruppe F um Vermerke (Druckerei, Setzer) und Stempel ergänzen. Wirkt erst bei einem Neulauf.
- Oder bewusst umgekehrt entscheiden (Stempel nur in Notizen) und das Protokoll anpassen.
  Wichtig ist, dass es eine Regel ist.
- **Bis dahin beim Redigieren:** fehlende Zusätze in Protokollform nachtragen
  (`[Marginalie:] …`, `[Stempel: …]`).

---

## 6 — Keine Notation für Umstellungen und Korrekturzeichen des Setzers

Gemeldet von der Projekt-Reviewerin (Universität Salzburg), 2026-10-19 · Status: offen — **editorische Entscheidung nötig**

### Symptom

Eine eingekringelte Wortgruppe mit Versetzungslinie wird nicht als Umstellung erkannt. Die
Transkription setzt nur eine öffnende Klammer, wo der Kringel beginnt.

### Reproduktion

**Die Autographensammlung als Kunstwerk**, SZ-AAP/W-AA11.3, `o:szd.2759`, Seite 1
→ `http://localhost:8000/#view/o_szd.2759_gemini-3.1-flash-lite-preview/1`

Im Faksimile ist „alles und das Wichtigste“ eingekringelt; eine Linie führt zu einer Einfügemarke
nach „Unterschrift,“, am Rand steht das Zeichen „L“. Korrigiert lautet der Satz:

```text
denn diesen Dilettanten ist ein Schriftzug die bloße Unterschrift, alles und das Wichtigste,
die dem wahren Sammler beinahe das wesenloseste wird
```

Die Transkription:

```text
die bloße Unterschrift, die dem wahren Sammler (alles und das Wichtigste
beinahe das wesenloseste wird,
```

In derselben Passage fehlt das Korrekturzeichen im Wort „automatischste“ (Randvermerk „/ e“).

### Ursache

Der System-Prompt kennt nur `[?]`, `[...]`, `~~…~~` und `{…}`. Der Korrekturfahnen-Prompt erwähnt
„Korrekturzeichen des Setzers oder Lektors“ (`group_f_korrekturfahne.md:15`), sagt aber nicht, wie
sie wiederzugeben sind. Das Annotationsprotokoll regelt Umstellungen nicht.

### Umfang

Ein Fall belegt. Betroffen ist potenziell jede Korrekturfahne: 43 in den Werken, 10 in der
Aufsatzablage (laut `group_f_korrekturfahne.md`).

### Folgen

1. **Die Klammer ist falsch und irreführend.** Sie sieht aus wie Text vom Blatt.
2. **Die Korrekturschicht einer Fahne geht verloren.** Gerade sie ist der editorische Wert einer
   Korrekturfahne.

### Vorschlag

- **Notation festlegen**, mindestens für Umstellung; Randzeichen des Setzers (`L`, `/ e`) entweder
  mitregeln oder ausdrücklich ausschließen.
- **Mit den vorhandenen Zeichen** lässt sich eine Umstellung schon jetzt abbilden: am Zielort
  `{alles und das Wichtigste,}`, am Ursprungsort `~~alles und das Wichtigste~~`, dazu eine Notiz
  „Umstellung durch Korrekturzeichen“. So beim Redigieren vorgehen, bis entschieden ist.
- Danach `group_f_korrekturfahne.md`, Annotationsprotokoll §3 und `marker_enrich.py`
  (→ TEI `<transpose>`) nachziehen.

---

<!-- Neue Befunde hier anhängen, Nummerierung fortlaufend.

## 7 — <Kurztitel>

Gemeldet von <Name>, <Datum> · Status: offen

### Symptom
### Reproduktion
### Ursache
### Umfang
### Folgen
### Vorschlag

-->
