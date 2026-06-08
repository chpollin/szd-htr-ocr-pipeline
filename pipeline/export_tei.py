"""SZD-HTR TEI Export: Page-JSON v0.2 -> teiCrafter-target TEI (deterministisch).

Faithful Python-Port des Referenz-Prototyps
  teiCrafter/test/tools/szd-pagejson-to-tei.mjs
Erzeugt BIT-FUER-BIT dieselbe Ausgabe wie der Prototyp. Kein LLM, kein API-Call.

Kontrakt (Quelle der Wahrheit):
  teiCrafter/knowledge/converter-reference.md
Abnahme je Datei (gegen die echte teiCrafter-Engine, nicht per Behauptung):
  1. Byte-identischer Round-Trip: serialize(parseEdition(tei)) === tei
  2. Laedt line-level: profile == "line", folios == pages, cells > 0

Drei Byte-Identitaets-Fallen, die hier bewusst behandelt sind:
  * JS Math.round() rundet .5 immer auf (round-half-up) -> jsround(), nicht round().
  * Windows uebersetzt '\\n' -> '\\r\\n' beim Schreiben -> open(..., newline="").
  * Template-Whitespace (2-/6-/8-Space-Einrueckung, '\\n        '-Joins) exakt wie im Prototyp.

Usage:
    python pipeline/export_tei.py o_szd.1079 -c korrespondenzen
    python pipeline/export_tei.py -c korrespondenzen
    python pipeline/export_tei.py --all
    python pipeline/export_tei.py --all --dry-run
"""

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path

from config import COLLECTIONS, RESULTS_BASE, results_dir_for
from marker_enrich import enrich_line


# --- Escaping (Prototyp: escText / escAttr) ---------------------------------

def esc_text(s) -> str:
    s = "" if s is None else str(s)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(s) -> str:
    return esc_text(s).replace('"', "&quot;")


# --- slug() (Prototyp: NFKD, Combining-Marks weg, lower, [^a-z0-9]+ -> _) ----

_COMBINING = re.compile(r"[̀-ͯ]")
_NONWORD = re.compile(r"[^a-z0-9]+")
_TRIM = re.compile(r"^_+|_+$")


def slug(s) -> str:
    s = "" if s is None else str(s)
    s = unicodedata.normalize("NFKD", s)
    s = _COMBINING.sub("", s)
    s = s.lower()
    s = _NONWORD.sub("_", s)
    s = _TRIM.sub("", s)
    return s or "x"


def jsround(v: float) -> int:
    """JS Math.round(): rundet .5 immer auf (Richtung +inf).

    Pixelkoordinaten sind nicht-negativ, daher ist floor(v + 0.5) exakt
    Math.round() -- im Gegensatz zu Pythons round() (banker's rounding).
    """
    return math.floor(v + 0.5)


# --- Konverter: Page-JSON -> TEI-String (Port von szd-pagejson-to-tei.mjs) ---

def build_tei(pj: dict, enrich: bool = False) -> str:
    src = pj.get("source") or {}
    dm = src.get("descriptive_metadata") or {}
    prov = pj.get("provenance") or {}
    pages = pj.get("pages") or []

    # --- persons (standOff) aus descriptive_metadata.creator ---
    persons = []
    for c in (dm.get("creator") or []):
        persons.append({
            "id": "pers_" + slug(c.get("name")),
            "name": c.get("name"),
            "gnd": c.get("gnd") or None,
        })

    person_xml = "\n".join(
        f'      <person xml:id="{esc_attr(p["id"])}">\n'
        f'        <persName>{esc_text(p["name"])}</persName>\n'
        + (f'        <idno type="GND">{esc_text(p["gnd"])}</idno>\n' if p["gnd"] else "")
        + "      </person>"
        for p in persons
    )

    # --- facsimile: ein surface pro Seite (graphic + zones aus region-bboxes) ---
    def zones_for(page: dict):
        w = page.get("image_width")
        h = page.get("image_height")
        regions = page.get("regions")
        if not w or not h or not isinstance(regions, list):
            return []
        out = []
        for r in regions:
            bb = r.get("bbox") or []
            x, y, bw, bh = bb[0], bb[1], bb[2], bb[3]
            ulx = jsround((x / 100) * w)
            uly = jsround((y / 100) * h)
            lrx = jsround(((x + bw) / 100) * w)
            lry = jsround(((y + bh) / 100) * h)
            typ = f' type="{esc_attr(r.get("type"))}"' if r.get("type") else ""
            out.append(
                f'      <zone xml:id="z_{page["page"]}_{esc_attr(r.get("id"))}" '
                f'ulx="{ulx}" uly="{uly}" lrx="{lrx}" lry="{lry}"{typ}/>'
            )
        return out

    images = src.get("images") or []
    surfaces = []
    surface_pages = set()
    for i, page in enumerate(pages):
        sid = f"surf_{page['page']}"
        img = (images[i] if i < len(images) else "") or page.get("image") or ""
        zs = zones_for(page)
        if not zs and not img:
            continue
        w = page.get("image_width")
        h = page.get("image_height")
        dims = f' ulx="0" uly="0" lrx="{w}" lry="{h}"' if (w and h) else ""
        surfaces.append(
            f'    <surface xml:id="{sid}"{dims}>\n'
            + (f'      <graphic url="{esc_attr(img)}"/>\n' if img else "")
            + (("\n".join(zs) + "\n") if zs else "")
            + "    </surface>"
        )
        surface_pages.add(page["page"])

    def has_surface(page: dict) -> bool:
        return page["page"] in surface_pages

    # --- body: pb pro Seite; Seitentext -> <p> an Leerzeile, <lb/> pro Zeile ---
    def body_for_page(page: dict) -> str:
        sid = f"surf_{page['page']}"
        facs = f' facs="#{sid}"' if has_surface(page) else ""
        pb = f'      <pb n="{esc_attr(page["page"])}"{facs}/>'
        text = (page.get("text") or "").replace("\r\n", "\n")
        if not text.strip():
            return pb  # blank / color_chart: Folio ohne Text
        def cell(ln: str) -> str:
            c = esc_text(ln)
            return enrich_line(c) if enrich else c  # enrich nur im opt-in Pfad
        paras = []
        for para in re.split(r"\n{2,}", text):
            inner = "\n        ".join(f"<lb/>{cell(ln)}" for ln in para.split("\n"))
            paras.append(f"      <p>\n        {inner}\n      </p>")
        return pb + "\n" + "\n".join(paras)

    body = "\n".join(body_for_page(p) for p in pages)

    # --- header aus descriptive metadata ---
    title = src.get("title") or src.get("id") or "Untitled"
    resp_list = "\n".join(
        f"        <respStmt><resp>contributor</resp>"
        f'<persName>{esc_text(p["name"])}</persName></respStmt>'
        for p in persons
    )
    resp_block = (resp_list + "\n") if resp_list else ""

    rights = dm.get("rights") or ""
    repo = ""
    holding = dm.get("holding")
    if isinstance(holding, dict):
        repo = holding.get("repository") or ""
    repo = repo or src.get("repository") or ""
    shelf = src.get("shelfmark") or ""
    lang = src.get("language") or "und"
    rv = pj.get("review")
    review_status = rv.get("status") if (isinstance(rv, dict) and rv.get("status")) else "unreviewed"
    model = prov.get("model") or "unknown model"

    pub_rights = f" Rights: {esc_text(rights)}." if rights else ""
    pub_p = (
        f"Machine-generated TEI from szd-htr Page-JSON ({esc_text(model)}). "
        f"Structure unreviewed; transcription {esc_text(review_status)}.{pub_rights}"
    )
    repo_part = f"\n            <repository>{esc_text(repo)}</repository>" if repo else ""
    shelf_part = (f'\n            <idno type="shelfmark">{esc_text(shelf)}</idno>'
                  if shelf else "")
    obj_id = esc_text(src.get("id") or "")

    header = (
        "  <teiHeader>\n"
        "    <fileDesc>\n"
        "      <titleStmt>\n"
        f"        <title>{esc_text(title)}</title>\n"
        f"{resp_block}      </titleStmt>\n"
        "      <publicationStmt>\n"
        f"        <p>{pub_p}</p>\n"
        "      </publicationStmt>\n"
        "      <sourceDesc>\n"
        "        <msDesc>\n"
        f"          <msIdentifier>{repo_part}{shelf_part}\n"
        f'            <idno type="objectId">{obj_id}</idno>\n'
        "          </msIdentifier>\n"
        "        </msDesc>\n"
        "      </sourceDesc>\n"
        "    </fileDesc>\n"
        "    <profileDesc>\n"
        f'      <langUsage><language ident="{esc_attr(lang)}"/></langUsage>\n'
        "    </profileDesc>\n"
        "  </teiHeader>"
    )

    facsimile = (
        "  <facsimile>\n" + "\n".join(surfaces) + "\n  </facsimile>\n"
        if surfaces else ""
    )
    stand_off = (
        "  <standOff>\n    <listPerson>\n" + person_xml + "\n    </listPerson>\n  </standOff>\n"
        if persons else ""
    )

    tei = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<TEI xmlns="http://www.tei-c.org/ns/1.0">\n'
        f"{header}\n"
        f"{stand_off}{facsimile}  <text>\n"
        "    <body>\n"
        f'      <div type="document" n="{esc_attr(src.get("id") or "")}">\n'
        f"{body}\n"
        "      </div>\n"
        "    </body>\n"
        "  </text>\n"
        "</TEI>\n"
    )
    return tei


# --- Objekt-Export ----------------------------------------------------------

def page_json_path(object_id: str, collection: str) -> Path:
    return RESULTS_BASE / collection / f"{object_id}_page.json"


def output_suffix(enrich: bool) -> str:
    return ".enriched.tei.xml" if enrich else ".tei.xml"


def export_object_tei(object_id: str, collection: str, force: bool = False,
                      enrich: bool = False) -> Path | None:
    out_path = results_dir_for(collection) / f"{object_id}{output_suffix(enrich)}"
    if out_path.exists() and not force:
        return None
    in_path = page_json_path(object_id, collection)
    if not in_path.exists():
        print(f"  {object_id}: kein Page-JSON ({in_path.name})", file=sys.stderr)
        return None
    pj = json.loads(in_path.read_text(encoding="utf-8"))
    tei = build_tei(pj, enrich=enrich)
    # newline="" verhindert Windows-CRLF-Uebersetzung -> Byte-Identitaet zum Prototyp.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(tei)
    return out_path


def discover_page_jsons(collection: str):
    d = RESULTS_BASE / collection
    if not d.exists():
        return []
    ids = []
    for p in sorted(d.glob("*_page.json")):
        ids.append(p.name[:-len("_page.json")])
    return ids


# --- CLI --------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="TEI Export: Page-JSON v0.2 -> teiCrafter-target TEI (deterministisch)"
    )
    parser.add_argument("object_id", nargs="?", help="Einzelnes Objekt (z.B. o_szd.1079)")
    parser.add_argument("-c", "--collection", help="Sammlung", choices=COLLECTIONS.keys())
    parser.add_argument("--all", action="store_true", help="Alle Sammlungen")
    parser.add_argument("--force", action="store_true", help="Bestehende ueberschreiben")
    parser.add_argument("--dry-run", action="store_true", help="Nur zaehlen, nicht exportieren")
    parser.add_argument("--enrich-markers", action="store_true",
                        help="Opt-in: Marker ([...N...], ~~x~~, {x}, WORT[?]) in TEI-Editorial-"
                             "Elemente umwandeln. Schreibt {id}.enriched.tei.xml (Standard-TEI "
                             "bleibt unveraendert). Mehrdeutiges bleibt Literal.")
    args = parser.parse_args()
    enrich = args.enrich_markers

    objects = []  # (object_id, collection)
    if args.object_id:
        if not args.collection:
            print("FEHLER: --collection erforderlich bei Einzelobjekt")
            sys.exit(1)
        objects = [(args.object_id, args.collection)]
    elif args.all:
        for col in COLLECTIONS:
            objects.extend((oid, col) for oid in discover_page_jsons(col))
    elif args.collection:
        objects = [(oid, args.collection) for oid in discover_page_jsons(args.collection)]
    else:
        parser.print_help()
        sys.exit(1)

    mode = " [enrich-markers]" if enrich else ""
    if args.dry_run:
        print(f"TEI Export (dry-run){mode}: {len(objects)} Objekte mit Page-JSON")
        for col in COLLECTIONS:
            n = sum(1 for _, c in objects if c == col)
            if n:
                print(f"  {col}: {n}")
        return

    print(f"TEI Export{mode}: {len(objects)} Objekte")
    print("=" * 60)
    done, skipped, failed = 0, 0, 0
    for i, (oid, col) in enumerate(objects):
        out_path = results_dir_for(col) / f"{oid}{output_suffix(enrich)}"
        if out_path.exists() and not args.force:
            skipped += 1
            continue
        path = export_object_tei(oid, col, args.force, enrich)
        if path:
            done += 1
            if done <= 5 or done % 200 == 0:
                print(f"  [{i + 1}/{len(objects)}] {col}/{path.name}")
        else:
            failed += 1
    print("=" * 60)
    print(f"Fertig: {done} exportiert, {skipped} uebersprungen, {failed} fehlgeschlagen")


if __name__ == "__main__":
    main()
