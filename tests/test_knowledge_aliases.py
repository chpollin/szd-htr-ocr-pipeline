"""Renamed knowledge documents stay reachable under their former slugs.

The knowledge base was renamed along the Promptotyping templates (2026-10-28).
Older journal entries, reviewer paragraphs and bookmarks still use the former
slugs; build_knowledge() must turn them into the current ones.
"""

import json

from build_viewer_data import build_knowledge

INDEX = """---
title: Index
---

## Dokumente

### Grundlagen

| Dokument | Funktion |
|---|---|
| [[transcription-guidelines]] | Domain Knowledge |
| [[old-name]] | Domain Knowledge |

## Lesepfade

- Sessionstart: [[INDEX]] → [[journal]]
"""

GUIDELINES = """---
title: Transcription Guidelines
aliases: [old-name]
related: ["[[journal]]"]
---

# Transcription Guidelines

See [[old-name]] and [[journal]] and [[INDEX]].
"""

JOURNAL = """---
title: Journal
aliases: [transcription-guidelines]
---

## 2026-04-01

Earlier entry linking [[old-name]].
"""


def _build(tmp_path):
    kdir = tmp_path / "knowledge"
    kdir.mkdir()
    (kdir / "INDEX.md").write_text(INDEX, encoding="utf-8")
    (kdir / "transcription-guidelines.md").write_text(GUIDELINES, encoding="utf-8")
    (kdir / "journal.md").write_text(JOURNAL, encoding="utf-8")
    out = tmp_path / "knowledge.json"
    build_knowledge(knowledge_dir=kdir, out_path=out)
    return json.loads(out.read_text(encoding="utf-8"))


def test_alias_table_maps_former_slug_to_current(tmp_path):
    data = _build(tmp_path)
    assert data["aliases"] == {"old-name": "transcription-guidelines"}


def test_alias_never_shadows_a_live_document(tmp_path):
    data = _build(tmp_path)
    assert "transcription-guidelines" not in data["aliases"]


def test_index_is_structure_not_a_document(tmp_path):
    data = _build(tmp_path)
    assert set(data["docs"]) == {"transcription-guidelines", "journal"}
    assert data["sections"] == [
        {"label": "Grundlagen", "slugs": ["transcription-guidelines"]}
    ]


def test_old_wikilinks_render_with_current_slug(tmp_path):
    data = _build(tmp_path)
    journal_html = data["docs"]["journal"]["html"]
    assert 'href="#knowledge/transcription-guidelines"' in journal_html
    assert "#knowledge/old-name" not in journal_html
    guide_html = data["docs"]["transcription-guidelines"]["html"]
    assert 'href="#knowledge"' in guide_html
    assert data["docs"]["transcription-guidelines"]["related"] == ["journal"]
