from rest_framework import viewsets, permissions
from .models.models import DeviceToken
from user.models import User
from .serializers import DeviceTokenSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class DeviceTokenViewSet(viewsets.ModelViewSet):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        user_id = request.data.get('user_id')
        if not user_id or not token:
                return Response({"detail": "Missing user_id or token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        device_token, created = DeviceToken.objects.update_or_create(
            token=token,
            defaults={'user': user}
        )

        return Response(DeviceTokenSerializer(device_token).data, status=status.HTTP_201_CREATED)
