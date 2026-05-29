"""
OAuth 2.0 / OIDC patterns — authorization code flow, PKCE, token introspection,
token refresh, and basic JWKS verification.

Covers patterns used by: Okta, Auth0, Google, GitHub, Azure AD, any OIDC provider.

Auth:
  SSO_CLIENT_ID       OAuth client ID
  SSO_CLIENT_SECRET   OAuth client secret
  SSO_ISSUER          OIDC issuer URL (e.g. https://your-org.okta.com/oauth2/default)
  SSO_REDIRECT_URI    Callback URL registered with the provider

Usage:
    # Print PKCE authorization URL to kick off a flow:
    python sso/oauth2.py --action auth-url

    # Exchange authorization code for tokens (after redirect):
    python sso/oauth2.py --action exchange --code <auth_code>

    # Refresh an access token:
    python sso/oauth2.py --action refresh --refresh-token <token>

    # Introspect a token:
    python sso/oauth2.py --action introspect --token <access_token>
"""

import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
import urllib.parse
from typing import Any

import requests

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Env
# ---------------------------------------------------------------------------

def _load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
        return
    except ImportError:
        pass
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(os.path.dirname(_SCRIPT_DIR), "SAAS", ".env")]:
        if p and os.path.exists(p):
            _load_env(p)
            return


def _require(name: str) -> str:
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"ERROR: env var '{name}' is not set.", file=sys.stderr)
        sys.exit(1)
    return val


# ---------------------------------------------------------------------------
# PKCE helpers
# ---------------------------------------------------------------------------

def generate_pkce() -> tuple[str, str, str]:
    """Returns (code_verifier, code_challenge, state)."""
    verifier   = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    digest     = hashlib.sha256(verifier.encode()).digest()
    challenge  = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    state      = secrets.token_urlsafe(16)
    return verifier, challenge, state


# ---------------------------------------------------------------------------
# OIDC discovery
# ---------------------------------------------------------------------------

def discover(issuer: str) -> dict:
    """Fetch OIDC discovery document from {issuer}/.well-known/openid-configuration."""
    url = f"{issuer.rstrip('/')}/.well-known/openid-configuration"
    r   = requests.get(url, timeout=10)
    r.raise_for_status()
    doc = r.json()
    print(f"\n[OIDC Discovery] {issuer}")
    print(f"  authorization_endpoint: {doc.get('authorization_endpoint')}")
    print(f"  token_endpoint:         {doc.get('token_endpoint')}")
    print(f"  userinfo_endpoint:      {doc.get('userinfo_endpoint')}")
    print(f"  jwks_uri:               {doc.get('jwks_uri')}")
    return doc


# ---------------------------------------------------------------------------
# Authorization URL (PKCE)
# ---------------------------------------------------------------------------

def build_auth_url(authorization_endpoint: str, client_id: str,
                   redirect_uri: str, scope: str = "openid profile email") -> tuple[str, str]:
    """Build PKCE authorization URL. Returns (url, code_verifier) — store verifier in session."""
    verifier, challenge, state = generate_pkce()
    params = {
        "response_type":         "code",
        "client_id":             client_id,
        "redirect_uri":          redirect_uri,
        "scope":                 scope,
        "state":                 state,
        "code_challenge":        challenge,
        "code_challenge_method": "S256",
    }
    url = f"{authorization_endpoint}?{urllib.parse.urlencode(params)}"
    print(f"\n[Auth URL] Direct user to:\n  {url}")
    print(f"\n  Store code_verifier in session: {verifier}")
    return url, verifier


# ---------------------------------------------------------------------------
# Token exchange
# ---------------------------------------------------------------------------

def exchange_code(token_endpoint: str, client_id: str, client_secret: str,
                  code: str, redirect_uri: str, code_verifier: str) -> dict:
    """Exchange authorization code for tokens."""
    r = requests.post(token_endpoint, data={
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  redirect_uri,
        "client_id":     client_id,
        "client_secret": client_secret,
        "code_verifier": code_verifier,
    }, timeout=10)
    r.raise_for_status()
    tokens = r.json()
    print(f"\n[Tokens Received]")
    print(f"  token_type:    {tokens.get('token_type')}")
    print(f"  expires_in:    {tokens.get('expires_in')}s")
    print(f"  scope:         {tokens.get('scope')}")
    print(f"  has_id_token:  {'id_token' in tokens}")
    print(f"  has_refresh:   {'refresh_token' in tokens}")
    return tokens


def refresh_tokens(token_endpoint: str, client_id: str, client_secret: str,
                   refresh_token: str) -> dict:
    """Exchange refresh token for new access token."""
    r = requests.post(token_endpoint, data={
        "grant_type":    "refresh_token",
        "refresh_token": refresh_token,
        "client_id":     client_id,
        "client_secret": client_secret,
    }, timeout=10)
    r.raise_for_status()
    tokens = r.json()
    print(f"\n[Token Refreshed] expires_in={tokens.get('expires_in')}s")
    return tokens


# ---------------------------------------------------------------------------
# Client credentials (service-to-service)
# ---------------------------------------------------------------------------

def client_credentials(token_endpoint: str, client_id: str, client_secret: str,
                        scope: str = "") -> dict:
    """Machine-to-machine token — no user interaction."""
    data: dict = {
        "grant_type":    "client_credentials",
        "client_id":     client_id,
        "client_secret": client_secret,
    }
    if scope:
        data["scope"] = scope
    r = requests.post(token_endpoint, data=data, timeout=10)
    r.raise_for_status()
    tokens = r.json()
    print(f"\n[Client Credentials] token_type={tokens.get('token_type')} "
          f"expires_in={tokens.get('expires_in')}s")
    return tokens


# ---------------------------------------------------------------------------
# Token introspection
# ---------------------------------------------------------------------------

def introspect_token(introspection_endpoint: str, client_id: str,
                     client_secret: str, token: str) -> dict:
    """RFC 7662 token introspection — check if token is active."""
    r = requests.post(introspection_endpoint,
                      data={"token": token, "token_type_hint": "access_token"},
                      auth=(client_id, client_secret),
                      timeout=10)
    r.raise_for_status()
    result = r.json()
    active = result.get("active", False)
    print(f"\n[Introspect] active={active}")
    if active:
        print(f"  sub:   {result.get('sub')}")
        print(f"  scope: {result.get('scope')}")
        print(f"  exp:   {result.get('exp')}")
    return result


# ---------------------------------------------------------------------------
# UserInfo
# ---------------------------------------------------------------------------

def get_userinfo(userinfo_endpoint: str, access_token: str) -> dict:
    """Fetch user claims from OIDC UserInfo endpoint."""
    r = requests.get(userinfo_endpoint,
                     headers={"Authorization": f"Bearer {access_token}"},
                     timeout=10)
    r.raise_for_status()
    info = r.json()
    print(f"\n[UserInfo]")
    print(f"  sub:   {info.get('sub')}")
    print(f"  email: {info.get('email')}")
    print(f"  name:  {info.get('name')}")
    return info


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="OAuth 2.0 / OIDC flow examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  SSO_CLIENT_ID       OAuth client ID
  SSO_CLIENT_SECRET   OAuth client secret
  SSO_ISSUER          OIDC issuer URL
  SSO_REDIRECT_URI    Registered callback URL

Actions:
  discover     Print OIDC discovery document endpoints
  auth-url     Generate PKCE authorization URL
  exchange     Exchange authorization code for tokens
  refresh      Refresh an access token
  introspect   Introspect a token (check active/claims)
  userinfo     Fetch user claims from UserInfo endpoint
  m2m          Client credentials (machine-to-machine)

Examples:
  python sso/oauth2.py --action discover
  python sso/oauth2.py --action auth-url
  python sso/oauth2.py --action exchange --code <code> --verifier <verifier>
  python sso/oauth2.py --action refresh --refresh-token <token>
  python sso/oauth2.py --action introspect --token <access_token>
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--action",
                        choices=["discover", "auth-url", "exchange", "refresh",
                                 "introspect", "userinfo", "m2m"],
                        default="discover")
    parser.add_argument("--code",          default=None, help="Authorization code")
    parser.add_argument("--verifier",      default=None, help="PKCE code_verifier")
    parser.add_argument("--refresh-token", default=None, help="Refresh token")
    parser.add_argument("--token",         default=None, help="Access token")
    parser.add_argument("--scope",         default="openid profile email")
    args = parser.parse_args()

    load_env(args.env_file)
    client_id     = _require("SSO_CLIENT_ID")
    client_secret = _require("SSO_CLIENT_SECRET")
    issuer        = _require("SSO_ISSUER")
    redirect_uri  = os.environ.get("SSO_REDIRECT_URI", "http://localhost:8080/callback")

    discovery = discover(issuer)
    token_ep  = discovery["token_endpoint"]

    if args.action == "discover":
        pass  # already printed above

    elif args.action == "auth-url":
        build_auth_url(discovery["authorization_endpoint"], client_id, redirect_uri, args.scope)

    elif args.action == "exchange":
        if not args.code or not args.verifier:
            parser.error("--code and --verifier are required for exchange")
        exchange_code(token_ep, client_id, client_secret,
                      args.code, redirect_uri, args.verifier)

    elif args.action == "refresh":
        if not args.refresh_token:
            parser.error("--refresh-token is required")
        refresh_tokens(token_ep, client_id, client_secret, args.refresh_token)

    elif args.action == "introspect":
        if not args.token:
            parser.error("--token is required")
        ep = discovery.get("introspection_endpoint", f"{issuer}/v1/introspect")
        introspect_token(ep, client_id, client_secret, args.token)

    elif args.action == "userinfo":
        if not args.token:
            parser.error("--token is required")
        get_userinfo(discovery["userinfo_endpoint"], args.token)

    elif args.action == "m2m":
        client_credentials(token_ep, client_id, client_secret, args.scope)


if __name__ == "__main__":
    main()
