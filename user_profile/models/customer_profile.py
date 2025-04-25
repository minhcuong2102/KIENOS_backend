from django.db import models
from user.models.user import User
from workout.models.workout_goal import WorkoutGoal


class CustomerProfile(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    gender = models.IntegerField()
    birthday = models.DateField()
    
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    body_fat = models.FloatField(null=True, blank=True)

    health_condition = models.TextField(null=True, blank=True)
    workout_goal = models.OneToOneField(WorkoutGoal, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'customer_profile'

