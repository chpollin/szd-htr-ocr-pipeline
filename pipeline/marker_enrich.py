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

Konvertiert (v2.1, nach adversarischer Semantik-Pruefung):
  [Stempel: X]      -> <note type="stamp">X</note>      (ganze Zeile)
  [Poststempel: X]  -> <note type="postmark">X</note>   (ganze Zeile; Postmark != Stempel)
  [Marginalie: X]   -> <note type="marginal">X</note>   (ganze Zeile; Protokoll §3.5)
  WORT[?]    -> <unclear cert="low">WORT</unclear>
               (nur direkt am Wort; KEIN reason="illegible" -- [?] ist unsicher-aber-lesbar
                (50-90%), nicht unleserlich (das waere [...]); nachgestellte Satzzeichen bleiben
                ausserhalb, weil [?] das Wort markiert, nicht den Punkt; §3.2)
  [...N...]  -> <gap reason="illegible" quantity="N" unit="chars"/>
  [...]      -> <gap reason="illegible"/>
               (beide nur NICHT allein auf der Zeile -- ein gap-only-<lb> faellt im
                Editor auf cells=0 und verschwaende, darum dann Literal)
  ~~x~~      -> <del>x</del>
               (gerade ~~-Zahl; OHNE @rend -- Protokoll §3.3 kodiert die Streichungsform
                bewusst nicht, "strikethrough" waere unbelegt. "Kein Nesting" meint ROH-Marker
                ineinander (~~ in ~~); ein in Schritt 1 erzeugtes <unclear>/<gap> DARF dagegen
                in <del>/<add> stehen -- z.B. ~~Wort[?]~~ -> <del><unclear cert="low">Wort
                </unclear></del>, semantisch ein getilgtes unsicheres Wort, stets wohlgeformt)
  {x}        -> <add>x</add>   KONSERVATIV
               (nur GENAU EIN kurzes {Wort}, eingebettet in anderen Text. Der VLM nutzt {}
                massenhaft als Wortsegmentierungs-Rauschen -- ~81% der {} sind keine echten
                Einfuegungen; daher bleiben >=2/Zeile, sole-on-line, Worttrennung (endet auf -),
                Mehrwort und {eingefuegt} literal. OHNE @place -- §3.4 = "ueber der Zeile ODER am
                Rand", "above" waere erfunden.)

Bewusst NICHT (bleibt Literal, verlustfrei): mid-line/mehrzeilige Stempel und sonstige
[Label: ...]-Varianten (Bild/Abbildung/Briefmarke ...), mehrzeilige ~~/{ }-Spans,
unbalancierte/ineinander verschachtelte ROH-Marker (~~ in ~~), [?] mit Leerzeichen / in Laeufen / direkt nach einem Tag,
plain/gez. Luecke allein-auf-Zeile, das [?3?]-Sonderzeichen.
"""

import re

_STAMP = re.compile(r"^(\s*)\[(Stempel|Poststempel):\s?(.*)\]\s*$")
_MARGIN = re.compile(r"^(\s*)\[Marginalie:\s?(.*)\]\s*$")
_UNCLEAR = re.compile(r"([^\s\[\]{}~]+)\[\?\]")
_GAP_N = re.compile(r"\[\.{3}(\d+)\.{3}\]")
_GAP_PLAIN = re.compile(r"\[\.{3}\]")
_DEL = re.compile(r"~~([^~\[\]{}]+?)~~")
_ADD = re.compile(r"\{([^{}~\[\]]+)\}")
_PLACEHOLDER = {"eingefuegt", "eingefügt"}
# Trailing-Satzzeichen, die NICHT zum unsicheren Wort gehoeren (";" bewusst NICHT, sonst
# wuerde eine Entity wie &amp; / &lt; zerschnitten).
_TRAIL = ".,:!?)\"'»«"


def _has_other_text(line: str, start: int, end: int) -> bool:
    """True, wenn ausserhalb des Spans [start:end] noch Nicht-Whitespace steht."""
    return bool(line[:start].strip() or line[end:].strip())


def enrich_line(escaped_line: str) -> str:
    """Wandle die Marker einer bereits escapeten Zeile um -- nur lokal eindeutige
    Faelle; alles andere bleibt unveraendert (Fail-safe auf Literal)."""
    s = escaped_line

    # 0a. Stempel/Poststempel (ganze Zeile) -> <note type="stamp|postmark">
    m = _STAMP.match(s)
    if m:
        typ = "postmark" if m.group(2) == "Poststempel" else "stamp"
        return f'{m.group(1)}<note type="{typ}">{m.group(3)}</note>'
    # 0b. Marginalie (ganze Zeile) -> <note type="marginal">  (Protokoll §3.5)
    m = _MARGIN.match(s)
    if m:
        return f'{m.group(1)}<note type="marginal">{m.group(2)}</note>'

    # 1. WORT[?] -> <unclear cert="low">WORT</unclear>  (ZUERST, auf tag-freiem Text.
    #    KEIN reason="illegible": [?]=unsicher-aber-lesbar (50-90%), nicht unleserlich -- das
    #    waere [...]. Nachgestellte Satzzeichen bleiben ausserhalb (markiert das Wort, nicht
    #    den Punkt; Protokoll §3.2).
    def _unclear(mm: "re.Match") -> str:
        tok = mm.group(1)
        core = tok.rstrip(_TRAIL)
        if not core:
            return mm.group(0)  # nur Satzzeichen vor [?] -> literal
        return f'<unclear cert="low">{core}</unclear>{tok[len(core):]}'
    s = _UNCLEAR.sub(_unclear, s)

    # 2. [...N...] gezaehlte Luecke -> <gap/>  (nie allein auf der Zeile -> sonst cells=0)
    def _gap_counted(mm: "re.Match") -> str:
        if not _has_other_text(s, mm.start(), mm.end()):
            return mm.group(0)
        return f'<gap reason="illegible" quantity="{mm.group(1)}" unit="chars"/>'
    s = _GAP_N.sub(_gap_counted, s)

    # 3. [...] plain Luecke -> <gap/>  (nie allein auf der Zeile)
    def _gap_plain(mm: "re.Match") -> str:
        if not _has_other_text(s, mm.start(), mm.end()):
            return mm.group(0)
        return '<gap reason="illegible"/>'
    s = _GAP_PLAIN.sub(_gap_plain, s)

    # 4. ~~x~~ Tilgung -> <del>  (gerade ~~-Zahl; OHNE @rend -- Protokoll §3.3 kodiert die
    #    Streichungsform bewusst nicht, "strikethrough" waere eine unbelegte Aussage)
    if s.count("~~") % 2 == 0:
        s = _DEL.sub(lambda mm: f'<del>{mm.group(1)}</del>', s)

    # 5. {x} Einfuegung -> <add>  KONSERVATIV. Der VLM nutzt {} massenhaft als
    #    Wortsegmentierungs-Rauschen (laufender Prosatext, >=2/Zeile, sole-on-line,
    #    Worttrennung, Mehrwort) -- ~81% sind KEINE echten Einfuegungen. Daher nur GENAU EIN
    #    kurzes {Wort}, eingebettet in anderen Text, konvertieren; Rest bleibt literal.
    #    OHNE @place -- {} kodiert "ueber der Zeile ODER am Rand" (§3.4), "above" waere erfunden.
    if s.count("{") == 1 and s.count("}") == 1:
        def _add(mm: "re.Match") -> str:
            payload = mm.group(1)
            if payload.strip().lower() in _PLACEHOLDER:
                return mm.group(0)  # {eingefuegt}-Platzhalter -> literal
            if not _has_other_text(s, mm.start(), mm.end()):
                return mm.group(0)  # sole-on-line -> literal
            if payload.rstrip().endswith("-"):
                return mm.group(0)  # Worttrennungs-Fragment -> literal
            if len(payload.split()) > 2:
                return mm.group(0)  # Mehrwort -> unplausible Einfuegung -> literal
            return f'<add>{payload}</add>'
        s = _ADD.sub(_add, s)

    return s
