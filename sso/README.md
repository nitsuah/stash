# SSO / Identity

Python examples for SSO protocols and identity platform integrations.

## Scripts

| Script | Covers |
|--------|--------|
| [`oauth2.py`](oauth2.py) | OAuth 2.0 / OIDC — auth code + PKCE, token exchange, refresh, introspection, client credentials, UserInfo |
| [`saml.py`](saml.py) | SAML 2.0 — IdP metadata parsing, AuthnRequest, SAMLResponse parsing, SP metadata generation |
| [`aws_sso.py`](aws_sso.py) | AWS IAM Identity Center — device auth flow, list accounts/roles, get temp credentials, Okta SCIM pattern |

---

## OAuth 2.0 / OIDC

Works with any OIDC-compliant provider: Okta, Auth0, Google, Azure AD, GitHub, Ping.

```bash
pip install requests python-dotenv
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `SSO_CLIENT_ID` | OAuth client ID |
| `SSO_CLIENT_SECRET` | OAuth client secret |
| `SSO_ISSUER` | OIDC issuer URL (e.g. `https://your-org.okta.com/oauth2/default`) |
| `SSO_REDIRECT_URI` | Registered callback URL |

### Actions

```bash
# Print OIDC discovery endpoints
python sso/oauth2.py --action discover

# Generate PKCE auth URL (SP-initiated login)
python sso/oauth2.py --action auth-url

# Exchange auth code for tokens (after IdP redirect)
python sso/oauth2.py --action exchange --code <code> --verifier <pkce_verifier>

# Refresh access token
python sso/oauth2.py --action refresh --refresh-token <token>

# Introspect token (check active/claims)
python sso/oauth2.py --action introspect --token <access_token>

# Fetch user claims from UserInfo endpoint
python sso/oauth2.py --action userinfo --token <access_token>

# Machine-to-machine (no user, client credentials grant)
python sso/oauth2.py --action m2m
```

---

## SAML 2.0

Works with Okta, ADFS, Azure AD, Ping Identity.

```bash
pip install requests python-dotenv
# For signature verification (production): pip install python3-saml
# System dep: apt install xmlsec1  OR  brew install libxmlsec1
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `SAML_SP_ENTITY_ID` | SP entity ID registered with IdP |
| `SAML_SP_ACS_URL` | Assertion Consumer Service URL |
| `SAML_IDP_METADATA_URL` | IdP metadata XML URL |
| `SAML_SP_CERT` | Path to SP signing certificate (PEM) |

### Actions

```bash
# Parse IdP metadata XML
python sso/saml.py --action metadata

# Build SP-initiated SSO redirect URL
python sso/saml.py --action sso-url

# Parse a base64 SAMLResponse (NameID + attributes extraction)
SAML_RESPONSE=<base64> python sso/saml.py --action parse

# Print SP metadata XML for IdP registration
python sso/saml.py --action sp-metadata
```

> **Note:** `saml.py` does not verify assertion signatures — use `python3-saml` or `pysaml2` for production. Signature verification requires matching the IdP certificate from metadata.

---

## AWS IAM Identity Center

```bash
pip install boto3 python-dotenv
```

### Environment variables

| Variable | Description |
|----------|-------------|
| `AWS_SSO_START_URL` | SSO portal URL (`https://your-org.awsapps.com/start`) |
| `AWS_SSO_REGION` | Region where Identity Center is configured |

### Actions

```bash
# Device authorization — opens browser, caches token
python sso/aws_sso.py --action login

# List all accessible accounts
python sso/aws_sso.py --action list-accounts

# List permission sets (roles) in an account
python sso/aws_sso.py --action list-roles --account-id 123456789012

# Get temporary credentials for account + role
python sso/aws_sso.py --action credentials --account-id 123456789012 --role-name ReadOnly

# Print Okta → IAM Identity Center SCIM setup pattern
python sso/aws_sso.py --action scim-pattern
```

---

## Auth patterns quick reference

| Scenario | Pattern | Script |
|----------|---------|--------|
| Web app user login | Auth code + PKCE | `oauth2.py --action auth-url` |
| Service-to-service API | Client credentials | `oauth2.py --action m2m` |
| Enterprise IdP (Okta/ADFS) | SAML 2.0 | `saml.py` |
| Token validation (middleware) | OIDC JWKS / introspection | `oauth2.py --action introspect` |
| AWS console / CLI access | IAM Identity Center SSO | `aws_sso.py` |
| User sync from Okta → AWS | SCIM provisioning | `aws_sso.py --action scim-pattern` |
