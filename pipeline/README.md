# Pipeline

## prompts/

Dreischichtiges Prompt-System für die VLM-Transkription:

| Schicht | Datei | Funktion |
|---|---|---|
| 1 — System | `system.md` | Rolle, Regeln, Output-Format (für alle Objekte gleich) |
| 2 — Gruppe | `group_*.md` | Typspezifische Anweisungen pro Dokumentgruppe |
| 3 — Kontext | `context_template.md` | Objektspezifische Metadaten aus TEI (zur Laufzeit generiert) |

### Gruppen (9 Stueck)

| Gruppe | Prompt | Sammlungen | Hauptmerkmal |
|---|---|---|---|
| A | `group_a_handschrift.md` | Lebensdok., Werke | Zweigs Handschrift, Kurrent |
| B | `group_b_typoskript.md` | Lebensdok., Werke, Aufsatz | Maschinenschrift, Durchschläge |
| C | `group_c_formular.md` | Lebensdokumente | Formulare, Urkunden |
| D | `group_d_kurztext.md` | Lebensdokumente | Kurztexte, Karten |
| E | `group_e_tabellarisch.md` | Lebensdok., Aufsatz | Register, Kalender, Listen |
| F | `group_f_korrekturfahne.md` | Werke, Aufsatz | Druck + handschriftl. Korrekturen |
| G | `group_g_konvolut.md` | Werke | Gemischte Materialien |
| H | `group_h_zeitungsausschnitt.md` | Aufsatzablage | Zeitungsdruck, ggf. Fraktur |
| I | `group_i_korrespondenz.md` | Korrespondenzen | Briefe, Postkarten |

## Scripts

| Script | Funktion |
|---|---|
| `test_single.py` | Einzelobjekt-Transkription (Multi-Collection, `--list` für verfügbare Tests) |
| `tei_context.py` | TEI-Parser: extrahiert Metadaten, generiert Kontext, ordnet Gruppen zu |
| `build_viewer_data.py` | Baut `catalog.json` + `data/{collection}.json` aus enriched Ergebnis-JSONs |

## Beispiel

`example_theaterkarte.md` — vollständig zusammengesetzter Prompt (alle 3 Schichten) für o:szd.161.
