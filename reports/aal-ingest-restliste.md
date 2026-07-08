# SZ-AAL — Ingest-Restliste

Stand: 2026-07-08. Kompakter Wiedereinstieg, was für Stefan Zweig Digital aus dem
SZ-AAL-Konvolut (Stefan Zweig – Lotte Altmann Nachlass, Ingest-Label SZ-AAL-2026-06) noch
zu ingestieren bzw. zu erfassen ist. Trennt vier Ebenen: GAMS-Faksimile-Ingest,
GAMS-Metadaten-Korrektur bestehender PIDs, TEI-Erfassung im Repo `chpollin/SZD`, und
HTR-Transkription in diesem Repo.

Quellen: `PROJECTS/szd/SZ-AAL_Arbeitsstand_offene-Aufgaben.md` (2026-06-22), die `_README.txt`
und `_INGEST_MANIFEST.csv` der Staging-Ordner unter `PROJECTS/szd/`, `reports/aal-ingest-qa.md`
und `reports/aal-review-triage.md` in diesem Repo, sowie die SZD-Commit-Historie.

## 1. Erledigt (GAMS-Faksimile-Ingest abgeschlossen)

Der Objekt-/Faksimile-Ingest nach GAMS ist bis auf einen Fall durch.

- Korrespondenz und Autographen vollständig: o:szd.3020–3501 plus B1.110a = o:szd.3528,
  alle Faksimiles per HEAD geprüft, 0 fehlend (Arbeitsstand §1).
- Lebensdokumente L1–L13: o:szd.3515–3527, zugleich TEI in SZDLEB.144–156.
- B3-Nachexport (zuvor unvollständige B3-Objekte, im Re-Export vom 2026-06-11 komplett
  geworden): ingestiert, im Autographen-Stand SZDAUT enthalten.
- SZDPER-Personennormdaten der neuen Beteiligten ergänzt, vier Dubletten bereinigt,
  GAMS-Objekt o:szd.personen re-ingestiert (SZD-Commits, Arbeitstree inzwischen sauber).

## 2. Offene Ingest-Punkte

### 2.1 GAMS-Faksimile: ein quellseitiger Nachexport

- **B3.108** ist das einzige noch nicht ingestierbare Faksimile-Objekt. Der Export enthält
  nur RAW-JPG/TIFF plus Lightroom-Katalog, kein Viewer-XML (fälschlich unter B3.105
  verschachtelt). Material unter `PROJECTS/szd/B3_unvollstaendig/SZ_AAL_B3.108/` (drei JPGs,
  kein `Result_*.xml`). Erst prüfen, ob sich aus dem RAW selbst ein valides Objekt bauen
  lässt; falls nicht, ist das der einzige echte Re-Export-Wunsch an den Partner
  (Arbeitsstand §E1, `B3_unvollstaendig/_README.txt`).

### 2.2 GAMS-Metadaten-Korrektur bestehender PIDs (kein Neu-Ingest)

Aus dem korrigierten B1-Re-Export, jeweils Metadaten-Update am bestehenden PID über den
lokalen Repo-Klon, nicht Cirilo:

- **o:szd.3034 (B1.110)**: Autor „Zweig, Stefan", Titel „Brief von Stefan Zweig an Binder,
  Hamlyn & Co. [2. April 1941]", Datum 2.4.1941, Struktur auf `_001`–`_005`. Setzt dc:creator
  und stellt damit die Kontext-Sichtbarkeit her (Arbeitsstand §C1). Bisher als
  „BRIEFE GEHÖREN NICHT ZUSAMMEN!" geführt (`aal-ingest-qa.md`).
- **B1.109 und B1.109a**: korrigierte Book-XML-Felder aus dem Re-Export übernehmen
  (Arbeitsstand §C3).
- **o:szd.3445 (B3.48)** und **o:szd.3402 (B3.131)**: kein dc:creator, daher nicht im
  Korrespondenz-Kontext sichtbar. Nach inhaltlicher Klärung von Verfasser/Adressat setzen
  (Arbeitsstand §C2, §D1).

### 2.3 Katalog-Lücken Verfasser/Adressat

- **B3.48, B3.131, B3.140, B3.141**: fehlende schreibende bzw. empfangende Person. Zuerst
  selbst aus dem Faksimile bestimmen (Objekte unter `PROJECTS/szd/ingeste/SZ_AAL_B3.xx/`),
  nur die nicht ermittelbaren dem Partner vorlegen. B3.48 und B3.131 hängen mit 2.2 zusammen
  (Arbeitsstand §D1).

### 2.4 TEI-Erfassung SZDKOR (größter eigenständiger Schritt)

- **SZ-AAL-B-Korrespondenz als TEI in `data/Correspondence/SZDKOR.xml`** (Repo `chpollin/SZD`).
  SZDKOR enthält bislang 0 SZ-AAL-Einträge. Quelle ist der Referenz-Vollexport
  `ingeste_B1_korrespondenz` (202 Objekte, ausdrücklich nicht für Cirilo) plus die
  SZ-AAL-CSV-Kataloge; Skript `csv_to_szdkor.py` noch zu bauen (Arbeitsstand §B1).

### 2.5 HTR-Transkription (dieses Repo, eigener Strang)

Unabhängig vom GAMS-/TEI-Strang, VLM-Schritt kostenpflichtig.

- **Nachzug-Transkription** (Autographen-Nachzug und Lebensdokumente L1–L13) mit
  `transcribe.py` noch nicht gestartet, danach `build_viewer_data` (Arbeitsstand §F1).
- **Neulauf zwei fehlerhafter Objekte** (Repetition-Runaway sprengt JSON): o:szd.3135
  (Stefan Zweig an Hannah Altmann [Okt. 1939]) und o:szd.3375 (Walther Haupolter an SZ,
  15 Scans, 12 Seiten fehlen) mit `--force` bzw. Anti-Repetition (`aal-review-triage.md`).
- **Operator-Sichtung vier strittiger Objekte**: o:szd.3231, o:szd.3277, o:szd.3280,
  o:szd.3306 (flüchtige Zweig-Kursive, Lesung am Faksimile nicht sicher bestimmbar,
  `aal-review-triage.md`).

## 3. Staging-Ordner-Status (`PROJECTS/szd/`, nur lesen)

| Ordner | Rolle | Ingest-Stand |
|---|---|---|
| `ingeste` | vollständige B1/B2/B3/B4-Objekte, Cirilo-ready | ingestiert |
| `ingeste_B1_110a` | einziges neues B1-Objekt B1.110a | ingestiert (o:szd.3528) |
| `ingeste_B1_korrespondenz` | B1-Vollexport, Referenz + TEI-Quelle, NICHT für Cirilo | 201 von 202 sind Dubletten bestehender PIDs; dient 2.4 |
| `ingeste_B3_nachexport` | zuvor unvollständige B3, im Re-Export komplett | ingestiert |
| `ingeste_L_lebensdokumente` | L1–L13, Cirilo-ready | ingestiert (o:szd.3515–3527) |
| `B3_unvollstaendig` | Vor-Re-Export-Reste, durch Nachexport abgelöst | nur noch B3.108 offen (siehe 2.1) |
| `todo/SZ_SAM_AK.204` | Alt-Eintrag ausserhalb SZ-AAL-2026-06 | Status unklar, nicht verifiziert |

## 4. Nicht sicher geklärt

- `todo/SZ_SAM_AK.204`: ein Einzelobjekt aus der SAM-Serie im `todo`-Ordner, ausserhalb des
  SZ-AAL-2026-06-Laufs. Ob offen, obsolet oder anderweitig erledigt, ist aus den vorliegenden
  Quellen nicht bestimmbar.
- SZDPER-Restpunkte: GND-Nachtrag für vier mutmaßlich private Personen (Meiler, Geiringer,
  Kahn, Kaufmann) blieb offen, weil lobid.org aus der Arbeitsumgebung nicht erreichbar war;
  GND ist kein Pflichtfeld (Arbeitsstand §A3). Ob nach dem 2026-06-22 nachgetragen, nicht geprüft.
