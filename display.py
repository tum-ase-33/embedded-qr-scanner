class Display:
	def __init__(self, lcd):
		self.lcd = lcd
		self.change_display("undefined", "undefined")
	
	def _set_variables(self, mode, status, blinking):
		if mode is not None:
			self.mode = str(mode)
		if status is not None:
			self.status = str(status)
			
		self.blinking  = blinking
	
	def change_display(self, mode, status, blinking):
		self._set_variables(mode, status, blinking)
	
		self._clear_screen()
		self._write_mode()
		self._write_status()
		self._set_blinking()
		
	def _set_blinking(self):
		if (self.blinking):
			self.lcd.blink_on()
			# disable blinking after 5 seconds
			# stop old blinking timer that blinking remains further 5 seconds
			if (self.timer is not None):
				self.timer.stop()
				self.timer = None
			
			self.timer = Timer(5.0, self._blinking_timer)
			self.timer.start()
		else:
			self.lcd.blink_off()
			
	def _blinking_timer(self):
		if self.timer is not None:
			self.lcd.blink_off()
			self.timer = None
		
	def _clear_screen(self):
		self.lcd.clear()
		
	def _write_mode(self):
		self.lcd.set_cursor(0, 0)
		self.lcd.write("Mode: " + self.mode)
		
	def _write_status(self):
		self.lcd.set_cursor(0, 1)
		self.lcd.write("Status: " + self.status)
		
	