---
title: "Review-Befunde"
aliases: ["Verbesserungsvorschlaege", "Findings"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
status: active
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
| [B-03](#b-03--lesereihenfolge-der-transkription-ist-nicht-geregelt) | Lesereihenfolge der Transkription ist nicht geregelt | **[J]** | offen |
| [B-04](#b-04--streichungen--was-machen-reviewerinnen-damit) | Streichungen — was machen Reviewer:innen damit? | **[J]** | in Klaerung |
| [B-05](#b-05--vordrucke-auf-briefpapier-werden-willkuerlich-erfasst) | Vordrucke auf Briefpapier werden willkuerlich erfasst | **[J]** | offen |
| [B-06](#b-06--ueberkorrektur-akzente-die-im-faksimile-nicht-stehen) | Ueberkorrektur: Akzente, die im Faksimile nicht stehen | **[J]** | offen |
| [B-07](#b-07--bug-im-filter-bild-text-mismatch-lassen-sich-keine-bilder-aufrufen) | **Bug:** im Filter "Bild-Text-Mismatch" laesst sich kein Faksimile aufrufen | **[J]** | Ursache belegt, Fix offen |
| [B-08](#b-08--label-vokabular-schriftart-und-funktionale-bloecke-markieren) | Label-Vokabular: Schriftart (gedruckt/handschriftlich) und funktionale Bloecke | **[J]** | Entwurf liegt vor, Entscheidung offen |

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

## B-03 — Lesereihenfolge der Transkription ist nicht geregelt

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | [[annotation-protocol]] §1 (Textfluss), `pipeline/prompts/system.md`, alle Gruppen-Prompts |
| **Status** | offen — Regel fehlt, muss formuliert und in den Prompt aufgenommen werden |

### Beobachtung **[J]**

Die Reihenfolge der Transkription ist mir nicht ganz verstaendlich. In diesem Fall SZ-AAP/B1.265 besonders ersichtlich. Es sollte eine Regel zur Transkription geben, so etwas wie von links nach rechts, von oben nach unten etc.

### Nachpruefung **[C]**

Belegt und reproduzierbar. SZ-AAP/B1.265 = `o:szd.1620`, Gruppe I (Korrespondenz), eine Postkarte mit zwei Seiten.

Auf **Seite 2** (Adressseite) liefert die Pipeline diese Folge:

```text
Absender: Otto J. Tressl / Wien III., Rennweg 50
Mr. Desmond Flower
Postkarte
Titl. Cassell & Company Ltd., London E.C. 4, La Belle Sauvage
```

`Postkarte` ist der gedruckte Kopftitel und steht auf dem Karton physisch **oben mittig** — in der Transkription erscheint er an dritter Stelle, zwischen zwei handschriftlichen Bloecken. Der Empfaengername (`Mr. Desmond Flower`) steht vor dem Wort `Titl.`, das ihn im Original einleitet. Weder "oben nach unten" noch "links nach rechts" noch "gedruckt vor handschriftlich" erklaert diese Folge; das Modell gruppiert offenbar semantisch (Absender → Empfaenger) und mischt den Vordruck ein, wo er gerade auffaellt.

**Ursache — Luecke, nicht Fehler:** Es gibt schlicht keine Vorgabe.

- `pipeline/prompts/system.md` regelt Zeilenumbrueche (Regel 2), aber keine Reihenfolge von Textbloecken.
- [[annotation-protocol]] §1 regelt Zeilenumbrueche, Silbentrennung, Absaetze und — als einzigen Reihenfolgefall — §1.4 mehrspaltigen Satz bei Zeitungsausschnitten (Gruppe H): "spaltenweise, links nach rechts, dann oben nach unten".
- Fuer alles andere (Briefe mit Randnotizen, Postkarten, Adressseiten, Briefkoepfe) ist die Reihenfolge undefiniert. Bei Gruppe I — mit 1.535 Objekten die groesste Gruppe — betrifft das praktisch jedes Objekt mit mehr als einem Textblock.

Das ist nicht nur Kosmetik: Die Reihenfolge geht direkt in die CER ein. Zwei zulaessige Anordnungen desselben korrekt gelesenen Textes erzeugen gegeneinander eine hohe CER, ohne dass ein einziges Zeichen falsch gelesen waere. Solange die Reihenfolge frei ist, misst die CER teilweise Anordnung statt Lesegenauigkeit.

### Vorschlag zur Diskussion **[C]**

Eine Regel in [[annotation-protocol]] §1 (neu: §1.6 Blockreihenfolge), gespiegelt in `system.md`, etwa:

1. **Grundregel:** Textbloecke in geometrischer Lesereihenfolge — oben nach unten, bei gleicher Hoehe links nach rechts. Das ist die Konvention, die auch PAGE XML mit `ReadingOrder` abbildet, also anschlussfaehig ans Zielformat.
2. **Ausnahmen explizit benannt und ans Blockende gestellt**, damit sie nicht im Fliesstext landen: Randnotizen, gedrehter Text (siehe die neue `[quer:]`-Konvention), Stempel, Vermerke.
3. **Gedruckter Vordruck** bleibt an seiner geometrischen Position — verbunden mit der Entscheidung aus B-05, ob er ueberhaupt transkribiert wird.
4. Ein Beispielblock in `group_i_korrespondenz.md` mit einer Adressseite, weil genau dort der Fehler entsteht.

Zu pruefen ist, ob die Regel als Prompt-Anweisung ueberhaupt greift — das Modell sieht das Bild, nicht die Koordinaten. Ein Vorher/Nachher-Vergleich an 5 Postkarten waere billig und wuerde es zeigen.

---

## B-04 — Streichungen: was machen Reviewer:innen damit?

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | [[annotation-protocol]] §3.3, `pipeline/marker_enrich.py`, Viewer-Leseansicht |
| **Status** | in Klaerung — Grundregel existiert, Praxisfaelle und Ausspielung fehlen |

### Frage **[J]**

Was machen wir mit Streichungen?

### Was bereits geregelt ist **[C]**

[[annotation-protocol]] §3.3 beantwortet den Grundfall: durchgestrichenen Text in `~~...~~` einschliessen und **vollstaendig transkribieren**, soweit lesbar; ist er unlesbar, `~~[...]~~`; die Intensitaet der Streichung (ein Strich, mehrfach ueberstrichen) wird **bewusst nicht** kodiert. Der TEI-Export macht daraus `<del>` ohne `@rend` (`marker_enrich.py` Schritt 4), und §5.4 haelt fest, dass der Inhalt fuer die Basis-CER **erhalten** bleibt — eine falsch gesetzte Streichung verschlechtert also nicht die Basis-CER, wohl aber die Markup-CER.

Dass diese Antwort trotzdem gefehlt hat, ist selbst der Befund: Das Protokoll liegt im Vault, nicht im Review-Workflow. Beim Gegenlesen im Viewer gibt es keinen Zugriff darauf — siehe Vorschlag unten.

### Was nicht geregelt ist **[C]**

Drei Faelle beantwortet §3.3 nicht, und alle drei kommen in den Daten vor:

1. **Ersetzung (Streichung + Einfuegung).** Zweig streicht ein Wort und schreibt das neue darueber. Das Protokoll kennt beide Marker einzeln, aber nicht ihr Verhaeltnis. Belegt: `o_szd.2268` — `das ~~verleugnete~~ {idealistische} Bekenntnis`. TEI haette dafuer `<subst><del/><add/></subst>`; `marker_enrich.py` erzeugt heute zwei unverbundene Elemente. **421 Seiten** zeigen dieses Muster.
2. **Fremde Hand.** Eine Streichung von spaeterer Hand (Lektorat, Archiv) ist etwas anderes als eine Autorkorrektur. Das Protokoll §4.5 verzichtet bewusst auf Haende-Zuweisung — fuer Streichungen ist das eine inhaltliche Aussage, die dadurch verloren geht.
3. **Ganzseitige Tilgung.** Ein Diagonalstrich ueber die ganze Seite ist keine Wortstreichung. Weder Marker noch `page.type` bilden das ab.

### Auszaehlung **[C]**

Ueber alle Ergebnis-JSONs: **28.745 Streichungen auf 1.274 Seiten in 421 Objekten**. Die Verteilung ist stark schief und legt Modellrauschen nahe:

| Befund | Wert | Einordnung |
|---|---|---|
| Streichungen gesamt | 28.745 | auf 1.274 Seiten in 421 Objekten |
| davon in `o_szd.75` allein (Notebook 1940) | 15.730 | **55 %** in einem einzigen Objekt |
| Top 5 Objekte | 21.742 | 76 % |
| Median pro Objekt | 2 | der Normalfall ist unauffaellig |
| Streichungen mit genau **einem** Wort | 27.516 | **96 %** |
| leere Streichungen `~~~~` | 71 | eindeutig Artefakt |
| mehrzeilige / unbalancierte Spans | 55 Seiten | bleiben im Export korrekt literal |

```bash
python -c "import json,re,pathlib,collections; per=collections.Counter(); [per.update({d.get('object_id'): (pg.get('transcription') or '').count('~~')//2}) for p in pathlib.Path('results').rglob('*.json') if not p.name.endswith(('_layout.json','_page.json')) for d in [json.loads(p.read_text(encoding='utf-8'))] for pg in (d.get('result') or {}).get('pages') or []]; print(sum(per.values()), per.most_common(5))"
```

Das 96-%-Muster bei Einzelwoertern gleicht dem, was `marker_enrich.py` fuer die geschweiften Klammern dokumentiert (~81 % der `{}` sind kein echtes Markup, sondern Wortsegmentierungs-Rauschen). Auszug aus `o_szd.75`, Seite 3: `E. [?] ~~auf~~ ~~ihren~~ ~~Leichtum~~, auf seine` — drei einzelne Woerter hintereinander gestrichen, dazu `leerlauf-\n~~dichten~~`, also eine Streichung mitten in einer Silbentrennung. Das sieht nach markierter Unsicherheit aus, nicht nach Tilgung.

**Nicht verifiziert:** Ob es sich wirklich um Rauschen handelt, laesst sich nur am Faksimile entscheiden — `o_szd.75` ist ein Notizbuch von 1940, und ein Notizbuch *darf* viele echte Streichungen haben. Die Auszaehlung ist ein Verdacht, kein Beweis. Eine Stichprobe von 10 Seiten aus `o_szd.75` wuerde es klaeren und ist der billigste naechste Schritt.

### Vorschlag **[C]**

1. **Kurzfristig, ohne Entscheidung:** Das Markup ist seit heute in der Leseansicht sichtbar ausgezeichnet (`docs/app.js`, `renderTranscription`) — gestrichener Text erscheint durchgestrichen statt als rohe `~~`-Zeichen. Damit ist beim Gegenlesen ueberhaupt erst erkennbar, was das Modell als Streichung gemeint hat.
2. **Protokoll ergaenzen** um die drei offenen Faelle oben, mindestens um die Ersetzung (§3.3a) — sie ist mit 421 Seiten der haeufigste und der einzige mit klarer TEI-Entsprechung.
3. **Praxisregel fuer Reviewer:innen** formulieren und im Viewer verlinken: Was tue ich, wenn das Modell eine Streichung erfunden hat (entfernen) und wenn es eine uebersehen hat (nachtragen)? Ohne diese Regel entscheidet jede Person anders, und die Markup-CER misst dann Reviewer-Varianz.
4. **`o_szd.75` gesondert pruefen**, bevor es in eine Auswertung eingeht — bei 55 % Anteil verzerrt dieses eine Objekt jede projektweite Markup-Statistik.

---

## B-05 — Vordrucke auf Briefpapier werden willkuerlich erfasst

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | [[annotation-protocol]] §4.3, `pipeline/prompts/group_i_korrespondenz.md` |
| **Status** | offen — Regel existiert nur fuer Gruppe C, nicht fuer Korrespondenz |

### Beobachtung **[J]**

Es wirkt auch etwas willkuerlich, weil teilweise (SZ-LAS/B1.57) beim Briefpapier Sachen transkribiert sind, aber nicht alles, was auf das Papier gedruckt ist.

### Nachpruefung **[C]**

Bestaetigt. SZ-LAS/B1.57 = `o:szd.1641`, Brief an Frans Masereel auf Briefpapier des Grand Pump Room Hotel, Bath. Seite 1 beginnt so:

```text
49, Hallamstreet W 1
TELEPHONE      TELEGRAMS
BATH 3266.     "PUMPOTEL, BATH"

GRAND PUMP ROOM HOTEL,
BATH.
Mon vieux, merci de ta lettre. …
```

Der Vordruck ist teilweise erfasst und in einer Reihenfolge, die dem Blatt nicht entspricht: Der Hotelname steht auf solchem Papier oben, die Telefon-/Telegrammzeile darunter — hier ist es umgekehrt, und `49, Hallamstreet W 1` (Zweigs eigene Londoner Adresse, handschriftlich) steht noch davor. Das ist zugleich ein Fall von B-03.

**Ursache:** Die Regel existiert, aber fuer die falsche Gruppe. [[annotation-protocol]] §4.3 sagt "Vorgedruckten Text und handschriftliche Eintragungen gleichermassen transkribieren" — ausdruecklich unter der Ueberschrift *"Gedruckte Formularfelder (Gruppe C: Formular)"*. Fuer Gruppe I (Korrespondenz, 1.535 Objekte) gibt es keine Entsprechung, und `group_i_korrespondenz.md` sagt zu Briefkoepfen nichts. Das Modell entscheidet daher pro Bild neu — daher die Willkuer.

### Offene Entscheidung — braucht **[J]**

Die Frage ist eine editorische, keine technische: **Gehoert der Briefkopf zum Dokumenttext?**

- **Dafuer:** Er ist Teil des Blattes, traegt Information (Ort, Datum, Aufenthalt Zweigs) und ist bei Korrespondenz oft der einzige Ortsbeleg. Das Protokoll verlangt an anderer Stelle (§4.2 Stempel) genau diese Logik: transkribieren, wenn Dokumentinhalt.
- **Dagegen:** Er ist gedruckte Massenware, nicht Zweigs Text, und blaeht jede Brieftranskription um 4–6 Zeilen auf, die in jeder CER-Rechnung mitlaufen.
- **Mittelweg (Vorschlag [C]):** transkribieren, aber ausgezeichnet — in der Art von `[Briefkopf: GRAND PUMP ROOM HOTEL, BATH]`, analog zu `[Stempel:]`. Damit ist er im Text vorhanden, im TEI als `<note type="letterhead">` abtrennbar und fuer die Basis-CER herausrechenbar. Das setzt allerdings voraus, dass das Label-Vokabular ueberhaupt festgelegt wird — siehe [[expert-in-the-loop]] §4: von 388 Label-Markern in den Daten konvertiert der Export heute nur 7 %.

---

## B-06 — Ueberkorrektur: Akzente, die im Faksimile nicht stehen

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | [[annotation-protocol]] §2.4/§2.6, [[evaluation-results]] (Fehlertypologie), `pipeline/prompts/system.md` Regel 7 |
| **Status** | offen — Fehlertyp benannt, aber nicht gemessen |

### Beobachtung **[J]**

Manchmal macht die Transkription auch Ueberkorrekturen, d.h. fuegt z.B. einen Accent ein, wo im Faksimile keiner ist (`déjeuner`).

### Einordnung **[C]**

Das ist ein eigener Fehlertyp und in der bestehenden Systematik nicht abgedeckt. [[annotation-protocol]] §2.6 warnt vor **Over-Historicization** (Levchenko 2025) — das Modell fuegt archaische Zeichen ein, die es nicht gibt (langes ſ). Der hier beobachtete Fehler ist die **Gegenrichtung**: Normalisierung auf die heutige Standardorthographie. §2.4 verbietet sie ("Beibehalten. Keine Modernisierung"), aber nur fuer deutsche Beispiele (`daß`, `Cadaver`, `Conflicte`); Diakritika in franzoesischen Passagen sind nicht genannt, und `system.md` Regel 7 bleibt allgemein ("keine Korrektur von Orthographie").

Der Fehler ist besonders unangenehm, weil er **plausibel** ist: `déjeuner` ist korrektes Franzoesisch, faellt beim Querlesen niemandem auf und ist nur am Faksimile widerlegbar. Er gehoert damit in dieselbe Kategorie wie die in CLAUDE.md dokumentierte Nonsens-Halluzination — nur schwerer zu entdecken.

Dass der Effekt in beide Richtungen laeuft, zeigt `o:szd.1641` (derselbe Brief wie B-05, Franzoesisch): in einem Text stehen nebeneinander `refugés`, `protegée`, `j'espere`, `presence`, `aujourdhui`, `n'etait` (ohne bzw. mit fehlenden Akzenten) und `délicieux`, `illustré`, `misère`, `ébraulé` (mit). Zweig schrieb Franzoesisch nachweislich akzentnachlaessig — **welche dieser Formen Zweigs Schreibung wiedergibt und welche das Modell veraendert hat, ist ohne Blick aufs Faksimile nicht entscheidbar.** Genau darin liegt der Aufwand.

### Vorschlag **[C]**

1. **Fehlertypologie ergaenzen** in [[evaluation-results]]: "Ueberkorrektur / Normalisierung" als eigener Typ neben Over-Historicization, mit dem Diakritika-Fall als Beispiel.
2. **Protokoll §2.4 erweitern** um eine Zeile zu Diakritika in fremdsprachigen Passagen: Akzent nur setzen, wenn im Faksimile sichtbar; im Zweifel weglassen und `[?]` anhaengen.
3. **Messbar machen:** Der Typ ist heute unsichtbar, weil kein Signal darauf anspricht und die Basis-CER ihn nur als einzelnes Zeichen zaehlt. Ein billiger Indikator waere die Akzentkonsistenz innerhalb eines fremdsprachigen Textes — sie sagt nichts ueber die Richtung, markiert aber die Objekte, bei denen sich das Hinsehen lohnt. Voraussetzung fuer eine echte Messung bleibt Ground Truth an franzoesischen Objekten.
4. **Nicht in den Prompt aufnehmen**, ohne es vorher zu messen: Eine Anweisung "setze keine Akzente, die nicht dastehen" kann genauso gut die Gegenrichtung verstaerken (Akzente weglassen, die dastehen). Erst messen, dann eingreifen.

---

## B-07 — Bug: im Filter "Bild-Text-Mismatch" lassen sich keine Bilder aufrufen

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | `pipeline/build_viewer_data.py:157`, `docs/data/*.json`, Viewer-Faksimilepanel |
| **Status** | Ursache belegt, Fix offen — zwei getrennte Probleme |

### Beobachtung **[J]**

Es gibt einen Error: Ich kann in der Kategorie "Bild-Text-Mismatch" keine Bilder aufrufen. Finde gerade nicht den Fehler auf Anhieb.

### Ursache **[C]** — belegt

Reproduziert. Der Filter "Bild-Text-Mismatch" (`page_image_mismatch`) enthaelt 36 Objekte. Bei **34 davon ist die Bildliste in den Viewer-Daten leer** — der Viewer hat schlicht keine URL, die er laden koennte, und zeigt "Kein Bild verfuegbar."

Bemerkenswert: Es sind projektweit **genau diese 34** Objekte, die ueberhaupt keine Bilder in den Viewer-Daten haben. Der Fehler trifft also nicht zufaellig diese Kategorie, sondern deckt sich exakt mit ihr.

**Es sind zwei uebereinanderliegende Probleme:**

**(1) Die Transkription ist leer — der eigentliche Datenfehler.** In den Ergebnis-JSONs dieser Objekte steht `result.pages: []` bei gleichzeitig vorhandenen `metadata.images`. Beispiel `o_szd.70`: 91 Faksimiles im Metadatensatz, **0** transkribierte Seiten. `quality_signals` erkennt das korrekt und setzt `page_image_mismatch` — das Signal funktioniert, es meldet einen fehlgeschlagenen Transkriptionslauf.

Betroffen sind 34 Objekte mit zusammen **836 Faksimiles**, verteilt auf alle vier grossen Sammlungen (korrespondenzen 12, aufsatzablage 10, werke 7, lebensdokumente 5) und quer ueber die Gruppen. Die groessten Ausfaelle sind `o_szd.267` (232 Bilder, Konvolut), `o_szd.1886` (175, Typoskript) und `o_szd.77` (95, Handschrift) — also gerade die aufwendigen Objekte, bei denen das Chunking greift.

**(2) Der Viewer wirft die Bilder weg — der sichtbare Fehler.** `pipeline/build_viewer_data.py:157` leitet die Bildliste aus den **Seiten** ab, nicht aus den Metadaten:

```python
page_images = [all_images[i] for i, _ in filtered if i < len(all_images)] if all_images else []
```

`filtered` entsteht aus `result.pages`. Sind dort null Seiten, ist `page_images` leer — obwohl `all_images` 91 Eintraege haelt. Die Kopplung ist fuer den Normalfall richtig (sie filtert Farbkarten-Seiten mit heraus), aber im Null-Seiten-Fall macht sie das Objekt **unpruefbar**: Man kann nicht gegenlesen, was man nicht sehen kann, und man kann nicht einmal feststellen, ob der leere Lauf berechtigt war.

Nachrechnen:

```bash
python -c "import json; d=json.load(open('docs/data/lebensdokumente.json',encoding='utf-8')); o=[x for x in (d['objects'] if 'objects' in d else d) if not x.get('images')]; print(len(o), [x['id'] for x in o][:5])"
```

### Vorschlag **[C]**

**Fix A — Bilder immer mitgeben (klein, sofort).** In `build_viewer_data.py` auf `all_images` zurueckfallen, wenn keine Seiten vorliegen:

```python
page_images = ([all_images[i] for i, _ in filtered if i < len(all_images)]
               if (all_images and filtered) else list(all_images))
```

Damit wird das Faksimile sichtbar, auch wenn die Transkription fehlt — der Viewer zeigt dann Bild ohne Text, was der Wahrheit entspricht. Anschliessend `python pipeline/build_viewer_data.py`.

**Achtung, A allein reicht nicht.** Die Seitennavigation im Viewer zaehlt ueber `obj.pages`, nicht ueber `obj.images` (`docs/app.js:1660`, `1716`, `3539`). Bei null Seiten waere damit nur das **erste** der 91 Faksimiles erreichbar, alle weiteren blieben unzugaenglich. Der Zaehler muss auf `Math.max(pages.length, images.length)` umgestellt werden, und `renderViewerPage()` muss eine Seite ohne Transkriptionsobjekt sauber behandeln (Text leer, Bild vorhanden). Das ist der eigentliche Aufwand an Fix A — die eine Zeile in `build_viewer_data.py` ist nur die Haelfte.

**Fix B — die 34 Objekte neu transkribieren (der eigentliche Punkt).** Ein leeres `result.pages` ist ein fehlgeschlagener Lauf, kein Ergebnis. `transcribe.py` ueberspringt Objekte, sobald eine Ergebnisdatei existiert — diese 34 gelten damit als erledigt und wuerden ohne `--force` nie wieder angefasst. Sie brauchen einen gezielten Neulauf.

**Fix C — Wiederholung verhindern.** Ein Lauf, der null Seiten liefert, sollte gar nicht erst als Ergebnisdatei geschrieben werden (oder mit einem `failed`-Kennzeichen, das `transcribe.py` beim Ueberspringen beachtet). Sonst faellt derselbe Fall beim naechsten Batch wieder durch. Dass die Luecke ueberhaupt so lange unbemerkt blieb, liegt daran, dass 34 leere Objekte in einem Katalog von 2.452 statistisch nicht auffallen — sichtbar wurden sie erst, weil jemand den Filter benutzt hat.

**Reihenfolge:** A zuerst (macht die Objekte pruefbar und kostet nichts), dann B (braucht API-Key und Backup, also nicht auf diesem Rechner), C beim naechsten Eingriff in `transcribe.py`.

---

## B-08 — Label-Vokabular: Schriftart und funktionale Bloecke markieren

| | |
|---|---|
| **Aufgeworfen von** | **[J]**, 2026-08-07 |
| **Betrifft** | [[annotation-protocol]] §3.1/§4, `pipeline/marker_enrich.py`, TEI/MODS-Export |
| **Status** | Entwurf liegt vor — Vokabular muss entschieden werden |

### Wunsch **[J]**

Es waere sehr gut, Markierungen setzen zu koennen zu gedruckter Schrift oder handschriftlich Geschriebenem. Auch Dinge wie Adressbloecke, Briefkopf des Briefpapiers, Postkarten-Metadaten etc.

### Einordnung **[C]**

Das sind **zwei verschiedene Achsen**, und sie sollten nicht in dieselbe Markerform gepresst werden:

- **Schriftart / Medium** (gedruckt vs. handschriftlich) ist eine *Eigenschaft* eines beliebigen Textabschnitts. Sie kann innerhalb einer Zeile wechseln — ein ausgefuelltes Formular ist genau das.
- **Funktionaler Block** (Briefkopf, Adressblock, Postkartenfeld) ist eine *Rolle* eines zusammenhaengenden Abschnitts, in aller Regel ganzzeilig oder mehrzeilig.

Beide Achsen sind unabhaengig: Ein Adressblock kann gedruckt (Vordruck) oder handschriftlich (Zweigs Adressierung) sein — auf `o:szd.1620` kommt beides auf derselben Karte vor.

**Das Modell improvisiert hier bereits.** Aus der Auszaehlung ueber alle Ergebnis-JSONs (Kommando in [[expert-in-the-loop]] §4):

| improvisiertes Label | Vorkommen |
|---|---|
| `[handschriftlich:]` / `[Handschriftlich:]` / `[handschriftlich am Rand:]` | 19 |
| `[Adressseite:]` / `[Adressfeld:]` | 14 |
| `[Absender:]` / `[Empfänger:]` | 6 |
| `[Unterschrift:]` | 15 |
| `[Bild:]` / `[Abbildung:]` / `[Bildunterschrift:]` | 65 |

Kein einziges davon wird exportiert. Der Wunsch ist also nicht "etwas Neues einfuehren", sondern **ein Vokabular festlegen, das es faktisch schon gibt** — heute nur in 68 Schreibvarianten, von denen `marker_enrich.py` drei kennt (7 % aller 388 Label-Vorkommen).

### Entwurf zur Entscheidung **[C]**

**Achse 1 — Schriftart.** Vorschlag: **nicht** als Textmarker. Begruendung: Sie wechselt zu kleinteilig, um ganzzeilig zu funktionieren, und ein Inline-Marker (`[hs: …]` mitten im Satz) waere das, was bei den geschweiften Klammern zu 81 % Rauschen gefuehrt hat. Sauberer waere die Layout-Ebene — PAGE XML kennt dafuer `TextRegion/@type` und `@production` (`printed` / `handwritten-cursive`), und `layout_analysis.py` erzeugt ohnehin Regionen. Kosten: laeuft nur, wo Layout-Analyse vorliegt, und die braucht Docling/Surya. **Alternative**, falls es im Reviewtext moeglich sein muss: ganzzeilig `[hs: …]` / `[dr: …]`, mit derselben Fail-safe-Regel wie `[quer:]`.

**Achse 2 — funktionale Bloecke.** Vorschlag: geschlossenes Vokabular, ganzzeilig, TEI-Abbildung festgelegt:

| Label | TEI | Deckt ab |
|---|---|---|
| `[Briefkopf: …]` | `<note type="letterhead">` | Vordruck auf Briefpapier (B-05) |
| `[Adresse: …]` | `<address>` | Adressblock, Adressfeld, Adressseite |
| `[Absender: …]` | `<address type="sender">` | Absenderangabe |
| `[Unterschrift: …]` | `<signed>` | Unterschrift |
| `[Bild: …]` | `<figure><figDesc>` | Abbildung, Bildunterschrift |
| `[Stempel: …]` `[Poststempel: …]` `[Marginalie: …]` | bestehend | unveraendert |
| `[quer: …]` `[kopf: …]` | bestehend (§3.7) | unveraendert |

"Postkarten-Metadaten" loesen sich damit in `[Adresse:]`, `[Absender:]`, `[Poststempel:]` und `[Briefmarke: …]` auf — praeziser als ein Sammellabel und ohne neuen Begriff.

### Offene Entscheidungen — brauchen **[J]** (bzw. Projektleitung)

1. **Geschlossen oder offen?** Geschlossen (nur definierte Labels sind gueltig, alles andere ist ein Fehler) macht den Export vollstaendig und die Daten pruefbar; offen ist bequemer, reproduziert aber den heutigen Wildwuchs.
2. **Schriftart: Layout-Ebene oder Textmarker?** Siehe Achse 1 — das ist die einzige wirklich strittige Frage.
3. **Was passiert mit dem Bestand?** 388 vorhandene Label-Vorkommen in 68 Varianten liessen sich groesstenteils deterministisch auf das neue Vokabular abbilden (`[Randnotiz links:]` → `[Marginalie:]` usw.). Das waere ein Migrationsskript in der Art von `backfill_*.py`, kein Neu-Transkribieren.
4. **Prompt erweitern?** Fuer `[quer:]` wurde entschieden: vorerst nein (§3.7). Fuer dieses Vokabular gilt dieselbe Abwaegung — erst von Hand setzen, messen, dann ggf. in den Prompt.

---

## Verwandte Dokumente

- [[evaluation-results]] — gemessene CER-Baseline und Fehlertypologie
- [[verification-concept]] — Verifikationsmethodik, Review-Stufen
- [[data-overview]] — Datengrundlage, §6 Master-Tabelle der Prompt-Gruppen
- [[journal]] — chronologisches Session-Log
