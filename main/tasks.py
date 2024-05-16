# from celery import shared_task
# from main.models import *
# from main.hubspot.functions import *
# from main.utilities.email_sender import send_email, send_welcome_email, validate_email, send_failed_payment_email
# import math
#
#
# @shared_task
# def create_contact(instance_pk):
#     client = Client.objects.get(pk=instance_pk)
#     if client.name != client.username:
#         name = client.name
#         name_s = name.split()
#         firstname = ""
#         lastname = ""
#         if len(name_s) == 2:
#             firstname = name_s[0]
#             lastname = name_s[1]
#
#         if client.email is not None and client.phone is not None:
#             create_contact_portal(client.email, firstname, lastname, client.phone)
#
#     else:
#         email = client.email
#         phone = client.phone
#         if email is not None and email != "":
#             if phone is None:
#                 phone = ""
#
#             create_contact_app(email, phone, type="email")
#
#         else:
#             email = ""
#             create_contact_app(email, phone, type="phone")
#
#
# @shared_task
# def send_partner_email(instance_pk):
#     commission_partner = CommissionPartner.objects.get(pk=instance_pk)
#     discount = commission_partner.discount
#     discount_code = discount.discount_code
#     partner = commission_partner.partner
#     partner_name = partner.name
#     email_partner = partner.email
#     subscription_id = discount.subscription.id
#     periodicity = discount.subscription.plan_id.periodicity
#     client_name = discount.subscription.client.name
#     commission = partner.commission
#     commission_amount_add = commission.additional_comm
#     amount_add = math.trunc(discount.add_final_amount / 1.19)
#     #   if commission is not None:
#     commission_sub = commission_partner.subs_commission
#     commission_add = commission_partner.add_commission
#     total_commission = commission_partner.total_commission
#
#     send_email(partner_name, email_partner, discount_code, subscription_id, periodicity, client_name,
#                commission_sub, commission_add, commission_amount_add, amount_add, total_commission)
#
#
# @shared_task
# def task_welcome_email(instance_pk):
#     subscription = Subscription.objects.get(pk=instance_pk)
#     discount = Discount.objects.filter(subscription=subscription).first()
#     subs_final_amount = 0
#     add_final_amount = 0
#     if discount is not None:
#         subs_final_amount = discount.subs_final_amount
#         add_final_amount = discount.add_final_amount
#
#     nombre_cliente = subscription.client.name
#     monto_plan = subscription.plan_id.total_price
#     periodicidad = subscription.plan_id.periodicity
#     email_client = subscription.client.email
#
#     if validate_email(email_client):
#         print(email_client, ":", "validado")
#         send_welcome_email(email_client, nombre_cliente, monto_plan, periodicidad, subs_final_amount, add_final_amount)
#     else:
#         print(email_client, ":", "no validado")
#
#
# @shared_task
# def task_failed_payment(webhook_pk):
#     webhook = WebhookEvent.objects.get(pk=webhook_pk)
#     subscription = Subscription.objects.get(subscription_id_gateway=webhook.subscriptionId)
#     email_cliente = webhook.contactDetails["email"]
#     brand = webhook.binInfo["info"]["brand"]
#     last_four_digit = webhook.lastFourDigits
#     periodicidad = webhook.periodicity
#     subtotalIva0 = webhook.amount["subtotalIva0"]
#     nombre_cliente = webhook.contactDetails["firstName"] + " " + webhook.contactDetails["lastName"]
#     subscription = webhook.subscriptionId
#     fecha_cobro = webhook.created_hook
#     fecha_cobro = fecha_cobro.strftime("%d/%m/%Y")
#     metodo_pago = webhook.binInfo["info"]["type"]
#     currency = webhook.binInfo["info"]["country"]["currency"]
#
#     send_failed_payment_email(email_cliente, brand, last_four_digit, periodicidad, subtotalIva0, nombre_cliente,
#                               subscription, fecha_cobro, metodo_pago, currency)
