from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.permissions import IsCoachOrCustomer, IsCoach
from rest_framework.response import Response
from rest_framework import status
from workout.models.exercise import Exercise
from base.utils.custom_pagination import CustomPagination
from rest_framework.decorators import action
from user.models.user import User
from ..serializers.exercise import ExerciseSerializer, EditExerciseSerializer
from base.permissions import IsAdmin, IsCoach, IsCustomer

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('id')    
    permission_classes = [IsCoach | IsCustomer | IsAdmin]
    # serializer_class = WorkoutScheduleSerializer
    # pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ExerciseSerializer
        if self.action == 'create':
            return EditExerciseSerializer
        if self.action in ['update', 'partial_update']:
            return EditExerciseSerializer
        return ExerciseSerializer 
    
    def create(self, request, *args, **kwargs):

        exercise_data = {
            'duration': request.data.get('duration'),
            'name': request.data.get('name'),
            'repetitions': request.data.get('repetitions'),
            'image_url': request.data.get('image_url'),
            'rest_period': request.data.get('rest_period'),
            'embedded_video_url': request.data.get('embedded_video_url'),
        }

        categories = request.data.get('categories')

        if isinstance(categories, str):
            categories = [int(cat_id.strip()) for cat_id in categories.split(',') if cat_id.strip().isdigit()]

        serializer = EditExerciseSerializer(data=exercise_data)
        
        if serializer.is_valid():
            exercise = serializer.save() 
            
            if categories:
                exercise.categories.set(categories)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) 
        exercise = self.get_object()
        
        exercise_data = {
            'duration': request.data.get('duration'),
            'name': request.data.get('name'),
            'repetitions': request.data.get('repetitions'),
            'rest_period': request.data.get('rest_period'),
            'embedded_video_url': request.data.get('embedded_video_url'),
        }
        categories = request.data.get('categories')

        if isinstance(categories, str):
            categories = [int(cat_id.strip()) for cat_id in categories.split(',') if cat_id.strip().isdigit()]

        if 'image_url' in request.data and isinstance(request.data['image_url'], str) and request.data['image_url'].startswith('http'):
            exercise_data['image_url'] = exercise.image_url if exercise.image_url else None
        else:
            exercise_data['image_url'] = request.data.get('image_url')
        
        
        serializer = EditExerciseSerializer(exercise, data=exercise_data, partial=partial)
        
        if serializer.is_valid():
            exercise = serializer.save()

            if categories:
                exercise.categories.set(categories) 
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @action(methods=['get'], url_path='get-by-categories', detail=False, permission_classes=[IsCoach | IsCustomer | IsAdmin], 
            renderer_classes=[renderers.JSONRenderer])  
    def get_by_categories(self, request):
        category_names = request.query_params.getlist('category-name')
        print(category_names)
        exercises = Exercise.objects.filter(categories__name__in=category_names).distinct()
        serializer = ExerciseSerializer(exercises, many=True)
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'No exercises found with these categories!'}, status=status.HTTP_404_NOT_FOUND)
    

    @action(methods=['put', 'patch'], detail=True, permission_classes=[IsCoach | IsAdmin])
    def update_fields(self, request, pk=None):
        exercise = self.get_object()
        serializer = ExerciseSerializer(exercise, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='delete-multiple', permission_classes=[IsCoach | IsAdmin])
    def delete_multiple(self, request):
        e_ids = request.data.get('ids', [])
        if not e_ids:
            return Response({'error': 'No ID(s) found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        es = Exercise.objects.filter(id__in=e_ids)
        
        if not es.exists():
            return Response({'error': 'Can not found exercise(s) with provided ID(s)!'}, status=status.HTTP_404_NOT_FOUND)
        
        deleted_count, _ = es.delete()
        
        return Response({'message': f'Deleted {deleted_count} exercise(s) successfully!'}, status=status.HTTP_200_OK)