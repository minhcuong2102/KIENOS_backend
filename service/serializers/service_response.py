from rest_framework import serializers
from ..models.service_response import ServiceResponse
from user_profile.serializers.user_profile import CustomerProfileSerializer, CoachProfileSerializer
import pytz

class ServiceResponseSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer()
    coach = CoachProfileSerializer()
    create_date = serializers.SerializerMethodField()

    class Meta:
        model = ServiceResponse
        fields = [
            'id',  
            'responded', 
            'comment', 
            'create_date', 
            'score', 
            'customer', 
            'coach',
        ]
        
    def get_create_date(self, obj):
        vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        localized_time = obj.create_date.astimezone(vn_timezone)
        return localized_time.strftime('%H:%M %d/%m/%Y')

class ServiceResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceResponse
        fields = [
            'comment', 
            'score', 
            'customer', 
            'coach'
            ]
        
class ServiceResponseShortSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_avatar = serializers.SerializerMethodField()

    class Meta:
        model = ServiceResponse
        fields = [
            'id',
            'customer_name',
            'customer_avatar',
            'comment', 
            'score', 
            'coach',
            'create_date', 
            
        ]

    def get_customer_name(self, obj):
        if obj.customer:
            return obj.customer.first_name + " " + obj.customer.last_name 
        return None

    def get_customer_avatar(self, obj):
        if obj.customer and obj.customer.customer.avatar_url:
            # return obj.customer.customer.avatar_url.url
            return obj.customer.customer.avatar_url
        return None
