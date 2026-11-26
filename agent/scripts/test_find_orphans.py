"""pytest coverage for find-orphans.py: strip_code, link regexes, collect."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("find_orphans", os.path.join(HERE, "find-orphans.py"))
fo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fo)


def test_strip_code_drops_backtick_and_tilde_fences():
    text = "keep one\n```\n[[hidden]]\n```\n~~~\n[[also]]\n~~~\nkeep two"
    assert fo.strip_code(text) == "keep one\nkeep two"


def test_strip_code_drops_inline_code_but_keeps_text():
    assert fo.strip_code("see `[[x]]` and [[y]]") == "see  and [[y]]"


def test_strip_code_unclosed_fence_drops_the_rest():
    assert fo.strip_code("before\n```\n[[a]]\n[[b]]") == "before"


def test_strip_code_shorter_closing_fence_does_not_close():
    text = "a\n````\n[[x]]\n```\n[[y]]\n````\nb"
    assert fo.strip_code(text) == "a\nb"


def test_wiki_extracts_target_from_all_link_forms():
    text = "[[a]] [[b|alias]] [[c#Heading]] ![[embed]]"
    assert fo.WIKI.findall(text) == ["a", "b", "c", "embed"]


def test_mdlink_extracts_paths():
    assert fo.MDLINK.findall("[text](dir/note.md)") == ["dir/note.md"]
    assert fo.MDLINK.findall(r"[a \] b](x.md)") == ["x.md"]
    assert fo.MDLINK.findall('[t](p.md "t")') == ["p.md"]


def test_collect_splits_notes_and_attachments_and_skips_ignored(tmp_path, monkeypatch):
    files = [
        "a.md",
        "sub/b.md",
        "img/c.png",
        ".obsidian/x.md",
        "node_modules/y.md",
        "logs/z.md",
        "run.log",
        "note.txt",
    ]
    for rel in files:
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("x", encoding="utf-8")
    monkeypatch.setattr(fo, "VAULT", str(tmp_path))
    notes, attachments = fo.collect()
    assert notes == ["a.md", "sub/b.md"]
    assert attachments == ["img/c.png"]
