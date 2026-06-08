---
title: "teiCrafter-Integration: Page-JSON → TEI"
aliases: ["teiCrafter", "TEI-Export", "export_tei"]
created: 2026-06-08
updated: 2026-06-08
type: spec
status: active
related:
  - "[[htr-interchange-format]]"
  - "[[page-xml-mets-architecture]]"
  - "[[annotation-protocol]]"
  - "[[layout-analysis]]"
---

# teiCrafter-Integration: Page-JSON → TEI

Deterministischer Schritt, der aus den vorhandenen **Page-JSON-v0.2**-Dateien eine
TEI erzeugt, die der **teiCrafter**-Editor line-level laden und byte-treu
zurueckspeichern kann. Damit ist die Luecke geschlossen: bisher gab es nur
Katalog-TEI (Metadaten), keine Transkriptions-TEI.

Implementierung: `pipeline/export_tei.py` (+ `pipeline/marker_enrich.py`).
Kein LLM, kein API-Call — die Transkription steht bereits in `pages[].text`, hier
wird nur deterministisch umgeformt.

> **Verbindlicher Kontrakt (Quelle der Wahrheit):**
> `teiCrafter/knowledge/converter-reference.md` (Vollspec) und der lauffaehige
> Referenz-Prototyp `teiCrafter/test/tools/szd-pagejson-to-tei.mjs`.
> `export_tei.py` ist ein **faithful Port** dieses Prototyps und erzeugt
> **bit-fuer-bit dieselbe Ausgabe**. Der Kontrakt ist auf `status: active` gehoben
> (Realitaetsabgleich gegen reale Objekte, siehe §6).

---

## 1. CLI

```bash
python pipeline/export_tei.py o_szd.1079 -c korrespondenzen   # ein Objekt
python pipeline/export_tei.py -c korrespondenzen              # ganze Sammlung
python pipeline/export_tei.py --all                           # alle ~2103
python pipeline/export_tei.py --all --dry-run                 # nur zaehlen
python pipeline/export_tei.py --all --enrich-markers          # opt-in Anreicherung (§4)
```

Input:  `results/<collection>/{id}_page.json`
Output: `results/<collection>/{id}.tei.xml` (Standard)
        `results/<collection>/{id}.enriched.tei.xml` (nur mit `--enrich-markers`)

Im Repo getrackt ist nur die Demo-Handvoll (o_szd.100, 72, 1079, 2215, 161),
der Rest ist gitignored und jederzeit neu erzeugbar.

---

## 2. Ausgabeformat (TEI-Skelett)

`<TEI>` mit fester Kindreihenfolge (TEI verlangt standOff und facsimile vor text):

```
teiHeader  →  standOff (nur wenn Entitaeten)  →  facsimile (nur wenn Bild/Zonen)  →  text/body
```

| TEI-Ziel | Quelle (Page-JSON) |
|---|---|
| `titleStmt/title` | `source.title` sonst `source.id` |
| `titleStmt/respStmt` (1/Creator) | `descriptive_metadata.creator[].name` |
| `publicationStmt/p` | Maschinen-Hinweis (`provenance.model`, `review.status`, Rights) |
| `msIdentifier/idno[@type=objectId]` | `source.id` |
| `langUsage/language/@ident` | `source.language` sonst `und` |
| `standOff/listPerson/person` + `idno[@type=GND]` | `creator[].name` + `creator[].gnd` (verbatim) |
| `facsimile/surface` + `graphic/@url` | `source.images[i]` (GAMS-URL, i = Seitenindex) |
| `facsimile/surface/zone @ulx/uly/lrx/lry` | `regions[].bbox` (Prozent → **Bildpixel**) |
| `body/div/pb` (1/Seite) | `pages[].page` |
| `body//p` + `lb` | `pages[].text`: Leerzeile → `<p>`, Zeilenumbruch → `<lb/>` |

Kerne der Umformung: ein `<pb>` je Seite; Seitentext an Leerzeile (`\n{2,}`) in
`<p>` teilen, je Einzelzeile ein `<lb/>` + Zeilentext. Leerseite
(`blank`/`color_chart` oder leerer Text) → nur `<pb>`, kein `<p>`. bbox-Pixel:
`round((bbox%/100)·image_dim)`.

### Bewusste Auslassungen (v1)
`regions[].reading_order/lines/label/source` und `pages[].notes` werden **nicht**
getragen (kein Editor-Mehrwert; Notizen → siehe §5). `[Stempel:]` und
weiteres standOff-Seeding (Orte, Organisationen, Korrespondenz-Partner) bleiben
Handannotation in teiCrafter.

---

## 3. Abnahme-Kriterien

Eine TEI ist akzeptiert, wenn **beides** gegen die echte teiCrafter-Engine gilt:

1. **Byte-identischer Round-Trip:** `serialize(parseEdition(tei)) === tei`.
2. **Laedt line-level:** `profile === "line"`, `folios.length === pages.length`,
   `cells.length > 0`.

Pruefwege:
- Byte-Vergleich Python-Ausgabe vs. Node-Prototyp (`szd-pagejson-to-tei.mjs`) —
  identisch ⇒ erbt die bereits bewiesene Engine-Abnahme.
- `teiCrafter/test/tools/roundtrip_sweep.mjs` (Engine-Tokenizer-Round-Trip).
- Ladbarkeits-Sweep (analog `hersch_loadability.mjs`) ueber das ganze Korpus.

### Drei Byte-Identitaets-Fallen im Port (geloest)
- **`Math.round` ≠ Python `round()`**: JS rundet `.5` immer auf, Python macht
  banker's rounding → `jsround()` (`floor(v+0.5)`) fuer die Zonen-Pixel.
- **Windows-CRLF**: `open(..., newline="")` verhindert `\n`→`\r\n`.
- **Template-Whitespace** exakt wie im Prototyp (2-/6-/8-Space, `\n        `-Joins).

---

## 4. Marker-Anreicherung (opt-in, `--enrich-markers`)

Die Transkriptionen enthalten diplomatische Marker (→ [[annotation-protocol]]).
Der **Standard-Export laesst sie als Text** (verlustfrei, byte-identisch). Der
opt-in `--enrich-markers` wandelt sie in echte TEI-Editorial-Elemente um und
schreibt eine **separate** `{id}.enriched.tei.xml` — der Standard bleibt
unveraendert.

### Leitregel: Fail-safe auf Literal
> Niemals raten. Ein **nicht** umgewandelter Marker ist verlustfrei (= heutiger
> Stand); ein **falsch** getaggter Marker ist Datenkorruption. Im Zweifel bleibt
> der Originaltext stehen.

Die Anreicherung arbeitet **line-lokal** (auf der bereits XML-escapeten Zeile):
nur Marker, die innerhalb *einer* Zeile eindeutig und ausbalanciert sind, werden
umgewandelt. Mehrzeilige Spans haben auf ihrer Eroeffnungszeile eine ungerade
Marker-Zahl → die Zeilen-Pruefung greift nicht → sie bleiben korrekt literal. So
kann ein mehrzeiliger Span nie falsch zerschnitten werden.

### Mapping (v1)
| Marker | Bedeutung | TEI | Bedingung (sonst literal) |
|---|---|---|---|
| `[...N...]` | gezaehlte Luecke | `<gap reason="illegible" quantity="N" unit="chars"/>` | nicht allein auf der Zeile |
| `~~x~~` | Tilgung | `<del rend="strikethrough">x</del>` | gerade `~~`-Zahl/Zeile, kein Nesting |
| `{x}` | Einfuegung | `<add place="above">x</add>` | balancierte `{}`/Zeile, kein Nesting, nicht `{eingefügt}` |
| `WORT[?]` | unsicher | `<unclear reason="illegible" cert="low">WORT</unclear>` | nur direkt am Wort (protokollkonform, §3.2) |

**Bleibt literal (v1):** plain `[...]` (meist allein-auf-Zeile), `[Stempel:]`/
`[Label:]` (braucht standoff-`<note target>`, vom Zeilen-Hook nicht erreichbar),
mehrzeilige/unbalancierte/verschachtelte Marker, `[?]` mit Leerzeichen oder in
Laeufen, `[?3?]`, `{eingefügt}`-Platzhalter.

### Korpus-Ergebnis (2103 Objekte, `--enrich-markers`)
0 Parse-Fehler · 0 Round-Trip-Abweichungen · 0 verlorene Zeilen · Struktur
identisch zum Standard. Erzeugt: **922 `<unclear>`, 26.971 `<del>`, 15.850
`<add>`, 687 `<gap>`**. Die Fail-safe-Quote bestaetigt die Datenrealitaet: nur
~11 % der `[?]` sind direkt am Wort (Rest bleibt literal); genau die 4
sole-on-line-Luecken von 691 blieben literal.

> Die line-lokale Bauweise ist die Antwort auf eine adversarische Pruefung, die
> einen frueheren „per-Marker, ganze Seite"-Entwurf als unsicher entlarvte
> (Mehrzeilen-Spans, unbalancierte `~~`/`{`, `[?]` meist *nicht* am Wort). v1
> konvertiert bewusst nur das lokal-Eindeutige; die restlichen Marker-Mappings
> (Stempel als standoff-`<note>`, Mehrzeilen-Spans) sind ein spaeterer,
> separat getesteter Schritt.

---

## 5. Seiten-Notizen (`pages[].notes`): drop-by-default

`pages[].notes` (KI-Beschreibungen *ueber* eine Seite, z.B. „Rueckseite, leer",
„Poststempel WIEN 22.5.01") werden im Standard **weggelassen**. Begruendung:
- **Kein Einfluss auf CER/WER** (verifiziert: `evaluate.py` liest nur
  `pages[].transcription`, nie `notes`).
- Der maschinell nutzbare Teil steckt bereits strukturiert in `page.type`
  (`blank`/`color_chart`, gesetzt von `quality_signals.py`).
- Der Rest (Tinte, Poststempel) ist KI-generiert und **teils nachweislich falsch**
  (in o_szd.1079 widersprechen sich Notiz und Layout-Label).

Empfehlung (noch nicht implementiert): optionales Mitnehmen als
`<note resp="#szd-htr-ai">` am `<pb>`, ausdruecklich als „maschinell, ungeprueft"
markiert, hinter einem Flag — der Default bleibt byte-identisch.

---

## 6. Realitaetsabgleich (friert den Kontrakt ein)

Gegen o_szd.100, 72, 1079, 2215, 161 geprueft:
1. **bbox**: kein Wert > 100 — bbox bleibt Prozent (Kontrakt bestaetigt).
2. **Marker real**: alle fuenf kommen vor; keiner enthaelt XML-Sonderzeichen →
   verbatim verlustfrei (Grundlage fuer §4).
3. **Verworfene Felder ok**: `reading_order/lines/label/source` ohne Editor-Sinn;
   `notes` → §5.
4. **standOff**: nur `creator[]` → `<person>`+GND; o_szd.1079 ohne Creator ⇒ kein
   `<standOff>`.
5. **images 1:1 zu pages**: bestaetigt fuer alle.

### Gemeldete Anomalien (Datenlage, nicht Konverter)
- **o_szd.161 doppelt**: liegt in `korrespondenzen/` *und* `lebensdokumente/`
  mit verschiedenem Inhalt. Beide werden in ihren Sammlungsordner konvertiert.
- **40 „leere" TEI** im Voll-Lauf: 34 Objekte mit leerem `pages[]` (kein
  transkribierter Inhalt — stromaufwaerts OCR/Page-JSON), 6 mit ausschliesslich
  `blank`/`color_chart`-Seiten (reine Faksimile-Objekte). Der Konverter erzeugt
  korrekt valide, aber inhaltsleere TEI; 0 Parse-Fehler.

---

## 7. Einordnung in die drei Ausgabeformate

| Format | Rolle | Erzeugt von |
|---|---|---|
| **Page-JSON v0.2** | internes Arbeitsformat (Viewer, Anreicherung) | `export_page_json.py` |
| **METS/MODS + PAGE XML** | Archiv-/Austauschformat (GAMS, Transkribus) | `export_pagexml.py`, `export_mets.py` |
| **TEI (teiCrafter)** | Editor-/Annotationsformat (line-level, Expert-in-the-Loop) | `export_tei.py` |

Alle drei werden deterministisch aus Page-JSON abgeleitet. TEI ist der Eingang in
die teiCrafter-Annotationsstufe (Personen/Orte/Organisationen, Marker → Editorial).
