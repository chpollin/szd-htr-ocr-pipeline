"""Gemeinsame Konfiguration für die SZD-HTR-Pipeline."""

import os
from pathlib import Path

from dotenv import load_dotenv

# .env automatisch laden
load_dotenv()

# --- Pfade ---
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_BASE = PROJECT_ROOT / "results"
RESULTS_DIR = RESULTS_BASE / "test"  # Legacy Test-Ergebnisse
PROMPTS_DIR = SCRIPT_DIR / "prompts"
BACKUP_ROOT = Path(os.environ.get(
    "SZD_BACKUP_ROOT",
    "C:/Users/Chrisi/Documents/PROJECTS/szd-backup/data"
))

# --- API ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
MODEL = os.environ.get("HTR_MODEL", "gemini-3.1-flash-lite-preview")
LAYOUT_MODEL = os.environ.get("HTR_LAYOUT_MODEL", "gemini-3-flash-preview")

# --- Sammlungen ---
COLLECTIONS = {
    "lebensdokumente": {"subdir": "lebensdokumente", "tei": "szd_lebensdokumente_tei.xml"},
    "werke":           {"subdir": "facsimiles",       "tei": "szd_werke_tei.xml"},
    "aufsatzablage":   {"subdir": "aufsatz",          "tei": "szd_aufsatzablage_tei.xml"},
    "korrespondenzen": {"subdir": "korrespondenzen",  "tei": "szd_korrespondenzen_tei.xml"},
    # Autographensammlung SZ-AAL (Cirilo-Ingest SZ-AAL-2026-06), Backup +
    # TEI generiert von import_autographen.py. Anhaengen am Ende: die
    # Reihenfolge ist Tie-Break in _canonical_collection (transcribe.py).
    "autographen":     {"subdir": "autographen",      "tei": "szd_autographen_tei.xml"},
}

# --- Bestandseinheiten (archivische Einheit aus der Signatur) ---
# Anzeige-Begriff je Sammlung fuer die aus der Signatur abgeleitete Einheit
# (Signatur minus letztes Punkt-Segment, siehe derive_unit in build_viewer_data.py).
# Die offizielle Terminologie der Erschliessung ist offen (Korrekturmeldung
# SZ-AAL 2026-06); bis dahin gelten diese Arbeitsbegriffe.
UNIT_TERMS = {
    "lebensdokumente": "Mappe",
    "werke":           "Werkmappe",
    "aufsatzablage":   "Werkmappe",
    "korrespondenzen": "Konvolut",
    "autographen":     "Konvolut",
}

# Klartext-Beschreibung je Ingest-Label (Tooltip im Viewer).
INGEST_INFO = {
    "SZ-AAL-2026-06": (
        "Lieferung Juni 2026: Briefkonvolute SZ-AAL/B1–B10 an/von Stefan "
        "und Lotte Zweig (379 Objekte, GAMS-Ingest 10.06.2026)"
    ),
}

# --- Batch ---
BATCH_DELAY = float(os.environ.get("HTR_BATCH_DELAY", "2.0"))
CHUNK_SIZE = int(os.environ.get("HTR_CHUNK_SIZE", "20"))

# --- Layout-Analyse Schwellenwerte ---
LAYOUT_MIN_REGION_WIDTH_PCT = 0.5   # Regionen schmaler als 0.5% = Rauschen
LAYOUT_MIN_REGION_HEIGHT_PCT = 0.3  # Regionen flacher als 0.3% = Rauschen
LAYOUT_MAX_REGION_PCT = 95.0        # Regionen groesser als 95% = VLM-Halluzination


def results_dir_for(collection: str) -> Path:
    """Return results directory for a collection, creating it if needed."""
    d = RESULTS_BASE / collection
    d.mkdir(parents=True, exist_ok=True)
    return d


# --- Prompt-Gruppen ---
GROUP_LABELS = {
    "kurztext":          ("D", "Kurztext"),
    "handschrift":       ("A", "Handschrift"),
    "typoskript":        ("B", "Typoskript"),
    "formular":          ("C", "Formular"),
    "tabellarisch":      ("E", "Tabellarisch"),
    "korrekturfahne":    ("F", "Korrekturfahne"),
    "konvolut":          ("G", "Konvolut"),
    "zeitungsausschnitt": ("H", "Zeitungsausschnitt"),
    "korrespondenz":     ("I", "Korrespondenz"),
}
