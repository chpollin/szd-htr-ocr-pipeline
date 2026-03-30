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
