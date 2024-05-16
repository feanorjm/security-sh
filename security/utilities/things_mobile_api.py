import requests
import xmltodict
import json


def get_sims():
    url = "https://api.thingsmobile.com"
    data = {}
    data["username"] = "adams@smarthomy.com"
    data["token"] = "8a128bd4-e56b-4dc4-8e21-11c2a14bdfe4"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        "page": 1,
        "pageSize": 10
    }

    response = requests.post(url + '/services/business-api/simListLite', params=params, data=data, headers=headers)
    if response.status_code == 200:
        obj = xmltodict.parse(response.content)
        sims = obj['result']['sims']['sim']

        new_sims = {}

        for sim in sims:
            new_sims[sim['msisdn']] = sim

        # print(new_sims)

        # print(json.dumps(obj))
        return new_sims


# url = "https://api.thingsmobile.com"
# data = {}
# data["username"] = "adams@smarthomy.com"
# data["token"] = "8a128bd4-e56b-4dc4-8e21-11c2a14bdfe4"
# headers = {
#     'User-Agent': 'Mozilla/5.0',
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
# params = {
#     "page": 1,
#     "pageSize": 10
# }
#
# response = requests.post(url + '/services/business-api/simListLite', params=params, data=data, headers=headers)
# if response.status_code == 200:
#     obj = xmltodict.parse(response.content)
#     sims = obj['result']['sims']['sim']
#
#     new_sims = {}
#
#     for sim in sims:
#         new_sims[sim['msisdn']] = sim
#
#     print(new_sims)

