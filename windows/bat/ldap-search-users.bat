@echo off
rem =============================================================================
rem LDAP User Search Utilities
rem =============================================================================
rem Requires ldapsearch / ldapadd (OpenLDAP tools or equivalent)
rem Set LDAP_HOST, BIND_DN, PASSWORD, and BASE_DN before running.
rem =============================================================================

set LDAP_HOST=ldap://LDAP_HOST
set BIND_DN=cn=admin,dc=DOMAIN,dc=com
set BASE_DN=ou=users,dc=DOMAIN,dc=com
set PASSWORD=PASSWORD

rem ── Search: all users ────────────────────────────────────────────────────────
rem Returns all entries under the users OU with common attributes
ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
    -b "%BASE_DN%" "(objectClass=person)" ^
    cn mail uid sAMAccountName

rem ── Search: user by email ────────────────────────────────────────────────────
rem ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
rem     -b "%BASE_DN%" "(mail=user@example.com)" ^
rem     cn uid sAMAccountName

rem ── Search: user by username ─────────────────────────────────────────────────
rem ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
rem     -b "%BASE_DN%" "(sAMAccountName=jsmith)" ^
rem     cn mail memberOf

rem ── Search: users in a specific group ────────────────────────────────────────
rem ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
rem     -b "ou=groups,dc=DOMAIN,dc=com" "(cn=GROUPNAME)" ^
rem     member uniqueMember

rem ── Search: disabled accounts ────────────────────────────────────────────────
rem Active Directory: userAccountControl bit 2 = disabled (flags AND 2 = 2)
rem ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
rem     -b "%BASE_DN%" "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=2))" ^
rem     cn sAMAccountName mail

rem ── Search: accounts not logged in since a date ──────────────────────────────
rem ldapsearch -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% ^
rem     -b "%BASE_DN%" "(&(objectClass=user)(lastLogon<=133000000000000000))" ^
rem     cn sAMAccountName lastLogon

rem ── Add: new user from LDIF ──────────────────────────────────────────────────
rem ldapadd -x -H %LDAP_HOST% -D "%BIND_DN%" -w %PASSWORD% -f C:\newusers.ldif
