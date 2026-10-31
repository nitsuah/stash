"""Test script-summary extraction strips closing docstring delimiters."""
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("build_vault_indexes", HERE / "build-vault-indexes.py")
BVI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BVI)


@pytest.mark.parametrize(
    "source, expected",
    [
        ('"""Conftest description."""\n', "Conftest description"),
        ("'''Single-quoted description.'''", "Single-quoted description"),
        ('"""No trailing period"""', "No trailing period"),
    ],
)
def test_script_summary_strips_closing_docstring_delimiter(monkeypatch, source, expected):
    monkeypatch.setattr(BVI, "read", lambda _rel: (source, "\n"))
    assert BVI.script_summary("scripts/sample.py") == expected
