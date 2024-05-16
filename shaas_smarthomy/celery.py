from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shaas_smarthomy.settings')

URL_broker = 'redis://smarthomy:$martHomy2022@redis-16290.c60.us-west-1-2.ec2.cloud.redislabs.com:16290/0'
app = Celery('shaas_smarthomy', broker=URL_broker)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
