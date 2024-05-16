from datetime import datetime
from django.template import loader
from django.core.mail import EmailMultiAlternatives
import re


def enviar_correo():
    html_message = loader.render_to_string('correo_mkt.html',{'caption': 'Ordenes Cloud Cam Renovadas',})

    message = 'hola'
    from_email = 'mensajeria@smarthomy.com'
    to_email = 'adams@smarthomy.com'
    cc = ['juan@smarthomy.com', 'valentina@smarthomy.com']

    msg = EmailMultiAlternatives('Información Smart Homy Security', message, from_email, [to_email], cc=cc)
    msg.attach_alternative(html_message, "text/html")
    send = msg.send()

    return 1


enviar_correo()
