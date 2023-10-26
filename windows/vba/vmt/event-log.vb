' Event Logging Process
' This section manages the logging process for changes made in a database. It utilizes TempVars to store relevant information,
' including the current date and time, the editor's username, and details about the action performed. Warnings are also disabled
' to suppress prompts. Log entries are inserted into the "Log" table.

'PARAMS & VARS
Dim ReqRef As TempVars
Dim Datetmp As TempVars
Dim Editor As TempVars
Dim CellField As TempVars
Dim IntVal As TempVars
Dim FinVal As TempVars
Dim Action As TempVars

'SET TEMPVARS
[TempVars]![Datetmp] = Now()
[TempVars]![Editor] = Environ("USERNAME")
Set TempVars!Step = "CURRENT STEP NAME"

'Action/Description
[TempVars]![Action] = "STEP: " & [TempVars]![Step] & vbCrLf & "User: " & [TempVars]![Editor] & vbCrLf & "Updated field: " & [TempVars]![CellField] & vbCrLf & "Initial Value: " & [TempVars]![IntVal] & vbCrLf & "Final Value: " & [TempVars]![FinVal] & vbCrLf & "Time: " & [TempVars]![Datetmp]
DoCmd.SetWarnings (False)
'Insert action to Request History log
DoCmd.RunSQL "INSERT into Log ([Timestamp],[Editor],[Step],[Description] VALUES ([TempVars]![Datetmp],[TempVars]![Editor],[TempVars]![Step],[TempVars]![Action])"
