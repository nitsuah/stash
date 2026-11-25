"""pytest coverage for agent/scripts/repo-breadcrumbs.py helpers."""
import importlib.util
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("repo_breadcrumbs", os.path.join(HERE, "repo-breadcrumbs.py"))
rb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rb)


def test_rel():
    assert rb.rel("/a/docs", "/a/README.md") == "../README.md"
    assert rb.rel("/a", "/a/docs/X.md") == "./docs/X.md"
    assert rb.rel("/a", "/a/X.md") == "./X.md"


def test_read_write_bom_crlf(tmp_path):
    p = tmp_path / "test.md"
    # Write with BOM and CRLF
    content = "﻿line1\r\nline2\r\n"
    p.write_bytes(content.encode("utf-8"))

    text, nl = rb.read(p)
    assert text == "line1\nline2\n"
    assert nl == "\r\n"

    # Write back with CRLF
    rb.write(p, text, nl)
    raw = p.read_bytes()
    assert raw == b"line1\r\nline2\r\n"


def test_read_write_lf(tmp_path):
    p = tmp_path / "test.md"
    p.write_bytes(b"line1\nline2\n")

    text, nl = rb.read(p)
    assert text == "line1\nline2\n"
    assert nl == "\n"

    rb.write(p, text, nl)
    assert p.read_bytes() == b"line1\nline2\n"


def test_title_of_with_h1(tmp_path):
    p = tmp_path / "test.md"
    p.write_text("# My Title\n\nBody")
    assert rb.title_of(p) == "My Title"


def test_title_of_no_h1(tmp_path):
    p = tmp_path / "my-file.md"
    p.write_text("Just content")
    assert rb.title_of(p) == "my-file"


def test_insert_nav_basic(tmp_path):
    text = "# T\n\nbody"
    nav = "> NAV <!-- nav -->"
    result = rb.insert_nav(text, nav)
    expected = "# T\n\n> NAV <!-- nav -->\n\nbody"
    assert result == expected


def test_insert_nav_idempotent(tmp_path):
    text = "# T\n\nbody"
    nav = "> NAV <!-- nav -->"
    first = rb.insert_nav(text, nav)
    second = rb.insert_nav(first, nav)
    assert first == second


def test_insert_nav_with_frontmatter(tmp_path):
    text = "---\nk: v\n---\n# T\n\nbody"
    nav = "> NAV <!-- nav -->"
    result = rb.insert_nav(text, nav)
    # nav goes after H1, not before front matter
    expected = "---\nk: v\n---\n# T\n\n> NAV <!-- nav -->\n\nbody"
    assert result == expected


def test_insert_nav_no_h1(tmp_path):
    text = "just text"
    nav = "> NAV <!-- nav -->"
    result = rb.insert_nav(text, nav)
    # nav and blank line prepended
    expected = "> NAV <!-- nav -->\n\njust text"
    assert result == expected


def test_insert_nav_removes_old_breadcrumb(tmp_path):
    text = "Breadcrumb: Home > X\n# T\n\nbody"
    nav = "> NAV <!-- nav -->"
    result = rb.insert_nav(text, nav)
    assert "Breadcrumb: Home > X" not in result
    assert result.startswith("# T")


def test_insert_nav_ignores_code_fence_comment(tmp_path):
    # H1 inside code fence should not be treated as title
    text = "```\n# not a title\n```\n# Real\n\nbody"
    nav = "> NAV <!-- nav -->"
    result = rb.insert_nav(text, nav)
    # nav should go after "# Real"
    expected = "```\n# not a title\n```\n# Real\n\n> NAV <!-- nav -->\n\nbody"
    assert result == expected


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
