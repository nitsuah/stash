Public Sub AR_import_cleanup()
'Params & Vars
FilePath as TempVars
FileName as TempVars 'or string

'If user selects no, exits form by using close buttons, or hits cancel insert current users from arb_tmp and remove from ARR_master
DoCmd.SQL=(select * from arb_tmp where AR_ID = Max(AR_ID) AND username = userID)

'Loop conditional if user backs out of wizard tool
loop (x, FilePath, x + 1 )
while x < Maxof AutoID from ARB_tmp
DoCmd.SQL=(delete * from AR_master where username = userID AND AR_ID = x)

'Add check step during loop to find any \\ntfs\ and  override for Z:\
if (FilePath LIKE "\\ntfs\")
then SET FilePath = "Z:\" & mid(FilePath,7,lens(FilePath)-7)
else 
sub HealthCheck()
end if

Public Sub HealthCheck()
'Params & Vars
FileHP as boolean

'Movement Report & DocHeath 
DoCmd.SQL=(Add column as FileHP, boolean)
DoCmd.SQL=(select * from ard_tmp)

'Execute health check loop until end of review query results
loop (i, FileHP, i + 1)
while i < Maxof AutoID from ARD_tmp
DoCmd.Prompt= ifError(cd [TempVars].FilePath) then (SET FileHP = "FALSE") else (SET FileHP = "TRUE")
