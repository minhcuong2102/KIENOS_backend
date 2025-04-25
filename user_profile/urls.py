from django.urls import path, include
from rest_framework import routers
from .views.coach_profile import CoachProfileViewSet
from .views.customer_profile import CustomerProfileViewSet

router = routers.DefaultRouter()
router.register(r'customer-profiles', CustomerProfileViewSet, basename='customer-profiles')
router.register(r'coach-profiles', CoachProfileViewSet, basename='coach-profiles')

app_name = "user-profile"
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
