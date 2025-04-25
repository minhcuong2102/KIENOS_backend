from rest_framework import serializers
from workout.models.exercise import Exercise
from workout.serializers.category import CategorySerializer


class ExerciseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    image_url = serializers.SerializerMethodField()
    id = serializers.IntegerField()
    
    class Meta:
        model = Exercise
        fields = [
            'id',
            'name',
            'duration',
            'repetitions',
            'image_url',
            'rest_period',
            'categories',
            'embedded_video_url',
        ]

    def get_image_url(self, obj):
        return obj.image_url.url if obj.image_url else None
    

class EditExerciseSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    
    class Meta:
        model = Exercise
        fields = [
            'name',
            'duration',
            'repetitions',
            'image_url',
            'rest_period',
            'embedded_video_url',
            # 'categories',
        ]
