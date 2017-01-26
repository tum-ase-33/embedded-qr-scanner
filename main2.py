import zbarlight
import pifacecad
import threading

from api import Api
from qrcode_scanner import QRCodeScanner
from display import Display

scanner = QRCodeScanner()
dbApi = Api()

print("Script started");

cad = pifacecad.PiFaceCAD()
display = Display(cad.lcd)
listener = pifacecad.SwitchEventListener(chip=cad)

def scan():
	global currentMode
	
	token = "test"
	if (token is not None and token != ''):
		if (currentMode == "attendance"):
			was_successful = dbApi.set_attendance(token)
		else:
			was_successful = dbApi.set_presentation(token)
			
		if (was_successful):
			display.change_display(currentMode, "Scanning successful", true)
			
			
		else:
			display.change_display(currentMode, "Invalid QR code")
		

def setAttendanceMode(active_pin): 
	global currentMode
	print("Attendance mode is activated");
	currentMode = "attendance"
	display.change_display(currentMode)
	
def setPresentationMode(active_pin):
	global currentMode
	print ("Presentation mode is activated")
	currentMode = "presentation"
	display.change_display(currentMode)

# threading.Timer(5.0, scan).start()
# scan()

listener.register(0, pifacecad.IODIR_FALLING_EDGE, setAttendanceMode)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, setPresentationMode)

listener.activate()

setAttendanceMode(0)
scan()
# threading.Timer(5.0, scan).start()
