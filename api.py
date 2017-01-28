import requests
import time
from config import ApiConfig

class Api:
	def _sendToken(self, token, tagName, created_at):
		if created_at is None:
			created_at = int(round(time.time() * 1000))
	
		data={'tag': {'name': tagName, 'data': created_at}}
		headers={'x-pi-token': ApiConfig["pi_token"]}
		
		url = ApiConfig["token_url"].replace(':token', token)
		r = requests.post(url, data=data, headers=headers)
		
		return r.status_code == 200

	def set_attendance(self, token, created_at):
		return self._sendToken(token, 'attendance')
		
	def set_presentation(self, token, created_at):
		return self._sendToken(token, 'presentation')
