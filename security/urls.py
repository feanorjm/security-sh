from django.urls import include, path
from security import views


report_list = views.ReportViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

store_phone_list = views.StorePhoneViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
store_phone_detail = views.StorePhoneViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

alarm_list = views.AlarmViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
alarm_detail = views.AlarmViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

sosafe_report_list = views.SosafeReportViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
sosafe_report_detail = views.SosafeReportViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

cloud_cam_order_list = views.CloudCamOrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    path('reports/', report_list, name='report_list'),
    path('store_phone/', store_phone_list, name='store_phone_list'),
    path('store_phone/<str:pk>/', store_phone_detail, name='store_phone_detail'),
    path('alarm/', alarm_list, name='alarm_list'),
    path('alarm/<str:pk>/', alarm_detail, name='alarm_detail'),
    path('ssf_report/', sosafe_report_list, name='sosafe_report_list'),
    path('ssf_report/<str:pk>/', sosafe_report_detail, name='sosafe_report_detail'),
    path('cloudcam_order/', cloud_cam_order_list, name='cloud_cam_order_list'),
    path('alarm-zone/', views.AlarmByZone.as_view(), name='alarm-zone'),
    path('report-history/', views.History.as_view(), name='report-history'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('alertas/', views.alertas, name='alertas'),
]
