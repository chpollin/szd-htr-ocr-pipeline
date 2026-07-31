---
title: "teiCrafter-Integration: Page-JSON → TEI"
aliases: ["teiCrafter", "TEI-Export", "export_tei"]
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
created: 2026-06-08
updated: 2026-06-08
authors: [Christopher Pollin]
generated-with: Claude Code (Claude Opus 4.8)
type: spec
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
python pipeline/export_tei.py --all --enrich-markers          # opt-in Marker-Anreicherung (§4)
python pipeline/export_tei.py --all --enrich-markers --carry-notes  # zusaetzlich Seiten-Notizen (§5)
```

Input:  `results/<collection>/{id}_page.json`
Output: `results/<collection>/{id}.tei.xml` (Standard, byte-identisch zum Prototyp)
        `results/<collection>/{id}.enriched.tei.xml` (mit `--enrich-markers` und/oder `--carry-notes`)

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
- `pipeline/test_marker_enrich.py` (eigenstaendig, ohne pytest): 30 Faelle, sichert den
  Fail-safe-Kontrakt + Invariante „jede Ausgabe ist wohlgeformtes XML". Ergaenzt durch
  `pipeline/test_canonical_collection.py` (Dedup, 6 Checks) und `pipeline/test_export_tei.py`
  (jsround + build_tei-Wohlgeformtheit, 12 Checks).

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

### Mapping (v2.1, nach adversarischer Semantik-Pruefung)
| Marker | Bedeutung | TEI | Bedingung (sonst literal) |
|---|---|---|---|
| `[Stempel: X]` | Stempel | `<note type="stamp">X</note>` | ganze Zeile |
| `[Poststempel: X]` | Postmark | `<note type="postmark">X</note>` | ganze Zeile (Postmark ≠ Stempel) |
| `[Marginalie: X]` | Randnotiz | `<note type="marginal">X</note>` | ganze Zeile (Protokoll §3.5) |
| `WORT[?]` | unsicher (lesbar) | `<unclear cert="low">WORT</unclear>` | direkt am Wort; **kein** `reason="illegible"` (das hiesse unleserlich = `[...]`); Satzzeichen bleibt aussen |
| `[...N...]` | gezaehlte Luecke | `<gap reason="illegible" quantity="N" unit="chars"/>` | nicht allein auf der Zeile |
| `[...]` | Luecke | `<gap reason="illegible"/>` | nicht allein auf der Zeile |
| `~~x~~` | Tilgung | `<del>x</del>` | gerade `~~`-Zahl/Zeile, kein Nesting; **ohne** `@rend` (Streichungsform laut §3.3 nicht kodiert) |
| `{x}` | Einfuegung | `<add>x</add>` | **konservativ**: genau EIN kurzes `{Wort}` in anderem Text; **ohne** `@place` |

`{x}` ist absichtlich streng: der VLM nutzt `{}` massenhaft als Wortsegmentierungs-Rauschen
(laufender Prosatext, `>=2`/Zeile, sole-on-line, Worttrennung, Mehrwort) — ~81 % sind keine
echten Einfuegungen und bleiben literal. `[?]` wird zuerst auf tag-freiem Text umgewandelt;
Luecken nie allein auf der Zeile (gap-only-`<lb>` faellt auf cells=0).

**Bleibt literal:** mid-line/mehrzeilige Stempel, sonstige `[Label:]`-Varianten
(Bild/Abbildung/Briefmarke …), Luecke allein-auf-Zeile, mehrzeilige/unbalancierte/
verschachtelte `~~`/`{}`, `{}`-Rauschen (s. o.), `[?]` mit Leerzeichen / in Laeufen / direkt
nach einem Tag, `[?3?]`, `{eingefügt}`-Platzhalter.

### Korpus-Ergebnis (2103 Objekte, `--enrich-markers`)
0 Parse-Fehler · 0 Round-Trip-Abweichungen · 0 verlorene Zeilen · Struktur
identisch zum Standard. Erzeugt: **888 `<unclear>`, 26.971 `<del>`, 3.013 `<add>`,
731 `<gap>`** (44 plain) · **18 `<note>`** (13 stamp, 5 postmark). Der konservative
`{}`-Filter entfernte ~12.900 zweifelhafte `<add>` (vorher 15.872) — nur die ~19 %
plausiblen Einfuegungen bleiben. Regressionstest: `pipeline/test_marker_enrich.py` (30 Faelle).

> Zwei adversarische Pruefungen haben das Mapping geformt: die erste verwarf einen
> „per-Marker, ganze Seite"-Entwurf (Mehrzeilen-Spans, unbalancierte Marker) zugunsten
> der line-lokalen Bauweise; die zweite (Semantik) deckte auf, dass der VLM `{}`
> massenhaft als Wortsegmentierungs-Rauschen nutzt (Blocker: 81 % der `<add>` waeren
> erfundene Editionsaussagen) und korrigierte `@reason`/`@rend`/`@place`. Die uebrigen
> `[Label:]`-Notizen und mehrzeiligen Spans bleiben verlustfrei literal (kuenftiger Schritt).

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

Opt-in `--carry-notes` (implementiert): haengt `pages[].notes` als
`<note resp="#szd-htr-ai" type="page">` an den `<pb>`, ausdruecklich als
„maschinell, ungeprueft" markiert (`@resp`), nur fuer non-empty Notizen. Schreibt
ebenfalls `{id}.enriched.tei.xml`; der Default `{id}.tei.xml` bleibt byte-identisch.
Verifiziert: o_szd.1079 mit 5 Seiten-Notizen rundet byte-identisch und laedt
line-level (profile=line, folios=5, cells=58).

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
- **Backup-Cross-Listing (34 Objekte, GELÖST)**: o_szd.161 ist einer von 34
  lebensdokumente-Objekten, die das Backup zusätzlich physisch unter `korrespondenzen/`
  listet. Die Transkriptions-Pipeline (`discover_objects` → `_canonical_collection`)
  dedupliziert diese seit Commit `fb48ca0` TEI-kanonisch (jedes Objekt genau einer
  Sammlung); die verwaisten korrespondenzen-Result-Kopien wurden entfernt. Der
  TEI-Konverter hier arbeitet pro vorhandenem Page-JSON und ist davon unberührt.
  Nicht zu verwechseln mit den „34 leeren `pages[]`" unten — anderes Phänomen, gleiche Zahl.
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

---

## 8. Coverage-Diagnose

`pipeline/diagnose_coverage.py` (read-only, kein API-Call) findet Objekte ohne
nutzbaren Transkriptionstext und klaert die Ursache, schreibt
`reports/coverage-gaps.json` und gibt den fertigen Re-Transkriptions-Befehl aus
(loest ihn aber NICHT selbst aus — Kosten-/Lane-Entscheidung des Operators):

- **34 leeres Page-JSON** (`pages[]==[]`): das OCR-Ergebnis ist ebenfalls leer,
  obwohl Bilder vorhanden sind → **stille Transkriptions-Fehlschlaege**, per
  `python pipeline/transcribe.py {id} -c {col} --force` behebbar.
- **6 alle Seiten blank**: reine Faksimile-/Leervorlage, nichts zu transkribieren.

```bash
python pipeline/diagnose_coverage.py      # Report + Konsolen-Summary + Retry-Befehle
```
