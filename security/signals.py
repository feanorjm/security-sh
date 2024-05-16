from security.models import *
from main.models import *
from django.db.models.signals import post_save
from django.core.signals import request_finished
from security.tasks import countdown, task_cloud_cam_create, warning_msg
from django.dispatch import receiver
from security.views import ReportViewSet
# from django_q.tasks import async_task, result
from security.hooks import print_result


@receiver(post_save, sender=Report)
def create_alert(sender, instance, created, **kwargs):
    report_type = ReportType.objects.filter(message=instance.message)

    if report_type.count() == 0:
        if instance.alarm_mode:
            alert = Alert(report=instance)
            alert.save()
    else:
        report_type = report_type.first()
        warning_msg.delay(instance.pk, report_type.msg_wsp)


# @receiver(post_save, sender=Alert)
# def update_alert_status(sender, instance, created, **kwargs):
#     if created:
#         countdown.delay(instance.pk)


# @receiver(post_save, sender=Alert)
# def update_alert_status(sender, instance, created, **kwargs):
#     if created:
#         async_task(countdown, instance.pk, hook=print_result)
#         #   print("Se ejecuta countdown para Alerta N°", instance.pk)


@receiver(post_save, sender=Subscription)
def assign_sim(sender, instance, created, **kwargs):
    if created:
        #   Aqui se debe asignar una simcard
        print("Se asignó sim")
        # query = SimCard.objects.filter(available=True)
        # if query.count() >= 1:
        #     sim = query.first()
        #     sim.subscription = instance
        #     sim.available = False
        #     sim.save()
        #     instance.assigned_sim = True
        #     instance.save()
        # else:
        #     instance.assigned_sim = False
        #     instance.save()


@receiver(post_save, sender=CloudCamOrder)
def create_cloud_cam_order(sender, instance, created, **kwargs):
    if created and instance.activated is False:
        msg = task_cloud_cam_create.delay(instance.pk)
        print(msg)
