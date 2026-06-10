"""Import der Autographensammlung (SZ-AAL) ins Pipeline-Backup.

Einmal-Import nach dem GAMS-Ingest SZ-AAL-2026-06. Baut aus dem lokalen
Ingest-Staging (Book-XMLs + Scans, eine Mappe pro Objekt) die Backup-Struktur

    BACKUP_ROOT/<subdir>/o_szd.N/metadata.json
    BACKUP_ROOT/<subdir>/o_szd.N/mets.xml
    BACKUP_ROOT/<subdir>/o_szd.N/images/IMG_<n>.jpg

und generiert die TEI-Kontextquelle data/szd_autographen_tei.xml (eine
biblFull pro Objekt, XPath-kompatibel zu tei_context.py).

Das METS kommt von GAMS (METS_SOURCE-Disseminator, wie szd-zenodo-backup);
die Bildmasse aus dem METS werden gegen die lokalen JPEG-Header geprueft --
das verifiziert die Zuordnung lokaler Scan -> GAMS IMG.n. metadata.json
spiegelt das Format der bestehenden Backup-Objekte; provenance.in_gams=true
laesst den Viewer die GAMS-URLs verwenden.

Die Sprache aus dem METS (Cirilo-Pauschalwert "Deutsch") wird NICHT in die
TEI uebernommen -- viele AAL-Briefe sind englisch, ein falscher Sprachhinweis
wuerde den VLM-Prompt irrefuehren. Das VLM erkennt die Sprache selbst.

Wiederaufnahme: vorhandene mets.xml/Bilder werden uebersprungen, das Skript
ist idempotent re-runnbar.
"""

import argparse
import json
import shutil
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from config import BACKUP_ROOT, COLLECTIONS, DATA_DIR

COLLECTION = "autographen"
INGEST_LABEL = "SZ-AAL-2026-06"
DEFAULT_SOURCE = Path("C:/Users/Chrisi/Documents/PROJECTS/szd/ingeste")
METS_URL_TEMPLATE = "https://gams.uni-graz.at/archive/get/{pid}/METS_SOURCE"

VI = {"vi": "http://gams.uni-graz.at/viewer"}
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
METS_NS = {
    "mets": "http://www.loc.gov/METS/",
    "mods": "http://www.loc.gov/mods/v3",
    "xlink": "http://www.w3.org/1999/xlink",
    "dv": "http://dfg-viewer.de/",
    "exif": "http://ns.adobe.com/exif/1.0/",
}
TEI_NS = "http://www.tei-c.org/ns/1.0"

# Titelpraefixe der Book-XMLs ("<Objekttyp> von X an Y ..."): alle 379
# Objekte sind Korrespondenzstuecke, der Praefix dient als TEI-objecttyp.
KNOWN_OBJECTTYPES = (
    "Ansichtspostkarte", "Briefabschriften", "Briefentwurf", "Brieffragment",
    "Postkarte", "Telegramm", "Entwurf", "Kuvert", "Brief",
)


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    """(width, height) aus dem JPEG-Header (SOF-Marker), ohne Bibliotheken."""
    with path.open("rb") as f:
        if f.read(2) != b"\xff\xd8":
            raise ValueError(f"Kein JPEG: {path}")
        while True:
            b = f.read(1)
            if not b:
                raise ValueError(f"Kein SOF-Marker gefunden: {path}")
            if b != b"\xff":
                continue
            code = f.read(1)
            while code == b"\xff":
                code = f.read(1)
            if not code:
                raise ValueError(f"Kein SOF-Marker gefunden: {path}")
            c = code[0]
            if c in (0x01, 0xD8) or 0xD0 <= c <= 0xD7:
                continue
            seg_len = int.from_bytes(f.read(2), "big")
            if 0xC0 <= c <= 0xCF and c not in (0xC4, 0xC8, 0xCC):
                seg = f.read(5)
                height = int.from_bytes(seg[1:3], "big")
                width = int.from_bytes(seg[3:5], "big")
                return width, height
            f.seek(seg_len - 2, 1)


def parse_book_xml(path: Path) -> dict:
    """Book-XML (GAMS-Viewer-Namespace) -> pid, title, author, date, owner, pages."""
    root = ET.parse(path).getroot()

    def text(tag: str) -> str:
        el = root.find(f"vi:{tag}", VI)
        return (el.text or "").strip() if el is not None else ""

    owner_el = root.find("vi:owner/vi:name", VI)
    pages = [p.get(XLINK_HREF) for p in root.findall(".//vi:page", VI)]
    return {
        "pid": text("idno"),
        "title": text("title"),
        "author": text("author"),
        "date": text("date"),
        "owner": (owner_el.text or "").strip() if owner_el is not None else "",
        "pages": pages,
    }


def fetch_mets(pid: str, dest: Path, retries: int = 3) -> bytes:
    """METS_SOURCE von GAMS laden (oder lokalen Cache lesen) und speichern."""
    if dest.exists():
        return dest.read_bytes()
    url = METS_URL_TEMPLATE.format(pid=pid)
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                content = resp.read()
            dest.write_bytes(content)
            return content
        except Exception as e:  # noqa: BLE001 - Retry auf alles (Netz/HTTP)
            last_err = e
            time.sleep(2 * attempt)
    raise RuntimeError(f"METS-Download fehlgeschlagen fuer {pid}: {last_err}")


def parse_mets(mets_xml: bytes, pid: str) -> dict:
    """METS_SOURCE -> metadata-Dict im Format von szd-zenodo-backup."""
    root = ET.fromstring(mets_xml)
    meta = {
        "object_id": pid,
        "title": None, "signature": None, "author": None,
        "language": None, "language_code": None,
        "owner": None, "rights": None, "images": [],
    }
    mods = root.find(".//mods:mods", METS_NS)
    if mods is not None:
        for key, xpath in (
            ("title", ".//mods:title"),
            ("signature", './/mods:note[@type="signature"]'),
            ("author", './/mods:name[@type="personal"]/mods:displayForm'),
            ("language", './/mods:languageTerm[@type="text"]'),
            ("language_code", './/mods:languageTerm[@type="code"]'),
        ):
            el = mods.find(xpath, METS_NS)
            if el is not None and el.text:
                meta[key] = el.text
        urn = mods.find('.//mods:identifier[@type="urn"]', METS_NS)
        if urn is not None and urn.text and pid not in urn.text:
            raise ValueError(f"METS-URN {urn.text!r} passt nicht zu {pid}")
    owner_el = root.find(".//dv:owner", METS_NS)
    if owner_el is not None:
        meta["owner"] = owner_el.text
        if "CC-BY" in (owner_el.text or ""):
            meta["rights"] = "CC-BY"
    for file_elem in root.findall('.//mets:file[@MIMETYPE="image/jpeg"]', METS_NS):
        file_id = file_elem.get("ID")
        if not file_id or not file_id.startswith("IMG."):
            continue
        flocat = file_elem.find(".//mets:FLocat", METS_NS)
        if flocat is None:
            continue
        width_el = file_elem.find(".//exif:PixelXDimension", METS_NS)
        height_el = file_elem.find(".//exif:PixelYDimension", METS_NS)
        # structMap ist bei den Cirilo-Ingests leer -> Reihenfolge aus IMG.n
        meta["images"].append({
            "id": file_id,
            "url": flocat.get(XLINK_HREF),
            "width": int(width_el.text) if width_el is not None and width_el.text else None,
            "height": int(height_el.text) if height_el is not None and height_el.text else None,
            "order": int(file_id.split(".", 1)[1]),
        })
    meta["images"].sort(key=lambda x: x["order"])
    return meta


def derive_signature(folder_name: str) -> str:
    """'SZ_AAL_B1.1' -> 'SZ-AAL/B1.1' (Konvention des Ingest-Stagings)."""
    parts = folder_name.split("_", 2)
    if len(parts) != 3:
        raise ValueError(f"Unerwarteter Mappenname: {folder_name}")
    return f"{parts[0]}-{parts[1]}/{parts[2]}"


def derive_objecttyp(title: str) -> str:
    for typ in KNOWN_OBJECTTYPES:
        if title.startswith(typ):
            return typ
    return "Brief"


def _sub(parent, tag, text=None, **attrib):
    el = ET.SubElement(parent, f"{{{TEI_NS}}}{tag}", attrib)
    if text:
        el.text = text
    return el


def build_tei(entries: list[dict]) -> ET.ElementTree:
    """Minimal-TEI mit einer biblFull pro Objekt (XPaths wie tei_context.py)."""
    tei = ET.Element(f"{{{TEI_NS}}}TEI")
    header = _sub(tei, "teiHeader")
    file_desc = _sub(header, "fileDesc")
    title_stmt = _sub(file_desc, "titleStmt")
    _sub(title_stmt, "title", "Autographen (SZ-AAL)", **{XML_LANG: "de"})
    pub = _sub(file_desc, "publicationStmt")
    _sub(pub, "ab", f"Generiert von pipeline/import_autographen.py aus den "
                    f"GAMS-Book-XMLs des Ingests {INGEST_LABEL}.")
    _sub(_sub(file_desc, "sourceDesc"), "p", "Literaturarchiv Salzburg, Stefan Zweig Digital")

    list_bibl = _sub(_sub(_sub(tei, "text"), "body"), "listBibl")
    for e in entries:
        bibl = _sub(list_bibl, "biblFull",
                    **{XML_ID: "SZDAAL." + e["pid"].rsplit(".", 1)[1]})
        fd = _sub(bibl, "fileDesc")
        ts = _sub(fd, "titleStmt")
        _sub(ts, "title", e["title"], **{XML_LANG: "de", "ana": "assigned"})
        if e["author"]:
            pers = _sub(_sub(ts, "author"), "persName")
            if ", " in e["author"]:
                surname, forename = e["author"].split(", ", 1)
                _sub(pers, "surname", surname)
                _sub(pers, "forename", forename)
            else:
                pers.text = e["author"]
        _sub(_sub(fd, "publicationStmt"), "ab", "Archivmaterial")
        ms_desc = _sub(_sub(fd, "sourceDesc"), "msDesc")
        ms_id = _sub(ms_desc, "msIdentifier")
        _sub(ms_id, "country", "Oesterreich")
        _sub(ms_id, "settlement", "Salzburg")
        _sub(ms_id, "repository", "Literaturarchiv Salzburg")
        _sub(ms_id, "idno", e["signature"], type="signature")
        _sub(_sub(ms_id, "altIdentifier"), "idno", e["pid"], type="PID")
        extent = _sub(_sub(_sub(_sub(ms_desc, "physDesc"), "objectDesc"),
                           "supportDesc"), "extent")
        span = _sub(extent, "span", **{XML_LANG: "de"})
        term = _sub(span, "term", e["objecttyp"], type="objecttyp")
        term.tail = ", "
        _sub(span, "measure", f"{e['n_pages']} Scans", type="leaf")
        if e["date"]:
            _sub(_sub(_sub(ms_desc, "history"), "origin"), "origDate", e["date"])
        _sub(_sub(_sub(_sub(bibl, "profileDesc"), "textClass"), "keywords"),
             "term", "Korrespondenz", type="classification")

    tree = ET.ElementTree(tei)
    ET.indent(tree, space="  ")
    return tree


def import_object(folder: Path, dest_base: Path, dry_run: bool) -> dict:
    """Ein Staging-Objekt importieren. Liefert den TEI-Eintrag."""
    book_files = list(folder.glob("Result_*.xml"))
    if len(book_files) != 1:
        raise ValueError(f"{folder.name}: erwartet genau 1 Book-XML, "
                         f"gefunden {len(book_files)}")
    book = parse_book_xml(book_files[0])
    pid = book["pid"]
    if not pid.startswith("o:szd."):
        raise ValueError(f"{folder.name}: unerwartete PID {pid!r}")
    signature = derive_signature(folder.name)

    # Lokale Konsistenz: jede referenzierte Seite muss als Datei da sein
    local_pages = []
    for href in book["pages"]:
        p = folder / href
        if not p.exists():
            raise ValueError(f"{folder.name}: referenziertes Bild fehlt: {href}")
        local_pages.append(p)
    n_jpgs = len(list(folder.glob("*.jpg")))
    if n_jpgs != len(local_pages):
        raise ValueError(f"{folder.name}: {n_jpgs} JPGs in der Mappe, aber "
                         f"{len(local_pages)} im Book-XML referenziert")

    entry = {
        "pid": pid,
        "title": book["title"],
        "author": book["author"],
        "date": book["date"],
        "signature": signature,
        "objecttyp": derive_objecttyp(book["title"]),
        "n_pages": len(local_pages),
    }
    if dry_run:
        return entry

    obj_dir = dest_base / pid.replace(":", "_")
    img_dir = obj_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    mets_content = fetch_mets(pid, obj_dir / "mets.xml")
    meta = parse_mets(mets_content, pid)
    if len(meta["images"]) != len(local_pages):
        raise ValueError(f"{pid}: METS hat {len(meta['images'])} Bilder, "
                         f"Staging {len(local_pages)}")

    # Zuordnung Scan -> IMG.n ueber Bildmasse verifizieren, dann kopieren
    for i, (img_meta, src) in enumerate(zip(meta["images"], local_pages), start=1):
        w, h = jpeg_dimensions(src)
        if img_meta["width"] is not None and (w, h) != (img_meta["width"], img_meta["height"]):
            raise ValueError(
                f"{pid}: Masse von {src.name} ({w}x{h}) passen nicht zu "
                f"{img_meta['id']} ({img_meta['width']}x{img_meta['height']})")
        dest = img_dir / f"IMG_{i}.jpg"
        if not (dest.exists() and dest.stat().st_size == src.stat().st_size):
            shutil.copy2(src, dest)

    meta["signature"] = meta["signature"] or signature
    # Cirilo setzt beim Ingest pauschal "Deutsch" -- kein Katalogwert, viele
    # AAL-Briefe sind englisch. Nicht uebernehmen (mets.xml bleibt als Beleg),
    # sonst flaggt quality_signals jeden englischen Brief als language_mismatch.
    meta["language"] = None
    meta["language_code"] = None
    meta["container"] = None
    meta["provenance"] = {
        "ingest_label": INGEST_LABEL,
        "in_gams": True,
        "source_folder": folder.name,
    }
    meta["download_date"] = datetime.now().isoformat()
    (obj_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                        help="Ingest-Staging (eine Mappe pro Objekt)")
    parser.add_argument("--tei-out", type=Path,
                        default=DATA_DIR / COLLECTIONS[COLLECTION]["tei"],
                        help="Zieldatei fuer die generierte TEI")
    parser.add_argument("--limit", type=int, default=0,
                        help="Nur die ersten N Objekte (0 = alle)")
    parser.add_argument("--delay", type=float, default=0.3,
                        help="Pause zwischen METS-Downloads in Sekunden")
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur pruefen und zaehlen, nichts schreiben")
    args = parser.parse_args()

    dest_base = BACKUP_ROOT / COLLECTIONS[COLLECTION]["subdir"]
    folders = sorted(d for d in args.source.iterdir()
                     if d.is_dir() and list(d.glob("Result_*.xml")))
    if args.limit:
        folders = folders[:args.limit]
    print(f"{len(folders)} Objektmappen in {args.source}")
    print(f"Ziel: {dest_base}")

    entries, failed = [], []
    for i, folder in enumerate(folders, start=1):
        try:
            entry = import_object(folder, dest_base, args.dry_run)
            entries.append(entry)
            print(f"  [{i}/{len(folders)}] {entry['pid']}  {folder.name}  "
                  f"({entry['n_pages']} Seiten)")
        except Exception as e:  # noqa: BLE001 - einzelnes Objekt soll Lauf nicht stoppen
            failed.append((folder.name, str(e)))
            print(f"  [{i}/{len(folders)}] FEHLER {folder.name}: {e}")
        if not args.dry_run and args.delay:
            time.sleep(args.delay)

    if entries and not args.dry_run:
        entries.sort(key=lambda e: int(e["pid"].rsplit(".", 1)[1]))
        build_tei(entries).write(args.tei_out, encoding="utf-8",
                                 xml_declaration=True)
        print(f"TEI geschrieben: {args.tei_out} ({len(entries)} biblFull)")

    total_pages = sum(e["n_pages"] for e in entries)
    print(f"\nImportiert: {len(entries)} Objekte, {total_pages} Seiten"
          f"{' (Dry-Run)' if args.dry_run else ''}")
    if failed:
        print(f"FEHLGESCHLAGEN: {len(failed)}")
        for name, err in failed:
            print(f"  - {name}: {err}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
