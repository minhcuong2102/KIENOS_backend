from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from service.models.contract import Contract
from user_profile.models.customer_profile import CustomerProfile
from base.permissions import IsCoachOrCustomer, IsCoach
from rest_framework.response import Response
from rest_framework import status
from workout.models.category import Category
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from ..serializers.category import CategorySerializer

from base.permissions import IsAdmin


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    permission_classes = [IsCoachOrCustomer | IsAdmin]
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        if self.action == 'create':
            return CategorySerializer
        if self.action in ['update', 'partial_update']:
            return CategorySerializer
        return CategorySerializer 
    