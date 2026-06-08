"""Regressionstest fuer die TEI-kanonische Sammlungszuordnung (Dedup-Fix fb48ca0).

Eigenstaendig, keine pytest-Abhaengigkeit:  python pipeline/test_canonical_collection.py
Laeuft OHNE das 23GB-Backup und ohne API-Key -- der TEI-Branch nutzt ausschliesslich die
im Repo liegenden data/szd_*_tei.xml, der Tie-Break-Branch ein temporaeres Fake-Backup.

Schreibt den Dedup-Kontrakt fest, damit ein Refactor von _tei_owner_index /
_canonical_collection / discover_objects die 34 Backup-Doppellistungen (Objekte, die
physisch in korrespondenzen/ UND lebensdokumente/ liegen) nicht lautlos wieder als
Doppel-Transkription einfuehrt.
Exit 0 = alles gruen, Exit 1 = Regression.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import transcribe as t


def main() -> int:
    failed = 0
    out = []

    def check(desc: str, cond: bool) -> None:
        nonlocal failed
        out.append(("ok   " if cond else "FAIL ") + desc)
        if not cond:
            failed += 1

    idx = t._tei_owner_index()

    # 1. korrespondenzen traegt 0 PIDs zum Owner-Index bei -- KEIN Parser-Bug:
    #    die korrespondenzen-TEI katalogisiert auf Konvolut-Ebene (o:szd.korrespondenzen.NAME),
    #    nicht auf numerischer Einzelbrief-Ebene; es gibt also keine o:szd.N-Objekt-PID.
    #    Daher laufen ALLE korrespondenzen-Objekte ueber den Backup-Tie-Break. Bekommt die
    #    TEI je echte numerische PIDs, schlaegt dieser Test bewusst an und erzwingt eine
    #    Re-Validierung des Tie-Breaks.
    korr = sum(1 for c in idx.values() if c == "korrespondenzen")
    check("korrespondenzen liefert 0 Owner-Index-PIDs (Konvolut-Granularitaet)", korr == 0)

    # 2. Reale TEI-Doppellistung: o:szd.118 steht in lebensdokumente- UND werke-TEI.
    #    setdefault + COLLECTIONS-Reihenfolge (lebensdokumente vor werke) loesen
    #    deterministisch auf lebensdokumente auf -- so wurde das Objekt auch real
    #    transkribiert. Der Tie-Break ist SCHARF (nicht theoretisch).
    check("o:szd.118 (doppelt in lebd+werke) -> lebensdokumente",
          t._canonical_collection("o_szd.118") == "lebensdokumente")

    # 3. Eindeutig TEI-gefuehrtes lebensdokumente-Objekt bleibt lebensdokumente.
    check("o:szd.141 (nur lebd-TEI) -> lebensdokumente",
          t._canonical_collection("o_szd.141") == "lebensdokumente")

    # 4. TEI-Branch hat Vorrang vor dem Backup: ein gemockter Index entscheidet, OHNE dass
    #    BACKUP_ROOT existieren muss.
    orig_idx = t._tei_owner_index
    try:
        t._tei_owner_index = lambda: {"o:szd.999999": "werke"}
        check("gemockter Index: o:szd.999999 -> werke (TEI-Branch vor Backup)",
              t._canonical_collection("o_szd.999999") == "werke")
    finally:
        t._tei_owner_index = orig_idx

    # 5. Orphan-Pfad (PID in KEINER TEI): erste COLLECTIONS-Sammlung mit Backup-Dir gewinnt.
    #    Genau dieser fragile, reihenfolgeabhaengige Zweig bestimmt die 5 echten Orphans
    #    (o_szd.76/77/175/176/179). Test gegen ein temporaeres Fake-Backup -- kein 23GB noetig.
    orig_root = t.BACKUP_ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            oid = "o_szd.99999999"  # in keiner TEI
            for col in ("lebensdokumente", "korrespondenzen"):
                d = root / t.COLLECTIONS[col]["subdir"] / oid
                d.mkdir(parents=True)
                (d / "metadata.json").write_text("{}", encoding="utf-8")
            t.BACKUP_ROOT = root
            check("Orphan in lebd+korr Backup -> lebensdokumente (COLLECTIONS-Reihenfolge)",
                  t._canonical_collection(oid) == "lebensdokumente")
            # Nur noch in korrespondenzen vorhanden -> korrespondenzen.
            shutil.rmtree(root / t.COLLECTIONS["lebensdokumente"]["subdir"])
            check("Orphan nur in korr Backup -> korrespondenzen",
                  t._canonical_collection(oid) == "korrespondenzen")
    finally:
        t.BACKUP_ROOT = orig_root

    print("\n".join(out))
    print("=" * 60)
    if failed:
        print(f"REGRESSION: {failed}/{len(out)} Checks fehlgeschlagen")
        return 1
    print(f"PASS: alle {len(out)} Checks gruen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
