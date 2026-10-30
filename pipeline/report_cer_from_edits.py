"""CER report from corrections, reported separately per correction source.

Every edited page yields a measurement: CER between the raw LLM text
(transcription_llm) and the corrected working text (transcription). Who
corrected the page decides what the figure means, so pages are grouped by
the `source` values in their edit_history and never pooled: "human" pages
measure against human corrections, "agent" pages against a vision agent's
corrections, "mixed" pages carry both, "unknown" pages lack a source field.
Human-checked objects WITHOUT edits count as confirmed error-free (CER 0)
under the project convention that approve means collated against the
facsimile; they are reported separately because they were not
character-corrected.

  python pipeline/report_cer_from_edits.py [--collection NAME] [--markdown PATH]
"""

import argparse
import json
from pathlib import Path

from config import RESULTS_BASE
from evaluate import cer

SKIP_DIRS = {"groundtruth", "test"}
HUMAN_STATUSES = {"approved", "gt_verified"}
SOURCE_ORDER = ("human", "agent", "mixed", "unknown")
SOURCE_LABELS = {
    "human": "Menschliche Korrekturen",
    "agent": "Agentische Korrekturen",
    "mixed": "Gemischte Korrekturen (Mensch und Agent)",
    "unknown": "Korrekturen ohne Quellenangabe",
}


def edit_source(page: dict) -> str:
    """Classify a page by the sources recorded in its edit_history."""
    sources = {h.get("source") for h in page.get("edit_history") or []}
    sources.discard(None)
    if sources == {"human"}:
        return "human"
    if sources == {"agent"}:
        return "agent"
    if "human" in sources:
        return "mixed"
    return "unknown"


def collect(
    results_base: Path, collection_filter: str | None
) -> tuple[list[dict], int]:
    rows = []
    approved_without_edits = 0
    for subdir in sorted(results_base.iterdir()):
        if not subdir.is_dir() or subdir.name in SKIP_DIRS:
            continue
        if collection_filter and subdir.name != collection_filter:
            continue
        for f in sorted(subdir.glob("*.json")):
            if f.name.endswith(
                (".bak", "_consensus.json", "_layout.json", "_page.json")
            ):
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
                rows.append(
                    {
                        "object_id": data.get("object_id", f.stem),
                        "collection": data.get("collection", subdir.name),
                        "page": p.get("page"),
                        "source": edit_source(p),
                        "review_status": review.get("status") or "-",
                        "cer": cer(raw, corrected),
                        "chars": len(corrected),
                    }
                )
    return rows, approved_without_edits


def summarize(rows: list[dict]) -> dict[str, dict]:
    """Character-weighted corpus CER per correction source."""
    summary = {}
    for source in SOURCE_ORDER:
        group = [r for r in rows if r["source"] == source]
        if not group:
            continue
        chars = sum(r["chars"] for r in group)
        summary[source] = {
            "pages": len(group),
            "objects": len({r["object_id"] for r in group}),
            "chars": chars,
            "cer": sum(r["cer"] * r["chars"] for r in group) / chars if chars else 0.0,
        }
    return summary


def render(rows: list[dict], approved_clean: int) -> str:
    summary = summarize(rows)
    lines = [
        "# CER aus Korrekturen, getrennt nach Korrekturquelle",
        "",
        "Erzeugt mit `python pipeline/report_cer_from_edits.py`. Gruppiert nach dem Feld "
        "`source` in `edit_history`. Die Gruppen werden nicht zusammengelegt, weil nur "
        "menschliche Korrekturen als Referenz gegen menschlich geprüfte Texte gelten.",
        "",
    ]
    for source, s in summary.items():
        lines.append(
            f"- {SOURCE_LABELS[source]}: {s['pages']} Seiten ({s['objects']} Objekte, "
            f"{s['chars']:,} Zeichen Referenz), Korpus-CER (zeichengewichtet) **{s['cer']:.3%}**"
        )
    lines += [
        f"- Mensch-geprüft ohne Edits (per Konvention fehlerfrei, nicht eingerechnet): {approved_clean} Objekte",
        "",
        "| Objekt | Sammlung | Seite | Quelle | Review-Status | CER | Zeichen |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (SOURCE_ORDER.index(r["source"]), -r["cer"])):
        lines.append(
            f"| {r['object_id']} | {r['collection']} | {r['page']} | {r['source']} | "
            f"{r['review_status']} | {r['cer']:.2%} | {r['chars']} |"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collection")
    parser.add_argument("--markdown", help="optional output path for a markdown report")
    args = parser.parse_args()

    rows, approved_clean = collect(RESULTS_BASE, args.collection)
    if not rows:
        print("Keine editierten Seiten mit transcription_llm gefunden.")
        print(f"(Mensch-geprueft ohne Edits: {approved_clean} Objekte)")
        return

    report = render(rows, approved_clean)
    print(report)
    if args.markdown:
        Path(args.markdown).write_text(report + "\n", encoding="utf-8")
        print(f"\nReport: {args.markdown}")


if __name__ == "__main__":
    main()
