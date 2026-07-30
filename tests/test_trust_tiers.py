"""Trust-tier transitions in the review API (pipeline/serve.py).

Four tiers are stored, not derived: gt_verified, approved, agent_verified, and
the absent review block. These tests pin the three properties the project makes
claims about: only known statuses are written, the machine-generated text
survives a human correction in transcription_llm plus edit_history, and the
review status stays separate from model confidence and quality signals.
"""

import json

import pytest

import serve

COLLECTION = "lebensdokumente"
OBJECT_ID = "o_szd.9001"
MODEL = "gemini-3.1-flash-lite-preview"

BASE_RESULT = {
    "object_id": OBJECT_ID,
    "collection": COLLECTION,
    "group": "A",
    "model": MODEL,
    "result": {
        "pages": [
            {"page": 1, "transcription": "maschinelle Fassung", "notes": "", "type": "content"},
            {"page": 2, "transcription": "zweite Seite", "notes": "", "type": "content"},
        ],
        "confidence": "high",
        "confidence_notes": "",
    },
    "quality_signals": {"needs_review": True, "needs_review_reasons": ["short_page"]},
}


@pytest.fixture
def result_file(tmp_path, monkeypatch):
    """An isolated results tree with one object, wired into serve.py."""
    monkeypatch.setattr(serve, "RESULTS_BASE", tmp_path)
    col_dir = tmp_path / COLLECTION
    col_dir.mkdir()
    path = col_dir / f"{OBJECT_ID}_{MODEL}.json"
    path.write_text(json.dumps(BASE_RESULT, ensure_ascii=False), encoding="utf-8")
    return path


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("status", ["gt_verified", "approved", "agent_verified"])
def test_approve_writes_each_known_tier(result_file, status):
    out = serve.handle_approve({
        "object_id": OBJECT_ID, "collection": COLLECTION,
        "status": status, "reviewed_by": "test-reviewer",
    })
    assert out.get("ok"), out
    assert load(result_file)["review"]["status"] == status


def test_approve_rejects_unknown_tier(result_file):
    out = serve.handle_approve({
        "object_id": OBJECT_ID, "collection": COLLECTION, "status": "verified",
    })
    assert "error" in out
    assert "review" not in load(result_file)


def test_agent_tier_records_the_verifying_model(result_file):
    serve.handle_approve({
        "object_id": OBJECT_ID, "collection": COLLECTION,
        "status": "agent_verified", "agent_model": "claude-opus-4-6",
        "errors_found": 2, "reviewed_by": "test-agent",
    })
    review = load(result_file)["review"]
    assert review["agent_model"] == "claude-opus-4-6"
    assert review["errors_found"] == 2


def test_edit_preserves_the_machine_state_and_logs_provenance(result_file):
    serve.handle_edit({
        "object_id": OBJECT_ID, "collection": COLLECTION,
        "pages": [{"page": 1, "transcription": "korrigierte Fassung"}],
        "reviewed_by": "test-reviewer",
    })
    page = load(result_file)["result"]["pages"][0]

    assert page["transcription"] == "korrigierte Fassung"
    assert page["transcription_llm"] == "maschinelle Fassung"
    assert len(page["edit_history"]) == 1
    entry = page["edit_history"][0]
    assert entry["original_transcription"] == "maschinelle Fassung"
    assert entry["source"] == "human"
    assert entry["edited_by"] == "test-reviewer"


def test_second_edit_appends_history_without_overwriting_the_machine_state(result_file):
    for text in ("erste Korrektur", "zweite Korrektur"):
        serve.handle_edit({
            "object_id": OBJECT_ID, "collection": COLLECTION,
            "pages": [{"page": 1, "transcription": text}],
            "reviewed_by": "test-reviewer",
        })
    page = load(result_file)["result"]["pages"][0]

    assert page["transcription_llm"] == "maschinelle Fassung"
    assert [e["original_transcription"] for e in page["edit_history"]] == [
        "maschinelle Fassung", "erste Korrektur",
    ]


def test_unchanged_page_creates_no_history(result_file):
    serve.handle_edit({
        "object_id": OBJECT_ID, "collection": COLLECTION,
        "pages": [{"page": 1, "transcription": "maschinelle Fassung"}],
    })
    page = load(result_file)["result"]["pages"][0]
    assert "edit_history" not in page
    assert "transcription_llm" not in page


def test_edit_path_cannot_claim_the_agent_tier(result_file):
    """A human edit is never recorded as agent verification."""
    serve.handle_edit({
        "object_id": OBJECT_ID, "collection": COLLECTION, "status": "agent_verified",
        "pages": [{"page": 1, "transcription": "korrigierte Fassung"}],
    })
    assert load(result_file)["review"]["status"] == "approved"


def test_tier_stays_separate_from_confidence_and_signals(result_file):
    """No aggregation: approving an object leaves the other judgements untouched."""
    serve.handle_approve({
        "object_id": OBJECT_ID, "collection": COLLECTION, "status": "approved",
    })
    data = load(result_file)

    assert data["result"]["confidence"] == "high"
    assert data["quality_signals"]["needs_review"] is True
    assert not {"trust_score", "confidence_score", "score"} & set(data)
