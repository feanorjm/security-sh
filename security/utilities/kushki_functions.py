import requests


headers = {
    "Content-Type": "application/json",
    "Public-Merchant-Id": "2056ba55ee95496ba63b65832366d6d5",
    "Private-Merchant-Id": "12c98d9e45654cd7afdfc2402f60a3b1"
}


def get_recurring_charge_info(subscriptionId):
    url = "https://api.kushkipagos.com/subscriptions/v1/card/search/" + subscriptionId
    response = requests.request("GET", url, headers=headers)

    print(response.text)


def list_transactions_list():
    querystring = {"from": "2022-09-01T13:39:00.836", "to": "2022-09-21T23:00:00.836"}
    url = "https://api.kushkipagos.com/analytics/v1/transactions-list"
    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)


def make_one_click_payment(subscriptionId):
    url = "https://api-uat.kushkipagos.com/subscriptions/v1/card/" + subscriptionId

    payload = {
        "language": "es",
        "amount": {
            "subtotalIva": 15.16,
            "subtotalIva0": 0,
            "ice": 0,
            "iva": 1.82,
            "currency": "USD"
        },
        "metadata": {"customerId": "123"},
        "contactDetails": {
            "documentType": "CC",
            "documentNumber": "1009283738",
            "email": "user@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "phoneNumber": "+593912345678"
        },
        "orderDetails": {
            "siteDomain": "tuebook.com",
            "shippingDetails": {
                "name": "John Doe",
                "phone": "+593912345678",
                "address": "Eloy Alfaro 139 y Catalina Aldaz",
                "city": "Quito",
                "region": "Pichincha",
                "country": "Ecuador",
                "zipCode": "170402"
            },
            "billingDetails": {
                "name": "John Doe",
                "phone": "+593912345678",
                "address": "Eloy Alfaro 139 y Catalina Aldaz",
                "city": "Quito",
                "region": "Pichincha",
                "country": "Ecuador",
                "zipCode": "170402"
            }
        },
        "productDetails": {"product": [
                {
                    "id": "198952AB",
                    "title": "eBook Digital Services",
                    "price": 6990000,
                    "sku": "10101042",
                    "quantity": 1
                },
                {
                    "id": "198953AB",
                    "title": "eBook Virtual Selling",
                    "price": 9990000,
                    "sku": "004834GQ",
                    "quantity": 1
                }
            ]},
        "fullResponse": "v2"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)