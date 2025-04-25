from rest_framework import serializers
from workout.models.training_plan import TrainingPlan
from workout.serializers.exercise import ExerciseSerializer
from workout.models.exercise import Exercise


class TrainingPlanSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    exercises = ExerciseSerializer(many=True)
    id = serializers.IntegerField()
    
    class Meta:
        model = TrainingPlan
        fields = [
            'id', 
            'customer',
            'overview',
            'note',
            'estimated_duration',
            'exercises',
            ]
    
    def get_customer(self, obj):
        from user_profile.serializers.user_profile import CustomerProfileShortSerializer
        return CustomerProfileShortSerializer(obj.customer, context=self.context).data

    

class EditTrainingPlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TrainingPlan
        fields = [
            'id', 
            'customer',
            'overview',
            'note',
            'estimated_duration',
            'exercises',
            ]
        
    def create(self, validated_data):
        exercises_ids = validated_data.pop('exercises', [])
        
        training_plan = TrainingPlan.objects.create(**validated_data)

        training_plan.exercises.set(exercises_ids)
        return training_plan

    def update(self, instance, validated_data):
        exercises_ids = validated_data.pop('exercises', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        instance.exercises.set(exercises_ids)
        return instance