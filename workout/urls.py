from django.urls import path, include
from rest_framework import routers
from .views.workout_schedule import WorkoutScheduleViewSet
from .views.exercise import ExerciseViewSet
from .views.training_plan import TrainingPlanViewSet
from .views.category import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'workout-schedules', WorkoutScheduleViewSet, basename='workout-schedules')
router.register(r'exercises', ExerciseViewSet, basename='exercises')
router.register(r'training-plans', TrainingPlanViewSet, basename='training-plans')
router.register(r'categories', CategoryViewSet, basename='categories')

app_name = "workout"
urlpatterns = [
    path('api/v1/', include(router.urls)),
]
