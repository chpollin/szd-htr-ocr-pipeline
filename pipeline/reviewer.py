"""Reviewer-Identitaet fuer schreibende Zugriffe auf results/.

Jeder Review-Eintrag traegt einen Namen (`review.reviewed_by`, `edited_by` in
`edit_history`). Dieser Name darf nirgends fest verdrahtet sein: der Checkout
liegt auf mehreren Rechnern, und eine falsche Zuschreibung entwertet genau die
Aussage, auf der das Trust-Tier-Modell beruht — `approved` und `gt_verified`
bedeuten "diese Person hat am Faksimile gegengelesen".

Aufloesung in dieser Reihenfolge:
  1. `SZD_REVIEWER` (Umgebungsvariable oder .env) — explizite Setzung
  2. `git config user.name` des Checkouts — stimmt per Definition mit dem
     Commit-Autor ueberein, unter dem die Aenderung spaeter gepusht wird
  3. "Unbekannt" — nie ein Personenname als Rueckfallwert

Das Frontend kann pro Browser einen abweichenden Namen senden (geteilter
Rechner, zwei Personen an einem Login); der wird hier nur normalisiert.
"""

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

UNKNOWN_REVIEWER = "Unbekannt"
MAX_LEN = 80

_cached_default: str | None = None


def _git_user_name() -> str:
    """git config user.name des Checkouts, oder '' wenn nicht ermittelbar."""
    try:
        proc = subprocess.run(
            ["git", "config", "user.name"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def default_reviewer(*, refresh: bool = False) -> str:
    """Rueckfall-Name fuer Schreibzugriffe ohne explizite Angabe.

    Wird beim ersten Aufruf ermittelt und gecacht (der Wert aendert sich
    waehrend einer Serverlaufzeit nicht). `refresh=True` erzwingt Neuermittlung.
    """
    global _cached_default
    if _cached_default is not None and not refresh:
        return _cached_default

    name = normalize(os.environ.get("SZD_REVIEWER", ""))
    if not name:
        name = normalize(_git_user_name())
    _cached_default = name or UNKNOWN_REVIEWER
    return _cached_default


def normalize(value) -> str:
    """Whitespace zusammenfassen, laengenbegrenzen; ungueltig -> ''."""
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())[:MAX_LEN]


def clean_reviewer(value) -> str:
    """Vom Frontend gesendeten Namen normalisieren; leer -> default_reviewer()."""
    return normalize(value) or default_reviewer()
