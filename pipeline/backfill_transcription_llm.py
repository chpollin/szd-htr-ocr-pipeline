"""One-off migration: set transcription_llm on already-edited pages.

The raw LLM text of an edited page is the original_transcription of its
OLDEST edit_history entry. Idempotent; pages without edits are untouched.

  python pipeline/backfill_transcription_llm.py [--dry-run]
"""

import argparse
import json

from config import RESULTS_BASE

SKIP_DIRS = {"groundtruth", "test"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    files_changed = 0
    pages_set = 0
    for subdir in sorted(RESULTS_BASE.iterdir()):
        if not subdir.is_dir() or subdir.name in SKIP_DIRS:
            continue
        for f in sorted(subdir.glob("*.json")):
            if f.name.endswith((".bak", "_consensus.json", "_layout.json", "_page.json")):
                continue
            data = json.loads(f.read_text(encoding="utf-8"))
            pages = data.get("result", {}).get("pages", [])
            changed = False
            for rp in pages:
                history = rp.get("edit_history")
                if not history or "transcription_llm" in rp:
                    continue
                rp["transcription_llm"] = history[0].get("original_transcription", "")
                pages_set += 1
                changed = True
            if changed:
                files_changed += 1
                if not args.dry_run:
                    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  {f.name}")

    mode = "DRY-RUN, nichts geschrieben" if args.dry_run else "geschrieben"
    print(f"{files_changed} Datei(en), {pages_set} Seite(n) mit transcription_llm ({mode})")


if __name__ == "__main__":
    main()
