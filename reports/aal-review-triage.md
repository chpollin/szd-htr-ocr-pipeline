# Agent-Triage der 28 geflaggten SZ-AAL-Objekte

Datum: 2026-06-10 · Prüfmodell: claude-opus-4-8 (3 parallele Agenten, strikt lesend) · Methode: Bild-gegen-Text-Vergleich jeder Inhaltsseite gegen die lokalen Faksimiles (`szd-backup/data/autographen/<id>/images/`), gezielte Prüfung des jeweiligen `needs_review`-Grunds.

**Ergebnis: 22 OK · 2 FEHLERHAFT · 4 STRITTIG**

Die 22 OK-Objekte wurden als `agent_verified` markiert (errors_found = Zahl der dokumentierten Kleinbefunde). Die 6 übrigen bleiben ungeprüft und brauchen Operator-Sichtung bzw. Neulauf.

## FEHLERHAFT (Neutranskription nötig)

| Objekt | Titel | Befund |
|---|---|---|
| o_szd.3135 | Stefan Zweig an Hannah Altmann [Okt. 1939] | **Totalausfall:** JSON strukturell defekt — kein `pages`-Array, stattdessen ein einziger Runaway-String (~98k Tokens) mit halluziniertem Inhalt; `total_pages: 0`. Der reale 3-seitige Brief (inkl. Lottes Bleistift-Nachsatz „Herzlichen Gruss! Brief folgt. Lotte") ist nicht brauchbar transkribiert. → Neulauf mit `--force`. |
| o_szd.3375 | Walther Haupolter an SZ, 2.12.1938 (15 Scans: Anwaltsbrief + Abschrift der Scheidungsklage Friderike ./. Stefan Zweig) | **Schwerer Pipeline-Fehler:** nur `result.raw`, JSON nicht parsbar. Modell geriet auf S. 3 an den gepunkteten Trennlinien (`-.-.-.-`) der Klage-Abschrift in eine Wiederholungsschleife, Abbruch nach 131.510 Zeichen. Nur S. 1–3 angelegt (S. 3 unvollständig); **12 von 15 Seiten fehlen**, darunter der volle Wortlaut des Scheidungsurteils. → Neulauf, ggf. mit Chunking/Anti-Repetition. Nebenbefund: Titel „Walter" vs. Briefkopf „Walther" Haupolter. |

Beide Ausfälle sind derselbe Mechanismus: degenerierte Wiederholungsschleife des VLM sprengt die JSON-Struktur. Die Signale (`page_image_mismatch` bzw. Längen-Anomalie) haben korrekt angeschlagen.

## STRITTIG (Operator-Sichtung nötig)

| Objekt | Titel | Strittige Stelle |
|---|---|---|
| o_szd.3231 | Alfred Beierle an Lotte Altmann (Ostende) | Schwerste Handschrift des Sets. Struktur, Zitatfolge (Maeterlinck/Schnitzler/Rilke/Zweig) und Schluss sicher; Zeilenanfang S. 3 „Feier, jähle unbedeckte ihr Herz" wirkt geraten, am Bild nicht auflösbar. |
| o_szd.3277 | SZ an Lotte Altmann, 20.8.1935 | Dichte Kursive S. 2: fragwürdige Eigennamen („Frazerleben", „Waizmann" — vermutlich Weizmann, „Temuande[?]"), improvisierte Einschub-Notation. Halluzinationsprofil, aber nicht widerlegbar. |
| o_szd.3280 | SZ an Lotte Altmann, 8.9.1935 | Hauptbrief treu; vertikale Randnotiz S. 1 semantisch inkohärent („eine sehr angenehme dunkle Geliebte…") — sehr wahrscheinlich teilhalluziniert, korrekte Lesung am Faksimile nicht bestimmbar. Nebenbefunde: „Reulner"→Reichner, „ich tele"→vermutlich „ich tue". |
| o_szd.3306 | SZ an Lotte Altmann, 3.9.1936 (Brasilien) | Sehr eilige Kursive; Inhalt grob treu (São Paulo, Büchersignieren, Zuchthaus-Kapelle, Volkshymne), aber S. 2 inkohärent: „viel weniger was Romans und Schaukel" (sinnlos), doppeltes „ich bewohne ich". |

Gemeinsames Muster: flüchtige Zweig-Kursive, bei der das Modell flüssigen, plausiblen Text liefert, dessen korrekte Lesung auch der Prüf-Agent am Bild nicht sicher bestimmen kann. Entscheidung braucht das Auge des Operators (ggf. höhere Auflösung).

## OK (22 Objekte, als agent_verified markiert)

| Objekt | Kleinbefunde |
|---|---|
| o_szd.3131 | — (Abschiedsbrief Lotte & Stefan an Hannah/Manfred, engl.; Umschlag inkl. EXAMINER-Stempel korrekt) |
| o_szd.3202 | — (dichte engl. Handschrift; beigelegte portug. Zeitungsausschnitte korrekt erfasst) |
| o_szd.3255 | unsichere Lesungen vom Modell selbst markiert |
| o_szd.3256 | „Gefälle" statt wohl „Gefühl"; „feller zu Mut"; doppeltes „aber" |
| o_szd.3257 | „Striderstube", „kleine Glatt" (Fehllesungen schwerer Stellen); S. 2/3 = dasselbe Blatt, korrekt erkannt |
| o_szd.3264 | „Zapfschlosserei" (Zahnarzt-Wortspiel, vgl. 3265), „rischen" |
| o_szd.3265 | — (Doppelfoto S. 1/2 und FREMDES eingelegtes Blatt S. 5 korrekt gelesen, keine Halluzination) |
| o_szd.3267 | interlineare Einfügung „mitte Juni" nur in Notiz, nicht im Text |
| o_szd.3268 | — („Hercheh[?]" selbst markiert) |
| o_szd.3270 | — (color_chart S. 5 redundant mittranskribiert, kein Fehler) |
| o_szd.3272 | „Mascreel"→Masereel, „Huen"→Ihnen, „Tonquel"→Touquet (Umschlag) |
| o_szd.3274 | „am fell am Ort"→wohl „wol am Ort" |
| o_szd.3279 | — („Polland" laut Bild korrekt) |
| o_szd.3282 | „Posthaus Place"→Portland Place |
| o_szd.3307 | — (Umschlag/Seitenzuordnung korrekt; flüchtige Hand nicht wortweise prüfbar) |
| o_szd.3308 | — (Umschläge korrekt; einzelne holprige Stellen nicht entscheidbar) |
| o_szd.3351 | „Worte" eher „Karte" (S. 6); nicht-lineare Original-Seitenfolge korrekt wiedergegeben |
| o_szd.3379 | — (Kopf/Umschlag bestätigt; Unsicherheiten ehrlich markiert) |
| o_szd.3382 | — (Bleistift-Absender „Maria Horn / Hotel d'Jéna" am Bild bestätigt, keine Halluzination) |
| o_szd.3391 | — (Umschlag mit durchgestrichener Nice-Adresse + London-Korrektur korrekt; Absender-Metadatenfrage: Titel „Charlotte Kaufmann" vs. Signatur „Montek[?]", jüd. Landschulheim b/ Potsdam) |
| o_szd.3393 | — (Typoskript Walter Bauer; „Englant" buchstabengetreu vom Original) |
| o_szd.3394 | — (Typoskript; Streichungen und hs. Signatur korrekt erfasst) |

## Querbefunde

1. **Farbkarten-Seiten als Flag-Ursache:** Bei mehreren Objekten (3270, 3279, 3280, 3282, 3306, 3307, 3308) geht das `needs_review`-Flag allein auf die color_chart-Doppelaufnahmen zurück — das Modell transkribiert den dort nochmals sichtbaren Brieftext redundant mit, was die Seitenlängen-Anomalie auslöst. Signal-Artefakt, kein inhaltlicher Fehler. Mögliche Pipeline-Verbesserung: color_chart-Seiten von der page_length-Anomalie ausnehmen.
2. **Zweifel landen in Notizen statt im Text:** Bei flüchtiger Kursive schreibt das Modell flüssigen Text und nennt Unsicherheiten nur in `notes`/confidence-Hinweisen, statt [?] im Fließtext zu setzen. Deckt sich mit dem bekannten Halluzinations-Hauptfehlertyp.
3. **Beide harten Ausfälle sind Generierungs-, keine Lesefehler** (Repetition-Runaway sprengt das JSON) — und beide wurden von den Signalen korrekt gefangen. Präzision der Flags in diesem Set: 2 echte Ausfälle + 4 echte Zweifelsfälle von 28 Flags.

## Stellvertreter-Sichtung am Faksimile (2026-07-08)

Agentische Sichtung als Entscheidungsvorlage, in Operator-Delegation vom 08.07. Provenienz und Reichweite sind damit festgehalten, die eigentliche Freigabe der Korrekturen bleibt beim Operator. Prüfmodell claude-opus-4-8, strikt lesend gegen die lokalen Faksimiles unter `szd-backup/data/autographen/<id>/images/`. Vorgehen war das gezielte Nachlesen der oben genannten Streitpunkte, mit Ausschnittsvergrößerung an den kritischen Stellen. Kein Ergebnis-JSON und nichts an GAMS wurde verändert; die Befunde sind Vorschläge zur Nachkorrektur.

Bei den vier strittigen Objekten brauchen alle vier Korrektur, drei davon mit sicherer neuer Lesung, eines nur teilweise auflösbar. Bei der Gegenprobe halten alle vier agent-geprüften Briefe der Sichtung stand.

### Strittige Objekte

**o_szd.3231 (Beierle an Lotte Altmann) — Korrektur nötig, Lesung nur teils recoverbar.** Der geflaggte Zeilenanfang S. 3 „Feier, jähle unbedeckte ihr Herz" ist keine treue Lesung, die Wortfolge ergibt keinen kohärenten Satz und ist geraten. Eine sichere Ersatzlesung liefert der Scan an dieser Stelle nicht, Beierles Hand ist die schwerste des Sets. Ein konkreter Teilbefund derselben Passage: „im Urapalast war" liest sich am Bild eher als „im Ufapalast war", also der UFA-Palast (Kino). Die Stelle braucht einen Editor mit Übung in Beierles Hand oder eine höhere Auflösung.

**o_szd.3277 (SZ an Lotte Altmann, 20.8.1935) — Korrektur nötig, mehrere sichere Stellen.** Die dichte Kursive S. 2 löst sich am vergrößerten Bild weitgehend auf.

- „Temuande[?]" ist **„Temianka"** (der Geiger Henri Temianka). Sichere Lesung, quergestützt durch o_szd.3274 und die Randnotiz von o_szd.3280, wo derselbe Name steht.
- Das vom Modell mit „[?]" ersetzte Wort danach ist **„schrieb"** („Temianka schrieb nicht, ebensowenig Rose W.").
- „die meiner Frau geworden ist" ist **„(die eine Duzfreundin meiner Frau geworden ist)"**, danach **„sie machen"** statt „die machen".
- „Waizmann" gibt das Geschriebene treu wieder und braucht keine Korrektur. Der Bezug ist mit hoher Wahrscheinlichkeit Chaim Weizmann, im Manuskript steht die Form „Waizmann".
- „großes Frazerleben!" ist ein Nichtwort und braucht Korrektur. Beste Lesung im Kontext (nach Prag, Wien, Paris „dann großes … in London") ist **„großes Faulenzerleben!"**. Rest­unsicherheit an den Anfangsbuchstaben, semantisch aber klar getragen.

**o_szd.3280 (SZ an Lotte Altmann, 8.9.1935) — Korrektur nötig, Randnotiz vollständig neu lesbar.** Die vertikale Randnotiz S. 1 ist entgegen dem Erstbefund weder inkohärent noch halluziniert, sie liest sich am gedrehten Ausschnitt klar als:

> „Von Temianka habe ich nie mehr etwas direkt gehört, es war eine sehr angenehme dunkle Geschichte mit seiner Schwester in Salzburg, über die ich noch nichts Näheres weiss."

Gegenüber der vorliegenden Transkription sind das die Korrekturen „von Tausends" zu „Von Temianka", „habe ich mehr" zu „habe ich nie mehr", „dunkle Geliebte" zu „dunkle Geschichte", „und daher schwerer in Salzburg" zu „mit seiner Schwester in Salzburg", „über sie ist noch nichts Näheres weiss" zu „über die ich noch nichts Näheres weiss". Nebenbefunde bestätigt: die Adresszeile „Reulner" ist **„Reichner"** (Verlag Herbert Reichner, quergestützt durch o_szd.3277). „ich tele das hier" ist am Bild nicht sicher, vermutlich „ich tue das hier", geringe Konfidenz.

**o_szd.3306 (SZ an Lotte Altmann, 3.9.1936, Brasilien) — Korrektur nötig, zwei sichere Stellen.**

- „viel weniger was Romans und Schaukel" ist eine schwere Fehllesung. Am Bild stehen drei Autorennamen, **„… Ludwig und Romains und Duhamel"** (Emil Ludwig, Jules Romains, Georges Duhamel). Die Namen Romains und Duhamel sind sicher, das Wort davor („viel" oder „weil") bleibt unsicher.
- Das doppelte „ich bewohne ich bloss drei Zimmer" löst sich auf. Am Zeilenende steht **„hier bewohne ich"**, dann „bloss drei Zimmer". Die Dopplung ist ein Lesefehler, mittlere Konfidenz.

### Gegenprobe (agent-geprüfte Briefe)

**o_szd.3202 (Lotte an Hanna & Manfred, engl., 12.1.1941) — bestätigt.** Die dichte englische Hand S. 3 deckt sich Zeile für Zeile mit der Transkription, von „Dear Hanna & Manfred, Rio 12.I.41" bis „he did not want to do it for the money!", inklusive der interlinearen Einfügung „(a needle with)". Die Agent-Prüfung hält.

**o_szd.3274 (SZ an Lotte Altmann, 30.7.1935) — hält, geflaggte Stelle aufgelöst.** Kopf, Körper und Namen (Toscanini, Walter, Temianka, Walter Bauer, Marienbad) sind treu. Der Kleinbefund „am fell am Ort" ist die Redewendung **„wohl fehl am Ort"** („dort wären Sie vorläufig wohl fehl am Ort!"). Damit ist die einzige offene Stelle geklärt, die Prüfung hält.

**o_szd.3379 (Joachim Maass an Lotte Altmann, 24.1.1936) — bestätigt.** Kopf „Altona/Elbe, Palmaille 21, 24.I.36", Anrede, Körper (Stoffwechselstörung, Beriberi, Skorbut, Sanatorium Schweiz) und Signatur „Joachim Maass" stimmen. Die Agent-Prüfung hält.

**o_szd.3393 (Walter Bauer an Lotte Altmann, 13.8.1935, Typoskript) — hält.** Das Typoskript ist maschinenlesbar sauber erfasst. Das handschriftliche „Englant[?]" auf dem Umschlag ist kursiv „England" mit mehrdeutigem Schlussbuchstaben, die diplomatische Kennzeichnung mit „[?]" ist vertretbar. Die Prüfung hält.

### Querbefund der Sichtung

Der Name „Temianka" (Geiger Henri Temianka) wird vom Modell wiederholt verlesen, als „Temuande" in o_szd.3277 und als „Tausends" in der Randnotiz von o_szd.3280, während er in o_szd.3274 korrekt steht. Eine gezielte Nachkorrektur dieses Namens über das Set hinweg ist angeraten. Das Muster stützt den Erstbefund, dass Eigennamen in flüchtiger Kursive der anfälligste Punkt sind, das Modell setzt dort eine plausible Lautgestalt statt „[?]".
