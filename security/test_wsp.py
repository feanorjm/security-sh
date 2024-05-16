import os
import pytz
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


# Find your Account SID and Auth Token at twilio.com/console
account_sid = 'AC93436856d3e08e33c60580f8ab624186'
auth_token = 'b33c1bc496b863dd2223809187833ef8'
client = Client(account_sid, auth_token)


def send():
    try:
        message = client.messages.create(
            from_='whatsapp:+56945950977',
            body='Estimad@ Pilar Bravo, se ha generado una alarma en la propiedad de Pilar Bravo a las 18:49, en '
                 'la dirección Las Carmelas 2083. Por favor llamar al +56988199100 para verificar. También puede '
                 'comunicar el hecho directamente a carabineros llamando al 133.',
            to='whatsapp:+56988199100'
        )
        print(message.status)
    except TwilioRestException as e:
        #   Agregar codigo alternativo aqui
        print(e, e.code)

