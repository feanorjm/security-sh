from hubspot.crm.contacts import SimplePublicObjectInput
from hubspot.crm.deals import SimplePublicObjectInput, ApiException
from hubspot.crm.tickets import SimplePublicObjectInput
from hubspot.crm.objects import notes
from hubspot.crm.contacts.exceptions import ApiException
from main.hubspot.conf import conn
from hubspot.crm.contacts import ApiException


def get_owners():
    api_client = conn()
    try:
        api_response = api_client.crm.owners.owners_api.get_page(limit=100, archived=False)
        print(api_response)
    except ApiException as e:
        print("Exception when calling owners_api->get_page: %s\n" % e)


def create_contact_portal(email, firstname, lastname, phone):
    api_client = conn()
    try:
        new_contact = SimplePublicObjectInput(
            properties={"email": email,
                        "firstname": firstname,
                        "lastname": lastname,
                        "phone": phone,
                        "hubspot_owner_id": "187777077"
                        }
        )
        api_response = api_client.crm.contacts.basic_api.create(simple_public_object_input=new_contact)
        id_contact = api_response.id
        print('contacto creado a través de Portal:', id_contact)
        create_deal(firstname, lastname, id_contact)
    except ApiException as e:
        print("Exception when creating contact: %s\n" % e)


def create_contact_app(email, phone, type):
    api_client = conn()
    try:
        if type == "email":
            new_contact = SimplePublicObjectInput(
                properties={"email": email,
                            "hubspot_owner_id": "187777077"
                            }
            )
            api_response = api_client.crm.contacts.basic_api.create(simple_public_object_input=new_contact)
            print("created with email")

        else:
            new_contact = SimplePublicObjectInput(
                properties={"phone": phone,
                            "firstname": phone,
                            "hubspot_owner_id": "187777077"
                            }
            )
            api_response = api_client.crm.contacts.basic_api.create(simple_public_object_input=new_contact)
            print("created with phone")

        print(api_response)
        id_contact = api_response.id
        print('contacto creado a través de App:', id_contact)
    except ApiException as e:
        print("Exception when creating contact: %s\n" % e)


def get_deals():
    api_client = conn()
    try:
        deals = api_client.crm.deals.get_all()
        print(deals)
    except:
        pass


def create_deal(firstname, lastname, id_contact):
    api_client = conn()

    properties = {
        "amount": "16990",
        "dealname": "Nuevo prospecto Suscripcion " + firstname + " " + lastname,
        "dealstage": "25285141",
        "hubspot_owner_id": "187777077",
        "pipeline": "75e28846-ad0d-4be2-a027-5e1da6590b98"
    }
    new_deal = SimplePublicObjectInput(properties=properties)
    try:
        api_response = api_client.crm.deals.basic_api.create(simple_public_object_input=new_deal)
        id_deal = api_response.id
        print('deal creado:', id_deal)
        #   associate_deal(id_contact, id_deal)
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)


# def associate_deal(id_contact, id_deal):
#     api_client = conn()
#     try:
#         api_response = api_client.crm.deals.associations_api.create(deal_id=id_deal, to_object_type="contact",
#                                                                 to_object_id=id_contact,
#                                                                 association_type="cliente_subs")
#         print('associacion creada:', api_response.id)
#     except ApiException as e:
#         print("Exception when calling associations_api->create: %s\n" % e)


# def get_contact_by_id():
#     api_client = conn()
#     try:
#         contact_fetched = api_client.crm.contacts.basic_api.get_by_id('751')
#         print(contact_fetched)
#     except ApiException as e:
#         print("Exception when requesting contact by id: %s\n" % e)
#
#
# def get_all_contacts():
#     api_client = conn()
#     all_contacts = api_client.crm.contacts.get_all()
#     print(all_contacts)
