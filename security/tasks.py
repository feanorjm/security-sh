from celery import shared_task
from security.models import *
from main.models import Subscription
import time
from django.utils.timezone import make_aware
from security.sender_wsp import send_whatsapp, send_warning_whatsapp
from security.utilities.tuya_functions import create_order
from datetime import datetime, date


commodities = {
        "ECbahf9ym6zh8g": "7-day event cloud storage_30 day",
        "ECbjmztwlpue4g": "30-day event cloud storage_30 day",
        "ECbjmzy0jzvlz4": "7-day event cloud storage_365 day",
        "ECbjn00quai5ts": "30-day event cloud storage_365 day"
    }


@shared_task()
def countdown(alert_pk):
    alert = Alert.objects.get(pk=alert_pk)
    report = alert.report
    status = False
    #   virtual_id = report.virtual_id
    #   alarm_phone = report.device_phone
    device_id = report.device_id
    print(device_id)
    print("time start")
    for i in range(30, 0, -1):
        #   new_report = Report.objects.filter(virtual_id=virtual_id).last()
        new_report = Report.objects.filter(device_id=device_id).last()
        if (new_report.pk > report.pk and new_report.alarm_mode is False):
            print("Whatsapp messages are canceled")
            break
        else:
            print(i)
            time.sleep(1)
            if i == 1:
                print("Whatsapp messages will be sent")
                #   send_whatsapp(report)
                send_whatsapp(device_id, report)
                status = True
                alert.sent_messages = True
                datetime_now = datetime.now()
                alert.update_time = make_aware(datetime_now)
                alert.save()

    if status:
        return "messages were sent"
    else:
        return "messages were not sent"


@shared_task()
def warning_msg(report_pk, msg_wsp):
    report = Report.objects.get(pk=report_pk)
    send_warning_whatsapp(report, msg_wsp)


@shared_task()
def task_cloud_cam_create(cloud_cam_order_pk):
    try:
        cloud_cam_order = CloudCamOrder.objects.get(pk=cloud_cam_order_pk)
        subscription = cloud_cam_order.subscription
        msg = ""

        dt_obj = datetime.now()
        millisec = dt_obj.timestamp() * 1000
        data = {}
        data["order_id"] = str(subscription.id) + '-' + str(round(millisec))
        data["tuya_uid"] = subscription.client.uid
        data["home_id"] = str(cloud_cam_order.home)
        data["commodity_code"] = cloud_cam_order.commodity_code
        data["device_id"] = cloud_cam_order.uuid
        data["pay_id"] = cloud_cam_order.pay_id
        order = create_order(data)  # primero crear falsamente
        # order = "Se ha creado nueva orden en tuya"
    except Exception as e:
        print('Problema en la creación de orden en TUYA: ', str(e))

    try:
        success = order['success']
        if success is True:
            activate_timestamp = order['t']
            result = order['result']
            expend_status = result['expend_status']
            commodity_code = data["commodity_code"]

            cloud_cam_order.order_id = data["order_id"]
            cloud_cam_order.commodity_name = commodities[commodity_code]
            cloud_cam_order.activate_timestamp = activate_timestamp
            cloud_cam_order.expiration_timestamp = result['expiration_timestamp']
            cloud_cam_order.expend_status = expend_status
            cloud_cam_order.activated = True

            cloud_cam_order.save()
            msg = "La orden cloud cam se ha creado satisfactoriamente: " + str(cloud_cam_order.id)
        else:
            msg = "Se ha producido un error: " + order
        return msg

    except Exception as e:
        print('Problema en la creación de CloudCamOrder: ', str(e))
