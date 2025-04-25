from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Contract
from ..serializers.contract import ContractCustomSerializer, ContractShortSerializer
from base.utils.custom_pagination import CustomPaginationSR
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsAdmin, IsCustomer, IsCoach, IsSale

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all().order_by('id')
    pagination_class = CustomPaginationSR
    permission_classes = [IsAuthenticated]
    serializer_class = ContractCustomSerializer
    

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractShortSerializer
        return ContractCustomSerializer  
    
    @action(detail=True, url_path='update-contract', methods=['patch', 'put'], permission_classes=[IsAuthenticated])
    def update_contract(self, request, pk=None):
        contract = Contract.objects.get(pk=pk)
        if not contract:
            return Response({'message': 'No contract with this key found!'})
        
        serializer = ContractCustomSerializer(contract, data=request.data, partial=(request.method == 'PATCH'))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    