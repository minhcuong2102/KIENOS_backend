from rest_framework import serializers
from user_profile.models.coach_profile import CoachProfile
from user_profile.models.customer_profile import CustomerProfile
from workout.serializers.workout_goal import WorkoutGoalSerializer
from service.serializers.service import PTServiceSerializer, NonPTServiceSerializer
from datetime import datetime
from workout.models.workout_goal import WorkoutGoal
from service.serializers.service import PTServiceSerializer
from service.serializers.contract import ContractSerializer, ContractShortSerializer, ContractCustomSerializer
from service.models.service_response import ServiceResponse
from django.utils import timezone
from django.db.models import F


class CustomerBriefSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'first_name',
            'last_name',
            'address',
            'gender',
            'birthday',
            'height',
            'weight',
            'body_fat',
            'muscle_mass',
            'avatar',
            'email',
            'phone',
            'health_condition',
        ]

    def get_avatar(self, obj):
        return obj.customer.avatar_url.url if obj.customer.avatar_url else None
    
    def get_email(self, obj):
        return obj.customer.email if obj.customer else None
    
    def get_phone(self, obj):
        return obj.customer.phone if obj.customer else None


class CoachProfileSerializer(serializers.ModelSerializer):
    coach_user_id = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    coach_contracts = ContractSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    class Meta:
        model = CoachProfile
        fields = [ 'id',
                  'coach_user_id',
                  'avatar',
                  'average_rating',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'height', 
                  'weight',
                  'start_date',
                  'coach_contracts',
                  'email',
                  'phone',
                  'experiences',
                  ]  
    
    def get_coach_user_id(self, obj):
        return obj.coach.id if obj.coach else None
    
    def get_avatar(self, obj):
        return obj.coach.avatar_url.url if obj.coach.avatar_url else None
    
    def get_email(self, obj):
        return obj.coach.email if obj.coach.email else None
    
    def get_phone(self, obj):
        return obj.coach.phone if obj.coach.phone else None
    
    def get_average_rating(self, obj):
        ratings = ServiceResponse.objects.filter(coach=obj).values_list('score', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings)) 
        return 0 
        
class CustomerProfileSerializer(serializers.ModelSerializer):
    workout_goal = WorkoutGoalSerializer()
    avatar = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    customer_user_id = serializers.SerializerMethodField()
    customer_contracts_pt = serializers.SerializerMethodField()
    customer_contracts_nonpt = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = ['id',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'workout_goal',
                  'height',
                  'weight',
                  'avatar',
                  'phone',
                  'email',
                  'customer_contracts_pt',
                  'customer_contracts_nonpt',
                  'customer_user_id',
                  'health_condition',
                  ]
        
    def get_customer_contracts_pt(self, obj):
        contracts = obj.customer_contracts.filter(
            ptservice__isnull=False, 
        )
        return ContractCustomSerializer(contracts, many=True).data if contracts.exists() else None
    
    def get_customer_contracts_nonpt(self, obj):
        contracts = obj.customer_contracts.filter(
            nonptservice__isnull=False,  
        )
        return ContractCustomSerializer(contracts, many=True).data if contracts.exists() else None

    def get_avatar(self, obj):
        return obj.customer.avatar_url.url if obj.customer.avatar_url else None
    
    def get_customer_user_id(self, obj):
        return obj.customer.id if obj.customer.id else None
    
    def get_phone(self, obj):
        return obj.customer.phone if obj.customer else None
    
    def get_email(self, obj):
        return obj.customer.email if obj.customer else None


class CoachProfileShortSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    coach_user_id = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    customer_ratings = serializers.SerializerMethodField()
    
    class Meta:
        model = CoachProfile
        fields = [ 'id',
                  'avatar',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'height', 
                  'weight',
                  'start_date',       
                  'coach_user_id',       
                  'experiences',    
                  'average_rating',
                  'customer_ratings',
                  ]  
    
    def get_avatar(self, obj):
        return obj.coach.avatar_url.url if obj.coach.avatar_url else None
    
    def get_coach_user_id(self, obj):
        return obj.coach.id if obj.coach else None
    
    def get_average_rating(self, obj):
        ratings = ServiceResponse.objects.filter(coach=obj).values_list('score', flat=True)
        if ratings:
            return round(sum(ratings) / len(ratings)) 
        return 0 

    def get_customer_ratings(self, obj):
        if obj.ratings is not None and obj.ratings.exists():
            from service.serializers.service_response import ServiceResponseShortSerializer
            serializer = ServiceResponseShortSerializer(obj.ratings.all(), many=True, context=self.context)
            return serializer.data
        return None
    
        

class CustomerProfileShortSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()  
    workout_goal = WorkoutGoalSerializer()
    customer_user_id = serializers.SerializerMethodField()
    used_sessions = serializers.SerializerMethodField()
    total_sessions = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = [
                  'id',
                  'customer_user_id',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'avatar',
                  'customer',
                  'height',
                  'weight',
                  'body_fat',
                  'workout_goal',
                  'health_condition',
                  'used_sessions',
                  'total_sessions',
                  ]  
        
    def get_avatar(self, obj):
        return obj.customer.avatar_url.url if obj.customer.avatar_url else None
    
    def get_customer_user_id(self, obj):
        return obj.customer.id if obj.customer.id else None
    
    def get_used_sessions(self, obj):
        active_contract = obj.customer_contracts.filter(
            customer=obj,
            ptservice__isnull=False,
            # used_sessions__lt=F('number_of_session'),
            is_purchased=True,
            expire_date__gt=timezone.now().date(),
        ).first()

        return active_contract.used_sessions if active_contract else None
    
    def get_total_sessions(self, obj):
        active_contract = obj.customer_contracts.filter(
            customer=obj,
            ptservice__isnull=False,
            # used_sessions__lt=F('number_of_session'),
            is_purchased=True,
            expire_date__gt=timezone.now().date(),
        ).first()

        return active_contract.number_of_session if active_contract else None

class CustomerProfileShowSerializer(serializers.ModelSerializer):
    workout_goal = WorkoutGoalSerializer()
    avatar = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    customer_contracts = ContractShortSerializer(many=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'workout_goal',
                  'height',
                  'weight',
                  'avatar',
                  'phone',
                  'email',
                  'health_condition',
                  'customer_contracts',
                  ]
        
    def get_avatar(self, obj):
        return obj.customer.avatar_url.url if obj.customer.avatar_url else None
    
    def get_phone(self, obj):
        return obj.customer.phone if obj.customer else None
    
    def get_email(self, obj):
        return obj.customer.email if obj.customer else None


class CreateCustomerProfileSerializer(serializers.ModelSerializer):
    workout_goal = WorkoutGoalSerializer()

    class Meta:
        model = CustomerProfile
        fields = [
                  'customer',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'height',
                  'weight',
                  'muscle_mass',
                  'body_fat',
                  'workout_goal',
                  'health_condition',
                  ]  
        
    def create(self, validated_data):
        workout_goal_data = validated_data.pop('workout_goal', None)
        customer_profile = CustomerProfile.objects.create(**validated_data)
        
        if workout_goal_data:
            workout_goal = WorkoutGoal.objects.create(**workout_goal_data)
            customer_profile.workout_goal = workout_goal
            customer_profile.save()

        return customer_profile

    def update(self, instance, validated_data):
        workout_goal_data = validated_data.pop('workout_goal', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if workout_goal_data:
            if instance.workout_goal:
                for attr, value in workout_goal_data.items():
                    setattr(instance.workout_goal, attr, value)
                instance.workout_goal.save()
            else:
                workout_goal = WorkoutGoal.objects.create(**workout_goal_data)
                instance.workout_goal = workout_goal
        
        instance.save()
        return instance
    

class CreateCoachProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachProfile
        fields = [
                  'coach',
                  'first_name', 
                  'last_name', 
                  'address', 
                  'gender', 
                  'birthday', 
                  'height', 
                  'weight',
                  'start_date',
                  'experiences',
                  ]  
    def validate_birthday(self, value):
        if isinstance(value, datetime):  
            return value.date()
        return value
    