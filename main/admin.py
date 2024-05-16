from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from security.utilities.tuya_functions import get_devices, sync_user
from main.models import *
from security.models import Alarm
import hashlib


admin.site.site_title = "Smart Homy administration"
admin.site.site_header = "Smart Homy administration"
#   admin.site.index_title = "hola2"


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'description', 'active', 'icon', 'image', 'requires_device', 'device_category', 'start_in')


class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'service', 'periodicity', 'description', 'price', 'iva', 'total_price', 'active')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'uid', 'email', 'phone', 'create_time', 'name')

    search_fields = ('username', 'uid', 'name')

    change_form_template = 'device_list.html'

    def save_model(self, request, obj, form, change):
        c = Client.objects.get(pk=obj.pk)
        if c.password != obj.password:
            if obj.password is not None and obj.password != "":
                password = obj.password
                password = hashlib.md5(password.encode('utf-8')).hexdigest()
                if obj.username_type == 1:
                    username = obj.username.split("-")[1]
                else:
                    username = obj.username
                data = {}
                data["country_code"] = "56"
                data["username"] = username
                data["password"] = password
                data["username_type"] = obj.username_type
                response = sync_user(data)
                #   print(response["success"])
                if response["success"] is True:
                    self.message_user(request, "The password was changed successfully.", messages.SUCCESS)
                else:
                    self.message_user(request, "there was a problem changing the password.", messages.ERROR)

        super().save_model(request, obj, form, change)

    def get_osm_info(self, object_id):
        client = Client.objects.get(pk=object_id)
        data = get_devices(client.uid)

        return data

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        data = self.get_osm_info(object_id)
        if data["success"] is True:
            extra_context['has_devices'] = True
            extra_context['osm_data'] = data["result"]

        else:
            extra_context['has_devices'] = False
            extra_context['osm_data'] = data["msg"]

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'home', 'installed', 'token_payment', 'subscription_id_gateway', 'service', 'plan_id', 'iva', 'subtotal_iva', 'currency',
                    'start_date', 'status', 'tester', 'assigned_sim', 'devices')

    list_filter = ('plan_id__service', 'plan_id', 'tester', 'status')

    search_fields = ('client__username', 'client__uid', 'subscription_id_gateway', 'home')

    raw_id_fields = ('client',)
    # define the autocomplete_lookup_fields
    autocomplete_lookup_fields = {
        'fk': ['client'],
    }

    def service(self, obj):
        return obj.plan_id.service

    def installed(self, obj):
        sub = Subscription.objects.get(pk=obj.id)
        alarm = Alarm.objects.filter(subscription=sub)
        if len(alarm) > 0:
            return True
        else:
            return False

    installed.boolean = True


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'id_subscription', 'plan_id', 'amount', 'payment_date', 'payment_gateway', 'payment_method',
                    'document_type', 'document_number', 'phone')


def make_predetermined(modeladmin, request, queryset):
    tokens = KushkiToken.objects.all()
    for token in tokens:
        token.active = False
        token.save()

    queryset.update(active=True)


make_predetermined.short_description = "Mark selected token as predetermined"


class KushkiTokenAdmin(admin.ModelAdmin):
    list_display = ('public_key', 'private_key', 'active', 'ambient')
    actions = [make_predetermined]


class CommissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comm_subs_type', 'subscription_comm', 'subscription_comm_yearly',
                    'comm_additional_type', 'additional_comm', 'active', 'create_date')

    list_filter = ('comm_subs_type', 'comm_additional_type', 'active')

    change_list_filter_template = "admin/filter_listing.html"


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'partner_type', 'commission', 'rut', 'email', 'region', 'comuna',
                    'active', 'create_date')

    list_filter = ('partner_type', 'commission', 'active', 'region')

    search_fields = ('name', 'email',)

    change_list_filter_template = "admin/filter_listing.html"

    # list_editable = ('name',)
    # actions = ['update_selected']
    # def update_selected(self, request, queryset):
    #     queryset.update()


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'code_type', 'subscription_discount', 'subscription_discount_type', 'subscription_discount_amount',
                    'additional_discount', 'additional_discount_type', 'additional_discount_amount', 'assigned_to',
                    'active', 'only_ondemand', 'unlimited', 'uses', 'create_date')

    list_filter = ('code_type', 'subscription_discount', 'additional_discount', 'only_ondemand')

    search_fields = ('code', 'assigned_to__name', 'assigned_to__email',)

    def uses(self, obj):
        uses = Discount.objects.filter(discount_code=obj).count()
        return uses


class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'coupon_type', 'discount_type', 'discount_amount', 'assigned_to', 'create_date',
                    'active', 'unlimited', 'uses')

    list_filter = ('coupon_type', 'discount_type', 'active')

    def uses(self, obj):
        uses = Discount.objects.filter(coupon=obj).count()
        return uses


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'discount_code', 'subscription', 'periodicity', 'create_date', 'subs_initial_amount',
                    'subs_discount_amount', 'subs_final_amount', 'add_initial_amount', 'add_discount_amount',
                    'add_final_amount', 'total_discount')

    list_filter = ('discount_code', 'create_date')

    search_fields = ('discount_code__code', 'subscription__id')

    def total_discount(self, obj):
        suma1 = 0
        suma2 = 0
        if obj.subs_discount_amount is not None:
            suma1 = obj.subs_discount_amount

        if obj.add_discount_amount is not None:
            suma2 = obj.add_discount_amount
        return suma1 + suma2

    def periodicity(self, obj):
        return obj.subscription.plan_id.periodicity


class CommissionPartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner', 'subscription', 'create_discount', 'service', 'plan', 'client', 'discount',
                    'type_commission', 'subs_commission', 'add_commission', 'total_commission')

    list_filter = ('partner',)

    def subscription(self, obj):
        return obj.discount.subscription

    def create_discount(self, obj):
        return obj.discount.create_date

    def service(self, obj):
        return obj.discount.subscription.plan_id.service

    def plan(self, obj):
        return obj.discount.subscription.plan_id

    def client(self, obj):
        return obj.discount.subscription.client

    def type_commission(self, obj):
        return obj.partner.commission


admin.site.register(Service, ServiceAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(KushkiToken, KushkiTokenAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(CommissionPartner, CommissionPartnerAdmin)
