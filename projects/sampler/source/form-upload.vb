'FORM-UPLOAD.VB
'PURPOSE: UPLOAD PDF TO BE SPLIT
Option Compare Database
Private Sub Command0_Click()
'Params
Const msoFileDialogFilePicker As Long = 3
Dim objDialog As Object
Dim PDFName As String
Dim PDFPath As TempVars

'File picker
Set PDFselect = Application.FileDialog(msoFileDialogFilePicker)
With PDFselect
    .InitialFileName = Environ("USERPROFILE") & "\Desktop\RandGen\archive\"
    .AllowMultiSelect = False
    .Show
    If .SelectedItems.Count = 0 Then
       MsgBox "No file selected."
       TempVars!PDFPath = "No PDF selected for upload."
    Else
        PDFName = .SelectedItems(1)
        'MsgBox "PDF selected:" & PDFName
        TempVars!PDFPath = PDFName
    End If
    End With
'Hold audit # and refresh display
Forms!Upload.Text2.Requery
End Sub
Private Sub Command10_Click()
'Declarations
Dim PDDoc As Acrobat.CAcroPDDoc, newPDF As Acrobat.CAcroPDDoc
Dim PDPage As Acrobat.CAcroPDPage
Dim thePDF As String, PNum As Long
Dim tmpwrkspc As String
Dim noticetype As String
Dim noticetyped As String
Dim noticecount As Integer
Dim filename As String
Dim prepfile As String
Dim prepdir As String
Dim PDFPath As TempVars
Dim NTT As TempVars

'TIMERS
Dim StartTime As Double
Dim MinutesElapsed As String
StartTime = Timer

'Initialization
If Forms!Upload.Text2.Value = "No PDF selected for upload." Then GoTo NoFileError
thePDF = TempVars!PDFPath
tmpwrkspc = Environ("USERPROFILE") & "\Desktop\RandGen\temp\"
Set PDDoc = CreateObject("AcroExch.pdDoc")
PDDoc.Open (thePDF)

'MOVEMENT STEP
'Gate, Page, & NoticeType counter
filename = PDDoc.GetFileName
PNum = PDDoc.GetNumPages
noticecount = DCount("[ID]", "Notices")
'Copy file to each temp workspace
For i = 1 To noticecount
noticetype = DLookup("[NoticeType]", "Notices", "[ID]=" & i)
FileCopy thePDF, tmpwrkspc & "notices\" & noticetype & "\" & noticetype & ".pdf"
'MsgBox noticetype & "-" & i
'MsgBox "FROM: " & thePDF & vbCrLf & "TO TEMP: " & tmpwrkspc & "notices\" & noticetype & "\" & filename
Next i
'Closure
'MsgBox "Temp setup done"
'GENERATION STEP
For x = 1 To noticecount
'DEV TEST  For x = 1 To 1
noticecount = DCount("[ID]", "Notices")
noticetyped = DLookup("[NoticeType]", "Notices", "[ID]=" & x)
'MsgBox noticetyped
prepdir = tmpwrkspc & "notices\" & noticetyped & "\"
prepfile = noticetyped & ".pdf"
TempVars!NTT = noticetyped
'MsgBox prepdir & prepfile
'Open pdf
Pause (1)
Call OpenPDF(prepdir, prepfile)
'Movemouse to run action & call close pdf
PDFActionRun
'PDF ACTION OVER

'NOTICE CHUNKER which calls randomgen
Next x
NoticeChunker

'DISPLAY ELAPSED TIME
'Determine how many seconds code took to run
  MinutesElapsed = Format((Timer - StartTime) / 86400, "hh:mm:ss")
MsgBox "COMPLETED IN: " & MinutesElapsed & " MINUTES", vbInformation
Exit Sub
ErrorHandler:
   MsgBox "Description:" & vbCrLf & Err.Description, vbCritical, "SAMPLER Error:" & Err.Number
   Exit Sub
NoFileError:
   MsgBox "NO PDF SELECTED", vbCritical, "SAMPLER Error: File"
   Exit Sub
End Sub
Private Sub Command33_Click()
'POINTER BUTTON
'Returns coordinates of mouse after button selected and then on each "ENTER" key
WHEREDICLICK
End Sub
Private Sub Command38_Click()
'TESTFUNCTION BUTTON
RandomGen (50)
'NoticeChunker
'NoticeChunker
End Sub

Private Sub Command70_Click()
GotPixel (1)
End Sub

Private Sub Form_Load()
'Checks for default temp userworkspace, creates if not found.
BuildBatcherHome
'Maybe change to delete BatcherHome on program exit? zip gen folder to desktop first?
End Sub
