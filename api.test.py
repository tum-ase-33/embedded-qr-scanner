from api import Api
 
api = Api()
 
print("#1 Send attendance with token token1234: ")
api.set_attendance("token1234", 1234)
 
print("#2 Send presentation with token token4321: ")
api.set_attendance("token4321", None)