"""Coverage-Diagnose: findet Objekte ohne nutzbaren Transkriptionstext und klaert
die Ursache (stiller Transkriptions-Fehlschlag vs. echte Leer-/Faksimile-Vorlage).

Deterministisch, READ-ONLY, KEIN API-Call. Loest selbst KEINE Re-Transkription aus --
gibt nur den fertigen Befehl dafuer aus (Kosten-/Lane-Entscheidung des Operators).

Zwei Befunde:
  * empty_pagejson  -- Page-JSON hat pages[]==[]; das OCR-Ergebnis ist ebenfalls leer,
    obwohl Bilder vorhanden sind  -> STILLER FEHLSCHLAG, per Re-Transkription behebbar.
  * all_blank       -- Seiten vorhanden, aber alle blank/color_chart  -> i.d.R. reine
    Faksimile-/Leervorlage, nichts zu transkribieren (zur Kenntnis, kein Fix).

Usage:
    python pipeline/diagnose_coverage.py            # Report nach reports/coverage-gaps.json
    python pipeline/diagnose_coverage.py --quiet     # nur Datei schreiben
"""

import argparse
import json
import sys
from pathlib import Path

from config import COLLECTIONS, PROJECT_ROOT, RESULTS_BASE

_SKIP = ("_page.json", "_layout.json", "_consensus.json", "_mets.xml")


def find_ocr_file(collection: str, object_id: str):
    """Primaeres OCR-Ergebnis results/<col>/{id}_{model}.json (ohne _page/_layout/...)."""
    d = RESULTS_BASE / collection
    for p in sorted(d.glob(f"{object_id}_*.json")):
        n = p.name
        if n.endswith(_SKIP) or n.endswith(".tei.xml"):
            continue
        return p
    return None


def ocr_stats(collection: str, object_id: str) -> dict:
    fp = find_ocr_file(collection, object_id)
    if not fp:
        return {"ocr_file": None, "ocr_pages": 0, "ocr_text_pages": 0, "images": 0}
    try:
        d = json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return {"ocr_file": fp.name, "ocr_pages": 0, "ocr_text_pages": 0, "images": 0}
    pages = (d.get("result") or {}).get("pages") or []
    return {
        "ocr_file": fp.name,
        "ocr_pages": len(pages),
        "ocr_text_pages": sum(1 for p in pages if (p.get("transcription") or "").strip()),
        "images": len((d.get("metadata") or {}).get("images") or []),
    }


def diagnose() -> dict:
    empty_pagejson, all_blank = [], []
    total = 0
    for col in COLLECTIONS:
        d = RESULTS_BASE / col
        if not d.exists():
            continue
        for fp in sorted(d.glob("*_page.json")):
            total += 1
            oid = fp.name[:-len("_page.json")]
            pj = json.loads(fp.read_text(encoding="utf-8"))
            pages = pj.get("pages") or []
            if len(pages) == 0:
                rec = {"object_id": oid, "collection": col}
                rec.update(ocr_stats(col, oid))
                empty_pagejson.append(rec)
            elif sum(1 for p in pages if (p.get("text") or "").strip()) == 0:
                types: dict = {}
                for p in pages:
                    t = p.get("type", "?")
                    types[t] = types.get(t, 0) + 1
                all_blank.append({"object_id": oid, "collection": col,
                                  "pages": len(pages), "types": types})

    # Re-Transkriptions-Befehle (nur fuer stille Fehlschlaege MIT Bildern)
    retry = [f"python pipeline/transcribe.py {r['object_id']} -c {r['collection']} --force"
             for r in empty_pagejson if r["images"] > 0]

    return {
        "summary": {
            "total_objects": total,
            "with_text": total - len(empty_pagejson) - len(all_blank),
            "empty_pagejson": len(empty_pagejson),
            "all_blank": len(all_blank),
            "retransscribable": len(retry),
        },
        "empty_pagejson": sorted(empty_pagejson, key=lambda r: (r["collection"], r["object_id"])),
        "all_blank": sorted(all_blank, key=lambda r: (r["collection"], r["object_id"])),
        "retry_commands": retry,
    }


def main():
    ap = argparse.ArgumentParser(description="Coverage-Diagnose (read-only, kein API-Call)")
    ap.add_argument("--quiet", action="store_true", help="nur Report-Datei schreiben")
    args = ap.parse_args()

    report = diagnose()
    out_dir = PROJECT_ROOT / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "coverage-gaps.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.quiet:
        print(out_path)
        return

    s = report["summary"]
    print("=" * 64)
    print("COVERAGE-DIAGNOSE (read-only, kein API-Call)")
    print("=" * 64)
    print(f"  Objekte gesamt:            {s['total_objects']}")
    print(f"  mit Text (nutzbar):        {s['with_text']}")
    print(f"  leeres Page-JSON:          {s['empty_pagejson']}  (stille Fehlschlaege)")
    print(f"    davon re-transkribierbar:{s['retransscribable']}  (Bilder vorhanden)")
    print(f"  alle Seiten blank:         {s['all_blank']}  (reine Faksimile-/Leervorlage)")
    print(f"\nReport: {out_path}")
    if report["retry_commands"]:
        print(f"\nRe-Transkription der {len(report['retry_commands'])} stillen Fehlschlaege")
        print("(Operator-Entscheidung -- Kosten; loest dieses Skript NICHT selbst aus):")
        for cmd in report["retry_commands"][:5]:
            print(f"  {cmd}")
        if len(report["retry_commands"]) > 5:
            print(f"  ... ({len(report['retry_commands']) - 5} weitere in {out_path.name})")


if __name__ == "__main__":
    main()
