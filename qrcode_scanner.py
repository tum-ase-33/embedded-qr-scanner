import os, signal, subprocess

class QRCodeScanner:
	def scan(self):
		zbarcam=subprocess.Popen("zbarcam --raw --nodisplay /dev/video0", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
		print("zbarcam erfolgreich gestartet...")
		while True:
			qrcodetext=zbarcam.stdout.readline()
			if qrcodetext != "":
				qrcodetext = qrcodetext.decode('ascii').replace('\n', '')
				print("Got barcode: " + qrcodetext)
				print("success")
				break
		os.killpg(zbarcam.pid, signal.SIGTERM)  # Prozess stoppen
		print("zbarcam erfolgreich gestoppt")
		return qrcodetext
