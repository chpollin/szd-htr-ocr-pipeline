"""Re-parse total failures (result.raw) with the salvage stage of the parser.

A total failure is a result JSON whose `result` holds only the unparseable model
response in `raw`, no `pages`. Most of these responses start as valid JSON and
break off in a repetition loop; parse_api_response() step 6 takes the complete
page objects before that point. This script applies it to the stored responses,
so no API call is needed.

For each recovered object: `result.raw` is replaced by the recovered pages, the
scans after the break-off get "Nicht transkribiert" placeholders (not blank
pages), `result.salvage` records what happened, and quality_signals are
recomputed (-> transcription_status "partial"). Objects without a single
complete page stay untouched and remain "failed" — they need a new API run.

The original responses stay in git history; the migration commit is the
reference. Background: reports/pipeline-totalausfaelle.md.

Usage:
    python pipeline/salvage_raw_results.py --dry-run
    python pipeline/salvage_raw_results.py
"""

import argparse
import json
from datetime import date
from pathlib import Path

from config import COLLECTIONS
from quality_signals import compute_signals
from transcribe import parse_api_response, untranscribed_placeholder

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def main():
    parser = argparse.ArgumentParser(description="Salvage pages from total failures.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    failed = recovered_objects = recovered_pages = text_pages = 0

    for col in COLLECTIONS:
        col_dir = RESULTS_DIR / col
        if not col_dir.exists():
            continue
        for f in sorted(col_dir.glob("*_gemini-*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            result = data.get("result") or {}
            if "raw" not in result:
                continue
            failed += 1

            salvaged, _ = parse_api_response(result["raw"], data["object_id"])
            pages = salvaged.get("pages", [])
            if not pages:
                print(f"  {data['object_id']:12s} keine vollstaendige Seite -> bleibt failed")
                continue

            # Scans actually sent to the model (o_szd.267: 107 of 232, see report)
            input_images = data.get("quality_signals", {}).get(
                "input_images", len(data.get("metadata", {}).get("images", [])))
            last_ok = len(pages)
            for page_nr in range(last_ok + 1, input_images + 1):
                pages.append(untranscribed_placeholder(
                    page_nr, f"Modellantwort nach Seite {last_ok} abgebrochen."))
            salvaged["salvage"]["migrated"] = str(date.today())
            salvaged["salvage"]["script"] = "pipeline/salvage_raw_results.py"

            with_text = sum(1 for p in pages[:last_ok] if (p.get("transcription") or "").strip())
            recovered_objects += 1
            recovered_pages += last_ok
            text_pages += with_text
            print(f"  {data['object_id']:12s} {last_ok:4d}/{input_images:<4d} Seiten gerettet "
                  f"({with_text} mit Text)")

            if not args.dry_run:
                data["result"] = salvaged
                data["quality_signals"] = compute_signals(
                    salvaged, data.get("metadata", {}), input_images)
                f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    mode = "DRY RUN: " if args.dry_run else ""
    print(f"{mode}{failed} Totalausfaelle, {recovered_objects} teilweise gerettet: "
          f"{recovered_pages} Seiten, davon {text_pages} mit Text. "
          f"{failed - recovered_objects} bleiben failed.")
    if not args.dry_run and recovered_objects:
        print("  Danach: backfill_quality_signals.py, build_viewer_data.py")


if __name__ == "__main__":
    main()
