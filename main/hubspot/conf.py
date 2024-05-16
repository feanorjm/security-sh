from hubspot import HubSpot


def conn():
    #   api_client = HubSpot(api_key='f45a3ae7-55ca-43a8-801a-ddc71798f037')
    api_client = HubSpot(access_token='pat-na1-964881cd-f340-45db-b7b2-1c769ce18cbc')
    #   api_client = HubSpot(api_key='c3d667b9-c39a-49af-949a-9e05c3170a7c') //developer "hubspot_owner_id": "188375142"
    return api_client
