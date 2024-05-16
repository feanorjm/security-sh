from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from security.models import *
from datetime import datetime, date


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'datetime', 'sos', 'mode', 'alarm_mode', 'alarm', 'client', 'device_id',
                    'device_phone', 'pid')

    list_filter = ('device_id',)
    search_fields = ('id', 'device_id',)

    change_list_template = "admin/change_list_filter_sidebar.html"

    def alarm(self, obj):
        alarm = Alarm.objects.filter(device_id=obj.device_id).first()
        return alarm

    def client(self, obj):
        alarm = Alarm.objects.filter(device_id=obj.device_id).first()
        if alarm is not None:
            return alarm.subscription.client
        else:
            return "Alarm no instalada"


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscription', 'home_id', 'name', 'last_name', 'email', 'phone', 'home_type', 'device_id',
                    'alarm_phone', 'alarm_address', 'country', 'region','comuna', 'lat', 'long', 'create_time',
                    'update_time', 'status', 'country_code', 'region_code', 'comuna_code')

    list_filter = ('status', 'home_type')
    search_fields = ('device_id', 'email')

    # change_list_template = "admin/change_list_filter_sidebar.html"


class StorePhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_alarm', 'name', 'phone')

    def link_to_alarm(self, obj):
        link = reverse("admin:security_alarm_change", args=[obj.alarm.id])
        return format_html('<a href="{}">{}</a>', link, obj.alarm.id)

    link_to_alarm.allow_tags = True


class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_to_report', 'create_time', 'update_time', 'cause', 'confirm', 'sent_messages',
                    'messages_number')

    def link_to_report(self, obj):
        link = reverse("admin:security_report_change", args=[obj.report.id])
        return format_html('<a href="{}">{}</a>', link, obj.report.id)

    link_to_report.allow_tags = True


class SosafeReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'ssf_report_id', 'ssf_report_uuid', 'link_to_alarm', 'virtual_id', 'user_id', 'home_id',
                    'message', 'state', 'create_time', 'update_time']

    def link_to_alarm(self, obj):
        link = reverse("admin:security_alarm_change", args=[obj.alarm.id])
        return format_html('<a href="{}">{}</a>', link, obj.alarm.id)

    link_to_alarm.allow_tags = True


class SimCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'msisdn', 'iccid', 'status', 'tag', 'available', 'subscription']

    list_filter = ('status', 'available')
    search_fields = ('msisdn', 'iccid',)


class CloudCamOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'subscription', 'client', 'order_id', 'pay_id', 'home', 'uuid', 'commodity_code', 'commodity_name', 'activated', 'tuya_order',
                    'activate_datetime', 'expiration_datetime', 'expend_status', 'service_status', 'create_time', 'next_activation']

    list_filter = ('subscription__plan_id__service', 'subscription', 'commodity_code', 'service_status')
    search_fields = ('uuid', 'commodity_code', 'subscription__client__uid')

    def client(self, obj):
        return obj.subscription.client

    def activate_datetime(self, obj):
        if obj.activate_timestamp is not None:
            activate = (int(obj.activate_timestamp))/1000
            dt_object = datetime.fromtimestamp(activate)
            return dt_object
        else:
            return None

    def expiration_datetime(self, obj):
        if obj.expiration_timestamp is not None:
            expiration = (int(obj.expiration_timestamp))/1000
            dt_object = datetime.fromtimestamp(expiration)
            return dt_object
        else:
            return None

    def next_activation(self, obj):
        if self.expiration_datetime(obj) is not None:
            expiration = self.expiration_datetime(obj)
            today = date.today()
            delta = expiration.date() - today
            if delta.days < 0:
                obj.service_status = 2
                obj.save()

            return delta.days
        else:
            return None


class ReportTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'msg_wsp', 'vars']



admin.site.register(Report, ReportAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(StorePhone, StorePhoneAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(SosafeReport, SosafeReportAdmin)
admin.site.register(SimCard, SimCardAdmin)
admin.site.register(CloudCamOrder, CloudCamOrderAdmin)
admin.site.register(ReportType, ReportTypeAdmin)

