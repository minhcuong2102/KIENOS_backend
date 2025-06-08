from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models.notification_user import NotificationUser
from .models.notification import Notification
from .serializers.notification_user import NotificationUserSerializer
from base.utils.custom_pagination import CustomPaginationNotification
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import renderers
from base.permissions import IsSale, IsAdmin, IsCoach, IsCustomer
from .firebase_utils import send_push_notification  # 👈 import hàm FCM
from device_token.models.models import DeviceToken        # 👈 import model device token

class NotificationUserViewSet(viewsets.ModelViewSet):
    queryset = NotificationUser.objects.all().order_by('-create_date')
    serializer_class = NotificationUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPaginationNotification

    def list(self, request, *args, **kwargs):
        user = request.user

        notifications = self.queryset.filter(user=user)

        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({"detail": "No notifications for this user found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notification_user = serializer.save()

            # 🟡 Gửi push notification cho user
            user = notification_user.user
            notification = notification_user.notification

            # Lấy tất cả device_token của user (nếu dùng nhiều thiết bị)
            device_tokens = DeviceToken.objects.filter(user=user)

            for device_token in device_tokens:
                print(f"Gửi tới token: {device_token.token}")
                try:
                    send_push_notification(
                        device_token.token,
                        title="Bạn có thông báo mới",
                        body=notification.message,
                        data={
                            "notification_id": str(notification.id),
                            "user_id": str(user.id)
                        }
                    )
                    print("Đã gửi.")
                except Exception as e:
                    print(f"Lỗi gửi push cho {user.username}: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    @action(methods=['get'], url_path='get-by-role', detail=False, permission_classes=[IsAuthenticated], 
        renderer_classes=[renderers.JSONRenderer])
    def get_by_role(self, request, *args, **kwargs):
        role = request.user.role.name
        notifications = self.queryset.filter(roles__icontains=role)
        page = self.paginate_queryset(notifications)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response({"detail": "No notifications for this user found."}, status=status.HTTP_404_NOT_FOUND)
    
