"""Aggregierte Qualitätsstatistiken über alle Transkriptionsergebnisse.

Liest alle result JSONs und zeigt Signal-Verteilung pro Gruppe und Sammlung.
"""

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

from config import GROUP_LABELS, RESULTS_BASE


def scan_results(collection: str | None = None, group: str | None = None) -> list[dict]:
    """Load all result JSONs, optionally filtered by collection/group."""
    results = []
    dirs = []
    if collection:
        dirs.append(RESULTS_BASE / collection)
    else:
        for subdir in sorted(RESULTS_BASE.iterdir()):
            if subdir.is_dir() and subdir.name != "test":
                dirs.append(subdir)

    for d in dirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            if "collection" not in data:
                continue
            if group and data.get("group") != group:
                continue
            results.append(data)
    return results


def aggregate_signals(results: list[dict]) -> dict:
    """Compute aggregate quality statistics."""
    total = len(results)
    if total == 0:
        return {"total": 0}

    needs_review_count = 0
    reason_counts = Counter()
    confidence_counts = Counter()
    group_stats = defaultdict(lambda: {"total": 0, "needs_review": 0, "reasons": Counter()})
    collection_stats = defaultdict(lambda: {"total": 0, "needs_review": 0})
    broken_count = 0

    for data in results:
        qs = data.get("quality_signals", {})
        grp = data.get("group", "?")
        col = data.get("collection", "?")
        conf = data.get("result", {}).get("confidence", "?")

        confidence_counts[conf] += 1
        group_stats[grp]["total"] += 1
        collection_stats[col]["total"] += 1

        if "raw" in data.get("result", {}):
            broken_count += 1

        if qs.get("needs_review"):
            needs_review_count += 1
            group_stats[grp]["needs_review"] += 1
            collection_stats[col]["needs_review"] += 1
            for reason in qs.get("needs_review_reasons", []):
                reason_counts[reason] += 1
                group_stats[grp]["reasons"][reason] += 1

    return {
        "total": total,
        "needs_review": needs_review_count,
        "needs_review_pct": round(needs_review_count / total * 100, 1),
        "broken": broken_count,
        "reasons": dict(reason_counts.most_common()),
        "confidence": dict(confidence_counts.most_common()),
        "by_group": {k: dict(v) for k, v in sorted(group_stats.items())},
        "by_collection": {k: dict(v) for k, v in sorted(collection_stats.items())},
    }


def print_report(stats: dict):
    """Print formatted quality report."""
    print(f"{'='*60}")
    print(f"SZD-HTR Quality Report — {stats['total']} Objekte")
    print(f"{'='*60}")
    print()

    nr = stats["needs_review"]
    pct = stats["needs_review_pct"]
    print(f"needs_review:  {nr}/{stats['total']} ({pct}%)")
    print(f"broken (raw):  {stats['broken']}")
    print()

    print("Confidence:")
    for conf, count in stats["confidence"].items():
        print(f"  {conf or '(leer)':10s} {count:4d}")
    print()

    print("Review-Gründe:")
    for reason, count in stats["reasons"].items():
        print(f"  {reason:25s} {count:4d}")
    print()

    print(f"{'Gruppe':<20s} {'Gesamt':>6s} {'Review':>7s} {'%':>6s}  Top-Gründe")
    print("-" * 70)
    for grp, gs in sorted(stats["by_group"].items()):
        total = gs["total"]
        review = gs["needs_review"]
        pct = round(review / total * 100) if total else 0
        reasons = gs.get("reasons", {})
        top = ", ".join(f"{r}({c})" for r, c in
                        sorted(reasons.items(), key=lambda x: -x[1])[:3])
        _, label = GROUP_LABELS.get(grp, ("?", grp))
        print(f"  {label:<18s} {total:>6d} {review:>7d} {pct:>5d}%  {top}")
    print()

    print(f"{'Sammlung':<20s} {'Gesamt':>6s} {'Review':>7s} {'%':>6s}")
    print("-" * 45)
    for col, cs in sorted(stats["by_collection"].items()):
        total = cs["total"]
        review = cs["needs_review"]
        pct = round(review / total * 100) if total else 0
        print(f"  {col:<18s} {total:>6d} {review:>7d} {pct:>5d}%")


def main():
    parser = argparse.ArgumentParser(description="SZD-HTR Quality Report")
    parser.add_argument("--collection", "-c", help="Nur diese Sammlung")
    parser.add_argument("--group", "-g", help="Nur diese Gruppe")
    parser.add_argument("--json", action="store_true", help="Output als JSON")
    args = parser.parse_args()

    results = scan_results(args.collection, args.group)
    stats = aggregate_signals(results)

    if args.json:
        # Convert Counter objects to dicts for JSON serialization
        for grp_data in stats.get("by_group", {}).values():
            if "reasons" in grp_data and isinstance(grp_data["reasons"], Counter):
                grp_data["reasons"] = dict(grp_data["reasons"])
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print_report(stats)


if __name__ == "__main__":
    main()
