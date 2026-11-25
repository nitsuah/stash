"""pytest coverage for agent/scripts/obsidian-json-clean.py normalize()"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "obsidian_json_clean", os.path.join(HERE, "obsidian-json-clean.py")
)
ojc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ojc)


def test_invalid_json_returns_unchanged():
    bad = "{not json"
    assert ojc.normalize(bad, ".obsidian/graph.json") == bad
    assert ojc.normalize(bad, ".obsidian/app.json") == bad


def test_valid_json_reindented_with_trailing_newline():
    inp = '{"a":1,"b":[1,2]}'
    path = ".obsidian/app.json"
    expected = json.dumps({"a": 1, "b": [1, 2]}, indent=2) + "\n"
    assert ojc.normalize(inp, path) == expected


def test_key_order_preserved():
    inp = '{"z":1,"a":2}'
    out = ojc.normalize(inp, ".obsidian/app.json")
    assert out.index('"z"') < out.index('"a"')


def test_non_ascii_survives():
    inp = '{"n":"café"}'
    out = ojc.normalize(inp, ".obsidian/app.json")
    assert "café" in out
    assert "\\u00e9" not in out


def test_graph_json_pins_and_rounds():
    inp = '{"scale":2.5,"close":false,"x":1.23456,"y":3}'
    out = ojc.normalize(inp, ".obsidian/graph.json")
    data = json.loads(out)
    assert data["scale"] == 1
    assert data["close"] is True
    assert data["x"] == 1.235
    assert data["y"] == 3


def test_windows_graph_path_same_behavior():
    inp = '{"scale":2.5,"close":false,"x":1.23456,"y":3}'
    out = ojc.normalize(inp, r"C:\vault\.obsidian\graph.json")
    data = json.loads(out)
    assert data["scale"] == 1
    assert data["close"] is True
    assert data["x"] == 1.235
    assert data["y"] == 3


def test_non_graph_path_only_reindented():
    inp = '{"scale":2.5,"close":false,"x":1.23456,"y":3}'
    out = ojc.normalize(inp, ".obsidian/app.json")
    data = json.loads(out)
    assert data["scale"] == 2.5
    assert data["close"] is False
    assert data["x"] == 1.23456
    assert data["y"] == 3


def test_bare_graph_json_not_matched():
    inp = '{"scale":2.5,"close":false,"x":1.23456,"y":3}'
    out = ojc.normalize(inp, "graph.json")
    data = json.loads(out)
    assert data["scale"] == 2.5
    assert data["close"] is False
    assert data["x"] == 1.23456
    assert data["y"] == 3


def test_top_level_list_at_graph_path_reindented():
    inp = "[1, 2, 3]"
    out = ojc.normalize(inp, ".obsidian/graph.json")
    assert out == json.dumps([1, 2, 3], indent=2) + "\n"
