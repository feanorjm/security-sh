from datetime import datetime
from django.template import loader
from django.core.mail import EmailMultiAlternatives
import re


def send_email(partner_name, email_partner, discount_code, subscription_id, periodicity, client_name,
               commission_sub, commission_add, commission_amount_add, amount_add, total_commission):
    now = datetime.now()
    year = now.strftime('%Y')
    message = 'hola'
    service_name = 'Smart Homy Security'

    html_message = loader.render_to_string(
        'mail_partner.html',
        {
            'service_name': service_name,
            'periodicity': periodicity,
            'partner_name': partner_name,
            'discount_code': discount_code,
            'subscription_id': subscription_id,
            'client_name': client_name,
            'commission_sub': commission_sub,
            'commission_add': commission_add,
            'commission_amount_add': commission_amount_add,
            'amount_add': amount_add,
            'total_commission': total_commission,
            'year': year
        }
    )
    from_email = 'mensajeria@smarthomy.com'
    to_email = email_partner
    cc = ['trabajemos@smarthomy.com']

    msg = EmailMultiAlternatives('[Nueva suscripción] - Smart Homy', message, from_email, [to_email], cc=cc)
    msg.attach_alternative(html_message, "text/html")
    send = msg.send()


def send_welcome_email(email_cliente, nombre_cliente, monto_plan, periodicidad, subs_final_amount, add_final_amount):
    if periodicidad == "A":
        periodicidad = "anual"
    else:
        periodicidad = "mensual"

    html_message = loader.render_to_string(
        'welcome_mail.html',
        {
            'nombre_cliente': nombre_cliente,
            'monto_plan': monto_plan,
            'periodicidad': periodicidad,
            'subs_final_amount': subs_final_amount,
            'add_final_amount': add_final_amount
        }
    )
    message = 'hola'
    from_email = 'mensajeria@smarthomy.com'
    to_email = email_cliente
    cc = []

    msg = EmailMultiAlternatives('Bienvenido a Smart Homy Security', message, from_email, [to_email], cc=cc)
    msg.attach_alternative(html_message, "text/html")
    send = msg.send()


def validate_email(email):
    regular_expression = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(regular_expression, email) is not None


def send_renovation_cloud_cam_email(orders):
    html_message = loader.render_to_string(
        'renovation_cloud_cam_mail.html',
        {
            'caption': 'Ordenes Cloud Cam Renovadas',
            'orders': orders
        }
    )

    message = 'hola'
    from_email = 'mensajeria@smarthomy.com'
    to_email = 'soporte@smarthomy.com'
    cc = []

    msg = EmailMultiAlternatives('Ordenes Cloud Cam', message, from_email, [to_email], cc=cc)
    msg.attach_alternative(html_message, "text/html")
    send = msg.send()


def send_failed_payment_email(email_cliente, brand, last_four_digit, periodicidad, subtotalIva0, nombre_cliente,
                              subscription, fecha_cobro, metodo_pago, currency):
    if periodicidad == "monthly":
        periodicidad = "Mensual"
        link_pago = "https://kshk.co/smart-homy/aJUJHE9PG"
    else:
        periodicidad = "Anual"
        link_pago = "https://kshk.co/smart-homy/mOIacffEZ"

    now = datetime.now()
    year = now.strftime('%Y')

    html_message = loader.render_to_string(
        'pago_fallido.html',
        {
            'brand': brand,
            'last_four_digit': last_four_digit,
            'periodicidad': periodicidad,
            'subtotalIva0': subtotalIva0,
            'client': nombre_cliente,
            'subscription': subscription,
            'fecha_cobro': fecha_cobro,
            'metodo_pago': metodo_pago,
            'currency': currency,
            'year': year,
            'link_pago': link_pago
        }
    )
    message = 'hola'
    from_email = 'mensajeria@smarthomy.com'
    to_email = email_cliente
    #   to_email = 'juan@smarthomy.com'
    cc = []

    msg = EmailMultiAlternatives('Pago fallido - Smart Homy Security', message, from_email, [to_email], cc=cc)
    msg.attach_alternative(html_message, "text/html")
    send = msg.send()
