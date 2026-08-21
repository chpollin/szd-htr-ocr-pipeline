"""Shared fixtures: make pipeline/ importable and locate repo paths."""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "pipeline"))


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT
