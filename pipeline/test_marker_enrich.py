"""Regressionstest fuer den deterministischen Marker-Konverter (marker_enrich.enrich_line).

Eigenstaendig, keine pytest-Abhaengigkeit:  python pipeline/test_marker_enrich.py
Schreibt den Fail-safe-Kontrakt fest (im Zweifel Literal) und prueft zwei Invarianten:
  1. erwartetes Verhalten je Marker-Familie + Haertefall,
  2. jede Ausgabe ist wohlgeformtes XML (kann nie kaputtes Markup erzeugen).
Exit 0 = alles gruen, Exit 1 = Regression.
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from marker_enrich import enrich_line
# Test- und Produktions-Escaping muessen identisch bleiben: dieselbe Funktion nutzen, die
# der TEI-Export vor enrich_line anwendet, statt sie hier zu duplizieren (Drift-Schutz).
from export_tei import esc_text as esc


def run(line: str) -> str:
    return enrich_line(esc(line))


# (Eingabe, Praedikat(out) -> bool, Beschreibung)
CASES = [
    # --- Stempel / Postmark / Marginalie ---
    ("[Stempel: WIEN 22.5.01]",
     lambda o: o == '<note type="stamp">WIEN 22.5.01</note>', "Stempel sole -> note type=stamp"),
    ("[Poststempel: ZUERICH 1932]",
     lambda o: o == '<note type="postmark">ZUERICH 1932</note>', "Poststempel -> note type=postmark"),
    ("[Marginalie: Anmerkung am Rand]",
     lambda o: o == '<note type="marginal">Anmerkung am Rand</note>', "Marginalie -> note type=marginal"),
    # --- gedrehter Text (Protokoll §3.7, reviewer-gesetzt) ---
    ("[quer: Nachsatz am linken Rand]",
     lambda o: o == '<seg rend="rotate(90)">Nachsatz am linken Rand</seg>', "quer -> seg rotate(90)"),
    ("[kopf: Bitte umgehend antworten!]",
     lambda o: o == '<seg rend="rotate(180)">Bitte umgehend antworten!</seg>', "kopf -> seg rotate(180)"),
    ("[Quer: Grossschreibung toleriert]",
     lambda o: o.startswith('<seg rend="rotate(90)">'), "Label case-insensitiv"),
    ("[quer: ]",
     lambda o: o == "[quer: ]", "leerer Payload -> literal (kein leeres seg)"),
    ("Text [quer: X] mitten drin",
     lambda o: "<seg" not in o and "[quer: X]" in o, "quer mid-line -> literal"),
    ("[quer: Anfang ohne Ende",
     lambda o: o == "[quer: Anfang ohne Ende", "quer mehrzeilig (kein ]) -> literal"),
    ("Brief [Stempel: X] hier",
     lambda o: "<note" not in o and "[Stempel: X]" in o, "Stempel mid-line -> literal"),
    ("[Stempel: AUSLIEFERUNG",
     lambda o: o == "[Stempel: AUSLIEFERUNG", "Stempel mehrzeilig (kein ]) -> literal"),
    # --- unsicher [?] (ohne reason; Satzzeichen ausserhalb) ---
    ("Latzust[?]",
     lambda o: o == '<unclear cert="low">Latzust</unclear>', "[?] am Wort -> unclear ohne @reason"),
    ("mirste.[?]",
     lambda o: o == '<unclear cert="low">mirste</unclear>.', "[?] -- Satzzeichen bleibt ausserhalb"),
    ("der [?] hier",
     lambda o: "<unclear" not in o, "[?] mit Leerzeichen -> literal"),
    ("und [?] [?] [?]",
     lambda o: "<unclear" not in o, "[?]-Lauf -> literal"),
    ("Kopf [?3?] art",
     lambda o: "[?3?]" in o and "<unclear" not in o, "[?3?]-Sonderzeichen -> literal"),
    # --- Luecken ---
    ("a [...5...] b",
     lambda o: '<gap reason="illegible" quantity="5" unit="chars"/>' in o, "gez. Luecke mid-line -> gap"),
    ("[...5...]",
     lambda o: o == "[...5...]", "gez. Luecke sole -> literal (cells=0-Schutz)"),
    ("a [...] b",
     lambda o: '<gap reason="illegible"/>' in o, "plain Luecke mid-line -> gap"),
    ("[...]",
     lambda o: o == "[...]", "plain Luecke sole -> literal (cells=0-Schutz)"),
    # --- Tilgung ~~ (ohne @rend) ---
    ("x ~~weg~~ y",
     lambda o: "<del>weg</del>" in o and "rend" not in o, "Tilgung (gerade) -> del ohne @rend"),
    ("a ~~ ~~ b",
     lambda o: "<del> </del>" in o, "gestrichenes Leerzeichen -> del"),
    ("~~a~~ b ~~c",
     lambda o: "<del" not in o, "ungerade ~~ -> literal"),
    ("EX ~ LIBRIS ~ tantum",
     lambda o: "<del" not in o, "einzelnes ~ (Trenner) -> literal"),
    ("~~Latzust[?]~~",
     lambda o: o == '<del><unclear cert="low">Latzust</unclear></del>',
     "Tilgung um unsicheres Wort -> del>unclear (zulaessiges, wohlgeformtes Nesting)"),
    # --- Einfuegung {} KONSERVATIV (ohne @place) ---
    ("Er ist {sehr} verzweifelt",
     lambda o: "<add>sehr</add>" in o and "place" not in o, "echte Einfuegung -> add ohne @place"),
    ("die {Persoenlich} wie {die} {hoehere} Welt",
     lambda o: "<add" not in o, ">=2 {} pro Zeile (VLM-Rauschen) -> literal"),
    ("{einigermassen}",
     lambda o: "<add" not in o, "sole-on-line {} -> literal"),
    ("Menschen {Mue-} dort",
     lambda o: "<add" not in o, "Worttrennungs-Fragment ({...-}) -> literal"),
    ("x {mit ihrer ungeheuren} y",
     lambda o: "<add" not in o, "Mehrwort {} (>2) -> literal"),
    ("vor {eingefügt} dem",
     lambda o: "<add" not in o and "{eingefügt}" in o, "{eingefügt}-Platzhalter -> literal"),
    ("offen {kein Schluss",
     lambda o: "<add" not in o, "unbalancierte { -> literal"),
    # --- Escaping / Robustheit ---
    ("Schuster & Löffler[?]",
     lambda o: "&amp;" in o and '<unclear cert="low">Löffler</unclear>' in o,
     "XML-Escaping bleibt erhalten, Token korrekt gewickelt"),
    ("x {a<b} y",
     lambda o: "&lt;" in o and "<add>a&lt;b</add>" in o, "Sonderzeichen im Add-Payload escaped"),
    # --- Nesting-Fail-safe ---
    ("~~a {b} c~~",
     lambda o: "<add>b</add>" in o and "~~a" in o,
     "Nesting ~~{ }: inneres {} konvertiert, ~~ bleibt literal"),
    ("leer",
     lambda o: o == "leer", "gewoehnlicher Text unveraendert"),
]


def main() -> int:
    failed = 0
    for line, pred, desc in CASES:
        out = run(line)
        ok_behaviour = pred(out)
        # Invariante: jede Ausgabe muss wohlgeformtes XML sein
        try:
            ET.fromstring(f"<r>{out}</r>")
            ok_xml = True
        except ET.ParseError:
            ok_xml = False
        ok = ok_behaviour and ok_xml
        if not ok:
            failed += 1
            why = []
            if not ok_behaviour:
                why.append("Verhalten")
            if not ok_xml:
                why.append("XML kaputt")
            print(f"FAIL [{', '.join(why)}] {desc}")
            print(f"     in : {line!r}")
            print(f"     out: {out!r}")
        else:
            print(f"ok   {desc}")

    print("=" * 60)
    if failed:
        print(f"REGRESSION: {failed}/{len(CASES)} Faelle fehlgeschlagen")
        return 1
    print(f"PASS: alle {len(CASES)} Faelle gruen (Verhalten + wohlgeformtes XML)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
