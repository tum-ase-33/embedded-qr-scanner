import requests
import time
from config import ApiConfig
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class Api:
	def _sendToken(self, token, tagName, created_at):
		if created_at is None:
			created_at = int(round(time.time() * 1000))
	
		data={'tag': {'name': tagName, 'data': created_at}}
		headers={'x-scanner-client-token': ApiConfig["pi_token"]}
		
		url = ApiConfig["token_url"].replace(':token', token)
		r = requests.post(url, data=data, headers=headers)
		print(url)
		print(str(r))
		print(str(headers))		
		return r.status_code == 200

	def set_attendance(self, token, created_at):
		return self._sendToken(token, 'attendance', created_at)
		
	def set_presentation(self, token, created_at):
		return self._sendToken(token, 'presentation', created_at)
