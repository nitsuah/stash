Private Sub Command130_Click()
'Load variables & params
Dim Filepath As String
Dim FormPath As String
Dim FormUNC As String
Dim SRtracker As Integer
Dim CompanyDD As Integer
Dim SystemDD As Integer
Dim CompanyTxt As String
Dim SystemTxt As String
Dim L5Response As Integer
Dim L6Response As Integer
Dim L9Response As Integer

'MsgBox "SR#:" & [TempVars]![SRtracker] & vbCrLf & "Company:" & [TempVars]![CompanyTxt] & vbCrLf & "System:" & [TempVars]![SystemTxt] & vbCrLf & "File:" & vbCrLf & [TempVars]![FilePath] & vbCrLf & "Form:" & vbCrLf & [TempVars]![FormPath] & vbCrLf
DoCmd.SetWarnings (False)

'Populate move params
Dim fs As Object
Dim BuiltPath As String
Dim oForm As String
Dim oFile As String
Dim nPath As TempVars
Dim nForm As TempVars
Dim nFile As TempVars


'Set Build Path and create directories
BuiltPath = "\\ntfs\ORG\TEAM\PROJECT\STORAGE\" & TempVars!SRtracker & "\"
TempVars!nPath = BuiltPath

Set fs = CreateObject("Scripting.FileSystemObject")
If fs.FolderExists(BuiltPath) = False Then
    fs.CreateFolder BuiltPath
End If
Set fs = Nothing

'Copy selected docs to STORAGE for splitting

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
        TempVars!nForm = fso.GetBaseName([TempVars]![FormPath])
        oForm = fso.GetFileName([TempVars]![FormPath])
        TempVars![nFilepath] = [TempVars]![nPath] & oFile
        TempVars![nFormpath] = [TempVars]![nPath] & oForm
        'MsgBox "FORM PATH: " & [TempVars]![nFormpath] & vbCrLf & "FORM NAME:" & TempVars!nForm
    End If
Set fso = Nothing

'Import tracker records into AR_upload table
DoCmd.RunSQL "INSERT into AR_upload ([SR],[FilePath],[FormPath],[Company],[System]) VALUES ([TempVars]![SRtracker],[TempVars]![nFilePath],[TempVars]![nFormPath],[TempVars]![CompanyDD],[TempVars]![SystemDD])"
DoCmd.SetWarnings (True)
L5Response = MsgBox("Ready to import Tracker?", vbYesNo, "Load Tracker")
If L5Response = vbYes Then
DoCmd.SetWarnings (False)
DoCmd.RunSQL "DELETE FROM arb_tmp"
DoCmd.TransferSpreadsheet acImport, , "arb_tmp", [TempVars]![nFilepath], True, "tracker!"
DoCmd.RunSQL "UPDATE arb_tmp SET arb_tmp.company = [TempVars]![CompanyDD] WHERE arb_tmp.[Last Name] IS NOT NULL"
DoCmd.RunSQL "UPDATE arb_tmp SET arb_tmp.system = [TempVars]![SystemDD] WHERE arb_tmp.[Last Name] IS NOT NULL"

'Import AR Batcher temp records into Access Request
DoCmd.OpenQuery "arb_tmp_append", acViewNormal, acEdit
DoCmd.OpenQuery "SetUserSystems", acViewNormal, acEdit
DoCmd.RunSQL "DELETE FROM ard_tmp"
DoCmd.RunSQL "INSERT into ard_tmp ([User ID],[Worker Last Name],[Worker First Name]) SELECT [Username], [Last Name], [First Name] FROM arb_tmp"
DoCmd.RunSQL "UPDATE ard_tmp SET [ard_tmp].[DateAdded] = Date()"
DoCmd.Close acForm, "AR_batcher", acSaveNo
DoCmd.Close acTable, "ard_tmp", acSaveYes
DoCmd.Close acTable, "ard_load", acSaveNo
DoCmd.Close acTable, "ard_loaded", acSaveNo
DoCmd.OpenQuery "ard_load", acViewNormal, acEdit
DoCmd.Close acTable, "ARD_loaded", acSaveYes
Dim strSQL As String
strSQL = "Alter Table ARD_loaded Add Column ID AutoIncrement"
CurrentDb.Execute strSQL
strSQL = "Alter Table ARD_loaded Add Constraint ID Primary Key(ID)"
CurrentDb.Execute strSQL
DoCmd.RunSQL "UPDATE ARD_loaded SET [ARD_loaded].[DocPath] = [TempVars]![nForm] & '_pg_' & [ARD_loaded].[ID] & '.pdf'"



'DOCSPLITTER - Split docs in TempVars!nPath
'Declarations
Dim PDDoc As Acrobat.CAcroPDDoc, newPDF As Acrobat.CAcroPDDoc
Dim PDPage As Acrobat.CAcroPDPage
Dim thePDF As String, PNum As Long

'Initialization
Set PDDoc = CreateObject("AcroExch.pdDoc")
thePDF = TempVars![nFormpath]
'MsgBox "Ready file for split:" & "Form Name:" & TempVars![nForm]
Result = PDDoc.Open(thePDF)
If Not Result Then
   MsgBox "Can't open file: " & thePDF
   Exit Sub
End If

'Gate & Page counter
PNum = PDDoc.GetNumPages
L9Response = MsgBox("Pages ready for split: " & PNum & "pages", vbYesNo, "PDF Splitter")
If L9Response = vbYes Then

'Split loop
For i = 0 To PNum - 1
    Set newPDF = CreateObject("AcroExch.pdDoc")
    newPDF.Create
    NewName = [TempVars]![nPath] & [TempVars]![nForm] & "_pg_" & i & ".pdf"
        newPDF.InsertPages -1, PDDoc, i, 1, 0
    newPDF.Save 1, NewName
    newPDF.Close
    'Set newPDF = Nothing
Next i
'Closure
MsgBox "PDF was split into " & PNum & " pages"
Else
MsgBox "PDF split failed"
End If

'E-FOLDER MOVEMENT
'Vars & Parms
Dim eFile As Variant
Dim eFolder As Variant
Dim L10Response As Integer
Dim fsc As Object
Set fsc = VBA.CreateObject("Scripting.FileSystemObject")

'Prep
L10Response = MsgBox("Pages ready to be moved:" & PNum & "pages", vbYesNo, "PDF Splitter")
If L10Response = vbYes Then
'Start Loop
For i = 1 To PNum
        eFolder = DLookup("[e-folder]", "ARD_loader", "[ID] = " & i)
        eFile = DLookup("[DocPath]", "ARD_loader", "[ID] = " & i)
        MsgBox "Coping file #" & PNum & "to:" & eFolder & eFile
        'Call fsc.CopyFile([TempVars]![nPath] & [TempVars]![nForm] & "_pg_" & (PNum + 1) & ".pdf", eFolder & eFile)
Next i
'End Loop
MsgBox PNum & "PDF's have been moved to e-folders"
Else
MsgBox "PDF move failed, please retry."
End If
Set fso = Nothing

'Import ARD into Documents table
DoCmd.OpenQuery "ard_loader_append", acViewNormal, acEdit
DoCmd.SetWarnings (True)
MsgBox "All tables generated. Click OK to review."
DoCmd.Close acForm, "AR_staging", acSaveNo
DoCmd.OpenForm "AR_batcher", acViewNormal, acEdit
Else
MsgBox "AR Batcher was aborted."
End If
End Sub