from security.models import *
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from security.serializers import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.shortcuts import render
import base64
import pytz
from django.db.models import Count
from django.db.models.functions import TruncDate
import json



class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-id')
    serializer_class = ReportSerializer
    #permission_classes = [permissions.AllowAny]
    permission_classes_by_action = {'create': [permissions.AllowAny],
                                    'list': [permissions.IsAuthenticated, TokenHasReadWriteScope]
                                    }

    def create(self, request, *args, **kwargs):
        if 'User-Agent' in request.headers:
            #   print(request.headers['User-Agent'])
            if request.headers['User-Agent'] == 'QUECTEL_MODULE':   #agregar POSTMAN tambien
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        return super(ReportViewSet, self).list(request, *args, **kwargs)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]


class StorePhoneViewSet(viewsets.ModelViewSet):
    queryset = StorePhone.objects.all().order_by('-id')
    serializer_class = StorePhoneSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class AlarmViewSet(viewsets.ModelViewSet):
    ##lookup_field = 'subscription'
    ##queryset = Alarm.objects.all().order_by('-id')

    serializer_class = AlarmSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get_queryset(self):
        subscription = self.request.query_params.get('subscription', None)
        home = self.request.query_params.get('home', None)

        if subscription is None and home is None:
            alarm = Alarm.objects.all().order_by('id')
        elif subscription and home is None:
            alarm = Alarm.objects.filter(subscription=subscription).order_by('id')
        elif home and subscription is None:
            alarm = Alarm.objects.filter(home_id=home).order_by('id')
        elif subscription and home:
            alarm = Alarm.objects.filter(subscription=subscription, home_id=home).order_by('id')
        return alarm

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        date_time = datetime.now()
        aware_datetime = make_aware(date_time)
        instance.update_time = aware_datetime
        instance.save()
        return Response(serializer.data)


class SosafeReportViewSet(viewsets.ModelViewSet):
    queryset = SosafeReport.objects.all().order_by('-id')
    serializer_class = SosafeReportSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class CloudCamOrderViewSet(viewsets.ModelViewSet):
    queryset = CloudCamOrder.objects.all().order_by('-id')
    serializer_class = CloudCamOrderSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class AlarmByZone(APIView):
    serializer_class = AlarmSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        region = request.query_params.get('region', None)
        comuna = request.query_params.get('comuna', None)

        if region and comuna is None:
            alarms = Alarm.objects.filter(region_code=region)
        elif comuna and region is None:
            alarms = Alarm.objects.filter(comuna_code=comuna)
        else:
            alarms = Alarm.objects.filter(region_code=region, comuna_code=comuna)

        serializer = AlarmSerializer(alarms, many=True)

        return Response({"response": serializer.data}, content_type='application/json')



class History(APIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        device = request.query_params.get('device', None)
        fecha_ini = request.query_params.get('fecha_ini', None)
        fecha_end = request.query_params.get('fecha_end', None)

        flag = False
        if fecha_ini and fecha_end:
            parsed_fecha_ini = datetime.strptime(fecha_ini, '%Y-%m-%d')
            parsed_fecha_end = datetime.strptime(fecha_end, '%Y-%m-%d')
            santiago_timezone = pytz.timezone('America/Santiago')
            fecha_ini = santiago_timezone.localize(parsed_fecha_ini)
            fecha_end = santiago_timezone.localize(parsed_fecha_end)
            flag = True

        if device and flag:
            reports = Report.objects.filter(device_id=device, datetime__range=[fecha_ini, fecha_end])
        elif device and flag is False:
            reports = Report.objects.filter(device_id=device)
        elif device is None and flag:
            reports = Report.objects.filter(datetime__range=[fecha_ini, fecha_end])
        else:
            reports = Report.objects.all()

        serializer = ReportSerializer(reports, many=True)

        return Response({"response": serializer.data}, content_type='application/json')



class Dashboard(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        year = datetime.now().date().year
        month = datetime.now().date().month
        day = datetime.now().date().day
        total_reports = Report.objects.all().count()
        total_month_reports = Report.objects.filter(datetime__year=year, datetime__month=month).count()
        total_day_reports = Report.objects.filter(datetime__year=year, datetime__month=month, datetime__day=day).count()
        total_month_alerts = Report.objects.filter(datetime__year=year, datetime__month=month, alarm_mode=True).count()
        total_day_alerts = Report.objects.filter(datetime__year=year, datetime__month=month, datetime__day=day,
                                                 alarm_mode=True).count()
        total_month_sos = Report.objects.filter(datetime__year=year, datetime__month=month, sos=True).count()

        arm = Report.objects.filter(mode="Arm").count()
        home = Report.objects.filter(mode="Home").count()
        disarm = Report.objects.filter(mode="Disarm").count()
        light_disconnect = Report.objects.filter(message__contains="¡Pérdida de alimentación!").count()
        light_connect = Report.objects.filter(message__contains="¡Alimentación restablecida!").count()
        alarm = Report.objects.filter(alarm_mode=True).count()

        now_ = datetime.now()
        santiago_timezone = pytz.timezone('America/Santiago')
        now_ = santiago_timezone.localize(now_)
        alerts = Report.objects.filter(
            alarm_mode=True,
            datetime__range=(now_ - timedelta(days=30), now_)
        ).values(
            date=TruncDate('datetime__date')
        ).annotate(
            quantity=Count('pk')
        ).order_by('date')

        dictionaries = [obj for obj in alerts]

        for i in dictionaries:
            i['date'] = i['date'].strftime('%Y-%m-%d')

        #   json_variation = json.dumps(dictionaries)

        data = {
            "total_reports": total_reports,
            "total_month_reports": total_month_reports,
            "total_day_reports": total_day_reports,
            "total_month_alerts": total_month_alerts,
            "total_day_alerts": total_day_alerts,
            "total_month_sos": total_month_sos,
            "categories": {
                "Armado completo": arm,
                "Armado en casa": home,
                "Desarmado": disarm,
                "Pérdida de alimentación": light_disconnect,
                "Alimentación restablecida": light_connect,
                "Alarma de emergencia": alarm,
            },
            "Alertas ultimos 30 días": dictionaries
        }

        return Response(data, content_type='application/json')


def alertas(request):
    return render(request, 'reports.html', {})