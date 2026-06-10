"""Regression test for archival unit derivation (derive_unit).

Standalone, no pytest:  python pipeline/test_unit_derivation.py
Runs without API key or backup. Contract: unit = signature minus its last
dot segment; signatures without one are their own unit. Also checks that
UNIT_TERMS only references known collections and covers the letter
collections. Exit 0 = green.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_viewer_data import derive_unit
from config import COLLECTION_LABELS, COLLECTIONS, UNIT_TERMS


def main() -> int:
    failed = 0

    def check(desc: str, cond: bool) -> None:
        nonlocal failed
        print(("ok   " if cond else "FAIL ") + desc)
        if not cond:
            failed += 1

    # derivation
    cases = [
        ("SZ-AAL/B1.113", "SZ-AAL/B1"),
        ("SZ-AAL/B2.71", "SZ-AAL/B2"),
        ("SZ-SAM/AK.159", "SZ-SAM/AK"),
        ("SZ-AAP/W-AA90.0", "SZ-AAP/W-AA90"),
        ("SZ-AP2/W-F4.3", "SZ-AP2/W-F4"),
        ("SZ-AAP/L3", "SZ-AAP/L3"),  # no dot: own unit
        ("SZ-SAM/W2", "SZ-SAM/W2"),
        ("", ""),
    ]
    for sig, expected in cases:
        check(f"derive_unit({sig!r}) == {expected!r}", derive_unit(sig) == expected)

    # idempotence
    for sig, _ in cases:
        unit = derive_unit(sig)
        check(f"idempotent: derive_unit({unit!r}) == {unit!r}", derive_unit(unit) == unit)

    # dots in earlier path segments are untouched
    check("dot before slash kept: SZ-X.Y/B1 -> SZ-X.Y/B1",
          derive_unit("SZ-X.Y/B1") == "SZ-X.Y/B1")

    # registry consistency
    for col in UNIT_TERMS:
        check(f"UNIT_TERMS-Key {col!r} ist bekannte Sammlung", col in COLLECTIONS)
    for col in ("korrespondenzen", "autographen"):
        check(f"UNIT_TERMS enthaelt {col!r}", col in UNIT_TERMS)
    check("COLLECTION_LABELS deckt genau die Sammlungen ab",
          set(COLLECTION_LABELS) == set(COLLECTIONS))

    print("=" * 60)
    if failed:
        print(f"FAIL: {failed} Check(s) rot")
        return 1
    print("PASS: alle Checks gruen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
