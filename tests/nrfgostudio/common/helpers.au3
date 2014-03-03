#include <Constants.au3>

Func open()
    Local $outdir = EnvGet("OUTDIR")
    If $outdir = "" Then
        MsgBox($MB_OK, "Error", "OUTDIR environment variable not defined")
        Exit(1)
    EndIf

    Run("C:\Program Files\Nordic Semiconductor\nRFgo Studio\nRFgoStudio.exe", $outdir)
    Local $hWnd = WinWaitActive("nRFgo Studio")

    Send("!fn{ENTER}")
    Sleep(500)

    Return $hWnd
EndFunc

Func save_and_close($hWnd)
    Send("^s")
    WinWaitActive("Save Profile")
    Send("services.xml{ENTER}")
    WinClose($hWnd)
EndFunc
