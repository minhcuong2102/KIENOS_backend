from rest_framework import serializers
from workout.models.workout_goal import WorkoutGoal

class WorkoutGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutGoal
        fields = [
            'general',
            'weight',
            'body_fat',
            'muscle_mass',
        ]
