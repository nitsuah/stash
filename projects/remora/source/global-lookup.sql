SELECT [user_name], "APP" as Type from APP_Roster
UNION ALL
SELECT [PRIME ID], "RATIONAL" as Type from [Rational Extended]
UNION ALL
SELECT [Username], "SNAPSHOT" as Type from [Snapshot Extended]
UNION ALL
SELECT [Username], "APPNP" as Type from [APPNP-AD-Xtd]
UNION ALL SELECT [Username], "APPSP" as Type  from [APPSP-AD-Xtd];
