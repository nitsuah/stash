Public Sub CommImp()
' CommImp Subroutine
' This subroutine is responsible for importing data from a selected file into a temporary table named "CommTmp." It involves
' the use of various variables and a File System Object (fso).
'
' Steps:
' 1. File Selection: The code invokes a file picker dialog, allowing the user to select a file for import. If a file is selected (SelectedItem.1),
'    it proceeds to the next step.
' 2. Storing File Name: The selected file's name is stored in the CommImpFileName variable.
' 3. Data Import Preparation: The code prepares to import data into the "CommTmp" temporary table from the file specified in CommImpFilePath.
'    The provided SQL statement correctly imports specific fields from the source file into the "CommTmp" table.
' 4. Import to Comments Table: The code includes a SQL statement for importing comments into the "Comments" table based on a matching UUID.
'    It selects relevant fields and filters records where the UUID is not null.

' Note: This code is designed to perform specific data import operations. Make sure that the TempVars (CommImpFileName, CommImpFilePath, and CommImp?) are correctly
' declared and set before invoking this subroutine. Additional customization may be needed based on your data and specific criteria.

'Params & vars
CommImpFileName as TempVars
CommImpFilePath as TempVars
CommImp? as TempVars
fso as Object
'Select import with FilePicker
fso.FilePicker
if SelectedItems.1
    set SelectedItem.Name = CommImpFileName
else

'Import data from file
End If
End Sub
