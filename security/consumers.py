import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from security.models import Alert


class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Me conecté al WS")

        # Obtener el reporte actual (si es necesario) y enviarlo al cliente
        #   await self.send_report()
        await self.channel_layer.group_add("alert_group", self.channel_name)


    async def alert_created(self, event):
        # Maneja el evento report.created y envía los datos al cliente
        alert_data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'alert.created',
            'data': alert_data,
        }))


@receiver(post_save, sender=Alert)
def alert_post_save(sender, instance, **kwargs):
    # Se llama cada vez que se guarda un informe
    group_name = "alert_group"
    alert_data = {
        'device_id': instance.report.device_id,
        'alarm_message': instance.report.message,
        'sos': instance.report.sos,
        # ... otros campos
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'alert.created',
            'data': alert_data,
        }
    )
