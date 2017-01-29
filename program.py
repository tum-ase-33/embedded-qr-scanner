import zbarlight
import pifacecad
import threading
import requests

from api import Api
from qrcode_scanner import QRCodeScanner
from display import Display

class Program:
	def __init__(self, debug):
		self.debug = debug
		self.scanner = QRCodeScanner()
		self.api = Api()
		self.cad = pifacecad.PiFaceCAD()
		self.display = Display(self.cad.lcd)
		self.previous_token = ""
		
	def start(self):
		self.listener = pifacecad.SwitchEventListener(chip=self.cad)
		self.listener.register(0, pifacecad.IODIR_FALLING_EDGE, self._set_attendance_mode)
		self.listener.register(1, pifacecad.IODIR_FALLING_EDGE, self._set_presentation_mode)
		self.listener.register(3, pifacecad.IODIR_FALLING_EDGE, self._send_offline_stored_entries)

		self.listener.activate()

		self._set_attendance_mode(0)
		self._scan()

	def _scan(self):		
		if self.debug:
			self.token = "test"
		else:
			self.token = str(self.scanner.scan())
		
		if (self.token is not None and self.token != '' and self.previous_token != self.token):
			try:
				if (self.mode == "attendance"):
					was_successful = self.api.set_attendance(self.token, None)
				else:
					was_successful = self.api.set_presentation(self.token, None)
				was_successful = self.debug or was_successful
				
				if (was_successful):
					self.display.change_display(self.mode, "Scanning successful", True)
					self.previous_token = self.token
					os.system("omxplayer sounds/accepted.mp3")
				else:
					self.display.change_display(self.mode, "Invalid QR code", False)
					os.system("omxplayer sounds/denied.mp3")
			except requests.ConnectionError:
				print("No internet connection available.")
				self.store.store(self.mode, self.token)
				
		if self.debug is None or self.debug is False:
			self._scan()
			
	def _change_pending_display(self):
		self.display.change_display(self.mode, "Pending", False)

	def _set_attendance_mode(self, active_pin): 
		print("Attendance mode is activated");
		
		self.mode = "attendance"
		self._change_pending_display()
		
	def _set_presentation_mode(self, active_pin):
		print ("Presentation mode is activated")
		
		self.mode = "presentation"
		self._change_pending_display()
		
	def _send_offline_stored_entries(self):
		self.display.change_display("Offline storage", "Uploading...", False)
		try:
			entries = self.store.getAll()
			for entry in entries:
				self.store(entry[0], entry[1], entry[2])
			self.display.change_display("Offline storage", "Success", True)
		except requests.ConnectionError:
			self.display.change_display("Failure", "No internet connection", False)
		
		threading.timer(5.0, self._change_pending_display).start()
