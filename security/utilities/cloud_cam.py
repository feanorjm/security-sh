from tuya_connector import TuyaOpenAPI
import requests
import base64


#   def getStartTimeofVideo():
ACCESS_ID = "pr8nrcuab2f9vycef77d"
ACCESS_KEY = "ec8261aada6e4efe8ae89a99e47aa9b5"
API_ENDPOINT = "https://openapi.tuyaus.com"
openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
conn = openapi.connect()

#   response = openapi.post("/v1.0/industry/order/card/expend", data)

payload = {'time_g_t': 1685358000,
           'time_l_t': 1685480400
           }

uid = 'az1604794105310xADPD'
#   device_id = 'eb0702544c96ce4eeeeiss'    # Outdoor cam Battery
device_id = 'ebb5dea3fab66d2a33x1gd'    # Indoor Cam

url = 'https://openapi.tuyaus.com/v1.0/users/' + uid + '/devices/' + device_id + '/storage/stream/timeline'

response = requests.get(url, params=payload)

print(response.status_code)
print(response.json())


    #   return response.status_code