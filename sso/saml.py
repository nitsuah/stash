"""
SAML 2.0 SP-initiated SSO — parsing assertions, attribute extraction,
and integration pattern for enterprise IdPs (Okta, ADFS, Azure AD, Ping).

This is a reference/demo — production SAML requires a hardened library.

Setup:
    pip install python3-saml requests python-dotenv
    # python3-saml wraps xmlsec1 — install system dep first:
    # Ubuntu: apt install xmlsec1
    # macOS:  brew install libxmlsec1

Environment:
    SAML_SP_ENTITY_ID      SP entity ID (registered with IdP)
    SAML_SP_ACS_URL        Assertion Consumer Service URL
    SAML_IDP_METADATA_URL  IdP metadata URL (or SAML_IDP_METADATA_XML for inline)
    SAML_SP_CERT           Path to SP signing certificate
    SAML_SP_KEY            Path to SP private key

Usage:
    python sso/saml.py --action metadata     # Print SP metadata XML
    python sso/saml.py --action sso-url      # Generate IdP redirect URL
    python sso/saml.py --action parse        # Parse a base64 SAMLResponse
"""

import argparse
import base64
import os
import sys
from xml.etree import ElementTree as ET

import requests

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# SAML namespace map
_NS = {
    "saml":  "urn:oasis:names:tc:SAML:2.0:assertion",
    "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
    "ds":    "http://www.w3.org/2000/09/xmldsig#",
    "md":    "urn:oasis:names:tc:SAML:2.0:metadata",
}


# ---------------------------------------------------------------------------
# Env
# ---------------------------------------------------------------------------

def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(os.path.dirname(_SCRIPT_DIR), "SAAS", ".env")]:
        if p and os.path.exists(p):
            try:
                from dotenv import load_dotenv  # type: ignore
                load_dotenv(p, override=False)
            except ImportError:
                with open(p) as fh:
                    for line in fh:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


# ---------------------------------------------------------------------------
# IdP metadata parsing
# ---------------------------------------------------------------------------

def fetch_idp_metadata(url: str) -> dict:
    """Fetch IdP metadata XML and extract key endpoints and certificate."""
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return parse_idp_metadata(r.text)


def parse_idp_metadata(xml: str) -> dict:
    """Parse IdP metadata XML → dict with sso_url, slo_url, certificate."""
    root   = ET.fromstring(xml)
    result: dict = {}

    # SSO redirect binding
    sso = root.find(".//md:IDPSSODescriptor/md:SingleSignOnService[@Binding='urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect']", _NS)
    if sso is not None:
        result["sso_url"] = sso.get("Location")

    # SLO endpoint
    slo = root.find(".//md:IDPSSODescriptor/md:SingleLogoutService[@Binding='urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect']", _NS)
    if slo is not None:
        result["slo_url"] = slo.get("Location")

    # Signing certificate
    cert = root.find(".//md:IDPSSODescriptor/md:KeyDescriptor[@use='signing']/ds:KeyInfo/ds:X509Data/ds:X509Certificate", _NS)
    if cert is not None and cert.text:
        result["certificate"] = cert.text.strip()

    entity_id = root.get("entityID")
    if entity_id:
        result["entity_id"] = entity_id

    print(f"\n[IdP Metadata] entityID={result.get('entity_id')}")
    print(f"  SSO URL: {result.get('sso_url')}")
    print(f"  SLO URL: {result.get('slo_url')}")
    print(f"  Cert:    {'present' if result.get('certificate') else 'missing'}")
    return result


# ---------------------------------------------------------------------------
# SAMLRequest (AuthnRequest)
# ---------------------------------------------------------------------------

def build_authn_request(sp_entity_id: str, acs_url: str, idp_sso_url: str) -> tuple[str, str]:
    """Build a minimal AuthnRequest. Returns (redirect_url, request_id)."""
    import uuid, zlib, urllib.parse

    request_id = f"_{uuid.uuid4().hex}"
    from datetime import datetime, timezone
    issue_instant = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    authn_request = (
        f'<samlp:AuthnRequest'
        f' xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"'
        f' xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"'
        f' ID="{request_id}"'
        f' Version="2.0"'
        f' IssueInstant="{issue_instant}"'
        f' Destination="{idp_sso_url}"'
        f' ProtocolBinding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"'
        f' AssertionConsumerServiceURL="{acs_url}">'
        f'  <saml:Issuer>{sp_entity_id}</saml:Issuer>'
        f'  <samlp:NameIDPolicy Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress" AllowCreate="true"/>'
        f'</samlp:AuthnRequest>'
    )

    # Deflate + base64 + url-encode (HTTP-Redirect binding)
    deflated  = zlib.compress(authn_request.encode())[2:-4]  # strip zlib header/checksum
    encoded   = base64.b64encode(deflated).decode()
    relay     = ""
    params    = urllib.parse.urlencode({"SAMLRequest": encoded, "RelayState": relay})
    url       = f"{idp_sso_url}?{params}"

    print(f"\n[AuthnRequest] id={request_id}")
    print(f"  Redirect to: {url[:80]}...")
    return url, request_id


# ---------------------------------------------------------------------------
# SAMLResponse parsing
# ---------------------------------------------------------------------------

def parse_saml_response(saml_response_b64: str) -> dict:
    """
    Parse a base64-encoded SAMLResponse.
    WARNING: this does NOT verify the signature — use python3-saml in production.
    """
    try:
        xml = base64.b64decode(saml_response_b64).decode("utf-8", errors="replace")
    except Exception as e:
        raise ValueError(f"Failed to decode SAMLResponse: {e}")

    root = ET.fromstring(xml)
    assertion = root.find(".//saml:Assertion", _NS)
    if assertion is None:
        raise ValueError("No Assertion found in SAMLResponse")

    # NameID (subject)
    name_id_el = assertion.find("saml:Subject/saml:NameID", _NS)
    name_id    = name_id_el.text.strip() if name_id_el is not None and name_id_el.text else None

    # Attributes
    attrs: dict[str, list[str]] = {}
    for attr in assertion.findall("saml:AttributeStatement/saml:Attribute", _NS):
        attr_name = attr.get("Name", "")
        values    = [
            v.text or ""
            for v in attr.findall("saml:AttributeValue", _NS)
        ]
        attrs[attr_name] = values

    # Conditions
    conditions = assertion.find("saml:Conditions", _NS)
    not_before = conditions.get("NotBefore") if conditions is not None else None
    not_after  = conditions.get("NotOnOrAfter") if conditions is not None else None

    result = {
        "name_id":    name_id,
        "attributes": attrs,
        "not_before": not_before,
        "not_after":  not_after,
    }

    print(f"\n[SAMLResponse Parsed]")
    print(f"  NameID:     {name_id}")
    print(f"  Valid:      {not_before} → {not_after}")
    print(f"  Attributes: {list(attrs.keys())}")

    # Common attribute aliases
    email  = (attrs.get("email") or attrs.get("http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress") or [None])[0]
    groups = attrs.get("groups") or attrs.get("memberOf") or []
    if email:
        print(f"  Email:      {email}")
    if groups:
        print(f"  Groups:     {groups[:5]}")

    return result


# ---------------------------------------------------------------------------
# SP Metadata
# ---------------------------------------------------------------------------

def generate_sp_metadata(sp_entity_id: str, acs_url: str,
                          sp_cert_pem: str | None = None) -> str:
    """Generate minimal SP metadata XML for registration with an IdP."""
    cert_block = ""
    if sp_cert_pem:
        cert_clean = sp_cert_pem.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
        cert_block = f"""
    <md:KeyDescriptor use="signing">
      <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:X509Data><ds:X509Certificate>{cert_clean}</ds:X509Certificate></ds:X509Data>
      </ds:KeyInfo>
    </md:KeyDescriptor>"""

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata"
                     entityID="{sp_entity_id}">
  <md:SPSSODescriptor AuthnRequestsSigned="false" WantAssertionsSigned="true"
                      protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">{cert_block}
    <md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat>
    <md:AssertionConsumerService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
                                  Location="{acs_url}" index="1"/>
  </md:SPSSODescriptor>
</md:EntityDescriptor>"""
    print(f"\n[SP Metadata] entityID={sp_entity_id}")
    return xml


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="SAML 2.0 SP-initiated SSO examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  SAML_SP_ENTITY_ID      SP entity ID
  SAML_SP_ACS_URL        Assertion Consumer Service URL
  SAML_IDP_METADATA_URL  IdP metadata URL
  SAML_SP_CERT           Path to SP certificate (PEM)

Actions:
  metadata    Fetch and parse IdP metadata
  sso-url     Build SP-initiated SSO redirect URL
  parse       Parse a base64 SAMLResponse (set SAML_RESPONSE env var)
  sp-metadata Print SP metadata XML for IdP registration

Examples:
  python sso/saml.py --action metadata
  python sso/saml.py --action sso-url
  SAML_RESPONSE=<base64> python sso/saml.py --action parse
  python sso/saml.py --action sp-metadata
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--action",
                        choices=["metadata", "sso-url", "parse", "sp-metadata"],
                        default="metadata")
    args = parser.parse_args()

    load_env(args.env_file)

    sp_entity_id   = os.environ.get("SAML_SP_ENTITY_ID", "https://app.example.com")
    acs_url        = os.environ.get("SAML_SP_ACS_URL",   "https://app.example.com/saml/acs")
    idp_metadata   = os.environ.get("SAML_IDP_METADATA_URL", "")
    sp_cert_path   = os.environ.get("SAML_SP_CERT", "")

    if args.action == "metadata":
        if not idp_metadata:
            print("Set SAML_IDP_METADATA_URL to fetch IdP metadata.", file=sys.stderr)
            sys.exit(1)
        meta = fetch_idp_metadata(idp_metadata)

    elif args.action == "sso-url":
        if not idp_metadata:
            print("Set SAML_IDP_METADATA_URL.", file=sys.stderr)
            sys.exit(1)
        meta = fetch_idp_metadata(idp_metadata)
        build_authn_request(sp_entity_id, acs_url, meta["sso_url"])

    elif args.action == "parse":
        response_b64 = os.environ.get("SAML_RESPONSE", "")
        if not response_b64:
            print("Set SAML_RESPONSE env var to a base64-encoded SAMLResponse.", file=sys.stderr)
            sys.exit(1)
        parse_saml_response(response_b64)

    elif args.action == "sp-metadata":
        cert_pem = None
        if sp_cert_path and os.path.exists(sp_cert_path):
            with open(sp_cert_path) as f:
                cert_pem = f.read()
        xml = generate_sp_metadata(sp_entity_id, acs_url, cert_pem)
        print(xml)


if __name__ == "__main__":
    main()
