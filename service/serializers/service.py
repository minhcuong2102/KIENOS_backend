from rest_framework import serializers
from ..models.service_response import ServiceResponse
from ..models.service import PTService, NonPTService


class PTServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTService
        fields = '__all__'  
        
class NonPTServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonPTService
        fields = '__all__'  
        