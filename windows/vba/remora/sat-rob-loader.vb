'SATROBLOADER
'Load variables & parameters
Dim Filepath As String
Dim FormPath As String
Dim FormUNC As String
Dim SRtracker As Integer
Dim CompanyDD As Integer
Dim DocTypeDD As Integer
Dim CompanyTxt As String
Dim DocTypeTxt As String
Dim L5Response As Integer
Dim L6Response As Integer

'MsgBox "SR#:" & [TempVars]![SRtracker] & vbCrLf & "Company:" & [TempVars]![CompanyTxt] & vbCrLf & "System:" & [TempVars]![DocTypeTxt] & vbCrLf & "File:" & vbCrLf & [TempVars]![FilePath] & vbCrLf & "Form:" & vbCrLf & [TempVars]![FormPath] & vbCrLf
DoCmd.SetWarnings (False)

'Copy selected docs to new dir from STAGING to STORAGE
'Populate move params and create SR directory
Dim fs As Object
Dim BuiltPath As String
Dim oForm As String
Dim oFile As String
Dim nPath As TempVars
Dim nForm As TempVars
Dim nFile As TempVars

'Set Build Path and create directories
BuiltPath = "\\ntfs\ORG\TEAM\PROJECT\STAGING\" & TempVars!SRtracker & "\"
TempVars!nPath = BuiltPath

Set fs = CreateObject("Scripting.FileSystemObject")
If fs.FolderExists(BuiltPath) = False Then
    fs.CreateFolder BuiltPath
End If
Set fs = Nothing

'Copy Tracker.xlsx file to STORAGE
Set fso = CreateObject("Scripting.FileSystemObject")
    'Check to see if the file already exists in the destination folder
    If fso.FileExists([TempVars]![nPath]) Then
        'Check to see if the file is read-only
        If Not fso.GetFile([TempVars]![nPath]).Attributes And 1 Then
            'The file exists and is not read-only.  Safe to replace the file.
            fso.CopyFile [TempVars]![Filepath], [TempVars]![nPath], True
        Else
            'The file exists and is read-only.
            'Remove the read-only attribute
            fso.GetFile([TempVars]![nPath]).Attributes = fso.GetFile([TempVars]![nPath]).Attributes - 1
            'Replace the file
            fso.CopyFile [TempVars]![Filepath], [TempVars]![nPath], True
            'Reapply the read-only attribute
            fso.GetFile([TempVars]![nPath]).Attributes = fso.GetFile([TempVars]![nPath]).Attributes + 1
        End If
    Else
        'The file does not exist in the destination folder.  Safe to copy file to this folder.
        fso.CopyFile [TempVars]![Filepath], [TempVars]![nPath], True
        oFile = fso.GetFileName([TempVars]![Filepath])
    End If
Set fso = Nothing

'Copy PDF forms to STORAGE
Set fso = CreateObject("Scripting.FileSystemObject")
    'Check to see if the file already exists in the destination folder
    If fso.FileExists([TempVars]![nPath]) Then
        'Check to see if the file is read-only
        If Not fso.GetFile([TempVars]![nPath]).Attributes And 1 Then
            'The file exists and is not read-only.  Safe to replace the file.
            fso.CopyFile [TempVars]![FormPath], [TempVars]![nPath], True
        Else
            'The file exists and is read-only.
            'Remove the read-only attribute
            fso.GetFile([TempVars]![nPath]).Attributes = fso.GetFile([TempVars]![nPath]).Attributes - 1
            'Replace the file
            fso.CopyFile [TempVars]![FormPath], [TempVars]![nPath], True
            'Reapply the read-only attribute
            fso.GetFile([TempVars]![nPath]).Attributes = fso.GetFile([TempVars]![nPath]).Attributes + 1
        End If
    Else
        'The file does not exist in the destination folder.  Safe to copy file to this folder.
        fso.CopyFile [TempVars]![FormPath], [TempVars]![nPath], True
        oForm = fso.GetFileName([TempVars]![FormPath])
    End If
Set fso = Nothing
'MsgBox [TempVars]![nPath] & vbCrLf & [TempVars]![FormPath] & [TempVars]![Filepath]
'MsgBox oFile & oForm
'MsgBox [TempVars]![nPath]
TempVars![nFilepath] = [TempVars]![nPath] & oFile
TempVars![nFormpath] = [TempVars]![nPath] & oForm
'CHECK MSG MsgBox "FORM: " & [TempVars]![nFormpath] & vbCrLf & vbCrLf & "FILE:" & [TempVars]![nFilepath]

'Import tracker records into sat_upload table
DoCmd.RunSQL "INSERT into sat_upload ([SR],[FilePath],[FormPath],[Company],[Doc Type]) VALUES ([TempVars]![SRtracker],[TempVars]![nFilePath],[TempVars]![nFormPath],[TempVars]![CompanyDD],[TempVars]![DocTypeDD])"
DoCmd.SetWarnings (True)
L5Response = MsgBox("Ready to import tracker?", vbYesNo, "Load Tracker")
If L5Response = vbYes Then
DoCmd.SetWarnings (False)
DoCmd.RunSQL "DELETE FROM sat_tmp"
DoCmd.TransferSpreadsheet acImport, , "sat_tmp", [TempVars]![nFilepath], True, "tracker!"
DoCmd.RunSQL "UPDATE sat_tmp SET sat_tmp.[Company] = [TempVars]![CompanyDD] WHERE sat_tmp.[Last Name] IS NOT NULL"
DoCmd.RunSQL "UPDATE sat_tmp SET sat_tmp.[Doc Type] = [TempVars]![DocTypeDD] WHERE sat_tmp.[Last Name] IS NOT NULL"
DoCmd.RunSQL "UPDATE sat_tmp SET [sat_tmp].[Doc Name] = [TempVars]![nFormPath]"
DoCmd.RunSQL "UPDATE sat_tmp SET [sat_tmp].[Doc Date] = Date()"

'Prep tables and data for append
DoCmd.OpenQuery "sat_load", acViewNormal, acEdit
strSQL = "Alter Table sat_loaded Add Column ID AutoIncrement"
CurrentDb.Execute strSQL
strSQL = "Alter Table sat_loaded Add Constraint ID Primary Key(ID)"
CurrentDb.Execute strSQL

'Import SAT_Loaded into SATROB_users table
DoCmd.OpenQuery "sat_loader_append", acViewNormal, acEdit
DoCmd.OpenQuery "SetUserSystems", acViewNormal, acEdit

'Finish up
DoCmd.SetWarnings (True)
MsgBox "SATROB batcher generated. Click OK to review."
DoCmd.OpenForm "SAT_batcher", acViewNormal, acEdit
DoCmd.Close acForm, "sat_staging", acSaveNo
Else
MsgBox "SATROB batcher was aborted."
End If