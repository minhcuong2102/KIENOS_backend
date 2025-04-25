from django.urls import path, include
from rest_framework import routers
from .views.service_response import ServiceResponseViewSet
from .views.service import PTServiceViewSet, NonPTServiceViewSet
from .views.contract import ContractViewSet

router = routers.DefaultRouter()
router.register(r'service-responses', ServiceResponseViewSet, basename='service-responses')
router.register(r'pt-services', PTServiceViewSet, basename='pt-services')
router.register(r'nonpt-services', NonPTServiceViewSet, basename='nonpt-services')
router.register(r'contracts', ContractViewSet, basename='contracts')

app_name = "service"
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
