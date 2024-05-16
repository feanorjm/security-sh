from django.db import models
from datetime import datetime
from main.models import Subscription
from django.db.models.signals import post_save
import random


class Pais(models.Model):
    pais_id = models.IntegerField(primary_key=True)
    pais_nombre = models.CharField(max_length=64)
    pais_iso3 = models.CharField(max_length=4)

    def __str__(self):
        return "%s" % self.pais_nombre


class Region(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region_nombre = models.CharField(max_length=64)
    region_ordinal = models.CharField(max_length=4)
    pais_id = models.IntegerField(null=True)

    def __str__(self):
        return "%s" % self.region_nombre


class Provincia(models.Model):
    provincia_id = models.IntegerField(primary_key=True)
    provincia_nombre = models.CharField(max_length=64)
    region_id = models.IntegerField()

    def __str__(self):
        return "%s" % self.provincia_nombre


class Comuna(models.Model):
    comuna_id = models.IntegerField(primary_key=True)
    comuna_nombre = models.CharField(max_length=64)
    provincia_id = models.IntegerField()
    region_id = models.IntegerField()

    def __str__(self):
        return "%s" % self.comuna_nombre


class SimCard(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    msisdn = models.CharField(max_length=50, null=True, blank=True)
    iccid = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    tag = models.CharField(max_length=100, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.msisdn)


class Alarm(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    home_id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    home_type = models.IntegerField(choices=((1, 'House'), (2, 'Apartment'), (3, 'Office')), null=True, blank=True)
    gender = models.IntegerField(choices=((1, 'Man'), (2, 'Woman'), (3, 'Do not report')), null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    virtual_id = models.CharField(max_length=50, null=True, blank=True)
    alarm_serial = models.CharField(max_length=50, null=True, blank=True)
    alarm_phone = models.CharField(max_length=50, null=True, blank=True)
    alarm_address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    comuna = models.CharField(max_length=200, null=True, blank=True)
    lat = models.CharField(max_length=25, null=True, blank=True)
    long = models.CharField(max_length=25, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now_add=True, null=True)
    sms_code = models.CharField(max_length=4, null=True, blank=True)
    status = models.IntegerField(choices=((0, 'inactive'), (1, 'active')), default=1, null=True, blank=True)
    device_id = models.CharField(max_length=50, null=True, blank=True)
    country_code = models.ForeignKey(Pais, null=True, blank=True, on_delete=models.CASCADE)
    region_code = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE)
    comuna_code = models.ForeignKey(Comuna, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    # @staticmethod
    # def autocomplete_search_fields():
    #     return ("id__iexact", "device_id__icontains",)

    def save(self, *args, **kwargs):
        self.sms_code = str(random.randint(1111, 9999))
        sim = SimCard.objects.filter(subscription=self.subscription).first()
        if sim is None:
            self.alarm_phone = '00'
        else:
            self.alarm_phone = '00' + sim.msisdn
        super(Alarm, self).save(*args, **kwargs)


class StorePhone(models.Model):
    alarm = models.ForeignKey(Alarm, related_name='store_phone', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.phone)


class Report(models.Model):
    alarm_louder = models.CharField(max_length=250,  blank=True, null=True, default=0)
    message = models.CharField(max_length=100, null=True, blank=True)
    sos = models.BooleanField(blank=True, null=True)
    alert_time = models.CharField(max_length=50, blank=True, null=True)
    mode = models.CharField(max_length=20, blank=True, null=True)
    alarm_mode = models.BooleanField(blank=True, null=True)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    device_id = models.CharField(max_length=50, null=True, blank=True)
    device_phone = models.CharField(max_length=20, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    virtual_id = models.CharField(max_length=50, null=True, blank=True)
    pid = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        msje = bytearray.fromhex(self.alarm_louder).decode(encoding='latin-1')
        self.message = msje.replace('\x00', '')
        #   print(self.message.format('UTF-8'))
        #   self.datetime = self.datetime.replace(tzinfo='America/Santiago')
        super(Report, self).save(*args, **kwargs)


class Alert(models.Model):
    CAUSES = (
        (1, 'Motion Sensor'),
        (2, 'Door Sensor'),
        (3, 'Smoke sensor'),
        (4, 'SOS'),
    )

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    cause = models.CharField(max_length=50, choices=CAUSES, null=True)
    confirm = models.BooleanField(default=False, null=True)
    sent_messages = models.BooleanField(default=False, null=True)
    messages_number = models.IntegerField(default=0, null=True)


class SosafeReport(models.Model):
    ssf_report_id = models.IntegerField()
    ssf_report_uuid = models.CharField(max_length=50, null=True)
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE)
    virtual_id = models.CharField(max_length=50, null=True)
    user_id = models.CharField(max_length=50, null=True)
    home_id = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class CloudCamOrder(models.Model):
    EXPEND_STATUS = (
        (1, 'Initiating activation'),
        (2, 'The activation is successful'),
        (3, 'Activation failed'),
        (4, 'Activation exception')
    )

    SERVICE_STATUS = (
        (1, 'In Effect'),
        (2, 'Expired'),
    )

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=50, null=True, blank=True)
    pay_id = models.CharField(max_length=50, null=True, blank=True)
    home = models.CharField(max_length=50, null=True, blank=True)
    uuid = models.CharField(max_length=100, null=True, blank=True)
    commodity_code = models.CharField(max_length=100, null=True, blank=True)
    commodity_name = models.CharField(max_length=100, null=True, blank=True)
    tuya_order = models.CharField(max_length=100, null=True, blank=True)
    activate_timestamp = models.CharField(max_length=50, null=True, blank=True)
    expiration_timestamp = models.CharField(max_length=50, null=True, blank=True)
    expend_status = models.IntegerField(choices=EXPEND_STATUS, null=True, blank=True)
    service_status = models.IntegerField(choices=SERVICE_STATUS, null=True, blank=True, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class ReportType(models.Model):
    message = models.CharField(max_length=100, null=True, blank=True)
    msg_wsp = models.TextField(max_length=300, null=True, blank=True)
    vars = models.JSONField(default=list, null=True, blank=True)
    def __str__(self):
        return str(self.message)
