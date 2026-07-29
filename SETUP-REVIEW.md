# SZD-HTR: Redaktionsarbeitsplatz einrichten (Windows)

Ziel: Transkriptionen am Faksimile korrigieren und freigeben.

Kein Google-API-Key nötig, keine Bilddaten auf dem Rechner — die Faksimiles kommen live von [GAMS](https://gams.uni-graz.at/), die Texte aus dem Git-Repository. Wer *neue* Objekte durch das Sprachmodell schicken will, braucht zusätzlich einen API-Key und das ~25 GB große Bild-Backup; das ist hier bewusst nicht Teil der Anleitung.

Dauer: ca. 30 Minuten, überwiegend Downloads.

---

## 1. Git installieren

Download: https://git-scm.com/download/win → Installer mit den Standardeinstellungen durchklicken.

Danach ein **neues** PowerShell-Fenster öffnen (alte Fenster kennen den geänderten PATH nicht):

```powershell
git --version
```

Dann einmalig Name und Mail setzen:

```powershell
git config --global user.name "Vorname Nachname"
git config --global user.email "mail@example.at"
```

Das ist wichtiger, als es aussieht: Dieser Name landet nicht nur in jedem Commit, sondern wird von der Pipeline auch als **Reviewer-Name** verwendet — er steht später in jedem freigegebenen Objekt. Also den echten Namen eintragen, keinen Spitznamen.

## 2. Python installieren

Download: https://www.python.org/downloads/ → Version **3.11 oder 3.12**.

⚠️ Im Installer **„Add python.exe to PATH"** ankreuzen, bevor „Install Now" geklickt wird. Ohne diesen Haken findet PowerShell `python` später nicht — der häufigste Windows-Stolperstein.

```powershell
python --version
```

Öffnet sich stattdessen der Microsoft Store, fehlt der PATH-Eintrag: Installer erneut starten → „Modify" → Haken setzen.

## 3. GitHub-Zugang klären

Zum Lesen und lokalen Arbeiten genügt der offene Klon. Zum **Zurückspielen** der Korrekturen braucht es einen GitHub-Account mit Schreibrechten:

- Christopher trägt den Account unter Settings → Collaborators mit der Rolle **Write** ein. Das kann **nur er** — Collaborators hinzufügen setzt Admin-Rechte am Repository voraus, die im Team sonst niemand hat.
- Die Einladung muss **angenommen** werden (Mail oder https://github.com/chpollin/szd-htr-ocr-pipeline/invitations), sonst schlägt der erste `git push` fehl. Sie verfällt nach 7 Tagen.

Das vorab erledigen — sonst blockiert es erst ganz am Schluss.

### Fallback ohne Schreibrechte: Fork + Pull Request

Falls die Einladung noch nicht da ist, blockiert das die Einrichtung **nicht**. Redigieren funktioniert vollständig lokal; nur das Zurückspielen läuft anders:

1. Auf https://github.com/chpollin/szd-htr-ocr-pipeline oben rechts **Fork** klicken — das erzeugt eine eigene Kopie unter dem eigenen Account.
2. In Schritt 4 statt des Originals den Fork klonen:
   `git clone https://github.com/<eigener-account>/szd-htr-ocr-pipeline.git`
3. Das Original als zweite Quelle eintragen, um Aktualisierungen zu holen:
   `git remote add upstream https://github.com/chpollin/szd-htr-ocr-pipeline.git`
4. Neuen Stand holen mit `git pull upstream main` statt `git pull`.
5. Nach dem Push in den eigenen Fork bietet GitHub „Compare & pull request" an — damit gehen die Korrekturen als Pull Request an Christopher, der sie prüft und übernimmt.

Der Umweg hat einen Vorteil: Korrekturen werden vor der Übernahme gesichtet. Für längerfristige Mitarbeit sind direkte Schreibrechte trotzdem bequemer.

## 4. Repository klonen

Zielordner ohne Sonderzeichen und **nicht** in einem OneDrive-synchronisierten Verzeichnis (die Synchronisation kommt mit tausenden kleinen JSON-Dateien schlecht zurecht):

```powershell
cd C:\Users\<benutzername>\Repos
git clone https://github.com/chpollin/szd-htr-ocr-pipeline.git
cd szd-htr-ocr-pipeline
```

Rund 45 MB. Die Faksimile-Bilder sind bewusst nicht enthalten.

## 5. Virtuelle Umgebung anlegen

Eine venv ist ein isolierter Python-Ordner nur für dieses Projekt, damit sich die Pakete nicht mit anderer Software auf dem Rechner ins Gehege kommen:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

⚠️ Sehr wahrscheinliche Fehlermeldung an dieser Stelle: *„die Datei kann nicht geladen werden, da die Ausführung von Skripts auf diesem System deaktiviert ist"*. Windows blockiert PowerShell-Skripte standardmäßig. Einmalig freischalten — nur für den eigenen Benutzer, keine Admin-Rechte nötig:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Mit `J` bestätigen, dann die Aktivierung wiederholen. Erfolgreich, sobald `(.venv)` am Zeilenanfang steht.

**Merken:** Die Aktivierung gilt pro Terminal-Fenster. In jedem neuen Fenster wieder `.\.venv\Scripts\Activate.ps1` — das ist die Fehlerquelle Nr. 1 am zweiten Tag.

## 6. Pakete installieren

Nicht `pip install -r requirements.txt` verwenden. Dort stehen `docling` und `surya-ocr`, die PyTorch nachziehen (mehrere GB) und ausschließlich für die Layout-Analyse gebraucht werden.

Für den Redaktionsarbeitsplatz genügen drei Pakete:

```powershell
.\.venv\Scripts\python.exe -m pip install python-dotenv==1.1.1 markdown==3.7 pyyaml==6.0.3
```

Der Umweg über `.\.venv\Scripts\python.exe -m pip` statt des kurzen `pip` ist Absicht: So ist unabhängig von der Aktivierung garantiert, dass die Pakete in der venv landen und nicht in irgendeiner anderen Python-Installation auf dem Rechner.

⚠️ Erscheint hier **„Zugriff verweigert" / „Access is denied" / „WinError 5"**, wurde in ein fremdes Python geschrieben — fast immer, weil `pip` ohne aktivierte venv aufgerufen wurde und dann den Microsoft-Store-Platzhalter unter `AppData\Local\Microsoft\WindowsApps\` trifft, dessen Ordner Windows gesperrt hält. Kontrolle:

```powershell
.\.venv\Scripts\python.exe -m pip -V
```

Der ausgegebene Pfad muss mit dem eigenen Repo-Ordner beginnen und `\.venv\` enthalten. Steht dort `WindowsApps`, `Program Files` oder ein Anaconda-Pfad, wirkt Schritt 5 nicht — venv neu anlegen bzw. aktivieren und Schritt 6 wiederholen. Auf keinen Fall mit `--user` oder einer Administrator-PowerShell nachhelfen: Das installiert am Projekt vorbei und verlagert das Problem nur auf Schritt 7.

## 7. Server starten

Aus dem Wurzelverzeichnis des Repos:

```powershell
python pipeline\serve.py
```

Erwartete Ausgabe:

```
SZD-HTR Dev-Server laeuft auf http://127.0.0.1:8000
  Frontend:   http://127.0.0.1:8000/index.html
  Docs-Dir:   ...\docs
  Reviewer:   Vorname Nachname
```

Die Zeile **Reviewer** kurz prüfen — unter diesem Namen werden die Freigaben gespeichert. Steht dort „Unbekannt", wurde Schritt 1 (`git config user.name`) übersprungen.

Im Browser öffnen: **http://localhost:8000**

Ist Port 8000 belegt (Teams, andere Dev-Server): `python pipeline\serve.py --port 5501`

Der Server lauscht nur auf `127.0.0.1` und ist aus dem Netzwerk nicht erreichbar.

## 8. Prüfen, ob der Editiermodus aktiv ist

Es ist dieselbe Website wie die öffentliche unter chpollin.github.io — allein durch den lokal laufenden Server schaltet sie vom Lese- in den Redaktionsmodus. Kein zweites Tool, keine zweite Oberfläche.

Erkennungszeichen: über dem Katalog die Zeile **Editorial Workspace**.

Fehlt sie, läuft die Seite über einen anderen Weg (öffentliche URL, VS Code Live Server o. ä.). Dann landen Änderungen nur im Browserspeicher und sind praktisch verloren. In dem Fall: Tab schließen, `serve.py` starten, http://localhost:8000 aufrufen.

## 9. Reviewer-Namen kontrollieren

Rechts in der Editorial-Workspace-Zeile steht ein Feld mit dem eigenen Namen, z. B. `Reviewer: Anna Muster`. Er wird beim ersten Start automatisch aus `git config user.name` übernommen.

Steht dort stattdessen burgunderrot **„Reviewer festlegen →"**, wurde kein Name gefunden: draufklicken und eintragen. Ein Klick auf das Feld ändert den Namen auch jederzeit später.

Warum das zählt: Der Name steht in jedem freigegebenen Objekt (`review.reviewed_by`) und ist die Grundlage des Vertrauensmodells — „geprüft" ist nur dann eine belastbare Aussage, wenn nachvollziehbar ist, *wer* geprüft hat. Nachträglich lässt sich eine falsche Zuschreibung nicht automatisch korrigieren.

**Geteilter Rechner mit gemeinsamem Windows-Login?** Dann in eine Datei `.env` im Repo-Wurzelverzeichnis schreiben:

```
SZD_REVIEWER=Anna Muster
```

Das übersteuert den git-Namen. Die `.env` wird nicht mitcommittet.

## 10. Arbeitsablauf

**Vor jeder Sitzung:**

```powershell
git pull
```

**Redigieren:**

1. Objekt im Katalog öffnen
2. **Edit** → Transkription seitenweise am Faksimile korrigieren
3. Speichern schreibt direkt in `results/{sammlung}/{objekt}_gemini….json`
4. **Approve** → verbindliche Freigabe

Zu Punkt 4: Approve bedeutet in diesem Projekt *am Faksimile gegengelesen*, nicht *überflogen*. Diese Texte gelten anschließend als Ground-Truth-fähig und dienen als Referenz für die Fehlermessung. Im Zweifel lieber ohne Approve speichern.

**Am Ende zurückspielen:**

```powershell
python pipeline\build_viewer_data.py
git add results/ docs/catalog.json docs/data/
git commit -m "review: o_szd.161 Korrekturen S. 2-4"
git push
```

`build_viewer_data.py` erzeugt die Dateien neu, aus denen der Katalog liest — ohne diesen Schritt bleiben die eigenen Korrekturen in der Katalogansicht unsichtbar. Nach dem Push deployt GitHub Pages automatisch, die Korrekturen sind dann öffentlich sichtbar.

**Absprache:** Wenn mehrere Personen gleichzeitig arbeiten, vorher aufteilen, wer welche Sammlung übernimmt. Merge-Konflikte in JSON-Dateien sind mühsam aufzulösen.

---

## Troubleshooting

| Symptom | Ursache | Lösung |
|---|---|---|
| `python` wird nicht erkannt | PATH-Haken im Installer vergessen | Installer → Modify → „Add to PATH", neues Fenster öffnen |
| „Ausführung von Skripts ist deaktiviert" | PowerShell Execution Policy | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| `ModuleNotFoundError: markdown` / `yaml` | venv nicht aktiviert | `.\.venv\Scripts\Activate.ps1` — auf `(.venv)` achten |
| pip meldet „Zugriff verweigert" / `WinError 5` | Installation ging an der venv vorbei in ein gesperrtes Python | `.\.venv\Scripts\python.exe -m pip -V` prüfen — Pfad muss `\.venv\` enthalten; nicht mit `--user` oder als Admin umgehen |
| Keine Editorial-Workspace-Zeile, keine Edit-Buttons | Seite nicht über `serve.py` geöffnet | `python pipeline\serve.py`, dann http://localhost:8000 |
| Server meldet `Reviewer: Unbekannt` | `git config user.name` nicht gesetzt | Schritt 1 nachholen oder `SZD_REVIEWER` in `.env` |
| Port belegt | anderer Dienst auf 8000 | `python pipeline\serve.py --port 5501` |
| Faksimiles bleiben leer | GAMS nicht erreichbar | Internetverbindung prüfen, https://gams.uni-graz.at aufrufen |
| Korrekturen im Katalog unsichtbar | Viewer-Daten nicht neu gebaut | `python pipeline\build_viewer_data.py` |
| `git push` abgelehnt | keine Schreibrechte / Einladung nicht angenommen | Collaborator-Einladung annehmen |
