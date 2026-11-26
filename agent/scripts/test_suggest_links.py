"""pytest coverage for suggest-links.py: embeddings() and link_map().

The script runs its report at import time, so only the definitions above the
`vecs, links = ...` line are executed here.
"""
import os
import shutil
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "suggest-links.py")

with open(SCRIPT, encoding="utf-8") as fh:
    _head = fh.read().split("\nvecs, links = ")[0]
sl = types.ModuleType("suggest_links")
sl.__file__ = SCRIPT
exec(compile(_head, SCRIPT, "exec"), sl.__dict__)


def write_ajson(tmp_path, lines, name="x.ajson"):
    folder = tmp_path / ".smart-env" / "multi"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def src_line(path, vec):
    return f'"smart_sources:{path}": {{"embeddings": {{"m": {{"vec": {list(vec)}}}}}}},'


def test_embeddings_normalises_vectors(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    write_ajson(tmp_path, [src_line("a.md", [3, 4])])
    assert sl.embeddings()["a.md"] == [0.6, 0.8]


def test_embeddings_null_line_deletes_the_note(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    write_ajson(tmp_path, [src_line("a.md", [3, 4]), '"smart_sources:a.md": null,'])
    assert sl.embeddings() == {}


def test_embeddings_skips_malformed_json(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    write_ajson(tmp_path, ['"smart_sources:bad.md": {"embeddings": oops},', src_line("a.md", [1, 0])])
    assert list(sl.embeddings()) == ["a.md"]


def test_embeddings_skips_vectors_of_a_different_dimension(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    write_ajson(tmp_path, [src_line("a.md", [1, 0]), src_line("b.md", [1, 0, 0])])
    assert list(sl.embeddings()) == ["a.md"]


def test_embeddings_zero_vector_does_not_divide_by_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    write_ajson(tmp_path, [src_line("a.md", [0, 0])])
    assert sl.embeddings()["a.md"] == [0, 0]


def test_link_map_records_links_in_both_directions(tmp_path, monkeypatch):
    (tmp_path / "scripts").mkdir()
    shutil.copy(os.path.join(HERE, "find-orphans.py"), tmp_path / "scripts" / "find-orphans.py")
    (tmp_path / "a.md").write_text("see [[b]]\n", encoding="utf-8")
    (tmp_path / "b.md").write_text("b\n", encoding="utf-8")
    (tmp_path / "c.md").write_text("c\n", encoding="utf-8")
    monkeypatch.setattr(sl, "VAULT", str(tmp_path))
    links = sl.link_map()
    assert links["a.md"] == ["b.md"]
    assert links["b.md"] == ["a.md"]
    assert links["c.md"] == []
