"""Character error rate of the raw LLM output against the texts a person confirmed.

Purpose: give the one figure a reader can recompute for the objects whose review
status was set by a person (`approved`, `gt_verified`).

Data flow: every result file under RESULTS_BASE with a human review status
contributes all of its pages. A page that was edited keeps the raw output in
`transcription_llm` and the confirmed text in `transcription`; a page approved
without a change has no `transcription_llm` and counts as free of errors, under
the project convention that approving means collating against the facsimile.
Both texts pass `evaluate.normalize_text` (Unicode NFC, whitespace, hyphenation,
markup removed, transcription-guidelines.md §5). The rate is the Levenshtein
distance summed over the pages, divided by the characters of the confirmed text.

What the figure is not: the confirmed texts were made by correcting the LLM's
output, so it measures how much the checkers changed, not the distance to an
independently produced ground truth. `report_cer_from_edits.py` reports the
edited pages alone, per correction source, and therefore gives higher rates.

Usage:
    python pipeline/report_cer_confirmed.py [--json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from config import RESULTS_BASE
from evaluate import normalize_text

SKIP_DIRS = frozenset({"groundtruth", "test"})
SKIP_SUFFIXES = (".bak", "_consensus.json", "_layout.json", "_page.json")
HUMAN_STATUSES = frozenset({"approved", "gt_verified"})


def levenshtein(a: str, b: str) -> int:
    """Edit distance with unit costs for insertion, deletion and substitution."""
    if a == b:
        return 0
    previous = list(range(len(b) + 1))
    for i, char_a in enumerate(a, 1):
        current = [i]
        for j, char_b in enumerate(b, 1):
            current.append(
                min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (char_a != char_b))
            )
        previous = current
    return previous[-1]


def measure_object(data: dict) -> dict | None:
    """Return the counts of one result file, or None when no person confirmed it."""
    if (data.get("review") or {}).get("status") not in HUMAN_STATUSES:
        return None
    counts = {"pages": 0, "pages_with_text": 0, "pages_edited": 0, "distance": 0, "chars": 0}
    for page in data.get("result", {}).get("pages", []):
        counts["pages"] += 1
        confirmed = normalize_text(page.get("transcription") or "")
        if not confirmed:
            continue
        counts["pages_with_text"] += 1
        counts["chars"] += len(confirmed)
        if "transcription_llm" in page:
            counts["pages_edited"] += 1
            counts["distance"] += levenshtein(normalize_text(page["transcription_llm"]), confirmed)
    return counts


def collect(results_base: Path) -> dict[str, dict]:
    """Sum the counts per collection over all result files a person confirmed."""
    totals: dict[str, dict] = {}
    for subdir in sorted(results_base.iterdir()):
        if not subdir.is_dir() or subdir.name in SKIP_DIRS:
            continue
        for path in sorted(subdir.glob("*.json")):
            if path.name.endswith(SKIP_SUFFIXES):
                continue
            counts = measure_object(json.loads(path.read_text(encoding="utf-8")))
            if counts is None:
                continue
            total = totals.setdefault(subdir.name, {"objects": 0, **dict.fromkeys(counts, 0)})
            total["objects"] += 1
            for key, value in counts.items():
                total[key] += value
    return totals


def with_rates(totals: dict[str, dict]) -> dict[str, dict]:
    """Add the sum over all collections and the rate of every row."""
    overall = {key: sum(row[key] for row in totals.values()) for key in next(iter(totals.values()))}
    rows = {**totals, "all": overall}
    for row in rows.values():
        row["cer"] = row["distance"] / row["chars"] if row["chars"] else 0.0
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", action="store_true", help="print the rows as JSON")
    args = parser.parse_args()
    totals = collect(RESULTS_BASE)
    if not totals:
        raise SystemExit(f"no human-confirmed result files under {RESULTS_BASE}")
    rows = with_rates(totals)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return
    for name, row in rows.items():
        print(
            f"{name}: {row['objects']} objects, {row['pages']} pages "
            f"({row['pages_with_text']} with text, {row['pages_edited']} edited), "
            f"distance {row['distance']} over {row['chars']} characters, CER {row['cer']:.2%}"
        )


if __name__ == "__main__":
    main()
