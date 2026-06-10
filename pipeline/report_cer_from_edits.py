"""CER report from human edits.

Every human-edited page yields a measurement: CER between the raw LLM
text (transcription_llm) and the human-corrected working text
(transcription). Human-checked objects WITHOUT edits count as confirmed
error-free (CER 0) under the project convention that approve means
collated against the facsimile; they are reported separately because
they were not character-corrected.

  python pipeline/report_cer_from_edits.py [--collection NAME] [--markdown PATH]
"""

import argparse
import json

from config import RESULTS_BASE
from evaluate import cer

SKIP_DIRS = {"groundtruth", "test"}
HUMAN_STATUSES = {"approved", "gt_verified"}


def collect(collection_filter: str | None) -> tuple[list[dict], int]:
    rows = []
    approved_without_edits = 0
    for subdir in sorted(RESULTS_BASE.iterdir()):
        if not subdir.is_dir() or subdir.name in SKIP_DIRS:
            continue
        if collection_filter and subdir.name != collection_filter:
            continue
        for f in sorted(subdir.glob("*.json")):
            if f.name.endswith((".bak", "_consensus.json", "_layout.json", "_page.json")):
                continue
            data = json.loads(f.read_text(encoding="utf-8"))
            review = data.get("review") or {}
            pages = data.get("result", {}).get("pages", [])
            edited = [p for p in pages if "transcription_llm" in p]
            if not edited:
                if review.get("status") in HUMAN_STATUSES:
                    approved_without_edits += 1
                continue
            for p in edited:
                raw = p.get("transcription_llm", "")
                corrected = p.get("transcription", "")
                if not corrected.strip():
                    continue
                rows.append({
                    "object_id": data.get("object_id", f.stem),
                    "collection": data.get("collection", subdir.name),
                    "page": p.get("page"),
                    "cer": cer(raw, corrected),
                    "chars": len(corrected),
                })
    return rows, approved_without_edits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection")
    parser.add_argument("--markdown", help="optional output path for a markdown report")
    args = parser.parse_args()

    rows, approved_clean = collect(args.collection)
    if not rows:
        print("Keine editierten Seiten mit transcription_llm gefunden.")
        print(f"(Mensch-geprueft ohne Edits: {approved_clean} Objekte)")
        return

    total_chars = sum(r["chars"] for r in rows)
    # char-weighted corpus CER: per-page CERs weighted by reference length
    weighted = sum(r["cer"] * r["chars"] for r in rows) / total_chars
    per_page = sorted(rows, key=lambda r: -r["cer"])

    lines = [
        "# CER aus menschlichen Korrekturen",
        "",
        f"- Editierte Seiten: {len(rows)} "
        f"({len({r['object_id'] for r in rows})} Objekte, {total_chars:,} Zeichen Referenz)",
        f"- Korpus-CER (zeichengewichtet): **{weighted:.3%}**",
        f"- Mensch-geprueft ohne Edits (per Konvention fehlerfrei, nicht eingerechnet): {approved_clean} Objekte",
        "",
        "| Objekt | Sammlung | Seite | CER | Zeichen |",
        "|---|---|---|---|---|",
    ]
    for r in per_page:
        lines.append(f"| {r['object_id']} | {r['collection']} | {r['page']} | {r['cer']:.2%} | {r['chars']} |")
    report = "\n".join(lines)

    print(report)
    if args.markdown:
        from pathlib import Path
        Path(args.markdown).write_text(report + "\n", encoding="utf-8")
        print(f"\nReport: {args.markdown}")


if __name__ == "__main__":
    main()
