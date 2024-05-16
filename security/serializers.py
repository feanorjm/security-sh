from rest_framework import serializers
from security.models import *


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ['id', 'message', 'alarm_louder', 'sos', 'alert_time', 'mode', 'alarm_mode', 'user_id', 'virtual_id',
                  'pid', 'device_id', 'device_phone', 'datetime']


class StorePhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePhone
        fields = ['id', 'alarm', 'name', 'phone']


class AlarmSerializer(serializers.ModelSerializer):
    store_phone = StorePhoneSerializer(many=True, read_only=True)

    class Meta:
        model = Alarm
        fields = ['id', 'subscription', 'home_id', 'name', 'last_name', 'email', 'phone', 'home_type', 'gender',
                  'birthday', 'virtual_id', 'alarm_serial', 'alarm_phone', 'alarm_address', 'country', 'region',
                  'comuna', 'lat', 'long', 'sms_code', 'status', 'device_id', 'store_phone', 'country_code',
                  'region_code', 'comuna_code']


class SosafeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SosafeReport
        fields = ['id', 'ssf_report_id', 'ssf_report_uuid', 'alarm', 'virtual_id', 'user_id', 'home_id', 'message', 'state']


class CloudCamOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudCamOrder
        fields = ['subscription', 'order_id', 'pay_id', 'home', 'uuid', 'commodity_code', 'commodity_name',
                  'activate_timestamp', 'expiration_timestamp', 'expend_status']
