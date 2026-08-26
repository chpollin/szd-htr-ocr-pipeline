# Totalausfaelle der Transkriptionspipeline — 34 Objekte ohne verwertbares Ergebnis

Stand: 2026-08-26 · Erhoben von Julia Hintersteiner aus `results/*/*_gemini-3.1-flash-lite-preview.json`
(Commit `0001f9e`) · Modell: `gemini-3.1-flash-lite-preview`

Bei diesen 34 Objekten hat die Pipeline **keine einzige Seite** erzeugt: `result` enthaelt nur
`raw`, kein `pages`-Array. Sie sind im Viewer als `needs_review` markiert, lassen sich aber nicht
redigieren — es gibt keinen Text zu korrigieren. Sie brauchen einen **Neulauf**, keine Sichtung.

Der Befund ist derselbe Mechanismus, der in `reports/aal-review-triage.md` fuer `o_szd.3135` und
`o_szd.3375` dokumentiert ist (Commit `a96cd7f`, "Neulauf der 2 Runaway-Objekte"). Die Klasse ist
also bekannt — neu ist, dass sie ueber alle vier Sammlungen hinweg 34 Objekte betrifft.

## Zusammenfassung

- Betroffene Objekte: **34** von 2.452 (1,4 %), zusammen **836 Faksimile-Scans**
- Vollstaendigkeit: Ein Scan aller 2.452 Ergebnis-JSONs findet **genau diese 34** mit `result.raw`
  bzw. ohne `pages`. Es gibt keine weiteren Totalausfaelle, und keines der 34 traegt einen Review-Status.
- **300 Seiten sind ohne neuen API-Call aus den Rohdaten rekonstruierbar** (187 davon mit Text,
  der Rest sind korrekt erkannte Leerseiten) — siehe "Salvage".

| Sammlung | Objekte | Scans |
|---|---|---|
| lebensdokumente | 5 | 252 |
| werke | 7 | 483 |
| aufsatzablage | 10 | 60 |
| korrespondenzen | 12 | 41 |
| **Summe** | **34** | **836** |

## Vier Ausfallarten

| Art | Objekte | Was passiert ist |
|---|---|---|
| Schleife in Markup-Zeichen | 28 | Das Modell geraet mitten in einem JSON-String in eine degenerierte Wiederholung einer kurzen Zeichenfolge und produziert sie bis zum Abbruch. Der String wird nie geschlossen, deshalb schlaegt jede der fuenf Sanitisierungsstufen in `parse_api_response()` fehl. |
| Schleife in einer Textphrase | 1 | Gleicher Mechanismus, aber die Wiederholungseinheit ist ein ganzer Satzteil (72 Zeichen). Nur `o_szd.2333`: "…die den Deutschen diese Idee der Einheit eine schon eingeborene ist, …" wiederholt sich ueber 97 % der Antwort. |
| Leere Antwort | 4 | Die API liefert einen leeren String zurueck (`raw` ist `""`). Kein Inhalt, kein Fehler. |
| Abbruch ohne Schleife | 1 | Nur `o_szd.1886`: die Antwort endet nach 234 kB mitten im Wort ("So nahm ich mir eine kleine Woh"), ohne Wiederholung. Klassische Truncation — inhaltlich ist die Antwort bis dahin einwandfrei. |

Aufschlussreich ist, *was* in den 29 Schleifen wiederholt wird. In 28 von 29 Faellen ist es kein
Fliesstext, sondern Leerraum oder ein Markup-Zeichen der Transkriptionskonvention:

| Wiederholte Sequenz | Objekte | Bedeutung im Annotationsschema |
|---|---|---|
| `\n`, `\t` | 10 | Zeilenumbruch / Tabulator |
| `[...]` | 7 | unleserliche Stelle |
| `[?]` | 6 | unsichere Lesung |
| `~~ ~~` | 3 | Streichung |
| `.` | 2 | Punktfolge (Trennlinien, Auslassungen) |
| Satzteil | 1 | — (`o_szd.2333`) |

Das Modell kippt also genau dort in die Schleife, wo das Annotationsschema selbst eine legitime
Wiederholung vorsieht: leere Seiten (`\n`), schwer lesbare Passagen (`[?]`, `[...]`) und
durchgestrichene Absaetze (`~~ ~~`). Das deckt sich mit dem in `reports/aal-review-triage.md`
fuer `o_szd.3375` beschriebenen Ausloeser — dort waren es die gepunkteten Trennlinien `-.-.-.-`
einer Klageschrift. Der Ausfall ist damit kein Zufallsrauschen, sondern an Materialeigenschaften
gebunden: er trifft bevorzugt schwer lesbare Handschrift und leerseitenreiche Konvolute.

## Salvage: 300 Seiten sind ohne API-Call zu retten

Bei den meisten Objekten ist der Anfang der Antwort valides JSON — die Schleife setzt erst spaeter
ein. Zaehlt man die vollstaendig geschlossenen `{"page": …, "transcription": …, "notes": …}`-Objekte
im Prefix, ergeben sich **300 verwertbare Seiten, davon 187 mit Text**. Vier Objekte tragen den
Grossteil:

| Objekt | Scans | Seiten im Prefix | davon mit Text | Anteil der Scans |
|---|---|---|---|---|
| `o_szd.1886` | 175 | 170 | 85 | 97 % |
| `o_szd.267` | 232 | 64 | 41 | 28 % |
| `o_szd.77` | 95 | 26 | 24 | 27 % |
| `o_szd.70` | 91 | 15 | 15 | 16 % |
| `o_szd.76` | 60 | 5 | 5 | 8 % |

Stichprobe `o_szd.1886` ("My three lives", Typoskript, 175 Scans): Die 170 rekonstruierbaren
Seiten sind luecken- und reihenfolgetreu (Seite 1–170), enthalten 211.623 Zeichen und lesen sich
sauber. Dieses eine Objekt ist der groesste Einzelposten des ganzen Befunds.

`parse_api_response()` in `pipeline/transcribe.py` (Zeilen 307–367) hat fuenf Reparaturstufen,
aber keine, die abgeschlossene Seitenobjekte aus einem abgeschnittenen Prefix uebernimmt.
Stufe 5 (`_extract_json_object`) schliesst offene Arrays mit `]`, kann aber einen offenen
String nicht schliessen — und genau darin steckt die Schleife.

## Empfehlung

1. **Sofort und ohne Kosten:** eine sechste Stufe in `parse_api_response()` — "vollstaendige
   Seitenobjekte aus dem Prefix uebernehmen, Rest als fehlend markieren" — und die 34 Rohdateien
   erneut durch den Parser schicken. Rettet 300 Seiten, kostet keinen API-Call.
2. **Neulauf mit kleinerem Chunk** fuer den Rest. Die grossen Objekte (`o_szd.267` 232 Scans,
   `o_szd.1886` 175, `o_szd.77` 95, `o_szd.70` 91) liegen weit ueber `CHUNK_SIZE = 20`;
   ein kleineres `--chunk-size` senkt die Schleifenwahrscheinlichkeit pro Call und begrenzt
   den Schaden, wenn doch eine auftritt.
3. **Ausgabelimit setzen:** In `transcribe.py` wird nur `temperature=0.1` gesetzt (Zeile 384),
   kein `max_output_tokens`. Ein explizites Limit schneidet die Schleife frueher ab und macht
   den brauchbaren Prefix zuverlaessig verfuegbar.
4. **Die vier leeren Antworten** (`o_szd.2230`, `o_szd.2256`, `o_szd.2307`, `o_szd.202`) sind der
   billigste Fall: mit `--force` neu laufen lassen.
5. **Erkennung dauerhaft einbauen:** `pipeline/quality_report.py` meldet diesen Fall bisher nicht.
   Ein Objekt ohne `pages` sollte als eigene Kategorie auffallen und nicht nur als `needs_review`
   im Katalog landen, wo es wie ein Sichtungsfall aussieht.

## Alle 34 Objekte

`Salvage` = vollstaendige Seitenobjekte im Prefix (in Klammern: davon mit Text).
`Schleife` = Anteil der Antwort, den die Wiederholung einnimmt.

### lebensdokumente (5)

| Objekt | Titel | Gruppe | Scans | Ausfall | Wiederholte Sequenz | Schleife | Salvage |
|---|---|---|---|---|---|---|---|
| `o_szd.77` | Notizen über Newyork 1935/1938 | Handschrift | 95 | Schleife | `[?] \n` | 79 % | 26 (24) |
| `o_szd.70` | Tagebuch in der Schweiz 1917 | Handschrift | 91 | Schleife | `[?] ` | 89 % | 15 (15) |
| `o_szd.76` | Notizbuch Paris 1936 | Handschrift | 60 | Schleife | `~~ ~~...` | 99 % | 5 (5) |
| `o_szd.121` | Vertrag Wydawnictwo J. Przeworskiego | Typoskript | 3 | Schleife | ` .` | 99 % | 0 |
| `o_szd.170` | Promotionskarte | Kurztext | 3 | Schleife | `\n` | 100 % | 0 |

### werke (7)

| Objekt | Titel | Gruppe | Scans | Ausfall | Wiederholte Sequenz | Schleife | Salvage |
|---|---|---|---|---|---|---|---|
| `o_szd.267` | Bau der Wiener Oper | Konvolut | 232 | Schleife | `[?] ` | 62 % | 64 (41) |
| `o_szd.1886` | My three lives (first draft) autobiography by S… | Typoskript | 175 | Abbruch | — | — | 170 (85) |
| `o_szd.1879` | The Marienbad Elegy | Typoskript | 25 | Schleife | `\n` | 100 % | 0 |
| `o_szd.311` | Marie Antoinette | Handschrift | 17 | Schleife | `[?] ` | 100 % | 0 |
| `o_szd.319` | Caput IV Eine Idee gewinnt Gewalt über einen Me… | Handschrift | 16 | Schleife | `~~~~~~ ` | 97 % | 1 (1) |
| `o_szd.202` | A great lesson from a great man | Handschrift | 13 | leer | — | — | 0 |
| `o_szd.209` | Moissi im Gespräch | Typoskript | 5 | Schleife | `~~xxxx~~ ` | 41 % | 0 |

### aufsatzablage (10)

| Objekt | Titel | Gruppe | Scans | Ausfall | Wiederholte Sequenz | Schleife | Salvage |
|---|---|---|---|---|---|---|---|
| `o_szd.2333` | Jakob Wassermann | Zeitungsausschnitt | 17 | Schleife (Phrase) | `\ngeborene ist, die den Deuts…` | 97 % | 2 (2) |
| `o_szd.2491` | Liebesbriefe | Handschrift | 7 | Schleife | `\n` | 100 % | 0 |
| `o_szd.2309` | Rückkehr zum Märchen. | Zeitungsausschnitt | 7 | Schleife | `\n` | 100 % | 0 |
| `o_szd.2422` | Méndez Pereira: Nuñez de Balboa | Typoskript | 5 | Schleife | `\n` | 89 % | 4 (4) |
| `o_szd.2230` | Ypern. | Zeitungsausschnitt | 5 | leer | — | — | 0 |
| `o_szd.2256` | Rabindranath Tagores "Sadhâna" | Zeitungsausschnitt | 5 | leer | — | — | 0 |
| `o_szd.2681` | Festliches Florenz. | Zeitungsausschnitt | 5 | Schleife | ` .` | 94 % | 1 (1) |
| `o_szd.2302` | Die Stimmung in Frankreich nach dem Siege und v… | Zeitungsausschnitt | 3 | Schleife | `[?] ` | 96 % | 0 |
| `o_szd.2307` | Jean Jacques Rousseau. Zu seinem 150. Todestag … | Zeitungsausschnitt | 3 | leer | — | — | 0 |
| `o_szd.2314` | "An Caliban". Epilog zu Shakespeares "Sturm". | Zeitungsausschnitt | 3 | Schleife | `[...]\n\n` | 93 % | 0 |

### korrespondenzen (12)

| Objekt | Titel | Gruppe | Scans | Ausfall | Wiederholte Sequenz | Schleife | Salvage |
|---|---|---|---|---|---|---|---|
| `o_szd.1418` | Brief an Friedrich Siegbert Mees vom 19. April … | Korrespondenz | 5 | Schleife | `[...]\n` | 100 % | 1 (1) |
| `o_szd.1461` | Brief an das International Copyright Bureau vom… | Korrespondenz | 5 | Schleife | `\n` | 98 % | 4 (2) |
| `o_szd.843` | Brief an Stefan Zweig vom 27. Januar 1937 | Korrespondenz | 4 | Schleife | `\t` | 99 % | 0 |
| `o_szd.1110` | Postkarte an Max Fleischer vom 24. Oktober 1902 | Korrespondenz | 3 | Schleife | `[...1...] ` | 100 % | 1 (1) |
| `o_szd.1535` | Brief an Stefan Zweig vom 30. September 1924 | Korrespondenz | 3 | Schleife | `\n` | 96 % | 1 (1) |
| `o_szd.1546` | Postkarte an Richard Friedenthal vom 3. Dezembe… | Korrespondenz | 3 | Schleife | `\n` | 100 % | 0 |
| `o_szd.1568` | Telegramm an Richard Friedenthal vom 1. Februar… | Korrespondenz | 3 | Schleife | `\n` | 100 % | 0 |
| `o_szd.1672` | Jüdischer Jugendverein an Stefan Zweig | Korrespondenz | 3 | Schleife | `[...]\n` | 100 % | 1 (1) |
| `o_szd.482` | Siegfried Trebitsch an Stefan Zweig, 1909 | Korrespondenz | 3 | Schleife | `[...]\n` | 100 % | 1 (1) |
| `o_szd.564` | Unidentified an Stefan Zweig, 1932-05-29 | Korrespondenz | 3 | Schleife | `[...]\n` | 100 % | 1 (1) |
| `o_szd.649` | Karl Ernst Henrici an Stefan Zweig, 1931-07-26 | Korrespondenz | 3 | Schleife | `[?] ` | 100 % | 1 (1) |
| `o_szd.937` | Baer an Stefan Zweig, 1928-08 | Korrespondenz | 3 | Schleife | `[...]\n` | 100 % | 1 (0) |

## Nebenbefund

Bei `o_szd.267` weichen zwei Zaehlungen in derselben Datei voneinander ab: `metadata.images`
listet 232 Scans, `quality_signals.input_images` sagt 107. Bei den anderen 33 Objekten stimmen
beide Werte ueberein. Ob der Lauf gedeckelt war (`--max-images`) oder die Zaehlung falsch ist,
liess sich aus der Ergebnisdatei nicht klaeren — vor dem Neulauf einmal ansehen.

## Reproduzieren

Die Liste der betroffenen Objekte:

```python
import json, glob
for fn in glob.glob("results/*/*_gemini-3.1-flash-lite-preview.json"):
    d = json.load(open(fn, encoding="utf-8"))
    if "raw" in (d.get("result") or {}):
        print(fn, len(d["result"]["raw"]))
```

Methode hinter den Tabellen oben, falls die Zahlen nachgerechnet werden sollen:

- **Schleifenerkennung:** kleinste Sequenz bis 200 Zeichen, die das Ende von `raw` durch
  Wiederholung fuellt (mindestens 3 Wiederholungen, Fenster 1.200 Zeichen). Die gefundene
  Einheit ist beliebig rotiert (`n\` und `\n` sind dieselbe Schleife) und wird fuer die
  Tabelle auf einen lesbaren Anfang gedreht.
- **Schleifenanteil:** Position, ab der die Einheit ununterbrochen bis zum Textende laeuft,
  geteilt durch die Gesamtlaenge von `raw`.
- **Salvage:** Anzahl der Treffer von `\{\s*"page"\s*:\s*\d+.*?"notes"\s*:\s*".*?"\s*\}`,
  die einzeln durch `json.loads()` gehen.
