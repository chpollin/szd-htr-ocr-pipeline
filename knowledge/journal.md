---
title: "Journal"
aliases: ["Journal", "Research Journal"]
project:
  name: "SZD OCR/HTR Pipeline"
  repository: "https://github.com/chpollin/szd-htr-ocr-pipeline"
method:
  name: "Promptotyping"
  url: "https://dhcraft.org/Promptotyping/"
template:
  name: "Vorlage Journal"
  version: 0.6
  url: "https://dhcraft.org/Promptotyping/promptotyping-document/journal"
  alias: "https://dhcraft.org/Promptotyping/#promptotyping-document-journal"
status: active
language: de
created: 2026-03-30
updated: 2026-10-30
authors: [Christopher Pollin]
related:
  - "[[plan]]"
  - "[[handoff]]"
  - "[[specification]]"
  - "[[transcription-verification]]"
---

# Journal

## Einträge

### 2026-10-30 CER aus Korrekturen nach Quelle getrennt

- Anlass: Audit vom 2026-10-30 zur Herkunft der Korpus-CER von 0,962 Prozent und zur Zahl menschlich geprüfter Objekte.
- Befund: `pipeline/report_cer_from_edits.py` nahm jede Seite mit `transcription_llm` auf, unabhängig von der Korrekturquelle. Alle 56 Seiten hinter dem Wert stammten aus agentischen Korrekturen (`agent_verified`). [[governance]] §4 nannte 21 mensch-geprüfte Objekte, `docs/catalog.json` weist 52 aus, im Stand vom 2026-08-07 bereits 44.
- Entschieden: Die CER aus Korrekturen wird je Quelle aus `edit_history.source` berichtet (human, agent, mixed, unknown) und nie zusammengelegt. `PAPER.md` und `PAPER-FINDINGS.md` bleiben nach `CLAUDE.md` eingefroren, die Korrektur steht als Hinweis in `paper/README.md`.
- Korrigiert: Neulauf 2026-10-30 ergibt 0,948 Prozent für agentisch korrigierte Seiten (56 Seiten, 40 Objekte) und 11,875 Prozent für menschlich korrigierte Seiten (34 Seiten, 23 Objekte). Die Bezeichnung „menschliche Korrekturen“ für den Agentenwert ist in `reports/cer-baseline-report-2026-04-02.md` berichtigt, die Objektzahl in [[governance]] verweist auf den Katalog als Quelle.
- Geändert: `pipeline/report_cer_from_edits.py`, `tests/test_cer_from_edits.py`, `reports/cer-from-edits.md`, `reports/cer-baseline-report-2026-04-02.md`, [[governance]], `paper/README.md`.
- Belege: `python pipeline/report_cer_from_edits.py`, `tests/test_cer_from_edits.py`

### 2026-10-28 verdichtet Journal

- Vorgängerstand: `3d7f216`
- Bereich: alle Einträge vom 2026-03-30 bis 2026-10-28 einschließlich der Liste „Offene Fragen (Stand 2026-04-03)“.
- Ergebnis: Die Sitzungsprotokolle sind auf die Felder der Vorlage Journal 0.6 umgeschrieben und stehen neueste zuerst. Behalten sind Entscheidungen mit Grund, Operator-Entscheidungen, Korrekturen, verworfene Alternativen, alle noch auflösbaren Commit-Hashes und die außerhalb zitierten Stellen mit ihrer Sessionnummer als Anker (Sessions 2, 3, 6, 7, 20, 23, 25b und 26, die Einträge vom 2026-06-08, 2026-07-31, 2026-08-26, 2026-09-25, 2026-10-19 und 2026-10-28). Die Kopfnotiz zur Reihenfolge entfällt, weil die Einträge jetzt nach Datum stehen und doppelte Sessionnummern im Eintrag selbst stehen. Noch offene Punkte, die kein anderes Dokument führte, stehen jetzt in [[plan]] unter „Aus dem Journal übernommene Punkte“. Statistiktabellen, Datei- und Funktionslisten, Stände, Wiedereinstiegsanleitungen und maschinenlokale Pfade sind ausschließlich über Git bewahrt.
- Korrigiert: Die Regel, vergangene Journaleinträge nicht umzuschreiben (`CLAUDE.md`, [[governance]], [[INDEX]], Eintrag vom 2026-10-28 zur Vereinheitlichung), gilt jetzt mit der Ausnahme der Verdichtung nach der Vorlage. Der frühere Wortlaut steht unverändert in `3d7f216`.
- Belege: `3d7f216`

### 2026-10-28 Vereinheitlichung nach Promptotyping-Vorlagen

- Anlass: Freigabe der Projektleitung am 2026-10-28. Die Wissensbasis trug gewachsene Dateinamen, die ihre Funktion nicht signalisierten, und es fehlten Projektbeschreibung, Specification, Architecture und Handoff.
- Entschieden: Die Dokumente folgen dem Naming Contract der Konvention. Jedes umbenannte oder aufgegangene Dokument führt seinen früheren Namen unter `aliases:`, sodass `build_knowledge()` alte Wikilinks und `docs/app.js` alte Lesezeichen umleiten. `review-findings.md` und die beiden Integrationsdokumente behalten ihren Zuschnitt. Vor dem Löschen eines aufgegangenen Dokuments wurde eine Deckungsliste gegen die Zieldokumente geprüft.
- Geändert: Die Zuordnung alt zu neu steht in [[INDEX]] unter „Frühere Dateinamen“ und in `paper/README.md`. Zitierter Stand vor der Vereinheitlichung ist `6f06c8e`, auf ihn beziehen sich Aussagen über die frühere Wissensbasis, auch im Paper zur Methode.
- Belege: `6f06c8e`, `5012d84`, `0a38677`, `91373bd`, `9cc5b97`, `6ff5c88`, `tests/test_knowledge_aliases.py`

### 2026-10-28 Kuratierung für die Fallstudie im Promptotyping-Paper

- Anlass: Das Repository dient als Fallstudie im Paper zur Methode. Eine lesende Prüfung hatte Widersprüche zwischen Wissensstand, Code und Rahmendokumenten gemeldet, jeder Befund wurde vor der Änderung gegen die Dateien geprüft. Ausgangsstand ist `9c5b836`.
- Befund: `CLAUDE.md` nannte CC BY 4.0 für alles, README, `LICENSE`, `CITATION.cff` und `codemeta.json` seit `2641b28` MIT für Code und CC BY 4.0 für Texte. Die Verifikationsdokumentation führte Modellkonsensus im Forschungsteil noch als validierten GT-Ersatz, während ihre Abschnitte zu Agreement Konsistenz ohne Korrektheitsaussage feststellen und das Dashboard ihn seit Session 23 nicht mehr zeigt. Die Empfehlung aus dem A/B/C-Experiment (Session 25b) wurde nie umgesetzt und nie verworfen. README und `CLAUDE.md` nannten allein Opus 4.6 als Modell.
- Entschieden: Inhaltliches wird vollständig korrigiert, Form nur dort, wo sie Lesenden von außen den Zugang erschwert. Reviews, Evaluationen und datierte Befunde bleiben als Beleg stehen. Die Modellangaben folgen den Co-Authored-By-Trailern. Personennamen Dritter in Wissensdokumenten und Berichten werden durch Rolle und Institution ersetzt, Git-Metadaten, Forschungsdaten und die Autorenzeilen unter `paper/drafts/` bleiben unberührt.
- Geändert: `CLAUDE.md` folgt in der Lizenz dem README. [[transcription-verification]] führt den aktuellen Stand zum Modellkonsensus mit der früheren Fassung datiert daneben. Die A/B/C-Empfehlung steht als offene Entscheidung in [[plan]]. Vorgabepfade in `config.py` und den Importskripten sind relativ zum Home-Verzeichnis gebildet. Das README hat den Abschnitt „How this was built“.
- Belege: `9c5b836`, `0cb9625`, `44cb5b0`, `52b6377`, `ca1ebf6`, `d03a285`

### 2026-10-19 Review-Session: Fehlerklassen am Faksimile, Viewer-Fix für Totalausfälle

- Anlass: Gegenlesen der Projekt-Reviewer:in (Universität Salzburg) am Faksimile, Befunde 3–6 in `reports/issue-review-fehlersammlung.md`.
- Befund: Bei Detailaufnahmen ergänzt das LLM am Bildrand angeschnittene Wörter aus anderen Scans und normalisiert sie (`o:szd.1056`). Fraktur-Drucke werden bei Konfidenz `high` über weite Strecken plausibel paraphrasiert („Genien“ → „Gatten“, „Weltfreunde“ → „weltfremden“, `o:szd.2745`, schwächer `o:szd.2759`, Handschrift `o:szd.263`), `needs_review` bleibt `false`. Gruppe F beschreibt den Basistext als Antiqua, beide Drucke sind Fraktur. Randnotizen, Bleistiftzusätze und Stempel fehlen im Text, weil das Annotationsprotokoll `[Marginalie:]` und `[Stempel:]` transkribiert, während die Gruppen-Prompts C, H und I beides in die Notizen schicken. Für Umstellungen fehlt eine Notation. Drei der vier Fehlerklassen sind für die Qualitätssignale unsichtbar, weil ergänzter, paraphrasierter oder weggelassener Text weder Länge noch Marker noch Sprache ändert. Das stützt die Regel, dass Approve „gegengelesen“ heißt.
- Geändert: `build_viewer_data.py` legt für Objekte ohne Seiten je Scan einen Platzhalter „Nicht transkribiert“ an, sodass der Viewer die Faksimiles der Totalausfälle zeigt. Die offenen Aufgaben stehen in [[plan]] Phase 4, die editorischen Entscheidungen in [[transcription-guidelines]] §8 Nr. 6–7.
- Belege: `624c6e0`, `a69b716`, `9c5b836`

### 2026-09-25 Totalausfälle: Salvage und Scans hinter Chunk-Platzhaltern

- Anlass: kostenlose Empfehlungen aus `reports/pipeline-totalausfaelle.md`.
- Befund: Parser-Stufe 6 (`_salvage_pages()`) übernimmt die vollständigen Seitenobjekte vom Anfang eines abgebrochenen `pages`-Arrays. Angewendet auf die gespeicherten Rohantworten rettete sie 18 Objekte teilweise, 300 Seiten, 187 mit Text, genau die Zahl des Reports. Die übrigen 16 Objekte bleiben Totalausfall.
- Korrigiert: „Die Liste war nicht geschlossen.“ Der Eintrag vom 2026-08-26 hielt die Liste der Totalausfälle für geschlossen. Die Platzhalter, die der Chunk-Modus für fehlgeschlagene Chunks einsetzt, klassifizierte `_classify_page()` jedoch als `blank`, sodass 33 weitere Objekte mit 1.373 Scans, fast alle Werke, als Objekte mit vielen Leerseiten statt als unvollständig im Katalog standen. Gültig ist `quality_signals` v1.7 mit dem Feld `transcription_status` (`complete`, `partial`, `failed`), beschrieben in [[transcription-verification]].
- Entschieden: Ein geretteter Teil trägt `result.salvage` und `confidence: low` und löst im Live-Lauf trotzdem den Retry aus. Nur die betroffenen Objekte wurden neu berechnet, weil ein vollständiger Backfill die Signale approbierter Objekte verändert hätte, deren Text nach Korrekturen nicht mehr zu den Signalen passt. Verworfen: ein engeres `max_output_tokens`, weil die Schleifen ohnehin am Ausgabelimit enden und echte Zeitungsseiten nahe daran liegen. Exporte nur auf einem Rechner mit Backup, weil ohne Backup still Felder aus `metadata.json` wegfallen.
- Geändert: [[plan]] Phase 4b (Neulauf, Neuexport, veraltete Signale nach Korrekturen).
- Belege: `b1171f8`, `tests/test_salvage.py`

### 2026-08-26 Review-Session: 34 Totalausfälle erhoben, Viewer nachgezogen

- Anlass: Redigier-Runde der Projekt-Reviewer:in (Universität Salzburg) am lokalen Dev-Server.
- Befund: Objekte ohne `pages`-Array lassen sich nicht redigieren. Ein Scan aller Ergebnis-JSONs fand 34 solche Fälle, verteilt über vier Sammlungen, keines mit Review-Status, „die Liste ist geschlossen“ (korrigiert am 2026-09-25). In 28 der 29 Wiederholungsschleifen wiederholt das LLM Leerraum oder ein Markup-Zeichen der eigenen Transkriptionskonvention, also dort, wo das Annotationsschema legitime Wiederholung vorsieht. Der Ausfall ist damit an Materialeigenschaften gebunden. `parse_api_response()` hatte keine Stufe, die abgeschlossene Seitenobjekte aus einem abgeschnittenen Prefix übernimmt.
- Entschieden: Objekt- und Seitennavigation werden optisch getrennt, weil sie sich bisher nur durch das Pfeilzeichen unterschieden. Die Editionsrichtlinien kommen als Panel „§ Richtlinien“ an den Ort der Arbeit, mit einer Markup-Leiste im Edit-Modus. Die Leiste schreibt nicht selbst durch, damit nicht jeder Klick ins Pipeline-JSON geht.
- Geändert: `reports/pipeline-totalausfaelle.md` mit Liste und Empfehlung. Die Pflege der Editionsrichtlinien steht in [[plan]] Phase 4a.
- Belege: `a693993`, `c49be4e`, `cc45c93`

### 2026-08-21 Proto-Edition-Manuskript als Forschungsartefakt eingeordnet

- Entschieden: Das im Juli 2026 abgeschlossene Manuskript wird nicht eingereicht. `paper/` bleibt als datierter Forschungsstand mit Evidenzbasis erhalten und bildet keine Publikationspipeline mehr ab.
- Geändert: Die dauerhaften Erkenntnisse liegen in [[editorial-methodology]] (editioneller Status pro Objekt, Betriebskontexte, Provenienzmodell, agentische Arbeit), in `reports/cer-baseline-report-2026-04-02.md` (korrekturbasierte CER mit ihren Grenzen) und in [[architecture]] (Trennung von Ergebnisartefakten, deterministischen Exporten und veränderlichen LLM-APIs). Zwei historische Journalverweise, die als tote Wikilinks gerendert wurden, sind repariert.
- Belege: `3e2c89b`

### 2026-07-31 Wissensbasis nachträglich an der Konvention ausgerichtet

- Anlass: das Methodenpaper „Promptotyping. Translating Research Data into Research Artefacts through Context Engineering and Agentic Engineering“, das dieses Repository als Fall führt.
- Entschieden: Die Ausrichtung geschah ausdrücklich post hoc. Die Evidenzzitate des Papers zeigen auf den Stand davor, `eb632d1`, und bleiben dort gültig. Die Runde setzte Metadaten nach und änderte keinen Inhalt und keinen Dateinamen. `created` und `updated` blieben unangetastet, weil die Korrektur `e67dc22` die handgesetzten Entstehungsdaten bewusst gegen die Git-Daten stehen ließ. `generated-with` steht nur, wo die Git-Historie ein einziges Modell über die ganze Dateigeschichte ausweist, weil ein berührender Commit keine Erzeugung belegt. Dokumente ohne passende Vorlage bleiben freihändig mit Begründung im Index, weil eine begründete Lücke eine Entscheidung ist.
- Geändert: Frontmatter und Vorlagenzuordnung aller Wissensdokumente. Der Index erhielt eine Zuordnungstabelle ohne Wikilinks, damit `parse_index_sections()` keine Pseudo-Sektion erzeugt.
- Belege: `eb632d1`, `11a9fc4`, `e67dc22`

### 2026-07-30 Hygiene-Runde: Root konsolidiert, Index modernisiert, Trust-Modell belegt

- Befund: Die Antragsbeschreibung des Vertrauensmodells hält am Code. Die vier Stufen sind gespeicherte Zustände und aus keinem Score abgeleitet, der Maschinenzustand überlebt die Korrektur in `transcription_llm` und `edit_history`, und Prüfstufe, Konfidenz und Signale werden nirgends verrechnet. Drei Abweichungen bleiben dokumentiert. `gt_verified` ist implementiert, aber kein Objekt trägt die Stufe. `import_reviews.py` kann einen fünften Wert `reviewed` schreiben, den weder die Beschreibung noch `isHumanChecked()` kennt. Die Anzeige fasst Stufe 0 und 1 bewusst zusammen (Operator-Entscheidung vom 2026-06-10). Die Annahme „kein Test vorhanden“ stimmte nicht, `pipeline/test_*.py` enthielt bereits Regressionstests.
- Entschieden: Berichte und Manuskript ziehen nach `paper/` statt nach `docs/paper/`, weil `docs/` das GitHub-Pages-Root ist. `knowledge/dia-xai-integration.md` wird nach der Auflösung von EQUALIS am 2026-07-18 als Verhältnisbestimmung neu geschrieben, der historische Stand bleibt als eigener Abschnitt. Neue Tests prüfen Page-JSON gegen das Schema und die Übergänge der Vertrauensstufen, weil Page-JSON der Vertrag mit teiCrafter, PAGE XML und METS ist. Die Arbeit wurde auf parallele Commits in `origin/main` rebased.
- Geändert: README-Abschnitt „Trust tiers and verification provenance“, [[dia-xai-integration]], `tests/`, `.github/ISSUE_TEMPLATE/`. Die offenen Punkte zu `gt_verified` und `reviewed` stehen in [[plan]].
- Belege: `eb632d1`

### 2026-07-27 Katalog-Triage nach einzelnem Qualitätssignal

- Anlass: Operator-Feedback, `needs_review` soll gefiltert mit Grund sichtbar sein.
- Befund: Die Precision der Signale unterscheidet sich stark (Seitenlänge und Bild-Text 100 %, Sprache 50 %), sodass eine gemeinsame Liste eine verlässliche mit einer zur Hälfte falsch-positiven Arbeitsliste mischt.
- Entschieden: Ein Filter je Signal mit klickbaren Gründen in der Status-Spalte. Der Signalfilter setzt bewusst keinen impliziten Ungeprüft-Filter, damit ein Signal auch über geprüftem Bestand nachschlagbar bleibt.
- Belege: `ac0e3db`, `cb22505`

### 2026-06-21 AAL-Lebensdokumente L1–L13 und Branch-Sicherung nach main

- Befund: Die Book-XMLs der Lieferung tragen keine `<idno>`. Cirilo vergibt PIDs alphabetisch, daher L10 vor L2.
- Entschieden: Die PIDs werden über den `mods:title` aufgelöst. Die TEI wird aus der Katalog-TEI `SZDLEB.xml` übernommen statt generiert, damit GND, Provenienz und Maße erhalten bleiben, und die Sprache kommt aus dem Katalog statt aus dem Cirilo-METS. Auf die Frage des Operators, ob der Branch `chore/frontmatter-migration` getrennt bleibt, entschied die Agent-Session in der Editionsphilologie-Persona, ihn abzuschließen und per Fast-Forward nach main zu bringen. Gründe waren, dass das Betriebsmodell der Leitstelle keine getrennten Feature-Branches vorhält, die Arbeit reversibel war und nichts genuin Neues öffentlich wurde. Die Entscheidung ist revidierbar.
- Belege: `f66a4e8`, `4b5d7f1`, `reports/aal-ingest-restliste.md`

### 2026-06-11 AAL B3-Nachzug: Re-Export, Ingest, Onboarding, Request-Timeout

- Befund: Der Re-Export ist doppelt verschachtelt, sodass Folder-Matching tiefenrobust sein muss. B3.108 blieb ohne Viewer-XML. Ein mitgelieferter Katalog `SZ-AAL_B3.xlsx` beantwortet die frühere Sprachfrage für B3. Die Signatur steht im `mods:title` und nicht in `note[@type=signature]`. Der genai-Client hatte kein Request-Timeout, sodass ein einzelner rate-limitierter Bild-Call den ganzen Batch einfror.
- Entschieden: Client-Timeout und retrybare `timeout`/`deadline`-Fehler in `_call_api`. Die Sprache wird weiterhin nicht aus dem METS übernommen, die Anreicherung aus dem Katalog bleibt ein eigener Strang. Die Korrekturmeldung an die Erschließung ging mit der Kontrollliste hinaus.
- Belege: `7bebfcd`, `reports/aal-ingest-restliste.md`

### 2026-06-10 Session 26 (Nachtrag 3): Agent-Triage und Signal v1.6 für Umschlagseiten

- Befund: Drei Agenten triagierten die geflaggten AAL-Objekte Bild gegen Text, Ergebnis in `reports/aal-review-triage.md`. Zwei Objekte scheiterten an einem Repetition-Runaway, der das JSON sprengt (`o_szd.3135`, `o_szd.3375`), vier blieben strittig für die Operator-Sichtung. Sieben Flags gingen allein auf kurze Umschlag- und Adressseiten zurück, die gegen den Median langer Briefseiten gemessen wurden.
- Entschieden: `quality_signals` v1.6 nimmt Umschlagseiten über `_is_envelope()` von der Längenanomalie aus. Die Runaway-Objekte laufen seitenweise neu, weil Einzelseiten-Verarbeitung die Schleife zuverlässig bricht. Die Fehler in `o_szd.3375` korrigierte ein Agent mit `edit_history` und Roh-Output in `transcription_llm`. Operator-Regel ab diesem Tag: Subagenten laufen mit Modell-Override auf Opus oder Sonnet.
- Korrigiert: Die Bezeichnung v1.6 trug im Eintrag zu Session 21 (2026-04-03) schon die Precision-Evaluation. Im Code (`pipeline/quality_signals.py`) bezeichnet v1.6 die Umschlag-Ausnahme.
- Belege: `8c35e4f`, `a96cd7f`, `09074ba`, `tests/test_quality_signals.py`

### 2026-06-10 Session 26: Statusmodell mit drei Stufen und zwei Datenströme je Seite

- Anlass: Operator-Feedbackrunde.
- Befund: `import_reviews.py` hatte bis dahin keine Sicherung des Roh-Outputs.
- Entschieden: Operator-Entscheidung, das Statusmodell der Anzeige auf drei Stufen zu vereinfachen. Mensch-geprüft gilt als verifiziert und Ground-Truth-fähig und ersetzt Geprüft und Verifiziert, Agent-geprüft ersetzt Auto-geprüft, „Review nötig“ ist nur noch Triage-Hinweis innerhalb von Ungeprüft. Die gespeicherten Werte bleiben unverändert. Operator: „Tabelle nicht klickbar machen“, das klickbare Signatur-Präfix entfällt. Operator-Regel: Code-Kommentare englisch und kompakt. Operator-Entscheidung zum Datenstrom-Modell: Jede Seite führt `transcription` als Arbeitsfassung und `transcription_llm` als unveränderlichen Roh-Output, gesetzt beim ersten Edit in `serve.py` und `import_reviews.py`. Damit ist jede menschliche Korrektur eine CER-Messung gegen den Roh-Output.
- Geändert: [[governance]], [[specification]], `report_cer_from_edits.py`.
- Belege: `78fa30f`, `6098153`, `6d8a13d`, `cf8390a`

### 2026-06-10 Session 26: AAL-Batch abgeschlossen, Katalog-Filter als Registry

- Befund: Der AAL-Voll-Batch endete mit zwei Restanten ohne Faksimiles, „Stichproben o_szd.3307/3100 bestaetigen Diskriminanz der Selbsteinschaetzung“. Diese Lesart steht gegen die Befunde der Sessions 6, 22 und 23 und des Reviews vom 2026-10-19, nach denen die Selbsteinschätzung nicht unterscheidet.
- Entschieden: Die Katalog-Filter werden als deklaratives Registry (`FILTER_DEFS`) geführt, ein neuer Filter ist ein Registry-Eintrag (Operator-Auftrag). Bestandseinheiten leitet die Pipeline aus der Signatur ab (`derive_unit()`). Die Einheitsbegriffe sind Arbeitsbegriffe, deren offizielle Bezeichnung über die Korrekturmeldung an die Erschließung geklärt wird. Die Sammlungs-Integration wurde nach Operator-Freigabe gepusht.
- Belege: `f9f111b`, `05917a3`, `842d117`

### 2026-06-10 Autographen (SZ-AAL): GAMS-Verifikation und fünfte Sammlung

- Befund: METS kommt von `archive/get/{pid}/METS_SOURCE`, `{pid}/METS` liefert 404. Die Zuordnung Scan zu `IMG.n` ließ sich über die Bildmaße im METS gegen die lokalen JPEG-Header prüfen, ohne Download. Cirilo setzt pauschal die Sprache „Deutsch“ in die MODS, was im Pilot 9 von 10 falsche `language_mismatch`-Flags erzeugte.
- Entschieden: Die Sprache wird nicht in `metadata.json` und TEI übernommen, das LLM erkennt sie selbst, `mets.xml` bleibt als Beleg. Die Sammlung `autographen` steht in `COLLECTIONS` am Ende, weil die Reihenfolge den Tie-Break bestimmt.
- Geändert: [[data]] Abschnitt zu den Autographen, `reports/aal-ingest-qa.md`.
- Belege: `f9f111b`, `reports/aal-ingest-qa.md`

### 2026-06-09 Session 25b: A/B/C-Transkriptions-Experiment (Vision-Auswertung)

- Anlass: Welcher Hebel verbessert die Transkription schwerer Kurrentschrift am meisten? Getestet wurden gegen die Kontrolle (`gemini-3.1-flash-lite-preview`) V1 mit Unsicherheits-Kalibrierung und Feld `uncertain_words`, V2 mit reichem Metadaten-Kontext und V3 mit dem stärkeren `gemini-3-flash-preview`, auf sechs AAL-Objekten mit 20 Seiten. Als belegt galten nur am Faksimile eindeutig entscheidbare Stellen.
- Befund: V3 liest den Poststempel „BATH / SOMERSET“ richtig, wo Kontrolle und V1 „HAMPSTEAD“ lesen, und korrigiert stille Fehler der Kontrolle („Garage“ statt „Sarge“, „Glaskasten“ statt „Glashütten“). V1s `uncertain_words` zeigen verlässlich auf die Fehlerstellen, ohne sie zu reparieren. V2 halluziniert „Hier in Bath musiciert“, weil der Metadaten-Prior „Entstehungsort: Bath“ in den Text sickert, und unterdrückt Unsicherheitsmarker. Zeichenmenge ist kein Qualitätsmaß.
- Entschieden: Empfehlung für den Produktivlauf `gemini-3-flash` als Basismodell mit `uncertain_words`, reines Typoskript könnte bei Flash Lite bleiben. Verworfen: V2, „netto negativ/gefaehrlich“ wegen belegter Prior-Leckage. Feine Paläografie auf Wortebene bleibt der Fachperson.
- Korrigiert: Die Empfehlung wurde nie umgesetzt und nie verworfen (Eintrag vom 2026-10-28). Sie steht als offene Entscheidung in [[plan]].
- Belege: `849ba88`

### 2026-06-09 Session 25: AAL-Lieferung, GAMS-Ingest-Vorbereitung, lokale Faksimiles

- Befund: Der Batch B3 der Lieferung war quellseitig unvollständig, ein Re-Download ergab eine identische Kopie. Lightroom-Kataloge waren in einzelne Objektordner mitexportiert. Bei schwerer violetter Kurrent produziert das LLM flüssiges Deutsch und markiert kaum Unsicherheit, wie schon in den Sessions 19 und 20.
- Entschieden: Noch nicht ingestierte Objekte erscheinen als Platzhalter mit Ingest-Label, ihre Faksimiles liefert `serve.py` lokal und gegen Traversal geschützt aus. Ein kontrolliertes A/B/C-Experiment soll den besten Hebel bestimmen (Session 25b).
- Korrigiert: Der Eintrag trug Entscheidungen und Statistik der Layout-Arbeit vom 2026-04-03. Sie stehen jetzt beim Eintrag „Session 24: Layout-Pipeline Refactoring“.
- Belege: `8453ac6`, `766b30e`

### 2026-06-08 Dedup: korrespondenzen-Discovery TEI-kanonisch

- Befund: Das Backup listet 34 Lebensdokumente-Objekte physisch doppelt, in `korrespondenzen/` und `lebensdokumente/`. `discover_objects()` scannte blind und transkribierte sie unter beiden Sammlungen, teils mit dem falschen Prompt. Die korrespondenzen-TEI katalogisiert auf Konvolut-Ebene ohne Einzelbrief-PID, das ist kein Parser-Bug. Die Zahl 34 ist von den 34 leeren `pages[]` der Coverage-Diagnose abzugrenzen, gleiche Zahl, anderes Phänomen.
- Entschieden: Die Discovery filtert TEI-kanonisch. Eine PID in einer TEI bestimmt die Sammlung, ein Orphan fällt an die erste Sammlung in `COLLECTIONS` mit Backup-Verzeichnis. Die verwaisten korrespondenzen-Ergebnisse wurden entfernt. Ein adversarischer Multi-Agent-Review fand keine funktionalen Bugs.
- Geändert: [[data]] Abschnitt TEI-Metadaten vs. Backup.
- Belege: `fb48ca0`, `50a9467`, `cb9cdd6`

### 2026-06-08 TEI v2: Marker-Anreicherung erweitert und Coverage-Diagnose

- Befund: `diagnose_coverage.py` fand 34 stille Transkriptions-Fehlschläge mit Bildern und leerem OCR sowie reine Leer-Objekte und schrieb `reports/coverage-gaps.json`. Den Neulauf löst das Skript nicht aus, er ist eine Operator-Entscheidung.
- Entschieden: Marker v2 bleibt line-lokal und fail-safe auf Literal. Stempel werden zu `<note>`, `[...]` mitten in der Zeile zu `<gap>`, mehrzeilige Spans bleiben bewusst literal. Notizen werden nur hinter `--carry-notes` mitgenommen und als maschinell und ungeprüft attribuiert, der Default bleibt byte-identisch.
- Korrigiert: Nachtrag Marker v2.1 nach adversarischer Semantik-Prüfung durch drei Review-Agenten. Blocker war `{x}` → `<add>`, weil das LLM `{}` massenhaft als Wortsegmentierungs-Rauschen setzt und nur ein kleiner Teil echte Einfügungen sind. Ein konservativer Filter senkte `<add>` von 15.872 auf 3.013 und entfernte damit rund 12.900 falsche Editionsaussagen. Dazu entfielen Attribute, die das Protokoll nicht kodiert (`reason="illegible"` an `<unclear>`, `@rend` an `<del>`, `@place` an `<add>`), und Stempel wurden nach Protokoll differenziert. Wohlgeformtes TEI besagt nichts über die Richtigkeit seiner editorischen Aussagen.
- Belege: `0fceaa4`, `pipeline/test_marker_enrich.py`

### 2026-06-08 TEI-Export: Page-JSON → teiCrafter (deterministisch)

- Befund: Die leeren TEI-Dateien gehen auf leeres `pages[]` stromaufwärts und auf reine Faksimile-Objekte zurück, kein Konverterfehler.
- Entschieden: `pipeline/export_tei.py` ist ein Python-Port des teiCrafter-Referenzprototyps mit bit-identischer Ausgabe, ohne LLM. Die Marker-Anreicherung konvertiert in v1 nur das line-lokal Eindeutige, weil ein früherer Entwurf für die ganze Seite und alle Marker bei der adversarischen Prüfung unsicher war. Seiten-Notizen fallen per Default weg, weil sie CER-neutral sind, ihr nützlicher Teil schon in `page.type` steht und der Rest unzuverlässig ist.
- Geändert: [[teicrafter-integration]].
- Belege: `cb5633f`

### 2026-04-15 Session 26: Interface Documents-First und Paper-Claim-Traceability

- Anlass: Der am 2026-04-15 eingereichte Code4Lib-Abstract (Projektleitung mit einer Co-Autor:in vom Literaturarchiv Salzburg und der Projekt-Reviewer:in der Universität Salzburg) behauptet drei Funktionen desselben Codes je nach Deployment, eine konzentrische Vertiefung der Edition durch Review (Vogeler 2025) und Vault plus Journal als Audit-Trail. Alle drei waren im Code realisiert, aber nicht sichtbar.
- Entschieden: Documents-First ist Leitprinzip, jede UI-Entscheidung prüft, ob sie die Dokumente aus dem Sichtfeld drängt. Das Workspace-Panel ist per Default eingeklappt, das Transparency-Panel zieht vom Katalog auf die Projektseite, das Journal erscheint als Link statt als Teaser. Export-Trigger gibt es nur als kopierbare Kommandos. Die GitHub-API ist die einzige externe Laufzeitabhängigkeit. Auf Wunsch der Projektleitung entfiel der Untertitel mit dem Verweis auf Vogeler 2025, weil Theorie ins Paper gehört.
- Korrigiert: Chip und Progress Bar zählten verschieden, weil die Aggregation ein Objekt in mehreren Stufen zählte (`84a111c`).
- Belege: `47a0a01`, `1c89a85`, `0c351d9`, `7d63735`, `84a111c`, `ae8e98e`, `dd72e76`, `80f2b9a`, `e4e9ce5`

### 2026-04-12 Session 25: METS-Export, JSON-Härtung, „An“-Halluzination

- Befund: Werke-Objekte mit vielen Leerseiten lassen Gemini aus dem JSON-Format rutschen.
- Entschieden: JSON-Reparatur, Extraktion des JSON-Objekts aus umgebendem Text und automatische Aufteilung fehlgeschlagener Chunks in kleinere Blöcke. Der Korrespondenz-Prompt verbietet ein ergänztes „An“ vor dem Empfänger. `export_mets.py` erzeugt METS mit MODS aus der TEI.
- Belege: `ef699fd`, `157397c`

### 2026-04-03 Session 24: teiCrafter Pipeline-Modus und Page-JSON-Batch-Export

- Entschieden: Die TEI-Erzeugung geschieht in teiCrafter. Der teiHeader entsteht deterministisch aus den Metadaten, die body-Grundstruktur aus den Regionstypen, Briefe bleiben ein einziges `div`, weil Umschlagadressen und Briefköpfe keine Kapitelgrenzen sind. Page-JSON dient als Fallback, solange `export_mets.py` fehlt. Nicht gemacht: RelaxNG-Validierung gegen das offizielle TEI-Schema, übernommen in [[plan]].
- Korrigiert: Der Eintrag nannte `631931a` für den Page-JSON-Batch-Export. Der Hash ist in der Historie nicht auflösbar, der Export liegt in `45db71d`.
- Belege: `d99a31c`, `45db71d`, teiCrafter `77fd4be`

### 2026-04-03 Session 24: Layout-Pipeline Refactoring und stratifizierter Test

- Entschieden: Merge und Verify der Layout-Analyse laufen in einem VLM-Call, weil der längere Prompt die Qualität nicht verschlechterte. Deterministische Post-Processing-Filter fangen systematische VLM-Schwächen günstig ab, Prompt-Regeln wirken davor. VLM-Nichtdeterminismus ist akzeptiert, Sachfotos statt Dokumenten blieben offen.
- Geändert: [[layout-analysis-architecture]].
- Belege: `ef699fd`

### 2026-04-03 Session 23: Stats-Dashboard als epistemische Infrastruktur, Page-JSON v0.2, METS als Zielformat

- Befund: Die VLM nummeriert nach Manuskriptblättern und überspringt Rückseiten, sodass der Viewer ab Seite 2 das falsche Bild zeigte.
- Entschieden: Das Dashboard verliert Sektionen, die nicht gegroundet sind. Der Donut der VLM-Konfidenz entfällt, weil High, Medium und Low nicht diskriminieren, das DWR-Histogramm wegen rho=0.05 und der Modellkonsensus, weil Agreement keine Korrektheit belegt. Jede Visualisierung nennt das erzeugende Skript. Page-JSON ist internes Arbeitsformat, METS/MODS mit PAGE XML das Archiv- und Austauschformat, weil GAMS mit METS arbeitet und kein eigenes Schema zu pflegen ist. Die Seiten-Bild-Synchronisation (`_fill_missing_pages()`) ist ein Pipeline-Schritt.
- Geändert: [[architecture]] Abschnitt Archivformat, [[page-json-architecture]], [[specification]] Abschnitt Statistik-Dashboard.
- Belege: `5455b23`, `b24a878`, `3ebe908`, `f3d498e`, `09ee835`

### 2026-04-03 Session 22: Badge-System und Header

- Entschieden: „Ungeprüft“ ersetzt „LLM OK“, weil das Label sagt, was der Zustand ist. Die VLM-Konfidenz verschwindet aus der Qualitätsspalte, weil die eigene Evaluation sie als unzuverlässig zeigt. Icons entfallen. Die Badge-Farben wurden nach Berechnung der Kontrastverhältnisse auf WCAG AA nachgeschärft.
- Belege: `eee8460`, `15a4522`

### 2026-04-03 Session 21: Scope-Bereinigung, GT-Review-Workflow, Signal-Precision

- Befund: Kein Objekt hatte `gt_verified`, die CER-Zahlen beruhten auf Agent-Schätzungen. Gegen agent-verifizierte Objekte gemessen hatten `page_image_mismatch` und `page_length_anomaly` volle Precision, `language_mismatch` die Hälfte und `duplicate_pages` keine, weil Korrekturfahnen physisch denselben Text zweimal enthalten und Register wiederholte Köpfe haben.
- Entschieden: Prompt-Ablation, Nondeterminismus-Test, Provider-Vergleich und die TEI-Erzeugung fallen aus dem Projekt. `duplicate_pages` zählt nicht mehr zu `needs_review`. `gt_verified` wird als oberste Stufe implementiert, `/api/edit` sichert den Originaltext für die CER-Berechnung.
- Korrigiert: Der Eintrag nannte die Precision-Evaluation „Quality-Signals v1.6“. Im Code heißt v1.6 die Umschlag-Ausnahme vom 2026-06-10. Der Eintrag trug außerdem Kontext und Statistik von Session 20b.
- Belege: `789bc57`, `52b8090`

### 2026-04-02 Session 20b: Korrespondenzen-Massenbatch

- Befund: `run_batch()` hatte keine Fehlerbehandlung um `transcribe_object()`, ein einzelner Fehler beendete den Batch lautlos. Die scheinbare Diskrepanz zwischen Backup-Objekten und Ergebnissen ging auf mitgezählte Konsensus-, Pro- und Layout-Dateien zurück.
- Entschieden: try/except mit Logging, der Batch läuft über Einzelfehler hinweg.
- Belege: `dcfaa23`

### 2026-04-02 Session 20: Edit-Tracking, Agent-Verifikation, Phase A Truncation-Fix

- Befund: Agent-Korrekturen überschrieben den Originaltext ohne Spur. Vier große Objekte hatten nur wenige ihrer Bilder transkribiert. Fraktur-Fehler sind häufiger als angenommen, mit Nonsens-Halluzinationen und falschen Eigennamen.
- Korrigiert: Phase A fand die Ursache der Truncation. Zuerst dem Chunking zugeschrieben, war sie die Voreinstellung `--max-images 5` in `run_sample_batch.py`. `diagnose_truncation.py` bestimmte die betroffenen Objekte, die Voreinstellung steht auf 0, und `transcribe.py` speichert `metadata.input_image_count_total`.
- Entschieden: `edit_history` auf Seitenebene hält jeden Originaltext vor einer Korrektur fest. Verworfen: DWR als Signal, weil es mit der Qualität nicht korreliert (rho=0.05, F1=0.20). Verworfen: Fraktur-Post-Processing zur Autokorrektur, weil es nur 38 % Precision erreicht. Es taugt allenfalls zum Flagging.
- Belege: `bd532e8`, `dcfaa23`, `fff0b5b`

### 2026-04-02 Session 19: Fehlermuster bei Kurrent

- Befund: Häufigste Fehlerquelle sind Kurrent-Verwechslungen (h/I, n/u, r/v, L/B, St/H, f/s), besonders bei hastiger Schrift. Gemini erfindet echte Wörter statt `[?]` zu setzen, in Session 8 beobachtet und hier quantifiziert, sodass `marker_density` als Signal nahezu wertlos ist. Auf Adressseiten halluziniert das LLM ein „An“. `duplicate_pages` schlägt bei Doppelaufnahmen mit und ohne Farbskala falsch an.
- Geändert: [[transcription-verification]] §9.
- Belege: `a1f7f46`

### 2026-04-02 Session 18: Agent-Verifikation als eigene Stufe, CER-Baseline

- Befund: Fraktur zeigt systematische f/s-Verwechslungen, tabellarisches Material ordnet Werte falschen Zeilen zu.
- Entschieden: `agent_verified` wird eine eigene Review-Stufe zwischen menschlicher Freigabe und Ungeprüft, mit Prüfmodell und Fehlerzahl als Metadaten. Approve und Edit schreiben über die API statt nur in `localStorage`.
- Geändert: `reports/cer-baseline-report-2026-04-02.md`.
- Belege: `791806b`, `0c5cd1c`, `fedf172`, `ed43661`, `8925a2f`

### 2026-04-02 Session 17: Chunking, Objekt-Prompts, Review-Server

- Befund: Viele Objekte hatten weniger Bilder verarbeitet als vorhanden, weil das API-Kontextlimit bei vielen hochaufgelösten Bildern greift. Die VLM wendet Tabellenanweisungen inkonsistent an.
- Entschieden: Objekte über 20 Bilder werden in Chunks transkribiert und gemergt. Ein optionaler Objekt-Prompt überschreibt den Gruppen-Prompt. Strukturrekonstruktion gehört in Layout-Analyse und TEI-Export. Die Pipeline-JSONs sind die einzige Quelle der Wahrheit, `localStorage` ist keine Datenquelle, deshalb schreibt `serve.py` direkt.
- Belege: `f1c6702`, `74c8d2b`, `d063211`

### 2026-04-02 Sessions 15–16: Wissensbasis im Frontend und Review-Write-Back

- Entschieden: Die Wissensdokumente werden zur Build-Zeit zu HTML gerendert und als eine `knowledge.json` ausgeliefert, damit die App ohne Laufzeitabhängigkeit auskommt und Wikilinks beim Build aufgelöst sind. `import_reviews.py` schreibt Frontend-Exporte zurück, der Review-Status wird dreistufig.
- Belege: `3486d89`, `32ae27f`, `e2a0b98`

### 2026-04-02 Session 14: Modellkonsensus-Metriken v2 und GT-Pipeline

- Befund: Die CER-Metrik allein stufte die meisten Paare als divergent ein, vor allem wegen Lesereihenfolge und Seiten-Halluzination. Korrekturfahnen sind unproblematisch, Korrespondenzen bleiben schwer. Das LLM transkribiert durchscheinenden Rückseitentext.
- Entschieden: `word_overlap` als reihenfolgeunabhängige Metrik und eine vierstufige Klassifikation. Gemini Pro wird drittes GT-Modell statt Claude, weil kein Providerwechsel nötig ist. Der Pilot mit fünf Seiten entfällt, weil Konsensus-Validierung und GT-Pipeline seine Fragen beantworten. Die Bleed-Through-Regel steht im System-Prompt, damit der Text gar nicht erst entsteht.
- Korrigiert: Session 7 hatte Claude Sonnet als zweites Modell vorgesehen.
- Belege: `823717c`, `e7f0238`, `0580133`, `f2a1276`

### 2026-04-01 Session 13: Qualitätsinfrastruktur und Modellkonsensus statt manueller GT

- Befund: Die Signale fingen Sammlungseigenschaften wie leere Rückseiten und Cover statt Fehler. Logprobs sind für Flash Lite Preview nicht verfügbar.
- Entschieden: Modellkonsensus mit drei Modellen statt manueller Ground Truth. DWR wird ergänzendes Signal. Pseudo-Perplexity wird verschoben, weil die Abhängigkeit zu schwer ist.
- Korrigiert: Die Rolle des Modellkonsensus als GT-Ersatz gilt seit Session 23 und der Kuratierung vom 2026-10-28 nicht mehr.
- Belege: `19d4177`, `56f249c`

### 2026-04-01 Sessions 11–12: Verification-by-Vision und DIA-XAI-Integration

- Befund: Der direkte Bild-Text-Vergleich durch einen Agenten liefert umsetzbare Fehlerbefunde. Drucktext ist korrekt, Handschrift gut, Korrekturen und Vermerke schwach. Objekte mit vielen Bildern erzeugten leere Ergebnisse.
- Entschieden: Verification-by-Vision wird der stärkste Verifikationsansatz des Projekts. DIA-XAI wurde als Aggregator über EQUALIS konzipiert, ein Stand, den der Eintrag vom 2026-07-30 ablöst.
- Geändert: [[transcription-verification]].
- Belege: `8cc9302`, `10a48d1`, `0a89a9a`

### 2026-04-01 Sessions 8–9: Selbstkritische Review der Wissensdokumente

- Befund: In einem Testbestand von rund 57.000 Zeichen standen zwei Marker, `marker_density` funktioniert als Signal nicht. Die Signale flaggten die meisten Objekte, überwiegend wegen normaler Leerseiten. Strukturelle Prompt-Anweisungen wirken, Vorsichtsanweisungen zum Setzen von Markern werden ignoriert. Die Sessions 8 und 9 hielten denselben Befund zweimal fest.
- Entschieden: Die Schwellen werden nach dem Pilot kalibriert, das Prompt-Experiment gewinnt an Gewicht.
- Belege: `7c80df3`

### 2026-04-01 Session 7: Gruppenabdeckung 9/9

- Befund: Fraktur funktioniert. Das Konvolut `o_szd.277` lieferte das erste Ergebnis unter `high`.
- Entschieden: Gruppe G (Konvolut) wird nachgereicht. Pilot vor vollem GT-Sample, `quality_signals` sofort, Cross-Model mit Agreement zuerst und Claude Sonnet als zweites Modell (korrigiert in Session 14).
- Belege: `1a092c5`, `9b8be4c`, `2d216be`

### 2026-04-01 Session 6: Single-Page-App und Verifikationskonzept

- Befund: 12/12 "high confidence", fast keine Marker. VLMs überschätzen ihre Leistung systematisch, stärkere Metriken sind nötig. Marker-Dichte ist allenfalls ein positives Signal.
- Entschieden: Das Frontend wird eine Single-Page-App mit getrenntem Katalog und nachgeladenen Sammlungsdaten im SZD-Design-System. Das Verifikationskonzept arbeitet mit drei Ebenen (Marker, Selbsteinschätzung, Textstatistik). `Plan.md` wird einzige Wahrheitsquelle für den Projektstand.
- Belege: `c45af9e`, `cd5f042`, `2cea998`

### 2026-03-31 Sessions 4–5: gemeinsame Konfiguration und Batch-CLI

- Befund: Der Kontext lässt sich zuverlässig aus der TEI ableiten. Die Backup-Verzeichnisse sind für die Object Discovery zuverlässiger als die TEI, weil dort PIDs fehlen.
- Entschieden: Eine gemeinsame `config.py` beseitigt Drift zwischen Skripten. `resolve_group()` prüft die Klassifikation vor dem Objekttyp. ASCII-Ausgaben vermeiden Encoding-Fehler unter Windows.
- Belege: `0152bae`, `a6ecdaf`, `4052532`

### 2026-03-30 Sessions 2–3: TEI-Analyse, Prompt-Schichten, Gruppen

- Befund: GAMS-URLs funktionieren als direkte Bildquellen. Die Korrespondenzen-TEI hat Verzeichnischarakter, Metadaten kommen aus dem Backup. Erwin Rieger ist mit 225 Registerblättern die zweithäufigste Hand in der Aufsatzablage. Alle Testobjekte kamen mit `high` zurück (7/7).
- Entschieden: Ein dreischichtiges Prompt-System aus System-Prompt, Gruppen-Prompt und Objekt-Kontext aus der TEI. Die Gruppen A–E entstehen aus der Sammlungsanalyse, F, H und I folgen in Session 3. Gruppe G wird aufgeschoben, weil zu wenige und zu heterogene Objekte vorliegen. Zeitungsausschnitte brauchen einen eigenen Fraktur-Prompt.
- Geändert: [[data]] Abschnitt zu den Gruppen.
- Belege: `913fb40`, `a8bb225`, `0b6ac2c`

### 2026-03-30 Session 1: Projektplanung

- Entschieden: Gemini 3.1 Flash-Lite transkribiert, weil es günstig ist (0,25 USD je 1M Input-Token), schnell, mit 1M-Token-Kontext und multimodal, und einen Kosten-Qualitäts-Vergleich zwischen Providern erlaubt. Konfidenz ist kategorial statt numerisch, weil LLMs Qualität nach der Erfahrung aus coOCR HTR nicht zuverlässig numerisch einschätzen.
- Belege: `e4b9fca`
