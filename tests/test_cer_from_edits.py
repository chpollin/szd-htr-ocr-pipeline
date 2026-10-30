"""CER from edits must never count agent corrections as human corrections."""

import json

from report_cer_from_edits import collect, edit_source, summarize


def _write(path, object_id, status, source, raw, corrected):
    path.write_text(
        json.dumps(
            {
                "object_id": object_id,
                "review": {"status": status},
                "result": {
                    "pages": [
                        {
                            "page": 1,
                            "transcription_llm": raw,
                            "transcription": corrected,
                            "edit_history": [
                                {"original_transcription": raw, "source": source}
                            ],
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )


def test_agent_edits_are_not_counted_as_human(tmp_path):
    coll = tmp_path / "werke"
    coll.mkdir()
    # human page: 1 of 10 characters wrong; agent page: identical text
    _write(coll / "o_h.json", "o_h", "approved", "human", "abcdefghiX", "abcdefghij")
    _write(
        coll / "o_a.json", "o_a", "agent_verified", "agent", "0123456789", "0123456789"
    )

    rows, _ = collect(tmp_path, None)
    summary = summarize(rows)

    assert summary["human"]["pages"] == 1
    assert summary["human"]["cer"] == 0.1
    assert summary["agent"]["pages"] == 1
    assert summary["agent"]["cer"] == 0.0


def test_mixed_and_missing_sources_stay_out_of_human():
    assert (
        edit_source({"edit_history": [{"source": "human"}, {"source": "agent"}]})
        == "mixed"
    )
    assert edit_source({"edit_history": [{}]}) == "unknown"
    assert edit_source({}) == "unknown"
