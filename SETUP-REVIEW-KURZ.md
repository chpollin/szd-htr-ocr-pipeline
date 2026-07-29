# SZD-HTR Kurzanleitung — Transkriptionen redigieren

Nur die Befehle. Ausführliche Fassung mit Erklärungen und Troubleshooting: [SETUP-REVIEW.md](SETUP-REVIEW.md).

Voraussetzung: [Git](https://git-scm.com/download/win) und [Python 3.11 oder 3.12](https://www.python.org/downloads/) sind installiert — im Python-Installer **„Add python.exe to PATH"** ankreuzen. Danach ein **neues** PowerShell-Fenster öffnen.

Kein API-Key nötig, keine Bilddaten. Die Faksimiles kommen live von GAMS.

---

## Einmalig einrichten

**1. Namen setzen** — hier den echten Vor- und Nachnamen eintragen, er steht später in jedem freigegebenen Objekt:

```powershell
git config --global user.name "Lina Nachname"
git config --global user.email "mail@example.at"
```

**2. Repository holen** — `<benutzername>` durch den eigenen Windows-Benutzernamen ersetzen:

```powershell
cd C:\Users\<benutzername>\Repos
git clone https://github.com/chpollin/szd-htr-ocr-pipeline.git
cd szd-htr-ocr-pipeline
```

**3. Umgebung anlegen und Pakete installieren:**

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install python-dotenv==1.1.1 markdown==3.7 pyyaml==6.0.3
```

Damit ist die Einrichtung fertig — Schritte 1–3 nie wieder nötig.

---

## Jedes Mal: starten

Im Ordner `szd-htr-ocr-pipeline`:

```powershell
git pull
.\.venv\Scripts\python.exe pipeline\serve.py
```

Erwartete Ausgabe, die Zeile **Reviewer** kurz prüfen:

```
SZD-HTR Dev-Server laeuft auf http://127.0.0.1:8000
  Reviewer:   Lina Nachname
```

Dann im Browser öffnen: **http://localhost:8000**

Das PowerShell-Fenster muss offen bleiben, solange redigiert wird. Beenden mit `Strg+C`.

---

## Im Browser: was wo einzugeben ist

**Kontrolle vor dem ersten Klick** — über dem Katalog muss die Zeile **Editorial Workspace** stehen. Fehlt sie, läuft die Seite nicht über den eigenen Server und alle Änderungen gehen verloren.

**Reviewer-Feld**, rechts in der Editorial-Workspace-Zeile: Dort muss der eigene Name stehen (`Reviewer: Lina Nachname`). Steht dort burgunderrot **„Reviewer festlegen →"**, draufklicken und den Namen eintragen. Ein Klick auf das Feld ändert ihn auch später.

**Redigieren:**

1. Objekt im Katalog anklicken
2. **Edit** — Transkription seitenweise am Faksimile korrigieren
3. **Speichern**
4. **Approve** nur, wenn die Seite wirklich am Faksimile gegengelesen wurde. Das gilt als verbindliche Freigabe und wird als Referenztext weiterverwendet. Im Zweifel ohne Approve speichern.

---

## Am Ende: Korrekturen zurückspielen

Server mit `Strg+C` beenden, dann im selben Fenster:

```powershell
.\.venv\Scripts\python.exe pipeline\build_viewer_data.py
git add results/ docs/catalog.json docs/data/
git commit -m "review: o_szd.161 Korrekturen S. 2-4"
git push
```

In der `git commit`-Zeile den Text in den Anführungszeichen anpassen: welches Objekt, welche Seiten.

Ohne `build_viewer_data.py` bleiben die eigenen Korrekturen in der Katalogansicht unsichtbar.

Schlägt `git push` fehl, fehlen die Schreibrechte: Christopher muss den GitHub-Account als Collaborator eintragen, die Einladung muss angenommen werden. Details und Alternative über einen Fork → [SETUP-REVIEW.md](SETUP-REVIEW.md), Schritt 3.

---

## Wenn etwas klemmt

| Meldung | Lösung |
|---|---|
| `python` wird nicht erkannt | Python-Installer → „Modify" → „Add to PATH", neues Fenster öffnen |
| „Ausführung von Skripts ist deaktiviert" | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, mit `J` bestätigen |
| pip meldet „Zugriff verweigert" | Nicht als Admin und nicht mit `--user` wiederholen — den Befehl aus Schritt 3 exakt mit `.\.venv\Scripts\python.exe -m pip` verwenden |
| `ModuleNotFoundError` | Befehle mit `.\.venv\Scripts\python.exe` starten, nicht mit `python` |
| Kein Editorial-Banner | Seite über http://localhost:8000 öffnen, nicht über die öffentliche Adresse |
| `Reviewer: Unbekannt` | Schritt 1 nachholen |
| Port 8000 belegt | `.\.venv\Scripts\python.exe pipeline\serve.py --port 5501`, dann http://localhost:5501 |
| Faksimiles bleiben leer | Internetverbindung prüfen, https://gams.uni-graz.at aufrufen |
