Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = scriptDir

venvPythonW = scriptDir & "\.venv\Scripts\pythonw.exe"
mainScript = scriptDir & "\main.py"

If fso.FileExists(venvPythonW) Then
    WshShell.Run """" & venvPythonW & """ """ & mainScript & """", 0, False
Else
    WshShell.Run "pythonw.exe """ & mainScript & """", 0, False
End If

Set WshShell = Nothing
Set fso = Nothing
