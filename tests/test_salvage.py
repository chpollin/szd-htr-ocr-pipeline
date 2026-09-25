"""Salvage of broken model responses and the transcription status (quality_signals v1.7).

The failure being pinned: a response that starts as valid JSON and falls into a
repetition loop inside one transcription string (reports/pipeline-totalausfaelle.md).
The complete pages before the loop must be kept, and every scan without a
transcription must count as untranscribed — never as a blank page.
"""

import json

from quality_signals import compute_signals
from transcribe import parse_api_response, untranscribed_placeholder

META = {"language": "Deutsch", "title": "Test"}


def _page(nr, text, notes=""):
    return {"page": nr, "transcription": text, "notes": notes}


def _looping_response(complete_pages, loop_unit="[?] ", repeats=2000):
    """Valid JSON for the complete pages, then a page whose string never closes."""
    head = json.dumps({"pages": complete_pages}, ensure_ascii=False, indent=2)
    head = head.rstrip().rstrip("}").rstrip().rstrip("]").rstrip()
    return head + ',\n    {"page": %d, "transcription": "Anfang ' % (len(complete_pages) + 1) \
        + loop_unit * repeats


def test_salvage_keeps_complete_pages_before_loop():
    pages = [_page(1, "Erste Seite."), _page(2, "Zweite Seite.", "Rueckseite")]
    result, log = parse_api_response(_looping_response(pages), "o_szd.test")
    assert "raw" not in result
    assert [p["page"] for p in result["pages"]] == [1, 2]
    assert result["pages"][1]["notes"] == "Rueckseite"
    assert result["salvage"]["pages_recovered"] == 2
    assert result["confidence"] == "low"
    assert any("vollstaendige Seiten" in m for m in log)


def test_salvage_handles_newline_loop():
    text = _looping_response([_page(1, "Text")], loop_unit="\\n")
    result, _ = parse_api_response(text, "o_szd.test")
    assert len(result["pages"]) == 1


def test_no_complete_page_stays_raw():
    text = _looping_response([], loop_unit="\\n")
    result, _ = parse_api_response(text, "o_szd.test")
    assert result == {"raw": text}


def test_valid_response_is_not_marked_salvaged():
    text = json.dumps({"pages": [_page(1, "Text")], "confidence": "high"})
    result, _ = parse_api_response(text, "o_szd.test")
    assert "salvage" not in result


def test_untranscribed_placeholder_is_not_blank():
    pages = [_page(1, "x" * 200), untranscribed_placeholder(2, "Modellantwort nach Seite 1 abgebrochen.")]
    q = compute_signals({"pages": pages}, META, 2)
    assert q["page_types"] == ["content", "content"]
    assert q["blank_pages"] == 0
    assert q["transcription_status"] == "partial"
    assert q["untranscribed_pages"] == [1]
    assert "transcription_partial" in q["needs_review_reasons"]


def test_legacy_chunk_error_counts_as_untranscribed():
    pages = [_page(1, "x" * 200), _page(2, "", "Chunk-Fehler: JSON nicht parsebar.")]
    q = compute_signals({"pages": pages}, META, 2)
    assert q["page_types"][1] == "content"
    assert q["transcription_status"] == "partial"


def test_raw_result_is_failed():
    q = compute_signals({"raw": "{\"pages\": ["}, META, 3)
    assert q["transcription_status"] == "failed"
    assert "transcription_failed" in q["needs_review_reasons"]


def test_real_blank_page_stays_blank_and_complete():
    pages = [_page(1, "x" * 200), _page(2, "", "Rueckseite, leer.")]
    q = compute_signals({"pages": pages}, META, 2)
    assert q["page_types"] == ["content", "blank"]
    assert q["transcription_status"] == "complete"
    assert not any(r.startswith("transcription_") for r in q["needs_review_reasons"])
