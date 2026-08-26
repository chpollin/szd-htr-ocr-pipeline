# Fehlersammlung Review — Befunde aus dem Redigieren

> Fertiger Issue-Text zum Anlegen unter
> https://github.com/chpollin/szd-htr-ocr-pipeline/issues/new
> Titel: **Fehlersammlung Review — Befunde aus dem Redigieren**
> Vorschlag Labels: `bug`, `viewer`, `review`

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
→ http://localhost:8000/#view/o_szd.2491_gemini-3.1-flash-lite-preview/1

### Die Bilder fehlen nicht

GAMS liefert die Faksimiles einwandfrei — geprüft am 2026-08-26:

```
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
