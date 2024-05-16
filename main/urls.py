from django.urls import include, path
from main import views


client_list = views.ClientViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
client_detail = views.ClientViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

service_list = views.ServiceViewSet.as_view({
    'get': 'list'
})
service_detail = views.ServiceViewSet.as_view({
    'get': 'retrieve'
})

plan_list = views.PlanViewSet.as_view({
    'get': 'list'
})
plan_detail = views.PlanViewSet.as_view({
    'get': 'retrieve'
})

subscription_list = views.SubscriptionViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
subscription_detail = views.SubscriptionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

payment_list = views.PaymentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
payment_detail = views.PaymentViewSet.as_view({
    'get': 'retrieve'
})
kushkitoken_list = views.KushkiTokenViewSet.as_view({
    'get': 'list'
})

coupon_list = views.CouponViewSet.as_view({
    'get': 'list'
})
coupon_detail = views.CouponViewSet.as_view({
    'get': 'retrieve'
})

discount_code_list = views.DiscountCodeViewSet.as_view({
    'get': 'list'
})
discount_code_detail = views.DiscountCodeViewSet.as_view({
    'get': 'retrieve'
})

discount_list = views.DiscountViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
discount_detail = views.DiscountViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})

home_list = views.HomeSubscriptionViewSet.as_view({
    'get': 'list',
})
home_detail = views.HomeSubscriptionViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
})


urlpatterns = [
    path('clients/', client_list, name='client-list'),
    path('clients/<str:uid>/', client_detail, name='client-detail'),
    path('services/', service_list, name='service-list'),
    path('services/<int:pk>/', service_detail, name='service-detail'),
    path('plans/', plan_list, name='plan-list'),
    path('plans/<int:pk>/', plan_detail, name='plan-detail'),
    path('subscriptions/', subscription_list, name='subscription-list'),
    path('subscriptions/<int:pk>/', subscription_detail, name='subscription-detail'),
    path('payments/', payment_list, name='payment-list'),
    path('payments/<str:uid>/', payment_detail, name='payment-detail'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('kushkitoken/', kushkitoken_list, name='kushkitoken-list'),
    path('coupons/', coupon_list, name='coupon_list'),
    path('coupons/<int:pk>/', coupon_detail, name='coupon_detail'),
    path('discount_code/', discount_code_list, name='discount_code_list'),
    path('discount_code/<int:pk>/', discount_code_detail, name='discount_code_detail'),
    path('discounts/', discount_list, name='discount_list'),
    path('discounts/<int:pk>/', discount_detail, name='discount_detail'),
    path('home_subs/', home_list, name='home_list'),
    path('home_subs/<int:pk>/', home_detail, name='home_detail'),
]
