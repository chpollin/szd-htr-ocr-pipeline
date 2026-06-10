"""Regressionstest fuer die Bestandseinheiten-Ableitung (derive_unit).

Eigenstaendig, keine pytest-Abhaengigkeit:  python pipeline/test_unit_derivation.py
Laeuft ohne API-Key und ohne Backup. Sichert den Kontrakt ab, auf dem der
Einheiten-Filter im Viewer steht: Einheit = Signatur minus letztes
Punkt-Segment, signaturlose Objekte haben keine Einheit. Zusaetzlich:
jede Sammlung in COLLECTIONS hat einen Anzeige-Begriff in UNIT_TERMS.
Exit 0 = gruen, Exit 1 = Regression.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_viewer_data import derive_unit
from config import COLLECTIONS, UNIT_TERMS


def main() -> int:
    failed = 0

    def check(desc: str, cond: bool) -> None:
        nonlocal failed
        print(("ok   " if cond else "FAIL ") + desc)
        if not cond:
            failed += 1

    # 1. Ableitung: letztes Punkt-Segment faellt weg.
    cases = [
        ("SZ-AAL/B1.113", "SZ-AAL/B1"),        # Briefkonvolut
        ("SZ-AAL/B2.71", "SZ-AAL/B2"),
        ("SZ-SAM/AK.159", "SZ-SAM/AK"),         # Korrespondenz-Album
        ("SZ-AAP/W-AA90.0", "SZ-AAP/W-AA90"),   # Werkmappe (Suffix .0)
        ("SZ-AP2/W-F4.3", "SZ-AP2/W-F4"),
        ("SZ-AAP/L3", "SZ-AAP/L3"),             # ohne Punkt: selbst die Einheit
        ("SZ-SAM/W2", "SZ-SAM/W2"),
        ("", ""),                                # leer bleibt leer
    ]
    for sig, expected in cases:
        check(f"derive_unit({sig!r}) == {expected!r}", derive_unit(sig) == expected)

    # 2. Idempotenz: eine Einheit bleibt unter erneuter Ableitung stabil.
    for sig, _ in cases:
        unit = derive_unit(sig)
        check(f"idempotent: derive_unit({unit!r}) == {unit!r}", derive_unit(unit) == unit)

    # 3. Kein Schraegstrich-Segment wird angeschnitten (Punkt nur im letzten Segment).
    check("Punkt vor Schraegstrich bleibt: SZ-X.Y/B1 -> SZ-X.Y/B1",
          derive_unit("SZ-X.Y/B1") == "SZ-X.Y/B1")

    # 4. Registry-Vollstaendigkeit: jede Sammlung hat einen Einheiten-Begriff.
    for col in COLLECTIONS:
        check(f"UNIT_TERMS enthaelt {col!r}", col in UNIT_TERMS)

    print("=" * 60)
    if failed:
        print(f"FAIL: {failed} Check(s) rot")
        return 1
    print("PASS: alle Checks gruen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
