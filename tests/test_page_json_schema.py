"""Validate the exported Page-JSON files against schemas/page-json-v0.2.json.

The exchange format is the contract with downstream tools (teiCrafter, PAGE XML,
METS). A silent drift between exporter and schema would only surface there.
"""

import json

import pytest

jsonschema = pytest.importorskip("jsonschema")


@pytest.fixture(scope="module")
def schema(repo_root):
    path = repo_root / "schemas" / "page-json-v0.2.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def page_json_files(repo_root):
    return sorted((repo_root / "results").glob("*/*_page.json"))


def test_schema_is_valid_draft_2020_12(schema):
    jsonschema.Draft202012Validator.check_schema(schema)


def test_exported_page_json_matches_schema(schema, page_json_files):
    if not page_json_files:
        pytest.skip("no exported Page-JSON files in results/")

    validator = jsonschema.Draft202012Validator(schema)
    failures = []
    for path in page_json_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for error in validator.iter_errors(data):
            location = "/".join(str(p) for p in error.absolute_path) or "<root>"
            failures.append(f"{path.name}: {location}: {error.message}")
            break

    assert not failures, "Page-JSON schema violations:\n" + "\n".join(failures[:20])


def test_page_json_declares_supported_version(page_json_files):
    if not page_json_files:
        pytest.skip("no exported Page-JSON files in results/")
    versions = {
        json.loads(p.read_text(encoding="utf-8")).get("page_json")
        for p in page_json_files
    }
    assert versions <= {"0.1", "0.2"}, f"unexpected page_json versions: {versions}"
