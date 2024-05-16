# from security.models import *
# from main.models import *
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from main.hubspot.functions import *
# from main.tasks import create_contact, send_partner_email, task_welcome_email
# import math


# @receiver(post_save, sender=Client)
# def create_contact_hubspot(sender, instance, created, **kwargs):
#     if created:
#         create_contact.delay(instance.pk)

#
# @receiver(post_save, sender=Discount)
# def create_discount(sender, instance, created, **kwargs):
#     if created:
#         discount = instance
#         subscription_obj = discount.subscription
#         anual = False
#         if discount.subs_initial_amount == 169900:
#             anual = True
#             # plan_sub_anual = Plan.objects.get(pk=10) # en local cambiar a 8
#             # subscription_obj.plan_id = plan_sub_anual
#             # subscription_obj.save()
#         ##############
#
#         partner = discount.discount_code.assigned_to
#         commission = partner.commission
#         if commission is None:
#             print('partner without commission')
#         else:
#             sub_final_amount = discount.subs_final_amount
#             add_final_amount = discount.add_final_amount
#             # if discount.subscription.plan_id.periodicity == "M":  cambiar despues
#             if anual is False:
#                 commission_sub = commission.subscription_comm
#             else:
#                 commission_sub = commission.subscription_comm_yearly
#
#             commission_add = commission.additional_comm
#             # se inicia calculo de comisiones
#             commission_1 = 0
#             commission_2 = 0
#             if commission.comm_subs_type == 'percent':
#                 subscription = math.trunc(sub_final_amount/1.19)     # Se calcula monto suscripción bruto
#                 commission_1 = math.trunc((subscription * commission_sub) / 100)  # Se calcula la comisión de la suscripción
#             else:
#                 commission_1 = commission_sub
#
#             if commission.comm_additional_type == 'percent':
#                 additionals = math.trunc(add_final_amount/1.19)     # Se calcula monto adicional bruto
#                 commission_2 = math.trunc((additionals * commission_add)/100)   # Se calcula la comisión de los adicionales
#             else:
#                 commission_2 = commission_add
#
#             total_commission = commission_1 + commission_2
#
#             commission_partner = CommissionPartner(discount=discount,
#                                                    partner=partner,
#                                                    subs_commission=commission_1,
#                                                    add_commission=commission_2,
#                                                    total_commission=total_commission)
#             commission_partner.save()
#
#
# @receiver(post_save, sender=CommissionPartner)
# def create_commission(sender, instance, created, **kwargs):
#     if created:
#         partner = instance.partner
#         if partner.partner_type != 'alliance':  #Se hace filtro solo para vendedores (seller)
#             send_partner_email.delay(instance.pk)
#             #   send_partner_email(instance.pk)
#
#
# @receiver(post_save, sender=Subscription)
# def create_subscription(sender, instance, created, **kwargs):
#     if created:
#         service = instance.plan_id.service
#         if service.id == 3:    # cambiar al pasar a prd 3
#             # task_welcome_email(instance.pk)
#             task_welcome_email.delay(instance.pk)
