"""Import der SZ-AAL-Lebensdokumente (L1-L13) in die Sammlung `lebensdokumente`.

Nachzug nach dem GAMS-Ingest der 13 SZ-AAL-Lebensdokumente. Anders als
import_autographen.py:

  * Die Book-XMLs im Staging tragen KEINE PID (<idno> fehlt). Die von Cirilo
    vergebenen PIDs werden per METS-Titel aufgeloest (--resolve START END,
    schreibt die Signatur->PID-Karte) -- erst moeglich, wenn die Faksimiles in
    GAMS liegen.
  * Die TEI wird NICHT generiert, sondern aus der maßgeblichen Katalog-TEI
    SZDLEB.xml uebernommen (die 13 biblFull SZDLEB.144-156). Diese sind bereits
    XPath-kompatibel zu tei_context.py; eingefuegt wird nur der PID-
    altIdentifier. So bleiben GND, Provenienz, Maße etc. erhalten.
  * Die Sprache kommt aus SZDLEB (echter Katalogwert, L5-L11 englisch) statt
    aus dem Cirilo-METS (pauschal "Deutsch") -- die Sprachfalle der Autographen
    greift hier also nicht.

Das Backup-Format spiegelt die bestehenden Sammlungsobjekte
(BACKUP_ROOT/lebensdokumente/o_szd.N/{metadata.json,mets.xml,images/IMG_n.jpg}).
provenance.in_gams=true laesst den Viewer die GAMS-URLs verwenden.

Ablauf nach Faksimile-Verfuegbarkeit:
    python import_lebensdokumente_aal.py --resolve 3502 3530   # PIDs mappen
    python import_lebensdokumente_aal.py --dry-run             # pruefen
    python import_lebensdokumente_aal.py                       # Backup + TEI

Idempotent re-runnbar (vorhandene mets.xml/Bilder werden uebersprungen, der
TEI-Merge ersetzt vorhandene PID-Eintraege).
"""

import argparse
import csv
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from config import BACKUP_ROOT, COLLECTIONS, DATA_DIR
# Erprobte GAMS-Bausteine wiederverwenden statt duplizieren.
from import_autographen import jpeg_dimensions, fetch_mets, parse_mets, METS_URL_TEMPLATE

COLLECTION = "lebensdokumente"
INGEST_LABEL = "SZ-AAL-L-2026-06"
DEFAULT_SOURCE = Path("C:/Users/Chrisi/Documents/PROJECTS/szd/ingeste_L_lebensdokumente")
SZDLEB_DEFAULT = Path("C:/Users/Chrisi/Documents/GitHub/SZD/data/PersonalDocument/SZDLEB.xml")
PIDMAP_DEFAULT = Path("C:/tmp/lebensdok_aal_pidmap.csv")

TEI_NS = "http://www.tei-c.org/ns/1.0"
NS = {"tei": TEI_NS}
MODS_NS = {"mods": "http://www.loc.gov/mods/v3"}
VI = {"vi": "http://gams.uni-graz.at/viewer"}
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
UA = {"User-Agent": "SZD-QA/1.0 (office@dhcraft.org)"}
BASE = "https://gams.uni-graz.at"
DELAY = 1.0

RE_FOLDER = re.compile(r"^SZ_AAL_L\d+[a-z]?$")
RE_SIG = re.compile(r"SZ-AAL/L\d+[a-z]?")

LANG_CODE = {"deutsch": "de", "englisch": "en", "französisch": "fr", "italienisch": "it"}


# ---------------------------------------------------------------- SZDLEB index

def load_szdleb(path: Path) -> dict:
    """Return {signature: {bibl, title, author, language, language_code}} for SZ-AAL/L*."""
    root = ET.parse(path).getroot()
    out = {}
    for bibl in root.findall(".//tei:biblFull", NS):
        sig_el = bibl.find('.//tei:msIdentifier/tei:idno[@type="signature"]', NS)
        sig = sig_el.text.strip() if sig_el is not None and sig_el.text else ""
        if not RE_SIG.fullmatch(sig):
            continue
        title_el = bibl.find(".//tei:titleStmt/tei:title", NS)
        lang_el = bibl.find(".//tei:textLang/tei:lang", NS)
        lang = (lang_el.text or "").strip() if lang_el is not None else ""
        author = ""
        for a in bibl.findall(".//tei:titleStmt/tei:author/tei:persName", NS):
            sn = a.find("tei:surname", NS)
            fn = a.find("tei:forename", NS)
            if sn is not None and sn.text:
                author = sn.text.strip() + (", " + fn.text.strip() if fn is not None and fn.text else "")
            else:
                author = " ".join(a.itertext()).strip()
            if author:
                break
        out[sig] = {
            "bibl": bibl,
            "title": (title_el.text or "").strip() if title_el is not None else "",
            "author": author,
            "language": lang,
            "language_code": LANG_CODE.get(lang.lower(), ""),
        }
    return out


def derive_signature(folder_name: str) -> str:
    """'SZ_AAL_L12' -> 'SZ-AAL/L12'."""
    parts = folder_name.split("_", 2)
    if len(parts) != 3:
        raise ValueError(f"Unerwarteter Mappenname: {folder_name}")
    return f"{parts[0]}-{parts[1]}/{parts[2]}"


# --------------------------------------------------------------- PID resolve

def _get(url, retries=3):
    last = None
    for a in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError:
            return None
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (a + 1))
    return None


def resolve_pids(start: int, end: int, want: set, pidmap: Path, delay: float) -> dict:
    """Probe o:szd.start..end, map each SZ-AAL/L* signature (from METS) to its PID.

    Probt den ganzen Bereich (kein Early-Stop): nur so faellt ein Doppel-Ingest
    auf. Signaturen mit mehr als einem Treffer werden NICHT geraten, sondern als
    mehrdeutig gemeldet und in der Karte leer gelassen -- der Doppel-Ingest muss
    erst in GAMS bereinigt werden.
    """
    hits = {}  # sig -> [pid, ...]
    print(f"PID-Aufloesung: pruefe o:szd.{start}..{end} fuer {len(want)} Signaturen")
    for n in range(start, end + 1):
        pid = f"o:szd.{n}"
        data = _get(f"{BASE}/archive/get/{pid}/METS_SOURCE")
        time.sleep(delay)
        if not data:
            print(f"  {pid}  METS n/a")
            continue
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            print(f"  {pid}  METS nicht wohlgeformt (leer/kaputt)")
            continue
        sig = None
        note = root.find('.//mods:note[@type="signature"]', MODS_NS)
        if note is not None and note.text:
            sig = note.text.strip()
        if not sig:
            t = root.find(".//mods:titleInfo/mods:title", MODS_NS)
            m = RE_SIG.search(t.text) if t is not None and t.text else None
            sig = m.group(0) if m else None
        if sig in want:
            hits.setdefault(sig, []).append(pid)
            print(f"  {pid}  ->  {sig}")

    resolved = {s: p[0] for s, p in hits.items() if len(p) == 1}
    ambiguous = {s: p for s, p in hits.items() if len(p) > 1}
    with open(pidmap, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["signatur", "pid"])
        for sig in sorted(want, key=lambda s: int(re.search(r"\d+", s).group())):
            w.writerow([sig, resolved.get(sig, "")])
    if ambiguous:
        print("MEHRDEUTIG (Doppel-Ingest? erst in GAMS bereinigen, Signatur offen gelassen):")
        for s, p in ambiguous.items():
            print(f"  {s}: {p}")
    miss = sorted(want - set(resolved))
    print(f"Karte: {pidmap}  ({len(resolved)}/{len(want)} eindeutig aufgeloest)")
    if miss:
        print(f"NOCH OFFEN: {', '.join(miss)} -- Bereich erweitern, Faksimiles fehlen oder mehrdeutig")
    return resolved


def load_pidmap(pidmap: Path) -> dict:
    if not pidmap.exists():
        return {}
    with open(pidmap, encoding="utf-8") as f:
        return {r["signatur"]: r["pid"].strip() for r in csv.DictReader(f, delimiter=";") if r["pid"].strip()}


# ----------------------------------------------------------------- backup

def build_object(folder: Path, pid: str, sz: dict, dest_base: Path, dry_run: bool) -> dict:
    """Build one backup object from staging + GAMS METS. Returns a summary dict."""
    book_files = list(folder.glob("Result_*.xml"))
    if len(book_files) != 1:
        raise ValueError(f"{folder.name}: erwartet genau 1 Book-XML")
    book = ET.parse(book_files[0]).getroot()
    booktitle_el = book.find("vi:title", VI)
    booktitle = (booktitle_el.text or "").strip() if booktitle_el is not None else ""
    pages = [p.get(XLINK_HREF) for p in book.findall(".//vi:page", VI)]
    local_pages = []
    for href in pages:
        p = folder / href
        if not p.exists():
            raise ValueError(f"{folder.name}: referenziertes Bild fehlt: {href}")
        local_pages.append(p)

    summary = {"pid": pid, "signature": derive_signature(folder.name),
               "n_pages": len(local_pages), "language": sz.get("language", "")}
    if dry_run:
        return summary

    obj_dir = dest_base / pid.replace(":", "_")
    img_dir = obj_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    mets_content = fetch_mets(pid, obj_dir / "mets.xml")
    meta = parse_mets(mets_content, pid)
    if len(meta["images"]) != len(local_pages):
        raise ValueError(f"{pid}: METS hat {len(meta['images'])} Bilder, Staging {len(local_pages)}")

    for i, (img_meta, src) in enumerate(zip(meta["images"], local_pages), start=1):
        w, h = jpeg_dimensions(src)
        if img_meta["width"] is not None and (w, h) != (img_meta["width"], img_meta["height"]):
            raise ValueError(f"{pid}: Maße {src.name} ({w}x{h}) != {img_meta['id']} "
                             f"({img_meta['width']}x{img_meta['height']})")
        dest = img_dir / f"IMG_{i}.jpg"
        if not (dest.exists() and dest.stat().st_size == src.stat().st_size):
            shutil.copy2(src, dest)

    meta["signature"] = summary["signature"]
    meta["title"] = booktitle or sz.get("title", "") or meta.get("title")
    if sz.get("author"):
        meta["author"] = sz["author"]
    # Echte Katalogsprache aus SZDLEB (nicht der Cirilo-Pauschalwert im METS).
    meta["language"] = sz.get("language") or None
    meta["language_code"] = sz.get("language_code") or None
    meta["container"] = None
    meta["provenance"] = {"ingest_label": INGEST_LABEL, "in_gams": True, "source_folder": folder.name}
    meta["download_date"] = datetime.now().isoformat()
    (obj_dir / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


# ------------------------------------------------------------------- TEI merge

def merge_tei(pid_by_sig: dict, szdleb: dict, tei_out: Path, dry_run: bool) -> int:
    """Clone SZDLEB biblFull for each resolved object, inject PID, merge into tei_out."""
    ET.register_namespace("", TEI_NS)
    tree = ET.parse(tei_out)
    root = tree.getroot()
    list_bibl = root.find(".//tei:listBibl", NS)
    if list_bibl is None:
        raise ValueError(f"{tei_out}: kein <listBibl> gefunden")

    existing = {}
    for bibl in list_bibl.findall("tei:biblFull", NS):
        pid_el = bibl.find('.//tei:altIdentifier/tei:idno[@type="PID"]', NS)
        if pid_el is not None and pid_el.text:
            existing[pid_el.text.strip()] = bibl

    added = replaced = 0
    for sig, pid in sorted(pid_by_sig.items(), key=lambda kv: int(re.search(r"\d+", kv[0]).group())):
        if sig not in szdleb:
            print(f"  WARN {sig}: nicht in SZDLEB -- uebersprungen")
            continue
        bibl = deepcopy(szdleb[sig]["bibl"])
        ms = bibl.find(".//tei:msIdentifier", NS)
        if ms.find('tei:altIdentifier/tei:idno[@type="PID"]', NS) is None:
            alt = ET.SubElement(ms, f"{{{TEI_NS}}}altIdentifier")
            idno = ET.SubElement(alt, f"{{{TEI_NS}}}idno")
            idno.set("type", "PID")
            idno.text = pid
        if pid in existing:
            if not dry_run:
                idx = list(list_bibl).index(existing[pid])
                list_bibl.remove(existing[pid])
                list_bibl.insert(idx, bibl)
            replaced += 1
        else:
            if not dry_run:
                list_bibl.append(bibl)
            added += 1

    if not dry_run:
        ET.indent(tree, space="  ")
        tree.write(tei_out, encoding="utf-8", xml_declaration=True)
    print(f"TEI-Merge ({'dry-run' if dry_run else tei_out.name}): "
          f"{added} neu, {replaced} ersetzt")
    return added + replaced


# ----------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    ap.add_argument("--szdleb", type=Path, default=SZDLEB_DEFAULT)
    ap.add_argument("--tei-out", type=Path, default=DATA_DIR / COLLECTIONS[COLLECTION]["tei"])
    ap.add_argument("--pidmap", type=Path, default=PIDMAP_DEFAULT)
    ap.add_argument("--resolve", nargs=2, type=int, metavar=("START", "END"),
                    help="PIDs per METS-Probing aufloesen und Karte schreiben, dann Ende")
    ap.add_argument("--delay", type=float, default=DELAY)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--tei-only", action="store_true", help="nur TEI-Merge, kein Backup")
    args = ap.parse_args()

    szdleb = load_szdleb(args.szdleb)
    folders = sorted((d for d in args.source.iterdir()
                      if d.is_dir() and RE_FOLDER.match(d.name)),
                     key=lambda d: int(re.search(r"\d+", d.name).group()))
    want = {derive_signature(d.name) for d in folders}
    print(f"{len(folders)} Staging-Objekte, {len(szdleb)} SZ-AAL/L-Eintraege in SZDLEB")
    miss_tei = want - set(szdleb)
    if miss_tei:
        print(f"WARN: ohne SZDLEB-Eintrag: {sorted(miss_tei)}")

    if args.resolve:
        resolve_pids(args.resolve[0], args.resolve[1], want, args.pidmap, args.delay)
        return 0

    pid_by_sig = load_pidmap(args.pidmap)
    pid_by_sig = {s: p for s, p in pid_by_sig.items() if s in want}
    if not pid_by_sig:
        print(f"\nKeine PIDs in {args.pidmap}. Erst: --resolve START END "
              f"(nach Faksimile-Verfuegbarkeit in GAMS).")
        return 1
    unresolved = want - set(pid_by_sig)
    if unresolved:
        print(f"Noch ohne PID (werden uebersprungen): {sorted(unresolved)}")

    dest_base = BACKUP_ROOT / COLLECTIONS[COLLECTION]["subdir"]
    summaries, failed = [], []
    if not args.tei_only:
        for d in folders:
            sig = derive_signature(d.name)
            pid = pid_by_sig.get(sig)
            if not pid:
                continue
            try:
                s = build_object(d, pid, szdleb.get(sig, {}), dest_base, args.dry_run)
                summaries.append(s)
                print(f"  {pid}  {sig:12s} {s['n_pages']:3d} Seiten  {s['language'] or '—'}")
            except Exception as e:  # noqa: BLE001
                failed.append((sig, str(e)))
                print(f"  FEHLER {sig}: {e}")
            if not args.dry_run:
                time.sleep(args.delay)  # throttle GAMS METS downloads

    merge_tei(pid_by_sig, szdleb, args.tei_out, args.dry_run)

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Objekte: {len(summaries)}, "
          f"Seiten: {sum(s['n_pages'] for s in summaries)}")
    if failed:
        print(f"FEHLGESCHLAGEN: {len(failed)}")
        for sig, err in failed:
            print(f"  - {sig}: {err}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
