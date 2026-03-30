# SZD-HTR — Research Journal

Dieses Journal dokumentiert alle Arbeitssessions, Erkenntnisse und Entscheidungen im Projektverlauf.

---

## 2026-03-30 — Session 1: Projektplanung

### Was wurde gemacht
- CLAUDE.md gelesen und Projektanforderungen verstanden
- Implementierungsplan erstellt (→ [Plan.md](../Plan.md))
- Knowledge-Ordner als Research-Vault angelegt

### Entscheidungen
- **Gemini 3.1 Flash-Lite** als zweiten Transkriptions-Provider aufgenommen (neben Claude Vision)
  - Grund: Günstig ($0.25/1M input), schnell, 1M-Token-Kontext, multimodal
  - Ermöglicht Kosten-/Qualitätsvergleich zwischen Providern
- **Kategoriale Konfidenz** (sicher/prüfenswert/problematisch) statt numerischer Scores
  - Erfahrung aus coOCR HTR: LLMs können Qualität nicht zuverlässig numerisch einschätzen

### Offene Fragen
- [ ] Wie gut erkennt Gemini 3.1 Flash-Lite Kurrentschrift? → Testlauf nötig
- [ ] Optimale Bildgröße für API-Calls? Originale sind 4912×7360 (~1.4MB)
- [ ] Lizenz klären: MIT für Code, CC-BY für Daten?

### Nächste Schritte
- Phase 1 umsetzen: pyproject.toml, Verzeichnisstruktur, Config
- Object-IDs der 10 Startset-Objekte ermitteln

---

## 2026-03-30 — Session 2: Pipeline aufgebaut, erste Tests, alle Sammlungen analysiert

### TEI-Metadaten heruntergeladen und analysiert

Vier TEI-XML-Dateien von stefanzweig.digital heruntergeladen:

| Sammlung | TEI-Datei | Einträge | mit PID | Größe |
|---|---|---|---|---|
| Lebensdokumente | `szd_lebensdokumente_tei.xml` | 143 | 120 | 666 KB |
| Werke | `szd_werke_tei.xml` | 352 | 162 | 1.6 MB |
| Aufsatzablage | `szd_aufsatzablage_tei.xml` | 624 | 624 | 2.5 MB |
| Korrespondenzen | `szd_korrespondenzen_tei.xml` | 723 | 0 (TEI) | 1.5 MB |

Backup-Daten (lokal, nicht im Repo): 1186 Korrespondenzen, 625 Aufsätze, 169 Faksimiles mit metadata.json und Bildern.

**Gesamtbestand: 2305+ digitalisierte Objekte über 4 Sammlungen.**

### Dreischichtiges Prompt-System entwickelt

Architektur: System-Prompt (global) → Gruppen-Prompt (A–E) → Objekt-Kontext (aus TEI).

Prompts abgelegt unter `pipeline/prompts/`:
- `system.md` — Rolle, diplomatische Transkription, JSON-Output
- `group_a_handschrift.md` — Zweigs Handschrift, Kurrent
- `group_b_typoskript.md` — Maschinenschrift, Durchschläge
- `group_c_formular.md` — Formulare, Urkunden
- `group_d_kurztext.md` — Kurztexte, Karten
- `group_e_tabellarisch.md` — Register, Kalender
- `context_template.md` — Template für TEI-Metadaten-Injection

### Erste Transkriptionstests mit Gemini 3.1 Flash Lite

Test-Script: `pipeline/test_single.py` — sendet Bilder + dreischichtigen Prompt an Gemini Vision.

| Objekt | Gruppe | Sprache | Confidence | Beobachtung |
|---|---|---|---|---|
| Theaterkarte Jeremias (o:szd.161) | D: Kurztext | DE | high | Gedruckter + handschriftl. Text korrekt, Abrissstreifen fehlt |
| Certified Copy of Marriage (o:szd.160) | C: Formular | EN | high | Alle Formularfelder korrekt, tabellarisch linearisiert |
| Verlagsvertrag Grasset (o:szd.78) | B: Typoskript | FR | high | Kompletter franz. Vertragstext, Durchstreichungen erkannt, „Lu et approuvé" |
| Tagebuch 1918, 5 Seiten (o:szd.72) | A: Handschrift | DE | high | Zweigs Handschrift flüssig gelesen, R.=Rolland erkannt, ~~Eltern~~ Korrektur |

**Kernbefund:** Gemini 3.1 Flash Lite liefert auf allen 4 Gruppen (A–D) high confidence. Selbst Zweigs Handschrift wird flüssig transkribiert — das ist überraschend gut für ein „lite" Modell.

### Viewer für Faksimile-Transkription-Vergleich

`docs/viewer.html` — Responsive Split-View:
- Desktop: Bild links, Transkription rechts
- Mobile: Bild oben, Text unten
- Bilder direkt von GAMS geladen (keine Downloads nötig)
- Seiten-Navigation, Zoom, Swipe-Support

### Alle 4 Sammlungen analysiert — Prompt-Gruppen erweitert

Aus der Analyse der Werke, Aufsatzablage und Korrespondenzen ergeben sich 4 neue Prompt-Gruppen:

| Gruppe | Neu? | Quelle | Objekte | Besonderheit |
|---|---|---|---|---|
| F: Korrekturfahne | NEU | Werke + Aufsatz | ~55 | Gedruckter Text + handschriftliche Korrekturen |
| G: Konvolut | NEU | Werke | 24 | Gemischte Materialien in einem Objekt |
| H: Zeitungsausschnitt | NEU | Aufsatzablage | 312 | Gedruckt (oft Fraktur!), verschiedene Layouts |
| I: Korrespondenz | NEU | Korrespondenzen | ~1186 | Handschriftliche Briefe, Briefkonventionen |

### Erkenntnisse

1. **GAMS-URLs funktionieren als direkte Bildquellen** — kein Download/Hosting nötig für den Viewer.
2. **Korrespondenzen-TEI** hat nur Verzeichnis-Charakter (wer-an-wen, wann), keine physischen Beschreibungen. Metadaten müssen aus den Backup-metadata.json kommen.
3. **Erwin Rieger** ist die zweithäufigste Hand in der Aufsatzablage (225×) — Zweigs Sekretär/Mitarbeiter, hat Registerblätter angelegt. Eigene Handschrift-Charakteristik.
4. **Zeitungsausschnitte (312)** sind ein komplett neuer Dokumenttyp — brauchen Fraktur-Prompt.
5. **Lotte Zweig** ist die zweithäufigste Hand in den Werken (83×) — eigene Handschrift, oft als Typist (Durchschläge).

### Offene Fragen

- [ ] Wie gut erkennt Gemini Frakturschrift? → Test mit Zeitungsausschnitt nötig
- [ ] Korrekturfahnen: Wie markiert man Korrekturen im Output? Brauchen wir ein erweitertes Markup?
- [ ] Konvolute: Wie geht die Pipeline mit gemischten Dokumenttypen in einem Objekt um?
- [ ] Viewer: Sammlungs-Tabs einbauen, damit man zwischen Lebensdokumente/Werke/Aufsatz/Korrespondenz wechseln kann

### Nächste Schritte (abgeschlossen in Session 3)

1. ~~Neue Prompts entwickeln für Gruppen F, H, I~~
2. ~~Je 1 Testobjekt pro neuer Gruppe transkribieren~~
3. ~~Viewer um Sammlungs-Navigation erweitern~~
4. Ergebnisse vergleichen und Prompts iterieren

---

## 2026-03-30 — Session 3: Phase 2 abgeschlossen, alle Sammlungen integriert

### Neue Gruppen-Prompts

Drei neue Prompt-Dateien in `pipeline/prompts/`:
- `group_f_korrekturfahne.md` — Gedruckter Text + handschriftliche Korrekturen (Tintenfarben als Korrektur-Runden)
- `group_h_zeitungsausschnitt.md` — Zeitungsdruck, Fraktur-Hinweise (s/f, ch/ck), Spalten-Layout
- `group_i_korrespondenz.md` — Briefstruktur (Anrede/Grußformel), Postkarten-Doppelseiten

Gruppe G (Konvolut) bewusst noch nicht umgesetzt — zu wenige Objekte (24), zu heterogen. Kann bei Bedarf später ergänzt werden.

### Pipeline auf Multi-Collection erweitert

`test_single.py` refactored:
- `BACKUP_ROOT` zeigt jetzt auf `szd-backup/data/` (nicht mehr `/lebensdokumente/`)
- `COLLECTIONS`-Dict mappt Sammlung → Backup-Unterordner
- Jeder Test Case hat ein `collection`-Feld
- Enriched JSON-Output enthält Metadaten + GAMS-URLs
- `--list` zeigt alle verfügbaren Tests

Neue Module:
- `tei_context.py` — TEI-Parser mit `parse_tei_for_object()`, `format_context()`, `resolve_group()`, `context_from_backup_metadata()` (Fallback für Korrespondenzen)
- `build_viewer_data.py` — baut `docs/data.json` aus enriched Ergebnis-JSONs

### Drei neue Test-Objekte transkribiert

| Objekt | Sammlung | Gruppe | Confidence | Beobachtung |
|---|---|---|---|---|
| Der Bildner (o:szd.287) | Werke | F: Korrekturfahne | high | Komplettes Rodin-Gedicht fehlerfrei, Stempel erkannt |
| Aus der Werkstatt der Dichter (o:szd.2215) | Aufsatzablage | H: Zeitungsausschnitt | high | Zweigs Werkstatt-Essay, Antiqua (kein Fraktur-Test) |
| Brief an Max Fleischer (o:szd.1079) | Korrespondenzen | I: Korrespondenz | high | Briefumschlag + Text, Zweigs Jugendhandschrift (1901) |

**Gesamtstand: 7/7 Objekte, alle high confidence, alle 4 Sammlungen abgedeckt.**

### Viewer mit Sammlungs-Navigation

`docs/viewer.html` komplett umgebaut:
- Daten aus `docs/data.json` geladen (kein hardcoded JavaScript mehr)
- Sammlungs-Tabs: Alle | Lebensdokumente | Werke | Aufsatzablage | Korrespondenzen
- Neue Tag-Farben für Gruppen F, H, I
- `build_viewer_data.py` als Build-Schritt

### Refactoring

- Prompts werden aus Markdown-Dateien geladen (nicht mehr dupliziert in test_single.py)
- Pfade konfigurierbar via Umgebungsvariablen (`SZD_BACKUP_ROOT`, `HTR_MODEL`)
- Error-Handling für fehlende Bilder, API-Fehler, unbekannte Tests
- Repo-URL konsistent: `szd-htr-ocr-pipline`

### Erkenntnisse

1. **Gemini 3.1 Flash Lite meistert alle Dokumenttypen** — Handschrift, Typoskript, Korrekturfahnen, Zeitungsausschnitte, Briefe. Kein einziges Objekt unter high confidence.
2. **Fraktur noch nicht getestet** — der Zeitungsausschnitt war Antiqua. Echte Fraktur-Ausschnitte müssen noch gezielt gesucht werden.
3. **Korrespondenzen-TEI hat keine physischen Beschreibungen** — Fallback auf Backup-metadata.json funktioniert. Der Kontext ist dünner, aber die Gruppen-Prompts kompensieren.
4. **GAMS-URLs als direkte Bildquellen** funktionieren zuverlässig für den Viewer.
5. **Enriched JSON-Format** (Metadaten + Ergebnis in einer Datei) vereinfacht den Viewer-Build erheblich.

### Offene Fragen

- [ ] Fraktur-Erkennung: Gezielt Zeitungsausschnitte mit Fraktur suchen und testen
- [ ] `--auto-context` Flag in test_single.py integrieren (tei_context.py ist fertig)
- [ ] Batch-Modus für mehrere Objekte nacheinander
- [ ] Provider-Vergleich: Claude Vision und GPT-4o gegen Gemini testen
- [ ] Gruppe G (Konvolut) bei Bedarf ergänzen

### Nächste Schritte

1. Phase 3: `--auto-context` und Batch-Transkription
2. Phase 4: Provider-Vergleich, Fraktur-Tests, Prompt-Iteration
3. Phase 5: TEI-Integration via teiCrafter
