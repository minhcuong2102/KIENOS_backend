from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from user_profile.models.customer_profile import CustomerProfile
from user_profile.serializers.user_profile import CustomerProfileSerializer, CustomerProfileShowSerializer
from ..models.service import PTService, NonPTService
from ..serializers.service import PTServiceSerializer, NonPTServiceSerializer
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.permissions import (
    IsAdmin, 
    IsCoach, 
    IsCustomer, 
    IsSale,
)

class PTServiceViewSet(viewsets.ModelViewSet):
    queryset = PTService.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    serializer_class = PTServiceSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PTServiceSerializer
        return PTServiceSerializer  
    
    @action(methods=['get'], url_path='customers', detail=False, permission_classes=[IsAdmin | IsSale], 
        renderer_classes=[renderers.JSONRenderer])
    def customers(self, request):
        pt_service_name = request.query_params.get('pt_service')
        
        queryset = CustomerProfile.objects.all()
    
        if pt_service_name:
            queryset = queryset.filter(customer_contracts__ptservice__id=pt_service_name)
        else:
            queryset = queryset.filter(customer_contracts__ptservice__isnull=False).distinct()


        serializer = CustomerProfileShowSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], url_path='all', detail=False, permission_classes=[IsAdmin | IsSale], 
            renderer_classes=[renderers.JSONRenderer])
    def all(self, request):
        queryset = PTService.objects.all().values('id', 'name')
        if queryset: 
            return Response(queryset, status=status.HTTP_200_OK)
        return Response({'error': 'Not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=False, url_path='delete-multiple', permission_classes=[IsAdmin])
    def delete_multiple(self, request):
        ptservice_ids = request.data.get('ids', [])
        if not ptservice_ids:
            return Response({'error': 'No ID(s) found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        ptservices = PTService.objects.filter(id__in=ptservice_ids)
        
        if not ptservices.exists():
            return Response({'error': 'Can not found ptservice(s) with provided ID(s)!'}, status=status.HTTP_404_NOT_FOUND)
        
        deleted_count, _ = ptservices.delete()
        
        return Response({'message': f'Deleted {deleted_count} ptservice(s) successfully!'}, status=status.HTTP_200_OK)
    
class NonPTServiceViewSet(viewsets.ModelViewSet):
    queryset = NonPTService.objects.all().order_by('id')
    permission_classes = [IsAdmin]
    serializer_class = NonPTServiceSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return NonPTServiceSerializer
        return NonPTServiceSerializer  

    @action(methods=['get'], url_path='customers', detail=False, permission_classes=[IsAdmin | IsSale], 
        renderer_classes=[renderers.JSONRenderer])
    def customers(self, request):
        non_pt_service_name = request.query_params.get('nonpt_service')
        
        queryset = CustomerProfile.objects.all()
    
        if non_pt_service_name:
            queryset = queryset.filter(customer_contracts__nonptservice__id=non_pt_service_name)
        else:
            queryset = queryset.filter(customer_contracts__nonptservice__isnull=False).distinct()

        serializer = CustomerProfileShowSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], url_path='all', detail=False, permission_classes=[IsAdmin | IsSale], 
            renderer_classes=[renderers.JSONRenderer])
    def all(self, request):
        queryset = NonPTService.objects.all().values('id', 'name')
        if queryset: 
            return Response(queryset, status=status.HTTP_200_OK)
        return Response({'error': 'Not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=False, url_path='delete-multiple', permission_classes=[IsAdmin])
    def delete_multiple(self, request):
        nonptservice_ids = request.data.get('ids', [])
        if not nonptservice_ids:
            return Response({'error': 'No ID(s) found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        nonptservices = NonPTService.objects.filter(id__in=nonptservice_ids)
        
        if not nonptservices.exists():
            return Response({'error': 'Can not found nonptservice(s) with provided ID(s)!'}, status=status.HTTP_404_NOT_FOUND)
        
        deleted_count, _ = nonptservices.delete()
        
        return Response({'message': f'Deleted {deleted_count} nonptservice(s) successfully!'}, status=status.HTTP_200_OK)