"""
AWS IAM Identity Center (SSO) — list accounts, roles, and generate
temporary credentials via the SSO API.

Auth:
  AWS_SSO_START_URL    SSO start URL (e.g. https://your-org.awsapps.com/start)
  AWS_SSO_REGION       Region where Identity Center is configured
  AWS_PROFILE          Optional: named profile for boto3 session

Usage:
    # Device authorization flow (opens browser for login):
    python sso/aws_sso.py --action login

    # List accounts and roles visible to the current SSO session:
    python sso/aws_sso.py --action list-accounts

    # Get temporary credentials for a specific account + role:
    python sso/aws_sso.py --action credentials --account-id 123456789012 --role-name ReadOnly
"""

import argparse
import json
import os
import sys
import time
import webbrowser

import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_TOKEN_CACHE = os.path.join(_SCRIPT_DIR, ".sso_token_cache.json")  # gitignored


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_env(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path, override=False)
    except ImportError:
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
              os.path.join(os.path.dirname(_SCRIPT_DIR), "cloud", ".env")]:
        if p and os.path.exists(p):
            _load_env(p)
            return


def _save_token(token: dict) -> None:
    with open(_TOKEN_CACHE, "w") as f:
        json.dump(token, f)


def _load_token() -> dict | None:
    if not os.path.exists(_TOKEN_CACHE):
        return None
    with open(_TOKEN_CACHE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Device authorization flow
# ---------------------------------------------------------------------------

def sso_login(start_url: str, region: str) -> str:
    """Complete device authorization flow; returns access token."""
    oidc = boto3.client("sso-oidc", region_name=region)

    # Register client (cached for ~90 days in production; recreate here for simplicity)
    reg = oidc.register_client(clientName="stash-sso-example", clientType="public")
    client_id     = reg["clientId"]
    client_secret = reg["clientSecret"]

    # Start device auth
    auth = oidc.start_device_authorization(
        clientId=client_id,
        clientSecret=client_secret,
        startUrl=start_url,
    )

    print(f"\n[SSO Login] Open in browser and authorize:")
    print(f"  {auth['verificationUriComplete']}")
    webbrowser.open(auth["verificationUriComplete"])

    # Poll for token
    interval = auth.get("interval", 5)
    expires  = time.time() + auth.get("expiresIn", 600)
    print(f"  Polling every {interval}s (expires in {auth.get('expiresIn')}s)...")

    while time.time() < expires:
        time.sleep(interval)
        try:
            token_resp = oidc.create_token(
                clientId=client_id,
                clientSecret=client_secret,
                grantType="urn:ietf:params:oauth:grant-type:device_code",
                deviceCode=auth["deviceCode"],
            )
            access_token = token_resp["accessToken"]
            _save_token({"accessToken": access_token, "expiresAt": time.time() + token_resp.get("expiresIn", 28800)})
            print("  Authorized — access token cached.")
            return access_token
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "AuthorizationPendingException":
                continue
            elif code == "SlowDownException":
                interval += 5
            else:
                raise

    raise TimeoutError("SSO login timed out — try again")


# ---------------------------------------------------------------------------
# List accounts / roles
# ---------------------------------------------------------------------------

def list_accounts(access_token: str, region: str) -> list[dict]:
    """List all AWS accounts the authenticated user has access to."""
    sso     = boto3.client("sso", region_name=region)
    accounts: list[dict] = []
    paginator = sso.get_paginator("list_accounts")
    for page in paginator.paginate(accessToken=access_token):
        accounts.extend(page.get("accountList", []))

    print(f"\n[AWS SSO Accounts] {len(accounts)} accounts:")
    for a in accounts:
        print(f"  {a['accountId']}  {a['accountName']}")
    return accounts


def list_account_roles(access_token: str, region: str, account_id: str) -> list[dict]:
    """List permission sets (roles) available in a specific account."""
    sso   = boto3.client("sso", region_name=region)
    roles: list[dict] = []
    paginator = sso.get_paginator("list_account_roles")
    for page in paginator.paginate(accessToken=access_token, accountId=account_id):
        roles.extend(page.get("roleList", []))

    print(f"\n[Roles in {account_id}] {len(roles)} roles:")
    for r in roles:
        print(f"  {r['roleName']}")
    return roles


# ---------------------------------------------------------------------------
# Temporary credentials
# ---------------------------------------------------------------------------

def get_role_credentials(access_token: str, region: str,
                          account_id: str, role_name: str) -> dict:
    """Return temporary STS credentials for a given account + role."""
    sso   = boto3.client("sso", region_name=region)
    resp  = sso.get_role_credentials(
        accessToken=access_token,
        accountId=account_id,
        roleName=role_name,
    )
    creds = resp["roleCredentials"]
    print(f"\n[Credentials] account={account_id} role={role_name}")
    print(f"  AccessKeyId:     {creds['accessKeyId']}")
    print(f"  Expiration:      {creds['expiration']}")
    print(f"\n  Export to shell:")
    print(f"  export AWS_ACCESS_KEY_ID={creds['accessKeyId']}")
    print(f"  export AWS_SECRET_ACCESS_KEY=<redacted>")
    print(f"  export AWS_SESSION_TOKEN=<redacted>")
    return creds


# ---------------------------------------------------------------------------
# Group sync example (Okta → AWS IAM Identity Center via SCIM)
# ---------------------------------------------------------------------------

def describe_scim_integration() -> None:
    """
    Print the pattern for Okta → AWS IAM Identity Center SCIM provisioning.
    The actual sync is configured in the AWS console and Okta admin panel —
    no API calls required on the app side once configured.
    """
    print("""
[SCIM Integration Pattern — Okta → AWS IAM Identity Center]

1. AWS Console → IAM Identity Center → Settings → Enable Automatic Provisioning
   → Copy: SCIM endpoint URL + Access Token

2. Okta Admin → Applications → AWS IAM Identity Center app → Provisioning
   → API Integration → SCIM 2.0 Base URL + OAuth Bearer Token (from step 1)
   → Enable: Push Users, Push Groups

3. Assign Okta groups → AWS Permission Sets in the Okta app assignments tab.
   Okta pushes group membership to IAM Identity Center automatically.

4. In AWS: IAM Identity Center → Permission sets → assign groups to accounts.
   Members of the Okta group get the mapped permission set in each account.

Result: users log in via Okta SSO and get just-in-time access to AWS accounts.
    """)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="AWS IAM Identity Center (SSO) examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  AWS_SSO_START_URL   https://your-org.awsapps.com/start
  AWS_SSO_REGION      us-east-1

Actions:
  login            Device authorization flow (opens browser)
  list-accounts    List accounts visible to current session
  list-roles       List roles in an account
  credentials      Get temp credentials for account + role
  scim-pattern     Print Okta → IAM Identity Center SCIM setup pattern

Examples:
  python sso/aws_sso.py --action login
  python sso/aws_sso.py --action list-accounts
  python sso/aws_sso.py --action credentials --account-id 123456789012 --role-name ReadOnly
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--action",
                        choices=["login", "list-accounts", "list-roles",
                                 "credentials", "scim-pattern"],
                        default="list-accounts")
    parser.add_argument("--account-id", default=None)
    parser.add_argument("--role-name",  default=None)
    args = parser.parse_args()

    load_env(args.env_file)

    start_url = os.environ.get("AWS_SSO_START_URL", "")
    region    = os.environ.get("AWS_SSO_REGION", "us-east-1")

    if args.action == "scim-pattern":
        describe_scim_integration()
        return

    if not start_url:
        print("ERROR: AWS_SSO_START_URL is not set.", file=sys.stderr)
        sys.exit(1)

    # Use cached token or require login
    cached = _load_token()
    if cached and cached.get("expiresAt", 0) > time.time() + 60:
        access_token = cached["accessToken"]
        print("[SSO] Using cached token.")
    else:
        if args.action != "login":
            print("[SSO] No valid token cached — run with --action login first.")
            sys.exit(1)
        access_token = sso_login(start_url, region)

    if args.action == "login":
        pass  # already done above

    elif args.action == "list-accounts":
        list_accounts(access_token, region)

    elif args.action == "list-roles":
        if not args.account_id:
            parser.error("--account-id is required")
        list_account_roles(access_token, region, args.account_id)

    elif args.action == "credentials":
        if not args.account_id or not args.role_name:
            parser.error("--account-id and --role-name are required")
        get_role_credentials(access_token, region, args.account_id, args.role_name)


if __name__ == "__main__":
    main()
