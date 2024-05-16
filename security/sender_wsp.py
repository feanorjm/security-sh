import os
import pytz
from django.utils.timezone import localtime
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from security.models import *


# Find your Account SID and Auth Token at twilio.com/console
account_sid = 'AC93436856d3e08e33c60580f8ab624186'
auth_token = 'b33c1bc496b863dd2223809187833ef8'
client = Client(account_sid, auth_token)


def send_whatsapp(device_id, report):
    #   alarm = Alarm.objects.filter(virtual_id=report.virtual_id).first()
    alarm = Alarm.objects.filter(device_id=device_id, status=1)
    if alarm.count() > 0:
        alarm = alarm.first()
        contacts = get_contacts(alarm)
        for contact in contacts:
            print("Enviando mensaje a ", contact.name, ": ", contact.phone)
            full_name = alarm.name + ' ' + alarm.last_name
            send(contact.name, full_name, report.datetime, alarm.alarm_address, alarm.phone, contact.phone)


def get_contacts(alarm):
    contacts = StorePhone.objects.filter(alarm=alarm)
    return contacts


def send(contact, user_name, time, address, user_phone, contact_phone):
    tz = pytz.timezone("America/Santiago")
    time_tz = localtime(time, tz)
    try:
        message = client.messages \
            .create(
                 from_='whatsapp:+56945950977',
                 body='Estimad@ '+contact+', se ha generado una alarma en la propiedad de '+user_name+' a las '+time_tz.strftime("%H:%M")+', '
                        'en la dirección '+address+'. Por favor llamar al '+user_phone+' para verificar. También puede '
                        'comunicar el hecho directamente a carabineros llamando al 133.',
                 to='whatsapp:' + contact_phone
             )
        print(message.status)
    except TwilioRestException as e:
        #   Agregar codigo alternativo aqui
        print(e, e.code)


def send_warning_whatsapp(report, msg_wsp):
    device_id = report.device_id
    alarm = Alarm.objects.filter(device_id=device_id, status=1)
    if alarm.count() > 0:
        alarm = alarm.first()
        print("Enviando warning a " + alarm.name + " - " + alarm.phone)
        send_warning(report.datetime, alarm.phone, msg_wsp)


def send_warning(time, user_phone, msg):
    tz = pytz.timezone("America/Santiago")
    time_tz = localtime(time, tz)
    try:
        message = client.messages \
            .create(
                 from_='whatsapp:+56945950977',
                 body='Mensaje de alarma: ' + msg,
                 to='whatsapp:' + user_phone
             )
        print(message.status)
    except TwilioRestException as e:
        #   Agregar codigo alternativo aqui
        print(e, e.code)
