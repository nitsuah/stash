'FORM-CALIBRATION.VB
'PURPOSE: CALIBRATION FOR AUTOCLICKER & ADOBE ACROBAT
Option Compare Database

Private Sub Command54_Click()
PDFFS
End Sub

Private Sub Command57_Click()
SEQUSET
End Sub

Private Sub Form_Load()
NewCalibration
ResetCalibrate
End Sub
Public Function OnCalibrate()
'PARAMS & VARS
Dim Datetmp As TempVars
Dim Editor As TempVars
Dim Step As TempVars
Dim Action As TempVars

'Store value of current TempVars
[TempVars]![Datetmp] = Now()
[TempVars]![Editor] = Environ("USERNAME")
[TempVars]![Step] = "STEP1"


DoCmd.RunSQL "INSERT into Calibre([Editor]) VALUES ([TempVars]![Editor])"
'Gate check to compare values before action
'If ([TempVars]![ComTxtIntVal] = [TempVars]![ComTxtFinVal]) Then
'Exit Sub
'Else
'End If

'Action/Description
[TempVars]![Action] = "CALIBRATION LOG" & "User: " & [TempVars]![Editor] & vbCrLf & "STEP: " & [TempVars]![Step] & vbCrLf & "Time: " & [TempVars]![Datetmp]
'Message prompt
Dim RdyCalibrate As Integer
RdyCalibrate = MsgBox("CALIBRATION" & [TempVars]![Step] & "?", vbYesNo, "CALIBRATION")
If RdyCalibrate = vbYes Then
DoCmd.SetWarnings (False)
'Insert action to Calibration log
DoCmd.RunSQL "INSERT into Log([Timestamp],[Editor],[Step],[Description]) VALUES ([TempVars]![Datetmp],[TempVars]![Editor],[TempVars]![Step],[TempVars]![Action])"
'Update field & refresh form
If Me.Dirty Then
  Me.Dirty = False
End If
DoCmd.SetWarnings (True)
'Action summary
MsgBox [TempVars]![Action]
Else
'add exitto on error w/ failure calibre entry

End If
End Function
