#   from django.contrib.auth.models import User
from main.models import Service, Plan, Client, Subscription, Payment, KushkiToken, Coupon, Discount, DiscountCode, WebhookEvent
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from main.serializers import ServiceSerializer, PlanSerializer, ClientSerializer, SubscriptionSerializer, \
    PaymentSerializer, KushkiTokenSerializer, CouponSerializer, DiscountSerializer, \
    DiscountCodeSerializer, HomeSubscriptionSerializer
from security.models import Alarm
import json
# from main.utilities.mongodb import insert_data
# from main.utilities.check_host import check

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class ClientViewSet(viewsets.ModelViewSet):
    lookup_field = 'uid'
    queryset = Client.objects.all().order_by('create_time')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def create(self, request, *args, **kwargs):
        uid = request.data['uid']
        client = Client.objects.filter(uid=uid).first()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if client is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(data={'message': 'Client Already Exist'}, status=status.HTTP_400_BAD_REQUEST)


class PlanViewSet(viewsets.ModelViewSet):
    # queryset = Plan.objects.all().order_by('id')
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        service = self.request.query_params.get('service', None)
        if service is None:
            plans = Plan.objects.all().order_by('id')
        else:
            plans = Plan.objects.filter(service=service).order_by('id')
        return plans


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('id')
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class SubscriptionViewSet(viewsets.ModelViewSet):
    #   lookup_field = 'uid'
    queryset = Subscription.objects.all().order_by('-start_date')
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        client = request.data['client']
        token_payment = request.data['token_payment']
        sub_id_gateway = request.data['subscription_id_gateway']
        #   Consulta si la suscripcion se está duplicando
        subscription = Subscription.objects.filter(client=client, token_payment=token_payment,
                                                   subscription_id_gateway=sub_id_gateway).first()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if subscription is None:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentViewSet(viewsets.ModelViewSet):
    #   queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        uid = self.request.query_params.get('uid', None)
        if uid is None:
            payments = Payment.objects.all().order_by('-payment_date')
        else:
            payments = Payment.objects.filter(uid=uid).order_by('-payment_date')
        return payments


class KushkiTokenViewSet(viewsets.ModelViewSet):
    queryset = KushkiToken.objects.filter(active=True).order_by('id')
    serializer_class = KushkiTokenSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class CouponViewSet(viewsets.ModelViewSet):
    # queryset = Plan.objects.all().order_by('id')
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        code = self.request.query_params.get('code', None)
        if code is None:
            coupons = Coupon.objects.all().order_by('id')
        else:
            coupons = Coupon.objects.filter(code=code).order_by('id')
        return coupons


class DiscountCodeViewSet(viewsets.ModelViewSet):
    # queryset = Plan.objects.all().order_by('id')
    serializer_class = DiscountCodeSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        code = self.request.query_params.get('code', None)
        if code is None:
            discount_codes = DiscountCode.objects.all().order_by('id')
        else:
            discount_codes = DiscountCode.objects.filter(code=code).order_by('id')
        return discount_codes


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all().order_by('id')
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class HomeSubscriptionViewSet(viewsets.ModelViewSet):
    # queryset = Plan.objects.all().order_by('id')
    serializer_class = HomeSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        uid = self.request.query_params.get('uid', None)
        if uid is None:
            data = Subscription.objects.all().order_by('id')
        else:
            subs_list = dict()
            data = Subscription.objects.filter(client__uid=uid).order_by('id')
        return data


# class HookEventCharge(CreateAPIView):
#     permission_classes = [permissions.AllowAny]
#
#     def create(self, request, *args, **kwargs):
#         try:
#             #   check = check(request)
#             hook_json = json.dumps(request.data)
#             hook_json_loads = json.loads(hook_json)
#             res = insert_data(hook_json_loads)  # Insert data in MongoDB
#             print(res)
#             event = hook_json_loads["event"]
#             name = hook_json_loads["name"]
#             fields = WebhookEvent._meta.fields
#             field_names = [f.name for f in fields]
#             event_obj = {}
#             event_obj["name"] = name
#             for key in event:
#                 if key in field_names:
#                     if key != "id":
#                         event_obj[key] = event[key]
#                     else:
#                         event_obj["event_id"] = event[key]
#
#             create = WebhookEvent.objects.create(**event_obj)
#             print("Event created", "id", create, create.name)
#
#             message = "event created successfully"
#         except Exception as e:
#             message = "Error creating event: " + str(e)
#
#         return Response({"message": message}, status=status.HTTP_200_OK)
#
#
# hook_event_charge = HookEventCharge.as_view()
#
#
# class WebHookWoocommerce(CreateAPIView):
#     permission_classes = [permissions.AllowAny]
#
#     def create(self, request, *args, **kwargs):
#         try:
#             #   check = check(request)
#             hook_json = json.dumps(request.data)
#             hook_json_loads = json.loads(hook_json)
#             print(hook_json)
#             message = "Success"
#         except Exception as e:
#             message = "Error creating event: " + str(e)
#
#         return Response({"message": message}, status=status.HTTP_200_OK)
#
#
# web_hook_woocommerce = WebHookWoocommerce.as_view()

