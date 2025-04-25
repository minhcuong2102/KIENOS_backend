from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from .views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

app_name = "user"
urlpatterns = [
    # Lấy access token (và refresh token): thời gian tồn tại 
    # của access token: 5 mins, của refresh token: 1 ngày
    path('auth/token/obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Làm mới access token: gửi refresh token -> trả về access 
    # token mới để tiếp tục truy cập
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),

]
