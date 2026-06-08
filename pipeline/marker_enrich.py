"""Optionale, deterministische Marker-Anreicherung fuer den TEI-Export (opt-in).

Wandelt diplomatische Transkriptionsmarker in echte TEI-Editorial-Elemente um --
ABER nur, wo die Umwandlung LOKAL (innerhalb EINER Zeile) eindeutig und
ausbalanciert ist. Alles Mehrdeutige (mehrzeilig, unbalanciert, verschachtelt,
allein-auf-der-Zeile) bleibt bewusst woertlicher Text.

Leitregel (aus adversarischer Pruefung, siehe knowledge/teicrafter-integration.md):
  Niemals raten. Ein NICHT umgewandelter Marker ist verlustfrei (= heutiger Stand);
  ein FALSCH getaggter Marker ist Datenkorruption. Also: Fail-safe auf Literal.

Warum line-lokal statt seitenweit: Der Export teilt den Seitentext erst in Absaetze
(\\n{2,}) und dann in Zeilen (\\n) und ruft die Anreicherung pro Zeile auf. Eine
mehrzeilige Tilgung/Einfuegung hat auf ihrer Eroeffnungszeile eine ungerade Marker-
Zahl -> die Zeilen-Pruefung greift NICHT -> sie bleibt korrekt Literal. So koennen
mehrzeilige Spans nie falsch zerschnitten werden.

Arbeitet auf der BEREITS XML-escapeten Zeile (esc_text). Marker-Delimiter
([ ] { } ~ ?) ueberleben das Escaping; Payloads sind schon escapet (auch '{< x}' ->
'{&lt; x}'), daher entsteht stets gueltiges XML.

Konvertiert in v1:
  [...N...]  -> <gap reason="illegible" quantity="N" unit="chars"/>
               (nur wenn NICHT allein auf der Zeile -- ein gap-only-<lb> faellt im
                Editor auf cells=0 und verschwaende, darum dann Literal)
  ~~x~~      -> <del rend="strikethrough">x</del>
               (nur bei GERADER ~~-Zahl auf der Zeile, Payload ohne ~ [ ] { } = kein Nesting)
  {x}        -> <add place="above">x</add>
               (nur bei balancierten {}-Klammern auf der Zeile, Payload ohne ~ [ ] = kein
                Nesting; NICHT der Platzhalter {eingefuegt})
  WORT[?]    -> <unclear reason="illegible" cert="low">WORT</unclear>
               (nur direkt am Wort ohne Leerzeichen -- genau die protokollkonforme Stelle,
                annotation-protocol.md S3.2 "direkt nach dem unsicheren Wort, ohne Leerzeichen")

Bewusst NICHT in v1 (bleibt Literal, verlustfrei): plain [...] (meist allein-auf-Zeile),
[Stempel:]/[Label:] (braucht standoff-<note> mit @target, vom Zeilen-Hook nicht erreichbar),
mehrzeilige Spans, unbalancierte/verschachtelte Marker, [?] mit Leerzeichen / in Laeufen,
{eingefuegt}-Platzhalter, das [?3?]-Sonderzeichen.
"""

import re

_GAP_N = re.compile(r"\[\.{3}(\d+)\.{3}\]")
_DEL = re.compile(r"~~([^~\[\]{}]+?)~~")
_ADD = re.compile(r"\{([^{}~\[\]]+)\}")
_UNCLEAR = re.compile(r"([^\s\[\]{}~]+)\[\?\]")
_PLACEHOLDER = {"eingefuegt", "eingefügt"}


def _has_other_text(line: str, start: int, end: int) -> bool:
    """True, wenn ausserhalb des Spans [start:end] noch Nicht-Whitespace steht."""
    return bool(line[:start].strip() or line[end:].strip())


def enrich_line(escaped_line: str) -> str:
    """Wandle die Marker einer bereits escapeten Zeile um -- nur lokal eindeutige
    Faelle; alles andere bleibt unveraendert (Fail-safe auf Literal)."""
    s = escaped_line

    # 1. [...N...] gezaehlte Luecke -> <gap/>  (nie allein auf der Zeile)
    def _gap(m: "re.Match") -> str:
        if not _has_other_text(s, m.start(), m.end()):
            return m.group(0)  # allein auf der Zeile -> Literal (sonst cells=0, Zeile weg)
        return f'<gap reason="illegible" quantity="{m.group(1)}" unit="chars"/>'
    s = _GAP_N.sub(_gap, s)

    # 2. ~~x~~ Tilgung -> <del>  (nur bei gerader ~~-Anzahl auf DIESER Zeile = sauber paarbar)
    if s.count("~~") % 2 == 0:
        s = _DEL.sub(lambda m: f'<del rend="strikethrough">{m.group(1)}</del>', s)

    # 3. {x} Einfuegung -> <add>  (nur bei balancierten {}-Klammern auf DIESER Zeile)
    if s.count("{") == s.count("}"):
        def _add(m: "re.Match") -> str:
            if m.group(1).strip().lower() in _PLACEHOLDER:
                return m.group(0)  # Platzhalter ohne echten Inhalt -> Literal
            return f'<add place="above">{m.group(1)}</add>'
        s = _ADD.sub(_add, s)

    # 4. WORT[?] -> <unclear>WORT</unclear>  (nur direkt am Wort, protokollkonform)
    s = _UNCLEAR.sub(
        lambda m: f'<unclear reason="illegible" cert="low">{m.group(1)}</unclear>', s
    )
    return s
