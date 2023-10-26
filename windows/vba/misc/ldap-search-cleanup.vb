'VBA LDAPSEARCH Cleanup & Replace SCRIPT
Const ForReading = 1
Const ForWriting = 2

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile("C:\users\USERNAME\desktop\ou_search.txt", ForReading)

strText = objFile.ReadAll

objFile.Close
strNewText = Replace(strText, "member: uid=", "")
strFinText = Replace(strNewText, ",ou=users,ou=group,dc=dc", "")

Set objFile = objFSO.OpenTextFile("C:\users\USERNAME\desktop\ou_usernames.txt", ForWriting)
objFile.WriteLine strNewText
objFile.Close