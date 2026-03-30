# Pipeline

## prompts/

Dreischichtiges Prompt-System für die VLM-Transkription:

| Schicht | Datei | Funktion |
|---|---|---|
| 1 — System | `system.md` | Rolle, Regeln, Output-Format (für alle Objekte gleich) |
| 2 — Gruppe | `group_a–e_*.md` | Typspezifische Anweisungen pro Dokumentgruppe |
| 3 — Kontext | `context_template.md` | Objektspezifische Metadaten aus TEI (zur Laufzeit generiert) |

### Gruppen

| Gruppe | Prompt | Objekte | Hauptmerkmal |
|---|---|---|---|
| A | `group_a_handschrift.md` | Tagebücher, Notizbücher (12) | Zweigs Handschrift |
| B | `group_b_typoskript.md` | Typoskripte, Durchschläge (74) | Maschinenschrift |
| C | `group_c_formular.md` | Rechtsdokumente, Finanzen (25) | Druck + Handschrift gemischt |
| D | `group_d_kurztext.md` | Diverses, Büromaterialien (27) | Wenig Text, heterogen |
| E | `group_e_tabellarisch.md` | Verzeichnisse, Kalender (16) | Tabellarisch/Listen |

### Erster Test Case

`example_theaterkarte.md` — vollständig zusammengesetzter Prompt für o:szd.161 (Theaterkarte Jeremias).
