import requests
import time
from config import ApiConfig

class Api:
	def _sendToken(self, token, tagName):
		data={'newTag': {'name': tagName, 'data': int(round(time.time() * 1000))}}
		headers={'x-pi-token': ApiConfig["pi_token"]}
		
		r = requests.post(ApiConfig["token_url"] + '/' + token, data=data, headers=headers)
		print(str(data))
		print(str(headers))
		
		return r.status_code == 200

	def set_attendance(self, token):
		return self._sendToken(token, 'attendance')
		
	def set_presentation(self, token):
		return self._sendToken(token, 'presentation')
