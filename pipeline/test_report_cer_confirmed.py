"""Checks that the confirmed-text error rate counts what its docstring says."""

from report_cer_confirmed import levenshtein, measure_object, with_rates


def _object(status: str, pages: list[dict]) -> dict:
    return {"review": {"status": status}, "result": {"pages": pages}}


def test_levenshtein_known_answers():
    assert levenshtein("kitten", "sitting") == 3
    assert levenshtein("", "abc") == 3
    assert levenshtein("auch tief", "auch tief") == 0


def test_only_human_statuses_are_measured():
    page = {"transcription": "nicht tief", "transcription_llm": "auch tief"}
    assert measure_object(_object("agent_verified", [page])) is None
    assert measure_object(_object("approved", [page])) is not None


def test_edited_page_counts_its_distance_and_unedited_page_counts_zero():
    counts = measure_object(
        _object(
            "approved",
            [
                {"transcription": "nicht tief", "transcription_llm": "auch tief"},
                {"transcription": "Salzburg"},
                {"transcription": ""},
            ],
        )
    )
    assert counts == {
        "pages": 3,
        "pages_with_text": 2,
        "pages_edited": 1,
        "distance": levenshtein("auch tief", "nicht tief"),
        "chars": len("nicht tief") + len("Salzburg"),
    }


def test_rate_is_distance_over_confirmed_characters():
    rows = with_rates(
        {"korrespondenzen": {"objects": 1, "pages": 1, "pages_with_text": 1, "pages_edited": 1, "distance": 5, "chars": 100}}
    )
    assert rows["all"]["cer"] == 0.05
