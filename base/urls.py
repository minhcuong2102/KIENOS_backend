from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BaseViewSet

router = DefaultRouter()
router.register(r'base', BaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
