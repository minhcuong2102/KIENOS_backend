from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from user.models.user import User
from user.serializers.user import UserSerializer


class BaseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    @action(methods=['get'], url_path='cronjob', detail=False, permission_classes=[AllowAny], 
        renderer_classes=[renderers.JSONRenderer])
    def cronjob(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
