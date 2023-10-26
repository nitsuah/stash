Private Sub Status_OnClick (Cancel As Integer)
'PARAMS & VARS
Dim CellField as TempVars
Dim IntVal as TempVars
'Set values during OnClick
[TempVars]![CellField] = getField(Name)
[TempVars]![IntVal] = getField(Value)
End Sub

Private Sub Status_BeforeUpdate(Cancel As Integer)
'PARAMS & VARS
'Store value of Request Item# -- from ITEM CONTROL
Dim ReqReftmp as TempVars

'Get username of active editor -- from GetLoggedOnUser
Dim Editor as TempVars

'Set Values during Before update
[TempVars]![ReqReftmp] = Form!Requests!Subform!ReqSide.[Item]
    [TempVars]![Editor] =
        k
End Sub

Private Sub Status_AfterUpdate(Cancel As Integer)
'PARAMS & VARS
Dim FinVal as TempVars
Dim Description as TempVars
'Store value of current timestamp -- from CurDate
Dim Datetmp as TempVars

'Storage of final action description
[TempVars]![Datetmp] = GetCurrDate()
[TempVars]![Description] = Editor & "modified the " & CellField & " field from " & IntVal & "to" & FinVal & "on " & Datetmp

'Insert action to Request History log
DoCmd.RunSQL "INSERT into ReqLog ([ReqRef],[Timestamp],[Editor],[Field],[IntVal],[FinVal],[Description]) VALUES ([TempVars]![ReqRef],[TempVars]![Datetmp],[TempVars]![Editor],[TempVars]![Field],[TempVars]![IntVal],[TempVars]![FinVal],[TempVars]![Description])"

End Sub