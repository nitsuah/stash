'MOUSE-MOVE.VB
'PURPOSE: MOUSE MOVEMENTS FOR SAMPLER
Option Compare Database
'LOAD PTR-SAFE 32bit Functions
Public Declare PtrSafe Function SetCursorPos Lib "user32" (ByVal x As Long, ByVal y As Long) As Long
Public Declare PtrSafe Function GetCursorPos Lib "user32" (lpPoint As POINTAPI) As Long
Private Declare PtrSafe Function GetPixel Lib "gdi32" (ByVal hdc As Long, ByVal x As Long, ByVal y As Long) As Long
Private Declare PtrSafe Function GetWindowDC Lib "user32" (ByVal hwnd As Long) As Long
' Create custom variable that holds two integers
Type POINTAPI
   Xcoord As Long
   Ycoord As Long
End Type
Public Declare PtrSafe Sub mouse_event Lib "user32" (ByVal dwFlags As Long, ByVal dx As Long, ByVal dy As Long, ByVal cButtons As Long, ByVal dwExtraInfo As Long)
Const MOUSEEVENTF_LEFTDOWN = &H2
Const MOUSEEVENTF_LEFTUP = &H4
Const MOUSEEVENTF_RIGHTDOWN As Long = &H8
Const MOUSEEVENTF_RIGHTUP As Long = &H10
'GENERATION - PDF MOUSE EVENTS
Public Sub ActionBtn()
  SetCursorPos 380, 60 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub StartBtn()
  SetCursorPos 1714, 222 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub OKBtn()
  SetCursorPos 826, 659 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub CloseBtn()
  SetCursorPos 1893, 8 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub ExitBtn()
  SetCursorPos 1893, 8 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub

Public Sub SearchTxt()
  SetCursorPos 1797, 353 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub ClickCurr()
  SetCursorPos 905, 390 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub ClickRmv()
  SetCursorPos 1083, 360 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub ClickTxt()
  SetCursorPos 905, 326 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub AddTxt()
  SetCursorPos 1087, 321 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub ClickOk()
  SetCursorPos 987, 760 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub SingleClick()
  SetCursorPos 100, 100 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub DoubleClick()
  'Double click as a quick series of two clicks
  SetCursorPos 100, 100 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub RightClick()
  'Right click
  SetCursorPos 200, 200 'x and y position
  mouse_event MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0
End Sub
Public Sub FinActBtn()
  SetCursorPos 1150, 580 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Public Sub AddActBtn()
  SetCursorPos 1055, 570 'x and y position
  mouse_event MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0
  mouse_event MOUSEEVENTF_LEFTUP, 0, 0, 0, 0
End Sub
Sub WHEREDICLICK()
Dim llCoord As POINTAPI
' Get the cursor positions
GetCursorPos llCoord
' Display the cursor position coordinates
MsgBox "X Position: " & llCoord.Xcoord & vbNewLine & "Y Position: " & llCoord.Ycoord
End Sub
Public Function Pause(NumberOfSeconds As Variant)
    On Error GoTo Error_GoTo
    DoCmd.Hourglass (True)
    Dim PauseTime As Variant
    Dim Start As Variant
    Dim Elapsed As Variant
    
    PauseTime = NumberOfSeconds
    Start = Timer
    Elapsed = 0
    Do While Timer < Start + PauseTime
        Elapsed = Elapsed + 1
        If Timer = 0 Then
            ' Crossing midnight
            PauseTime = PauseTime - Elapsed
            Start = 0
            Elapsed = 0
        End If
        DoEvents
    Loop
    DoCmd.Hourglass (False)
Exit_GoTo:
    On Error GoTo 0
    DoCmd.Hourglass (False)
    Exit Function
Error_GoTo:
    Debug.Print Err.Number, Err.Description, Erl
    DoCmd.Hourglass (False)
    GoTo Exit_GoTo
End Function
Public Function TypeNotice()
Dim ntp As String
Dim nt1 As String
Dim nt2 As String
Dim nt3 As String
Dim nt4 As String
ntp = TempVars!NTT
'MsgBox TempVars!NTT
nt1 = Left(ntp, 1)
nt2 = Mid(ntp, 2, 1)
nt3 = Mid(ntp, 3, 1)
nt4 = Right(ntp, 1)
'MsgBox nt1 & " " & nt2 & " " & nt3 & " " & nt4
SendKeys (nt1)
SendKeys (nt2)
SendKeys (nt3)
SendKeys (nt4)
End Function
Public Function PDFActionRun()
Pause (1.5)
DoCmd.Hourglass (False)
ActionBtn
Pause (1)
DoCmd.Hourglass (False)
UpdateST

'Add modifiers for larger notices
Dim BigMod As Integer
Dim SmallMod As Integer
BigMod = 0
SmallMod = 0

'Set extra delay modifier to WG30 OR WG32 process
If TempVars!NTT = "WG30" Then BigMod = "30"
If TempVars!NTT = "WG30" Then SmallMod = "5"
If TempVars!NTT = "WG32" Then BigMod = "40"
If TempVars!NTT = "WG32" Then SmallMod = "5"

'Add detection method for early finish
Pause (BigMod)
Pause (30)
Pause (SmallMod)
DoCmd.Hourglass (False)
StartBtn
Pause (6)
DoCmd.Hourglass (False)
Pause (SmallMod)
OKBtn
Pause (6)
DoCmd.Hourglass (False)
CloseBtn
Pause (1)
DoCmd.Hourglass (False)
ExitBtn
End Function
Public Function OpenFWS(strAddress As String)
Dim shell As Object
Dim result As Long
Dim acrbtdir As String
Dim pgmode As String
Dim filedir As String
Dim strFILE As String
'Dim strAddress As String
Set shell = CreateObject("WScript.shell")
acrbtdir = "C:\Program Files (x86)\Adobe\Acrobat 11.0\Acrobat\Acrobat.exe"
strFILE = Chr(34) & acrbtdir & Chr(34) & " " & Chr(34) & strAddress & Chr(34)
'MsgBox (strFILE)
result = shell.Run(strFILE, 0, False)
End Function
Public Function UpdateST()
'Updates search text value based upon TypeNotice function
SearchTxt
Pause (0.5)
ClickCurr
Pause (0.5)
ClickRmv
Pause (0.5)
ClickTxt
Pause (0.5)
TypeNotice
Pause (0.5)
AddTxt
Pause (0.5)
ClickOk
Pause (0.5)
'delay?
End Function
'RANDOM INSERT FUNCTION
Public Function RandomGen(maxpgct As Integer)
'PARMS & VARS
Dim samplesize As Integer
Dim MaxPgs As Integer
Dim n As Integer
Dim randompg As Integer
Dim currRec As Integer
'Cleanup prior rands

DoCmd.SetWarnings False
DoCmd.OpenQuery "randrefresh", acViewNormal, acEdit
DoCmd.OpenQuery "randrefresh", acViewNormal, acEdit
DoCmd.OpenQuery "randrefresh", acViewNormal, acEdit
DoCmd.SetWarnings True
'Get notice type, page counts, doc paths on each loop (maybe store name as well?)
MaxPgs = maxpgct
samplesize = 30
currRec = 1
'Sample size check and set
If MaxPgs < samplesize Then n = MaxPgs Else n = samplesize
If (n = MaxPgs) Then
'MsgBox "sample too small"
'Small RandomSampler function
'set notice extract type to small
'else set notice extract type to big for notice
'RANDOM INT GEN
For n = 1 To n
randompg = Int((MaxPgs * Rnd) + 1)
If (randompg = currRec) Then
randompg = Int((MaxPgs * Rnd) + 1)
End If
'check if # is = previous in table
FindMatchingValue (randompg)

'Do insert to random table once done, referencial integrity should keep items unqiue, will need to control for non-unqiue items with exit command to re-loop with #-1?)
DoCmd.SetWarnings False
DoCmd.RunSQL "Update RandInts set Page=" & randompg & " where ID=" & n
DoCmd.SetWarnings True
'MsgBox "#" & currRec & vbNewLine & "Page=" & randompg
Next n
'Build out PrintPath to include all values in table up to samplesize, then call file export for each pathing.
'MsgBox "Random selection created"

'Split loop
For S = 0 To TempVars!Noticepgct - 1
    Set newPDF = CreateObject("AcroExch.pdDoc")
    newPDF.Create
    NewName = nPath & noticetype & "_pg_" & (S + 1) & ".pdf"
    newPDF.InsertPages -1, PDDoc, i, 1, 0
    newPDF.Save 1, NewName
    newPDF.Close
    'Set newPDF = Nothing
    'Loop to next page
Next S
    'Loop to next notice type
'Next z

Exit Function
End If

End Function

Sub FindMatchingValue(intValueToFind As Integer)
   Dim samechk As String
   Dim z As String
   Dim currRec As Integer
  'MsgBox "looking for:" & intValueToFind
        samechk = DLookup("[Page]", "RandInts", "[Page]")
        z = samechk
        If intValueToFind = z Then
            'MsgBox ("Found" & intValueToFind & "value on row " & z)
            Exit Sub
            Else: End If
            currRec = currRec + 1
    ' This MsgBox will only show if the loop completes with no success
    'MsgBox ("Value not found in the range!")
End Sub

Public Function BuildBatcherHome()
'SETUP BATCHER_HOME
'PARMS & VARS
Dim fsz As Object
Dim bpz As String
Dim fs1 As Object
Dim bp1 As String
Dim bp2 As String
Dim tmpwrkspc As String
Dim appdir As String
Dim sampsetfile As String
Dim sampsetsequ As String
Dim setupdir As String

'SETUP INITIAL DIRECTORIES
gdrive = "G:\Public Folder\Austin\RandGen\setup\"
appdir = Environ("USERPROFILE") & "\Desktop\RandGen\"
tmpwrkspc = Environ("USERPROFILE") & "\Desktop\RandGen\temp\"
setupdir = Environ("USERPROFILE") & "\Desktop\RandGen\setup\"
sampsetfile = gdrive & "test_sample.pdf"
samplesequ = gdrive & "SAMPLER_MK2.sequ"
finsetfile = setupdir & "test.pdf"
finsetsequ = setupdir & "SAMPLER_MK2.sequ"

'INITIAL DIR CHECK CASE
For w = 1 To 6
'MsgBox w
Select Case w
Case 1
    bpz = appdir
Case 2
    bpz = tmpwrkspc
Case 3
    bpz = tmpwrkspc & "notices\"
Case 4
    bpz = appdir & "archive\"
Case 5
    bpz = appdir & "setup\"
Case 6
    bpz = appdir & "gen\"
End Select
'MsgBox bpz
Set fsz = CreateObject("Scripting.FileSystemObject")
If fsz.FolderExists(bpz) = False Then
    fsz.Createfolder bpz
End If
Set fsz = Nothing
Next w

'BuildBatcherHome temp directory
Dim ntcfldct As Integer
Dim noticefolder As String
'SETUP INITIAL DIRECTORIES
ntcfldct = DCount("[ID]", "Notices")

'NOTICE FOLDER BUILD LOOP
For b = 1 To ntcfldct
'DEV TEST  For b = 1 To 1
noticefolder = DLookup("[NoticeType]", "Notices", "[ID]=" & b)
'BUILD NOTICE FOLDER
bp1 = tmpwrkspc & "notices\" & noticefolder & "\"
bp2 = tmpwrkspc & "notices\" & noticefolder & "\split"
Set fs1 = CreateObject("Scripting.FileSystemObject")
If fs1.FolderExists(bp1) = False Then
    fs1.Createfolder bp1
    fs1.Createfolder bp2
End If
Set fs1 = Nothing
Next b
'MsgBox "FINISHED TEMP BUILD"
'COPY SAMPLE FILES FROM G:\public\austin
FileCopy sampsetfile, finsetfile
FileCopy samplesequ, finsetsequ

End Function

Public Function NoticeChunker()

'NOTICE CHUNKER
'PARAMS & VARS
Dim fs As Object
Dim BuiltPath As String
Dim GenPath As String
Dim oFile As String
Dim oFilename As String
Dim nPath As String
Dim nForm As String
Dim nFile As String
Dim noticetype As String
Dim Noticepgct As TempVars
Dim tmpwrkspc As String
Dim NT As Integer

tmpwrkspc = Environ("USERPROFILE") & "\Desktop\RandGen\temp\"
'start loop per each notice type
notice_type_ct = DCount("[ID]", "Notices")
For z = 1 To notice_type_ct
noticetype = DLookup("[NoticeType]", "Notices", "[ID]=" & z)

'SETUP
oFilename = noticetype & "_extracted.pdf"
BuiltPath = tmpwrkspc & "notices\" & noticetype & "\"
oFile = BuiltPath & oFilename
nPath = Environ("USERPROFILE") & "\Desktop\RandGen\temp\notices\" & noticetype & "\split\"
nForm = noticetype & "_extracted.pdf"
nFile = nPath & nForm
'MsgBox oFile
Set fs = CreateObject("Scripting.FileSystemObject")
If fs.FolderExists(BuiltPath) = False Then
    fs.Createfolder BuiltPath
End If
Set fs = Nothing

'DOCSPLITTER
'Declarations
Dim PDDoc As Acrobat.CAcroPDDoc, newPDF As Acrobat.CAcroPDDoc
Dim PDPage As Acrobat.CAcroPDPage
Dim thePDF As String, PNum As Long


'Initialization
Set PDDoc = CreateObject("AcroExch.pdDoc")
thePDF = oFile
'MsgBox "Split extract? File name:" & thePDF
result = PDDoc.Open(thePDF)
If Not result Then Exit Function
'Page counter
PNum = PDDoc.GetNumPages
TempVars!Noticepgct = PNum
TempVars!noticetype = noticetype
'Run RandomGen using updated noticepgct
'MsgBox "TOTAL COUNT: " & TempVars!Noticepgct & "pages"
RandomGen (TempVars!Noticepgct)
Next z
'Combine loop - combine all _pg_#.pdfs into one document named after noticetype

'Move loop, move all finished docs to Gen folder (nPath)

'Closure
End Function
Public Function OpenPDF(Folder, File)
'Folder path cleanup
Dim strAddress As String
strAddress = Nz(Folder)
strAddress = strAddress & IIf(strAddress = "", "", "") & Nz(File)
strAddress = strAddress & IIf(strAddress = "", "", "")
If strAddress = "No PDF selected for upload." Then GoTo NoFileError
'WORKING PDF OPEN coverted to OpenFWS function
'shell "C:\Program Files (x86)\Adobe\Acrobat 11.0\Acrobat\Acrobat.exe" & " " & strAddress, vbMaximizedFocus
'TEST OF OpenFileWithShell mk2
'strAddress = Environ("USERPROFILE") & "\Desktop\RandGen\temp\notices\CB01\CB01.pdf"
'MsgBox strAddress & vbNewLine & Environ("USERPROFILE") & "\Desktop\RandGen\temp\notices\CB01\CB01.pdf"
'MsgBox strAddress, vbYesNo
OpenFWS (strAddress)
Exit Function
NoFileError:
   MsgBox "NO PDF SELECTED", vbCritical, "SAMPLER Error: File"
End Function
Public Function NewCalibration()
'PARAMS & VARS
Dim Editor As TempVars
[TempVars]![Editor] = Environ("USERNAME")
DoCmd.SetWarnings (False)
DoCmd.RunSQL "INSERT into Calibre([Editor]) VALUES ([TempVars]![Editor])"
Forms!Calibre.Editor.Requery
DoCmd.SetWarnings (True)
If Warnings Then MsgBox "Exists" Else Exit Function
End Function
Public Function PDFFS()
Dim testfile As String
Dim testdir As String
testfile = "test.pdf"
testdir = Environ("USERPROFILE") & "\Desktop\RandGen\setup\"
Call OpenPDF(testdir, testfile)
End Function
Public Function SEQUSET()
Dim sequfile As String
Dim sequdir As String
testfile = "SAMPLER_MK2.sequ"
testdir = Environ("USERPROFILE") & "\Desktop\RandGen\setup\"
Call OpenPDF(testdir, testfile)
Pause (1.5)
AddActBtn
Pause (1.5)
AddActBtn
Pause (1.5)
FinActBtn

End Function
Public Function ResetCalibrate()
Dim fststep As Integer
Dim scndstep As Integer
Dim thrdstep As Integer
Dim totalcalibre As Integer
Dim RECAL As Integer

fststep = DCount("[Step1]", "Calibre")
scndstep = DCount("[Step2]", "Calibre")
thrdstep = DCount("[Step3]", "Calibre")
totalcalibre = (fststep + scndstep + thrdstep)
'MsgBox totalcalibre
If totalcalibre < 3 Then
DoCmd.SetWarnings (False)
DoCmd.RunSQL "UPDATE Calibre SET Step1='0',Step2='0',Step3='0' WHERE [Calibre].[Editor]=[TempVars]![Editor]"
DoCmd.SetWarnings (True)
Else: RECAL = MsgBox("User already calibrated, do you want to re-calibrate?", vbYesNo, "CALIBRATE")
If RECAL = vbYes Then
DoCmd.SetWarnings (False)
DoCmd.RunSQL "UPDATE Calibre SET Step1='0',Step2='0',Step3='0' WHERE [Calibre].[Editor]=[TempVars]![Editor]"
DoCmd.SetWarnings (True)
Else
MsgBox "User will not be recalibrated"
End If
End If
End Function
Public Function GotPixel(seconds As Integer)
    Dim tPOS As POINTAPI
    Dim sTmp As String
    Dim pxrgb As Long
    Dim lDC As Long
    Dim PIXELRGB As String
        MaxTime = seconds
    For time1 = 0 To MaxTime
    wDC = GetWindowDC(0)
    Call GetCursorPos(tPOS)
    pxrgb = GetPixel(wDC, tPOS.Xcoord, tPOS.Ycoord)
    'Label2.BackColor = pxrgb
    sTmp = Right$("000000" & Hex(pxrgb), 6)
    PIXELRGB = ("#" & Right$(sTmp, 2) & "" & Mid$(sTmp, 3, 2) & "" & Left$(sTmp, 2))
    Next time1
    MsgBox "LOC: " & tPOS.Xcoord & ", " & tPOS.Ycoord & vbNewLine & "PIX: " & PIXELRGB
End Function
