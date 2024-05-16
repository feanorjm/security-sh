from django.core.management.base import BaseCommand, CommandError
from main.models import Subscription
from security.models import CloudCamOrder
from security.utilities.tuya_functions import create_order, create_order2
from main.utilities2.email_sender import send_renovation_cloud_cam_email
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Renueva las ordenes cloud cam cuando falta 1 día'

    def handle(self, *args, **options):
        commodities = {
            "ECbahf9ym6zh8g": "7-day event cloud storage_30 day",
            "ECbjmztwlpue4g": "30-day event cloud storage_30 day",
            "ECbjmzy0jzvlz4": "7-day event cloud storage_365 day",
            "ECbjn00quai5ts": "30-day event cloud storage_365 day"
        }
        self.stdout.write(self.style.SUCCESS('Se inicia la renovación de ordenes cloud cam'))
        subscriptions = Subscription.objects.filter(status="active", tester=False)
        activated = []
        for s in subscriptions:
            last_order = CloudCamOrder.objects.filter(service_status=1, subscription__id=s.id)
            if last_order.count() != 0:
                last_order = last_order.last()
                exp = (int(last_order.expiration_timestamp)) / 1000
                expiration = datetime.fromtimestamp(exp)
                today = date.today()
                delta = expiration.date() - today
                if delta.days == 1:
                    print("s_id:", last_order.subscription, "- dias", delta.days)
                    #   revisar si en kushki aún sigue creada la suscripción y pagada
                    dt_obj = datetime.now()
                    millisec = dt_obj.timestamp() * 1000
                    data = {}
                    data["order_id"] = str(s.id) + str(round(millisec))
                    data["tuya_uid"] = s.client.uid
                    data["home_id"] = str(last_order.home)
                    data["commodity_code"] = last_order.commodity_code
                    data["device_id"] = last_order.uuid
                    data["pay_id"] = "pago_" + dt_obj.strftime("%B_%Y")
                    print(data)
                    order = create_order2(data)
                    # order = {'result': {'expend_status': 2, 'expiration_timestamp': 1666372024819, 'order_id': '520'}, 'success': True, 't': 1663780024910, 'tid': 'd0f08aed39cf11edb15d4a9758e475c4'}
                    # print(order)
                    success = order['success']
                    if success is True:
                        activate_timestamp = order['t']
                        result = order['result']
                        commodity_code = data["commodity_code"]
                        cloud_cam_order = CloudCamOrder(
                            subscription=s,
                            order_id=data["order_id"],
                            pay_id=data["pay_id"],
                            home=data["home_id"],
                            uuid=data["device_id"],
                            commodity_code=data["commodity_code"],
                            commodity_name=commodities[commodity_code],
                            activate_timestamp=activate_timestamp,
                            expiration_timestamp=result['expiration_timestamp'],
                            expend_status=result['expend_status'],
                            activated=True
                        )
                        cloud_cam_order.save()
                        activated.append(cloud_cam_order)

                        self.stdout.write(self.style.SUCCESS('Successfully created order for subscription "%s"' % s.id))

        print(activated)
        if len(activated) > 0:
            send_renovation_cloud_cam_email(activated)

