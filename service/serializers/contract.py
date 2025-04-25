from rest_framework import serializers
from .service import PTServiceSerializer, NonPTServiceSerializer
from ..models.contract import Contract

class ContractSerializer(serializers.ModelSerializer):
    ptservice = PTServiceSerializer()
    nonptservice = NonPTServiceSerializer()
    customer = serializers.SerializerMethodField('get_customer')

    class Meta:

        model = Contract
        fields = [
            'id',
            'ptservice',
            'nonptservice',
            'start_date',
            'expire_date',
            'customer',
            'coach',
            'is_purchased',
            'used_sessions',
            'number_of_session',
            
            ]  

    def get_customer(self, obj):
        from user_profile.serializers.user_profile import CustomerProfileSerializer
        return CustomerProfileSerializer(obj.customer, context=self.context).data
    

class ContractShortSerializer(serializers.ModelSerializer):
    ptservice = PTServiceSerializer()
    nonptservice = NonPTServiceSerializer()
    coach = serializers.SerializerMethodField('get_coach')

    class Meta:
        model = Contract
        fields = [
            'id',
            'ptservice',
            'nonptservice',
            'start_date',
            'expire_date',
            'coach',
            'is_purchased',
            'used_sessions',
            'number_of_session',
        ]

    def get_coach(self, obj):
        from user_profile.serializers.user_profile import CoachProfileShortSerializer
        return CoachProfileShortSerializer(obj.coach, context=self.context).data
    

class ContractCustomSerializer(serializers.ModelSerializer):
    ptservice = PTServiceSerializer()
    nonptservice = NonPTServiceSerializer()
    
    class Meta:
        model = Contract
        fields = [
            'id',
            'ptservice',
            'nonptservice',
            'start_date',
            'expire_date',
            'coach',
            'is_purchased',
            'used_sessions',
            'number_of_session',
        ]

    
