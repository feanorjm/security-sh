from tuya_connector import TuyaOpenAPI
import requests


def create_order(data):
    ACCESS_ID = "pr8nrcuab2f9vycef77d"
    ACCESS_KEY = "ec8261aada6e4efe8ae89a99e47aa9b5"
    API_ENDPOINT = "https://openapi.tuyaus.com"
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    conn = openapi.connect()

    response = openapi.post("/v1.0/industry/order/card/expend", data)
    return response


def create_order2(data):
    response = requests.post('http://35.208.29.226/create_order/', data)
    print(response.json())

    return response.json()


# data = {}
# data["order_id"] = 521
# data["tuya_uid"] = "az1651120192974P"
# data["home_id"] = "697701"
# data["commodity_code"] = "ECbahf9ym6zh"
# data["device_id"] = "pp0190707fb723df21"
# data["pay_id"] = "pago_septiembre_2022"
# create_order(data)


def get_devices_uid(uid):
    ACCESS_ID = "5praja9pqkn8a8x9jc9c"
    ACCESS_KEY = "sj34f75qdhymj8xrxpjtvd8uswarwmd8"
    API_ENDPOINT = "https://openapi.tuyaus.com"
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    conn = openapi.connect()

    url = "/v1.0/users/" + uid + "/devices"
    data = {}

    response = openapi.get(url, data)

    print(response)
    return response


def get_device(id):
    ACCESS_ID = "5praja9pqkn8a8x9jc9c"
    ACCESS_KEY = "sj34f75qdhymj8xrxpjtvd8uswarwmd8"
    API_ENDPOINT = "https://openapi.tuyaus.com"
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    conn = openapi.connect()

    url = "/v1.0/devices/" + id
    data = {}

    response = openapi.get(url, data)

    print(response)
    return response


def get_devices(uid):
    # ACCESS_ID = "5praja9pqkn8a8x9jc9c"
    # ACCESS_KEY = "sj34f75qdhymj8xrxpjtvd8uswarwmd8"
    # API_ENDPOINT = "https://openapi.tuyaus.com"
    # openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    # conn = openapi.connect()
    #
    # url = "/v1.0/users/" + uid + "/devices"
    # data = {}
    #
    # response = openapi.get(url, data)
    response = requests.get('http://35.208.29.226/get_devices?uid=' + uid)

    return response.json()


def sync_user(data):
    response = requests.post('http://35.208.29.226/sync_user/', data)
    print(response.json())

    return response.json()


