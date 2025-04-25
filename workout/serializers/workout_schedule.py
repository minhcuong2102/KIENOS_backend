from rest_framework import serializers
from workout.models.workout_schedule import WorkoutSchedule
from workout.serializers.training_plan import TrainingPlanSerializer
from workout.models.training_plan import TrainingPlan

class WorkoutScheduleSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    training_plan = TrainingPlanSerializer()

    class Meta:
        model = WorkoutSchedule
        fields = [
            'id', 
            'customer',
            'coach',
            'attendance',
            'completed',
            'start_time',
            'end_time',
            'training_plan',
            
            ]
    
    def get_customer(self, obj):
        from user_profile.serializers.user_profile import CustomerProfileShortSerializer
        return CustomerProfileShortSerializer(obj.customer, context=self.context).data

    

class EditWorkoutScheduleSerializer(serializers.ModelSerializer):
    training_plan = TrainingPlanSerializer()

    class Meta:
        model = WorkoutSchedule
        fields = [
            'id', 
            'customer',
            'coach',
            'attendance',
            'completed',
            'start_time',
            'end_time',
            'training_plan',
            
            ]
    

    def validate_training_plan(self, value):
        print("AAAAA", value)
        return value
    

class CustomWorkoutScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutSchedule
        fields = [
            'id', 
            'customer',
            'coach',
            'attendance',
            'completed',
            'start_time',
            'end_time',
            
            ]