#include "../common/helpers.au3"

Local $hWnd = open()

; Focus on tab bar
Send("{TAB 5}")
; Switch to next tab
Send("^{TAB}")
; Focus on "Bluetooth Device Name" text input field
Send("{TAB 2}")
; Set device name as "A"
Send("A")

save_and_close($hWnd)
