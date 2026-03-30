"""Test: Einzelobjekt-Transkription mit Gemini Vision."""

import base64
import json
import os
import sys
from pathlib import Path

from google import genai

# --- Config ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL = "gemini-3.1-flash-lite-preview"
BACKUP_ROOT = Path("C:/Users/Chrisi/Documents/PROJECTS/szd-backup/data/lebensdokumente")

# --- Prompts (3 Schichten) ---

SYSTEM_PROMPT = """Du bist ein Transkriptionsspezialist für historische Dokumente aus dem Nachlass von Stefan Zweig (Literaturarchiv Salzburg). Deine Aufgabe ist die diplomatische Transkription der abgebildeten Faksimiles.

## Regeln

1. Transkribiere den sichtbaren Text so originalgetreu wie möglich (diplomatisch).
2. Behalte Zeilenumbrüche bei, wo sie eindeutig erkennbar sind.
3. Markiere unsichere Lesungen mit [?] direkt nach dem Wort: "Beispiel[?]"
4. Unleserliche Stellen: [...] mit optionaler Angabe der geschätzten Zeichenzahl: [...3...]
5. Durchgestrichenes: ~~durchgestrichen~~
6. Ergänzungen/Einfügungen über der Zeile: {eingefügt}
7. Keine Interpretation, keine Korrektur von Orthographie oder Grammatik.
8. Gedruckten Text und handschriftlichen Text gleichermaßen transkribieren.

## Output-Format

Antworte ausschließlich als JSON:

{
  "pages": [
    {
      "page": 1,
      "transcription": "...",
      "notes": "Kurze Beobachtungen zu Lesbarkeit, Besonderheiten"
    }
  ],
  "confidence": "high | medium | low",
  "confidence_notes": "Begründung der Gesamteinschätzung"
}"""

GROUP_PROMPTS = {
    "kurztext": """## Dokumenttyp

Kurzes Dokument mit wenig Text (Karte, Eintrittskarte, Notizzettel).

## Schriftspezifika

- Oft gedruckter Text, teils mit handschriftlichen Ergänzungen.
- Wenig Text — jedes Wort zählt, Genauigkeit besonders wichtig.
- Rückseiten können Beschriftungen enthalten.

## Hinweise

- Bei sehr kurzem Text: alle Details erfassen, auch Kleingedrucktes und Randnotizen.
- Mehrere Textebenen (Vorderseite/Rückseite) als separate Bereiche kennzeichnen.""",

    "handschrift": """## Dokumenttyp

Handschriftliches Dokument aus dem Nachlass Stefan Zweigs.

## Schriftspezifika

- Stefan Zweig schrieb in einer Mischung aus lateinischer Schrift und Kurrentelementen.
- Sein bevorzugtes Instrument war violette Tinte; Bleistift für Ergänzungen.
- Abkürzungen sind häufig, besonders bei Personennamen und Ortsangaben.
- Zweig schrieb oft schnell — Buchstabenverbindungen können unkonventionell sein.

## Hinweise

- Bei Kurrentbuchstaben: beachte besonders die Verwechslungsgefahr bei e/n, s/f, u/n, d/l.
- Eigennamen nach Möglichkeit vollständig auflösen, aber als unsicher markieren wenn nötig.
- Tagebucheinträge beginnen oft mit einem Datum.""",

    "typoskript": """## Dokumenttyp

Maschinenschriftliches Dokument (Typoskript oder Durchschlag).

## Schriftspezifika

- Maschinenschrift auf Schreibmaschine, teils mit handschriftlichen Ergänzungen.
- Bei Durchschlägen: Text kann blass oder ungleichmäßig sein.
- Handschriftliche Teile sind meist Unterschriften, Datumsangaben oder Randnotizen.

## Hinweise

- Trenne gedruckten/getippten Text nicht von handschriftlichen Ergänzungen — transkribiere alles fortlaufend.
- Vertragsstruktur (Paragraphen, Nummerierung) beibehalten.
- Bei Durchschlägen mit geringem Kontrast: lieber [?] setzen als raten.""",

    "formular": """## Dokumenttyp

Amtliches Formular oder Urkunde mit vorgedruckten und handschriftlich/maschinell ausgefüllten Teilen.

## Schriftspezifika

- Vorgedruckter Text (Formularfelder, Überschriften) und handschriftlich/maschinell ausgefüllte Felder.
- Oft Mischung aus Druck, Maschinenschrift und Handschrift auf einem Dokument.
- Stempel, Siegel oder offizielle Vermerke können vorkommen.

## Hinweise

- Transkribiere sowohl den vorgedruckten Formulartext als auch die Ausfüllungen.
- Kennzeichne Stempel und Siegel in den Notizen, nicht im Transkriptionstext.
- Tabellarische Strukturen so gut wie möglich linear wiedergeben (Feld: Wert).""",

    "tabellarisch": """## Dokumenttyp

Tabellarisches oder listenartiges Dokument (Register, Verzeichnis, Kalender).

## Schriftspezifika

- Strukturierter Aufbau: Spalten, Zeilen, Rubriken.
- Handschriftliche Einträge in vorgedruckten oder handgezeichneten Rastern.
- Oft viele kurze Einträge pro Seite statt Fließtext.
- Mehrere Hände möglich.

## Hinweise

- Tabellenstruktur so gut wie möglich beibehalten. Spalten mit | trennen.
- Leere Felder als (leer) kennzeichnen.
- Bei Registern: Eintragsstruktur erkennen und konsistent wiedergeben.""",
}

# --- Test Cases ---
TEST_CASES = {
    "theaterkarte": {
        "object_id": "o_szd.161",
        "group": "kurztext",
        "context": """## Dieses Dokument

- Titel: Theaterkarte zur Uraufführung von „Jeremias" 1918
- Signatur: SZ-SDP/L2
- Datum: 27. Febr. 1918
- Sprache: Deutsch
- Objekttyp: Eintrittskarte
- Umfang: 1 Blatt (3 Scans: Vorderseite, Rückseite, Gesamtansicht)
- Schreibinstrument: Bleistift
- Hand: Friderike Zweig
- Anmerkungen: „Jerem. Uraufführung" von Friderike Zweigs Hand auf der Rückseite""",
    },
    "certificate": {
        "object_id": "o_szd.160",
        "group": "formular",
        "context": """## Dieses Dokument

- Titel: Certified Copy of an Entry of Marriage
- Signatur: SZ-SDP/L1
- Datum: Sixth September 1939
- Sprache: Englisch
- Objekttyp: Typoskript (beglaubigte Kopie einer Heiratsurkunde)
- Umfang: 1 Blatt
- Schreibinstrument: Schwarze Tinte
- Hand: Fremde Hand
- Anmerkungen: Beglaubigte Kopie vom 3. September 1980""",
    },
    "vertrag_grasset": {
        "object_id": "o_szd.78",
        "group": "typoskript",
        "context": """## Dieses Dokument

- Titel: Verlagsvertrag Grasset
- Signatur: SZ-AAP/L13.1
- Datum: le Premier Février, mil neuf cent trente deux (1. Februar 1932)
- Sprache: Französisch
- Objekttyp: Typoskript (Verlagsvertrag in Formularform)
- Umfang: 1 Blatt
- Schreibinstrument: Violettes Farbband, violette und schwarze Tinte
- Hand: Stefan Zweig, fremde Hand
- Anmerkungen: Maschinschriftliche Eintragungen in Formular, recto mit aufgeklebter Stempelmarke und mehrfach gestempelt, verso mit eigenhändiger Aufschrift „lu et approuvé" und Unterschrift von Stefan Zweig und unbekannt""",
    },
    "tagebuch_1918": {
        "object_id": "o_szd.72",
        "group": "handschrift",
        "max_images": 5,
        "context": """## Dieses Dokument

- Titel: Tagebuch 1918
- Signatur: SZ-AAP/L6
- Datum: [1918]
- Sprache: Deutsch
- Objekttyp: Notizbuch
- Umfang: 19 Blatt beschrieben (39 Scans)
- Schreibinstrument: Violette Tinte
- Hand: Stefan Zweig
- Anmerkungen: Tagebuch aus dem letzten Kriegsjahr. Hier werden nur die ersten Seiten transkribiert (Testlauf).""",
    },
}


def load_images(object_id: str, max_images: int = 0) -> list[tuple[str, bytes]]:
    """Load all images for an object from the backup."""
    img_dir = BACKUP_ROOT / object_id / "images"
    images = []
    # Sort numerically: IMG_1, IMG_2, ..., IMG_10, IMG_11
    img_paths = sorted(img_dir.glob("IMG_*.jpg"), key=lambda p: int(p.stem.split("_")[1]))
    for img_path in img_paths:
        images.append((img_path.name, img_path.read_bytes()))
        if max_images and len(images) >= max_images:
            break
    return images


def run_test(test_name: str):
    tc = TEST_CASES[test_name]
    max_img = tc.get("max_images", 0)
    images = load_images(tc["object_id"], max_img)
    print(f"Objekt: {tc['object_id']} — {len(images)} Bilder geladen")

    # Build prompt
    group_prompt = GROUP_PROMPTS[tc["group"]]
    context = tc["context"]
    user_prompt = f"{group_prompt}\n\n{context}\n\nTranskribiere die folgenden {len(images)} Faksimile-Scans."

    # Build content parts for Gemini
    parts = []
    for name, img_bytes in images:
        parts.append(genai.types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
        parts.append(f"[{name}]")
    parts.append(user_prompt)

    # Call Gemini
    if not GOOGLE_API_KEY:
        print("FEHLER: GOOGLE_API_KEY nicht gesetzt. Export: export GOOGLE_API_KEY=...")
        sys.exit(1)
    client = genai.Client(api_key=GOOGLE_API_KEY)
    print(f"Sende an {MODEL}...")
    response = client.models.generate_content(
        model=MODEL,
        contents=parts,
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.1,
        ),
    )

    # Output
    result_text = response.text
    print("\n" + "=" * 60)
    print("ERGEBNIS")
    print("=" * 60)
    print(result_text)

    # Save result
    results_dir = Path("C:/Users/Chrisi/Documents/GitHub/szd-htr/results/test")
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / f"{test_name}_{MODEL}.json"
    out_path.write_text(result_text, encoding="utf-8")
    print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    test = sys.argv[1] if len(sys.argv) > 1 else "theaterkarte"
    run_test(test)
