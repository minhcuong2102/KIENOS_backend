from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationUserViewSet
from device_token.views import DeviceTokenViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationUserViewSet)
router.register(r'device-token', DeviceTokenViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]