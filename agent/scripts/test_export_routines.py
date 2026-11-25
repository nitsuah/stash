"""pytest coverage for the redaction helpers in agent/scripts/export-routines.py."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "export_routines", os.path.join(HERE, "export-routines.py")
)
er = importlib.util.module_from_spec(spec)
spec.loader.exec_module(er)


def test_unquote_plain():
    assert er.unquote('"plain"') == "plain"


def test_unquote_json_escaped():
    assert er.unquote('"a\\nb"') == "a\nb"


def test_unquote_single_quoted_with_apostrophe():
    assert er.unquote("'it''s'") == "it's"


def test_unquote_unquoted_unchanged():
    assert er.unquote("x") == "x"


def test_unquote_lone_double_quote_unchanged():
    assert er.unquote('"') == '"'


def test_unquote_mismatched_quotes_unchanged():
    assert er.unquote("\"abc'") == "\"abc'"


def test_leaks_nothing_to_see():
    assert er.leaks("nothing to see here") == []


def test_leaks_flags_personal_email():
    hits = er.leaks("someone@gmail.com")
    assert hits == ["someone@gmail.com"]


def test_leaks_does_not_flag_allowed_emails():
    allowed = [
        "noreply@anthropic.com",
        "no-reply@x.io",
        "12345+user@users.noreply.github.com",
        "dev@example.com",
    ]
    for email in allowed:
        assert er.leaks(email) == [], f"should not flag {email}"


def test_leaks_flags_us_phone():
    hits = er.leaks("415-555-1234")
    assert hits, "should flag US phone number"


def test_leaks_flags_github_token():
    token = "ghp_" + "a" * 36
    hits = er.leaks(token)
    assert hits, "should flag GitHub token"


def test_leaks_flags_aws_key_id():
    key = "AKIA" + "A" * 16
    hits = er.leaks(key)
    assert hits, "should flag AWS key id"


def test_leaks_flags_rsa_private_key_header():
    hits = er.leaks("-----BEGIN RSA PRIVATE KEY-----")
    assert hits, "should flag RSA private key header"


def test_leaks_flags_sk_ant_key():
    key = "sk-ant-" + "a" * 24
    hits = er.leaks(key)
    assert hits, "should flag sk-ant key"


def test_leaks_multiple_hits():
    text = "contact someone@gmail.com and token ghp_" + "a" * 36
    hits = er.leaks(text)
    assert len(hits) >= 2, "should find both email and token"
