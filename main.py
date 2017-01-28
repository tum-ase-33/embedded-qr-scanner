import zbarlight
import pifacecad
import threading

from api import Api
from qrcode_scanner import QRCodeScanner
from display import Display
from localstorage import LocalStorage

store = LocalStorage()
scanner = QRCodeScanner()
dbApi = Api()

print("Script started");

cad = pifacecad.PiFaceCAD()
display = Display(cad.lcd)
listener = pifacecad.SwitchEventListener(chip=cad)

def store(mode, token, created_at):
	if (mode == "attendance"):
		was_successful = dbApi.set_attendance(token, created_at)
	else:
		was_successful = dbApi.set_presentation(token, created_at)
	return was_successful

previous_token = ''
def scan():
	global currentMode, previous_token
	
	token = str(scanner.scan().decode("utf-8"))
	if (token is not None and token != '' and token != previous_token):
		try:
			was_successful = store(currentMode, token, None)
				
			if (was_successful):
				display.change_display(currentMode, "Scanning successful", true)
		except requests.ConnectionError:
			print("No internet connection available.")
			store.store(currentMode, token)
			
		else:
			display.change_display(currentMode, "Invalid QR code")
			
	# and restart scanning process for other qr codes again
	scan()
	
		

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
	
def restore_display():
	display.change_display(currentMode)
	
def sendOfflineStoredEntries():
	display.change_display("Offline storage", "Uploading...", False)
	try:
		entries = store.getAll()
		for entry in entries:
			store(entry[0], entry[1], entry[2])
		display.change_display("Offline storage", "Success", True)
	except requests.ConnectionError:
		display.change_display("Failure", "No internet connection", False)
	threading.timer(5.0, restore_display).start()
		

listener.register(0, pifacecad.IODIR_FALLING_EDGE, setAttendanceMode)
listener.register(1, pifacecad.IODIR_FALLING_EDGE, setPresentationMode)
listener.register(3, pifacecad.IODIR_FALLING_EDGE, sendOfflineStoredEntries)

listener.activate()

setAttendanceMode(0)
scan()
