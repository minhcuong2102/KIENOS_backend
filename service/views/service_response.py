from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import ServiceResponse
from ..serializers.service_response import ServiceResponseSerializer, ServiceResponseCreateSerializer, ServiceResponseShortSerializer
from base.utils.custom_pagination import CustomPaginationSR
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsAdmin, IsCustomer, IsCoach, IsSale
from user_profile.models.coach_profile import CoachProfile


class ServiceResponseViewSet(viewsets.ModelViewSet):
    queryset = ServiceResponse.objects.all().order_by('-create_date')
    pagination_class = CustomPaginationSR
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceResponseSerializer
    

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceResponseSerializer
        if self.action == 'create':
            return ServiceResponseCreateSerializer
        return ServiceResponseSerializer  


    @action(methods=['get'], url_path='get-all', detail=False, permission_classes=[IsAuthenticated], 
            renderer_classes=[renderers.JSONRenderer])
    def get_all(self, request):
        service_responses = ServiceResponse.objects.all().order_by("-create_date")
        serializer = ServiceResponseShortSerializer(service_responses, many=True)
        return Response({'service_responses': serializer.data}, status=status.HTTP_200_OK)
    

    