Option Compare Database

Private Sub cmdSearch_Click()
    Dim bkmk As Variant
    Dim strField As String

    Me.RecordsetClone.MoveFirst
    'Find the first record that matches what is in the search text box.
    Me.RecordsetClone.FindFirst "FLN Like " _
        & Chr(34) & "*" & Me.txtSearch & "*" & Chr(34)
            If Me.RecordsetClone.NoMatch Then
             MsgBox "Not Found"
             Else
            bkmk = Me.RecordsetClone.Bookmark
            Me.Recordset.Bookmark = bkmk
            End If
End Sub
Private Sub Command661_Click()
'Variables & Parameters
Dim xFilter As String
Dim yFilter As String
Dim zFilter As String
Dim FileName As String
Dim FormName As String
Dim FolderName As String
Dim FolderPath As String
Dim XportResp As Integer

'Hide inactives
Me.txtSearch.Visible = False
Me.ID.Visible = False

' Filter Define and File Naming
FormName = "APP_ROSTER"
'xFilter = Me.Filter
xFilter = Forms!APP_roster.Filter
yFilter = Replace(xFilter, Chr(34), "'")
        If InStr(yFilter, "'") > 0 Then
        aFilter = Trim(Split(yFilter, "'")(1))
            If InStr(yFilter, "AND") > 0 Then
                zFilter = Trim(Split(yFilter, "AND")(1))
                    If InStr(zFilter, "Is Not Null") > 0 Then
                        bFilter = "Not empty"
                        ExportFilter = aFilter & "_"
                        If InStr(zFilter, "Is Null") > 0 Then
                            bFilter = "Null"
                            ExportFilter = aFilter & "_"
                        Else
                        End If
                    Else
                        bFilter = Trim(Split(zFilter, "'")(1))
                            If Len(bFilter) > 10 Then
                            bFilter = "Multiple"
                            ExportFilter = aFilter & "_" & "Multi"
                            Else
                            ExportFilter = aFilter & "_" & bFilter
                            End If
                    End If
            Else
            bFilter = "All"
            ExportFilter = "_" & aFilter & "_" & bFilter
            If InStr(xFilter, "IN") Then
                aFilter = "Multi"
                    If InStr(yFilter, "IN") Then
                    bFilter = "Multi"
                    ExportFilter = "_" & aFilter & "_" & bFilter
                    Else
                    End If
                Else
                End If
            End If
        Else
        ExportFilter = "_All"
        End If
ExportFilter2 = Left(Replace(Replace(ExportFilter, ",", ""), " ", ""), 20)

'Export Prompt
XportResp = MsgBox("Filter1: " & aFilter & vbCrLf & "Filter2: " & bFilter & vbCrLf & "File Naming:" & vbCrLf & ExportFilter2, vbYesNo, "EXPORT FILTERS")
If XportResp = vbYes Then

'File export settings
'FolderName = Environ("USERPROFILE") & "\Desktop"
FolderName = "W:\REMORA\EXPORTS"
FileName = FormName & ExportFilter2 & "_" & Format(Date, "YYYYMMDD") & ".xls"
FolderPath = FolderName & "\" & FileName

'Export report to selected folder Path
   DoCmd.OutputTo acOutputForm, FormName, acFormatXLS, exportFile & FolderPath
  
'Export completion
   MsgBox FormName & "was exported successfully as" & FolderPath
   Shell "C:\WINDOWS\explorer.exe """ & FolderName & "", vbNormalFocus
Else
'Exit on cancel
MsgBox "View export failed for: " & FormName
End If

'Show inactives
Me.txtSearch.Visible = True
Me.ID.Visible = True
End Sub

Private Sub Form_Current()
DoCmd.Maximize
End Sub
Private Sub Form_Load()
DoCmd.Maximize
End Sub

Private Sub txtSearch_KeyPress(KeyAscii As Integer)
End Sub

