"""Test: Einzelobjekt-Transkription mit Gemini Vision."""

import json
import re
import sys

from google import genai

from config import (
    BACKUP_ROOT, COLLECTIONS, DATA_DIR, GOOGLE_API_KEY, MODEL,
    PROMPTS_DIR, RESULTS_DIR,
)
from tei_context import (
    context_from_backup_metadata, format_context, parse_tei_for_object,
    resolve_group,
)


def load_prompt(filename: str) -> str:
    """Load prompt text from a markdown file, extracting content from code blocks."""
    path = PROMPTS_DIR / filename
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```\n(.*?)```", text, re.DOTALL)
    if not blocks:
        print(f"WARNUNG: Kein Codeblock in {filename}, verwende gesamten Text")
        return text.strip()
    if len(blocks) > 1:
        print(f"WARNUNG: {len(blocks)} Codeblöcke in {filename}, verwende ersten")
    return blocks[0].strip()


# --- Prompts (loaded from files) ---
SYSTEM_PROMPT = load_prompt("system.md")

GROUP_PROMPTS = {
    "kurztext": load_prompt("group_d_kurztext.md"),
    "handschrift": load_prompt("group_a_handschrift.md"),
    "typoskript": load_prompt("group_b_typoskript.md"),
    "formular": load_prompt("group_c_formular.md"),
    "tabellarisch": load_prompt("group_e_tabellarisch.md"),
    "korrekturfahne": load_prompt("group_f_korrekturfahne.md"),
    "zeitungsausschnitt": load_prompt("group_h_zeitungsausschnitt.md"),
    "korrespondenz": load_prompt("group_i_korrespondenz.md"),
}

# --- Test Cases ---
# Gruppe und Kontext werden automatisch aus TEI/Backup-Metadaten aufgelöst.
# Optionale Overrides: "group", "context", "max_images"
TEST_CASES = {
    "theaterkarte":            {"object_id": "o_szd.161",  "collection": "lebensdokumente"},
    "certificate":             {"object_id": "o_szd.160",  "collection": "lebensdokumente"},
    "vertrag_grasset":         {"object_id": "o_szd.78",   "collection": "lebensdokumente"},
    "tagebuch_1918":           {"object_id": "o_szd.72",   "collection": "lebensdokumente", "max_images": 5},
    "korrekturfahne_bildner":  {"object_id": "o_szd.287",  "collection": "werke", "max_images": 3},
    "zeitungsausschnitt":      {"object_id": "o_szd.2215", "collection": "aufsatzablage"},
    "korrespondenz_fleischer": {"object_id": "o_szd.1079", "collection": "korrespondenzen", "max_images": 3},
}


def resolve_context(tc: dict) -> tuple[str, str]:
    """Resolve group and context for a test case from TEI or backup metadata.

    Returns (group, context) tuple. Uses manual overrides if present in tc.
    """
    collection = tc["collection"]
    object_id = tc["object_id"]
    pid = object_id.replace("_", ":")

    # Try TEI first
    tei_file = DATA_DIR / COLLECTIONS[collection]["tei"]
    metadata = parse_tei_for_object(tei_file, pid)

    # Fallback to backup metadata
    if metadata is None:
        subdir = COLLECTIONS[collection]["subdir"]
        meta_path = BACKUP_ROOT / subdir / object_id / "metadata.json"
        if meta_path.exists():
            metadata = context_from_backup_metadata(meta_path)
        else:
            metadata = {}

    group = tc.get("group") or resolve_group(metadata, collection)
    context = tc.get("context") or format_context(metadata)
    return group, context


def load_images(object_id: str, collection: str, max_images: int = 0) -> list[tuple[str, bytes]]:
    """Load images for an object from the backup directory."""
    subdir = COLLECTIONS[collection]["subdir"]
    img_dir = BACKUP_ROOT / subdir / object_id / "images"
    if not img_dir.exists():
        print(f"FEHLER: Bildverzeichnis nicht gefunden: {img_dir}")
        sys.exit(1)
    img_paths = sorted(img_dir.glob("IMG_*.jpg"), key=lambda p: int(p.stem.split("_")[1]))
    if not img_paths:
        print(f"FEHLER: Keine Bilder gefunden in {img_dir}")
        sys.exit(1)
    images = []
    for img_path in img_paths:
        images.append((img_path.name, img_path.read_bytes()))
        if max_images and len(images) >= max_images:
            break
    return images


def load_backup_metadata(object_id: str, collection: str) -> dict:
    """Load backup metadata.json for GAMS URLs and other info."""
    subdir = COLLECTIONS[collection]["subdir"]
    meta_path = BACKUP_ROOT / subdir / object_id / "metadata.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {}


def run_test(test_name: str):
    if test_name not in TEST_CASES:
        print(f"FEHLER: Unbekannter Test '{test_name}'")
        print(f"Verfügbar: {', '.join(TEST_CASES.keys())}")
        sys.exit(1)

    if not GOOGLE_API_KEY:
        print("FEHLER: GOOGLE_API_KEY nicht gesetzt.")
        print("  export GOOGLE_API_KEY=AIza...")
        sys.exit(1)

    tc = TEST_CASES[test_name]
    collection = tc["collection"]
    max_img = tc.get("max_images", 0)
    images = load_images(tc["object_id"], collection, max_img)
    print(f"Objekt: {tc['object_id']} ({collection}) — {len(images)} Bilder geladen")

    # Resolve group and context from TEI/backup metadata
    group, context = resolve_context(tc)
    print(f"Gruppe: {group} — Kontext: {len(context)} Zeichen")

    # Build prompt
    group_prompt = GROUP_PROMPTS[group]
    user_prompt = f"{group_prompt}\n\n{context}\n\nTranskribiere die folgenden {len(images)} Faksimile-Scans."

    # Build content parts for Gemini
    parts = []
    for name, img_bytes in images:
        parts.append(genai.types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"))
        parts.append(f"[{name}]")
    parts.append(user_prompt)

    # Call Gemini
    client = genai.Client(api_key=GOOGLE_API_KEY)
    print(f"Sende an {MODEL}...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=parts,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.1,
            ),
        )
    except Exception as e:
        print(f"FEHLER bei API-Aufruf: {e}")
        sys.exit(1)

    result_text = response.text

    # Parse result
    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        print("WARNUNG: API hat kein valides JSON zurückgegeben, speichere Rohtext")
        result_json = {"raw": result_text}

    # Load backup metadata for GAMS URLs
    backup_meta = load_backup_metadata(tc["object_id"], collection)
    gams_images = [img["url"].replace("http://", "https://") for img in backup_meta.get("images", [])]

    # Build enriched output
    enriched = {
        "object_id": tc["object_id"],
        "collection": collection,
        "group": group,
        "model": MODEL,
        "metadata": {
            "title": backup_meta.get("title", ""),
            "language": backup_meta.get("language", ""),
            "images": gams_images,
        },
        "context": context,
        "result": result_json,
    }

    print("\n" + "=" * 60)
    print("ERGEBNIS")
    print("=" * 60)
    print(result_text)

    # Save enriched result
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS_DIR / f"{test_name}_{MODEL}.json"
    out_path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nGespeichert: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        for name, tc in TEST_CASES.items():
            group, _ = resolve_context(tc)
            print(f"  {name:30s} {tc['collection']:20s} {group}")
        sys.exit(0)
    test = sys.argv[1] if len(sys.argv) > 1 else "theaterkarte"
    run_test(test)
