"""Smoke-/Regressionstest fuer den deterministischen Page-JSON->TEI-Export.

Eigenstaendig, keine pytest-Abhaengigkeit:  python pipeline/test_export_tei.py
Laeuft ohne API-Key. Sichert zwei Kontrakte ab, von denen die Byte-Identitaet zum
teiCrafter-Prototyp abhaengt:
  1. jsround() = JS Math.round (round-half-up, floor(v+0.5)) -- Grundlage der
     bbox-Pixelumrechnung; Pythons round() (banker's rounding) wuerde driften.
  2. build_tei() erzeugt wohlgeformtes XML in Default- UND enrich/carry_notes-Modus.
Exit 0 = gruen, Exit 1 = Regression.
"""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from export_tei import build_tei, jsround

FIXTURE = Path(__file__).resolve().parent.parent / "results" / "lebensdokumente" / "o_szd.100_page.json"


def main() -> int:
    failed = 0
    out = []

    def check(desc: str, cond: bool) -> None:
        nonlocal failed
        out.append(("ok   " if cond else "FAIL ") + desc)
        if not cond:
            failed += 1

    # 1. jsround: round-half-up wie JS Math.round (Pixelkoordinaten sind nicht-negativ).
    for v, exp in [(0.0, 0), (0.4, 0), (0.5, 1), (0.6, 1), (1.5, 2), (2.5, 3), (10.0, 10)]:
        check(f"jsround({v}) == {exp}", jsround(v) == exp)

    # 2. build_tei: wohlgeformtes XML in allen drei Modi auf echtem Page-JSON.
    if FIXTURE.exists():
        pj = json.loads(FIXTURE.read_text(encoding="utf-8"))
        for label, kwargs in [("default", {}),
                              ("enrich", {"enrich": True}),
                              ("enrich+carry_notes", {"enrich": True, "carry_notes": True})]:
            ok = False
            try:
                xml = build_tei(pj, **kwargs)
                ET.fromstring(xml)
                ok = xml.lstrip().startswith("<?xml")
            except Exception as e:  # noqa: BLE001 -- Testdiagnose
                out.append(f"     ({label}: {type(e).__name__}: {e})")
            check(f"build_tei({label}) -> wohlgeformtes XML", ok)

        # 3. End-to-End: line-lokale Marker-Garantie + carry_notes auf injiziertem Inhalt.
        pj2 = json.loads(FIXTURE.read_text(encoding="utf-8"))
        target = next((p for p in (pj2.get("pages") or []) if (p.get("text") or "").strip()), None)
        if target is not None:
            target["text"] = "alpha ~~weg\nund weg~~ omega"  # mehrzeilige Tilgung
            target["notes"] = "Test-Seitennotiz"
            literal = False
            try:
                xe = build_tei(pj2, enrich=True)
                ET.fromstring(xe)
                # an \n getrennt -> jede Zeile hat ungerade ~~-Zahl -> KEIN <del>, Marker literal
                literal = "~~weg" in xe and "und weg~~" in xe
            except Exception as e:  # noqa: BLE001 -- Testdiagnose
                out.append(f"     (multiline: {type(e).__name__}: {e})")
            check("mehrzeilige ~~Tilgung~~ bleibt literal (line-lokale Garantie e2e)", literal)
            noted = False
            try:
                xn = build_tei(pj2, carry_notes=True)
                ET.fromstring(xn)
                noted = '<note resp="#szd-htr-ai" type="page">Test-Seitennotiz</note>' in xn
            except Exception as e:  # noqa: BLE001 -- Testdiagnose
                out.append(f"     (carry_notes: {type(e).__name__}: {e})")
            check('carry_notes -> attributierte Seitennotiz <note resp="#szd-htr-ai">', noted)
    else:
        out.append(f"WARN Fixture fehlt, build_tei-Checks uebersprungen: {FIXTURE}")

    print("\n".join(out))
    print("=" * 60)
    if failed:
        print(f"REGRESSION: {failed} Checks fehlgeschlagen")
        return 1
    print(f"PASS: alle {len(out)} Checks gruen")
    return 0


if __name__ == "__main__":
    sys.exit(main())
