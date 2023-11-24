INITIALIZER - 	G:\FOLDER\Team\User\Project\FORMS.pdf#page=1
WORKING LINK - file:///G:/FOLDER/team/user/project/FORMS.pdf#page=7

'PDF LINK CODE for DOC LINK ONCLICK EVENT
Dim varPDFPage As Variant
varPDFPage = Shell("C:\Program Files\Internet Explorer\iexplore.exe" & " " & "file:///" & [ard_loaded].[DocLink], vbNormalNoFocus)
Forms!fromAR_batcher.from[ARD_loader subform].[User ID]


'Import AR Batcher temp records into Access Request
DoCmd.OpenQuery "arb_tmp_append", acViewNormal, acEdit
'Update MaxofRefID as Ref_ID in ard_tmp
DoCmd.RunSQL "UPDATE ard_tmp SET [ard_tmp].[Ref_ID] = [ARD_loader].[MaxOfRef_ID]"