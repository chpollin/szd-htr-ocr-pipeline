"""Tests for quality_signals — focus on Signal 1 envelope exemption (v1.6)."""

from quality_signals import compute_signals, _is_envelope


def _page(num, text, notes="", ):
    return {"page": num, "transcription": text, "notes": notes}


def _signals(pages, n_images=None):
    return compute_signals(
        {"pages": pages}, metadata={}, input_image_count=n_images or len(pages)
    )


def test_envelope_page_does_not_trigger_anomaly():
    # Real AAL pattern: two long letter pages + short envelope address side
    pages = [
        _page(1, "x" * 1200, "Brief, handschriftlich."),
        _page(2, "x" * 1000, "Fortsetzung des Briefs."),
        _page(3, "Miss Lotte Altmann\nLondon NW 11", "Adressseite eines Briefumschlags."),
    ]
    q = _signals(pages)
    assert q["page_length_anomalies"] == []
    assert "page_length_anomaly" not in q["needs_review_reasons"]


def test_short_content_page_still_triggers_anomaly():
    # Same lengths, but the short page is NOT an envelope -> must still flag
    pages = [
        _page(1, "x" * 1200, "Brief, handschriftlich."),
        _page(2, "x" * 1000, "Fortsetzung des Briefs."),
        _page(3, "x" * 30, "Letzte Seite des Briefs."),
    ]
    q = _signals(pages)
    assert q["page_length_anomalies"] == [2]
    assert "page_length_anomaly" in q["needs_review_reasons"]


def test_envelope_detection_keywords():
    assert _is_envelope({"notes": "Adressseite eines Briefumschlags."})
    assert _is_envelope({"notes": "Rückseite des Briefumschlags mit Absenderadresse."})
    assert _is_envelope({"notes": "Kuvert mit Briefmarke."})
    assert _is_envelope({"notes": "Envelope, address side."})
    assert not _is_envelope({"notes": "Brief auf Briefpapier mit Briefkopf."})
    assert not _is_envelope({"notes": ""})
    assert not _is_envelope({})


def test_envelope_stays_content_page():
    # Exemption must not reclassify the page — addresses are research-relevant
    pages = [
        _page(1, "x" * 1200, "Brief."),
        _page(2, "Miss Lotte Altmann\nLondon NW 11", "Adressseite eines Briefumschlags."),
    ]
    q = _signals(pages)
    assert q["page_types"] == ["content", "content"]
    assert q["content_pages"] == 2


def test_version_bumped():
    q = _signals([_page(1, "x" * 100, "Brief.")])
    assert q["version"] == "1.6"


if __name__ == "__main__":
    import sys
    mod = sys.modules["__main__"]
    failed = 0
    for name in dir(mod):
        if name.startswith("test_"):
            try:
                getattr(mod, name)()
                print(f"  OK   {name}")
            except AssertionError as e:
                failed += 1
                print(f"  FAIL {name}: {e}")
    sys.exit(1 if failed else 0)
