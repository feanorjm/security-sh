from rest_framework import serializers
from main.models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    uid = serializers.SlugRelatedField(slug_field='uid', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'client', 'token_payment', 'subscription_id_gateway', 'plan_id', 'subtotal_iva', 'currency',
                  'start_date', 'status', 'devices', 'uid']


class ClientSerializer(serializers.ModelSerializer):
    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'uid', 'email', 'phone', 'create_time', 'name', 'address', 'country', 'zip_code',
                  'subscriptions', 'username', 'password', 'username_type']


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = ['id', 'uid', 'id_subscription', 'plan_id', 'amount', 'payment_date', 'payment_gateway', 'payment_method',
                  'document_type', 'document_number', 'phone']


class PlanSerializer(serializers.ModelSerializer):
    #    url = serializers.HyperlinkedIdentityField(view_name="main:plan-detail")
    service = serializers.SlugRelatedField(many=False, read_only=True, slug_field='sku')

    class Meta:
        model = Plan
        fields = ['id', 'service', 'name', 'sku', 'description', 'price', 'iva', 'total_price', 'active', 'image', 'periodicity']


class ServiceSerializer(serializers.ModelSerializer):
    #   url = serializers.HyperlinkedIdentityField(view_name="main:service-detail")
    #   plans = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="main:plan-detail")
    #   plans = PlanSerializer(many=True, read_only=True)
    plans = serializers.SlugRelatedField(many=True, read_only=True, slug_field='sku')

    class Meta:
        model = Service
        fields = ['id', 'name', 'sku', 'description', 'active', 'icon', 'image', 'requires_device', 'device_category',
                  'plans', 'metadata', 'start_in']


class KushkiTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = KushkiToken
        fields = ['id', 'public_key', 'private_key', 'active', 'ambient']


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'coupon_type', 'discount_type', 'discount_amount', 'create_date', 'active', 'unlimited']


class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountCode
        fields = ['id', 'code', 'code_type', 'subscription_discount', 'subscription_discount_type', 'subscription_discount_amount',
        'additional_discount', 'additional_discount_type', 'additional_discount_amount', 'active', 'unlimited', 'only_ondemand']


class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ['id', 'discount_code', 'subscription', 'subs_initial_amount', 'subs_discount_amount',
                  'subs_final_amount', 'add_initial_amount', 'add_discount_amount', 'add_final_amount']


class HomeSubscriptionSerializer(serializers.ModelSerializer):
    service = serializers.CharField(source='plan_id.service', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'client', 'home', 'status', 'service']
